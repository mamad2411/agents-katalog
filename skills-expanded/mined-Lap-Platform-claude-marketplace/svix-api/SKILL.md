---
name: svix-api
description: "Svix API skill. Use when working with Svix for api, ingest. Covers 128 endpoints."
version: 1.0.0
generator: lapsh
---

# Svix API
API version: 1.84.0

## Auth
Bearer bearer

## Base URL
https://api.eu.svix.com/

## Setup
1. Set Authorization header with your Bearer token
2. GET /api/v1/app -- verify access
3. POST /api/v1/app -- create first app

## Endpoints

128 endpoints across 2 groups. See references/api-spec.lap for full details.

### api
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/v1/app | List Applications |
| POST | /api/v1/app | Create Application |
| GET | /api/v1/app/{app_id} | Get Application |
| PUT | /api/v1/app/{app_id} | Update Application |
| DELETE | /api/v1/app/{app_id} | Delete Application |
| PATCH | /api/v1/app/{app_id} | Patch Application |
| GET | /api/v1/app/{app_id}/attempt/endpoint/{endpoint_id} | List Attempts By Endpoint |
| GET | /api/v1/app/{app_id}/attempt/msg/{msg_id} | List Attempts By Msg |
| GET | /api/v1/app/{app_id}/endpoint | List Endpoints |
| POST | /api/v1/app/{app_id}/endpoint | Create Endpoint |
| GET | /api/v1/app/{app_id}/endpoint/{endpoint_id} | Get Endpoint |
| PUT | /api/v1/app/{app_id}/endpoint/{endpoint_id} | Update Endpoint |
| DELETE | /api/v1/app/{app_id}/endpoint/{endpoint_id} | Delete Endpoint |
| PATCH | /api/v1/app/{app_id}/endpoint/{endpoint_id} | Patch Endpoint |
| POST | /api/v1/app/{app_id}/endpoint/{endpoint_id}/bulk-replay | Bulk Replay Messages |
| GET | /api/v1/app/{app_id}/endpoint/{endpoint_id}/headers | Get Endpoint Headers |
| PUT | /api/v1/app/{app_id}/endpoint/{endpoint_id}/headers | Update Endpoint Headers |
| PATCH | /api/v1/app/{app_id}/endpoint/{endpoint_id}/headers | Patch Endpoint Headers |
| GET | /api/v1/app/{app_id}/endpoint/{endpoint_id}/msg | List Attempted Messages |
| POST | /api/v1/app/{app_id}/endpoint/{endpoint_id}/recover | Recover Failed Webhooks |
| POST | /api/v1/app/{app_id}/endpoint/{endpoint_id}/replay-missing | Replay Missing Webhooks |
| GET | /api/v1/app/{app_id}/endpoint/{endpoint_id}/secret | Get Endpoint Secret |
| POST | /api/v1/app/{app_id}/endpoint/{endpoint_id}/secret/rotate | Rotate Endpoint Secret |
| POST | /api/v1/app/{app_id}/endpoint/{endpoint_id}/send-example | Send Event Type Example Message |
| GET | /api/v1/app/{app_id}/endpoint/{endpoint_id}/stats | Endpoint Stats |
| GET | /api/v1/app/{app_id}/endpoint/{endpoint_id}/transformation | Get Endpoint Transformation |
| PATCH | /api/v1/app/{app_id}/endpoint/{endpoint_id}/transformation | Patch Endpoint Transformation |
| GET | /api/v1/app/{app_id}/integration | List Integrations |
| POST | /api/v1/app/{app_id}/integration | Create Integration |
| GET | /api/v1/app/{app_id}/integration/{integ_id} | Get Integration |
| PUT | /api/v1/app/{app_id}/integration/{integ_id} | Update Integration |
| DELETE | /api/v1/app/{app_id}/integration/{integ_id} | Delete Integration |
| GET | /api/v1/app/{app_id}/integration/{integ_id}/key | Get Integration Key |
| POST | /api/v1/app/{app_id}/integration/{integ_id}/key/rotate | Rotate Integration Key |
| GET | /api/v1/app/{app_id}/msg | List Messages |
| POST | /api/v1/app/{app_id}/msg | Create Message |
| POST | /api/v1/app/{app_id}/msg/expunge-all-contents | Expunge all message contents |
| POST | /api/v1/app/{app_id}/msg/precheck/active | Create Message Precheck |
| GET | /api/v1/app/{app_id}/msg/{msg_id} | Get Message |
| GET | /api/v1/app/{app_id}/msg/{msg_id}/attempt/{attempt_id} | Get Attempt |
| DELETE | /api/v1/app/{app_id}/msg/{msg_id}/attempt/{attempt_id}/content | Delete attempt response body |
| DELETE | /api/v1/app/{app_id}/msg/{msg_id}/content | Delete message payload |
| GET | /api/v1/app/{app_id}/msg/{msg_id}/endpoint | List Attempted Destinations |
| POST | /api/v1/app/{app_id}/msg/{msg_id}/endpoint/{endpoint_id}/resend | Resend Webhook |
| GET | /api/v1/app/{app_id}/poller/{sink_id} | Poller Poll |
| GET | /api/v1/app/{app_id}/poller/{sink_id}/consumer/{consumer_id} | Poller Consumer Poll |
| POST | /api/v1/app/{app_id}/poller/{sink_id}/consumer/{consumer_id}/seek | Poller Consumer Seek |
| POST | /api/v1/auth/app-portal-access/{app_id} | Get Consumer App Portal Access |
| POST | /api/v1/auth/app/{app_id}/expire-all | Expire All |
| POST | /api/v1/auth/logout | Logout |
| POST | /api/v1/auth/stream-logout | Stream Logout |
| POST | /api/v1/auth/stream-portal-access/{stream_id} | Get Stream Portal Access |
| POST | /api/v1/auth/stream/{stream_id}/expire-all | Stream Expire All |
| GET | /api/v1/auth/stream/{stream_id}/sink/{sink_id}/poller/token | Get Poller Token |
| POST | /api/v1/auth/stream/{stream_id}/sink/{sink_id}/poller/token/rotate | Rotate Poller Token |
| GET | /api/v1/background-task | List Background Tasks |
| GET | /api/v1/background-task/{task_id} | Get Background Task |
| GET | /api/v1/connector | List Connectors |
| POST | /api/v1/connector | Create Connector |
| GET | /api/v1/connector/{connector_id} | Get Connector |
| PUT | /api/v1/connector/{connector_id} | Update Connector |
| DELETE | /api/v1/connector/{connector_id} | Delete Connector |
| PATCH | /api/v1/connector/{connector_id} | Patch Connector |
| POST | /api/v1/environment/export | Export Environment Configuration |
| POST | /api/v1/environment/import | Import Environment Configuration |
| GET | /api/v1/event-type | List Event Types |
| POST | /api/v1/event-type | Create Event Type |
| POST | /api/v1/event-type/import/openapi | Event Type Import From Openapi |
| GET | /api/v1/event-type/{event_type_name} | Get Event Type |
| PUT | /api/v1/event-type/{event_type_name} | Update Event Type |
| DELETE | /api/v1/event-type/{event_type_name} | Delete Event Type |
| PATCH | /api/v1/event-type/{event_type_name} | Patch Event Type |
| GET | /api/v1/health | Health |
| GET | /api/v1/operational-webhook/endpoint | List Operational Webhook Endpoints |
| POST | /api/v1/operational-webhook/endpoint | Create Operational Webhook Endpoint |
| GET | /api/v1/operational-webhook/endpoint/{endpoint_id} | Get Operational Webhook Endpoint |
| PUT | /api/v1/operational-webhook/endpoint/{endpoint_id} | Update Operational Webhook Endpoint |
| DELETE | /api/v1/operational-webhook/endpoint/{endpoint_id} | Delete Operational Webhook Endpoint |
| GET | /api/v1/operational-webhook/endpoint/{endpoint_id}/headers | Get Operational Webhook Endpoint Headers |
| PUT | /api/v1/operational-webhook/endpoint/{endpoint_id}/headers | Update Operational Webhook Endpoint Headers |
| GET | /api/v1/operational-webhook/endpoint/{endpoint_id}/secret | Get Operational Webhook Endpoint Secret |
| POST | /api/v1/operational-webhook/endpoint/{endpoint_id}/secret/rotate | Rotate Operational Webhook Endpoint Secret |
| POST | /api/v1/stats/usage/app | Aggregate App Stats |
| PUT | /api/v1/stats/usage/event-types | Aggregate Event Types |
| GET | /api/v1/stream | List Streams |
| POST | /api/v1/stream | Create Stream |
| GET | /api/v1/stream/event-type | List Stream Event Types |
| POST | /api/v1/stream/event-type | Create Stream Event Type |
| GET | /api/v1/stream/event-type/{name} | Get Stream Event Type |
| PUT | /api/v1/stream/event-type/{name} | Update Stream Event Type |
| DELETE | /api/v1/stream/event-type/{name} | Delete Stream Event Type |
| PATCH | /api/v1/stream/event-type/{name} | Patch Stream Event Type |
| GET | /api/v1/stream/{stream_id} | Get Stream |
| PUT | /api/v1/stream/{stream_id} | Update Stream |
| DELETE | /api/v1/stream/{stream_id} | Delete Stream |
| PATCH | /api/v1/stream/{stream_id} | Patch Stream |
| POST | /api/v1/stream/{stream_id}/events | Create Events |
| GET | /api/v1/stream/{stream_id}/sink | List Sinks |
| POST | /api/v1/stream/{stream_id}/sink | Create Sink |
| GET | /api/v1/stream/{stream_id}/sink/{sink_id} | Get Sink |
| PUT | /api/v1/stream/{stream_id}/sink/{sink_id} | Update Sink |
| DELETE | /api/v1/stream/{stream_id}/sink/{sink_id} | Delete Sink |
| PATCH | /api/v1/stream/{stream_id}/sink/{sink_id} | Patch Sink |
| GET | /api/v1/stream/{stream_id}/sink/{sink_id}/events | Poller Sink Stream Events |
| GET | /api/v1/stream/{stream_id}/sink/{sink_id}/headers | Get Sink Headers |
| PATCH | /api/v1/stream/{stream_id}/sink/{sink_id}/headers | Patch Sink Headers |
| GET | /api/v1/stream/{stream_id}/sink/{sink_id}/secret | Get Sink Secret |
| POST | /api/v1/stream/{stream_id}/sink/{sink_id}/secret/rotate | Rotate Sink Secret |
| GET | /api/v1/stream/{stream_id}/sink/{sink_id}/transformation | Get Sink Transformation |
| PATCH | /api/v1/stream/{stream_id}/sink/{sink_id}/transformation | Set Sink Transformation |

### ingest
| Method | Path | Description |
|--------|------|-------------|
| GET | /ingest/api/v1/source | List Ingest Sources |
| POST | /ingest/api/v1/source | Create Ingest Source |
| GET | /ingest/api/v1/source/{source_id} | Get Ingest Source |
| PUT | /ingest/api/v1/source/{source_id} | Update Source |
| DELETE | /ingest/api/v1/source/{source_id} | Delete Ingest Source |
| POST | /ingest/api/v1/source/{source_id}/dashboard | Ingest Source Consumer Portal |
| GET | /ingest/api/v1/source/{source_id}/endpoint | List Ingest Endpoints |
| POST | /ingest/api/v1/source/{source_id}/endpoint | Create Ingest Endpoint |
| GET | /ingest/api/v1/source/{source_id}/endpoint/{endpoint_id} | Get Ingest Endpoint |
| PUT | /ingest/api/v1/source/{source_id}/endpoint/{endpoint_id} | Update Ingest Endpoint |
| DELETE | /ingest/api/v1/source/{source_id}/endpoint/{endpoint_id} | Delete Ingest Endpoint |
| GET | /ingest/api/v1/source/{source_id}/endpoint/{endpoint_id}/headers | Get Ingest Endpoint Headers |
| PUT | /ingest/api/v1/source/{source_id}/endpoint/{endpoint_id}/headers | Update Ingest Endpoint Headers |
| GET | /ingest/api/v1/source/{source_id}/endpoint/{endpoint_id}/secret | Get Ingest Endpoint Secret |
| POST | /ingest/api/v1/source/{source_id}/endpoint/{endpoint_id}/secret/rotate | Rotate Ingest Endpoint Secret |
| GET | /ingest/api/v1/source/{source_id}/endpoint/{endpoint_id}/transformation | Get Ingest Endpoint Transformation |
| PATCH | /ingest/api/v1/source/{source_id}/endpoint/{endpoint_id}/transformation | Patch Ingest Endpoint Transformation |
| POST | /ingest/api/v1/source/{source_id}/token/rotate | Rotate Ingest Token |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all app?" -> GET /api/v1/app
- "Create a app?" -> POST /api/v1/app
- "Get app details?" -> GET /api/v1/app/{app_id}
- "Update a app?" -> PUT /api/v1/app/{app_id}
- "Delete a app?" -> DELETE /api/v1/app/{app_id}
- "Partially update a app?" -> PATCH /api/v1/app/{app_id}
- "Get endpoint details?" -> GET /api/v1/app/{app_id}/attempt/endpoint/{endpoint_id}
- "Get msg details?" -> GET /api/v1/app/{app_id}/attempt/msg/{msg_id}
- "List all endpoint?" -> GET /api/v1/app/{app_id}/endpoint
- "Create a endpoint?" -> POST /api/v1/app/{app_id}/endpoint
- "Get endpoint details?" -> GET /api/v1/app/{app_id}/endpoint/{endpoint_id}
- "Update a endpoint?" -> PUT /api/v1/app/{app_id}/endpoint/{endpoint_id}
- "Delete a endpoint?" -> DELETE /api/v1/app/{app_id}/endpoint/{endpoint_id}
- "Partially update a endpoint?" -> PATCH /api/v1/app/{app_id}/endpoint/{endpoint_id}
- "Create a bulk-replay?" -> POST /api/v1/app/{app_id}/endpoint/{endpoint_id}/bulk-replay
- "List all headers?" -> GET /api/v1/app/{app_id}/endpoint/{endpoint_id}/headers
- "List all msg?" -> GET /api/v1/app/{app_id}/endpoint/{endpoint_id}/msg
- "Create a recover?" -> POST /api/v1/app/{app_id}/endpoint/{endpoint_id}/recover
- "Create a replay-missing?" -> POST /api/v1/app/{app_id}/endpoint/{endpoint_id}/replay-missing
- "List all secret?" -> GET /api/v1/app/{app_id}/endpoint/{endpoint_id}/secret
- "Create a rotate?" -> POST /api/v1/app/{app_id}/endpoint/{endpoint_id}/secret/rotate
- "Create a send-example?" -> POST /api/v1/app/{app_id}/endpoint/{endpoint_id}/send-example
- "List all stats?" -> GET /api/v1/app/{app_id}/endpoint/{endpoint_id}/stats
- "List all transformation?" -> GET /api/v1/app/{app_id}/endpoint/{endpoint_id}/transformation
- "List all integration?" -> GET /api/v1/app/{app_id}/integration
- "Create a integration?" -> POST /api/v1/app/{app_id}/integration
- "Get integration details?" -> GET /api/v1/app/{app_id}/integration/{integ_id}
- "Update a integration?" -> PUT /api/v1/app/{app_id}/integration/{integ_id}
- "Delete a integration?" -> DELETE /api/v1/app/{app_id}/integration/{integ_id}
- "List all key?" -> GET /api/v1/app/{app_id}/integration/{integ_id}/key
- "Create a rotate?" -> POST /api/v1/app/{app_id}/integration/{integ_id}/key/rotate
- "List all msg?" -> GET /api/v1/app/{app_id}/msg
- "Create a msg?" -> POST /api/v1/app/{app_id}/msg
- "Create a expunge-all-content?" -> POST /api/v1/app/{app_id}/msg/expunge-all-contents
- "Create a active?" -> POST /api/v1/app/{app_id}/msg/precheck/active
- "Get msg details?" -> GET /api/v1/app/{app_id}/msg/{msg_id}
- "Get attempt details?" -> GET /api/v1/app/{app_id}/msg/{msg_id}/attempt/{attempt_id}
- "List all endpoint?" -> GET /api/v1/app/{app_id}/msg/{msg_id}/endpoint
- "Create a resend?" -> POST /api/v1/app/{app_id}/msg/{msg_id}/endpoint/{endpoint_id}/resend
- "Get poller details?" -> GET /api/v1/app/{app_id}/poller/{sink_id}
- "Get consumer details?" -> GET /api/v1/app/{app_id}/poller/{sink_id}/consumer/{consumer_id}
- "Create a seek?" -> POST /api/v1/app/{app_id}/poller/{sink_id}/consumer/{consumer_id}/seek
- "Create a expire-all?" -> POST /api/v1/auth/app/{app_id}/expire-all
- "Create a logout?" -> POST /api/v1/auth/logout
- "Create a stream-logout?" -> POST /api/v1/auth/stream-logout
- "Create a expire-all?" -> POST /api/v1/auth/stream/{stream_id}/expire-all
- "List all token?" -> GET /api/v1/auth/stream/{stream_id}/sink/{sink_id}/poller/token
- "Create a rotate?" -> POST /api/v1/auth/stream/{stream_id}/sink/{sink_id}/poller/token/rotate
- "List all background-task?" -> GET /api/v1/background-task
- "Get background-task details?" -> GET /api/v1/background-task/{task_id}
- "List all connector?" -> GET /api/v1/connector
- "Create a connector?" -> POST /api/v1/connector
- "Get connector details?" -> GET /api/v1/connector/{connector_id}
- "Update a connector?" -> PUT /api/v1/connector/{connector_id}
- "Delete a connector?" -> DELETE /api/v1/connector/{connector_id}
- "Partially update a connector?" -> PATCH /api/v1/connector/{connector_id}
- "Create a export?" -> POST /api/v1/environment/export
- "Create a import?" -> POST /api/v1/environment/import
- "List all event-type?" -> GET /api/v1/event-type
- "Create a event-type?" -> POST /api/v1/event-type
- "Create a openapi?" -> POST /api/v1/event-type/import/openapi
- "Get event-type details?" -> GET /api/v1/event-type/{event_type_name}
- "Update a event-type?" -> PUT /api/v1/event-type/{event_type_name}
- "Delete a event-type?" -> DELETE /api/v1/event-type/{event_type_name}
- "Partially update a event-type?" -> PATCH /api/v1/event-type/{event_type_name}
- "List all health?" -> GET /api/v1/health
- "List all endpoint?" -> GET /api/v1/operational-webhook/endpoint
- "Create a endpoint?" -> POST /api/v1/operational-webhook/endpoint
- "Get endpoint details?" -> GET /api/v1/operational-webhook/endpoint/{endpoint_id}
- "Update a endpoint?" -> PUT /api/v1/operational-webhook/endpoint/{endpoint_id}
- "Delete a endpoint?" -> DELETE /api/v1/operational-webhook/endpoint/{endpoint_id}
- "List all headers?" -> GET /api/v1/operational-webhook/endpoint/{endpoint_id}/headers
- "List all secret?" -> GET /api/v1/operational-webhook/endpoint/{endpoint_id}/secret
- "Create a rotate?" -> POST /api/v1/operational-webhook/endpoint/{endpoint_id}/secret/rotate
- "Create a app?" -> POST /api/v1/stats/usage/app
- "List all stream?" -> GET /api/v1/stream
- "Create a stream?" -> POST /api/v1/stream
- "List all event-type?" -> GET /api/v1/stream/event-type
- "Create a event-type?" -> POST /api/v1/stream/event-type
- "Get event-type details?" -> GET /api/v1/stream/event-type/{name}
- "Update a event-type?" -> PUT /api/v1/stream/event-type/{name}
- "Delete a event-type?" -> DELETE /api/v1/stream/event-type/{name}
- "Partially update a event-type?" -> PATCH /api/v1/stream/event-type/{name}
- "Get stream details?" -> GET /api/v1/stream/{stream_id}
- "Update a stream?" -> PUT /api/v1/stream/{stream_id}
- "Delete a stream?" -> DELETE /api/v1/stream/{stream_id}
- "Partially update a stream?" -> PATCH /api/v1/stream/{stream_id}
- "Create a event?" -> POST /api/v1/stream/{stream_id}/events
- "List all sink?" -> GET /api/v1/stream/{stream_id}/sink
- "Create a sink?" -> POST /api/v1/stream/{stream_id}/sink
- "Get sink details?" -> GET /api/v1/stream/{stream_id}/sink/{sink_id}
- "Update a sink?" -> PUT /api/v1/stream/{stream_id}/sink/{sink_id}
- "Delete a sink?" -> DELETE /api/v1/stream/{stream_id}/sink/{sink_id}
- "Partially update a sink?" -> PATCH /api/v1/stream/{stream_id}/sink/{sink_id}
- "List all events?" -> GET /api/v1/stream/{stream_id}/sink/{sink_id}/events
- "List all headers?" -> GET /api/v1/stream/{stream_id}/sink/{sink_id}/headers
- "List all secret?" -> GET /api/v1/stream/{stream_id}/sink/{sink_id}/secret
- "Create a rotate?" -> POST /api/v1/stream/{stream_id}/sink/{sink_id}/secret/rotate
- "List all transformation?" -> GET /api/v1/stream/{stream_id}/sink/{sink_id}/transformation
- "List all source?" -> GET /ingest/api/v1/source
- "Create a source?" -> POST /ingest/api/v1/source
- "Get source details?" -> GET /ingest/api/v1/source/{source_id}
- "Update a source?" -> PUT /ingest/api/v1/source/{source_id}
- "Delete a source?" -> DELETE /ingest/api/v1/source/{source_id}
- "Create a dashboard?" -> POST /ingest/api/v1/source/{source_id}/dashboard
- "List all endpoint?" -> GET /ingest/api/v1/source/{source_id}/endpoint
- "Create a endpoint?" -> POST /ingest/api/v1/source/{source_id}/endpoint
- "Get endpoint details?" -> GET /ingest/api/v1/source/{source_id}/endpoint/{endpoint_id}
- "Update a endpoint?" -> PUT /ingest/api/v1/source/{source_id}/endpoint/{endpoint_id}
- "Delete a endpoint?" -> DELETE /ingest/api/v1/source/{source_id}/endpoint/{endpoint_id}
- "List all headers?" -> GET /ingest/api/v1/source/{source_id}/endpoint/{endpoint_id}/headers
- "List all secret?" -> GET /ingest/api/v1/source/{source_id}/endpoint/{endpoint_id}/secret
- "Create a rotate?" -> POST /ingest/api/v1/source/{source_id}/endpoint/{endpoint_id}/secret/rotate
- "List all transformation?" -> GET /ingest/api/v1/source/{source_id}/endpoint/{endpoint_id}/transformation
- "Create a rotate?" -> POST /ingest/api/v1/source/{source_id}/token/rotate
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
