---
name: wireless-probe
description: Use when assessing declared wireless/RF targets under an engagement contract (Wi-Fi capture analysis, handshake conversion, BLE/SDR signal review, RFID). Routes to extensions/offsec-tools/wrapper.py tools: aircrack-ng, hcxdumptool, hcxtools, kismet, bettercap, hashcat, urh. Offline analysis needs no hardware; capture/inject needs usbipd-win passthrough.
triggers: [user, model]
---

# Wireless Probe

Wireless/RF assessment under contract, via
`extensions/offsec-tools/wrapper.py` (domain `wireless`).

## Contract (mandatory)

`--target` (SSID/BSSID, capture path, or device), `--window`, `--roe`.
ROE states band/channel scope and whether deauth/injection is permitted.

## Tools

| Tool | Mode | Tier | Use |
|---|---|---|---|
| `hcxtools` | passive | wsl2-ready | offline pcap -> hash conversion |
| `aircrack-ng` | active | wsl2-fragile | WEP/WPA analysis; monitor mode needs USB adapter |
| `hcxdumptool` | active | wsl2-fragile | PMKID/handshake capture (usbipd-win required) |
| `kismet` | active | wsl2-fragile | wireless IDS/capture |
| `bettercap` | active | wsl2-fragile | Wi-Fi/BLE/MITM workflows |
| `hashcat` | destructive | wsl2-gated | offline hash recovery; GPU-heavy |
| `urh` | passive | wsl2-fragile | SDR signal analysis |

## Platform reality (Windows + WSL2)

- Offline analysis (pcap conversion, hash cracking, signal review):
  works in WSL2 without hardware.
- Live capture/injection: requires a USB Wi-Fi adapter with monitor
  mode + `usbipd-win` attach into WSL2; built-in NICs cannot do this.
- SDR/RFID (HackRF, Proxmark3): USB passthrough per device, verify per
  device before promising capability.
- No adapter attached = `unsupported_platform`-equivalent: report the
  limitation, do not fake capture.

## Commands

```bash
W=extensions/offsec-tools/wrapper.py

python $W run --tool hcxtools --target cap.pcapng --window "..." \
  --roe "..." --backend wsl -- -o out.hc22000 cap.pcapng
python $W run --tool aircrack-ng --target cap.ivs --window "..." \
  --roe "..." --confirm --backend wsl -- cap.ivs
python $W run --tool hashcat --target out.hc22000 --window "..." \
  --roe "..." --confirm -- -m 22000 out.hc22000 wordlist.txt
```

`hashcat` is `mode: destructive` (resource-heavy, denial risk on shared
hosts) -- always `--confirm` and scope the run duration in ROE.

## Evidence

Per finding: capture provenance (interface, adapter, timestamp), tool
version, hash/verifier for artifacts, confidence. Handshake captures are
evidence only when the capture chain is documented.

## Boundaries

- Declared BSSIDs only; ambient networks are out of scope.
- Deauth/jamming only with an explicit ROE line.
- No harvesting of client credentials (enterprise PSK capture of
  in-scope APs is itself the declared objective when in ROE).
