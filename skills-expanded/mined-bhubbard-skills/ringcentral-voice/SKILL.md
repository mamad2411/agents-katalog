---
name: ringcentral-voice
description: "Handling Voice calls, Call Control, and WebRTC with the RingCentral API"
---

# RingCentral Voice API Skill

This skill documents how to manage voice communications, including call routing, call control, and WebRTC integrations using the RingCentral API.

## Making and Managing Calls (RingOut)
The RingOut API connects two phone numbers. It's an easy way to initiate a call from your application without needing a SIP client.
- **Endpoint**: `POST /restapi/v1.0/account/~/extension/~/ring-out`
- **Usage**: Specify a `from` (your RingCentral number) and `to` number. RingCentral will first call your device, and upon answering, call the destination.

## Call Control API
For deeper integration, the Call Control API allows you to monitor, park, transfer, mute, or record active calls.
- **Active Calls**: Retrieve a list of active calls using `GET /restapi/v1.0/account/~/extension/~/active-calls`.
- **Actions**: Perform operations like forwarding, answering (if supported), or transferring via `POST /restapi/v1.0/account/~/telephony/sessions/{telephonySessionId}/parties/{partyId}/transfer`.

## WebRTC
Build fully-featured softphones in the browser using RingCentral's WebRTC library.
- **SDK**: RingCentral provides a WebRTC SDK that works alongside the REST API.
- **Authentication**: Requires an active session via the standard OAuth or JWT endpoints.
- **SIP Provisioning**: The REST API is used to provision a WebRTC endpoint (`POST /restapi/v1.0/client-info/sip-provision`), which provides SIP credentials and WebSocket URIs to the WebRTC client.

## Webhooks and Event Subscriptions
- To get real-time status of calls (e.g., ringing, connected, disconnected), create a webhook subscription for telephony events (`/restapi/v1.0/account/~/extension/~/telephony/sessions`).

## Best Practices
- When building Voice applications, always prioritize network reliability and implement reconnection logic for WebSockets.
- Use Call Control events instead of polling to react instantly to incoming calls.
