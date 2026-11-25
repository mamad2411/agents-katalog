---
name: youtube-data-api-v3
description: "YouTube Data API v3 API skill. Use when working with YouTube Data API v3 for youtube. Covers 76 endpoints."
version: 1.0.0
generator: lapsh
---

# YouTube Data API v3
API version: v3

## Auth
OAuth2 | OAuth2

## Base URL
https://youtube.googleapis.com/

## Setup
1. Configure auth: OAuth2 | OAuth2
2. GET /youtube/v3/activities -- verify access
3. POST /youtube/v3/abuseReports -- create first abuseReports

## Endpoints

76 endpoints across 1 groups. See references/api-spec.lap for full details.

### youtube
| Method | Path | Description |
|--------|------|-------------|
| POST | /youtube/v3/abuseReports | Inserts a new resource into this collection. |
| GET | /youtube/v3/activities | Retrieves a list of resources, possibly filtered. |
| DELETE | /youtube/v3/captions | Deletes a resource. |
| GET | /youtube/v3/captions | Retrieves a list of resources, possibly filtered. |
| POST | /youtube/v3/captions | Inserts a new resource into this collection. |
| PUT | /youtube/v3/captions | Updates an existing resource. |
| GET | /youtube/v3/captions/{id} | Downloads a caption track. |
| POST | /youtube/v3/channelBanners/insert | Inserts a new resource into this collection. |
| DELETE | /youtube/v3/channelSections | Deletes a resource. |
| GET | /youtube/v3/channelSections | Retrieves a list of resources, possibly filtered. |
| POST | /youtube/v3/channelSections | Inserts a new resource into this collection. |
| PUT | /youtube/v3/channelSections | Updates an existing resource. |
| GET | /youtube/v3/channels | Retrieves a list of resources, possibly filtered. |
| PUT | /youtube/v3/channels | Updates an existing resource. |
| GET | /youtube/v3/commentThreads | Retrieves a list of resources, possibly filtered. |
| POST | /youtube/v3/commentThreads | Inserts a new resource into this collection. |
| PUT | /youtube/v3/commentThreads | Updates an existing resource. |
| DELETE | /youtube/v3/comments | Deletes a resource. |
| GET | /youtube/v3/comments | Retrieves a list of resources, possibly filtered. |
| POST | /youtube/v3/comments | Inserts a new resource into this collection. |
| PUT | /youtube/v3/comments | Updates an existing resource. |
| POST | /youtube/v3/comments/markAsSpam | Expresses the caller's opinion that one or more comments should be flagged as spam. |
| POST | /youtube/v3/comments/setModerationStatus | Sets the moderation status of one or more comments. |
| GET | /youtube/v3/i18nLanguages | Retrieves a list of resources, possibly filtered. |
| GET | /youtube/v3/i18nRegions | Retrieves a list of resources, possibly filtered. |
| DELETE | /youtube/v3/liveBroadcasts | Delete a given broadcast. |
| GET | /youtube/v3/liveBroadcasts | Retrieve the list of broadcasts associated with the given channel. |
| POST | /youtube/v3/liveBroadcasts | Inserts a new stream for the authenticated user. |
| PUT | /youtube/v3/liveBroadcasts | Updates an existing broadcast for the authenticated user. |
| POST | /youtube/v3/liveBroadcasts/bind | Bind a broadcast to a stream. |
| POST | /youtube/v3/liveBroadcasts/cuepoint | Insert cuepoints in a broadcast |
| POST | /youtube/v3/liveBroadcasts/transition | Transition a broadcast to a given status. |
| DELETE | /youtube/v3/liveChat/bans | Deletes a chat ban. |
| POST | /youtube/v3/liveChat/bans | Inserts a new resource into this collection. |
| DELETE | /youtube/v3/liveChat/messages | Deletes a chat message. |
| GET | /youtube/v3/liveChat/messages | Retrieves a list of resources, possibly filtered. |
| POST | /youtube/v3/liveChat/messages | Inserts a new resource into this collection. |
| DELETE | /youtube/v3/liveChat/moderators | Deletes a chat moderator. |
| GET | /youtube/v3/liveChat/moderators | Retrieves a list of resources, possibly filtered. |
| POST | /youtube/v3/liveChat/moderators | Inserts a new resource into this collection. |
| DELETE | /youtube/v3/liveStreams | Deletes an existing stream for the authenticated user. |
| GET | /youtube/v3/liveStreams | Retrieve the list of streams associated with the given channel. -- |
| POST | /youtube/v3/liveStreams | Inserts a new stream for the authenticated user. |
| PUT | /youtube/v3/liveStreams | Updates an existing stream for the authenticated user. |
| GET | /youtube/v3/members | Retrieves a list of members that match the request criteria for a channel. |
| GET | /youtube/v3/membershipsLevels | Retrieves a list of all pricing levels offered by a creator to the fans. |
| DELETE | /youtube/v3/playlistItems | Deletes a resource. |
| GET | /youtube/v3/playlistItems | Retrieves a list of resources, possibly filtered. |
| POST | /youtube/v3/playlistItems | Inserts a new resource into this collection. |
| PUT | /youtube/v3/playlistItems | Updates an existing resource. |
| DELETE | /youtube/v3/playlists | Deletes a resource. |
| GET | /youtube/v3/playlists | Retrieves a list of resources, possibly filtered. |
| POST | /youtube/v3/playlists | Inserts a new resource into this collection. |
| PUT | /youtube/v3/playlists | Updates an existing resource. |
| GET | /youtube/v3/search | Retrieves a list of search resources |
| DELETE | /youtube/v3/subscriptions | Deletes a resource. |
| GET | /youtube/v3/subscriptions | Retrieves a list of resources, possibly filtered. |
| POST | /youtube/v3/subscriptions | Inserts a new resource into this collection. |
| GET | /youtube/v3/superChatEvents | Retrieves a list of resources, possibly filtered. |
| POST | /youtube/v3/tests | POST method. |
| DELETE | /youtube/v3/thirdPartyLinks | Deletes a resource. |
| GET | /youtube/v3/thirdPartyLinks | Retrieves a list of resources, possibly filtered. |
| POST | /youtube/v3/thirdPartyLinks | Inserts a new resource into this collection. |
| PUT | /youtube/v3/thirdPartyLinks | Updates an existing resource. |
| POST | /youtube/v3/thumbnails/set | As this is not an insert in a strict sense (it supports uploading/setting of a thumbnail for multiple videos, which doesn't result in creation of a single resource), I use a custom verb here. |
| GET | /youtube/v3/videoAbuseReportReasons | Retrieves a list of resources, possibly filtered. |
| GET | /youtube/v3/videoCategories | Retrieves a list of resources, possibly filtered. |
| DELETE | /youtube/v3/videos | Deletes a resource. |
| GET | /youtube/v3/videos | Retrieves a list of resources, possibly filtered. |
| POST | /youtube/v3/videos | Inserts a new resource into this collection. |
| PUT | /youtube/v3/videos | Updates an existing resource. |
| GET | /youtube/v3/videos/getRating | Retrieves the ratings that the authorized user gave to a list of specified videos. |
| POST | /youtube/v3/videos/rate | Adds a like or dislike rating to a video or removes a rating from a video. |
| POST | /youtube/v3/videos/reportAbuse | Report abuse for a video. |
| POST | /youtube/v3/watermarks/set | Allows upload of watermark image and setting it for a channel. |
| POST | /youtube/v3/watermarks/unset | Allows removal of channel watermark. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a abuseReport?" -> POST /youtube/v3/abuseReports
- "List all activities?" -> GET /youtube/v3/activities
- "List all captions?" -> GET /youtube/v3/captions
- "Create a caption?" -> POST /youtube/v3/captions
- "Get caption details?" -> GET /youtube/v3/captions/{id}
- "Create a insert?" -> POST /youtube/v3/channelBanners/insert
- "List all channelSections?" -> GET /youtube/v3/channelSections
- "Create a channelSection?" -> POST /youtube/v3/channelSections
- "List all channels?" -> GET /youtube/v3/channels
- "List all commentThreads?" -> GET /youtube/v3/commentThreads
- "Create a commentThread?" -> POST /youtube/v3/commentThreads
- "List all comments?" -> GET /youtube/v3/comments
- "Create a comment?" -> POST /youtube/v3/comments
- "Create a markAsSpam?" -> POST /youtube/v3/comments/markAsSpam
- "Create a setModerationStatus?" -> POST /youtube/v3/comments/setModerationStatus
- "List all i18nLanguages?" -> GET /youtube/v3/i18nLanguages
- "List all i18nRegions?" -> GET /youtube/v3/i18nRegions
- "List all liveBroadcasts?" -> GET /youtube/v3/liveBroadcasts
- "Create a liveBroadcast?" -> POST /youtube/v3/liveBroadcasts
- "Create a bind?" -> POST /youtube/v3/liveBroadcasts/bind
- "Create a cuepoint?" -> POST /youtube/v3/liveBroadcasts/cuepoint
- "Create a transition?" -> POST /youtube/v3/liveBroadcasts/transition
- "Create a ban?" -> POST /youtube/v3/liveChat/bans
- "List all messages?" -> GET /youtube/v3/liveChat/messages
- "Create a message?" -> POST /youtube/v3/liveChat/messages
- "List all moderators?" -> GET /youtube/v3/liveChat/moderators
- "Create a moderator?" -> POST /youtube/v3/liveChat/moderators
- "List all liveStreams?" -> GET /youtube/v3/liveStreams
- "Create a liveStream?" -> POST /youtube/v3/liveStreams
- "List all members?" -> GET /youtube/v3/members
- "List all membershipsLevels?" -> GET /youtube/v3/membershipsLevels
- "List all playlistItems?" -> GET /youtube/v3/playlistItems
- "Create a playlistItem?" -> POST /youtube/v3/playlistItems
- "List all playlists?" -> GET /youtube/v3/playlists
- "Create a playlist?" -> POST /youtube/v3/playlists
- "Search search?" -> GET /youtube/v3/search
- "List all subscriptions?" -> GET /youtube/v3/subscriptions
- "Create a subscription?" -> POST /youtube/v3/subscriptions
- "List all superChatEvents?" -> GET /youtube/v3/superChatEvents
- "Create a test?" -> POST /youtube/v3/tests
- "List all thirdPartyLinks?" -> GET /youtube/v3/thirdPartyLinks
- "Create a thirdPartyLink?" -> POST /youtube/v3/thirdPartyLinks
- "Create a set?" -> POST /youtube/v3/thumbnails/set
- "List all videoAbuseReportReasons?" -> GET /youtube/v3/videoAbuseReportReasons
- "List all videoCategories?" -> GET /youtube/v3/videoCategories
- "List all videos?" -> GET /youtube/v3/videos
- "Create a video?" -> POST /youtube/v3/videos
- "List all getRating?" -> GET /youtube/v3/videos/getRating
- "Create a rate?" -> POST /youtube/v3/videos/rate
- "Create a reportAbuse?" -> POST /youtube/v3/videos/reportAbuse
- "Create a set?" -> POST /youtube/v3/watermarks/set
- "Create a unset?" -> POST /youtube/v3/watermarks/unset
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
