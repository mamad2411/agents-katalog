---
name: ip-geolocation
description: Look up geographic location of an IP address using free API
---

# IP Geolocation Lookup

Look up geographic location of an IP address using free API

## When to Use

- User wants to ip location
- User wants to geolocate ip
- Keywords: ip, geolocation, location, network

## Required Parameters

- **ip_address** (string): IP address to look up

## Output

- **country** (string): Country name
- **city** (string): City name
- **lat** (number): Latitude
- **lon** (number): Longitude
- **isp** (string): ISP name

## Security

- Sandbox level: strict
- Max execution time: 30000ms
- Network whitelist: ip-api.com
- JadeGate verified: Yes (5-layer security check passed)

## Execution Flow

Entry: `fetch` -> 6 steps -> Exit: `ret_ok`, `ret_fail`
