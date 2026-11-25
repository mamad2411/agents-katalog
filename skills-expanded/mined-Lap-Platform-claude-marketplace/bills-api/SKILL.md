---
name: bills-api
description: "Bills API skill. Use when working with Bills for api. Covers 21 endpoints."
version: 1.0.0
generator: lapsh
---

# Bills API
API version: v1

## Auth
No authentication required.

## Base URL
Not specified.

## Setup
1. No auth setup needed
2. GET /api/v1/BillTypes -- verify access

## Endpoints

21 endpoints across 1 groups. See references/api-spec.lap for full details.

### api
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/v1/Bills/{billId}/Stages/{billStageId}/Amendments | Returns a list of amendments. |
| GET | /api/v1/Bills/{billId}/Stages/{billStageId}/Amendments/{amendmentId} | Returns an amendment. |
| GET | /api/v1/Bills/{billId}/NewsArticles | Returns a list of news articles for a Bill. |
| GET | /api/v1/BillTypes | Returns a list of Bill types. |
| GET | /api/v1/Bills | Returns a list of Bills. |
| GET | /api/v1/Bills/{billId} | Return a Bill. |
| GET | /api/v1/Bills/{billId}/Stages/{billStageId} | Returns a Bill stage. |
| GET | /api/v1/Bills/{billId}/Stages | Returns all Bill stages. |
| GET | /api/v1/Publications/{publicationId}/Documents/{documentId} | Return information on a document. |
| GET | /api/v1/Publications/{publicationId}/Documents/{documentId}/Download | Return a document. |
| GET | /api/v1/Bills/{billId}/Stages/{billStageId}/PingPongItems | Returns a list of motions or amendments. |
| GET | /api/v1/Bills/{billId}/Stages/{billStageId}/PingPongItems/{pingPongItemId} | Returns amendment or motion detail. |
| GET | /api/v1/PublicationTypes | Returns a list of publication types. |
| GET | /api/v1/Bills/{billId}/Publications | Return a list of Bill publications. |
| GET | /api/v1/Bills/{billId}/Stages/{stageId}/Publications | Return a list of Bill stage publications. |
| GET | /api/v1/Rss/allbills.rss | Returns an Rss feed of all Bills. |
| GET | /api/v1/Rss/publicbills.rss | Returns an Rss feed of public Bills. |
| GET | /api/v1/Rss/privatebills.rss | Returns an Rss feed of private Bills. |
| GET | /api/v1/Rss/Bills/{id}.rss | Returns an Rss feed of a certain Bill. |
| GET | /api/v1/Sittings | Returns a list of Sittings. |
| GET | /api/v1/Stages | Returns a list of Bill stages. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all Amendments?" -> GET /api/v1/Bills/{billId}/Stages/{billStageId}/Amendments
- "Get Amendment details?" -> GET /api/v1/Bills/{billId}/Stages/{billStageId}/Amendments/{amendmentId}
- "List all NewsArticles?" -> GET /api/v1/Bills/{billId}/NewsArticles
- "List all BillTypes?" -> GET /api/v1/BillTypes
- "List all Bills?" -> GET /api/v1/Bills
- "Get Bill details?" -> GET /api/v1/Bills/{billId}
- "Get Stage details?" -> GET /api/v1/Bills/{billId}/Stages/{billStageId}
- "List all Stages?" -> GET /api/v1/Bills/{billId}/Stages
- "Get Document details?" -> GET /api/v1/Publications/{publicationId}/Documents/{documentId}
- "List all Download?" -> GET /api/v1/Publications/{publicationId}/Documents/{documentId}/Download
- "List all PingPongItems?" -> GET /api/v1/Bills/{billId}/Stages/{billStageId}/PingPongItems
- "Get PingPongItem details?" -> GET /api/v1/Bills/{billId}/Stages/{billStageId}/PingPongItems/{pingPongItemId}
- "List all PublicationTypes?" -> GET /api/v1/PublicationTypes
- "List all Publications?" -> GET /api/v1/Bills/{billId}/Publications
- "List all Publications?" -> GET /api/v1/Bills/{billId}/Stages/{stageId}/Publications
- "List all allbills.rss?" -> GET /api/v1/Rss/allbills.rss
- "List all publicbills.rss?" -> GET /api/v1/Rss/publicbills.rss
- "List all privatebills.rss?" -> GET /api/v1/Rss/privatebills.rss
- "Get Bill details?" -> GET /api/v1/Rss/Bills/{id}.rss
- "List all Sittings?" -> GET /api/v1/Sittings
- "List all Stages?" -> GET /api/v1/Stages

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
