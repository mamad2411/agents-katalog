---
name: art19-content-api-documentation
description: "ART19 Content API Documentation API skill. Use when working with ART19 Content API Documentation for classification_inclusions, classifications, credits. Covers 62 endpoints."
version: 1.0.0
generator: lapsh
---

# ART19 Content API Documentation
API version: 1.0.0

## Auth
ApiKey Authorization in header

## Base URL
https://art19.com/

## Setup
1. Set your API key in the appropriate header
2. GET /classification_inclusions -- verify access
3. POST /credits -- create first credits

## Endpoints

62 endpoints across 15 groups. See references/api-spec.lap for full details.

### classification_inclusions
| Method | Path | Description |
|--------|------|-------------|
| GET | /classification_inclusions | Get ClassificationInclusion records |
| GET | /classification_inclusions/{id} | Get a specific classification inclusion |

### classifications
| Method | Path | Description |
|--------|------|-------------|
| GET | /classifications | Get a list of classifications |
| GET | /classifications/{id} | Get a specific classification |

### credits
| Method | Path | Description |
|--------|------|-------------|
| GET | /credits | Get a list of credits |
| POST | /credits | Create a new credit |
| DELETE | /credits/{id} | Delete a specific credit |
| GET | /credits/{id} | Get a specific credit |
| PATCH | /credits/{id} | Update a specific credit |

### episode_versions
| Method | Path | Description |
|--------|------|-------------|
| GET | /episode_versions | Get a list of episode versions |
| POST | /episode_versions | Create a new episode version |
| DELETE | /episode_versions/{id} | Delete an episode version |
| GET | /episode_versions/{id} | Get a specific episode version |
| PATCH | /episode_versions/{id} | Update an episode version |

### episodes
| Method | Path | Description |
|--------|------|-------------|
| GET | /episodes | Get a list of episodes |
| POST | /episodes | Create a new episode |
| DELETE | /episodes/{id} | Delete a specific episode |
| GET | /episodes/{id} | Get a specific episode |
| PATCH | /episodes/{id} | Update a specific episode |
| GET | /episodes/{id}/next_sibling | Get the episode released right after the specified one |
| GET | /episodes/{id}/previous_sibling | Get the episode released right before the specified one |

### feed_items
| Method | Path | Description |
|--------|------|-------------|
| GET | /feed_items | Get a list of feed items |
| POST | /feed_items | Create a new feed item |
| DELETE | /feed_items/{id} | Delete a specific feed item |
| GET | /feed_items/{id} | Get a specific feed item |
| PATCH | /feed_items/{id} | Update a specific feed item |

### feeds
| Method | Path | Description |
|--------|------|-------------|
| GET | /feeds | Get a list of feeds |
| POST | /feeds | Create a new feed |
| DELETE | /feeds/{id} | Delete a specific feed |
| GET | /feeds/{id} | Get a specific feed |
| PATCH | /feeds/{id} | Update a specific feed |

### images
| Method | Path | Description |
|--------|------|-------------|
| GET | /images | Get a list of images |
| POST | /images | Create a new image |
| DELETE | /images/{id} | Delete an image |
| GET | /images/{id} | Get a specific image |

### marker_point_content_rules
| Method | Path | Description |
|--------|------|-------------|
| GET | /marker_point_content_rules | Get a list of marker point content rules |
| POST | /marker_point_content_rules | Create a new marker point content rule |
| DELETE | /marker_point_content_rules/{id} | Delete a marker point content rule |
| GET | /marker_point_content_rules/{id} | Get a specific marker point content rule |
| PATCH | /marker_point_content_rules/{id} | Update a marker point content rule |

### marker_points
| Method | Path | Description |
|--------|------|-------------|
| GET | /marker_points | Get a list of marker points |
| POST | /marker_points | Create a new marker point |
| DELETE | /marker_points/{id} | Delete a marker point |
| GET | /marker_points/{id} | Get a specific marker point |
| PATCH | /marker_points/{id} | Update a marker point |

### media_assets
| Method | Path | Description |
|--------|------|-------------|
| GET | /media_assets | Get a list of media assets |
| GET | /media_assets/{id} | Get a specific media asset |

### networks
| Method | Path | Description |
|--------|------|-------------|
| GET | /networks | Get a list of networks |
| GET | /networks/{id} | Get a specific network |
| PATCH | /networks/{id} | Update a specific network |

### people
| Method | Path | Description |
|--------|------|-------------|
| GET | /people | Get a list of people |
| POST | /people | Create a new person |
| GET | /people/{id} | Get a specific person |
| PATCH | /people/{id} | Update a specific person |

### seasons
| Method | Path | Description |
|--------|------|-------------|
| GET | /seasons | Get a list of seasons |
| POST | /seasons | Create a new season |
| DELETE | /seasons/{id} | Delete a specific season |
| GET | /seasons/{id} | Get a specific season |
| PATCH | /seasons/{id} | Update a specific season |

### series
| Method | Path | Description |
|--------|------|-------------|
| GET | /series | Get a list of series |
| GET | /series/{id} | Get a specific series |
| PATCH | /series/{id} | Update a specific series |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Search classification_inclusions?" -> GET /classification_inclusions
- "Get classification_inclusion details?" -> GET /classification_inclusions/{id}
- "Search classifications?" -> GET /classifications
- "Get classification details?" -> GET /classifications/{id}
- "List all credits?" -> GET /credits
- "Create a credit?" -> POST /credits
- "Delete a credit?" -> DELETE /credits/{id}
- "Get credit details?" -> GET /credits/{id}
- "Partially update a credit?" -> PATCH /credits/{id}
- "List all episode_versions?" -> GET /episode_versions
- "Create a episode_version?" -> POST /episode_versions
- "Delete a episode_version?" -> DELETE /episode_versions/{id}
- "Get episode_version details?" -> GET /episode_versions/{id}
- "Partially update a episode_version?" -> PATCH /episode_versions/{id}
- "Search episodes?" -> GET /episodes
- "Create a episode?" -> POST /episodes
- "Delete a episode?" -> DELETE /episodes/{id}
- "Get episode details?" -> GET /episodes/{id}
- "Partially update a episode?" -> PATCH /episodes/{id}
- "List all next_sibling?" -> GET /episodes/{id}/next_sibling
- "List all previous_sibling?" -> GET /episodes/{id}/previous_sibling
- "Search feed_items?" -> GET /feed_items
- "Create a feed_item?" -> POST /feed_items
- "Delete a feed_item?" -> DELETE /feed_items/{id}
- "Get feed_item details?" -> GET /feed_items/{id}
- "Partially update a feed_item?" -> PATCH /feed_items/{id}
- "List all feeds?" -> GET /feeds
- "Create a feed?" -> POST /feeds
- "Delete a feed?" -> DELETE /feeds/{id}
- "Get feed details?" -> GET /feeds/{id}
- "Partially update a feed?" -> PATCH /feeds/{id}
- "List all images?" -> GET /images
- "Create a image?" -> POST /images
- "Delete a image?" -> DELETE /images/{id}
- "Get image details?" -> GET /images/{id}
- "List all marker_point_content_rules?" -> GET /marker_point_content_rules
- "Create a marker_point_content_rule?" -> POST /marker_point_content_rules
- "Delete a marker_point_content_rule?" -> DELETE /marker_point_content_rules/{id}
- "Get marker_point_content_rule details?" -> GET /marker_point_content_rules/{id}
- "Partially update a marker_point_content_rule?" -> PATCH /marker_point_content_rules/{id}
- "List all marker_points?" -> GET /marker_points
- "Create a marker_point?" -> POST /marker_points
- "Delete a marker_point?" -> DELETE /marker_points/{id}
- "Get marker_point details?" -> GET /marker_points/{id}
- "Partially update a marker_point?" -> PATCH /marker_points/{id}
- "List all media_assets?" -> GET /media_assets
- "Get media_asset details?" -> GET /media_assets/{id}
- "Search networks?" -> GET /networks
- "Get network details?" -> GET /networks/{id}
- "Partially update a network?" -> PATCH /networks/{id}
- "Search people?" -> GET /people
- "Create a people?" -> POST /people
- "Get people details?" -> GET /people/{id}
- "Partially update a people?" -> PATCH /people/{id}
- "Search seasons?" -> GET /seasons
- "Create a season?" -> POST /seasons
- "Delete a season?" -> DELETE /seasons/{id}
- "Get season details?" -> GET /seasons/{id}
- "Partially update a season?" -> PATCH /seasons/{id}
- "Search series?" -> GET /series
- "Get sery details?" -> GET /series/{id}
- "Partially update a sery?" -> PATCH /series/{id}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
