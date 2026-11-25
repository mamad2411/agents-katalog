---
name: aws-iot-secure-tunneling
description: "AWS IoT Secure Tunneling API skill. Use when working with AWS IoT Secure Tunneling for root. Covers 8 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS IoT Secure Tunneling
API version: 2018-10-05

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST / -- create first resource

## Endpoints

8 endpoints across 1 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| POST | / | Closes a tunnel identified by the unique tunnel id. When a CloseTunnel request is received, we close the WebSocket connections between the client and proxy server so no data can be transmitted. Requires permission to access the CloseTunnel action. |
| POST | / | Gets information about a tunnel identified by the unique tunnel id. Requires permission to access the DescribeTunnel action. |
| POST | / | Lists the tags for the specified resource. |
| POST | / | List all tunnels for an Amazon Web Services account. Tunnels are listed by creation time in descending order, newer tunnels will be listed before older tunnels. Requires permission to access the ListTunnels action. |
| POST | / | Creates a new tunnel, and returns two client access tokens for clients to use to connect to the IoT Secure Tunneling proxy server. Requires permission to access the OpenTunnel action. |
| POST | / | Revokes the current client access token (CAT) and returns new CAT for clients to use when reconnecting to secure tunneling to access the same tunnel. Requires permission to access the RotateTunnelAccessToken action.  Rotating the CAT doesn't extend the tunnel duration. For example, say the tunnel duration is 12 hours and the tunnel has already been open for 4 hours. When you rotate the access tokens, the new tokens that are generated can only be used for the remaining 8 hours. |
| POST | / | A resource tag. |
| POST | / | Removes a tag from a resource. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
