---
name: insightappsec-api
description: "InsightAppSec API skill. Use when working with InsightAppSec for apps, attack-templates, blackouts. Covers 102 endpoints."
version: 1.0.0
generator: lapsh
---

# InsightAppSec API
API version: v1

## Auth
ApiKey (inferred from docs)

## Base URL
https://[region].api.insight.rapid7.com/ias/v1

## Setup
1. Set your API key in the appropriate header
2. GET /apps -- verify access
3. POST /apps -- create first apps

## Endpoints

102 endpoints across 14 groups. See references/api-spec.lap for full details.

### apps
| Method | Path | Description |
|--------|------|-------------|
| GET | /apps | Get Apps |
| POST | /apps | Create App |
| GET | /apps/{app-id} | Get App |
| PUT | /apps/{app-id} | Update App |
| DELETE | /apps/{app-id} | Delete App |
| GET | /apps/{app-id}/files | Get Files |
| POST | /apps/{app-id}/files | Create File |
| GET | /apps/{app-id}/files/{file-id} | Get File |
| PUT | /apps/{app-id}/files/{file-id} | Update File |
| POST | /apps/{app-id}/files/{file-id} | Upload File Content |
| DELETE | /apps/{app-id}/files/{file-id} | Delete File |
| GET | /apps/{app-id}/tags | Get App Tags |
| POST | /apps/{app-id}/tags | Add App Tag |
| DELETE | /apps/{app-id}/tags/{tag-id} | Remove App Tag |
| GET | /apps/{app-id}/users | Get App Users |
| POST | /apps/{app-id}/users | Add App User |
| DELETE | /apps/{app-id}/users/{user-id} | Remove App User |

### attack-templates
| Method | Path | Description |
|--------|------|-------------|
| GET | /attack-templates | Get Attack Templates |
| POST | /attack-templates | Create Attack Template |
| GET | /attack-templates/module-configs | Get Attack Modules Configs |
| GET | /attack-templates/{attack-template-id} | Get Attack Template |
| PUT | /attack-templates/{attack-template-id} | Update Attack Template |
| DELETE | /attack-templates/{attack-template-id} | Delete Attack Template |
| GET | /attack-templates/{attack-template-id}/modules | Get Attack Modules |
| POST | /attack-templates/{attack-template-id}/modules | Create Attack Module |
| PUT | /attack-templates/{attack-template-id}/modules/{attack-module-id} | Update Attack Module |
| DELETE | /attack-templates/{attack-template-id}/modules/{attack-module-id} | Delete Attack Module |

### blackouts
| Method | Path | Description |
|--------|------|-------------|
| GET | /blackouts | Get Blackouts |
| POST | /blackouts | Create Blackout |
| GET | /blackouts/{blackout-id} | Get Blackout |
| PUT | /blackouts/{blackout-id} | Update Blackout |
| DELETE | /blackouts/{blackout-id} | Delete Blackout |

### engine-groups
| Method | Path | Description |
|--------|------|-------------|
| GET | /engine-groups | Get Engine Groups |
| POST | /engine-groups | Create Engine Group |
| GET | /engine-groups/{engine-group-id} | Get Engine Group |
| PUT | /engine-groups/{engine-group-id} | Update Engine Group |
| DELETE | /engine-groups/{engine-group-id} | Delete Engine Group |
| GET | /engine-groups/{engine-group-id}/engines | Get Engine Group Engines |

### engines
| Method | Path | Description |
|--------|------|-------------|
| GET | /engines | Get Engines |
| POST | /engines | Create Engine |
| GET | /engines/{engine-id} | Get Engine |
| PUT | /engines/{engine-id} | Update Engine |
| DELETE | /engines/{engine-id} | Delete Engine |
| GET | /engines/{engine-id}/credential | Get Engine Credential |
| PUT | /engines/{engine-id}/credential | Regenerate Engine Credential |
| DELETE | /engines/{engine-id}/credential | Delete Engine Credential |
| POST | /engines/{engine-id}/upgrade | Upgrade Engine |

### modules
| Method | Path | Description |
|--------|------|-------------|
| GET | /modules | Get Modules |
| GET | /modules/{module-id} | Get Module |
| GET | /modules/{module-id}/attacks/{attack-id} | Get Attack |
| GET | /modules/{module-id}/attacks/{attack-id}/documentation | Get Attack Documentation |

### reports
| Method | Path | Description |
|--------|------|-------------|
| GET | /reports | Get Reports |
| POST | /reports | Generate Report |
| GET | /reports/{report-id} | Get Report |
| DELETE | /reports/{report-id} | Delete Report |

### scan-configs
| Method | Path | Description |
|--------|------|-------------|
| GET | /scan-configs | Get Scan Configs |
| POST | /scan-configs | Create Scan Config |
| GET | /scan-configs/options/default | Get Scan Configs Options Default |
| GET | /scan-configs/{scan-config-id} | Get Scan Config |
| PUT | /scan-configs/{scan-config-id} | Update Scan Config |
| DELETE | /scan-configs/{scan-config-id} | Delete Scan Config |
| GET | /scan-configs/{scan-config-id}/options | Get Scan Config Options |
| PUT | /scan-configs/{scan-config-id}/options | Update Scan Config Options |
| PATCH | /scan-configs/{scan-config-id}/options | Patch Scan Config Options |

### scans
| Method | Path | Description |
|--------|------|-------------|
| GET | /scans | Get Scans |
| POST | /scans | Submit Scan |
| GET | /scans/{scan-id} | Get Scan |
| DELETE | /scans/{scan-id} | Delete Scan |
| GET | /scans/{scan-id}/action | Get Scan Action |
| PUT | /scans/{scan-id}/action | Submit Scan Action |
| GET | /scans/{scan-id}/engine-events | Get Scan Engine Events |
| GET | /scans/{scan-id}/execution-details | Get Scan Execution Details |
| GET | /scans/{scan-id}/platform-events | Get Scan Platform Events |

### schedules
| Method | Path | Description |
|--------|------|-------------|
| GET | /schedules | Get Schedules |
| POST | /schedules | Create Schedule |
| GET | /schedules/{schedule-id} | Get Schedule |
| PUT | /schedules/{schedule-id} | Update Schedule |
| DELETE | /schedules/{schedule-id} | Delete Schedule |

### search
| Method | Path | Description |
|--------|------|-------------|
| POST | /search | Perform Search |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags | Get Tags |
| POST | /tags | Create Tag |
| GET | /tags/{tag-id} | Get Tag |
| PUT | /tags/{tag-id} | Update Tag |
| DELETE | /tags/{tag-id} | Delete Tag |

### targets
| Method | Path | Description |
|--------|------|-------------|
| GET | /targets | Get Targets |
| POST | /targets | Create Target |
| GET | /targets/{target-id} | Get Target |
| PUT | /targets/{target-id} | Update Target |
| DELETE | /targets/{target-id} | Delete Target |

### vulnerabilities
| Method | Path | Description |
|--------|------|-------------|
| GET | /vulnerabilities | Get Vulnerabilities |
| POST | /vulnerabilities/variances/documentation | Get Vulnerability Variances Documentation |
| GET | /vulnerabilities/{vuln-id} | Get Vulnerability |
| PUT | /vulnerabilities/{vuln-id} | Update Vulnerability |
| GET | /vulnerabilities/{vuln-id}/comments | Get Vulnerability Comments |
| POST | /vulnerabilities/{vuln-id}/comments | Create Vulnerability Comment |
| GET | /vulnerabilities/{vuln-id}/comments/{comment-id} | Get Vulnerability Comment |
| PUT | /vulnerabilities/{vuln-id}/comments/{comment-id} | Update Vulnerability Comment |
| DELETE | /vulnerabilities/{vuln-id}/comments/{comment-id} | Delete Vulnerability Comment |
| GET | /vulnerabilities/{vuln-id}/discoveries | Get Vulnerability Discoveries |
| GET | /vulnerabilities/{vuln-id}/discoveries/{vuln-discovery-id} | Get Vulnerability Discovery |
| GET | /vulnerabilities/{vuln-id}/history | Get Vulnerability History |
| GET | /vulnerabilities/{vuln-id}/variances/{variance-id}/documentation | Get Vulnerability Variance Documentation |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all apps?" -> GET /apps
- "Create a app?" -> POST /apps
- "Get app details?" -> GET /apps/{app-id}
- "Update a app?" -> PUT /apps/{app-id}
- "Delete a app?" -> DELETE /apps/{app-id}
- "List all files?" -> GET /apps/{app-id}/files
- "Create a file?" -> POST /apps/{app-id}/files
- "Get file details?" -> GET /apps/{app-id}/files/{file-id}
- "Update a file?" -> PUT /apps/{app-id}/files/{file-id}
- "Delete a file?" -> DELETE /apps/{app-id}/files/{file-id}
- "List all tags?" -> GET /apps/{app-id}/tags
- "Create a tag?" -> POST /apps/{app-id}/tags
- "Delete a tag?" -> DELETE /apps/{app-id}/tags/{tag-id}
- "List all users?" -> GET /apps/{app-id}/users
- "Create a user?" -> POST /apps/{app-id}/users
- "Delete a user?" -> DELETE /apps/{app-id}/users/{user-id}
- "List all attack-templates?" -> GET /attack-templates
- "Create a attack-template?" -> POST /attack-templates
- "List all module-configs?" -> GET /attack-templates/module-configs
- "Get attack-template details?" -> GET /attack-templates/{attack-template-id}
- "Update a attack-template?" -> PUT /attack-templates/{attack-template-id}
- "Delete a attack-template?" -> DELETE /attack-templates/{attack-template-id}
- "List all modules?" -> GET /attack-templates/{attack-template-id}/modules
- "Create a module?" -> POST /attack-templates/{attack-template-id}/modules
- "Update a module?" -> PUT /attack-templates/{attack-template-id}/modules/{attack-module-id}
- "Delete a module?" -> DELETE /attack-templates/{attack-template-id}/modules/{attack-module-id}
- "List all blackouts?" -> GET /blackouts
- "Create a blackout?" -> POST /blackouts
- "Get blackout details?" -> GET /blackouts/{blackout-id}
- "Update a blackout?" -> PUT /blackouts/{blackout-id}
- "Delete a blackout?" -> DELETE /blackouts/{blackout-id}
- "List all engine-groups?" -> GET /engine-groups
- "Create a engine-group?" -> POST /engine-groups
- "Get engine-group details?" -> GET /engine-groups/{engine-group-id}
- "Update a engine-group?" -> PUT /engine-groups/{engine-group-id}
- "Delete a engine-group?" -> DELETE /engine-groups/{engine-group-id}
- "List all engines?" -> GET /engine-groups/{engine-group-id}/engines
- "List all engines?" -> GET /engines
- "Create a engine?" -> POST /engines
- "Get engine details?" -> GET /engines/{engine-id}
- "Update a engine?" -> PUT /engines/{engine-id}
- "Delete a engine?" -> DELETE /engines/{engine-id}
- "List all credential?" -> GET /engines/{engine-id}/credential
- "Create a upgrade?" -> POST /engines/{engine-id}/upgrade
- "List all modules?" -> GET /modules
- "Get module details?" -> GET /modules/{module-id}
- "Get attack details?" -> GET /modules/{module-id}/attacks/{attack-id}
- "List all documentation?" -> GET /modules/{module-id}/attacks/{attack-id}/documentation
- "List all reports?" -> GET /reports
- "Create a report?" -> POST /reports
- "Get report details?" -> GET /reports/{report-id}
- "Delete a report?" -> DELETE /reports/{report-id}
- "List all scan-configs?" -> GET /scan-configs
- "Create a scan-config?" -> POST /scan-configs
- "List all default?" -> GET /scan-configs/options/default
- "Get scan-config details?" -> GET /scan-configs/{scan-config-id}
- "Update a scan-config?" -> PUT /scan-configs/{scan-config-id}
- "Delete a scan-config?" -> DELETE /scan-configs/{scan-config-id}
- "List all options?" -> GET /scan-configs/{scan-config-id}/options
- "List all scans?" -> GET /scans
- "Create a scan?" -> POST /scans
- "Get scan details?" -> GET /scans/{scan-id}
- "Delete a scan?" -> DELETE /scans/{scan-id}
- "List all action?" -> GET /scans/{scan-id}/action
- "List all engine-events?" -> GET /scans/{scan-id}/engine-events
- "List all execution-details?" -> GET /scans/{scan-id}/execution-details
- "List all platform-events?" -> GET /scans/{scan-id}/platform-events
- "List all schedules?" -> GET /schedules
- "Create a schedule?" -> POST /schedules
- "Get schedule details?" -> GET /schedules/{schedule-id}
- "Update a schedule?" -> PUT /schedules/{schedule-id}
- "Delete a schedule?" -> DELETE /schedules/{schedule-id}
- "Create a search?" -> POST /search
- "List all tags?" -> GET /tags
- "Create a tag?" -> POST /tags
- "Get tag details?" -> GET /tags/{tag-id}
- "Update a tag?" -> PUT /tags/{tag-id}
- "Delete a tag?" -> DELETE /tags/{tag-id}
- "List all targets?" -> GET /targets
- "Create a target?" -> POST /targets
- "Get target details?" -> GET /targets/{target-id}
- "Update a target?" -> PUT /targets/{target-id}
- "Delete a target?" -> DELETE /targets/{target-id}
- "List all vulnerabilities?" -> GET /vulnerabilities
- "Create a documentation?" -> POST /vulnerabilities/variances/documentation
- "Get vulnerability details?" -> GET /vulnerabilities/{vuln-id}
- "Update a vulnerability?" -> PUT /vulnerabilities/{vuln-id}
- "List all comments?" -> GET /vulnerabilities/{vuln-id}/comments
- "Create a comment?" -> POST /vulnerabilities/{vuln-id}/comments
- "Get comment details?" -> GET /vulnerabilities/{vuln-id}/comments/{comment-id}
- "Update a comment?" -> PUT /vulnerabilities/{vuln-id}/comments/{comment-id}
- "Delete a comment?" -> DELETE /vulnerabilities/{vuln-id}/comments/{comment-id}
- "List all discoveries?" -> GET /vulnerabilities/{vuln-id}/discoveries
- "Get discovery details?" -> GET /vulnerabilities/{vuln-id}/discoveries/{vuln-discovery-id}
- "List all history?" -> GET /vulnerabilities/{vuln-id}/history
- "List all documentation?" -> GET /vulnerabilities/{vuln-id}/variances/{variance-id}/documentation
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
