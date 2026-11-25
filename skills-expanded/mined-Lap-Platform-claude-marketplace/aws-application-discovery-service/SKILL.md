---
name: aws-application-discovery-service
description: "AWS Application Discovery Service API skill. Use when working with AWS Application Discovery Service for root. Covers 28 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS Application Discovery Service
API version: 2015-11-01

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST / -- create first resource

## Endpoints

28 endpoints across 1 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| POST | / | Associates one or more configuration items with an application. |
| POST | / | Deletes one or more agents or collectors as specified by ID. Deleting an agent or collector does not delete the previously discovered data. To delete the data collected, use StartBatchDeleteConfigurationTask. |
| POST | / | Deletes one or more import tasks, each identified by their import ID. Each import task has a number of records that can identify servers or applications.  Amazon Web Services Application Discovery Service has built-in matching logic that will identify when discovered servers match existing entries that you've previously discovered, the information for the already-existing discovered server is updated. When you delete an import task that contains records that were used to match, the information in those matched records that comes from the deleted records will also be deleted. |
| POST | / | Creates an application with the given name and description. |
| POST | / | Creates one or more tags for configuration items. Tags are metadata that help you categorize IT assets. This API accepts a list of multiple configuration items.  Do not store sensitive information (like personal data) in tags. |
| POST | / | Deletes a list of applications and their associations with configuration items. |
| POST | / | Deletes the association between configuration items and one or more tags. This API accepts a list of multiple configuration items. |
| POST | / | Lists agents or collectors as specified by ID or other filters. All agents/collectors associated with your user can be listed if you call DescribeAgents as is without passing any parameters. |
| POST | / | Takes a unique deletion task identifier as input and returns metadata about a configuration deletion task. |
| POST | / | Retrieves attributes for a list of configuration item IDs.  All of the supplied IDs must be for the same asset type from one of the following:   server   application   process   connection   Output fields are specific to the asset type specified. For example, the output for a server configuration item includes a list of attributes about the server, such as host name, operating system, number of network cards, etc. For a complete list of outputs for each asset type, see Using the DescribeConfigurations Action in the Amazon Web Services Application Discovery Service User Guide. |
| POST | / | Lists exports as specified by ID. All continuous exports associated with your user can be listed if you call DescribeContinuousExports as is without passing any parameters. |
| POST | / | DescribeExportConfigurations is deprecated. Use DescribeExportTasks, instead. |
| POST | / | Retrieve status of one or more export tasks. You can retrieve the status of up to 100 export tasks. |
| POST | / | Returns an array of import tasks for your account, including status information, times, IDs, the Amazon S3 Object URL for the import file, and more. |
| POST | / | Retrieves a list of configuration items that have tags as specified by the key-value pairs, name and value, passed to the optional parameter filters. There are three valid tag filter names:   tagKey   tagValue   configurationId   Also, all configuration items associated with your user that have tags can be listed if you call DescribeTags as is without passing any parameters. |
| POST | / | Disassociates one or more configuration items from an application. |
| POST | / | Deprecated. Use StartExportTask instead. Exports all discovered configuration data to an Amazon S3 bucket or an application that enables you to view and evaluate the data. Data includes tags and tag associations, processes, connections, servers, and system performance. This API returns an export ID that you can query using the DescribeExportConfigurations API. The system imposes a limit of two configuration exports in six hours. |
| POST | / | Retrieves a short summary of discovered assets. This API operation takes no request parameters and is called as is at the command prompt as shown in the example. |
| POST | / | Retrieves a list of configuration items as specified by the value passed to the required parameter configurationType. Optional filtering may be applied to refine search results. |
| POST | / | Retrieves a list of servers that are one network hop away from a specified server. |
| POST | / | Takes a list of configurationId as input and starts an asynchronous deletion task to remove the configurationItems. Returns a unique deletion task identifier. |
| POST | / | Start the continuous flow of agent's discovered data into Amazon Athena. |
| POST | / | Instructs the specified agents to start collecting data. |
| POST | / | Begins the export of a discovered data report to an Amazon S3 bucket managed by Amazon Web Services.  Exports might provide an estimate of fees and savings based on certain information that you provide. Fee estimates do not include any taxes that might apply. Your actual fees and savings depend on a variety of factors, including your actual usage of Amazon Web Services services, which might vary from the estimates provided in this report.  If you do not specify preferences or agentIds in the filter, a summary of all servers, applications, tags, and performance is generated. This data is an aggregation of all server data collected through on-premises tooling, file import, application grouping and applying tags. If you specify agentIds in a filter, the task exports up to 72 hours of detailed data collected by the identified Application Discovery Agent, including network, process, and performance details. A time range for exported agent data may be set by using startTime and endTime. Export of detailed agent data is limited to five concurrently running exports. Export of detailed agent data is limited to two exports per day. If you enable ec2RecommendationsPreferences in preferences , an Amazon EC2 instance matching the characteristics of each server in Application Discovery Service is generated. Changing the attributes of the ec2RecommendationsPreferences changes the criteria of the recommendation. |
| POST | / | Starts an import task, which allows you to import details of your on-premises environment directly into Amazon Web Services Migration Hub without having to use the Amazon Web Services Application Discovery Service (Application Discovery Service) tools such as the Amazon Web Services Application Discovery Service Agentless Collector or Application Discovery Agent. This gives you the option to perform migration assessment and planning directly from your imported data, including the ability to group your devices as applications and track their migration status. To start an import request, do this:   Download the specially formatted comma separated value (CSV) import template, which you can find here: https://s3.us-west-2.amazonaws.com/templates-7cffcf56-bd96-4b1c-b45b-a5b42f282e46/import_template.csv.   Fill out the template with your server and application data.   Upload your import file to an Amazon S3 bucket, and make a note of it's Object URL. Your import file must be in the CSV format.   Use the console or the StartImportTask command with the Amazon Web Services CLI or one of the Amazon Web Services SDKs to import the records from your file.   For more information, including step-by-step procedures, see Migration Hub Import in the Amazon Web Services Application Discovery Service User Guide.  There are limits to the number of import tasks you can create (and delete) in an Amazon Web Services account. For more information, see Amazon Web Services Application Discovery Service Limits in the Amazon Web Services Application Discovery Service User Guide. |
| POST | / | Stop the continuous flow of agent's discovered data into Amazon Athena. |
| POST | / | Instructs the specified agents to stop collecting data. |
| POST | / | Updates metadata about an application. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
