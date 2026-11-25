---
name: netlifys-api-documentation
description: "Netlify's API documentation API skill. Use when working with Netlify's API documentation for sites, accounts, api. Covers 165 endpoints."
version: 1.0.0
generator: lapsh
---

# Netlify's API documentation
API version: 2.50.0

## Auth
OAuth2

## Base URL
https://api.netlify.com/api/v1

## Setup
1. Configure auth: OAuth2
2. GET /sites -- verify access
3. POST /sites -- create first sites

## Endpoints

165 endpoints across 19 groups. See references/api-spec.lap for full details.

### sites
| Method | Path | Description |
|--------|------|-------------|
| GET | /sites | **Note:** Environment variable keys and values have moved from `build_settings.env` and `repo.env` to a new endpoint. Please use [getEnvVars](#tag/environmentVariables/operation/getEnvVars) to retrieve site environment variables. |
| POST | /sites | **Note:** Environment variable keys and values have moved from `build_settings.env` and `repo.env` to a new endpoint. Please use [createEnvVars](#tag/environmentVariables/operation/createEnvVars) to create environment variables for a site. |
| GET | /sites/{site_id} | **Note:** Environment variable keys and values have moved from `build_settings.env` and `repo.env` to a new endpoint. Please use [getEnvVars](#tag/environmentVariables/operation/getEnvVars) to retrieve site environment variables. |
| PATCH | /sites/{site_id} | **Note:** Environment variable keys and values have moved from `build_settings.env` and `repo.env` to a new endpoint. Please use [updateEnvVar](#tag/environmentVariables/operation/updateEnvVar) to update a site's environment variables. |
| DELETE | /sites/{site_id} |  |
| POST | /sites/{site_id}/ssl | Provisions or updates a TLS certificate for the site. |
| GET | /sites/{site_id}/ssl |  |
| GET | /sites/{site_id}/ssl/certificates |  |
| GET | /sites/{site_id}/functions |  |
| GET | /sites/{site_id}/forms |  |
| DELETE | /sites/{site_id}/forms/{form_id} |  |
| GET | /sites/{site_id}/submissions |  |
| GET | /sites/{site_id}/files |  |
| GET | /sites/{site_id}/assets |  |
| POST | /sites/{site_id}/assets |  |
| GET | /sites/{site_id}/assets/{asset_id} |  |
| PUT | /sites/{site_id}/assets/{asset_id} |  |
| DELETE | /sites/{site_id}/assets/{asset_id} |  |
| GET | /sites/{site_id}/assets/{asset_id}/public_signature |  |
| GET | /sites/{site_id}/files/{file_path} |  |
| GET | /sites/{site_id}/snippets |  |
| POST | /sites/{site_id}/snippets |  |
| GET | /sites/{site_id}/snippets/{snippet_id} |  |
| PUT | /sites/{site_id}/snippets/{snippet_id} |  |
| DELETE | /sites/{site_id}/snippets/{snippet_id} |  |
| GET | /sites/{site_id}/metadata |  |
| PUT | /sites/{site_id}/metadata |  |
| GET | /sites/{site_id}/build_hooks |  |
| POST | /sites/{site_id}/build_hooks |  |
| GET | /sites/{site_id}/build_hooks/{id} |  |
| PUT | /sites/{site_id}/build_hooks/{id} |  |
| DELETE | /sites/{site_id}/build_hooks/{id} |  |
| GET | /sites/{site_id}/deploys |  |
| POST | /sites/{site_id}/deploys |  |
| GET | /sites/{site_id}/deploys/{deploy_id} |  |
| PUT | /sites/{site_id}/deploys/{deploy_id} |  |
| DELETE | /sites/{site_id}/deploys/{deploy_id} |  |
| POST | /sites/{site_id}/deploys/{deploy_id}/restore |  |
| GET | /sites/{site_id}/builds |  |
| POST | /sites/{site_id}/builds | Runs a build for a site. The build will be scheduled to run at the first opportunity, but it might not start immediately if insufficient account build capacity is available. |
| GET | /sites/{site_id}/deployed-branches |  |
| PUT | /sites/{site_id}/unlink_repo | [Beta] Unlinks the repo from the site. |
| PUT | /sites/{site_id}/enable | Re-enables a site that was previously disabled by the user. Sites that were disabled for usage exceeded or marked as spam cannot be re-enabled via this endpoint. |
| PUT | /sites/{site_id}/disable | Disables a site, preventing it from serving content. The site can be re-enabled later using the enable endpoint. |
| GET | /sites/{site_id}/dns |  |
| PUT | /sites/{site_id}/dns |  |
| PUT | /sites/{site_id}/rollback |  |
| PUT | /sites/{site_id}/plugins/{package} | This is an internal-only endpoint. |
| GET | /sites/{site_id}/plugin_runs/latest | This is an internal-only endpoint. |
| GET | /sites/{site_id}/service-instances |  |
| POST | /sites/{site_id}/services/{addon}/instances |  |
| GET | /sites/{site_id}/services/{addon}/instances/{instance_id} |  |
| PUT | /sites/{site_id}/services/{addon}/instances/{instance_id} |  |
| DELETE | /sites/{site_id}/services/{addon}/instances/{instance_id} |  |
| POST | /sites/{site_id}/traffic_splits |  |
| GET | /sites/{site_id}/traffic_splits |  |
| PUT | /sites/{site_id}/traffic_splits/{split_test_id} |  |
| GET | /sites/{site_id}/traffic_splits/{split_test_id} |  |
| POST | /sites/{site_id}/traffic_splits/{split_test_id}/publish |  |
| POST | /sites/{site_id}/traffic_splits/{split_test_id}/unpublish |  |
| GET | /sites/{site_id}/dev_servers |  |
| POST | /sites/{site_id}/dev_servers |  |
| DELETE | /sites/{site_id}/dev_servers |  |
| GET | /sites/{site_id}/dev_servers/{dev_server_id} |  |
| POST | /sites/{site_id}/dev_servers/{dev_server_id}/activity |  |
| POST | /sites/{site_id}/dev_servers/{dev_server_id}/state |  |
| GET | /sites/{site_id}/dev_server_hooks |  |
| POST | /sites/{site_id}/dev_server_hooks |  |
| GET | /sites/{site_id}/dev_server_hooks/{id} |  |
| PUT | /sites/{site_id}/dev_server_hooks/{id} |  |
| DELETE | /sites/{site_id}/dev_server_hooks/{id} |  |
| GET | /sites/{site_id}/ai-gateway/token | Returns an AI Gateway token for a specific site |
| POST | /sites/{site_id}/database | Creates a new database for the specified site. If a database already exists, returns the existing connection string. The database region defaults to the site's functions region if not specified. |
| GET | /sites/{site_id}/database | Returns the database connection string for the specified site. |
| DELETE | /sites/{site_id}/database | Deletes the database and all associated branches and snapshots for the specified site. |
| POST | /sites/{site_id}/database/branch | Creates a new database branch for a deploy. If a branch already exists for the specified deploy ID, returns the existing connection string. |
| GET | /sites/{site_id}/database/branch/{deploy_id} | Returns the database branch connection string for a specific deploy. |
| DELETE | /sites/{site_id}/database/branch/{deploy_id} | Deletes a database branch associated with a deploy. |
| POST | /sites/{site_id}/database/snapshot | Creates a point-in-time snapshot of a database branch. Defaults to the production branch if no branch name is specified. |
| GET | /sites/{site_id}/database/snapshots | Returns all snapshots for the site's database. |
| DELETE | /sites/{site_id}/database/snapshot/{snapshot_id} | Deletes a database snapshot. |
| POST | /sites/{site_id}/database/snapshot/{snapshot_id}/restore | Restores a snapshot to a database branch. Defaults to the production branch if no branch_name is specified. |

### accounts
| Method | Path | Description |
|--------|------|-------------|
| GET | /accounts/{account_id}/env | Returns all environment variables for an account or site. An account corresponds to a team in the Netlify UI. |
| POST | /accounts/{account_id}/env | Creates new environment variables. Granular scopes are available on Pro plans and above. |
| GET | /accounts/{account_id}/env/{key} | Returns an individual environment variable. |
| PUT | /accounts/{account_id}/env/{key} | Updates an existing environment variable and all of its values. Existing values will be replaced by values provided. |
| PATCH | /accounts/{account_id}/env/{key} | Updates or creates a new value for an existing environment variable. |
| DELETE | /accounts/{account_id}/env/{key} | Deletes an environment variable |
| DELETE | /accounts/{account_id}/env/{key}/value/{id} | Deletes a specific environment variable value. |
| GET | /accounts/types |  |
| GET | /accounts |  |
| POST | /accounts |  |
| GET | /accounts/{account_id} |  |
| PUT | /accounts/{account_id} |  |
| DELETE | /accounts/{account_id} |  |
| GET | /accounts/{account_id}/audit |  |
| GET | /accounts/{account_id}/ai-gateway/token | Returns an AI Gateway token scoped to an account |

### api
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/v1/sites/{site_id}/env | Returns all environment variables for a site. This convenience method behaves the same as `getEnvVars` but doesn't require an `account_id` as input. |

### purge
| Method | Path | Description |
|--------|------|-------------|
| POST | /purge | Purges cached content from Netlify's CDN. Supports purging by Cache-Tag. |

### deploys
| Method | Path | Description |
|--------|------|-------------|
| POST | /deploys/{deploy_id}/cancel |  |
| GET | /deploys/{deploy_id} |  |
| DELETE | /deploys/{deploy_id} |  |
| PATCH | /deploys/{deploy_id}/validations_report | Updates the deploy validations report for a deploy. |
| POST | /deploys/{deploy_id}/lock |  |
| POST | /deploys/{deploy_id}/unlock |  |
| PUT | /deploys/{deploy_id}/files/{path} |  |
| PUT | /deploys/{deploy_id}/functions/{name} |  |
| POST | /deploys/{deploy_id}/plugin_runs | This is an internal-only endpoint. |

### builds
| Method | Path | Description |
|--------|------|-------------|
| GET | /builds/{build_id} |  |
| POST | /builds/{build_id}/log |  |
| POST | /builds/{build_id}/start |  |

### {account_id}
| Method | Path | Description |
|--------|------|-------------|
| GET | /{account_id}/builds/status |  |

### forms
| Method | Path | Description |
|--------|------|-------------|
| GET | /forms/{form_id}/submissions |  |

### hooks
| Method | Path | Description |
|--------|------|-------------|
| GET | /hooks |  |
| POST | /hooks |  |
| GET | /hooks/{hook_id} |  |
| PUT | /hooks/{hook_id} |  |
| DELETE | /hooks/{hook_id} |  |
| POST | /hooks/{hook_id}/enable |  |
| GET | /hooks/types |  |

### oauth
| Method | Path | Description |
|--------|------|-------------|
| POST | /oauth/tickets |  |
| GET | /oauth/tickets/{ticket_id} |  |
| POST | /oauth/tickets/{ticket_id}/exchange |  |

### deploy_keys
| Method | Path | Description |
|--------|------|-------------|
| GET | /deploy_keys |  |
| POST | /deploy_keys |  |
| GET | /deploy_keys/{key_id} |  |
| DELETE | /deploy_keys/{key_id} |  |

### {account_slug}
| Method | Path | Description |
|--------|------|-------------|
| POST | /{account_slug}/sites | **Note:** Environment variable keys and values have moved from `build_settings.env` and `repo.env` to a new endpoint. Please use [createEnvVars](#tag/environmentVariables/operation/createEnvVars) to create environment variables for a site. |
| GET | /{account_slug}/sites | **Note:** Environment variable keys and values have moved from `build_settings.env` and `repo.env` to a new endpoint. Please use [getEnvVars](#tag/environmentVariables/operation/getEnvVars) to retrieve site environment variables. |
| GET | /{account_slug}/members |  |
| POST | /{account_slug}/members |  |
| GET | /{account_slug}/members/{member_id} |  |
| PUT | /{account_slug}/members/{member_id} |  |
| DELETE | /{account_slug}/members/{member_id} |  |

### billing
| Method | Path | Description |
|--------|------|-------------|
| GET | /billing/payment_methods |  |

### agent_runners
| Method | Path | Description |
|--------|------|-------------|
| GET | /agent_runners |  |
| POST | /agent_runners |  |
| POST | /agent_runners/upload_url |  |
| GET | /agent_runners/{agent_runner_id} |  |
| PATCH | /agent_runners/{agent_runner_id} |  |
| DELETE | /agent_runners/{agent_runner_id} |  |
| POST | /agent_runners/{agent_runner_id}/archive |  |
| POST | /agent_runners/{agent_runner_id}/pull_request |  |
| POST | /agent_runners/{agent_runner_id}/commit |  |
| GET | /agent_runners/{agent_runner_id}/sessions |  |
| POST | /agent_runners/{agent_runner_id}/sessions |  |
| GET | /agent_runners/{agent_runner_id}/sessions/{agent_runner_session_id} |  |
| PATCH | /agent_runners/{agent_runner_id}/sessions/{agent_runner_session_id} |  |
| DELETE | /agent_runners/{agent_runner_id}/sessions/{agent_runner_session_id} |  |

### submissions
| Method | Path | Description |
|--------|------|-------------|
| GET | /submissions/{submission_id} |  |
| DELETE | /submissions/{submission_id} |  |

### services
| Method | Path | Description |
|--------|------|-------------|
| GET | /services/ |  |
| GET | /services/{addonName} |  |
| GET | /services/{addonName}/manifest |  |

### user
| Method | Path | Description |
|--------|------|-------------|
| GET | /user |  |

### dns_zones
| Method | Path | Description |
|--------|------|-------------|
| POST | /dns_zones |  |
| GET | /dns_zones |  |
| GET | /dns_zones/{zone_id} |  |
| DELETE | /dns_zones/{zone_id} |  |
| PUT | /dns_zones/{zone_id}/transfer |  |
| GET | /dns_zones/{zone_id}/dns_records |  |
| POST | /dns_zones/{zone_id}/dns_records |  |
| GET | /dns_zones/{zone_id}/dns_records/{dns_record_id} |  |
| DELETE | /dns_zones/{zone_id}/dns_records/{dns_record_id} |  |

### ai-gateway
| Method | Path | Description |
|--------|------|-------------|
| GET | /ai-gateway/providers |  |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all sites?" -> GET /sites
- "Create a site?" -> POST /sites
- "Get site details?" -> GET /sites/{site_id}
- "Partially update a site?" -> PATCH /sites/{site_id}
- "Delete a site?" -> DELETE /sites/{site_id}
- "Create a ssl?" -> POST /sites/{site_id}/ssl
- "List all ssl?" -> GET /sites/{site_id}/ssl
- "List all certificates?" -> GET /sites/{site_id}/ssl/certificates
- "List all env?" -> GET /accounts/{account_id}/env
- "Create a env?" -> POST /accounts/{account_id}/env
- "List all env?" -> GET /api/v1/sites/{site_id}/env
- "Get env details?" -> GET /accounts/{account_id}/env/{key}
- "Update a env?" -> PUT /accounts/{account_id}/env/{key}
- "Partially update a env?" -> PATCH /accounts/{account_id}/env/{key}
- "Delete a env?" -> DELETE /accounts/{account_id}/env/{key}
- "Delete a value?" -> DELETE /accounts/{account_id}/env/{key}/value/{id}
- "List all functions?" -> GET /sites/{site_id}/functions
- "List all forms?" -> GET /sites/{site_id}/forms
- "Delete a form?" -> DELETE /sites/{site_id}/forms/{form_id}
- "List all submissions?" -> GET /sites/{site_id}/submissions
- "List all files?" -> GET /sites/{site_id}/files
- "List all assets?" -> GET /sites/{site_id}/assets
- "Create a asset?" -> POST /sites/{site_id}/assets
- "Get asset details?" -> GET /sites/{site_id}/assets/{asset_id}
- "Update a asset?" -> PUT /sites/{site_id}/assets/{asset_id}
- "Delete a asset?" -> DELETE /sites/{site_id}/assets/{asset_id}
- "List all public_signature?" -> GET /sites/{site_id}/assets/{asset_id}/public_signature
- "Get file details?" -> GET /sites/{site_id}/files/{file_path}
- "Create a purge?" -> POST /purge
- "List all snippets?" -> GET /sites/{site_id}/snippets
- "Create a snippet?" -> POST /sites/{site_id}/snippets
- "Get snippet details?" -> GET /sites/{site_id}/snippets/{snippet_id}
- "Update a snippet?" -> PUT /sites/{site_id}/snippets/{snippet_id}
- "Delete a snippet?" -> DELETE /sites/{site_id}/snippets/{snippet_id}
- "List all metadata?" -> GET /sites/{site_id}/metadata
- "List all build_hooks?" -> GET /sites/{site_id}/build_hooks
- "Create a build_hook?" -> POST /sites/{site_id}/build_hooks
- "Get build_hook details?" -> GET /sites/{site_id}/build_hooks/{id}
- "Update a build_hook?" -> PUT /sites/{site_id}/build_hooks/{id}
- "Delete a build_hook?" -> DELETE /sites/{site_id}/build_hooks/{id}
- "List all deploys?" -> GET /sites/{site_id}/deploys
- "Create a deploy?" -> POST /sites/{site_id}/deploys
- "Get deploy details?" -> GET /sites/{site_id}/deploys/{deploy_id}
- "Update a deploy?" -> PUT /sites/{site_id}/deploys/{deploy_id}
- "Delete a deploy?" -> DELETE /sites/{site_id}/deploys/{deploy_id}
- "Create a cancel?" -> POST /deploys/{deploy_id}/cancel
- "Create a restore?" -> POST /sites/{site_id}/deploys/{deploy_id}/restore
- "List all builds?" -> GET /sites/{site_id}/builds
- "Create a build?" -> POST /sites/{site_id}/builds
- "List all deployed-branches?" -> GET /sites/{site_id}/deployed-branches
- "Get build details?" -> GET /builds/{build_id}
- "Create a log?" -> POST /builds/{build_id}/log
- "Create a start?" -> POST /builds/{build_id}/start
- "List all status?" -> GET /{account_id}/builds/status
- "List all dns?" -> GET /sites/{site_id}/dns
- "Get deploy details?" -> GET /deploys/{deploy_id}
- "Delete a deploy?" -> DELETE /deploys/{deploy_id}
- "Create a lock?" -> POST /deploys/{deploy_id}/lock
- "Create a unlock?" -> POST /deploys/{deploy_id}/unlock
- "Update a file?" -> PUT /deploys/{deploy_id}/files/{path}
- "Update a function?" -> PUT /deploys/{deploy_id}/functions/{name}
- "Update a plugin?" -> PUT /sites/{site_id}/plugins/{package}
- "List all latest?" -> GET /sites/{site_id}/plugin_runs/latest
- "Create a plugin_run?" -> POST /deploys/{deploy_id}/plugin_runs
- "List all submissions?" -> GET /forms/{form_id}/submissions
- "List all hooks?" -> GET /hooks
- "Create a hook?" -> POST /hooks
- "Get hook details?" -> GET /hooks/{hook_id}
- "Update a hook?" -> PUT /hooks/{hook_id}
- "Delete a hook?" -> DELETE /hooks/{hook_id}
- "Create a enable?" -> POST /hooks/{hook_id}/enable
- "List all types?" -> GET /hooks/types
- "Create a ticket?" -> POST /oauth/tickets
- "Get ticket details?" -> GET /oauth/tickets/{ticket_id}
- "Create a exchange?" -> POST /oauth/tickets/{ticket_id}/exchange
- "List all deploy_keys?" -> GET /deploy_keys
- "Create a deploy_key?" -> POST /deploy_keys
- "Get deploy_key details?" -> GET /deploy_keys/{key_id}
- "Delete a deploy_key?" -> DELETE /deploy_keys/{key_id}
- "Create a site?" -> POST /{account_slug}/sites
- "List all sites?" -> GET /{account_slug}/sites
- "List all members?" -> GET /{account_slug}/members
- "Create a member?" -> POST /{account_slug}/members
- "Get member details?" -> GET /{account_slug}/members/{member_id}
- "Update a member?" -> PUT /{account_slug}/members/{member_id}
- "Delete a member?" -> DELETE /{account_slug}/members/{member_id}
- "List all payment_methods?" -> GET /billing/payment_methods
- "List all types?" -> GET /accounts/types
- "List all accounts?" -> GET /accounts
- "Create a account?" -> POST /accounts
- "Get account details?" -> GET /accounts/{account_id}
- "Update a account?" -> PUT /accounts/{account_id}
- "Delete a account?" -> DELETE /accounts/{account_id}
- "Search audit?" -> GET /accounts/{account_id}/audit
- "List all agent_runners?" -> GET /agent_runners
- "Create a agent_runner?" -> POST /agent_runners
- "Create a upload_url?" -> POST /agent_runners/upload_url
- "Get agent_runner details?" -> GET /agent_runners/{agent_runner_id}
- "Partially update a agent_runner?" -> PATCH /agent_runners/{agent_runner_id}
- "Delete a agent_runner?" -> DELETE /agent_runners/{agent_runner_id}
- "Create a archive?" -> POST /agent_runners/{agent_runner_id}/archive
- "Create a pull_request?" -> POST /agent_runners/{agent_runner_id}/pull_request
- "Create a commit?" -> POST /agent_runners/{agent_runner_id}/commit
- "List all sessions?" -> GET /agent_runners/{agent_runner_id}/sessions
- "Create a session?" -> POST /agent_runners/{agent_runner_id}/sessions
- "Get session details?" -> GET /agent_runners/{agent_runner_id}/sessions/{agent_runner_session_id}
- "Partially update a session?" -> PATCH /agent_runners/{agent_runner_id}/sessions/{agent_runner_session_id}
- "Delete a session?" -> DELETE /agent_runners/{agent_runner_id}/sessions/{agent_runner_session_id}
- "Search submissions?" -> GET /submissions/{submission_id}
- "Delete a submission?" -> DELETE /submissions/{submission_id}
- "List all service-instances?" -> GET /sites/{site_id}/service-instances
- "Create a instance?" -> POST /sites/{site_id}/services/{addon}/instances
- "Get instance details?" -> GET /sites/{site_id}/services/{addon}/instances/{instance_id}
- "Update a instance?" -> PUT /sites/{site_id}/services/{addon}/instances/{instance_id}
- "Delete a instance?" -> DELETE /sites/{site_id}/services/{addon}/instances/{instance_id}
- "List all services?" -> GET /services/
- "Get service details?" -> GET /services/{addonName}
- "List all manifest?" -> GET /services/{addonName}/manifest
- "List all user?" -> GET /user
- "Create a traffic_split?" -> POST /sites/{site_id}/traffic_splits
- "List all traffic_splits?" -> GET /sites/{site_id}/traffic_splits
- "Update a traffic_split?" -> PUT /sites/{site_id}/traffic_splits/{split_test_id}
- "Get traffic_split details?" -> GET /sites/{site_id}/traffic_splits/{split_test_id}
- "Create a publish?" -> POST /sites/{site_id}/traffic_splits/{split_test_id}/publish
- "Create a unpublish?" -> POST /sites/{site_id}/traffic_splits/{split_test_id}/unpublish
- "Create a dns_zone?" -> POST /dns_zones
- "List all dns_zones?" -> GET /dns_zones
- "Get dns_zone details?" -> GET /dns_zones/{zone_id}
- "Delete a dns_zone?" -> DELETE /dns_zones/{zone_id}
- "List all dns_records?" -> GET /dns_zones/{zone_id}/dns_records
- "Create a dns_record?" -> POST /dns_zones/{zone_id}/dns_records
- "Get dns_record details?" -> GET /dns_zones/{zone_id}/dns_records/{dns_record_id}
- "Delete a dns_record?" -> DELETE /dns_zones/{zone_id}/dns_records/{dns_record_id}
- "List all dev_servers?" -> GET /sites/{site_id}/dev_servers
- "Create a dev_server?" -> POST /sites/{site_id}/dev_servers
- "Get dev_server details?" -> GET /sites/{site_id}/dev_servers/{dev_server_id}
- "Create a activity?" -> POST /sites/{site_id}/dev_servers/{dev_server_id}/activity
- "Create a state?" -> POST /sites/{site_id}/dev_servers/{dev_server_id}/state
- "List all dev_server_hooks?" -> GET /sites/{site_id}/dev_server_hooks
- "Create a dev_server_hook?" -> POST /sites/{site_id}/dev_server_hooks
- "Get dev_server_hook details?" -> GET /sites/{site_id}/dev_server_hooks/{id}
- "Update a dev_server_hook?" -> PUT /sites/{site_id}/dev_server_hooks/{id}
- "Delete a dev_server_hook?" -> DELETE /sites/{site_id}/dev_server_hooks/{id}
- "List all providers?" -> GET /ai-gateway/providers
- "List all token?" -> GET /sites/{site_id}/ai-gateway/token
- "List all token?" -> GET /accounts/{account_id}/ai-gateway/token
- "Create a database?" -> POST /sites/{site_id}/database
- "List all database?" -> GET /sites/{site_id}/database
- "Create a branch?" -> POST /sites/{site_id}/database/branch
- "Get branch details?" -> GET /sites/{site_id}/database/branch/{deploy_id}
- "Delete a branch?" -> DELETE /sites/{site_id}/database/branch/{deploy_id}
- "Create a snapshot?" -> POST /sites/{site_id}/database/snapshot
- "List all snapshots?" -> GET /sites/{site_id}/database/snapshots
- "Delete a snapshot?" -> DELETE /sites/{site_id}/database/snapshot/{snapshot_id}
- "Create a restore?" -> POST /sites/{site_id}/database/snapshot/{snapshot_id}/restore
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
