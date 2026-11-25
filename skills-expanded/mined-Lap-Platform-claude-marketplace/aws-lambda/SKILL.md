---
name: aws-lambda
description: "AWS Lambda API skill. Use when working with AWS Lambda for 2018-10-31, 2015-03-31, 2020-04-22. Covers 68 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS Lambda
API version: 2015-03-31

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /2016-08-19/account-settings/ -- verify access
3. POST /2018-10-31/layers/{LayerName}/versions/{VersionNumber}/policy -- create first policy

## Endpoints

68 endpoints across 14 groups. See references/api-spec.lap for full details.

### 2018-10-31
| Method | Path | Description |
|--------|------|-------------|
| POST | /2018-10-31/layers/{LayerName}/versions/{VersionNumber}/policy | Adds permissions to the resource-based policy of a version of an Lambda layer. Use this action to grant layer usage permission to other accounts. You can grant permission to a single account, all accounts in an organization, or all Amazon Web Services accounts.  To revoke permission, call RemoveLayerVersionPermission with the statement ID that you specified when you added it. |
| DELETE | /2018-10-31/layers/{LayerName}/versions/{VersionNumber} | Deletes a version of an Lambda layer. Deleted versions can no longer be viewed or added to functions. To avoid breaking functions, a copy of the version remains in Lambda until no functions refer to it. |
| GET | /2018-10-31/layers/{LayerName}/versions/{VersionNumber} | Returns information about a version of an Lambda layer, with a link to download the layer archive that's valid for 10 minutes. |
| GET | /2018-10-31/layers?find=LayerVersion | Returns information about a version of an Lambda layer, with a link to download the layer archive that's valid for 10 minutes. |
| GET | /2018-10-31/layers/{LayerName}/versions/{VersionNumber}/policy | Returns the permission policy for a version of an Lambda layer. For more information, see AddLayerVersionPermission. |
| GET | /2018-10-31/layers/{LayerName}/versions | Lists the versions of an Lambda layer. Versions that have been deleted aren't listed. Specify a runtime identifier to list only versions that indicate that they're compatible with that runtime. Specify a compatible architecture to include only layer versions that are compatible with that architecture. |
| GET | /2018-10-31/layers | Lists Lambda layers and shows information about the latest version of each. Specify a runtime identifier to list only layers that indicate that they're compatible with that runtime. Specify a compatible architecture to include only layers that are compatible with that instruction set architecture. |
| POST | /2018-10-31/layers/{LayerName}/versions | Creates an Lambda layer from a ZIP archive. Each time you call PublishLayerVersion with the same layer name, a new version is created. Add layers to your function with CreateFunction or UpdateFunctionConfiguration. |
| DELETE | /2018-10-31/layers/{LayerName}/versions/{VersionNumber}/policy/{StatementId} | Removes a statement from the permissions policy for a version of an Lambda layer. For more information, see AddLayerVersionPermission. |

### 2015-03-31
| Method | Path | Description |
|--------|------|-------------|
| POST | /2015-03-31/functions/{FunctionName}/policy | Grants an Amazon Web Servicesservice, Amazon Web Services account, or Amazon Web Services organization permission to use a function. You can apply the policy at the function level, or specify a qualifier to restrict access to a single version or alias. If you use a qualifier, the invoker must use the full Amazon Resource Name (ARN) of that version or alias to invoke the function. Note: Lambda does not support adding policies to version $LATEST. To grant permission to another account, specify the account ID as the Principal. To grant permission to an organization defined in Organizations, specify the organization ID as the PrincipalOrgID. For Amazon Web Servicesservices, the principal is a domain-style identifier that the service defines, such as s3.amazonaws.com or sns.amazonaws.com. For Amazon Web Servicesservices, you can also specify the ARN of the associated resource as the SourceArn. If you grant permission to a service principal without specifying the source, other accounts could potentially configure resources in their account to invoke your Lambda function. This operation adds a statement to a resource-based permissions policy for the function. For more information about function policies, see Using resource-based policies for Lambda. |
| POST | /2015-03-31/functions/{FunctionName}/aliases | Creates an alias for a Lambda function version. Use aliases to provide clients with a function identifier that you can update to invoke a different version. You can also map an alias to split invocation requests between two versions. Use the RoutingConfig parameter to specify a second version and the percentage of invocation requests that it receives. |
| POST | /2015-03-31/event-source-mappings/ | Creates a mapping between an event source and an Lambda function. Lambda reads items from the event source and invokes the function. For details about how to configure different event sources, see the following topics.      Amazon DynamoDB Streams      Amazon Kinesis      Amazon SQS      Amazon MQ and RabbitMQ      Amazon MSK      Apache Kafka      Amazon DocumentDB    The following error handling options are available only for stream sources (DynamoDB and Kinesis):    BisectBatchOnFunctionError – If the function returns an error, split the batch in two and retry.    DestinationConfig – Send discarded records to an Amazon SQS queue or Amazon SNS topic.    MaximumRecordAgeInSeconds – Discard records older than the specified age. The default value is infinite (-1). When set to infinite (-1), failed records are retried until the record expires    MaximumRetryAttempts – Discard records after the specified number of retries. The default value is infinite (-1). When set to infinite (-1), failed records are retried until the record expires.    ParallelizationFactor – Process multiple batches from each shard concurrently.   For information about which configuration parameters apply to each event source, see the following topics.     Amazon DynamoDB Streams      Amazon Kinesis      Amazon SQS      Amazon MQ and RabbitMQ      Amazon MSK      Apache Kafka      Amazon DocumentDB |
| POST | /2015-03-31/functions | Creates a Lambda function. To create a function, you need a deployment package and an execution role. The deployment package is a .zip file archive or container image that contains your function code. The execution role grants the function permission to use Amazon Web Servicesservices, such as Amazon CloudWatch Logs for log streaming and X-Ray for request tracing. If the deployment package is a container image, then you set the package type to Image. For a container image, the code property must include the URI of a container image in the Amazon ECR registry. You do not need to specify the handler and runtime properties. If the deployment package is a .zip file archive, then you set the package type to Zip. For a .zip file archive, the code property specifies the location of the .zip file. You must also specify the handler and runtime properties. The code in the deployment package must be compatible with the target instruction set architecture of the function (x86-64 or arm64). If you do not specify the architecture, then the default value is x86-64. When you create a function, Lambda provisions an instance of the function and its supporting resources. If your function connects to a VPC, this process can take a minute or so. During this time, you can't invoke or modify the function. The State, StateReason, and StateReasonCode fields in the response from GetFunctionConfiguration indicate when the function is ready to invoke. For more information, see Lambda function states. A function has an unpublished version, and can have published versions and aliases. The unpublished version changes when you update your function's code and configuration. A published version is a snapshot of your function code and configuration that can't be changed. An alias is a named resource that maps to a version, and can be changed to map to a different version. Use the Publish parameter to create version 1 of your function from its initial configuration. The other parameters let you configure version-specific and function-level settings. You can modify version-specific settings later with UpdateFunctionConfiguration. Function-level settings apply to both the unpublished and published versions of the function, and include tags (TagResource) and per-function concurrency limits (PutFunctionConcurrency). You can use code signing if your deployment package is a .zip file archive. To enable code signing for this function, specify the ARN of a code-signing configuration. When a user attempts to deploy a code package with UpdateFunctionCode, Lambda checks that the code package has a valid signature from a trusted publisher. The code-signing configuration includes set of signing profiles, which define the trusted publishers for this function. If another Amazon Web Services account or an Amazon Web Servicesservice invokes your function, use AddPermission to grant permission by creating a resource-based Identity and Access Management (IAM) policy. You can grant permissions at the function level, on a version, or on an alias. To invoke your function directly, use Invoke. To invoke your function in response to events in other Amazon Web Servicesservices, create an event source mapping (CreateEventSourceMapping), or configure a function trigger in the other service. For more information, see Invoking Lambda functions. |
| DELETE | /2015-03-31/functions/{FunctionName}/aliases/{Name} | Deletes a Lambda function alias. |
| DELETE | /2015-03-31/event-source-mappings/{UUID} | Deletes an event source mapping. You can get the identifier of a mapping from the output of ListEventSourceMappings. When you delete an event source mapping, it enters a Deleting state and might not be completely deleted for several seconds. |
| DELETE | /2015-03-31/functions/{FunctionName} | Deletes a Lambda function. To delete a specific function version, use the Qualifier parameter. Otherwise, all versions and aliases are deleted. This doesn't require the user to have explicit permissions for DeleteAlias. To delete Lambda event source mappings that invoke a function, use DeleteEventSourceMapping. For Amazon Web Servicesservices and resources that invoke your function directly, delete the trigger in the service where you originally configured it. |
| GET | /2015-03-31/functions/{FunctionName}/aliases/{Name} | Returns details about a Lambda function alias. |
| GET | /2015-03-31/event-source-mappings/{UUID} | Returns details about an event source mapping. You can get the identifier of a mapping from the output of ListEventSourceMappings. |
| GET | /2015-03-31/functions/{FunctionName} | Returns information about the function or function version, with a link to download the deployment package that's valid for 10 minutes. If you specify a function version, only details that are specific to that version are returned. |
| GET | /2015-03-31/functions/{FunctionName}/configuration | Returns the version-specific settings of a Lambda function or version. The output includes only options that can vary between versions of a function. To modify these settings, use UpdateFunctionConfiguration. To get all of a function's details, including function-level settings, use GetFunction. |
| GET | /2015-03-31/functions/{FunctionName}/policy | Returns the resource-based IAM policy for a function, version, or alias. |
| POST | /2015-03-31/functions/{FunctionName}/invocations | Invokes a Lambda function. You can invoke a function synchronously (and wait for the response), or asynchronously. By default, Lambda invokes your function synchronously (i.e. theInvocationType is RequestResponse). To invoke a function asynchronously, set InvocationType to Event. Lambda passes the ClientContext object to your function for synchronous invocations only. For synchronous invocation, details about the function response, including errors, are included in the response body and headers. For either invocation type, you can find more information in the execution log and trace. When an error occurs, your function may be invoked multiple times. Retry behavior varies by error type, client, event source, and invocation type. For example, if you invoke a function asynchronously and it returns an error, Lambda executes the function up to two more times. For more information, see Error handling and automatic retries in Lambda. For asynchronous invocation, Lambda adds events to a queue before sending them to your function. If your function does not have enough capacity to keep up with the queue, events may be lost. Occasionally, your function may receive the same event multiple times, even if no error occurs. To retain events that were not processed, configure your function with a dead-letter queue. The status code in the API response doesn't reflect function errors. Error codes are reserved for errors that prevent your function from executing, such as permissions errors, quota errors, or issues with your function's code and configuration. For example, Lambda returns TooManyRequestsException if running the function would cause you to exceed a concurrency limit at either the account level (ConcurrentInvocationLimitExceeded) or function level (ReservedFunctionConcurrentInvocationLimitExceeded). For functions with a long timeout, your client might disconnect during synchronous invocation while it waits for a response. Configure your HTTP client, SDK, firewall, proxy, or operating system to allow for long connections with timeout or keep-alive settings. This operation requires permission for the lambda:InvokeFunction action. For details on how to set up permissions for cross-account invocations, see Granting function access to other accounts. |
| GET | /2015-03-31/functions/{FunctionName}/aliases | Returns a list of aliases for a Lambda function. |
| GET | /2015-03-31/event-source-mappings/ | Lists event source mappings. Specify an EventSourceArn to show only event source mappings for a single event source. |
| GET | /2015-03-31/functions/ | Returns a list of Lambda functions, with the version-specific configuration of each. Lambda returns up to 50 functions per call. Set FunctionVersion to ALL to include all published versions of each function in addition to the unpublished version.  The ListFunctions operation returns a subset of the FunctionConfiguration fields. To get the additional fields (State, StateReasonCode, StateReason, LastUpdateStatus, LastUpdateStatusReason, LastUpdateStatusReasonCode, RuntimeVersionConfig) for a function or version, use GetFunction. |
| GET | /2015-03-31/functions/{FunctionName}/versions | Returns a list of versions, with the version-specific configuration of each. Lambda returns up to 50 versions per call. |
| POST | /2015-03-31/functions/{FunctionName}/versions | Creates a version from the current code and configuration of a function. Use versions to create a snapshot of your function code and configuration that doesn't change. Lambda doesn't publish a version if the function's configuration and code haven't changed since the last version. Use UpdateFunctionCode or UpdateFunctionConfiguration to update the function before publishing a version. Clients can invoke versions directly or with an alias. To create an alias, use CreateAlias. |
| DELETE | /2015-03-31/functions/{FunctionName}/policy/{StatementId} | Revokes function-use permission from an Amazon Web Servicesservice or another Amazon Web Services account. You can get the ID of the statement from the output of GetPolicy. |
| PUT | /2015-03-31/functions/{FunctionName}/aliases/{Name} | Updates the configuration of a Lambda function alias. |
| PUT | /2015-03-31/event-source-mappings/{UUID} | Updates an event source mapping. You can change the function that Lambda invokes, or pause invocation and resume later from the same location. For details about how to configure different event sources, see the following topics.      Amazon DynamoDB Streams      Amazon Kinesis      Amazon SQS      Amazon MQ and RabbitMQ      Amazon MSK      Apache Kafka      Amazon DocumentDB    The following error handling options are available only for stream sources (DynamoDB and Kinesis):    BisectBatchOnFunctionError – If the function returns an error, split the batch in two and retry.    DestinationConfig – Send discarded records to an Amazon SQS queue or Amazon SNS topic.    MaximumRecordAgeInSeconds – Discard records older than the specified age. The default value is infinite (-1). When set to infinite (-1), failed records are retried until the record expires    MaximumRetryAttempts – Discard records after the specified number of retries. The default value is infinite (-1). When set to infinite (-1), failed records are retried until the record expires.    ParallelizationFactor – Process multiple batches from each shard concurrently.   For information about which configuration parameters apply to each event source, see the following topics.     Amazon DynamoDB Streams      Amazon Kinesis      Amazon SQS      Amazon MQ and RabbitMQ      Amazon MSK      Apache Kafka      Amazon DocumentDB |
| PUT | /2015-03-31/functions/{FunctionName}/code | Updates a Lambda function's code. If code signing is enabled for the function, the code package must be signed by a trusted publisher. For more information, see Configuring code signing for Lambda. If the function's package type is Image, then you must specify the code package in ImageUri as the URI of a container image in the Amazon ECR registry. If the function's package type is Zip, then you must specify the deployment package as a .zip file archive. Enter the Amazon S3 bucket and key of the code .zip file location. You can also provide the function code inline using the ZipFile field. The code in the deployment package must be compatible with the target instruction set architecture of the function (x86-64 or arm64). The function's code is locked when you publish a version. You can't modify the code of a published version, only the unpublished version.  For a function defined as a container image, Lambda resolves the image tag to an image digest. In Amazon ECR, if you update the image tag to a new image, Lambda does not automatically update the function. |
| PUT | /2015-03-31/functions/{FunctionName}/configuration | Modify the version-specific settings of a Lambda function. When you update a function, Lambda provisions an instance of the function and its supporting resources. If your function connects to a VPC, this process can take a minute. During this time, you can't modify the function, but you can still invoke it. The LastUpdateStatus, LastUpdateStatusReason, and LastUpdateStatusReasonCode fields in the response from GetFunctionConfiguration indicate when the update is complete and the function is processing events with the new configuration. For more information, see Lambda function states. These settings can vary between versions of a function and are locked when you publish a version. You can't modify the configuration of a published version, only the unpublished version. To configure function concurrency, use PutFunctionConcurrency. To grant invoke permissions to an Amazon Web Services account or Amazon Web Servicesservice, use AddPermission. |

### 2020-04-22
| Method | Path | Description |
|--------|------|-------------|
| POST | /2020-04-22/code-signing-configs/ | Creates a code signing configuration. A code signing configuration defines a list of allowed signing profiles and defines the code-signing validation policy (action to be taken if deployment validation checks fail). |
| DELETE | /2020-04-22/code-signing-configs/{CodeSigningConfigArn} | Deletes the code signing configuration. You can delete the code signing configuration only if no function is using it. |
| GET | /2020-04-22/code-signing-configs/{CodeSigningConfigArn} | Returns information about the specified code signing configuration. |
| GET | /2020-04-22/code-signing-configs/ | Returns a list of code signing configurations. A request returns up to 10,000 configurations per call. You can use the MaxItems parameter to return fewer configurations per call. |
| GET | /2020-04-22/code-signing-configs/{CodeSigningConfigArn}/functions | List the functions that use the specified code signing configuration. You can use this method prior to deleting a code signing configuration, to verify that no functions are using it. |
| PUT | /2020-04-22/code-signing-configs/{CodeSigningConfigArn} | Update the code signing configuration. Changes to the code signing configuration take effect the next time a user tries to deploy a code package to the function. |

### 2021-10-31
| Method | Path | Description |
|--------|------|-------------|
| POST | /2021-10-31/functions/{FunctionName}/url | Creates a Lambda function URL with the specified configuration parameters. A function URL is a dedicated HTTP(S) endpoint that you can use to invoke your function. |
| DELETE | /2021-10-31/functions/{FunctionName}/url | Deletes a Lambda function URL. When you delete a function URL, you can't recover it. Creating a new function URL results in a different URL address. |
| GET | /2021-10-31/functions/{FunctionName}/url | Returns details about a Lambda function URL. |
| GET | /2021-10-31/functions/{FunctionName}/urls | Returns a list of Lambda function URLs for the specified function. |
| PUT | /2021-10-31/functions/{FunctionName}/url | Updates the configuration for a Lambda function URL. |

### 2020-06-30
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /2020-06-30/functions/{FunctionName}/code-signing-config | Removes the code signing configuration from the function. |
| GET | /2020-06-30/functions/{FunctionName}/code-signing-config | Returns the code signing configuration for the specified function. |
| PUT | /2020-06-30/functions/{FunctionName}/code-signing-config | Update the code signing configuration for the function. Changes to the code signing configuration take effect the next time a user tries to deploy a code package to the function. |

### 2017-10-31
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /2017-10-31/functions/{FunctionName}/concurrency | Removes a concurrent execution limit from a function. |
| PUT | /2017-10-31/functions/{FunctionName}/concurrency | Sets the maximum number of simultaneous executions for a function, and reserves capacity for that concurrency level. Concurrency settings apply to the function as a whole, including all published versions and the unpublished version. Reserving concurrency both ensures that your function has capacity to process the specified number of events simultaneously, and prevents it from scaling beyond that level. Use GetFunction to see the current setting for a function. Use GetAccountSettings to see your Regional concurrency limit. You can reserve concurrency for as many functions as you like, as long as you leave at least 100 simultaneous executions unreserved for functions that aren't configured with a per-function limit. For more information, see Lambda function scaling. |

### 2019-09-25
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /2019-09-25/functions/{FunctionName}/event-invoke-config | Deletes the configuration for asynchronous invocation for a function, version, or alias. To configure options for asynchronous invocation, use PutFunctionEventInvokeConfig. |
| GET | /2019-09-25/functions/{FunctionName}/event-invoke-config | Retrieves the configuration for asynchronous invocation for a function, version, or alias. To configure options for asynchronous invocation, use PutFunctionEventInvokeConfig. |
| GET | /2019-09-25/functions/{FunctionName}/event-invoke-config/list | Retrieves a list of configurations for asynchronous invocation for a function. To configure options for asynchronous invocation, use PutFunctionEventInvokeConfig. |
| PUT | /2019-09-25/functions/{FunctionName}/event-invoke-config | Configures options for asynchronous invocation on a function, version, or alias. If a configuration already exists for a function, version, or alias, this operation overwrites it. If you exclude any settings, they are removed. To set one option without affecting existing settings for other options, use UpdateFunctionEventInvokeConfig. By default, Lambda retries an asynchronous invocation twice if the function returns an error. It retains events in a queue for up to six hours. When an event fails all processing attempts or stays in the asynchronous invocation queue for too long, Lambda discards it. To retain discarded events, configure a dead-letter queue with UpdateFunctionConfiguration. To send an invocation record to a queue, topic, function, or event bus, specify a destination. You can configure separate destinations for successful invocations (on-success) and events that fail all processing attempts (on-failure). You can configure destinations in addition to or instead of a dead-letter queue. |
| POST | /2019-09-25/functions/{FunctionName}/event-invoke-config | Updates the configuration for asynchronous invocation for a function, version, or alias. To configure options for asynchronous invocation, use PutFunctionEventInvokeConfig. |

### 2019-09-30
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /2019-09-30/functions/{FunctionName}/provisioned-concurrency | Deletes the provisioned concurrency configuration for a function. |
| GET | /2019-09-30/functions/{FunctionName}/concurrency | Returns details about the reserved concurrency configuration for a function. To set a concurrency limit for a function, use PutFunctionConcurrency. |
| GET | /2019-09-30/functions/{FunctionName}/provisioned-concurrency | Retrieves the provisioned concurrency configuration for a function's alias or version. |
| GET | /2019-09-30/functions/{FunctionName}/provisioned-concurrency?List=ALL | Retrieves a list of provisioned concurrency configurations for a function. |
| PUT | /2019-09-30/functions/{FunctionName}/provisioned-concurrency | Adds a provisioned concurrency configuration to a function's alias or version. |

### 2016-08-19
| Method | Path | Description |
|--------|------|-------------|
| GET | /2016-08-19/account-settings/ | Retrieves details about your account's limits and usage in an Amazon Web Services Region. |

### 2024-08-31
| Method | Path | Description |
|--------|------|-------------|
| GET | /2024-08-31/functions/{FunctionName}/recursion-config | Returns your function's recursive loop detection configuration. |
| PUT | /2024-08-31/functions/{FunctionName}/recursion-config | Sets your function's recursive loop detection configuration. When you configure a Lambda function to output to the same service or resource that invokes the function, it's possible to create an infinite recursive loop. For example, a Lambda function might write a message to an Amazon Simple Queue Service (Amazon SQS) queue, which then invokes the same function. This invocation causes the function to write another message to the queue, which in turn invokes the function again. Lambda can detect certain types of recursive loops shortly after they occur. When Lambda detects a recursive loop and your function's recursive loop detection configuration is set to Terminate, it stops your function being invoked and notifies you. |

### 2021-07-20
| Method | Path | Description |
|--------|------|-------------|
| GET | /2021-07-20/functions/{FunctionName}/runtime-management-config | Retrieves the runtime management configuration for a function's version. If the runtime update mode is Manual, this includes the ARN of the runtime version and the runtime update mode. If the runtime update mode is Auto or Function update, this includes the runtime update mode and null is returned for the ARN. For more information, see Runtime updates. |
| PUT | /2021-07-20/functions/{FunctionName}/runtime-management-config | Sets the runtime management configuration for a function's version. For more information, see Runtime updates. |

### 2014-11-13
| Method | Path | Description |
|--------|------|-------------|
| POST | /2014-11-13/functions/{FunctionName}/invoke-async/ | For asynchronous function invocation, use Invoke.  Invokes a function asynchronously.  If you do use the InvokeAsync action, note that it doesn't support the use of X-Ray active tracing. Trace ID is not propagated to the function, even if X-Ray active tracing is turned on. |

### 2021-11-15
| Method | Path | Description |
|--------|------|-------------|
| POST | /2021-11-15/functions/{FunctionName}/response-streaming-invocations | Configure your Lambda functions to stream response payloads back to clients. For more information, see Configuring a Lambda function to stream responses. This operation requires permission for the lambda:InvokeFunction action. For details on how to set up permissions for cross-account invocations, see Granting function access to other accounts. |

### 2017-03-31
| Method | Path | Description |
|--------|------|-------------|
| GET | /2017-03-31/tags/{ARN} | Returns a function's tags. You can also view tags with GetFunction. |
| POST | /2017-03-31/tags/{ARN} | Adds tags to a function. |
| DELETE | /2017-03-31/tags/{ARN} | Removes tags from a function. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a policy?" -> POST /2018-10-31/layers/{LayerName}/versions/{VersionNumber}/policy
- "Create a policy?" -> POST /2015-03-31/functions/{FunctionName}/policy
- "Create a aliase?" -> POST /2015-03-31/functions/{FunctionName}/aliases
- "Create a code-signing-config?" -> POST /2020-04-22/code-signing-configs/
- "Create a event-source-mapping?" -> POST /2015-03-31/event-source-mappings/
- "Create a function?" -> POST /2015-03-31/functions
- "Create a url?" -> POST /2021-10-31/functions/{FunctionName}/url
- "Delete a aliase?" -> DELETE /2015-03-31/functions/{FunctionName}/aliases/{Name}
- "Delete a code-signing-config?" -> DELETE /2020-04-22/code-signing-configs/{CodeSigningConfigArn}
- "Delete a event-source-mapping?" -> DELETE /2015-03-31/event-source-mappings/{UUID}
- "Delete a function?" -> DELETE /2015-03-31/functions/{FunctionName}
- "Delete a version?" -> DELETE /2018-10-31/layers/{LayerName}/versions/{VersionNumber}
- "List all account-settings?" -> GET /2016-08-19/account-settings/
- "Get aliase details?" -> GET /2015-03-31/functions/{FunctionName}/aliases/{Name}
- "Get code-signing-config details?" -> GET /2020-04-22/code-signing-configs/{CodeSigningConfigArn}
- "Get event-source-mapping details?" -> GET /2015-03-31/event-source-mappings/{UUID}
- "Get function details?" -> GET /2015-03-31/functions/{FunctionName}
- "List all code-signing-config?" -> GET /2020-06-30/functions/{FunctionName}/code-signing-config
- "List all concurrency?" -> GET /2019-09-30/functions/{FunctionName}/concurrency
- "List all configuration?" -> GET /2015-03-31/functions/{FunctionName}/configuration
- "List all event-invoke-config?" -> GET /2019-09-25/functions/{FunctionName}/event-invoke-config
- "List all recursion-config?" -> GET /2024-08-31/functions/{FunctionName}/recursion-config
- "List all url?" -> GET /2021-10-31/functions/{FunctionName}/url
- "Get version details?" -> GET /2018-10-31/layers/{LayerName}/versions/{VersionNumber}
- "List all layers?find=LayerVersion?" -> GET /2018-10-31/layers?find=LayerVersion
- "List all policy?" -> GET /2018-10-31/layers/{LayerName}/versions/{VersionNumber}/policy
- "List all policy?" -> GET /2015-03-31/functions/{FunctionName}/policy
- "List all provisioned-concurrency?" -> GET /2019-09-30/functions/{FunctionName}/provisioned-concurrency
- "List all runtime-management-config?" -> GET /2021-07-20/functions/{FunctionName}/runtime-management-config
- "Create a invocation?" -> POST /2015-03-31/functions/{FunctionName}/invocations
- "Create a invoke-async?" -> POST /2014-11-13/functions/{FunctionName}/invoke-async/
- "Create a response-streaming-invocation?" -> POST /2021-11-15/functions/{FunctionName}/response-streaming-invocations
- "List all aliases?" -> GET /2015-03-31/functions/{FunctionName}/aliases
- "List all code-signing-configs?" -> GET /2020-04-22/code-signing-configs/
- "List all event-source-mappings?" -> GET /2015-03-31/event-source-mappings/
- "List all list?" -> GET /2019-09-25/functions/{FunctionName}/event-invoke-config/list
- "List all urls?" -> GET /2021-10-31/functions/{FunctionName}/urls
- "List all functions?" -> GET /2015-03-31/functions/
- "List all functions?" -> GET /2020-04-22/code-signing-configs/{CodeSigningConfigArn}/functions
- "List all versions?" -> GET /2018-10-31/layers/{LayerName}/versions
- "List all layers?" -> GET /2018-10-31/layers
- "List all provisioned-concurrency?List=ALL?" -> GET /2019-09-30/functions/{FunctionName}/provisioned-concurrency?List=ALL
- "Get tag details?" -> GET /2017-03-31/tags/{ARN}
- "List all versions?" -> GET /2015-03-31/functions/{FunctionName}/versions
- "Create a version?" -> POST /2018-10-31/layers/{LayerName}/versions
- "Create a version?" -> POST /2015-03-31/functions/{FunctionName}/versions
- "Delete a policy?" -> DELETE /2018-10-31/layers/{LayerName}/versions/{VersionNumber}/policy/{StatementId}
- "Delete a policy?" -> DELETE /2015-03-31/functions/{FunctionName}/policy/{StatementId}
- "Delete a tag?" -> DELETE /2017-03-31/tags/{ARN}
- "Update a aliase?" -> PUT /2015-03-31/functions/{FunctionName}/aliases/{Name}
- "Update a code-signing-config?" -> PUT /2020-04-22/code-signing-configs/{CodeSigningConfigArn}
- "Update a event-source-mapping?" -> PUT /2015-03-31/event-source-mappings/{UUID}
- "Create a event-invoke-config?" -> POST /2019-09-25/functions/{FunctionName}/event-invoke-config
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
