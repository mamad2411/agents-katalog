---
name: val-town-api
description: "Val Town API skill. Use when working with Val Town for alias, me, blob. Covers 36 endpoints."
version: 1.0.0
generator: lapsh
---

# Val Town API
API version: 1

## Auth
Bearer bearer

## Base URL
https://api.val.town

## Setup
1. Set Authorization header with your Bearer token
2. GET /v1/me -- verify access
3. POST /v1/blob/{key} -- create first blob

## Endpoints

36 endpoints across 11 groups. See references/api-spec.lap for full details.

### alias
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/alias/{username} | Get basic details about a user, given their username |
| GET | /v2/alias/vals/{username}/{val_name} | Get a val |

### me
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/me | Get profile information for the current user |
| GET | /v2/me/vals | [BETA] List all of a user's vals for authenticated users |

### blob
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/blob | List blobs in your account |
| GET | /v1/blob/{key} | Get a blob’s contents. |
| POST | /v1/blob/{key} | Store data in blob storage |
| DELETE | /v1/blob/{key} | Delete a blob |

### users
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/users/{user_id} | Get basic information about a user |

### sqlite
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/sqlite/execute | Execute a single SQLite statement and return results |
| POST | /v1/sqlite/batch | Execute a batch of SQLite statements and return results for all of them |

### email
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/email | Send emails |

### telemetry
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/telemetry/traces | Get OpenTelemetry traces within a specified time window with flexible pagination options: Pass in only the end time to paginate backwards from there. Pass in a start time to paginate backwards from now until the start time. Pass in both to get resources within the time window. Choose to return in end_time order instead to view traces that completed in a window or since a time. Filter additionally by branch_ids or file_id. |
| GET | /v1/telemetry/logs | Get OpenTelemetry logs within a specified time window with flexible pagination options: Pass in only the end time to paginate backwards from there. Pass in a start time to paginate backwards from now until the start time. Pass in both to get resources within the time window. Filter additionally by branch_ids or file_id. |

### vals
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/vals/{val_id} | Get a val by id |
| DELETE | /v2/vals/{val_id} | Delete a project |
| GET | /v2/vals | Lists all vals including all public vals and your unlisted and private vals |
| POST | /v2/vals | Create a new val |
| GET | /v2/vals/{val_id}/branches/{branch_id} | Get a branch by id |
| DELETE | /v2/vals/{val_id}/branches/{branch_id} | Delete a branch |
| GET | /v2/vals/{val_id}/branches | List all branches for a val |
| POST | /v2/vals/{val_id}/branches | Create a new branch |
| GET | /v2/vals/{val_id}/files | Get metadata for files and directories in a val. If path is an empty string, returns files at the root directory. |
| POST | /v2/vals/{val_id}/files | Create a new file, project val or directory |
| DELETE | /v2/vals/{val_id}/files | Deletes a file or a directory. To delete a directory and all of its children, use the recursive flag. To delete all files, pass in an empty path and the recursive flag. |
| PUT | /v2/vals/{val_id}/files | Update a file's content |
| GET | /v2/vals/{val_id}/environment_variables | List environment variables defined in this project. This only includes names, not values. |
| POST | /v2/vals/{val_id}/environment_variables | Create a new environment variable scoped to this project. |
| PUT | /v2/vals/{val_id}/environment_variables/{key} | Update a environment variable scoped to this project. |
| DELETE | /v2/vals/{val_id}/environment_variables/{key} | Delete a environment variable scoped to this project. |
| GET | /v2/vals/{val_id}/files/content | Download file content |

### files
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/files/{file_id} | Get file metadata by file ID |

### orgs
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/orgs | Get all orgs you are a member of |
| GET | /v2/orgs/{org_id}/memberships | List all memberships of an org |

### connections
| Method | Path | Description |
|--------|------|-------------|
| POST | /v3/connections/slack/token | Get a valid Slack access token for a connected workspace. Automatically refreshes the token if expired. |
| POST | /v3/connections/google-docs/token | Get a valid Google access token for a connected Google account. Automatically refreshes the token if expired. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get alia details?" -> GET /v1/alias/{username}
- "List all me?" -> GET /v1/me
- "List all blob?" -> GET /v1/blob
- "Get blob details?" -> GET /v1/blob/{key}
- "Delete a blob?" -> DELETE /v1/blob/{key}
- "Get user details?" -> GET /v1/users/{user_id}
- "Create a execute?" -> POST /v1/sqlite/execute
- "Create a batch?" -> POST /v1/sqlite/batch
- "Create a email?" -> POST /v1/email
- "List all traces?" -> GET /v1/telemetry/traces
- "List all logs?" -> GET /v1/telemetry/logs
- "Get val details?" -> GET /v2/vals/{val_id}
- "Delete a val?" -> DELETE /v2/vals/{val_id}
- "List all vals?" -> GET /v2/vals
- "Create a val?" -> POST /v2/vals
- "Get branche details?" -> GET /v2/vals/{val_id}/branches/{branch_id}
- "Delete a branche?" -> DELETE /v2/vals/{val_id}/branches/{branch_id}
- "List all branches?" -> GET /v2/vals/{val_id}/branches
- "Create a branche?" -> POST /v2/vals/{val_id}/branches
- "List all files?" -> GET /v2/vals/{val_id}/files
- "Create a file?" -> POST /v2/vals/{val_id}/files
- "List all environment_variables?" -> GET /v2/vals/{val_id}/environment_variables
- "Create a environment_variable?" -> POST /v2/vals/{val_id}/environment_variables
- "Update a environment_variable?" -> PUT /v2/vals/{val_id}/environment_variables/{key}
- "Delete a environment_variable?" -> DELETE /v2/vals/{val_id}/environment_variables/{key}
- "List all content?" -> GET /v2/vals/{val_id}/files/content
- "Get file details?" -> GET /v2/files/{file_id}
- "Get val details?" -> GET /v2/alias/vals/{username}/{val_name}
- "List all vals?" -> GET /v2/me/vals
- "List all orgs?" -> GET /v2/orgs
- "List all memberships?" -> GET /v2/orgs/{org_id}/memberships
- "Create a token?" -> POST /v3/connections/slack/token
- "Create a token?" -> POST /v3/connections/google-docs/token
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object
- Error responses use types: Conflict

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
