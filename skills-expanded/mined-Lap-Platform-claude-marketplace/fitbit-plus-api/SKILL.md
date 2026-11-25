---
name: fitbit-plus-api
description: "Fitbit Plus API skill. Use when working with Fitbit Plus for oauth, organization, group. Covers 62 endpoints."
version: 1.0.0
generator: lapsh
---

# Fitbit Plus API
API version: v7.78.1

## Auth
OAuth2

## Base URL
https://api.twinehealth.com/pub

## Setup
1. Configure auth: OAuth2
2. GET /group -- verify access
3. POST /oauth/token -- create first token

## Endpoints

62 endpoints across 22 groups. See references/api-spec.lap for full details.

### oauth
| Method | Path | Description |
|--------|------|-------------|
| POST | /oauth/token | Create an oauth token |
| GET | /oauth/token/{id}/groups | Get the groups for a token |
| GET | /oauth/token/{id}/organization | Get the organization for a token |

### organization
| Method | Path | Description |
|--------|------|-------------|
| GET | /organization/{id} | Get an organization |

### group
| Method | Path | Description |
|--------|------|-------------|
| POST | /group | Create a group |
| GET | /group | List groups |
| GET | /group/{id} | Get a group |

### coach
| Method | Path | Description |
|--------|------|-------------|
| GET | /coach | List coaches |
| GET | /coach/{id} | Get a coach |

### reward_program
| Method | Path | Description |
|--------|------|-------------|
| POST | /reward_program | Create a reward program |
| GET | /reward_program | List reward programs |
| GET | /reward_program/{id} | Get a reward program |
| GET | /reward_program/{id}/group | Get group for a reward program |

### action
| Method | Path | Description |
|--------|------|-------------|
| POST | /action | Create action |
| GET | /action/{id} | Get an action |
| PATCH | /action/{id} | Update an action |

### bundle
| Method | Path | Description |
|--------|------|-------------|
| POST | /bundle | Create bundle |
| GET | /bundle/{id} | Get a bundle |
| PATCH | /bundle/{id} | Update a bundle |

### calendar_event
| Method | Path | Description |
|--------|------|-------------|
| POST | /calendar_event | Create calendar event |
| GET | /calendar_event | List calendar events |
| GET | /calendar_event/{id} | Get a calendar event |
| PATCH | /calendar_event/{id} | Update a calendar event |
| DELETE | /calendar_event/{id} | Delete a calendar event |

### calendar_event_response
| Method | Path | Description |
|--------|------|-------------|
| POST | /calendar_event_response | Create calendar event response |

### email_history
| Method | Path | Description |
|--------|------|-------------|
| GET | /email_history | List email histories |
| GET | /email_history/{id} | Get an email history |

### health_profile
| Method | Path | Description |
|--------|------|-------------|
| GET | /health_profile | List health profiles |
| GET | /health_profile/{id} | Get a health profile |

### health_profile_question
| Method | Path | Description |
|--------|------|-------------|
| GET | /health_profile_question | List health profile questions |
| GET | /health_profile_question/{id} | Get a health profile question |

### health_profile_answer
| Method | Path | Description |
|--------|------|-------------|
| GET | /health_profile_answer | List health profile answers |
| GET | /health_profile_answer/{id} | Get a health profile answer |

### health_question_definition
| Method | Path | Description |
|--------|------|-------------|
| GET | /health_question_definition | List health question definitions |
| GET | /health_question_definition/{id} | Get a health question definition |

### patient_health_metric
| Method | Path | Description |
|--------|------|-------------|
| POST | /patient_health_metric | Create patient health metrics |
| GET | /patient_health_metric | List patient health metrics |
| GET | /patient_health_metric/{id} | Get a patient health metric |

### patient
| Method | Path | Description |
|--------|------|-------------|
| POST | /patient | Create a patient |
| GET | /patient | List patients |
| PUT | /patient | Upsert patient |
| GET | /patient/{id} | Get a patient |
| PATCH | /patient/{id} | Update a patient |
| GET | /patient/{id}/groups | List groups for a patient |
| GET | /patient/{id}/coaches | List coaches for a patient |

### patient_plan_summary
| Method | Path | Description |
|--------|------|-------------|
| GET | /patient_plan_summary | List patient plan summaries |
| GET | /patient_plan_summary/{id} | Get the plan summary for a patient |
| PATCH | /patient_plan_summary/{id} | Update a plan summary |

### result
| Method | Path | Description |
|--------|------|-------------|
| GET | /result | List patient health results |
| GET | /result/{id} | Get a patient health result |

### reward
| Method | Path | Description |
|--------|------|-------------|
| POST | /reward | Create a reward |
| GET | /reward | List rewards |
| GET | /reward/{id} | Get a reward |

### reward_earning
| Method | Path | Description |
|--------|------|-------------|
| POST | /reward_earning | Create a reward earning |
| GET | /reward_earning | List reward earnings |
| GET | /reward_earning/{id} | Get a reward earning |

### reward_earning_fulfillment
| Method | Path | Description |
|--------|------|-------------|
| POST | /reward_earning_fulfillment | Create a reward earning fulfillment |
| GET | /reward_earning_fulfillment | List reward earning fulfillments |
| GET | /reward_earning_fulfillment/{id} | Get a reward earning fulfillment |

### reward_program_activation
| Method | Path | Description |
|--------|------|-------------|
| POST | /reward_program_activation | Create a reward program activation |
| GET | /reward_program_activation | List reward program activations |
| GET | /reward_program_activation/{id} | Get a reward program activation |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a token?" -> POST /oauth/token
- "List all groups?" -> GET /oauth/token/{id}/groups
- "List all organization?" -> GET /oauth/token/{id}/organization
- "Get organization details?" -> GET /organization/{id}
- "Create a group?" -> POST /group
- "List all group?" -> GET /group
- "Get group details?" -> GET /group/{id}
- "List all coach?" -> GET /coach
- "Get coach details?" -> GET /coach/{id}
- "Create a reward_program?" -> POST /reward_program
- "List all reward_program?" -> GET /reward_program
- "Get reward_program details?" -> GET /reward_program/{id}
- "List all group?" -> GET /reward_program/{id}/group
- "Create a action?" -> POST /action
- "Get action details?" -> GET /action/{id}
- "Partially update a action?" -> PATCH /action/{id}
- "Create a bundle?" -> POST /bundle
- "Get bundle details?" -> GET /bundle/{id}
- "Partially update a bundle?" -> PATCH /bundle/{id}
- "Create a calendar_event?" -> POST /calendar_event
- "List all calendar_event?" -> GET /calendar_event
- "Get calendar_event details?" -> GET /calendar_event/{id}
- "Partially update a calendar_event?" -> PATCH /calendar_event/{id}
- "Delete a calendar_event?" -> DELETE /calendar_event/{id}
- "Create a calendar_event_response?" -> POST /calendar_event_response
- "List all email_history?" -> GET /email_history
- "Get email_history details?" -> GET /email_history/{id}
- "List all health_profile?" -> GET /health_profile
- "Get health_profile details?" -> GET /health_profile/{id}
- "List all health_profile_question?" -> GET /health_profile_question
- "Get health_profile_question details?" -> GET /health_profile_question/{id}
- "List all health_profile_answer?" -> GET /health_profile_answer
- "Get health_profile_answer details?" -> GET /health_profile_answer/{id}
- "List all health_question_definition?" -> GET /health_question_definition
- "Get health_question_definition details?" -> GET /health_question_definition/{id}
- "Create a patient_health_metric?" -> POST /patient_health_metric
- "List all patient_health_metric?" -> GET /patient_health_metric
- "Get patient_health_metric details?" -> GET /patient_health_metric/{id}
- "Create a patient?" -> POST /patient
- "List all patient?" -> GET /patient
- "Get patient details?" -> GET /patient/{id}
- "Partially update a patient?" -> PATCH /patient/{id}
- "List all groups?" -> GET /patient/{id}/groups
- "List all coaches?" -> GET /patient/{id}/coaches
- "List all patient_plan_summary?" -> GET /patient_plan_summary
- "Get patient_plan_summary details?" -> GET /patient_plan_summary/{id}
- "Partially update a patient_plan_summary?" -> PATCH /patient_plan_summary/{id}
- "List all result?" -> GET /result
- "Get result details?" -> GET /result/{id}
- "Create a reward?" -> POST /reward
- "List all reward?" -> GET /reward
- "Get reward details?" -> GET /reward/{id}
- "Create a reward_earning?" -> POST /reward_earning
- "List all reward_earning?" -> GET /reward_earning
- "Get reward_earning details?" -> GET /reward_earning/{id}
- "Create a reward_earning_fulfillment?" -> POST /reward_earning_fulfillment
- "List all reward_earning_fulfillment?" -> GET /reward_earning_fulfillment
- "Get reward_earning_fulfillment details?" -> GET /reward_earning_fulfillment/{id}
- "Create a reward_program_activation?" -> POST /reward_program_activation
- "List all reward_program_activation?" -> GET /reward_program_activation
- "Get reward_program_activation details?" -> GET /reward_program_activation/{id}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
