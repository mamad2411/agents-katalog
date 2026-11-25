---
name: finspace-user-environment-management-service
description: "FinSpace User Environment Management service API skill. Use when working with FinSpace User Environment Management service for environment, kx, tags. Covers 50 endpoints."
version: 1.0.0
generator: lapsh
---

# FinSpace User Environment Management service
API version: 2021-03-12

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /environment -- verify access
3. POST /environment -- create first environment

## Endpoints

50 endpoints across 3 groups. See references/api-spec.lap for full details.

### environment
| Method | Path | Description |
|--------|------|-------------|
| POST | /environment | Create a new FinSpace environment. |
| DELETE | /environment/{environmentId} | Delete an FinSpace environment. |
| GET | /environment/{environmentId} | Returns the FinSpace environment object. |
| GET | /environment | A list of all of your FinSpace environments. |
| PUT | /environment/{environmentId} | Update your FinSpace environment. |

### kx
| Method | Path | Description |
|--------|------|-------------|
| POST | /kx/environments/{environmentId}/databases/{databaseName}/changesets | Creates a changeset for a kdb database. A changeset allows you to add and delete existing files by using an ordered list of change requests. |
| POST | /kx/environments/{environmentId}/clusters | Creates a new kdb cluster. |
| POST | /kx/environments/{environmentId}/databases | Creates a new kdb database in the environment. |
| POST | /kx/environments/{environmentId}/databases/{databaseName}/dataviews | Creates a snapshot of kdb database with tiered storage capabilities and a pre-warmed cache, ready for mounting on kdb clusters. Dataviews are only available for clusters running on a scaling group. They are not supported on dedicated clusters. |
| POST | /kx/environments | Creates a managed kdb environment for the account. |
| POST | /kx/environments/{environmentId}/scalingGroups | Creates a new scaling group. |
| POST | /kx/environments/{environmentId}/users | Creates a user in FinSpace kdb environment with an associated IAM role. |
| POST | /kx/environments/{environmentId}/kxvolumes | Creates a new volume with a specific amount of throughput and storage capacity. |
| DELETE | /kx/environments/{environmentId}/clusters/{clusterName} | Deletes a kdb cluster. |
| DELETE | /kx/environments/{environmentId}/clusters/{clusterName}/nodes/{nodeId} | Deletes the specified nodes from a cluster. |
| DELETE | /kx/environments/{environmentId}/databases/{databaseName} | Deletes the specified database and all of its associated data. This action is irreversible. You must copy any data out of the database before deleting it if the data is to be retained. |
| DELETE | /kx/environments/{environmentId}/databases/{databaseName}/dataviews/{dataviewName} | Deletes the specified dataview. Before deleting a dataview, make sure that it is not in use by any cluster. |
| DELETE | /kx/environments/{environmentId} | Deletes the kdb environment. This action is irreversible. Deleting a kdb environment will remove all the associated data and any services running in it. |
| DELETE | /kx/environments/{environmentId}/scalingGroups/{scalingGroupName} | Deletes the specified scaling group. This action is irreversible. You cannot delete a scaling group until all the clusters running on it have been deleted. |
| DELETE | /kx/environments/{environmentId}/users/{userName} | Deletes a user in the specified kdb environment. |
| DELETE | /kx/environments/{environmentId}/kxvolumes/{volumeName} | Deletes a volume. You can only delete a volume if it's not attached to a cluster or a dataview. When a volume is deleted, any data on the volume is lost. This action is irreversible. |
| GET | /kx/environments/{environmentId}/databases/{databaseName}/changesets/{changesetId} | Returns information about a kdb changeset. |
| GET | /kx/environments/{environmentId}/clusters/{clusterName} | Retrieves information about a kdb cluster. |
| GET | /kx/environments/{environmentId}/connectionString | Retrieves a connection string for a user to connect to a kdb cluster. You must call this API using the same role that you have defined while creating a user. |
| GET | /kx/environments/{environmentId}/databases/{databaseName} | Returns database information for the specified environment ID. |
| GET | /kx/environments/{environmentId}/databases/{databaseName}/dataviews/{dataviewName} | Retrieves details of the dataview. |
| GET | /kx/environments/{environmentId} | Retrieves all the information for the specified kdb environment. |
| GET | /kx/environments/{environmentId}/scalingGroups/{scalingGroupName} | Retrieves details of a scaling group. |
| GET | /kx/environments/{environmentId}/users/{userName} | Retrieves information about the specified kdb user. |
| GET | /kx/environments/{environmentId}/kxvolumes/{volumeName} | Retrieves the information about the volume. |
| GET | /kx/environments/{environmentId}/databases/{databaseName}/changesets | Returns a list of all the changesets for a database. |
| GET | /kx/environments/{environmentId}/clusters/{clusterName}/nodes | Lists all the nodes in a kdb cluster. |
| GET | /kx/environments/{environmentId}/clusters | Returns a list of clusters. |
| GET | /kx/environments/{environmentId}/databases | Returns a list of all the databases in the kdb environment. |
| GET | /kx/environments/{environmentId}/databases/{databaseName}/dataviews | Returns a list of all the dataviews in the database. |
| GET | /kx/environments | Returns a list of kdb environments created in an account. |
| GET | /kx/environments/{environmentId}/scalingGroups | Returns a list of scaling groups in a kdb environment. |
| GET | /kx/environments/{environmentId}/users | Lists all the users in a kdb environment. |
| GET | /kx/environments/{environmentId}/kxvolumes | Lists all the volumes in a kdb environment. |
| PUT | /kx/environments/{environmentId}/clusters/{clusterName}/configuration/code | Allows you to update code configuration on a running cluster. By using this API you can update the code, the initialization script path, and the command line arguments for a specific cluster. The configuration that you want to update will override any existing configurations on the cluster. |
| PUT | /kx/environments/{environmentId}/clusters/{clusterName}/configuration/databases | Updates the databases mounted on a kdb cluster, which includes the changesetId and all the dbPaths to be cached. This API does not allow you to change a database name or add a database if you created a cluster without one.  Using this API you can point a cluster to a different changeset and modify a list of partitions being cached. |
| PUT | /kx/environments/{environmentId}/databases/{databaseName} | Updates information for the given kdb database. |
| PUT | /kx/environments/{environmentId}/databases/{databaseName}/dataviews/{dataviewName} | Updates the specified dataview. The dataviews get automatically updated when any new changesets are ingested. Each update of the dataview creates a new version, including changeset details and cache configurations |
| PUT | /kx/environments/{environmentId} | Updates information for the given kdb environment. |
| PUT | /kx/environments/{environmentId}/network | Updates environment network to connect to your internal network by using a transit gateway. This API supports request to create a transit gateway attachment from FinSpace VPC to your transit gateway ID and create a custom Route-53 outbound resolvers. Once you send a request to update a network, you cannot change it again. Network update might require termination of any clusters that are running in the existing network. |
| PUT | /kx/environments/{environmentId}/users/{userName} | Updates the user details. You can only update the IAM role associated with a user. |
| PATCH | /kx/environments/{environmentId}/kxvolumes/{volumeName} | Updates the throughput or capacity of a volume. During the update process, the filesystem might be unavailable for a few minutes. You can retry any operations after the update is complete. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags/{resourceArn} | A list of all tags for a resource. |
| POST | /tags/{resourceArn} | Adds metadata tags to a FinSpace resource. |
| DELETE | /tags/{resourceArn} | Removes metadata tags from a FinSpace resource. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a environment?" -> POST /environment
- "Create a changeset?" -> POST /kx/environments/{environmentId}/databases/{databaseName}/changesets
- "Create a cluster?" -> POST /kx/environments/{environmentId}/clusters
- "Create a database?" -> POST /kx/environments/{environmentId}/databases
- "Create a dataview?" -> POST /kx/environments/{environmentId}/databases/{databaseName}/dataviews
- "Create a environment?" -> POST /kx/environments
- "Create a scalingGroup?" -> POST /kx/environments/{environmentId}/scalingGroups
- "Create a user?" -> POST /kx/environments/{environmentId}/users
- "Create a kxvolume?" -> POST /kx/environments/{environmentId}/kxvolumes
- "Delete a environment?" -> DELETE /environment/{environmentId}
- "Delete a cluster?" -> DELETE /kx/environments/{environmentId}/clusters/{clusterName}
- "Delete a node?" -> DELETE /kx/environments/{environmentId}/clusters/{clusterName}/nodes/{nodeId}
- "Delete a database?" -> DELETE /kx/environments/{environmentId}/databases/{databaseName}
- "Delete a dataview?" -> DELETE /kx/environments/{environmentId}/databases/{databaseName}/dataviews/{dataviewName}
- "Delete a environment?" -> DELETE /kx/environments/{environmentId}
- "Delete a scalingGroup?" -> DELETE /kx/environments/{environmentId}/scalingGroups/{scalingGroupName}
- "Delete a user?" -> DELETE /kx/environments/{environmentId}/users/{userName}
- "Delete a kxvolume?" -> DELETE /kx/environments/{environmentId}/kxvolumes/{volumeName}
- "Get environment details?" -> GET /environment/{environmentId}
- "Get changeset details?" -> GET /kx/environments/{environmentId}/databases/{databaseName}/changesets/{changesetId}
- "Get cluster details?" -> GET /kx/environments/{environmentId}/clusters/{clusterName}
- "List all connectionString?" -> GET /kx/environments/{environmentId}/connectionString
- "Get database details?" -> GET /kx/environments/{environmentId}/databases/{databaseName}
- "Get dataview details?" -> GET /kx/environments/{environmentId}/databases/{databaseName}/dataviews/{dataviewName}
- "Get environment details?" -> GET /kx/environments/{environmentId}
- "Get scalingGroup details?" -> GET /kx/environments/{environmentId}/scalingGroups/{scalingGroupName}
- "Get user details?" -> GET /kx/environments/{environmentId}/users/{userName}
- "Get kxvolume details?" -> GET /kx/environments/{environmentId}/kxvolumes/{volumeName}
- "List all environment?" -> GET /environment
- "List all changesets?" -> GET /kx/environments/{environmentId}/databases/{databaseName}/changesets
- "List all nodes?" -> GET /kx/environments/{environmentId}/clusters/{clusterName}/nodes
- "List all clusters?" -> GET /kx/environments/{environmentId}/clusters
- "List all databases?" -> GET /kx/environments/{environmentId}/databases
- "List all dataviews?" -> GET /kx/environments/{environmentId}/databases/{databaseName}/dataviews
- "List all environments?" -> GET /kx/environments
- "List all scalingGroups?" -> GET /kx/environments/{environmentId}/scalingGroups
- "List all users?" -> GET /kx/environments/{environmentId}/users
- "List all kxvolumes?" -> GET /kx/environments/{environmentId}/kxvolumes
- "Get tag details?" -> GET /tags/{resourceArn}
- "Delete a tag?" -> DELETE /tags/{resourceArn}
- "Update a environment?" -> PUT /environment/{environmentId}
- "Update a database?" -> PUT /kx/environments/{environmentId}/databases/{databaseName}
- "Update a dataview?" -> PUT /kx/environments/{environmentId}/databases/{databaseName}/dataviews/{dataviewName}
- "Update a environment?" -> PUT /kx/environments/{environmentId}
- "Update a user?" -> PUT /kx/environments/{environmentId}/users/{userName}
- "Partially update a kxvolume?" -> PATCH /kx/environments/{environmentId}/kxvolumes/{volumeName}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
