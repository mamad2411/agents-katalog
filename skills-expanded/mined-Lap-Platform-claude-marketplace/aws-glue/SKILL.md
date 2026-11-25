---
name: aws-glue
description: "AWS Glue API skill. Use when working with AWS Glue for root. Covers 224 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS Glue
API version: 2017-03-31

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST / -- create first resource

## Endpoints

224 endpoints across 1 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| POST | / | Creates one or more partitions in a batch operation. |
| POST | / | Deletes a list of connection definitions from the Data Catalog. |
| POST | / | Deletes one or more partitions in a batch operation. |
| POST | / | Deletes multiple tables at once.  After completing this operation, you no longer have access to the table versions and partitions that belong to the deleted table. Glue deletes these "orphaned" resources asynchronously in a timely manner, at the discretion of the service. To ensure the immediate deletion of all related resources, before calling BatchDeleteTable, use DeleteTableVersion or BatchDeleteTableVersion, and DeletePartition or BatchDeletePartition, to delete any resources that belong to the table. |
| POST | / | Deletes a specified batch of versions of a table. |
| POST | / | Retrieves information about a list of blueprints. |
| POST | / | Returns a list of resource metadata for a given list of crawler names. After calling the ListCrawlers operation, you can call this operation to access the data to which you have been granted permissions. This operation supports all IAM permissions, including permission conditions that uses tags. |
| POST | / | Retrieves the details for the custom patterns specified by a list of names. |
| POST | / | Retrieves a list of data quality results for the specified result IDs. |
| POST | / | Returns a list of resource metadata for a given list of development endpoint names. After calling the ListDevEndpoints operation, you can call this operation to access the data to which you have been granted permissions. This operation supports all IAM permissions, including permission conditions that uses tags. |
| POST | / | Returns a list of resource metadata for a given list of job names. After calling the ListJobs operation, you can call this operation to access the data to which you have been granted permissions. This operation supports all IAM permissions, including permission conditions that uses tags. |
| POST | / | Retrieves partitions in a batch request. |
| POST | / | Returns the configuration for the specified table optimizers. |
| POST | / | Returns a list of resource metadata for a given list of trigger names. After calling the ListTriggers operation, you can call this operation to access the data to which you have been granted permissions. This operation supports all IAM permissions, including permission conditions that uses tags. |
| POST | / | Returns a list of resource metadata for a given list of workflow names. After calling the ListWorkflows operation, you can call this operation to access the data to which you have been granted permissions. This operation supports all IAM permissions, including permission conditions that uses tags. |
| POST | / | Annotate datapoints over time for a specific data quality statistic. |
| POST | / | Stops one or more job runs for a specified job definition. |
| POST | / | Updates one or more partitions in a batch operation. |
| POST | / | Cancels the specified recommendation run that was being used to generate rules. |
| POST | / | Cancels a run where a ruleset is being evaluated against a data source. |
| POST | / | Cancels (stops) a task run. Machine learning task runs are asynchronous tasks that Glue runs on your behalf as part of various machine learning workflows. You can cancel a machine learning task run at any time by calling CancelMLTaskRun with a task run's parent transform's TransformID and the task run's TaskRunId. |
| POST | / | Cancels the statement. |
| POST | / | Validates the supplied schema. This call has no side effects, it simply validates using the supplied schema using DataFormat as the format. Since it does not take a schema set name, no compatibility checks are performed. |
| POST | / | Registers a blueprint with Glue. |
| POST | / | Creates a classifier in the user's account. This can be a GrokClassifier, an XMLClassifier, a JsonClassifier, or a CsvClassifier, depending on which field of the request is present. |
| POST | / | Creates a connection definition in the Data Catalog. Connections used for creating federated resources require the IAM glue:PassConnection permission. |
| POST | / | Creates a new crawler with specified targets, role, configuration, and optional schedule. At least one crawl target must be specified, in the s3Targets field, the jdbcTargets field, or the DynamoDBTargets field. |
| POST | / | Creates a custom pattern that is used to detect sensitive data across the columns and rows of your structured data. Each custom pattern you create specifies a regular expression and an optional list of context words. If no context words are passed only a regular expression is checked. |
| POST | / | Creates a data quality ruleset with DQDL rules applied to a specified Glue table. You create the ruleset using the Data Quality Definition Language (DQDL). For more information, see the Glue developer guide. |
| POST | / | Creates a new database in a Data Catalog. |
| POST | / | Creates a new development endpoint. |
| POST | / | Creates a new job definition. |
| POST | / | Creates an Glue machine learning transform. This operation creates the transform and all the necessary parameters to train it. Call this operation as the first step in the process of using a machine learning transform (such as the FindMatches transform) for deduplicating data. You can provide an optional Description, in addition to the parameters that you want to use for your algorithm. You must also specify certain parameters for the tasks that Glue runs on your behalf as part of learning from your data and creating a high-quality machine learning transform. These parameters include Role, and optionally, AllocatedCapacity, Timeout, and MaxRetries. For more information, see Jobs. |
| POST | / | Creates a new partition. |
| POST | / | Creates a specified partition index in an existing table. |
| POST | / | Creates a new registry which may be used to hold a collection of schemas. |
| POST | / | Creates a new schema set and registers the schema definition. Returns an error if the schema set already exists without actually registering the version. When the schema set is created, a version checkpoint will be set to the first version. Compatibility mode "DISABLED" restricts any additional schema versions from being added after the first schema version. For all other compatibility modes, validation of compatibility settings will be applied only from the second version onwards when the RegisterSchemaVersion API is used. When this API is called without a RegistryId, this will create an entry for a "default-registry" in the registry database tables, if it is not already present. |
| POST | / | Transforms a directed acyclic graph (DAG) into code. |
| POST | / | Creates a new security configuration. A security configuration is a set of security properties that can be used by Glue. You can use a security configuration to encrypt data at rest. For information about using security configurations in Glue, see Encrypting Data Written by Crawlers, Jobs, and Development Endpoints. |
| POST | / | Creates a new session. |
| POST | / | Creates a new table definition in the Data Catalog. |
| POST | / | Creates a new table optimizer for a specific function. compaction is the only currently supported optimizer type. |
| POST | / | Creates a new trigger. |
| POST | / | Creates an Glue usage profile. |
| POST | / | Creates a new function definition in the Data Catalog. |
| POST | / | Creates a new workflow. |
| POST | / | Deletes an existing blueprint. |
| POST | / | Removes a classifier from the Data Catalog. |
| POST | / | Delete the partition column statistics of a column. The Identity and Access Management (IAM) permission required for this operation is DeletePartition. |
| POST | / | Retrieves table statistics of columns. The Identity and Access Management (IAM) permission required for this operation is DeleteTable. |
| POST | / | Deletes a connection from the Data Catalog. |
| POST | / | Removes a specified crawler from the Glue Data Catalog, unless the crawler state is RUNNING. |
| POST | / | Deletes a custom pattern by specifying its name. |
| POST | / | Deletes a data quality ruleset. |
| POST | / | Removes a specified database from a Data Catalog.  After completing this operation, you no longer have access to the tables (and all table versions and partitions that might belong to the tables) and the user-defined functions in the deleted database. Glue deletes these "orphaned" resources asynchronously in a timely manner, at the discretion of the service. To ensure the immediate deletion of all related resources, before calling DeleteDatabase, use DeleteTableVersion or BatchDeleteTableVersion, DeletePartition or BatchDeletePartition, DeleteUserDefinedFunction, and DeleteTable or BatchDeleteTable, to delete any resources that belong to the database. |
| POST | / | Deletes a specified development endpoint. |
| POST | / | Deletes a specified job definition. If the job definition is not found, no exception is thrown. |
| POST | / | Deletes an Glue machine learning transform. Machine learning transforms are a special type of transform that use machine learning to learn the details of the transformation to be performed by learning from examples provided by humans. These transformations are then saved by Glue. If you no longer need a transform, you can delete it by calling DeleteMLTransforms. However, any Glue jobs that still reference the deleted transform will no longer succeed. |
| POST | / | Deletes a specified partition. |
| POST | / | Deletes a specified partition index from an existing table. |
| POST | / | Delete the entire registry including schema and all of its versions. To get the status of the delete operation, you can call the GetRegistry API after the asynchronous call. Deleting a registry will deactivate all online operations for the registry such as the UpdateRegistry, CreateSchema, UpdateSchema, and RegisterSchemaVersion APIs. |
| POST | / | Deletes a specified policy. |
| POST | / | Deletes the entire schema set, including the schema set and all of its versions. To get the status of the delete operation, you can call GetSchema API after the asynchronous call. Deleting a registry will deactivate all online operations for the schema, such as the GetSchemaByDefinition, and RegisterSchemaVersion APIs. |
| POST | / | Remove versions from the specified schema. A version number or range may be supplied. If the compatibility mode forbids deleting of a version that is necessary, such as BACKWARDS_FULL, an error is returned. Calling the GetSchemaVersions API after this call will list the status of the deleted versions. When the range of version numbers contain check pointed version, the API will return a 409 conflict and will not proceed with the deletion. You have to remove the checkpoint first using the DeleteSchemaCheckpoint API before using this API. You cannot use the DeleteSchemaVersions API to delete the first schema version in the schema set. The first schema version can only be deleted by the DeleteSchema API. This operation will also delete the attached SchemaVersionMetadata under the schema versions. Hard deletes will be enforced on the database. If the compatibility mode forbids deleting of a version that is necessary, such as BACKWARDS_FULL, an error is returned. |
| POST | / | Deletes a specified security configuration. |
| POST | / | Deletes the session. |
| POST | / | Removes a table definition from the Data Catalog.  After completing this operation, you no longer have access to the table versions and partitions that belong to the deleted table. Glue deletes these "orphaned" resources asynchronously in a timely manner, at the discretion of the service. To ensure the immediate deletion of all related resources, before calling DeleteTable, use DeleteTableVersion or BatchDeleteTableVersion, and DeletePartition or BatchDeletePartition, to delete any resources that belong to the table. |
| POST | / | Deletes an optimizer and all associated metadata for a table. The optimization will no longer be performed on the table. |
| POST | / | Deletes a specified version of a table. |
| POST | / | Deletes a specified trigger. If the trigger is not found, no exception is thrown. |
| POST | / | Deletes the Glue specified usage profile. |
| POST | / | Deletes an existing function definition from the Data Catalog. |
| POST | / | Deletes a workflow. |
| POST | / | Retrieves the details of a blueprint. |
| POST | / | Retrieves the details of a blueprint run. |
| POST | / | Retrieves the details of blueprint runs for a specified blueprint. |
| POST | / | Retrieves the status of a migration operation. |
| POST | / | Retrieve a classifier by name. |
| POST | / | Lists all classifier objects in the Data Catalog. |
| POST | / | Retrieves partition statistics of columns. The Identity and Access Management (IAM) permission required for this operation is GetPartition. |
| POST | / | Retrieves table statistics of columns. The Identity and Access Management (IAM) permission required for this operation is GetTable. |
| POST | / | Get the associated metadata/information for a task run, given a task run ID. |
| POST | / | Retrieves information about all runs associated with the specified table. |
| POST | / | Retrieves a connection definition from the Data Catalog. |
| POST | / | Retrieves a list of connection definitions from the Data Catalog. |
| POST | / | Retrieves metadata for a specified crawler. |
| POST | / | Retrieves metrics about specified crawlers. |
| POST | / | Retrieves metadata for all crawlers defined in the customer account. |
| POST | / | Retrieves the details of a custom pattern by specifying its name. |
| POST | / | Retrieves the security configuration for a specified catalog. |
| POST | / | Retrieve the training status of the model along with more information (CompletedOn, StartedOn, FailureReason). |
| POST | / | Retrieve a statistic's predictions for a given Profile ID. |
| POST | / | Retrieves the result of a data quality rule evaluation. |
| POST | / | Gets the specified recommendation run that was used to generate rules. |
| POST | / | Returns an existing ruleset by identifier or name. |
| POST | / | Retrieves a specific run where a ruleset is evaluated against a data source. |
| POST | / | Retrieves the definition of a specified database. |
| POST | / | Retrieves all databases defined in a given Data Catalog. |
| POST | / | Transforms a Python script into a directed acyclic graph (DAG). |
| POST | / | Retrieves information about a specified development endpoint.  When you create a development endpoint in a virtual private cloud (VPC), Glue returns only a private IP address, and the public IP address field is not populated. When you create a non-VPC development endpoint, Glue returns only a public IP address. |
| POST | / | Retrieves all the development endpoints in this Amazon Web Services account.  When you create a development endpoint in a virtual private cloud (VPC), Glue returns only a private IP address and the public IP address field is not populated. When you create a non-VPC development endpoint, Glue returns only a public IP address. |
| POST | / | Retrieves an existing job definition. |
| POST | / | Returns information on a job bookmark entry. For more information about enabling and using job bookmarks, see:    Tracking processed data using job bookmarks     Job parameters used by Glue     Job structure |
| POST | / | Retrieves the metadata for a given job run. Job run history is accessible for 90 days for your workflow and job run. |
| POST | / | Retrieves metadata for all runs of a given job definition. |
| POST | / | Retrieves all current job definitions. |
| POST | / | Gets details for a specific task run on a machine learning transform. Machine learning task runs are asynchronous tasks that Glue runs on your behalf as part of various machine learning workflows. You can check the stats of any task run by calling GetMLTaskRun with the TaskRunID and its parent transform's TransformID. |
| POST | / | Gets a list of runs for a machine learning transform. Machine learning task runs are asynchronous tasks that Glue runs on your behalf as part of various machine learning workflows. You can get a sortable, filterable list of machine learning task runs by calling GetMLTaskRuns with their parent transform's TransformID and other optional parameters as documented in this section. This operation returns a list of historic runs and must be paginated. |
| POST | / | Gets an Glue machine learning transform artifact and all its corresponding metadata. Machine learning transforms are a special type of transform that use machine learning to learn the details of the transformation to be performed by learning from examples provided by humans. These transformations are then saved by Glue. You can retrieve their metadata by calling GetMLTransform. |
| POST | / | Gets a sortable, filterable list of existing Glue machine learning transforms. Machine learning transforms are a special type of transform that use machine learning to learn the details of the transformation to be performed by learning from examples provided by humans. These transformations are then saved by Glue, and you can retrieve their metadata by calling GetMLTransforms. |
| POST | / | Creates mappings. |
| POST | / | Retrieves information about a specified partition. |
| POST | / | Retrieves the partition indexes associated with a table. |
| POST | / | Retrieves information about the partitions in a table. |
| POST | / | Gets code to perform a specified mapping. |
| POST | / | Describes the specified registry in detail. |
| POST | / | Retrieves the resource policies set on individual resources by Resource Access Manager during cross-account permission grants. Also retrieves the Data Catalog resource policy. If you enabled metadata encryption in Data Catalog settings, and you do not have permission on the KMS key, the operation can't return the Data Catalog resource policy. |
| POST | / | Retrieves a specified resource policy. |
| POST | / | Describes the specified schema in detail. |
| POST | / | Retrieves a schema by the SchemaDefinition. The schema definition is sent to the Schema Registry, canonicalized, and hashed. If the hash is matched within the scope of the SchemaName or ARN (or the default registry, if none is supplied), that schema’s metadata is returned. Otherwise, a 404 or NotFound error is returned. Schema versions in Deleted statuses will not be included in the results. |
| POST | / | Get the specified schema by its unique ID assigned when a version of the schema is created or registered. Schema versions in Deleted status will not be included in the results. |
| POST | / | Fetches the schema version difference in the specified difference type between two stored schema versions in the Schema Registry. This API allows you to compare two schema versions between two schema definitions under the same schema. |
| POST | / | Retrieves a specified security configuration. |
| POST | / | Retrieves a list of all security configurations. |
| POST | / | Retrieves the session. |
| POST | / | Retrieves the statement. |
| POST | / | Retrieves the Table definition in a Data Catalog for a specified table. |
| POST | / | Returns the configuration of all optimizers associated with a specified table. |
| POST | / | Retrieves a specified version of a table. |
| POST | / | Retrieves a list of strings that identify available versions of a specified table. |
| POST | / | Retrieves the definitions of some or all of the tables in a given Database. |
| POST | / | Retrieves a list of tags associated with a resource. |
| POST | / | Retrieves the definition of a trigger. |
| POST | / | Gets all the triggers associated with a job. |
| POST | / | Retrieves partition metadata from the Data Catalog that contains unfiltered metadata. For IAM authorization, the public IAM action associated with this API is glue:GetPartition. |
| POST | / | Retrieves partition metadata from the Data Catalog that contains unfiltered metadata. For IAM authorization, the public IAM action associated with this API is glue:GetPartitions. |
| POST | / | Allows a third-party analytical engine to retrieve unfiltered table metadata from the Data Catalog. For IAM authorization, the public IAM action associated with this API is glue:GetTable. |
| POST | / | Retrieves information about the specified Glue usage profile. |
| POST | / | Retrieves a specified function definition from the Data Catalog. |
| POST | / | Retrieves multiple function definitions from the Data Catalog. |
| POST | / | Retrieves resource metadata for a workflow. |
| POST | / | Retrieves the metadata for a given workflow run. Job run history is accessible for 90 days for your workflow and job run. |
| POST | / | Retrieves the workflow run properties which were set during the run. |
| POST | / | Retrieves metadata for all runs of a given workflow. |
| POST | / | Imports an existing Amazon Athena Data Catalog to Glue. |
| POST | / | Lists all the blueprint names in an account. |
| POST | / | List all task runs for a particular account. |
| POST | / | Retrieves the names of all crawler resources in this Amazon Web Services account, or the resources with the specified tag. This operation allows you to see which resources are available in your account, and their names. This operation takes the optional Tags field, which you can use as a filter on the response so that tagged resources can be retrieved as a group. If you choose to use tags filtering, only resources with the tag are retrieved. |
| POST | / | Returns all the crawls of a specified crawler. Returns only the crawls that have occurred since the launch date of the crawler history feature, and only retains up to 12 months of crawls. Older crawls will not be returned. You may use this API to:   Retrive all the crawls of a specified crawler.   Retrieve all the crawls of a specified crawler within a limited count.   Retrieve all the crawls of a specified crawler in a specific time range.   Retrieve all the crawls of a specified crawler with a particular state, crawl ID, or DPU hour value. |
| POST | / | Lists all the custom patterns that have been created. |
| POST | / | Returns all data quality execution results for your account. |
| POST | / | Lists the recommendation runs meeting the filter criteria. |
| POST | / | Lists all the runs meeting the filter criteria, where a ruleset is evaluated against a data source. |
| POST | / | Returns a paginated list of rulesets for the specified list of Glue tables. |
| POST | / | Retrieve annotations for a data quality statistic. |
| POST | / | Retrieves a list of data quality statistics. |
| POST | / | Retrieves the names of all DevEndpoint resources in this Amazon Web Services account, or the resources with the specified tag. This operation allows you to see which resources are available in your account, and their names. This operation takes the optional Tags field, which you can use as a filter on the response so that tagged resources can be retrieved as a group. If you choose to use tags filtering, only resources with the tag are retrieved. |
| POST | / | Retrieves the names of all job resources in this Amazon Web Services account, or the resources with the specified tag. This operation allows you to see which resources are available in your account, and their names. This operation takes the optional Tags field, which you can use as a filter on the response so that tagged resources can be retrieved as a group. If you choose to use tags filtering, only resources with the tag are retrieved. |
| POST | / | Retrieves a sortable, filterable list of existing Glue machine learning transforms in this Amazon Web Services account, or the resources with the specified tag. This operation takes the optional Tags field, which you can use as a filter of the responses so that tagged resources can be retrieved as a group. If you choose to use tag filtering, only resources with the tags are retrieved. |
| POST | / | Returns a list of registries that you have created, with minimal registry information. Registries in the Deleting status will not be included in the results. Empty results will be returned if there are no registries available. |
| POST | / | Returns a list of schema versions that you have created, with minimal information. Schema versions in Deleted status will not be included in the results. Empty results will be returned if there are no schema versions available. |
| POST | / | Returns a list of schemas with minimal details. Schemas in Deleting status will not be included in the results. Empty results will be returned if there are no schemas available. When the RegistryId is not provided, all the schemas across registries will be part of the API response. |
| POST | / | Retrieve a list of sessions. |
| POST | / | Lists statements for the session. |
| POST | / | Lists the history of previous optimizer runs for a specific table. |
| POST | / | Retrieves the names of all trigger resources in this Amazon Web Services account, or the resources with the specified tag. This operation allows you to see which resources are available in your account, and their names. This operation takes the optional Tags field, which you can use as a filter on the response so that tagged resources can be retrieved as a group. If you choose to use tags filtering, only resources with the tag are retrieved. |
| POST | / | List all the Glue usage profiles. |
| POST | / | Lists names of workflows created in the account. |
| POST | / | Sets the security configuration for a specified catalog. After the configuration has been set, the specified encryption is applied to every catalog write thereafter. |
| POST | / | Annotate all datapoints for a Profile. |
| POST | / | Sets the Data Catalog resource policy for access control. |
| POST | / | Puts the metadata key value pair for a specified schema version ID. A maximum of 10 key value pairs will be allowed per schema version. They can be added over one or more calls. |
| POST | / | Puts the specified workflow run properties for the given workflow run. If a property already exists for the specified run, then it overrides the value otherwise adds the property to existing properties. |
| POST | / | Queries for the schema version metadata information. |
| POST | / | Adds a new version to the existing schema. Returns an error if new version of schema does not meet the compatibility requirements of the schema set. This API will not create a new schema set and will return a 404 error if the schema set is not already present in the Schema Registry. If this is the first schema definition to be registered in the Schema Registry, this API will store the schema version and return immediately. Otherwise, this call has the potential to run longer than other operations due to compatibility modes. You can call the GetSchemaVersion API with the SchemaVersionId to check compatibility modes. If the same schema definition is already stored in Schema Registry as a version, the schema ID of the existing schema is returned to the caller. |
| POST | / | Removes a key value pair from the schema version metadata for the specified schema version ID. |
| POST | / | Resets a bookmark entry. For more information about enabling and using job bookmarks, see:    Tracking processed data using job bookmarks     Job parameters used by Glue     Job structure |
| POST | / | Restarts selected nodes of a previous partially completed workflow run and resumes the workflow run. The selected nodes and all nodes that are downstream from the selected nodes are run. |
| POST | / | Executes the statement. |
| POST | / | Searches a set of tables based on properties in the table metadata as well as on the parent database. You can search against text or filter conditions.  You can only get tables that you have access to based on the security policies defined in Lake Formation. You need at least a read-only access to the table for it to be returned. If you do not have access to all the columns in the table, these columns will not be searched against when returning the list of tables back to you. If you have access to the columns but not the data in the columns, those columns and the associated metadata for those columns will be included in the search. |
| POST | / | Starts a new run of the specified blueprint. |
| POST | / | Starts a column statistics task run, for a specified table and columns. |
| POST | / | Starts a crawl using the specified crawler, regardless of what is scheduled. If the crawler is already running, returns a CrawlerRunningException. |
| POST | / | Changes the schedule state of the specified crawler to SCHEDULED, unless the crawler is already running or the schedule state is already SCHEDULED. |
| POST | / | Starts a recommendation run that is used to generate rules when you don't know what rules to write. Glue Data Quality analyzes the data and comes up with recommendations for a potential ruleset. You can then triage the ruleset and modify the generated ruleset to your liking. Recommendation runs are automatically deleted after 90 days. |
| POST | / | Once you have a ruleset definition (either recommended or your own), you call this operation to evaluate the ruleset against a data source (Glue table). The evaluation computes results which you can retrieve with the GetDataQualityResult API. |
| POST | / | Begins an asynchronous task to export all labeled data for a particular transform. This task is the only label-related API call that is not part of the typical active learning workflow. You typically use StartExportLabelsTaskRun when you want to work with all of your existing labels at the same time, such as when you want to remove or change labels that were previously submitted as truth. This API operation accepts the TransformId whose labels you want to export and an Amazon Simple Storage Service (Amazon S3) path to export the labels to. The operation returns a TaskRunId. You can check on the status of your task run by calling the GetMLTaskRun API. |
| POST | / | Enables you to provide additional labels (examples of truth) to be used to teach the machine learning transform and improve its quality. This API operation is generally used as part of the active learning workflow that starts with the StartMLLabelingSetGenerationTaskRun call and that ultimately results in improving the quality of your machine learning transform.  After the StartMLLabelingSetGenerationTaskRun finishes, Glue machine learning will have generated a series of questions for humans to answer. (Answering these questions is often called 'labeling' in the machine learning workflows). In the case of the FindMatches transform, these questions are of the form, “What is the correct way to group these rows together into groups composed entirely of matching records?” After the labeling process is finished, users upload their answers/labels with a call to StartImportLabelsTaskRun. After StartImportLabelsTaskRun finishes, all future runs of the machine learning transform use the new and improved labels and perform a higher-quality transformation. By default, StartMLLabelingSetGenerationTaskRun continually learns from and combines all labels that you upload unless you set Replace to true. If you set Replace to true, StartImportLabelsTaskRun deletes and forgets all previously uploaded labels and learns only from the exact set that you upload. Replacing labels can be helpful if you realize that you previously uploaded incorrect labels, and you believe that they are having a negative effect on your transform quality. You can check on the status of your task run by calling the GetMLTaskRun operation. |
| POST | / | Starts a job run using a job definition. |
| POST | / | Starts a task to estimate the quality of the transform.  When you provide label sets as examples of truth, Glue machine learning uses some of those examples to learn from them. The rest of the labels are used as a test to estimate quality. Returns a unique identifier for the run. You can call GetMLTaskRun to get more information about the stats of the EvaluationTaskRun. |
| POST | / | Starts the active learning workflow for your machine learning transform to improve the transform's quality by generating label sets and adding labels. When the StartMLLabelingSetGenerationTaskRun finishes, Glue will have generated a "labeling set" or a set of questions for humans to answer. In the case of the FindMatches transform, these questions are of the form, “What is the correct way to group these rows together into groups composed entirely of matching records?”  After the labeling process is finished, you can upload your labels with a call to StartImportLabelsTaskRun. After StartImportLabelsTaskRun finishes, all future runs of the machine learning transform will use the new and improved labels and perform a higher-quality transformation. |
| POST | / | Starts an existing trigger. See Triggering Jobs for information about how different types of trigger are started. |
| POST | / | Starts a new run of the specified workflow. |
| POST | / | Stops a task run for the specified table. |
| POST | / | If the specified crawler is running, stops the crawl. |
| POST | / | Sets the schedule state of the specified crawler to NOT_SCHEDULED, but does not stop the crawler if it is already running. |
| POST | / | Stops the session. |
| POST | / | Stops a specified trigger. |
| POST | / | Stops the execution of the specified workflow run. |
| POST | / | Adds tags to a resource. A tag is a label you can assign to an Amazon Web Services resource. In Glue, you can tag only certain resources. For information about what resources you can tag, see Amazon Web Services Tags in Glue. |
| POST | / | Removes tags from a resource. |
| POST | / | Updates a registered blueprint. |
| POST | / | Modifies an existing classifier (a GrokClassifier, an XMLClassifier, a JsonClassifier, or a CsvClassifier, depending on which field is present). |
| POST | / | Creates or updates partition statistics of columns. The Identity and Access Management (IAM) permission required for this operation is UpdatePartition. |
| POST | / | Creates or updates table statistics of columns. The Identity and Access Management (IAM) permission required for this operation is UpdateTable. |
| POST | / | Updates a connection definition in the Data Catalog. |
| POST | / | Updates a crawler. If a crawler is running, you must stop it using StopCrawler before updating it. |
| POST | / | Updates the schedule of a crawler using a cron expression. |
| POST | / | Updates the specified data quality ruleset. |
| POST | / | Updates an existing database definition in a Data Catalog. |
| POST | / | Updates a specified development endpoint. |
| POST | / | Updates an existing job definition. The previous job definition is completely overwritten by this information. |
| POST | / | Synchronizes a job from the source control repository. This operation takes the job artifacts that are located in the remote repository and updates the Glue internal stores with these artifacts. This API supports optional parameters which take in the repository information. |
| POST | / | Updates an existing machine learning transform. Call this operation to tune the algorithm parameters to achieve better results. After calling this operation, you can call the StartMLEvaluationTaskRun operation to assess how well your new parameters achieved your goals (such as improving the quality of your machine learning transform, or making it more cost-effective). |
| POST | / | Updates a partition. |
| POST | / | Updates an existing registry which is used to hold a collection of schemas. The updated properties relate to the registry, and do not modify any of the schemas within the registry. |
| POST | / | Updates the description, compatibility setting, or version checkpoint for a schema set. For updating the compatibility setting, the call will not validate compatibility for the entire set of schema versions with the new compatibility setting. If the value for Compatibility is provided, the VersionNumber (a checkpoint) is also required. The API will validate the checkpoint version number for consistency. If the value for the VersionNumber (checkpoint) is provided, Compatibility is optional and this can be used to set/reset a checkpoint for the schema. This update will happen only if the schema is in the AVAILABLE state. |
| POST | / | Synchronizes a job to the source control repository. This operation takes the job artifacts from the Glue internal stores and makes a commit to the remote repository that is configured on the job. This API supports optional parameters which take in the repository information. |
| POST | / | Updates a metadata table in the Data Catalog. |
| POST | / | Updates the configuration for an existing table optimizer. |
| POST | / | Updates a trigger definition. |
| POST | / | Update an Glue usage profile. |
| POST | / | Updates an existing function definition in the Data Catalog. |
| POST | / | Updates an existing workflow. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
