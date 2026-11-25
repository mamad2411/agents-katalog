---
name: aws-datasync
description: "AWS DataSync API skill. Use when working with AWS DataSync for root. Covers 60 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS DataSync
API version: 2018-11-09

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST / -- create first resource

## Endpoints

60 endpoints across 1 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| POST | / | Creates an Amazon Web Services resource for an on-premises storage system that you want DataSync Discovery to collect information about. |
| POST | / | Stops an DataSync task execution that's in progress. The transfer of some files are abruptly interrupted. File contents that're transferred to the destination might be incomplete or inconsistent with the source files. However, if you start a new task execution using the same task and allow it to finish, file content on the destination will be complete and consistent. This applies to other unexpected failures that interrupt a task execution. In all of these cases, DataSync successfully completes the transfer when you start the next task execution. |
| POST | / | Activates an DataSync agent that you've deployed in your storage environment. The activation process associates the agent with your Amazon Web Services account. If you haven't deployed an agent yet, see the following topics to learn more:    Agent requirements     Create an agent     If you're transferring between Amazon Web Services storage services, you don't need a DataSync agent. |
| POST | / | Creates a transfer location for a Microsoft Azure Blob Storage container. DataSync can use this location as a transfer source or destination. Before you begin, make sure you know how DataSync accesses Azure Blob Storage and works with access tiers and blob types. You also need a DataSync agent that can connect to your container. |
| POST | / | Creates a transfer location for an Amazon EFS file system. DataSync can use this location as a source or destination for transferring data. Before you begin, make sure that you understand how DataSync accesses Amazon EFS file systems. |
| POST | / | Creates a transfer location for an Amazon FSx for Lustre file system. DataSync can use this location as a source or destination for transferring data. Before you begin, make sure that you understand how DataSync accesses FSx for Lustre file systems. |
| POST | / | Creates a transfer location for an Amazon FSx for NetApp ONTAP file system. DataSync can use this location as a source or destination for transferring data. Before you begin, make sure that you understand how DataSync accesses FSx for ONTAP file systems. |
| POST | / | Creates a transfer location for an Amazon FSx for OpenZFS file system. DataSync can use this location as a source or destination for transferring data. Before you begin, make sure that you understand how DataSync accesses FSx for OpenZFS file systems.  Request parameters related to SMB aren't supported with the CreateLocationFsxOpenZfs operation. |
| POST | / | Creates a transfer location for an Amazon FSx for Windows File Server file system. DataSync can use this location as a source or destination for transferring data. Before you begin, make sure that you understand how DataSync accesses FSx for Windows File Server file systems. |
| POST | / | Creates a transfer location for a Hadoop Distributed File System (HDFS). DataSync can use this location as a source or destination for transferring data. Before you begin, make sure that you understand how DataSync accesses HDFS clusters. |
| POST | / | Creates a transfer location for a Network File System (NFS) file server. DataSync can use this location as a source or destination for transferring data. Before you begin, make sure that you understand how DataSync accesses NFS file servers.  If you're copying data to or from an Snowcone device, you can also use CreateLocationNfs to create your transfer location. For more information, see Configuring transfers with Snowcone. |
| POST | / | Creates a transfer location for an object storage system. DataSync can use this location as a source or destination for transferring data. Before you begin, make sure that you understand the prerequisites for DataSync to work with object storage systems. |
| POST | / | Creates a transfer location for an Amazon S3 bucket. DataSync can use this location as a source or destination for transferring data.  Before you begin, make sure that you read the following topics:    Storage class considerations with Amazon S3 locations     Evaluating S3 request costs when using DataSync      For more information, see Configuring transfers with Amazon S3. |
| POST | / | Creates a transfer location for a Server Message Block (SMB) file server. DataSync can use this location as a source or destination for transferring data. Before you begin, make sure that you understand how DataSync accesses SMB file servers. |
| POST | / | Configures a task, which defines where and how DataSync transfers your data. A task includes a source location, destination location, and transfer options (such as bandwidth limits, scheduling, and more).  If you're planning to transfer data to or from an Amazon S3 location, review how DataSync can affect your S3 request charges and the DataSync pricing page before you begin. |
| POST | / | Removes an DataSync agent resource from your Amazon Web Services account. Keep in mind that this operation (which can't be undone) doesn't remove the agent's virtual machine (VM) or Amazon EC2 instance from your storage environment. For next steps, you can delete the VM or instance from your storage environment or reuse it to activate a new agent. |
| POST | / | Deletes a transfer location resource from DataSync. |
| POST | / | Deletes a transfer task resource from DataSync. |
| POST | / | Returns information about an DataSync agent, such as its name, service endpoint type, and status. |
| POST | / | Returns information about a DataSync discovery job. |
| POST | / | Provides details about how an DataSync transfer location for Microsoft Azure Blob Storage is configured. |
| POST | / | Provides details about how an DataSync transfer location for an Amazon EFS file system is configured. |
| POST | / | Provides details about how an DataSync transfer location for an Amazon FSx for Lustre file system is configured. |
| POST | / | Provides details about how an DataSync transfer location for an Amazon FSx for NetApp ONTAP file system is configured.  If your location uses SMB, the DescribeLocationFsxOntap operation doesn't actually return a Password. |
| POST | / | Provides details about how an DataSync transfer location for an Amazon FSx for OpenZFS file system is configured.  Response elements related to SMB aren't supported with the DescribeLocationFsxOpenZfs operation. |
| POST | / | Provides details about how an DataSync transfer location for an Amazon FSx for Windows File Server file system is configured. |
| POST | / | Provides details about how an DataSync transfer location for a Hadoop Distributed File System (HDFS) is configured. |
| POST | / | Provides details about how an DataSync transfer location for a Network File System (NFS) file server is configured. |
| POST | / | Provides details about how an DataSync transfer location for an object storage system is configured. |
| POST | / | Provides details about how an DataSync transfer location for an S3 bucket is configured. |
| POST | / | Provides details about how an DataSync transfer location for a Server Message Block (SMB) file server is configured. |
| POST | / | Returns information about an on-premises storage system that you're using with DataSync Discovery. |
| POST | / | Returns information, including performance data and capacity usage, which DataSync Discovery collects about a specific resource in your-premises storage system. |
| POST | / | Returns information that DataSync Discovery collects about resources in your on-premises storage system. |
| POST | / | Provides information about a task, which defines where and how DataSync transfers your data. |
| POST | / | Provides information about an execution of your DataSync task. You can use this operation to help monitor the progress of an ongoing transfer or check the results of the transfer. |
| POST | / | Creates recommendations about where to migrate your data to in Amazon Web Services. Recommendations are generated based on information that DataSync Discovery collects about your on-premises storage system's resources. For more information, see Recommendations provided by DataSync Discovery. Once generated, you can view your recommendations by using the DescribeStorageSystemResources operation. |
| POST | / | Returns a list of DataSync agents that belong to an Amazon Web Services account in the Amazon Web Services Region specified in the request. With pagination, you can reduce the number of agents returned in a response. If you get a truncated list of agents in a response, the response contains a marker that you can specify in your next request to fetch the next page of agents.  ListAgents is eventually consistent. This means the result of running the operation might not reflect that you just created or deleted an agent. For example, if you create an agent with CreateAgent and then immediately run ListAgents, that agent might not show up in the list right away. In situations like this, you can always confirm whether an agent has been created (or deleted) by using DescribeAgent. |
| POST | / | Provides a list of the existing discovery jobs in the Amazon Web Services Region and Amazon Web Services account where you're using DataSync Discovery. |
| POST | / | Returns a list of source and destination locations. If you have more locations than are returned in a response (that is, the response returns only a truncated list of your agents), the response contains a token that you can specify in your next request to fetch the next page of locations. |
| POST | / | Lists the on-premises storage systems that you're using with DataSync Discovery. |
| POST | / | Returns all the tags associated with an Amazon Web Services resource. |
| POST | / | Returns a list of executions for an DataSync transfer task. |
| POST | / | Returns a list of the DataSync tasks you created. |
| POST | / | Permanently removes a storage system resource from DataSync Discovery, including the associated discovery jobs, collected data, and recommendations. |
| POST | / | Runs a DataSync discovery job on your on-premises storage system. If you haven't added the storage system to DataSync Discovery yet, do this first by using the AddStorageSystem operation. |
| POST | / | Starts an DataSync transfer task. For each task, you can only run one task execution at a time. There are several phases to a task execution. For more information, see Task execution statuses.  If you're planning to transfer data to or from an Amazon S3 location, review how DataSync can affect your S3 request charges and the DataSync pricing page before you begin. |
| POST | / | Stops a running DataSync discovery job. You can stop a discovery job anytime. A job that's stopped before it's scheduled to end likely will provide you some information about your on-premises storage system resources. To get recommendations for a stopped job, you must use the GenerateRecommendations operation. |
| POST | / | Applies a tag to an Amazon Web Services resource. Tags are key-value pairs that can help you manage, filter, and search for your resources. These include DataSync resources, such as locations, tasks, and task executions. |
| POST | / | Removes tags from an Amazon Web Services resource. |
| POST | / | Updates the name of an DataSync agent. |
| POST | / | Edits a DataSync discovery job configuration. |
| POST | / | Modifies some configurations of the Microsoft Azure Blob Storage transfer location that you're using with DataSync. |
| POST | / | Updates some parameters of a previously created location for a Hadoop Distributed File System cluster. |
| POST | / | Modifies some configurations of the Network File System (NFS) transfer location that you're using with DataSync. For more information, see Configuring transfers to or from an NFS file server. |
| POST | / | Updates some parameters of an existing DataSync location for an object storage system. |
| POST | / | Updates some of the parameters of a Server Message Block (SMB) file server location that you can use for DataSync transfers. |
| POST | / | Modifies some configurations of an on-premises storage system resource that you're using with DataSync Discovery. |
| POST | / | Updates the configuration of a task, which defines where and how DataSync transfers your data. |
| POST | / | Updates the configuration of a running DataSync task execution.  Currently, the only Option that you can modify with UpdateTaskExecution is  BytesPerSecond , which throttles bandwidth for a running or queued task execution. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
