---
name: zoom-api
description: "Zoom API skill. Use when working with Zoom for accounts, groups, h323. Covers 155 endpoints."
version: 1.0.0
generator: lapsh
---

# Zoom API
API version: 2.0.0

## Auth
ApiKey access_token in query

## Base URL
https://api.zoom.us/v2

## Setup
1. Set your API key in the appropriate header
2. GET /accounts -- verify access
3. POST /accounts -- create first accounts

## Endpoints

155 endpoints across 14 groups. See references/api-spec.lap for full details.

### accounts
| Method | Path | Description |
|--------|------|-------------|
| GET | /accounts | List sub accounts |
| POST | /accounts | Create a sub account |
| GET | /accounts/{accountId} | Retrieve a sub account |
| DELETE | /accounts/{accountId} | Disassociate an account |
| PATCH | /accounts/{accountId}/options | Update a sub account's options |
| GET | /accounts/{accountId}/settings | Retrieve a sub account's settings |
| PATCH | /accounts/{accountId}/settings | Update a sub account's settings |
| GET | /accounts/{accountId}/managed_domains | Retrieve a sub account's managed domains |
| GET | /accounts/{accountId}/billing | Retrieve billing information for a sub account |
| PATCH | /accounts/{accountId}/billing | Update billing information for a sub account |
| GET | /accounts/{accountId}/plans | Retrieve plan information for a sub account |
| POST | /accounts/{accountId}/plans | Subscribe plans for a sub account |
| PUT | /accounts/{accountId}/plans/base | Update a base plan for a sub account |
| POST | /accounts/{accountId}/plans/addons | Add an additional plan for sub account |
| PUT | /accounts/{accountId}/plans/addons | Update an additional plan for sub account |

### groups
| Method | Path | Description |
|--------|------|-------------|
| GET | /groups | List groups |
| POST | /groups | Create a group |
| GET | /groups/{groupId} | Retrieve a group |
| PATCH | /groups/{groupId} | Update a group |
| DELETE | /groups/{groupId} | Delete a group |
| GET | /groups/{groupId}/members | List a group's members |
| POST | /groups/{groupId}/members | Add group members |
| DELETE | /groups/{groupId}/members/{memberId} | Delete a group member |

### h323
| Method | Path | Description |
|--------|------|-------------|
| GET | /h323/devices | List H.323/SIP Devices. |
| POST | /h323/devices | Create a H.323/SIP Device |
| PATCH | /h323/devices/{deviceId} | Update a H.323/SIP Device |
| DELETE | /h323/devices/{deviceId} | Delete a H.323/SIP Device |

### tracking_fields
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/tracking_fields | List Tracking Fields. |
| POST | /v2/tracking_fields | Create a Tracking Field |
| GET | /v2/tracking_fields/{fieldId} | Retrieve a tracking field |
| PATCH | /v2/tracking_fields/{fieldId} | Update a Tracking Field |
| DELETE | /v2/tracking_fields/{fieldId} | Delete a Tracking Field |

### im
| Method | Path | Description |
|--------|------|-------------|
| GET | /im/groups | List IM Groups |
| POST | /im/groups | Create an IM Group |
| GET | /im/groups/{groupId} | Retrieve an IM Group |
| PATCH | /im/groups/{groupId} | Update an IM Group |
| DELETE | /im/groups/{groupId} | Delete an IM Group |
| GET | /im/groups/{groupId}/members | List an IM Group's members |
| POST | /im/groups/{groupId}/members | Add IM Group members |
| DELETE | /im/groups/{groupId}/members/{memberId} | Delete an IM Group member |
| GET | /im/chat/sessions | Retrieve IM Chat sessions |
| GET | /im/chat/sessions/{sessionId} | Retrieve IM Chat messages |

### users
| Method | Path | Description |
|--------|------|-------------|
| GET | /users/{userId}/meetings | List meetings |
| POST | /users/{userId}/meetings | Create a meeting |
| GET | /users/{userId}/recordings | List all the recordings |
| GET | /users | List Users |
| POST | /users | Create a user |
| GET | /users/{userId} | Retrieve a user |
| PATCH | /users/{userId} | Update a user |
| DELETE | /users/{userId} | Delete a user |
| GET | /users/{userId}/assistants | List a user's assistants |
| POST | /users/{userId}/assistants | Add assistants |
| DELETE | /users/{userId}/assistants | Delete a user's assistants |
| DELETE | /users/{userId}/assistants/{assistantId} | Delete a user's assistant |
| GET | /users/{userId}/schedulers | List a user's schedulers |
| DELETE | /users/{userId}/schedulers | Delete a user's schedulers |
| DELETE | /users/{userId}/schedulers/{schedulerId} | Delete a user's scheduler |
| POST | /users/{userId}/picture | Upload a user's picture |
| GET | /users/{userId}/settings | Retrieve a user's settings |
| PATCH | /users/{userId}/settings | Update a user's settings |
| PUT | /users/{userId}/status | Update a user's status |
| PUT | /users/{userId}/password | Update a user's password |
| GET | /users/{userId}/permissions | Retrieve a user's permissions |
| GET | /users/{userId}/pac | List user's PAC accounts |
| GET | /users/{userId}/tsp | List user's TSP accounts |
| POST | /users/{userId}/tsp | Add a user's TSP account |
| GET | /users/{userId}/tsp/{tspId} | Retrieve a user's TSP account |
| PATCH | /users/{userId}/tsp/{tspId} | Update a TSP account |
| DELETE | /users/{userId}/tsp/{tspId} | Delete a user's TSP account |
| GET | /users/{userId}/token | Retrieve a user's token |
| DELETE | /users/{userId}/token | Revoke a user's SSO token |
| PUT | /users/{userId}/email | Update a user's email |
| GET | /users/zpk | Verify a user's zpk (Deprecated |
| GET | /users/email | Check a user's email |
| GET | /users/vanity_name | Check a user's personal meeting room name |
| GET | /users/{userId}/webinars | List webinars |
| POST | /users/{userId}/webinars | Create a webinar |

### meetings
| Method | Path | Description |
|--------|------|-------------|
| GET | /meetings/{meetingId} | Retrieve a meeting |
| PATCH | /meetings/{meetingId} | Update a meeting |
| DELETE | /meetings/{meetingId} | Delete a meeting |
| PUT | /meetings/{meetingId}/status | Update a meeting's status |
| GET | /meetings/{meetingId}/invitation | Retrieve meeting invitation |
| GET | /meetings/{meetingId}/registrants | List a meeting's registrants |
| POST | /meetings/{meetingId}/registrants | Add a meeting registrant |
| PUT | /meetings/{meetingId}/registrants/status | Update a meeting registrant's status |
| PATCH | /meetings/{meetingId}/livestream | Update a meeting live stream |
| PATCH | /meetings/{meetingId}/livestream/status | Update a meeting live stream status |
| GET | /meetings/{meetingId}/polls | List a meeting's polls |
| POST | /meetings/{meetingId}/polls | Create a meeting's poll |
| GET | /meetings/{meetingId}/polls/{pollId} | Retrieve a meeting's poll |
| PUT | /meetings/{meetingId}/polls/{pollId} | Update a meeting's poll |
| DELETE | /meetings/{meetingId}/polls/{pollId} | Delete a meeting's Poll |
| GET | /meetings/{meetingId}/recordings | Retrieve a meeting’s all recordings |
| DELETE | /meetings/{meetingId}/recordings | Delete a meeting's recordings |
| DELETE | /meetings/{meetingId}/recordings/{recordingId} | Delete one meeting recording file |
| PUT | /meetings/{meetingId}/recordings/status | Recover a meeting's recordings |
| PUT | /meetings/{meetingId}/recordings/{recordingId}/status | Recover a single recording |
| GET | /meetings/{meetingId}/recordings/settings | Retrieve a meeting recording's settings |
| PATCH | /meetings/{meetingId}/recordings/settings | Update a meeting recording's settings |

### past_meetings
| Method | Path | Description |
|--------|------|-------------|
| GET | /past_meetings/{meetingUUID} | Retrieve past meeting details |
| GET | /past_meetings/{meetingUUID}/participants | Retrieve past meeting participants |
| GET | /past_meetings/{meetingId}/instances | List of ended meeting instances |

### metrics
| Method | Path | Description |
|--------|------|-------------|
| GET | /metrics/meetings | List meetings |
| GET | /metrics/meetings/{meetingId} | Retrieve meeting detail |
| GET | /metrics/meetings/{meetingId}/participants | Retrieve meeting participants |
| GET | /metrics/meetings/{meetingId}/participants/{participantId}/qos | Retrieve meeting participant QOS |
| GET | /metrics/meetings/{meetingId}/participants/qos | List meeting participants QOS |
| GET | /metrics/meetings/{meetingId}/participants/sharing | Retrieve sharing/recording details of meeting participant |
| GET | /metrics/webinars | List webinars |
| GET | /metrics/webinars/{webinarId} | Retrieve webinar detail |
| GET | /metrics/webinars/{webinarId}/participants | Retrieve webinar participants |
| GET | /metrics/webinars/{webinarId}/participants/{participantId}/qos | Retrieve webinar participant QOS |
| GET | /metrics/webinars/{webinarId}/participants/qos | List webinar participant QOS |
| GET | /metrics/webinars/{webinarId}/participants/sharing | Retrieve sharing/recording details of webinar participant |
| GET | /metrics/zoomrooms | List Zoom Rooms |
| GET | /metrics/zoomrooms/{zoomroomId} | Retrieve Zoom Room |
| GET | /metrics/crc | Retrieve CRC Port Usage |
| GET | /metrics/im | Retrieve IM |

### report
| Method | Path | Description |
|--------|------|-------------|
| GET | /report/daily | Retrieve daily report |
| GET | /report/users | Retrieve hosts report |
| GET | /report/users/{userId}/meetings | Retrieve meetings report |
| GET | /report/meetings/{meetingId} | Retrieve meeting details report |
| GET | /report/meetings/{meetingId}/participants | Retrieve meeting participants report |
| GET | /report/meetings/{meetingId}/polls | Retrieve meeting polls report |
| GET | /report/webinars/{webinarId} | Retrieve webinar details report |
| GET | /report/webinars/{webinarId}/participants | Retrieve webinar participants report |
| GET | /report/webinars/{webinarId}/polls | Retrieve webinar polls report |
| GET | /report/webinars/{webinarId}/qa | Retrieve webinar Q&A report |
| GET | /report/telephone | Retrieve telephone report |
| GET | /report/cloud_recording | Retrieve cloud recording usage report |

### tsp
| Method | Path | Description |
|--------|------|-------------|
| GET | /tsp | Retrieve account's TSP information |
| PATCH | /tsp | Update account's TSP information |

### webinars
| Method | Path | Description |
|--------|------|-------------|
| GET | /webinars/{webinarId} | Retrieve a webinar |
| PATCH | /webinars/{webinarId} | Update a webinar |
| DELETE | /webinars/{webinarId} | Delete a webinar |
| PUT | /webinars/{webinarId}/status | Update a webinar's status |
| GET | /webinars/{webinarId}/panelists | List a webinar's panelists |
| POST | /webinars/{webinarId}/panelists | Add a webinar panelist |
| DELETE | /webinars/{webinarId}/panelists | Remove a webinar's panelists |
| DELETE | /webinars/{webinarId}/panelists/{panelistId} | Remove a webinar panelist |
| GET | /webinars/{webinarId}/registrants | List a webinar's registrants |
| POST | /webinars/{webinarId}/registrants | Add a webinar registrant |
| PUT | /webinars/{webinarId}/registrants/status | Update a webinar registrant's status |
| GET | /webinars/{webinarId}/polls | List a webinar's polls |
| POST | /webinars/{webinarId}/polls | Create a webinar's poll |
| GET | /webinars/{webinarId}/polls/{pollId} | Retrieve a webinar's poll |
| PUT | /webinars/{webinarId}/polls/{pollId} | Update a webinar's poll |
| DELETE | /webinars/{webinarId}/polls/{pollId} | Delete a webinar's Poll |

### past_webinars
| Method | Path | Description |
|--------|------|-------------|
| GET | /past_webinars/{webinarId}/instances | List of ended webinar instances |

### webhooks
| Method | Path | Description |
|--------|------|-------------|
| PATCH | /webhooks/options | Switch webhook version |
| GET | /webhooks | List webhooks |
| POST | /webhooks | Create a webhook |
| GET | /webhooks/{webhookId} | Retrieve a webhook |
| PATCH | /webhooks/{webhookId} | Update a webhook |
| DELETE | /webhooks/{webhookId} | Delete a webhook |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all accounts?" -> GET /accounts
- "Create a account?" -> POST /accounts
- "Get account details?" -> GET /accounts/{accountId}
- "Delete a account?" -> DELETE /accounts/{accountId}
- "List all settings?" -> GET /accounts/{accountId}/settings
- "List all managed_domains?" -> GET /accounts/{accountId}/managed_domains
- "List all billing?" -> GET /accounts/{accountId}/billing
- "List all plans?" -> GET /accounts/{accountId}/plans
- "Create a plan?" -> POST /accounts/{accountId}/plans
- "Create a addon?" -> POST /accounts/{accountId}/plans/addons
- "List all groups?" -> GET /groups
- "Create a group?" -> POST /groups
- "Get group details?" -> GET /groups/{groupId}
- "Partially update a group?" -> PATCH /groups/{groupId}
- "Delete a group?" -> DELETE /groups/{groupId}
- "List all members?" -> GET /groups/{groupId}/members
- "Create a member?" -> POST /groups/{groupId}/members
- "Delete a member?" -> DELETE /groups/{groupId}/members/{memberId}
- "List all devices?" -> GET /h323/devices
- "Create a device?" -> POST /h323/devices
- "Partially update a device?" -> PATCH /h323/devices/{deviceId}
- "Delete a device?" -> DELETE /h323/devices/{deviceId}
- "List all tracking_fields?" -> GET /v2/tracking_fields
- "Create a tracking_field?" -> POST /v2/tracking_fields
- "Get tracking_field details?" -> GET /v2/tracking_fields/{fieldId}
- "Partially update a tracking_field?" -> PATCH /v2/tracking_fields/{fieldId}
- "Delete a tracking_field?" -> DELETE /v2/tracking_fields/{fieldId}
- "List all groups?" -> GET /im/groups
- "Create a group?" -> POST /im/groups
- "Get group details?" -> GET /im/groups/{groupId}
- "Partially update a group?" -> PATCH /im/groups/{groupId}
- "Delete a group?" -> DELETE /im/groups/{groupId}
- "List all members?" -> GET /im/groups/{groupId}/members
- "Create a member?" -> POST /im/groups/{groupId}/members
- "Delete a member?" -> DELETE /im/groups/{groupId}/members/{memberId}
- "List all sessions?" -> GET /im/chat/sessions
- "Get session details?" -> GET /im/chat/sessions/{sessionId}
- "List all meetings?" -> GET /users/{userId}/meetings
- "Create a meeting?" -> POST /users/{userId}/meetings
- "Get meeting details?" -> GET /meetings/{meetingId}
- "Partially update a meeting?" -> PATCH /meetings/{meetingId}
- "Delete a meeting?" -> DELETE /meetings/{meetingId}
- "List all invitation?" -> GET /meetings/{meetingId}/invitation
- "List all registrants?" -> GET /meetings/{meetingId}/registrants
- "Create a registrant?" -> POST /meetings/{meetingId}/registrants
- "Get past_meeting details?" -> GET /past_meetings/{meetingUUID}
- "List all participants?" -> GET /past_meetings/{meetingUUID}/participants
- "List all instances?" -> GET /past_meetings/{meetingId}/instances
- "List all polls?" -> GET /meetings/{meetingId}/polls
- "Create a poll?" -> POST /meetings/{meetingId}/polls
- "Get poll details?" -> GET /meetings/{meetingId}/polls/{pollId}
- "Update a poll?" -> PUT /meetings/{meetingId}/polls/{pollId}
- "Delete a poll?" -> DELETE /meetings/{meetingId}/polls/{pollId}
- "List all recordings?" -> GET /users/{userId}/recordings
- "List all recordings?" -> GET /meetings/{meetingId}/recordings
- "Delete a recording?" -> DELETE /meetings/{meetingId}/recordings/{recordingId}
- "List all settings?" -> GET /meetings/{meetingId}/recordings/settings
- "List all meetings?" -> GET /metrics/meetings
- "Get meeting details?" -> GET /metrics/meetings/{meetingId}
- "List all participants?" -> GET /metrics/meetings/{meetingId}/participants
- "List all qos?" -> GET /metrics/meetings/{meetingId}/participants/{participantId}/qos
- "List all qos?" -> GET /metrics/meetings/{meetingId}/participants/qos
- "List all sharing?" -> GET /metrics/meetings/{meetingId}/participants/sharing
- "List all webinars?" -> GET /metrics/webinars
- "Get webinar details?" -> GET /metrics/webinars/{webinarId}
- "List all participants?" -> GET /metrics/webinars/{webinarId}/participants
- "List all qos?" -> GET /metrics/webinars/{webinarId}/participants/{participantId}/qos
- "List all qos?" -> GET /metrics/webinars/{webinarId}/participants/qos
- "List all sharing?" -> GET /metrics/webinars/{webinarId}/participants/sharing
- "List all zoomrooms?" -> GET /metrics/zoomrooms
- "Get zoomroom details?" -> GET /metrics/zoomrooms/{zoomroomId}
- "List all crc?" -> GET /metrics/crc
- "List all im?" -> GET /metrics/im
- "List all daily?" -> GET /report/daily
- "List all users?" -> GET /report/users
- "List all meetings?" -> GET /report/users/{userId}/meetings
- "Get meeting details?" -> GET /report/meetings/{meetingId}
- "List all participants?" -> GET /report/meetings/{meetingId}/participants
- "List all polls?" -> GET /report/meetings/{meetingId}/polls
- "Get webinar details?" -> GET /report/webinars/{webinarId}
- "List all participants?" -> GET /report/webinars/{webinarId}/participants
- "List all polls?" -> GET /report/webinars/{webinarId}/polls
- "List all qa?" -> GET /report/webinars/{webinarId}/qa
- "List all telephone?" -> GET /report/telephone
- "List all cloud_recording?" -> GET /report/cloud_recording
- "List all tsp?" -> GET /tsp
- "List all users?" -> GET /users
- "Create a user?" -> POST /users
- "Get user details?" -> GET /users/{userId}
- "Partially update a user?" -> PATCH /users/{userId}
- "Delete a user?" -> DELETE /users/{userId}
- "List all assistants?" -> GET /users/{userId}/assistants
- "Create a assistant?" -> POST /users/{userId}/assistants
- "Delete a assistant?" -> DELETE /users/{userId}/assistants/{assistantId}
- "List all schedulers?" -> GET /users/{userId}/schedulers
- "Delete a scheduler?" -> DELETE /users/{userId}/schedulers/{schedulerId}
- "Create a picture?" -> POST /users/{userId}/picture
- "List all settings?" -> GET /users/{userId}/settings
- "List all permissions?" -> GET /users/{userId}/permissions
- "List all pac?" -> GET /users/{userId}/pac
- "List all tsp?" -> GET /users/{userId}/tsp
- "Create a tsp?" -> POST /users/{userId}/tsp
- "Get tsp details?" -> GET /users/{userId}/tsp/{tspId}
- "Partially update a tsp?" -> PATCH /users/{userId}/tsp/{tspId}
- "Delete a tsp?" -> DELETE /users/{userId}/tsp/{tspId}
- "List all token?" -> GET /users/{userId}/token
- "List all zpk?" -> GET /users/zpk
- "List all email?" -> GET /users/email
- "List all vanity_name?" -> GET /users/vanity_name
- "List all webinars?" -> GET /users/{userId}/webinars
- "Create a webinar?" -> POST /users/{userId}/webinars
- "Get webinar details?" -> GET /webinars/{webinarId}
- "Partially update a webinar?" -> PATCH /webinars/{webinarId}
- "Delete a webinar?" -> DELETE /webinars/{webinarId}
- "List all panelists?" -> GET /webinars/{webinarId}/panelists
- "Create a panelist?" -> POST /webinars/{webinarId}/panelists
- "Delete a panelist?" -> DELETE /webinars/{webinarId}/panelists/{panelistId}
- "List all registrants?" -> GET /webinars/{webinarId}/registrants
- "Create a registrant?" -> POST /webinars/{webinarId}/registrants
- "List all instances?" -> GET /past_webinars/{webinarId}/instances
- "List all polls?" -> GET /webinars/{webinarId}/polls
- "Create a poll?" -> POST /webinars/{webinarId}/polls
- "Get poll details?" -> GET /webinars/{webinarId}/polls/{pollId}
- "Update a poll?" -> PUT /webinars/{webinarId}/polls/{pollId}
- "Delete a poll?" -> DELETE /webinars/{webinarId}/polls/{pollId}
- "List all webhooks?" -> GET /webhooks
- "Create a webhook?" -> POST /webhooks
- "Get webhook details?" -> GET /webhooks/{webhookId}
- "Partially update a webhook?" -> PATCH /webhooks/{webhookId}
- "Delete a webhook?" -> DELETE /webhooks/{webhookId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
