---
name: reimbursements-api
description: "Reimbursements API skill. Use when working with Reimbursements for api-docs, expense, health. Covers 7 endpoints."
version: 1.0.0
generator: lapsh
---

# Reimbursements API
API version: 1.0

## Auth
ApiKey X-API-Key in header

## Base URL
Not specified.

## Setup
1. Set your API key in the appropriate header
2. GET /api-docs -- verify access
3. POST /expense/{action}/{reportId} -- create first expense

## Endpoints

7 endpoints across 6 groups. See references/api-spec.lap for full details.

### api-docs
| Method | Path | Description |
|--------|------|-------------|
| GET | /api-docs | Get swagger documentation |

### expense
| Method | Path | Description |
|--------|------|-------------|
| POST | /expense/{action}/{reportId} | Expense Action |

### health
| Method | Path | Description |
|--------|------|-------------|
| GET | /health | Get API Health Status |

### reimbursement
| Method | Path | Description |
|--------|------|-------------|
| POST | /reimbursement/{projectId} | Create Reimbursement |
| PATCH | /reimbursement/{projectId} | Update Reimbursement |

### reset
| Method | Path | Description |
|--------|------|-------------|
| POST | /reset | Reset Policy |

### tag
| Method | Path | Description |
|--------|------|-------------|
| POST | /tag | Tag Policy |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all api-docs?" -> GET /api-docs
- "List all health?" -> GET /health
- "Partially update a reimbursement?" -> PATCH /reimbursement/{projectId}
- "Create a reset?" -> POST /reset
- "Create a tag?" -> POST /tag
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
