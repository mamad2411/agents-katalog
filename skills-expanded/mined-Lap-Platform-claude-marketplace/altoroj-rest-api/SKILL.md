---
name: altoroj-rest-api
description: "AltoroJ REST API skill. Use when working with AltoroJ REST for login, account, transfer. Covers 12 endpoints."
version: 1.0.0
generator: lapsh
---

# AltoroJ REST API
API version: 1.0.2

## Auth
ApiKey Authorization in header

## Base URL
Not specified.

## Setup
1. Set your API key in the appropriate header
2. GET /login -- verify access
3. POST /login -- create first login

## Endpoints

12 endpoints across 6 groups. See references/api-spec.lap for full details.

### login
| Method | Path | Description |
|--------|------|-------------|
| GET | /login | Check if any user is logged in |
| POST | /login | Login method |

### account
| Method | Path | Description |
|--------|------|-------------|
| GET | /account | Returns a list of all the accounts owned by the user |
| GET | /account/{accountNo} | Returns details about a specific account |
| GET | /account/{accountNo}/transactions | Returns the last 10 transactions attached to an account |
| POST | /account/{accountNo}/transactions | Return transactions between 2 specific dates |

### transfer
| Method | Path | Description |
|--------|------|-------------|
| POST | /transfer | Transfer money between two accounts |

### feedback
| Method | Path | Description |
|--------|------|-------------|
| POST | /feedback/submit | Submit feedback for the bank |
| GET | /feedback/{feedbackId} | Retrieve feedback |

### admin
| Method | Path | Description |
|--------|------|-------------|
| POST | /admin/addUser | Add new user |
| POST | /admin/changePassword | Change user password |

### logout
| Method | Path | Description |
|--------|------|-------------|
| GET | /logout | Logout from the bank |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all login?" -> GET /login
- "Create a login?" -> POST /login
- "List all account?" -> GET /account
- "Get account details?" -> GET /account/{accountNo}
- "List all transactions?" -> GET /account/{accountNo}/transactions
- "Create a transaction?" -> POST /account/{accountNo}/transactions
- "Create a transfer?" -> POST /transfer
- "Create a submit?" -> POST /feedback/submit
- "Get feedback details?" -> GET /feedback/{feedbackId}
- "Create a addUser?" -> POST /admin/addUser
- "Create a changePassword?" -> POST /admin/changePassword
- "List all logout?" -> GET /logout
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
