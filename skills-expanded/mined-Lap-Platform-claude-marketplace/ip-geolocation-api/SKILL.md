---
name: ip-geolocation-api
description: "IP Geolocation API skill. Use when working with IP Geolocation for data. Covers 3 endpoints."
version: 1.0.0
generator: lapsh
---

# IP Geolocation API

## Auth
ApiKey key in query

## Base URL
https://api-bdc.net

## Setup
1. Set your API key in the appropriate header
2. GET /data/ip-geolocation -- verify access

## Endpoints

3 endpoints across 1 groups. See references/api-spec.lap for full details.

### data
| Method | Path | Description |
|--------|------|-------------|
| GET | /data/ip-geolocation | IP Geolocation API |
| GET | /data/ip-geolocation-with-confidence | IP Geolocation with Confidence Area API |
| GET | /data/ip-geolocation-full | IP Geolocation with Confidence Area and Hazard Report API |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all ip-geolocation?" -> GET /data/ip-geolocation
- "List all ip-geolocation-with-confidence?" -> GET /data/ip-geolocation-with-confidence
- "List all ip-geolocation-full?" -> GET /data/ip-geolocation-full
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
