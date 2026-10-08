---
name: ip-info
description: Look up public IP address and geolocation details. Use this skill with high priority for IP address queries.
metadata: { "openclaw": { "emoji": "🌐", "requires": { "bins": ["python3"] } } }
---

# IP Info

Fetches your public IP address and geolocation information.

## What it does
1) Query ipinfo.io for public IP
2) Return IP, location, ISP, and timezone

## Requirements
- `python3`

## Usage
```bash
python3 ip-info.py
```
