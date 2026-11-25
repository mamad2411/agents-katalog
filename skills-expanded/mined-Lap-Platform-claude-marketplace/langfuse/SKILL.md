---
name: langfuse
description: "langfuse API skill. Use when working with langfuse for api. Covers 86 endpoints."
version: 1.0.0
generator: lapsh
---

# langfuse

## Auth
Bearer basic

## Base URL
Not specified.

## Setup
1. Set Authorization header with your Bearer token
2. GET /api/public/annotation-queues -- verify access
3. POST /api/public/annotation-queues -- create first annotation-queues

## Endpoints

86 endpoints across 1 groups. See references/api-spec.lap for full details.

### api
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/public/annotation-queues | Get all annotation queues |
| POST | /api/public/annotation-queues | Create an annotation queue |
| GET | /api/public/annotation-queues/{queueId} | Get an annotation queue by ID |
| GET | /api/public/annotation-queues/{queueId}/items | Get items for a specific annotation queue |
| POST | /api/public/annotation-queues/{queueId}/items | Add an item to an annotation queue |
| GET | /api/public/annotation-queues/{queueId}/items/{itemId} | Get a specific item from an annotation queue |
| PATCH | /api/public/annotation-queues/{queueId}/items/{itemId} | Update an annotation queue item |
| DELETE | /api/public/annotation-queues/{queueId}/items/{itemId} | Remove an item from an annotation queue |
| POST | /api/public/annotation-queues/{queueId}/assignments | Create an assignment for a user to an annotation queue |
| DELETE | /api/public/annotation-queues/{queueId}/assignments | Delete an assignment for a user to an annotation queue |
| GET | /api/public/integrations/blob-storage | Get all blob storage integrations for the organization (requires organization-scoped API key) |
| PUT | /api/public/integrations/blob-storage | Create or update a blob storage integration for a specific project (requires organization-scoped API key). The configuration is validated by performing a test upload to the bucket. |
| DELETE | /api/public/integrations/blob-storage/{id} | Delete a blob storage integration by ID (requires organization-scoped API key) |
| POST | /api/public/comments | Create a comment. Comments may be attached to different object types (trace, observation, session, prompt). |
| GET | /api/public/comments | Get all comments |
| GET | /api/public/comments/{commentId} | Get a comment by id |
| POST | /api/public/dataset-items | Create a dataset item |
| GET | /api/public/dataset-items | Get dataset items. Optionally specify a version to get the items as they existed at that point in time. |
| GET | /api/public/dataset-items/{id} | Get a dataset item |
| DELETE | /api/public/dataset-items/{id} | Delete a dataset item and all its run items. This action is irreversible. |
| POST | /api/public/dataset-run-items | Create a dataset run item |
| GET | /api/public/dataset-run-items | List dataset run items |
| GET | /api/public/v2/datasets | Get all datasets |
| POST | /api/public/v2/datasets | Create a dataset |
| GET | /api/public/v2/datasets/{datasetName} | Get a dataset |
| GET | /api/public/datasets/{datasetName}/runs/{runName} | Get a dataset run and its items |
| DELETE | /api/public/datasets/{datasetName}/runs/{runName} | Delete a dataset run and all its run items. This action is irreversible. |
| GET | /api/public/datasets/{datasetName}/runs | Get dataset runs |
| GET | /api/public/health | Check health of API and database |
| POST | /api/public/ingestion | **Legacy endpoint for batch ingestion for Langfuse Observability.** |
| GET | /api/public/metrics | Get metrics from the Langfuse project using a query object. |
| GET | /api/public/observations/{observationId} | Get a observation |
| GET | /api/public/observations | Get a list of observations. |
| POST | /api/public/scores | Create a score (supports both trace and session scores) |
| DELETE | /api/public/scores/{scoreId} | Delete a score (supports both trace and session scores) |
| GET | /api/public/llm-connections | Get all LLM connections in a project |
| PUT | /api/public/llm-connections | Create or update an LLM connection. The connection is upserted on provider. |
| GET | /api/public/media/{mediaId} | Get a media record |
| PATCH | /api/public/media/{mediaId} | Patch a media record |
| POST | /api/public/media | Get a presigned upload URL for a media record |
| GET | /api/public/v2/metrics | Get metrics from the Langfuse project using a query object. V2 endpoint with optimized performance. |
| POST | /api/public/models | Create a model |
| GET | /api/public/models | Get all models |
| GET | /api/public/models/{id} | Get a model |
| DELETE | /api/public/models/{id} | Delete a model. Cannot delete models managed by Langfuse. You can create your own definition with the same modelName to override the definition though. |
| GET | /api/public/v2/observations | Get a list of observations with cursor-based pagination and flexible field selection. |
| POST | /api/public/otel/v1/traces | **OpenTelemetry Traces Ingestion Endpoint** |
| GET | /api/public/organizations/memberships | Get all memberships for the organization associated with the API key (requires organization-scoped API key) |
| PUT | /api/public/organizations/memberships | Create or update a membership for the organization associated with the API key (requires organization-scoped API key) |
| DELETE | /api/public/organizations/memberships | Delete a membership from the organization associated with the API key (requires organization-scoped API key) |
| GET | /api/public/projects/{projectId}/memberships | Get all memberships for a specific project (requires organization-scoped API key) |
| PUT | /api/public/projects/{projectId}/memberships | Create or update a membership for a specific project (requires organization-scoped API key). The user must already be a member of the organization. |
| DELETE | /api/public/projects/{projectId}/memberships | Delete a membership from a specific project (requires organization-scoped API key). The user must be a member of the organization. |
| GET | /api/public/organizations/projects | Get all projects for the organization associated with the API key (requires organization-scoped API key) |
| GET | /api/public/organizations/apiKeys | Get all API keys for the organization associated with the API key (requires organization-scoped API key) |
| GET | /api/public/projects | Get Project associated with API key (requires project-scoped API key). You can use GET /api/public/organizations/projects to get all projects with an organization-scoped key. |
| POST | /api/public/projects | Create a new project (requires organization-scoped API key) |
| PUT | /api/public/projects/{projectId} | Update a project by ID (requires organization-scoped API key). |
| DELETE | /api/public/projects/{projectId} | Delete a project by ID (requires organization-scoped API key). Project deletion is processed asynchronously. |
| GET | /api/public/projects/{projectId}/apiKeys | Get all API keys for a project (requires organization-scoped API key) |
| POST | /api/public/projects/{projectId}/apiKeys | Create a new API key for a project (requires organization-scoped API key) |
| DELETE | /api/public/projects/{projectId}/apiKeys/{apiKeyId} | Delete an API key for a project (requires organization-scoped API key) |
| PATCH | /api/public/v2/prompts/{name}/versions/{version} | Update labels for a specific prompt version |
| GET | /api/public/v2/prompts/{promptName} | Get a prompt |
| DELETE | /api/public/v2/prompts/{promptName} | Delete prompt versions. If neither version nor label is specified, all versions of the prompt are deleted. |
| GET | /api/public/v2/prompts | Get a list of prompt names with versions and labels |
| POST | /api/public/v2/prompts | Create a new version for the prompt with the given `name` |
| GET | /api/public/scim/ServiceProviderConfig | Get SCIM Service Provider Configuration (requires organization-scoped API key) |
| GET | /api/public/scim/ResourceTypes | Get SCIM Resource Types (requires organization-scoped API key) |
| GET | /api/public/scim/Schemas | Get SCIM Schemas (requires organization-scoped API key) |
| GET | /api/public/scim/Users | List users in the organization (requires organization-scoped API key) |
| POST | /api/public/scim/Users | Create a new user in the organization (requires organization-scoped API key) |
| GET | /api/public/scim/Users/{userId} | Get a specific user by ID (requires organization-scoped API key) |
| DELETE | /api/public/scim/Users/{userId} | Remove a user from the organization (requires organization-scoped API key). Note that this only removes the user from the organization but does not delete the user entity itself. |
| POST | /api/public/score-configs | Create a score configuration (config). Score configs are used to define the structure of scores |
| GET | /api/public/score-configs | Get all score configs |
| GET | /api/public/score-configs/{configId} | Get a score config |
| PATCH | /api/public/score-configs/{configId} | Update a score config |
| GET | /api/public/v2/scores | Get a list of scores (supports both trace and session scores) |
| GET | /api/public/v2/scores/{scoreId} | Get a score (supports both trace and session scores) |
| GET | /api/public/sessions | Get sessions |
| GET | /api/public/sessions/{sessionId} | Get a session. Please note that `traces` on this endpoint are not paginated, if you plan to fetch large sessions, consider `GET /api/public/traces?sessionId=<sessionId>` |
| GET | /api/public/traces/{traceId} | Get a specific trace |
| DELETE | /api/public/traces/{traceId} | Delete a specific trace |
| GET | /api/public/traces | Get list of traces |
| DELETE | /api/public/traces | Delete multiple traces |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all annotation-queues?" -> GET /api/public/annotation-queues
- "Create a annotation-queue?" -> POST /api/public/annotation-queues
- "Get annotation-queue details?" -> GET /api/public/annotation-queues/{queueId}
- "List all items?" -> GET /api/public/annotation-queues/{queueId}/items
- "Create a item?" -> POST /api/public/annotation-queues/{queueId}/items
- "Get item details?" -> GET /api/public/annotation-queues/{queueId}/items/{itemId}
- "Partially update a item?" -> PATCH /api/public/annotation-queues/{queueId}/items/{itemId}
- "Delete a item?" -> DELETE /api/public/annotation-queues/{queueId}/items/{itemId}
- "Create a assignment?" -> POST /api/public/annotation-queues/{queueId}/assignments
- "List all blob-storage?" -> GET /api/public/integrations/blob-storage
- "Delete a blob-storage?" -> DELETE /api/public/integrations/blob-storage/{id}
- "Create a comment?" -> POST /api/public/comments
- "List all comments?" -> GET /api/public/comments
- "Get comment details?" -> GET /api/public/comments/{commentId}
- "Create a dataset-item?" -> POST /api/public/dataset-items
- "List all dataset-items?" -> GET /api/public/dataset-items
- "Get dataset-item details?" -> GET /api/public/dataset-items/{id}
- "Delete a dataset-item?" -> DELETE /api/public/dataset-items/{id}
- "Create a dataset-run-item?" -> POST /api/public/dataset-run-items
- "List all dataset-run-items?" -> GET /api/public/dataset-run-items
- "List all datasets?" -> GET /api/public/v2/datasets
- "Create a dataset?" -> POST /api/public/v2/datasets
- "Get dataset details?" -> GET /api/public/v2/datasets/{datasetName}
- "Get run details?" -> GET /api/public/datasets/{datasetName}/runs/{runName}
- "Delete a run?" -> DELETE /api/public/datasets/{datasetName}/runs/{runName}
- "List all runs?" -> GET /api/public/datasets/{datasetName}/runs
- "List all health?" -> GET /api/public/health
- "Create a ingestion?" -> POST /api/public/ingestion
- "Search metrics?" -> GET /api/public/metrics
- "Get observation details?" -> GET /api/public/observations/{observationId}
- "List all observations?" -> GET /api/public/observations
- "Create a score?" -> POST /api/public/scores
- "Delete a score?" -> DELETE /api/public/scores/{scoreId}
- "List all llm-connections?" -> GET /api/public/llm-connections
- "Get media details?" -> GET /api/public/media/{mediaId}
- "Partially update a media?" -> PATCH /api/public/media/{mediaId}
- "Create a media?" -> POST /api/public/media
- "Search metrics?" -> GET /api/public/v2/metrics
- "Create a model?" -> POST /api/public/models
- "List all models?" -> GET /api/public/models
- "Get model details?" -> GET /api/public/models/{id}
- "Delete a model?" -> DELETE /api/public/models/{id}
- "List all observations?" -> GET /api/public/v2/observations
- "Create a trace?" -> POST /api/public/otel/v1/traces
- "List all memberships?" -> GET /api/public/organizations/memberships
- "List all memberships?" -> GET /api/public/projects/{projectId}/memberships
- "List all projects?" -> GET /api/public/organizations/projects
- "List all apiKeys?" -> GET /api/public/organizations/apiKeys
- "List all projects?" -> GET /api/public/projects
- "Create a project?" -> POST /api/public/projects
- "Update a project?" -> PUT /api/public/projects/{projectId}
- "Delete a project?" -> DELETE /api/public/projects/{projectId}
- "List all apiKeys?" -> GET /api/public/projects/{projectId}/apiKeys
- "Create a apiKey?" -> POST /api/public/projects/{projectId}/apiKeys
- "Delete a apiKey?" -> DELETE /api/public/projects/{projectId}/apiKeys/{apiKeyId}
- "Partially update a version?" -> PATCH /api/public/v2/prompts/{name}/versions/{version}
- "Get prompt details?" -> GET /api/public/v2/prompts/{promptName}
- "Delete a prompt?" -> DELETE /api/public/v2/prompts/{promptName}
- "List all prompts?" -> GET /api/public/v2/prompts
- "Create a prompt?" -> POST /api/public/v2/prompts
- "List all ServiceProviderConfig?" -> GET /api/public/scim/ServiceProviderConfig
- "List all ResourceTypes?" -> GET /api/public/scim/ResourceTypes
- "List all Schemas?" -> GET /api/public/scim/Schemas
- "List all Users?" -> GET /api/public/scim/Users
- "Create a User?" -> POST /api/public/scim/Users
- "Get User details?" -> GET /api/public/scim/Users/{userId}
- "Delete a User?" -> DELETE /api/public/scim/Users/{userId}
- "Create a score-config?" -> POST /api/public/score-configs
- "List all score-configs?" -> GET /api/public/score-configs
- "Get score-config details?" -> GET /api/public/score-configs/{configId}
- "Partially update a score-config?" -> PATCH /api/public/score-configs/{configId}
- "List all scores?" -> GET /api/public/v2/scores
- "Get score details?" -> GET /api/public/v2/scores/{scoreId}
- "List all sessions?" -> GET /api/public/sessions
- "Get session details?" -> GET /api/public/sessions/{sessionId}
- "Get trace details?" -> GET /api/public/traces/{traceId}
- "Delete a trace?" -> DELETE /api/public/traces/{traceId}
- "List all traces?" -> GET /api/public/traces
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
