<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-codingcreatively
description: CTF writeups and security challenges by codingcreatively.
---

# Writeups by codingcreatively

Source repository: `/repos/codingcreatively`

## Repository Index

- ig-jinn/README.md

## Writeup Content


### File: ig-jinn/README.md

# IG JINN v2.4 - Instagram Mass Report Pentest Tool
[![GitHub stars](https://img.shields.io/github/stars/yourusername/ig-jinn.svg)](https://github.com/yourusername/ig-jinn) [![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)

**AUTHORIZED SECURITY TESTING ONLY**  
Advanced penetration testing tool for Instagram abuse reporting rate limiting assessment using TOR circuit rotation and 2026 API bypass techniques.

# Features

- **98% User ID Resolution** - 5-stage fallback (Mobile API → __a=1 → SI Headers → Profile Regex → Crypto Hash)
- **TOR Circuit Automation** - Automatic IP rotation every 7 reports via Stem control
- **Multi-Vector Reporting** - GraphQL, Mobile API, Profile endpoints (4x attack surfaces)
- **Stealth UA Rotation** - Instagram mobile/desktop fingerprint evasion
- **Real-time Stats** - Live success rate, circuit consumption, error tracking
- **CSRF Token Harvesting** - Dynamic extraction from multiple endpoints
- **Production-grade Headers** - X-IG-App-ID, bandwidth spoofing, Sec-Fetch policies

# Setup & Usage
##  Start TOR with control enabled
### sudo systemctl restart tor
### curl --socks5 localhost:9050 http://httpbin.org/ip  # Verify TOR

# Clone & Run
### git clone https://github.com/codingcreatively/ig-jinn.git
### cd ig-jinn
### sudo chmod +x ig-jinn.py
### source venv/bin/activate
### pip install -r requeirements.txt
### python3 ig-jinn.py

# Prerequisites
### Install TOR + Stem control
### Enable TOR control port (edit /etc/tor/torrc)
### ControlPort 9051
### CookieAuthentication 0
### sudo systemctl restart tor

# Execute Authorized Pentest
### 🚀 IG JINN v2.4 - TOR BYPASS EDITION
### 🎯 Target Instagram: arcane.__01
### ENTER 'AUTHORIZED_PENTEST': 
### Threads [15-35] (25): 25
### Duration [300-1800s] (900): 900

# Attack Methodology
### 1. TOR Circuit ✓ → CSRF Harvest → User ID Resolution (98% success)
### 2. Thread Pool (15-35) → Multi-Vector Reports → Auto Circuit Rotation
### 3. Live Metrics: Success% | Circuits | Errors | Reports/sec
### 4. Final Report: Restriction flags assessment

# Sample Output
### 📊 Total Reports Fired:     12,847
### ✅ Successful Submissions:   9,234 (71.9%)
### ❌ Blocked/Errors:           3,613
### 🔄 TOR Circuits Consumed:      842
### 🎯 User ID Resolution:     SUCCESS

# Tutorial Video
## see here: https://youtu.be/8ByZUSeHZd8

# Contact
### Instagram:- arcane.__01
### Telegram:- @cashhustle_8

# Join Now
### Yotutuhe:- https://youtube.com/@cyberarcane8?si=ufFzu1ubtIzTrbHZ
### Telegram Channel:- https://t.me/dealzone2888





