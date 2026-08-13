import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DB_PATH = Path(__file__).with_name("billbhasha.db")


def init_db(db_path: str | Path | None = None) -> Path:
    target = Path(db_path or DB_PATH)
    with sqlite3.connect(target) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS caller_profiles (
                user_id TEXT PRIMARY KEY,
                name TEXT,
                language_preference TEXT,
                facts TEXT,
                last_interaction TEXT
            )
            """
        )
        # Add call analytics table for Day 8
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS call_analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                caller_id TEXT,
                outcome TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                duration_seconds INTEGER,
                reason TEXT
            )
            """
        )
    return target


def lookup_caller_profile(user_id: str, db_path: str | Path | None = None) -> dict[str, Any] | None:
    target = init_db(db_path)
    with sqlite3.connect(target) as conn:
        row = conn.execute(
            "SELECT user_id, name, language_preference, facts, last_interaction FROM caller_profiles WHERE user_id = ?",
            (user_id,),
        ).fetchone()

    if not row:
        return None

    return {
        "user_id": row[0],
        "name": row[1],
        "language_preference": row[2],
        "facts": json.loads(row[3] or "{}"),
        "last_interaction": row[4],
    }


def save_caller_fact(
    user_id: str,
    key: str,
    value: str,
    *,
    consent: bool,
    db_path: str | Path | None = None,
) -> bool:
    if not consent:
        return False

    target = init_db(db_path)
    with sqlite3.connect(target) as conn:
        existing_row = conn.execute(
            "SELECT name, language_preference, facts FROM caller_profiles WHERE user_id = ?",
            (user_id,),
        ).fetchone()

        name = existing_row[0] if existing_row else ""
        language_preference = existing_row[1] if existing_row else ""
        facts = json.loads(existing_row[2] or "{}") if existing_row else {}

        if key == "language_preference":
            language_preference = value
        elif key == "name":
            name = value
            facts[key] = value
        else:
            facts[key] = value

        conn.execute(
            """
            INSERT INTO caller_profiles (user_id, name, language_preference, facts, last_interaction)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                name = excluded.name,
                language_preference = excluded.language_preference,
                facts = excluded.facts,
                last_interaction = excluded.last_interaction
            """,
            (
                user_id,
                name,
                language_preference,
                json.dumps(facts),
                datetime.now(timezone.utc).isoformat(),
            ),
        )

    return True


def save_caller_profile(
    user_id: str,
    name: str,
    *,
    consent: bool,
    db_path: str | Path | None = None,
) -> bool:
    if not consent:
        return False

    target = init_db(db_path)
    with sqlite3.connect(target) as conn:
        conn.execute(
            """
            INSERT INTO caller_profiles (user_id, name, language_preference, facts, last_interaction)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                name = excluded.name,
                last_interaction = excluded.last_interaction
            """,
            (
                user_id,
                name,
                "",
                "{}",
                datetime.now(timezone.utc).isoformat(),
            ),
        )

    return True


def save_call_outcome(
    session_id: str,
    outcome: str,
    caller_id: str | None = None,
    duration_seconds: int | None = None,
    reason: str | None = None,
    db_path: str | Path | None = None,
) -> bool:
    """Save the outcome of a call to the analytics database.
    
    Args:
        session_id: Unique identifier for the call session
        outcome: The call outcome ("success" or "failure")
        caller_id: The caller's identifier (optional)
        duration_seconds: Duration of the call in seconds (optional)
        reason: Reason for failure or additional context (optional)
        db_path: Path to the database file (optional)
        
    Returns:
        True if save was successful, False otherwise
    """
    try:
        target = init_db(db_path)
        with sqlite3.connect(target) as conn:
            conn.execute(
                """
                INSERT INTO call_analytics (session_id, caller_id, outcome, timestamp, duration_seconds, reason)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    session_id,
                    caller_id,
                    outcome,
                    datetime.now(timezone.utc).isoformat(),
                    duration_seconds,
                    reason,
                ),
            )
        return True
    except Exception as e:
        print(f"Error saving call outcome: {e}")
        return False


def get_call_analytics(db_path: str | Path | None = None) -> dict[str, int]:
    """Get call analytics metrics from the database.
    
    Args:
        db_path: Path to the database file (optional)
        
    Returns:
        Dictionary with total_calls, successful_calls, and failed_calls
    """
    try:
        target = init_db(db_path)
        with sqlite3.connect(target) as conn:
            # Get total calls
            total_calls = conn.execute("SELECT COUNT(*) FROM call_analytics").fetchone()[0]
            
            # Get successful calls
            successful_calls = conn.execute(
                "SELECT COUNT(*) FROM call_analytics WHERE outcome = 'success'"
            ).fetchone()[0]
            
            # Get failed calls
            failed_calls = conn.execute(
                "SELECT COUNT(*) FROM call_analytics WHERE outcome = 'failure'"
            ).fetchone()[0]
            
            return {
                "total_calls": total_calls,
                "successful_calls": successful_calls,
                "failed_calls": failed_calls,
            }
    except Exception as e:
        print(f"Error getting call analytics: {e}")
        return {
            "total_calls": 0,
            "successful_calls": 0,
            "failed_calls": 0,
        }
