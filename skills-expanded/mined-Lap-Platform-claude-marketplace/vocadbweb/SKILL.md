---
name: vocadbweb
description: "VocaDbWeb API skill. Use when working with VocaDbWeb for api. Covers 134 endpoints."
version: 1.0.0
generator: lapsh
---

# VocaDbWeb
API version: 1.0

## Auth
No authentication required.

## Base URL
Not specified.

## Setup
1. No auth setup needed
2. GET /api/activityEntries -- verify access
3. POST /api/albums/comments/{commentId} -- create first comments

## Endpoints

134 endpoints across 1 groups. See references/api-spec.lap for full details.

### api
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/activityEntries |  |
| DELETE | /api/albums/{id} |  |
| GET | /api/albums/{id} |  |
| DELETE | /api/albums/comments/{commentId} |  |
| POST | /api/albums/comments/{commentId} |  |
| GET | /api/albums/{id}/comments |  |
| POST | /api/albums/{id}/comments |  |
| GET | /api/albums |  |
| GET | /api/albums/names |  |
| GET | /api/albums/new |  |
| GET | /api/albums/{id}/reviews |  |
| POST | /api/albums/{id}/reviews |  |
| GET | /api/albums/{id}/user-collections |  |
| DELETE | /api/albums/{id}/reviews/{reviewId} |  |
| GET | /api/albums/top |  |
| GET | /api/albums/{id}/tracks |  |
| GET | /api/albums/{id}/tracks/fields |  |
| GET | /api/albums/{id}/related |  |
| DELETE | /api/artists/{id} |  |
| GET | /api/artists/{id} |  |
| DELETE | /api/artists/comments/{commentId} |  |
| POST | /api/artists/comments/{commentId} |  |
| GET | /api/artists/{id}/comments |  |
| POST | /api/artists/{id}/comments |  |
| GET | /api/artists |  |
| GET | /api/artists/names |  |
| DELETE | /api/comments/{entryType}-comments/{commentId} |  |
| POST | /api/comments/{entryType}-comments/{commentId} |  |
| GET | /api/comments/{entryType}-comments |  |
| POST | /api/comments/{entryType}-comments |  |
| GET | /api/comments/{entryType}-comments/{entryId}/locked |  |
| POST | /api/comments/{entryType}-comments/{entryId}/locked |  |
| GET | /api/comments |  |
| DELETE | /api/discussions/comments/{commentId} |  |
| POST | /api/discussions/comments/{commentId} |  |
| DELETE | /api/discussions/topics/{topicId} |  |
| GET | /api/discussions/topics/{topicId} |  |
| POST | /api/discussions/topics/{topicId} |  |
| GET | /api/discussions/folders |  |
| POST | /api/discussions/folders |  |
| GET | /api/discussions/topics |  |
| GET | /api/discussions/folders/{folderId}/topics |  |
| POST | /api/discussions/folders/{folderId}/topics |  |
| POST | /api/discussions/topics/{topicId}/comments |  |
| GET | /api/entries |  |
| GET | /api/entries/random |  |
| GET | /api/entries/names |  |
| GET | /api/entry-types/{entryType}/{subType}/tag |  |
| GET | /api/pvs/for-songs |  |
| GET | /api/pvs/thumbnail |  |
| DELETE | /api/releaseEvents/{id} |  |
| GET | /api/releaseEvents/{id} |  |
| GET | /api/releaseEvents/{eventId}/albums |  |
| GET | /api/releaseEvents/{eventId}/published-songs |  |
| GET | /api/releaseEvents |  |
| GET | /api/releaseEvents/names |  |
| POST | /api/releaseEvents/{eventId}/reports |  |
| DELETE | /api/releaseEventSeries/{id} |  |
| GET | /api/releaseEventSeries/{id} |  |
| GET | /api/releaseEventSeries |  |
| GET | /api/releaseEventSeries/{id}/for-edit |  |
| GET | /api/resources/{cultureCode} |  |
| DELETE | /api/songs/comments/{commentId} |  |
| POST | /api/songs/comments/{commentId} |  |
| DELETE | /api/songs/{id} |  |
| GET | /api/songs/{id} |  |
| GET | /api/songs/{id}/comments |  |
| POST | /api/songs/{id}/comments |  |
| GET | /api/songs/{id}/derived |  |
| GET | /api/songs/highlighted |  |
| GET | /api/songs/{id}/ratings |  |
| POST | /api/songs/{id}/ratings |  |
| GET | /api/songs/{id}/related |  |
| GET | /api/songs |  |
| GET | /api/songs/lyrics/{lyricsId} |  |
| GET | /api/songs/names |  |
| GET | /api/songs/byPv |  |
| GET | /api/songs/top-rated |  |
| DELETE | /api/songLists/{id} |  |
| DELETE | /api/songLists/comments/{commentId} |  |
| POST | /api/songLists/comments/{commentId} |  |
| GET | /api/songLists/{listId}/comments |  |
| POST | /api/songLists/{listId}/comments |  |
| GET | /api/songLists/featured |  |
| GET | /api/songLists/featured/names |  |
| GET | /api/songLists/{listId}/songs |  |
| POST | /api/songLists |  |
| DELETE | /api/tags/{id} |  |
| GET | /api/tags/{id} |  |
| DELETE | /api/tags/comments/{commentId} |  |
| POST | /api/tags/comments/{commentId} |  |
| GET | /api/tags/byName/{name} |  |
| GET | /api/tags/categoryNames |  |
| GET | /api/tags/{tagId}/children |  |
| GET | /api/tags/{tagId}/comments |  |
| POST | /api/tags/{tagId}/comments |  |
| GET | /api/tags |  |
| POST | /api/tags |  |
| GET | /api/tags/names |  |
| GET | /api/tags/top |  |
| POST | /api/tags/{tagId}/reports |  |
| DELETE | /api/users/current/followedTags/{tagId} |  |
| POST | /api/users/current/followedTags/{tagId} |  |
| DELETE | /api/users/profileComments/{commentId} |  |
| POST | /api/users/profileComments/{commentId} |  |
| GET | /api/users/{id}/albums |  |
| GET | /api/users/current |  |
| GET | /api/users/{id}/events |  |
| GET | /api/users/{id}/followedArtists |  |
| GET | /api/users |  |
| GET | /api/users/{id} |  |
| GET | /api/users/messages/{messageId} |  |
| GET | /api/users/{id}/messages |  |
| DELETE | /api/users/{id}/messages |  |
| POST | /api/users/{id}/messages |  |
| GET | /api/users/names |  |
| GET | /api/users/{id}/profileComments |  |
| POST | /api/users/{id}/profileComments |  |
| GET | /api/users/{id}/ratedSongs |  |
| GET | /api/users/{id}/songLists |  |
| GET | /api/users/{id}/ratedSongs/{songId} |  |
| GET | /api/users/current/ratedSongs/{songId} |  |
| POST | /api/users/current/albums/{albumId} |  |
| POST | /api/users/current/refreshEntryEdit |  |
| POST | /api/users/{id}/reports |  |
| POST | /api/users/current/songTags/{songId} |  |
| POST | /api/users/{id}/settings/{settingName} |  |
| GET | /api/users/{id}/followedArtists/{artistId} |  |
| GET | /api/users/current/followedArtists/{artistId} |  |
| GET | /api/users/{id}/album-collection-statuses/{albumId} |  |
| GET | /api/users/current/album-collection-statuses/{albumId} |  |
| DELETE | /api/venues/{id} |  |
| GET | /api/venues |  |
| POST | /api/venues/{id}/reports |  |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all activityEntries?" -> GET /api/activityEntries
- "Delete a album?" -> DELETE /api/albums/{id}
- "Get album details?" -> GET /api/albums/{id}
- "Delete a comment?" -> DELETE /api/albums/comments/{commentId}
- "List all comments?" -> GET /api/albums/{id}/comments
- "Create a comment?" -> POST /api/albums/{id}/comments
- "Search albums?" -> GET /api/albums
- "Search names?" -> GET /api/albums/names
- "List all new?" -> GET /api/albums/new
- "List all reviews?" -> GET /api/albums/{id}/reviews
- "Create a review?" -> POST /api/albums/{id}/reviews
- "List all user-collections?" -> GET /api/albums/{id}/user-collections
- "Delete a review?" -> DELETE /api/albums/{id}/reviews/{reviewId}
- "List all top?" -> GET /api/albums/top
- "List all tracks?" -> GET /api/albums/{id}/tracks
- "List all fields?" -> GET /api/albums/{id}/tracks/fields
- "List all related?" -> GET /api/albums/{id}/related
- "Delete a artist?" -> DELETE /api/artists/{id}
- "Get artist details?" -> GET /api/artists/{id}
- "Delete a comment?" -> DELETE /api/artists/comments/{commentId}
- "List all comments?" -> GET /api/artists/{id}/comments
- "Create a comment?" -> POST /api/artists/{id}/comments
- "Search artists?" -> GET /api/artists
- "Search names?" -> GET /api/artists/names
- "Delete a comment?" -> DELETE /api/comments/{entryType}-comments/{commentId}
- "Get comment details?" -> GET /api/comments/{entryType}-comments
- "List all locked?" -> GET /api/comments/{entryType}-comments/{entryId}/locked
- "Create a locked?" -> POST /api/comments/{entryType}-comments/{entryId}/locked
- "List all comments?" -> GET /api/comments
- "Delete a comment?" -> DELETE /api/discussions/comments/{commentId}
- "Delete a topic?" -> DELETE /api/discussions/topics/{topicId}
- "Get topic details?" -> GET /api/discussions/topics/{topicId}
- "List all folders?" -> GET /api/discussions/folders
- "Create a folder?" -> POST /api/discussions/folders
- "List all topics?" -> GET /api/discussions/topics
- "List all topics?" -> GET /api/discussions/folders/{folderId}/topics
- "Create a topic?" -> POST /api/discussions/folders/{folderId}/topics
- "Create a comment?" -> POST /api/discussions/topics/{topicId}/comments
- "Search entries?" -> GET /api/entries
- "List all random?" -> GET /api/entries/random
- "Search names?" -> GET /api/entries/names
- "List all tag?" -> GET /api/entry-types/{entryType}/{subType}/tag
- "List all for-songs?" -> GET /api/pvs/for-songs
- "List all thumbnail?" -> GET /api/pvs/thumbnail
- "Delete a releaseEvent?" -> DELETE /api/releaseEvents/{id}
- "Get releaseEvent details?" -> GET /api/releaseEvents/{id}
- "List all albums?" -> GET /api/releaseEvents/{eventId}/albums
- "List all published-songs?" -> GET /api/releaseEvents/{eventId}/published-songs
- "Search releaseEvents?" -> GET /api/releaseEvents
- "Search names?" -> GET /api/releaseEvents/names
- "Create a report?" -> POST /api/releaseEvents/{eventId}/reports
- "Delete a releaseEventSery?" -> DELETE /api/releaseEventSeries/{id}
- "Get releaseEventSery details?" -> GET /api/releaseEventSeries/{id}
- "Search releaseEventSeries?" -> GET /api/releaseEventSeries
- "List all for-edit?" -> GET /api/releaseEventSeries/{id}/for-edit
- "Get resource details?" -> GET /api/resources/{cultureCode}
- "Delete a comment?" -> DELETE /api/songs/comments/{commentId}
- "Delete a song?" -> DELETE /api/songs/{id}
- "Get song details?" -> GET /api/songs/{id}
- "List all comments?" -> GET /api/songs/{id}/comments
- "Create a comment?" -> POST /api/songs/{id}/comments
- "List all derived?" -> GET /api/songs/{id}/derived
- "List all highlighted?" -> GET /api/songs/highlighted
- "List all ratings?" -> GET /api/songs/{id}/ratings
- "Create a rating?" -> POST /api/songs/{id}/ratings
- "List all related?" -> GET /api/songs/{id}/related
- "Search songs?" -> GET /api/songs
- "Get lyric details?" -> GET /api/songs/lyrics/{lyricsId}
- "Search names?" -> GET /api/songs/names
- "List all byPv?" -> GET /api/songs/byPv
- "List all top-rated?" -> GET /api/songs/top-rated
- "Delete a songList?" -> DELETE /api/songLists/{id}
- "Delete a comment?" -> DELETE /api/songLists/comments/{commentId}
- "List all comments?" -> GET /api/songLists/{listId}/comments
- "Create a comment?" -> POST /api/songLists/{listId}/comments
- "Search featured?" -> GET /api/songLists/featured
- "Search names?" -> GET /api/songLists/featured/names
- "Search songs?" -> GET /api/songLists/{listId}/songs
- "Create a songList?" -> POST /api/songLists
- "Delete a tag?" -> DELETE /api/tags/{id}
- "Get tag details?" -> GET /api/tags/{id}
- "Delete a comment?" -> DELETE /api/tags/comments/{commentId}
- "Get byName details?" -> GET /api/tags/byName/{name}
- "Search categoryNames?" -> GET /api/tags/categoryNames
- "List all children?" -> GET /api/tags/{tagId}/children
- "List all comments?" -> GET /api/tags/{tagId}/comments
- "Create a comment?" -> POST /api/tags/{tagId}/comments
- "Search tags?" -> GET /api/tags
- "Create a tag?" -> POST /api/tags
- "Search names?" -> GET /api/tags/names
- "List all top?" -> GET /api/tags/top
- "Create a report?" -> POST /api/tags/{tagId}/reports
- "Delete a followedTag?" -> DELETE /api/users/current/followedTags/{tagId}
- "Delete a profileComment?" -> DELETE /api/users/profileComments/{commentId}
- "Search albums?" -> GET /api/users/{id}/albums
- "List all current?" -> GET /api/users/current
- "List all events?" -> GET /api/users/{id}/events
- "Search followedArtists?" -> GET /api/users/{id}/followedArtists
- "Search users?" -> GET /api/users
- "Get user details?" -> GET /api/users/{id}
- "Get message details?" -> GET /api/users/messages/{messageId}
- "List all messages?" -> GET /api/users/{id}/messages
- "Create a message?" -> POST /api/users/{id}/messages
- "Search names?" -> GET /api/users/names
- "List all profileComments?" -> GET /api/users/{id}/profileComments
- "Create a profileComment?" -> POST /api/users/{id}/profileComments
- "Search ratedSongs?" -> GET /api/users/{id}/ratedSongs
- "Search songLists?" -> GET /api/users/{id}/songLists
- "Get ratedSong details?" -> GET /api/users/{id}/ratedSongs/{songId}
- "Get ratedSong details?" -> GET /api/users/current/ratedSongs/{songId}
- "Create a refreshEntryEdit?" -> POST /api/users/current/refreshEntryEdit
- "Create a report?" -> POST /api/users/{id}/reports
- "Get followedArtist details?" -> GET /api/users/{id}/followedArtists/{artistId}
- "Get followedArtist details?" -> GET /api/users/current/followedArtists/{artistId}
- "Get album-collection-statuse details?" -> GET /api/users/{id}/album-collection-statuses/{albumId}
- "Get album-collection-statuse details?" -> GET /api/users/current/album-collection-statuses/{albumId}
- "Delete a venue?" -> DELETE /api/venues/{id}
- "Search venues?" -> GET /api/venues
- "Create a report?" -> POST /api/venues/{id}/reports

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
