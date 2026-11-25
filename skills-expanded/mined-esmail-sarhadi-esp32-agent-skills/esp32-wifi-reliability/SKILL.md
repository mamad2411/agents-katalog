---
name: esp32-wifi-reliability
description: Use when an ESP32 drops off Wi-Fi, reconnects in a loop, is slow to respond, or works on the bench and fails in the field. Covers reconnect storms, power save, AP+STA, and what the RSSI actually tells you.
license: MIT
---

# Wi-Fi that stays connected

An ESP32 that connects once is easy. One that is still connected after a week,
after a router reboot, and after the neighbour bought a new access point is a
different problem, and it is almost always the reconnect logic.

## The reconnect loop

The Arduino core already has a reconnect mechanism. Turning on your own as well
produces two reconnects racing each other, which looks like a board that
connects and drops every few seconds.

- Let the core handle it: `WiFi.setAutoReconnect(true)`.
- Do not call `WiFi.begin()` in a tight loop. Each call tears down the state
  machine and starts over, and you will never get past association.
- When you do retry, back off: 1s, 2s, 5s, 15s, 30s, then stay at 30s. A board
  retrying every 200 ms keeps the radio busy and drains the battery.
- `WiFi.persistent(false)` before `begin()` stops the core writing credentials
  to flash on every connection. On a board that reconnects constantly, that
  write is what eventually kills the flash.

## Power save is a latency setting

By default the radio sleeps between beacons, which saves a lot of power and adds
up to a few hundred milliseconds of latency.

```cpp
WiFi.setSleep(false);   // responsive, and hungrier
```

- For a sensor that wakes every five minutes, leave power save on.
- For anything that answers a request (web server, MQTT command handler), turn
  it off and budget the current.
- Never turn it off "just in case" on a battery device. Measure first.

## AP+STA is not free

`WIFI_AP_STA` runs two interfaces on one radio. It works, but:

- The AP and the station share the same channel as the station's connection.
- Throughput on both drops noticeably.
- The radio never sleeps, so a battery-powered AP+STA node is not a thing.

Use it for provisioning (open an AP, take credentials, close the AP) rather than
as a permanent mode.

## What RSSI tells you, and what it does not

| RSSI | Reality |
|---|---|
| -50 to -60 | strong, nothing to fix |
| -67 | the usual threshold for "fine" |
| -70 to -75 | marginal: retries climb, latency spikes |
| below -80 | association problems, and TLS handshakes start failing |

A fluctuating RSSI with a strong average means interference or a crowded
channel, not distance. Check the channel before adding an antenna.

## Symptoms and their usual cause

- **Connects, then drops after 10-60 seconds.** Often a DHCP or DNS failure, or
  the router rejecting the device for too many associations. Check the DHCP
  lease count on the router.
- **Works at home, fails at the customer site.** Enterprise Wi-Fi with a captive
  portal or WPA2-Enterprise. The Arduino core does not do a portal.
- **Connects but nothing resolves.** DNS. Try an IP address before blaming the
  server.
- **Fine until a second device is added.** Channel congestion, or the router's
  client limit.

## Rules for the agent

- Never write a `while (WiFi.status() != WL_CONNECTED) { delay(500); }` that can
  spin forever. Bound it, and say what happens when the bound is reached.
- Log the disconnect reason (`WiFi.onEvent` with `ARDUINO_EVENT_WIFI_STA_DISCONNECTED`).
  The reason code names the cause; without it you are guessing.
- When a user says "it disconnects", ask for the disconnect reason and the RSSI
  before changing code.
