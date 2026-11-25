---
name: annotations-api
description: "Annotations API skill. Use when working with Annotations for projects. Covers 7 endpoints."
version: 1.0.0
generator: lapsh
---

# Annotations API
API version: 1.0.0

## Auth
No authentication required.

## Base URL
Not specified.

## Setup
1. No auth setup needed
2. GET /projects/{projectId}/annotations -- verify access
3. POST /projects/{projectId}/annotations -- create first annotations

## Endpoints

7 endpoints across 1 groups. See references/api-spec.lap for full details.

### projects
| Method | Path | Description |
|--------|------|-------------|
| GET | /projects/{projectId}/annotations | List Annotations |
| POST | /projects/{projectId}/annotations | Create Annotations |
| GET | /projects/{projectId}/annotations/{annotationId} | Get Annotation |
| PATCH | /projects/{projectId}/annotations/{annotationId} | Patch Annotation |
| DELETE | /projects/{projectId}/annotations/{annotationId} | Delete Annotation |
| GET | /projects/{projectId}/annotations/tags | Get Annotation Tags |
| POST | /projects/{projectId}/annotations/tags | Create Annotation Tag |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all annotations?" -> GET /projects/{projectId}/annotations
- "Create a annotation?" -> POST /projects/{projectId}/annotations
- "Get annotation details?" -> GET /projects/{projectId}/annotations/{annotationId}
- "Partially update a annotation?" -> PATCH /projects/{projectId}/annotations/{annotationId}
- "Delete a annotation?" -> DELETE /projects/{projectId}/annotations/{annotationId}
- "List all tags?" -> GET /projects/{projectId}/annotations/tags
- "Create a tag?" -> POST /projects/{projectId}/annotations/tags

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
