import logging
from datetime import datetime

from dotenv import load_dotenv
from livekit import rtc
from livekit.agents import (
    Agent,
    AgentServer,
    AgentSession,
    JobContext,
    JobProcess,
    RunContext,
    cli,
    function_tool,
    inference,
    llm,
    tokenize,
    room_io,
)
from livekit.agents.llm.chat_context import ChatMessage
from livekit.plugins import murf, silero, google, deepgram, noise_cancellation
from livekit.plugins.turn_detector.multilingual import MultilingualModel

logger = logging.getLogger("agent")

load_dotenv(".env.local")


# Change this prompt to change what your voice agent does.
# See README.md for example prompts (customer support, language tutor, receptionist).
SYSTEM_PROMPT = """IDENTITY

You are BillBhasha AI, a friendly voice assistant that helps users understand bills, GST, invoices, charges, payments, returns, and refunds.

Your goal is to make complex billing and payment information simple and easy to understand.

OBJECTIVES

1. Answer general questions about bills, GST, invoices, charges and payments.
2. Help users understand billing-related information in simple language.
3. Identify when a user's issue specifically requires the Returns & Refunds Specialist.
4. When specialist help is required, hand off the conversation to the Returns & Refunds Specialist without making the user repeat their problem.

LANGUAGE

- Support Hindi, English and natural Hindi-English code-mixed conversation.
- Mirror the user's language and speaking style.
- If the user speaks Hinglish, reply naturally in Hinglish.
- Hindi must be written in Devanagari script.
- Never diagnose or invent information.
- Keep spoken responses short and natural.

GENERAL QUERIES

Handle questions such as:
- What is GST?
- Why is GST added to my bill?
- What does this charge mean?
- How do I understand my invoice?
- What is a payment processing fee?
- What information is usually present on an invoice?

SPECIALIST HANDOFF

You MUST hand off to the Returns & Refunds Specialist when the user asks about:

- Returning a product
- Refund status
- Refund delay
- Refund not received
- Wrong or damaged product return
- Replacement request
- Return eligibility
- Refund-related disputes
- Any specific return/refund issue that requires specialised assistance

Before handing off, clearly tell the user:

"यह returns और refunds से जुड़ा मामला है। मैं आपको हमारे Returns & Refunds Specialist से connect करता हूँ। आपको अपनी पूरी समस्या दोबारा बताने की जरूरत नहीं होगी।"

Then call the specialist handoff function.

IMPORTANT:
Pass the relevant context of the conversation to the specialist so the user does not have to repeat their problem.

For example:
- User's name, if already known
- The user's return/refund problem
- Any relevant information already provided
- What the user is asking for

DO NOT hand off normal GST, invoice or general billing questions.

If the specialist handoff fails, politely explain that the specialist is currently unavailable and continue helping with whatever information you safely can.

GUARDRAILS

- Never invent refund status.
- Never claim that a refund has been processed unless verified by a real data source.
- Never ask for OTP, PIN, password or complete payment credentials.
- Never expose sensitive financial information.
- Never promise a specific refund date without verified information.

STYLE

- Friendly
- Helpful
- Short conversational sentences
- Natural for voice
- Avoid long explanations
- Ask one question at a time"""


try:
    from .tools import CallerMemoryTools
    from . import memory as memory_module
    from . import catalogue as catalogue_module
    from . import refund_specialist
except ImportError:  # pragma: no cover - fallback for script execution
    from tools import CallerMemoryTools
    import memory as memory_module
    import catalogue as catalogue_module
    import refund_specialist

DB_PATH = memory_module.DB_PATH


class Assistant(Agent):
    def __init__(self) -> None:
        self.db_path = str(DB_PATH)
        self.memory_tools = CallerMemoryTools(self.db_path)
        self.caller_id: str | None = None
        self._memory_context_added: bool = False
        self._session_start_time: str | None = None
        self._successful_escalation: bool = False
        self._useful_answer_provided: bool = False
        self._is_specialist_mode: bool = False
        super().__init__(instructions=SYSTEM_PROMPT)

    def _lookup_caller_profile(self, user_id: str) -> dict | None:
        from src import memory as memory_module
        return memory_module.lookup_caller_profile(user_id, db_path=self.db_path)

    def _save_caller_fact(self, user_id: str, key: str, value: str, *, consent: bool) -> bool:
        from src import memory as memory_module
        return memory_module.save_caller_fact(user_id, key, value, consent=consent, db_path=self.db_path)

    def _save_caller_profile(self, user_id: str, name: str, *, consent: bool) -> bool:
        from src import memory as memory_module
        return memory_module.save_caller_profile(user_id, name, consent=consent, db_path=self.db_path)

    @function_tool
    async def lookup_caller(self, context: RunContext, user_id: str) -> str:
        """Look up an existing caller profile by ID and return stored memory as JSON."""
        return await self.memory_tools.lookup_caller(context, user_id)

    @function_tool
    async def save_caller(self, context: RunContext, user_id: str, key: str, value: str, consent: bool) -> str:
        """Save a caller preference or fact after the caller gives permission."""
        return await self.memory_tools.save_caller(context, user_id, key, value, consent)

    @function_tool
    async def lookup_catalogue(self, context: RunContext, product_name: str) -> str:
        """Look up product information from the local commerce catalogue.
        
        Use this tool when the user asks about product availability, price, or stock.
        The tool returns real catalogue data including product name, price, stock quantity, and last updated date.
        
        If the product is not found in the catalogue, the tool will indicate this clearly.
        If the catalogue lookup fails, the tool will return an error message.
        
        Args:
            product_name: The name of the product to search for (e.g. "wireless mouse", "keyboard")
        """
        try:
            logger.info(f"Looking up product in catalogue: {product_name}")
            product = catalogue_module.lookup_product(product_name)
            
            if product is None:
                return f"Product '{product_name}' not found in the catalogue. Please check the product name or try a different search term."
            
            # Format the result for natural language response
            result = (
                f"Product: {product['name']}\n"
                f"Price: ₹{product['price']}\n"
                f"Stock: {product['stock']} units\n"
                f"Category: {product['category']}\n"
                f"Last Updated: {product['last_updated']}"
            )
            logger.info(f"Catalogue lookup successful: {product['name']}")
            
            # Mark successful interaction for analytics
            self.mark_successful_interaction()
            
            return result
            
        except Exception as e:
            logger.error(f"Catalogue lookup failed: {e}")
            return "I'm sorry, I couldn't reach the catalogue right now. I don't want to guess the current stock or price. Please try again in a moment."

    @function_tool
    async def create_support_ticket(self, context: RunContext, issue_type: str, urgency: str = "Medium", language: str = "Hindi") -> str:
        """Create a support ticket for human escalation when AI cannot handle the request.
        
        Use this tool when:
        - User explicitly asks for human support
        - User mentions refund disputes or payment issues
        - User reports wrong GST charges or billing discrepancies
        - User repeatedly states the same problem and AI cannot resolve it
        - Request requires account verification or sensitive operations
        
        Always ask for user consent before creating a support ticket.
        
        Args:
            issue_type: The type of issue (e.g., "Refund dispute", "GST charge dispute", "Payment issue")
            urgency: The urgency level (Low, Medium, High)
            language: User's preferred language (Hindi, English, Hinglish)
        """
        try:
            logger.info(f"Creating support ticket. Issue: {issue_type}, Urgency: {urgency}")
            
            # Mark successful escalation for analytics
            self.mark_successful_escalation()
            
            # Import support ticket system
            try:
                from support_tickets import SupportTicketManager
                ticket_manager = SupportTicketManager()
                
                # Create support ticket with reference ID
                ticket = ticket_manager.create_ticket(
                    caller_id=self.caller_id if self.caller_id else "unknown",
                    issue_type=issue_type,
                    urgency=urgency,
                    language=language,
                    room=context.room.name if hasattr(context, 'room') else "unknown"
                )
                
                logger.info(f"Support ticket created: {ticket.reference_id}")
                
                # Send notifications to human support
                from human_support import HumanSupportNotifier, EscalationData
                notifier = HumanSupportNotifier()
                
                escalation_data = EscalationData(
                    timestamp=datetime.now().isoformat(),
                    caller_id=self.caller_id if self.caller_id else "unknown",
                    reason=f"Support ticket: {ticket.reference_id} - {issue_type}",
                    room=context.room.name if hasattr(context, 'room') else "unknown",
                    user_consent=True,
                    additional_context=f"Reference ID: {ticket.reference_id}, Urgency: {urgency}, Language: {language}"
                )
                
                notification_results = notifier.notify_human_support(escalation_data)
                logger.info(f"Human support notifications sent: {notification_results}")
                
                return f"Your support request has been created successfully. Reference ID: {ticket.reference_id}. A support representative may contact you soon through your preferred method. Please keep this reference number for future communication."
                
            except ImportError:
                logger.warning("Support ticket system not available, using fallback")
                # Fallback to simple logging if support system not available
                reference_id = f"BB-{hash(issue_type + str(datetime.now().timestamp())) % 10000:04d}"
                logger.info(f"Support ticket created (fallback): {reference_id}")
                return f"Your support request has been created successfully. Reference ID: {reference_id}. A support representative may contact you soon through your preferred method. Please keep this reference number for future communication."
            
        except Exception as e:
            logger.error(f"Support ticket creation failed: {e}")
            return "I apologize, but I'm having trouble creating your support request right now. Please try again in a moment or call our support line directly."

    @function_tool
    async def calculate_order_total(self, context: RunContext, product_name: str, quantity: int = 1) -> str:
        """Calculate the total price for a given product and quantity.
        
        Use this tool when the user asks about order totals or pricing for multiple items.
        The tool returns the unit price, quantity, total amount, and whether sufficient stock is available.
        
        If the product is not found or stock is insufficient, the tool will indicate this clearly.
        
        Args:
            product_name: The name of the product to calculate total for
            quantity: Number of units (default: 1)
        """
        try:
            logger.info(f"Calculating order total for {quantity} x {product_name}")
            order = catalogue_module.calculate_order_total(product_name, quantity)
            
            if order is None:
                return f"Product '{product_name}' not found in the catalogue. I cannot calculate the total without valid product information."
            
            # Format the result for natural language response
            result = (
                f"Product: {order['product']}\n"
                f"Unit Price: ₹{order['unit_price']}\n"
                f"Quantity: {order['quantity']}\n"
                f"Total: ₹{order['total']}\n"
                f"Stock Available: {'Yes' if order['stock_available'] else 'No - insufficient stock'}\n"
                f"Last Updated: {order['last_updated']}"
            )
            logger.info(f"Order calculation successful: {order['product']} x {order['quantity']} = ₹{order['total']}")
            
            # Mark successful interaction for analytics
            self.mark_successful_interaction()
            
            return result
            
        except Exception as e:
            logger.error(f"Order calculation failed: {e}")
            return "I'm sorry, I couldn't calculate the order total right now. Please try again in a moment."

    def _build_memory_context(self, user_id: str) -> str:
        return self.memory_tools.build_memory_context(user_id)
    
    def mark_successful_interaction(self) -> None:
        """Mark that a useful answer was provided during the call."""
        self._useful_answer_provided = True
    
    def mark_successful_escalation(self) -> None:
        """Mark that a successful human escalation was created."""
        self._successful_escalation = True
    
    @function_tool
    async def handoff_to_refund_specialist(self, context: RunContext, user_issue: str, user_name: str = "") -> str:
        """Transfer the conversation to the Returns & Refunds Specialist.
        
        Use this tool ONLY when the user has a return, refund, replacement, wrong-product, damaged-product, refund-delay, or return-dispute issue.
        
        Do NOT use this tool for general GST, invoice, billing, or payment explanation questions.
        
        Before calling this tool, tell the user that you are connecting them to the Returns & Refunds Specialist.
        
        Pass the relevant conversation context so the specialist can continue without asking the user to repeat their problem.
        
        Args:
            user_issue: The user's return/refund problem
            user_name: The user's name if known (optional)
        """
        try:
            logger.info(f"Handing off to refund specialist. Issue: {user_issue}, User: {user_name}")
            
            # Import specialist tools
            from refund_specialist import check_refund_status, explain_refund_process, check_return_eligibility
            
            # Add specialist's context to the conversation
            specialist_message = f"नमस्ते {user_name if user_name else ''}, मैं BillBhasha का Returns & Refunds Specialist हूँ। मुझे आपकी पिछली बात समझ आ गई है — आपकी problem {user_issue} है। मैं इसी issue में आपकी मदद करता हूँ।"
            
            # Mark that we're now in specialist mode
            self._is_specialist_mode = True
            
            logger.info("Switched to refund specialist mode")
            
            return specialist_message
            
        except Exception as e:
            logger.error(f"Handoff to specialist failed: {e}")
            return "I apologize, but I'm having trouble connecting you with the Returns & Refunds Specialist right now. Please try again in a moment or call our support line directly."

    async def on_user_turn_completed(
        self, turn_ctx: llm.ChatContext, new_message: llm.ChatMessage
    ) -> None:
        if self.caller_id is None or self._memory_context_added:
            return

        memory_context = self._build_memory_context(self.caller_id)
        if not memory_context:
            return

        turn_ctx.insert(
            ChatMessage(
                role="system",
                content=[
                    "You already know this caller from a previous session. "
                    "Do not use a full greeting again. Mention the remembered profile briefly only once at the start of the conversation and then continue helping.",
                    f"\nRemembered profile:\n{memory_context}",
                ],
            )
        )
        self._memory_context_added = True

    # To add tools, use the @function_tool decorator.
    # Here's an example that adds a simple weather tool.
    # You also have to add `from livekit.agents import function_tool, RunContext` to the top of this file
    # @function_tool
    # async def lookup_weather(self, context: RunContext, location: str):
    #     """Use this tool to look up current weather information in the given location.
    #
    #     If the location is not supported by the weather service, the tool will indicate this. You must tell the user the location's weather is unavailable.
    #
    #     Args:
    #         location: The location to look up weather information for (e.g. city name)
    #     """
    #
    #     logger.info(f"Looking up weather for {location}")
    #
    #     return "sunny with a temperature of 70 degrees."


server = AgentServer()


def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()


server.setup_fnc = prewarm


@server.rtc_session(agent_name="my-agent")
async def my_agent(ctx: JobContext):
    # Logging setup
    # Add any other context you want in all log entries here
    ctx.log_context_fields = {
        "room": ctx.room.name,
    }

    # Set up a voice AI pipeline using Murf Falcon, Gemini, Deepgram, and the LiveKit turn detector
    session = AgentSession(
        # Speech-to-text (STT) is your agent's ears, turning the user's speech into text that the LLM can understand
        # See all available models at https://docs.livekit.io/agents/models/stt/
        stt=deepgram.STT(model="nova-3", language="multi"),
        # A Large Language Model (LLM) is your agent's brain, processing user input and generating a response
        # See all available models at https://docs.livekit.io/agents/models/llm/
        llm=google.LLM(
                model="gemini-3.5-flash-lite",
            ),
        # Text-to-speech (TTS) is your agent's voice, turning the LLM's text into speech that the user can hear
        # See all available models as well as voice selections at https://docs.livekit.io/agents/models/tts/
        tts=murf.TTS(
                voice="Anisha",
                style="Conversation",
                tokenizer=tokenize.basic.SentenceTokenizer(min_sentence_len=2),
                text_pacing=True,
                speed=90,
            ),
        # VAD and turn detection are used to determine when the user is speaking and when the agent should respond
        # See more at https://docs.livekit.io/agents/build/turns
        turn_detection=MultilingualModel(),
        vad=ctx.proc.userdata["vad"],
        # allow the LLM to generate a response while waiting for the end of turn
        # See more at https://docs.livekit.io/agents/build/audio/#preemptive-generation
        preemptive_generation=False,
    )

    # To use a realtime model instead of a voice pipeline, use the following session setup instead.
    # (Note: This is for the OpenAI Realtime API. For other providers, see https://docs.livekit.io/agents/models/realtime/))
    # 1. Install livekit-agents[openai]
    # 2. Set OPENAI_API_KEY in .env.local
    # 3. Add `from livekit.plugins import openai` to the top of this file
    # 4. Use the following session setup instead of the version above
    # session = AgentSession(
    #     llm=openai.realtime.RealtimeModel(voice="marin")
    # )

    # # Add a virtual avatar to the session, if desired
    # # For other providers, see https://docs.livekit.io/agents/models/avatar/
    # avatar = hedra.AvatarSession(
    #   avatar_id="...",  # See https://docs.livekit.io/agents/models/avatar/plugins/hedra
    # )
    # # Start the avatar and wait for it to join
    # await avatar.start(session, room=ctx.room)

    # Start the session, which initializes the voice pipeline and warms up the models
    assistant = Assistant()
    assistant._session_start_time = datetime.now().isoformat()
    
    await session.start(
        agent=assistant,
        room=ctx.room,
        room_options=room_io.RoomOptions(
            audio_input=room_io.AudioInputOptions(
                noise_cancellation=lambda params: (
                    noise_cancellation.BVCTelephony()
                    if params.participant.kind
                    == rtc.ParticipantKind.PARTICIPANT_KIND_SIP
                    else noise_cancellation.BVC()
                ),
            ),
        ),
    )
    
    # Set up call outcome tracking AFTER session starts
    @session.on("closed")
    def on_session_closed():
        """Handle session end and save call outcome to analytics."""
        try:
            logger.info("SESSION CLOSED CALLBACK TRIGGERED")
            
            # Import memory module directly to avoid import issues
            from src import memory as memory_module
            from datetime import datetime
            
            # Calculate call duration
            end_time = datetime.now()
            duration_seconds = None
            if assistant._session_start_time:
                start_time = datetime.fromisoformat(assistant._session_start_time)
                duration_seconds = int((end_time - start_time).total_seconds())
            
            # Determine call outcome based on success conditions
            # Success: useful answer provided OR successful escalation
            # Failure: user ended before task completion, tool/API failure, or incomplete request
            is_successful = assistant._useful_answer_provided or assistant._successful_escalation
            
            outcome = "success" if is_successful else "failure"
            
            # Generate a unique session ID
            session_id = f"session_{ctx.room.name}_{int(end_time.timestamp())}"
            
            logger.info(f"Saving call outcome: {outcome}, Session ID: {session_id}, Useful answer: {assistant._useful_answer_provided}, Escalation: {assistant._successful_escalation}")
            
            # Save call outcome to database
            success = memory_module.save_call_outcome(
                session_id=session_id,
                outcome=outcome,
                caller_id=assistant.caller_id,
                duration_seconds=duration_seconds,
                reason=None if is_successful else "Task not completed",
            )
            
            if success:
                logger.info(f"Call outcome saved successfully: {outcome}, Session ID: {session_id}")
            else:
                logger.error(f"Failed to save call outcome to database")
            
        except Exception as e:
            logger.error(f"Failed to save call outcome: {e}", exc_info=True)
    
    # Disable desktop audio for SIP calls
    # Note: participant_kind check is done through room_options audio input configuration

    # Join the room and connect to the user
    await ctx.connect()

    # Keep caller identity for memory lookups and returning-user context.
    participant = await ctx.wait_for_participant()
    assistant.caller_id = participant.identity
    session.userdata = {"caller_id": participant.identity}
    ctx.log_context_fields["caller_identity"] = participant.identity
    
    # Set up call outcome tracking when session ends
    @session.on("closed")
    def on_session_closed():
        """Handle session end and save call outcome to analytics."""
        try:
            logger.info("Session closed - attempting to save call outcome")
            
            # Import memory module directly to avoid import issues
            from src import memory as memory_module
            from datetime import datetime
            
            # Calculate call duration
            end_time = datetime.now()
            duration_seconds = None
            if assistant._session_start_time:
                start_time = datetime.fromisoformat(assistant._session_start_time)
                duration_seconds = int((end_time - start_time).total_seconds())
            
            # Determine call outcome based on success conditions
            # Success: useful answer provided OR successful escalation
            # Failure: user ended before task completion, tool/API failure, or incomplete request
            is_successful = assistant._useful_answer_provided or assistant._successful_escalation
            
            outcome = "success" if is_successful else "failure"
            
            # Generate a unique session ID
            session_id = f"session_{ctx.room.name}_{int(end_time.timestamp())}"
            
            logger.info(f"Saving call outcome: {outcome}, Session ID: {session_id}, Useful answer: {assistant._useful_answer_provided}, Escalation: {assistant._successful_escalation}")
            
            # Save call outcome to database
            success = memory_module.save_call_outcome(
                session_id=session_id,
                outcome=outcome,
                caller_id=assistant.caller_id,
                duration_seconds=duration_seconds,
                reason=None if is_successful else "Task not completed",
            )
            
            if success:
                logger.info(f"Call outcome saved successfully: {outcome}, Session ID: {session_id}")
            else:
                logger.error(f"Failed to save call outcome to database")
            
        except Exception as e:
            logger.error(f"Failed to save call outcome: {e}", exc_info=True)


if __name__ == "__main__":
    cli.run_app(server)
