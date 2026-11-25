---
name: amazonapigatewaymanagementapi
description: "AmazonApiGatewayManagementApi API skill. Use when working with AmazonApiGatewayManagementApi for @connections. Covers 3 endpoints."
version: 1.0.0
generator: lapsh
---

# AmazonApiGatewayManagementApi
API version: 2018-11-29

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /@connections/{connectionId} -- verify access
3. POST /@connections/{connectionId} -- create first @connections

## Endpoints

3 endpoints across 1 groups. See references/api-spec.lap for full details.

### @connections
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /@connections/{connectionId} | Delete the connection with the provided id. |
| GET | /@connections/{connectionId} | Get information about the connection with the provided id. |
| POST | /@connections/{connectionId} | Sends the provided data to the specified connection. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Delete a @connection?" -> DELETE /@connections/{connectionId}
- "Get @connection details?" -> GET /@connections/{connectionId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
