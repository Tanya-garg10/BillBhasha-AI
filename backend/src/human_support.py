"""
Human support notification system for BillBhasha AI.

This module handles notifications to human support when AI escalation is triggered.
Supports multiple notification channels: webhooks, Discord, Slack, etc.
"""

import logging
import os
import json
import requests
from datetime import datetime
from typing import Optional, Dict, Any
from dataclasses import dataclass
from dotenv import load_dotenv

logger = logging.getLogger("human_support")
load_dotenv(".env.local")


@dataclass
class EscalationData:
    """Data structure for human escalation notifications."""
    timestamp: str
    caller_id: str
    reason: str
    room: str
    user_consent: bool
    additional_context: Optional[str] = None


class HumanSupportNotifier:
    """Handles notifications to human support for escalations."""
    
    def __init__(self):
        """Initialize the notifier with configuration from environment variables."""
        self.webhook_url = os.getenv("HUMAN_SUPPORT_WEBHOOK_URL")
        self.discord_webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
        self.slack_webhook_url = os.getenv("SLACK_WEBHOOK_URL")
        
        logger.info("HumanSupportNotifier initialized")
    
    def send_webhook_notification(self, escalation_data: EscalationData) -> bool:
        """Send a webhook notification to the configured webhook URL.
        
        Args:
            escalation_data: The escalation data to send
            
        Returns:
            True if notification was sent successfully, False otherwise
        """
        if not self.webhook_url:
            logger.warning("No webhook URL configured for human support notifications")
            return False
        
        try:
            payload = {
                "timestamp": escalation_data.timestamp,
                "caller_id": escalation_data.caller_id,
                "reason": escalation_data.reason,
                "room": escalation_data.room,
                "user_consent": escalation_data.user_consent,
                "additional_context": escalation_data.additional_context,
                "service": "BillBhasha AI",
                "escalation_type": "human_handoff"
            }
            
            response = requests.post(
                self.webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info(f"Webhook notification sent successfully for escalation: {escalation_data.caller_id}")
                return True
            else:
                logger.error(f"Webhook notification failed with status {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to send webhook notification: {e}")
            return False
    
    def send_discord_notification(self, escalation_data: EscalationData) -> bool:
        """Send a Discord webhook notification for escalation.
        
        Args:
            escalation_data: The escalation data to send
            
        Returns:
            True if notification was sent successfully, False otherwise
        """
        if not self.discord_webhook_url:
            logger.warning("No Discord webhook URL configured")
            return False
        
        try:
            # Create Discord-specific message format
            embed = {
                "title": "🚨 BillBhasha AI - Human Escalation Required",
                "color": 15158332,  # Red color for urgency
                "fields": [
                    {
                        "name": "Caller ID",
                        "value": escalation_data.caller_id,
                        "inline": True
                    },
                    {
                        "name": "Reason",
                        "value": escalation_data.reason,
                        "inline": True
                    },
                    {
                        "name": "Room",
                        "value": escalation_data.room,
                        "inline": True
                    },
                    {
                        "name": "Timestamp",
                        "value": escalation_data.timestamp,
                        "inline": True
                    },
                    {
                        "name": "User Consent",
                        "value": "Yes" if escalation_data.user_consent else "No",
                        "inline": True
                    }
                ],
                "footer": {
                    "text": "BillBhasha AI - Human Support Notification"
                }
            }
            
            if escalation_data.additional_context:
                embed["fields"].append({
                    "name": "Additional Context",
                    "value": escalation_data.additional_context,
                    "inline": False
                })
            
            payload = {
                "embeds": [embed]
            }
            
            response = requests.post(
                self.discord_webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 204:  # Discord returns 204 No Content on success
                logger.info(f"Discord notification sent successfully for escalation: {escalation_data.caller_id}")
                return True
            else:
                logger.error(f"Discord notification failed with status {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to send Discord notification: {e}")
            return False
    
    def send_slack_notification(self, escalation_data: EscalationData) -> bool:
        """Send a Slack webhook notification for escalation.
        
        Args:
            escalation_data: The escalation data to send
            
        Returns:
            True if notification was sent successfully, False otherwise
        """
        if not self.slack_webhook_url:
            logger.warning("No Slack webhook URL configured")
            return False
        
        try:
            # Create Slack-specific message format
            payload = {
                "text": "🚨 BillBhasha AI - Human Escalation Required",
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": "🚨 BillBhasha AI - Human Escalation Required"
                        }
                    },
                    {
                        "type": "section",
                        "fields": [
                            {
                                "type": "mrkdwn",
                                "text": f"*Caller ID:*\n{escalation_data.caller_id}"
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*Reason:*\n{escalation_data.reason}"
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*Room:*\n{escalation_data.room}"
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*Timestamp:*\n{escalation_data.timestamp}"
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*User Consent:*\n{'Yes' if escalation_data.user_consent else 'No'}"
                            }
                        ]
                    }
                ]
            }
            
            if escalation_data.additional_context:
                payload["blocks"].append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Additional Context:*\n{escalation_data.additional_context}"
                    }
                })
            
            response = requests.post(
                self.slack_webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info(f"Slack notification sent successfully for escalation: {escalation_data.caller_id}")
                return True
            else:
                logger.error(f"Slack notification failed with status {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to send Slack notification: {e}")
            return False
    
    def notify_human_support(self, escalation_data: EscalationData) -> Dict[str, bool]:
        """Send notifications to all configured channels.
        
        Args:
            escalation_data: The escalation data to send
            
        Returns:
            Dictionary with channel names as keys and success status as values
        """
        results = {}
        
        # Try webhook notification
        if self.webhook_url:
            results["webhook"] = self.send_webhook_notification(escalation_data)
        
        # Try Discord notification
        if self.discord_webhook_url:
            results["discord"] = self.send_discord_notification(escalation_data)
        
        # Try Slack notification
        if self.slack_webhook_url:
            results["slack"] = self.send_slack_notification(escalation_data)
        
        # Log if no channels are configured
        if not results:
            logger.warning("No notification channels configured for human support")
            results["none"] = False
        
        return results


def create_notifier() -> HumanSupportNotifier:
    """Factory function to create a HumanSupportNotifier instance.
    
    Returns:
        Configured HumanSupportNotifier instance
    """
    return HumanSupportNotifier()


# Example usage (for testing purposes)
if __name__ == "__main__":
    try:
        notifier = create_notifier()
        
        # Test escalation notification
        test_escalation = EscalationData(
            timestamp=datetime.now().isoformat(),
            caller_id="test_user_123",
            reason="billing dispute",
            room="test_room_456",
            user_consent=True,
            additional_context="User reports incorrect charge on recent invoice"
        )
        
        results = notifier.notify_human_support(test_escalation)
        print(f"Notification results: {results}")
        
    except Exception as e:
        print(f"Error: {e}")