---
name: snyk-api
description: "Snyk API skill. Use when working with Snyk for user, group, orgs. Covers 100 endpoints."
version: 1.0.0
generator: lapsh
---

# Snyk API
API version: 1.0

## Auth
ApiKey Authorization in header

## Base URL
https://api.snyk.io/v1

## Setup
1. Set your API key in the appropriate header
2. GET /user/me -- verify access
3. POST /group/{groupId}/org/{orgId}/members -- create first members

## Endpoints

100 endpoints across 7 groups. See references/api-spec.lap for full details.

### user
| Method | Path | Description |
|--------|------|-------------|
| GET | /user/{userId} | Get User Details |
| GET | /user/me | Get My Details |
| GET | /user/me/notification-settings/org/{orgId} | Get organization notification settings |
| PUT | /user/me/notification-settings/org/{orgId} | Modify organization notification settings |
| GET | /user/me/notification-settings/org/{orgId}/project/{projectId} | Get project notification settings |
| PUT | /user/me/notification-settings/org/{orgId}/project/{projectId} | Modify project notification settings |

### group
| Method | Path | Description |
|--------|------|-------------|
| GET | /group/{groupId}/settings | View group settings |
| PUT | /group/{groupId}/settings | Update group settings |
| GET | /group/{groupId}/members | List all members in a group |
| POST | /group/{groupId}/org/{orgId}/members | Add a member to an organization within a group |
| GET | /group/{groupId}/tags | List all tags in a group |
| POST | /group/{groupId}/tags/delete | Delete tag from group |
| GET | /group/{groupId}/orgs | List all organizations in a group |
| GET | /group/{groupId}/roles | List all roles in a group |

### orgs
| Method | Path | Description |
|--------|------|-------------|
| GET | /orgs | List all the organizations a user belongs to |

### org
| Method | Path | Description |
|--------|------|-------------|
| POST | /org | Create a new organization |
| GET | /org/{orgId}/notification-settings | Get organization notification settings |
| PUT | /org/{orgId}/notification-settings | Set notification settings |
| POST | /org/{orgId}/invite | Invite users |
| GET | /org/{orgId}/members | List Members |
| GET | /org/{orgId}/settings | View organization settings |
| PUT | /org/{orgId}/settings | Update organization settings |
| PUT | /org/{orgId}/members/{userId} | Update a member in the organization |
| DELETE | /org/{orgId}/members/{userId} | Remove a member from the organization |
| PUT | /org/{orgId}/members/update/{userId} | Update a member's role in the organization |
| DELETE | /org/{orgId} | Remove organization |
| POST | /org/{orgId}/provision | Provision a user to the organization |
| GET | /org/{orgId}/provision | List pending user provisions |
| DELETE | /org/{orgId}/provision | Delete pending user provision |
| GET | /org/{orgId}/integrations | List |
| POST | /org/{orgId}/integrations | Add new integration |
| PUT | /org/{orgId}/integrations/{integrationId} | Update existing integration |
| DELETE | /org/{orgId}/integrations/{integrationId}/authentication | Delete credentials |
| POST | /org/{orgId}/integrations/{integrationId}/authentication/provision-token | Provision new broker token |
| POST | /org/{orgId}/integrations/{integrationId}/authentication/switch-token | Switch between broker tokens |
| POST | /org/{orgId}/integrations/{integrationId}/clone | Clone an integration (with settings and credentials) |
| GET | /org/{orgId}/integrations/{type} | Get existing integration by type |
| GET | /org/{orgId}/integrations/{integrationId}/settings | Get Integration Settings |
| PUT | /org/{orgId}/integrations/{integrationId}/settings | Update Integration Settings |
| POST | /org/{orgId}/integrations/{integrationId}/import | Import targets |
| GET | /org/{orgId}/integrations/{integrationId}/import/{jobId} | Get import job details |
| GET | /org/{orgId}/project/{projectId} | Retrieve a single project |
| PUT | /org/{orgId}/project/{projectId} | Update a project |
| DELETE | /org/{orgId}/project/{projectId} | Delete a project |
| POST | /org/{orgId}/project/{projectId}/deactivate | Deactivate a project |
| POST | /org/{orgId}/project/{projectId}/activate | Activate a project |
| POST | /org/{orgId}/project/{projectId}/aggregated-issues | List all Aggregated issues |
| GET | /org/{orgId}/project/{projectId}/issue/{issueId}/paths | List all project issue paths |
| POST | /org/{orgId}/project/{projectId}/history | List all project snapshots |
| POST | /org/{orgId}/project/{projectId}/history/{snapshotId}/aggregated-issues | List all project snapshot aggregated issues |
| GET | /org/{orgId}/project/{projectId}/history/{snapshotId}/issue/{issueId}/paths | List all project snapshot issue paths |
| GET | /org/{orgId}/project/{projectId}/dep-graph | Get Project dependency graph |
| GET | /org/{orgId}/project/{projectId}/ignores | List all ignores |
| GET | /org/{orgId}/project/{projectId}/ignore/{issueId} | Retrieve ignore |
| POST | /org/{orgId}/project/{projectId}/ignore/{issueId} | Add ignore |
| PUT | /org/{orgId}/project/{projectId}/ignore/{issueId} | Replace ignores |
| DELETE | /org/{orgId}/project/{projectId}/ignore/{issueId} | Delete ignores |
| GET | /org/{orgId}/project/{projectId}/jira-issues | List all jira issues |
| POST | /org/{orgId}/project/{projectId}/issue/{issueId}/jira-issue | Create jira issue |
| GET | /org/{orgId}/project/{projectId}/settings | List project settings |
| PUT | /org/{orgId}/project/{projectId}/settings | Update project settings |
| DELETE | /org/{orgId}/project/{projectId}/settings | Delete project settings |
| PUT | /org/{orgId}/project/{projectId}/move | Move project to a different organization |
| POST | /org/{orgId}/project/{projectId}/tags | Add a tag to a project |
| POST | /org/{orgId}/project/{projectId}/tags/remove | Remove a tag from a project |
| POST | /org/{orgId}/project/{projectId}/attributes | Applying attributes |
| POST | /org/{orgId}/dependencies | List all dependencies |
| POST | /org/{orgId}/licenses | List all licenses |
| GET | /org/{orgId}/entitlements | List all entitlements |
| GET | /org/{orgId}/entitlement/{entitlementKey} | Get an organization's entitlement value |
| POST | /org/{orgId}/webhooks | Create a webhook |
| GET | /org/{orgId}/webhooks | List webhooks |
| GET | /org/{orgId}/webhooks/{webhookId} | Retrieve a webhook |
| DELETE | /org/{orgId}/webhooks/{webhookId} | Delete a webhook |
| POST | /org/{orgId}/webhooks/{webhookId}/ping | Ping a webhook |

### test
| Method | Path | Description |
|--------|------|-------------|
| GET | /test/maven/{groupId}/{artifactId}/{version} | Test for issues in a public package by group id, artifact id and version |
| POST | /test/maven | Test maven file |
| GET | /test/npm/{packageName}/{version} | Test for issues in a public package by name and version |
| POST | /test/npm | Test package.json & package-lock.json File |
| POST | /test/golangdep | Test Gopkg.toml & Gopkg.lock File |
| POST | /test/govendor | Test vendor.json File |
| POST | /test/yarn | Test package.json & yarn.lock File |
| GET | /test/rubygems/{gemName}/{version} | Test for issues in a public gem by name and version |
| POST | /test/rubygems | Test gemfile.lock file |
| GET | /test/gradle/{group}/{name}/{version} | Test for issues in a public package by group, name and version |
| POST | /test/gradle | Test gradle file |
| GET | /test/sbt/{groupId}/{artifactId}/{version} | sbt_Test for issues in a public package by group id, artifact id and version |
| POST | /test/sbt | Test sbt file |
| GET | /test/pip/{packageName}/{version} | pip_Test for issues in a public package by name and version |
| POST | /test/pip | Test requirements.txt file |
| POST | /test/composer | Test composer.json & composer.lock file |
| POST | /test/dep-graph | Test Dep Graph |

### monitor
| Method | Path | Description |
|--------|------|-------------|
| POST | /monitor/dep-graph | Monitor Dep Graph |

### reporting
| Method | Path | Description |
|--------|------|-------------|
| POST | /reporting/issues/latest | Get list of latest issues |
| POST | /reporting/issues | Get list of issues |
| POST | /reporting/counts/issues/latest | Get latest issue counts |
| POST | /reporting/counts/issues | Get issue counts |
| POST | /reporting/counts/projects/latest | Get latest project counts |
| POST | /reporting/counts/projects | Get project counts |
| POST | /reporting/counts/tests | Get test counts |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get user details?" -> GET /user/{userId}
- "List all me?" -> GET /user/me
- "Get org details?" -> GET /user/me/notification-settings/org/{orgId}
- "Update a org?" -> PUT /user/me/notification-settings/org/{orgId}
- "Get project details?" -> GET /user/me/notification-settings/org/{orgId}/project/{projectId}
- "Update a project?" -> PUT /user/me/notification-settings/org/{orgId}/project/{projectId}
- "List all settings?" -> GET /group/{groupId}/settings
- "List all members?" -> GET /group/{groupId}/members
- "Create a member?" -> POST /group/{groupId}/org/{orgId}/members
- "List all tags?" -> GET /group/{groupId}/tags
- "Create a delete?" -> POST /group/{groupId}/tags/delete
- "List all orgs?" -> GET /group/{groupId}/orgs
- "List all roles?" -> GET /group/{groupId}/roles
- "List all orgs?" -> GET /orgs
- "Create a org?" -> POST /org
- "List all notification-settings?" -> GET /org/{orgId}/notification-settings
- "Create a invite?" -> POST /org/{orgId}/invite
- "List all members?" -> GET /org/{orgId}/members
- "List all settings?" -> GET /org/{orgId}/settings
- "Update a member?" -> PUT /org/{orgId}/members/{userId}
- "Delete a member?" -> DELETE /org/{orgId}/members/{userId}
- "Update a update?" -> PUT /org/{orgId}/members/update/{userId}
- "Delete a org?" -> DELETE /org/{orgId}
- "Create a provision?" -> POST /org/{orgId}/provision
- "List all provision?" -> GET /org/{orgId}/provision
- "List all integrations?" -> GET /org/{orgId}/integrations
- "Create a integration?" -> POST /org/{orgId}/integrations
- "Update a integration?" -> PUT /org/{orgId}/integrations/{integrationId}
- "Create a provision-token?" -> POST /org/{orgId}/integrations/{integrationId}/authentication/provision-token
- "Create a switch-token?" -> POST /org/{orgId}/integrations/{integrationId}/authentication/switch-token
- "Create a clone?" -> POST /org/{orgId}/integrations/{integrationId}/clone
- "Get integration details?" -> GET /org/{orgId}/integrations/{type}
- "List all settings?" -> GET /org/{orgId}/integrations/{integrationId}/settings
- "Create a import?" -> POST /org/{orgId}/integrations/{integrationId}/import
- "Get import details?" -> GET /org/{orgId}/integrations/{integrationId}/import/{jobId}
- "Get project details?" -> GET /org/{orgId}/project/{projectId}
- "Update a project?" -> PUT /org/{orgId}/project/{projectId}
- "Delete a project?" -> DELETE /org/{orgId}/project/{projectId}
- "Create a deactivate?" -> POST /org/{orgId}/project/{projectId}/deactivate
- "Create a activate?" -> POST /org/{orgId}/project/{projectId}/activate
- "Create a aggregated-issue?" -> POST /org/{orgId}/project/{projectId}/aggregated-issues
- "List all paths?" -> GET /org/{orgId}/project/{projectId}/issue/{issueId}/paths
- "Create a history?" -> POST /org/{orgId}/project/{projectId}/history
- "Create a aggregated-issue?" -> POST /org/{orgId}/project/{projectId}/history/{snapshotId}/aggregated-issues
- "List all paths?" -> GET /org/{orgId}/project/{projectId}/history/{snapshotId}/issue/{issueId}/paths
- "List all dep-graph?" -> GET /org/{orgId}/project/{projectId}/dep-graph
- "List all ignores?" -> GET /org/{orgId}/project/{projectId}/ignores
- "Get ignore details?" -> GET /org/{orgId}/project/{projectId}/ignore/{issueId}
- "Update a ignore?" -> PUT /org/{orgId}/project/{projectId}/ignore/{issueId}
- "Delete a ignore?" -> DELETE /org/{orgId}/project/{projectId}/ignore/{issueId}
- "List all jira-issues?" -> GET /org/{orgId}/project/{projectId}/jira-issues
- "Create a jira-issue?" -> POST /org/{orgId}/project/{projectId}/issue/{issueId}/jira-issue
- "List all settings?" -> GET /org/{orgId}/project/{projectId}/settings
- "Create a tag?" -> POST /org/{orgId}/project/{projectId}/tags
- "Create a remove?" -> POST /org/{orgId}/project/{projectId}/tags/remove
- "Create a attribute?" -> POST /org/{orgId}/project/{projectId}/attributes
- "Create a dependency?" -> POST /org/{orgId}/dependencies
- "Create a license?" -> POST /org/{orgId}/licenses
- "List all entitlements?" -> GET /org/{orgId}/entitlements
- "Get entitlement details?" -> GET /org/{orgId}/entitlement/{entitlementKey}
- "Get maven details?" -> GET /test/maven/{groupId}/{artifactId}/{version}
- "Create a maven?" -> POST /test/maven
- "Get npm details?" -> GET /test/npm/{packageName}/{version}
- "Create a npm?" -> POST /test/npm
- "Create a golangdep?" -> POST /test/golangdep
- "Create a govendor?" -> POST /test/govendor
- "Create a yarn?" -> POST /test/yarn
- "Get rubygem details?" -> GET /test/rubygems/{gemName}/{version}
- "Create a rubygem?" -> POST /test/rubygems
- "Get gradle details?" -> GET /test/gradle/{group}/{name}/{version}
- "Create a gradle?" -> POST /test/gradle
- "Get sbt details?" -> GET /test/sbt/{groupId}/{artifactId}/{version}
- "Create a sbt?" -> POST /test/sbt
- "Get pip details?" -> GET /test/pip/{packageName}/{version}
- "Create a pip?" -> POST /test/pip
- "Create a composer?" -> POST /test/composer
- "Create a dep-graph?" -> POST /test/dep-graph
- "Create a dep-graph?" -> POST /monitor/dep-graph
- "Create a latest?" -> POST /reporting/issues/latest
- "Create a issue?" -> POST /reporting/issues
- "Create a latest?" -> POST /reporting/counts/issues/latest
- "Create a issue?" -> POST /reporting/counts/issues
- "Create a latest?" -> POST /reporting/counts/projects/latest
- "Create a project?" -> POST /reporting/counts/projects
- "Create a test?" -> POST /reporting/counts/tests
- "Create a webhook?" -> POST /org/{orgId}/webhooks
- "List all webhooks?" -> GET /org/{orgId}/webhooks
- "Get webhook details?" -> GET /org/{orgId}/webhooks/{webhookId}
- "Delete a webhook?" -> DELETE /org/{orgId}/webhooks/{webhookId}
- "Create a ping?" -> POST /org/{orgId}/webhooks/{webhookId}/ping
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
