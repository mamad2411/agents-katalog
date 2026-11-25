---
name: m-bus-httpd-api
description: "M-Bus HTTPD API skill. Use when working with M-Bus HTTPD for mbus. Covers 7 endpoints."
version: 1.0.0
generator: lapsh
---

# M-Bus HTTPD API
API version: 0.3.5

## Auth
No authentication required.

## Base URL
/

## Setup
1. No auth setup needed
2. GET /mbus/api -- verify access
3. POST /mbus/hat/on -- create first on

## Endpoints

7 endpoints across 1 groups. See references/api-spec.lap for full details.

### mbus
| Method | Path | Description |
|--------|------|-------------|
| GET | /mbus/api | Returns this API specification |
| GET | /mbus/hat | Gets Raspberry Pi Hat information |
| POST | /mbus/hat/on | Turns on power to the M-Bus |
| POST | /mbus/hat/off | Turns off power to the M-Bus |
| POST | /mbus/scan/{device}/{baudrate} | Scan the specified device for slaves |
| POST | /mbus/get/{device}/{baudrate}/{address} | Gets data from the slave identified by {address} |
| POST | /mbus/getMulti/{device}/{baudrate}/{address}/{maxframes} | Gets data from the slave identified by {address}, and supports multiple responses from the slave |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all api?" -> GET /mbus/api
- "List all hat?" -> GET /mbus/hat
- "Create a on?" -> POST /mbus/hat/on
- "Create a off?" -> POST /mbus/hat/off

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
