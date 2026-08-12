"""
Test script for human escalation functionality.
This script tests the escalation tool and notification system.
"""

import asyncio
import os
from dotenv import load_dotenv
from datetime import datetime
from src.human_support import HumanSupportNotifier, EscalationData

async def test_escalation_notification():
    """Test the human support notification system."""
    load_dotenv('.env.local')
    
    print("Testing Human Support Escalation System...")
    print("=" * 60)
    
    # Create notifier
    notifier = HumanSupportNotifier()
    
    # Create test escalation data
    test_escalation = EscalationData(
        timestamp=datetime.now().isoformat(),
        caller_id="test_user_123",
        reason="billing dispute",
        room="test_room_456",
        user_consent=True,
        additional_context="User reports incorrect charge on recent invoice - 500 INR unexpected charge"
    )
    
    print(f"Escalation Data:")
    print(f"  Caller ID: {test_escalation.caller_id}")
    print(f"  Reason: {test_escalation.reason}")
    print(f"  Room: {test_escalation.room}")
    print(f"  User Consent: {test_escalation.user_consent}")
    print(f"  Additional Context: {test_escalation.additional_context}")
    print()
    
    # Send notifications
    print("Sending notifications to configured channels...")
    results = notifier.notify_human_support(test_escalation)
    
    print(f"Notification Results:")
    for channel, success in results.items():
        status = "Success" if success else "Failed"
        print(f"  {channel}: {status}")
    
    print()
    print("=" * 60)
    
    if any(results.values()):
        print("At least one notification channel is working!")
    else:
        print("No notification channels are configured or working.")
        print("Please set up HUMAN_SUPPORT_WEBHOOK_URL, DISCORD_WEBHOOK_URL, or SLACK_WEBHOOK_URL in .env.local")
    
    return any(results.values())

if __name__ == "__main__":
    success = asyncio.run(test_escalation_notification())
    exit(0 if success else 1)