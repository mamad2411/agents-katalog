---
name: call-control-api
description: "Call Control API skill. Use when working with Call Control for api. Covers 6 endpoints."
version: 1.0.0
generator: lapsh
---

# Call Control API
API version: 2015-11-01

## Auth
ApiKey apiKey in header

## Base URL
https://api.callcontrol.com

## Setup
1. Set your API key in the appropriate header
2. GET /api/2015-11-01/Complaints/{phoneNumber} -- verify access
3. POST /api/2015-11-01/Enterprise/UpsertUser -- create first UpsertUser

## Endpoints

6 endpoints across 1 groups. See references/api-spec.lap for full details.

### api
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/2015-11-01/Complaints/{phoneNumber} | Complaints: Free service (with registration), providing community and government complaint lookup by phone number for up to 2,000 queries per month.  Details include number complaint rates from (FTC, FCC, IRS, Indiana Attorney  General) and key entity tag extractions from complaints. |
| GET | /api/2015-11-01/Enterprise/ShouldBlock/{phoneNumber}/{userPhoneNumber} | Enterprise  GET: ShouldBlock |
| GET | /api/2015-11-01/Enterprise/GetUser/{phoneNumber} | Enterprise  GET: GetUser |
| POST | /api/2015-11-01/Enterprise/UpsertUser | UpsertUser: insert or update all properties from a user |
| GET | /api/2015-11-01/Reputation/{phoneNumber} | Reputation: |
| POST | /api/2015-11-01/Report | Report: report spam calls received to better tune our algorithms based upon spam calls you receive |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get Complaint details?" -> GET /api/2015-11-01/Complaints/{phoneNumber}
- "Get ShouldBlock details?" -> GET /api/2015-11-01/Enterprise/ShouldBlock/{phoneNumber}/{userPhoneNumber}
- "Get GetUser details?" -> GET /api/2015-11-01/Enterprise/GetUser/{phoneNumber}
- "Create a UpsertUser?" -> POST /api/2015-11-01/Enterprise/UpsertUser
- "Get Reputation details?" -> GET /api/2015-11-01/Reputation/{phoneNumber}
- "Create a Report?" -> POST /api/2015-11-01/Report
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
