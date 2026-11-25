---
name: lucidtech-api
description: "Lucidtech API skill. Use when working with Lucidtech for appClients, assets, datasets. Covers 133 endpoints."
version: 1.0.0
generator: lapsh
---

# Lucidtech API
API version: 2024-11-29T08:05:46Z

## Auth
OAuth2

## Base URL
https://api.lucidtech.ai/{basePath}

## Setup
1. Configure auth: OAuth2
2. GET /appClients -- verify access
3. POST /appClients -- create first appClients

## Endpoints

133 endpoints across 17 groups. See references/api-spec.lap for full details.

### appClients
| Method | Path | Description |
|--------|------|-------------|
| GET | /appClients |  |
| OPTIONS | /appClients |  |
| POST | /appClients |  |
| DELETE | /appClients/{appClientId} |  |
| GET | /appClients/{appClientId} |  |
| OPTIONS | /appClients/{appClientId} |  |
| PATCH | /appClients/{appClientId} |  |

### assets
| Method | Path | Description |
|--------|------|-------------|
| GET | /assets |  |
| OPTIONS | /assets |  |
| POST | /assets |  |
| DELETE | /assets/{assetId} |  |
| GET | /assets/{assetId} |  |
| OPTIONS | /assets/{assetId} |  |
| PATCH | /assets/{assetId} |  |

### datasets
| Method | Path | Description |
|--------|------|-------------|
| GET | /datasets |  |
| OPTIONS | /datasets |  |
| POST | /datasets |  |
| DELETE | /datasets/{datasetId} |  |
| GET | /datasets/{datasetId} |  |
| OPTIONS | /datasets/{datasetId} |  |
| PATCH | /datasets/{datasetId} |  |
| GET | /datasets/{datasetId}/transformations |  |
| OPTIONS | /datasets/{datasetId}/transformations |  |
| POST | /datasets/{datasetId}/transformations |  |
| DELETE | /datasets/{datasetId}/transformations/{transformationId} |  |
| OPTIONS | /datasets/{datasetId}/transformations/{transformationId} |  |

### deploymentEnvironments
| Method | Path | Description |
|--------|------|-------------|
| GET | /deploymentEnvironments |  |
| OPTIONS | /deploymentEnvironments |  |
| GET | /deploymentEnvironments/{deploymentEnvironmentId} |  |
| OPTIONS | /deploymentEnvironments/{deploymentEnvironmentId} |  |

### documents
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /documents |  |
| GET | /documents |  |
| OPTIONS | /documents |  |
| POST | /documents |  |
| DELETE | /documents/{documentId} |  |
| GET | /documents/{documentId} |  |
| OPTIONS | /documents/{documentId} |  |
| PATCH | /documents/{documentId} |  |

### logs
| Method | Path | Description |
|--------|------|-------------|
| GET | /logs |  |
| OPTIONS | /logs |  |
| GET | /logs/{logId} |  |
| OPTIONS | /logs/{logId} |  |

### models
| Method | Path | Description |
|--------|------|-------------|
| GET | /models |  |
| OPTIONS | /models |  |
| POST | /models |  |
| DELETE | /models/{modelId} |  |
| GET | /models/{modelId} |  |
| OPTIONS | /models/{modelId} |  |
| PATCH | /models/{modelId} |  |
| GET | /models/{modelId}/dataBundles |  |
| OPTIONS | /models/{modelId}/dataBundles |  |
| POST | /models/{modelId}/dataBundles |  |
| DELETE | /models/{modelId}/dataBundles/{dataBundleId} |  |
| GET | /models/{modelId}/dataBundles/{dataBundleId} |  |
| OPTIONS | /models/{modelId}/dataBundles/{dataBundleId} |  |
| PATCH | /models/{modelId}/dataBundles/{dataBundleId} |  |
| GET | /models/{modelId}/trainings |  |
| OPTIONS | /models/{modelId}/trainings |  |
| POST | /models/{modelId}/trainings |  |
| GET | /models/{modelId}/trainings/{trainingId} |  |
| OPTIONS | /models/{modelId}/trainings/{trainingId} |  |
| PATCH | /models/{modelId}/trainings/{trainingId} |  |

### organizations
| Method | Path | Description |
|--------|------|-------------|
| GET | /organizations |  |
| OPTIONS | /organizations |  |
| POST | /organizations |  |
| GET | /organizations/{organizationId} |  |
| OPTIONS | /organizations/{organizationId} |  |
| PATCH | /organizations/{organizationId} |  |

### paymentMethods
| Method | Path | Description |
|--------|------|-------------|
| GET | /paymentMethods |  |
| OPTIONS | /paymentMethods |  |
| POST | /paymentMethods |  |
| DELETE | /paymentMethods/{paymentMethodId} |  |
| GET | /paymentMethods/{paymentMethodId} |  |
| OPTIONS | /paymentMethods/{paymentMethodId} |  |
| PATCH | /paymentMethods/{paymentMethodId} |  |

### plans
| Method | Path | Description |
|--------|------|-------------|
| GET | /plans |  |
| OPTIONS | /plans |  |
| GET | /plans/{planId} |  |
| OPTIONS | /plans/{planId} |  |

### predictions
| Method | Path | Description |
|--------|------|-------------|
| GET | /predictions |  |
| OPTIONS | /predictions |  |
| POST | /predictions |  |
| GET | /predictions/{predictionId} |  |
| OPTIONS | /predictions/{predictionId} |  |

### profiles
| Method | Path | Description |
|--------|------|-------------|
| GET | /profiles/{profileId} |  |
| OPTIONS | /profiles/{profileId} |  |
| PATCH | /profiles/{profileId} |  |

### roles
| Method | Path | Description |
|--------|------|-------------|
| GET | /roles |  |
| OPTIONS | /roles |  |
| GET | /roles/{roleId} |  |
| OPTIONS | /roles/{roleId} |  |

### secrets
| Method | Path | Description |
|--------|------|-------------|
| GET | /secrets |  |
| OPTIONS | /secrets |  |
| POST | /secrets |  |
| DELETE | /secrets/{secretId} |  |
| OPTIONS | /secrets/{secretId} |  |
| PATCH | /secrets/{secretId} |  |

### transitions
| Method | Path | Description |
|--------|------|-------------|
| GET | /transitions |  |
| OPTIONS | /transitions |  |
| POST | /transitions |  |
| DELETE | /transitions/{transitionId} |  |
| GET | /transitions/{transitionId} |  |
| OPTIONS | /transitions/{transitionId} |  |
| PATCH | /transitions/{transitionId} |  |
| GET | /transitions/{transitionId}/executions |  |
| OPTIONS | /transitions/{transitionId}/executions |  |
| POST | /transitions/{transitionId}/executions |  |
| GET | /transitions/{transitionId}/executions/{executionId} |  |
| OPTIONS | /transitions/{transitionId}/executions/{executionId} |  |
| PATCH | /transitions/{transitionId}/executions/{executionId} |  |
| OPTIONS | /transitions/{transitionId}/executions/{executionId}/heartbeats |  |
| POST | /transitions/{transitionId}/executions/{executionId}/heartbeats |  |

### users
| Method | Path | Description |
|--------|------|-------------|
| GET | /users |  |
| OPTIONS | /users |  |
| POST | /users |  |
| DELETE | /users/{userId} |  |
| GET | /users/{userId} |  |
| OPTIONS | /users/{userId} |  |
| PATCH | /users/{userId} |  |

### workflows
| Method | Path | Description |
|--------|------|-------------|
| GET | /workflows |  |
| OPTIONS | /workflows |  |
| POST | /workflows |  |
| DELETE | /workflows/{workflowId} |  |
| GET | /workflows/{workflowId} |  |
| OPTIONS | /workflows/{workflowId} |  |
| PATCH | /workflows/{workflowId} |  |
| GET | /workflows/{workflowId}/executions |  |
| OPTIONS | /workflows/{workflowId}/executions |  |
| POST | /workflows/{workflowId}/executions |  |
| DELETE | /workflows/{workflowId}/executions/{executionId} |  |
| GET | /workflows/{workflowId}/executions/{executionId} |  |
| OPTIONS | /workflows/{workflowId}/executions/{executionId} |  |
| PATCH | /workflows/{workflowId}/executions/{executionId} |  |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all appClients?" -> GET /appClients
- "Create a appClient?" -> POST /appClients
- "Delete a appClient?" -> DELETE /appClients/{appClientId}
- "Get appClient details?" -> GET /appClients/{appClientId}
- "Partially update a appClient?" -> PATCH /appClients/{appClientId}
- "List all assets?" -> GET /assets
- "Create a asset?" -> POST /assets
- "Delete a asset?" -> DELETE /assets/{assetId}
- "Get asset details?" -> GET /assets/{assetId}
- "Partially update a asset?" -> PATCH /assets/{assetId}
- "List all datasets?" -> GET /datasets
- "Create a dataset?" -> POST /datasets
- "Delete a dataset?" -> DELETE /datasets/{datasetId}
- "Get dataset details?" -> GET /datasets/{datasetId}
- "Partially update a dataset?" -> PATCH /datasets/{datasetId}
- "List all transformations?" -> GET /datasets/{datasetId}/transformations
- "Create a transformation?" -> POST /datasets/{datasetId}/transformations
- "Delete a transformation?" -> DELETE /datasets/{datasetId}/transformations/{transformationId}
- "List all deploymentEnvironments?" -> GET /deploymentEnvironments
- "Get deploymentEnvironment details?" -> GET /deploymentEnvironments/{deploymentEnvironmentId}
- "List all documents?" -> GET /documents
- "Create a document?" -> POST /documents
- "Delete a document?" -> DELETE /documents/{documentId}
- "Get document details?" -> GET /documents/{documentId}
- "Partially update a document?" -> PATCH /documents/{documentId}
- "List all logs?" -> GET /logs
- "Get log details?" -> GET /logs/{logId}
- "List all models?" -> GET /models
- "Create a model?" -> POST /models
- "Delete a model?" -> DELETE /models/{modelId}
- "Get model details?" -> GET /models/{modelId}
- "Partially update a model?" -> PATCH /models/{modelId}
- "List all dataBundles?" -> GET /models/{modelId}/dataBundles
- "Create a dataBundle?" -> POST /models/{modelId}/dataBundles
- "Delete a dataBundle?" -> DELETE /models/{modelId}/dataBundles/{dataBundleId}
- "Get dataBundle details?" -> GET /models/{modelId}/dataBundles/{dataBundleId}
- "Partially update a dataBundle?" -> PATCH /models/{modelId}/dataBundles/{dataBundleId}
- "List all trainings?" -> GET /models/{modelId}/trainings
- "Create a training?" -> POST /models/{modelId}/trainings
- "Get training details?" -> GET /models/{modelId}/trainings/{trainingId}
- "Partially update a training?" -> PATCH /models/{modelId}/trainings/{trainingId}
- "List all organizations?" -> GET /organizations
- "Create a organization?" -> POST /organizations
- "Get organization details?" -> GET /organizations/{organizationId}
- "Partially update a organization?" -> PATCH /organizations/{organizationId}
- "List all paymentMethods?" -> GET /paymentMethods
- "Create a paymentMethod?" -> POST /paymentMethods
- "Delete a paymentMethod?" -> DELETE /paymentMethods/{paymentMethodId}
- "Get paymentMethod details?" -> GET /paymentMethods/{paymentMethodId}
- "Partially update a paymentMethod?" -> PATCH /paymentMethods/{paymentMethodId}
- "List all plans?" -> GET /plans
- "Get plan details?" -> GET /plans/{planId}
- "List all predictions?" -> GET /predictions
- "Create a prediction?" -> POST /predictions
- "Get prediction details?" -> GET /predictions/{predictionId}
- "Get profile details?" -> GET /profiles/{profileId}
- "Partially update a profile?" -> PATCH /profiles/{profileId}
- "List all roles?" -> GET /roles
- "Get role details?" -> GET /roles/{roleId}
- "List all secrets?" -> GET /secrets
- "Create a secret?" -> POST /secrets
- "Delete a secret?" -> DELETE /secrets/{secretId}
- "Partially update a secret?" -> PATCH /secrets/{secretId}
- "List all transitions?" -> GET /transitions
- "Create a transition?" -> POST /transitions
- "Delete a transition?" -> DELETE /transitions/{transitionId}
- "Get transition details?" -> GET /transitions/{transitionId}
- "Partially update a transition?" -> PATCH /transitions/{transitionId}
- "List all executions?" -> GET /transitions/{transitionId}/executions
- "Create a execution?" -> POST /transitions/{transitionId}/executions
- "Get execution details?" -> GET /transitions/{transitionId}/executions/{executionId}
- "Partially update a execution?" -> PATCH /transitions/{transitionId}/executions/{executionId}
- "Create a heartbeat?" -> POST /transitions/{transitionId}/executions/{executionId}/heartbeats
- "List all users?" -> GET /users
- "Create a user?" -> POST /users
- "Delete a user?" -> DELETE /users/{userId}
- "Get user details?" -> GET /users/{userId}
- "Partially update a user?" -> PATCH /users/{userId}
- "List all workflows?" -> GET /workflows
- "Create a workflow?" -> POST /workflows
- "Delete a workflow?" -> DELETE /workflows/{workflowId}
- "Get workflow details?" -> GET /workflows/{workflowId}
- "Partially update a workflow?" -> PATCH /workflows/{workflowId}
- "List all executions?" -> GET /workflows/{workflowId}/executions
- "Create a execution?" -> POST /workflows/{workflowId}/executions
- "Delete a execution?" -> DELETE /workflows/{workflowId}/executions/{executionId}
- "Get execution details?" -> GET /workflows/{workflowId}/executions/{executionId}
- "Partially update a execution?" -> PATCH /workflows/{workflowId}/executions/{executionId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
