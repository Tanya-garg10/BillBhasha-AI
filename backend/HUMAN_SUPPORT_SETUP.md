# Human Support Escalation Setup - Day 7

This document explains how to set up and configure the human support escalation feature for BillBhasha AI.

## Overview

The human support escalation feature allows BillBhasha AI to recognize when it cannot handle a user's request and automatically create support tickets for human resolution. This is crucial for:

- Refund disputes and payment issues
- Wrong GST charges or billing discrepancies
- Complex account issues requiring verification
- User frustration or repeated unresolved issues
- Account verification and sensitive operations

## Key Features

- **Support Ticket Creation**: Automatic ticket generation with unique reference IDs
- **Privacy Protection**: Only shares necessary information, no sensitive data
- **Priority Levels**: Urgency levels (Low, Medium, High) for ticket prioritization
- **Language Preferences**: Tracks user's preferred language
- **Dashboard**: Simple database to track and manage support tickets
- **Notification System**: Alerts human support via webhooks, Discord, or Slack

## Configuration

### Environment Variables

Add the following to your `backend/.env.local` file:

```bash
# Generic webhook URL for human support notifications
HUMAN_SUPPORT_WEBHOOK_URL=https://your-webhook-endpoint.com/escalations

# Discord webhook for human support notifications (optional)
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/your-webhook-url

# Slack webhook for human support notifications (optional)
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/your-webhook-url
```

### Support Ticket Database

The system automatically creates a `support_tickets.json` file in the backend directory to store:
- Reference IDs
- Caller information
- Issue types
- Urgency levels
- Language preferences
- Ticket status

## Support Ticket Creation

The AI will automatically create support tickets when:

1. **Refund disputes and payment issues**
   - "I haven't received my refund"
   - "Payment not processed"
   - "Wrong amount charged"

2. **GST and billing discrepancies**
   - "Wrong GST charge"
   - "Incorrect bill amount"
   - "Billing error"

3. **User explicitly requests human support**
   - "Mujhe human se baat karni hai"
   - "Human se connect karo"
   - "I want to speak to a human"

4. **Repeated unresolved issues**
   - User repeats the same problem multiple times
   - AI cannot provide satisfactory solution

5. **Account verification needs**
   - Account changes requiring verification
   - Identity verification requests
   - Security-related issues

## Support Ticket Workflow

1. **Detection**: AI identifies complex issue requiring human support
2. **Consent**: AI asks for user permission to create support ticket
3. **Information Sharing**: AI explains what information will be shared (no sensitive data)
4. **Ticket Creation**: System generates unique reference ID (e.g., BB-2045)
5. **Notification**: Human support is notified via configured channels
6. **Tracking**: Ticket is stored in database for status tracking

## Testing the Support Ticket System

### Manual Testing

Test the support ticket creation:

```python
# Test the support ticket system
python test_support_tickets.py
```

### Voice Testing

During a call, say something like:
- "I paid for an online order two weeks ago, but I still haven't received my refund."

The AI should:
1. Acknowledge the refund issue
2. Explain it requires human support
3. Ask for consent to create ticket
4. Explain what information will be shared
5. Create the ticket with reference ID
6. Provide the reference ID to the user

## Dashboard and Monitoring

### View Support Tickets

You can view the support ticket database directly:

```bash
# View all support tickets
cat backend/support_tickets.json
```

### Dashboard Data

The system provides dashboard statistics:
- Total tickets
- Open tickets
- In Progress tickets
- Resolved tickets
- Recent tickets list

Access this programmatically via the `SupportTicketManager` class.

## Support Ticket Management

### Update Ticket Status

You can update ticket status programmatically:

```python
from src.support_tickets import SupportTicketManager

manager = SupportTicketManager()
manager.update_ticket_status("BB-2045", "In Progress")
```

### Get Ticket Information

```python
ticket = manager.get_ticket("BB-2045")
print(f"Issue: {ticket.issue_type}")
print(f"Status: {ticket.status}")
print(f"Urgency: {ticket.urgency}")
```

## Privacy and Security

The system is designed to protect user privacy:

- **No sensitive data shared**: Only shares name, issue type, urgency, language
- **Consent-based**: Always asks for user permission before creating tickets
- **Reference IDs**: Uses unique IDs instead of personal identifiers
- **Limited information**: Only shares what's necessary for human support

## Troubleshooting

### Support Tickets Not Creating

1. Check that `support_tickets.json` file is writable
2. Verify the `create_support_ticket` tool is properly registered
3. Test with clear refund dispute phrases
4. Review agent logs for errors

### Reference ID Generation Issues

1. Check if the support_tickets.json file exists
2. Verify file permissions
3. Test the ticket generation manually
4. Check for concurrent access issues

### Notification Failures

1. Check environment variables are set correctly
2. Verify webhook URLs are accessible
3. Test webhook endpoints independently
4. Review notification logs

## Best Practices

1. **Always ask for consent** before creating support tickets
2. **Explain clearly** what information will be shared
3. **Provide reference IDs** for easy tracking
4. **Monitor ticket patterns** to improve AI capabilities
5. **Set proper urgency levels** for prioritization
6. **Train human support** on ticket context and handling

## Future Enhancements

Potential improvements for the support ticket system:

- Integration with ticket systems (Zendesk, Freshdesk)
- Automatic ticket status updates from human support
- Customer satisfaction surveys after resolution
- Escalation analytics and reporting
- Multi-language support for ticket responses
- Automated ticket routing based on issue type