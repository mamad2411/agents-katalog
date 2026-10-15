---
name: signal-messenger
version: 1.0.0
description: Signal Messenger integration - Send and receive Signal messages. Requires signal-cli or signal-cli-rest-api installed.
metadata:
  { "openclaw": { "emoji": "📱", "tags": ["messaging", "signal", "communication"], "safety": "review-before-use" } }
---

# Signal Messenger Integration

Send messages via Signal using signal-cli or signal-cli-rest-api.

## Requirements

### Option 1: signal-cli (Command Line)

**Install on Linux:**
```bash
# Ubuntu/Debian
sudo apt install signal-cli

# Or from source
git clone https://github.com/AsamK/signal-cli.git
cd signal-cli
./gradlew installDist
```

**Install on macOS:**
```bash
brew install signal-cli
```

**Register your number:**
```bash
signal-cli -u +1234567890 register
# You'll receive SMS with verification code
signal-cli -u +1234567890 verify <CODE>
```

### Option 2: signal-cli-rest-api (Docker - Recommended)

**Run with Docker:**
```bash
docker run -d --name signal-api \
  -p 8080:8080 \
  -v $(pwd)/signal-cli-config:/home/.local/share/signal-cli \
  -e SIGNAL_CLI_HTTP_BASIC_AUTH_USER=admin \
  -e SIGNAL_CLI_HTTP_BASIC_AUTH_PASSWORD=secret123 \
  bbernhard/signal-cli-rest-api:latest
```

**Register:**
```bash
# Request verification code
curl -X POST -H "Content-Type: application/json" \
  http://localhost:8080/v1/register/+1234567890

# Verify with code from SMS
curl -X PUT -H "Content-Type: application/json" \
  http://localhost:8080/v1/register/+1234567890/verify/<CODE>
```

## Configuration

Create `.env` file or set environment variables:

```bash
# For signal-cli
SIGNAL_CLI_PATH=/usr/bin/signal-cli
SIGNAL_PHONE_NUMBER=+1234567890

# For signal-cli-rest-api
SIGNAL_API_URL=http://localhost:8080
SIGNAL_API_USER=admin
SIGNAL_API_PASSWORD=secret123
SIGNAL_PHONE_NUMBER=+1234567890
```

## Usage

### Send Message (CLI)
```bash
python3 skills/signal-messenger/lib/send_message.py \
  --to +1234567890 \
  --message "Hello from Signal!"
```

### Send Message (REST API)
```bash
python3 skills/signal-messenger/lib/send_message.py \
  --api \
  --to +1234567890 \
  --message "Hello from Signal!"
```

### Send to Group
```bash
python3 skills/signal-messenger/lib/send_message.py \
  --group <GROUP_ID> \
  --message "Group message!"
```

### Receive Messages (Polling)
```bash
python3 skills/signal-messenger/lib/receive_messages.py --poll
```

## Example Output

```
✅ Message sent to +1234567890
📱 Signal ID: 1234567890.1234567890.0
⏰ Timestamp: 2026-04-14 04:40:00 UTC
```

## Features

- ✅ Send individual messages
- ✅ Send group messages
- ✅ Send attachments (images, files)
- ✅ Receive messages (polling mode)
- ✅ Message reactions
- ✅ Read receipts
- ✅ Typing indicators

## Security Notes

1. **Phone number** - Must be verified before sending
2. **Rate limits** - Signal has anti-spam limits
3. **Attachments** - Max 100MB per file
4. **Groups** - Must be member to send
5. **Privacy** - Messages are end-to-end encrypted

## Troubleshooting

### "Not registered"
```bash
# Re-register your number
signal-cli -u +1234567890 register
signal-cli -u +1234567890 verify <CODE>
```

### "Rate limit exceeded"
Wait 1 hour before sending more messages.

### "Group not found"
Get group ID with:
```bash
signal-cli -u +1234567890 listGroups
```

### Docker container not starting
```bash
docker logs signal-api
docker restart signal-api
```

## API Endpoints (REST API)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/v1/register/+{number}` | POST | Register number |
| `/v1/register/+{number}/verify/{code}` | PUT | Verify registration |
| `/v1/send` | POST | Send message |
| `/v1/receive` | GET | Receive messages |
| `/v1/groups` | GET | List groups |
| `/v1/attachments` | POST | Upload attachment |

## Related Skills

- `telegram-notify` - Telegram notifications
- `openclaw-whatsapp` - WhatsApp integration
- `notification-hub` - Multi-channel notifications

---

*Signal is a registered trademark of Signal Foundation. This skill is not affiliated with Signal.*
