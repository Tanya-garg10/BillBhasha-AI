"""
Script to trigger outbound calls for BillBhasha AI order confirmation.

This script can be run manually or integrated into your order processing system
to automatically trigger outbound calls when orders are placed.
"""

import argparse
import logging
import sys
from datetime import datetime
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.outbound_caller import create_outbound_caller, CallOutcome

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("trigger_outbound_call")


def trigger_order_confirmation_call(
    phone_number: str,
    customer_name: str,
    order_id: str
) -> CallOutcome:
    """
    Trigger an outbound call for order confirmation.
    
    Args:
        phone_number: Customer's phone number (E.164 format)
        customer_name: Customer's name
        order_id: Order ID to confirm
        
    Returns:
        CallOutcome object
    """
    try:
        caller = create_outbound_caller()
        logger.info(f"Initiating order confirmation call for order {order_id}")
        
        outcome = caller.schedule_order_confirmation_call(
            phone_number=phone_number,
            customer_name=customer_name,
            order_id=order_id
        )
        
        logger.info(f"Call initiated with status: {outcome.status}")
        return outcome
        
    except Exception as e:
        logger.error(f"Failed to trigger outbound call: {e}")
        return CallOutcome(
            status="failed",
            timestamp=datetime.now(),
            error_message=str(e)
        )


def main():
    """Main function to handle command line arguments."""
    parser = argparse.ArgumentParser(
        description="Trigger outbound calls for BillBhasha AI order confirmation"
    )
    
    parser.add_argument(
        "--phone",
        required=True,
        help="Customer's phone number in E.164 format (e.g., +919876543210)"
    )
    
    parser.add_argument(
        "--name",
        required=True,
        help="Customer's name"
    )
    
    parser.add_argument(
        "--order-id",
        required=True,
        help="Order ID to confirm"
    )
    
    args = parser.parse_args()
    
    # Validate phone number format
    if not args.phone.startswith("+"):
        logger.error("Phone number must be in E.164 format (e.g., +919876543210)")
        sys.exit(1)
    
    logger.info(f"Starting outbound call process for {args.name}")
    logger.info(f"Phone: {args.phone}, Order ID: {args.order_id}")
    
    # Trigger the call
    outcome = trigger_order_confirmation_call(
        phone_number=args.phone,
        customer_name=args.name,
        order_id=args.order_id
    )
    
    # Report the outcome
    print(f"\n{'='*50}")
    print(f"Outbound Call Result")
    print(f"{'='*50}")
    print(f"Status: {outcome.status}")
    print(f"Timestamp: {outcome.timestamp}")
    
    if outcome.error_message:
        print(f"Error: {outcome.error_message}")
    else:
        print(f"Call initiated successfully!")
        print(f"Customer: {args.name}")
        print(f"Order ID: {args.order_id}")
        print(f"Phone: {args.phone}")
    
    print(f"{'='*50}\n")
    
    # Exit with appropriate code
    sys.exit(0 if outcome.status == "initiated" else 1)


if __name__ == "__main__":
    main()