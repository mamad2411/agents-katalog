---
name: rumble-api-deprecated
description: "Rumble API (deprecated) API skill. Use when working with Rumble API (deprecated) for releases, export, org. Covers 116 endpoints."
version: 1.0.0
generator: lapsh
---

# Rumble API (deprecated)
API version: 2.15.0

## Auth
Bearer bearer

## Base URL
https://console.rumble.run/api/v1.0

## Setup
1. Set Authorization header with your Bearer token
2. GET /releases/agent/version -- verify access
3. POST /org/agents/{agent_id}/update -- create first update

## Endpoints

116 endpoints across 4 groups. See references/api-spec.lap for full details.

### releases
| Method | Path | Description |
|--------|------|-------------|
| GET | /releases/agent/version | Returns latest agent version |
| GET | /releases/scanner/version | Returns latest scanner version |
| GET | /releases/platform/version | Returns latest platform version |

### export
| Method | Path | Description |
|--------|------|-------------|
| GET | /export/org/assets.json | Exports the asset inventory |
| GET | /export/org/assets.jsonl | Asset inventory as JSON line-delimited |
| GET | /export/org/assets.csv | Asset inventory as CSV |
| GET | /export/org/assets.nmap.xml | Asset inventory as Nmap-style XML |
| GET | /export/org/services.json | Service inventory as JSON |
| GET | /export/org/services.jsonl | Service inventory as JSON line-delimited |
| GET | /export/org/services.csv | Service inventory as CSV |
| GET | /export/org/sites.json | Export all sites |
| GET | /export/org/sites.jsonl | Site list as JSON line-delimited |
| GET | /export/org/sites.csv | Site list as CSV |
| GET | /export/org/wireless.json | Wireless inventory as JSON |
| GET | /export/org/wireless.jsonl | Wireless inventory as JSON line-delimited |
| GET | /export/org/wireless.csv | Wireless inventory as CSV |
| GET | /export/org/assets/sync/created/assets.json | Exports the asset inventory in a sync-friendly manner using created_at as a checkpoint. Requires the Splunk entitlement. |
| GET | /export/org/assets/sync/updated/assets.json | Exports the asset inventory in a sync-friendly manner using updated_at as a checkpoint. Requires the Splunk entitlement. |
| GET | /export/org/assets.servicenow.csv | Export an asset inventory as CSV for ServiceNow integration |
| GET | /export/org/assets.servicenow.json | Exports the asset inventory as JSON |
| GET | /export/org/services.servicenow.csv | Export a service inventory as CSV for ServiceNow integration |
| GET | /export/org/assets.cisco.csv | Cisco serial number and model name export for Cisco Smart Net Total Care Service. |

### org
| Method | Path | Description |
|--------|------|-------------|
| GET | /org/assets/top.types.csv | Top asset types as CSV |
| GET | /org/assets/top.os.csv | Top asset operating systems as CSV |
| GET | /org/assets/top.hw.csv | Top asset hardware products as CSV |
| GET | /org/assets/top.tags.csv | Top asset tags as CSV |
| GET | /org/services/top.tcp.csv | Top TCP services as CSV |
| GET | /org/services/top.udp.csv | Top UDP services as CSV |
| GET | /org/services/top.protocols.csv | Top service protocols as CSV |
| GET | /org/services/top.products.csv | Top service products as CSV |
| GET | /org/services/subnet.stats.csv | Subnet utilization statistics as as CSV |
| GET | /org | Get organization details |
| PATCH | /org | Update organization details |
| GET | /org/key | Get API key details |
| DELETE | /org/key | Remove the current API key |
| PATCH | /org/key/rotate | Rotate the API key secret and return the updated key |
| GET | /org/agents | Get all agents |
| GET | /org/agents/{agent_id} | Get details for a single agent |
| DELETE | /org/agents/{agent_id} | Remove and uninstall an agent |
| PATCH | /org/agents/{agent_id} | Update the site associated with agent |
| POST | /org/agents/{agent_id}/update | Force an agent to update and restart |
| GET | /org/sites | Get all sites |
| PUT | /org/sites | Create a new site |
| GET | /org/sites/{site_id} | Get site details |
| DELETE | /org/sites/{site_id} | Remove a site and associated assets |
| PATCH | /org/sites/{site_id} | Update a site definition |
| PUT | /org/sites/{site_id}/import | Import a scan data file into a site |
| PUT | /org/sites/{site_id}/import/nessus | Import a Nessus scan data file into a site |
| PUT | /org/sites/{site_id}/scan | Create a scan task for a given site |
| GET | /org/assets | Get all assets |
| GET | /org/assets/{asset_id} | Get asset details |
| DELETE | /org/assets/{asset_id} | Remove an asset |
| PATCH | /org/assets/{asset_id}/comments | Update asset comments |
| PATCH | /org/assets/{asset_id}/tags | Update asset tags |
| PATCH | /org/assets/bulk/tags | Update tags across multiple assets based on a search query |
| POST | /org/assets/bulk/clearTags | Clear all tags across multiple assets based on a search query |
| GET | /org/services | Get all services |
| GET | /org/services/{service_id} | Get service details |
| DELETE | /org/services/{service_id} | Remove a service |
| GET | /org/wireless | Get all wireless LANs |
| GET | /org/wireless/{wireless_id} | Get wireless LAN details |
| DELETE | /org/wireless/{wireless_id} | Remove a wireless LAN |
| GET | /org/tasks | Get all tasks (last 1000) |
| GET | /org/tasks/{task_id} | Get task details |
| PATCH | /org/tasks/{task_id} | Update task parameters |
| GET | /org/tasks/{task_id}/data | Returns a temporary task scan data url |
| GET | /org/tasks/{task_id}/changes | Returns a temporary task change report data url |
| GET | /org/tasks/{task_id}/log | Returns a temporary task log data url |
| POST | /org/tasks/{task_id}/stop | Signal that a task should be stopped or canceledThis will also remove recurring and scheduled tasks |
| POST | /org/tasks/{task_id}/hide | Signal that a completed task should be hidden |

### account
| Method | Path | Description |
|--------|------|-------------|
| GET | /account/orgs | Get all organization details |
| PUT | /account/orgs | Create a new organization |
| GET | /account/orgs/{org_id} | Get organization details |
| PATCH | /account/orgs/{org_id} | Update organization details |
| DELETE | /account/orgs/{org_id} | Remove this organization |
| DELETE | /account/orgs/{org_id}/exportToken | Removes the export token from the specified organization |
| PATCH | /account/orgs/{org_id}/exportToken/rotate | Rotates the organization export token and returns the updated organization |
| GET | /account/license | Get license details |
| GET | /account/sites | Get all sites details across all organizations |
| GET | /account/credentials | Get all account credentials |
| PUT | /account/credentials | Create a new credential |
| GET | /account/credentials/{credential_id} | Get credential details |
| DELETE | /account/credentials/{credential_id} | Remove this credential |
| GET | /account/keys | Get all active API keys |
| PUT | /account/keys | Create a new key |
| GET | /account/keys/{key_id} | Get key details |
| DELETE | /account/keys/{key_id} | Remove this key |
| PATCH | /account/keys/{key_id}/rotate | Rotates the key secret |
| GET | /account/events.json | System event log as JSON |
| GET | /account/events.jsonl | System event log as JSON line-delimited |
| GET | /account/tasks | Get all task details across all organizations (up to 1000) |
| GET | /account/tasks/templates | Get all scan templates across all organizations (up to 1000) |
| POST | /account/tasks/templates | Create a new scan template |
| PUT | /account/tasks/templates | Update scan template |
| GET | /account/tasks/templates/{scan_template_id} | Get scan template details |
| DELETE | /account/tasks/templates/{scan_template_id} | Remove scan template |
| GET | /account/agents | Get all agents across all organizations |
| GET | /account/users | Get all users |
| PUT | /account/users | Create a new user account |
| PUT | /account/users/invite | Create a new user account and send an email invite |
| GET | /account/users/{user_id} | Get user details |
| DELETE | /account/users/{user_id} | Remove this user |
| PATCH | /account/users/{user_id} | Update a user's details |
| PATCH | /account/users/{user_id}/resetMFA | Resets the user's MFA tokens |
| PATCH | /account/users/{user_id}/resetLockout | Resets the user's lockout status |
| PATCH | /account/users/{user_id}/resetPassword | Sends the user a password reset email |
| GET | /account/groups | Get all groups |
| POST | /account/groups | Create a new group |
| PUT | /account/groups | Update an existing group |
| GET | /account/groups/{group_id} | Get group details |
| DELETE | /account/groups/{group_id} | Remove this group |
| GET | /account/sso/groups | Get all SSO group mappings |
| POST | /account/sso/groups | Create a new SSO group mapping |
| PUT | /account/sso/groups | Update an existing SSO group mapping |
| GET | /account/sso/groups/{group_mapping_id} | Get SSO group mapping details |
| DELETE | /account/sso/groups/{group_mapping_id} | Remove this SSO group mapping |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all version?" -> GET /releases/agent/version
- "List all version?" -> GET /releases/scanner/version
- "List all version?" -> GET /releases/platform/version
- "Search assets.json?" -> GET /export/org/assets.json
- "Search assets.jsonl?" -> GET /export/org/assets.jsonl
- "Search assets.csv?" -> GET /export/org/assets.csv
- "Search assets.nmap.xml?" -> GET /export/org/assets.nmap.xml
- "Search services.json?" -> GET /export/org/services.json
- "Search services.jsonl?" -> GET /export/org/services.jsonl
- "Search services.csv?" -> GET /export/org/services.csv
- "Search sites.json?" -> GET /export/org/sites.json
- "Search sites.jsonl?" -> GET /export/org/sites.jsonl
- "List all sites.csv?" -> GET /export/org/sites.csv
- "Search wireless.json?" -> GET /export/org/wireless.json
- "Search wireless.jsonl?" -> GET /export/org/wireless.jsonl
- "Search wireless.csv?" -> GET /export/org/wireless.csv
- "List all top.types.csv?" -> GET /org/assets/top.types.csv
- "List all top.os.csv?" -> GET /org/assets/top.os.csv
- "List all top.hw.csv?" -> GET /org/assets/top.hw.csv
- "List all top.tags.csv?" -> GET /org/assets/top.tags.csv
- "List all top.tcp.csv?" -> GET /org/services/top.tcp.csv
- "List all top.udp.csv?" -> GET /org/services/top.udp.csv
- "List all top.protocols.csv?" -> GET /org/services/top.protocols.csv
- "List all top.products.csv?" -> GET /org/services/top.products.csv
- "List all subnet.stats.csv?" -> GET /org/services/subnet.stats.csv
- "List all org?" -> GET /org
- "List all key?" -> GET /org/key
- "List all agents?" -> GET /org/agents
- "Get agent details?" -> GET /org/agents/{agent_id}
- "Delete a agent?" -> DELETE /org/agents/{agent_id}
- "Partially update a agent?" -> PATCH /org/agents/{agent_id}
- "Create a update?" -> POST /org/agents/{agent_id}/update
- "List all sites?" -> GET /org/sites
- "Get site details?" -> GET /org/sites/{site_id}
- "Delete a site?" -> DELETE /org/sites/{site_id}
- "Partially update a site?" -> PATCH /org/sites/{site_id}
- "Search assets?" -> GET /org/assets
- "Get asset details?" -> GET /org/assets/{asset_id}
- "Delete a asset?" -> DELETE /org/assets/{asset_id}
- "Create a clearTag?" -> POST /org/assets/bulk/clearTags
- "Search services?" -> GET /org/services
- "Get service details?" -> GET /org/services/{service_id}
- "Delete a service?" -> DELETE /org/services/{service_id}
- "Search wireless?" -> GET /org/wireless
- "Get wireless details?" -> GET /org/wireless/{wireless_id}
- "Delete a wireless?" -> DELETE /org/wireless/{wireless_id}
- "Search tasks?" -> GET /org/tasks
- "Get task details?" -> GET /org/tasks/{task_id}
- "Partially update a task?" -> PATCH /org/tasks/{task_id}
- "List all data?" -> GET /org/tasks/{task_id}/data
- "List all changes?" -> GET /org/tasks/{task_id}/changes
- "List all log?" -> GET /org/tasks/{task_id}/log
- "Create a stop?" -> POST /org/tasks/{task_id}/stop
- "Create a hide?" -> POST /org/tasks/{task_id}/hide
- "Search orgs?" -> GET /account/orgs
- "Get org details?" -> GET /account/orgs/{org_id}
- "Partially update a org?" -> PATCH /account/orgs/{org_id}
- "Delete a org?" -> DELETE /account/orgs/{org_id}
- "List all license?" -> GET /account/license
- "Search sites?" -> GET /account/sites
- "Search credentials?" -> GET /account/credentials
- "Get credential details?" -> GET /account/credentials/{credential_id}
- "Delete a credential?" -> DELETE /account/credentials/{credential_id}
- "List all keys?" -> GET /account/keys
- "Get key details?" -> GET /account/keys/{key_id}
- "Delete a key?" -> DELETE /account/keys/{key_id}
- "Search events.json?" -> GET /account/events.json
- "Search events.jsonl?" -> GET /account/events.jsonl
- "Search tasks?" -> GET /account/tasks
- "Search templates?" -> GET /account/tasks/templates
- "Create a template?" -> POST /account/tasks/templates
- "Get template details?" -> GET /account/tasks/templates/{scan_template_id}
- "Delete a template?" -> DELETE /account/tasks/templates/{scan_template_id}
- "Search agents?" -> GET /account/agents
- "List all users?" -> GET /account/users
- "Get user details?" -> GET /account/users/{user_id}
- "Delete a user?" -> DELETE /account/users/{user_id}
- "Partially update a user?" -> PATCH /account/users/{user_id}
- "List all groups?" -> GET /account/groups
- "Create a group?" -> POST /account/groups
- "Get group details?" -> GET /account/groups/{group_id}
- "Delete a group?" -> DELETE /account/groups/{group_id}
- "List all groups?" -> GET /account/sso/groups
- "Create a group?" -> POST /account/sso/groups
- "Get group details?" -> GET /account/sso/groups/{group_mapping_id}
- "Delete a group?" -> DELETE /account/sso/groups/{group_mapping_id}
- "Search assets.json?" -> GET /export/org/assets/sync/created/assets.json
- "Search assets.json?" -> GET /export/org/assets/sync/updated/assets.json
- "List all assets.servicenow.csv?" -> GET /export/org/assets.servicenow.csv
- "List all assets.servicenow.json?" -> GET /export/org/assets.servicenow.json
- "List all services.servicenow.csv?" -> GET /export/org/services.servicenow.csv
- "Search assets.cisco.csv?" -> GET /export/org/assets.cisco.csv
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
