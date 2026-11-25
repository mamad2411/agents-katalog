---
name: statutory-instruments-api
description: "Statutory Instruments API skill. Use when working with Statutory Instruments for api. Covers 16 endpoints."
version: 1.0.0
generator: lapsh
---

# Statutory Instruments API
API version: v1

## Auth
No authentication required.

## Base URL
Not specified.

## Setup
1. No auth setup needed
2. GET /api/v1/LayingBody -- verify access

## Endpoints

16 endpoints across 1 groups. See references/api-spec.lap for full details.

### api
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/v1/BusinessItem/{id} | Returns business item by ID. |
| GET | /api/v1/LayingBody | Returns all laying bodies. |
| GET | /api/v1/Procedure | Returns all procedures. |
| GET | /api/v1/Procedure/{id} | Returns procedure by ID. |
| GET | /api/v1/ProposedNegativeStatutoryInstrument | Returns a list of proposed negative statutory instruments. |
| GET | /api/v1/ProposedNegativeStatutoryInstrument/{id} | Returns proposed negative statutory instrument by ID. |
| GET | /api/v1/ProposedNegativeStatutoryInstrument/{id}/BusinessItems | Returns business items belonging to a proposed negative statutory instrument. |
| GET | /api/v1/StatutoryInstrument | Returns a list of statutory instruments. |
| GET | /api/v1/StatutoryInstrument/{id} | Returns a statutory instrument by ID. |
| GET | /api/v1/StatutoryInstrument/{id}/BusinessItems | Returns business items belonging to statutory instrument with ID. |
| GET | /api/v2/ActOfParliament | Search through Acts of Parliament |
| GET | /api/v2/ActOfParliament/{id} | Search individual Act of Parliament by ID |
| GET | /api/v2/StatutoryInstrument | Search through statutory instruments and proposed negatives |
| GET | /api/v2/StatutoryInstrument/{instrumentId} | Get individual statutory instrument or proposed negative by id |
| GET | /api/v2/StatutoryInstrument/{instrumentId}/BusinessItems | Get business items associated with a particular instrument |
| GET | /api/v2/Timeline/{timelineId}/BusinessItems | Get business items associated with a particular timeline |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get BusinessItem details?" -> GET /api/v1/BusinessItem/{id}
- "List all LayingBody?" -> GET /api/v1/LayingBody
- "List all Procedure?" -> GET /api/v1/Procedure
- "Get Procedure details?" -> GET /api/v1/Procedure/{id}
- "List all ProposedNegativeStatutoryInstrument?" -> GET /api/v1/ProposedNegativeStatutoryInstrument
- "Get ProposedNegativeStatutoryInstrument details?" -> GET /api/v1/ProposedNegativeStatutoryInstrument/{id}
- "List all BusinessItems?" -> GET /api/v1/ProposedNegativeStatutoryInstrument/{id}/BusinessItems
- "List all StatutoryInstrument?" -> GET /api/v1/StatutoryInstrument
- "Get StatutoryInstrument details?" -> GET /api/v1/StatutoryInstrument/{id}
- "List all BusinessItems?" -> GET /api/v1/StatutoryInstrument/{id}/BusinessItems
- "List all ActOfParliament?" -> GET /api/v2/ActOfParliament
- "Get ActOfParliament details?" -> GET /api/v2/ActOfParliament/{id}
- "List all StatutoryInstrument?" -> GET /api/v2/StatutoryInstrument
- "Get StatutoryInstrument details?" -> GET /api/v2/StatutoryInstrument/{instrumentId}
- "List all BusinessItems?" -> GET /api/v2/StatutoryInstrument/{instrumentId}/BusinessItems
- "List all BusinessItems?" -> GET /api/v2/Timeline/{timelineId}/BusinessItems

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
