---
name: spotify-web-api
description: "Spotify Web API skill. Use when working with Spotify Web for albums, artists, shows. Covers 96 endpoints."
version: 1.0.0
generator: lapsh
---

# Spotify Web API
API version: 1.0.0

## Auth
OAuth2

## Base URL
https://api.spotify.com/v1

## Setup
1. Configure auth: OAuth2
2. GET /albums -- verify access
3. POST /playlists/{playlist_id}/tracks -- create first tracks

## Endpoints

96 endpoints across 16 groups. See references/api-spec.lap for full details.

### albums
| Method | Path | Description |
|--------|------|-------------|
| GET | /albums/{id} | Get Album |
| GET | /albums | Get Several Albums |
| GET | /albums/{id}/tracks | Get Album Tracks |

### artists
| Method | Path | Description |
|--------|------|-------------|
| GET | /artists/{id} | Get Artist |
| GET | /artists | Get Several Artists |
| GET | /artists/{id}/albums | Get Artist's Albums |
| GET | /artists/{id}/top-tracks | Get Artist's Top Tracks |
| GET | /artists/{id}/related-artists | Get Artist's Related Artists |

### shows
| Method | Path | Description |
|--------|------|-------------|
| GET | /shows/{id} | Get Show |
| GET | /shows | Get Several Shows |
| GET | /shows/{id}/episodes | Get Show Episodes |

### episodes
| Method | Path | Description |
|--------|------|-------------|
| GET | /episodes/{id} | Get Episode |
| GET | /episodes | Get Several Episodes |

### audiobooks
| Method | Path | Description |
|--------|------|-------------|
| GET | /audiobooks/{id} | Get an Audiobook |
| GET | /audiobooks | Get Several Audiobooks |
| GET | /audiobooks/{id}/chapters | Get Audiobook Chapters |

### me
| Method | Path | Description |
|--------|------|-------------|
| GET | /me/audiobooks | Get User's Saved Audiobooks |
| PUT | /me/audiobooks | Save Audiobooks for Current User |
| DELETE | /me/audiobooks | Remove User's Saved Audiobooks |
| GET | /me/audiobooks/contains | Check User's Saved Audiobooks |
| GET | /me | Get Current User's Profile |
| GET | /me/playlists | Get Current User's Playlists |
| POST | /me/playlists | Create Playlist |
| PUT | /me/library | Save Items to Library |
| DELETE | /me/library | Remove Items from Library |
| GET | /me/library/contains | Check User's Saved Items |
| GET | /me/albums | Get User's Saved Albums |
| PUT | /me/albums | Save Albums for Current User |
| DELETE | /me/albums | Remove Users' Saved Albums |
| GET | /me/albums/contains | Check User's Saved Albums |
| GET | /me/tracks | Get User's Saved Tracks |
| PUT | /me/tracks | Save Tracks for Current User |
| DELETE | /me/tracks | Remove User's Saved Tracks |
| GET | /me/tracks/contains | Check User's Saved Tracks |
| GET | /me/episodes | Get User's Saved Episodes |
| PUT | /me/episodes | Save Episodes for Current User |
| DELETE | /me/episodes | Remove User's Saved Episodes |
| GET | /me/episodes/contains | Check User's Saved Episodes |
| GET | /me/shows | Get User's Saved Shows |
| PUT | /me/shows | Save Shows for Current User |
| DELETE | /me/shows | Remove User's Saved Shows |
| GET | /me/shows/contains | Check User's Saved Shows |
| GET | /me/top/{type} | Get User's Top Items |
| GET | /me/following | Get Followed Artists |
| PUT | /me/following | Follow Artists or Users |
| DELETE | /me/following | Unfollow Artists or Users |
| GET | /me/following/contains | Check If User Follows Artists or Users |
| GET | /me/player | Get Playback State |
| PUT | /me/player | Transfer Playback |
| GET | /me/player/devices | Get Available Devices |
| GET | /me/player/currently-playing | Get Currently Playing Track |
| PUT | /me/player/play | Start/Resume Playback |
| PUT | /me/player/pause | Pause Playback |
| POST | /me/player/next | Skip To Next |
| POST | /me/player/previous | Skip To Previous |
| PUT | /me/player/seek | Seek To Position |
| PUT | /me/player/repeat | Set Repeat Mode |
| PUT | /me/player/volume | Set Playback Volume |
| PUT | /me/player/shuffle | Toggle Playback Shuffle |
| GET | /me/player/recently-played | Get Recently Played Tracks |
| GET | /me/player/queue | Get the User's Queue |
| POST | /me/player/queue | Add Item to Playback Queue |

### chapters
| Method | Path | Description |
|--------|------|-------------|
| GET | /chapters/{id} | Get a Chapter |
| GET | /chapters | Get Several Chapters |

### tracks
| Method | Path | Description |
|--------|------|-------------|
| GET | /tracks/{id} | Get Track |
| GET | /tracks | Get Several Tracks |

### search
| Method | Path | Description |
|--------|------|-------------|
| GET | /search | Search for Item |

### playlists
| Method | Path | Description |
|--------|------|-------------|
| GET | /playlists/{playlist_id} | Get Playlist |
| PUT | /playlists/{playlist_id} | Change Playlist Details |
| GET | /playlists/{playlist_id}/tracks | Get Playlist Items [DEPRECATED] |
| POST | /playlists/{playlist_id}/tracks | Add Items to Playlist [DEPRECATED] |
| PUT | /playlists/{playlist_id}/tracks | Update Playlist Items [DEPRECATED] |
| DELETE | /playlists/{playlist_id}/tracks | Remove Playlist Items [DEPRECATED] |
| GET | /playlists/{playlist_id}/items | Get Playlist Items |
| POST | /playlists/{playlist_id}/items | Add Items to Playlist |
| PUT | /playlists/{playlist_id}/items | Update Playlist Items |
| DELETE | /playlists/{playlist_id}/items | Remove Playlist Items |
| PUT | /playlists/{playlist_id}/followers | Follow Playlist |
| DELETE | /playlists/{playlist_id}/followers | Unfollow Playlist |
| GET | /playlists/{playlist_id}/images | Get Playlist Cover Image |
| PUT | /playlists/{playlist_id}/images | Add Custom Playlist Cover Image |
| GET | /playlists/{playlist_id}/followers/contains | Check if Current User Follows Playlist |

### users
| Method | Path | Description |
|--------|------|-------------|
| GET | /users/{user_id} | Get User's Profile |
| GET | /users/{user_id}/playlists | Get User's Playlists |
| POST | /users/{user_id}/playlists | Create Playlist for user |

### browse
| Method | Path | Description |
|--------|------|-------------|
| GET | /browse/featured-playlists | Get Featured Playlists |
| GET | /browse/categories | Get Several Browse Categories |
| GET | /browse/categories/{category_id} | Get Single Browse Category |
| GET | /browse/categories/{category_id}/playlists | Get Category's Playlists |
| GET | /browse/new-releases | Get New Releases |

### audio-features
| Method | Path | Description |
|--------|------|-------------|
| GET | /audio-features | Get Several Tracks' Audio Features |
| GET | /audio-features/{id} | Get Track's Audio Features |

### audio-analysis
| Method | Path | Description |
|--------|------|-------------|
| GET | /audio-analysis/{id} | Get Track's Audio Analysis |

### recommendations
| Method | Path | Description |
|--------|------|-------------|
| GET | /recommendations | Get Recommendations |
| GET | /recommendations/available-genre-seeds | Get Available Genre Seeds |

### markets
| Method | Path | Description |
|--------|------|-------------|
| GET | /markets | Get Available Markets |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get album details?" -> GET /albums/{id}
- "List all albums?" -> GET /albums
- "List all tracks?" -> GET /albums/{id}/tracks
- "Get artist details?" -> GET /artists/{id}
- "List all artists?" -> GET /artists
- "List all albums?" -> GET /artists/{id}/albums
- "List all top-tracks?" -> GET /artists/{id}/top-tracks
- "List all related-artists?" -> GET /artists/{id}/related-artists
- "Get show details?" -> GET /shows/{id}
- "List all shows?" -> GET /shows
- "List all episodes?" -> GET /shows/{id}/episodes
- "Get episode details?" -> GET /episodes/{id}
- "List all episodes?" -> GET /episodes
- "Get audiobook details?" -> GET /audiobooks/{id}
- "List all audiobooks?" -> GET /audiobooks
- "List all chapters?" -> GET /audiobooks/{id}/chapters
- "List all audiobooks?" -> GET /me/audiobooks
- "List all contains?" -> GET /me/audiobooks/contains
- "Get chapter details?" -> GET /chapters/{id}
- "List all chapters?" -> GET /chapters
- "Get track details?" -> GET /tracks/{id}
- "List all tracks?" -> GET /tracks
- "Search search?" -> GET /search
- "List all me?" -> GET /me
- "Get playlist details?" -> GET /playlists/{playlist_id}
- "Update a playlist?" -> PUT /playlists/{playlist_id}
- "List all tracks?" -> GET /playlists/{playlist_id}/tracks
- "Create a track?" -> POST /playlists/{playlist_id}/tracks
- "List all items?" -> GET /playlists/{playlist_id}/items
- "Create a item?" -> POST /playlists/{playlist_id}/items
- "List all playlists?" -> GET /me/playlists
- "Create a playlist?" -> POST /me/playlists
- "List all contains?" -> GET /me/library/contains
- "List all albums?" -> GET /me/albums
- "List all contains?" -> GET /me/albums/contains
- "List all tracks?" -> GET /me/tracks
- "List all contains?" -> GET /me/tracks/contains
- "List all episodes?" -> GET /me/episodes
- "List all contains?" -> GET /me/episodes/contains
- "List all shows?" -> GET /me/shows
- "List all contains?" -> GET /me/shows/contains
- "Get top details?" -> GET /me/top/{type}
- "Get user details?" -> GET /users/{user_id}
- "List all playlists?" -> GET /users/{user_id}/playlists
- "Create a playlist?" -> POST /users/{user_id}/playlists
- "List all featured-playlists?" -> GET /browse/featured-playlists
- "List all categories?" -> GET /browse/categories
- "Get category details?" -> GET /browse/categories/{category_id}
- "List all playlists?" -> GET /browse/categories/{category_id}/playlists
- "List all images?" -> GET /playlists/{playlist_id}/images
- "List all new-releases?" -> GET /browse/new-releases
- "List all following?" -> GET /me/following
- "List all contains?" -> GET /me/following/contains
- "List all contains?" -> GET /playlists/{playlist_id}/followers/contains
- "List all audio-features?" -> GET /audio-features
- "Get audio-feature details?" -> GET /audio-features/{id}
- "Get audio-analysis details?" -> GET /audio-analysis/{id}
- "List all recommendations?" -> GET /recommendations
- "List all available-genre-seeds?" -> GET /recommendations/available-genre-seeds
- "List all player?" -> GET /me/player
- "List all devices?" -> GET /me/player/devices
- "List all currently-playing?" -> GET /me/player/currently-playing
- "Create a next?" -> POST /me/player/next
- "Create a previous?" -> POST /me/player/previous
- "List all recently-played?" -> GET /me/player/recently-played
- "List all queue?" -> GET /me/player/queue
- "Create a queue?" -> POST /me/player/queue
- "List all markets?" -> GET /markets
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
