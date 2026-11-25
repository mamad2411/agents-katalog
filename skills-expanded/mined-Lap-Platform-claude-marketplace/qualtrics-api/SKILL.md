---
name: qualtrics-api
description: "Qualtrics API skill. Use when working with Qualtrics for survey-definitions, distributions, directories. Covers 8 endpoints."
version: 1.0.0
generator: lapsh
---

# Qualtrics API
API version: 0.2

## Auth
ApiKey X-API-TOKEN in header

## Base URL
https://fra1.qualtrics.com/API/v3

## Setup
1. Set your API key in the appropriate header
2. GET /distributions -- verify access
3. POST /distributions -- create first distributions

## Endpoints

8 endpoints across 4 groups. See references/api-spec.lap for full details.

### survey-definitions
| Method | Path | Description |
|--------|------|-------------|
| GET | /survey-definitions/{SurveyId} | Get survey |

### distributions
| Method | Path | Description |
|--------|------|-------------|
| GET | /distributions | Get distributions for survey |
| POST | /distributions | Generate distribution links |
| GET | /distributions/{DistributionId}/links | Retrieve distribution links |

### directories
| Method | Path | Description |
|--------|------|-------------|
| POST | /directories/{DirectoryId}/mailinglists/{MailingListId}/contacts | Create contact in mailing list |

### eventsubscriptions
| Method | Path | Description |
|--------|------|-------------|
| POST | /eventsubscriptions/ | Triggers when a response is submitted to a qualtrics survey |
| DELETE | /eventsubscriptions/ | Remove subscription to response event |
| GET | /eventsubscriptions/{SubscriptionId} | Get event subscriptions |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get survey-definition details?" -> GET /survey-definitions/{SurveyId}
- "List all distributions?" -> GET /distributions
- "Create a distribution?" -> POST /distributions
- "List all links?" -> GET /distributions/{DistributionId}/links
- "Create a contact?" -> POST /directories/{DirectoryId}/mailinglists/{MailingListId}/contacts
- "Create a eventsubscription?" -> POST /eventsubscriptions/
- "Get eventsubscription details?" -> GET /eventsubscriptions/{SubscriptionId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
