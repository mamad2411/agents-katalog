---
name: qnamaker-runtime-client
description: "QnAMaker Runtime Client API skill. Use when working with QnAMaker Runtime Client for knowledgebases. Covers 2 endpoints."
version: 1.0.0
generator: lapsh
---

# QnAMaker Runtime Client
API version: 4.0

## Auth
ApiKey Authorization in header

## Base URL
Not specified.

## Setup
1. Set your API key in the appropriate header
3. POST /knowledgebases/{kbId}/generateAnswer -- create first generateAnswer

## Endpoints

2 endpoints across 1 groups. See references/api-spec.lap for full details.

### knowledgebases
| Method | Path | Description |
|--------|------|-------------|
| POST | /knowledgebases/{kbId}/generateAnswer | GenerateAnswer call to query the knowledgebase. |
| POST | /knowledgebases/{kbId}/train | Train call to add suggestions to the knowledgebase. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a generateAnswer?" -> POST /knowledgebases/{kbId}/generateAnswer
- "Create a train?" -> POST /knowledgebases/{kbId}/train
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
