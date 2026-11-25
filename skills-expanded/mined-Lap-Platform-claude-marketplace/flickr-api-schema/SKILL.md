---
name: flickr-api-schema
description: "Flickr API Schema API skill. Use when working with Flickr API Schema for rest?method=flickr.favorites.getList, rest?method=flickr.people.getPhotos, rest?method=flickr.photosets.getList. Covers 25 endpoints."
version: 1.0.0
generator: lapsh
---

# Flickr API Schema
API version: 1.0.0

## Auth
ApiKey api_key in query

## Base URL
https://api.flickr.com/services

## Setup
1. Set your API key in the appropriate header
2. GET /rest?method=flickr.favorites.getList -- verify access
3. POST /upload -- create first upload

## Endpoints

25 endpoints across 24 groups. See references/api-spec.lap for full details.

### rest?method=flickr.favorites.getList
| Method | Path | Description |
|--------|------|-------------|
| GET | /rest?method=flickr.favorites.getList | Returns a list of the user's favorite photos. Only photos which the calling user has permission to see are returned. |

### rest?method=flickr.people.getPhotos
| Method | Path | Description |
|--------|------|-------------|
| GET | /rest?method=flickr.people.getPhotos | Return photos from the given user's photostream |

### rest?method=flickr.photosets.getList
| Method | Path | Description |
|--------|------|-------------|
| GET | /rest?method=flickr.photosets.getList | Returns the albums belonging to the specified user |

### rest?method=flickr.favorites.getContext
| Method | Path | Description |
|--------|------|-------------|
| GET | /rest?method=flickr.favorites.getContext | Returns next and previous favorites for a photo in a user's favorites |

### rest?method=flickr.groups.getInfo
| Method | Path | Description |
|--------|------|-------------|
| GET | /rest?method=flickr.groups.getInfo | Get information about a group |

### rest?method=flickr.groups.pools.getPhotos
| Method | Path | Description |
|--------|------|-------------|
| GET | /rest?method=flickr.groups.pools.getPhotos | Returns a list of pool photos for a given group |

### rest?method=flickr.groups.discuss.topics.getList
| Method | Path | Description |
|--------|------|-------------|
| GET | /rest?method=flickr.groups.discuss.topics.getList | Get a list of discussion topics in a group. |

### rest?method=flickr.groups.discuss.replies.getInfo
| Method | Path | Description |
|--------|------|-------------|
| GET | /rest?method=flickr.groups.discuss.replies.getInfo | Get information on a group topic reply |

### rest?method=flickr.groups.discuss.topics.getInfo
| Method | Path | Description |
|--------|------|-------------|
| GET | /rest?method=flickr.groups.discuss.topics.getInfo | Get information about a group discussion topic |

### rest?method=flickr.groups.pools.getContext
| Method | Path | Description |
|--------|------|-------------|
| GET | /rest?method=flickr.groups.pools.getContext | Returns next and previous photos for a photo in a group pool |

### rest?method=flickr.photolist.getContext
| Method | Path | Description |
|--------|------|-------------|
| GET | /rest?method=flickr.photolist.getContext | Returns next and previous photos in a photo list |

### rest?method=flickr.photos.getContext
| Method | Path | Description |
|--------|------|-------------|
| GET | /rest?method=flickr.photos.getContext | Returns next and previous photos for a photo in a photostream |

### rest?method=flickr.photos.licenses.getInfo
| Method | Path | Description |
|--------|------|-------------|
| GET | /rest?method=flickr.photos.licenses.getInfo | Fetches a list of available photo licenses for Flickr |

### rest?method=flickr.people.getInfo
| Method | Path | Description |
|--------|------|-------------|
| GET | /rest?method=flickr.people.getInfo | Returns a person |

### rest?method=flickr.photos.getExif
| Method | Path | Description |
|--------|------|-------------|
| GET | /rest?method=flickr.photos.getExif | Retrieves a list of EXIF/TIFF/GPS tags for a given photo. The calling user must have permission to view the photo. |

### rest?method=flickr.photos.getInfo
| Method | Path | Description |
|--------|------|-------------|
| GET | /rest?method=flickr.photos.getInfo | Returns a photo |

### rest?method=flickr.photos.getSizes
| Method | Path | Description |
|--------|------|-------------|
| GET | /rest?method=flickr.photos.getSizes | Returns photo sizes |

### rest?method=flickr.photosets.getContext
| Method | Path | Description |
|--------|------|-------------|
| GET | /rest?method=flickr.photosets.getContext | Returns next and previous photos for a photo in a set |

### rest?method=flickr.photosets.getPhotos
| Method | Path | Description |
|--------|------|-------------|
| GET | /rest?method=flickr.photosets.getPhotos | Returns a list of photos in an album. |

### rest?method=flickr.galleries.getPhotos
| Method | Path | Description |
|--------|------|-------------|
| GET | /rest?method=flickr.galleries.getPhotos | Returns a list of photos in a gallery. |

### rest?method=flickr.photos.search
| Method | Path | Description |
|--------|------|-------------|
| GET | /rest?method=flickr.photos.search | Return a list of photos matching some criteria. |

### upload
| Method | Path | Description |
|--------|------|-------------|
| POST | /upload | Uploads a new photo to Flickr |

### rest?method=flickr.test.echo
| Method | Path | Description |
|--------|------|-------------|
| GET | /rest?method=flickr.test.echo | Echos the input parameters back in the response |

### oauth
| Method | Path | Description |
|--------|------|-------------|
| GET | /oauth/request_token | Returns an oauth token and oauth token secret |
| GET | /oauth/access_token | Returns an access token |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all rest?method=flickr.favorites.getList?" -> GET /rest?method=flickr.favorites.getList
- "List all rest?method=flickr.people.getPhotos?" -> GET /rest?method=flickr.people.getPhotos
- "List all rest?method=flickr.photosets.getList?" -> GET /rest?method=flickr.photosets.getList
- "List all rest?method=flickr.favorites.getContext?" -> GET /rest?method=flickr.favorites.getContext
- "List all rest?method=flickr.groups.getInfo?" -> GET /rest?method=flickr.groups.getInfo
- "List all rest?method=flickr.groups.pools.getPhotos?" -> GET /rest?method=flickr.groups.pools.getPhotos
- "List all rest?method=flickr.groups.discuss.topics.getList?" -> GET /rest?method=flickr.groups.discuss.topics.getList
- "List all rest?method=flickr.groups.discuss.replies.getInfo?" -> GET /rest?method=flickr.groups.discuss.replies.getInfo
- "List all rest?method=flickr.groups.discuss.topics.getInfo?" -> GET /rest?method=flickr.groups.discuss.topics.getInfo
- "List all rest?method=flickr.groups.pools.getContext?" -> GET /rest?method=flickr.groups.pools.getContext
- "List all rest?method=flickr.photolist.getContext?" -> GET /rest?method=flickr.photolist.getContext
- "List all rest?method=flickr.photos.getContext?" -> GET /rest?method=flickr.photos.getContext
- "List all rest?method=flickr.photos.licenses.getInfo?" -> GET /rest?method=flickr.photos.licenses.getInfo
- "List all rest?method=flickr.people.getInfo?" -> GET /rest?method=flickr.people.getInfo
- "List all rest?method=flickr.photos.getExif?" -> GET /rest?method=flickr.photos.getExif
- "List all rest?method=flickr.photos.getInfo?" -> GET /rest?method=flickr.photos.getInfo
- "List all rest?method=flickr.photos.getSizes?" -> GET /rest?method=flickr.photos.getSizes
- "List all rest?method=flickr.photosets.getContext?" -> GET /rest?method=flickr.photosets.getContext
- "List all rest?method=flickr.photosets.getPhotos?" -> GET /rest?method=flickr.photosets.getPhotos
- "List all rest?method=flickr.galleries.getPhotos?" -> GET /rest?method=flickr.galleries.getPhotos
- "List all rest?method=flickr.photos.search?" -> GET /rest?method=flickr.photos.search
- "Create a upload?" -> POST /upload
- "List all rest?method=flickr.test.echo?" -> GET /rest?method=flickr.test.echo
- "List all request_token?" -> GET /oauth/request_token
- "List all access_token?" -> GET /oauth/access_token
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
