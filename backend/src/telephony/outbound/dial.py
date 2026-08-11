"""
Dial script for making outbound calls via LiveKit SIP trunking to Linphone.

This script provides instructions for making outbound calls to Linphone accounts.
"""

import argparse
import logging
import os
import sys
from pathlib import Path
from datetime import datetime

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("dial")

load_dotenv(".env.local")


def make_outbound_call(to_username: str, room_name: str = None):
    """
    Provide instructions for making an outbound call to a Linphone account.
    
    Args:
        to_username: The Linphone username to call (without @sip.linphone.org)
        room_name: Optional room name for the call (auto-generated if not provided)
    """
    # Get LiveKit credentials
    livekit_url = os.getenv("LIVEKIT_URL")
    livekit_api_key = os.getenv("LIVEKIT_API_KEY")
    livekit_api_secret = os.getenv("LIVEKIT_API_SECRET")
    sip_trunk_id = os.getenv("LIVEKIT_SIP_OUTBOUND_TRUNK_ID")
    
    if not all([livekit_url, livekit_api_key, livekit_api_secret]):
        logger.error("Missing LiveKit credentials. Please set LIVEKIT_URL, LIVEKIT_API_KEY, and LIVEKIT_API_SECRET in .env.local")
        return False
    
    if not sip_trunk_id:
        logger.error("Missing SIP trunk ID. Please set LIVEKIT_SIP_OUTBOUND_TRUNK_ID in .env.local")
        return False
    
    # Generate room name if not provided
    if not room_name:
        room_name = f"outbound-call-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    logger.info(f"=" * 60)
    logger.info(f"Outbound Call Setup for Linphone")
    logger.info(f"=" * 60)
    logger.info(f"Target: {to_username}@sip.linphone.org")
    logger.info(f"Room: {room_name}")
    logger.info(f"SIP Trunk ID: {sip_trunk_id}")
    logger.info(f"=" * 60)
    
    logger.info(f"\nTo make this call, follow these steps:")
    logger.info(f"1. Start the agent in one terminal:")
    logger.info(f"   cd backend")
    logger.info(f"   uv run python src/telephony/outbound/agent.py dev")
    
    logger.info(f"\n2. Use LiveKit CLI or API to initiate the SIP call:")
    logger.info(f"   You can use the LiveKit CLI to make SIP calls:")
    logger.info(f"   livekit-cli sip-call create \\")
    logger.info(f"     --trunk-id {sip_trunk_id} \\")
    logger.info(f"     --to sip:{to_username}@sip.linphone.org \\")
    logger.info(f"     --room {room_name}")
    
    logger.info(f"\n3. Ensure your Linphone app is:")
    logger.info(f"   - Running and logged in")
    logger.info(f"   - Has microphone permissions")
    logger.info(f"   - Has 'Media encryption mandatory' turned OFF")
    
    logger.info(f"\n4. You will receive the call on your Linphone app")
    logger.info(f"   and can start talking to BillBhasha AI")
    
    logger.info(f"\n" + "=" * 60)
    
    return True


def main():
    """Main function to handle command line arguments."""
    parser = argparse.ArgumentParser(
        description="Get instructions for making outbound calls via LiveKit SIP trunking to Linphone"
    )
    
    parser.add_argument(
        "--to",
        required=True,
        help="Linphone username to call (without @sip.linphone.org)"
    )
    
    parser.add_argument(
        "--room",
        help="Optional room name for the call (auto-generated if not provided)"
    )
    
    args = parser.parse_args()
    
    logger.info(f"Starting outbound call setup for {args.to}")
    
    # Provide instructions
    success = make_outbound_call(
        to_username=args.to,
        room_name=args.room
    )
    
    if success:
        logger.info("Instructions provided successfully")
        sys.exit(0)
    else:
        logger.error("Failed to provide instructions")
        sys.exit(1)


if __name__ == "__main__":
    main()