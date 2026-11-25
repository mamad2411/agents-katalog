---
name: tvmaze-user-api
description: "TVmaze user API skill. Use when working with TVmaze user for user, scrobble, auth. Covers 42 endpoints."
version: 1.0.0
generator: lapsh
---

# TVmaze user API
API version: 1.0

## Auth
basic

## Base URL
https://api.tvmaze.com/v1

## Setup
1. Configure auth: basic
2. GET /user/episodes -- verify access
3. POST /user/tags -- create first tags

## Endpoints

42 endpoints across 3 groups. See references/api-spec.lap for full details.

### user
| Method | Path | Description |
|--------|------|-------------|
| GET | /user/episodes | List the marked episodes |
| GET | /user/episodes/{episode_id} | Check if an episode is marked |
| PUT | /user/episodes/{episode_id} | Mark an episode |
| DELETE | /user/episodes/{episode_id} | Unmark an episode |
| GET | /user/follows/shows | List the followed shows |
| GET | /user/follows/shows/{show_id} | Check if a show is followed |
| PUT | /user/follows/shows/{show_id} | Follow a show |
| DELETE | /user/follows/shows/{show_id} | Unfollow a show |
| GET | /user/follows/people | List the followed people |
| GET | /user/follows/people/{person_id} | Check if a person is followed |
| PUT | /user/follows/people/{person_id} | Follow a person |
| DELETE | /user/follows/people/{person_id} | Unfollow a person |
| GET | /user/follows/networks | List the followed networks |
| GET | /user/follows/networks/{network_id} | Check if a network is followed |
| PUT | /user/follows/networks/{network_id} | Follow a network |
| DELETE | /user/follows/networks/{network_id} | Unfollow a network |
| GET | /user/follows/webchannels | List the followed webchannels |
| GET | /user/follows/webchannels/{webchannel_id} | Check if a webchannel is followed |
| PUT | /user/follows/webchannels/{webchannel_id} | Follow a webchannel |
| DELETE | /user/follows/webchannels/{webchannel_id} | Unfollow a webchannel |
| GET | /user/tags | List all tags |
| POST | /user/tags | Create a new tag |
| DELETE | /user/tags/{tag_id} | Delete a specific tag |
| PATCH | /user/tags/{tag_id} | Update a specific tag |
| GET | /user/tags/{tag_id}/shows | List all shows under this tag |
| PUT | /user/tags/{tag_id}/shows/{show_id} | Tag a show |
| DELETE | /user/tags/{tag_id}/shows/{show_id} | Untag a show |
| GET | /user/votes/shows | List the shows voted for |
| GET | /user/votes/shows/{show_id} | Check if a show is voted for |
| PUT | /user/votes/shows/{show_id} | Vote for a show |
| DELETE | /user/votes/shows/{show_id} | Remove a show vote |
| GET | /user/votes/episodes | List the episodes voted for |
| GET | /user/votes/episodes/{episode_id} | Check if an episode is voted for |
| PUT | /user/votes/episodes/{episode_id} | Vote for an episode |
| DELETE | /user/votes/episodes/{episode_id} | Remove an episode vote |

### scrobble
| Method | Path | Description |
|--------|------|-------------|
| GET | /scrobble/shows/{show_id} | List watched and acquired episodes for a show |
| PUT | /scrobble/episodes/{episode_id} | Mark an episode as acquired or watched based on its ID |
| POST | /scrobble/shows | Mark episodes within a show as acquired or watched based on their attributes |
| POST | /scrobble/episodes | Mark episodes as acquired or watched based on their IDs |

### auth
| Method | Path | Description |
|--------|------|-------------|
| POST | /auth/start | Start an authentication request |
| POST | /auth/poll | Poll whether an authentication request was confirmed |
| GET | /auth/validate | Validate your authentication credentials |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all episodes?" -> GET /user/episodes
- "Get episode details?" -> GET /user/episodes/{episode_id}
- "Update a episode?" -> PUT /user/episodes/{episode_id}
- "Delete a episode?" -> DELETE /user/episodes/{episode_id}
- "List all shows?" -> GET /user/follows/shows
- "Get show details?" -> GET /user/follows/shows/{show_id}
- "Update a show?" -> PUT /user/follows/shows/{show_id}
- "Delete a show?" -> DELETE /user/follows/shows/{show_id}
- "List all people?" -> GET /user/follows/people
- "Get people details?" -> GET /user/follows/people/{person_id}
- "Update a people?" -> PUT /user/follows/people/{person_id}
- "Delete a people?" -> DELETE /user/follows/people/{person_id}
- "List all networks?" -> GET /user/follows/networks
- "Get network details?" -> GET /user/follows/networks/{network_id}
- "Update a network?" -> PUT /user/follows/networks/{network_id}
- "Delete a network?" -> DELETE /user/follows/networks/{network_id}
- "List all webchannels?" -> GET /user/follows/webchannels
- "Get webchannel details?" -> GET /user/follows/webchannels/{webchannel_id}
- "Update a webchannel?" -> PUT /user/follows/webchannels/{webchannel_id}
- "Delete a webchannel?" -> DELETE /user/follows/webchannels/{webchannel_id}
- "List all tags?" -> GET /user/tags
- "Create a tag?" -> POST /user/tags
- "Delete a tag?" -> DELETE /user/tags/{tag_id}
- "Partially update a tag?" -> PATCH /user/tags/{tag_id}
- "List all shows?" -> GET /user/tags/{tag_id}/shows
- "Update a show?" -> PUT /user/tags/{tag_id}/shows/{show_id}
- "Delete a show?" -> DELETE /user/tags/{tag_id}/shows/{show_id}
- "List all shows?" -> GET /user/votes/shows
- "Get show details?" -> GET /user/votes/shows/{show_id}
- "Update a show?" -> PUT /user/votes/shows/{show_id}
- "Delete a show?" -> DELETE /user/votes/shows/{show_id}
- "List all episodes?" -> GET /user/votes/episodes
- "Get episode details?" -> GET /user/votes/episodes/{episode_id}
- "Update a episode?" -> PUT /user/votes/episodes/{episode_id}
- "Delete a episode?" -> DELETE /user/votes/episodes/{episode_id}
- "Get show details?" -> GET /scrobble/shows/{show_id}
- "Update a episode?" -> PUT /scrobble/episodes/{episode_id}
- "Create a show?" -> POST /scrobble/shows
- "Create a episode?" -> POST /scrobble/episodes
- "Create a start?" -> POST /auth/start
- "Create a poll?" -> POST /auth/poll
- "List all validate?" -> GET /auth/validate
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
