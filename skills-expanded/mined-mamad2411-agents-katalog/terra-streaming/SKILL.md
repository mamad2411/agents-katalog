---
name: terra-streaming
description: Best practices for the Terra API Streaming (Real-Time) API – live, roughly per-second biometric data from wearables over websockets. Use when building realtime streaming with Terra API, TerraRT SDKs, or wss://ws.tryterra.co; streaming live heart rate, steps, distance, acceleration, ECG, HRV, calories, location, or gyroscope; pairing a wearable over BLE or ANT+; producing sensor data from a mobile app; consuming a live stream on a backend; or streaming from an Apple Watch or Wear OS watch. Covers the producer/broker/consumer architecture, the websocket handshake and opcodes, token minting, close codes, replay/backfill, and per-platform SDK setup (iOS, Android, React Native, Flutter, Wear OS).
license: MIT
compatibility: Requires network access to docs.tryterra.co for the full websocket protocol reference
metadata:
  author: terra
  version: "1.0.0"
---

# Terra API Streaming Best Practices

Guidelines for building on the Terra API Streaming (Real-Time) API, which delivers live, roughly per-second metrics from wearables. This skill carries the architecture and the protocol gotchas inline; platform setup and the full consumer protocol live in `references/`.

## Streaming vs Health & Fitness

The Streaming API is for realtime, sub-second-to-per-second signals only: heart rate, steps, distance covered, acceleration, ECG, HRV, calories, location, and gyroscope. Anything with a longer span – workouts, sleep, daily totals, body, nutrition – belongs to the [Health & Fitness API](https://docs.tryterra.co/health-and-fitness-api/getting-started), not here. If you need a completed workout summary rather than a live feed, you are on the wrong API.

Devices only appear on the stream when they actually broadcast over BLE, ANT+, or a supported custom Bluetooth protocol (heart-rate straps like the Polar H10 or Wahoo TICKR, and some watches). No broadcast means no stream.

## Architecture: producer, broker, consumer

Realtime streaming has four parts and you build three connections between them. See [getting-started](https://docs.tryterra.co/streaming-api/getting-started).

1. **Wearable** – the strap, watch, or sensor, broadcasting over BLE or ANT+.
2. **Producer** – your mobile app, running a Terra Real-Time (RT) SDK. It receives the wearable's data and forwards it to the Terra API.
3. **Terra API WebSocket broker** – the server that routes the live stream. This is Terra API infrastructure; you never host it.
4. **Consumer** – your backend, which connects to the broker and receives the stream.

The three connections you build:

- **Wearable to app**: the user pairs their wearable to your app over Bluetooth/ANT+ using an RT SDK.
- **App to broker**: your app opens a _producer_ connection and forwards the wearable's data.
- **Broker to backend**: your backend opens a _consumer_ connection and receives the data live.

You identify a user by your own `reference_id`. The Terra API mints a Terra user ID for that user (no auth widget needed); that ID is what the token endpoints take and what arrives as the `uid` field on every payload.

## Tokens

Every websocket connection authenticates with a short-lived token minted by your backend from your Dev ID and API key. **All three tokens are single-use** – the server deletes each one after a successful IDENTIFY, so every reconnect needs a freshly minted token. Never ship your API key into the app; mint tokens server-side and hand them off.

| Token                | Endpoint                                                   | Used by                                                     | IDENTIFY type     |
| -------------------- | ---------------------------------------------------------- | ----------------------------------------------------------- | ----------------- |
| Phone-registration   | `POST https://api.tryterra.co/v2/auth/generateAuthToken`   | RT SDK `initConnection` (registers the phone as a producer) | n/a (SDK-managed) |
| Producer             | `POST https://ws.tryterra.co/auth/user?id=<terra_user_id>` | producer connection sending data                            | 0 (USER)          |
| Consumer / developer | `POST https://ws.tryterra.co/auth/developer`               | your backend consumer                                       | 1 (DEVELOPER)     |

Note the hosts: only `generateAuthToken` lives on the main API (`api.tryterra.co`). The producer and consumer token endpoints are served over HTTPS by the websocket host (`ws.tryterra.co`) and do **not** exist on `api.tryterra.co`. For the exact request/response schemas, fetch [the REST endpoints reference](https://docs.tryterra.co/reference/streaming-api/api-endpoints.md) when building the request.

The phone-registration token is single-use and **expires 3 minutes** after minting (returned as `expires_in`), so mint it just-in-time – when the app is about to call `initConnection`, not at app startup or ahead of a queue. The producer endpoint needs the Terra user ID in the `id` query parameter; retrieve it from the SDK's `getUserId`.

## The websocket

There is one endpoint for both roles: `wss://ws.tryterra.co/connect`. The IDENTIFY `type` field (0 producer, 1 consumer) decides which role the connection plays. The SDKs open and drive the producer connection for you; you write the consumer connection by hand against the walkthrough in [references/consumer-protocol.md](references/consumer-protocol.md).

The protocol is opcode-framed: HELLO and heartbeats, then IDENTIFY and READY, then DISPATCH data payloads, with REPLAY for backfill (SUBMIT is producer-side and SDK-abstracted). For the full opcode table and exact JSON payload shapes, fetch [terra-greater-than-your-backend.md](https://docs.tryterra.co/streaming-api/terra-greater-than-your-backend.md) when writing the frames.

## Protocol gotchas

These are the things that bite. The step-by-step consumer walkthrough is in [references/consumer-protocol.md](references/consumer-protocol.md).

- **IDENTIFY within 15 seconds** of connecting or the server closes with **4000**.
- **Tokens are deleted after a successful IDENTIFY.** A dropped connection cannot reuse its token; mint a fresh one before reconnecting.
- **Heartbeats.** HELLO carries `heartbeat_interval` (ms). Send the first heartbeat after `heartbeat_interval * jitter` (jitter random in 0..1), then at most once per interval. If you get no HEARTBEAT_ACK, close and reconnect. If the server sees no heartbeat within the window it closes with **4005**.
- **Close codes split into two groups.** 4000, 4003, 4004, and 1003 signal a client bug – fix the client, do not retry-loop, since a blind reconnect just loops on the same error. 4001 means mint a fresh token. 4002 means the server's consumer session cap rejected the connection – do not architect around any guaranteed number of concurrent consumers; on 4002, close an existing session or back off rather than retry-looping.
- **`seq` is monotonic but sparse.** Gaps between consecutive sequence numbers are normal and do not mean lost data. Use `seq` only to order DISPATCHes and as the `after` bound for replay.
- **REPLAY takes exclusive bounds; send both.** `after` and `before` are both required – a REPLAY that omits `before` returns no messages. On reconnect, set `after` to the last `seq` you processed and `before` to the `seq` of the first live DISPATCH to backfill exactly the gap.
- **Replay lags a few seconds.** A payload becomes replayable a few seconds after it was delivered live. If a REPLAY returns fewer messages than expected, wait a moment and request again.
- **Test without hardware.** From the Streaming page of the [Terra dashboard](https://dashboard.tryterra.co/dashboard/streaming), create a test user; the Terra API streams synthetic live data through the real API so you can validate a consumer end to end before touching a device.
- **Re-init the RT SDK on every app open or foreground.** Producer registration does not survive backgrounding.
- **Apple Watch records at reduced frequency outside a workout session.** Start a workout session on the watch to capture data at the highest frequency.

## References

Read the reference for the surface you are building.

- [references/consumer-protocol.md](references/consumer-protocol.md) – **read this before writing the backend consumer.** The handshake walkthrough (HELLO, heartbeats, IDENTIFY, READY, DISPATCH), DISPATCH field semantics, the REPLAY backfill recipe, and close-code handling, with pointers to the live doc for exact payload shapes.
- [references/ios.md](references/ios.md) – read when the producer app is native iOS or you are wiring an Apple Watch. Apple Developer Program membership is required.
- [references/android.md](references/android.md) – read when the producer app is native Android, including ANT+ and programmatic device scans.
- [references/react-native.md](references/react-native.md) – read when the producer app is React Native.
- [references/flutter.md](references/flutter.md) – read when the producer app is Flutter (note the `startRealtimeToApp` vs `startRealtimeToServer` split).
- [references/wear-os.md](references/wear-os.md) – read when streaming from a Wear OS watch paired to an Android phone.

Full docs: [docs.tryterra.co/streaming-api](https://docs.tryterra.co/streaming-api/getting-started) (append `.md` to any docs URL for a markdown version). If the terra-docs MCP server (`https://docs.tryterra.co/~gitbook/mcp`) is connected, use its tools to search and fetch the docs instead.

## Decisions that are yours to make

The docs deliberately leave these open; pick what fits your app rather than assuming a default:

- **Which data types to stream.** You pass the set of types to the SDK; stream only what you use.
- **Device-scan caching.** Flags like `useCache` and `showWidgetIfCacheNotFound` (Android) trade a faster reconnect to a known device against always showing the picker.
- **Local-only vs server streaming.** Streaming to your app locally and streaming to the broker are separate choices. Flutter forces the split explicitly: `startRealtimeToApp` (local callback only) vs `startRealtimeToServer` (broker only). On other platforms the same `startRealtime` call streams to the broker when you pass a token.
- **Token hand-off.** How the app fetches a producer token from your backend (endpoint shape, auth) is up to you.
- **Reconnect and backfill strategy.** How aggressively you reconnect, whether you replay on every drop, and how you persist the last processed `seq` are your call.
- **Consumer topology.** One consumer fanning out internally vs several is your architecture (subject to the session cap).
- **`reference_id` scheme.** What your `reference_id` maps to in your own system.
