---
name: railradar
description: Indian Railways API for train tracking - live status, PNR, stations, trains between stations. Uses RailRadar API. No Zo-specific setup required - uses standard environment variables.
metadata:
  author: ankitjh4
  display-name: RailRadar (Indian Railways)
---

# RailRadar - Indian Railways API

Track Indian trains using RailRadar API.

## API Key Required

Get your free API key from: https://railradar.in

### Setup

```bash
# Set environment variable (works anywhere)
export RAILRADAR_API_KEY="your-api-key"

# Or use in Python
import os
api_key = os.environ.get("RAILRADAR_API_KEY")
```

## Features

- Search stations by name/code
- Find trains between stations
- Live train running status
- PNR status check

## Usage

```bash
# Search stations
python3 scripts/railradar.py stations "Delhi"

# Trains between stations
python3 scripts/railradar.py trains NDLS BKN

# Live status
python3 scripts/railradar.py live 12002

# PNR status (if supported)
python3 scripts/railradar.py pnr 1234567890
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| RAILRADAR_API_KEY | Yes | Your RailRadar API key |

## API Endpoints

- Base: `https://railradar.in/api/v1`
- Stations: `/search/stations`
- Trains: `/trains-between-stations`
- Live: `/live-train-status`
- PNR: `/pnr-status`

## Links

- Dashboard: https://railradar.in
- Docs: https://railradar.in/docs
- Not affiliated with Indian Railways or IRCTC
