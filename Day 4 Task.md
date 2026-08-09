# Day 4 Task — BillBhasha AI: Add Memory Across Conversations

## Goal
Make BillBhasha AI remember useful user preferences and short context across conversations, without storing sensitive financial data permanently.

This is the Day 4 upgrade for the voice assistant demo.

---

## What we want to demonstrate

### Conversation 1
User:
> "Hi BillBhasha, I prefer speaking in Hindi."

Agent should remember this preference.

### Conversation 2 / later session
User:
> "Hello again."

Agent should respond like:
> "नमस्ते! Welcome back. मैं आपसे हिंदी में बात करूँगा।"

Then if the user asks:
> "Mere bill me convenience fee kya hai?"

Agent should explain it in Hindi.

---

## Best memory approach for this project
Use a lightweight, safe memory layer:

- Store short preferences like:
  - preferred language
  - preferred style (Hindi, Hinglish, English)
  - business context (shop owner, invoice checker, customer)
- Store short conversation context like:
  - "user usually checks shop invoices"
  - "user wants explanations in simple language"
- Do not store:
  - bill values
  - card numbers
  - bank account details
  - personal identity documents
  - full sensitive financial records

The simplest and safest version is a JSON file stored locally in the backend folder.

---

## Exact implementation plan

### 1) Update the system prompt
Add a memory section so the agent knows how to use stored context.

Add this to the prompt under the existing LANGUAGE section:

```text
# MEMORY
- Remember useful user preferences and short context across conversations.
- Examples of good memory:
  - preferred language (Hindi, Hinglish, English)
  - business context (shop owner, invoice checker, customer)
  - preference for simple explanations
- Do not store sensitive financial information such as card numbers, bank details, or full bill values.
- If the user says they prefer Hindi, remember it and use it in future replies.
- If the user mentions a recurring context, use it naturally in later conversations.
```

Also add the multilingual instruction explicitly:

```text
LANGUAGE & SCRIPT
- Always write every language in its own native script.
- Hindi → Devanagari (नमस्ते), never romanized.
- English → English.
- If the user speaks Hindi, respond in Hindi script.
- If the user speaks Hinglish, naturally follow the user's language preference while using the correct script.
```

---

### 2) Add a small local memory store
Create a simple JSON file such as:

```text
backend/src/user_memory.json
```

Example content:

```json
{
  "preferences": {
    "language": "Hindi"
  },
  "context": [
    "user often checks shop invoices"
  ]
}
```

---

### 3) Add memory helpers in the agent file
Update [backend/src/agent.py](backend/src/agent.py) with:

```python
import json
from pathlib import Path
```

Then add:

```python
MEMORY_PATH = Path(__file__).with_name("user_memory.json")


def load_memory() -> dict:
    if MEMORY_PATH.exists():
        with MEMORY_PATH.open("r", encoding="utf-8") as f:
            return json.load(f)
    return {"preferences": {}, "context": []}


def save_memory(memory: dict) -> None:
    with MEMORY_PATH.open("w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2, ensure_ascii=False)
```

Then in the Assistant class add methods like:

```python
class Assistant(Agent):
    def __init__(self) -> None:
        self.memory = load_memory()
        super().__init__(instructions=self._build_instructions())

    def _build_instructions(self) -> str:
        memory_summary = ""
        prefs = self.memory.get("preferences", {})
        context = self.memory.get("context", [])

        if prefs:
            memory_summary += "\n# USER MEMORY\n"
            for key, value in prefs.items():
                memory_summary += f"- {key}: {value}\n"

        if context:
            memory_summary += "- context: " + "; ".join(context) + "\n"

        if memory_summary:
            return SYSTEM_PROMPT + memory_summary + "\nUse this information only for personalization and context."
        return SYSTEM_PROMPT

    def remember_preference(self, key: str, value: str) -> None:
        self.memory.setdefault("preferences", {})
        self.memory["preferences"][key] = value
        save_memory(self.memory)

    def remember_context(self, note: str) -> None:
        self.memory.setdefault("context", [])
        if note not in self.memory["context"]:
            self.memory["context"].append(note)
        if len(self.memory["context"]) > 3:
            self.memory["context"] = self.memory["context"][-3:]
        save_memory(self.memory)
```

---

### 4) Make the agent actually update memory from user input
For a demo-friendly version, add a simple rule-based memory update before the agent responds.

Example logic:

```python
def update_memory_from_user_message(self, user_input: str) -> None:
    text = user_input.lower()

    if "prefer speaking in hindi" in text or "hindi me baat" in text:
        self.remember_preference("language", "Hindi")

    if "shop" in text and "invoice" in text:
        self.remember_context("user often checks shop invoices")

    if "simple language" in text or "easy explanation" in text:
        self.remember_preference("explanation_style", "simple")
```

Then call this at the start of the assistant turn, before the response is generated.

> For the first version, this can be a lightweight rule-based memory layer. That is perfect for the demo and easy to build.

---

### 5) Add a short test
Create a new test in [backend/tests/test_agent.py](backend/tests/test_agent.py) to verify the assistant can acknowledge a remembered preference.

Example idea:

```python
def test_remembers_language_preference():
    assistant = Assistant()
    assistant.update_memory_from_user_message("I prefer speaking in Hindi")
    assert assistant.memory["preferences"]["language"] == "Hindi"
```

This is a simple unit-style test and good for validating the memory logic.

---

## Demo script (1–2 minutes)

### Demo flow
1. Start the backend agent.
2. Say:
   > "Hi BillBhasha, I prefer speaking in Hindi."
3. The agent should acknowledge it.
4. End the session or restart the agent.
5. Say:
   > "Hello again."
6. The agent should reply in a way that shows it remembers the preference.
7. Then ask:
   > "Mere bill me convenience fee kya hai?"
8. The agent should explain it in Hindi.

### Suggested demo response

User:
> "Hi BillBhasha, I prefer speaking in Hindi."

Agent:
> "ज़रूर! मैं आपकी पसंद के अनुसार हिंदी में बात करूँगा।"

User:
> "Hello again."

Agent:
> "नमस्ते! Welcome back. मैं आपसे हिंदी में बात करूँगा।"

User:
> "Mere bill me convenience fee kya hai?"

Agent:
> "Convenience fee ek extra charge hota hai jo service ko easy aur fast banana ke liye lagaya jata hai. Yeh usually payment processing ya booking ke liye diya jata hai."

---

## What success looks like
The Day 4 task is complete when:

- the agent remembers a user preference like Hindi
- the agent uses that preference in a later conversation
- the response is naturally multilingual
- the agent does not store sensitive financial data such as card or account numbers

---

## LinkedIn post draft

Here is a ready-to-post LinkedIn version:

```text
Day 4 of building BillBhasha AI is live: memory across conversations. 🧠🧾

Today I focused on making the agent remember useful preferences like preferred language and short context, so it can feel more personal without storing sensitive financial data permanently.

Example:
- User: “I prefer speaking in Hindi.”
- Later: the agent responds naturally in Hindi and continues the conversation more personally.

This is a small but meaningful step toward making voice AI feel more human, helpful, and trustworthy in everyday billing conversations.

#AI #VoiceAI #LLM #StartupBuilding #ProductDemo #BillBhashaAI
```

---

## Suggested implementation order
1. Update prompt with memory rules
2. Add JSON memory file and helper functions
3. Add simple preference/context update logic
4. Test the memory flow locally
5. Record the demo and share it

---

## Final note
Keep this version simple and safe. The goal is not full long-term memory. The goal is useful short-term personalization that makes the agent feel smarter and more human.
