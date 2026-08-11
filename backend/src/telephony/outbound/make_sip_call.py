"""
Direct SIP call creation using LiveKit API.
This script creates a SIP call using LiveKit's Python SDK.
"""

import os
import sys
import asyncio
from pathlib import Path
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("make_sip_call")

load_dotenv(".env.local")

async def create_sip_call(trunk_id: str, to_number: str, room_name: str):
    """
    Create a SIP call using LiveKit API.
    
    Args:
        trunk_id: The SIP trunk ID
        to_number: The destination SIP address (e.g., sip:user@domain.com)
        room_name: The LiveKit room name
    """
    try:
        from livekit.api import LiveKitAPI, CreateSIPParticipantRequest
    except ImportError:
        logger.error("LiveKit API package not found")
        return False
    
    livekit_url = os.getenv("LIVEKIT_URL")
    api_key = os.getenv("LIVEKIT_API_KEY")
    api_secret = os.getenv("LIVEKIT_API_SECRET")
    
    if not all([livekit_url, api_key, api_secret]):
        logger.error("Missing LiveKit credentials")
        return False
    
    client = None
    try:
        logger.info(f"Creating SIP call to sip:{to_number}")
        logger.info(f"Room: {room_name}")
        logger.info(f"Trunk ID: {trunk_id}")
        
        # Convert WebSocket URL to HTTP URL
        http_url = livekit_url.replace("wss://", "https://").replace("ws://", "http://")
        
        # Create LiveKit API client
        client = LiveKitAPI(http_url, api_key, api_secret)
        
        # Create SIP participant request
        request = CreateSIPParticipantRequest(
            room_name=room_name,
            sip_trunk_id=trunk_id,
            sip_call_to=to_number,
        )
        
        # Make the call
        response = await client.sip.create_sip_participant(request)
        
        logger.info("SIP call created successfully!")
        logger.info(f"Participant ID: {response.participant_id}")
        # Handle status field gracefully
        try:
            logger.info(f"Status: {response.status}")
        except AttributeError:
            logger.info("Status: Created (no status field in response)")
        return True
        
    except Exception as e:
        logger.error(f"Error creating SIP call: {e}")
        return False
    finally:
        # Clean up client session
        if client is not None:
            await client.aclose()

async def main():
    trunk_id = "ST_HWeW8KS4uXvy"
    to_number = "tanya5315"  # Just the username
    from datetime import datetime
    room_name = f"outbound-call-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    success = await create_sip_call(trunk_id, to_number, room_name)
    return success

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)