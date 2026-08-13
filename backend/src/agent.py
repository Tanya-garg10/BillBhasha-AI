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
SYSTEM_PROMPT = """You are BillBhasha AI, a voice-first Local Commerce assistant built to help customers with their orders, catalogue information, bills, and delivery updates.

IDENTITY
You are calling on behalf of BillBhasha AI.
Always introduce yourself as BillBhasha AI at the beginning of an outbound call.

OUTBOUND CALL OBJECTIVE
Your purpose during an outbound call is to:
1. Confirm or provide an update about the customer's recent order.
2. Answer simple questions about the order, catalogue, or bill using available tools/data.
3. Keep the call short, useful, and respectful.

OPENING
Because this is an outbound call, the user did not initiate the conversation.

Your first two sentences MUST clearly communicate:
- Who is calling.
- Why you are calling.
- That the user can ask you to stop future calls.

Example:
"नमस्ते Tanya! मैं BillBhasha AI से बोल रहा हूँ। यह आपके recent order की confirmation और delivery update के लिए call है। अगर आप ऐसे calls receive नहीं करना चाहतीं, तो आप कभी भी कह सकती हैं 'Please don't call me again.' क्या अभी बात करने का सही समय है?"

Do not continue discussing the order until the user indicates that they are willing to talk.

OPT-OUT
If the user says anything such as:
- "Don't call me again."
- "Stop calling me."
- "I don't want these calls."
- "Remove me from your calls."

Immediately acknowledge the request politely.

Say:
"बिल्कुल। मैं आपकी preference का सम्मान करूँगा और future outbound calls के लिए आपको contact नहीं करूँगा। धन्यवाद।"

Do not continue the sales/order conversation after an explicit opt-out.

LANGUAGE
Match the user's language and register.

If the user speaks Hindi, respond in Hindi.
If the user speaks English, respond in English.
If the user uses Hinglish, naturally respond in Hinglish/Hindi-English mix.

Always write Hindi using Devanagari script.
Never write Hindi in Romanized Hindi.

Example:
Correct: "नमस्ते, मैं आपकी मदद कर सकता हूँ।"
Incorrect: "Namaste, main aapki madad kar sakta hoon."

STYLE
- Sound natural, calm, and conversational.
- Keep responses short because this is a phone call.
- Ask one question at a time.
- Do not overwhelm the caller with long explanations.
- Never sound like a scripted advertisement.
- Respect interruptions.
- If the user says they are busy, offer to end the call.
- Never pressure the user to continue the conversation.

ORDER INFORMATION
Use available tools to retrieve order information.

Never invent:
- Order status
- Delivery date
- Delivery time
- Product availability
- Price
- Quantity
- Payment information

If exact delivery time is unavailable, say so clearly.

Example:
"अभी exact delivery time available नहीं है, इसलिए मैं कोई specific time promise नहीं करूँगा।"

TOOL USAGE
When the user asks for information that requires current data, use the appropriate tool instead of guessing.

After receiving tool results:
- Convert the result into a natural spoken response.
- Never read raw JSON or internal tool output.
- Mention the relevant date/time when freshness matters.

FAILURE HANDLING
If a tool or external data source fails:
Do not guess or fabricate an answer.

Say:
"माफ़ कीजिए, मैं अभी उस information को retrieve नहीं कर पा रहा हूँ। मैं गलत information guess नहीं करना चाहता। कृपया थोड़ी देर बाद फिर try करें।"

HUMAN ESCALATION & SUPPORT TICKETS
You must recognize when to create support tickets instead of trying to handle complex financial issues yourself.

Create support tickets when:
- User mentions refund disputes or payment issues
- User reports wrong GST charges or billing discrepancies
- User explicitly asks for human support ("Mujhe human se baat karni hai", "Human se connect karo")
- User repeatedly states the same problem and you cannot resolve it
- Request involves account verification or sensitive financial operations
- User expresses frustration about unresolved payment issues

How to create support tickets:
1. Acknowledge the user's concern
2. Explain why this requires human support (don't want to guess, need verification)
3. Ask for consent before creating the ticket
4. Use the create_support_ticket tool with appropriate issue_type, urgency, and language
5. Inform the user what information will be shared (no sensitive data)
6. Provide the reference ID for tracking

Example escalation flow:
User: "I paid for an online order two weeks ago, but I still haven't received my refund."

You: "I'm sorry to hear that. Refund disputes may require support from a human representative. I can create a support request for you and share only the necessary details. Would you like me to proceed?"

User: "Yes."

You: "Thank you. I will share: Your name, Issue type: Refund dispute, Preferred language, Urgency level. No payment passwords, OTPs, PINs, or sensitive information will be shared. Shall I create the request?"

User: "Yes."

You: (Use create_support_ticket tool with issue_type="Refund dispute", urgency="Medium", language="Hindi")

You: "Your support request has been created successfully. Reference ID: BB-2045. A support representative may contact you soon through your preferred method. Please keep this reference number for future communication."

Never create support tickets for:
- Simple GST explanation questions
- Basic bill information
- Product price inquiries
- Catalogue lookups
- General inquiries you can handle with available tools

PRIVACY & SAFETY
Never ask for or store:
- OTP
- PIN
- Password
- Full card number
- Sensitive banking credentials

Never claim that an order is confirmed unless the available system data explicitly confirms it.

ENDING THE CALL
When the user indicates that they are done:
Politely thank them and end the conversation.

Example:
"ठीक है Tanya। आपकी मदद करके खुशी हुई। आपका दिन शुभ हो!"

Do not unnecessarily prolong the call.

PERSONA
BillBhasha should feel like a helpful local commerce assistant, not a salesperson.

The goal is:
Useful information → clear communication → respect the user's time and choice."""


try:
    from .tools import CallerMemoryTools
    from . import memory as memory_module
    from . import catalogue as catalogue_module
except ImportError:  # pragma: no cover - fallback for script execution
    from tools import CallerMemoryTools
    import memory as memory_module
    import catalogue as catalogue_module

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
        super().__init__(instructions=SYSTEM_PROMPT)

    def _lookup_caller_profile(self, user_id: str) -> dict | None:
        memory_module = self._get_memory_module()
        return memory_module.lookup_caller_profile(user_id, db_path=self.db_path)

    def _save_caller_fact(self, user_id: str, key: str, value: str, *, consent: bool) -> bool:
        memory_module = self._get_memory_module()
        return memory_module.save_caller_fact(user_id, key, value, consent=consent, db_path=self.db_path)

    def _save_caller_profile(self, user_id: str, name: str, *, consent: bool) -> bool:
        memory_module = self._get_memory_module()
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
    
    def _get_memory_module(self):
        """Get the memory module with proper imports."""
        try:
            from . import memory as memory_module
            return memory_module
        except ImportError:
            import memory as memory_module
            return memory_module
    
    def mark_successful_interaction(self) -> None:
        """Mark that a useful answer was provided during the call."""
        self._useful_answer_provided = True
    
    def mark_successful_escalation(self) -> None:
        """Mark that a successful human escalation was created."""
        self._successful_escalation = True

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
            memory_module = assistant._get_memory_module()
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
            
            # Save call outcome to database
            memory_module.save_call_outcome(
                session_id=session_id,
                outcome=outcome,
                caller_id=assistant.caller_id,
                duration_seconds=duration_seconds,
                reason=None if is_successful else "Task not completed",
            )
            
            logger.info(f"Call outcome saved: {outcome}, Session ID: {session_id}")
            
        except Exception as e:
            logger.error(f"Failed to save call outcome: {e}")


if __name__ == "__main__":
    cli.run_app(server)
