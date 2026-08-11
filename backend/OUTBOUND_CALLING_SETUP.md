# Outbound Calling Setup for BillBhasha AI

This guide explains how to set up and use outbound calling functionality for BillBhasha AI. You have two options:

1. **Twilio** (Recommended for production)
2. **Linphone** (Free alternative, good for testing)

## Overview

The outbound calling system enables BillBhasha AI to:
- Make automated calls to customers for order confirmation
- Provide delivery updates
- Handle call outcomes (no answer, busy, voicemail, hang-up)
- Respect user preferences for opt-out

## Option 1: Twilio Setup (Recommended for Production)

### Prerequisites

1. **Twilio Account**: Sign up at https://www.twilio.com/
2. **LiveKit SIP Trunk**: Configure SIP trunking in your LiveKit project
3. **Twilio Phone Number**: Purchase a phone number from Twilio console
4. **Environment Variables**: Configure all required credentials

### Step 1: Configure Twilio

### 1.1 Get Twilio Credentials

1. Log in to your Twilio Console: https://console.twilio.com/
2. Navigate to Settings → General Settings
3. Copy your **Account SID** and **Auth Token**

### 1.2 Purchase a Phone Number

1. In Twilio Console, go to Phone Numbers → Buy a Number
2. Select a number (preferably with SMS and Voice capabilities)
3. Purchase the number

### 1.3 Configure SIP Trunking

1. In Twilio Console, go to SIP Trunking → Trunks
2. Create a new SIP Trunk or configure existing one
3. Set up the SIP Domain to connect with LiveKit
4. Configure the SIP URI to point to your LiveKit server

## Step 2: Configure Environment Variables

Add the following to your `backend/.env.local` file:

```bash
# Twilio Configuration
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=your_twilio_phone_number_here

# Ensure LiveKit URL is also configured
LIVEKIT_URL=wss://your-project.livekit.cloud
```

## Step 3: Install Dependencies

The new Twilio dependency has been added to `pyproject.toml`. Install it:

```bash
cd backend
uv sync
```

## Step 4: Test the Setup

### 4.1 Test Order Simulator

Run the order simulator to create sample orders:

```bash
uv run python src/order_simulator.py
```

This will:
- Create sample orders with test customer data
- Save them to `sample_orders.json`
- Display the latest order for testing

### 4.2 Test Outbound Call

Trigger an outbound call using the trigger script:

```bash
uv run python src/trigger_outbound_call.py \
  --phone +919876543210 \
  --name "Tanya" \
  --order-id ORD12345
```

**Important**: Replace the phone number with your actual test number.

## Step 5: Integration with Order System

To integrate with your actual order processing system:

### 5.1 Programmatic Integration

```python
from src.outbound_caller import create_outbound_caller

# Create the caller instance
caller = create_outbound_caller()

# Trigger order confirmation call
outcome = caller.schedule_order_confirmation_call(
    phone_number="+919876543210",
    customer_name="Tanya",
    order_id="ORD12345"
)

print(f"Call status: {outcome.status}")
```

### 5.2 Webhook Integration

Set up a webhook endpoint in your order system that calls the trigger script when:
- A new order is placed
- Order status changes to "confirmed"
- Delivery status updates

## Step 6: Call Outcome Handling

The system handles different call outcomes:

| Outcome | Description | Retry Logic |
|---------|-------------|-------------|
| `completed` | Call completed successfully | No retry needed |
| `no_answer` | Customer didn't answer | Retry in 5 minutes |
| `busy` | Line was busy | Retry in 2 minutes |
| `failed` | Call failed due to error | Check number, retry later |
| `canceled` | Call was canceled | No retry needed |

### Example: Handle Call Outcome

```python
from src.outbound_caller import create_outbound_caller

caller = create_outbound_caller()

# Make the call
outcome = caller.make_outbound_call(
    phone_number="+919876543210",
    room_name="order-ORD12345",
    customer_name="Tanya"
)

# Handle the outcome
if outcome.status == "no_answer":
    # Schedule retry in 5 minutes
    schedule_retry(phone_number, delay_minutes=5)
elif outcome.status == "busy":
    # Schedule retry in 2 minutes
    schedule_retry(phone_number, delay_minutes=2)
```

## Step 7: Advanced Features

### 7.1 Custom Retry Logic

Implement custom retry strategies based on your business needs:

```python
def handle_retry(phone_number, attempt_count):
    if attempt_count < 3:
        delay = 2 ** attempt_count * 60  # Exponential backoff
        schedule_retry(phone_number, delay_minutes=delay)
    else:
        send_sms_notification(phone_number, "Order confirmation call failed")
```

### 7.2 Voicemail Detection

Configure voicemail detection in Twilio to handle voicemail scenarios:

```python
# In Twilio SIP Trunk settings, enable voicemail detection
# The system can then leave a pre-recorded message
```

### 7.3 Opt-Out Management

The agent automatically handles opt-out requests. When a user says:
- "Don't call me again"
- "Stop calling me"
- "I don't want these calls"

The agent responds with the standard opt-out message and you should:
1. Log the opt-out preference
2. Update your customer database
3. Exclude from future outbound calls

## Option 2: Linphone Setup (Free Alternative)

If your Twilio free trial is exhausted, you can use Linphone to make outbound calls for free.

### Prerequisites

1. **Linphone Account**: Create a free account at https://linphone.org/
2. **LiveKit Cloud Account**: Sign up at https://livekit.com/
3. **Linphone App**: Download the Linphone app for your phone
4. **Environment Variables**: Configure LiveKit credentials

### Step 1: Set up Linphone Account

1. Go to https://linphone.org/ and create a new account
2. After account creation, you'll receive your SIP address (usually `sip:<username>@sip.linphone.org`)
3. Make note of your username

### Step 2: Configure LiveKit Cloud

1. Log in to your LiveKit Cloud account
2. Create a new project or use existing one
3. Get your LiveKit URL, API key, and API secret
4. Save these in your `backend/.env.local` file:
   ```bash
   LIVEKIT_URL=wss://your-project.livekit.cloud
   LIVEKIT_API_KEY=your_livekit_api_key_here
   LIVEKIT_API_SECRET=your_livekit_api_secret_here
   ```

### Step 3: Create SIP Trunk in LiveKit

1. In LiveKit Cloud, go to the **Telephony** section
2. Click on **SIP Trunks**
3. Create a new outbound trunk with these details:
   ```json
   {
     "name": "linphone-trunk",
     "address": "sip.linphone.org",
     "transport": "SIP_TRANSPORT_TLS",
     "numbers": ["sip:<your-linphone-username>"]
   }
   ```
4. After creation, you'll receive a **TRUNK ID**
5. Save this as `LIVEKIT_SIP_OUTBOUND_TRUNK_ID` in your `.env.local` file

### Step 4: Set up Linphone App

1. Download and install the Linphone app on your phone
2. Log in with your linphone.org credentials
3. Grant microphone permissions to the app
4. **Important**: In Linphone app settings:
   - Go to **Settings → Calls → Advanced calls settings**
   - Turn **"Media encryption mandatory" OFF**

### Step 5: Start the Agent

Run the outbound agent:

```bash
cd backend
uv run python src/telephony/outbound/agent.py dev
```

### Step 6: Make Test Call

In a separate terminal, make a call to your Linphone account:

```bash
cd backend
uv run python src/telephony/outbound/dial.py --to <your-linphone-username>
```

You will receive a call on your Linphone app and can start talking to the agent.

### Step 7: Testing Checklist for Linphone

- [ ] Linphone account created
- [ ] LiveKit credentials configured in `.env.local`
- [ ] SIP trunk created in LiveKit Cloud
- [ ] Trunk ID saved in `.env.local`
- [ ] Linphone app installed and logged in
- [ ] Microphone permissions granted
- [ ] Media encryption mandatory turned OFF
- [ ] Agent runs successfully
- [ ] Test call connects to Linphone app
- [ ] Voice conversation works

## Troubleshooting

### Twilio Issues

**Issue**: `Missing Twilio credentials` error
- **Solution**: Ensure all TWILIO_* variables are set in `.env.local`

**Issue**: Calls not connecting
- **Solution**: Verify SIP trunk configuration in Twilio and LiveKit

**Issue**: Invalid phone number format
- **Solution**: Use E.164 format (e.g., +919876543210)

**Issue**: Authentication errors
- **Solution**: Verify TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN are correct

### Linphone Issues

**Issue**: `Missing SIP trunk ID` error
- **Solution**: Ensure LIVEKIT_SIP_OUTBOUND_TRUNK_ID is set in `.env.local`

**Issue**: Call not reaching Linphone app
- **Solution**: Verify SIP trunk configuration in LiveKit Cloud and that Linphone app is running

**Issue**: No audio in call
- **Solution**: Ensure "Media encryption mandatory" is OFF in Linphone app settings

**Issue**: Connection failed
- **Solution**: Check that you're using the correct Linphone username and that SIP trunk numbers match

**Issue**: Agent not joining room
- **Solution**: Ensure the agent is running with `uv run python src/telephony/outbound/agent.py dev`

## Testing Checklist

### Twilio Testing
- [ ] Twilio credentials configured in `.env.local`
- [ ] Phone number purchased in Twilio
- [ ] SIP trunk configured
- [ ] Dependencies installed with `uv sync`
- [ ] Order simulator runs successfully
- [ ] Test outbound call completes
- [ ] Call outcomes handled correctly
- [ ] Opt-out functionality tested

### Linphone Testing
- [ ] Linphone account created
- [ ] LiveKit credentials configured in `.env.local`
- [ ] SIP trunk created in LiveKit Cloud
- [ ] Trunk ID saved in `.env.local`
- [ ] Linphone app installed and logged in
- [ ] Microphone permissions granted
- [ ] Media encryption mandatory turned OFF
- [ ] Agent runs successfully
- [ ] Test call connects to Linphone app
- [ ] Voice conversation works

## Production Considerations

1. **Rate Limiting**: Implement rate limiting to avoid Twilio API limits
2. **Error Handling**: Add comprehensive error handling and logging
3. **Monitoring**: Set up monitoring for call success rates
4. **Compliance**: Ensure compliance with local regulations (TRAI in India)
5. **Cost Management**: Monitor Twilio usage and costs
6. **Database Integration**: Store call outcomes in your database
7. **User Preferences**: Respect user contact preferences and timing

## Next Steps

1. Test with your actual Twilio credentials
2. Integrate with your order management system
3. Set up webhook endpoints for automated triggering
4. Implement retry logic and call outcome handling
5. Monitor and optimize call success rates
6. Add compliance features (DND registry check, etc.)

## Support

For issues specific to:
- **Twilio**: https://www.twilio.com/docs
- **LiveKit**: https://docs.livekit.io
- **This Project**: Check the main README.md