---
name: shutterstock-api-explorer
description: "Shutterstock API Explorer API skill. Use when working with Shutterstock API Explorer for images, bulk_search, videos. Covers 109 endpoints."
version: 1.0.0
generator: lapsh
---

# Shutterstock API Explorer
API version: 1.2.0

## Auth
Bearer basic | OAuth2

## Base URL
https://api.shutterstock.com

## Setup
1. Set Authorization header with your Bearer token
2. GET /v2/images/search -- verify access
3. POST /v2/bulk_search/images -- create first images

## Endpoints

109 endpoints across 12 groups. See references/api-spec.lap for full details.

### images
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/images/search | Search for images |
| GET | /v2/images/search/suggestions | Get suggestions for a search term |
| POST | /v2/images/search/suggestions | Get keywords from text |
| GET | /v2/images | List images |
| GET | /v2/images/{id} | Get details about images |
| GET | /v2/images/categories | List image categories |
| GET | /v2/images/{id}/similar | List similar images |
| POST | /v2/images/licenses | License images |
| GET | /v2/images/licenses | List image licenses |
| POST | /v2/images/licenses/{id}/downloads | Download images |
| GET | /v2/images/recommendations | List recommended images |
| POST | /v2/images/collections | Create image collections |
| GET | /v2/images/collections | List image collections |
| GET | /v2/images/collections/{id} | Get the details of image collections |
| POST | /v2/images/collections/{id} | Rename image collections |
| DELETE | /v2/images/collections/{id} | Delete image collections |
| POST | /v2/images/collections/{id}/items | Add images to collections |
| GET | /v2/images/collections/{id}/items | Get the contents of image collections |
| DELETE | /v2/images/collections/{id}/items | Remove images from collections |
| GET | /v2/images/updated | List updated images |

### bulk_search
| Method | Path | Description |
|--------|------|-------------|
| POST | /v2/bulk_search/images | Run multiple image searches |

### videos
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/videos/search | Search for videos |
| GET | /v2/videos/search/suggestions | Get suggestions for a search term |
| GET | /v2/videos | List videos |
| GET | /v2/videos/{id} | Get details about videos |
| POST | /v2/videos/licenses | License videos |
| GET | /v2/videos/licenses | List video licenses |
| POST | /v2/videos/licenses/{id}/downloads | Download videos |
| POST | /v2/videos/collections | Create video collections |
| GET | /v2/videos/collections | List video collections |
| GET | /v2/videos/collections/{id} | Get the details of video collections |
| POST | /v2/videos/collections/{id} | Rename video collections |
| DELETE | /v2/videos/collections/{id} | Delete video collections |
| GET | /v2/videos/categories | List video categories |
| POST | /v2/videos/collections/{id}/items | Add videos to collections |
| GET | /v2/videos/collections/{id}/items | Get the contents of video collections |
| DELETE | /v2/videos/collections/{id}/items | Remove videos from collections |
| GET | /v2/videos/{id}/similar | List similar videos |
| GET | /v2/videos/updated | List updated videos |

### audio
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/audio/search | Search for tracks |
| GET | /v2/audio/genres | List audio genres |
| GET | /v2/audio/instruments | List audio instruments |
| GET | /v2/audio/moods | List audio moods |
| GET | /v2/audio | List audio tracks |
| GET | /v2/audio/{id} | Get details about audio tracks |
| POST | /v2/audio/licenses | License audio tracks |
| GET | /v2/audio/licenses | List audio licenses |
| POST | /v2/audio/licenses/{id}/downloads | Download audio tracks |
| POST | /v2/audio/collections | Create audio collections |
| GET | /v2/audio/collections | List audio collections |
| GET | /v2/audio/collections/{id} | Get the details of audio collections |
| POST | /v2/audio/collections/{id} | Rename audio collections |
| DELETE | /v2/audio/collections/{id} | Delete audio collections |
| POST | /v2/audio/collections/{id}/items | Add audio tracks to collections |
| GET | /v2/audio/collections/{id}/items | Get the contents of audio collections |
| DELETE | /v2/audio/collections/{id}/items | Remove audio tracks from collections |

### sfx
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/sfx/search | Search for sound effects |
| GET | /v2/sfx/{id} | Get details about sound effects |
| GET | /v2/sfx | List details about sound effects |
| GET | /v2/sfx/licenses | List sound effects licenses |
| POST | /v2/sfx/licenses | License sound effects |
| POST | /v2/sfx/licenses/{id}/downloads | Download sound effects |

### editorial
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/editorial/images/search | Search editorial images |
| GET | /v2/editorial/images/categories | List editorial categories |
| GET | /v2/editorial/images/updated | List updated content |
| GET | /v2/editorial/images/{id} | Get editorial content details |
| GET | /v2/editorial/images | list editorial image details |
| GET | /v2/editorial/images/licenses | List editorial image licenses |
| POST | /v2/editorial/images/licenses | License editorial content |
| GET | /v2/editorial/images/livefeeds | Get editorial livefeed list |
| GET | /v2/editorial/images/livefeeds/{id} | Get editorial livefeed |
| GET | /v2/editorial/images/livefeeds/{id}/items | Get editorial livefeed items |
| GET | /v2/editorial/videos/search | Search editorial video content |
| GET | /v2/editorial/videos/categories | List editorial video categories |
| GET | /v2/editorial/videos/{id} | Get editorial video content details |
| GET | /v2/editorial/videos | List editorial videos details by ID list |
| GET | /v2/editorial/videos/licenses | List editorial video licenses |
| POST | /v2/editorial/videos/licenses | License editorial video content |
| GET | /v2/editorial/{id} | (Deprecated) Get editorial content details |
| POST | /v2/editorial/licenses | (Deprecated) License editorial content |
| GET | /v2/editorial/livefeeds | (Deprecated) Get editorial livefeed list |
| GET | /v2/editorial/livefeeds/{id} | (Deprecated) Get editorial livefeed |
| GET | /v2/editorial/livefeeds/{id}/items | (Deprecated) Get editorial livefeed items |
| GET | /v2/editorial/search | (Deprecated) Search editorial content |
| GET | /v2/editorial/categories | (Deprecated) List editorial categories |
| GET | /v2/editorial/updated | (Deprecated) List updated content |

### cv
| Method | Path | Description |
|--------|------|-------------|
| POST | /v2/cv/images | Upload images |
| GET | /v2/cv/similar/images | List similar images |
| GET | /v2/cv/similar/videos | List similar videos |
| GET | /v2/cv/keywords | List suggested keywords |

### catalog
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/catalog/search | Search catalogs for assets |
| GET | /v2/catalog/collections | List catalog collections |
| POST | /v2/catalog/collections | Create catalog collections |
| PATCH | /v2/catalog/collections/{collection_id} | Update collection metadata |
| DELETE | /v2/catalog/collections/{collection_id} | Delete catalog collections |
| POST | /v2/catalog/collections/{collection_id}/items | Add items to catalog collections |
| DELETE | /v2/catalog/collections/{collection_id}/items | Remove items from catalog collection |

### contributors
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/contributors | Get details about multiple contributors |
| GET | /v2/contributors/{contributor_id} | Get details about a single contributor |
| GET | /v2/contributors/{contributor_id}/collections | List contributors' collections |
| GET | /v2/contributors/{contributor_id}/collections/{id} | Get details about contributors' collections |
| GET | /v2/contributors/{contributor_id}/collections/{id}/items | Get the items in contributors' collections |

### user
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/user | Get user details |
| GET | /v2/user/access_token | Get access token details |
| GET | /v2/user/subscriptions | List user subscriptions |

### test
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/test | Echo text |
| GET | /v2/test/validate | Validate input |

### oauth
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/oauth/authorize | Authorize applications |
| POST | /v2/oauth/access_token | Get access tokens |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Search search?" -> GET /v2/images/search
- "Create a image?" -> POST /v2/bulk_search/images
- "Search suggestions?" -> GET /v2/images/search/suggestions
- "Create a suggestion?" -> POST /v2/images/search/suggestions
- "List all images?" -> GET /v2/images
- "Get image details?" -> GET /v2/images/{id}
- "List all categories?" -> GET /v2/images/categories
- "List all similar?" -> GET /v2/images/{id}/similar
- "Create a license?" -> POST /v2/images/licenses
- "List all licenses?" -> GET /v2/images/licenses
- "Create a download?" -> POST /v2/images/licenses/{id}/downloads
- "List all recommendations?" -> GET /v2/images/recommendations
- "Create a collection?" -> POST /v2/images/collections
- "List all collections?" -> GET /v2/images/collections
- "Get collection details?" -> GET /v2/images/collections/{id}
- "Delete a collection?" -> DELETE /v2/images/collections/{id}
- "Create a item?" -> POST /v2/images/collections/{id}/items
- "List all items?" -> GET /v2/images/collections/{id}/items
- "List all updated?" -> GET /v2/images/updated
- "Search search?" -> GET /v2/videos/search
- "Search suggestions?" -> GET /v2/videos/search/suggestions
- "List all videos?" -> GET /v2/videos
- "Get video details?" -> GET /v2/videos/{id}
- "Create a license?" -> POST /v2/videos/licenses
- "List all licenses?" -> GET /v2/videos/licenses
- "Create a download?" -> POST /v2/videos/licenses/{id}/downloads
- "Create a collection?" -> POST /v2/videos/collections
- "List all collections?" -> GET /v2/videos/collections
- "Get collection details?" -> GET /v2/videos/collections/{id}
- "Delete a collection?" -> DELETE /v2/videos/collections/{id}
- "List all categories?" -> GET /v2/videos/categories
- "Create a item?" -> POST /v2/videos/collections/{id}/items
- "List all items?" -> GET /v2/videos/collections/{id}/items
- "List all similar?" -> GET /v2/videos/{id}/similar
- "List all updated?" -> GET /v2/videos/updated
- "Search search?" -> GET /v2/audio/search
- "List all genres?" -> GET /v2/audio/genres
- "List all instruments?" -> GET /v2/audio/instruments
- "List all moods?" -> GET /v2/audio/moods
- "List all audio?" -> GET /v2/audio
- "Get audio details?" -> GET /v2/audio/{id}
- "Create a license?" -> POST /v2/audio/licenses
- "List all licenses?" -> GET /v2/audio/licenses
- "Create a download?" -> POST /v2/audio/licenses/{id}/downloads
- "Create a collection?" -> POST /v2/audio/collections
- "List all collections?" -> GET /v2/audio/collections
- "Get collection details?" -> GET /v2/audio/collections/{id}
- "Delete a collection?" -> DELETE /v2/audio/collections/{id}
- "Create a item?" -> POST /v2/audio/collections/{id}/items
- "List all items?" -> GET /v2/audio/collections/{id}/items
- "Search search?" -> GET /v2/sfx/search
- "Get sfx details?" -> GET /v2/sfx/{id}
- "List all sfx?" -> GET /v2/sfx
- "List all licenses?" -> GET /v2/sfx/licenses
- "Create a license?" -> POST /v2/sfx/licenses
- "Create a download?" -> POST /v2/sfx/licenses/{id}/downloads
- "Search search?" -> GET /v2/editorial/images/search
- "List all categories?" -> GET /v2/editorial/images/categories
- "List all updated?" -> GET /v2/editorial/images/updated
- "Get image details?" -> GET /v2/editorial/images/{id}
- "List all images?" -> GET /v2/editorial/images
- "List all licenses?" -> GET /v2/editorial/images/licenses
- "Create a license?" -> POST /v2/editorial/images/licenses
- "List all livefeeds?" -> GET /v2/editorial/images/livefeeds
- "Get livefeed details?" -> GET /v2/editorial/images/livefeeds/{id}
- "List all items?" -> GET /v2/editorial/images/livefeeds/{id}/items
- "Search search?" -> GET /v2/editorial/videos/search
- "List all categories?" -> GET /v2/editorial/videos/categories
- "Get video details?" -> GET /v2/editorial/videos/{id}
- "List all videos?" -> GET /v2/editorial/videos
- "List all licenses?" -> GET /v2/editorial/videos/licenses
- "Create a license?" -> POST /v2/editorial/videos/licenses
- "Create a image?" -> POST /v2/cv/images
- "List all images?" -> GET /v2/cv/similar/images
- "List all videos?" -> GET /v2/cv/similar/videos
- "List all keywords?" -> GET /v2/cv/keywords
- "Search search?" -> GET /v2/catalog/search
- "List all collections?" -> GET /v2/catalog/collections
- "Create a collection?" -> POST /v2/catalog/collections
- "Partially update a collection?" -> PATCH /v2/catalog/collections/{collection_id}
- "Delete a collection?" -> DELETE /v2/catalog/collections/{collection_id}
- "Create a item?" -> POST /v2/catalog/collections/{collection_id}/items
- "List all contributors?" -> GET /v2/contributors
- "Get contributor details?" -> GET /v2/contributors/{contributor_id}
- "List all collections?" -> GET /v2/contributors/{contributor_id}/collections
- "Get collection details?" -> GET /v2/contributors/{contributor_id}/collections/{id}
- "List all items?" -> GET /v2/contributors/{contributor_id}/collections/{id}/items
- "List all user?" -> GET /v2/user
- "List all access_token?" -> GET /v2/user/access_token
- "List all subscriptions?" -> GET /v2/user/subscriptions
- "List all test?" -> GET /v2/test
- "List all validate?" -> GET /v2/test/validate
- "List all authorize?" -> GET /v2/oauth/authorize
- "Create a access_token?" -> POST /v2/oauth/access_token
- "Get editorial details?" -> GET /v2/editorial/{id}
- "Create a license?" -> POST /v2/editorial/licenses
- "List all livefeeds?" -> GET /v2/editorial/livefeeds
- "Get livefeed details?" -> GET /v2/editorial/livefeeds/{id}
- "List all items?" -> GET /v2/editorial/livefeeds/{id}/items
- "Search search?" -> GET /v2/editorial/search
- "List all categories?" -> GET /v2/editorial/categories
- "List all updated?" -> GET /v2/editorial/updated
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
