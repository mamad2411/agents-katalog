---
name: livekit-stream
description: "Manage WebRTC streaming rooms using LiveKit at {{LIVEKIT_HOST}}:{{LIVEKIT_PORT}}."
metadata:
  openclaw:
    emoji: "🎥"
---

# LiveKit Streaming

LiveKit is available at `ws://{{LIVEKIT_HOST}}:{{LIVEKIT_PORT}}` within the Docker network.

## Create Room

```bash
curl -X POST "http://{{LIVEKIT_HOST}}:{{LIVEKIT_PORT}}/twirp/livekit.RoomService/CreateRoom" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $LIVEKIT_API_KEY" \
  -d '{"name": "my-room", "max_participants": 10}'
```

## Tips for AI Agents

- LiveKit provides real-time audio/video streaming via WebRTC.
- Supports server-side recording, egress, and ingress.
- Agent framework enables AI agents to participate in rooms.
- Low-latency, scalable architecture suitable for production use.
