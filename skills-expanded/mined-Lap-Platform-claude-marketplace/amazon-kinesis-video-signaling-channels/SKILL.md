---
name: amazon-kinesis-video-signaling-channels
description: "Amazon Kinesis Video Signaling Channels API skill. Use when working with Amazon Kinesis Video Signaling Channels for get-ice-server-config, send-alexa-offer-to-master. Covers 2 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon Kinesis Video Signaling Channels
API version: 2019-12-04

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST /v1/get-ice-server-config -- create first get-ice-server-config

## Endpoints

2 endpoints across 2 groups. See references/api-spec.lap for full details.

### get-ice-server-config
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/get-ice-server-config | Gets the Interactive Connectivity Establishment (ICE) server configuration information, including URIs, username, and password which can be used to configure the WebRTC connection. The ICE component uses this configuration information to setup the WebRTC connection, including authenticating with the Traversal Using Relays around NAT (TURN) relay server.  TURN is a protocol that is used to improve the connectivity of peer-to-peer applications. By providing a cloud-based relay service, TURN ensures that a connection can be established even when one or more peers are incapable of a direct peer-to-peer connection. For more information, see A REST API For Access To TURN Services.  You can invoke this API to establish a fallback mechanism in case either of the peers is unable to establish a direct peer-to-peer connection over a signaling channel. You must specify either a signaling channel ARN or the client ID in order to invoke this API. |

### send-alexa-offer-to-master
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/send-alexa-offer-to-master | This API allows you to connect WebRTC-enabled devices with Alexa display devices. When invoked, it sends the Alexa Session Description Protocol (SDP) offer to the master peer. The offer is delivered as soon as the master is connected to the specified signaling channel. This API returns the SDP answer from the connected master. If the master is not connected to the signaling channel, redelivery requests are made until the message expires. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a get-ice-server-config?" -> POST /v1/get-ice-server-config
- "Create a send-alexa-offer-to-master?" -> POST /v1/send-alexa-offer-to-master
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
