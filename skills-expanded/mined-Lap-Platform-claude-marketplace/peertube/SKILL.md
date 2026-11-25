---
name: peertube
description: "PeerTube API skill. Use when working with PeerTube for static, download, feeds. Covers 265 endpoints."
version: 1.0.0
generator: lapsh
---

# PeerTube
API version: 8.0.0

## Auth
OAuth2

## Base URL
https://peertube2.cpy.re

## Setup
1. Configure auth: OAuth2
2. GET /feeds/podcast/videos.xml -- verify access
3. POST /api/v1/config/instance-banner/pick -- create first pick

## Endpoints

265 endpoints across 4 groups. See references/api-spec.lap for full details.

### static
| Method | Path | Description |
|--------|------|-------------|
| GET | /static/web-videos/{filename} | Get public Web Video file |
| GET | /static/web-videos/private/{filename} | Get private Web Video file |
| GET | /static/streaming-playlists/hls/{filename} | Get public HLS video file |
| GET | /static/streaming-playlists/hls/private/{filename} | Get private HLS video file |

### download
| Method | Path | Description |
|--------|------|-------------|
| GET | /download/videos/generate/{videoId} | Download video file |

### feeds
| Method | Path | Description |
|--------|------|-------------|
| GET | /feeds/video-comments.{format} | Comments on videos feeds |
| GET | /feeds/videos.{format} | Common videos feeds |
| GET | /feeds/subscriptions.{format} | Videos of subscriptions feeds |
| GET | /feeds/podcast/videos.xml | Videos podcast feed |

### api
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/v1/accounts/{name} | Get an account |
| GET | /api/v1/accounts/{name}/videos | List videos of an account |
| GET | /api/v1/accounts/{name}/followers | List followers of an account |
| GET | /api/v1/accounts | List accounts |
| GET | /api/v1/config | Get instance public configuration |
| GET | /api/v1/config/about | Get instance "About" information |
| GET | /api/v1/config/custom | Get instance runtime configuration |
| PUT | /api/v1/config/custom | Set instance runtime configuration |
| DELETE | /api/v1/config/custom | Delete instance runtime configuration |
| POST | /api/v1/config/instance-banner/pick | Update instance banner |
| DELETE | /api/v1/config/instance-banner | Delete instance banner |
| POST | /api/v1/config/instance-avatar/pick | Update instance avatar |
| DELETE | /api/v1/config/instance-avatar | Delete instance avatar |
| POST | /api/v1/config/instance-logo/{logoType}/pick | Update instance logo |
| DELETE | /api/v1/config/instance-logo/{logoType} | Delete instance logo |
| GET | /api/v1/custom-pages/homepage/instance | Get instance custom homepage |
| PUT | /api/v1/custom-pages/homepage/instance | Set instance custom homepage |
| POST | /api/v1/jobs/pause | Pause job queue |
| POST | /api/v1/jobs/resume | Resume job queue |
| GET | /api/v1/jobs/{state} | List instance jobs |
| GET | /api/v1/server/followers | List instances following the server |
| DELETE | /api/v1/server/followers/{handle} | Remove or reject a follower to your server |
| POST | /api/v1/server/followers/{handle}/reject | Reject a pending follower to your server |
| POST | /api/v1/server/followers/{handle}/accept | Accept a pending follower to your server |
| GET | /api/v1/server/following | List instances followed by the server |
| POST | /api/v1/server/following | Follow a list of actors (PeerTube instance, channel or account) |
| DELETE | /api/v1/server/following/{hostOrHandle} | Unfollow an actor (PeerTube instance, channel or account) |
| POST | /api/v1/users | Create a user |
| GET | /api/v1/users | List users |
| DELETE | /api/v1/users/{id} | Delete a user |
| GET | /api/v1/users/{id} | Get a user |
| PUT | /api/v1/users/{id} | Update a user |
| GET | /api/v1/oauth-clients/local | Login prerequisite |
| POST | /api/v1/users/token | Login |
| POST | /api/v1/users/revoke-token | Logout |
| GET | /api/v1/users/{id}/token-sessions | List token sessions |
| GET | /api/v1/users/{id}/token-sessions/{tokenSessionId}/revoke | List token sessions |
| POST | /api/v1/users/ask-send-verify-email | Resend user verification link |
| POST | /api/v1/users/registrations/ask-send-verify-email | Resend verification link to registration request email |
| POST | /api/v1/users/{id}/verify-email | Verify a user |
| POST | /api/v1/users/registrations/{registrationId}/verify-email | Verify a registration email |
| POST | /api/v1/users/ask-reset-password | Ask to reset password |
| POST | /api/v1/users/{id}/reset-password | Reset password |
| POST | /api/v1/users/{id}/two-factor/request | Request two factor auth |
| POST | /api/v1/users/{id}/two-factor/confirm-request | Confirm two factor auth |
| POST | /api/v1/users/{id}/two-factor/disable | Disable two factor auth |
| POST | /api/v1/users/{userId}/imports/import-resumable | Initialize the resumable user import |
| PUT | /api/v1/users/{userId}/imports/import-resumable | Send chunk for the resumable user import |
| DELETE | /api/v1/users/{userId}/imports/import-resumable | Cancel the resumable user import |
| GET | /api/v1/users/{userId}/imports/latest | Get latest user import |
| POST | /api/v1/users/{userId}/exports/request | Request user export |
| GET | /api/v1/users/{userId}/exports | List user exports |
| DELETE | /api/v1/users/{userId}/exports/{id} | Delete a user export |
| GET | /api/v1/users/me | Get my user information |
| PUT | /api/v1/users/me | Update my user information |
| GET | /api/v1/users/me/videos/comments | List comments on user's videos |
| GET | /api/v1/users/me/videos/imports | Get video imports of my user |
| GET | /api/v1/users/me/video-quota-used | Get my user used quota |
| GET | /api/v1/users/me/videos/{videoId}/rating | Get rate of my user for a video |
| GET | /api/v1/users/me/videos | List videos of my user |
| GET | /api/v1/users/me/subscriptions | List my user subscriptions |
| POST | /api/v1/users/me/subscriptions | Add subscription to my user |
| GET | /api/v1/users/me/subscriptions/exist | Get if subscriptions exist for my user |
| GET | /api/v1/users/me/subscriptions/videos | List videos of subscriptions of my user |
| GET | /api/v1/users/me/subscriptions/{subscriptionHandle} | Get subscription of my user |
| DELETE | /api/v1/users/me/subscriptions/{subscriptionHandle} | Delete subscription of my user |
| GET | /api/v1/users/me/notifications | List my notifications |
| POST | /api/v1/users/me/notifications/read | Mark notifications as read by their id |
| POST | /api/v1/users/me/notifications/read-all | Mark all my notification as read |
| PUT | /api/v1/users/me/notification-settings | Update my notification settings |
| POST | /api/v1/users/me/new-feature-info/read | Mark feature info as read |
| GET | /api/v1/users/me/history/videos | List watched videos history |
| DELETE | /api/v1/users/me/history/videos/{videoId} | Delete history element |
| POST | /api/v1/users/me/history/videos/remove | Clear video history |
| POST | /api/v1/users/me/avatar/pick | Update my user avatar |
| DELETE | /api/v1/users/me/avatar | Delete my avatar |
| POST | /api/v1/users/register | Register a user |
| POST | /api/v1/users/registrations/request | Request registration |
| POST | /api/v1/users/registrations/{registrationId}/accept | Accept registration |
| POST | /api/v1/users/registrations/{registrationId}/reject | Reject registration |
| DELETE | /api/v1/users/registrations/{registrationId} | Delete registration |
| GET | /api/v1/users/registrations | List registrations |
| GET | /api/v1/videos/ownership | List video ownership changes |
| POST | /api/v1/videos/ownership/{id}/accept | Accept ownership change request |
| POST | /api/v1/videos/ownership/{id}/refuse | Refuse ownership change request |
| POST | /api/v1/videos/{id}/give-ownership | Request ownership change |
| POST | /api/v1/videos/{id}/token | Request video token |
| POST | /api/v1/videos/{id}/studio/edit | Create a studio task |
| GET | /api/v1/videos | List videos |
| GET | /api/v1/videos/categories | List available video categories |
| GET | /api/v1/videos/licences | List available video licences |
| GET | /api/v1/videos/languages | List available video languages |
| GET | /api/v1/videos/privacies | List available video privacy policies |
| PUT | /api/v1/videos/{id} | Update a video |
| GET | /api/v1/videos/{id} | Get a video |
| DELETE | /api/v1/videos/{id} | Delete a video |
| GET | /api/v1/videos/{id}/description | Get complete video description |
| POST | /api/v1/videos/{id}/views | Notify user is watching a video |
| GET | /api/v1/videos/{id}/stats/overall | Get overall stats of a video |
| GET | /api/v1/videos/{id}/stats/user-agent | Get user agent stats of a video |
| GET | /api/v1/videos/{id}/stats/retention | Get retention stats of a video |
| GET | /api/v1/videos/{id}/stats/timeseries/{metric} | Get timeserie stats of a video |
| POST | /api/v1/videos/upload | Upload a video |
| POST | /api/v1/videos/upload-resumable | Initialize the resumable upload of a video |
| PUT | /api/v1/videos/upload-resumable | Send chunk for the resumable upload of a video |
| DELETE | /api/v1/videos/upload-resumable | Cancel the resumable upload of a video, deleting any data uploaded so far |
| POST | /api/v1/videos/imports | Import a video |
| POST | /api/v1/videos/imports/{id}/cancel | Cancel video import |
| POST | /api/v1/videos/imports/{id}/retry | Retry video import |
| DELETE | /api/v1/videos/imports/{id} | Delete video import |
| POST | /api/v1/videos/live | Create a live |
| GET | /api/v1/videos/live/{id} | Get information about a live |
| PUT | /api/v1/videos/live/{id} | Update information about a live |
| GET | /api/v1/videos/live/{id}/sessions | List live sessions |
| GET | /api/v1/videos/{id}/live-session | Get live session of a replay |
| GET | /api/v1/videos/{id}/source | Get video source file metadata |
| DELETE | /api/v1/videos/{id}/source/file | Delete video source file |
| POST | /api/v1/videos/{id}/source/replace-resumable | Initialize the resumable replacement of a video |
| PUT | /api/v1/videos/{id}/source/replace-resumable | Send chunk for the resumable replacement of a video |
| DELETE | /api/v1/videos/{id}/source/replace-resumable | Cancel the resumable replacement of a video |
| GET | /api/v1/users/me/abuses | List my abuses |
| GET | /api/v1/abuses | List abuses |
| POST | /api/v1/abuses | Report an abuse |
| PUT | /api/v1/abuses/{abuseId} | Update an abuse |
| DELETE | /api/v1/abuses/{abuseId} | Delete an abuse |
| GET | /api/v1/abuses/{abuseId}/messages | List messages of an abuse |
| POST | /api/v1/abuses/{abuseId}/messages | Add message to an abuse |
| DELETE | /api/v1/abuses/{abuseId}/messages/{abuseMessageId} | Delete an abuse message |
| POST | /api/v1/videos/{id}/blacklist | Block a video |
| DELETE | /api/v1/videos/{id}/blacklist | Unblock a video by its id |
| GET | /api/v1/videos/blacklist | List video blocks |
| GET | /api/v1/videos/{id}/storyboards | List storyboards of a video |
| GET | /api/v1/videos/{id}/captions | List captions of a video |
| POST | /api/v1/videos/{id}/captions/generate | Generate a video caption |
| PUT | /api/v1/videos/{id}/captions/{captionLanguage} | Add or replace a video caption |
| DELETE | /api/v1/videos/{id}/captions/{captionLanguage} | Delete a video caption |
| GET | /api/v1/videos/{id}/chapters | Get chapters of a video |
| PUT | /api/v1/videos/{id}/chapters | Replace video chapters |
| GET | /api/v1/videos/{id}/embed-privacy | Get video embed privacy |
| PUT | /api/v1/videos/{id}/embed-privacy | Update video embed privacy |
| GET | /api/v1/videos/{id}/embed-privacy/allowed | Check if embed is allowed |
| GET | /api/v1/videos/{id}/passwords | List video passwords |
| PUT | /api/v1/videos/{id}/passwords | Update video passwords |
| POST | /api/v1/videos/{id}/passwords | Add a video password |
| DELETE | /api/v1/videos/{id}/passwords/{videoPasswordId} | Delete a video password |
| GET | /api/v1/video-channels | List video channels |
| POST | /api/v1/video-channels | Create a video channel |
| GET | /api/v1/video-channels/{channelHandle} | Get a video channel |
| PUT | /api/v1/video-channels/{channelHandle} | Update a video channel |
| DELETE | /api/v1/video-channels/{channelHandle} | Delete a video channel |
| GET | /api/v1/video-channels/{channelHandle}/videos | List videos of a video channel |
| GET | /api/v1/video-channels/{channelHandle}/activities | List activities of a video channel |
| GET | /api/v1/video-channels/{channelHandle}/video-playlists | List playlists of a channel |
| POST | /api/v1/video-channels/{channelHandle}/video-playlists/reorder | Reorder channel playlists |
| GET | /api/v1/video-channels/{channelHandle}/followers | List followers of a video channel |
| POST | /api/v1/video-channels/{channelHandle}/avatar/pick | Update channel avatar |
| DELETE | /api/v1/video-channels/{channelHandle}/avatar | Delete channel avatar |
| POST | /api/v1/video-channels/{channelHandle}/banner/pick | Update channel banner |
| DELETE | /api/v1/video-channels/{channelHandle}/banner | Delete channel banner |
| POST | /api/v1/video-channels/{channelHandle}/import-videos | Import videos in channel |
| POST | /api/v1/video-channel-syncs | Create a synchronization for a video channel |
| DELETE | /api/v1/video-channel-syncs/{channelSyncId} | Delete a video channel synchronization |
| POST | /api/v1/video-channel-syncs/{channelSyncId}/sync | Triggers the channel synchronization job, fetching all the videos from the remote channel |
| GET | /api/v1/player-settings/videos/{id} | Get video player settings |
| PUT | /api/v1/player-settings/videos/{id} | Update video player settings |
| GET | /api/v1/player-settings/video-channels/{channelHandle} | Get channel player settings |
| PUT | /api/v1/player-settings/video-channels/{channelHandle} | Update channel player settings |
| GET | /api/v1/video-playlists/privacies | List available playlist privacy policies |
| GET | /api/v1/video-playlists | List video playlists |
| POST | /api/v1/video-playlists | Create a video playlist |
| GET | /api/v1/video-playlists/{playlistId} | Get a video playlist |
| PUT | /api/v1/video-playlists/{playlistId} | Update a video playlist |
| DELETE | /api/v1/video-playlists/{playlistId} | Delete a video playlist |
| GET | /api/v1/video-playlists/{playlistId}/videos | List videos of a playlist |
| POST | /api/v1/video-playlists/{playlistId}/videos | Add a video in a playlist |
| POST | /api/v1/video-playlists/{playlistId}/videos/reorder | Reorder playlist elements |
| PUT | /api/v1/video-playlists/{playlistId}/videos/{playlistElementId} | Update a playlist element |
| DELETE | /api/v1/video-playlists/{playlistId}/videos/{playlistElementId} | Delete an element from a playlist |
| GET | /api/v1/users/me/video-playlists/videos-exist | Check video exists in my playlists |
| GET | /api/v1/accounts/{name}/video-playlists | List playlists of an account |
| GET | /api/v1/accounts/{name}/video-channels | List video channels of an account |
| GET | /api/v1/accounts/{name}/video-channel-syncs | List the synchronizations of video channels of an account |
| GET | /api/v1/accounts/{name}/ratings | List ratings of an account |
| GET | /api/v1/videos/{id}/comment-threads | List threads of a video |
| POST | /api/v1/videos/{id}/comment-threads | Create a thread |
| GET | /api/v1/videos/{id}/comment-threads/{threadId} | Get a thread |
| GET | /api/v1/videos/comments | List instance comments |
| POST | /api/v1/videos/{id}/comments/{commentId} | Reply to a thread of a video |
| DELETE | /api/v1/videos/{id}/comments/{commentId} | Delete a comment or a reply |
| POST | /api/v1/videos/{id}/comments/{commentId}/approve | Approve a comment |
| PUT | /api/v1/videos/{id}/rate | Like/dislike a video |
| DELETE | /api/v1/videos/{id}/hls | Delete video HLS files |
| DELETE | /api/v1/videos/{id}/web-videos | Delete video Web Video files |
| POST | /api/v1/videos/{id}/transcoding | Create a transcoding job |
| GET | /api/v1/search/videos | Search videos |
| GET | /api/v1/search/video-channels | Search channels |
| GET | /api/v1/search/video-playlists | Search playlists |
| GET | /api/v1/blocklist/status | Get block status of accounts/hosts |
| GET | /api/v1/server/blocklist/accounts | List account blocks |
| POST | /api/v1/server/blocklist/accounts | Block an account |
| DELETE | /api/v1/server/blocklist/accounts/{accountName} | Unblock an account by its handle |
| GET | /api/v1/server/blocklist/servers | List server blocks |
| POST | /api/v1/server/blocklist/servers | Block a server |
| DELETE | /api/v1/server/blocklist/servers/{host} | Unblock a server by its domain |
| PUT | /api/v1/server/redundancy/{host} | Update a server redundancy policy |
| GET | /api/v1/server/redundancy/videos | List videos being mirrored |
| POST | /api/v1/server/redundancy/videos | Mirror a video |
| DELETE | /api/v1/server/redundancy/videos/{redundancyId} | Delete a mirror done on a video |
| GET | /api/v1/server/stats | Get instance stats |
| POST | /api/v1/server/logs/client | Send client log |
| GET | /api/v1/server/logs | Get instance logs |
| GET | /api/v1/server/audit-logs | Get instance audit logs |
| GET | /api/v1/plugins | List plugins |
| GET | /api/v1/plugins/available | List available plugins |
| POST | /api/v1/plugins/install | Install a plugin |
| POST | /api/v1/plugins/update | Update a plugin |
| POST | /api/v1/plugins/uninstall | Uninstall a plugin |
| GET | /api/v1/plugins/{npmName} | Get a plugin |
| PUT | /api/v1/plugins/{npmName}/settings | Set a plugin's settings |
| GET | /api/v1/plugins/{npmName}/public-settings | Get a plugin's public settings |
| GET | /api/v1/plugins/{npmName}/registered-settings | Get a plugin's registered settings |
| POST | /api/v1/metrics/playback | Create playback metrics |
| POST | /api/v1/runners/registration-tokens/generate | Generate registration token |
| DELETE | /api/v1/runners/registration-tokens/{registrationTokenId} | Remove registration token |
| GET | /api/v1/runners/registration-tokens | List registration tokens |
| POST | /api/v1/runners/register | Register a new runner |
| POST | /api/v1/runners/unregister | Unregister a runner |
| DELETE | /api/v1/runners/{runnerId} | Delete a runner |
| GET | /api/v1/runners | List runners |
| POST | /api/v1/runners/jobs/request | Request a new job |
| POST | /api/v1/runners/jobs/{jobUUID}/accept | Accept job |
| POST | /api/v1/runners/jobs/{jobUUID}/abort | Abort job |
| POST | /api/v1/runners/jobs/{jobUUID}/update | Update job |
| POST | /api/v1/runners/jobs/{jobUUID}/error | Post job error |
| POST | /api/v1/runners/jobs/{jobUUID}/success | Post job success |
| GET | /api/v1/runners/jobs/{jobUUID}/cancel | Cancel a job |
| DELETE | /api/v1/runners/jobs/{jobUUID} | Delete a job |
| GET | /api/v1/runners/jobs | List jobs |
| GET | /api/v1/automatic-tags/policies/accounts/{accountName}/comments | Get account auto tag policies on comments |
| PUT | /api/v1/automatic-tags/policies/accounts/{accountName}/comments | Update account auto tag policies on comments |
| GET | /api/v1/automatic-tags/accounts/{accountName}/available | Get account available auto tags |
| GET | /api/v1/automatic-tags/server/available | Get server available auto tags |
| GET | /api/v1/watched-words/accounts/{accountName}/lists | List account watched words |
| POST | /api/v1/watched-words/accounts/{accountName}/lists | Add account watched words |
| PUT | /api/v1/watched-words/accounts/{accountName}/lists/{listId} | Update account watched words |
| DELETE | /api/v1/watched-words/accounts/{accountName}/lists/{listId} | Delete account watched words |
| GET | /api/v1/watched-words/server/lists | List server watched words |
| POST | /api/v1/watched-words/server/lists | Add server watched words |
| PUT | /api/v1/watched-words/server/lists/{listId} | Update server watched words |
| DELETE | /api/v1/watched-words/server/lists/{listId} | Delete server watched words |
| POST | /api/v1/client-config/update-language | Update client language |
| GET | /api/v1/video-channels/{channelHandle}/collaborators | *List channel collaborators |
| POST | /api/v1/video-channels/{channelHandle}/collaborators/invite | Invite a collaborator |
| POST | /api/v1/video-channels/{channelHandle}/collaborators/{collaboratorId}/accept | Accept a collaboration invitation |
| POST | /api/v1/video-channels/{channelHandle}/collaborators/{collaboratorId}/reject | Reject a collaboration invitation |
| DELETE | /api/v1/video-channels/{channelHandle}/collaborators/{collaboratorId} | Remove a channel collaborator |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get web-video details?" -> GET /static/web-videos/{filename}
- "Get private details?" -> GET /static/web-videos/private/{filename}
- "Get hl details?" -> GET /static/streaming-playlists/hls/{filename}
- "Get private details?" -> GET /static/streaming-playlists/hls/private/{filename}
- "Get generate details?" -> GET /download/videos/generate/{videoId}
- "Get video-comments.{format} details?" -> GET /feeds/video-comments.{format}
- "Get videos.{format} details?" -> GET /feeds/videos.{format}
- "Get subscriptions.{format} details?" -> GET /feeds/subscriptions.{format}
- "List all videos.xml?" -> GET /feeds/podcast/videos.xml
- "Get account details?" -> GET /api/v1/accounts/{name}
- "Search videos?" -> GET /api/v1/accounts/{name}/videos
- "Search followers?" -> GET /api/v1/accounts/{name}/followers
- "List all accounts?" -> GET /api/v1/accounts
- "List all config?" -> GET /api/v1/config
- "List all about?" -> GET /api/v1/config/about
- "List all custom?" -> GET /api/v1/config/custom
- "Create a pick?" -> POST /api/v1/config/instance-banner/pick
- "Create a pick?" -> POST /api/v1/config/instance-avatar/pick
- "Create a pick?" -> POST /api/v1/config/instance-logo/{logoType}/pick
- "Delete a instance-logo?" -> DELETE /api/v1/config/instance-logo/{logoType}
- "List all instance?" -> GET /api/v1/custom-pages/homepage/instance
- "Create a pause?" -> POST /api/v1/jobs/pause
- "Create a resume?" -> POST /api/v1/jobs/resume
- "Get job details?" -> GET /api/v1/jobs/{state}
- "List all followers?" -> GET /api/v1/server/followers
- "Delete a follower?" -> DELETE /api/v1/server/followers/{handle}
- "Create a reject?" -> POST /api/v1/server/followers/{handle}/reject
- "Create a accept?" -> POST /api/v1/server/followers/{handle}/accept
- "List all following?" -> GET /api/v1/server/following
- "Create a following?" -> POST /api/v1/server/following
- "Delete a following?" -> DELETE /api/v1/server/following/{hostOrHandle}
- "Create a user?" -> POST /api/v1/users
- "Search users?" -> GET /api/v1/users
- "Delete a user?" -> DELETE /api/v1/users/{id}
- "Get user details?" -> GET /api/v1/users/{id}
- "Update a user?" -> PUT /api/v1/users/{id}
- "List all local?" -> GET /api/v1/oauth-clients/local
- "Create a token?" -> POST /api/v1/users/token
- "Create a revoke-token?" -> POST /api/v1/users/revoke-token
- "List all token-sessions?" -> GET /api/v1/users/{id}/token-sessions
- "List all revoke?" -> GET /api/v1/users/{id}/token-sessions/{tokenSessionId}/revoke
- "Create a ask-send-verify-email?" -> POST /api/v1/users/ask-send-verify-email
- "Create a ask-send-verify-email?" -> POST /api/v1/users/registrations/ask-send-verify-email
- "Create a verify-email?" -> POST /api/v1/users/{id}/verify-email
- "Create a verify-email?" -> POST /api/v1/users/registrations/{registrationId}/verify-email
- "Create a ask-reset-password?" -> POST /api/v1/users/ask-reset-password
- "Create a reset-password?" -> POST /api/v1/users/{id}/reset-password
- "Create a request?" -> POST /api/v1/users/{id}/two-factor/request
- "Create a confirm-request?" -> POST /api/v1/users/{id}/two-factor/confirm-request
- "Create a disable?" -> POST /api/v1/users/{id}/two-factor/disable
- "Create a import-resumable?" -> POST /api/v1/users/{userId}/imports/import-resumable
- "List all latest?" -> GET /api/v1/users/{userId}/imports/latest
- "Create a request?" -> POST /api/v1/users/{userId}/exports/request
- "List all exports?" -> GET /api/v1/users/{userId}/exports
- "Delete a export?" -> DELETE /api/v1/users/{userId}/exports/{id}
- "List all me?" -> GET /api/v1/users/me
- "Search comments?" -> GET /api/v1/users/me/videos/comments
- "Search imports?" -> GET /api/v1/users/me/videos/imports
- "List all video-quota-used?" -> GET /api/v1/users/me/video-quota-used
- "List all rating?" -> GET /api/v1/users/me/videos/{videoId}/rating
- "Search videos?" -> GET /api/v1/users/me/videos
- "List all subscriptions?" -> GET /api/v1/users/me/subscriptions
- "Create a subscription?" -> POST /api/v1/users/me/subscriptions
- "List all exist?" -> GET /api/v1/users/me/subscriptions/exist
- "Search videos?" -> GET /api/v1/users/me/subscriptions/videos
- "Get subscription details?" -> GET /api/v1/users/me/subscriptions/{subscriptionHandle}
- "Delete a subscription?" -> DELETE /api/v1/users/me/subscriptions/{subscriptionHandle}
- "List all notifications?" -> GET /api/v1/users/me/notifications
- "Create a read?" -> POST /api/v1/users/me/notifications/read
- "Create a read-all?" -> POST /api/v1/users/me/notifications/read-all
- "Create a read?" -> POST /api/v1/users/me/new-feature-info/read
- "Search videos?" -> GET /api/v1/users/me/history/videos
- "Delete a video?" -> DELETE /api/v1/users/me/history/videos/{videoId}
- "Create a remove?" -> POST /api/v1/users/me/history/videos/remove
- "Create a pick?" -> POST /api/v1/users/me/avatar/pick
- "Create a register?" -> POST /api/v1/users/register
- "Create a request?" -> POST /api/v1/users/registrations/request
- "Create a accept?" -> POST /api/v1/users/registrations/{registrationId}/accept
- "Create a reject?" -> POST /api/v1/users/registrations/{registrationId}/reject
- "Delete a registration?" -> DELETE /api/v1/users/registrations/{registrationId}
- "Search registrations?" -> GET /api/v1/users/registrations
- "List all ownership?" -> GET /api/v1/videos/ownership
- "Create a accept?" -> POST /api/v1/videos/ownership/{id}/accept
- "Create a refuse?" -> POST /api/v1/videos/ownership/{id}/refuse
- "Create a give-ownership?" -> POST /api/v1/videos/{id}/give-ownership
- "Create a token?" -> POST /api/v1/videos/{id}/token
- "Create a edit?" -> POST /api/v1/videos/{id}/studio/edit
- "Search videos?" -> GET /api/v1/videos
- "List all categories?" -> GET /api/v1/videos/categories
- "List all licences?" -> GET /api/v1/videos/licences
- "List all languages?" -> GET /api/v1/videos/languages
- "List all privacies?" -> GET /api/v1/videos/privacies
- "Update a video?" -> PUT /api/v1/videos/{id}
- "Get video details?" -> GET /api/v1/videos/{id}
- "Delete a video?" -> DELETE /api/v1/videos/{id}
- "List all description?" -> GET /api/v1/videos/{id}/description
- "Create a view?" -> POST /api/v1/videos/{id}/views
- "List all overall?" -> GET /api/v1/videos/{id}/stats/overall
- "List all user-agent?" -> GET /api/v1/videos/{id}/stats/user-agent
- "List all retention?" -> GET /api/v1/videos/{id}/stats/retention
- "Get timesery details?" -> GET /api/v1/videos/{id}/stats/timeseries/{metric}
- "Create a upload?" -> POST /api/v1/videos/upload
- "Create a upload-resumable?" -> POST /api/v1/videos/upload-resumable
- "Create a import?" -> POST /api/v1/videos/imports
- "Create a cancel?" -> POST /api/v1/videos/imports/{id}/cancel
- "Create a retry?" -> POST /api/v1/videos/imports/{id}/retry
- "Delete a import?" -> DELETE /api/v1/videos/imports/{id}
- "Create a live?" -> POST /api/v1/videos/live
- "Get live details?" -> GET /api/v1/videos/live/{id}
- "Update a live?" -> PUT /api/v1/videos/live/{id}
- "List all sessions?" -> GET /api/v1/videos/live/{id}/sessions
- "List all live-session?" -> GET /api/v1/videos/{id}/live-session
- "List all source?" -> GET /api/v1/videos/{id}/source
- "Create a replace-resumable?" -> POST /api/v1/videos/{id}/source/replace-resumable
- "List all abuses?" -> GET /api/v1/users/me/abuses
- "Search abuses?" -> GET /api/v1/abuses
- "Create a abuse?" -> POST /api/v1/abuses
- "Update a abuse?" -> PUT /api/v1/abuses/{abuseId}
- "Delete a abuse?" -> DELETE /api/v1/abuses/{abuseId}
- "List all messages?" -> GET /api/v1/abuses/{abuseId}/messages
- "Create a message?" -> POST /api/v1/abuses/{abuseId}/messages
- "Delete a message?" -> DELETE /api/v1/abuses/{abuseId}/messages/{abuseMessageId}
- "Create a blacklist?" -> POST /api/v1/videos/{id}/blacklist
- "Search blacklist?" -> GET /api/v1/videos/blacklist
- "List all storyboards?" -> GET /api/v1/videos/{id}/storyboards
- "List all captions?" -> GET /api/v1/videos/{id}/captions
- "Create a generate?" -> POST /api/v1/videos/{id}/captions/generate
- "Update a caption?" -> PUT /api/v1/videos/{id}/captions/{captionLanguage}
- "Delete a caption?" -> DELETE /api/v1/videos/{id}/captions/{captionLanguage}
- "List all chapters?" -> GET /api/v1/videos/{id}/chapters
- "List all embed-privacy?" -> GET /api/v1/videos/{id}/embed-privacy
- "List all allowed?" -> GET /api/v1/videos/{id}/embed-privacy/allowed
- "List all passwords?" -> GET /api/v1/videos/{id}/passwords
- "Create a password?" -> POST /api/v1/videos/{id}/passwords
- "Delete a password?" -> DELETE /api/v1/videos/{id}/passwords/{videoPasswordId}
- "List all video-channels?" -> GET /api/v1/video-channels
- "Create a video-channel?" -> POST /api/v1/video-channels
- "Get video-channel details?" -> GET /api/v1/video-channels/{channelHandle}
- "Update a video-channel?" -> PUT /api/v1/video-channels/{channelHandle}
- "Delete a video-channel?" -> DELETE /api/v1/video-channels/{channelHandle}
- "Search videos?" -> GET /api/v1/video-channels/{channelHandle}/videos
- "List all activities?" -> GET /api/v1/video-channels/{channelHandle}/activities
- "List all video-playlists?" -> GET /api/v1/video-channels/{channelHandle}/video-playlists
- "Create a reorder?" -> POST /api/v1/video-channels/{channelHandle}/video-playlists/reorder
- "Search followers?" -> GET /api/v1/video-channels/{channelHandle}/followers
- "Create a pick?" -> POST /api/v1/video-channels/{channelHandle}/avatar/pick
- "Create a pick?" -> POST /api/v1/video-channels/{channelHandle}/banner/pick
- "Create a import-video?" -> POST /api/v1/video-channels/{channelHandle}/import-videos
- "Create a video-channel-sync?" -> POST /api/v1/video-channel-syncs
- "Delete a video-channel-sync?" -> DELETE /api/v1/video-channel-syncs/{channelSyncId}
- "Create a sync?" -> POST /api/v1/video-channel-syncs/{channelSyncId}/sync
- "Get video details?" -> GET /api/v1/player-settings/videos/{id}
- "Update a video?" -> PUT /api/v1/player-settings/videos/{id}
- "Get video-channel details?" -> GET /api/v1/player-settings/video-channels/{channelHandle}
- "Update a video-channel?" -> PUT /api/v1/player-settings/video-channels/{channelHandle}
- "List all privacies?" -> GET /api/v1/video-playlists/privacies
- "List all video-playlists?" -> GET /api/v1/video-playlists
- "Create a video-playlist?" -> POST /api/v1/video-playlists
- "Get video-playlist details?" -> GET /api/v1/video-playlists/{playlistId}
- "Update a video-playlist?" -> PUT /api/v1/video-playlists/{playlistId}
- "Delete a video-playlist?" -> DELETE /api/v1/video-playlists/{playlistId}
- "List all videos?" -> GET /api/v1/video-playlists/{playlistId}/videos
- "Create a video?" -> POST /api/v1/video-playlists/{playlistId}/videos
- "Create a reorder?" -> POST /api/v1/video-playlists/{playlistId}/videos/reorder
- "Update a video?" -> PUT /api/v1/video-playlists/{playlistId}/videos/{playlistElementId}
- "Delete a video?" -> DELETE /api/v1/video-playlists/{playlistId}/videos/{playlistElementId}
- "List all videos-exist?" -> GET /api/v1/users/me/video-playlists/videos-exist
- "Search video-playlists?" -> GET /api/v1/accounts/{name}/video-playlists
- "Search video-channels?" -> GET /api/v1/accounts/{name}/video-channels
- "List all video-channel-syncs?" -> GET /api/v1/accounts/{name}/video-channel-syncs
- "List all ratings?" -> GET /api/v1/accounts/{name}/ratings
- "List all comment-threads?" -> GET /api/v1/videos/{id}/comment-threads
- "Create a comment-thread?" -> POST /api/v1/videos/{id}/comment-threads
- "Get comment-thread details?" -> GET /api/v1/videos/{id}/comment-threads/{threadId}
- "Search comments?" -> GET /api/v1/videos/comments
- "Delete a comment?" -> DELETE /api/v1/videos/{id}/comments/{commentId}
- "Create a approve?" -> POST /api/v1/videos/{id}/comments/{commentId}/approve
- "Create a transcoding?" -> POST /api/v1/videos/{id}/transcoding
- "Search videos?" -> GET /api/v1/search/videos
- "Search video-channels?" -> GET /api/v1/search/video-channels
- "Search video-playlists?" -> GET /api/v1/search/video-playlists
- "List all status?" -> GET /api/v1/blocklist/status
- "List all accounts?" -> GET /api/v1/server/blocklist/accounts
- "Create a account?" -> POST /api/v1/server/blocklist/accounts
- "Delete a account?" -> DELETE /api/v1/server/blocklist/accounts/{accountName}
- "List all servers?" -> GET /api/v1/server/blocklist/servers
- "Create a server?" -> POST /api/v1/server/blocklist/servers
- "Delete a server?" -> DELETE /api/v1/server/blocklist/servers/{host}
- "Update a redundancy?" -> PUT /api/v1/server/redundancy/{host}
- "List all videos?" -> GET /api/v1/server/redundancy/videos
- "Create a video?" -> POST /api/v1/server/redundancy/videos
- "Delete a video?" -> DELETE /api/v1/server/redundancy/videos/{redundancyId}
- "List all stats?" -> GET /api/v1/server/stats
- "Create a client?" -> POST /api/v1/server/logs/client
- "List all logs?" -> GET /api/v1/server/logs
- "List all audit-logs?" -> GET /api/v1/server/audit-logs
- "List all plugins?" -> GET /api/v1/plugins
- "Search available?" -> GET /api/v1/plugins/available
- "Create a install?" -> POST /api/v1/plugins/install
- "Create a update?" -> POST /api/v1/plugins/update
- "Create a uninstall?" -> POST /api/v1/plugins/uninstall
- "Get plugin details?" -> GET /api/v1/plugins/{npmName}
- "List all public-settings?" -> GET /api/v1/plugins/{npmName}/public-settings
- "List all registered-settings?" -> GET /api/v1/plugins/{npmName}/registered-settings
- "Create a playback?" -> POST /api/v1/metrics/playback
- "Create a generate?" -> POST /api/v1/runners/registration-tokens/generate
- "Delete a registration-token?" -> DELETE /api/v1/runners/registration-tokens/{registrationTokenId}
- "List all registration-tokens?" -> GET /api/v1/runners/registration-tokens
- "Create a register?" -> POST /api/v1/runners/register
- "Create a unregister?" -> POST /api/v1/runners/unregister
- "Delete a runner?" -> DELETE /api/v1/runners/{runnerId}
- "List all runners?" -> GET /api/v1/runners
- "Create a request?" -> POST /api/v1/runners/jobs/request
- "Create a accept?" -> POST /api/v1/runners/jobs/{jobUUID}/accept
- "Create a abort?" -> POST /api/v1/runners/jobs/{jobUUID}/abort
- "Create a update?" -> POST /api/v1/runners/jobs/{jobUUID}/update
- "Create a error?" -> POST /api/v1/runners/jobs/{jobUUID}/error
- "Create a success?" -> POST /api/v1/runners/jobs/{jobUUID}/success
- "List all cancel?" -> GET /api/v1/runners/jobs/{jobUUID}/cancel
- "Delete a job?" -> DELETE /api/v1/runners/jobs/{jobUUID}
- "Search jobs?" -> GET /api/v1/runners/jobs
- "List all comments?" -> GET /api/v1/automatic-tags/policies/accounts/{accountName}/comments
- "List all available?" -> GET /api/v1/automatic-tags/accounts/{accountName}/available
- "List all available?" -> GET /api/v1/automatic-tags/server/available
- "List all lists?" -> GET /api/v1/watched-words/accounts/{accountName}/lists
- "Create a list?" -> POST /api/v1/watched-words/accounts/{accountName}/lists
- "Update a list?" -> PUT /api/v1/watched-words/accounts/{accountName}/lists/{listId}
- "Delete a list?" -> DELETE /api/v1/watched-words/accounts/{accountName}/lists/{listId}
- "List all lists?" -> GET /api/v1/watched-words/server/lists
- "Create a list?" -> POST /api/v1/watched-words/server/lists
- "Update a list?" -> PUT /api/v1/watched-words/server/lists/{listId}
- "Delete a list?" -> DELETE /api/v1/watched-words/server/lists/{listId}
- "Create a update-language?" -> POST /api/v1/client-config/update-language
- "List all collaborators?" -> GET /api/v1/video-channels/{channelHandle}/collaborators
- "Create a invite?" -> POST /api/v1/video-channels/{channelHandle}/collaborators/invite
- "Create a accept?" -> POST /api/v1/video-channels/{channelHandle}/collaborators/{collaboratorId}/accept
- "Create a reject?" -> POST /api/v1/video-channels/{channelHandle}/collaborators/{collaboratorId}/reject
- "Delete a collaborator?" -> DELETE /api/v1/video-channels/{channelHandle}/collaborators/{collaboratorId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
