---
name: cloud-storage-json-api
description: "Cloud Storage JSON API skill. Use when working with Cloud Storage JSON for b, channels, projects. Covers 52 endpoints."
version: 1.0.0
generator: lapsh
---

# Cloud Storage JSON API
API version: v1

## Auth
OAuth2 | OAuth2

## Base URL
https://storage.googleapis.com/storage/v1

## Setup
1. Configure auth: OAuth2 | OAuth2
2. GET /b -- verify access
3. POST /b -- create first b

## Endpoints

52 endpoints across 3 groups. See references/api-spec.lap for full details.

### b
| Method | Path | Description |
|--------|------|-------------|
| GET | /b | Retrieves a list of buckets for a given project. |
| POST | /b | Creates a new bucket. |
| DELETE | /b/{bucket} | Permanently deletes an empty bucket. |
| GET | /b/{bucket} | Returns metadata for the specified bucket. |
| PATCH | /b/{bucket} | Patches a bucket. Changes to the bucket will be readable immediately after writing, but configuration changes may take time to propagate. |
| PUT | /b/{bucket} | Updates a bucket. Changes to the bucket will be readable immediately after writing, but configuration changes may take time to propagate. |
| GET | /b/{bucket}/acl | Retrieves ACL entries on the specified bucket. |
| POST | /b/{bucket}/acl | Creates a new ACL entry on the specified bucket. |
| DELETE | /b/{bucket}/acl/{entity} | Permanently deletes the ACL entry for the specified entity on the specified bucket. |
| GET | /b/{bucket}/acl/{entity} | Returns the ACL entry for the specified entity on the specified bucket. |
| PATCH | /b/{bucket}/acl/{entity} | Patches an ACL entry on the specified bucket. |
| PUT | /b/{bucket}/acl/{entity} | Updates an ACL entry on the specified bucket. |
| GET | /b/{bucket}/defaultObjectAcl | Retrieves default object ACL entries on the specified bucket. |
| POST | /b/{bucket}/defaultObjectAcl | Creates a new default object ACL entry on the specified bucket. |
| DELETE | /b/{bucket}/defaultObjectAcl/{entity} | Permanently deletes the default object ACL entry for the specified entity on the specified bucket. |
| GET | /b/{bucket}/defaultObjectAcl/{entity} | Returns the default object ACL entry for the specified entity on the specified bucket. |
| PATCH | /b/{bucket}/defaultObjectAcl/{entity} | Patches a default object ACL entry on the specified bucket. |
| PUT | /b/{bucket}/defaultObjectAcl/{entity} | Updates a default object ACL entry on the specified bucket. |
| GET | /b/{bucket}/iam | Returns an IAM policy for the specified bucket. |
| PUT | /b/{bucket}/iam | Updates an IAM policy for the specified bucket. |
| GET | /b/{bucket}/iam/testPermissions | Tests a set of permissions on the given bucket to see which, if any, are held by the caller. |
| POST | /b/{bucket}/lockRetentionPolicy | Locks retention policy on a bucket. |
| GET | /b/{bucket}/notificationConfigs | Retrieves a list of notification subscriptions for a given bucket. |
| POST | /b/{bucket}/notificationConfigs | Creates a notification subscription for a given bucket. |
| DELETE | /b/{bucket}/notificationConfigs/{notification} | Permanently deletes a notification subscription. |
| GET | /b/{bucket}/notificationConfigs/{notification} | View a notification configuration. |
| GET | /b/{bucket}/o | Retrieves a list of objects matching the criteria. |
| POST | /b/{bucket}/o | Stores a new object and metadata. |
| POST | /b/{bucket}/o/watch | Watch for changes on all objects in a bucket. |
| DELETE | /b/{bucket}/o/{object} | Deletes an object and its metadata. Deletions are permanent if versioning is not enabled for the bucket, or if the generation parameter is used. |
| GET | /b/{bucket}/o/{object} | Retrieves an object or its metadata. |
| PATCH | /b/{bucket}/o/{object} | Patches an object's metadata. |
| PUT | /b/{bucket}/o/{object} | Updates an object's metadata. |
| GET | /b/{bucket}/o/{object}/acl | Retrieves ACL entries on the specified object. |
| POST | /b/{bucket}/o/{object}/acl | Creates a new ACL entry on the specified object. |
| DELETE | /b/{bucket}/o/{object}/acl/{entity} | Permanently deletes the ACL entry for the specified entity on the specified object. |
| GET | /b/{bucket}/o/{object}/acl/{entity} | Returns the ACL entry for the specified entity on the specified object. |
| PATCH | /b/{bucket}/o/{object}/acl/{entity} | Patches an ACL entry on the specified object. |
| PUT | /b/{bucket}/o/{object}/acl/{entity} | Updates an ACL entry on the specified object. |
| GET | /b/{bucket}/o/{object}/iam | Returns an IAM policy for the specified object. |
| PUT | /b/{bucket}/o/{object}/iam | Updates an IAM policy for the specified object. |
| GET | /b/{bucket}/o/{object}/iam/testPermissions | Tests a set of permissions on the given object to see which, if any, are held by the caller. |
| POST | /b/{destinationBucket}/o/{destinationObject}/compose | Concatenates a list of existing objects into a new object in the same bucket. |
| POST | /b/{sourceBucket}/o/{sourceObject}/copyTo/b/{destinationBucket}/o/{destinationObject} | Copies a source object to a destination object. Optionally overrides metadata. |
| POST | /b/{sourceBucket}/o/{sourceObject}/rewriteTo/b/{destinationBucket}/o/{destinationObject} | Rewrites a source object to a destination object. Optionally overrides metadata. |

### channels
| Method | Path | Description |
|--------|------|-------------|
| POST | /channels/stop | Stop watching resources through this channel |

### projects
| Method | Path | Description |
|--------|------|-------------|
| GET | /projects/{projectId}/hmacKeys | Retrieves a list of HMAC keys matching the criteria. |
| POST | /projects/{projectId}/hmacKeys | Creates a new HMAC key for the specified service account. |
| DELETE | /projects/{projectId}/hmacKeys/{accessId} | Deletes an HMAC key. |
| GET | /projects/{projectId}/hmacKeys/{accessId} | Retrieves an HMAC key's metadata |
| PUT | /projects/{projectId}/hmacKeys/{accessId} | Updates the state of an HMAC key. See the HMAC Key resource descriptor for valid states. |
| GET | /projects/{projectId}/serviceAccount | Get the email address of this project's Google Cloud Storage service account. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all b?" -> GET /b
- "Create a b?" -> POST /b
- "Delete a b?" -> DELETE /b/{bucket}
- "Get b details?" -> GET /b/{bucket}
- "Partially update a b?" -> PATCH /b/{bucket}
- "Update a b?" -> PUT /b/{bucket}
- "List all acl?" -> GET /b/{bucket}/acl
- "Create a acl?" -> POST /b/{bucket}/acl
- "Delete a acl?" -> DELETE /b/{bucket}/acl/{entity}
- "Get acl details?" -> GET /b/{bucket}/acl/{entity}
- "Partially update a acl?" -> PATCH /b/{bucket}/acl/{entity}
- "Update a acl?" -> PUT /b/{bucket}/acl/{entity}
- "List all defaultObjectAcl?" -> GET /b/{bucket}/defaultObjectAcl
- "Create a defaultObjectAcl?" -> POST /b/{bucket}/defaultObjectAcl
- "Delete a defaultObjectAcl?" -> DELETE /b/{bucket}/defaultObjectAcl/{entity}
- "Get defaultObjectAcl details?" -> GET /b/{bucket}/defaultObjectAcl/{entity}
- "Partially update a defaultObjectAcl?" -> PATCH /b/{bucket}/defaultObjectAcl/{entity}
- "Update a defaultObjectAcl?" -> PUT /b/{bucket}/defaultObjectAcl/{entity}
- "List all iam?" -> GET /b/{bucket}/iam
- "List all testPermissions?" -> GET /b/{bucket}/iam/testPermissions
- "Create a lockRetentionPolicy?" -> POST /b/{bucket}/lockRetentionPolicy
- "List all notificationConfigs?" -> GET /b/{bucket}/notificationConfigs
- "Create a notificationConfig?" -> POST /b/{bucket}/notificationConfigs
- "Delete a notificationConfig?" -> DELETE /b/{bucket}/notificationConfigs/{notification}
- "Get notificationConfig details?" -> GET /b/{bucket}/notificationConfigs/{notification}
- "List all o?" -> GET /b/{bucket}/o
- "Create a o?" -> POST /b/{bucket}/o
- "Create a watch?" -> POST /b/{bucket}/o/watch
- "Delete a o?" -> DELETE /b/{bucket}/o/{object}
- "Get o details?" -> GET /b/{bucket}/o/{object}
- "Partially update a o?" -> PATCH /b/{bucket}/o/{object}
- "Update a o?" -> PUT /b/{bucket}/o/{object}
- "List all acl?" -> GET /b/{bucket}/o/{object}/acl
- "Create a acl?" -> POST /b/{bucket}/o/{object}/acl
- "Delete a acl?" -> DELETE /b/{bucket}/o/{object}/acl/{entity}
- "Get acl details?" -> GET /b/{bucket}/o/{object}/acl/{entity}
- "Partially update a acl?" -> PATCH /b/{bucket}/o/{object}/acl/{entity}
- "Update a acl?" -> PUT /b/{bucket}/o/{object}/acl/{entity}
- "List all iam?" -> GET /b/{bucket}/o/{object}/iam
- "List all testPermissions?" -> GET /b/{bucket}/o/{object}/iam/testPermissions
- "Create a compose?" -> POST /b/{destinationBucket}/o/{destinationObject}/compose
- "Create a stop?" -> POST /channels/stop
- "List all hmacKeys?" -> GET /projects/{projectId}/hmacKeys
- "Create a hmacKey?" -> POST /projects/{projectId}/hmacKeys
- "Delete a hmacKey?" -> DELETE /projects/{projectId}/hmacKeys/{accessId}
- "Get hmacKey details?" -> GET /projects/{projectId}/hmacKeys/{accessId}
- "Update a hmacKey?" -> PUT /projects/{projectId}/hmacKeys/{accessId}
- "List all serviceAccount?" -> GET /projects/{projectId}/serviceAccount
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
