---
name: hookdeck-admin-rest-api
description: "Hookdeck Admin REST API skill. Use when working with Hookdeck Admin REST for issue-triggers, attempts, bookmarks. Covers 101 endpoints."
version: 1.0.0
generator: lapsh
---

# Hookdeck Admin REST API
API version: 1.0.0

## Auth
Bearer bearer | Bearer basic

## Base URL
https://api.hookdeck.com/2024-09-01

## Setup
1. Set Authorization header with your Bearer token
2. GET /issue-triggers -- verify access
3. POST /issue-triggers -- create first issue-triggers

## Endpoints

101 endpoints across 14 groups. See references/api-spec.lap for full details.

### issue-triggers
| Method | Path | Description |
|--------|------|-------------|
| GET | /issue-triggers | Get issue triggers |
| POST | /issue-triggers | Create an issue trigger |
| PUT | /issue-triggers | Create or update an issue trigger |
| GET | /issue-triggers/{id} | Get a single issue trigger |
| PUT | /issue-triggers/{id} | Update an issue trigger |
| DELETE | /issue-triggers/{id} | Delete an issue trigger |
| PUT | /issue-triggers/{id}/disable | Disable an issue trigger |
| PUT | /issue-triggers/{id}/enable | Enable an issue trigger |

### attempts
| Method | Path | Description |
|--------|------|-------------|
| GET | /attempts | Get attempts |
| GET | /attempts/{id} | Get a single attempt |

### bookmarks
| Method | Path | Description |
|--------|------|-------------|
| GET | /bookmarks | Get bookmarks |
| POST | /bookmarks | Create a bookmark |
| GET | /bookmarks/{id} | Get a single bookmark |
| PUT | /bookmarks/{id} | Update a bookmark |
| DELETE | /bookmarks/{id} | Delete a bookmark |
| GET | /bookmarks/{id}/raw_body | Get a bookmark raw body data |
| POST | /bookmarks/{id}/trigger | Trigger a bookmark |

### destinations
| Method | Path | Description |
|--------|------|-------------|
| GET | /destinations | Get destinations |
| POST | /destinations | Create a destination |
| PUT | /destinations | Update or create a destination |
| GET | /destinations/{id} | Get a destination |
| PUT | /destinations/{id} | Update a destination |
| DELETE | /destinations/{id} | Delete a destination |
| PUT | /destinations/{id}/disable | Disable a destination |
| PUT | /destinations/{id}/archive | Disable a destination |
| PUT | /destinations/{id}/enable | Enable a destination |
| PUT | /destinations/{id}/unarchive | Enable a destination |

### bulk
| Method | Path | Description |
|--------|------|-------------|
| GET | /bulk/events/retry | Get events bulk retries |
| POST | /bulk/events/retry | Create an events bulk retry |
| GET | /bulk/events/retry/plan | Generate an events bulk retry plan |
| GET | /bulk/events/retry/{id} | Get an events bulk retry |
| POST | /bulk/events/retry/{id}/cancel | Cancel an events bulk retry |
| GET | /bulk/ignored-events/retry | Get ignored events bulk retries |
| POST | /bulk/ignored-events/retry | Create an ignored events bulk retry |
| GET | /bulk/ignored-events/retry/plan | Generate an ignored events bulk retry plan |
| GET | /bulk/ignored-events/retry/{id} | Get an ignored events bulk retry |
| POST | /bulk/ignored-events/retry/{id}/cancel | Cancel an ignored events bulk retry |
| GET | /bulk/requests/retry | Get request bulk retries |
| POST | /bulk/requests/retry | Create a requests bulk retry |
| GET | /bulk/requests/retry/plan | Generate a requests bulk retry plan |
| GET | /bulk/requests/retry/{id} | Get a requests bulk retry |
| POST | /bulk/requests/retry/{id}/cancel | Cancel a requests bulk retry |

### events
| Method | Path | Description |
|--------|------|-------------|
| GET | /events | Get events |
| GET | /events/{id} | Get an event |
| GET | /events/{id}/raw_body | Get a event raw body data |
| POST | /events/{id}/retry | Retry an event |
| PUT | /events/{id}/mute | Mute an event |

### integrations
| Method | Path | Description |
|--------|------|-------------|
| GET | /integrations | Get integrations |
| POST | /integrations | Create an integration |
| GET | /integrations/{id} | Get an integration |
| PUT | /integrations/{id} | Update an integration |
| DELETE | /integrations/{id} | Delete an integration |
| PUT | /integrations/{id}/attach/{source_id} | Attach an integration to a source |
| PUT | /integrations/{id}/detach/{source_id} | Detach an integration from a source |

### issues
| Method | Path | Description |
|--------|------|-------------|
| GET | /issues | Get issues |
| GET | /issues/count | Get the number of issues |
| GET | /issues/{id} | Get a single issue |
| PUT | /issues/{id} | Update issue |
| DELETE | /issues/{id} | Dismiss an issue |

### requests
| Method | Path | Description |
|--------|------|-------------|
| GET | /requests | Get requests |
| GET | /requests/{id} | Get a request |
| GET | /requests/{id}/raw_body | Get a request raw body data |
| POST | /requests/{id}/retry | Retry a request |
| GET | /requests/{id}/events | Get request events |
| GET | /requests/{id}/ignored_events | Get request ignored events |

### sources
| Method | Path | Description |
|--------|------|-------------|
| GET | /sources | Get sources |
| POST | /sources | Create a source |
| PUT | /sources | Update or create a source |
| GET | /sources/{id} | Get a source |
| PUT | /sources/{id} | Update a source |
| DELETE | /sources/{id} | Delete a source |
| PUT | /sources/{id}/disable | Disable a source |
| PUT | /sources/{id}/archive | Disable a source |
| PUT | /sources/{id}/enable | Enable a source |
| PUT | /sources/{id}/unarchive | Enable a source |

### notifications
| Method | Path | Description |
|--------|------|-------------|
| PUT | /notifications/webhooks | Toggle webhook notifications for the project |

### teams
| Method | Path | Description |
|--------|------|-------------|
| POST | /teams/current/custom_domains | Add a custom domain to the project |
| GET | /teams/current/custom_domains | List all custom domains and their verification statuses for the project |
| DELETE | /teams/current/custom_domains/{domain_id} | Removes a custom domain from the project |

### transformations
| Method | Path | Description |
|--------|------|-------------|
| GET | /transformations | Get transformations |
| POST | /transformations | Create a transformation |
| PUT | /transformations | Update or create a transformation |
| GET | /transformations/{id} | Get a transformation |
| DELETE | /transformations/{id} | Delete a transformation |
| PUT | /transformations/{id} | Update a transformation |
| PUT | /transformations/run | Test a transformation code |
| GET | /transformations/{id}/executions | Get transformation executions |
| GET | /transformations/{id}/executions/{execution_id} | Get a transformation execution |

### connections
| Method | Path | Description |
|--------|------|-------------|
| GET | /connections | Get connections |
| POST | /connections | Create a connection |
| PUT | /connections | Update or create a connection |
| GET | /connections/count | Count connections |
| GET | /connections/{id} | Get a single connection |
| PUT | /connections/{id} | Update a connection |
| DELETE | /connections/{id} | Delete a connection |
| PUT | /connections/{id}/disable | Disable a connection |
| PUT | /connections/{id}/archive | Disable a connection |
| PUT | /connections/{id}/enable | Enable a connection |
| PUT | /connections/{id}/unarchive | Enable a connection |
| PUT | /connections/{id}/pause | Pause a connection |
| PUT | /connections/{id}/unpause | Unpause a connection |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all issue-triggers?" -> GET /issue-triggers
- "Create a issue-trigger?" -> POST /issue-triggers
- "Get issue-trigger details?" -> GET /issue-triggers/{id}
- "Update a issue-trigger?" -> PUT /issue-triggers/{id}
- "Delete a issue-trigger?" -> DELETE /issue-triggers/{id}
- "List all attempts?" -> GET /attempts
- "Get attempt details?" -> GET /attempts/{id}
- "List all bookmarks?" -> GET /bookmarks
- "Create a bookmark?" -> POST /bookmarks
- "Get bookmark details?" -> GET /bookmarks/{id}
- "Update a bookmark?" -> PUT /bookmarks/{id}
- "Delete a bookmark?" -> DELETE /bookmarks/{id}
- "List all raw_body?" -> GET /bookmarks/{id}/raw_body
- "Create a trigger?" -> POST /bookmarks/{id}/trigger
- "List all destinations?" -> GET /destinations
- "Create a destination?" -> POST /destinations
- "Get destination details?" -> GET /destinations/{id}
- "Update a destination?" -> PUT /destinations/{id}
- "Delete a destination?" -> DELETE /destinations/{id}
- "Search retry?" -> GET /bulk/events/retry
- "Create a retry?" -> POST /bulk/events/retry
- "Search plan?" -> GET /bulk/events/retry/plan
- "Get retry details?" -> GET /bulk/events/retry/{id}
- "Create a cancel?" -> POST /bulk/events/retry/{id}/cancel
- "List all events?" -> GET /events
- "Get event details?" -> GET /events/{id}
- "List all raw_body?" -> GET /events/{id}/raw_body
- "Create a retry?" -> POST /events/{id}/retry
- "Search retry?" -> GET /bulk/ignored-events/retry
- "Create a retry?" -> POST /bulk/ignored-events/retry
- "Search plan?" -> GET /bulk/ignored-events/retry/plan
- "Get retry details?" -> GET /bulk/ignored-events/retry/{id}
- "Create a cancel?" -> POST /bulk/ignored-events/retry/{id}/cancel
- "List all integrations?" -> GET /integrations
- "Create a integration?" -> POST /integrations
- "Get integration details?" -> GET /integrations/{id}
- "Update a integration?" -> PUT /integrations/{id}
- "Delete a integration?" -> DELETE /integrations/{id}
- "Update a attach?" -> PUT /integrations/{id}/attach/{source_id}
- "Update a detach?" -> PUT /integrations/{id}/detach/{source_id}
- "List all issues?" -> GET /issues
- "List all count?" -> GET /issues/count
- "Get issue details?" -> GET /issues/{id}
- "Update a issue?" -> PUT /issues/{id}
- "Delete a issue?" -> DELETE /issues/{id}
- "List all requests?" -> GET /requests
- "Get request details?" -> GET /requests/{id}
- "List all raw_body?" -> GET /requests/{id}/raw_body
- "Create a retry?" -> POST /requests/{id}/retry
- "List all events?" -> GET /requests/{id}/events
- "List all ignored_events?" -> GET /requests/{id}/ignored_events
- "Search retry?" -> GET /bulk/requests/retry
- "Create a retry?" -> POST /bulk/requests/retry
- "Search plan?" -> GET /bulk/requests/retry/plan
- "Get retry details?" -> GET /bulk/requests/retry/{id}
- "Create a cancel?" -> POST /bulk/requests/retry/{id}/cancel
- "List all sources?" -> GET /sources
- "Create a source?" -> POST /sources
- "Get source details?" -> GET /sources/{id}
- "Update a source?" -> PUT /sources/{id}
- "Delete a source?" -> DELETE /sources/{id}
- "Create a custom_domain?" -> POST /teams/current/custom_domains
- "List all custom_domains?" -> GET /teams/current/custom_domains
- "Delete a custom_domain?" -> DELETE /teams/current/custom_domains/{domain_id}
- "List all transformations?" -> GET /transformations
- "Create a transformation?" -> POST /transformations
- "Get transformation details?" -> GET /transformations/{id}
- "Delete a transformation?" -> DELETE /transformations/{id}
- "Update a transformation?" -> PUT /transformations/{id}
- "List all executions?" -> GET /transformations/{id}/executions
- "Get execution details?" -> GET /transformations/{id}/executions/{execution_id}
- "List all connections?" -> GET /connections
- "Create a connection?" -> POST /connections
- "List all count?" -> GET /connections/count
- "Get connection details?" -> GET /connections/{id}
- "Update a connection?" -> PUT /connections/{id}
- "Delete a connection?" -> DELETE /connections/{id}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
