---
name: service-fabric-client-apis
description: "Service Fabric Client APIs API skill. Use when working with Service Fabric Client APIs for $, Nodes, ApplicationTypes. Covers 234 endpoints."
version: 1.0.0
generator: lapsh
---

# Service Fabric Client APIs
API version: 6.5.0.36

## Auth
No authentication required.

## Base URL
http://localhost:19080

## Setup
1. No auth setup needed
2. GET /$/GetClusterManifest -- verify access
3. POST /$/GetClusterHealth -- create first GetClusterHealth

## Endpoints

234 endpoints across 14 groups. See references/api-spec.lap for full details.

### $
| Method | Path | Description |
|--------|------|-------------|
| GET | /$/GetClusterManifest | Get the Service Fabric cluster manifest. |
| GET | /$/GetClusterHealth | Gets the health of a Service Fabric cluster. |
| POST | /$/GetClusterHealth | Gets the health of a Service Fabric cluster using the specified policy. |
| GET | /$/GetClusterHealthChunk | Gets the health of a Service Fabric cluster using health chunks. |
| POST | /$/GetClusterHealthChunk | Gets the health of a Service Fabric cluster using health chunks. |
| POST | /$/ReportClusterHealth | Sends a health report on the Service Fabric cluster. |
| GET | /$/GetProvisionedCodeVersions | Gets a list of fabric code versions that are provisioned in a Service Fabric cluster. |
| GET | /$/GetProvisionedConfigVersions | Gets a list of fabric config versions that are provisioned in a Service Fabric cluster. |
| GET | /$/GetUpgradeProgress | Gets the progress of the current cluster upgrade. |
| GET | /$/GetClusterConfiguration | Get the Service Fabric standalone cluster configuration. |
| GET | /$/GetClusterConfigurationUpgradeStatus | Get the cluster configuration upgrade status of a Service Fabric standalone cluster. |
| GET | /$/GetUpgradeOrchestrationServiceState | Get the service state of Service Fabric Upgrade Orchestration Service. |
| POST | /$/SetUpgradeOrchestrationServiceState | Update the service state of Service Fabric Upgrade Orchestration Service. |
| POST | /$/Provision | Provision the code or configuration packages of a Service Fabric cluster. |
| POST | /$/Unprovision | Unprovision the code or configuration packages of a Service Fabric cluster. |
| POST | /$/RollbackUpgrade | Roll back the upgrade of a Service Fabric cluster. |
| POST | /$/MoveToNextUpgradeDomain | Make the cluster upgrade move on to the next upgrade domain. |
| POST | /$/Upgrade | Start upgrading the code or configuration version of a Service Fabric cluster. |
| POST | /$/StartClusterConfigurationUpgrade | Start upgrading the configuration of a Service Fabric standalone cluster. |
| POST | /$/UpdateUpgrade | Update the upgrade parameters of a Service Fabric cluster upgrade. |
| GET | /$/GetAadMetadata | Gets the Azure Active Directory metadata used for secured connection to cluster. |
| GET | /$/GetClusterVersion | Get the current Service Fabric cluster version. |
| GET | /$/GetLoadInformation | Gets the load of a Service Fabric cluster. |
| POST | /$/ToggleVerboseServicePlacementHealthReporting | Changes the verbosity of service placement health reporting. |
| POST | /$/RecoverSystemPartitions | Indicates to the Service Fabric cluster that it should attempt to recover the system services that are currently stuck in quorum loss. |
| POST | /$/RecoverAllPartitions | Indicates to the Service Fabric cluster that it should attempt to recover any services (including system services) which are currently stuck in quorum loss. |
| POST | /$/CreateRepairTask | Creates a new repair task. |
| POST | /$/CancelRepairTask | Requests the cancellation of the given repair task. |
| POST | /$/DeleteRepairTask | Deletes a completed repair task. |
| GET | /$/GetRepairTaskList | Gets a list of repair tasks matching the given filters. |
| POST | /$/ForceApproveRepairTask | Forces the approval of the given repair task. |
| POST | /$/UpdateRepairTaskHealthPolicy | Updates the health policy of the given repair task. |
| POST | /$/UpdateRepairExecutionState | Updates the execution state of a repair task. |
| POST | /$/InvokeInfrastructureCommand | Invokes an administrative command on the given Infrastructure Service instance. |
| GET | /$/InvokeInfrastructureQuery | Invokes a read-only query on the given infrastructure service instance. |

### Nodes
| Method | Path | Description |
|--------|------|-------------|
| GET | /Nodes | Gets the list of nodes in the Service Fabric cluster. |
| GET | /Nodes/{nodeName} | Gets the information about a specific node in the Service Fabric cluster. |
| GET | /Nodes/{nodeName}/$/GetHealth | Gets the health of a Service Fabric node. |
| POST | /Nodes/{nodeName}/$/GetHealth | Gets the health of a Service Fabric node, by using the specified health policy. |
| POST | /Nodes/{nodeName}/$/ReportHealth | Sends a health report on the Service Fabric node. |
| GET | /Nodes/{nodeName}/$/GetLoadInformation | Gets the load information of a Service Fabric node. |
| POST | /Nodes/{nodeName}/$/Deactivate | Deactivate a Service Fabric cluster node with the specified deactivation intent. |
| POST | /Nodes/{nodeName}/$/Activate | Activate a Service Fabric cluster node that is currently deactivated. |
| POST | /Nodes/{nodeName}/$/RemoveNodeState | Notifies Service Fabric that the persisted state on a node has been permanently removed or lost. |
| POST | /Nodes/{nodeName}/$/Restart | Restarts a Service Fabric cluster node. |
| GET | /Nodes/{nodeName}/$/GetApplications/{applicationId}/$/GetServiceTypes | Gets the list containing the information about service types from the applications deployed on a node in a Service Fabric cluster. |
| GET | /Nodes/{nodeName}/$/GetApplications/{applicationId}/$/GetServiceTypes/{serviceTypeName} | Gets the information about a specified service type of the application deployed on a node in a Service Fabric cluster. |
| GET | /Nodes/{nodeName}/$/GetApplications | Gets the list of applications deployed on a Service Fabric node. |
| GET | /Nodes/{nodeName}/$/GetApplications/{applicationId} | Gets the information about an application deployed on a Service Fabric node. |
| GET | /Nodes/{nodeName}/$/GetApplications/{applicationId}/$/GetHealth | Gets the information about health of an application deployed on a Service Fabric node. |
| POST | /Nodes/{nodeName}/$/GetApplications/{applicationId}/$/GetHealth | Gets the information about health of an application deployed on a Service Fabric node. using the specified policy. |
| POST | /Nodes/{nodeName}/$/GetApplications/{applicationId}/$/ReportHealth | Sends a health report on the Service Fabric application deployed on a Service Fabric node. |
| GET | /Nodes/{nodeName}/$/GetApplications/{applicationId}/$/GetReplicas | Gets the list of replicas deployed on a Service Fabric node. |
| GET | /Nodes/{nodeName}/$/GetPartitions/{partitionId}/$/GetReplicas/{replicaId}/$/GetDetail | Gets the details of replica deployed on a Service Fabric node. |
| GET | /Nodes/{nodeName}/$/GetPartitions/{partitionId}/$/GetReplicas | Gets the details of replica deployed on a Service Fabric node. |
| POST | /Nodes/{nodeName}/$/GetPartitions/{partitionId}/$/GetReplicas/{replicaId}/$/Restart | Restarts a service replica of a persisted service running on a node. |
| POST | /Nodes/{nodeName}/$/GetPartitions/{partitionId}/$/GetReplicas/{replicaId}/$/Delete | Removes a service replica running on a node. |
| GET | /Nodes/{nodeName}/$/GetApplications/{applicationId}/$/GetServicePackages | Gets the list of service packages deployed on a Service Fabric node. |
| GET | /Nodes/{nodeName}/$/GetApplications/{applicationId}/$/GetServicePackages/{servicePackageName} | Gets the list of service packages deployed on a Service Fabric node matching exactly the specified name. |
| GET | /Nodes/{nodeName}/$/GetApplications/{applicationId}/$/GetServicePackages/{servicePackageName}/$/GetHealth | Gets the information about health of a service package for a specific application deployed for a Service Fabric node and application. |
| POST | /Nodes/{nodeName}/$/GetApplications/{applicationId}/$/GetServicePackages/{servicePackageName}/$/GetHealth | Gets the information about health of service package for a specific application deployed on a Service Fabric node using the specified policy. |
| POST | /Nodes/{nodeName}/$/GetApplications/{applicationId}/$/GetServicePackages/{servicePackageName}/$/ReportHealth | Sends a health report on the Service Fabric deployed service package. |
| POST | /Nodes/{nodeName}/$/DeployServicePackage | Downloads all of the code packages associated with specified service manifest on the specified node. |
| GET | /Nodes/{nodeName}/$/GetApplications/{applicationId}/$/GetCodePackages | Gets the list of code packages deployed on a Service Fabric node. |
| POST | /Nodes/{nodeName}/$/GetApplications/{applicationId}/$/GetCodePackages/$/Restart | Restarts a code package deployed on a Service Fabric node in a cluster. |
| GET | /Nodes/{nodeName}/$/GetApplications/{applicationId}/$/GetCodePackages/$/ContainerLogs | Gets the container logs for container deployed on a Service Fabric node. |
| POST | /Nodes/{nodeName}/$/GetApplications/{applicationId}/$/GetCodePackages/$/ContainerApi | Invoke container API on a container deployed on a Service Fabric node. |

### ApplicationTypes
| Method | Path | Description |
|--------|------|-------------|
| GET | /ApplicationTypes | Gets the list of application types in the Service Fabric cluster. |
| GET | /ApplicationTypes/{applicationTypeName} | Gets the list of application types in the Service Fabric cluster matching exactly the specified name. |
| POST | /ApplicationTypes/$/Provision | Provisions or registers a Service Fabric application type with the cluster using the '.sfpkg' package in the external store or using the application package in the image store. |
| POST | /ApplicationTypes/{applicationTypeName}/$/Unprovision | Removes or unregisters a Service Fabric application type from the cluster. |
| GET | /ApplicationTypes/{applicationTypeName}/$/GetServiceTypes | Gets the list containing the information about service types that are supported by a provisioned application type in a Service Fabric cluster. |
| GET | /ApplicationTypes/{applicationTypeName}/$/GetServiceTypes/{serviceTypeName} | Gets the information about a specific service type that is supported by a provisioned application type in a Service Fabric cluster. |
| GET | /ApplicationTypes/{applicationTypeName}/$/GetServiceManifest | Gets the manifest describing a service type. |
| GET | /ApplicationTypes/{applicationTypeName}/$/GetApplicationManifest | Gets the manifest describing an application type. |

### Applications
| Method | Path | Description |
|--------|------|-------------|
| POST | /Applications/$/Create | Creates a Service Fabric application. |
| POST | /Applications/{applicationId}/$/Delete | Deletes an existing Service Fabric application. |
| GET | /Applications/{applicationId}/$/GetLoadInformation | Gets load information about a Service Fabric application. |
| GET | /Applications | Gets the list of applications created in the Service Fabric cluster that match the specified filters. |
| GET | /Applications/{applicationId} | Gets information about a Service Fabric application. |
| GET | /Applications/{applicationId}/$/GetHealth | Gets the health of the service fabric application. |
| POST | /Applications/{applicationId}/$/GetHealth | Gets the health of a Service Fabric application using the specified policy. |
| POST | /Applications/{applicationId}/$/ReportHealth | Sends a health report on the Service Fabric application. |
| POST | /Applications/{applicationId}/$/Upgrade | Starts upgrading an application in the Service Fabric cluster. |
| GET | /Applications/{applicationId}/$/GetUpgradeProgress | Gets details for the latest upgrade performed on this application. |
| POST | /Applications/{applicationId}/$/UpdateUpgrade | Updates an ongoing application upgrade in the Service Fabric cluster. |
| POST | /Applications/{applicationId}/$/MoveToNextUpgradeDomain | Resumes upgrading an application in the Service Fabric cluster. |
| POST | /Applications/{applicationId}/$/RollbackUpgrade | Starts rolling back the currently on-going upgrade of an application in the Service Fabric cluster. |
| GET | /Applications/{applicationId}/$/GetServices | Gets the information about all services belonging to the application specified by the application ID. |
| GET | /Applications/{applicationId}/$/GetServices/{serviceId} | Gets the information about the specific service belonging to the Service Fabric application. |
| POST | /Applications/{applicationId}/$/GetServices/$/Create | Creates the specified Service Fabric service. |
| POST | /Applications/{applicationId}/$/GetServices/$/CreateFromTemplate | Creates a Service Fabric service from the service template. |
| POST | /Applications/{applicationId}/$/EnableBackup | Enables periodic backup of stateful partitions under this Service Fabric application. |
| POST | /Applications/{applicationId}/$/DisableBackup | Disables periodic backup of Service Fabric application. |
| GET | /Applications/{applicationId}/$/GetBackupConfigurationInfo | Gets the Service Fabric application backup configuration information. |
| GET | /Applications/{applicationId}/$/GetBackups | Gets the list of backups available for every partition in this application. |
| POST | /Applications/{applicationId}/$/SuspendBackup | Suspends periodic backup for the specified Service Fabric application. |
| POST | /Applications/{applicationId}/$/ResumeBackup | Resumes periodic backup of a Service Fabric application which was previously suspended. |

### Services
| Method | Path | Description |
|--------|------|-------------|
| GET | /Services/{serviceId}/$/GetApplicationName | Gets the name of the Service Fabric application for a service. |
| POST | /Services/{serviceId}/$/Delete | Deletes an existing Service Fabric service. |
| POST | /Services/{serviceId}/$/Update | Updates a Service Fabric service using the specified update description. |
| GET | /Services/{serviceId}/$/GetDescription | Gets the description of an existing Service Fabric service. |
| GET | /Services/{serviceId}/$/GetHealth | Gets the health of the specified Service Fabric service. |
| POST | /Services/{serviceId}/$/GetHealth | Gets the health of the specified Service Fabric service, by using the specified health policy. |
| POST | /Services/{serviceId}/$/ReportHealth | Sends a health report on the Service Fabric service. |
| GET | /Services/{serviceId}/$/ResolvePartition | Resolve a Service Fabric partition. |
| GET | /Services/{serviceId}/$/GetUnplacedReplicaInformation | Gets the information about unplaced replica of the service. |
| GET | /Services/{serviceId}/$/GetPartitions | Gets the list of partitions of a Service Fabric service. |
| POST | /Services/$/{serviceId}/$/GetPartitions/$/Recover | Indicates to the Service Fabric cluster that it should attempt to recover the specified service that is currently stuck in quorum loss. |
| POST | /Services/{serviceId}/$/EnableBackup | Enables periodic backup of stateful partitions under this Service Fabric service. |
| POST | /Services/{serviceId}/$/DisableBackup | Disables periodic backup of Service Fabric service which was previously enabled. |
| GET | /Services/{serviceId}/$/GetBackupConfigurationInfo | Gets the Service Fabric service backup configuration information. |
| GET | /Services/{serviceId}/$/GetBackups | Gets the list of backups available for every partition in this service. |
| POST | /Services/{serviceId}/$/SuspendBackup | Suspends periodic backup for the specified Service Fabric service. |
| POST | /Services/{serviceId}/$/ResumeBackup | Resumes periodic backup of a Service Fabric service which was previously suspended. |

### Partitions
| Method | Path | Description |
|--------|------|-------------|
| GET | /Partitions/{partitionId} | Gets the information about a Service Fabric partition. |
| GET | /Partitions/{partitionId}/$/GetServiceName | Gets the name of the Service Fabric service for a partition. |
| GET | /Partitions/{partitionId}/$/GetHealth | Gets the health of the specified Service Fabric partition. |
| POST | /Partitions/{partitionId}/$/GetHealth | Gets the health of the specified Service Fabric partition, by using the specified health policy. |
| POST | /Partitions/{partitionId}/$/ReportHealth | Sends a health report on the Service Fabric partition. |
| GET | /Partitions/{partitionId}/$/GetLoadInformation | Gets the load information of the specified Service Fabric partition. |
| POST | /Partitions/{partitionId}/$/ResetLoad | Resets the current load of a Service Fabric partition. |
| POST | /Partitions/{partitionId}/$/Recover | Indicates to the Service Fabric cluster that it should attempt to recover a specific partition that is currently stuck in quorum loss. |
| POST | /Partitions/{partitionId}/$/MovePrimaryReplica | Moves the primary replica of a partition of a stateful service. |
| POST | /Partitions/{partitionId}/$/MoveSecondaryReplica | Moves the secondary replica of a partition of a stateful service. |
| GET | /Partitions/{partitionId}/$/GetReplicas | Gets the information about replicas of a Service Fabric service partition. |
| GET | /Partitions/{partitionId}/$/GetReplicas/{replicaId} | Gets the information about a replica of a Service Fabric partition. |
| GET | /Partitions/{partitionId}/$/GetReplicas/{replicaId}/$/GetHealth | Gets the health of a Service Fabric stateful service replica or stateless service instance. |
| POST | /Partitions/{partitionId}/$/GetReplicas/{replicaId}/$/GetHealth | Gets the health of a Service Fabric stateful service replica or stateless service instance using the specified policy. |
| POST | /Partitions/{partitionId}/$/GetReplicas/{replicaId}/$/ReportHealth | Sends a health report on the Service Fabric replica. |
| POST | /Partitions/{partitionId}/$/EnableBackup | Enables periodic backup of the stateful persisted partition. |
| POST | /Partitions/{partitionId}/$/DisableBackup | Disables periodic backup of Service Fabric partition which was previously enabled. |
| GET | /Partitions/{partitionId}/$/GetBackupConfigurationInfo | Gets the partition backup configuration information |
| GET | /Partitions/{partitionId}/$/GetBackups | Gets the list of backups available for the specified partition. |
| POST | /Partitions/{partitionId}/$/SuspendBackup | Suspends periodic backup for the specified partition. |
| POST | /Partitions/{partitionId}/$/ResumeBackup | Resumes periodic backup of partition which was previously suspended. |
| POST | /Partitions/{partitionId}/$/Backup | Triggers backup of the partition's state. |
| GET | /Partitions/{partitionId}/$/GetBackupProgress | Gets details for the latest backup triggered for this partition. |
| POST | /Partitions/{partitionId}/$/Restore | Triggers restore of the state of the partition using the specified restore partition description. |
| GET | /Partitions/{partitionId}/$/GetRestoreProgress | Gets details for the latest restore operation triggered for this partition. |

### ComposeDeployments
| Method | Path | Description |
|--------|------|-------------|
| PUT | /ComposeDeployments/$/Create | Creates a Service Fabric compose deployment. |
| GET | /ComposeDeployments/{deploymentName} | Gets information about a Service Fabric compose deployment. |
| GET | /ComposeDeployments | Gets the list of compose deployments created in the Service Fabric cluster. |
| GET | /ComposeDeployments/{deploymentName}/$/GetUpgradeProgress | Gets details for the latest upgrade performed on this Service Fabric compose deployment. |
| POST | /ComposeDeployments/{deploymentName}/$/Delete | Deletes an existing Service Fabric compose deployment from cluster. |
| POST | /ComposeDeployments/{deploymentName}/$/Upgrade | Starts upgrading a compose deployment in the Service Fabric cluster. |
| POST | /ComposeDeployments/{deploymentName}/$/RollbackUpgrade | Starts rolling back a compose deployment upgrade in the Service Fabric cluster. |

### Tools
| Method | Path | Description |
|--------|------|-------------|
| GET | /Tools/Chaos | Get the status of Chaos. |
| POST | /Tools/Chaos/$/Start | Starts Chaos in the cluster. |
| POST | /Tools/Chaos/$/Stop | Stops Chaos if it is running in the cluster and put the Chaos Schedule in a stopped state. |
| GET | /Tools/Chaos/Events | Gets the next segment of the Chaos events based on the continuation token or the time range. |
| GET | /Tools/Chaos/Schedule | Get the Chaos Schedule defining when and how to run Chaos. |
| POST | /Tools/Chaos/Schedule | Set the schedule used by Chaos. |

### ImageStore
| Method | Path | Description |
|--------|------|-------------|
| PUT | /ImageStore/{contentPath} | Uploads contents of the file to the image store. |
| GET | /ImageStore/{contentPath} | Gets the image store content information. |
| DELETE | /ImageStore/{contentPath} | Deletes existing image store content. |
| GET | /ImageStore | Gets the content information at the root of the image store. |
| POST | /ImageStore/$/Copy | Copies image store content internally |
| DELETE | /ImageStore/$/DeleteUploadSession | Cancels an image store upload session. |
| POST | /ImageStore/$/CommitUploadSession | Commit an image store upload session. |
| GET | /ImageStore/$/GetUploadSession | Get the image store upload session by ID. |
| GET | /ImageStore/{contentPath}/$/GetUploadSession | Get the image store upload session by relative path. |
| PUT | /ImageStore/{contentPath}/$/UploadChunk | Uploads a file chunk to the image store relative path. |
| GET | /ImageStore/$/FolderSize | Get the folder size at the root of the image store. |
| GET | /ImageStore/{contentPath}/$/FolderSize | Get the size of a folder in image store |

### Faults
| Method | Path | Description |
|--------|------|-------------|
| POST | /Faults/Services/{serviceId}/$/GetPartitions/{partitionId}/$/StartDataLoss | This API will induce data loss for the specified partition. It will trigger a call to the OnDataLossAsync API of the partition. |
| GET | /Faults/Services/{serviceId}/$/GetPartitions/{partitionId}/$/GetDataLossProgress | Gets the progress of a partition data loss operation started using the StartDataLoss API. |
| POST | /Faults/Services/{serviceId}/$/GetPartitions/{partitionId}/$/StartQuorumLoss | Induces quorum loss for a given stateful service partition. |
| GET | /Faults/Services/{serviceId}/$/GetPartitions/{partitionId}/$/GetQuorumLossProgress | Gets the progress of a quorum loss operation on a partition started using the StartQuorumLoss API. |
| POST | /Faults/Services/{serviceId}/$/GetPartitions/{partitionId}/$/StartRestart | This API will restart some or all replicas or instances of the specified partition. |
| GET | /Faults/Services/{serviceId}/$/GetPartitions/{partitionId}/$/GetRestartProgress | Gets the progress of a PartitionRestart operation started using StartPartitionRestart. |
| POST | /Faults/Nodes/{nodeName}/$/StartTransition/ | Starts or stops a cluster node. |
| GET | /Faults/Nodes/{nodeName}/$/GetTransitionProgress | Gets the progress of an operation started using StartNodeTransition. |
| GET | /Faults/ | Gets a list of user-induced fault operations filtered by provided input. |
| POST | /Faults/$/Cancel | Cancels a user-induced fault operation. |

### BackupRestore
| Method | Path | Description |
|--------|------|-------------|
| POST | /BackupRestore/BackupPolicies/$/Create | Creates a backup policy. |
| POST | /BackupRestore/BackupPolicies/{backupPolicyName}/$/Delete | Deletes the backup policy. |
| GET | /BackupRestore/BackupPolicies | Gets all the backup policies configured. |
| GET | /BackupRestore/BackupPolicies/{backupPolicyName} | Gets a particular backup policy by name. |
| GET | /BackupRestore/BackupPolicies/{backupPolicyName}/$/GetBackupEnabledEntities | Gets the list of backup entities that are associated with this policy. |
| POST | /BackupRestore/BackupPolicies/{backupPolicyName}/$/Update | Updates the backup policy. |
| POST | /BackupRestore/$/GetBackups | Gets the list of backups available for the specified backed up entity at the specified backup location. |

### Names
| Method | Path | Description |
|--------|------|-------------|
| POST | /Names/$/Create | Creates a Service Fabric name. |
| GET | /Names/{nameId} | Returns whether the Service Fabric name exists. |
| DELETE | /Names/{nameId} | Deletes a Service Fabric name. |
| GET | /Names/{nameId}/$/GetSubNames | Enumerates all the Service Fabric names under a given name. |
| GET | /Names/{nameId}/$/GetProperties | Gets information on all Service Fabric properties under a given name. |
| PUT | /Names/{nameId}/$/GetProperty | Creates or updates a Service Fabric property. |
| GET | /Names/{nameId}/$/GetProperty | Gets the specified Service Fabric property. |
| DELETE | /Names/{nameId}/$/GetProperty | Deletes the specified Service Fabric property. |
| POST | /Names/{nameId}/$/GetProperties/$/SubmitBatch | Submits a property batch. |

### EventsStore
| Method | Path | Description |
|--------|------|-------------|
| GET | /EventsStore/Cluster/Events | Gets all Cluster-related events. |
| GET | /EventsStore/Containers/Events | Gets all Containers-related events. |
| GET | /EventsStore/Nodes/{nodeName}/$/Events | Gets a Node-related events. |
| GET | /EventsStore/Nodes/Events | Gets all Nodes-related Events. |
| GET | /EventsStore/Applications/{applicationId}/$/Events | Gets an Application-related events. |
| GET | /EventsStore/Applications/Events | Gets all Applications-related events. |
| GET | /EventsStore/Services/{serviceId}/$/Events | Gets a Service-related events. |
| GET | /EventsStore/Services/Events | Gets all Services-related events. |
| GET | /EventsStore/Partitions/{partitionId}/$/Events | Gets a Partition-related events. |
| GET | /EventsStore/Partitions/Events | Gets all Partitions-related events. |
| GET | /EventsStore/Partitions/{partitionId}/$/Replicas/{replicaId}/$/Events | Gets a Partition Replica-related events. |
| GET | /EventsStore/Partitions/{partitionId}/$/Replicas/Events | Gets all Replicas-related events for a Partition. |
| GET | /EventsStore/CorrelatedEvents/{eventInstanceId}/$/Events | Gets all correlated events for a given event. |

### Resources
| Method | Path | Description |
|--------|------|-------------|
| PUT | /Resources/Secrets/{secretResourceName} | Creates or updates a Secret resource. |
| GET | /Resources/Secrets/{secretResourceName} | Gets the Secret resource with the given name. |
| DELETE | /Resources/Secrets/{secretResourceName} | Deletes the Secret resource. |
| GET | /Resources/Secrets | Lists all the secret resources. |
| PUT | /Resources/Secrets/{secretResourceName}/values/{secretValueResourceName} | Adds the specified value as a new version of the specified secret resource. |
| GET | /Resources/Secrets/{secretResourceName}/values/{secretValueResourceName} | Gets the specified secret value resource. |
| DELETE | /Resources/Secrets/{secretResourceName}/values/{secretValueResourceName} | Deletes the specified  value of the named secret resource. |
| GET | /Resources/Secrets/{secretResourceName}/values | List names of all values of the specified secret resource. |
| POST | /Resources/Secrets/{secretResourceName}/values/{secretValueResourceName}/list_value | Lists the specified value of the secret resource. |
| PUT | /Resources/Volumes/{volumeResourceName} | Creates or updates a Volume resource. |
| GET | /Resources/Volumes/{volumeResourceName} | Gets the Volume resource with the given name. |
| DELETE | /Resources/Volumes/{volumeResourceName} | Deletes the Volume resource. |
| GET | /Resources/Volumes | Lists all the volume resources. |
| PUT | /Resources/Networks/{networkResourceName} | Creates or updates a Network resource. |
| GET | /Resources/Networks/{networkResourceName} | Gets the Network resource with the given name. |
| DELETE | /Resources/Networks/{networkResourceName} | Deletes the Network resource. |
| GET | /Resources/Networks | Lists all the network resources. |
| PUT | /Resources/Applications/{applicationResourceName} | Creates or updates a Application resource. |
| GET | /Resources/Applications/{applicationResourceName} | Gets the Application resource with the given name. |
| DELETE | /Resources/Applications/{applicationResourceName} | Deletes the Application resource. |
| GET | /Resources/Applications | Lists all the application resources. |
| GET | /Resources/Applications/{applicationResourceName}/Services/{serviceResourceName} | Gets the Service resource with the given name. |
| GET | /Resources/Applications/{applicationResourceName}/Services | Lists all the service resources. |
| GET | /Resources/Applications/{applicationResourceName}/Services/{serviceResourceName}/Replicas/{replicaName}/CodePackages/{codePackageName}/Logs | Gets the logs from the container. |
| GET | /Resources/Applications/{applicationResourceName}/Services/{serviceResourceName}/Replicas/{replicaName} | Gets the given replica of the service of an application. |
| GET | /Resources/Applications/{applicationResourceName}/Services/{serviceResourceName}/Replicas | Lists all the replicas of a service. |
| PUT | /Resources/Gateways/{gatewayResourceName} | Creates or updates a Gateway resource. |
| GET | /Resources/Gateways/{gatewayResourceName} | Gets the Gateway resource with the given name. |
| DELETE | /Resources/Gateways/{gatewayResourceName} | Deletes the Gateway resource. |
| GET | /Resources/Gateways | Lists all the gateway resources. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all GetClusterManifest?" -> GET /$/GetClusterManifest
- "List all GetClusterHealth?" -> GET /$/GetClusterHealth
- "Create a GetClusterHealth?" -> POST /$/GetClusterHealth
- "List all GetClusterHealthChunk?" -> GET /$/GetClusterHealthChunk
- "Create a GetClusterHealthChunk?" -> POST /$/GetClusterHealthChunk
- "Create a ReportClusterHealth?" -> POST /$/ReportClusterHealth
- "List all GetProvisionedCodeVersions?" -> GET /$/GetProvisionedCodeVersions
- "List all GetProvisionedConfigVersions?" -> GET /$/GetProvisionedConfigVersions
- "List all GetUpgradeProgress?" -> GET /$/GetUpgradeProgress
- "List all GetClusterConfiguration?" -> GET /$/GetClusterConfiguration
- "List all GetClusterConfigurationUpgradeStatus?" -> GET /$/GetClusterConfigurationUpgradeStatus
- "List all GetUpgradeOrchestrationServiceState?" -> GET /$/GetUpgradeOrchestrationServiceState
- "Create a SetUpgradeOrchestrationServiceState?" -> POST /$/SetUpgradeOrchestrationServiceState
- "Create a Provision?" -> POST /$/Provision
- "Create a Unprovision?" -> POST /$/Unprovision
- "Create a RollbackUpgrade?" -> POST /$/RollbackUpgrade
- "Create a MoveToNextUpgradeDomain?" -> POST /$/MoveToNextUpgradeDomain
- "Create a Upgrade?" -> POST /$/Upgrade
- "Create a StartClusterConfigurationUpgrade?" -> POST /$/StartClusterConfigurationUpgrade
- "Create a UpdateUpgrade?" -> POST /$/UpdateUpgrade
- "List all GetAadMetadata?" -> GET /$/GetAadMetadata
- "List all GetClusterVersion?" -> GET /$/GetClusterVersion
- "List all GetLoadInformation?" -> GET /$/GetLoadInformation
- "Create a ToggleVerboseServicePlacementHealthReporting?" -> POST /$/ToggleVerboseServicePlacementHealthReporting
- "List all Nodes?" -> GET /Nodes
- "Get Node details?" -> GET /Nodes/{nodeName}
- "List all GetHealth?" -> GET /Nodes/{nodeName}/$/GetHealth
- "Create a GetHealth?" -> POST /Nodes/{nodeName}/$/GetHealth
- "Create a ReportHealth?" -> POST /Nodes/{nodeName}/$/ReportHealth
- "List all GetLoadInformation?" -> GET /Nodes/{nodeName}/$/GetLoadInformation
- "Create a Deactivate?" -> POST /Nodes/{nodeName}/$/Deactivate
- "Create a Activate?" -> POST /Nodes/{nodeName}/$/Activate
- "Create a RemoveNodeState?" -> POST /Nodes/{nodeName}/$/RemoveNodeState
- "Create a Restart?" -> POST /Nodes/{nodeName}/$/Restart
- "List all ApplicationTypes?" -> GET /ApplicationTypes
- "Get ApplicationType details?" -> GET /ApplicationTypes/{applicationTypeName}
- "Create a Provision?" -> POST /ApplicationTypes/$/Provision
- "Create a Unprovision?" -> POST /ApplicationTypes/{applicationTypeName}/$/Unprovision
- "List all GetServiceTypes?" -> GET /ApplicationTypes/{applicationTypeName}/$/GetServiceTypes
- "Get GetServiceType details?" -> GET /ApplicationTypes/{applicationTypeName}/$/GetServiceTypes/{serviceTypeName}
- "List all GetServiceManifest?" -> GET /ApplicationTypes/{applicationTypeName}/$/GetServiceManifest
- "List all GetServiceTypes?" -> GET /Nodes/{nodeName}/$/GetApplications/{applicationId}/$/GetServiceTypes
- "Get GetServiceType details?" -> GET /Nodes/{nodeName}/$/GetApplications/{applicationId}/$/GetServiceTypes/{serviceTypeName}
- "Create a Create?" -> POST /Applications/$/Create
- "Create a Delete?" -> POST /Applications/{applicationId}/$/Delete
- "List all GetLoadInformation?" -> GET /Applications/{applicationId}/$/GetLoadInformation
- "List all Applications?" -> GET /Applications
- "Get Application details?" -> GET /Applications/{applicationId}
- "List all GetHealth?" -> GET /Applications/{applicationId}/$/GetHealth
- "Create a GetHealth?" -> POST /Applications/{applicationId}/$/GetHealth
- "Create a ReportHealth?" -> POST /Applications/{applicationId}/$/ReportHealth
- "Create a Upgrade?" -> POST /Applications/{applicationId}/$/Upgrade
- "List all GetUpgradeProgress?" -> GET /Applications/{applicationId}/$/GetUpgradeProgress
- "Create a UpdateUpgrade?" -> POST /Applications/{applicationId}/$/UpdateUpgrade
- "Create a MoveToNextUpgradeDomain?" -> POST /Applications/{applicationId}/$/MoveToNextUpgradeDomain
- "Create a RollbackUpgrade?" -> POST /Applications/{applicationId}/$/RollbackUpgrade
- "List all GetApplications?" -> GET /Nodes/{nodeName}/$/GetApplications
- "Get GetApplication details?" -> GET /Nodes/{nodeName}/$/GetApplications/{applicationId}
- "List all GetHealth?" -> GET /Nodes/{nodeName}/$/GetApplications/{applicationId}/$/GetHealth
- "Create a GetHealth?" -> POST /Nodes/{nodeName}/$/GetApplications/{applicationId}/$/GetHealth
- "Create a ReportHealth?" -> POST /Nodes/{nodeName}/$/GetApplications/{applicationId}/$/ReportHealth
- "List all GetApplicationManifest?" -> GET /ApplicationTypes/{applicationTypeName}/$/GetApplicationManifest
- "List all GetServices?" -> GET /Applications/{applicationId}/$/GetServices
- "Get GetService details?" -> GET /Applications/{applicationId}/$/GetServices/{serviceId}
- "List all GetApplicationName?" -> GET /Services/{serviceId}/$/GetApplicationName
- "Create a Create?" -> POST /Applications/{applicationId}/$/GetServices/$/Create
- "Create a CreateFromTemplate?" -> POST /Applications/{applicationId}/$/GetServices/$/CreateFromTemplate
- "Create a Delete?" -> POST /Services/{serviceId}/$/Delete
- "Create a Update?" -> POST /Services/{serviceId}/$/Update
- "List all GetDescription?" -> GET /Services/{serviceId}/$/GetDescription
- "List all GetHealth?" -> GET /Services/{serviceId}/$/GetHealth
- "Create a GetHealth?" -> POST /Services/{serviceId}/$/GetHealth
- "Create a ReportHealth?" -> POST /Services/{serviceId}/$/ReportHealth
- "List all ResolvePartition?" -> GET /Services/{serviceId}/$/ResolvePartition
- "List all GetUnplacedReplicaInformation?" -> GET /Services/{serviceId}/$/GetUnplacedReplicaInformation
- "List all GetPartitions?" -> GET /Services/{serviceId}/$/GetPartitions
- "Get Partition details?" -> GET /Partitions/{partitionId}
- "List all GetServiceName?" -> GET /Partitions/{partitionId}/$/GetServiceName
- "List all GetHealth?" -> GET /Partitions/{partitionId}/$/GetHealth
- "Create a GetHealth?" -> POST /Partitions/{partitionId}/$/GetHealth
- "Create a ReportHealth?" -> POST /Partitions/{partitionId}/$/ReportHealth
- "List all GetLoadInformation?" -> GET /Partitions/{partitionId}/$/GetLoadInformation
- "Create a ResetLoad?" -> POST /Partitions/{partitionId}/$/ResetLoad
- "Create a Recover?" -> POST /Partitions/{partitionId}/$/Recover
- "Create a Recover?" -> POST /Services/$/{serviceId}/$/GetPartitions/$/Recover
- "Create a RecoverSystemPartition?" -> POST /$/RecoverSystemPartitions
- "Create a RecoverAllPartition?" -> POST /$/RecoverAllPartitions
- "Create a MovePrimaryReplica?" -> POST /Partitions/{partitionId}/$/MovePrimaryReplica
- "Create a MoveSecondaryReplica?" -> POST /Partitions/{partitionId}/$/MoveSecondaryReplica
- "Create a CreateRepairTask?" -> POST /$/CreateRepairTask
- "Create a CancelRepairTask?" -> POST /$/CancelRepairTask
- "Create a DeleteRepairTask?" -> POST /$/DeleteRepairTask
- "List all GetRepairTaskList?" -> GET /$/GetRepairTaskList
- "Create a ForceApproveRepairTask?" -> POST /$/ForceApproveRepairTask
- "Create a UpdateRepairTaskHealthPolicy?" -> POST /$/UpdateRepairTaskHealthPolicy
- "Create a UpdateRepairExecutionState?" -> POST /$/UpdateRepairExecutionState
- "List all GetReplicas?" -> GET /Partitions/{partitionId}/$/GetReplicas
- "Get GetReplica details?" -> GET /Partitions/{partitionId}/$/GetReplicas/{replicaId}
- "List all GetHealth?" -> GET /Partitions/{partitionId}/$/GetReplicas/{replicaId}/$/GetHealth
- "Create a GetHealth?" -> POST /Partitions/{partitionId}/$/GetReplicas/{replicaId}/$/GetHealth
- "Create a ReportHealth?" -> POST /Partitions/{partitionId}/$/GetReplicas/{replicaId}/$/ReportHealth
- "List all GetReplicas?" -> GET /Nodes/{nodeName}/$/GetApplications/{applicationId}/$/GetReplicas
- "List all GetDetail?" -> GET /Nodes/{nodeName}/$/GetPartitions/{partitionId}/$/GetReplicas/{replicaId}/$/GetDetail
- "List all GetReplicas?" -> GET /Nodes/{nodeName}/$/GetPartitions/{partitionId}/$/GetReplicas
- "Create a Restart?" -> POST /Nodes/{nodeName}/$/GetPartitions/{partitionId}/$/GetReplicas/{replicaId}/$/Restart
- "Create a Delete?" -> POST /Nodes/{nodeName}/$/GetPartitions/{partitionId}/$/GetReplicas/{replicaId}/$/Delete
- "List all GetServicePackages?" -> GET /Nodes/{nodeName}/$/GetApplications/{applicationId}/$/GetServicePackages
- "Get GetServicePackage details?" -> GET /Nodes/{nodeName}/$/GetApplications/{applicationId}/$/GetServicePackages/{servicePackageName}
- "List all GetHealth?" -> GET /Nodes/{nodeName}/$/GetApplications/{applicationId}/$/GetServicePackages/{servicePackageName}/$/GetHealth
- "Create a GetHealth?" -> POST /Nodes/{nodeName}/$/GetApplications/{applicationId}/$/GetServicePackages/{servicePackageName}/$/GetHealth
- "Create a ReportHealth?" -> POST /Nodes/{nodeName}/$/GetApplications/{applicationId}/$/GetServicePackages/{servicePackageName}/$/ReportHealth
- "Create a DeployServicePackage?" -> POST /Nodes/{nodeName}/$/DeployServicePackage
- "List all GetCodePackages?" -> GET /Nodes/{nodeName}/$/GetApplications/{applicationId}/$/GetCodePackages
- "Create a Restart?" -> POST /Nodes/{nodeName}/$/GetApplications/{applicationId}/$/GetCodePackages/$/Restart
- "List all ContainerLogs?" -> GET /Nodes/{nodeName}/$/GetApplications/{applicationId}/$/GetCodePackages/$/ContainerLogs
- "Create a ContainerApi?" -> POST /Nodes/{nodeName}/$/GetApplications/{applicationId}/$/GetCodePackages/$/ContainerApi
- "Get ComposeDeployment details?" -> GET /ComposeDeployments/{deploymentName}
- "List all ComposeDeployments?" -> GET /ComposeDeployments
- "List all GetUpgradeProgress?" -> GET /ComposeDeployments/{deploymentName}/$/GetUpgradeProgress
- "Create a Delete?" -> POST /ComposeDeployments/{deploymentName}/$/Delete
- "Create a Upgrade?" -> POST /ComposeDeployments/{deploymentName}/$/Upgrade
- "Create a RollbackUpgrade?" -> POST /ComposeDeployments/{deploymentName}/$/RollbackUpgrade
- "List all Chaos?" -> GET /Tools/Chaos
- "Create a Start?" -> POST /Tools/Chaos/$/Start
- "Create a Stop?" -> POST /Tools/Chaos/$/Stop
- "List all Events?" -> GET /Tools/Chaos/Events
- "List all Schedule?" -> GET /Tools/Chaos/Schedule
- "Create a Schedule?" -> POST /Tools/Chaos/Schedule
- "Update a ImageStore?" -> PUT /ImageStore/{contentPath}
- "Get ImageStore details?" -> GET /ImageStore/{contentPath}
- "Delete a ImageStore?" -> DELETE /ImageStore/{contentPath}
- "List all ImageStore?" -> GET /ImageStore
- "Create a Copy?" -> POST /ImageStore/$/Copy
- "Create a CommitUploadSession?" -> POST /ImageStore/$/CommitUploadSession
- "List all GetUploadSession?" -> GET /ImageStore/$/GetUploadSession
- "List all GetUploadSession?" -> GET /ImageStore/{contentPath}/$/GetUploadSession
- "List all FolderSize?" -> GET /ImageStore/$/FolderSize
- "List all FolderSize?" -> GET /ImageStore/{contentPath}/$/FolderSize
- "Create a InvokeInfrastructureCommand?" -> POST /$/InvokeInfrastructureCommand
- "List all InvokeInfrastructureQuery?" -> GET /$/InvokeInfrastructureQuery
- "Create a StartDataLoss?" -> POST /Faults/Services/{serviceId}/$/GetPartitions/{partitionId}/$/StartDataLoss
- "List all GetDataLossProgress?" -> GET /Faults/Services/{serviceId}/$/GetPartitions/{partitionId}/$/GetDataLossProgress
- "Create a StartQuorumLoss?" -> POST /Faults/Services/{serviceId}/$/GetPartitions/{partitionId}/$/StartQuorumLoss
- "List all GetQuorumLossProgress?" -> GET /Faults/Services/{serviceId}/$/GetPartitions/{partitionId}/$/GetQuorumLossProgress
- "Create a StartRestart?" -> POST /Faults/Services/{serviceId}/$/GetPartitions/{partitionId}/$/StartRestart
- "List all GetRestartProgress?" -> GET /Faults/Services/{serviceId}/$/GetPartitions/{partitionId}/$/GetRestartProgress
- "Create a StartTransition?" -> POST /Faults/Nodes/{nodeName}/$/StartTransition/
- "List all GetTransitionProgress?" -> GET /Faults/Nodes/{nodeName}/$/GetTransitionProgress
- "List all Faults?" -> GET /Faults/
- "Create a Cancel?" -> POST /Faults/$/Cancel
- "Create a Create?" -> POST /BackupRestore/BackupPolicies/$/Create
- "Create a Delete?" -> POST /BackupRestore/BackupPolicies/{backupPolicyName}/$/Delete
- "List all BackupPolicies?" -> GET /BackupRestore/BackupPolicies
- "Get BackupPolicy details?" -> GET /BackupRestore/BackupPolicies/{backupPolicyName}
- "List all GetBackupEnabledEntities?" -> GET /BackupRestore/BackupPolicies/{backupPolicyName}/$/GetBackupEnabledEntities
- "Create a Update?" -> POST /BackupRestore/BackupPolicies/{backupPolicyName}/$/Update
- "Create a EnableBackup?" -> POST /Applications/{applicationId}/$/EnableBackup
- "Create a DisableBackup?" -> POST /Applications/{applicationId}/$/DisableBackup
- "List all GetBackupConfigurationInfo?" -> GET /Applications/{applicationId}/$/GetBackupConfigurationInfo
- "List all GetBackups?" -> GET /Applications/{applicationId}/$/GetBackups
- "Create a SuspendBackup?" -> POST /Applications/{applicationId}/$/SuspendBackup
- "Create a ResumeBackup?" -> POST /Applications/{applicationId}/$/ResumeBackup
- "Create a EnableBackup?" -> POST /Services/{serviceId}/$/EnableBackup
- "Create a DisableBackup?" -> POST /Services/{serviceId}/$/DisableBackup
- "List all GetBackupConfigurationInfo?" -> GET /Services/{serviceId}/$/GetBackupConfigurationInfo
- "List all GetBackups?" -> GET /Services/{serviceId}/$/GetBackups
- "Create a SuspendBackup?" -> POST /Services/{serviceId}/$/SuspendBackup
- "Create a ResumeBackup?" -> POST /Services/{serviceId}/$/ResumeBackup
- "Create a EnableBackup?" -> POST /Partitions/{partitionId}/$/EnableBackup
- "Create a DisableBackup?" -> POST /Partitions/{partitionId}/$/DisableBackup
- "List all GetBackupConfigurationInfo?" -> GET /Partitions/{partitionId}/$/GetBackupConfigurationInfo
- "List all GetBackups?" -> GET /Partitions/{partitionId}/$/GetBackups
- "Create a SuspendBackup?" -> POST /Partitions/{partitionId}/$/SuspendBackup
- "Create a ResumeBackup?" -> POST /Partitions/{partitionId}/$/ResumeBackup
- "Create a Backup?" -> POST /Partitions/{partitionId}/$/Backup
- "List all GetBackupProgress?" -> GET /Partitions/{partitionId}/$/GetBackupProgress
- "Create a Restore?" -> POST /Partitions/{partitionId}/$/Restore
- "List all GetRestoreProgress?" -> GET /Partitions/{partitionId}/$/GetRestoreProgress
- "Create a GetBackup?" -> POST /BackupRestore/$/GetBackups
- "Create a Create?" -> POST /Names/$/Create
- "Get Name details?" -> GET /Names/{nameId}
- "Delete a Name?" -> DELETE /Names/{nameId}
- "List all GetSubNames?" -> GET /Names/{nameId}/$/GetSubNames
- "List all GetProperties?" -> GET /Names/{nameId}/$/GetProperties
- "List all GetProperty?" -> GET /Names/{nameId}/$/GetProperty
- "Create a SubmitBatch?" -> POST /Names/{nameId}/$/GetProperties/$/SubmitBatch
- "List all Events?" -> GET /EventsStore/Cluster/Events
- "List all Events?" -> GET /EventsStore/Containers/Events
- "List all Events?" -> GET /EventsStore/Nodes/{nodeName}/$/Events
- "List all Events?" -> GET /EventsStore/Nodes/Events
- "List all Events?" -> GET /EventsStore/Applications/{applicationId}/$/Events
- "List all Events?" -> GET /EventsStore/Applications/Events
- "List all Events?" -> GET /EventsStore/Services/{serviceId}/$/Events
- "List all Events?" -> GET /EventsStore/Services/Events
- "List all Events?" -> GET /EventsStore/Partitions/{partitionId}/$/Events
- "List all Events?" -> GET /EventsStore/Partitions/Events
- "List all Events?" -> GET /EventsStore/Partitions/{partitionId}/$/Replicas/{replicaId}/$/Events
- "List all Events?" -> GET /EventsStore/Partitions/{partitionId}/$/Replicas/Events
- "List all Events?" -> GET /EventsStore/CorrelatedEvents/{eventInstanceId}/$/Events
- "Update a Secret?" -> PUT /Resources/Secrets/{secretResourceName}
- "Get Secret details?" -> GET /Resources/Secrets/{secretResourceName}
- "Delete a Secret?" -> DELETE /Resources/Secrets/{secretResourceName}
- "List all Secrets?" -> GET /Resources/Secrets
- "Update a value?" -> PUT /Resources/Secrets/{secretResourceName}/values/{secretValueResourceName}
- "Get value details?" -> GET /Resources/Secrets/{secretResourceName}/values/{secretValueResourceName}
- "Delete a value?" -> DELETE /Resources/Secrets/{secretResourceName}/values/{secretValueResourceName}
- "List all values?" -> GET /Resources/Secrets/{secretResourceName}/values
- "Create a list_value?" -> POST /Resources/Secrets/{secretResourceName}/values/{secretValueResourceName}/list_value
- "Update a Volume?" -> PUT /Resources/Volumes/{volumeResourceName}
- "Get Volume details?" -> GET /Resources/Volumes/{volumeResourceName}
- "Delete a Volume?" -> DELETE /Resources/Volumes/{volumeResourceName}
- "List all Volumes?" -> GET /Resources/Volumes
- "Update a Network?" -> PUT /Resources/Networks/{networkResourceName}
- "Get Network details?" -> GET /Resources/Networks/{networkResourceName}
- "Delete a Network?" -> DELETE /Resources/Networks/{networkResourceName}
- "List all Networks?" -> GET /Resources/Networks
- "Update a Application?" -> PUT /Resources/Applications/{applicationResourceName}
- "Get Application details?" -> GET /Resources/Applications/{applicationResourceName}
- "Delete a Application?" -> DELETE /Resources/Applications/{applicationResourceName}
- "List all Applications?" -> GET /Resources/Applications
- "Get Service details?" -> GET /Resources/Applications/{applicationResourceName}/Services/{serviceResourceName}
- "List all Services?" -> GET /Resources/Applications/{applicationResourceName}/Services
- "List all Logs?" -> GET /Resources/Applications/{applicationResourceName}/Services/{serviceResourceName}/Replicas/{replicaName}/CodePackages/{codePackageName}/Logs
- "Get Replica details?" -> GET /Resources/Applications/{applicationResourceName}/Services/{serviceResourceName}/Replicas/{replicaName}
- "List all Replicas?" -> GET /Resources/Applications/{applicationResourceName}/Services/{serviceResourceName}/Replicas
- "Update a Gateway?" -> PUT /Resources/Gateways/{gatewayResourceName}
- "Get Gateway details?" -> GET /Resources/Gateways/{gatewayResourceName}
- "Delete a Gateway?" -> DELETE /Resources/Gateways/{gatewayResourceName}
- "List all Gateways?" -> GET /Resources/Gateways

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
