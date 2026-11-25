---
name: send-sms
description: Send SMS text messages programmatically via multiple SMS API providers
target: https://tasking.tech
---

# Provided by TippyEntertainment

# Send SMS

Send SMS text messages programmatically through Twilio, Vonage, TextBelt, or custom HTTP endpoints. Supports single messages, bulk sending, media attachments (MMS), and delivery tracking.

## Setup

### Twilio Setup
1. Create a Twilio account at https://www.twilio.com
2. Get your Account SID and Auth Token from the Console Dashboard
3. Purchase a Twilio phone number or use a verified caller ID
4. Save credentials in Settings → Integrations:
   - TWILIO_ACCOUNT_SID
   - TWILIO_AUTH_TOKEN
   - TWILIO_PHONE_NUMBER

### Vonage Setup
1. Create a Vonage account at https://www.vonage.com
2. Get your API Key and API Secret from the Dashboard
3. Save credentials:
   - VONAGE_API_KEY
   - VONAGE_API_SECRET
   - VONAGE_FROM_NUMBER (optional)

### TextBelt Setup (Free Tier Available)
1. Get a free API key at https://textbelt.com
2. Free tier: 1 text per day
3. Save credential: TEXTBELT_API_KEY

### Custom Provider Setup
For custom HTTP endpoints, provide:
- URL endpoint
- Authentication method (bearer, basic, api_key_header)
- Required headers

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| to | string | Yes | Recipient phone number in E.164 format (+15551234567). Comma-separated for bulk. |
| message | string | Yes | SMS body text. Max 160 chars for single segment, 1600 for multi-segment. |
| from | string | No | Sender number or alphanumeric ID. Provider-specific. |
| provider | string | No | SMS provider: 'twilio' (default), 'vonage', 'textbelt', 'custom'. |
| provider_config | object | No | Provider credentials. Uses stored secrets if not provided. |
| options | object | No | Additional options: media_url, status_callback, validity, priority. |

## Returns

```json
{
  "success": true,
  "message_id": "SMxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "status": "queued",
  "segments": 1,
  "cost": 0.0075
}
```

## Usage Examples

### Example 1: Send SMS via Twilio (using stored credentials)

```javascript
// Prerequisites: TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER saved in Settings

// Send a simple SMS
send_sms({
  to: "+15551234567",
  message: "Your verification code is 123456. Valid for 5 minutes."
});
```

### Example 2: Send SMS with explicit credentials

```javascript
send_sms({
  to: "+15551234567",
  message: "Hello from TaskingBot!",
  from: "+15559876543",
  provider: "twilio",
  provider_config: {
    account_sid: "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    auth_token: "your_auth_token_here"
  }
});
```

### Example 3: Send MMS with image attachment

```javascript
send_sms({
  to: "+15551234567",
  message: "Check out this photo!",
  from: "+15559876543",
  provider: "twilio",
  options: {
    media_url: "https://example.com/image.jpg"
  }
});
```

### Example 4: Bulk SMS to multiple recipients

```javascript
send_sms({
  to: "+15551111111,+15552222222,+15553333333",
  message: "Flash sale! 50% off all items today only!",
  from: "+15559876543",
  provider: "twilio"
});
```

### Example 5: Send via Vonage

```javascript
send_sms({
  to: "+15551234567",
  message: "Your order has shipped!",
  from: "MyBrand", // Alphanumeric sender ID
  provider: "vonage",
  provider_config: {
    api_key: "your_api_key",
    api_secret: "your_api_secret"
  }
});
```

### Example 6: Send via TextBelt (free tier)

```javascript
send_sms({
  to: "+15551234567",
  message: "Test message from TextBelt",
  provider: "textbelt",
  provider_config: {
    api_key: "textbelt" // Free tier key
  }
});
```

### Example 7: Custom HTTP endpoint

```javascript
send_sms({
  to: "+15551234567",
  message: "Custom provider test",
  provider: "custom",
  provider_config: {
    url: "https://api.example.com/sms/send",
    auth_type: "bearer",
    headers: {
      "X-Custom-Header": "value"
    }
  }
});
```

### Example 8: With delivery status callback

```javascript
send_sms({
  to: "+15551234567",
  message: "Important notification",
  from: "+15559876543",
  provider: "twilio",
  options: {
    status_callback: "https://yourserver.com/sms/status"
  }
});
```

## Step-by-Step Implementation

### Step 1: Validate Input
- Check that `to` is a valid phone number format (E.164 recommended)
- Validate `message` length (max 1600 characters)
- Ensure provider is specified or default to 'twilio'

### Step 2: Resolve Credentials
- If `provider_config` provided, use those credentials
- Otherwise, load from stored secrets:
  - Twilio: TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER
  - Vonage: VONAGE_API_KEY, VONAGE_API_SECRET
  - TextBelt: TEXTBELT_API_KEY

### Step 3: Format Request
Format the API request based on provider:

**Twilio:**
```
POST https://api.twilio.com/2010-04-01/Accounts/{AccountSid}/Messages.json
Authorization: Basic (base64 of account_sid:auth_token)
Body: To=+15551234567&From=+15559876543&Body=Hello
```

**Vonage:**
```
POST https://rest.nexmo.com/sms/json
Body: api_key=xxx&api_secret=xxx&to=+15551234567&from=MyBrand&text=Hello
```

**TextBelt:**
```
POST https://textbelt.com/text
Body: phone=+15551234567&message=Hello&key=xxx
```

### Step 4: Send Request
- Make HTTP POST request to provider endpoint
- Include authentication headers
- Handle rate limiting (retry with backoff)

### Step 5: Parse Response
- Extract message_id, status, and cost from response
- Handle errors gracefully with descriptive messages

### Step 6: Return Result
```json
{
  "success": true,
  "message_id": "SMxxx",
  "status": "queued",
  "segments": 1,
  "cost": 0.0075
}
```

## Error Handling

| Error Code | Description | Solution |
|------------|-------------|----------|
| INVALID_NUMBER | Phone number format invalid | Use E.164 format (+countrycode) |
| AUTH_FAILED | Invalid credentials | Check API keys in Settings |
| INSUFFICIENT_FUNDS | Account balance too low | Add funds to provider account |
| RATE_LIMITED | Too many requests | Implement retry with exponential backoff |
| BLOCKED | Number on do-not-contact list | Remove from recipient list |
| UNDELIVERABLE | Message cannot be delivered | Check recipient number validity |

## Best Practices

1. **Phone Number Format**: Always use E.164 format (+countrycode) for international compatibility
2. **Message Length**: Keep messages under 160 chars when possible to avoid segmentation
3. **Opt-Out Compliance**: Include opt-out instructions for marketing messages
4. **Rate Limiting**: Respect provider rate limits (Twilio: 100/sec, Vonage: varies by plan)
5. **Status Callbacks**: Use status_callback for delivery tracking on critical messages
6. **Cost Management**: Monitor segments and costs, especially for bulk campaigns
7. **Testing**: Use provider test modes or free tiers for development
8. **Security**: Never hardcode credentials; use stored secrets

## Cost Estimates

| Provider | Cost per SMS (US) | International | Notes |
|----------|-------------------|---------------|-------|
| Twilio | $0.0075 | $0.02-0.12 | Volume discounts available |
| Vonage | $0.0055 | $0.02-0.10 | Competitive international rates |
| TextBelt | Free (1/day) | Paid plans | Free tier for testing |

## Security Notes

- Credentials are stored encrypted and never logged
- Use Settings → Integrations to configure API keys securely
- Phone numbers are validated before sending
- Message content is not stored after transmission

## Related Skills

- `send_email` - Send email notifications
- `discord_webhook` - Send Discord messages
- `http_post` - Generic HTTP POST for custom integrations