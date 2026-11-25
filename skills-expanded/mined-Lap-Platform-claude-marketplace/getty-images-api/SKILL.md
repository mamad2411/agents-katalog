---
name: getty-images-api
description: "Getty Images API skill. Use when working with Getty Images for affiliates, ai, artists. Covers 76 endpoints."
version: 1.0.0
generator: lapsh
---

# Getty Images API
API version: 3

## Auth
ApiKey Api-Key in header | OAuth2

## Base URL
Not specified.

## Setup
1. Set your API key in the appropriate header
2. GET /v3/affiliates/search/images -- verify access
3. POST /v3/ai/image-generations -- create first image-generations

## Endpoints

76 endpoints across 19 groups. See references/api-spec.lap for full details.

### affiliates
| Method | Path | Description |
|--------|------|-------------|
| GET | /v3/affiliates/search/images |  |
| GET | /v3/affiliates/search/videos |  |

### ai
| Method | Path | Description |
|--------|------|-------------|
| POST | /v3/ai/image-generations | Generates images from a prompt |
| GET | /v3/ai/image-generations/{generationRequestId} | Get generated images from a previous generation request |
| POST | /v3/ai/image-generations/{generationRequestId}/images/{index}/variations | Get variations on a generated image |
| POST | /v3/ai/file-registrations | Register a client provided file for use with AIGenerator endpoints |
| GET | /v3/ai/file-registrations |  |
| GET | /v3/ai/file-registrations/{fileRegistrationId} | Get details on a registered file |
| DELETE | /v3/ai/file-registrations/{fileRegistrationId} | Archives a registered file |
| POST | /v3/ai/image-generations/refine | Refine an image |
| POST | /v3/ai/image-generations/extend | Extend an image |
| POST | /v3/ai/image-generations/background-removal | Remove a background |
| POST | /v3/ai/image-generations/object-removal | Remove object(s) |
| POST | /v3/ai/image-generations/background-replacement | Replace the background of an existing image |
| POST | /v3/ai/image-generations/influence-color-by-image | Influence the color of generated images using a reference image |
| POST | /v3/ai/image-generations/influence-composition-by-image | Influence the composition of generated images using a reference image |
| POST | /v3/ai/image-generations/background-generations | Add a background to a reference image |
| GET | /v3/ai/generation-history | Retrieve history of AI generations |
| GET | /v3/ai/generation-history/{generationRequestId} | Retrieve history item for an individual generation request |
| GET | /v3/ai/image-generations/{generationRequestId}/images/{index}/download-sizes | Get download sizes for a generated image |
| PUT | /v3/ai/image-generations/{generationRequestId}/images/{index}/download | Begin the download process |
| GET | /v3/ai/image-generations/{generationRequestId}/images/{index}/download | Once the download process has started, this endpoint can be used to check the status of the download and get the |
| POST | /v3/ai/redownloads | Re-download a previously downloaded item |
| POST | /v3/ai/enhance-prompt | Expands and enriches a short prompt to produce a more detailed and descriptive prompt which can then be used to generate images. |

### artists
| Method | Path | Description |
|--------|------|-------------|
| GET | /v3/artists/images | Search for images by a photographer |
| GET | /v3/artists/videos | Search for videos by a photographer |

### asset-changes
| Method | Path | Description |
|--------|------|-------------|
| PUT | /v3/asset-changes/change-sets | Get asset change notifications. |
| DELETE | /v3/asset-changes/change-sets/{change-set-id} | Confirm asset change notifications. |
| GET | /v3/asset-changes/channels | Get a list of asset change notification channels. |

### asset-licensing
| Method | Path | Description |
|--------|------|-------------|
| POST | /v3/asset-licensing/{assetId} | Endpoint for acquiring extended licenses with iStock credits for an asset. |

### boards
| Method | Path | Description |
|--------|------|-------------|
| GET | /v3/boards | Get all boards that the user participates in |
| POST | /v3/boards | Create a new board |
| GET | /v3/boards/{board_id} | Get assets and metadata for a specific board |
| DELETE | /v3/boards/{board_id} | Delete a board |
| PUT | /v3/boards/{board_id} | Update a board |
| PUT | /v3/boards/{board_id}/assets | Add assets to a board |
| DELETE | /v3/boards/{board_id}/assets | Remove assets from a board |
| PUT | /v3/boards/{board_id}/assets/{asset_id} | Add an asset to a board |
| DELETE | /v3/boards/{board_id}/assets/{asset_id} | Remove an asset from a board |
| POST | /v3/boards/{board_id}/assets/{asset_id}/comments | Add a comment to an asset on the specified board. |
| DELETE | /v3/boards/{board_id}/assets/{asset_id}/comments/{comment_id} | Delete a comment from an asset on the specified board. |
| GET | /v3/boards/{board_id}/comments | Get comments from a board |
| POST | /v3/boards/{board_id}/comments | Add a comment to a board |
| DELETE | /v3/boards/{board_id}/comments/{comment_id} | Delete a comment from a board |

### collections
| Method | Path | Description |
|--------|------|-------------|
| GET | /v3/collections | Gets collections applicable for the customer. |

### countries
| Method | Path | Description |
|--------|------|-------------|
| GET | /v3/countries | Gets countries codes and names. |

### customers
| Method | Path | Description |
|--------|------|-------------|
| GET | /v3/customers/current | Returns information about the current user. |

### downloads
| Method | Path | Description |
|--------|------|-------------|
| GET | /v3/downloads | Returns information about a customer's downloaded assets. |
| POST | /v3/downloads/images/{id} | Download an image |
| POST | /v3/downloads/videos/{id} | Download a video |

### events
| Method | Path | Description |
|--------|------|-------------|
| GET | /v3/events | Get metadata for multiple events |
| GET | /v3/events/{id} | Get metadata for a single event |

### image-match
| Method | Path | Description |
|--------|------|-------------|
| GET | /v3/image-match/search | Searches for image matches using the provided URL. |

### images
| Method | Path | Description |
|--------|------|-------------|
| GET | /v3/images | Get metadata for multiple images by supplying multiple image ids |
| GET | /v3/images/{id} | Get metadata for a single image by supplying one image id |
| GET | /v3/images/{id}/downloadhistory | Returns information about a customer's download history for a specific asset |
| GET | /v3/images/{id}/same-series | Retrieve creative images from the same series |
| GET | /v3/images/{id}/similar | Retrieve similar images |

### orders
| Method | Path | Description |
|--------|------|-------------|
| GET | /v3/orders/{id} | Get order metadata |

### products
| Method | Path | Description |
|--------|------|-------------|
| GET | /v3/products | Get Products |

### purchased-assets
| Method | Path | Description |
|--------|------|-------------|
| GET | /v3/purchased-assets | Get Previously Purchased Images and Video |

### search
| Method | Path | Description |
|--------|------|-------------|
| GET | /v3/search/events | Search for events |
| GET | /v3/search/images/creative | Search for creative images only |
| GET | /v3/search/images/creative/by-image | Search for creative images based on url |
| GET | /v3/search/images/editorial | Search for editorial images only |
| GET | /v3/search/videos/creative | Search for creative videos |
| GET | /v3/search/videos/creative/by-image | Search for creative videos based on url |
| GET | /v3/search/videos/editorial | Search for editorial videos |
| PUT | /v3/search/by-image/uploads/{file-name} | Upload image for use by the search creative images/videos operations |
| GET | /v3/search/images | Search for both creative and editorial images - *** DEPRECATED *** |

### usage-batches
| Method | Path | Description |
|--------|------|-------------|
| PUT | /v3/usage-batches/{id} | Report usage of assets via a batch format. |

### videos
| Method | Path | Description |
|--------|------|-------------|
| GET | /v3/videos | Get metadata for multiple videos by supplying multiple video ids |
| GET | /v3/videos/{id} | Get metadata for a single video by supplying one video id |
| GET | /v3/videos/{id}/downloadhistory | Returns information about a customer's download history for a specific asset |
| GET | /v3/videos/{id}/same-series | Retrieve creative videos from the same series |
| GET | /v3/videos/{id}/similar | Retrieve similar videos |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all images?" -> GET /v3/affiliates/search/images
- "List all videos?" -> GET /v3/affiliates/search/videos
- "Create a image-generation?" -> POST /v3/ai/image-generations
- "Get image-generation details?" -> GET /v3/ai/image-generations/{generationRequestId}
- "Create a variation?" -> POST /v3/ai/image-generations/{generationRequestId}/images/{index}/variations
- "Create a file-registration?" -> POST /v3/ai/file-registrations
- "List all file-registrations?" -> GET /v3/ai/file-registrations
- "Get file-registration details?" -> GET /v3/ai/file-registrations/{fileRegistrationId}
- "Delete a file-registration?" -> DELETE /v3/ai/file-registrations/{fileRegistrationId}
- "Create a refine?" -> POST /v3/ai/image-generations/refine
- "Create a extend?" -> POST /v3/ai/image-generations/extend
- "Create a background-removal?" -> POST /v3/ai/image-generations/background-removal
- "Create a object-removal?" -> POST /v3/ai/image-generations/object-removal
- "Create a background-replacement?" -> POST /v3/ai/image-generations/background-replacement
- "Create a influence-color-by-image?" -> POST /v3/ai/image-generations/influence-color-by-image
- "Create a influence-composition-by-image?" -> POST /v3/ai/image-generations/influence-composition-by-image
- "Create a background-generation?" -> POST /v3/ai/image-generations/background-generations
- "List all generation-history?" -> GET /v3/ai/generation-history
- "Get generation-history details?" -> GET /v3/ai/generation-history/{generationRequestId}
- "List all download-sizes?" -> GET /v3/ai/image-generations/{generationRequestId}/images/{index}/download-sizes
- "List all download?" -> GET /v3/ai/image-generations/{generationRequestId}/images/{index}/download
- "Create a redownload?" -> POST /v3/ai/redownloads
- "Create a enhance-prompt?" -> POST /v3/ai/enhance-prompt
- "List all images?" -> GET /v3/artists/images
- "List all videos?" -> GET /v3/artists/videos
- "Delete a change-set?" -> DELETE /v3/asset-changes/change-sets/{change-set-id}
- "List all channels?" -> GET /v3/asset-changes/channels
- "List all boards?" -> GET /v3/boards
- "Create a board?" -> POST /v3/boards
- "Get board details?" -> GET /v3/boards/{board_id}
- "Delete a board?" -> DELETE /v3/boards/{board_id}
- "Update a board?" -> PUT /v3/boards/{board_id}
- "Update a asset?" -> PUT /v3/boards/{board_id}/assets/{asset_id}
- "Delete a asset?" -> DELETE /v3/boards/{board_id}/assets/{asset_id}
- "Create a comment?" -> POST /v3/boards/{board_id}/assets/{asset_id}/comments
- "Delete a comment?" -> DELETE /v3/boards/{board_id}/assets/{asset_id}/comments/{comment_id}
- "List all comments?" -> GET /v3/boards/{board_id}/comments
- "Create a comment?" -> POST /v3/boards/{board_id}/comments
- "Delete a comment?" -> DELETE /v3/boards/{board_id}/comments/{comment_id}
- "List all collections?" -> GET /v3/collections
- "List all countries?" -> GET /v3/countries
- "List all current?" -> GET /v3/customers/current
- "List all downloads?" -> GET /v3/downloads
- "List all events?" -> GET /v3/events
- "Get event details?" -> GET /v3/events/{id}
- "List all search?" -> GET /v3/image-match/search
- "List all images?" -> GET /v3/images
- "Get image details?" -> GET /v3/images/{id}
- "List all downloadhistory?" -> GET /v3/images/{id}/downloadhistory
- "List all same-series?" -> GET /v3/images/{id}/same-series
- "List all similar?" -> GET /v3/images/{id}/similar
- "Get order details?" -> GET /v3/orders/{id}
- "List all products?" -> GET /v3/products
- "List all purchased-assets?" -> GET /v3/purchased-assets
- "List all events?" -> GET /v3/search/events
- "List all creative?" -> GET /v3/search/images/creative
- "List all by-image?" -> GET /v3/search/images/creative/by-image
- "List all editorial?" -> GET /v3/search/images/editorial
- "List all creative?" -> GET /v3/search/videos/creative
- "List all by-image?" -> GET /v3/search/videos/creative/by-image
- "List all editorial?" -> GET /v3/search/videos/editorial
- "Update a upload?" -> PUT /v3/search/by-image/uploads/{file-name}
- "List all images?" -> GET /v3/search/images
- "Update a usage-batche?" -> PUT /v3/usage-batches/{id}
- "List all videos?" -> GET /v3/videos
- "Get video details?" -> GET /v3/videos/{id}
- "List all downloadhistory?" -> GET /v3/videos/{id}/downloadhistory
- "List all same-series?" -> GET /v3/videos/{id}/same-series
- "List all similar?" -> GET /v3/videos/{id}/similar
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
