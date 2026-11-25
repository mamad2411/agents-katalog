---
name: aws-rds-dataservice
description: "AWS RDS DataService API skill. Use when working with AWS RDS DataService for BatchExecute, BeginTransaction, CommitTransaction. Covers 6 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS RDS DataService
API version: 2018-08-01

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST /BatchExecute -- create first BatchExecute

## Endpoints

6 endpoints across 6 groups. See references/api-spec.lap for full details.

### BatchExecute
| Method | Path | Description |
|--------|------|-------------|
| POST | /BatchExecute | Runs a batch SQL statement over an array of data. You can run bulk update and insert operations for multiple records using a DML statement with different parameter sets. Bulk operations can provide a significant performance improvement over individual insert and update operations.  If a call isn't part of a transaction because it doesn't include the transactionID parameter, changes that result from the call are committed automatically. There isn't a fixed upper limit on the number of parameter sets. However, the maximum size of the HTTP request submitted through the Data API is 4 MiB. If the request exceeds this limit, the Data API returns an error and doesn't process the request. This 4-MiB limit includes the size of the HTTP headers and the JSON notation in the request. Thus, the number of parameter sets that you can include depends on a combination of factors, such as the size of the SQL statement and the size of each parameter set. The response size limit is 1 MiB. If the call returns more than 1 MiB of response data, the call is terminated. |

### BeginTransaction
| Method | Path | Description |
|--------|------|-------------|
| POST | /BeginTransaction | Starts a SQL transaction.  A transaction can run for a maximum of 24 hours. A transaction is terminated and rolled back automatically after 24 hours. A transaction times out if no calls use its transaction ID in three minutes. If a transaction times out before it's committed, it's rolled back automatically. DDL statements inside a transaction cause an implicit commit. We recommend that you run each DDL statement in a separate ExecuteStatement call with continueAfterTimeout enabled. |

### CommitTransaction
| Method | Path | Description |
|--------|------|-------------|
| POST | /CommitTransaction | Ends a SQL transaction started with the BeginTransaction operation and commits the changes. |

### ExecuteSql
| Method | Path | Description |
|--------|------|-------------|
| POST | /ExecuteSql | Runs one or more SQL statements.  This operation isn't supported for Aurora PostgreSQL Serverless v2 and provisioned DB clusters, and for Aurora Serverless v1 DB clusters, the operation is deprecated. Use the BatchExecuteStatement or ExecuteStatement operation. |

### Execute
| Method | Path | Description |
|--------|------|-------------|
| POST | /Execute | Runs a SQL statement against a database.  If a call isn't part of a transaction because it doesn't include the transactionID parameter, changes that result from the call are committed automatically. If the binary response data from the database is more than 1 MB, the call is terminated. |

### RollbackTransaction
| Method | Path | Description |
|--------|------|-------------|
| POST | /RollbackTransaction | Performs a rollback of a transaction. Rolling back a transaction cancels its changes. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a BatchExecute?" -> POST /BatchExecute
- "Create a BeginTransaction?" -> POST /BeginTransaction
- "Create a CommitTransaction?" -> POST /CommitTransaction
- "Create a ExecuteSql?" -> POST /ExecuteSql
- "Create a Execute?" -> POST /Execute
- "Create a RollbackTransaction?" -> POST /RollbackTransaction
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
