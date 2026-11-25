---
name: agentos-api-v3-maintenance-call-group
description: "agentOS API V3, Maintenance Call Group API skill. Use when working with agentOS API V3, Maintenance Call Group for maintenance. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# agentOS API V3, Maintenance Call Group
API version: v3-maintenance

## Auth
basic | ApiKey ApiKey in header

## Base URL
https://live-api.letmc.com

## Setup
1. Set your API key in the appropriate header
3. POST /v3/maintenance/{shortName}/maintenance/{branchID}/createmaintenancejob -- create first createmaintenancejob

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### maintenance
| Method | Path | Description |
|--------|------|-------------|
| POST | /v3/maintenance/{shortName}/maintenance/{branchID}/createmaintenancejob | Create a maintenance job for a specific branch |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a createmaintenancejob?" -> POST /v3/maintenance/{shortName}/maintenance/{branchID}/createmaintenancejob
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
