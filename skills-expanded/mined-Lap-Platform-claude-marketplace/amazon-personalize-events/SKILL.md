---
name: amazon-personalize-events
description: "Amazon Personalize Events API skill. Use when working with Amazon Personalize Events for action-interactions, actions, events. Covers 5 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon Personalize Events
API version: 2018-03-22

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST /action-interactions -- create first action-interactions

## Endpoints

5 endpoints across 5 groups. See references/api-spec.lap for full details.

### action-interactions
| Method | Path | Description |
|--------|------|-------------|
| POST | /action-interactions | Records action interaction event data. An action interaction event is an interaction between a user and an action. For example, a user taking an action, such a enrolling in a membership program or downloading your app.  For more information about recording action interactions, see Recording action interaction events. For more information about actions in an Actions dataset, see Actions dataset. |

### actions
| Method | Path | Description |
|--------|------|-------------|
| POST | /actions | Adds one or more actions to an Actions dataset. For more information see Importing actions individually. |

### events
| Method | Path | Description |
|--------|------|-------------|
| POST | /events | Records item interaction event data. For more information see Recording item interaction events. |

### items
| Method | Path | Description |
|--------|------|-------------|
| POST | /items | Adds one or more items to an Items dataset. For more information see Importing items individually. |

### users
| Method | Path | Description |
|--------|------|-------------|
| POST | /users | Adds one or more users to a Users dataset. For more information see Importing users individually. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a action-interaction?" -> POST /action-interactions
- "Create a action?" -> POST /actions
- "Create a event?" -> POST /events
- "Create a item?" -> POST /items
- "Create a user?" -> POST /users
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
