---
name: otoroshi-admin-api
description: "Otoroshi Admin API skill. Use when working with Otoroshi Admin for new, lines, api. Covers 102 endpoints."
version: 1.0.0
generator: lapsh
---

# Otoroshi Admin API
API version: 1.5.0-dev

## Auth
Bearer basic

## Base URL
http://otoroshi-api.oto.tools/

## Setup
1. Set Authorization header with your Bearer token
2. GET /new/apikey -- verify access
3. POST /api/services/{serviceId}/apikeys -- create first apikeys

## Endpoints

102 endpoints across 4 groups. See references/api-spec.lap for full details.

### new
| Method | Path | Description |
|--------|------|-------------|
| GET | /new/apikey | Get a template of an Otoroshi Api Key |
| GET | /new/service | Get a template of an Otoroshi service descriptor |
| GET | /new/group | Get a template of an Otoroshi service group |

### lines
| Method | Path | Description |
|--------|------|-------------|
| GET | /lines | Get all environments |
| GET | /lines/{line}/services | Get all services for an environment |

### api
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/services/{serviceId}/apikeys/{clientId}/quotas | Get the quota state of an api key |
| DELETE | /api/services/{serviceId}/apikeys/{clientId}/quotas | Reset the quota state of an api key |
| GET | /api/services/{serviceId}/apikeys/{clientId}/group | Get the group of an api key |
| GET | /api/services/{serviceId}/apikeys/{clientId} | Get an api key |
| PUT | /api/services/{serviceId}/apikeys/{clientId} | Update an api key |
| PATCH | /api/services/{serviceId}/apikeys/{clientId} | Update an api key with a diff |
| DELETE | /api/services/{serviceId}/apikeys/{clientId} | Delete an api key |
| GET | /api/services/{serviceId}/apikeys | Get all api keys for the group of a service |
| POST | /api/services/{serviceId}/apikeys | Create a new api key for a service |
| GET | /api/groups/{groupId}/apikeys/{clientId}/quotas | Get the quota state of an api key |
| DELETE | /api/groups/{groupId}/apikeys/{clientId}/quotas | Reset the quota state of an api key |
| GET | /api/groups/{groupId}/apikeys/{clientId} | Get an api key |
| PUT | /api/groups/{groupId}/apikeys/{clientId} | Update an api key |
| PATCH | /api/groups/{groupId}/apikeys/{clientId} | Update an api key with a diff |
| DELETE | /api/groups/{groupId}/apikeys/{clientId} | Delete an api key |
| GET | /api/groups/{groupId}/apikeys | Get all api keys for the group of a service |
| POST | /api/groups/{groupId}/apikeys | Create a new api key for a group |
| GET | /api/apikeys | Get all api keys |
| GET | /api/services/{serviceId}/template | Get a service descriptor error template |
| PUT | /api/services/{serviceId}/template | Update an error template to a service descriptor |
| POST | /api/services/{serviceId}/template | Create a service descriptor error template |
| DELETE | /api/services/{serviceId}/template | Delete a service descriptor error template |
| GET | /api/services/{serviceId}/targets | Get a service descriptor targets |
| POST | /api/services/{serviceId}/targets | Add a target to a service descriptor |
| PATCH | /api/services/{serviceId}/targets | Update a service descriptor targets |
| DELETE | /api/services/{serviceId}/targets | Delete a service descriptor target |
| GET | /api/services/{serviceId} | Get a service descriptor |
| PUT | /api/services/{serviceId} | Update a service descriptor |
| PATCH | /api/services/{serviceId} | Update a service descriptor with a diff |
| DELETE | /api/services/{serviceId} | Delete a service descriptor |
| GET | /api/services | Get all services |
| POST | /api/services | Create a new service descriptor |
| GET | /api/groups/{serviceGroupId}/services | Get all services descriptor for a group |
| GET | /api/groups/{serviceGroupId} | Get a service group |
| PUT | /api/groups/{serviceGroupId} | Update a service group |
| PATCH | /api/groups/{serviceGroupId} | Update a service group with a diff |
| DELETE | /api/groups/{serviceGroupId} | Delete a service group |
| GET | /api/groups | Get all service groups |
| POST | /api/groups | Create a new service group |
| GET | /api/verifiers | Get all global JWT verifiers |
| POST | /api/verifiers | Create one global JWT verifiers |
| GET | /api/verifiers/{verifierId} | Get one global JWT verifiers |
| DELETE | /api/verifiers/{verifierId} | Delete one global JWT verifiers |
| PUT | /api/verifiers/{verifierId} | Update one global JWT verifiers |
| PATCH | /api/verifiers/{verifierId} | Update one global JWT verifiers |
| GET | /api/auths | Get all global auth. module configs |
| POST | /api/auths | Create one global auth. module config |
| GET | /api/auths/{id} | Get one global auth. module configs |
| DELETE | /api/auths/{id} | Delete one global auth. module config |
| PUT | /api/auths/{id} | Update one global auth. module config |
| PATCH | /api/auths/{id} | Update one global auth. module config |
| POST | /api/scripts/_compile | Compile a script |
| GET | /api/scripts/{scriptId} | Get a script |
| PUT | /api/scripts/{scriptId} | Update a script |
| PATCH | /api/scripts/{scriptId} | Update a script with a diff |
| DELETE | /api/scripts/{scriptId} | Delete a script |
| GET | /api/scripts | Get all scripts |
| POST | /api/scripts | Create a new script |
| GET | /api/data-exporter-configs/_template | Get all data exporter configs |
| POST | /api/data-exporter-configs/_bulk | Create a new data exporter configs |
| PUT | /api/data-exporter-configs/_bulk | Update a data exporter configs |
| PATCH | /api/data-exporter-configs/_bulk | Update a data exporter configs with a diff |
| DELETE | /api/data-exporter-configs/_bulk | Delete a data exporter config |
| GET | /api/data-exporter-configs/{dataExporterConfigId} | Get a data exporter config |
| PUT | /api/data-exporter-configs/{dataExporterConfigId} | Update a data exporter config |
| PATCH | /api/data-exporter-configs/{dataExporterConfigId} | Update a data exporter config with a diff |
| DELETE | /api/data-exporter-configs/{dataExporterConfigId} | Delete a data exporter config |
| GET | /api/data-exporter-configs | Get all data exporter configs |
| POST | /api/data-exporter-configs | Create a new data exporter config |
| GET | /api/certificates | Get all certificates |
| POST | /api/certificates | Create one certificate |
| GET | /api/certificates/{id} | Get one certificate by id |
| DELETE | /api/certificates/{id} | Delete one certificate by id |
| PUT | /api/certificates/{id} | Update one certificate by id |
| PATCH | /api/certificates/{id} | Update one certificate by id |
| GET | /api/client-validators | Get all validation authoritiess |
| POST | /api/client-validators | Create one validation authorities |
| GET | /api/client-validators/{id} | Get one validation authorities by id |
| DELETE | /api/client-validators/{id} | Delete one validation authorities by id |
| PUT | /api/client-validators/{id} | Update one validation authorities by id |
| PATCH | /api/client-validators/{id} | Update one validation authorities by id |
| GET | /api/snowmonkey/config | Get current Snow Monkey config |
| PUT | /api/snowmonkey/config | Update current Snow Monkey config |
| PATCH | /api/snowmonkey/config | Update current Snow Monkey config |
| GET | /api/snowmonkey/outages | Get all current Snow Monkey ourages |
| DELETE | /api/snowmonkey/outages | Reset Snow Monkey Outages for the day |
| POST | /api/snowmonkey/_start | Start the Snow Monkey |
| POST | /api/snowmonkey/_stop | Stop the Snow Monkey |
| GET | /api/live/{id} | Get live feed of otoroshi stats |
| GET | /api/live | Get global otoroshi stats |
| GET | /api/globalconfig | Get the full configuration of Otoroshi |
| PUT | /api/globalconfig | Update the global configuration |
| PATCH | /api/globalconfig | Update the global configuration with a diff |
| GET | /api/otoroshi.json | Export the full state of Otoroshi |
| POST | /api/otoroshi.json | Import the full state of Otoroshi |
| POST | /api/import | Import the full state of Otoroshi as a file |

### health
| Method | Path | Description |
|--------|------|-------------|
| GET | /health | Return current Otoroshi health |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all apikey?" -> GET /new/apikey
- "List all service?" -> GET /new/service
- "List all group?" -> GET /new/group
- "List all lines?" -> GET /lines
- "List all services?" -> GET /lines/{line}/services
- "List all quotas?" -> GET /api/services/{serviceId}/apikeys/{clientId}/quotas
- "List all group?" -> GET /api/services/{serviceId}/apikeys/{clientId}/group
- "Get apikey details?" -> GET /api/services/{serviceId}/apikeys/{clientId}
- "Update a apikey?" -> PUT /api/services/{serviceId}/apikeys/{clientId}
- "Partially update a apikey?" -> PATCH /api/services/{serviceId}/apikeys/{clientId}
- "Delete a apikey?" -> DELETE /api/services/{serviceId}/apikeys/{clientId}
- "List all apikeys?" -> GET /api/services/{serviceId}/apikeys
- "Create a apikey?" -> POST /api/services/{serviceId}/apikeys
- "List all quotas?" -> GET /api/groups/{groupId}/apikeys/{clientId}/quotas
- "Get apikey details?" -> GET /api/groups/{groupId}/apikeys/{clientId}
- "Update a apikey?" -> PUT /api/groups/{groupId}/apikeys/{clientId}
- "Partially update a apikey?" -> PATCH /api/groups/{groupId}/apikeys/{clientId}
- "Delete a apikey?" -> DELETE /api/groups/{groupId}/apikeys/{clientId}
- "List all apikeys?" -> GET /api/groups/{groupId}/apikeys
- "Create a apikey?" -> POST /api/groups/{groupId}/apikeys
- "List all apikeys?" -> GET /api/apikeys
- "List all template?" -> GET /api/services/{serviceId}/template
- "Create a template?" -> POST /api/services/{serviceId}/template
- "List all targets?" -> GET /api/services/{serviceId}/targets
- "Create a target?" -> POST /api/services/{serviceId}/targets
- "Get service details?" -> GET /api/services/{serviceId}
- "Update a service?" -> PUT /api/services/{serviceId}
- "Partially update a service?" -> PATCH /api/services/{serviceId}
- "Delete a service?" -> DELETE /api/services/{serviceId}
- "List all services?" -> GET /api/services
- "Create a service?" -> POST /api/services
- "List all services?" -> GET /api/groups/{serviceGroupId}/services
- "Get group details?" -> GET /api/groups/{serviceGroupId}
- "Update a group?" -> PUT /api/groups/{serviceGroupId}
- "Partially update a group?" -> PATCH /api/groups/{serviceGroupId}
- "Delete a group?" -> DELETE /api/groups/{serviceGroupId}
- "List all groups?" -> GET /api/groups
- "Create a group?" -> POST /api/groups
- "List all verifiers?" -> GET /api/verifiers
- "Create a verifier?" -> POST /api/verifiers
- "Get verifier details?" -> GET /api/verifiers/{verifierId}
- "Delete a verifier?" -> DELETE /api/verifiers/{verifierId}
- "Update a verifier?" -> PUT /api/verifiers/{verifierId}
- "Partially update a verifier?" -> PATCH /api/verifiers/{verifierId}
- "List all auths?" -> GET /api/auths
- "Create a auth?" -> POST /api/auths
- "Get auth details?" -> GET /api/auths/{id}
- "Delete a auth?" -> DELETE /api/auths/{id}
- "Update a auth?" -> PUT /api/auths/{id}
- "Partially update a auth?" -> PATCH /api/auths/{id}
- "Create a _compile?" -> POST /api/scripts/_compile
- "Get script details?" -> GET /api/scripts/{scriptId}
- "Update a script?" -> PUT /api/scripts/{scriptId}
- "Partially update a script?" -> PATCH /api/scripts/{scriptId}
- "Delete a script?" -> DELETE /api/scripts/{scriptId}
- "List all scripts?" -> GET /api/scripts
- "Create a script?" -> POST /api/scripts
- "List all _template?" -> GET /api/data-exporter-configs/_template
- "Create a _bulk?" -> POST /api/data-exporter-configs/_bulk
- "Get data-exporter-config details?" -> GET /api/data-exporter-configs/{dataExporterConfigId}
- "Update a data-exporter-config?" -> PUT /api/data-exporter-configs/{dataExporterConfigId}
- "Partially update a data-exporter-config?" -> PATCH /api/data-exporter-configs/{dataExporterConfigId}
- "Delete a data-exporter-config?" -> DELETE /api/data-exporter-configs/{dataExporterConfigId}
- "List all data-exporter-configs?" -> GET /api/data-exporter-configs
- "Create a data-exporter-config?" -> POST /api/data-exporter-configs
- "List all certificates?" -> GET /api/certificates
- "Create a certificate?" -> POST /api/certificates
- "Get certificate details?" -> GET /api/certificates/{id}
- "Delete a certificate?" -> DELETE /api/certificates/{id}
- "Update a certificate?" -> PUT /api/certificates/{id}
- "Partially update a certificate?" -> PATCH /api/certificates/{id}
- "List all client-validators?" -> GET /api/client-validators
- "Create a client-validator?" -> POST /api/client-validators
- "Get client-validator details?" -> GET /api/client-validators/{id}
- "Delete a client-validator?" -> DELETE /api/client-validators/{id}
- "Update a client-validator?" -> PUT /api/client-validators/{id}
- "Partially update a client-validator?" -> PATCH /api/client-validators/{id}
- "List all config?" -> GET /api/snowmonkey/config
- "List all outages?" -> GET /api/snowmonkey/outages
- "Create a _start?" -> POST /api/snowmonkey/_start
- "Create a _stop?" -> POST /api/snowmonkey/_stop
- "Get live details?" -> GET /api/live/{id}
- "List all live?" -> GET /api/live
- "List all globalconfig?" -> GET /api/globalconfig
- "List all otoroshi.json?" -> GET /api/otoroshi.json
- "Create a otoroshi.json?" -> POST /api/otoroshi.json
- "Create a import?" -> POST /api/import
- "List all health?" -> GET /health
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
