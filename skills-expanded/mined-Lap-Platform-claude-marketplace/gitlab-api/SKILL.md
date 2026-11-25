---
name: gitlab-api
description: "GitLab API skill. Use when working with GitLab for groups, projects, admin. Covers 73 endpoints."
version: 1.0.0
generator: lapsh
---

# GitLab API
API version: v4

## Auth
ApiKey Private-Token in header

## Base URL
https://www.gitlab.com/api/v4

## Setup
1. Set your API key in the appropriate header
2. GET /admin/batched_background_migrations -- verify access
3. POST /groups/{id}/badges -- create first badges

## Endpoints

73 endpoints across 10 groups. See references/api-spec.lap for full details.

### groups
| Method | Path | Description |
|--------|------|-------------|
| GET | /groups/{id}/badges/{badge_id} | Gets a badge of a group. |
| PUT | /groups/{id}/badges/{badge_id} | Updates a badge of a group. |
| DELETE | /groups/{id}/badges/{badge_id} | Removes a badge from the group. |
| GET | /groups/{id}/badges | Gets a list of group badges viewable by the authenticated user. |
| POST | /groups/{id}/badges | Adds a badge to a group. |
| GET | /groups/{id}/badges/render | Preview a badge from a group. |
| DELETE | /groups/{id}/access_requests/{user_id} | Denies an access request for the given user. |
| PUT | /groups/{id}/access_requests/{user_id}/approve | Approves an access request for the given user. |
| GET | /groups/{id}/access_requests | Gets a list of access requests for a group. |
| POST | /groups/{id}/access_requests | Requests access for the authenticated user to a group. |

### projects
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /projects/{id}/repository/merged_branches | Delete all merged branches |
| GET | /projects/{id}/repository/branches/{branch} | Get a single repository branch |
| DELETE | /projects/{id}/repository/branches/{branch} | Delete a branch |
| HEAD | /projects/{id}/repository/branches/{branch} | Check if a branch exists |
| GET | /projects/{id}/repository/branches | Get a project repository branches |
| POST | /projects/{id}/repository/branches | Create branch |
| PUT | /projects/{id}/repository/branches/{branch}/unprotect | Unprotect a single branch |
| PUT | /projects/{id}/repository/branches/{branch}/protect | Protect a single branch |
| GET | /projects/{id}/badges/{badge_id} | Gets a badge of a project. |
| PUT | /projects/{id}/badges/{badge_id} | Updates a badge of a project. |
| DELETE | /projects/{id}/badges/{badge_id} | Removes a badge from the project. |
| GET | /projects/{id}/badges | Gets a list of project badges viewable by the authenticated user. |
| POST | /projects/{id}/badges | Adds a badge to a project. |
| GET | /projects/{id}/badges/render | Preview a badge from a project. |
| DELETE | /projects/{id}/access_requests/{user_id} | Denies an access request for the given user. |
| PUT | /projects/{id}/access_requests/{user_id}/approve | Approves an access request for the given user. |
| GET | /projects/{id}/access_requests | Gets a list of access requests for a project. |
| POST | /projects/{id}/access_requests | Requests access for the authenticated user to a project. |
| PUT | /projects/{id}/alert_management_alerts/{alert_iid}/metric_images/{metric_image_id} | Update a metric image for an alert |
| DELETE | /projects/{id}/alert_management_alerts/{alert_iid}/metric_images/{metric_image_id} | Remove a metric image for an alert |
| GET | /projects/{id}/alert_management_alerts/{alert_iid}/metric_images | Metric Images for alert |
| POST | /projects/{id}/alert_management_alerts/{alert_iid}/metric_images | Upload a metric image for an alert |
| POST | /projects/{id}/alert_management_alerts/{alert_iid}/metric_images/authorize | Workhorse authorize metric image file upload |
| GET | /projects/{id}/jobs | List jobs for a project |
| GET | /projects/{id}/jobs/{job_id} | Get a single job by ID |
| POST | /projects/{id}/jobs/{job_id}/play | Run a manual job |

### admin
| Method | Path | Description |
|--------|------|-------------|
| GET | /admin/batched_background_migrations/{id} | Retrieve a batched background migration |
| GET | /admin/batched_background_migrations | Get the list of batched background migrations |
| PUT | /admin/batched_background_migrations/{id}/resume | Resume a batched background migration |
| PUT | /admin/batched_background_migrations/{id}/pause | Pause a batched background migration |
| GET | /admin/ci/variables/{key} | Get the details of a specific instance-level variable |
| PUT | /admin/ci/variables/{key} | Update an instance-level variable |
| DELETE | /admin/ci/variables/{key} | Delete an existing instance-level variable |
| GET | /admin/ci/variables | List all instance-level variables |
| POST | /admin/ci/variables | Create a new instance-level variable |
| GET | /admin/databases/{database_name}/dictionary/tables/{table_name} | Retrieve dictionary details |
| GET | /admin/clusters/{cluster_id} | Get a single instance cluster |
| PUT | /admin/clusters/{cluster_id} | Edit instance cluster |
| DELETE | /admin/clusters/{cluster_id} | Delete instance cluster |
| POST | /admin/clusters/add | Add existing instance cluster |
| GET | /admin/clusters | List instance clusters |
| POST | /admin/migrations/{timestamp}/mark | Mark the migration as successfully executed |

### applications
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /applications/{id} | Delete an application |
| GET | /applications | Get applications |
| POST | /applications | Create a new application |

### avatar
| Method | Path | Description |
|--------|------|-------------|
| GET | /avatar | Return avatar url for a user |

### broadcast_messages
| Method | Path | Description |
|--------|------|-------------|
| GET | /broadcast_messages/{id} | Get a specific broadcast message |
| PUT | /broadcast_messages/{id} | Update a broadcast message |
| DELETE | /broadcast_messages/{id} | Delete a broadcast message |
| GET | /broadcast_messages | Get all broadcast messages |
| POST | /broadcast_messages | Create a broadcast message |

### bulk_imports
| Method | Path | Description |
|--------|------|-------------|
| GET | /bulk_imports/{import_id}/entities/{entity_id} | Get GitLab Migration entity details |
| GET | /bulk_imports/{import_id}/entities | List GitLab Migration entities |
| GET | /bulk_imports/{import_id} | Get GitLab Migration details |
| GET | /bulk_imports/entities | List all GitLab Migrations' entities |
| GET | /bulk_imports | List all GitLab Migrations |
| POST | /bulk_imports | Start a new GitLab Migration |

### application
| Method | Path | Description |
|--------|------|-------------|
| GET | /application/appearance | Get the current appearance |
| PUT | /application/appearance | Modify appearance |
| GET | /application/plan_limits | Get current plan limits |
| PUT | /application/plan_limits | Change plan limits |

### metadata
| Method | Path | Description |
|--------|------|-------------|
| GET | /metadata | Retrieve metadata information for this GitLab instance |

### version
| Method | Path | Description |
|--------|------|-------------|
| GET | /version | Retrieves version information for the GitLab instance |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get badge details?" -> GET /groups/{id}/badges/{badge_id}
- "Update a badge?" -> PUT /groups/{id}/badges/{badge_id}
- "Delete a badge?" -> DELETE /groups/{id}/badges/{badge_id}
- "List all badges?" -> GET /groups/{id}/badges
- "Create a badge?" -> POST /groups/{id}/badges
- "List all render?" -> GET /groups/{id}/badges/render
- "Delete a access_request?" -> DELETE /groups/{id}/access_requests/{user_id}
- "List all access_requests?" -> GET /groups/{id}/access_requests
- "Create a access_request?" -> POST /groups/{id}/access_requests
- "Get branche details?" -> GET /projects/{id}/repository/branches/{branch}
- "Delete a branche?" -> DELETE /projects/{id}/repository/branches/{branch}
- "Search branches?" -> GET /projects/{id}/repository/branches
- "Create a branche?" -> POST /projects/{id}/repository/branches
- "Get badge details?" -> GET /projects/{id}/badges/{badge_id}
- "Update a badge?" -> PUT /projects/{id}/badges/{badge_id}
- "Delete a badge?" -> DELETE /projects/{id}/badges/{badge_id}
- "List all badges?" -> GET /projects/{id}/badges
- "Create a badge?" -> POST /projects/{id}/badges
- "List all render?" -> GET /projects/{id}/badges/render
- "Delete a access_request?" -> DELETE /projects/{id}/access_requests/{user_id}
- "List all access_requests?" -> GET /projects/{id}/access_requests
- "Create a access_request?" -> POST /projects/{id}/access_requests
- "Update a metric_image?" -> PUT /projects/{id}/alert_management_alerts/{alert_iid}/metric_images/{metric_image_id}
- "Delete a metric_image?" -> DELETE /projects/{id}/alert_management_alerts/{alert_iid}/metric_images/{metric_image_id}
- "List all metric_images?" -> GET /projects/{id}/alert_management_alerts/{alert_iid}/metric_images
- "Create a metric_image?" -> POST /projects/{id}/alert_management_alerts/{alert_iid}/metric_images
- "Create a authorize?" -> POST /projects/{id}/alert_management_alerts/{alert_iid}/metric_images/authorize
- "Get batched_background_migration details?" -> GET /admin/batched_background_migrations/{id}
- "List all batched_background_migrations?" -> GET /admin/batched_background_migrations
- "Get variable details?" -> GET /admin/ci/variables/{key}
- "Update a variable?" -> PUT /admin/ci/variables/{key}
- "Delete a variable?" -> DELETE /admin/ci/variables/{key}
- "List all variables?" -> GET /admin/ci/variables
- "Create a variable?" -> POST /admin/ci/variables
- "Get table details?" -> GET /admin/databases/{database_name}/dictionary/tables/{table_name}
- "Get cluster details?" -> GET /admin/clusters/{cluster_id}
- "Update a cluster?" -> PUT /admin/clusters/{cluster_id}
- "Delete a cluster?" -> DELETE /admin/clusters/{cluster_id}
- "Create a add?" -> POST /admin/clusters/add
- "List all clusters?" -> GET /admin/clusters
- "Create a mark?" -> POST /admin/migrations/{timestamp}/mark
- "Delete a application?" -> DELETE /applications/{id}
- "List all applications?" -> GET /applications
- "Create a application?" -> POST /applications
- "List all avatar?" -> GET /avatar
- "Get broadcast_message details?" -> GET /broadcast_messages/{id}
- "Update a broadcast_message?" -> PUT /broadcast_messages/{id}
- "Delete a broadcast_message?" -> DELETE /broadcast_messages/{id}
- "List all broadcast_messages?" -> GET /broadcast_messages
- "Create a broadcast_message?" -> POST /broadcast_messages
- "Get entity details?" -> GET /bulk_imports/{import_id}/entities/{entity_id}
- "List all entities?" -> GET /bulk_imports/{import_id}/entities
- "Get bulk_import details?" -> GET /bulk_imports/{import_id}
- "List all entities?" -> GET /bulk_imports/entities
- "List all bulk_imports?" -> GET /bulk_imports
- "Create a bulk_import?" -> POST /bulk_imports
- "List all appearance?" -> GET /application/appearance
- "List all plan_limits?" -> GET /application/plan_limits
- "List all metadata?" -> GET /metadata
- "List all version?" -> GET /version
- "List all jobs?" -> GET /projects/{id}/jobs
- "Get job details?" -> GET /projects/{id}/jobs/{job_id}
- "Create a play?" -> POST /projects/{id}/jobs/{job_id}/play
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
