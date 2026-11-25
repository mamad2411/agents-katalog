---
name: adafruit-io-rest-api
description: "Adafruit IO REST API skill. Use when working with Adafruit IO REST for user, {username}, webhooks. Covers 71 endpoints."
version: 1.0.0
generator: lapsh
---

# Adafruit IO REST API
API version: 2.0.0

## Auth
ApiKey X-AIO-Key in header | ApiKey X-AIO-Key in query | ApiKey X-AIO-Signature in header

## Base URL
https://io.adafruit.com/api/v2

## Setup
1. Set your API key in the appropriate header
2. GET /user -- verify access
3. POST /{username}/feeds -- create first feeds

## Endpoints

71 endpoints across 3 groups. See references/api-spec.lap for full details.

### user
| Method | Path | Description |
|--------|------|-------------|
| GET | /user | Get information about the current user |

### {username}
| Method | Path | Description |
|--------|------|-------------|
| GET | /{username}/throttle | Get the user's data rate limit and current activity level. |
| GET | /{username}/activities | All activities for current user |
| DELETE | /{username}/activities | All activities for current user |
| GET | /{username}/activities/{type} | Get activities by type for current user |
| GET | /{username}/feeds | All feeds for current user |
| POST | /{username}/feeds | Create a new Feed |
| GET | /{username}/feeds/{feed_key} | Get feed by feed key |
| PUT | /{username}/feeds/{feed_key} | Replace an existing Feed |
| PATCH | /{username}/feeds/{feed_key} | Update properties of an existing Feed |
| DELETE | /{username}/feeds/{feed_key} | Delete an existing Feed |
| GET | /{username}/feeds/{feed_key}/details | Get detailed feed by feed key |
| GET | /{username}/feeds/{feed_key}/data | Get all data for the given feed |
| POST | /{username}/feeds/{feed_key}/data | Create new Data |
| GET | /{username}/feeds/{feed_key}/data/chart | Chart data for current feed |
| POST | /{username}/feeds/{feed_key}/data/batch | Create multiple new Data records |
| GET | /{username}/feeds/{feed_key}/data/previous | Previous Data in Queue |
| GET | /{username}/feeds/{feed_key}/data/next | Next Data in Queue |
| GET | /{username}/feeds/{feed_key}/data/last | Last Data in Queue |
| GET | /{username}/feeds/{feed_key}/data/first | First Data in Queue |
| GET | /{username}/feeds/{feed_key}/data/retain | Last Data in MQTT CSV format |
| GET | /{username}/feeds/{feed_key}/data/{id} | Returns data based on feed key |
| PUT | /{username}/feeds/{feed_key}/data/{id} | Replace existing Data |
| PATCH | /{username}/feeds/{feed_key}/data/{id} | Update properties of existing Data |
| DELETE | /{username}/feeds/{feed_key}/data/{id} | Delete existing Data |
| GET | /{username}/groups | All groups for current user |
| POST | /{username}/groups | Create a new Group |
| GET | /{username}/groups/{group_key} | Returns Group based on ID |
| PUT | /{username}/groups/{group_key} | Replace an existing Group |
| PATCH | /{username}/groups/{group_key} | Update properties of an existing Group |
| DELETE | /{username}/groups/{group_key} | Delete an existing Group |
| POST | /{username}/groups/{group_key}/add | Add an existing Feed to a Group |
| POST | /{username}/groups/{group_key}/remove | Remove a Feed from a Group |
| GET | /{username}/groups/{group_key}/feeds | All feeds for current user in a given group |
| POST | /{username}/groups/{group_key}/feeds | Create a new Feed in a Group |
| POST | /{username}/groups/{group_key}/data | Create new data for multiple feeds in a group |
| GET | /{username}/groups/{group_key}/feeds/{feed_key}/data | All data for current feed in a specific group |
| POST | /{username}/groups/{group_key}/feeds/{feed_key}/data | Create new Data in a feed belonging to a particular group |
| POST | /{username}/groups/{group_key}/feeds/{feed_key}/data/batch | Create multiple new Data records in a feed belonging to a particular group |
| GET | /{username}/dashboards | All dashboards for current user |
| POST | /{username}/dashboards | Create a new Dashboard |
| GET | /{username}/dashboards/{id} | Returns Dashboard based on ID |
| PUT | /{username}/dashboards/{id} | Replace an existing Dashboard |
| PATCH | /{username}/dashboards/{id} | Update properties of an existing Dashboard |
| DELETE | /{username}/dashboards/{id} | Delete an existing Dashboard |
| GET | /{username}/dashboards/{dashboard_id}/blocks | All blocks for current user |
| POST | /{username}/dashboards/{dashboard_id}/blocks | Create a new Block |
| GET | /{username}/dashboards/{dashboard_id}/blocks/{id} | Returns Block based on ID |
| PUT | /{username}/dashboards/{dashboard_id}/blocks/{id} | Replace an existing Block |
| PATCH | /{username}/dashboards/{dashboard_id}/blocks/{id} | Update properties of an existing Block |
| DELETE | /{username}/dashboards/{dashboard_id}/blocks/{id} | Delete an existing Block |
| GET | /{username}/tokens | All tokens for current user |
| POST | /{username}/tokens | Create a new Token |
| GET | /{username}/tokens/{id} | Returns Token based on ID |
| PUT | /{username}/tokens/{id} | Replace an existing Token |
| PATCH | /{username}/tokens/{id} | Update properties of an existing Token |
| DELETE | /{username}/tokens/{id} | Delete an existing Token |
| GET | /{username}/triggers | All triggers for current user |
| POST | /{username}/triggers | Create a new Trigger |
| GET | /{username}/triggers/{id} | Returns Trigger based on ID |
| PUT | /{username}/triggers/{id} | Replace an existing Trigger |
| PATCH | /{username}/triggers/{id} | Update properties of an existing Trigger |
| DELETE | /{username}/triggers/{id} | Delete an existing Trigger |
| GET | /{username}/{type}/{type_id}/acl | All permissions for current user and type |
| POST | /{username}/{type}/{type_id}/acl | Create a new Permission |
| GET | /{username}/{type}/{type_id}/acl/{id} | Returns Permission based on ID |
| PUT | /{username}/{type}/{type_id}/acl/{id} | Replace an existing Permission |
| PATCH | /{username}/{type}/{type_id}/acl/{id} | Update properties of an existing Permission |
| DELETE | /{username}/{type}/{type_id}/acl/{id} | Delete an existing Permission |

### webhooks
| Method | Path | Description |
|--------|------|-------------|
| POST | /webhooks/feed/:token | Send data to a feed via webhook URL. |
| POST | /webhooks/feed/:token/raw | Send arbitrary data to a feed via webhook URL. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all user?" -> GET /user
- "List all throttle?" -> GET /{username}/throttle
- "List all activities?" -> GET /{username}/activities
- "Get activity details?" -> GET /{username}/activities/{type}
- "List all feeds?" -> GET /{username}/feeds
- "Create a feed?" -> POST /{username}/feeds
- "Get feed details?" -> GET /{username}/feeds/{feed_key}
- "Update a feed?" -> PUT /{username}/feeds/{feed_key}
- "Partially update a feed?" -> PATCH /{username}/feeds/{feed_key}
- "Delete a feed?" -> DELETE /{username}/feeds/{feed_key}
- "List all details?" -> GET /{username}/feeds/{feed_key}/details
- "List all data?" -> GET /{username}/feeds/{feed_key}/data
- "Create a data?" -> POST /{username}/feeds/{feed_key}/data
- "List all chart?" -> GET /{username}/feeds/{feed_key}/data/chart
- "Create a batch?" -> POST /{username}/feeds/{feed_key}/data/batch
- "List all previous?" -> GET /{username}/feeds/{feed_key}/data/previous
- "List all next?" -> GET /{username}/feeds/{feed_key}/data/next
- "List all last?" -> GET /{username}/feeds/{feed_key}/data/last
- "List all first?" -> GET /{username}/feeds/{feed_key}/data/first
- "List all retain?" -> GET /{username}/feeds/{feed_key}/data/retain
- "Get data details?" -> GET /{username}/feeds/{feed_key}/data/{id}
- "Update a data?" -> PUT /{username}/feeds/{feed_key}/data/{id}
- "Partially update a data?" -> PATCH /{username}/feeds/{feed_key}/data/{id}
- "Delete a data?" -> DELETE /{username}/feeds/{feed_key}/data/{id}
- "List all groups?" -> GET /{username}/groups
- "Create a group?" -> POST /{username}/groups
- "Get group details?" -> GET /{username}/groups/{group_key}
- "Update a group?" -> PUT /{username}/groups/{group_key}
- "Partially update a group?" -> PATCH /{username}/groups/{group_key}
- "Delete a group?" -> DELETE /{username}/groups/{group_key}
- "Create a add?" -> POST /{username}/groups/{group_key}/add
- "Create a remove?" -> POST /{username}/groups/{group_key}/remove
- "List all feeds?" -> GET /{username}/groups/{group_key}/feeds
- "Create a feed?" -> POST /{username}/groups/{group_key}/feeds
- "Create a data?" -> POST /{username}/groups/{group_key}/data
- "List all data?" -> GET /{username}/groups/{group_key}/feeds/{feed_key}/data
- "Create a data?" -> POST /{username}/groups/{group_key}/feeds/{feed_key}/data
- "Create a batch?" -> POST /{username}/groups/{group_key}/feeds/{feed_key}/data/batch
- "List all dashboards?" -> GET /{username}/dashboards
- "Create a dashboard?" -> POST /{username}/dashboards
- "Get dashboard details?" -> GET /{username}/dashboards/{id}
- "Update a dashboard?" -> PUT /{username}/dashboards/{id}
- "Partially update a dashboard?" -> PATCH /{username}/dashboards/{id}
- "Delete a dashboard?" -> DELETE /{username}/dashboards/{id}
- "List all blocks?" -> GET /{username}/dashboards/{dashboard_id}/blocks
- "Create a block?" -> POST /{username}/dashboards/{dashboard_id}/blocks
- "Get block details?" -> GET /{username}/dashboards/{dashboard_id}/blocks/{id}
- "Update a block?" -> PUT /{username}/dashboards/{dashboard_id}/blocks/{id}
- "Partially update a block?" -> PATCH /{username}/dashboards/{dashboard_id}/blocks/{id}
- "Delete a block?" -> DELETE /{username}/dashboards/{dashboard_id}/blocks/{id}
- "List all tokens?" -> GET /{username}/tokens
- "Create a token?" -> POST /{username}/tokens
- "Get token details?" -> GET /{username}/tokens/{id}
- "Update a token?" -> PUT /{username}/tokens/{id}
- "Partially update a token?" -> PATCH /{username}/tokens/{id}
- "Delete a token?" -> DELETE /{username}/tokens/{id}
- "List all triggers?" -> GET /{username}/triggers
- "Create a trigger?" -> POST /{username}/triggers
- "Get trigger details?" -> GET /{username}/triggers/{id}
- "Update a trigger?" -> PUT /{username}/triggers/{id}
- "Partially update a trigger?" -> PATCH /{username}/triggers/{id}
- "Delete a trigger?" -> DELETE /{username}/triggers/{id}
- "List all acl?" -> GET /{username}/{type}/{type_id}/acl
- "Create a acl?" -> POST /{username}/{type}/{type_id}/acl
- "Get acl details?" -> GET /{username}/{type}/{type_id}/acl/{id}
- "Update a acl?" -> PUT /{username}/{type}/{type_id}/acl/{id}
- "Partially update a acl?" -> PATCH /{username}/{type}/{type_id}/acl/{id}
- "Delete a acl?" -> DELETE /{username}/{type}/{type_id}/acl/{id}
- "Create a :token?" -> POST /webhooks/feed/:token
- "Create a raw?" -> POST /webhooks/feed/:token/raw
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
