---
name: ip2proxy-proxy-detection
description: "IP2Proxy Proxy Detection API skill. Use when working with IP2Proxy Proxy Detection for root. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# IP2Proxy Proxy Detection
API version: 1.0

## Auth
ApiKey key in query

## Base URL
https://api.ip2proxy.com

## Setup
1. Set your API key in the appropriate header
2. GET / -- verify access

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| GET | / | Check if an IP address is proxy |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
