---
name: cloud-functions-api
description: "Cloud Functions API skill. Use when working with Cloud Functions for {name}, {name}:generateDownloadUrl, {parent}. Covers 13 endpoints."
version: 1.0.0
generator: lapsh
---

# Cloud Functions API
API version: v2

## Auth
OAuth2 | OAuth2

## Base URL
https://cloudfunctions.googleapis.com/

## Setup
1. Configure auth: OAuth2 | OAuth2
2. GET /v2/{name}/locations -- verify access
3. POST /v2/{name}:generateDownloadUrl -- create first resource

## Endpoints

13 endpoints across 6 groups. See references/api-spec.lap for full details.

### {name}
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /v2/{name} | Deletes a function with the given name from the specified project. If the given function is used by some trigger, the trigger will be updated to remove this function. |
| GET | /v2/{name} | Gets the latest state of a long-running operation. Clients can use this method to poll the operation result at intervals as recommended by the API service. |
| PATCH | /v2/{name} | Updates existing function. |
| GET | /v2/{name}/locations | Lists information about the supported locations for this service. |
| GET | /v2/{name}/operations | Lists operations that match the specified filter in the request. If the server doesn't support this method, it returns `UNIMPLEMENTED`. |

### {name}:generateDownloadUrl
| Method | Path | Description |
|--------|------|-------------|
| POST | /v2/{name}:generateDownloadUrl | Returns a signed URL for downloading deployed function source code. The URL is only valid for a limited period and should be used within 30 minutes of generation. For more information about the signed URL usage see: https://cloud.google.com/storage/docs/access-control/signed-urls |

### {parent}
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/{parent}/functions | Returns a list of functions that belong to the requested project. |
| POST | /v2/{parent}/functions | Creates a new function. If a function with the given name already exists in the specified project, the long running operation will return `ALREADY_EXISTS` error. |
| POST | /v2/{parent}/functions:generateUploadUrl | Returns a signed URL for uploading a function source code. For more information about the signed URL usage see: https://cloud.google.com/storage/docs/access-control/signed-urls. Once the function source code upload is complete, the used signed URL should be provided in CreateFunction or UpdateFunction request as a reference to the function source code. When uploading source code to the generated signed URL, please follow these restrictions: * Source file type should be a zip file. * No credentials should be attached - the signed URLs provide access to the target bucket using internal service identity; if credentials were attached, the identity from the credentials would be used, but that identity does not have permissions to upload files to the URL. When making a HTTP PUT request, these two headers need to be specified: * `content-type: application/zip` And this header SHOULD NOT be specified: * `Authorization: Bearer YOUR_TOKEN` |
| GET | /v2/{parent}/runtimes | Returns a list of runtimes that are supported for the requested project. |

### {resource}:getIamPolicy
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/{resource}:getIamPolicy | Gets the access control policy for a resource. Returns an empty policy if the resource exists and does not have a policy set. |

### {resource}:setIamPolicy
| Method | Path | Description |
|--------|------|-------------|
| POST | /v2/{resource}:setIamPolicy | Sets the access control policy on the specified resource. Replaces any existing policy. Can return `NOT_FOUND`, `INVALID_ARGUMENT`, and `PERMISSION_DENIED` errors. |

### {resource}:testIamPermissions
| Method | Path | Description |
|--------|------|-------------|
| POST | /v2/{resource}:testIamPermissions | Returns permissions that a caller has on the specified resource. If the resource does not exist, this will return an empty set of permissions, not a `NOT_FOUND` error. Note: This operation is designed to be used for building permission-aware UIs and command-line tools, not for authorization checking. This operation may "fail open" without warning. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all locations?" -> GET /v2/{name}/locations
- "List all operations?" -> GET /v2/{name}/operations
- "List all functions?" -> GET /v2/{parent}/functions
- "Create a function?" -> POST /v2/{parent}/functions
- "Create a functions:generateUploadUrl?" -> POST /v2/{parent}/functions:generateUploadUrl
- "List all runtimes?" -> GET /v2/{parent}/runtimes
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
