"""
Support ticket management system for BillBhasha AI.

This module handles creation and management of support tickets for human escalation.
Generates reference IDs and stores ticket information.
"""

import logging
import json
import os
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, asdict
from pathlib import Path

logger = logging.getLogger("support_tickets")

# Database file for storing support tickets
TICKETS_DB = Path(__file__).parent.parent / "support_tickets.json"


@dataclass
class SupportTicket:
    """Data structure for a support ticket."""
    reference_id: str
    caller_id: str
    issue_type: str
    urgency: str
    language: str
    room: str
    timestamp: str
    status: str = "Open"
    additional_context: Optional[str] = None
    updated_at: Optional[str] = None


class SupportTicketManager:
    """Manages support tickets for human escalation."""
    
    def __init__(self):
        """Initialize the ticket manager."""
        self._ensure_db_exists()
        logger.info("SupportTicketManager initialized")
    
    def _ensure_db_exists(self):
        """Ensure the tickets database file exists."""
        if not TICKETS_DB.exists():
            with open(TICKETS_DB, 'w') as f:
                json.dump([], f)
            logger.info(f"Created support tickets database: {TICKETS_DB}")
    
    def _load_tickets(self) -> List[Dict[str, Any]]:
        """Load all tickets from the database."""
        try:
            with open(TICKETS_DB, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load tickets: {e}")
            return []
    
    def _save_tickets(self, tickets: List[Dict[str, Any]]) -> bool:
        """Save tickets to the database."""
        try:
            with open(TICKETS_DB, 'w') as f:
                json.dump(tickets, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Failed to save tickets: {e}")
            return False
    
    def _generate_reference_id(self) -> str:
        """Generate a unique reference ID for the support ticket."""
        # Use timestamp and random number for uniqueness
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        import random
        random_num = random.randint(1000, 9999)
        return f"BB-{random_num}"
    
    def create_ticket(
        self,
        caller_id: str,
        issue_type: str,
        urgency: str = "Medium",
        language: str = "Hindi",
        room: str = "unknown",
        additional_context: Optional[str] = None
    ) -> SupportTicket:
        """Create a new support ticket.
        
        Args:
            caller_id: The caller's identifier
            issue_type: The type of issue (e.g., "Refund dispute", "GST charge dispute")
            urgency: The urgency level (Low, Medium, High)
            language: User's preferred language
            room: The room name where the issue occurred
            additional_context: Any additional context about the issue
            
        Returns:
            The created SupportTicket object
        """
        try:
            # Generate reference ID
            reference_id = self._generate_reference_id()
            
            # Create ticket
            ticket = SupportTicket(
                reference_id=reference_id,
                caller_id=caller_id,
                issue_type=issue_type,
                urgency=urgency,
                language=language,
                room=room,
                timestamp=datetime.now().isoformat(),
                status="Open",
                additional_context=additional_context
            )
            
            # Load existing tickets
            tickets = self._load_tickets()
            
            # Add new ticket
            tickets.append(asdict(ticket))
            
            # Save to database
            if self._save_tickets(tickets):
                logger.info(f"Support ticket created: {reference_id}")
                return ticket
            else:
                logger.error(f"Failed to save ticket: {reference_id}")
                return ticket
                
        except Exception as e:
            logger.error(f"Failed to create support ticket: {e}")
            # Return ticket anyway even if save failed
            return ticket
    
    def get_ticket(self, reference_id: str) -> Optional[SupportTicket]:
        """Get a support ticket by reference ID.
        
        Args:
            reference_id: The reference ID of the ticket
            
        Returns:
            The SupportTicket if found, None otherwise
        """
        try:
            tickets = self._load_tickets()
            for ticket_data in tickets:
                if ticket_data.get('reference_id') == reference_id:
                    return SupportTicket(**ticket_data)
            return None
        except Exception as e:
            logger.error(f"Failed to get ticket {reference_id}: {e}")
            return None
    
    def get_all_tickets(self) -> List[SupportTicket]:
        """Get all support tickets.
        
        Returns:
            List of all SupportTicket objects
        """
        try:
            tickets = self._load_tickets()
            return [SupportTicket(**ticket_data) for ticket_data in tickets]
        except Exception as e:
            logger.error(f"Failed to get all tickets: {e}")
            return []
    
    def update_ticket_status(self, reference_id: str, status: str) -> bool:
        """Update the status of a support ticket.
        
        Args:
            reference_id: The reference ID of the ticket
            status: The new status (Open, In Progress, Resolved, Closed)
            
        Returns:
            True if update was successful, False otherwise
        """
        try:
            tickets = self._load_tickets()
            for ticket_data in tickets:
                if ticket_data.get('reference_id') == reference_id:
                    ticket_data['status'] = status
                    ticket_data['updated_at'] = datetime.now().isoformat()
                    return self._save_tickets(tickets)
            return False
        except Exception as e:
            logger.error(f"Failed to update ticket status: {e}")
            return False
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get dashboard data for support tickets.
        
        Returns:
            Dictionary with dashboard statistics and recent tickets
        """
        try:
            tickets = self.get_all_tickets()
            
            # Calculate statistics
            total_tickets = len(tickets)
            open_tickets = len([t for t in tickets if t.status == "Open"])
            in_progress_tickets = len([t for t in tickets if t.status == "In Progress"])
            resolved_tickets = len([t for t in tickets if t.status == "Resolved"])
            
            # Get recent tickets (last 10)
            recent_tickets = sorted(tickets, key=lambda t: t.timestamp, reverse=True)[:10]
            
            return {
                "statistics": {
                    "total": total_tickets,
                    "open": open_tickets,
                    "in_progress": in_progress_tickets,
                    "resolved": resolved_tickets
                },
                "recent_tickets": [asdict(ticket) for ticket in recent_tickets]
            }
        except Exception as e:
            logger.error(f"Failed to get dashboard data: {e}")
            return {
                "statistics": {"total": 0, "open": 0, "in_progress": 0, "resolved": 0},
                "recent_tickets": []
            }


def create_ticket_manager() -> SupportTicketManager:
    """Factory function to create a SupportTicketManager instance.
    
    Returns:
        Configured SupportTicketManager instance
    """
    return SupportTicketManager()


# Example usage (for testing purposes)
if __name__ == "__main__":
    try:
        manager = create_ticket_manager()
        
        # Test ticket creation
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
        print(f"Status: {test_ticket.status}")
        
        # Test dashboard data
        dashboard = manager.get_dashboard_data()
        print(f"\nDashboard statistics: {dashboard['statistics']}")
        
    except Exception as e:
        print(f"Error: {e}")