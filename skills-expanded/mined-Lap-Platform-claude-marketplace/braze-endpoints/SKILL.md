---
name: braze-endpoints
description: "Braze Endpoints API skill. Use when working with Braze Endpoints for email, campaigns, sends. Covers 68 endpoints."
version: 1.0.0
generator: lapsh
---

# Braze Endpoints

## Auth
ApiKey Authorization in header

## Base URL
https://{{instance_url}}

## Setup
1. Set your API key in the appropriate header
2. GET /email/hard_bounces -- verify access
3. POST /email/status -- create first status

## Endpoints

68 endpoints across 17 groups. See references/api-spec.lap for full details.

### email
| Method | Path | Description |
|--------|------|-------------|
| GET | /email/hard_bounces | Query Hard Bounced Emails |
| GET | /email/unsubscribes | Query List of Unsubscribed Email Addresses |
| POST | /email/status | Change Email Subscription Status |
| POST | /email/bounce/remove | Remove Hard Bounced Emails |
| POST | /email/spam/remove | Remove Email Addresses from Spam List |
| POST | /email/blacklist | Blacklist Email Addresses |

### campaigns
| Method | Path | Description |
|--------|------|-------------|
| GET | /campaigns/data_series | Campaign Analytics |
| GET | /campaigns/details | Campaign Details |
| GET | /campaigns/list | Campaign List |
| POST | /campaigns/trigger/schedule/delete | Delete Scheduled API Triggered Campaigns |
| POST | /campaigns/trigger/schedule/create | Schedule API Triggered Campaigns |
| POST | /campaigns/trigger/schedule/update | Update Scheduled API Triggered Campaigns |
| POST | /campaigns/trigger/send | Sending Campaign Messages via API Triggered Delivery |

### sends
| Method | Path | Description |
|--------|------|-------------|
| GET | /sends/data_series | Send Analytics |
| POST | /sends/id/create | Create Send IDs For Message Send Tracking |

### canvas
| Method | Path | Description |
|--------|------|-------------|
| GET | /canvas/data_series | Canvas Data Series Analytics |
| GET | /canvas/data_summary | Canvas Data Analytics Summary |
| GET | /canvas/details | Canvas Details |
| GET | /canvas/list | Canvas List |
| POST | /canvas/trigger/schedule/delete | Delete Scheduled API-Triggered Canvases |
| POST | /canvas/trigger/schedule/create | Schedule API Triggered Canvases |
| POST | /canvas/trigger/schedule/update | Update Scheduled API Triggered Canvases |
| POST | /canvas/trigger/send | Sending Canvas Messages via API Triggered Delivery |

### events
| Method | Path | Description |
|--------|------|-------------|
| GET | /events/list | Custom Events List |
| GET | /events/data_series | Custom Events Analytics |

### kpi
| Method | Path | Description |
|--------|------|-------------|
| GET | /kpi/new_users/data_series | Daily New Users by Date |
| GET | /kpi/dau/data_series | Daily Active Users by Date |
| GET | /kpi/mau/data_series | Monthly Active Users for Last 30 Days |
| GET | /kpi/uninstalls/data_series | KPIs for Daily App Uninstalls by Date |

### feed
| Method | Path | Description |
|--------|------|-------------|
| GET | /feed/data_series | News Feed Card Analytics |
| GET | /feed/details | News Feed Cards Details |
| GET | /feed/list | News Feed Cards List |

### purchases
| Method | Path | Description |
|--------|------|-------------|
| GET | /purchases/product_list | Product IDs List |

### segments
| Method | Path | Description |
|--------|------|-------------|
| GET | /segments/list | Segment List |
| GET | /segments/data_series | Segment Analytics |
| GET | /segments/details | Segment Details |

### sessions
| Method | Path | Description |
|--------|------|-------------|
| GET | /sessions/data_series | App Sessions by Time |

### users
| Method | Path | Description |
|--------|------|-------------|
| POST | /users/export/ids | User Profile Export by Identifier |
| POST | /users/export/segment | User Profile Export by Segment |
| POST | /users/export/global_control_group | User Profile Export by Global Control Group |
| POST | /users/external_ids/remove | External ID Remove |
| POST | /users/external_ids/rename | External ID Rename |
| POST | /users/alias/new | Create New User Aliases |
| POST | /users/delete | User Delete |
| POST | /users/identify | Identify Users |
| POST | /users/track | User Track |

### messages
| Method | Path | Description |
|--------|------|-------------|
| GET | /messages/scheduled_broadcasts | Get Upcoming Scheduled Campaigns and Canvases |
| POST | /messages/schedule/delete | Delete Scheduled Messages |
| POST | /messages/schedule/create | Create Scheduled Messages |
| POST | /messages/schedule/update | Update Scheduled Messages |
| POST | /messages/send | Sending Messages Immediately via API Only |

### transactional
| Method | Path | Description |
|--------|------|-------------|
| POST | /transactional/v1/campaigns/YOUR_CAMPAIGN_ID_HERE/send | Sending Transactional Email via API Triggered Delivery |

### sms
| Method | Path | Description |
|--------|------|-------------|
| GET | /sms/invalid_phone_numbers | Query Invalid Phone Numbers |
| POST | /sms/invalid_phone_numbers/remove | Remove Invalid Phone Numbers |

### subscription
| Method | Path | Description |
|--------|------|-------------|
| GET | /subscription/status/get | List User's  Subscription Group Status - Email |
| GET | /subscription/user/status | List User's Subscription Group - Email |
| POST | /subscription/status/set | Update User's Subscription Group Status - Email |
| GET | /subscription/status/get | List User's  Subscription Group Status - SMS |
| GET | /subscription/user/status | List User's Subscription Group - SMS |
| POST | /subscription/status/set | Update User's Subscription Group Status - SMS |

### content_blocks
| Method | Path | Description |
|--------|------|-------------|
| GET | /content_blocks/list | List Available Content Blocks |
| GET | /content_blocks/info | See Content Block Information |
| POST | /content_blocks/create | Create Content Block |
| POST | /content_blocks/update | Update Content Block |

### templates
| Method | Path | Description |
|--------|------|-------------|
| GET | /templates/email/list | List Available Email Templates |
| GET | /templates/email/info | See Email Template Information |
| POST | /templates/email/create | Create Email Template |
| POST | /templates/email/update | Update Email Template |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all hard_bounces?" -> GET /email/hard_bounces
- "List all unsubscribes?" -> GET /email/unsubscribes
- "Create a status?" -> POST /email/status
- "Create a remove?" -> POST /email/bounce/remove
- "Create a remove?" -> POST /email/spam/remove
- "Create a blacklist?" -> POST /email/blacklist
- "List all data_series?" -> GET /campaigns/data_series
- "List all details?" -> GET /campaigns/details
- "List all list?" -> GET /campaigns/list
- "List all data_series?" -> GET /sends/data_series
- "List all data_series?" -> GET /canvas/data_series
- "List all data_summary?" -> GET /canvas/data_summary
- "List all details?" -> GET /canvas/details
- "List all list?" -> GET /canvas/list
- "List all list?" -> GET /events/list
- "List all data_series?" -> GET /events/data_series
- "List all data_series?" -> GET /kpi/new_users/data_series
- "List all data_series?" -> GET /kpi/dau/data_series
- "List all data_series?" -> GET /kpi/mau/data_series
- "List all data_series?" -> GET /kpi/uninstalls/data_series
- "List all data_series?" -> GET /feed/data_series
- "List all details?" -> GET /feed/details
- "List all list?" -> GET /feed/list
- "List all product_list?" -> GET /purchases/product_list
- "List all list?" -> GET /segments/list
- "List all data_series?" -> GET /segments/data_series
- "List all details?" -> GET /segments/details
- "List all data_series?" -> GET /sessions/data_series
- "Create a id?" -> POST /users/export/ids
- "Create a segment?" -> POST /users/export/segment
- "Create a global_control_group?" -> POST /users/export/global_control_group
- "List all scheduled_broadcasts?" -> GET /messages/scheduled_broadcasts
- "Create a delete?" -> POST /messages/schedule/delete
- "Create a delete?" -> POST /campaigns/trigger/schedule/delete
- "Create a delete?" -> POST /canvas/trigger/schedule/delete
- "Create a create?" -> POST /messages/schedule/create
- "Create a create?" -> POST /campaigns/trigger/schedule/create
- "Create a create?" -> POST /canvas/trigger/schedule/create
- "Create a update?" -> POST /messages/schedule/update
- "Create a update?" -> POST /campaigns/trigger/schedule/update
- "Create a update?" -> POST /canvas/trigger/schedule/update
- "Create a create?" -> POST /sends/id/create
- "Create a send?" -> POST /messages/send
- "Create a send?" -> POST /campaigns/trigger/send
- "Create a send?" -> POST /canvas/trigger/send
- "Create a send?" -> POST /transactional/v1/campaigns/YOUR_CAMPAIGN_ID_HERE/send
- "List all invalid_phone_numbers?" -> GET /sms/invalid_phone_numbers
- "Create a remove?" -> POST /sms/invalid_phone_numbers/remove
- "List all get?" -> GET /subscription/status/get
- "List all status?" -> GET /subscription/user/status
- "Create a set?" -> POST /subscription/status/set
- "List all list?" -> GET /content_blocks/list
- "List all info?" -> GET /content_blocks/info
- "Create a create?" -> POST /content_blocks/create
- "Create a update?" -> POST /content_blocks/update
- "List all list?" -> GET /templates/email/list
- "List all info?" -> GET /templates/email/info
- "Create a create?" -> POST /templates/email/create
- "Create a update?" -> POST /templates/email/update
- "Create a remove?" -> POST /users/external_ids/remove
- "Create a rename?" -> POST /users/external_ids/rename
- "Create a new?" -> POST /users/alias/new
- "Create a delete?" -> POST /users/delete
- "Create a identify?" -> POST /users/identify
- "Create a track?" -> POST /users/track
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
