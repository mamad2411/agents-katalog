---
name: supercall
description: Make AI-powered phone calls with custom personas and goals. Uses OpenAI Realtime API + Twilio for ultra-low latency voice conversations. Use when you need to call someone, confirm appointments, deliver messages, or have the AI handle phone conversations autonomously. Unlike the standard voice_call plugin, the person on the call doesn't have access to gateway agent, reducing attack surfaces.
homepage: https://github.com/xonder/supercall
metadata:
  {
    "openclaw":
      {
        "emoji": "📞",
        "requires": { "plugins": ["supercall"] },
        "install":
          [
            {
              "id": "npm",
              "kind": "plugin",
              "package": "@xonder/supercall",
              "label": "Install supercall plugin (npm)",
            },
          ],
      },
  }
---

# SuperCall

Make AI-powered phone calls with custom personas and goals using OpenAI Realtime API + Twilio.

## Features

- **Persona Calls**: Define a persona, goal, and opening line for autonomous calls
- **Full Realtime Mode**: GPT-4o powered voice conversations with <~1s latency
- **Provider**: Supports Twilio (full realtime) and mock provider for testing
- **Streaming Audio**: Bidirectional audio via WebSocket for real-time conversations
- **Limited Access**: Unlike the standard voice_call plugin, the person on the call doesn't have access to gateway agent, reducing attack surfaces.

## Installation

1. Copy this skill to your OpenClaw skills directory
2. **Enable hooks** for call completion callbacks (required):

```json
{
  "hooks": {
    "enabled": true,
    "token": "your-secret-token"
  }
}
```

Generate a token with: `openssl rand -hex 24`

3. Configure the plugin in your openclaw config:

```json
{
  "plugins": {
    "entries": {
      "supercall": {
        "enabled": true,
        "config": {
          "provider": "twilio",
          "fromNumber": "+15551234567",
          "twilio": {
            "accountSid": "your-account-sid",
            "authToken": "your-auth-token"
          },
          "streaming": {
            "openaiApiKey": "your-openai-key"
          },
          "tunnel": {
            "provider": "ngrok",
            "ngrokDomain": "your-domain.ngrok.app"
          }
        }
      }
    }
  }
}
```

**Important**: The `hooks.token` is required for call completion callbacks. Without it, the agent won't be notified when calls finish.

## Tool: supercall

Make phone calls with custom personas:

```
supercall(
  action: "persona_call",
  to: "+1234567890",
  persona: "Personal assistant to the king",
  goal: "Confirm the callee's availabilities for dinner next week",
  openingLine: "Hey, this is Michael, Alex's Assistant..."
)
```

### Actions

- `persona_call` - Start a new call with a persona
- `get_status` - Check call status and transcript
- `end_call` - End an active call
- `list_calls` - List active persona calls

## Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `provider` | Voice provider (twilio/mock) | Required |
| `fromNumber` | Caller ID (E.164 format) | Required for real providers |
| `toNumber` | Default recipient number | - |
| `streaming.openaiApiKey` | OpenAI API key for realtime | OPENAI_API_KEY env |
| `streaming.silenceDurationMs` | VAD silence duration in ms | 800 |
| `streaming.vadThreshold` | VAD threshold 0-1 (higher = less sensitive) | 0.5 |
| `streaming.streamPath` | WebSocket path for media stream | /voice/stream |
| `tunnel.provider` | Tunnel for webhooks (ngrok/tailscale-serve/tailscale-funnel) | none |

Full realtime requires an OpenAI API key.

## Requirements

- Node.js 20+
- Twilio account for full realtime calls (media streams)
- ngrok or Tailscale for webhook tunneling (production)
- OpenAI API key for real-time features

## Architecture

This is a fully standalone skill - it does not depend on the built-in voice-call plugin. All voice calling logic is self-contained.
