"""
Test script for support ticket system.
This script tests the support ticket creation and dashboard functionality.
"""

import asyncio
import os
from dotenv import load_dotenv
from src.support_tickets import SupportTicketManager

def test_support_tickets():
    """Test the support ticket system."""
    load_dotenv('.env.local')
    
    print("Testing Support Ticket System...")
    print("=" * 60)
    
    # Create ticket manager
    manager = SupportTicketManager()
    
    # Test ticket creation
    print("Creating test support ticket...")
    test_ticket = manager.create_ticket(
        caller_id="test_user_123",
        issue_type="Refund dispute",
        urgency="Medium",
        language="Hindi",
        room="test_room_456"
    )
    
    print(f"Support ticket created: {test_ticket.reference_id}")
    print(f"Issue: {test_ticket.issue_type}")
    print(f"Urgency: {test_ticket.urgency}")
    print(f"Language: {test_ticket.language}")
    print(f"Status: {test_ticket.status}")
    print()
    
    # Test ticket retrieval
    print("Retrieving ticket by reference ID...")
    retrieved_ticket = manager.get_ticket(test_ticket.reference_id)
    if retrieved_ticket:
        print(f"Ticket found: {retrieved_ticket.reference_id}")
        print(f"Status: {retrieved_ticket.status}")
    else:
        print("Ticket not found")
    print()
    
    # Test dashboard data
    print("Getting dashboard data...")
    dashboard = manager.get_dashboard_data()
    print(f"Statistics: {dashboard['statistics']}")
    print(f"Recent tickets: {len(dashboard['recent_tickets'])}")
    print()
    
    # Test ticket status update
    print("Updating ticket status...")
    success = manager.update_ticket_status(test_ticket.reference_id, "In Progress")
    print(f"Status update: {'Success' if success else 'Failed'}")
    
    # Verify update
    updated_ticket = manager.get_ticket(test_ticket.reference_id)
    if updated_ticket:
        print(f"Updated status: {updated_ticket.status}")
    print()
    
    print("=" * 60)
    print("Support ticket system test completed!")
    
    return True

if __name__ == "__main__":
    success = test_support_tickets()
    exit(0 if success else 1)