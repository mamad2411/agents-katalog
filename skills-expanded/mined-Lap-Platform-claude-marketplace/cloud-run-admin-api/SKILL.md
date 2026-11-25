---
name: cloud-run-admin-api
description: "Cloud Run Admin API skill. Use when working with Cloud Run Admin for {name}, {name}:run, {name}:wait. Covers 16 endpoints."
version: 1.0.0
generator: lapsh
---

# Cloud Run Admin API
API version: v2

## Auth
OAuth2 | OAuth2

## Base URL
https://run.googleapis.com/

## Setup
1. Configure auth: OAuth2 | OAuth2
2. GET /v2/{name}/operations -- verify access
3. POST /v2/{name}:run -- create first resource

## Endpoints

16 endpoints across 7 groups. See references/api-spec.lap for full details.

### {name}
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /v2/{name} | Deletes a Revision. |
| GET | /v2/{name} | Gets information about a Revision. |
| PATCH | /v2/{name} | Updates a Service. |
| GET | /v2/{name}/operations | Lists operations that match the specified filter in the request. If the server doesn't support this method, it returns `UNIMPLEMENTED`. |

### {name}:run
| Method | Path | Description |
|--------|------|-------------|
| POST | /v2/{name}:run | Triggers creation of a new Execution of this Job. |

### {name}:wait
| Method | Path | Description |
|--------|------|-------------|
| POST | /v2/{name}:wait | Waits until the specified long-running operation is done or reaches at most a specified timeout, returning the latest state. If the operation is already done, the latest state is immediately returned. If the timeout specified is greater than the default HTTP/RPC timeout, the HTTP/RPC timeout is used. If the server does not support this method, it returns `google.rpc.Code.UNIMPLEMENTED`. Note that this method is on a best-effort basis. It may return the latest state before the specified timeout (including immediately), meaning even an immediate response is no guarantee that the operation is done. |

### {parent}
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/{parent}/executions | Lists Executions from a Job. |
| GET | /v2/{parent}/jobs | Lists Jobs. |
| POST | /v2/{parent}/jobs | Creates a Job. |
| GET | /v2/{parent}/revisions | Lists Revisions from a given Service, or from a given location. |
| GET | /v2/{parent}/services | Lists Services. |
| POST | /v2/{parent}/services | Creates a new Service in a given project and location. |
| GET | /v2/{parent}/tasks | Lists Tasks from an Execution of a Job. |

### {resource}:getIamPolicy
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/{resource}:getIamPolicy | Gets the IAM Access Control policy currently in effect for the given Cloud Run Service. This result does not include any inherited policies. |

### {resource}:setIamPolicy
| Method | Path | Description |
|--------|------|-------------|
| POST | /v2/{resource}:setIamPolicy | Sets the IAM Access control policy for the specified Service. Overwrites any existing policy. |

### {resource}:testIamPermissions
| Method | Path | Description |
|--------|------|-------------|
| POST | /v2/{resource}:testIamPermissions | Returns permissions that a caller has on the specified Project. There are no permissions required for making this API call. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all operations?" -> GET /v2/{name}/operations
- "List all executions?" -> GET /v2/{parent}/executions
- "List all jobs?" -> GET /v2/{parent}/jobs
- "Create a job?" -> POST /v2/{parent}/jobs
- "List all revisions?" -> GET /v2/{parent}/revisions
- "List all services?" -> GET /v2/{parent}/services
- "Create a service?" -> POST /v2/{parent}/services
- "List all tasks?" -> GET /v2/{parent}/tasks
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
