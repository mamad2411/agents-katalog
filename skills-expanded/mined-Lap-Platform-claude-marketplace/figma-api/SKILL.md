---
name: figma-api
description: "Figma API skill. Use when working with Figma for files, images, teams. Covers 46 endpoints."
version: 1.0.0
generator: lapsh
---

# Figma API
API version: 0.36.0

## Auth
ApiKey X-Figma-Token in header | OAuth2 | OAuth2

## Base URL
https://api.figma.com

## Setup
1. Set your API key in the appropriate header
2. GET /v1/me -- verify access
3. POST /v1/files/{file_key}/comments -- create first comments

## Endpoints

46 endpoints across 13 groups. See references/api-spec.lap for full details.

### files
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/files/{file_key} | Get file JSON |
| GET | /v1/files/{file_key}/nodes | Get file JSON for specific nodes |
| GET | /v1/files/{file_key}/images | Get image fills |
| GET | /v1/files/{file_key}/meta | Get file metadata |
| GET | /v1/files/{file_key}/versions | Get versions of a file |
| GET | /v1/files/{file_key}/comments | Get comments in a file |
| POST | /v1/files/{file_key}/comments | Add a comment to a file |
| DELETE | /v1/files/{file_key}/comments/{comment_id} | Delete a comment |
| GET | /v1/files/{file_key}/comments/{comment_id}/reactions | Get reactions for a comment |
| POST | /v1/files/{file_key}/comments/{comment_id}/reactions | Add a reaction to a comment |
| DELETE | /v1/files/{file_key}/comments/{comment_id}/reactions | Delete a reaction |
| GET | /v1/files/{file_key}/components | Get file components |
| GET | /v1/files/{file_key}/component_sets | Get file component sets |
| GET | /v1/files/{file_key}/styles | Get file styles |
| GET | /v1/files/{file_key}/variables/local | Get local variables |
| GET | /v1/files/{file_key}/variables/published | Get published variables |
| POST | /v1/files/{file_key}/variables | Create/modify/delete variables |
| GET | /v1/files/{file_key}/dev_resources | Get dev resources |
| DELETE | /v1/files/{file_key}/dev_resources/{dev_resource_id} | Delete dev resource |

### images
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/images/{file_key} | Render images of file nodes |

### teams
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/teams/{team_id}/projects | Get projects in a team |
| GET | /v1/teams/{team_id}/components | Get team components |
| GET | /v1/teams/{team_id}/component_sets | Get team component sets |
| GET | /v1/teams/{team_id}/styles | Get team styles |
| GET | /v2/teams/{team_id}/webhooks | [Deprecated] Get team webhooks |

### projects
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/projects/{project_id}/files | Get files in a project |

### me
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/me | Get current user |

### components
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/components/{key} | Get component |

### component_sets
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/component_sets/{key} | Get component set |

### styles
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/styles/{key} | Get style |

### webhooks
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/webhooks | Get webhooks by context or plan |
| POST | /v2/webhooks | Create a webhook |
| GET | /v2/webhooks/{webhook_id} | Get a webhook |
| PUT | /v2/webhooks/{webhook_id} | Update a webhook |
| DELETE | /v2/webhooks/{webhook_id} | Delete a webhook |
| GET | /v2/webhooks/{webhook_id}/requests | Get webhook requests |

### activity_logs
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/activity_logs | Get activity logs |

### payments
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/payments | Get payments |

### dev_resources
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/dev_resources | Create dev resources |
| PUT | /v1/dev_resources | Update dev resources |

### analytics
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/analytics/libraries/{file_key}/component/actions | Get library analytics component action data. |
| GET | /v1/analytics/libraries/{file_key}/component/usages | Get library analytics component usage data. |
| GET | /v1/analytics/libraries/{file_key}/style/actions | Get library analytics style action data. |
| GET | /v1/analytics/libraries/{file_key}/style/usages | Get library analytics style usage data. |
| GET | /v1/analytics/libraries/{file_key}/variable/actions | Get library analytics variable action data. |
| GET | /v1/analytics/libraries/{file_key}/variable/usages | Get library analytics variable usage data. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get file details?" -> GET /v1/files/{file_key}
- "List all nodes?" -> GET /v1/files/{file_key}/nodes
- "Get image details?" -> GET /v1/images/{file_key}
- "List all images?" -> GET /v1/files/{file_key}/images
- "List all meta?" -> GET /v1/files/{file_key}/meta
- "List all projects?" -> GET /v1/teams/{team_id}/projects
- "List all files?" -> GET /v1/projects/{project_id}/files
- "List all versions?" -> GET /v1/files/{file_key}/versions
- "List all comments?" -> GET /v1/files/{file_key}/comments
- "Create a comment?" -> POST /v1/files/{file_key}/comments
- "Delete a comment?" -> DELETE /v1/files/{file_key}/comments/{comment_id}
- "List all reactions?" -> GET /v1/files/{file_key}/comments/{comment_id}/reactions
- "Create a reaction?" -> POST /v1/files/{file_key}/comments/{comment_id}/reactions
- "List all me?" -> GET /v1/me
- "List all components?" -> GET /v1/teams/{team_id}/components
- "List all components?" -> GET /v1/files/{file_key}/components
- "Get component details?" -> GET /v1/components/{key}
- "List all component_sets?" -> GET /v1/teams/{team_id}/component_sets
- "List all component_sets?" -> GET /v1/files/{file_key}/component_sets
- "Get component_set details?" -> GET /v1/component_sets/{key}
- "List all styles?" -> GET /v1/teams/{team_id}/styles
- "List all styles?" -> GET /v1/files/{file_key}/styles
- "Get style details?" -> GET /v1/styles/{key}
- "List all webhooks?" -> GET /v2/webhooks
- "Create a webhook?" -> POST /v2/webhooks
- "Get webhook details?" -> GET /v2/webhooks/{webhook_id}
- "Update a webhook?" -> PUT /v2/webhooks/{webhook_id}
- "Delete a webhook?" -> DELETE /v2/webhooks/{webhook_id}
- "List all webhooks?" -> GET /v2/teams/{team_id}/webhooks
- "List all requests?" -> GET /v2/webhooks/{webhook_id}/requests
- "List all activity_logs?" -> GET /v1/activity_logs
- "List all payments?" -> GET /v1/payments
- "List all local?" -> GET /v1/files/{file_key}/variables/local
- "List all published?" -> GET /v1/files/{file_key}/variables/published
- "Create a variable?" -> POST /v1/files/{file_key}/variables
- "List all dev_resources?" -> GET /v1/files/{file_key}/dev_resources
- "Create a dev_resource?" -> POST /v1/dev_resources
- "Delete a dev_resource?" -> DELETE /v1/files/{file_key}/dev_resources/{dev_resource_id}
- "List all actions?" -> GET /v1/analytics/libraries/{file_key}/component/actions
- "List all usages?" -> GET /v1/analytics/libraries/{file_key}/component/usages
- "List all actions?" -> GET /v1/analytics/libraries/{file_key}/style/actions
- "List all usages?" -> GET /v1/analytics/libraries/{file_key}/style/usages
- "List all actions?" -> GET /v1/analytics/libraries/{file_key}/variable/actions
- "List all usages?" -> GET /v1/analytics/libraries/{file_key}/variable/usages
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
