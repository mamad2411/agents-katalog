---
name: pos-terminal-management-api-deprecated
description: "POS Terminal Management API (deprecated) API skill. Use when working with POS Terminal Management API (deprecated) for assignTerminals, findTerminal, getStoresUnderAccount. Covers 5 endpoints."
version: 1.0.0
generator: lapsh
---

# POS Terminal Management API (deprecated)
API version: 1

## Auth
ApiKey X-API-Key in header | Bearer basic

## Base URL
https://postfmapi-test.adyen.com/postfmapi/terminal/v1

## Setup
1. Set Authorization header with your Bearer token
3. POST /assignTerminals -- create first assignTerminals

## Endpoints

5 endpoints across 5 groups. See references/api-spec.lap for full details.

### assignTerminals
| Method | Path | Description |
|--------|------|-------------|
| POST | /assignTerminals | Assign terminals |

### findTerminal
| Method | Path | Description |
|--------|------|-------------|
| POST | /findTerminal | Get the account or store of a terminal |

### getStoresUnderAccount
| Method | Path | Description |
|--------|------|-------------|
| POST | /getStoresUnderAccount | Get the stores of an account |

### getTerminalDetails
| Method | Path | Description |
|--------|------|-------------|
| POST | /getTerminalDetails | Get the details of a terminal |

### getTerminalsUnderAccount
| Method | Path | Description |
|--------|------|-------------|
| POST | /getTerminalsUnderAccount | Get the list of terminals |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a assignTerminal?" -> POST /assignTerminals
- "Create a findTerminal?" -> POST /findTerminal
- "Create a getStoresUnderAccount?" -> POST /getStoresUnderAccount
- "Create a getTerminalDetail?" -> POST /getTerminalDetails
- "Create a getTerminalsUnderAccount?" -> POST /getTerminalsUnderAccount
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
