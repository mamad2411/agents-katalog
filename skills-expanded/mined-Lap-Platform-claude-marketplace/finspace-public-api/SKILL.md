---
name: finspace-public-api
description: "FinSpace Public API skill. Use when working with FinSpace Public for permission-group, datasets, datasetsv2. Covers 31 endpoints."
version: 1.0.0
generator: lapsh
---

# FinSpace Public API
API version: 2020-07-13

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /credentials/programmatic -- verify access
3. POST /permission-group/{permissionGroupId}/users/{userId} -- create first users

## Endpoints

31 endpoints across 6 groups. See references/api-spec.lap for full details.

### permission-group
| Method | Path | Description |
|--------|------|-------------|
| POST | /permission-group/{permissionGroupId}/users/{userId} | Adds a user to a permission group to grant permissions for actions a user can perform in FinSpace. |
| POST | /permission-group | Creates a group of permissions for various actions that a user can perform in FinSpace. |
| DELETE | /permission-group/{permissionGroupId} | Deletes a permission group. This action is irreversible. |
| DELETE | /permission-group/{permissionGroupId}/users/{userId} | Removes a user from a permission group. |
| GET | /permission-group/{permissionGroupId} | Retrieves the details of a specific permission group. |
| GET | /permission-group | Lists all available permission groups in FinSpace. |
| GET | /permission-group/{permissionGroupId}/users | Lists details of all the users in a specific permission group. |
| PUT | /permission-group/{permissionGroupId} | Modifies the details of a permission group. You cannot modify a permissionGroupID. |

### datasets
| Method | Path | Description |
|--------|------|-------------|
| POST | /datasets/{datasetId}/changesetsv2 | Creates a new Changeset in a FinSpace Dataset. |
| POST | /datasets/{datasetId}/dataviewsv2 | Creates a Dataview for a Dataset. |
| GET | /datasets/{datasetId}/changesetsv2/{changesetId} | Get information about a Changeset. |
| GET | /datasets/{datasetId}/dataviewsv2/{dataviewId} | Gets information about a Dataview. |
| POST | /datasets/{datasetId}/dataviewsv2/{dataviewId}/external-access-details | Returns the credentials to access the external Dataview from an S3 location. To call this API:   You must retrieve the programmatic credentials.   You must be a member of a FinSpace user group, where the dataset that you want to access has Read Dataset Data permissions. |
| GET | /datasets/{datasetId}/changesetsv2 | Lists the FinSpace Changesets for a Dataset. |
| GET | /datasets/{datasetId}/dataviewsv2 | Lists all available Dataviews for a Dataset. |
| PUT | /datasets/{datasetId}/changesetsv2/{changesetId} | Updates a FinSpace Changeset. |

### datasetsv2
| Method | Path | Description |
|--------|------|-------------|
| POST | /datasetsv2 | Creates a new FinSpace Dataset. |
| DELETE | /datasetsv2/{datasetId} | Deletes a FinSpace Dataset. |
| GET | /datasetsv2/{datasetId} | Returns information about a Dataset. |
| GET | /datasetsv2 | Lists all of the active Datasets that a user has access to. |
| PUT | /datasetsv2/{datasetId} | Updates a FinSpace Dataset. |

### user
| Method | Path | Description |
|--------|------|-------------|
| POST | /user | Creates a new user in FinSpace. |
| POST | /user/{userId}/disable | Denies access to the FinSpace web application and API for the specified user. |
| POST | /user/{userId}/enable | Allows the specified user to access the FinSpace web application and API. |
| GET | /user/{userId} | Retrieves details for a specific user. |
| GET | /user/{userId}/permission-groups | Lists all the permission groups that are associated with a specific user. |
| GET | /user | Lists all available users in FinSpace. |
| POST | /user/{userId}/password | Resets the password for a specified user ID and generates a temporary one. Only a superuser can reset password for other users. Resetting the password immediately invalidates the previous password associated with the user. |
| PUT | /user/{userId} | Modifies the details of the specified user. You cannot update the userId for a user. |

### credentials
| Method | Path | Description |
|--------|------|-------------|
| GET | /credentials/programmatic | Request programmatic credentials to use with FinSpace SDK. For more information, see Step 2. Access credentials programmatically using IAM access key id and secret access key. |

### workingLocationV1
| Method | Path | Description |
|--------|------|-------------|
| POST | /workingLocationV1 | A temporary Amazon S3 location, where you can copy your files from a source location to stage or use as a scratch space in FinSpace notebook. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a changesetsv2?" -> POST /datasets/{datasetId}/changesetsv2
- "Create a dataviewsv2?" -> POST /datasets/{datasetId}/dataviewsv2
- "Create a datasetsv2?" -> POST /datasetsv2
- "Create a permission-group?" -> POST /permission-group
- "Create a user?" -> POST /user
- "Delete a datasetsv2?" -> DELETE /datasetsv2/{datasetId}
- "Delete a permission-group?" -> DELETE /permission-group/{permissionGroupId}
- "Create a disable?" -> POST /user/{userId}/disable
- "Delete a user?" -> DELETE /permission-group/{permissionGroupId}/users/{userId}
- "Create a enable?" -> POST /user/{userId}/enable
- "Get changesetsv2 details?" -> GET /datasets/{datasetId}/changesetsv2/{changesetId}
- "Get dataviewsv2 details?" -> GET /datasets/{datasetId}/dataviewsv2/{dataviewId}
- "Get datasetsv2 details?" -> GET /datasetsv2/{datasetId}
- "Create a external-access-detail?" -> POST /datasets/{datasetId}/dataviewsv2/{dataviewId}/external-access-details
- "Get permission-group details?" -> GET /permission-group/{permissionGroupId}
- "List all programmatic?" -> GET /credentials/programmatic
- "Get user details?" -> GET /user/{userId}
- "Create a workingLocationV1?" -> POST /workingLocationV1
- "List all changesetsv2?" -> GET /datasets/{datasetId}/changesetsv2
- "List all dataviewsv2?" -> GET /datasets/{datasetId}/dataviewsv2
- "List all datasetsv2?" -> GET /datasetsv2
- "List all permission-group?" -> GET /permission-group
- "List all permission-groups?" -> GET /user/{userId}/permission-groups
- "List all user?" -> GET /user
- "List all users?" -> GET /permission-group/{permissionGroupId}/users
- "Create a password?" -> POST /user/{userId}/password
- "Update a changesetsv2?" -> PUT /datasets/{datasetId}/changesetsv2/{changesetId}
- "Update a datasetsv2?" -> PUT /datasetsv2/{datasetId}
- "Update a permission-group?" -> PUT /permission-group/{permissionGroupId}
- "Update a user?" -> PUT /user/{userId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
