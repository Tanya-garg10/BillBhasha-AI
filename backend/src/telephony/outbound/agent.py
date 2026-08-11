"""
Outbound agent for BillBhasha AI using LiveKit SIP trunking with Linphone.

This script runs the voice agent that will handle outbound calls via SIP.
"""

import logging
import sys
from pathlib import Path

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

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

logger = logging.getLogger("outbound_agent")

load_dotenv(".env.local")

# BillBhasha AI System Prompt for Outbound Calls
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
    from src.tools import CallerMemoryTools
    from src import memory as memory_module
    from src import catalogue as catalogue_module
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
        super().__init__(instructions=SYSTEM_PROMPT)

    def _lookup_caller_profile(self, user_id: str) -> dict | None:
        from memory import lookup_caller_profile as lookup_profile
        return lookup_profile(user_id, db_path=self.db_path)

    def _save_caller_fact(self, user_id: str, key: str, value: str, *, consent: bool) -> bool:
        from memory import save_caller_fact as save_fact
        return save_fact(user_id, key, value, consent=consent, db_path=self.db_path)

    def _save_caller_profile(self, user_id: str, name: str, *, consent: bool) -> bool:
        from memory import save_caller_profile as save_profile
        return save_profile(user_id, name, consent=consent, db_path=self.db_path)

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
                f"Price: INR {product['price']}\n"
                f"Stock: {product['stock']} units\n"
                f"Category: {product['category']}\n"
                f"Last Updated: {product['last_updated']}"
            )
            logger.info(f"Catalogue lookup successful: {product['name']}")
            return result
            
        except Exception as e:
            logger.error(f"Catalogue lookup failed: {e}")
            return "I'm sorry, I couldn't reach the catalogue right now. I don't want to guess the current stock or price. Please try again in a moment."

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
                f"Unit Price: INR {order['unit_price']}\n"
                f"Quantity: {order['quantity']}\n"
                f"Total: INR {order['total']}\n"
                f"Stock Available: {'Yes' if order['stock_available'] else 'No - insufficient stock'}\n"
                f"Last Updated: {order['last_updated']}"
            )
            logger.info(f"Order calculation successful: {order['product']} x {order['quantity']} = INR {order['total']}")
            return result
            
        except Exception as e:
            logger.error(f"Order calculation failed: {e}")
            return "I'm sorry, I couldn't calculate the order total right now. Please try again in a moment."

    def _build_memory_context(self, user_id: str) -> str:
        return self.memory_tools.build_memory_context(user_id)

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


server = AgentServer()


def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()


server.setup_fnc = prewarm


@server.rtc_session(agent_name="my-agent")
async def my_agent(ctx: JobContext):
    # Logging setup
    ctx.log_context_fields = {
        "room": ctx.room.name,
    }

    # Set up a voice AI pipeline using Murf Falcon, Gemini, Deepgram, and the LiveKit turn detector
    session = AgentSession(
        # Speech-to-text (STT) is your agent's ears, turning the user's speech into text that the LLM can understand
        stt=deepgram.STT(model="nova-3", language="multi"),
        # A Large Language Model (LLM) is your agent's brain, processing user input and generating a response
        llm=google.LLM(
                model="gemini-3.5-flash-lite",
            ),
        # Text-to-speech (TTS) is your agent's voice, turning the LLM's text into speech that the user can hear
        tts=murf.TTS(
                voice="Anisha",
                style="Conversation",
                tokenizer=tokenize.basic.SentenceTokenizer(min_sentence_len=2),
                text_pacing=True,
                speed=90,
            ),
        # VAD and turn detection are used to determine when the user is speaking and when the agent should respond
        turn_detection=MultilingualModel(),
        vad=ctx.proc.userdata["vad"],
        # allow the LLM to generate a response while waiting for the end of turn
        preemptive_generation=False,
    )

    # Start the session, which initializes the voice pipeline and warms up the models
    assistant = Assistant()
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

    # Join the room and connect to the user
    await ctx.connect()

    # Keep caller identity for memory lookups and returning-user context.
    participant = await ctx.wait_for_participant()
    assistant.caller_id = participant.identity


if __name__ == "__main__":
    # Run the agent server
    cli.run_app(server)