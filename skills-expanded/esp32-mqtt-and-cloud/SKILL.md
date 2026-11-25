---
name: esp32-mqtt-and-cloud
description: Use when an ESP32 publishes to MQTT, talks to a cloud endpoint, or drops messages. Covers the 256 byte buffer that silently truncates payloads, keepalive and last will, TLS memory, and why QoS 0 loses data.
license: MIT
---

# MQTT and cloud endpoints from ESP32

The failures here are quiet. A payload over the buffer size is not sent, a
message at QoS 0 is not retried, and a TLS connection that cannot allocate its
buffers fails in a way that reads like a network problem.

## The buffer that eats your payload

`PubSubClient` has a fixed packet buffer. The long-standing default is 256
bytes, and anything larger is silently dropped - `publish()` returns `false` and
a lot of code ignores that return value.

```cpp
// ArduinoJson payloads grow fast: 20 sensors in one document is not 256 bytes.
client.setBufferSize(1024);   // must be called before connect()
```

Two things people get wrong:

- `setBufferSize` only takes effect on the **next** connection. Set it, then
  connect.
- The buffer is allocated in RAM per client. On a classic ESP32 with a few tens
  of KB of heap, 4 KB is a real cost, not a free knob.

## Keepalive and last will

- Keepalive is a promise: if the broker hears nothing for 1.5x the interval, it
  considers the client dead. Too long and a dead node looks alive; too short and
  a slow reconnect flaps the topic.
- The **last will** is the only reliable way to tell the world a node died. Set
  it to a payload like `offline` on a status topic, with `retain = true`. A node
  that only publishes `online` on connect leaves the last `online` retained
  forever after a power cut.
- `client.loop()` must be called often enough to service the keepalive. A sketch
  that blocks for 10 seconds in `loop()` will be disconnected by the broker, and
  the code will look correct.

## QoS, honestly

- **QoS 0** is fire and forget. It is right for a sensor reading you will take
  again in 30 seconds, and wrong for anything you cannot recompute.
- **QoS 1** is at least once: duplicates are possible, so the receiver must be
  idempotent. On a constrained device this is usually the right choice.
- **QoS 2** costs a four-way handshake per message and is rarely worth it on a
  microcontroller.
- `retain` is not a queue. It stores the last message for new subscribers; it
  does not deliver missed ones.

## TLS on a microcontroller

- A TLS session needs tens of kilobytes of RAM, and the handshake is the peak.
  On a classic ESP32 that is a significant slice of the heap.
- `WiFiClientSecure::setInsecure()` skips certificate validation. It is fine for
  a demo and wrong for anything that matters: it accepts any certificate,
  including the one from whoever is intercepting the traffic.
- The correct middle ground is pinning the CA or the public key, not disabling
  validation.
- A handshake that fails with an allocation error is a memory problem, not a
  certificate problem. Check the free heap before the connect.

## Rules for the agent

- Always check the return value of `publish()`. If the payload can exceed the
  buffer, say so and size the buffer explicitly.
- When adding a device that publishes status, add a retained last will in the
  same commit. A status topic without one lies after the first power cut.
- Do not put a blocking `delay()` inside the publish path. It starves
  `client.loop()` and the broker disconnects you.
- If a user reports missing messages, ask which QoS they use before anything
  else. QoS 0 losing messages is not a bug.
