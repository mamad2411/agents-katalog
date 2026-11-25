---
name: google-docs-api
description: "Google Docs API skill. Use when working with Google Docs for documents. Covers 3 endpoints."
version: 1.0.0
generator: lapsh
---

# Google Docs API
API version: v1

## Auth
OAuth2 | OAuth2

## Base URL
https://docs.googleapis.com/

## Setup
1. Configure auth: OAuth2 | OAuth2
2. GET /v1/documents/{documentId} -- verify access
3. POST /v1/documents -- create first documents

## Endpoints

3 endpoints across 1 groups. See references/api-spec.lap for full details.

### documents
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/documents | Creates a blank document using the title given in the request. Other fields in the request, including any provided content, are ignored. Returns the created document. |
| GET | /v1/documents/{documentId} | Gets the latest version of the specified document. |
| POST | /v1/documents/{documentId}:batchUpdate | Applies one or more updates to the document. Each request is validated before being applied. If any request is not valid, then the entire request will fail and nothing will be applied. Some requests have replies to give you some information about how they are applied. Other requests do not need to return information; these each return an empty reply. The order of replies matches that of the requests. For example, suppose you call batchUpdate with four updates, and only the third one returns information. The response would have two empty replies, the reply to the third request, and another empty reply, in that order. Because other users may be editing the document, the document might not exactly reflect your changes: your changes may be altered with respect to collaborator changes. If there are no collaborators, the document should reflect your changes. In any case, the updates in your request are guaranteed to be applied together atomically. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a document?" -> POST /v1/documents
- "Get document details?" -> GET /v1/documents/{documentId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
