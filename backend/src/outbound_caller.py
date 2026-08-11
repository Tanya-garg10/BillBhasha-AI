"""
Outbound calling module for BillBhasha AI using Twilio SIP trunking with LiveKit.

This module handles:
- Creating outbound calls via Twilio
- Connecting calls to LiveKit rooms
- Managing call outcomes (no answer, busy, voicemail, hang-up)
"""

import logging
import os
from typing import Optional
from dataclasses import dataclass
from datetime import datetime
from dotenv import load_dotenv
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

logger = logging.getLogger("outbound_caller")
load_dotenv(".env.local")


@dataclass
class CallOutcome:
    """Represents the outcome of an outbound call attempt."""
    status: str
    timestamp: datetime
    duration_seconds: Optional[int] = None
    error_message: Optional[str] = None


class OutboundCaller:
    """Handles outbound calls using Twilio SIP trunking with LiveKit."""
    
    def __init__(self):
        """Initialize Twilio client with credentials from environment variables."""
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.twilio_number = os.getenv("TWILIO_PHONE_NUMBER")
        self.livekit_url = os.getenv("LIVEKIT_URL")
        
        if not all([self.account_sid, self.auth_token, self.twilio_number]):
            raise ValueError(
                "Missing Twilio credentials. Please set TWILIO_ACCOUNT_SID, "
                "TWILIO_AUTH_TOKEN, and TWILIO_PHONE_NUMBER in .env.local"
            )
        
        self.client = Client(self.account_sid, self.auth_token)
        logger.info("OutboundCaller initialized with Twilio credentials")
    
    def make_outbound_call(
        self,
        phone_number: str,
        room_name: str,
        customer_name: str = "customer"
    ) -> CallOutcome:
        """
        Make an outbound call to a phone number and connect to a LiveKit room.
        
        Args:
            phone_number: The phone number to call (E.164 format, e.g., +919876543210)
            room_name: The LiveKit room name to connect the call to
            customer_name: Name of the customer for logging purposes
            
        Returns:
            CallOutcome object with the result of the call attempt
        """
        start_time = datetime.now()
        
        try:
            logger.info(f"Initiating outbound call to {customer_name} at {phone_number}")
            
            # Create SIP URI for LiveKit
            # Format: sip:room_name@your_livekit_sip_domain
            sip_uri = f"sip:{room_name}@{self._extract_sip_domain()}"
            
            # Make the call via Twilio
            call = self.client.calls.create(
                to=phone_number,
                from_=self.twilio_number,
                url=f"{self.livekit_url}/sip/{room_name}",  # This would need a SIP trunk setup
                method="POST",
                status_callback_event=["initiated", "ringing", "answered", "completed"],
                status_callback=f"{self.livekit_url}/webhook/twilio",  # Webhook for status updates
                timeout=30  # 30 seconds timeout for no answer
            )
            
            logger.info(f"Call initiated with SID: {call.sid}")
            
            return CallOutcome(
                status="initiated",
                timestamp=start_time,
                error_message=None
            )
            
        except TwilioRestException as e:
            error_msg = f"Twilio API error: {e.msg}"
            logger.error(error_msg)
            
            # Map Twilio error codes to call outcomes
            if e.code == 13227:  # No answer
                return CallOutcome(
                    status="no_answer",
                    timestamp=start_time,
                    error_message=error_msg
                )
            elif e.code in [13228, 13229]:  # Busy
                return CallOutcome(
                    status="busy",
                    timestamp=start_time,
                    error_message=error_msg
                )
            else:
                return CallOutcome(
                    status="failed",
                    timestamp=start_time,
                    error_message=error_msg
                )
                
        except Exception as e:
            error_msg = f"Unexpected error during outbound call: {str(e)}"
            logger.error(error_msg)
            return CallOutcome(
                status="failed",
                timestamp=start_time,
                error_message=error_msg
            )
    
    def get_call_status(self, call_sid: str) -> Optional[dict]:
        """
        Get the current status of a call by its SID.
        
        Args:
            call_sid: The Twilio call SID
            
        Returns:
            Dictionary with call status information or None if not found
        """
        try:
            call = self.client.calls(call_sid).fetch()
            return {
                "sid": call.sid,
                "status": call.status,
                "duration": call.duration,
                "direction": call.direction,
                "to": call.to,
                "from": call.from_,
                "start_time": call.start_time,
                "end_time": call.end_time
            }
        except TwilioRestException as e:
            logger.error(f"Failed to fetch call status: {e.msg}")
            return None
    
    def handle_call_outcome(self, call_sid: str, customer_name: str) -> str:
        """
        Handle different call outcomes and determine retry logic.
        
        Args:
            call_sid: The Twilio call SID
            customer_name: Name of the customer
            
        Returns:
            Message describing the outcome and next actions
        """
        call_info = self.get_call_status(call_sid)
        
        if not call_info:
            return f"Could not retrieve call information for {call_sid}"
        
        status = call_info["status"]
        
        # Handle different outcomes
        if status == "completed":
            duration = call_info.get("duration", 0)
            logger.info(f"Call to {customer_name} completed successfully. Duration: {duration}s")
            return f"Call completed successfully. Duration: {duration} seconds"
            
        elif status == "no-answer":
            logger.warning(f"Call to {customer_name} was not answered")
            return "No answer - recommend retry in 5 minutes"
            
        elif status == "busy":
            logger.warning(f"Call to {customer_name} was busy")
            return "Line busy - recommend retry in 2 minutes"
            
        elif status == "failed":
            logger.error(f"Call to {customer_name} failed")
            return "Call failed - check number and retry later"
            
        elif status == "canceled":
            logger.info(f"Call to {customer_name} was canceled")
            return "Call was canceled"
            
        else:
            logger.info(f"Call to {customer_name} status: {status}")
            return f"Call status: {status}"
    
    def _extract_sip_domain(self) -> str:
        """
        Extract SIP domain from LiveKit URL for SIP trunking.
        
        Returns:
            SIP domain string
        """
        # This would need to be configured based on your LiveKit SIP setup
        # For now, return a placeholder that would need to be replaced
        # with actual SIP domain from LiveKit SIP trunk configuration
        if self.livekit_url:
            # Extract domain from URL (e.g., wss://project.livekit.cloud -> project.livekit.cloud)
            return self.livekit_url.replace("wss://", "").replace("ws://", "")
        return "livekit-sip-domain.example.com"
    
    def schedule_order_confirmation_call(
        self,
        phone_number: str,
        customer_name: str,
        order_id: str
    ) -> CallOutcome:
        """
        Schedule an order confirmation call to a customer.
        
        Args:
            phone_number: Customer's phone number
            customer_name: Customer's name
            order_id: Order ID to confirm
            
        Returns:
            CallOutcome object
        """
        room_name = f"order-{order_id}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        logger.info(f"Scheduling order confirmation call for order {order_id} to {customer_name}")
        
        return self.make_outbound_call(
            phone_number=phone_number,
            room_name=room_name,
            customer_name=customer_name
        )


def create_outbound_caller() -> OutboundCaller:
    """
    Factory function to create an OutboundCaller instance.
    
    Returns:
        Configured OutboundCaller instance
    """
    return OutboundCaller()


# Example usage (for testing purposes)
if __name__ == "__main__":
    try:
        caller = create_outbound_caller()
        
        # Example: Make a test call
        # outcome = caller.make_outbound_call(
        #     phone_number="+919876543210",
        #     room_name="test-room",
        #     customer_name="Test Customer"
        # )
        # print(f"Call outcome: {outcome.status}")
        
        # Example: Schedule order confirmation call
        # outcome = caller.schedule_order_confirmation_call(
        #     phone_number="+919876543210",
        #     customer_name="Tanya",
        #     order_id="ORD12345"
        # )
        # print(f"Order confirmation call initiated: {outcome.status}")
        
        print("OutboundCaller module loaded successfully")
        
    except ValueError as e:
        print(f"Configuration error: {e}")
    except Exception as e:
        print(f"Error: {e}")