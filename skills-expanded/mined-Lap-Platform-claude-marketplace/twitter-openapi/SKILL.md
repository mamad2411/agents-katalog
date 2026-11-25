---
name: twitter-openapi
description: "Twitter OpenAPI API skill. Use when working with Twitter OpenAPI for 1.1, 2, graphql. Covers 39 endpoints."
version: 1.0.0
generator: lapsh
---

# Twitter OpenAPI
API version: 0.0.1

## Auth
ApiKey Accept in header | ApiKey Accept-Encoding in header | ApiKey Accept-Language in header | ApiKey x-twitter-active-user in header | ApiKey x-twitter-auth-type in header | Bearer bearer | ApiKey x-twitter-client-language in header | ApiKey x-client-transaction-id in header | ApiKey x-client-uuid in header | ApiKey auth_token in cookie | ApiKey ct0 in cookie | ApiKey gt0 in cookie | ApiKey x-csrf-token in header | ApiKey x-guest-token in header | ApiKey Priority in header | ApiKey Referer in header | ApiKey Sec-Ch-Ua in header | ApiKey Sec-Ch-Ua-Mobile in header | ApiKey Sec-Ch-Ua-Platform in header | ApiKey Sec-Fetch-Dest in header | ApiKey Sec-Fetch-Mode in header | ApiKey Sec-Fetch-Site in header | ApiKey user-agent in header

## Base URL
https://x.com/i/api

## Setup
1. Set Authorization header with your Bearer token
2. GET /1.1/friends/following/list.json -- verify access
3. POST /1.1/friendships/create.json -- create first create.json

## Endpoints

39 endpoints across 4 groups. See references/api-spec.lap for full details.

### 1.1
| Method | Path | Description |
|--------|------|-------------|
| GET | /1.1/friends/following/list.json | get friends following list |
| POST | /1.1/friendships/create.json | post create friendships |
| POST | /1.1/friendships/destroy.json | post destroy friendships |
| GET | /1.1/search/typeahead.json | get search typeahead |

### 2
| Method | Path | Description |
|--------|------|-------------|
| GET | /2/search/adaptive.json | get search adaptive |

### graphql
| Method | Path | Description |
|--------|------|-------------|
| GET | /graphql/{pathQueryId}/Bookmarks | get bookmarks |
| GET | /graphql/{pathQueryId}/CommunityAboutTimeline | get about of community |
| GET | /graphql/{pathQueryId}/CommunityMediaTimeline | get media list of community |
| GET | /graphql/{pathQueryId}/CommunityTweetsTimeline | get tweet list of community. rankingMode:[Recency, Relevance] |
| POST | /graphql/{pathQueryId}/CreateBookmark | create Bookmark |
| POST | /graphql/{pathQueryId}/CreateRetweet | create Retweet |
| POST | /graphql/{pathQueryId}/CreateTweet | create Tweet |
| POST | /graphql/{pathQueryId}/DeleteBookmark | delete Bookmark |
| POST | /graphql/{pathQueryId}/DeleteRetweet | delete Retweet |
| POST | /graphql/{pathQueryId}/DeleteTweet | delete Retweet |
| POST | /graphql/{pathQueryId}/FavoriteTweet | favorite Tweet |
| GET | /graphql/{pathQueryId}/Favoriters | get tweet favoriters |
| GET | /graphql/{pathQueryId}/Followers | get user list of followers |
| GET | /graphql/{pathQueryId}/FollowersYouKnow | get followers you know |
| GET | /graphql/{pathQueryId}/Following | get user list of following |
| GET | /graphql/{pathQueryId}/HomeLatestTimeline | get tweet list of timeline |
| GET | /graphql/{pathQueryId}/HomeTimeline | get tweet list of timeline |
| GET | /graphql/{pathQueryId}/Likes | get user likes tweets |
| GET | /graphql/{pathQueryId}/ListLatestTweetsTimeline | get tweet list of timeline |
| GET | /graphql/{pathQueryId}/NotificationsTimeline | get notification list. timeline_type:[All, Verified, Mentions] |
| GET | /graphql/{pathQueryId}/ProfileSpotlightsQuery | get user by screen name |
| GET | /graphql/{pathQueryId}/Retweeters | get tweet retweeters |
| GET | /graphql/{pathQueryId}/SearchTimeline | search tweet list. product:[Top, Latest, People, Photos, Videos] |
| GET | /graphql/{pathQueryId}/TweetDetail | get TweetDetail |
| GET | /graphql/{pathQueryId}/TweetResultByRestId | get TweetResultByRestId |
| POST | /graphql/{pathQueryId}/UnfavoriteTweet | unfavorite Tweet |
| GET | /graphql/{pathQueryId}/UserByRestId | get user by rest id |
| GET | /graphql/{pathQueryId}/UserByScreenName | get user by screen name |
| GET | /graphql/{pathQueryId}/UserHighlightsTweets | get user highlights tweets |
| GET | /graphql/{pathQueryId}/UserMedia | get user media tweets |
| GET | /graphql/{pathQueryId}/UserTweets | get user tweets |
| GET | /graphql/{pathQueryId}/UserTweetsAndReplies | get user replies tweets |
| GET | /graphql/{pathQueryId}/UsersByRestIds | get users by rest ids |

### other
| Method | Path | Description |
|--------|------|-------------|
| GET | /other | This is not an actual endpoint |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all list.json?" -> GET /1.1/friends/following/list.json
- "Create a create.json?" -> POST /1.1/friendships/create.json
- "Create a destroy.json?" -> POST /1.1/friendships/destroy.json
- "Search typeahead.json?" -> GET /1.1/search/typeahead.json
- "Search adaptive.json?" -> GET /2/search/adaptive.json
- "List all Bookmarks?" -> GET /graphql/{pathQueryId}/Bookmarks
- "List all CommunityAboutTimeline?" -> GET /graphql/{pathQueryId}/CommunityAboutTimeline
- "List all CommunityMediaTimeline?" -> GET /graphql/{pathQueryId}/CommunityMediaTimeline
- "List all CommunityTweetsTimeline?" -> GET /graphql/{pathQueryId}/CommunityTweetsTimeline
- "Create a CreateBookmark?" -> POST /graphql/{pathQueryId}/CreateBookmark
- "Create a CreateRetweet?" -> POST /graphql/{pathQueryId}/CreateRetweet
- "Create a CreateTweet?" -> POST /graphql/{pathQueryId}/CreateTweet
- "Create a DeleteBookmark?" -> POST /graphql/{pathQueryId}/DeleteBookmark
- "Create a DeleteRetweet?" -> POST /graphql/{pathQueryId}/DeleteRetweet
- "Create a DeleteTweet?" -> POST /graphql/{pathQueryId}/DeleteTweet
- "Create a FavoriteTweet?" -> POST /graphql/{pathQueryId}/FavoriteTweet
- "List all Favoriters?" -> GET /graphql/{pathQueryId}/Favoriters
- "List all Followers?" -> GET /graphql/{pathQueryId}/Followers
- "List all FollowersYouKnow?" -> GET /graphql/{pathQueryId}/FollowersYouKnow
- "List all Following?" -> GET /graphql/{pathQueryId}/Following
- "List all HomeLatestTimeline?" -> GET /graphql/{pathQueryId}/HomeLatestTimeline
- "List all HomeTimeline?" -> GET /graphql/{pathQueryId}/HomeTimeline
- "List all Likes?" -> GET /graphql/{pathQueryId}/Likes
- "List all ListLatestTweetsTimeline?" -> GET /graphql/{pathQueryId}/ListLatestTweetsTimeline
- "List all NotificationsTimeline?" -> GET /graphql/{pathQueryId}/NotificationsTimeline
- "List all ProfileSpotlightsQuery?" -> GET /graphql/{pathQueryId}/ProfileSpotlightsQuery
- "List all Retweeters?" -> GET /graphql/{pathQueryId}/Retweeters
- "List all SearchTimeline?" -> GET /graphql/{pathQueryId}/SearchTimeline
- "List all TweetDetail?" -> GET /graphql/{pathQueryId}/TweetDetail
- "List all TweetResultByRestId?" -> GET /graphql/{pathQueryId}/TweetResultByRestId
- "Create a UnfavoriteTweet?" -> POST /graphql/{pathQueryId}/UnfavoriteTweet
- "List all UserByRestId?" -> GET /graphql/{pathQueryId}/UserByRestId
- "List all UserByScreenName?" -> GET /graphql/{pathQueryId}/UserByScreenName
- "List all UserHighlightsTweets?" -> GET /graphql/{pathQueryId}/UserHighlightsTweets
- "List all UserMedia?" -> GET /graphql/{pathQueryId}/UserMedia
- "List all UserTweets?" -> GET /graphql/{pathQueryId}/UserTweets
- "List all UserTweetsAndReplies?" -> GET /graphql/{pathQueryId}/UserTweetsAndReplies
- "List all UsersByRestIds?" -> GET /graphql/{pathQueryId}/UsersByRestIds
- "List all other?" -> GET /other
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
