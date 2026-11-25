---
name: amazon-emr
description: "Amazon EMR API skill. Use when working with Amazon EMR for root. Covers 56 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon EMR
API version: 2009-03-31

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST / -- create first resource

## Endpoints

56 endpoints across 1 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| POST | / | Adds an instance fleet to a running cluster.  The instance fleet configuration is available only in Amazon EMR releases 4.8.0 and later, excluding 5.0.x. |
| POST | / | Adds one or more instance groups to a running cluster. |
| POST | / | AddJobFlowSteps adds new steps to a running cluster. A maximum of 256 steps are allowed in each job flow. If your cluster is long-running (such as a Hive data warehouse) or complex, you may require more than 256 steps to process your data. You can bypass the 256-step limitation in various ways, including using SSH to connect to the master node and submitting queries directly to the software running on the master node, such as Hive and Hadoop. A step specifies the location of a JAR file stored either on the master node of the cluster or in Amazon S3. Each step is performed by the main function of the main class of the JAR file. The main class can be specified either in the manifest of the JAR or by using the MainFunction parameter of the step. Amazon EMR executes each step in the order listed. For a step to be considered complete, the main function must exit with a zero exit code and all Hadoop jobs started while the step was running must have completed and run successfully. You can only add steps to a cluster that is in one of the following states: STARTING, BOOTSTRAPPING, RUNNING, or WAITING.  The string values passed into HadoopJarStep object cannot exceed a total of 10240 characters. |
| POST | / | Adds tags to an Amazon EMR resource, such as a cluster or an Amazon EMR Studio. Tags make it easier to associate resources in various ways, such as grouping clusters to track your Amazon EMR resource allocation costs. For more information, see Tag Clusters. |
| POST | / | Cancels a pending step or steps in a running cluster. Available only in Amazon EMR versions 4.8.0 and later, excluding version 5.0.0. A maximum of 256 steps are allowed in each CancelSteps request. CancelSteps is idempotent but asynchronous; it does not guarantee that a step will be canceled, even if the request is successfully submitted. When you use Amazon EMR releases 5.28.0 and later, you can cancel steps that are in a PENDING or RUNNING state. In earlier versions of Amazon EMR, you can only cancel steps that are in a PENDING state. |
| POST | / | Creates a security configuration, which is stored in the service and can be specified when a cluster is created. |
| POST | / | Creates a new Amazon EMR Studio. |
| POST | / | Maps a user or group to the Amazon EMR Studio specified by StudioId, and applies a session policy to refine Studio permissions for that user or group. Use CreateStudioSessionMapping to assign users to a Studio when you use IAM Identity Center authentication. For instructions on how to assign users to a Studio when you use IAM authentication, see Assign a user or group to your EMR Studio. |
| POST | / | Deletes a security configuration. |
| POST | / | Removes an Amazon EMR Studio from the Studio metadata store. |
| POST | / | Removes a user or group from an Amazon EMR Studio. |
| POST | / | Provides cluster-level details including status, hardware and software configuration, VPC settings, and so on. |
| POST | / | This API is no longer supported and will eventually be removed. We recommend you use ListClusters, DescribeCluster, ListSteps, ListInstanceGroups and ListBootstrapActions instead. DescribeJobFlows returns a list of job flows that match all of the supplied parameters. The parameters can include a list of job flow IDs, job flow states, and restrictions on job flow creation date and time. Regardless of supplied parameters, only job flows created within the last two months are returned. If no parameters are supplied, then job flows matching either of the following criteria are returned:   Job flows created and completed in the last two weeks    Job flows created within the last two months that are in one of the following states: RUNNING, WAITING, SHUTTING_DOWN, STARTING    Amazon EMR can return a maximum of 512 job flow descriptions. |
| POST | / | Provides details of a notebook execution. |
| POST | / | Provides Amazon EMR release label details, such as the releases available the Region where the API request is run, and the available applications for a specific Amazon EMR release label. Can also list Amazon EMR releases that support a specified version of Spark. |
| POST | / | Provides the details of a security configuration by returning the configuration JSON. |
| POST | / | Provides more detail about the cluster step. |
| POST | / | Returns details for the specified Amazon EMR Studio including ID, Name, VPC, Studio access URL, and so on. |
| POST | / | Returns the auto-termination policy for an Amazon EMR cluster. |
| POST | / | Returns the Amazon EMR block public access configuration for your Amazon Web Services account in the current Region. For more information see Configure Block Public Access for Amazon EMR in the Amazon EMR Management Guide. |
| POST | / | Provides temporary, HTTP basic credentials that are associated with a given runtime IAM role and used by a cluster with fine-grained access control activated. You can use these credentials to connect to cluster endpoints that support username and password authentication. |
| POST | / | Fetches the attached managed scaling policy for an Amazon EMR cluster. |
| POST | / | Fetches mapping details for the specified Amazon EMR Studio and identity (user or group). |
| POST | / | Provides information about the bootstrap actions associated with a cluster. |
| POST | / | Provides the status of all clusters visible to this Amazon Web Services account. Allows you to filter the list of clusters based on certain criteria; for example, filtering by cluster creation date and time or by status. This call returns a maximum of 50 clusters in unsorted order per call, but returns a marker to track the paging of the cluster list across multiple ListClusters calls. |
| POST | / | Lists all available details about the instance fleets in a cluster.  The instance fleet configuration is available only in Amazon EMR releases 4.8.0 and later, excluding 5.0.x versions. |
| POST | / | Provides all available details about the instance groups in a cluster. |
| POST | / | Provides information for all active Amazon EC2 instances and Amazon EC2 instances terminated in the last 30 days, up to a maximum of 2,000. Amazon EC2 instances in any of the following states are considered active: AWAITING_FULFILLMENT, PROVISIONING, BOOTSTRAPPING, RUNNING. |
| POST | / | Provides summaries of all notebook executions. You can filter the list based on multiple criteria such as status, time range, and editor id. Returns a maximum of 50 notebook executions and a marker to track the paging of a longer notebook execution list across multiple ListNotebookExecutions calls. |
| POST | / | Retrieves release labels of Amazon EMR services in the Region where the API is called. |
| POST | / | Lists all the security configurations visible to this account, providing their creation dates and times, and their names. This call returns a maximum of 50 clusters per call, but returns a marker to track the paging of the cluster list across multiple ListSecurityConfigurations calls. |
| POST | / | Provides a list of steps for the cluster in reverse order unless you specify stepIds with the request or filter by StepStates. You can specify a maximum of 10 stepIDs. The CLI automatically paginates results to return a list greater than 50 steps. To return more than 50 steps using the CLI, specify a Marker, which is a pagination token that indicates the next set of steps to retrieve. |
| POST | / | Returns a list of all user or group session mappings for the Amazon EMR Studio specified by StudioId. |
| POST | / | Returns a list of all Amazon EMR Studios associated with the Amazon Web Services account. The list includes details such as ID, Studio Access URL, and creation time for each Studio. |
| POST | / | A list of the instance types that Amazon EMR supports. You can filter the list by Amazon Web Services Region and Amazon EMR release. |
| POST | / | Modifies the number of steps that can be executed concurrently for the cluster specified using ClusterID. |
| POST | / | Modifies the target On-Demand and target Spot capacities for the instance fleet with the specified InstanceFleetID within the cluster specified using ClusterID. The call either succeeds or fails atomically.  The instance fleet configuration is available only in Amazon EMR releases 4.8.0 and later, excluding 5.0.x versions. |
| POST | / | ModifyInstanceGroups modifies the number of nodes and configuration settings of an instance group. The input parameters include the new target instance count for the group and the instance group ID. The call will either succeed or fail atomically. |
| POST | / | Creates or updates an automatic scaling policy for a core instance group or task instance group in an Amazon EMR cluster. The automatic scaling policy defines how an instance group dynamically adds and terminates Amazon EC2 instances in response to the value of a CloudWatch metric. |
| POST | / | Auto-termination is supported in Amazon EMR releases 5.30.0 and 6.1.0 and later. For more information, see Using an auto-termination policy.  Creates or updates an auto-termination policy for an Amazon EMR cluster. An auto-termination policy defines the amount of idle time in seconds after which a cluster automatically terminates. For alternative cluster termination options, see Control cluster termination. |
| POST | / | Creates or updates an Amazon EMR block public access configuration for your Amazon Web Services account in the current Region. For more information see Configure Block Public Access for Amazon EMR in the Amazon EMR Management Guide. |
| POST | / | Creates or updates a managed scaling policy for an Amazon EMR cluster. The managed scaling policy defines the limits for resources, such as Amazon EC2 instances that can be added or terminated from a cluster. The policy only applies to the core and task nodes. The master node cannot be scaled after initial configuration. |
| POST | / | Removes an automatic scaling policy from a specified instance group within an Amazon EMR cluster. |
| POST | / | Removes an auto-termination policy from an Amazon EMR cluster. |
| POST | / | Removes a managed scaling policy from a specified Amazon EMR cluster. |
| POST | / | Removes tags from an Amazon EMR resource, such as a cluster or Amazon EMR Studio. Tags make it easier to associate resources in various ways, such as grouping clusters to track your Amazon EMR resource allocation costs. For more information, see Tag Clusters.  The following example removes the stack tag with value Prod from a cluster: |
| POST | / | RunJobFlow creates and starts running a new cluster (job flow). The cluster runs the steps specified. After the steps complete, the cluster stops and the HDFS partition is lost. To prevent loss of data, configure the last step of the job flow to store results in Amazon S3. If the JobFlowInstancesConfig KeepJobFlowAliveWhenNoSteps parameter is set to TRUE, the cluster transitions to the WAITING state rather than shutting down after the steps have completed.  For additional protection, you can set the JobFlowInstancesConfig TerminationProtected parameter to TRUE to lock the cluster and prevent it from being terminated by API call, user intervention, or in the event of a job flow error. A maximum of 256 steps are allowed in each job flow. If your cluster is long-running (such as a Hive data warehouse) or complex, you may require more than 256 steps to process your data. You can bypass the 256-step limitation in various ways, including using the SSH shell to connect to the master node and submitting queries directly to the software running on the master node, such as Hive and Hadoop. For long-running clusters, we recommend that you periodically store your results.  The instance fleets configuration is available only in Amazon EMR releases 4.8.0 and later, excluding 5.0.x versions. The RunJobFlow request can contain InstanceFleets parameters or InstanceGroups parameters, but not both. |
| POST | / | You can use the SetKeepJobFlowAliveWhenNoSteps to configure a cluster (job flow) to terminate after the step execution, i.e., all your steps are executed. If you want a transient cluster that shuts down after the last of the current executing steps are completed, you can configure SetKeepJobFlowAliveWhenNoSteps to false. If you want a long running cluster, configure SetKeepJobFlowAliveWhenNoSteps to true. For more information, see Managing Cluster Termination in the Amazon EMR Management Guide. |
| POST | / | SetTerminationProtection locks a cluster (job flow) so the Amazon EC2 instances in the cluster cannot be terminated by user intervention, an API call, or in the event of a job-flow error. The cluster still terminates upon successful completion of the job flow. Calling SetTerminationProtection on a cluster is similar to calling the Amazon EC2 DisableAPITermination API on all Amazon EC2 instances in a cluster.  SetTerminationProtection is used to prevent accidental termination of a cluster and to ensure that in the event of an error, the instances persist so that you can recover any data stored in their ephemeral instance storage.  To terminate a cluster that has been locked by setting SetTerminationProtection to true, you must first unlock the job flow by a subsequent call to SetTerminationProtection in which you set the value to false.   For more information, see Managing Cluster Termination in the Amazon EMR Management Guide. |
| POST | / | Specify whether to enable unhealthy node replacement, which lets Amazon EMR gracefully replace core nodes on a cluster if any nodes become unhealthy. For example, a node becomes unhealthy if disk usage is above 90%. If unhealthy node replacement is on and TerminationProtected are off, Amazon EMR immediately terminates the unhealthy core nodes. To use unhealthy node replacement and retain unhealthy core nodes, use to turn on termination protection. In such cases, Amazon EMR adds the unhealthy nodes to a denylist, reducing job interruptions and failures. If unhealthy node replacement is on, Amazon EMR notifies YARN and other applications on the cluster to stop scheduling tasks with these nodes, moves the data, and then terminates the nodes. For more information, see graceful node replacement in the Amazon EMR Management Guide. |
| POST | / | The SetVisibleToAllUsers parameter is no longer supported. Your cluster may be visible to all users in your account. To restrict cluster access using an IAM policy, see Identity and Access Management for Amazon EMR.   Sets the Cluster$VisibleToAllUsers value for an Amazon EMR cluster. When true, IAM principals in the Amazon Web Services account can perform Amazon EMR cluster actions that their IAM policies allow. When false, only the IAM principal that created the cluster and the Amazon Web Services account root user can perform Amazon EMR actions on the cluster, regardless of IAM permissions policies attached to other IAM principals. This action works on running clusters. When you create a cluster, use the RunJobFlowInput$VisibleToAllUsers parameter. For more information, see Understanding the Amazon EMR Cluster VisibleToAllUsers Setting in the Amazon EMR Management Guide. |
| POST | / | Starts a notebook execution. |
| POST | / | Stops a notebook execution. |
| POST | / | TerminateJobFlows shuts a list of clusters (job flows) down. When a job flow is shut down, any step not yet completed is canceled and the Amazon EC2 instances on which the cluster is running are stopped. Any log files not already saved are uploaded to Amazon S3 if a LogUri was specified when the cluster was created. The maximum number of clusters allowed is 10. The call to TerminateJobFlows is asynchronous. Depending on the configuration of the cluster, it may take up to 1-5 minutes for the cluster to completely terminate and release allocated resources, such as Amazon EC2 instances. |
| POST | / | Updates an Amazon EMR Studio configuration, including attributes such as name, description, and subnets. |
| POST | / | Updates the session policy attached to the user or group for the specified Amazon EMR Studio. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
