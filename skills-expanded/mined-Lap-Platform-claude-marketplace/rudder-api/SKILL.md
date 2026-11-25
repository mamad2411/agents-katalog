---
name: rudder-api
description: "Rudder API skill. Use when working with Rudder for api, apiaccounts, archives. Covers 176 endpoints."
version: 1.0.0
generator: lapsh
---

# Rudder API
API version: 22

## Auth
ApiKey X-API-Token in header

## Base URL
https://{rudderServer}/rudder/api/latest

## Setup
1. Set your API key in the appropriate header
2. GET /api/changeRequests -- verify access
3. POST /apiaccounts -- create first apiaccounts

## Endpoints

176 endpoints across 31 groups. See references/api-spec.lap for full details.

### api
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/changeRequests | List all change requests |

### apiaccounts
| Method | Path | Description |
|--------|------|-------------|
| GET | /apiaccounts | List all API accounts |
| POST | /apiaccounts | Create an API account |
| GET | /apiaccounts/${apiAccountId} | Get an API account details |
| DELETE | /apiaccounts/${apiAccountId} | Delete an API account |
| POST | /apiaccounts/${apiAccountId} | Update an API account details |
| POST | /apiaccounts/${apiAccountId}/regenerate | Regenerate the token of an API account |
| GET | /apiaccounts/token | Get API account for the currently identified token |

### archives
| Method | Path | Description |
|--------|------|-------------|
| GET | /archives/export | Get a ZIP archive of the requested items and their dependencies |
| POST | /archives/import | Import a ZIP archive of policies into Rudder |

### branding
| Method | Path | Description |
|--------|------|-------------|
| GET | /branding | Get branding configuration |
| POST | /branding | Update web interface customization |
| POST | /branding/reload | Reload branding file |

### campaigns
| Method | Path | Description |
|--------|------|-------------|
| GET | /campaigns | Get all campaigns details |
| POST | /campaigns | Save a campaign |
| GET | /campaigns/events | Get all campaign events |
| GET | /campaigns/events/{id} | Get a campaign event details |
| POST | /campaigns/events/{id} | Update an existing event |
| DELETE | /campaigns/events/{id} | Delete a campaign event details |
| GET | /campaigns/{id} | Get a campaign details |
| DELETE | /campaigns/{id} | Delete a campaign |
| GET | /campaigns/{id}/events | Get campaign events for a campaign |
| POST | /campaigns/{id}/schedule | Schedule a campaign event for a campaign |

### changeRequests
| Method | Path | Description |
|--------|------|-------------|
| GET | /changeRequests/{changeRequestId} | Get a change request details |
| DELETE | /changeRequests/{changeRequestId} | Decline a request details |
| POST | /changeRequests/{changeRequestId} | Update a request details |
| POST | /changeRequests/{changeRequestId}/accept | Accept a request details |

### compliance
| Method | Path | Description |
|--------|------|-------------|
| GET | /compliance | Global compliance |
| GET | /compliance/directives | Compliance details for all directives |
| GET | /compliance/directives/{directiveId} | Compliance details by directive |
| GET | /compliance/groups/{targetOrNodeGroupId} | Compliance details by group (global) |
| GET | /compliance/groups/{targetOrNodeGroupId}/target | Compliance details by group (targeted) |
| GET | /compliance/nodes | Compliance details for all nodes |
| GET | /compliance/nodes/{nodeId} | Compliance details by node |
| GET | /compliance/rules | Compliance details for all rules |
| GET | /compliance/rules/{ruleId} | Compliance details by rule |

### cve
| Method | Path | Description |
|--------|------|-------------|
| GET | /cve | Get all CVE details |
| POST | /cve/check | Trigger a CVE check |
| GET | /cve/check/config | Get CVE check config |
| POST | /cve/check/config | Update cve check config |
| GET | /cve/check/last | Get last CVE check result |
| POST | /cve/list | Get a list of CVE details |
| POST | /cve/update | Update CVE database from remote source |
| POST | /cve/update/fs | Update CVE database from file system |
| GET | /cve/{cveId} | Get a CVE details |

### datasources
| Method | Path | Description |
|--------|------|-------------|
| GET | /datasources | List all data sources |
| PUT | /datasources | Create a data source |
| POST | /datasources/reload | Update properties from data sources |
| POST | /datasources/reload/{datasourceId} | Update properties from data sources |
| GET | /datasources/{datasourceId} | Get data source configuration |
| POST | /datasources/{datasourceId} | Update a data source configuration |
| DELETE | /datasources/{datasourceId} | Delete a data source |

### directives
| Method | Path | Description |
|--------|------|-------------|
| GET | /directives | List all directives |
| PUT | /directives | Create a directive |
| GET | /directives/tree | Get directive tree |
| GET | /directives/{directiveId} | Get directive details |
| DELETE | /directives/{directiveId} | Delete a directive |
| POST | /directives/{directiveId} | Update a directive details |
| POST | /directives/{directiveId}/check | Check that update on a directive is valid |

### groups
| Method | Path | Description |
|--------|------|-------------|
| GET | /groups | List all groups |
| PUT | /groups | Create a group |
| PUT | /groups/categories | Create a group category |
| GET | /groups/categories/{groupCategoryId} | Get group category details |
| DELETE | /groups/categories/{groupCategoryId} | Delete group category |
| POST | /groups/categories/{groupCategoryId} | Update group category details |
| GET | /groups/tree | Get groups tree |
| GET | /groups/{groupId} | Get group details |
| POST | /groups/{groupId} | Update group details |
| DELETE | /groups/{groupId} | Delete a group |
| POST | /groups/{groupId}/reload | Reload a group |

### info
| Method | Path | Description |
|--------|------|-------------|
| GET | /info | List all endpoints |
| GET | /info/details/{endpointName} | Get information about one API endpoint |
| GET | /info/{sectionId} | Get information on endpoint in a section |

### inventories
| Method | Path | Description |
|--------|------|-------------|
| POST | /inventories/upload | Upload an inventory for processing |
| POST | /inventories/watcher/restart | Restart inventory watcher |
| POST | /inventories/watcher/start | Start inventory watcher |
| POST | /inventories/watcher/stop | Stop inventory watcher |

### methods
| Method | Path | Description |
|--------|------|-------------|
| GET | /methods | List methods |
| POST | /methods/reload | Reload methods |

### nodes
| Method | Path | Description |
|--------|------|-------------|
| GET | /nodes | List managed nodes |
| PUT | /nodes | Create one or several new nodes |
| POST | /nodes/applyPolicy | Trigger an agent run on all nodes |
| GET | /nodes/pending | List pending nodes |
| POST | /nodes/pending | Update pending nodes status |
| POST | /nodes/pending/{nodeId} | Update pending node status |
| GET | /nodes/status | Get nodes acceptation status |
| GET | /nodes/{nodeId} | Get information about a node |
| POST | /nodes/{nodeId} | Update node settings and properties |
| DELETE | /nodes/{nodeId} | Delete a node |
| POST | /nodes/{nodeId}/applyPolicy | Trigger an agent run |
| POST | /nodes/{nodeId}/fetchData | Update properties for one node from all data sources |
| POST | /nodes/{nodeId}/fetchData/{datasourceId} | Update properties for one node from a data source |
| GET | /nodes/{nodeId}/inheritedProperties | Get inherited node properties for a node |

### openscap
| Method | Path | Description |
|--------|------|-------------|
| GET | /openscap/report/{nodeId} | Get an OpenSCAP report |

### parameters
| Method | Path | Description |
|--------|------|-------------|
| GET | /parameters | List all global properties |
| PUT | /parameters | Create a new property |
| GET | /parameters/{parameterId} | Get the value of a global property |
| POST | /parameters/{parameterId} | Update a global property's value |
| DELETE | /parameters/{parameterId} | Delete a global parameter |

### plugins
| Method | Path | Description |
|--------|------|-------------|
| GET | /plugins/info | Information about installed plugins |
| GET | /plugins/settings | Get plugins repository settings |
| POST | /plugins/settings | Update plugins settings |

### rules
| Method | Path | Description |
|--------|------|-------------|
| GET | /rules | List all rules |
| PUT | /rules | Create a rule |
| PUT | /rules/categories | Create a rule category |
| GET | /rules/categories/{ruleCategoryId} | Get rule category details |
| DELETE | /rules/categories/{ruleCategoryId} | Delete group category |
| POST | /rules/categories/{ruleCategoryId} | Update rule category details |
| GET | /rules/tree | Get rules tree |
| GET | /rules/{ruleId} | Get a rule details |
| POST | /rules/{ruleId} | Update a rule details |
| DELETE | /rules/{ruleId} | Delete a rule |

### scaleoutrelay
| Method | Path | Description |
|--------|------|-------------|
| POST | /scaleoutrelay/demote/{nodeId} | Demote a relay to simple node |
| POST | /scaleoutrelay/promote/{nodeId} | Promote a node to relay |

### secret
| Method | Path | Description |
|--------|------|-------------|
| GET | /secret | List all secrets |
| POST | /secret | Update a secret |
| PUT | /secret | Create a secret |
| GET | /secret/{name} | Get one secret |
| DELETE | /secret/{name} | Delete a secret |

### securitytags
| Method | Path | Description |
|--------|------|-------------|
| POST | /securitytags/nodes | Define a tenant on nodes |
| DELETE | /securitytags/nodes | Remove tenant value on nodes |

### settings
| Method | Path | Description |
|--------|------|-------------|
| GET | /settings | List all settings |
| GET | /settings/allowed_networks/{nodeId} | Get allowed networks for a policy server |
| POST | /settings/allowed_networks/{nodeId} | Set allowed networks for a policy server |
| POST | /settings/allowed_networks/{nodeId}/diff | Modify allowed networks for a policy server |
| GET | /settings/{settingId} | Get the value of a setting |
| POST | /settings/{settingId} | Set the value of a setting |

### status
| Method | Path | Description |
|--------|------|-------------|
| GET | /status | Check if Rudder is alive |

### system
| Method | Path | Description |
|--------|------|-------------|
| GET | /system/archives/{archiveKind} | List archives |
| POST | /system/archives/{archiveKind} | Create an archive |
| POST | /system/archives/{archiveKind}/restore/{archiveRestoreKind} | Restore an archive |
| GET | /system/archives/{archiveKind}/zip/{commitId} | Get an archive as a ZIP |
| GET | /system/healthcheck | Get healthcheck |
| GET | /system/info | Get server information |
| POST | /system/maintenance/purgeSoftware | Trigger batch for cleaning unreferenced software |
| POST | /system/regenerate/policies | Trigger a new policy generation |
| POST | /system/reload | Reload both techniques and dynamic groups |
| POST | /system/reload/groups | Reload dynamic groups |
| POST | /system/reload/techniques | Reload techniques |
| GET | /system/status | Get server status |
| POST | /system/update/policies | Trigger update of policies |

### systemUpdate
| Method | Path | Description |
|--------|------|-------------|
| GET | /systemUpdate/campaign/{id}/history | Get a campaign result history |
| GET | /systemUpdate/events/{id}/report | Get report of campaign |
| GET | /systemUpdate/events/{id}/result | Get a campaign event result |
| GET | /systemUpdate/events/{id}/result/{nodeId} | Get detailed campaign event result for a Node |
| GET | /systemUpdate/events/{id}/summaryReport | Get summary report of campaign |

### techniques
| Method | Path | Description |
|--------|------|-------------|
| GET | /techniques | List all techniques |
| PUT | /techniques | Create technique |
| GET | /techniques/categories | List categories |
| POST | /techniques/reload | Reload techniques |
| GET | /techniques/versions | List versions |
| GET | /techniques/{techniqueId} | Technique metadata by ID |
| GET | /techniques/{techniqueId}/directives | List all directives based on a technique |
| POST | /techniques/{techniqueId}/{techniqueVersion} | Update technique |
| DELETE | /techniques/{techniqueId}/{techniqueVersion} | Delete technique |
| GET | /techniques/{techniqueId}/{techniqueVersion} | Technique metadata by version and ID |
| GET | /techniques/{techniqueId}/{techniqueVersion}/directives | List all directives based on a version of a technique |
| GET | /techniques/{techniqueId}/{techniqueVersion}/resources | Technique's resources |
| GET | /techniques/{techniqueId}/{techniqueVersion}/revisions | Technique's revisions |

### tenants
| Method | Path | Description |
|--------|------|-------------|
| GET | /tenants | Get the list of all tenants. |
| POST | /tenants | Add one or more tenants |
| DELETE | /tenants | Delete a list of tenants |
| GET | /tenants/{id} | Get tenant details |

### usermanagement
| Method | Path | Description |
|--------|------|-------------|
| POST | /usermanagement | Add user |
| POST | /usermanagement/coverage/{username} | Compute the role coverage |
| GET | /usermanagement/roles | List all roles |
| PUT | /usermanagement/status/activate/{username} | Activate user |
| PUT | /usermanagement/status/disable/{username} | Disable user |
| POST | /usermanagement/update/info/{username} | Update user information |
| POST | /usermanagement/update/{username} | Update user access to Rudder |
| GET | /usermanagement/users | List all users |
| POST | /usermanagement/users/reload | Reload users |
| DELETE | /usermanagement/{username} | Delete an user |

### users
| Method | Path | Description |
|--------|------|-------------|
| GET | /users | List user |

### validatedUsers
| Method | Path | Description |
|--------|------|-------------|
| POST | /validatedUsers | Update validated user list |
| DELETE | /validatedUsers/{username} | Remove an user from validated user list |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all changeRequests?" -> GET /api/changeRequests
- "List all apiaccounts?" -> GET /apiaccounts
- "Create a apiaccount?" -> POST /apiaccounts
- "Get ${apiAccountId} details?" -> GET /apiaccounts/${apiAccountId}
- "Delete a ${apiAccountId}?" -> DELETE /apiaccounts/${apiAccountId}
- "Create a regenerate?" -> POST /apiaccounts/${apiAccountId}/regenerate
- "List all token?" -> GET /apiaccounts/token
- "List all export?" -> GET /archives/export
- "Create a import?" -> POST /archives/import
- "List all branding?" -> GET /branding
- "Create a branding?" -> POST /branding
- "Create a reload?" -> POST /branding/reload
- "List all campaigns?" -> GET /campaigns
- "Create a campaign?" -> POST /campaigns
- "List all events?" -> GET /campaigns/events
- "Get event details?" -> GET /campaigns/events/{id}
- "Delete a event?" -> DELETE /campaigns/events/{id}
- "Get campaign details?" -> GET /campaigns/{id}
- "Delete a campaign?" -> DELETE /campaigns/{id}
- "List all events?" -> GET /campaigns/{id}/events
- "Create a schedule?" -> POST /campaigns/{id}/schedule
- "Get changeRequest details?" -> GET /changeRequests/{changeRequestId}
- "Delete a changeRequest?" -> DELETE /changeRequests/{changeRequestId}
- "Create a accept?" -> POST /changeRequests/{changeRequestId}/accept
- "List all compliance?" -> GET /compliance
- "List all directives?" -> GET /compliance/directives
- "Get directive details?" -> GET /compliance/directives/{directiveId}
- "Get group details?" -> GET /compliance/groups/{targetOrNodeGroupId}
- "List all target?" -> GET /compliance/groups/{targetOrNodeGroupId}/target
- "List all nodes?" -> GET /compliance/nodes
- "Get node details?" -> GET /compliance/nodes/{nodeId}
- "List all rules?" -> GET /compliance/rules
- "Get rule details?" -> GET /compliance/rules/{ruleId}
- "List all cve?" -> GET /cve
- "Create a check?" -> POST /cve/check
- "List all config?" -> GET /cve/check/config
- "Create a config?" -> POST /cve/check/config
- "List all last?" -> GET /cve/check/last
- "Create a list?" -> POST /cve/list
- "Create a update?" -> POST /cve/update
- "Create a f?" -> POST /cve/update/fs
- "Get cve details?" -> GET /cve/{cveId}
- "List all datasources?" -> GET /datasources
- "Create a reload?" -> POST /datasources/reload
- "Get datasource details?" -> GET /datasources/{datasourceId}
- "Delete a datasource?" -> DELETE /datasources/{datasourceId}
- "List all directives?" -> GET /directives
- "List all tree?" -> GET /directives/tree
- "Get directive details?" -> GET /directives/{directiveId}
- "Delete a directive?" -> DELETE /directives/{directiveId}
- "Create a check?" -> POST /directives/{directiveId}/check
- "List all groups?" -> GET /groups
- "Get category details?" -> GET /groups/categories/{groupCategoryId}
- "Delete a category?" -> DELETE /groups/categories/{groupCategoryId}
- "List all tree?" -> GET /groups/tree
- "Get group details?" -> GET /groups/{groupId}
- "Delete a group?" -> DELETE /groups/{groupId}
- "Create a reload?" -> POST /groups/{groupId}/reload
- "List all info?" -> GET /info
- "Get detail details?" -> GET /info/details/{endpointName}
- "Get info details?" -> GET /info/{sectionId}
- "Create a upload?" -> POST /inventories/upload
- "Create a restart?" -> POST /inventories/watcher/restart
- "Create a start?" -> POST /inventories/watcher/start
- "Create a stop?" -> POST /inventories/watcher/stop
- "List all methods?" -> GET /methods
- "Create a reload?" -> POST /methods/reload
- "Search nodes?" -> GET /nodes
- "Create a applyPolicy?" -> POST /nodes/applyPolicy
- "Search pending?" -> GET /nodes/pending
- "Create a pending?" -> POST /nodes/pending
- "List all status?" -> GET /nodes/status
- "Get node details?" -> GET /nodes/{nodeId}
- "Delete a node?" -> DELETE /nodes/{nodeId}
- "Create a applyPolicy?" -> POST /nodes/{nodeId}/applyPolicy
- "Create a fetchData?" -> POST /nodes/{nodeId}/fetchData
- "List all inheritedProperties?" -> GET /nodes/{nodeId}/inheritedProperties
- "Get report details?" -> GET /openscap/report/{nodeId}
- "List all parameters?" -> GET /parameters
- "Get parameter details?" -> GET /parameters/{parameterId}
- "Delete a parameter?" -> DELETE /parameters/{parameterId}
- "List all info?" -> GET /plugins/info
- "List all settings?" -> GET /plugins/settings
- "Create a setting?" -> POST /plugins/settings
- "List all rules?" -> GET /rules
- "Get category details?" -> GET /rules/categories/{ruleCategoryId}
- "Delete a category?" -> DELETE /rules/categories/{ruleCategoryId}
- "List all tree?" -> GET /rules/tree
- "Get rule details?" -> GET /rules/{ruleId}
- "Delete a rule?" -> DELETE /rules/{ruleId}
- "List all secret?" -> GET /secret
- "Create a secret?" -> POST /secret
- "Get secret details?" -> GET /secret/{name}
- "Delete a secret?" -> DELETE /secret/{name}
- "Create a node?" -> POST /securitytags/nodes
- "List all settings?" -> GET /settings
- "Get allowed_network details?" -> GET /settings/allowed_networks/{nodeId}
- "Create a diff?" -> POST /settings/allowed_networks/{nodeId}/diff
- "Get setting details?" -> GET /settings/{settingId}
- "List all status?" -> GET /status
- "Get archive details?" -> GET /system/archives/{archiveKind}
- "Get zip details?" -> GET /system/archives/{archiveKind}/zip/{commitId}
- "List all healthcheck?" -> GET /system/healthcheck
- "List all info?" -> GET /system/info
- "Create a purgeSoftware?" -> POST /system/maintenance/purgeSoftware
- "Create a policy?" -> POST /system/regenerate/policies
- "Create a reload?" -> POST /system/reload
- "Create a group?" -> POST /system/reload/groups
- "Create a technique?" -> POST /system/reload/techniques
- "List all status?" -> GET /system/status
- "Create a policy?" -> POST /system/update/policies
- "List all history?" -> GET /systemUpdate/campaign/{id}/history
- "List all report?" -> GET /systemUpdate/events/{id}/report
- "List all result?" -> GET /systemUpdate/events/{id}/result
- "Get result details?" -> GET /systemUpdate/events/{id}/result/{nodeId}
- "List all summaryReport?" -> GET /systemUpdate/events/{id}/summaryReport
- "List all techniques?" -> GET /techniques
- "List all categories?" -> GET /techniques/categories
- "Create a reload?" -> POST /techniques/reload
- "List all versions?" -> GET /techniques/versions
- "Get technique details?" -> GET /techniques/{techniqueId}
- "List all directives?" -> GET /techniques/{techniqueId}/directives
- "Delete a technique?" -> DELETE /techniques/{techniqueId}/{techniqueVersion}
- "Get technique details?" -> GET /techniques/{techniqueId}/{techniqueVersion}
- "List all directives?" -> GET /techniques/{techniqueId}/{techniqueVersion}/directives
- "List all resources?" -> GET /techniques/{techniqueId}/{techniqueVersion}/resources
- "List all revisions?" -> GET /techniques/{techniqueId}/{techniqueVersion}/revisions
- "List all tenants?" -> GET /tenants
- "Create a tenant?" -> POST /tenants
- "Get tenant details?" -> GET /tenants/{id}
- "Create a usermanagement?" -> POST /usermanagement
- "List all roles?" -> GET /usermanagement/roles
- "Update a activate?" -> PUT /usermanagement/status/activate/{username}
- "Update a disable?" -> PUT /usermanagement/status/disable/{username}
- "List all users?" -> GET /usermanagement/users
- "Create a reload?" -> POST /usermanagement/users/reload
- "Delete a usermanagement?" -> DELETE /usermanagement/{username}
- "List all users?" -> GET /users
- "Create a validatedUser?" -> POST /validatedUsers
- "Delete a validatedUser?" -> DELETE /validatedUsers/{username}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
