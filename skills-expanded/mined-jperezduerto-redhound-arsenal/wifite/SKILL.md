---
name: wifite
description: >
  Build, extend, and operate Wifite — an automated wireless auditing tool for WPA/WPA2,
  WPS, PMKID, and WEP attacks. Use when the user needs to audit wireless networks, capture
  handshakes, perform PMKID attacks, crack WPS PINs, or run automated Wi-Fi assessments.
  Covers installation, target selection, WPA handshake capture, PMKID attacks, WPS attacks,
  WEP cracking, custom wordlists, monitor mode management, and comparison with manual
  aircrack-ng workflow for professional wireless penetration testing engagements.
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/derv82/wifite2
  stars: '6.8k'
---

# wifite Agent Skill

## When to Use This Skill

Use this skill when:
- The user is performing a wireless penetration test and needs automated handshake capture
- Auditing WPA/WPA2, WPS, or WEP networks in scope
- The user wants PMKID attacks without deauthentication (clientless)
- Setting up Wifite with custom wordlists and attack parameters
- The user asks how Wifite compares to the manual aircrack-ng suite workflow

## What Wifite Does

Wifite2 is a complete rewrite of the original Wifite, designed to automate the entire wireless attack workflow: putting the adapter into monitor mode, scanning for targets, capturing handshakes or PMKID hashes, and optionally cracking them with a wordlist. It chains aircrack-ng, hcxdumptool, hcxtools, hashcat, and Pyrit. The project has ~6.8k GitHub stars.

## Installation

### Kali Linux (apt — recommended)
```bash
sudo apt update && sudo apt install -y wifite
wifite --version
```

### From Source (latest features)
```bash
git clone https://github.com/derv82/wifite2.git /opt/wifite2
cd /opt/wifite2
sudo python3 setup.py install
# Or run directly:
sudo python3 wifite.py --help
```

### pip
```bash
pip3 install wifite
```

### Dependencies
```bash
sudo apt install -y \
  aircrack-ng \
  hcxdumptool \
  hcxtools \
  hashcat \
  reaver \
  bully \
  pixiewps \
  pyrit \
  tshark

# Verify wireless tools
iwconfig
airmon-ng
```

### Wireless Adapter Requirement
Wifite requires a wireless adapter that supports monitor mode and packet injection:
- Recommended: Alfa AWUS036ACS (AC600, 802.11ac), Alfa AWUS036ACH
- Supported chipsets: Atheros (ath9k_htc), Realtek (rtl8812au), Ralink (rt2800usb)
- Test injection support: `aireplay-ng --test <interface>`

## Core Concepts

### Monitor Mode Management
Wifite automatically puts the adapter into monitor mode and restores it afterward:
```bash
# Wifite manages this, but you can also do it manually
airmon-ng check kill          # Kill interfering processes
airmon-ng start wlan0         # Start monitor mode → creates wlan0mon
# After Wifite:
airmon-ng stop wlan0mon
service NetworkManager start
```

### Attack Types
| Attack | Target | Requirement |
|--------|--------|-------------|
| WPA Handshake | WPA/WPA2 | Client must be connected (deauth triggers reconnect) |
| PMKID | WPA/WPA2 | No client required (AP-side capture) |
| WPS PIN | WPS-enabled | Reaver or Bully; very slow |
| WPS Pixie-Dust | WPS-enabled | Pixiewps; fast if AP vulnerable |
| WEP | WEP (legacy) | Traffic injection required |

### Output Files
```
~/.wifite/                   Default output directory
  hs/                        WPA handshakes (.cap files)
  pmkid/                     PMKID hashes (.22000 format for hashcat)
  wps/                       WPS PINs
```

## CLI Reference

### Basic Usage
```bash
# Start Wifite (interactive scan — select targets from list)
sudo wifite

# Specify interface explicitly
sudo wifite -i wlan0

# Use wlan0mon if already in monitor mode
sudo wifite -i wlan0mon
```

### Target Selection
```bash
# Target by ESSID (network name)
sudo wifite --essid "TargetNetwork"

# Target by BSSID (AP MAC address)
sudo wifite --bssid AA:BB:CC:DD:EE:FF

# Target by channel
sudo wifite --channel 6

# Target by BSSID + channel (fastest lock-on)
sudo wifite --bssid AA:BB:CC:DD:EE:FF --channel 11

# Multiple BSSIDs (comma-separated, not natively supported — use scan and select)
sudo wifite --essid "Corp-WiFi"
```

### WPA/WPA2 Handshake Capture
```bash
# WPA capture only (no PMKID, no WPS)
sudo wifite --wpa --no-pmkid --no-wps \
  --bssid AA:BB:CC:DD:EE:FF \
  --channel 6

# Set deauth packets count (default: 1 deauth frame burst)
sudo wifite --wpa --deauth-count 5 \
  --bssid AA:BB:CC:DD:EE:FF

# Timeout per target before moving on (seconds)
sudo wifite --wpa --timeout 60 \
  --bssid AA:BB:CC:DD:EE:FF

# Capture handshake then crack immediately with wordlist
sudo wifite --wpa --dict /usr/share/wordlists/rockyou.txt \
  --bssid AA:BB:CC:DD:EE:FF --channel 6
```

### PMKID Attack (clientless)
```bash
# PMKID attack only (no deauth needed — works without any clients connected)
sudo wifite --pmkid --no-wpa --no-wps \
  --bssid AA:BB:CC:DD:EE:FF

# PMKID with hashcat cracking
sudo wifite --pmkid --dict /opt/wordlists/cewl_corp.txt \
  --bssid AA:BB:CC:DD:EE:FF

# PMKID capture only (no cracking), save hash manually
sudo wifite --pmkid --no-crack \
  --bssid AA:BB:CC:DD:EE:FF
# Hash saved to ~/.wifite/pmkid/*.22000
```

### WPS Attacks
```bash
# WPS PIN attack with Reaver (slow, ~2-10 hours per AP)
sudo wifite --wps --no-wpa --no-pmkid \
  --bssid AA:BB:CC:DD:EE:FF --channel 6

# Pixie-Dust attack (fast, seconds if AP vulnerable)
sudo wifite --wps-pixie --no-wpa --no-pmkid \
  --bssid AA:BB:CC:DD:EE:FF

# WPS only with Bully instead of Reaver
sudo wifite --wps --bully --bssid AA:BB:CC:DD:EE:FF

# WPS timeout per attempt
sudo wifite --wps --wps-timeout 300 --bssid AA:BB:CC:DD:EE:FF
```

### WEP Attacks
```bash
# WEP cracking (legacy networks)
sudo wifite --wep --bssid AA:BB:CC:DD:EE:FF --channel 6

# WEP with ARP replay injection
sudo wifite --wep --require-fakeauth \
  --bssid AA:BB:CC:DD:EE:FF --channel 6
```

### Signal Strength Filter
```bash
# Only target APs with signal strength >= -70 dBm (closer targets)
sudo wifite --power 70

# Very close targets only (strong signal, better injection)
sudo wifite --power 80
```

### Wordlists and Cracking
```bash
# Custom wordlist for WPA cracking
sudo wifite --dict /opt/wordlists/custom.txt

# Multiple wordlists (chain them — Wifite takes one path; pre-merge)
cat /usr/share/wordlists/rockyou.txt \
    /opt/wordlists/cewl_corp.txt \
    /opt/wordlists/hashcat_rules_out.txt \
  | sort -u > /tmp/merged.txt
sudo wifite --dict /tmp/merged.txt

# No cracking (capture only, crack offline)
sudo wifite --no-crack --wpa --bssid AA:BB:CC:DD:EE:FF
```

### Process Management
```bash
# Kill interfering processes automatically (NetworkManager, wpa_supplicant)
sudo wifite -k    # Kill before starting

# Kill specific processes manually
sudo airmon-ng check kill

# After engagement — restore interface
sudo airmon-ng stop wlan0mon
sudo systemctl start NetworkManager
sudo systemctl start wpa_supplicant
```

### Output Directory
```bash
# Change output directory
sudo wifite --output /opt/captures/client_engagement/

# Handshakes saved as:
# /opt/captures/client_engagement/hs/ESSID_BSSID.cap

# PMKID hashes saved as:
# /opt/captures/client_engagement/pmkid/ESSID_BSSID.22000
```

### Daemon / Background Mode
```bash
# Run continuously, scanning for any targets matching filter
sudo wifite --kill --power 70 --wpa --pmkid --no-crack \
  --output /opt/captures/ 2>&1 | tee /var/log/wifite.log &

# Monitor log
tail -f /var/log/wifite.log
```

### Skipping Targets
```bash
# Skip specific BSSIDs (exclude from scan)
sudo wifite --skip AA:BB:CC:DD:EE:FF

# Skip targets with fewer than N clients
# (not built-in; filter via handshake capture timeout --timeout 30)

# In interactive mode: press S during scan to skip current target
```

## Common Workflows

### Full Wireless Audit
```bash
# 1. Kill interfering processes
sudo airmon-ng check kill

# 2. Start Wifite with all attack types, capture-only mode
sudo wifite --kill \
  --power 60 \
  --wpa --pmkid --wps-pixie \
  --no-crack \
  --output /opt/engagement/wireless/captures/ \
  --timeout 120

# 3. After capture, crack offline with hashcat
# WPA handshake:
hashcat -a 0 -m 22000 /opt/engagement/wireless/captures/hs/*.cap \
  /opt/wordlists/rockyou.txt \
  -r /usr/share/hashcat/rules/best64.rule \
  --force --status

# PMKID hash:
hashcat -a 0 -m 22000 \
  /opt/engagement/wireless/captures/pmkid/*.22000 \
  /opt/wordlists/rockyou.txt \
  -r /usr/share/hashcat/rules/best64.rule \
  --force --status
```

### PMKID-Only Clientless Audit
```bash
# No deauth packets (stealthier, no client disruption)
sudo wifite --pmkid --no-wpa --no-wps --no-crack \
  --power 65 \
  --output /opt/pmkid_captures/

# Crack after:
hashcat -a 0 -m 22000 /opt/pmkid_captures/pmkid/*.22000 \
  /usr/share/wordlists/rockyou.txt -O
```

### Targeted Corporate AP Audit
```bash
# 1. Recon phase - passive scan
sudo airodump-ng wlan0mon --band bg --write /tmp/survey --output-format csv
# Identify target BSSID and channel from survey

# 2. Targeted Wifite attack
sudo wifite --kill \
  --bssid AA:BB:CC:DD:EE:FF \
  --channel 11 \
  --essid "Corp-Internal" \
  --wpa --pmkid \
  --no-crack \
  --output /opt/corp_wireless/ \
  --deauth-count 3 \
  --timeout 180
```

## Comparison: Wifite vs Manual aircrack-ng

| Step | Wifite | Manual aircrack-ng |
|------|--------|--------------------|
| Monitor mode | Automatic | `airmon-ng start wlan0` |
| Network scan | Automatic | `airodump-ng wlan0mon` |
| Target lock | Menu selection or flag | `airodump-ng -c CH --bssid BSSID` |
| Deauth | Automatic | `aireplay-ng -0 5 -a BSSID` |
| Handshake verify | Automatic | `aircrack-ng -w /dev/null *.cap` |
| PMKID capture | Automatic (hcxdumptool) | `hcxdumptool -i wlan0mon -o out.pcapng` |
| PMKID convert | Automatic (hcxtools) | `hcxpcapngtool out.pcapng -o hash.22000` |
| WPS attack | Automatic (reaver/bully) | `reaver -i wlan0mon -b BSSID -v` |
| Cracking | Built-in (aircrack-ng) | `aircrack-ng -w list.txt *.cap` |
| Control | Limited | Full |
| Speed | Fast | Slow |
| Learning | Low | High |

**When to use manual aircrack-ng**: When you need fine-grained control, specific injection parameters, or are debugging why a capture isn't working.

## Advanced Techniques

### Post-Capture Offline Cracking
```bash
# Convert cap to hashcat 22000 format
hcxpcapngtool /opt/captures/hs/Corp-WiFi_AABBCCDDEEFF.cap \
  -o /tmp/hash.22000

# Rule-based cracking
hashcat -a 0 -m 22000 /tmp/hash.22000 \
  /usr/share/wordlists/rockyou.txt \
  -r /usr/share/hashcat/rules/d3ad0ne.rule \
  -r /usr/share/hashcat/rules/best64.rule \
  --status --status-timer=60 -O

# Brute force 8-digit numeric (common WPA defaults)
hashcat -a 3 -m 22000 /tmp/hash.22000 "?d?d?d?d?d?d?d?d"

# Mask: Word + 4 digits
hashcat -a 6 -m 22000 /tmp/hash.22000 \
  /opt/cewl_corp.txt "?d?d?d?d"
```

### Verifying Handshake Quality
```bash
# Check handshake is complete (has EAPOL frames 1-4)
tshark -r capture.cap -Y "eapol" | head -20

# Use aircrack-ng to test (no wordlist = just verification)
aircrack-ng -w /dev/null capture.cap
# Look for "WPA (x handshake)" in output
```

## Integration with Other Tools

| Tool | Integration |
|------|-------------|
| aircrack-ng | Wifite uses it for WPA cracking and handshake verification |
| hcxdumptool | Wifite uses it for PMKID capture |
| hcxtools | Wifite uses `hcxpcapngtool` for PMKID hash conversion |
| hashcat | Offline cracking of `.22000` PMKID and WPA hashes |
| Reaver | Wifite calls reaver for WPS PIN attacks |
| Bully | Alternative to Reaver for WPS |
| Pixiewps | Wifite calls pixiewps for Pixie-Dust WPS attacks |
| CeWL | Generate target-specific wordlists for WPA cracking |
| Crunch | Generate pattern-based wordlists (SSID-based, numeric) |

## Troubleshooting

**No networks found**
```bash
# Verify interface is in monitor mode
iwconfig wlan0mon
# Ensure correct band (2.4GHz vs 5GHz)
sudo wifite -i wlan0mon --band bg   # 2.4GHz only
sudo wifite -i wlan0mon --band a    # 5GHz only
sudo wifite -i wlan0mon --band abg  # Both
```

**"Interface is not in monitor mode"**
```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
sudo wifite -i wlan0mon
```

**Handshake captured but not cracking**
```bash
# Test manually
aircrack-ng -w /usr/share/wordlists/rockyou.txt ~/.wifite/hs/*.cap
# If "No valid WPA handshakes found": recapture with more deauth frames
sudo wifite --wpa --deauth-count 10 --bssid TARGET_BSSID
```

**WPS attack running forever**
- WPS is often rate-limited or locked after failed attempts (WPS lock)
- Try Pixie-Dust first: `--wps-pixie`; if not vulnerable, WPS PIN is impractical
- Move on: `sudo wifite` → press `S` to skip current target

**hcxdumptool not found (PMKID fails)**
```bash
sudo apt install hcxdumptool hcxtools -y
# Or build from source:
git clone https://github.com/ZerBea/hcxdumptool.git
cd hcxdumptool && make && sudo make install
```

**NetworkManager conflicts**
```bash
sudo systemctl stop NetworkManager
sudo systemctl stop wpa_supplicant
sudo airmon-ng check kill
sudo wifite
# After:
sudo systemctl start NetworkManager
```
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
