---
name: personalizer-client
description: "Personalizer Client API skill. Use when working with Personalizer Client for configurations, evaluations, events. Covers 17 endpoints."
version: 1.0.0
generator: lapsh
---

# Personalizer Client
API version: v1.0

## Auth
ApiKey Ocp-Apim-Subscription-Key in header

## Base URL
Not specified.

## Setup
1. Set your API key in the appropriate header
2. GET /configurations/service -- verify access
3. POST /evaluations -- create first evaluations

## Endpoints

17 endpoints across 6 groups. See references/api-spec.lap for full details.

### configurations
| Method | Path | Description |
|--------|------|-------------|
| GET | /configurations/service | Get Service Configuration. |
| PUT | /configurations/service | Update Service Configuration. |
| GET | /configurations/policy | Get Policy. |
| PUT | /configurations/policy | Update Policy. |
| DELETE | /configurations/policy | Reset Policy. |

### evaluations
| Method | Path | Description |
|--------|------|-------------|
| GET | /evaluations/{evaluationId} | Get Evaluation. |
| DELETE | /evaluations/{evaluationId} | Delete Evaluation. |
| GET | /evaluations | List Evaluations. |
| POST | /evaluations | Create Evaluation. |

### events
| Method | Path | Description |
|--------|------|-------------|
| POST | /events/{eventId}/reward | Post Reward. |
| POST | /events/{eventId}/activate | Activate Event. |

### logs
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /logs | Deletes Logs. |
| GET | /logs/properties | Get Log Properties. |

### model
| Method | Path | Description |
|--------|------|-------------|
| GET | /model | Get Model. |
| DELETE | /model | Reset Model. |
| GET | /model/properties | Get Model Properties. |

### rank
| Method | Path | Description |
|--------|------|-------------|
| POST | /rank | Post Rank. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all service?" -> GET /configurations/service
- "List all policy?" -> GET /configurations/policy
- "Get evaluation details?" -> GET /evaluations/{evaluationId}
- "Delete a evaluation?" -> DELETE /evaluations/{evaluationId}
- "List all evaluations?" -> GET /evaluations
- "Create a evaluation?" -> POST /evaluations
- "Create a reward?" -> POST /events/{eventId}/reward
- "Create a activate?" -> POST /events/{eventId}/activate
- "List all properties?" -> GET /logs/properties
- "List all model?" -> GET /model
- "List all properties?" -> GET /model/properties
- "Create a rank?" -> POST /rank
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
