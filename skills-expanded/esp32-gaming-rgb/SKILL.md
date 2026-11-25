---
name: esp32-gaming-rgb
description: Use when making an ESP32 LED strip appear inside a gaming lighting app such as OpenRGB or SignalRGB, or when the lighting lags behind the screen or the music.
license: MIT
---

# Gaming RGB from an ESP32

Desktop lighting apps expect a device they can enumerate and push colours to.
An ESP32 is not one of those by default, so the work is a bridge: implement the
protocol the app speaks, and be honest about latency.

The constants below are taken from the OpenRGB reference client
(`openrgb-python`, `openrgb/utils.py`), not from memory. Check them again if you
target a newer protocol version.

## OpenRGB SDK, the part that matters

OpenRGB's SDK server is a plain TCP server. A device that implements it appears
in the OpenRGB device list with no plugin and no driver.

| Fact | Value |
|---|---|
| Default port | `6742` |
| Header | 16 bytes |
| Header layout | 4 magic bytes `ORGB`, then three little-endian `uint32`: device index, packet type, payload size |
| Protocol version to report | `4` |

Packet types you must handle to be usable:

| Value | Name | What to answer |
|---|---|---|
| `0` | `REQUEST_CONTROLLER_COUNT` | one `uint32`: how many devices you expose |
| `1` | `REQUEST_CONTROLLER_DATA` | the device descriptor (name, vendor, zones, LEDs, modes) |
| `40` | `REQUEST_PROTOCOL_VERSION` | one `uint32`: `4` |
| `50` | `SET_CLIENT_NAME` | nothing |
| `1050` | `RGBCONTROLLER_UPDATELEDS` | the payload is `uint32 size` then `size/3` RGB triples |
| `1100` | `RGBCONTROLLER_SETCUSTOMMODE` | nothing, but remember you are now taking colours |

Note the trap: the *packet type* for asking the protocol version is `40`, while
the *version value* you answer with is `4`. Mixing those up makes clients hang
waiting for a reply they can parse.

The descriptor is length-prefixed strings and fixed-width integers in a specific
order. Do not invent it: read the struct sequence from the reference client and
follow it field by field, because a single wrong `uint16` shifts everything
after it and the client shows a garbled device instead of an error.

## SignalRGB

SignalRGB has no open SDK for third-party devices. The practical routes are:

- Speak the **WLED protocol** and register as a WLED device, or
- Speak a supported USB HID protocol (Razer, Corsair) over a wired link.

Over Wi-Fi, the WLED-compatible route is the one that works, and it is what the
existing community shims do. Do not promise native SignalRGB support over
network without one of those two.

## Latency, honestly

- Wi-Fi power save adds latency spikes in the hundreds of milliseconds. Call
  `WiFi.setSleep(false)` for a lighting device, and say so, because it costs
  power.
- A Wi-Fi round trip is roughly 5-30 ms on a clean network. That is fine for
  ambient colour and wrong for music reactivity.
- For screen or audio sync, wired (USB serial, or a DDP stream over Ethernet) is
  the only honest answer. Say that instead of shipping a laggy demo.
- Keep the LED refresh out of the network task. Receive a frame into a buffer,
  then let the LED task render it; a blocking `show()` inside the socket handler
  stalls the connection.

## Rules for the agent

- State the protocol and port explicitly in the README. "Works with OpenRGB" is
  not a specification; "implements the OpenRGB SDK server on TCP 6742, protocol
  version 4" is.
- Test with the reference client before claiming compatibility, and paste the
  client output as proof.
- Never claim SignalRGB support without naming which protocol you speak.
- If the user asks for audio-reactive lighting over Wi-Fi, explain the latency
  budget before writing the code. It is a design constraint, not a bug to fix
  later.
