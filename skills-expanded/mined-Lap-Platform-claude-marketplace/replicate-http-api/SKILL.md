---
name: replicate-http-api
description: "Replicate HTTP API skill. Use when working with Replicate HTTP for account, collections, deployments. Covers 36 endpoints."
version: 1.0.0
generator: lapsh
---

# Replicate HTTP API
API version: 1.0.0-a1

## Auth
Bearer bearer

## Base URL
https://api.replicate.com/v1

## Setup
1. Set Authorization header with your Bearer token
2. GET /account -- verify access
3. POST /deployments -- create first deployments

## Endpoints

36 endpoints across 10 groups. See references/api-spec.lap for full details.

### account
| Method | Path | Description |
|--------|------|-------------|
| GET | /account | Get the authenticated account |

### collections
| Method | Path | Description |
|--------|------|-------------|
| GET | /collections | List collections of models |
| GET | /collections/{collection_slug} | Get a collection of models |

### deployments
| Method | Path | Description |
|--------|------|-------------|
| GET | /deployments | List deployments |
| POST | /deployments | Create a deployment |
| DELETE | /deployments/{deployment_owner}/{deployment_name} | Delete a deployment |
| GET | /deployments/{deployment_owner}/{deployment_name} | Get a deployment |
| PATCH | /deployments/{deployment_owner}/{deployment_name} | Update a deployment |
| POST | /deployments/{deployment_owner}/{deployment_name}/predictions | Create a prediction using a deployment |

### files
| Method | Path | Description |
|--------|------|-------------|
| GET | /files | List files |
| POST | /files | Create a file |
| DELETE | /files/{file_id} | Delete a file |
| GET | /files/{file_id} | Get a file |
| GET | /files/{file_id}/download | Download a file |

### hardware
| Method | Path | Description |
|--------|------|-------------|
| GET | /hardware | List available hardware for models |

### models
| Method | Path | Description |
|--------|------|-------------|
| GET | /models | List public models |
| POST | /models | Create a model |
| DELETE | /models/{model_owner}/{model_name} | Delete a model |
| GET | /models/{model_owner}/{model_name} | Get a model |
| PATCH | /models/{model_owner}/{model_name} | Update metadata for a model |
| GET | /models/{model_owner}/{model_name}/examples | List examples for a model |
| POST | /models/{model_owner}/{model_name}/predictions | Create a prediction using an official model |
| GET | /models/{model_owner}/{model_name}/readme | Get a model's README |
| GET | /models/{model_owner}/{model_name}/versions | List model versions |
| DELETE | /models/{model_owner}/{model_name}/versions/{version_id} | Delete a model version |
| GET | /models/{model_owner}/{model_name}/versions/{version_id} | Get a model version |
| POST | /models/{model_owner}/{model_name}/versions/{version_id}/trainings | Create a training |

### predictions
| Method | Path | Description |
|--------|------|-------------|
| GET | /predictions | List predictions |
| POST | /predictions | Create a prediction |
| GET | /predictions/{prediction_id} | Get a prediction |
| POST | /predictions/{prediction_id}/cancel | Cancel a prediction |

### search
| Method | Path | Description |
|--------|------|-------------|
| GET | /search | Search models, collections, and docs (beta) |

### trainings
| Method | Path | Description |
|--------|------|-------------|
| GET | /trainings | List trainings |
| GET | /trainings/{training_id} | Get a training |
| POST | /trainings/{training_id}/cancel | Cancel a training |

### webhooks
| Method | Path | Description |
|--------|------|-------------|
| GET | /webhooks/default/secret | Get the signing secret for the default webhook |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all account?" -> GET /account
- "List all collections?" -> GET /collections
- "Get collection details?" -> GET /collections/{collection_slug}
- "List all deployments?" -> GET /deployments
- "Create a deployment?" -> POST /deployments
- "Delete a deployment?" -> DELETE /deployments/{deployment_owner}/{deployment_name}
- "Get deployment details?" -> GET /deployments/{deployment_owner}/{deployment_name}
- "Partially update a deployment?" -> PATCH /deployments/{deployment_owner}/{deployment_name}
- "Create a prediction?" -> POST /deployments/{deployment_owner}/{deployment_name}/predictions
- "List all files?" -> GET /files
- "Create a file?" -> POST /files
- "Delete a file?" -> DELETE /files/{file_id}
- "Get file details?" -> GET /files/{file_id}
- "List all download?" -> GET /files/{file_id}/download
- "List all hardware?" -> GET /hardware
- "List all models?" -> GET /models
- "Create a model?" -> POST /models
- "Delete a model?" -> DELETE /models/{model_owner}/{model_name}
- "Get model details?" -> GET /models/{model_owner}/{model_name}
- "Partially update a model?" -> PATCH /models/{model_owner}/{model_name}
- "List all examples?" -> GET /models/{model_owner}/{model_name}/examples
- "Create a prediction?" -> POST /models/{model_owner}/{model_name}/predictions
- "List all readme?" -> GET /models/{model_owner}/{model_name}/readme
- "List all versions?" -> GET /models/{model_owner}/{model_name}/versions
- "Delete a version?" -> DELETE /models/{model_owner}/{model_name}/versions/{version_id}
- "Get version details?" -> GET /models/{model_owner}/{model_name}/versions/{version_id}
- "Create a training?" -> POST /models/{model_owner}/{model_name}/versions/{version_id}/trainings
- "List all predictions?" -> GET /predictions
- "Create a prediction?" -> POST /predictions
- "Get prediction details?" -> GET /predictions/{prediction_id}
- "Create a cancel?" -> POST /predictions/{prediction_id}/cancel
- "Search search?" -> GET /search
- "List all trainings?" -> GET /trainings
- "Get training details?" -> GET /trainings/{training_id}
- "Create a cancel?" -> POST /trainings/{training_id}/cancel
- "List all secret?" -> GET /webhooks/default/secret
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
