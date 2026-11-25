---
name: render-public-api
description: "Render Public API skill. Use when working with Render Public for blueprints, owners, disks. Covers 196 endpoints."
version: 1.0.0
generator: lapsh
---

# Render Public API
API version: 1.0.0

## Auth
Bearer bearer

## Base URL
https://api.render.com/v1

## Setup
1. Set Authorization header with your Bearer token
2. GET /blueprints -- verify access
3. POST /blueprints/validate -- create first validate

## Endpoints

196 endpoints across 25 groups. See references/api-spec.lap for full details.

### blueprints
| Method | Path | Description |
|--------|------|-------------|
| GET | /blueprints | List Blueprints |
| POST | /blueprints/validate | Validate Blueprint |
| GET | /blueprints/{blueprintId} | Retrieve Blueprint |
| PATCH | /blueprints/{blueprintId} | Update Blueprint |
| DELETE | /blueprints/{blueprintId} | Disconnect Blueprint |
| GET | /blueprints/{blueprintId}/syncs | List Blueprint syncs |

### owners
| Method | Path | Description |
|--------|------|-------------|
| PATCH | /owners/{ownerId}/members/{userId} | Update workspace member role |
| DELETE | /owners/{ownerId}/members/{userId} | Remove workspace member |
| GET | /owners | List workspaces |
| GET | /owners/{ownerId} | Retrieve workspace |
| GET | /owners/{ownerId}/members | List workspace members |
| GET | /owners/{ownerId}/audit-logs | List workspace audit logs |

### disks
| Method | Path | Description |
|--------|------|-------------|
| GET | /disks | List disks |
| POST | /disks | Add disk |
| GET | /disks/{diskId} | Retrieve disk |
| PATCH | /disks/{diskId} | Update disk |
| DELETE | /disks/{diskId} | Delete disk |
| GET | /disks/{diskId}/snapshots | List snapshots |
| POST | /disks/{diskId}/snapshots/restore | Restore snapshot |

### users
| Method | Path | Description |
|--------|------|-------------|
| GET | /users | Get the authenticated user |

### organizations
| Method | Path | Description |
|--------|------|-------------|
| GET | /organizations/{orgId}/audit-logs | List organization audit logs |

### notification-settings
| Method | Path | Description |
|--------|------|-------------|
| GET | /notification-settings/owners/{ownerId} | Retrieve notification settings |
| PATCH | /notification-settings/owners/{ownerId} | Update notification settings |
| GET | /notification-settings/overrides | List notification overrides |
| GET | /notification-settings/overrides/services/{serviceId} | Retrieve notification override |
| PATCH | /notification-settings/overrides/services/{serviceId} | Update notification override |

### registrycredentials
| Method | Path | Description |
|--------|------|-------------|
| GET | /registrycredentials | List registry credentials |
| POST | /registrycredentials | Create registry credential |
| GET | /registrycredentials/{registryCredentialId} | Retrieve registry credential |
| PATCH | /registrycredentials/{registryCredentialId} | Update registry credential |
| DELETE | /registrycredentials/{registryCredentialId} | Delete registry credential |

### services
| Method | Path | Description |
|--------|------|-------------|
| GET | /services | List services |
| POST | /services | Create service |
| GET | /services/{serviceId} | Retrieve service |
| PATCH | /services/{serviceId} | Update service |
| DELETE | /services/{serviceId} | Delete service |
| POST | /services/{serviceId}/cache/purge | Purge Web Service Cache |
| GET | /services/{serviceId}/deploys | List deploys |
| POST | /services/{serviceId}/deploys | Trigger deploy |
| GET | /services/{serviceId}/deploys/{deployId} | Retrieve deploy |
| POST | /services/{serviceId}/deploys/{deployId}/cancel | Cancel deploy |
| POST | /services/{serviceId}/rollback | Roll back deploy |
| GET | /services/{serviceId}/env-vars | List environment variables |
| PUT | /services/{serviceId}/env-vars | Update environment variables |
| GET | /services/{serviceId}/env-vars/{envVarKey} | Retrieve environment variable |
| PUT | /services/{serviceId}/env-vars/{envVarKey} | Add or update environment variable |
| DELETE | /services/{serviceId}/env-vars/{envVarKey} | Delete environment variable |
| GET | /services/{serviceId}/secret-files | List secret files |
| PUT | /services/{serviceId}/secret-files | Update secret files |
| GET | /services/{serviceId}/secret-files/{secretFileName} | Retrieve secret file |
| PUT | /services/{serviceId}/secret-files/{secretFileName} | Add or update secret file |
| DELETE | /services/{serviceId}/secret-files/{secretFileName} | Delete secret file |
| GET | /services/{serviceId}/events | List events |
| GET | /services/{serviceId}/headers | List header rules |
| POST | /services/{serviceId}/headers | Add header rule |
| PUT | /services/{serviceId}/headers | Replace header rules |
| DELETE | /services/{serviceId}/headers/{headerId} | Delete header rule |
| GET | /services/{serviceId}/routes | List redirect/rewrite rules |
| POST | /services/{serviceId}/routes | Add redirect/rewrite rules |
| PATCH | /services/{serviceId}/routes | Update redirect/rewrite rule priority |
| PUT | /services/{serviceId}/routes | Update redirect/rewrite rules |
| DELETE | /services/{serviceId}/routes/{routeId} | Delete redirect/rewrite rule |
| GET | /services/{serviceId}/custom-domains | List custom domains |
| POST | /services/{serviceId}/custom-domains | Add custom domain |
| GET | /services/{serviceId}/custom-domains/{customDomainIdOrName} | Retrieve custom domain |
| DELETE | /services/{serviceId}/custom-domains/{customDomainIdOrName} | Delete custom domain |
| POST | /services/{serviceId}/custom-domains/{customDomainIdOrName}/verify | Verify DNS configuration |
| POST | /services/{serviceId}/suspend | Suspend service |
| POST | /services/{serviceId}/resume | Resume service |
| POST | /services/{serviceId}/restart | Restart service |
| POST | /services/{serviceId}/scale | Scale instance count |
| PUT | /services/{serviceId}/autoscaling | Update autoscaling config |
| DELETE | /services/{serviceId}/autoscaling | Delete autoscaling config |
| POST | /services/{serviceId}/preview | Create service preview (image-backed) |
| GET | /services/{serviceId}/jobs | List jobs |
| POST | /services/{serviceId}/jobs | Create job |
| GET | /services/{serviceId}/jobs/{jobId} | Retrieve job |
| POST | /services/{serviceId}/jobs/{jobId}/cancel | Cancel running job |
| GET | /services/{serviceId}/instances | List instances |

### cron-jobs
| Method | Path | Description |
|--------|------|-------------|
| POST | /cron-jobs/{cronJobId}/runs | Trigger cron job run |
| DELETE | /cron-jobs/{cronJobId}/runs | Cancel running cron job |

### events
| Method | Path | Description |
|--------|------|-------------|
| GET | /events/{eventId} | Retrieve event |

### logs
| Method | Path | Description |
|--------|------|-------------|
| GET | /logs | List logs |
| GET | /logs/subscribe | Subscribe to new logs |
| GET | /logs/values | List log label values |
| GET | /logs/streams/owner/{ownerId} | Retrieve log stream |
| PUT | /logs/streams/owner/{ownerId} | Update log stream |
| DELETE | /logs/streams/owner/{ownerId} | Delete log stream |
| GET | /logs/streams/resource | List log stream overrides |
| GET | /logs/streams/resource/{resourceId} | Retrieve log stream override |
| PUT | /logs/streams/resource/{resourceId} | Update log stream override |
| DELETE | /logs/streams/resource/{resourceId} | Delete log stream override |

### metrics-stream
| Method | Path | Description |
|--------|------|-------------|
| GET | /metrics-stream/{ownerId} | Retrieve metrics stream |
| PUT | /metrics-stream/{ownerId} | Create or update metrics stream |
| DELETE | /metrics-stream/{ownerId} | Delete metrics stream |

### metrics
| Method | Path | Description |
|--------|------|-------------|
| GET | /metrics/cpu | Get CPU usage |
| GET | /metrics/cpu-limit | Get CPU limit |
| GET | /metrics/cpu-target | Get CPU target |
| GET | /metrics/memory | Get memory usage |
| GET | /metrics/memory-limit | Get memory limit |
| GET | /metrics/memory-target | Get memory target |
| GET | /metrics/http-requests | Get HTTP request count |
| GET | /metrics/http-latency | Get HTTP latency |
| GET | /metrics/bandwidth | Get bandwidth usage |
| GET | /metrics/bandwidth-sources | Get bandwidth usage breakdown by traffic source |
| GET | /metrics/disk-usage | Get disk usage |
| GET | /metrics/disk-capacity | Get disk capacity |
| GET | /metrics/instance-count | Get instance count |
| GET | /metrics/active-connections | Get active connection count |
| GET | /metrics/replication-lag | Get replica lag |
| GET | /metrics/filters/application | List queryable instance values |
| GET | /metrics/filters/http | List queryable status codes and host values |
| GET | /metrics/filters/path | List queryable paths |
| GET | /metrics/task-runs-queued | Get task runs queued count |
| GET | /metrics/task-runs-completed | Get task runs completed count |

### key-value
| Method | Path | Description |
|--------|------|-------------|
| GET | /key-value | List Key Value instances |
| POST | /key-value | Create Key Value instance |
| GET | /key-value/{keyValueId} | Retrieve Key Value instance |
| PATCH | /key-value/{keyValueId} | Update Key Value instance |
| DELETE | /key-value/{keyValueId} | Delete Key Value instance |
| GET | /key-value/{keyValueId}/connection-info | Retrieve Key Value connection info |
| POST | /key-value/{keyValueId}/suspend | Suspend Key Value instance |
| POST | /key-value/{keyValueId}/resume | Resume Key Value instance |

### redis
| Method | Path | Description |
|--------|------|-------------|
| GET | /redis | List Redis instances |
| POST | /redis | Create Redis instance |
| GET | /redis/{redisId} | Retrieve Redis instance |
| PATCH | /redis/{redisId} | Update Redis instance |
| DELETE | /redis/{redisId} | Delete Redis instance |
| GET | /redis/{redisId}/connection-info | Retrieve Redis connection info |

### postgres
| Method | Path | Description |
|--------|------|-------------|
| GET | /postgres | List Postgres instances |
| POST | /postgres | Create Postgres instance |
| GET | /postgres/{postgresId} | Retrieve Postgres instance |
| PATCH | /postgres/{postgresId} | Update Postgres instance |
| DELETE | /postgres/{postgresId} | Delete Postgres instance |
| GET | /postgres/{postgresId}/connection-info | Retrieve Postgres connection info |
| GET | /postgres/{postgresId}/recovery | Retrieve point-in-time recovery status |
| POST | /postgres/{postgresId}/recovery | Trigger point-in-time recovery |
| POST | /postgres/{postgresId}/suspend | Suspend Postgres instance |
| POST | /postgres/{postgresId}/resume | Resume Postgres instance |
| POST | /postgres/{postgresId}/restart | Restart Postgres instance |
| POST | /postgres/{postgresId}/failover | Failover Postgres instance |
| GET | /postgres/{postgresId}/export | List Postgres exports |
| POST | /postgres/{postgresId}/export | Create Postgres export |
| GET | /postgres/{postgresId}/credentials | List PostgreSQL Users |
| POST | /postgres/{postgresId}/credentials | Create PostgreSQL User |
| DELETE | /postgres/{postgresId}/credentials/{username} | Delete PostgreSQL User |

### projects
| Method | Path | Description |
|--------|------|-------------|
| GET | /projects | List projects |
| POST | /projects | Create project |
| GET | /projects/{projectId} | Retrieve Project |
| PATCH | /projects/{projectId} | Update project |
| DELETE | /projects/{projectId} | Delete project |

### environments
| Method | Path | Description |
|--------|------|-------------|
| POST | /environments | Create environment |
| GET | /environments | List environments |
| GET | /environments/{environmentId} | Retrieve environment |
| PATCH | /environments/{environmentId} | Update environment |
| DELETE | /environments/{environmentId} | Delete environment |
| POST | /environments/{environmentId}/resources | Add resources to environment |
| DELETE | /environments/{environmentId}/resources | Remove resources from environment |

### env-groups
| Method | Path | Description |
|--------|------|-------------|
| GET | /env-groups | List environment groups |
| POST | /env-groups | Create environment group |
| GET | /env-groups/{envGroupId} | Retrieve environment group |
| PATCH | /env-groups/{envGroupId} | Update environment group |
| DELETE | /env-groups/{envGroupId} | Delete environment group |
| POST | /env-groups/{envGroupId}/services/{serviceId} | Link service |
| DELETE | /env-groups/{envGroupId}/services/{serviceId} | Unlink service |
| GET | /env-groups/{envGroupId}/env-vars/{envVarKey} | Retrieve environment variable |
| PUT | /env-groups/{envGroupId}/env-vars/{envVarKey} | Add or update environment variable |
| DELETE | /env-groups/{envGroupId}/env-vars/{envVarKey} | Remove environment variable |
| GET | /env-groups/{envGroupId}/secret-files/{secretFileName} | Retrieve secret file |
| PUT | /env-groups/{envGroupId}/secret-files/{secretFileName} | Add or update secret file |
| DELETE | /env-groups/{envGroupId}/secret-files/{secretFileName} | Remove secret file |

### maintenance
| Method | Path | Description |
|--------|------|-------------|
| GET | /maintenance | List maintenance runs |
| GET | /maintenance/{maintenanceRunParam} | Retrieve maintenance run |
| PATCH | /maintenance/{maintenanceRunParam} | Update maintenance run |
| POST | /maintenance/{maintenanceRunParam}/trigger | Trigger maintenance run |

### webhooks
| Method | Path | Description |
|--------|------|-------------|
| POST | /webhooks | Create a webhook |
| GET | /webhooks | List webhooks |
| GET | /webhooks/{webhookId} | Retrieve a webhook |
| PATCH | /webhooks/{webhookId} | Update a webhook |
| DELETE | /webhooks/{webhookId} | Delete a webhook |
| GET | /webhooks/{webhookId}/events | List webhook events |

### workflows
| Method | Path | Description |
|--------|------|-------------|
| GET | /workflows | List workflows |
| POST | /workflows | Create a workflow |
| GET | /workflows/{workflowId} | Retrieve workflow |
| PATCH | /workflows/{workflowId} | Update workflow |
| DELETE | /workflows/{workflowId} | Delete workflow |

### workflowversions
| Method | Path | Description |
|--------|------|-------------|
| GET | /workflowversions | List workflow versions |
| POST | /workflowversions | Deploy a workflow version |
| GET | /workflowversions/{workflowVersionId} | Retrieve workflow version |

### tasks
| Method | Path | Description |
|--------|------|-------------|
| GET | /tasks | List tasks |
| GET | /tasks/{taskId} | Retrieve task |

### task-runs
| Method | Path | Description |
|--------|------|-------------|
| GET | /task-runs | List task runs |
| POST | /task-runs | Run task |
| GET | /task-runs/events | Stream realtime events (SSE) |
| GET | /task-runs/{taskRunId} | Retrieve task run |
| DELETE | /task-runs/{taskRunId} | Cancel task run |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all blueprints?" -> GET /blueprints
- "Create a validate?" -> POST /blueprints/validate
- "Partially update a member?" -> PATCH /owners/{ownerId}/members/{userId}
- "Delete a member?" -> DELETE /owners/{ownerId}/members/{userId}
- "Get blueprint details?" -> GET /blueprints/{blueprintId}
- "Partially update a blueprint?" -> PATCH /blueprints/{blueprintId}
- "Delete a blueprint?" -> DELETE /blueprints/{blueprintId}
- "List all syncs?" -> GET /blueprints/{blueprintId}/syncs
- "List all disks?" -> GET /disks
- "Create a disk?" -> POST /disks
- "Get disk details?" -> GET /disks/{diskId}
- "Partially update a disk?" -> PATCH /disks/{diskId}
- "Delete a disk?" -> DELETE /disks/{diskId}
- "List all snapshots?" -> GET /disks/{diskId}/snapshots
- "Create a restore?" -> POST /disks/{diskId}/snapshots/restore
- "List all users?" -> GET /users
- "List all owners?" -> GET /owners
- "Get owner details?" -> GET /owners/{ownerId}
- "List all members?" -> GET /owners/{ownerId}/members
- "List all audit-logs?" -> GET /owners/{ownerId}/audit-logs
- "List all audit-logs?" -> GET /organizations/{orgId}/audit-logs
- "Get owner details?" -> GET /notification-settings/owners/{ownerId}
- "Partially update a owner?" -> PATCH /notification-settings/owners/{ownerId}
- "List all overrides?" -> GET /notification-settings/overrides
- "Get service details?" -> GET /notification-settings/overrides/services/{serviceId}
- "Partially update a service?" -> PATCH /notification-settings/overrides/services/{serviceId}
- "List all registrycredentials?" -> GET /registrycredentials
- "Create a registrycredential?" -> POST /registrycredentials
- "Get registrycredential details?" -> GET /registrycredentials/{registryCredentialId}
- "Partially update a registrycredential?" -> PATCH /registrycredentials/{registryCredentialId}
- "Delete a registrycredential?" -> DELETE /registrycredentials/{registryCredentialId}
- "List all services?" -> GET /services
- "Create a service?" -> POST /services
- "Get service details?" -> GET /services/{serviceId}
- "Partially update a service?" -> PATCH /services/{serviceId}
- "Delete a service?" -> DELETE /services/{serviceId}
- "Create a purge?" -> POST /services/{serviceId}/cache/purge
- "List all deploys?" -> GET /services/{serviceId}/deploys
- "Create a deploy?" -> POST /services/{serviceId}/deploys
- "Get deploy details?" -> GET /services/{serviceId}/deploys/{deployId}
- "Create a cancel?" -> POST /services/{serviceId}/deploys/{deployId}/cancel
- "Create a rollback?" -> POST /services/{serviceId}/rollback
- "List all env-vars?" -> GET /services/{serviceId}/env-vars
- "Get env-var details?" -> GET /services/{serviceId}/env-vars/{envVarKey}
- "Update a env-var?" -> PUT /services/{serviceId}/env-vars/{envVarKey}
- "Delete a env-var?" -> DELETE /services/{serviceId}/env-vars/{envVarKey}
- "List all secret-files?" -> GET /services/{serviceId}/secret-files
- "Get secret-file details?" -> GET /services/{serviceId}/secret-files/{secretFileName}
- "Update a secret-file?" -> PUT /services/{serviceId}/secret-files/{secretFileName}
- "Delete a secret-file?" -> DELETE /services/{serviceId}/secret-files/{secretFileName}
- "List all events?" -> GET /services/{serviceId}/events
- "List all headers?" -> GET /services/{serviceId}/headers
- "Create a header?" -> POST /services/{serviceId}/headers
- "Delete a header?" -> DELETE /services/{serviceId}/headers/{headerId}
- "List all routes?" -> GET /services/{serviceId}/routes
- "Create a route?" -> POST /services/{serviceId}/routes
- "Delete a route?" -> DELETE /services/{serviceId}/routes/{routeId}
- "List all custom-domains?" -> GET /services/{serviceId}/custom-domains
- "Create a custom-domain?" -> POST /services/{serviceId}/custom-domains
- "Get custom-domain details?" -> GET /services/{serviceId}/custom-domains/{customDomainIdOrName}
- "Delete a custom-domain?" -> DELETE /services/{serviceId}/custom-domains/{customDomainIdOrName}
- "Create a verify?" -> POST /services/{serviceId}/custom-domains/{customDomainIdOrName}/verify
- "Create a suspend?" -> POST /services/{serviceId}/suspend
- "Create a resume?" -> POST /services/{serviceId}/resume
- "Create a restart?" -> POST /services/{serviceId}/restart
- "Create a scale?" -> POST /services/{serviceId}/scale
- "Create a preview?" -> POST /services/{serviceId}/preview
- "List all jobs?" -> GET /services/{serviceId}/jobs
- "Create a job?" -> POST /services/{serviceId}/jobs
- "Get job details?" -> GET /services/{serviceId}/jobs/{jobId}
- "Create a cancel?" -> POST /services/{serviceId}/jobs/{jobId}/cancel
- "List all instances?" -> GET /services/{serviceId}/instances
- "Create a run?" -> POST /cron-jobs/{cronJobId}/runs
- "Get event details?" -> GET /events/{eventId}
- "List all logs?" -> GET /logs
- "List all subscribe?" -> GET /logs/subscribe
- "List all values?" -> GET /logs/values
- "Get owner details?" -> GET /logs/streams/owner/{ownerId}
- "Update a owner?" -> PUT /logs/streams/owner/{ownerId}
- "Delete a owner?" -> DELETE /logs/streams/owner/{ownerId}
- "List all resource?" -> GET /logs/streams/resource
- "Get resource details?" -> GET /logs/streams/resource/{resourceId}
- "Update a resource?" -> PUT /logs/streams/resource/{resourceId}
- "Delete a resource?" -> DELETE /logs/streams/resource/{resourceId}
- "Get metrics-stream details?" -> GET /metrics-stream/{ownerId}
- "Update a metrics-stream?" -> PUT /metrics-stream/{ownerId}
- "Delete a metrics-stream?" -> DELETE /metrics-stream/{ownerId}
- "List all cpu?" -> GET /metrics/cpu
- "List all cpu-limit?" -> GET /metrics/cpu-limit
- "List all cpu-target?" -> GET /metrics/cpu-target
- "List all memory?" -> GET /metrics/memory
- "List all memory-limit?" -> GET /metrics/memory-limit
- "List all memory-target?" -> GET /metrics/memory-target
- "List all http-requests?" -> GET /metrics/http-requests
- "List all http-latency?" -> GET /metrics/http-latency
- "List all bandwidth?" -> GET /metrics/bandwidth
- "List all bandwidth-sources?" -> GET /metrics/bandwidth-sources
- "List all disk-usage?" -> GET /metrics/disk-usage
- "List all disk-capacity?" -> GET /metrics/disk-capacity
- "List all instance-count?" -> GET /metrics/instance-count
- "List all active-connections?" -> GET /metrics/active-connections
- "List all replication-lag?" -> GET /metrics/replication-lag
- "List all application?" -> GET /metrics/filters/application
- "List all http?" -> GET /metrics/filters/http
- "List all path?" -> GET /metrics/filters/path
- "List all task-runs-queued?" -> GET /metrics/task-runs-queued
- "List all task-runs-completed?" -> GET /metrics/task-runs-completed
- "List all key-value?" -> GET /key-value
- "Create a key-value?" -> POST /key-value
- "Get key-value details?" -> GET /key-value/{keyValueId}
- "Partially update a key-value?" -> PATCH /key-value/{keyValueId}
- "Delete a key-value?" -> DELETE /key-value/{keyValueId}
- "List all connection-info?" -> GET /key-value/{keyValueId}/connection-info
- "Create a suspend?" -> POST /key-value/{keyValueId}/suspend
- "Create a resume?" -> POST /key-value/{keyValueId}/resume
- "List all redis?" -> GET /redis
- "Create a redis?" -> POST /redis
- "Get redis details?" -> GET /redis/{redisId}
- "Partially update a redis?" -> PATCH /redis/{redisId}
- "Delete a redis?" -> DELETE /redis/{redisId}
- "List all connection-info?" -> GET /redis/{redisId}/connection-info
- "List all postgres?" -> GET /postgres
- "Create a postgre?" -> POST /postgres
- "Get postgre details?" -> GET /postgres/{postgresId}
- "Partially update a postgre?" -> PATCH /postgres/{postgresId}
- "Delete a postgre?" -> DELETE /postgres/{postgresId}
- "List all connection-info?" -> GET /postgres/{postgresId}/connection-info
- "List all recovery?" -> GET /postgres/{postgresId}/recovery
- "Create a recovery?" -> POST /postgres/{postgresId}/recovery
- "Create a suspend?" -> POST /postgres/{postgresId}/suspend
- "Create a resume?" -> POST /postgres/{postgresId}/resume
- "Create a restart?" -> POST /postgres/{postgresId}/restart
- "Create a failover?" -> POST /postgres/{postgresId}/failover
- "List all export?" -> GET /postgres/{postgresId}/export
- "Create a export?" -> POST /postgres/{postgresId}/export
- "List all credentials?" -> GET /postgres/{postgresId}/credentials
- "Create a credential?" -> POST /postgres/{postgresId}/credentials
- "Delete a credential?" -> DELETE /postgres/{postgresId}/credentials/{username}
- "List all projects?" -> GET /projects
- "Create a project?" -> POST /projects
- "Get project details?" -> GET /projects/{projectId}
- "Partially update a project?" -> PATCH /projects/{projectId}
- "Delete a project?" -> DELETE /projects/{projectId}
- "Create a environment?" -> POST /environments
- "List all environments?" -> GET /environments
- "Get environment details?" -> GET /environments/{environmentId}
- "Partially update a environment?" -> PATCH /environments/{environmentId}
- "Delete a environment?" -> DELETE /environments/{environmentId}
- "Create a resource?" -> POST /environments/{environmentId}/resources
- "List all env-groups?" -> GET /env-groups
- "Create a env-group?" -> POST /env-groups
- "Get env-group details?" -> GET /env-groups/{envGroupId}
- "Partially update a env-group?" -> PATCH /env-groups/{envGroupId}
- "Delete a env-group?" -> DELETE /env-groups/{envGroupId}
- "Delete a service?" -> DELETE /env-groups/{envGroupId}/services/{serviceId}
- "Get env-var details?" -> GET /env-groups/{envGroupId}/env-vars/{envVarKey}
- "Update a env-var?" -> PUT /env-groups/{envGroupId}/env-vars/{envVarKey}
- "Delete a env-var?" -> DELETE /env-groups/{envGroupId}/env-vars/{envVarKey}
- "Get secret-file details?" -> GET /env-groups/{envGroupId}/secret-files/{secretFileName}
- "Update a secret-file?" -> PUT /env-groups/{envGroupId}/secret-files/{secretFileName}
- "Delete a secret-file?" -> DELETE /env-groups/{envGroupId}/secret-files/{secretFileName}
- "List all maintenance?" -> GET /maintenance
- "Get maintenance details?" -> GET /maintenance/{maintenanceRunParam}
- "Partially update a maintenance?" -> PATCH /maintenance/{maintenanceRunParam}
- "Create a trigger?" -> POST /maintenance/{maintenanceRunParam}/trigger
- "Create a webhook?" -> POST /webhooks
- "List all webhooks?" -> GET /webhooks
- "Get webhook details?" -> GET /webhooks/{webhookId}
- "Partially update a webhook?" -> PATCH /webhooks/{webhookId}
- "Delete a webhook?" -> DELETE /webhooks/{webhookId}
- "List all events?" -> GET /webhooks/{webhookId}/events
- "List all workflows?" -> GET /workflows
- "Create a workflow?" -> POST /workflows
- "Get workflow details?" -> GET /workflows/{workflowId}
- "Partially update a workflow?" -> PATCH /workflows/{workflowId}
- "Delete a workflow?" -> DELETE /workflows/{workflowId}
- "List all workflowversions?" -> GET /workflowversions
- "Create a workflowversion?" -> POST /workflowversions
- "Get workflowversion details?" -> GET /workflowversions/{workflowVersionId}
- "List all tasks?" -> GET /tasks
- "Get task details?" -> GET /tasks/{taskId}
- "List all task-runs?" -> GET /task-runs
- "Create a task-run?" -> POST /task-runs
- "List all events?" -> GET /task-runs/events
- "Get task-run details?" -> GET /task-runs/{taskRunId}
- "Delete a task-run?" -> DELETE /task-runs/{taskRunId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
