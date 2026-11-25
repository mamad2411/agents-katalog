---
name: vsonline
description: "VSOnline API skill. Use when working with VSOnline for api, health, internal. Covers 61 endpoints."
version: 1.0.0
generator: lapsh
---

# VSOnline
API version: v1

## Auth
Bearer bearer

## Base URL
https://online.visualstudio.com

## Setup
1. Set Authorization header with your Bearer token
2. GET /api/v1/Billing -- verify access
3. POST /api/v1/AgentTelemetry -- create first AgentTelemetry

## Endpoints

61 endpoints across 5 groups. See references/api-spec.lap for full details.

### api
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/v1/Agents/{family} |  |
| POST | /api/v1/AgentTelemetry |  |
| POST | /api/v1/AgentTelemetry/standalone |  |
| PUT | /api/v1/Billing/ensure_plan |  |
| GET | /api/v1/Billing |  |
| GET | /api/v1/GenevaActions/Billing/{environmentId} |  |
| POST | /api/v1/GenevaActions/Billing/resend |  |
| POST | /api/v1/GenevaActions/Billing/{environmentId}/state-changes |  |
| GET | /api/v1/GenevaActions/Billing/{environmentId}/state-changes |  |
| GET | /api/v1/GenevaActions/Configuration/{key} |  |
| DELETE | /api/v1/GenevaActions/Configuration/{key} |  |
| POST | /api/v1/GenevaActions/Configuration |  |
| GET | /api/v1/Environments/{environmentId} |  |
| DELETE | /api/v1/Environments/{environmentId} |  |
| PATCH | /api/v1/Environments/{environmentId} |  |
| GET | /api/v1/Environments |  |
| POST | /api/v1/Environments |  |
| POST | /api/v1/Environments/{environmentId}/shutdown |  |
| POST | /api/v1/Environments/{environmentId}/start |  |
| POST | /api/v1/Environments/{environmentId}/archive |  |
| GET | /api/v1/Environments/{environmentId}/archive |  |
| POST | /api/v1/Environments/{environmentId}/export |  |
| PATCH | /api/v1/Environments/{environmentId}/restore |  |
| PATCH | /api/v1/Environments/{environmentId}/folder |  |
| PUT | /api/v1/Environments/{environmentId}/secrets |  |
| POST | /api/v1/Environments/{environmentId}/notify |  |
| GET | /api/v1/GenevaActions/Environments/{environmentId} |  |
| DELETE | /api/v1/GenevaActions/Environments/{environmentId} |  |
| PUT | /api/v1/GenevaActions/Environments/{environmentId}/shutdown |  |
| PUT | /api/v1/GenevaActions/Environments/{environmentId}/archive |  |
| GET | /api/v1/GenevaActions/Environments/storage/{environmentIdOrFriendlyName}/{targetBlob} |  |
| POST | /api/v1/GenevaActions/Environments/{environmentId}/upload/running/vm/logs |  |
| GET | /api/v1/Environments/{environmentId}/state |  |
| POST | /api/v1/GenevaActions/Failover/start/{region} |  |
| POST | /api/v1/HeartBeat |  |
| GET | /api/v1/Locations |  |
| GET | /api/v1/Locations/{location} |  |
| GET | /api/v1/pools/default |  |
| POST | /api/v1/GenevaActions/Pools/rotate-pools |  |
| POST | /api/v1/GenevaActions/Pools |  |
| POST | /api/v1/GenevaActions/Pools/change-resource-deletion-setting |  |
| POST | /api/v2/prebuilds/templates |  |
| POST | /api/v2/prebuilds/templates/{templateId}/updatestatus |  |
| GET | /api/v2/prebuilds/templates/skus/repo/{repoId}/branch/{branchName}/hash/{prebuildHash}/location/{location}/devcontainerpath/{devContainerPath} |  |
| POST | /api/v2/prebuilds/delete |  |
| POST | /api/v2/prebuilds/templates/updatemaxversions |  |
| PUT | /api/v2/prebuilds/pools/{poolId}/instances |  |
| POST | /api/v2/prebuilds/pools/{poolId}/instances |  |
| GET | /api/v2/prebuilds/template/{environmentId} |  |
| POST | /api/v1/GenevaActions/Prebuilds/pools/delete |  |
| POST | /api/v1/GenevaActions/Prebuilds/pools/createorupdatesettings |  |
| POST | /api/v1/GenevaActions/Resources/{resourceId}/under-investigation |  |
| POST | /api/v1/GenevaActions/Resources/{resourceId}/storage-credentials |  |
| GET | /api/v1/Tunnel/{environmentId}/portInfo |  |
| POST | /api/v1/GenevaActions/VnetPoolDefinitions |  |
| DELETE | /api/v1/GenevaActions/VnetPoolDefinitions |  |

### health
| Method | Path | Description |
|--------|------|-------------|
| GET | /health |  |

### internal
| Method | Path | Description |
|--------|------|-------------|
| GET | /internal/Netmon/correlation |  |

### .well-known
| Method | Path | Description |
|--------|------|-------------|
| GET | /.well-known/jwks |  |
| GET | /.well-known/openid-configuration |  |

### warmup
| Method | Path | Description |
|--------|------|-------------|
| GET | /warmup |  |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get Agent details?" -> GET /api/v1/Agents/{family}
- "Create a AgentTelemetry?" -> POST /api/v1/AgentTelemetry
- "Create a standalone?" -> POST /api/v1/AgentTelemetry/standalone
- "List all Billing?" -> GET /api/v1/Billing
- "Get Billing details?" -> GET /api/v1/GenevaActions/Billing/{environmentId}
- "Create a resend?" -> POST /api/v1/GenevaActions/Billing/resend
- "Create a state-change?" -> POST /api/v1/GenevaActions/Billing/{environmentId}/state-changes
- "List all state-changes?" -> GET /api/v1/GenevaActions/Billing/{environmentId}/state-changes
- "Get Configuration details?" -> GET /api/v1/GenevaActions/Configuration/{key}
- "Delete a Configuration?" -> DELETE /api/v1/GenevaActions/Configuration/{key}
- "Create a Configuration?" -> POST /api/v1/GenevaActions/Configuration
- "Get Environment details?" -> GET /api/v1/Environments/{environmentId}
- "Delete a Environment?" -> DELETE /api/v1/Environments/{environmentId}
- "Partially update a Environment?" -> PATCH /api/v1/Environments/{environmentId}
- "List all Environments?" -> GET /api/v1/Environments
- "Create a Environment?" -> POST /api/v1/Environments
- "Create a shutdown?" -> POST /api/v1/Environments/{environmentId}/shutdown
- "Create a start?" -> POST /api/v1/Environments/{environmentId}/start
- "Create a archive?" -> POST /api/v1/Environments/{environmentId}/archive
- "List all archive?" -> GET /api/v1/Environments/{environmentId}/archive
- "Create a export?" -> POST /api/v1/Environments/{environmentId}/export
- "Create a notify?" -> POST /api/v1/Environments/{environmentId}/notify
- "Get Environment details?" -> GET /api/v1/GenevaActions/Environments/{environmentId}
- "Delete a Environment?" -> DELETE /api/v1/GenevaActions/Environments/{environmentId}
- "Get storage details?" -> GET /api/v1/GenevaActions/Environments/storage/{environmentIdOrFriendlyName}/{targetBlob}
- "Create a log?" -> POST /api/v1/GenevaActions/Environments/{environmentId}/upload/running/vm/logs
- "List all state?" -> GET /api/v1/Environments/{environmentId}/state
- "List all health?" -> GET /health
- "Create a HeartBeat?" -> POST /api/v1/HeartBeat
- "List all Locations?" -> GET /api/v1/Locations
- "Get Location details?" -> GET /api/v1/Locations/{location}
- "List all correlation?" -> GET /internal/Netmon/correlation
- "List all jwks?" -> GET /.well-known/jwks
- "List all openid-configuration?" -> GET /.well-known/openid-configuration
- "List all default?" -> GET /api/v1/pools/default
- "Create a rotate-pool?" -> POST /api/v1/GenevaActions/Pools/rotate-pools
- "Create a Pool?" -> POST /api/v1/GenevaActions/Pools
- "Create a change-resource-deletion-setting?" -> POST /api/v1/GenevaActions/Pools/change-resource-deletion-setting
- "Create a template?" -> POST /api/v2/prebuilds/templates
- "Create a updatestatus?" -> POST /api/v2/prebuilds/templates/{templateId}/updatestatus
- "Get devcontainerpath details?" -> GET /api/v2/prebuilds/templates/skus/repo/{repoId}/branch/{branchName}/hash/{prebuildHash}/location/{location}/devcontainerpath/{devContainerPath}
- "Create a delete?" -> POST /api/v2/prebuilds/delete
- "Create a updatemaxversion?" -> POST /api/v2/prebuilds/templates/updatemaxversions
- "Create a instance?" -> POST /api/v2/prebuilds/pools/{poolId}/instances
- "Get template details?" -> GET /api/v2/prebuilds/template/{environmentId}
- "Create a delete?" -> POST /api/v1/GenevaActions/Prebuilds/pools/delete
- "Create a createorupdatesetting?" -> POST /api/v1/GenevaActions/Prebuilds/pools/createorupdatesettings
- "Create a under-investigation?" -> POST /api/v1/GenevaActions/Resources/{resourceId}/under-investigation
- "Create a storage-credential?" -> POST /api/v1/GenevaActions/Resources/{resourceId}/storage-credentials
- "List all portInfo?" -> GET /api/v1/Tunnel/{environmentId}/portInfo
- "Create a VnetPoolDefinition?" -> POST /api/v1/GenevaActions/VnetPoolDefinitions
- "List all warmup?" -> GET /warmup
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
