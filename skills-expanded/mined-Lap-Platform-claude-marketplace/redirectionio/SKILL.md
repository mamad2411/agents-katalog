---
name: redirectionio
description: "redirection.io API skill. Use when working with redirection.io for domains, drafts, instances. Covers 24 endpoints."
version: 1.0.0
generator: lapsh
---

# redirection.io
API version: 2.0.0

## Auth
Bearer bearer | ApiKey Authorization in header

## Base URL
https://api.redirection.io/

## Setup
1. Set Authorization header with your Bearer token
2. GET /domains -- verify access
3. POST /domains -- create first domains

## Endpoints

24 endpoints across 8 groups. See references/api-spec.lap for full details.

### domains
| Method | Path | Description |
|--------|------|-------------|
| GET | /domains | Retrieves the collection of the domains. |
| POST | /domains | Creates a new domain |
| DELETE | /domains/{id} | Permanently deletes a domain |
| GET | /domains/{id} | Retrieves a ProjectDomain resource. |

### drafts
| Method | Path | Description |
|--------|------|-------------|
| GET | /drafts | Retrieves the collection of Draft rules |
| DELETE | /drafts/{id} | Deletes a Draft |
| GET | /drafts/{id} | Retrieves a Draft resource. |

### instances
| Method | Path | Description |
|--------|------|-------------|
| GET | /instances | List project instances |
| DELETE | /instances/{id} | Delete an instance |
| GET | /instances/{id} | Retrieves a Instance resource. |

### ips
| Method | Path | Description |
|--------|------|-------------|
| GET | /ips | Retrieves the collection of Ip resources. |

### organization
| Method | Path | Description |
|--------|------|-------------|
| GET | /organization | Retrieve the details of your organization |

### projects
| Method | Path | Description |
|--------|------|-------------|
| GET | /projects | Retrieves the collection of Project resources. |
| POST | /projects | Creates a new project |
| DELETE | /projects/{id} | Permanently deletes a project |
| GET | /projects/{id} | Retrieves a Project resource. |
| POST | /projects/{id}/publish | Publishes the collection of Draft resources |

### redirections
| Method | Path | Description |
|--------|------|-------------|
| POST | /redirections | Creates a new Redirection |

### rules
| Method | Path | Description |
|--------|------|-------------|
| GET | /rules | Retrieves the collection of currently published Rule resources. |
| POST | /rules | Creates a new draft Rule |
| DELETE | /rules/{id} | Deletes a Rule |
| GET | /rules/{id} | Retrieves a Rule resource |
| PUT | /rules/{id} | Updates an existing Rule |
| GET | /rules/{id}/statistics | Retrieves the usage statistics of a rule. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all domains?" -> GET /domains
- "Create a domain?" -> POST /domains
- "Delete a domain?" -> DELETE /domains/{id}
- "Get domain details?" -> GET /domains/{id}
- "List all drafts?" -> GET /drafts
- "Delete a draft?" -> DELETE /drafts/{id}
- "Get draft details?" -> GET /drafts/{id}
- "List all instances?" -> GET /instances
- "Delete a instance?" -> DELETE /instances/{id}
- "Get instance details?" -> GET /instances/{id}
- "List all ips?" -> GET /ips
- "List all organization?" -> GET /organization
- "List all projects?" -> GET /projects
- "Create a project?" -> POST /projects
- "Delete a project?" -> DELETE /projects/{id}
- "Get project details?" -> GET /projects/{id}
- "Create a publish?" -> POST /projects/{id}/publish
- "Create a redirection?" -> POST /redirections
- "List all rules?" -> GET /rules
- "Create a rule?" -> POST /rules
- "Delete a rule?" -> DELETE /rules/{id}
- "Get rule details?" -> GET /rules/{id}
- "Update a rule?" -> PUT /rules/{id}
- "List all statistics?" -> GET /rules/{id}/statistics
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
