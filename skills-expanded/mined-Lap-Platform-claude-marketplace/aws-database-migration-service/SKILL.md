---
name: aws-database-migration-service
description: "AWS Database Migration Service API skill. Use when working with AWS Database Migration Service for root. Covers 106 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS Database Migration Service
API version: 2016-01-01

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST / -- create first resource

## Endpoints

106 endpoints across 1 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| POST | / | Adds metadata tags to an DMS resource, including replication instance, endpoint, subnet group, and migration task. These tags can also be used with cost allocation reporting to track cost associated with DMS resources, or used in a Condition statement in an IAM policy for DMS. For more information, see  Tag  data type description. |
| POST | / | Applies a pending maintenance action to a resource (for example, to a replication instance). |
| POST | / | Starts the analysis of up to 20 source databases to recommend target engines for each source database. This is a batch version of StartRecommendations. The result of analysis of each source database is reported individually in the response. Because the batch request can result in a combination of successful and unsuccessful actions, you should check for batch errors even when the call returns an HTTP status code of 200. |
| POST | / | Cancels a single premigration assessment run. This operation prevents any individual assessments from running if they haven't started running. It also attempts to cancel any individual assessments that are currently running. |
| POST | / | Creates a data provider using the provided settings. A data provider stores a data store type and location information about your database. |
| POST | / | Creates an endpoint using the provided settings.  For a MySQL source or target endpoint, don't explicitly specify the database using the DatabaseName request parameter on the CreateEndpoint API call. Specifying DatabaseName when you create a MySQL endpoint replicates all the task tables to this single database. For MySQL endpoints, you specify the database only when you specify the schema in the table-mapping rules of the DMS task. |
| POST | / | Creates an DMS event notification subscription.  You can specify the type of source (SourceType) you want to be notified of, provide a list of DMS source IDs (SourceIds) that triggers the events, and provide a list of event categories (EventCategories) for events you want to be notified of. If you specify both the SourceType and SourceIds, such as SourceType = replication-instance and SourceIdentifier = my-replinstance, you will be notified of all the replication instance events for the specified source. If you specify a SourceType but don't specify a SourceIdentifier, you receive notice of the events for that source type for all your DMS sources. If you don't specify either SourceType nor SourceIdentifier, you will be notified of events generated from all DMS sources belonging to your customer account. For more information about DMS events, see Working with Events and Notifications in the Database Migration Service User Guide. |
| POST | / | Creates a Fleet Advisor collector using the specified parameters. |
| POST | / | Creates the instance profile using the specified parameters. |
| POST | / | Creates the migration project using the specified parameters. You can run this action only after you create an instance profile and data providers using CreateInstanceProfile and CreateDataProvider. |
| POST | / | Creates a configuration that you can later provide to configure and start an DMS Serverless replication. You can also provide options to validate the configuration inputs before you start the replication. |
| POST | / | Creates the replication instance using the specified parameters. DMS requires that your account have certain roles with appropriate permissions before you can create a replication instance. For information on the required roles, see Creating the IAM Roles to Use With the CLI and DMS API. For information on the required permissions, see IAM Permissions Needed to Use DMS.  If you don't specify a version when creating a replication instance, DMS will create the instance using the default engine version. For information about the default engine version, see Release Notes. |
| POST | / | Creates a replication subnet group given a list of the subnet IDs in a VPC. The VPC needs to have at least one subnet in at least two availability zones in the Amazon Web Services Region, otherwise the service will throw a ReplicationSubnetGroupDoesNotCoverEnoughAZs exception. If a replication subnet group exists in your Amazon Web Services account, the CreateReplicationSubnetGroup action returns the following error message: The Replication Subnet Group already exists. In this case, delete the existing replication subnet group. To do so, use the DeleteReplicationSubnetGroup action. Optionally, choose Subnet groups in the DMS console, then choose your subnet group. Next, choose Delete from Actions. |
| POST | / | Creates a replication task using the specified parameters. |
| POST | / | Deletes the specified certificate. |
| POST | / | Deletes the connection between a replication instance and an endpoint. |
| POST | / | Deletes the specified data provider.  All migration projects associated with the data provider must be deleted or modified before you can delete the data provider. |
| POST | / | Deletes the specified endpoint.  All tasks associated with the endpoint must be deleted before you can delete the endpoint. |
| POST | / | Deletes an DMS event subscription. |
| POST | / | Deletes the specified Fleet Advisor collector. |
| POST | / | Deletes the specified Fleet Advisor collector databases. |
| POST | / | Deletes the specified instance profile.  All migration projects associated with the instance profile must be deleted or modified before you can delete the instance profile. |
| POST | / | Deletes the specified migration project.  The migration project must be closed before you can delete it. |
| POST | / | Deletes an DMS Serverless replication configuration. This effectively deprovisions any and all replications that use this configuration. You can't delete the configuration for an DMS Serverless replication that is ongoing. You can delete the configuration when the replication is in a non-RUNNING and non-STARTING state. |
| POST | / | Deletes the specified replication instance.  You must delete any migration tasks that are associated with the replication instance before you can delete it. |
| POST | / | Deletes a subnet group. |
| POST | / | Deletes the specified replication task. |
| POST | / | Deletes the record of a single premigration assessment run. This operation removes all metadata that DMS maintains about this assessment run. However, the operation leaves untouched all information about this assessment run that is stored in your Amazon S3 bucket. |
| POST | / | Lists all of the DMS attributes for a customer account. These attributes include DMS quotas for the account and a unique account identifier in a particular DMS region. DMS quotas include a list of resource quotas supported by the account, such as the number of replication instances allowed. The description for each resource quota, includes the quota name, current usage toward that quota, and the quota's maximum value. DMS uses the unique account identifier to name each artifact used by DMS in the given region. This command does not take any parameters. |
| POST | / | Provides a list of individual assessments that you can specify for a new premigration assessment run, given one or more parameters. If you specify an existing migration task, this operation provides the default individual assessments you can specify for that task. Otherwise, the specified parameters model elements of a possible migration task on which to base a premigration assessment run. To use these migration task modeling parameters, you must specify an existing replication instance, a source database engine, a target database engine, and a migration type. This combination of parameters potentially limits the default individual assessments available for an assessment run created for a corresponding migration task. If you specify no parameters, this operation provides a list of all possible individual assessments that you can specify for an assessment run. If you specify any one of the task modeling parameters, you must specify all of them or the operation cannot provide a list of individual assessments. The only parameter that you can specify alone is for an existing migration task. The specified task definition then determines the default list of individual assessments that you can specify in an assessment run for the task. |
| POST | / | Provides a description of the certificate. |
| POST | / | Describes the status of the connections that have been made between the replication instance and an endpoint. Connections are created when you test an endpoint. |
| POST | / | Returns configuration parameters for a schema conversion project. |
| POST | / | Returns a paginated list of data providers for your account in the current region. |
| POST | / | Returns information about the possible endpoint settings available when you create an endpoint for a specific database engine. |
| POST | / | Returns information about the type of endpoints available. |
| POST | / | Returns information about the endpoints for your account in the current region. |
| POST | / | Returns information about the replication instance versions used in the project. |
| POST | / | Lists categories for all event source types, or, if specified, for a specified source type. You can see a list of the event categories and source types in Working with Events and Notifications in the Database Migration Service User Guide. |
| POST | / | Lists all the event subscriptions for a customer account. The description of a subscription includes SubscriptionName, SNSTopicARN, CustomerID, SourceType, SourceID, CreationTime, and Status.  If you specify SubscriptionName, this action lists the description for that subscription. |
| POST | / | Lists events for a given source identifier and source type. You can also specify a start and end time. For more information on DMS events, see Working with Events and Notifications in the Database Migration Service User Guide. |
| POST | / | Returns a paginated list of extension pack associations for the specified migration project. An extension pack is an add-on module that emulates functions present in a source database that are required when converting objects to the target database. |
| POST | / | Returns a list of the Fleet Advisor collectors in your account. |
| POST | / | Returns a list of Fleet Advisor databases in your account. |
| POST | / | Provides descriptions of large-scale assessment (LSA) analyses produced by your Fleet Advisor collectors. |
| POST | / | Provides descriptions of the schemas discovered by your Fleet Advisor collectors. |
| POST | / | Returns a list of schemas detected by Fleet Advisor Collectors in your account. |
| POST | / | Returns a paginated list of instance profiles for your account in the current region. |
| POST | / | Returns a paginated list of metadata model assessments for your account in the current region. |
| POST | / | Returns a paginated list of metadata model conversions for a migration project. |
| POST | / | Returns a paginated list of metadata model exports. |
| POST | / | Returns a paginated list of metadata model exports. |
| POST | / | Returns a paginated list of metadata model imports. |
| POST | / | Returns a paginated list of migration projects for your account in the current region. |
| POST | / | Returns information about the replication instance types that can be created in the specified region. |
| POST | / | For internal use only |
| POST | / | Returns a paginated list of limitations for recommendations of target Amazon Web Services engines. |
| POST | / | Returns a paginated list of target engine recommendations for your source databases. |
| POST | / | Returns the status of the RefreshSchemas operation. |
| POST | / | Returns one or more existing DMS Serverless replication configurations as a list of structures. |
| POST | / | Returns information about the task logs for the specified task. |
| POST | / | Returns information about replication instances for your account in the current region. |
| POST | / | Returns information about the replication subnet groups. |
| POST | / | Returns table and schema statistics for one or more provisioned replications that use a given DMS Serverless replication configuration. |
| POST | / | Returns the task assessment results from the Amazon S3 bucket that DMS creates in your Amazon Web Services account. This action always returns the latest results. For more information about DMS task assessments, see Creating a task assessment report in the Database Migration Service User Guide. |
| POST | / | Returns a paginated list of premigration assessment runs based on filter settings. These filter settings can specify a combination of premigration assessment runs, migration tasks, replication instances, and assessment run status values.  This operation doesn't return information about individual assessments. For this information, see the DescribeReplicationTaskIndividualAssessments operation. |
| POST | / | Returns a paginated list of individual assessments based on filter settings. These filter settings can specify a combination of premigration assessment runs, migration tasks, and assessment status values. |
| POST | / | Returns information about replication tasks for your account in the current region. |
| POST | / | Provides details on replication progress by returning status information for one or more provisioned DMS Serverless replications. |
| POST | / | Returns information about the schema for the specified endpoint. |
| POST | / | Returns table statistics on the database migration task, including table name, rows inserted, rows updated, and rows deleted. Note that the "last updated" column the DMS console only indicates the time that DMS last updated the table statistics record for a table. It does not indicate the time of the last update to the table. |
| POST | / | Saves a copy of a database migration assessment report to your Amazon S3 bucket. DMS can save your assessment report as a comma-separated value (CSV) or a PDF file. |
| POST | / | Uploads the specified certificate. |
| POST | / | Lists all metadata tags attached to an DMS resource, including replication instance, endpoint, subnet group, and migration task. For more information, see  Tag  data type description. |
| POST | / | Modifies the specified schema conversion configuration using the provided parameters. |
| POST | / | Modifies the specified data provider using the provided settings.  You must remove the data provider from all migration projects before you can modify it. |
| POST | / | Modifies the specified endpoint.  For a MySQL source or target endpoint, don't explicitly specify the database using the DatabaseName request parameter on the ModifyEndpoint API call. Specifying DatabaseName when you modify a MySQL endpoint replicates all the task tables to this single database. For MySQL endpoints, you specify the database only when you specify the schema in the table-mapping rules of the DMS task. |
| POST | / | Modifies an existing DMS event notification subscription. |
| POST | / | Modifies the specified instance profile using the provided parameters.  All migration projects associated with the instance profile must be deleted or modified before you can modify the instance profile. |
| POST | / | Modifies the specified migration project using the provided parameters.  The migration project must be closed before you can modify it. |
| POST | / | Modifies an existing DMS Serverless replication configuration that you can use to start a replication. This command includes input validation and logic to check the state of any replication that uses this configuration. You can only modify a replication configuration before any replication that uses it has started. As soon as you have initially started a replication with a given configuiration, you can't modify that configuration, even if you stop it. Other run statuses that allow you to run this command include FAILED and CREATED. A provisioning state that allows you to run this command is FAILED_PROVISION. |
| POST | / | Modifies the replication instance to apply new settings. You can change one or more parameters by specifying these parameters and the new values in the request. Some settings are applied during the maintenance window. |
| POST | / | Modifies the settings for the specified replication subnet group. |
| POST | / | Modifies the specified replication task. You can't modify the task endpoints. The task must be stopped before you can modify it.  For more information about DMS tasks, see Working with Migration Tasks in the Database Migration Service User Guide. |
| POST | / | Moves a replication task from its current replication instance to a different target replication instance using the specified parameters. The target replication instance must be created with the same or later DMS version as the current replication instance. |
| POST | / | Reboots a replication instance. Rebooting results in a momentary outage, until the replication instance becomes available again. |
| POST | / | Populates the schema for the specified endpoint. This is an asynchronous operation and can take several minutes. You can check the status of this operation by calling the DescribeRefreshSchemasStatus operation. |
| POST | / | Reloads the target database table with the source data for a given DMS Serverless replication configuration. You can only use this operation with a task in the RUNNING state, otherwise the service will throw an InvalidResourceStateFault exception. |
| POST | / | Reloads the target database table with the source data.  You can only use this operation with a task in the RUNNING state, otherwise the service will throw an InvalidResourceStateFault exception. |
| POST | / | Removes metadata tags from an DMS resource, including replication instance, endpoint, subnet group, and migration task. For more information, see  Tag  data type description. |
| POST | / | Runs large-scale assessment (LSA) analysis on every Fleet Advisor collector in your account. |
| POST | / | Applies the extension pack to your target database. An extension pack is an add-on module that emulates functions present in a source database that are required when converting objects to the target database. |
| POST | / | Creates a database migration assessment report by assessing the migration complexity for your source database. A database migration assessment report summarizes all of the schema conversion tasks. It also details the action items for database objects that can't be converted to the database engine of your target database instance. |
| POST | / | Converts your source database objects to a format compatible with the target database. |
| POST | / | Saves your converted code to a file as a SQL script, and stores this file on your Amazon S3 bucket. |
| POST | / | Applies converted database objects to your target database. |
| POST | / | Loads the metadata for all the dependent database objects of the parent object. This operation uses your project's Amazon S3 bucket as a metadata cache to improve performance. |
| POST | / | Starts the analysis of your source database to provide recommendations of target engines. You can create recommendations for multiple source databases using BatchStartRecommendations. |
| POST | / | For a given DMS Serverless replication configuration, DMS connects to the source endpoint and collects the metadata to analyze the replication workload. Using this metadata, DMS then computes and provisions the required capacity and starts replicating to the target endpoint using the server resources that DMS has provisioned for the DMS Serverless replication. |
| POST | / | Starts the replication task. For more information about DMS tasks, see Working with Migration Tasks  in the Database Migration Service User Guide. |
| POST | / | Starts the replication task assessment for unsupported data types in the source database.  You can only use this operation for a task if the following conditions are true:   The task must be in the stopped state.   The task must have successful connections to the source and target.   If either of these conditions are not met, an InvalidResourceStateFault error will result.  For information about DMS task assessments, see Creating a task assessment report in the Database Migration Service User Guide. |
| POST | / | Starts a new premigration assessment run for one or more individual assessments of a migration task. The assessments that you can specify depend on the source and target database engine and the migration type defined for the given task. To run this operation, your migration task must already be created. After you run this operation, you can review the status of each individual assessment. You can also run the migration task manually after the assessment run and its individual assessments complete. |
| POST | / | For a given DMS Serverless replication configuration, DMS stops any and all ongoing DMS Serverless replications. This command doesn't deprovision the stopped replications. |
| POST | / | Stops the replication task. |
| POST | / | Tests the connection between the replication instance and the endpoint. |
| POST | / | Migrates 10 active and enabled Amazon SNS subscriptions at a time and converts them to corresponding Amazon EventBridge rules. By default, this operation migrates subscriptions only when all your replication instance versions are 3.4.5 or higher. If any replication instances are from versions earlier than 3.4.5, the operation raises an error and tells you to upgrade these instances to version 3.4.5 or higher. To enable migration regardless of version, set the Force option to true. However, if you don't upgrade instances earlier than version 3.4.5, some types of events might not be available when you use Amazon EventBridge. To call this operation, make sure that you have certain permissions added to your user account. For more information, see Migrating event subscriptions to Amazon EventBridge in the Amazon Web Services Database Migration Service User Guide. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
