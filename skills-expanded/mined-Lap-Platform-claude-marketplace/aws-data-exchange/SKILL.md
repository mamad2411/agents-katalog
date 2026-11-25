---
name: aws-data-exchange
description: "AWS Data Exchange API skill. Use when working with AWS Data Exchange for jobs, data-sets, event-actions. Covers 30 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS Data Exchange
API version: 2017-07-25

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /v1/data-sets -- verify access
3. POST /v1/data-sets -- create first data-sets

## Endpoints

30 endpoints across 5 groups. See references/api-spec.lap for full details.

### jobs
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /v1/jobs/{JobId} | This operation cancels a job. Jobs can be cancelled only when they are in the WAITING state. |
| POST | /v1/jobs | This operation creates a job. |
| GET | /v1/jobs/{JobId} | This operation returns information about a job. |
| GET | /v1/jobs | This operation lists your jobs sorted by CreatedAt in descending order. |
| PATCH | /v1/jobs/{JobId} | This operation starts a job. |

### data-sets
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/data-sets | This operation creates a data set. |
| POST | /v1/data-sets/{DataSetId}/revisions | This operation creates a revision for a data set. |
| DELETE | /v1/data-sets/{DataSetId}/revisions/{RevisionId}/assets/{AssetId} | This operation deletes an asset. |
| DELETE | /v1/data-sets/{DataSetId} | This operation deletes a data set. |
| DELETE | /v1/data-sets/{DataSetId}/revisions/{RevisionId} | This operation deletes a revision. |
| GET | /v1/data-sets/{DataSetId}/revisions/{RevisionId}/assets/{AssetId} | This operation returns information about an asset. |
| GET | /v1/data-sets/{DataSetId} | This operation returns information about a data set. |
| GET | /v1/data-sets/{DataSetId}/revisions/{RevisionId} | This operation returns information about a revision. |
| GET | /v1/data-sets/{DataSetId}/revisions | This operation lists a data set's revisions sorted by CreatedAt in descending order. |
| GET | /v1/data-sets | This operation lists your data sets. When listing by origin OWNED, results are sorted by CreatedAt in descending order. When listing by origin ENTITLED, there is no order and the maxResults parameter is ignored. |
| GET | /v1/data-sets/{DataSetId}/revisions/{RevisionId}/assets | This operation lists a revision's assets sorted alphabetically in descending order. |
| POST | /v1/data-sets/{DataSetId}/revisions/{RevisionId}/revoke | This operation revokes subscribers' access to a revision. |
| POST | /v1/data-sets/{DataSetId}/notification | The type of event associated with the data set. |
| PATCH | /v1/data-sets/{DataSetId}/revisions/{RevisionId}/assets/{AssetId} | This operation updates an asset. |
| PATCH | /v1/data-sets/{DataSetId} | This operation updates a data set. |
| PATCH | /v1/data-sets/{DataSetId}/revisions/{RevisionId} | This operation updates a revision. |

### event-actions
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/event-actions | This operation creates an event action. |
| DELETE | /v1/event-actions/{EventActionId} | This operation deletes the event action. |
| GET | /v1/event-actions/{EventActionId} | This operation retrieves information about an event action. |
| GET | /v1/event-actions | This operation lists your event actions. |
| PATCH | /v1/event-actions/{EventActionId} | This operation updates the event action. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags/{ResourceArn} | This operation lists the tags on the resource. |
| POST | /tags/{ResourceArn} | This operation tags a resource. |
| DELETE | /tags/{ResourceArn} | This operation removes one or more tags from a resource. |

### v1
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1 | This operation invokes an API Gateway API asset. The request is proxied to the provider’s API Gateway API. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Delete a job?" -> DELETE /v1/jobs/{JobId}
- "Create a data-set?" -> POST /v1/data-sets
- "Create a event-action?" -> POST /v1/event-actions
- "Create a job?" -> POST /v1/jobs
- "Create a revision?" -> POST /v1/data-sets/{DataSetId}/revisions
- "Delete a asset?" -> DELETE /v1/data-sets/{DataSetId}/revisions/{RevisionId}/assets/{AssetId}
- "Delete a data-set?" -> DELETE /v1/data-sets/{DataSetId}
- "Delete a event-action?" -> DELETE /v1/event-actions/{EventActionId}
- "Delete a revision?" -> DELETE /v1/data-sets/{DataSetId}/revisions/{RevisionId}
- "Get asset details?" -> GET /v1/data-sets/{DataSetId}/revisions/{RevisionId}/assets/{AssetId}
- "Get data-set details?" -> GET /v1/data-sets/{DataSetId}
- "Get event-action details?" -> GET /v1/event-actions/{EventActionId}
- "Get job details?" -> GET /v1/jobs/{JobId}
- "Get revision details?" -> GET /v1/data-sets/{DataSetId}/revisions/{RevisionId}
- "List all revisions?" -> GET /v1/data-sets/{DataSetId}/revisions
- "List all data-sets?" -> GET /v1/data-sets
- "List all event-actions?" -> GET /v1/event-actions
- "List all jobs?" -> GET /v1/jobs
- "List all assets?" -> GET /v1/data-sets/{DataSetId}/revisions/{RevisionId}/assets
- "Get tag details?" -> GET /tags/{ResourceArn}
- "Create a revoke?" -> POST /v1/data-sets/{DataSetId}/revisions/{RevisionId}/revoke
- "Create a notification?" -> POST /v1/data-sets/{DataSetId}/notification
- "Partially update a job?" -> PATCH /v1/jobs/{JobId}
- "Delete a tag?" -> DELETE /tags/{ResourceArn}
- "Partially update a asset?" -> PATCH /v1/data-sets/{DataSetId}/revisions/{RevisionId}/assets/{AssetId}
- "Partially update a data-set?" -> PATCH /v1/data-sets/{DataSetId}
- "Partially update a event-action?" -> PATCH /v1/event-actions/{EventActionId}
- "Partially update a revision?" -> PATCH /v1/data-sets/{DataSetId}/revisions/{RevisionId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
