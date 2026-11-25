---
name: esp32-esp-now
description: Use when ESP32s talk to each other without a router - peers never receive, messages stop after a channel change, the payload is truncated, or the range is far shorter than the datasheet. Covers pairing, channels, encryption and long range mode.
license: MIT
---

# ESP-NOW between ESP32s

ESP-NOW is a connectionless link layer on top of Wi-Fi. There is no association,
no IP, and no retry you can rely on - which is exactly why it is fast and why its
failures are silent.

## The channel is the whole network

Every peer must be on the same Wi-Fi channel. The channel comes from the
interface: if the station connects to an AP on channel 6, ESP-NOW moves to 6 and
every peer still on 1 stops receiving. Two rules follow:

- Set the channel explicitly with `esp_wifi_set_channel()` and never let a STA
  connection change it under you.
- After any reconnect, re-add the peers. The peer list is not guaranteed across a
  channel switch.

## Payload size

250 bytes per frame, including your header. A struct with a 240 byte buffer and
four fields is already over. The send returns an error, but only if you check the
return value - the usual symptom is "the big messages never arrive".

## Encryption needs pairing, not just a key

`esp_now_set_pmk()` sets the network key; each peer still needs its own LMK
through `peer.lmk`. A peer added with `encrypt = true` and no LMK silently fails
to send. Six encrypted peers maximum, twenty unencrypted.

## Delivery is not guaranteed

The send callback tells you whether the frame was acknowledged at the link layer,
not that your application handled it. For anything that matters, add a sequence
number and an application-level ack, or accept loss.

## Long range mode

`WIFI_PROTOCOL_LR` trades throughput for sensitivity (about 250 kbit/s, roughly
-8 dB better). Both ends must enable it, and it is ESP32-only: a C3 or S3 peer
cannot hear an LR sender at all.

## Range that is shorter than the datasheet

| Symptom | Usually |
|---|---|
| one peer receives, another does not | different channel, or peer added while on another channel |
| works at 1 m, dies at 10 m | both boards in metal boxes, or antenna inside a ground plane |
| stops after Wi-Fi connects | channel changed by the AP |
| send returns OK, nothing arrives | receiver in a different Wi-Fi mode (AP-only, or modem sleep) |
| throughput collapses with more peers | broadcast frames, no ack, airtime shared |
