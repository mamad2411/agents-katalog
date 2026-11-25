---
name: amazon-kinesis-analytics
description: "Amazon Kinesis Analytics API skill. Use when working with Amazon Kinesis Analytics for root. Covers 33 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon Kinesis Analytics
API version: 2018-05-23

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST / -- create first resource

## Endpoints

33 endpoints across 1 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| POST | / | Adds an Amazon CloudWatch log stream to monitor application configuration errors. |
| POST | / | Adds a streaming source to your SQL-based Kinesis Data Analytics application.  You can add a streaming source when you create an application, or you can use this operation to add a streaming source after you create an application. For more information, see CreateApplication. Any configuration update, including adding a streaming source using this operation, results in a new version of the application. You can use the DescribeApplication operation to find the current application version. |
| POST | / | Adds an InputProcessingConfiguration to a SQL-based Kinesis Data Analytics application. An input processor pre-processes records on the input stream before the application's SQL code executes. Currently, the only input processor available is Amazon Lambda. |
| POST | / | Adds an external destination to your SQL-based Kinesis Data Analytics application. If you want Kinesis Data Analytics to deliver data from an in-application stream within your application to an external destination (such as an Kinesis data stream, a Kinesis Data Firehose delivery stream, or an Amazon Lambda function), you add the relevant configuration to your application using this operation. You can configure one or more outputs for your application. Each output configuration maps an in-application stream and an external destination.  You can use one of the output configurations to deliver data from your in-application error stream to an external destination so that you can analyze the errors.   Any configuration update, including adding a streaming source using this operation, results in a new version of the application. You can use the DescribeApplication operation to find the current application version. |
| POST | / | Adds a reference data source to an existing SQL-based Kinesis Data Analytics application. Kinesis Data Analytics reads reference data (that is, an Amazon S3 object) and creates an in-application table within your application. In the request, you provide the source (S3 bucket name and object key name), name of the in-application table to create, and the necessary mapping information that describes how data in an Amazon S3 object maps to columns in the resulting in-application table. |
| POST | / | Adds a Virtual Private Cloud (VPC) configuration to the application. Applications can use VPCs to store and access resources securely. Note the following about VPC configurations for Managed Service for Apache Flink applications:   VPC configurations are not supported for SQL applications.   When a VPC is added to a Managed Service for Apache Flink application, the application can no longer be accessed from the Internet directly. To enable Internet access to the application, add an Internet gateway to your VPC. |
| POST | / | Creates a Managed Service for Apache Flink application. For information about creating a Managed Service for Apache Flink application, see Creating an Application. |
| POST | / | Creates and returns a URL that you can use to connect to an application's extension. The IAM role or user used to call this API defines the permissions to access the extension. After the presigned URL is created, no additional permission is required to access this URL. IAM authorization policies for this API are also enforced for every HTTP request that attempts to connect to the extension.  You control the amount of time that the URL will be valid using the SessionExpirationDurationInSeconds parameter. If you do not provide this parameter, the returned URL is valid for twelve hours.  The URL that you get from a call to CreateApplicationPresignedUrl must be used within 3 minutes to be valid. If you first try to use the URL after the 3-minute limit expires, the service returns an HTTP 403 Forbidden error. |
| POST | / | Creates a snapshot of the application's state data. |
| POST | / | Deletes the specified application. Managed Service for Apache Flink halts application execution and deletes the application. |
| POST | / | Deletes an Amazon CloudWatch log stream from an SQL-based Kinesis Data Analytics application. |
| POST | / | Deletes an InputProcessingConfiguration from an input. |
| POST | / | Deletes the output destination configuration from your SQL-based Kinesis Data Analytics application's configuration. Kinesis Data Analytics will no longer write data from the corresponding in-application stream to the external output destination. |
| POST | / | Deletes a reference data source configuration from the specified SQL-based Kinesis Data Analytics application's configuration. If the application is running, Kinesis Data Analytics immediately removes the in-application table that you created using the AddApplicationReferenceDataSource operation. |
| POST | / | Deletes a snapshot of application state. |
| POST | / | Removes a VPC configuration from a Managed Service for Apache Flink application. |
| POST | / | Returns information about a specific Managed Service for Apache Flink application. If you want to retrieve a list of all applications in your account, use the ListApplications operation. |
| POST | / | Returns information about a specific operation performed on a Managed Service for Apache Flink application |
| POST | / | Returns information about a snapshot of application state data. |
| POST | / | Provides a detailed description of a specified version of the application. To see a list of all the versions of an application, invoke the ListApplicationVersions operation.  This operation is supported only for Managed Service for Apache Flink. |
| POST | / | Infers a schema for a SQL-based Kinesis Data Analytics application by evaluating sample records on the specified streaming source (Kinesis data stream or Kinesis Data Firehose delivery stream) or Amazon S3 object. In the response, the operation returns the inferred schema and also the sample records that the operation used to infer the schema.  You can use the inferred schema when configuring a streaming source for your application. When you create an application using the Kinesis Data Analytics console, the console uses this operation to infer a schema and show it in the console user interface. |
| POST | / | Lists information about operations performed on a Managed Service for Apache Flink application |
| POST | / | Lists information about the current application snapshots. |
| POST | / | Lists all the versions for the specified application, including versions that were rolled back. The response also includes a summary of the configuration associated with each version. To get the complete description of a specific application version, invoke the DescribeApplicationVersion operation.  This operation is supported only for Managed Service for Apache Flink. |
| POST | / | Returns a list of Managed Service for Apache Flink applications in your account. For each application, the response includes the application name, Amazon Resource Name (ARN), and status.  If you want detailed information about a specific application, use DescribeApplication. |
| POST | / | Retrieves the list of key-value tags assigned to the application. For more information, see Using Tagging. |
| POST | / | Reverts the application to the previous running version. You can roll back an application if you suspect it is stuck in a transient status or in the running status.  You can roll back an application only if it is in the UPDATING, AUTOSCALING, or RUNNING statuses. When you rollback an application, it loads state data from the last successful snapshot. If the application has no snapshots, Managed Service for Apache Flink rejects the rollback request. |
| POST | / | Starts the specified Managed Service for Apache Flink application. After creating an application, you must exclusively call this operation to start your application. |
| POST | / | Stops the application from processing data. You can stop an application only if it is in the running status, unless you set the Force parameter to true. You can use the DescribeApplication operation to find the application status.  Managed Service for Apache Flink takes a snapshot when the application is stopped, unless Force is set to true. |
| POST | / | Adds one or more key-value tags to a Managed Service for Apache Flink application. Note that the maximum number of application tags includes system tags. The maximum number of user-defined application tags is 50. For more information, see Using Tagging. |
| POST | / | Removes one or more tags from a Managed Service for Apache Flink application. For more information, see Using Tagging. |
| POST | / | Updates an existing Managed Service for Apache Flink application. Using this operation, you can update application code, input configuration, and output configuration.  Managed Service for Apache Flink updates the ApplicationVersionId each time you update your application. |
| POST | / | Updates the maintenance configuration of the Managed Service for Apache Flink application.  You can invoke this operation on an application that is in one of the two following states: READY or RUNNING. If you invoke it when the application is in a state other than these two states, it throws a ResourceInUseException. The service makes use of the updated configuration the next time it schedules maintenance for the application. If you invoke this operation after the service schedules maintenance, the service will apply the configuration update the next time it schedules maintenance for the application. This means that you might not see the maintenance configuration update applied to the maintenance process that follows a successful invocation of this operation, but to the following maintenance process instead. To see the current maintenance configuration of your application, invoke the DescribeApplication operation. For information about application maintenance, see Managed Service for Apache Flink for Apache Flink Maintenance.  This operation is supported only for Managed Service for Apache Flink. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
