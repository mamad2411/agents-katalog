---
name: pipelines
description: "Pipelines API skill. Use when working with Pipelines for crm. Covers 14 endpoints."
version: 1.0.0
generator: lapsh
---

# Pipelines
API version: v3

## Auth
OAuth2 | ApiKey private-app-legacy in header | ApiKey private-app in header

## Base URL
https://api.hubapi.com

## Setup
1. Set your API key in the appropriate header
2. GET /crm/v3/pipelines/{objectType}/{pipelineId}/audit -- verify access
3. POST /crm/v3/pipelines/{objectType} -- create first pipelines

## Endpoints

14 endpoints across 1 groups. See references/api-spec.lap for full details.

### crm
| Method | Path | Description |
|--------|------|-------------|
| GET | /crm/v3/pipelines/{objectType} | Retrieve all pipelines |
| POST | /crm/v3/pipelines/{objectType} | Create a pipeline |
| GET | /crm/v3/pipelines/{objectType}/{pipelineId} | Return a pipeline by ID |
| PUT | /crm/v3/pipelines/{objectType}/{pipelineId} | Replace a pipeline |
| DELETE | /crm/v3/pipelines/{objectType}/{pipelineId} | Delete a pipeline |
| PATCH | /crm/v3/pipelines/{objectType}/{pipelineId} | Perform a partial update of the pipeline identified by pipelineId. |
| GET | /crm/v3/pipelines/{objectType}/{pipelineId}/audit | Return an audit of all changes to the pipeline |
| GET | /crm/v3/pipelines/{objectType}/{pipelineId}/stages | Return all stages of a pipeline |
| POST | /crm/v3/pipelines/{objectType}/{pipelineId}/stages | Create a pipeline stage |
| GET | /crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId} | Return a pipeline stage by ID |
| PUT | /crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId} | Replace a pipeline stage |
| DELETE | /crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId} | Delete a pipeline stage |
| PATCH | /crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId} | Update specific properties of an existing pipeline stage. |
| GET | /crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}/audit | Retrieve a reverse chronological list of all changes made to a specific pipeline stage. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get pipeline details?" -> GET /crm/v3/pipelines/{objectType}
- "Get pipeline details?" -> GET /crm/v3/pipelines/{objectType}/{pipelineId}
- "Update a pipeline?" -> PUT /crm/v3/pipelines/{objectType}/{pipelineId}
- "Delete a pipeline?" -> DELETE /crm/v3/pipelines/{objectType}/{pipelineId}
- "Partially update a pipeline?" -> PATCH /crm/v3/pipelines/{objectType}/{pipelineId}
- "List all audit?" -> GET /crm/v3/pipelines/{objectType}/{pipelineId}/audit
- "List all stages?" -> GET /crm/v3/pipelines/{objectType}/{pipelineId}/stages
- "Create a stage?" -> POST /crm/v3/pipelines/{objectType}/{pipelineId}/stages
- "Get stage details?" -> GET /crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}
- "Update a stage?" -> PUT /crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}
- "Delete a stage?" -> DELETE /crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}
- "Partially update a stage?" -> PATCH /crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}
- "List all audit?" -> GET /crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}/audit
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
