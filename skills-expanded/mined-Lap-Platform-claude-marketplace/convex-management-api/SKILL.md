---
name: convex-management-api
description: "Convex Management API skill. Use when working with Convex Management for teams, projects, deployments. Covers 20 endpoints."
version: 1.0.0
generator: lapsh
---

# Convex Management API
API version: 1.0.0

## Auth
Bearer bearer | Bearer bearer | Bearer bearer

## Base URL
https://api.convex.dev/v1

## Setup
1. Set Authorization header with your Bearer token
2. GET /token_details -- verify access
3. POST /teams/{team_id}/create_project -- create first create_project

## Endpoints

20 endpoints across 4 groups. See references/api-spec.lap for full details.

### teams
| Method | Path | Description |
|--------|------|-------------|
| POST | /teams/{team_id}/create_project | Create project |
| GET | /teams/{team_id}/list_projects | List projects |
| GET | /teams/{team_id_or_slug}/projects/{project_slug} | Get project by slug |
| GET | /teams/{team_id}/list_deployment_classes | List deployment classes |
| GET | /teams/{team_id}/list_deployment_regions | List deployment regions |
| GET | /teams/{team_id}/list_members | List team members |

### projects
| Method | Path | Description |
|--------|------|-------------|
| GET | /projects/{project_id}/list_deployments | List deployments |
| POST | /projects/{project_id}/delete | Delete project |
| GET | /projects/{project_id} | Get project by ID |
| POST | /projects/{project_id}/create_deployment | Create deployment |

### deployments
| Method | Path | Description |
|--------|------|-------------|
| POST | /deployments/{deployment_name}/delete | Delete deployment |
| GET | /deployments/{deployment_name} | Get deployment |
| PATCH | /deployments/{deployment_name} | Update deployment |
| POST | /deployments/{deployment_name}/create_deploy_key | Create deploy key |
| GET | /deployments/{deployment_name}/list_deploy_keys | List deploy keys |
| POST | /deployments/{deployment_name}/delete_deploy_key | Delete deploy key |
| POST | /deployments/{deployment_name}/create_custom_domain | Create custom domain |
| POST | /deployments/{deployment_name}/delete_custom_domain | Delete custom domain |
| GET | /deployments/{deployment_name}/custom_domains | List custom domains |

### token_details
| Method | Path | Description |
|--------|------|-------------|
| GET | /token_details | Get token details |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a create_project?" -> POST /teams/{team_id}/create_project
- "List all list_projects?" -> GET /teams/{team_id}/list_projects
- "List all list_deployments?" -> GET /projects/{project_id}/list_deployments
- "Create a delete?" -> POST /projects/{project_id}/delete
- "Get project details?" -> GET /projects/{project_id}
- "Get project details?" -> GET /teams/{team_id_or_slug}/projects/{project_slug}
- "Create a create_deployment?" -> POST /projects/{project_id}/create_deployment
- "Create a delete?" -> POST /deployments/{deployment_name}/delete
- "Get deployment details?" -> GET /deployments/{deployment_name}
- "Partially update a deployment?" -> PATCH /deployments/{deployment_name}
- "List all list_deployment_classes?" -> GET /teams/{team_id}/list_deployment_classes
- "List all list_deployment_regions?" -> GET /teams/{team_id}/list_deployment_regions
- "Create a create_deploy_key?" -> POST /deployments/{deployment_name}/create_deploy_key
- "List all list_deploy_keys?" -> GET /deployments/{deployment_name}/list_deploy_keys
- "Create a delete_deploy_key?" -> POST /deployments/{deployment_name}/delete_deploy_key
- "List all token_details?" -> GET /token_details
- "Create a create_custom_domain?" -> POST /deployments/{deployment_name}/create_custom_domain
- "Create a delete_custom_domain?" -> POST /deployments/{deployment_name}/delete_custom_domain
- "List all custom_domains?" -> GET /deployments/{deployment_name}/custom_domains
- "List all list_members?" -> GET /teams/{team_id}/list_members
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
