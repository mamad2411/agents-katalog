---
name: ios-protocol-capture
description: Use when the user wants to reverse-engineer how an iOS app talks to an external device — BLE pairing flow, WiFi commands, private protocols, the actual bytes on the wire. Captures iPhone HCI traffic (decrypted) via `idevicebtlogger` and WiFi traffic via `rvictl` + `tcpdump`, parses with `tshark`, decodes PTP-IP and Sony private opcodes. Trigger whenever the user mentions sniffing/capturing/decoding traffic between an iPhone and a Bluetooth or WiFi device (cameras, smart locks, IoT, fitness equipment, car infotainment, smart home), debugging a private protocol, looking at HCI/ATT/SMP logs, comparing what their app does vs what a vendor app does, or wants to see "real bytes" or "what's actually being sent." Also trigger when the user has a `.pcap` / `.pklg` / `.logarchive` file from an iPhone and needs it analyzed.
---

# iOS Protocol Capture & Decode

Reverse-engineering how an iOS app communicates with hardware doesn't need expensive hardware sniffers. The iPhone exposes its full Bluetooth HCI stream and full WiFi packet stream over USB, and both streams are **already decrypted** (because iOS is the endpoint of the BLE encryption / WPA2 association). This skill turns that into a reliable workflow.

The skill is structured around three jobs:

1. **Capture** — get clean BLE and/or WiFi traces with proper time alignment
2. **Decode** — turn raw pcap into a human-readable protocol timeline (especially for PTP-IP and Sony cameras, but the framework generalizes)
3. **Sanitize** — strip secrets (WiFi credentials, device IDs, third-party tokens) before sharing

## When to use which capture mode

| Scenario | Mode | Why |
|---------|------|-----|
| Reverse-engineering BLE pairing / GATT writes / SMP | BLE-only | Smaller files, faster iteration. Run `scripts/capture-ble.sh` |
| App connects to device over WiFi (HTTP, PTP-IP, custom TCP) | WiFi-only | Run `scripts/capture-wifi.sh` |
| Both — pairing handoff, BLE-triggered WiFi flows, full app↔device session | **Both, time-aligned** | Run `scripts/capture-both.sh`. Most reverse-engineering tasks land here |

Read each script before running so you understand what it does — they're short and self-contained.

## Setup (run once)

Run `scripts/check-tools.sh`. It verifies and offers to install:

- `libimobiledevice` (provides `idevicebtlogger`, `idevice_id`) via Homebrew
- `wireshark` (provides `tshark`, `capinfos`) via Homebrew
- `rvictl` is shipped by Apple at `/Library/Apple/usr/bin/rvictl` — no install needed

The user must:
- USB-connect the iPhone and tap "Trust this computer"
- For WiFi capture: have `sudo` available (rvi0 packet capture is root-only)

No Configuration Profile, no Apple Developer login, no Xcode Additional Tools. The libimobiledevice command-line stack handles authentication via the lockdown protocol when the phone is paired.

## Capture workflows

### BLE-only

```
scripts/capture-ble.sh [output.pcap]
```

Starts `idevicebtlogger -f pcap` in the foreground. The user does whatever they want to capture (open the target app, perform pairing, send commands), then Ctrl+C. The script prints the file path and packet count.

### WiFi-only

```
scripts/capture-wifi.sh [output.pcap]
```

Starts `rvictl -s <UDID>` to expose the iPhone's network stack as `rvi0`, then `sudo tcpdump -i rvi0 -s 0 -w <file>` excluding DNS/mDNS noise. Ctrl+C stops capture and tears down `rvi0`.

### Both (time-aligned)

```
scripts/capture-both.sh [output_prefix]
```

Runs BLE and WiFi captures in parallel. Both use the macOS system clock so timestamps align across files. Outputs `<prefix>_ble.pcap` and `<prefix>_wifi.pcap`.

**Time-alignment caveat**: `idevicebtlogger` uses the iPhone's clock-derived timestamp from PacketLogger. `tcpdump -i rvi0` uses the Mac's clock. They are usually within ~50ms of each other (NTP keeps both in sync), but for sub-second BLE→WiFi causality analysis, do a known-good calibration burst (open the target app once, immediately Ctrl+C, look at the offset between the BLE "ATT write" and the WiFi "TCP SYN" of the same triggering action).

## Decode

Read `references/tshark-recipes.md` for the common analysis queries. Headlines:

- Get protocol distribution: `tshark -r file.pcap -q -z io,phs`
- TCP conversations sorted by bytes: `tshark -r file.pcap -q -z conv,tcp`
- Filter only one BLE connection (multi-device noise): `bthci_acl.chandle == 0x0404`
- Decode ATT writes: `btatt.opcode == 0x12 || btatt.opcode == 0x52`
- Decode SMP pairing: `btsmp`

For **PTP-IP** (Sony, Canon, Nikon WiFi cameras), use `scripts/decode_ptp_ip.py` — it parses the standard PTP-IP frame format and includes a Sony private OpCode dictionary (0x9201 SDIOConnect, 0x9207 SDIOControlDevice, 0x9211 GetPartialObject, etc.). Pipe tshark output to it:

```
tshark -r wifi.pcap -Y "ptpip && tcp.port == 15740" \
  -T fields -e frame.time_relative -e ip.src -e tcp.payload \
  | python3 scripts/decode_ptp_ip.py
```

For protocol-specific deep dives, read the relevant reference:

- `references/ble-analysis.md` — BLE GATT services, ATT errors (incl. application errors 0x80-0x9F), SMP pairing analysis, CCCD subscriptions
- `references/wifi-analysis.md` — Common iOS-camera WiFi patterns (PTP-IP, HTTP liveview streams, mDNS/Bonjour discovery), how to identify private protocols
- `references/tools.md` — Reference for each command-line tool, including non-obvious flags
- `references/sanitization.md` — What sensitive data appears in pcaps and how to scrub it before committing

## Sanitize before sharing

iPhone HCI captures **always** contain things you don't want in a public repo:

- WiFi SSIDs and PSKs (BLE GATT reads on Sony/Canon cameras)
- Device unique IDs (`did`, `serialNumber`)
- Third-party SDK tokens (e.g., DingTalk `corpId` if you wear a smart wristband)
- Personal LAN topology (your home router IP, neighbor SSIDs from probe responses)

Before committing any pcap or sharing externally, run the steps in `references/sanitization.md`. The basic move is to filter to only the relevant BLE connection handle / WiFi peer IP using `tshark ... -w sanitized.pcap`, then grep the output for known leaks.

A `.gitignore` rule should exclude `*.pcap`, `*.pklg`, `*.logarchive`, and any `captures/` directory. The skill doesn't enforce this — the user's repo does.

## Common patterns by device type

| Device | Likely protocols | Where to start |
|--------|-----------------|---------------|
| Sony / Canon / Nikon camera | BLE (pair + WiFi creds) → WiFi (PTP-IP 15740 + private HTTP for liveview) | Both-mode capture; `decode_ptp_ip.py` |
| Smart lock / smart home | BLE GATT only (most cases), or BLE → cloud (HTTPS, opaque) | BLE-only; `references/ble-analysis.md` |
| Fitness scale / band | BLE GATT, occasionally WiFi for firmware updates | BLE-only |
| Car infotainment | BLE for pairing handshake → WiFi or USB Ethernet for CarPlay | Both-mode; expect Apple-flavored protocols |
| Generic IoT (Tuya etc.) | mDNS discovery → HTTP/MQTT over WiFi | WiFi-only |

## Output format

When the user asks for analysis, structure the response as a **timeline** with:

1. **Headline finding** — what protocol, what port, what's the surprising thing
2. **Time-stamped events** — `T+0.0s` relative to capture start, with which side initiated each action
3. **Hex payload for any non-trivial command** — let the user see the actual bytes
4. **Decoded structure** — for known protocols (PTP-IP, HTTP, ATT) include the dissected fields
5. **Open questions** — things the capture didn't clarify, suggesting follow-up captures

This is the difference between "I see some BLE traffic" and "Shutter writes `06 08 01 00 00 00` to handle 0x0104 (EE01) which returns ATT Application Error 0x90, then writes `0x01` to handle 0x003B (CC08) which triggers iOS SMP pairing". The user wants the second.

## Things that look like problems but aren't

- **`tcpdump: WARNING: rvi0: That device doesn't support promiscuous mode`** — expected. rvi0 only sees this iPhone's traffic by design. Ignore.
- **`capinfos: appears to have been cut short in the middle of a packet`** — happens if Ctrl+C interrupted a packet write. Analysis still works.
- **Packets you expected aren't in the pcap** — confirm the iPhone was on the right network. If you expected camera DIRECT-AP traffic but the iPhone stayed on home WiFi, the camera-bound traffic isn't on rvi0 at all (it physically can't be sent). Capture again after confirming the iPhone is associated.
- **A second BLE device's traffic mixed in** — iPhone may have your watch, AirPods, smart wristband, etc. all active. Filter by `bthci_acl.chandle` after identifying which handle corresponds to the device under study (look at the LE Connection Complete event right after the target's BD_ADDR shows up).
