---
name: amazon-athena
description: "Amazon Athena API skill. Use when working with Amazon Athena for root. Covers 68 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon Athena
API version: 2017-05-18

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST / -- create first resource

## Endpoints

68 endpoints across 1 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| POST | / | Returns the details of a single named query or a list of up to 50 queries, which you provide as an array of query ID strings. Requires you to have access to the workgroup in which the queries were saved. Use ListNamedQueriesInput to get the list of named query IDs in the specified workgroup. If information could not be retrieved for a submitted query ID, information about the query ID submitted is listed under UnprocessedNamedQueryId. Named queries differ from executed queries. Use BatchGetQueryExecutionInput to get details about each unique query execution, and ListQueryExecutionsInput to get a list of query execution IDs. |
| POST | / | Returns the details of a single prepared statement or a list of up to 256 prepared statements for the array of prepared statement names that you provide. Requires you to have access to the workgroup to which the prepared statements belong. If a prepared statement cannot be retrieved for the name specified, the statement is listed in UnprocessedPreparedStatementNames. |
| POST | / | Returns the details of a single query execution or a list of up to 50 query executions, which you provide as an array of query execution ID strings. Requires you to have access to the workgroup in which the queries ran. To get a list of query execution IDs, use ListQueryExecutionsInput$WorkGroup. Query executions differ from named (saved) queries. Use BatchGetNamedQueryInput to get details about named queries. |
| POST | / | Cancels the capacity reservation with the specified name. Cancelled reservations remain in your account and will be deleted 45 days after cancellation. During the 45 days, you cannot re-purpose or reuse a reservation that has been cancelled, but you can refer to its tags and view it for historical reference. |
| POST | / | Creates a capacity reservation with the specified name and number of requested data processing units. |
| POST | / | Creates (registers) a data catalog with the specified name and properties. Catalogs created are visible to all users of the same Amazon Web Services account. |
| POST | / | Creates a named query in the specified workgroup. Requires that you have access to the workgroup. |
| POST | / | Creates an empty ipynb file in the specified Apache Spark enabled workgroup. Throws an error if a file in the workgroup with the same name already exists. |
| POST | / | Creates a prepared statement for use with SQL queries in Athena. |
| POST | / | Gets an authentication token and the URL at which the notebook can be accessed. During programmatic access, CreatePresignedNotebookUrl must be called every 10 minutes to refresh the authentication token. For information about granting programmatic access, see Grant programmatic access. |
| POST | / | Creates a workgroup with the specified name. A workgroup can be an Apache Spark enabled workgroup or an Athena SQL workgroup. |
| POST | / | Deletes a cancelled capacity reservation. A reservation must be cancelled before it can be deleted. A deleted reservation is immediately removed from your account and can no longer be referenced, including by its ARN. A deleted reservation cannot be called by GetCapacityReservation, and deleted reservations do not appear in the output of ListCapacityReservations. |
| POST | / | Deletes a data catalog. |
| POST | / | Deletes the named query if you have access to the workgroup in which the query was saved. |
| POST | / | Deletes the specified notebook. |
| POST | / | Deletes the prepared statement with the specified name from the specified workgroup. |
| POST | / | Deletes the workgroup with the specified name. The primary workgroup cannot be deleted. |
| POST | / | Exports the specified notebook and its metadata. |
| POST | / | Describes a previously submitted calculation execution. |
| POST | / | Retrieves the unencrypted code that was executed for the calculation. |
| POST | / | Gets the status of a current calculation. |
| POST | / | Gets the capacity assignment configuration for a capacity reservation, if one exists. |
| POST | / | Returns information about the capacity reservation with the specified name. |
| POST | / | Returns the specified data catalog. |
| POST | / | Returns a database object for the specified database and data catalog. |
| POST | / | Returns information about a single query. Requires that you have access to the workgroup in which the query was saved. |
| POST | / | Retrieves notebook metadata for the specified notebook ID. |
| POST | / | Retrieves the prepared statement with the specified name from the specified workgroup. |
| POST | / | Returns information about a single execution of a query if you have access to the workgroup in which the query ran. Each time a query executes, information about the query execution is saved with a unique ID. |
| POST | / | Streams the results of a single query execution specified by QueryExecutionId from the Athena query results location in Amazon S3. For more information, see Working with query results, recent queries, and output files in the Amazon Athena User Guide. This request does not execute the query but returns results. Use StartQueryExecution to run a query. To stream query results successfully, the IAM principal with permission to call GetQueryResults also must have permissions to the Amazon S3 GetObject action for the Athena query results location.  IAM principals with permission to the Amazon S3 GetObject action for the query results location are able to retrieve query results from Amazon S3 even if permission to the GetQueryResults action is denied. To restrict user or role access, ensure that Amazon S3 permissions to the Athena query location are denied. |
| POST | / | Returns query execution runtime statistics related to a single execution of a query if you have access to the workgroup in which the query ran. Statistics from the Timeline section of the response object are available as soon as QueryExecutionStatus$State is in a SUCCEEDED or FAILED state. The remaining non-timeline statistics in the response (like stage-level input and output row count and data size) are updated asynchronously and may not be available immediately after a query completes. The non-timeline statistics are also not included when a query has row-level filters defined in Lake Formation. |
| POST | / | Gets the full details of a previously created session, including the session status and configuration. |
| POST | / | Gets the current status of a session. |
| POST | / | Returns table metadata for the specified catalog, database, and table. |
| POST | / | Returns information about the workgroup with the specified name. |
| POST | / | Imports a single ipynb file to a Spark enabled workgroup. To import the notebook, the request must specify a value for either Payload or NoteBookS3LocationUri. If neither is specified or both are specified, an InvalidRequestException occurs. The maximum file size that can be imported is 10 megabytes. If an ipynb file with the same name already exists in the workgroup, throws an error. |
| POST | / | Returns the supported DPU sizes for the supported application runtimes (for example, Athena notebook version 1). |
| POST | / | Lists the calculations that have been submitted to a session in descending order. Newer calculations are listed first; older calculations are listed later. |
| POST | / | Lists the capacity reservations for the current account. |
| POST | / | Lists the data catalogs in the current Amazon Web Services account.  In the Athena console, data catalogs are listed as "data sources" on the Data sources page under the Data source name column. |
| POST | / | Lists the databases in the specified data catalog. |
| POST | / | Returns a list of engine versions that are available to choose from, including the Auto option. |
| POST | / | Lists, in descending order, the executors that joined a session. Newer executors are listed first; older executors are listed later. The result can be optionally filtered by state. |
| POST | / | Provides a list of available query IDs only for queries saved in the specified workgroup. Requires that you have access to the specified workgroup. If a workgroup is not specified, lists the saved queries for the primary workgroup. |
| POST | / | Displays the notebook files for the specified workgroup in paginated format. |
| POST | / | Lists, in descending order, the sessions that have been created in a notebook that are in an active state like CREATING, CREATED, IDLE or BUSY. Newer sessions are listed first; older sessions are listed later. |
| POST | / | Lists the prepared statements in the specified workgroup. |
| POST | / | Provides a list of available query execution IDs for the queries in the specified workgroup. Athena keeps a query history for 45 days. If a workgroup is not specified, returns a list of query execution IDs for the primary workgroup. Requires you to have access to the workgroup in which the queries ran. |
| POST | / | Lists the sessions in a workgroup that are in an active state like CREATING, CREATED, IDLE, or BUSY. Newer sessions are listed first; older sessions are listed later. |
| POST | / | Lists the metadata for the tables in the specified data catalog database. |
| POST | / | Lists the tags associated with an Athena resource. |
| POST | / | Lists available workgroups for the account. |
| POST | / | Puts a new capacity assignment configuration for a specified capacity reservation. If a capacity assignment configuration already exists for the capacity reservation, replaces the existing capacity assignment configuration. |
| POST | / | Submits calculations for execution within a session. You can supply the code to run as an inline code block within the request.  The request syntax requires the StartCalculationExecutionRequest$CodeBlock parameter or the CalculationConfiguration$CodeBlock parameter, but not both. Because CalculationConfiguration$CodeBlock is deprecated, use the StartCalculationExecutionRequest$CodeBlock parameter instead. |
| POST | / | Runs the SQL query statements contained in the Query. Requires you to have access to the workgroup in which the query ran. Running queries against an external catalog requires GetDataCatalog permission to the catalog. For code samples using the Amazon Web Services SDK for Java, see Examples and Code Samples in the Amazon Athena User Guide. |
| POST | / | Creates a session for running calculations within a workgroup. The session is ready when it reaches an IDLE state. |
| POST | / | Requests the cancellation of a calculation. A StopCalculationExecution call on a calculation that is already in a terminal state (for example, STOPPED, FAILED, or COMPLETED) succeeds but has no effect.  Cancelling a calculation is done on a best effort basis. If a calculation cannot be cancelled, you can be charged for its completion. If you are concerned about being charged for a calculation that cannot be cancelled, consider terminating the session in which the calculation is running. |
| POST | / | Stops a query execution. Requires you to have access to the workgroup in which the query ran. |
| POST | / | Adds one or more tags to an Athena resource. A tag is a label that you assign to a resource. Each tag consists of a key and an optional value, both of which you define. For example, you can use tags to categorize Athena workgroups, data catalogs, or capacity reservations by purpose, owner, or environment. Use a consistent set of tag keys to make it easier to search and filter the resources in your account. For best practices, see Tagging Best Practices. Tag keys can be from 1 to 128 UTF-8 Unicode characters, and tag values can be from 0 to 256 UTF-8 Unicode characters. Tags can use letters and numbers representable in UTF-8, and the following characters: + - = . _ : / @. Tag keys and values are case-sensitive. Tag keys must be unique per resource. If you specify more than one tag, separate them by commas. |
| POST | / | Terminates an active session. A TerminateSession call on a session that is already inactive (for example, in a FAILED, TERMINATED or TERMINATING state) succeeds but has no effect. Calculations running in the session when TerminateSession is called are forcefully stopped, but may display as FAILED instead of STOPPED. |
| POST | / | Removes one or more tags from an Athena resource. |
| POST | / | Updates the number of requested data processing units for the capacity reservation with the specified name. |
| POST | / | Updates the data catalog that has the specified name. |
| POST | / | Updates a NamedQuery object. The database or workgroup cannot be updated. |
| POST | / | Updates the contents of a Spark notebook. |
| POST | / | Updates the metadata for a notebook. |
| POST | / | Updates a prepared statement. |
| POST | / | Updates the workgroup with the specified name. The workgroup's name cannot be changed. Only ConfigurationUpdates can be specified. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
