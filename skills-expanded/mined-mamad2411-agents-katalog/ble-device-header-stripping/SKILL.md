---
name: ble-device-header-stripping
description: Strip fixed firmware headers from BLE audio packets, emit headerless payloads downstream, and reuse the header bytes as a sync key for write-ahead-log frame alignment.
category: ble-audio-streaming
version: 1.0.0
version_origin: extracted
confidence: high
tags: [ble, audio-source, opus, wal, wearable, flutter]
source_type: extracted-from-git
source_url: https://github.com/BasedHardware/omi.git
source_ref: main
source_commit: 1c310f7fc4c37acf7e1bedb014e3a4adfd56546e
source_project: omi
imported_at: 2026-04-18T00:00:00Z
---

# BLE Audio Source with Header Stripping and WAL Sync Keys

A clean abstraction for ingesting audio from BLE wearables where each packet prepends a small firmware header (packet id / sequence index). The `AudioSource` interface separates framing (sync + dedup) from payload (what actually reaches the codec / socket).

## When to use

- Custom BLE audio device streams Opus/PCM over a characteristic with a small firmware-supplied header.
- You maintain a local WAL (write-ahead-log) of audio frames for offline resync and need a stable per-frame sync key.
- You want to swap devices (Omi vs. OpenGlass vs. phone mic) without rewriting the transport layer.

## Core pattern

```
raw BLE bytes  ─►  AudioSource.processBytes()  ─►  [WalFrame(payload, syncKey)]
                                              ─►  getSocketPayload()  ─►  backend WebSocket
```

- **Header format** (Omi / OpenGlass): `[packet_id_low, packet_id_high, packet_index]` — 3 bytes prefix.
- **`processBytes(rawBytes)`** returns `List<WalFrame>` (typically one entry) with `payload = rawBytes.sublist(3)` and `syncKey = FrameSyncKey.fromBleHeader(rawBytes)`.
- **`getSocketPayload(rawBytes)`** returns the headerless bytes for the live socket (skip if ≤ 3 bytes — malformed packet).
- **`flush()`** returns any buffered partial frames at end of stream.

## Steps

1. Define an `AudioSource` interface with `{codec, deviceId, deviceModel, processBytes, getSocketPayload, flush}`.
2. Implement per-device (`BleDeviceSource`, `PhoneMicSource`, `FileSource`) — header stripping lives only in `BleDeviceSource`.
3. Downstream consumers (WAL writer + WebSocket sender) depend on the interface, not the device.
4. On each BLE notification:
   - `final frames = source.processBytes(bytes); walService.write(frames);`
   - `final payload = source.getSocketPayload(bytes); socket.add(payload);`
5. On device disconnect: `final tail = source.flush(); walService.write(tail);`

## Implementation notes

- Keep the header constant (`headerSize = 3`) on the class — makes it easy to bump per firmware rev.
- Never pass raw BLE bytes to the backend socket; always go through `getSocketPayload()` so the codec on the server side sees clean Opus/PCM.
- `FrameSyncKey.fromBleHeader` should hash the 3-byte header into a stable key that survives reconnects — use it to dedupe when the same packet arrives via SD-card replay and live stream.
- Guard against short packets: `rawBytes.length <= headerSize` → return empty list (no payload, no frame).
- If firmware later adds CRC bytes at the tail, extend the source (not the consumer) to trim them.

## Evidence in source

- `app/lib/services/audio_sources/ble_device_source.dart` — header stripper + sync key
- `app/lib/services/audio_sources/audio_source.dart` — interface definition
- `backend/routers/transcribe.py` — downstream ingestion (payload is header-free)

## Reusability

Generalizes to any BLE / custom-protocol audio device (Oura-style wearables, ESP32 BLE mics) where firmware adds metadata bytes and you need both a live stream and a retry-safe WAL buffer.
