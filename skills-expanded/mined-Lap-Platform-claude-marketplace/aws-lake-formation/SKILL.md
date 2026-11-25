---
name: aws-lake-formation
description: "AWS Lake Formation API skill. Use when working with AWS Lake Formation for AddLFTagsToResource, AssumeDecoratedRoleWithSAML, BatchGrantPermissions. Covers 55 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS Lake Formation
API version: 2017-03-31

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST /AddLFTagsToResource -- create first AddLFTagsToResource

## Endpoints

55 endpoints across 55 groups. See references/api-spec.lap for full details.

### AddLFTagsToResource
| Method | Path | Description |
|--------|------|-------------|
| POST | /AddLFTagsToResource | Attaches one or more LF-tags to an existing resource. |

### AssumeDecoratedRoleWithSAML
| Method | Path | Description |
|--------|------|-------------|
| POST | /AssumeDecoratedRoleWithSAML | Allows a caller to assume an IAM role decorated as the SAML user specified in the SAML assertion included in the request. This decoration allows Lake Formation to enforce access policies against the SAML users and groups. This API operation requires SAML federation setup in the caller’s account as it can only be called with valid SAML assertions. Lake Formation does not scope down the permission of the assumed role. All permissions attached to the role via the SAML federation setup will be included in the role session.   This decorated role is expected to access data in Amazon S3 by getting temporary access from Lake Formation which is authorized via the virtual API GetDataAccess. Therefore, all SAML roles that can be assumed via AssumeDecoratedRoleWithSAML must at a minimum include lakeformation:GetDataAccess in their role policies. A typical IAM policy attached to such a role would look as follows: |

### BatchGrantPermissions
| Method | Path | Description |
|--------|------|-------------|
| POST | /BatchGrantPermissions | Batch operation to grant permissions to the principal. |

### BatchRevokePermissions
| Method | Path | Description |
|--------|------|-------------|
| POST | /BatchRevokePermissions | Batch operation to revoke permissions from the principal. |

### CancelTransaction
| Method | Path | Description |
|--------|------|-------------|
| POST | /CancelTransaction | Attempts to cancel the specified transaction. Returns an exception if the transaction was previously committed. |

### CommitTransaction
| Method | Path | Description |
|--------|------|-------------|
| POST | /CommitTransaction | Attempts to commit the specified transaction. Returns an exception if the transaction was previously aborted. This API action is idempotent if called multiple times for the same transaction. |

### CreateDataCellsFilter
| Method | Path | Description |
|--------|------|-------------|
| POST | /CreateDataCellsFilter | Creates a data cell filter to allow one to grant access to certain columns on certain rows. |

### CreateLFTag
| Method | Path | Description |
|--------|------|-------------|
| POST | /CreateLFTag | Creates an LF-tag with the specified name and values. |

### CreateLakeFormationIdentityCenterConfiguration
| Method | Path | Description |
|--------|------|-------------|
| POST | /CreateLakeFormationIdentityCenterConfiguration | Creates an IAM Identity Center connection with Lake Formation to allow IAM Identity Center users and groups to access Data Catalog resources. |

### CreateLakeFormationOptIn
| Method | Path | Description |
|--------|------|-------------|
| POST | /CreateLakeFormationOptIn | Enforce Lake Formation permissions for the given databases, tables, and principals. |

### DeleteDataCellsFilter
| Method | Path | Description |
|--------|------|-------------|
| POST | /DeleteDataCellsFilter | Deletes a data cell filter. |

### DeleteLFTag
| Method | Path | Description |
|--------|------|-------------|
| POST | /DeleteLFTag | Deletes the specified LF-tag given a key name. If the input parameter tag key was not found, then the operation will throw an exception. When you delete an LF-tag, the LFTagPolicy attached to the LF-tag becomes invalid. If the deleted LF-tag was still assigned to any resource, the tag policy attach to the deleted LF-tag will no longer be applied to the resource. |

### DeleteLakeFormationIdentityCenterConfiguration
| Method | Path | Description |
|--------|------|-------------|
| POST | /DeleteLakeFormationIdentityCenterConfiguration | Deletes an IAM Identity Center connection with Lake Formation. |

### DeleteLakeFormationOptIn
| Method | Path | Description |
|--------|------|-------------|
| POST | /DeleteLakeFormationOptIn | Remove the Lake Formation permissions enforcement of the given databases, tables, and principals. |

### DeleteObjectsOnCancel
| Method | Path | Description |
|--------|------|-------------|
| POST | /DeleteObjectsOnCancel | For a specific governed table, provides a list of Amazon S3 objects that will be written during the current transaction and that can be automatically deleted if the transaction is canceled. Without this call, no Amazon S3 objects are automatically deleted when a transaction cancels.   The Glue ETL library function write_dynamic_frame.from_catalog() includes an option to automatically call DeleteObjectsOnCancel before writes. For more information, see Rolling Back Amazon S3 Writes. |

### DeregisterResource
| Method | Path | Description |
|--------|------|-------------|
| POST | /DeregisterResource | Deregisters the resource as managed by the Data Catalog. When you deregister a path, Lake Formation removes the path from the inline policy attached to your service-linked role. |

### DescribeLakeFormationIdentityCenterConfiguration
| Method | Path | Description |
|--------|------|-------------|
| POST | /DescribeLakeFormationIdentityCenterConfiguration | Retrieves the instance ARN and application ARN for the connection. |

### DescribeResource
| Method | Path | Description |
|--------|------|-------------|
| POST | /DescribeResource | Retrieves the current data access role for the given resource registered in Lake Formation. |

### DescribeTransaction
| Method | Path | Description |
|--------|------|-------------|
| POST | /DescribeTransaction | Returns the details of a single transaction. |

### ExtendTransaction
| Method | Path | Description |
|--------|------|-------------|
| POST | /ExtendTransaction | Indicates to the service that the specified transaction is still active and should not be treated as idle and aborted. Write transactions that remain idle for a long period are automatically aborted unless explicitly extended. |

### GetDataCellsFilter
| Method | Path | Description |
|--------|------|-------------|
| POST | /GetDataCellsFilter | Returns a data cells filter. |

### GetDataLakePrincipal
| Method | Path | Description |
|--------|------|-------------|
| POST | /GetDataLakePrincipal | Returns the identity of the invoking principal. |

### GetDataLakeSettings
| Method | Path | Description |
|--------|------|-------------|
| POST | /GetDataLakeSettings | Retrieves the list of the data lake administrators of a Lake Formation-managed data lake. |

### GetEffectivePermissionsForPath
| Method | Path | Description |
|--------|------|-------------|
| POST | /GetEffectivePermissionsForPath | Returns the Lake Formation permissions for a specified table or database resource located at a path in Amazon S3. GetEffectivePermissionsForPath will not return databases and tables if the catalog is encrypted. |

### GetLFTag
| Method | Path | Description |
|--------|------|-------------|
| POST | /GetLFTag | Returns an LF-tag definition. |

### GetQueryState
| Method | Path | Description |
|--------|------|-------------|
| POST | /GetQueryState | Returns the state of a query previously submitted. Clients are expected to poll GetQueryState to monitor the current state of the planning before retrieving the work units. A query state is only visible to the principal that made the initial call to StartQueryPlanning. |

### GetQueryStatistics
| Method | Path | Description |
|--------|------|-------------|
| POST | /GetQueryStatistics | Retrieves statistics on the planning and execution of a query. |

### GetResourceLFTags
| Method | Path | Description |
|--------|------|-------------|
| POST | /GetResourceLFTags | Returns the LF-tags applied to a resource. |

### GetTableObjects
| Method | Path | Description |
|--------|------|-------------|
| POST | /GetTableObjects | Returns the set of Amazon S3 objects that make up the specified governed table. A transaction ID or timestamp can be specified for time-travel queries. |

### GetTemporaryGluePartitionCredentials
| Method | Path | Description |
|--------|------|-------------|
| POST | /GetTemporaryGluePartitionCredentials | This API is identical to GetTemporaryTableCredentials except that this is used when the target Data Catalog resource is of type Partition. Lake Formation restricts the permission of the vended credentials with the same scope down policy which restricts access to a single Amazon S3 prefix. |

### GetTemporaryGlueTableCredentials
| Method | Path | Description |
|--------|------|-------------|
| POST | /GetTemporaryGlueTableCredentials | Allows a caller in a secure environment to assume a role with permission to access Amazon S3. In order to vend such credentials, Lake Formation assumes the role associated with a registered location, for example an Amazon S3 bucket, with a scope down policy which restricts the access to a single prefix. |

### GetWorkUnitResults
| Method | Path | Description |
|--------|------|-------------|
| POST | /GetWorkUnitResults | Returns the work units resulting from the query. Work units can be executed in any order and in parallel. |

### GetWorkUnits
| Method | Path | Description |
|--------|------|-------------|
| POST | /GetWorkUnits | Retrieves the work units generated by the StartQueryPlanning operation. |

### GrantPermissions
| Method | Path | Description |
|--------|------|-------------|
| POST | /GrantPermissions | Grants permissions to the principal to access metadata in the Data Catalog and data organized in underlying data storage such as Amazon S3. For information about permissions, see Security and Access Control to Metadata and Data. |

### ListDataCellsFilter
| Method | Path | Description |
|--------|------|-------------|
| POST | /ListDataCellsFilter | Lists all the data cell filters on a table. |

### ListLFTags
| Method | Path | Description |
|--------|------|-------------|
| POST | /ListLFTags | Lists LF-tags that the requester has permission to view. |

### ListLakeFormationOptIns
| Method | Path | Description |
|--------|------|-------------|
| POST | /ListLakeFormationOptIns | Retrieve the current list of resources and principals that are opt in to enforce Lake Formation permissions. |

### ListPermissions
| Method | Path | Description |
|--------|------|-------------|
| POST | /ListPermissions | Returns a list of the principal permissions on the resource, filtered by the permissions of the caller. For example, if you are granted an ALTER permission, you are able to see only the principal permissions for ALTER. This operation returns only those permissions that have been explicitly granted. For information about permissions, see Security and Access Control to Metadata and Data. |

### ListResources
| Method | Path | Description |
|--------|------|-------------|
| POST | /ListResources | Lists the resources registered to be managed by the Data Catalog. |

### ListTableStorageOptimizers
| Method | Path | Description |
|--------|------|-------------|
| POST | /ListTableStorageOptimizers | Returns the configuration of all storage optimizers associated with a specified table. |

### ListTransactions
| Method | Path | Description |
|--------|------|-------------|
| POST | /ListTransactions | Returns metadata about transactions and their status. To prevent the response from growing indefinitely, only uncommitted transactions and those available for time-travel queries are returned. This operation can help you identify uncommitted transactions or to get information about transactions. |

### PutDataLakeSettings
| Method | Path | Description |
|--------|------|-------------|
| POST | /PutDataLakeSettings | Sets the list of data lake administrators who have admin privileges on all resources managed by Lake Formation. For more information on admin privileges, see Granting Lake Formation Permissions. This API replaces the current list of data lake admins with the new list being passed. To add an admin, fetch the current list and add the new admin to that list and pass that list in this API. |

### RegisterResource
| Method | Path | Description |
|--------|------|-------------|
| POST | /RegisterResource | Registers the resource as managed by the Data Catalog. To add or update data, Lake Formation needs read/write access to the chosen Amazon S3 path. Choose a role that you know has permission to do this, or choose the AWSServiceRoleForLakeFormationDataAccess service-linked role. When you register the first Amazon S3 path, the service-linked role and a new inline policy are created on your behalf. Lake Formation adds the first path to the inline policy and attaches it to the service-linked role. When you register subsequent paths, Lake Formation adds the path to the existing policy. The following request registers a new location and gives Lake Formation permission to use the service-linked role to access that location.  ResourceArn = arn:aws:s3:::my-bucket UseServiceLinkedRole = true  If UseServiceLinkedRole is not set to true, you must provide or set the RoleArn:  arn:aws:iam::12345:role/my-data-access-role |

### RemoveLFTagsFromResource
| Method | Path | Description |
|--------|------|-------------|
| POST | /RemoveLFTagsFromResource | Removes an LF-tag from the resource. Only database, table, or tableWithColumns resource are allowed. To tag columns, use the column inclusion list in tableWithColumns to specify column input. |

### RevokePermissions
| Method | Path | Description |
|--------|------|-------------|
| POST | /RevokePermissions | Revokes permissions to the principal to access metadata in the Data Catalog and data organized in underlying data storage such as Amazon S3. |

### SearchDatabasesByLFTags
| Method | Path | Description |
|--------|------|-------------|
| POST | /SearchDatabasesByLFTags | This operation allows a search on DATABASE resources by TagCondition. This operation is used by admins who want to grant user permissions on certain TagConditions. Before making a grant, the admin can use SearchDatabasesByTags to find all resources where the given TagConditions are valid to verify whether the returned resources can be shared. |

### SearchTablesByLFTags
| Method | Path | Description |
|--------|------|-------------|
| POST | /SearchTablesByLFTags | This operation allows a search on TABLE resources by LFTags. This will be used by admins who want to grant user permissions on certain LF-tags. Before making a grant, the admin can use SearchTablesByLFTags to find all resources where the given LFTags are valid to verify whether the returned resources can be shared. |

### StartQueryPlanning
| Method | Path | Description |
|--------|------|-------------|
| POST | /StartQueryPlanning | Submits a request to process a query statement. This operation generates work units that can be retrieved with the GetWorkUnits operation as soon as the query state is WORKUNITS_AVAILABLE or FINISHED. |

### StartTransaction
| Method | Path | Description |
|--------|------|-------------|
| POST | /StartTransaction | Starts a new transaction and returns its transaction ID. Transaction IDs are opaque objects that you can use to identify a transaction. |

### UpdateDataCellsFilter
| Method | Path | Description |
|--------|------|-------------|
| POST | /UpdateDataCellsFilter | Updates a data cell filter. |

### UpdateLFTag
| Method | Path | Description |
|--------|------|-------------|
| POST | /UpdateLFTag | Updates the list of possible values for the specified LF-tag key. If the LF-tag does not exist, the operation throws an EntityNotFoundException. The values in the delete key values will be deleted from list of possible values. If any value in the delete key values is attached to a resource, then API errors out with a 400 Exception - "Update not allowed". Untag the attribute before deleting the LF-tag key's value. |

### UpdateLakeFormationIdentityCenterConfiguration
| Method | Path | Description |
|--------|------|-------------|
| POST | /UpdateLakeFormationIdentityCenterConfiguration | Updates the IAM Identity Center connection parameters. |

### UpdateResource
| Method | Path | Description |
|--------|------|-------------|
| POST | /UpdateResource | Updates the data access role used for vending access to the given (registered) resource in Lake Formation. |

### UpdateTableObjects
| Method | Path | Description |
|--------|------|-------------|
| POST | /UpdateTableObjects | Updates the manifest of Amazon S3 objects that make up the specified governed table. |

### UpdateTableStorageOptimizer
| Method | Path | Description |
|--------|------|-------------|
| POST | /UpdateTableStorageOptimizer | Updates the configuration of the storage optimizers for a table. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a AddLFTagsToResource?" -> POST /AddLFTagsToResource
- "Create a AssumeDecoratedRoleWithSAML?" -> POST /AssumeDecoratedRoleWithSAML
- "Create a BatchGrantPermission?" -> POST /BatchGrantPermissions
- "Create a BatchRevokePermission?" -> POST /BatchRevokePermissions
- "Create a CancelTransaction?" -> POST /CancelTransaction
- "Create a CommitTransaction?" -> POST /CommitTransaction
- "Create a CreateDataCellsFilter?" -> POST /CreateDataCellsFilter
- "Create a CreateLFTag?" -> POST /CreateLFTag
- "Create a CreateLakeFormationIdentityCenterConfiguration?" -> POST /CreateLakeFormationIdentityCenterConfiguration
- "Create a CreateLakeFormationOptIn?" -> POST /CreateLakeFormationOptIn
- "Create a DeleteDataCellsFilter?" -> POST /DeleteDataCellsFilter
- "Create a DeleteLFTag?" -> POST /DeleteLFTag
- "Create a DeleteLakeFormationIdentityCenterConfiguration?" -> POST /DeleteLakeFormationIdentityCenterConfiguration
- "Create a DeleteLakeFormationOptIn?" -> POST /DeleteLakeFormationOptIn
- "Create a DeleteObjectsOnCancel?" -> POST /DeleteObjectsOnCancel
- "Create a DeregisterResource?" -> POST /DeregisterResource
- "Create a DescribeLakeFormationIdentityCenterConfiguration?" -> POST /DescribeLakeFormationIdentityCenterConfiguration
- "Create a DescribeResource?" -> POST /DescribeResource
- "Create a DescribeTransaction?" -> POST /DescribeTransaction
- "Create a ExtendTransaction?" -> POST /ExtendTransaction
- "Create a GetDataCellsFilter?" -> POST /GetDataCellsFilter
- "Create a GetDataLakePrincipal?" -> POST /GetDataLakePrincipal
- "Create a GetDataLakeSetting?" -> POST /GetDataLakeSettings
- "Create a GetEffectivePermissionsForPath?" -> POST /GetEffectivePermissionsForPath
- "Create a GetLFTag?" -> POST /GetLFTag
- "Create a GetQueryState?" -> POST /GetQueryState
- "Create a GetQueryStatistic?" -> POST /GetQueryStatistics
- "Create a GetResourceLFTag?" -> POST /GetResourceLFTags
- "Create a GetTableObject?" -> POST /GetTableObjects
- "Create a GetTemporaryGluePartitionCredential?" -> POST /GetTemporaryGluePartitionCredentials
- "Create a GetTemporaryGlueTableCredential?" -> POST /GetTemporaryGlueTableCredentials
- "Create a GetWorkUnitResult?" -> POST /GetWorkUnitResults
- "Create a GetWorkUnit?" -> POST /GetWorkUnits
- "Create a GrantPermission?" -> POST /GrantPermissions
- "Create a ListDataCellsFilter?" -> POST /ListDataCellsFilter
- "Create a ListLFTag?" -> POST /ListLFTags
- "Create a ListLakeFormationOptIn?" -> POST /ListLakeFormationOptIns
- "Create a ListPermission?" -> POST /ListPermissions
- "Create a ListResource?" -> POST /ListResources
- "Create a ListTableStorageOptimizer?" -> POST /ListTableStorageOptimizers
- "Create a ListTransaction?" -> POST /ListTransactions
- "Create a PutDataLakeSetting?" -> POST /PutDataLakeSettings
- "Create a RegisterResource?" -> POST /RegisterResource
- "Create a RemoveLFTagsFromResource?" -> POST /RemoveLFTagsFromResource
- "Create a RevokePermission?" -> POST /RevokePermissions
- "Create a SearchDatabasesByLFTag?" -> POST /SearchDatabasesByLFTags
- "Create a SearchTablesByLFTag?" -> POST /SearchTablesByLFTags
- "Create a StartQueryPlanning?" -> POST /StartQueryPlanning
- "Create a StartTransaction?" -> POST /StartTransaction
- "Create a UpdateDataCellsFilter?" -> POST /UpdateDataCellsFilter
- "Create a UpdateLFTag?" -> POST /UpdateLFTag
- "Create a UpdateLakeFormationIdentityCenterConfiguration?" -> POST /UpdateLakeFormationIdentityCenterConfiguration
- "Create a UpdateResource?" -> POST /UpdateResource
- "Create a UpdateTableObject?" -> POST /UpdateTableObjects
- "Create a UpdateTableStorageOptimizer?" -> POST /UpdateTableStorageOptimizer
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
