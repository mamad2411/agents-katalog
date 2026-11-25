---
name: turbine-labs-api
description: "Turbine Labs API skill. Use when working with Turbine Labs for admin, changelog, zone. Covers 44 endpoints."
version: 1.0.0
generator: lapsh
---

# Turbine Labs API
API version: 1.0

## Auth
ApiKey Authorization in header

## Base URL
https://api.turbinelabs.io/v1.0

## Setup
1. Set your API key in the appropriate header
2. GET /admin/user/self -- verify access
3. POST /admin/user/self/access_tokens -- create first access_tokens

## Endpoints

44 endpoints across 9 groups. See references/api-spec.lap for full details.

### admin
| Method | Path | Description |
|--------|------|-------------|
| GET | /admin/user/self | Returns the user object for the account authorized and making this request. |
| GET | /admin/user/self/access_tokens | Lists Access Tokens that are configured for the authenticated user. |
| POST | /admin/user/self/access_tokens | Creates a new Access Token and associates it with the authenticated user. |
| DELETE | /admin/user/self/access_token/{access-token-key} | Delete the specified access token. |

### changelog
| Method | Path | Description |
|--------|------|-------------|
| GET | /changelog/adhoc | Allows an arbitrary filter to be specified and applied to the org\'s change log. |
| GET | /changelog/domain-graph/{domainKey} | get changes related to the indicated domain |
| GET | /changelog/route-graph/{routeKey} | get changes related to the indicated route |
| GET | /changelog/shared-rules-graph/{sharedRulesKey} | get changes related to the indicated SharedRules |
| GET | /changelog/cluster-graph/{clusterKey} | get changes related to the indicated cluster |
| GET | /changelog/zone/{zoneKey} | get changes in a specified zone |

### zone
| Method | Path | Description |
|--------|------|-------------|
| GET | /zone | get a list of zones |
| POST | /zone | create zone |
| GET | /zone/{zoneKey} | get zone |
| DELETE | /zone/{zoneKey} | delete zone |

### domain
| Method | Path | Description |
|--------|------|-------------|
| GET | /domain | get domains |
| POST | /domain | create domain |
| GET | /domain/{domainKey} | get domain |
| DELETE | /domain/{domainKey} | delete domain |

### proxy
| Method | Path | Description |
|--------|------|-------------|
| GET | /proxy | list proxies |
| POST | /proxy | create proxy |
| GET | /proxy/{proxyKey} | get proxy |
| DELETE | /proxy/{proxyKey} | delete proxy |

### listener
| Method | Path | Description |
|--------|------|-------------|
| GET | /listener | list listeners |
| POST | /listener | create listener |
| GET | /listener/{listenerKey} | get listener |
| PUT | /listener/{listenerKey} | modify listener |
| DELETE | /listener/{listenerKey} | delete listener |

### shared_rules
| Method | Path | Description |
|--------|------|-------------|
| GET | /shared_rules | get shared_rules |
| POST | /shared_rules | create shared_rules |
| GET | /shared_rules/{sharedRulesKey} | get shared_rules object |
| PUT | /shared_rules/{sharedRulesKey} | modify shared_rules object |
| DELETE | /shared_rules/{sharedRulesKey} | delete shared_rules object |

### route
| Method | Path | Description |
|--------|------|-------------|
| GET | /route | get routes |
| POST | /route | create route |
| GET | /route/{routeKey} | get route |
| PUT | /route/{routeKey} | modify route |
| DELETE | /route/{routeKey} | delete route |

### cluster
| Method | Path | Description |
|--------|------|-------------|
| GET | /cluster | get clusters |
| POST | /cluster | create cluster |
| GET | /cluster/{clusterKey} | get cluster |
| PUT | /cluster/{clusterKey} | modify cluster |
| DELETE | /cluster/{clusterKey} | delete cluster |
| POST | /cluster/{clusterKey}/instances | add instance |
| DELETE | /cluster/{clusterKey}/instances/{instanceIdentifier} | remove instance |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all self?" -> GET /admin/user/self
- "List all access_tokens?" -> GET /admin/user/self/access_tokens
- "Create a access_token?" -> POST /admin/user/self/access_tokens
- "Delete a access_token?" -> DELETE /admin/user/self/access_token/{access-token-key}
- "List all adhoc?" -> GET /changelog/adhoc
- "Get domain-graph details?" -> GET /changelog/domain-graph/{domainKey}
- "Get route-graph details?" -> GET /changelog/route-graph/{routeKey}
- "Get shared-rules-graph details?" -> GET /changelog/shared-rules-graph/{sharedRulesKey}
- "Get cluster-graph details?" -> GET /changelog/cluster-graph/{clusterKey}
- "Get zone details?" -> GET /changelog/zone/{zoneKey}
- "List all zone?" -> GET /zone
- "Create a zone?" -> POST /zone
- "Get zone details?" -> GET /zone/{zoneKey}
- "Delete a zone?" -> DELETE /zone/{zoneKey}
- "List all domain?" -> GET /domain
- "Create a domain?" -> POST /domain
- "Get domain details?" -> GET /domain/{domainKey}
- "Delete a domain?" -> DELETE /domain/{domainKey}
- "List all proxy?" -> GET /proxy
- "Create a proxy?" -> POST /proxy
- "Get proxy details?" -> GET /proxy/{proxyKey}
- "Delete a proxy?" -> DELETE /proxy/{proxyKey}
- "List all listener?" -> GET /listener
- "Create a listener?" -> POST /listener
- "Get listener details?" -> GET /listener/{listenerKey}
- "Update a listener?" -> PUT /listener/{listenerKey}
- "Delete a listener?" -> DELETE /listener/{listenerKey}
- "List all shared_rules?" -> GET /shared_rules
- "Create a shared_rule?" -> POST /shared_rules
- "Get shared_rule details?" -> GET /shared_rules/{sharedRulesKey}
- "Update a shared_rule?" -> PUT /shared_rules/{sharedRulesKey}
- "Delete a shared_rule?" -> DELETE /shared_rules/{sharedRulesKey}
- "List all route?" -> GET /route
- "Create a route?" -> POST /route
- "Get route details?" -> GET /route/{routeKey}
- "Update a route?" -> PUT /route/{routeKey}
- "Delete a route?" -> DELETE /route/{routeKey}
- "List all cluster?" -> GET /cluster
- "Create a cluster?" -> POST /cluster
- "Get cluster details?" -> GET /cluster/{clusterKey}
- "Update a cluster?" -> PUT /cluster/{clusterKey}
- "Delete a cluster?" -> DELETE /cluster/{clusterKey}
- "Create a instance?" -> POST /cluster/{clusterKey}/instances
- "Delete a instance?" -> DELETE /cluster/{clusterKey}/instances/{instanceIdentifier}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
