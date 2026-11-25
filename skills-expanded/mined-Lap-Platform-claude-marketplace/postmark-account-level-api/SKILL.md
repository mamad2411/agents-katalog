---
name: postmark-account-level-api
description: "Postmark Account-level API skill. Use when working with Postmark Account-level for servers, senders, domains. Covers 23 endpoints."
version: 1.0.0
generator: lapsh
---

# Postmark Account-level API
API version: 0.9.0

## Auth
No authentication required.

## Base URL
https://api.postmarkapp.com/

## Setup
1. No auth setup needed
2. GET /servers -- verify access
3. POST /servers -- create first servers

## Endpoints

23 endpoints across 4 groups. See references/api-spec.lap for full details.

### servers
| Method | Path | Description |
|--------|------|-------------|
| GET | /servers/{serverid} | Get a Server |
| PUT | /servers/{serverid} | Edit a Server |
| DELETE | /servers/{serverid} | Delete a Server |
| GET | /servers | List servers |
| POST | /servers | Create a Server |

### senders
| Method | Path | Description |
|--------|------|-------------|
| GET | /senders | List Sender Signatures |
| POST | /senders | Create a Sender Signature |
| GET | /senders/{signatureid} | Get a Sender Signature |
| PUT | /senders/{signatureid} | Update a Sender Signature |
| DELETE | /senders/{signatureid} | Delete a Sender Signature |
| POST | /senders/{signatureid}/resend | Resend Signature Confirmation Email |
| POST | /senders/{signatureid}/verifyspf | Request DNS Verification for SPF |
| POST | /senders/{signatureid}/requestnewdkim | Request a new DKIM Key |

### domains
| Method | Path | Description |
|--------|------|-------------|
| GET | /domains | List Domains |
| POST | /domains | Create a Domain |
| GET | /domains/{domainid} | Get a Domain |
| PUT | /domains/{domainid} | Update a Domain |
| DELETE | /domains/{domainid} | Delete a Domain |
| PUT | /domains/{domainid}/verifydkim | Request DNS Verification for DKIM |
| PUT | /domains/{domainid}/verifyreturnpath | Request DNS Verification for Return-Path |
| POST | /domains/{domainid}/verifyspf | Request DNS Verification for SPF |
| POST | /domains/{domainid}/rotatedkim | Rotate DKIM Key |

### templates
| Method | Path | Description |
|--------|------|-------------|
| PUT | /templates/push | Push templates from one server to another |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get server details?" -> GET /servers/{serverid}
- "Update a server?" -> PUT /servers/{serverid}
- "Delete a server?" -> DELETE /servers/{serverid}
- "List all servers?" -> GET /servers
- "Create a server?" -> POST /servers
- "List all senders?" -> GET /senders
- "Create a sender?" -> POST /senders
- "Get sender details?" -> GET /senders/{signatureid}
- "Update a sender?" -> PUT /senders/{signatureid}
- "Delete a sender?" -> DELETE /senders/{signatureid}
- "Create a resend?" -> POST /senders/{signatureid}/resend
- "Create a verifyspf?" -> POST /senders/{signatureid}/verifyspf
- "Create a requestnewdkim?" -> POST /senders/{signatureid}/requestnewdkim
- "List all domains?" -> GET /domains
- "Create a domain?" -> POST /domains
- "Get domain details?" -> GET /domains/{domainid}
- "Update a domain?" -> PUT /domains/{domainid}
- "Delete a domain?" -> DELETE /domains/{domainid}
- "Create a verifyspf?" -> POST /domains/{domainid}/verifyspf
- "Create a rotatedkim?" -> POST /domains/{domainid}/rotatedkim

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
