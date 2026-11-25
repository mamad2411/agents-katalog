---
name: circleci-rest-api
description: "CircleCI REST API skill. Use when working with CircleCI REST for me, projects, project. Covers 22 endpoints."
version: 1.0.0
generator: lapsh
---

# CircleCI REST API
API version: v1

## Auth
ApiKey circle-token in query

## Base URL
https://circleci.com/api/v1

## Setup
1. Set your API key in the appropriate header
2. GET /me -- verify access
3. POST /project/{username}/{project} -- create first project

## Endpoints

22 endpoints across 5 groups. See references/api-spec.lap for full details.

### me
| Method | Path | Description |
|--------|------|-------------|
| GET | /me | Provides information about the signed in user. |

### projects
| Method | Path | Description |
|--------|------|-------------|
| GET | /projects | List of all the projects you're following on CircleCI, with build information organized by branch. |

### project
| Method | Path | Description |
|--------|------|-------------|
| GET | /project/{username}/{project} | Build summary for each of the last 30 builds for a single git repo. |
| POST | /project/{username}/{project} | Triggers a new build, returns a summary of the build. |
| GET | /project/{username}/{project}/{build_num} | Full details for a single build. The response includes all of the fields from the build summary. |
| GET | /project/{username}/{project}/{build_num}/artifacts | List the artifacts produced by a given build. |
| POST | /project/{username}/{project}/{build_num}/retry | Retries the build, returns a summary of the new build. |
| POST | /project/{username}/{project}/{build_num}/cancel | Cancels the build, returns a summary of the build. |
| GET | /project/{username}/{project}/{build_num}/tests | Provides test metadata for a build |
| POST | /project/{username}/{project}/tree/{branch} | Triggers a new build, returns a summary of the build. |
| POST | /project/{username}/{project}/ssh-key | Create an ssh key used to access external systems that require SSH key-based authentication |
| GET | /project/{username}/{project}/checkout-key | Lists checkout keys. |
| POST | /project/{username}/{project}/checkout-key | Creates a new checkout key. |
| GET | /project/{username}/{project}/checkout-key/{fingerprint} | Get a checkout key. |
| DELETE | /project/{username}/{project}/checkout-key/{fingerprint} | Delete a checkout key. |
| DELETE | /project/{username}/{project}/build-cache | Clears the cache for a project. |
| GET | /project/{username}/{project}/envvar | Lists the environment variables for :project |
| POST | /project/{username}/{project}/envvar | Creates a new environment variable |
| GET | /project/{username}/{project}/envvar/{name} | Gets the hidden value of environment variable :name |
| DELETE | /project/{username}/{project}/envvar/{name} | Deletes the environment variable named ':name' |

### recent-builds
| Method | Path | Description |
|--------|------|-------------|
| GET | /recent-builds | Build summary for each of the last 30 recent builds, ordered by build_num. |

### user
| Method | Path | Description |
|--------|------|-------------|
| POST | /user/heroku-key | Adds your Heroku API key to CircleCI, takes apikey as form param name. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all me?" -> GET /me
- "List all projects?" -> GET /projects
- "Get project details?" -> GET /project/{username}/{project}
- "List all recent-builds?" -> GET /recent-builds
- "Get project details?" -> GET /project/{username}/{project}/{build_num}
- "List all artifacts?" -> GET /project/{username}/{project}/{build_num}/artifacts
- "Create a retry?" -> POST /project/{username}/{project}/{build_num}/retry
- "Create a cancel?" -> POST /project/{username}/{project}/{build_num}/cancel
- "List all tests?" -> GET /project/{username}/{project}/{build_num}/tests
- "Create a ssh-key?" -> POST /project/{username}/{project}/ssh-key
- "List all checkout-key?" -> GET /project/{username}/{project}/checkout-key
- "Create a checkout-key?" -> POST /project/{username}/{project}/checkout-key
- "Get checkout-key details?" -> GET /project/{username}/{project}/checkout-key/{fingerprint}
- "Delete a checkout-key?" -> DELETE /project/{username}/{project}/checkout-key/{fingerprint}
- "List all envvar?" -> GET /project/{username}/{project}/envvar
- "Create a envvar?" -> POST /project/{username}/{project}/envvar
- "Get envvar details?" -> GET /project/{username}/{project}/envvar/{name}
- "Delete a envvar?" -> DELETE /project/{username}/{project}/envvar/{name}
- "Create a heroku-key?" -> POST /user/heroku-key
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
