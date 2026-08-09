import json
from typing import Any

from livekit.agents import RunContext, function_tool

from memory import lookup_caller_profile as lookup_profile, save_caller_fact as save_fact, save_caller_profile as save_profile


class CallerMemoryTools:
    def __init__(self, db_path: str | None = None) -> None:
        self.db_path = db_path

    @function_tool
    async def lookup_caller(self, context: RunContext, user_id: str) -> str:
        """Look up an existing caller profile by ID and return the stored memory as JSON."""
        profile = lookup_profile(user_id, db_path=self.db_path)
        if not profile:
            return "{}"
        return json.dumps(profile)

    @function_tool
    async def save_caller(self, context: RunContext, user_id: str, key: str, value: str, consent: bool) -> str:
        """Save a caller preference or fact after the caller gives permission."""
        if key == "name":
            saved = save_profile(user_id, value, consent=consent, db_path=self.db_path)
        else:
            saved = save_fact(user_id, key, value, consent=consent, db_path=self.db_path)
        return "saved" if saved else "not_saved"

    def build_memory_context(self, user_id: str) -> str:
        profile = lookup_profile(user_id, db_path=self.db_path)
        if not profile:
            return ""

        parts = [f"Caller ID: {profile['user_id']}"]
        if profile.get("name"):
            parts.append(f"Name: {profile['name']}")
        if profile.get("language_preference"):
            parts.append(f"Preferred language: {profile['language_preference']}")

        facts = profile.get("facts", {})
        for key, value in facts.items():
            parts.append(f"{key}: {value}")

        return "\n".join(parts)
