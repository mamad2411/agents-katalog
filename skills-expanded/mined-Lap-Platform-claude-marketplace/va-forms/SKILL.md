---
name: va-forms
description: "VA Forms API skill. Use when working with VA Forms for forms. Covers 2 endpoints."
version: 1.0.0
generator: lapsh
---

# VA Forms
API version: 0.0.0

## Auth
ApiKey apikey in header

## Base URL
https://sandbox-api.va.gov/services/va_forms/v0

## Setup
1. Set your API key in the appropriate header
2. GET /forms -- verify access

## Endpoints

2 endpoints across 1 groups. See references/api-spec.lap for full details.

### forms
| Method | Path | Description |
|--------|------|-------------|
| GET | /forms | Returns all VA Forms and their last revision date |
| GET | /forms/{form_name} | Find form by form name |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Search forms?" -> GET /forms
- "Get form details?" -> GET /forms/{form_name}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
