# Human Support Escalation Setup - Day 7

This document explains how to set up and configure the human support escalation feature for BillBhasha AI.

## Overview

The human support escalation feature allows BillBhasha AI to recognize when it cannot handle a user's request and automatically escalate to human support. This is crucial for:

- Billing disputes and complex account issues
- Refund requests requiring verification
- Unusual charges that AI cannot explain
- User frustration or repeated unresolved issues
- Account verification and sensitive operations

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

### Notification Channels

You can configure one or more notification channels:

#### 1. Generic Webhook
- Set `HUMAN_SUPPORT_WEBHOOK_URL` to your webhook endpoint
- The system will send a JSON POST request with escalation data
- Payload format:
  ```json
  {
    "timestamp": "2026-08-11T19:00:00",
    "caller_id": "user_123",
    "reason": "billing dispute",
    "room": "room_456",
    "user_consent": true,
    "service": "BillBhasha AI",
    "escalation_type": "human_handoff"
  }
  ```

#### 2. Discord Webhook
- Set `DISCORD_WEBHOOK_URL` to your Discord webhook URL
- Creates a formatted Discord embed with escalation details
- Shows up as a colored alert in your Discord channel

#### 3. Slack Webhook
- Set `SLACK_WEBHOOK_URL` to your Slack webhook URL
- Creates a formatted Slack message with escalation details
- Shows up as a notification in your Slack channel

## Escalation Triggers

The AI will automatically escalate to human support when:

1. **User explicitly requests human support**
   - "Mujhe human se baat karni hai"
   - "Human se connect karo"
   - "I want to speak to a human"

2. **Billing disputes and complex account issues**
   - User reports incorrect charges
   - Complex billing questions AI cannot resolve
   - Account verification requests

3. **Refund requests**
   - User asks for refunds
   - Dispute resolution required

4. **Repeated unresolved issues**
   - User repeats the same problem multiple times
   - AI cannot provide satisfactory solution

5. **Sensitive operations**
   - Account changes requiring verification
   - Identity verification requests
   - Security-related issues

## Testing the Escalation

### Manual Testing

You can test the escalation by simulating a conversation that triggers escalation:

```python
# Test the escalation notification system
python src/human_support.py
```

### Voice Testing

During a call, say something like:
- "Mere bill mein ek charge hai jo mujhe bilkul samajh nahi aa raha, aur mujhe lag raha hai ye galat hai. Mujhe human se baat karni hai."

The AI should:
1. Acknowledge the concern
2. Explain why it needs to escalate
3. Ask for consent
4. Use the escalation tool
5. Send notifications to configured channels

## Monitoring Escalations

The system logs all escalation attempts:
- Timestamp
- Caller ID
- Reason for escalation
- Room information
- Notification status

Check the logs for escalation activity:
```bash
# View agent logs
tail -f logs/agent.log | grep escalation
```

## Customization

### Adding Custom Escalation Reasons

You can customize the escalation logic by modifying the system prompt in `src/agent.py`:

```python
HUMAN ESCALATION
You must recognize when to escalate to human support...

# Add your custom triggers here
- Add custom escalation scenarios specific to your use case
```

### Custom Notification Formats

Modify `src/human_support.py` to customize notification formats for your specific needs:

```python
def send_webhook_notification(self, escalation_data: EscalationData) -> bool:
    # Customize the payload format
    payload = {
        # Your custom fields
    }
```

## Troubleshooting

### Notifications Not Sending

1. Check environment variables are set correctly
2. Verify webhook URLs are accessible
3. Check network connectivity
4. Review error logs

### AI Not Escalating

1. Check system prompt escalation triggers
2. Verify escalation tool is properly registered
3. Test with clear escalation phrases
4. Review conversation logs

### Multiple Notifications

If you receive duplicate notifications:
- Check for multiple notification channels configured
- Review escalation timing logic
- Check for network retry issues

## Best Practices

1. **Always ask for consent** before escalating
2. **Provide clear reasons** for escalation to the user
3. **Monitor escalation patterns** to improve AI capabilities
4. **Set up proper monitoring** for human support notifications
5. **Have a backup plan** if notification systems fail
6. **Train human support** on escalation context and information

## Future Enhancements

Potential improvements for the escalation system:

- Priority levels for different escalation types
- Automatic callback scheduling
- Integration with ticket systems (Zendesk, Freshdesk)
- Real-time agent availability checking
- Escalation analytics and reporting
- Multi-language support for escalation messages