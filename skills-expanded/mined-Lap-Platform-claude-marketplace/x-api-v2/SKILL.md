---
name: x-api-v2
description: "X API v2 API skill. Use when working with X API v2 for 2. Covers 156 endpoints."
version: 1.0.0
generator: lapsh
---

# X API v2
API version: 2.159

## Auth
Bearer | OAuth2 | Oauth

## Base URL
https://api.x.com

## Setup
1. Set Authorization header with your Bearer token
2. GET /2/account_activity/subscriptions/count -- verify access
3. POST /2/account_activity/replay/webhooks/{webhook_id}/subscriptions/all -- create first all

## Endpoints

156 endpoints across 1 groups. See references/api-spec.lap for full details.

### 2
| Method | Path | Description |
|--------|------|-------------|
| POST | /2/account_activity/replay/webhooks/{webhook_id}/subscriptions/all | Create replay job |
| GET | /2/account_activity/subscriptions/count | Get subscription count |
| GET | /2/account_activity/webhooks/{webhook_id}/subscriptions/all | Validate subscription |
| POST | /2/account_activity/webhooks/{webhook_id}/subscriptions/all | Create subscription |
| GET | /2/account_activity/webhooks/{webhook_id}/subscriptions/all/list | Get subscriptions |
| DELETE | /2/account_activity/webhooks/{webhook_id}/subscriptions/{user_id}/all | Delete subscription |
| GET | /2/activity/stream | Activity Stream |
| GET | /2/activity/subscriptions | Get X activity subscriptions |
| POST | /2/activity/subscriptions | Create X activity subscription |
| DELETE | /2/activity/subscriptions/{subscription_id} | Deletes X activity subscription |
| PUT | /2/activity/subscriptions/{subscription_id} | Update X activity subscription |
| GET | /2/chat/conversations | Get Chat Conversations |
| GET | /2/chat/conversations/{conversation_id} | Get Chat Conversation |
| POST | /2/chat/conversations/{conversation_id}/messages | Send Chat Message |
| POST | /2/chat/conversations/{conversation_id}/read | Mark Conversation as Read |
| POST | /2/chat/conversations/{conversation_id}/typing | Send Typing Indicator |
| POST | /2/chat/media/upload/initialize | Initialize Chat Media Upload |
| POST | /2/chat/media/upload/{id}/append | Append Chat Media Upload |
| POST | /2/chat/media/upload/{id}/finalize | Finalize Chat Media Upload |
| GET | /2/chat/media/{conversation_id}/{media_hash_key} | Download Chat Media |
| GET | /2/communities/search | Search Communities |
| GET | /2/communities/{id} | Get Community by ID |
| GET | /2/compliance/jobs | Get Compliance Jobs |
| POST | /2/compliance/jobs | Create Compliance Job |
| GET | /2/compliance/jobs/{id} | Get Compliance Job by ID |
| DELETE | /2/connections | Terminate multiple connections |
| GET | /2/connections | Get Connection History |
| DELETE | /2/connections/all | Terminate all connections |
| DELETE | /2/connections/{endpoint_id} | Terminate connections by endpoint |
| POST | /2/dm_conversations | Create DM conversation |
| GET | /2/dm_conversations/with/{participant_id}/dm_events | Get DM events for a DM conversation |
| POST | /2/dm_conversations/with/{participant_id}/messages | Create DM message by participant ID |
| POST | /2/dm_conversations/{dm_conversation_id}/messages | Create DM message by conversation ID |
| GET | /2/dm_conversations/{id}/dm_events | Get DM events for a DM conversation |
| GET | /2/dm_events | Get DM events |
| DELETE | /2/dm_events/{event_id} | Delete DM event |
| GET | /2/dm_events/{event_id} | Get DM event by ID |
| POST | /2/evaluate_note | Evaluate a Community Note |
| GET | /2/insights/28hr | Get 28-hour Post insights |
| GET | /2/insights/historical | Get historical Post insights |
| GET | /2/likes/compliance/stream | Stream Likes compliance data |
| GET | /2/likes/firehose/stream | Stream all Likes |
| GET | /2/likes/sample10/stream | Stream sampled Likes |
| POST | /2/lists | Create List |
| DELETE | /2/lists/{id} | Delete List |
| GET | /2/lists/{id} | Get List by ID |
| PUT | /2/lists/{id} | Update List |
| GET | /2/lists/{id}/followers | Get List followers |
| GET | /2/lists/{id}/members | Get List members |
| POST | /2/lists/{id}/members | Add List member |
| DELETE | /2/lists/{id}/members/{user_id} | Remove List member |
| GET | /2/lists/{id}/tweets | Get List Posts |
| GET | /2/media | Get Media by media keys |
| GET | /2/media/analytics | Get Media analytics |
| POST | /2/media/metadata | Create Media metadata |
| DELETE | /2/media/subtitles | Delete Media subtitles |
| POST | /2/media/subtitles | Create Media subtitles |
| GET | /2/media/upload | Get Media upload status |
| POST | /2/media/upload | Upload media |
| POST | /2/media/upload/initialize | Initialize media upload |
| POST | /2/media/upload/{id}/append | Append Media upload |
| POST | /2/media/upload/{id}/finalize | Finalize Media upload |
| GET | /2/media/{media_key} | Get Media by media key |
| GET | /2/news/search | Search News |
| GET | /2/news/{id} | Get news stories by ID |
| POST | /2/notes | Create a Community Note |
| GET | /2/notes/search/notes_written | Search for Community Notes Written |
| GET | /2/notes/search/posts_eligible_for_notes | Search for Posts Eligible for Community Notes |
| DELETE | /2/notes/{id} | Delete a Community Note |
| GET | /2/openapi.json | Get OpenAPI Spec. |
| GET | /2/spaces | Get Spaces by IDs |
| GET | /2/spaces/by/creator_ids | Get Spaces by creator IDs |
| GET | /2/spaces/search | Search Spaces |
| GET | /2/spaces/{id} | Get space by ID |
| GET | /2/spaces/{id}/buyers | Get Space ticket buyers |
| GET | /2/spaces/{id}/tweets | Get Space Posts |
| GET | /2/trends/by/woeid/{woeid} | Get Trends by WOEID |
| GET | /2/tweets | Get Posts by IDs |
| POST | /2/tweets | Create or Edit Post |
| GET | /2/tweets/analytics | Get Post analytics |
| GET | /2/tweets/compliance/stream | Stream Posts compliance data |
| GET | /2/tweets/counts/all | Get count of all Posts |
| GET | /2/tweets/counts/recent | Get count of recent Posts |
| GET | /2/tweets/firehose/stream | Stream all Posts |
| GET | /2/tweets/firehose/stream/lang/en | Stream English Posts |
| GET | /2/tweets/firehose/stream/lang/ja | Stream Japanese Posts |
| GET | /2/tweets/firehose/stream/lang/ko | Stream Korean Posts |
| GET | /2/tweets/firehose/stream/lang/pt | Stream Portuguese Posts |
| GET | /2/tweets/label/stream | Stream Post labels |
| GET | /2/tweets/sample/stream | Stream sampled Posts |
| GET | /2/tweets/sample10/stream | Stream 10% sampled Posts |
| GET | /2/tweets/search/all | Search all Posts |
| GET | /2/tweets/search/recent | Search recent Posts |
| GET | /2/tweets/search/stream | Stream filtered Posts |
| GET | /2/tweets/search/stream/rules | Get stream rules |
| POST | /2/tweets/search/stream/rules | Update stream rules |
| GET | /2/tweets/search/stream/rules/counts | Get stream rule counts |
| GET | /2/tweets/search/webhooks | Get stream links |
| DELETE | /2/tweets/search/webhooks/{webhook_id} | Delete stream link |
| POST | /2/tweets/search/webhooks/{webhook_id} | Create stream link |
| DELETE | /2/tweets/{id} | Delete Post |
| GET | /2/tweets/{id} | Get Post by ID |
| GET | /2/tweets/{id}/liking_users | Get Liking Users |
| GET | /2/tweets/{id}/quote_tweets | Get Quoted Posts |
| GET | /2/tweets/{id}/retweeted_by | Get Reposted by |
| GET | /2/tweets/{id}/retweets | Get Reposts |
| PUT | /2/tweets/{tweet_id}/hidden | Hide reply |
| GET | /2/usage/tweets | Get usage |
| GET | /2/users | Get Users by IDs |
| GET | /2/users/by | Get Users by usernames |
| GET | /2/users/by/username/{username} | Get User by username |
| GET | /2/users/compliance/stream | Stream Users compliance data |
| GET | /2/users/me | Get my User |
| GET | /2/users/personalized_trends | Get personalized Trends |
| GET | /2/users/reposts_of_me | Get Reposts of me |
| GET | /2/users/search | Search Users |
| GET | /2/users/{id} | Get User by ID |
| GET | /2/users/{id}/affiliates | Get affiliates |
| GET | /2/users/{id}/blocking | Get blocking |
| GET | /2/users/{id}/bookmarks | Get Bookmarks |
| POST | /2/users/{id}/bookmarks | Create Bookmark |
| GET | /2/users/{id}/bookmarks/folders | Get Bookmark folders |
| GET | /2/users/{id}/bookmarks/folders/{folder_id} | Get Bookmarks by folder ID |
| DELETE | /2/users/{id}/bookmarks/{tweet_id} | Delete Bookmark |
| POST | /2/users/{id}/dm/block | Block DMs |
| POST | /2/users/{id}/dm/unblock | Unblock DMs |
| GET | /2/users/{id}/followed_lists | Get followed Lists |
| POST | /2/users/{id}/followed_lists | Follow List |
| DELETE | /2/users/{id}/followed_lists/{list_id} | Unfollow List |
| GET | /2/users/{id}/followers | Get followers |
| GET | /2/users/{id}/following | Get following |
| POST | /2/users/{id}/following | Follow User |
| GET | /2/users/{id}/liked_tweets | Get liked Posts |
| POST | /2/users/{id}/likes | Like Post |
| DELETE | /2/users/{id}/likes/{tweet_id} | Unlike Post |
| GET | /2/users/{id}/list_memberships | Get List memberships |
| GET | /2/users/{id}/mentions | Get mentions |
| GET | /2/users/{id}/muting | Get muting |
| POST | /2/users/{id}/muting | Mute User |
| GET | /2/users/{id}/owned_lists | Get owned Lists |
| GET | /2/users/{id}/pinned_lists | Get pinned Lists |
| POST | /2/users/{id}/pinned_lists | Pin List |
| DELETE | /2/users/{id}/pinned_lists/{list_id} | Unpin List |
| GET | /2/users/{id}/public_keys | Get user public keys |
| POST | /2/users/{id}/public_keys | Add public key |
| POST | /2/users/{id}/retweets | Repost Post |
| DELETE | /2/users/{id}/retweets/{source_tweet_id} | Unrepost Post |
| GET | /2/users/{id}/timelines/reverse_chronological | Get Timeline |
| GET | /2/users/{id}/tweets | Get Posts |
| DELETE | /2/users/{source_user_id}/following/{target_user_id} | Unfollow User |
| DELETE | /2/users/{source_user_id}/muting/{target_user_id} | Unmute User |
| GET | /2/webhooks | Get webhook |
| POST | /2/webhooks | Create webhook |
| POST | /2/webhooks/replay | Create replay job for webhook |
| DELETE | /2/webhooks/{webhook_id} | Delete webhook |
| PUT | /2/webhooks/{webhook_id} | Validate webhook |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a all?" -> POST /2/account_activity/replay/webhooks/{webhook_id}/subscriptions/all
- "List all count?" -> GET /2/account_activity/subscriptions/count
- "List all all?" -> GET /2/account_activity/webhooks/{webhook_id}/subscriptions/all
- "Create a all?" -> POST /2/account_activity/webhooks/{webhook_id}/subscriptions/all
- "List all list?" -> GET /2/account_activity/webhooks/{webhook_id}/subscriptions/all/list
- "List all stream?" -> GET /2/activity/stream
- "List all subscriptions?" -> GET /2/activity/subscriptions
- "Create a subscription?" -> POST /2/activity/subscriptions
- "Delete a subscription?" -> DELETE /2/activity/subscriptions/{subscription_id}
- "Update a subscription?" -> PUT /2/activity/subscriptions/{subscription_id}
- "List all conversations?" -> GET /2/chat/conversations
- "Get conversation details?" -> GET /2/chat/conversations/{conversation_id}
- "Create a message?" -> POST /2/chat/conversations/{conversation_id}/messages
- "Create a read?" -> POST /2/chat/conversations/{conversation_id}/read
- "Create a typing?" -> POST /2/chat/conversations/{conversation_id}/typing
- "Create a initialize?" -> POST /2/chat/media/upload/initialize
- "Create a append?" -> POST /2/chat/media/upload/{id}/append
- "Create a finalize?" -> POST /2/chat/media/upload/{id}/finalize
- "Get media details?" -> GET /2/chat/media/{conversation_id}/{media_hash_key}
- "Search search?" -> GET /2/communities/search
- "Get community details?" -> GET /2/communities/{id}
- "List all jobs?" -> GET /2/compliance/jobs
- "Create a job?" -> POST /2/compliance/jobs
- "Get job details?" -> GET /2/compliance/jobs/{id}
- "List all connections?" -> GET /2/connections
- "Delete a connection?" -> DELETE /2/connections/{endpoint_id}
- "Create a dm_conversation?" -> POST /2/dm_conversations
- "List all dm_events?" -> GET /2/dm_conversations/with/{participant_id}/dm_events
- "Create a message?" -> POST /2/dm_conversations/with/{participant_id}/messages
- "Create a message?" -> POST /2/dm_conversations/{dm_conversation_id}/messages
- "List all dm_events?" -> GET /2/dm_conversations/{id}/dm_events
- "List all dm_events?" -> GET /2/dm_events
- "Delete a dm_event?" -> DELETE /2/dm_events/{event_id}
- "Get dm_event details?" -> GET /2/dm_events/{event_id}
- "Create a evaluate_note?" -> POST /2/evaluate_note
- "List all 28hr?" -> GET /2/insights/28hr
- "List all historical?" -> GET /2/insights/historical
- "List all stream?" -> GET /2/likes/compliance/stream
- "List all stream?" -> GET /2/likes/firehose/stream
- "List all stream?" -> GET /2/likes/sample10/stream
- "Create a list?" -> POST /2/lists
- "Delete a list?" -> DELETE /2/lists/{id}
- "Get list details?" -> GET /2/lists/{id}
- "Update a list?" -> PUT /2/lists/{id}
- "List all followers?" -> GET /2/lists/{id}/followers
- "List all members?" -> GET /2/lists/{id}/members
- "Create a member?" -> POST /2/lists/{id}/members
- "Delete a member?" -> DELETE /2/lists/{id}/members/{user_id}
- "List all tweets?" -> GET /2/lists/{id}/tweets
- "List all media?" -> GET /2/media
- "List all analytics?" -> GET /2/media/analytics
- "Create a metadata?" -> POST /2/media/metadata
- "Create a subtitle?" -> POST /2/media/subtitles
- "List all upload?" -> GET /2/media/upload
- "Create a upload?" -> POST /2/media/upload
- "Create a initialize?" -> POST /2/media/upload/initialize
- "Create a append?" -> POST /2/media/upload/{id}/append
- "Create a finalize?" -> POST /2/media/upload/{id}/finalize
- "Get media details?" -> GET /2/media/{media_key}
- "Search search?" -> GET /2/news/search
- "Get new details?" -> GET /2/news/{id}
- "Create a note?" -> POST /2/notes
- "List all notes_written?" -> GET /2/notes/search/notes_written
- "List all posts_eligible_for_notes?" -> GET /2/notes/search/posts_eligible_for_notes
- "Delete a note?" -> DELETE /2/notes/{id}
- "List all openapi.json?" -> GET /2/openapi.json
- "List all spaces?" -> GET /2/spaces
- "List all creator_ids?" -> GET /2/spaces/by/creator_ids
- "Search search?" -> GET /2/spaces/search
- "Get space details?" -> GET /2/spaces/{id}
- "List all buyers?" -> GET /2/spaces/{id}/buyers
- "List all tweets?" -> GET /2/spaces/{id}/tweets
- "Get woeid details?" -> GET /2/trends/by/woeid/{woeid}
- "List all tweets?" -> GET /2/tweets
- "Create a tweet?" -> POST /2/tweets
- "List all analytics?" -> GET /2/tweets/analytics
- "List all stream?" -> GET /2/tweets/compliance/stream
- "Search all?" -> GET /2/tweets/counts/all
- "Search recent?" -> GET /2/tweets/counts/recent
- "List all stream?" -> GET /2/tweets/firehose/stream
- "List all en?" -> GET /2/tweets/firehose/stream/lang/en
- "List all ja?" -> GET /2/tweets/firehose/stream/lang/ja
- "List all ko?" -> GET /2/tweets/firehose/stream/lang/ko
- "List all pt?" -> GET /2/tweets/firehose/stream/lang/pt
- "List all stream?" -> GET /2/tweets/label/stream
- "List all stream?" -> GET /2/tweets/sample/stream
- "List all stream?" -> GET /2/tweets/sample10/stream
- "Search all?" -> GET /2/tweets/search/all
- "Search recent?" -> GET /2/tweets/search/recent
- "List all stream?" -> GET /2/tweets/search/stream
- "List all rules?" -> GET /2/tweets/search/stream/rules
- "Create a rule?" -> POST /2/tweets/search/stream/rules
- "List all counts?" -> GET /2/tweets/search/stream/rules/counts
- "List all webhooks?" -> GET /2/tweets/search/webhooks
- "Delete a webhook?" -> DELETE /2/tweets/search/webhooks/{webhook_id}
- "Delete a tweet?" -> DELETE /2/tweets/{id}
- "Get tweet details?" -> GET /2/tweets/{id}
- "List all liking_users?" -> GET /2/tweets/{id}/liking_users
- "List all quote_tweets?" -> GET /2/tweets/{id}/quote_tweets
- "List all retweeted_by?" -> GET /2/tweets/{id}/retweeted_by
- "List all retweets?" -> GET /2/tweets/{id}/retweets
- "List all tweets?" -> GET /2/usage/tweets
- "List all users?" -> GET /2/users
- "List all by?" -> GET /2/users/by
- "Get username details?" -> GET /2/users/by/username/{username}
- "List all stream?" -> GET /2/users/compliance/stream
- "List all me?" -> GET /2/users/me
- "List all personalized_trends?" -> GET /2/users/personalized_trends
- "List all reposts_of_me?" -> GET /2/users/reposts_of_me
- "Search search?" -> GET /2/users/search
- "Get user details?" -> GET /2/users/{id}
- "List all affiliates?" -> GET /2/users/{id}/affiliates
- "List all blocking?" -> GET /2/users/{id}/blocking
- "List all bookmarks?" -> GET /2/users/{id}/bookmarks
- "Create a bookmark?" -> POST /2/users/{id}/bookmarks
- "List all folders?" -> GET /2/users/{id}/bookmarks/folders
- "Get folder details?" -> GET /2/users/{id}/bookmarks/folders/{folder_id}
- "Delete a bookmark?" -> DELETE /2/users/{id}/bookmarks/{tweet_id}
- "Create a block?" -> POST /2/users/{id}/dm/block
- "Create a unblock?" -> POST /2/users/{id}/dm/unblock
- "List all followed_lists?" -> GET /2/users/{id}/followed_lists
- "Create a followed_list?" -> POST /2/users/{id}/followed_lists
- "Delete a followed_list?" -> DELETE /2/users/{id}/followed_lists/{list_id}
- "List all followers?" -> GET /2/users/{id}/followers
- "List all following?" -> GET /2/users/{id}/following
- "Create a following?" -> POST /2/users/{id}/following
- "List all liked_tweets?" -> GET /2/users/{id}/liked_tweets
- "Create a like?" -> POST /2/users/{id}/likes
- "Delete a like?" -> DELETE /2/users/{id}/likes/{tweet_id}
- "List all list_memberships?" -> GET /2/users/{id}/list_memberships
- "List all mentions?" -> GET /2/users/{id}/mentions
- "List all muting?" -> GET /2/users/{id}/muting
- "Create a muting?" -> POST /2/users/{id}/muting
- "List all owned_lists?" -> GET /2/users/{id}/owned_lists
- "List all pinned_lists?" -> GET /2/users/{id}/pinned_lists
- "Create a pinned_list?" -> POST /2/users/{id}/pinned_lists
- "Delete a pinned_list?" -> DELETE /2/users/{id}/pinned_lists/{list_id}
- "List all public_keys?" -> GET /2/users/{id}/public_keys
- "Create a public_key?" -> POST /2/users/{id}/public_keys
- "Create a retweet?" -> POST /2/users/{id}/retweets
- "Delete a retweet?" -> DELETE /2/users/{id}/retweets/{source_tweet_id}
- "List all reverse_chronological?" -> GET /2/users/{id}/timelines/reverse_chronological
- "List all tweets?" -> GET /2/users/{id}/tweets
- "Delete a following?" -> DELETE /2/users/{source_user_id}/following/{target_user_id}
- "Delete a muting?" -> DELETE /2/users/{source_user_id}/muting/{target_user_id}
- "List all webhooks?" -> GET /2/webhooks
- "Create a webhook?" -> POST /2/webhooks
- "Create a replay?" -> POST /2/webhooks/replay
- "Delete a webhook?" -> DELETE /2/webhooks/{webhook_id}
- "Update a webhook?" -> PUT /2/webhooks/{webhook_id}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
