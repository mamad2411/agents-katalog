---
name: azure-container-registry
description: "Azure Container Registry API skill. Use when working with Azure Container Registry for v2, {name}, {nextBlobUuidLink}. Covers 26 endpoints."
version: 1.0.0
generator: lapsh
---

# Azure Container Registry
API version: 2019-08-15-preview

## Auth
basic | ApiKey Authorization in header

## Base URL
Not specified.

## Setup
1. Set your API key in the appropriate header
2. GET /v2/ -- verify access
3. POST /v2/{name}/blobs/uploads/ -- create first uploads

## Endpoints

26 endpoints across 5 groups. See references/api-spec.lap for full details.

### v2
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/ | Tells whether this Docker Registry instance supports Docker Registry HTTP API v2 |

### {name}
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/{name}/manifests/{reference} | Get the manifest identified by `name` and `reference` where `reference` can be a tag or digest. |
| PUT | /v2/{name}/manifests/{reference} | Put the manifest identified by `name` and `reference` where `reference` can be a tag or digest. |
| DELETE | /v2/{name}/manifests/{reference} | Delete the manifest identified by `name` and `reference`. Note that a manifest can _only_ be deleted by `digest`. |
| GET | /v2/{name}/blobs/{digest} | Retrieve the blob from the registry identified by digest. |
| HEAD | /v2/{name}/blobs/{digest} | Same as GET, except only the headers are returned. |
| DELETE | /v2/{name}/blobs/{digest} | Removes an already uploaded blob. |
| POST | /v2/{name}/blobs/uploads/ | Mount a blob identified by the `mount` parameter from another repository. |

### {nextBlobUuidLink}
| Method | Path | Description |
|--------|------|-------------|
| GET | /{nextBlobUuidLink} | Retrieve status of upload identified by uuid. The primary purpose of this endpoint is to resolve the current status of a resumable upload. |
| PATCH | /{nextBlobUuidLink} | Upload a stream of data without completing the upload. |
| PUT | /{nextBlobUuidLink} | Complete the upload, providing all the data in the body, if necessary. A request without a body will just complete the upload with previously uploaded content. |
| DELETE | /{nextBlobUuidLink} | Cancel outstanding upload processes, releasing associated resources. If this is not called, the unfinished uploads will eventually timeout. |

### acr
| Method | Path | Description |
|--------|------|-------------|
| GET | /acr/v1/_catalog | List repositories |
| GET | /acr/v1/{name} | Get repository attributes |
| DELETE | /acr/v1/{name} | Delete the repository identified by `name` |
| PATCH | /acr/v1/{name} | Update the attribute identified by `name` where `reference` is the name of the repository. |
| GET | /acr/v1/{name}/_tags | List tags of a repository |
| GET | /acr/v1/{name}/_tags/{reference} | Get tag attributes by tag |
| PATCH | /acr/v1/{name}/_tags/{reference} | Update tag attributes |
| DELETE | /acr/v1/{name}/_tags/{reference} | Delete tag |
| GET | /acr/v1/{name}/_manifests | List manifests of a repository |
| GET | /acr/v1/{name}/_manifests/{reference} | Get manifest attributes |
| PATCH | /acr/v1/{name}/_manifests/{reference} | Update attributes of a manifest |

### oauth2
| Method | Path | Description |
|--------|------|-------------|
| POST | /oauth2/exchange | Exchange AAD tokens for an ACR refresh Token |
| POST | /oauth2/token | Exchange ACR Refresh token for an ACR Access Token |
| GET | /oauth2/token | Exchange Username, Password and Scope an ACR Access Token |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get manifest details?" -> GET /v2/{name}/manifests/{reference}
- "Update a manifest?" -> PUT /v2/{name}/manifests/{reference}
- "Delete a manifest?" -> DELETE /v2/{name}/manifests/{reference}
- "Get blob details?" -> GET /v2/{name}/blobs/{digest}
- "Delete a blob?" -> DELETE /v2/{name}/blobs/{digest}
- "Create a upload?" -> POST /v2/{name}/blobs/uploads/
- "List all _catalog?" -> GET /acr/v1/_catalog
- "Get acr details?" -> GET /acr/v1/{name}
- "Delete a acr?" -> DELETE /acr/v1/{name}
- "Partially update a acr?" -> PATCH /acr/v1/{name}
- "List all _tags?" -> GET /acr/v1/{name}/_tags
- "Get _tag details?" -> GET /acr/v1/{name}/_tags/{reference}
- "Partially update a _tag?" -> PATCH /acr/v1/{name}/_tags/{reference}
- "Delete a _tag?" -> DELETE /acr/v1/{name}/_tags/{reference}
- "List all _manifests?" -> GET /acr/v1/{name}/_manifests
- "Get _manifest details?" -> GET /acr/v1/{name}/_manifests/{reference}
- "Partially update a _manifest?" -> PATCH /acr/v1/{name}/_manifests/{reference}
- "Create a exchange?" -> POST /oauth2/exchange
- "Create a token?" -> POST /oauth2/token
- "List all token?" -> GET /oauth2/token
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
