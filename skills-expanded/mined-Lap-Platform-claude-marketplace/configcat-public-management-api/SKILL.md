---
name: configcat-public-management-api
description: "ConfigCat Public Management API skill. Use when working with ConfigCat Public Management for proxy-profiles, organizations, products. Covers 105 endpoints."
version: 1.0.0
generator: lapsh
---

# ConfigCat Public Management API
API version: v1

## Auth
Bearer basic

## Base URL
https://api.configcat.com

## Setup
1. Set Authorization header with your Bearer token
2. GET /v1/organizations -- verify access
3. POST /v1/organizations/{organizationId}/proxy-profiles -- create first proxy-profiles

## Endpoints

105 endpoints across 16 groups. See references/api-spec.lap for full details.

### proxy-profiles
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/proxy-profiles/{proxyProfileId} | Get Proxy Profile |
| PUT | /v1/proxy-profiles/{proxyProfileId} | Replace Proxy Profile |
| PATCH | /v1/proxy-profiles/{proxyProfileId} | Update Proxy Profile |
| DELETE | /v1/proxy-profiles/{proxyProfileId} | Delete Proxy Profile |
| GET | /v1/proxy-profiles/{proxyProfileId}/sdk-keys | Get selected SDK keys |
| POST | /v1/proxy-profiles/{proxyProfileId}/sdk-keys/deselect | Deselect SDK keys |
| POST | /v1/proxy-profiles/{proxyProfileId}/secret | Generate Secret |
| POST | /v1/proxy-profiles/{proxyProfileId}/sdk-keys/select | Select SDK keys |

### organizations
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/organizations | List Organizations |
| GET | /v1/organizations/{organizationId}/proxy-profiles | List Proxy Profiles |
| POST | /v1/organizations/{organizationId}/proxy-profiles | Create Proxy Profile |
| GET | /v1/organizations/{organizationId}/auditlogs | List Audit log items for Organization |
| GET | /v1/organizations/{organizationId}/organization-limitations | Get Organization limitations |
| GET | /v1/organizations/{organizationId}/members | List Organization Members |
| GET | /v2/organizations/{organizationId}/members | List Organization Members |
| GET | /v1/organizations/{organizationId}/invitations | List Pending Invitations in Organization |
| POST | /v1/organizations/{organizationId}/products | Create Product |
| POST | /v1/organizations/{organizationId}/members/{userId} | Update Member Permissions |
| DELETE | /v1/organizations/{organizationId}/members/{userId} | Delete Member from Organization |

### products
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/products | List Products |
| GET | /v1/products/{productId}/tags | List Tags |
| POST | /v1/products/{productId}/tags | Create Tag |
| GET | /v1/products/{productId}/webhooks | List Webhooks |
| GET | /v1/products/{productId}/configs | List Configs |
| POST | /v1/products/{productId}/configs | Create Config |
| GET | /v1/products/{productId}/environments | List Environments |
| POST | /v1/products/{productId}/environments | Create Environment |
| GET | /v1/products/{productId}/permissions | List Permission Groups |
| POST | /v1/products/{productId}/permissions | Create Permission Group |
| GET | /v1/products/{productId}/integrations | List Integrations |
| POST | /v1/products/{productId}/integrations | Create Integration |
| GET | /v1/products/{productId}/segments | List Segments |
| POST | /v1/products/{productId}/segments | Create Segment |
| GET | /v1/products/{productId}/auditlogs | List Audit log items for Product |
| GET | /v1/products/{productId}/staleflags | List Zombie (stale) flags for Product |
| GET | /v1/products/{productId}/invitations | List Pending Invitations in Product |
| GET | /v1/products/{productId} | Get Product |
| PUT | /v1/products/{productId} | Update Product |
| DELETE | /v1/products/{productId} | Delete Product |
| GET | /v1/products/{productId}/members | List Product Members |
| GET | /v1/products/{productId}/preferences | Get Product Preferences |
| POST | /v1/products/{productId}/preferences | Update Product Preferences |
| POST | /v1/products/{productId}/members/invite | Invite Member |
| DELETE | /v1/products/{productId}/members/{userId} | Delete Member from Product |

### configs
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/configs/{configId}/settings | List Flags |
| POST | /v1/configs/{configId}/settings | Create Flag |
| GET | /v1/configs/{configId} | Get Config |
| PUT | /v1/configs/{configId} | Update Config |
| DELETE | /v1/configs/{configId} | Delete Config |
| GET | /v1/configs/{configId}/deleted-settings | List Deleted Settings |
| GET | /v1/configs/{configId}/environments/{environmentId} | Get SDK Key |
| GET | /v1/configs/{configId}/environments/{environmentId}/values | Get values |
| POST | /v1/configs/{configId}/environments/{environmentId}/values | Post values |
| GET | /v2/configs/{configId}/environments/{environmentId}/values | Get values |
| POST | /v2/configs/{configId}/environments/{environmentId}/values | Post values |
| POST | /v1/configs/{configId}/environments/{environmentId}/webhooks | Create Webhook |

### settings
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/settings/{settingId}/code-references | Get References for Feature Flag or Setting |
| GET | /v1/settings/{settingId}/predefined-variations | Get predefined variations |
| PUT | /v1/settings/{settingId}/predefined-variations | Update predefined variations |
| GET | /v1/settings/{settingId} | Get Flag |
| PUT | /v1/settings/{settingId} | Replace Flag |
| PATCH | /v1/settings/{settingId} | Update Flag |
| DELETE | /v1/settings/{settingId} | Delete Flag |
| GET | /v1/settings/{settingKeyOrId}/value | Get value |
| PUT | /v1/settings/{settingKeyOrId}/value | Replace value |
| PATCH | /v1/settings/{settingKeyOrId}/value | Update value |
| GET | /v2/settings/{settingKeyOrId}/value | Get value |
| PUT | /v2/settings/{settingKeyOrId}/value | Replace value |
| PATCH | /v2/settings/{settingKeyOrId}/value | Update value |

### environments
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/environments/{environmentId} | Get Environment |
| PUT | /v1/environments/{environmentId} | Update Environment |
| DELETE | /v1/environments/{environmentId} | Delete Environment |
| GET | /v1/environments/{environmentId}/settings/{settingId}/value | Get value |
| PUT | /v1/environments/{environmentId}/settings/{settingId}/value | Replace value |
| PATCH | /v1/environments/{environmentId}/settings/{settingId}/value | Update value |
| GET | /v2/environments/{environmentId}/settings/{settingId}/value | Get value |
| PUT | /v2/environments/{environmentId}/settings/{settingId}/value | Replace value |
| PATCH | /v2/environments/{environmentId}/settings/{settingId}/value | Update value |
| POST | /v1/environments/{environmentId}/settings/{settingId}/integrationLinks/{integrationLinkType}/{key} | Add or update Integration link |
| DELETE | /v1/environments/{environmentId}/settings/{settingId}/integrationLinks/{integrationLinkType}/{key} | Delete Integration link |

### permissions
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/permissions/{permissionGroupId} | Get Permission Group |
| PUT | /v1/permissions/{permissionGroupId} | Update Permission Group |
| DELETE | /v1/permissions/{permissionGroupId} | Delete Permission Group |

### integrations
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/integrations/{integrationId} | Get Integration |
| PUT | /v1/integrations/{integrationId} | Update Integration |
| DELETE | /v1/integrations/{integrationId} | Delete Integration |

### integrationLink
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/integrationLink/{integrationLinkType}/{key}/details | Get Integration link |

### me
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/me | Get authenticated user details |

### segments
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/segments/{segmentId} | Get Segment |
| PUT | /v1/segments/{segmentId} | Update Segment |
| DELETE | /v1/segments/{segmentId} | Delete Segment |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/tags/{tagId}/settings | List Settings by Tag |
| GET | /v1/tags/{tagId} | Get Tag |
| PUT | /v1/tags/{tagId} | Update Tag |
| DELETE | /v1/tags/{tagId} | Delete Tag |

### webhooks
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/webhooks/{webhookId} | Get Webhook |
| PUT | /v1/webhooks/{webhookId} | Replace Webhook |
| PATCH | /v1/webhooks/{webhookId} | Update Webhook |
| DELETE | /v1/webhooks/{webhookId} | Delete Webhook |
| GET | /v1/webhooks/{webhookId}/keys | Get Webhook Signing Keys |

### jira
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/jira/environments/{environmentId}/settings/{settingId}/integrationLinks/{key} |  |
| POST | /v1/jira/connect |  |

### code-references
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/code-references/delete-reports | Delete Reference reports |
| POST | /v1/code-references | Upload References |

### invitations
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /v1/invitations/{invitationId} | Delete Invitation |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get proxy-profile details?" -> GET /v1/proxy-profiles/{proxyProfileId}
- "Update a proxy-profile?" -> PUT /v1/proxy-profiles/{proxyProfileId}
- "Partially update a proxy-profile?" -> PATCH /v1/proxy-profiles/{proxyProfileId}
- "Delete a proxy-profile?" -> DELETE /v1/proxy-profiles/{proxyProfileId}
- "List all organizations?" -> GET /v1/organizations
- "List all products?" -> GET /v1/products
- "List all proxy-profiles?" -> GET /v1/organizations/{organizationId}/proxy-profiles
- "Create a proxy-profile?" -> POST /v1/organizations/{organizationId}/proxy-profiles
- "List all tags?" -> GET /v1/products/{productId}/tags
- "Create a tag?" -> POST /v1/products/{productId}/tags
- "List all webhooks?" -> GET /v1/products/{productId}/webhooks
- "List all configs?" -> GET /v1/products/{productId}/configs
- "Create a config?" -> POST /v1/products/{productId}/configs
- "List all environments?" -> GET /v1/products/{productId}/environments
- "Create a environment?" -> POST /v1/products/{productId}/environments
- "List all permissions?" -> GET /v1/products/{productId}/permissions
- "Create a permission?" -> POST /v1/products/{productId}/permissions
- "List all integrations?" -> GET /v1/products/{productId}/integrations
- "Create a integration?" -> POST /v1/products/{productId}/integrations
- "List all segments?" -> GET /v1/products/{productId}/segments
- "Create a segment?" -> POST /v1/products/{productId}/segments
- "List all settings?" -> GET /v1/configs/{configId}/settings
- "Create a setting?" -> POST /v1/configs/{configId}/settings
- "List all auditlogs?" -> GET /v1/products/{productId}/auditlogs
- "List all staleflags?" -> GET /v1/products/{productId}/staleflags
- "List all code-references?" -> GET /v1/settings/{settingId}/code-references
- "Get config details?" -> GET /v1/configs/{configId}
- "Update a config?" -> PUT /v1/configs/{configId}
- "Delete a config?" -> DELETE /v1/configs/{configId}
- "List all deleted-settings?" -> GET /v1/configs/{configId}/deleted-settings
- "Get environment details?" -> GET /v1/environments/{environmentId}
- "Update a environment?" -> PUT /v1/environments/{environmentId}
- "Delete a environment?" -> DELETE /v1/environments/{environmentId}
- "Get permission details?" -> GET /v1/permissions/{permissionGroupId}
- "Update a permission?" -> PUT /v1/permissions/{permissionGroupId}
- "Delete a permission?" -> DELETE /v1/permissions/{permissionGroupId}
- "Get integration details?" -> GET /v1/integrations/{integrationId}
- "Update a integration?" -> PUT /v1/integrations/{integrationId}
- "Delete a integration?" -> DELETE /v1/integrations/{integrationId}
- "List all details?" -> GET /v1/integrationLink/{integrationLinkType}/{key}/details
- "Get environment details?" -> GET /v1/configs/{configId}/environments/{environmentId}
- "List all me?" -> GET /v1/me
- "List all auditlogs?" -> GET /v1/organizations/{organizationId}/auditlogs
- "List all organization-limitations?" -> GET /v1/organizations/{organizationId}/organization-limitations
- "List all members?" -> GET /v1/organizations/{organizationId}/members
- "List all members?" -> GET /v2/organizations/{organizationId}/members
- "List all invitations?" -> GET /v1/organizations/{organizationId}/invitations
- "List all invitations?" -> GET /v1/products/{productId}/invitations
- "List all predefined-variations?" -> GET /v1/settings/{settingId}/predefined-variations
- "Get product details?" -> GET /v1/products/{productId}
- "Update a product?" -> PUT /v1/products/{productId}
- "Delete a product?" -> DELETE /v1/products/{productId}
- "List all members?" -> GET /v1/products/{productId}/members
- "List all preferences?" -> GET /v1/products/{productId}/preferences
- "Create a preference?" -> POST /v1/products/{productId}/preferences
- "Get segment details?" -> GET /v1/segments/{segmentId}
- "Update a segment?" -> PUT /v1/segments/{segmentId}
- "Delete a segment?" -> DELETE /v1/segments/{segmentId}
- "Get setting details?" -> GET /v1/settings/{settingId}
- "Update a setting?" -> PUT /v1/settings/{settingId}
- "Partially update a setting?" -> PATCH /v1/settings/{settingId}
- "Delete a setting?" -> DELETE /v1/settings/{settingId}
- "List all settings?" -> GET /v1/tags/{tagId}/settings
- "List all value?" -> GET /v1/settings/{settingKeyOrId}/value
- "List all value?" -> GET /v1/environments/{environmentId}/settings/{settingId}/value
- "List all value?" -> GET /v2/settings/{settingKeyOrId}/value
- "List all value?" -> GET /v2/environments/{environmentId}/settings/{settingId}/value
- "List all values?" -> GET /v1/configs/{configId}/environments/{environmentId}/values
- "Create a value?" -> POST /v1/configs/{configId}/environments/{environmentId}/values
- "List all values?" -> GET /v2/configs/{configId}/environments/{environmentId}/values
- "Create a value?" -> POST /v2/configs/{configId}/environments/{environmentId}/values
- "Get tag details?" -> GET /v1/tags/{tagId}
- "Update a tag?" -> PUT /v1/tags/{tagId}
- "Delete a tag?" -> DELETE /v1/tags/{tagId}
- "Get webhook details?" -> GET /v1/webhooks/{webhookId}
- "Update a webhook?" -> PUT /v1/webhooks/{webhookId}
- "Partially update a webhook?" -> PATCH /v1/webhooks/{webhookId}
- "Delete a webhook?" -> DELETE /v1/webhooks/{webhookId}
- "List all keys?" -> GET /v1/webhooks/{webhookId}/keys
- "List all sdk-keys?" -> GET /v1/proxy-profiles/{proxyProfileId}/sdk-keys
- "Delete a integrationLink?" -> DELETE /v1/environments/{environmentId}/settings/{settingId}/integrationLinks/{integrationLinkType}/{key}
- "Create a connect?" -> POST /v1/jira/connect
- "Create a product?" -> POST /v1/organizations/{organizationId}/products
- "Create a webhook?" -> POST /v1/configs/{configId}/environments/{environmentId}/webhooks
- "Create a delete-report?" -> POST /v1/code-references/delete-reports
- "Create a deselect?" -> POST /v1/proxy-profiles/{proxyProfileId}/sdk-keys/deselect
- "Create a secret?" -> POST /v1/proxy-profiles/{proxyProfileId}/secret
- "Create a invite?" -> POST /v1/products/{productId}/members/invite
- "Create a code-reference?" -> POST /v1/code-references
- "Create a select?" -> POST /v1/proxy-profiles/{proxyProfileId}/sdk-keys/select
- "Delete a member?" -> DELETE /v1/organizations/{organizationId}/members/{userId}
- "Delete a invitation?" -> DELETE /v1/invitations/{invitationId}
- "Delete a member?" -> DELETE /v1/products/{productId}/members/{userId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
