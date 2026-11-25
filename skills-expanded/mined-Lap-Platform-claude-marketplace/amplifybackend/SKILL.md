---
name: amplifybackend
description: "AmplifyBackend API skill. Use when working with AmplifyBackend for backend, s3Buckets. Covers 31 endpoints."
version: 1.0.0
generator: lapsh
---

# AmplifyBackend
API version: 2020-08-11

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /backend/{appId}/job/{backendEnvironmentName}/{jobId} -- verify access
3. POST /backend/{appId}/environments/{backendEnvironmentName}/clone -- create first clone

## Endpoints

31 endpoints across 2 groups. See references/api-spec.lap for full details.

### backend
| Method | Path | Description |
|--------|------|-------------|
| POST | /backend/{appId}/environments/{backendEnvironmentName}/clone | This operation clones an existing backend. |
| POST | /backend | This operation creates a backend for an Amplify app. Backends are automatically created at the time of app creation. |
| POST | /backend/{appId}/api | Creates a new backend API resource. |
| POST | /backend/{appId}/auth | Creates a new backend authentication resource. |
| POST | /backend/{appId}/config | Creates a config object for a backend. |
| POST | /backend/{appId}/storage | Creates a backend storage resource. |
| POST | /backend/{appId}/challenge | Generates a one-time challenge code to authenticate a user into your Amplify Admin UI. |
| POST | /backend/{appId}/environments/{backendEnvironmentName}/remove | Removes an existing environment from your Amplify project. |
| POST | /backend/{appId}/api/{backendEnvironmentName}/remove | Deletes an existing backend API resource. |
| POST | /backend/{appId}/auth/{backendEnvironmentName}/remove | Deletes an existing backend authentication resource. |
| POST | /backend/{appId}/storage/{backendEnvironmentName}/remove | Removes the specified backend storage resource. |
| POST | /backend/{appId}/challenge/{sessionId}/remove | Deletes the challenge token based on the given appId and sessionId. |
| POST | /backend/{appId}/api/{backendEnvironmentName}/generateModels | Generates a model schema for an existing backend API resource. |
| POST | /backend/{appId}/details | Provides project-level details for your Amplify UI project. |
| POST | /backend/{appId}/api/{backendEnvironmentName}/details | Gets the details for a backend API. |
| POST | /backend/{appId}/api/{backendEnvironmentName}/getModels | Gets a model introspection schema for an existing backend API resource. |
| POST | /backend/{appId}/auth/{backendEnvironmentName}/details | Gets a backend auth details. |
| GET | /backend/{appId}/job/{backendEnvironmentName}/{jobId} | Returns information about a specific job. |
| POST | /backend/{appId}/storage/{backendEnvironmentName}/details | Gets details for a backend storage resource. |
| GET | /backend/{appId}/challenge/{sessionId} | Gets the challenge token based on the given appId and sessionId. |
| POST | /backend/{appId}/auth/{backendEnvironmentName}/import | Imports an existing backend authentication resource. |
| POST | /backend/{appId}/storage/{backendEnvironmentName}/import | Imports an existing backend storage resource. |
| POST | /backend/{appId}/job/{backendEnvironmentName} | Lists the jobs for the backend of an Amplify app. |
| POST | /backend/{appId}/remove | Removes all backend environments from your Amplify project. |
| POST | /backend/{appId}/config/remove | Removes the AWS resources required to access the Amplify Admin UI. |
| POST | /backend/{appId}/api/{backendEnvironmentName} | Updates an existing backend API resource. |
| POST | /backend/{appId}/auth/{backendEnvironmentName} | Updates an existing backend authentication resource. |
| POST | /backend/{appId}/config/update | Updates the AWS resources required to access the Amplify Admin UI. |
| POST | /backend/{appId}/job/{backendEnvironmentName}/{jobId} | Updates a specific job. |
| POST | /backend/{appId}/storage/{backendEnvironmentName} | Updates an existing backend storage resource. |

### s3Buckets
| Method | Path | Description |
|--------|------|-------------|
| POST | /s3Buckets | The list of S3 buckets in your account. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a clone?" -> POST /backend/{appId}/environments/{backendEnvironmentName}/clone
- "Create a backend?" -> POST /backend
- "Create a api?" -> POST /backend/{appId}/api
- "Create a auth?" -> POST /backend/{appId}/auth
- "Create a config?" -> POST /backend/{appId}/config
- "Create a storage?" -> POST /backend/{appId}/storage
- "Create a challenge?" -> POST /backend/{appId}/challenge
- "Create a remove?" -> POST /backend/{appId}/environments/{backendEnvironmentName}/remove
- "Create a remove?" -> POST /backend/{appId}/api/{backendEnvironmentName}/remove
- "Create a remove?" -> POST /backend/{appId}/auth/{backendEnvironmentName}/remove
- "Create a remove?" -> POST /backend/{appId}/storage/{backendEnvironmentName}/remove
- "Create a remove?" -> POST /backend/{appId}/challenge/{sessionId}/remove
- "Create a generateModel?" -> POST /backend/{appId}/api/{backendEnvironmentName}/generateModels
- "Create a detail?" -> POST /backend/{appId}/details
- "Create a detail?" -> POST /backend/{appId}/api/{backendEnvironmentName}/details
- "Create a getModel?" -> POST /backend/{appId}/api/{backendEnvironmentName}/getModels
- "Create a detail?" -> POST /backend/{appId}/auth/{backendEnvironmentName}/details
- "Get job details?" -> GET /backend/{appId}/job/{backendEnvironmentName}/{jobId}
- "Create a detail?" -> POST /backend/{appId}/storage/{backendEnvironmentName}/details
- "Get challenge details?" -> GET /backend/{appId}/challenge/{sessionId}
- "Create a import?" -> POST /backend/{appId}/auth/{backendEnvironmentName}/import
- "Create a import?" -> POST /backend/{appId}/storage/{backendEnvironmentName}/import
- "Create a s3Bucket?" -> POST /s3Buckets
- "Create a remove?" -> POST /backend/{appId}/remove
- "Create a remove?" -> POST /backend/{appId}/config/remove
- "Create a update?" -> POST /backend/{appId}/config/update
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
