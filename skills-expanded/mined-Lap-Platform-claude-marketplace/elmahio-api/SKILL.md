---
name: elmahio-api
description: "elmah.io API skill. Use when working with elmah.io for deployments, heartbeats, installations. Covers 24 endpoints."
version: 1.0.0
generator: lapsh
---

# elmah.io API
API version: v3

## Auth
ApiKey api_key in query

## Base URL
Not specified.

## Setup
1. Set your API key in the appropriate header
2. GET /v3/deployments -- verify access
3. POST /v3/deployments -- create first deployments

## Endpoints

24 endpoints across 7 groups. See references/api-spec.lap for full details.

### deployments
| Method | Path | Description |
|--------|------|-------------|
| GET | /v3/deployments | Fetch a list of deployments. |
| POST | /v3/deployments | Create a new deployment. |
| GET | /v3/deployments/{id} | Fetch a deployment by its ID. |
| DELETE | /v3/deployments/{id} | Delete a deployment by its ID. |

### heartbeats
| Method | Path | Description |
|--------|------|-------------|
| POST | /v3/heartbeats/{logId}/{id} | Create a new heartbeat. |

### installations
| Method | Path | Description |
|--------|------|-------------|
| POST | /v3/installations/{logId} | Create a new installation. |

### logs
| Method | Path | Description |
|--------|------|-------------|
| GET | /v3/logs | Fetch a list of logs. |
| POST | /v3/logs | Create a new log. |
| GET | /v3/logs/{id} | Fetch a log by its ID. |
| DELETE | /v3/logs/{id} | Delete a log by its ID. |
| POST | /v3/logs/{id}/_disable | Disable a log by its ID. |
| POST | /v3/logs/{id}/_enable | Enable a log by its ID. |
| GET | /v3/logs/{id}/_diagnose | Help diagnose logging problems. |

### messages
| Method | Path | Description |
|--------|------|-------------|
| GET | /v3/messages/{logId} | Fetch messages from a log. |
| DELETE | /v3/messages/{logId} | Deletes a list of messages by logid and query. |
| POST | /v3/messages/{logId} | Create a new message. |
| GET | /v3/messages/{logId}/{id} | Fetch a message by its ID. |
| DELETE | /v3/messages/{logId}/{id} | Delete a message by its ID. |
| POST | /v3/messages/{logId}/_fix | Mark a list of messages as fixed by logid and query. |
| POST | /v3/messages/{logId}/{id}/_hide | Hide a message by its ID. |
| POST | /v3/messages/{logId}/{id}/_fix | Fix a message by its ID. |
| POST | /v3/messages/{logId}/_bulk | Create one or more new messages. |

### sourcemaps
| Method | Path | Description |
|--------|------|-------------|
| POST | /v3/sourcemaps/{logId} | Create or update a translation between a minified JavaScript path to the minified JavaScript and source map files. |

### uptimechecks
| Method | Path | Description |
|--------|------|-------------|
| GET | /v3/uptimechecks | Fetch a list of uptime checks. Currently in closed beta. Get in contact to get access to this endpoint. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all deployments?" -> GET /v3/deployments
- "Create a deployment?" -> POST /v3/deployments
- "Get deployment details?" -> GET /v3/deployments/{id}
- "Delete a deployment?" -> DELETE /v3/deployments/{id}
- "List all logs?" -> GET /v3/logs
- "Create a log?" -> POST /v3/logs
- "Get log details?" -> GET /v3/logs/{id}
- "Delete a log?" -> DELETE /v3/logs/{id}
- "Create a _disable?" -> POST /v3/logs/{id}/_disable
- "Create a _enable?" -> POST /v3/logs/{id}/_enable
- "List all _diagnose?" -> GET /v3/logs/{id}/_diagnose
- "Search messages?" -> GET /v3/messages/{logId}
- "Delete a message?" -> DELETE /v3/messages/{logId}
- "Get message details?" -> GET /v3/messages/{logId}/{id}
- "Delete a message?" -> DELETE /v3/messages/{logId}/{id}
- "Create a _fix?" -> POST /v3/messages/{logId}/_fix
- "Create a _hide?" -> POST /v3/messages/{logId}/{id}/_hide
- "Create a _fix?" -> POST /v3/messages/{logId}/{id}/_fix
- "Create a _bulk?" -> POST /v3/messages/{logId}/_bulk
- "List all uptimechecks?" -> GET /v3/uptimechecks
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
