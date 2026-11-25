---
name: custom-vision-training-client
description: "Custom Vision Training Client API skill. Use when working with Custom Vision Training Client for domains, projects. Covers 48 endpoints."
version: 1.0.0
generator: lapsh
---

# Custom Vision Training Client
API version: 3.2

## Auth
ApiKey Training-Key in header

## Base URL
https://southcentralus.api.cognitive.microsoft.com/customvision/v3.2/training

## Setup
1. Set your API key in the appropriate header
2. GET /domains -- verify access
3. POST /projects -- create first projects

## Endpoints

48 endpoints across 2 groups. See references/api-spec.lap for full details.

### domains
| Method | Path | Description |
|--------|------|-------------|
| GET | /domains | Get a list of the available domains. |
| GET | /domains/{domainId} | Get information about a specific domain. |

### projects
| Method | Path | Description |
|--------|------|-------------|
| GET | /projects | Get your projects. |
| POST | /projects | Create a project. |
| GET | /projects/{projectId} | Get a specific project. |
| DELETE | /projects/{projectId} | Delete a specific project. |
| PATCH | /projects/{projectId} | Update a specific project. |
| GET | /projects/{projectId}/export | Exports a project. |
| POST | /projects/{projectId}/images | This API accepts body content as multipart/form-data and application/octet-stream. When using multipart |
| DELETE | /projects/{projectId}/images | Delete images from the set of training images. |
| POST | /projects/{projectId}/images/{imageId}/regionproposals | This API will get region proposals for an image along with confidences for the region. It returns an empty array if no proposals are found. |
| POST | /projects/{projectId}/images/files | This API accepts a batch of files, and optionally tags, to create images. There is a limit of 64 images and 20 tags. |
| GET | /projects/{projectId}/images/id | This API will return a set of Images for the specified tags and optionally iteration. If no iteration is specified the |
| POST | /projects/{projectId}/images/predictions | This API creates a batch of images from predicted images specified. There is a limit of 64 images and 20 tags. |
| POST | /projects/{projectId}/images/regions | This API accepts a batch of image regions, and optionally tags, to update existing images with region information. |
| DELETE | /projects/{projectId}/images/regions | Delete a set of image regions. |
| POST | /projects/{projectId}/images/suggested | This API will fetch untagged images filtered by suggested tags Ids. It returns an empty array if no images are found. |
| POST | /projects/{projectId}/images/suggested/count | This API takes in tagIds to get count of untagged images per suggested tags for a given threshold. |
| GET | /projects/{projectId}/images/tagged | This API supports batching and range selection. By default it will only return first 50 images matching images. |
| GET | /projects/{projectId}/images/tagged/count | The filtering is on an and/or relationship. For example, if the provided tag ids are for the "Dog" and |
| POST | /projects/{projectId}/images/tags | Associate a set of images with a set of tags. |
| DELETE | /projects/{projectId}/images/tags | Remove a set of tags from a set of images. |
| GET | /projects/{projectId}/images/untagged | This API supports batching and range selection. By default it will only return first 50 images matching images. |
| GET | /projects/{projectId}/images/untagged/count | This API returns the images which have no tags for a given project and optionally an iteration. If no iteration is specified the |
| POST | /projects/{projectId}/images/urls | This API accepts a batch of urls, and optionally tags, to create images. There is a limit of 64 images and 20 tags. |
| GET | /projects/{projectId}/iterations | Get iterations for the project. |
| GET | /projects/{projectId}/iterations/{iterationId} | Get a specific iteration. |
| DELETE | /projects/{projectId}/iterations/{iterationId} | Delete a specific iteration of a project. |
| PATCH | /projects/{projectId}/iterations/{iterationId} | Update a specific iteration. |
| GET | /projects/{projectId}/iterations/{iterationId}/export | Get the list of exports for a specific iteration. |
| POST | /projects/{projectId}/iterations/{iterationId}/export | Export a trained iteration. |
| GET | /projects/{projectId}/iterations/{iterationId}/performance | Get detailed performance information about an iteration. |
| GET | /projects/{projectId}/iterations/{iterationId}/performance/images | This API supports batching and range selection. By default it will only return first 50 images matching images. |
| GET | /projects/{projectId}/iterations/{iterationId}/performance/images/count | The filtering is on an and/or relationship. For example, if the provided tag ids are for the "Dog" and |
| POST | /projects/{projectId}/iterations/{iterationId}/publish | Publish a specific iteration. |
| DELETE | /projects/{projectId}/iterations/{iterationId}/publish | Unpublish a specific iteration. |
| DELETE | /projects/{projectId}/predictions | Delete a set of predicted images and their associated prediction results. |
| POST | /projects/{projectId}/predictions/query | Get images that were sent to your prediction endpoint. |
| POST | /projects/{projectId}/quicktest/image | Quick test an image. |
| POST | /projects/{projectId}/quicktest/url | Quick test an image url. |
| GET | /projects/{projectId}/tags | Get the tags for a given project and iteration. |
| POST | /projects/{projectId}/tags | Create a tag for the project. |
| GET | /projects/{projectId}/tags/{tagId} | Get information about a specific tag. |
| DELETE | /projects/{projectId}/tags/{tagId} | Delete a tag from the project. |
| PATCH | /projects/{projectId}/tags/{tagId} | Update a tag. |
| POST | /projects/{projectId}/tagsandregions/suggestions | This API will get suggested tags and regions for an array/batch of untagged images along with confidences for the tags. It returns an empty array if no tags are found. |
| POST | /projects/{projectId}/train | Queues project for training. |
| POST | /projects/import | Imports a project. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all domains?" -> GET /domains
- "Get domain details?" -> GET /domains/{domainId}
- "List all projects?" -> GET /projects
- "Create a project?" -> POST /projects
- "Get project details?" -> GET /projects/{projectId}
- "Delete a project?" -> DELETE /projects/{projectId}
- "Partially update a project?" -> PATCH /projects/{projectId}
- "List all export?" -> GET /projects/{projectId}/export
- "Create a image?" -> POST /projects/{projectId}/images
- "Create a regionproposal?" -> POST /projects/{projectId}/images/{imageId}/regionproposals
- "Create a file?" -> POST /projects/{projectId}/images/files
- "List all id?" -> GET /projects/{projectId}/images/id
- "Create a prediction?" -> POST /projects/{projectId}/images/predictions
- "Create a region?" -> POST /projects/{projectId}/images/regions
- "Create a suggested?" -> POST /projects/{projectId}/images/suggested
- "Create a count?" -> POST /projects/{projectId}/images/suggested/count
- "List all tagged?" -> GET /projects/{projectId}/images/tagged
- "List all count?" -> GET /projects/{projectId}/images/tagged/count
- "Create a tag?" -> POST /projects/{projectId}/images/tags
- "List all untagged?" -> GET /projects/{projectId}/images/untagged
- "List all count?" -> GET /projects/{projectId}/images/untagged/count
- "Create a url?" -> POST /projects/{projectId}/images/urls
- "List all iterations?" -> GET /projects/{projectId}/iterations
- "Get iteration details?" -> GET /projects/{projectId}/iterations/{iterationId}
- "Delete a iteration?" -> DELETE /projects/{projectId}/iterations/{iterationId}
- "Partially update a iteration?" -> PATCH /projects/{projectId}/iterations/{iterationId}
- "List all export?" -> GET /projects/{projectId}/iterations/{iterationId}/export
- "Create a export?" -> POST /projects/{projectId}/iterations/{iterationId}/export
- "List all performance?" -> GET /projects/{projectId}/iterations/{iterationId}/performance
- "List all images?" -> GET /projects/{projectId}/iterations/{iterationId}/performance/images
- "List all count?" -> GET /projects/{projectId}/iterations/{iterationId}/performance/images/count
- "Create a publish?" -> POST /projects/{projectId}/iterations/{iterationId}/publish
- "Create a query?" -> POST /projects/{projectId}/predictions/query
- "Create a image?" -> POST /projects/{projectId}/quicktest/image
- "Create a url?" -> POST /projects/{projectId}/quicktest/url
- "List all tags?" -> GET /projects/{projectId}/tags
- "Create a tag?" -> POST /projects/{projectId}/tags
- "Get tag details?" -> GET /projects/{projectId}/tags/{tagId}
- "Delete a tag?" -> DELETE /projects/{projectId}/tags/{tagId}
- "Partially update a tag?" -> PATCH /projects/{projectId}/tags/{tagId}
- "Create a suggestion?" -> POST /projects/{projectId}/tagsandregions/suggestions
- "Create a train?" -> POST /projects/{projectId}/train
- "Create a import?" -> POST /projects/import
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
