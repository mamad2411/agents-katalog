---
name: datalakeanalyticscatalogmanagementclient
description: "DataLakeAnalyticsCatalogManagementClient API skill. Use when working with DataLakeAnalyticsCatalogManagementClient for catalog. Covers 45 endpoints."
version: 1.0.0
generator: lapsh
---

# DataLakeAnalyticsCatalogManagementClient
API version: 2016-11-01

## Auth
No authentication required.

## Base URL
Not specified.

## Setup
1. No auth setup needed
2. GET /catalog/usql/acl -- verify access
3. POST /catalog/usql/databases/{databaseName}/credentials/{credentialName} -- create first credentials

## Endpoints

45 endpoints across 1 groups. See references/api-spec.lap for full details.

### catalog
| Method | Path | Description |
|--------|------|-------------|
| PUT | /catalog/usql/databases/{databaseName}/secrets/{secretName} | Creates the specified secret for use with external data sources in the specified database. This is deprecated and will be removed in the next release. Please use CreateCredential instead. |
| GET | /catalog/usql/databases/{databaseName}/secrets/{secretName} | Gets the specified secret in the specified database. This is deprecated and will be removed in the next release. Please use GetCredential instead. |
| PATCH | /catalog/usql/databases/{databaseName}/secrets/{secretName} | Modifies the specified secret for use with external data sources in the specified database. This is deprecated and will be removed in the next release. Please use UpdateCredential instead. |
| DELETE | /catalog/usql/databases/{databaseName}/secrets/{secretName} | Deletes the specified secret in the specified database. This is deprecated and will be removed in the next release. Please use DeleteCredential instead. |
| DELETE | /catalog/usql/databases/{databaseName}/secrets | Deletes all secrets in the specified database. This is deprecated and will be removed in the next release. In the future, please only drop individual credentials using DeleteCredential |
| PUT | /catalog/usql/databases/{databaseName}/credentials/{credentialName} | Creates the specified credential for use with external data sources in the specified database. |
| GET | /catalog/usql/databases/{databaseName}/credentials/{credentialName} | Retrieves the specified credential from the Data Lake Analytics catalog. |
| PATCH | /catalog/usql/databases/{databaseName}/credentials/{credentialName} | Modifies the specified credential for use with external data sources in the specified database |
| POST | /catalog/usql/databases/{databaseName}/credentials/{credentialName} | Deletes the specified credential in the specified database |
| GET | /catalog/usql/databases/{databaseName}/credentials | Retrieves the list of credentials from the Data Lake Analytics catalog. |
| GET | /catalog/usql/databases/{databaseName}/externaldatasources/{externalDataSourceName} | Retrieves the specified external data source from the Data Lake Analytics catalog. |
| GET | /catalog/usql/databases/{databaseName}/externaldatasources | Retrieves the list of external data sources from the Data Lake Analytics catalog. |
| GET | /catalog/usql/databases/{databaseName}/schemas/{schemaName}/procedures/{procedureName} | Retrieves the specified procedure from the Data Lake Analytics catalog. |
| GET | /catalog/usql/databases/{databaseName}/schemas/{schemaName}/procedures | Retrieves the list of procedures from the Data Lake Analytics catalog. |
| GET | /catalog/usql/databases/{databaseName}/schemas/{schemaName}/tables/{tableName} | Retrieves the specified table from the Data Lake Analytics catalog. |
| GET | /catalog/usql/databases/{databaseName}/schemas/{schemaName}/tables/{tableName}/tablefragments | Retrieves the list of table fragments from the Data Lake Analytics catalog. |
| GET | /catalog/usql/databases/{databaseName}/schemas/{schemaName}/tables | Retrieves the list of tables from the Data Lake Analytics catalog. |
| GET | /catalog/usql/databases/{databaseName}/schemas/{schemaName}/statistics | Retrieves the list of all table statistics within the specified schema from the Data Lake Analytics catalog. |
| GET | /catalog/usql/databases/{databaseName}/schemas/{schemaName}/tabletypes/{tableTypeName} | Retrieves the specified table type from the Data Lake Analytics catalog. |
| GET | /catalog/usql/databases/{databaseName}/schemas/{schemaName}/tabletypes | Retrieves the list of table types from the Data Lake Analytics catalog. |
| GET | /catalog/usql/databases/{databaseName}/schemas/{schemaName}/packages/{packageName} | Retrieves the specified package from the Data Lake Analytics catalog. |
| GET | /catalog/usql/databases/{databaseName}/schemas/{schemaName}/packages | Retrieves the list of packages from the Data Lake Analytics catalog. |
| GET | /catalog/usql/databases/{databaseName}/schemas/{schemaName}/views/{viewName} | Retrieves the specified view from the Data Lake Analytics catalog. |
| GET | /catalog/usql/databases/{databaseName}/schemas/{schemaName}/views | Retrieves the list of views from the Data Lake Analytics catalog. |
| GET | /catalog/usql/databases/{databaseName}/schemas/{schemaName}/tables/{tableName}/statistics/{statisticsName} | Retrieves the specified table statistics from the Data Lake Analytics catalog. |
| GET | /catalog/usql/databases/{databaseName}/schemas/{schemaName}/tables/{tableName}/statistics | Retrieves the list of table statistics from the Data Lake Analytics catalog. |
| GET | /catalog/usql/databases/{databaseName}/schemas/{schemaName}/tables/{tableName}/partitions/{partitionName}/previewrows | Retrieves a preview set of rows in given partition. |
| GET | /catalog/usql/databases/{databaseName}/schemas/{schemaName}/tables/{tableName}/partitions/{partitionName} | Retrieves the specified table partition from the Data Lake Analytics catalog. |
| GET | /catalog/usql/databases/{databaseName}/schemas/{schemaName}/tables/{tableName}/previewrows | Retrieves a preview set of rows in given table. |
| GET | /catalog/usql/databases/{databaseName}/schemas/{schemaName}/tables/{tableName}/partitions | Retrieves the list of table partitions from the Data Lake Analytics catalog. |
| GET | /catalog/usql/databases/{databaseName}/schemas/{schemaName}/types | Retrieves the list of types within the specified database and schema from the Data Lake Analytics catalog. |
| GET | /catalog/usql/databases/{databaseName}/schemas/{schemaName}/tablevaluedfunctions/{tableValuedFunctionName} | Retrieves the specified table valued function from the Data Lake Analytics catalog. |
| GET | /catalog/usql/databases/{databaseName}/schemas/{schemaName}/tablevaluedfunctions | Retrieves the list of table valued functions from the Data Lake Analytics catalog. |
| GET | /catalog/usql/databases/{databaseName}/assemblies/{assemblyName} | Retrieves the specified assembly from the Data Lake Analytics catalog. |
| GET | /catalog/usql/databases/{databaseName}/assemblies | Retrieves the list of assemblies from the Data Lake Analytics catalog. |
| GET | /catalog/usql/databases/{databaseName}/schemas/{schemaName} | Retrieves the specified schema from the Data Lake Analytics catalog. |
| GET | /catalog/usql/databases/{databaseName}/schemas | Retrieves the list of schemas from the Data Lake Analytics catalog. |
| GET | /catalog/usql/databases/{databaseName}/statistics | Retrieves the list of all statistics in a database from the Data Lake Analytics catalog. |
| GET | /catalog/usql/databases/{databaseName}/tables | Retrieves the list of all tables in a database from the Data Lake Analytics catalog. |
| GET | /catalog/usql/databases/{databaseName}/tablevaluedfunctions | Retrieves the list of all table valued functions in a database from the Data Lake Analytics catalog. |
| GET | /catalog/usql/databases/{databaseName}/views | Retrieves the list of all views in a database from the Data Lake Analytics catalog. |
| GET | /catalog/usql/databases/{databaseName}/acl | Retrieves the list of access control list (ACL) entries for the database from the Data Lake Analytics catalog. |
| GET | /catalog/usql/acl | Retrieves the list of access control list (ACL) entries for the Data Lake Analytics catalog. |
| GET | /catalog/usql/databases/{databaseName} | Retrieves the specified database from the Data Lake Analytics catalog. |
| GET | /catalog/usql/databases | Retrieves the list of databases from the Data Lake Analytics catalog. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Update a secret?" -> PUT /catalog/usql/databases/{databaseName}/secrets/{secretName}
- "Get secret details?" -> GET /catalog/usql/databases/{databaseName}/secrets/{secretName}
- "Partially update a secret?" -> PATCH /catalog/usql/databases/{databaseName}/secrets/{secretName}
- "Delete a secret?" -> DELETE /catalog/usql/databases/{databaseName}/secrets/{secretName}
- "Update a credential?" -> PUT /catalog/usql/databases/{databaseName}/credentials/{credentialName}
- "Get credential details?" -> GET /catalog/usql/databases/{databaseName}/credentials/{credentialName}
- "Partially update a credential?" -> PATCH /catalog/usql/databases/{databaseName}/credentials/{credentialName}
- "List all credentials?" -> GET /catalog/usql/databases/{databaseName}/credentials
- "Get externaldatasource details?" -> GET /catalog/usql/databases/{databaseName}/externaldatasources/{externalDataSourceName}
- "List all externaldatasources?" -> GET /catalog/usql/databases/{databaseName}/externaldatasources
- "Get procedure details?" -> GET /catalog/usql/databases/{databaseName}/schemas/{schemaName}/procedures/{procedureName}
- "List all procedures?" -> GET /catalog/usql/databases/{databaseName}/schemas/{schemaName}/procedures
- "Get table details?" -> GET /catalog/usql/databases/{databaseName}/schemas/{schemaName}/tables/{tableName}
- "List all tablefragments?" -> GET /catalog/usql/databases/{databaseName}/schemas/{schemaName}/tables/{tableName}/tablefragments
- "List all tables?" -> GET /catalog/usql/databases/{databaseName}/schemas/{schemaName}/tables
- "List all statistics?" -> GET /catalog/usql/databases/{databaseName}/schemas/{schemaName}/statistics
- "Get tabletype details?" -> GET /catalog/usql/databases/{databaseName}/schemas/{schemaName}/tabletypes/{tableTypeName}
- "List all tabletypes?" -> GET /catalog/usql/databases/{databaseName}/schemas/{schemaName}/tabletypes
- "Get package details?" -> GET /catalog/usql/databases/{databaseName}/schemas/{schemaName}/packages/{packageName}
- "List all packages?" -> GET /catalog/usql/databases/{databaseName}/schemas/{schemaName}/packages
- "Get view details?" -> GET /catalog/usql/databases/{databaseName}/schemas/{schemaName}/views/{viewName}
- "List all views?" -> GET /catalog/usql/databases/{databaseName}/schemas/{schemaName}/views
- "Get statistic details?" -> GET /catalog/usql/databases/{databaseName}/schemas/{schemaName}/tables/{tableName}/statistics/{statisticsName}
- "List all statistics?" -> GET /catalog/usql/databases/{databaseName}/schemas/{schemaName}/tables/{tableName}/statistics
- "List all previewrows?" -> GET /catalog/usql/databases/{databaseName}/schemas/{schemaName}/tables/{tableName}/partitions/{partitionName}/previewrows
- "Get partition details?" -> GET /catalog/usql/databases/{databaseName}/schemas/{schemaName}/tables/{tableName}/partitions/{partitionName}
- "List all previewrows?" -> GET /catalog/usql/databases/{databaseName}/schemas/{schemaName}/tables/{tableName}/previewrows
- "List all partitions?" -> GET /catalog/usql/databases/{databaseName}/schemas/{schemaName}/tables/{tableName}/partitions
- "List all types?" -> GET /catalog/usql/databases/{databaseName}/schemas/{schemaName}/types
- "Get tablevaluedfunction details?" -> GET /catalog/usql/databases/{databaseName}/schemas/{schemaName}/tablevaluedfunctions/{tableValuedFunctionName}
- "List all tablevaluedfunctions?" -> GET /catalog/usql/databases/{databaseName}/schemas/{schemaName}/tablevaluedfunctions
- "Get assembly details?" -> GET /catalog/usql/databases/{databaseName}/assemblies/{assemblyName}
- "List all assemblies?" -> GET /catalog/usql/databases/{databaseName}/assemblies
- "Get schema details?" -> GET /catalog/usql/databases/{databaseName}/schemas/{schemaName}
- "List all schemas?" -> GET /catalog/usql/databases/{databaseName}/schemas
- "List all statistics?" -> GET /catalog/usql/databases/{databaseName}/statistics
- "List all tables?" -> GET /catalog/usql/databases/{databaseName}/tables
- "List all tablevaluedfunctions?" -> GET /catalog/usql/databases/{databaseName}/tablevaluedfunctions
- "List all views?" -> GET /catalog/usql/databases/{databaseName}/views
- "List all acl?" -> GET /catalog/usql/databases/{databaseName}/acl
- "List all acl?" -> GET /catalog/usql/acl
- "Get database details?" -> GET /catalog/usql/databases/{databaseName}
- "List all databases?" -> GET /catalog/usql/databases

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
