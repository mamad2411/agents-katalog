---
name: application-migration-service
description: "Application Migration Service API skill. Use when working with Application Migration Service for ArchiveApplication, ArchiveWave, AssociateApplications. Covers 70 endpoints."
version: 1.0.0
generator: lapsh
---

# Application Migration Service
API version: 2020-02-26

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /DescribeVcenterClients -- verify access
3. POST /ArchiveApplication -- create first ArchiveApplication

## Endpoints

70 endpoints across 68 groups. See references/api-spec.lap for full details.

### ArchiveApplication
| Method | Path | Description |
|--------|------|-------------|
| POST | /ArchiveApplication | Archive application. |

### ArchiveWave
| Method | Path | Description |
|--------|------|-------------|
| POST | /ArchiveWave | Archive wave. |

### AssociateApplications
| Method | Path | Description |
|--------|------|-------------|
| POST | /AssociateApplications | Associate applications to wave. |

### AssociateSourceServers
| Method | Path | Description |
|--------|------|-------------|
| POST | /AssociateSourceServers | Associate source servers to application. |

### ChangeServerLifeCycleState
| Method | Path | Description |
|--------|------|-------------|
| POST | /ChangeServerLifeCycleState | Allows the user to set the SourceServer.LifeCycle.state property for specific Source Server IDs to one of the following: READY_FOR_TEST or READY_FOR_CUTOVER. This command only works if the Source Server is already launchable (dataReplicationInfo.lagDuration is not null.) |

### CreateApplication
| Method | Path | Description |
|--------|------|-------------|
| POST | /CreateApplication | Create application. |

### CreateConnector
| Method | Path | Description |
|--------|------|-------------|
| POST | /CreateConnector | Create Connector. |

### CreateLaunchConfigurationTemplate
| Method | Path | Description |
|--------|------|-------------|
| POST | /CreateLaunchConfigurationTemplate | Creates a new Launch Configuration Template. |

### CreateReplicationConfigurationTemplate
| Method | Path | Description |
|--------|------|-------------|
| POST | /CreateReplicationConfigurationTemplate | Creates a new ReplicationConfigurationTemplate. |

### CreateWave
| Method | Path | Description |
|--------|------|-------------|
| POST | /CreateWave | Create wave. |

### DeleteApplication
| Method | Path | Description |
|--------|------|-------------|
| POST | /DeleteApplication | Delete application. |

### DeleteConnector
| Method | Path | Description |
|--------|------|-------------|
| POST | /DeleteConnector | Delete Connector. |

### DeleteJob
| Method | Path | Description |
|--------|------|-------------|
| POST | /DeleteJob | Deletes a single Job by ID. |

### DeleteLaunchConfigurationTemplate
| Method | Path | Description |
|--------|------|-------------|
| POST | /DeleteLaunchConfigurationTemplate | Deletes a single Launch Configuration Template by ID. |

### DeleteReplicationConfigurationTemplate
| Method | Path | Description |
|--------|------|-------------|
| POST | /DeleteReplicationConfigurationTemplate | Deletes a single Replication Configuration Template by ID |

### DeleteSourceServer
| Method | Path | Description |
|--------|------|-------------|
| POST | /DeleteSourceServer | Deletes a single source server by ID. |

### DeleteVcenterClient
| Method | Path | Description |
|--------|------|-------------|
| POST | /DeleteVcenterClient | Deletes a given vCenter client by ID. |

### DeleteWave
| Method | Path | Description |
|--------|------|-------------|
| POST | /DeleteWave | Delete wave. |

### DescribeJobLogItems
| Method | Path | Description |
|--------|------|-------------|
| POST | /DescribeJobLogItems | Retrieves detailed job log items with paging. |

### DescribeJobs
| Method | Path | Description |
|--------|------|-------------|
| POST | /DescribeJobs | Returns a list of Jobs. Use the JobsID and fromDate and toData filters to limit which jobs are returned. The response is sorted by creationDataTime - latest date first. Jobs are normally created by the StartTest, StartCutover, and TerminateTargetInstances APIs. Jobs are also created by DiagnosticLaunch and TerminateDiagnosticInstances, which are APIs available only to *Support* and only used in response to relevant support tickets. |

### DescribeLaunchConfigurationTemplates
| Method | Path | Description |
|--------|------|-------------|
| POST | /DescribeLaunchConfigurationTemplates | Lists all Launch Configuration Templates, filtered by Launch Configuration Template IDs |

### DescribeReplicationConfigurationTemplates
| Method | Path | Description |
|--------|------|-------------|
| POST | /DescribeReplicationConfigurationTemplates | Lists all ReplicationConfigurationTemplates, filtered by Source Server IDs. |

### DescribeSourceServers
| Method | Path | Description |
|--------|------|-------------|
| POST | /DescribeSourceServers | Retrieves all SourceServers or multiple SourceServers by ID. |

### DescribeVcenterClients
| Method | Path | Description |
|--------|------|-------------|
| GET | /DescribeVcenterClients | Returns a list of the installed vCenter clients. |

### DisassociateApplications
| Method | Path | Description |
|--------|------|-------------|
| POST | /DisassociateApplications | Disassociate applications from wave. |

### DisassociateSourceServers
| Method | Path | Description |
|--------|------|-------------|
| POST | /DisassociateSourceServers | Disassociate source servers from application. |

### DisconnectFromService
| Method | Path | Description |
|--------|------|-------------|
| POST | /DisconnectFromService | Disconnects specific Source Servers from Application Migration Service. Data replication is stopped immediately. All AWS resources created by Application Migration Service for enabling the replication of these source servers will be terminated / deleted within 90 minutes. Launched Test or Cutover instances will NOT be terminated. If the agent on the source server has not been prevented from communicating with the Application Migration Service service, then it will receive a command to uninstall itself (within approximately 10 minutes). The following properties of the SourceServer will be changed immediately: dataReplicationInfo.dataReplicationState will be set to DISCONNECTED; The totalStorageBytes property for each of dataReplicationInfo.replicatedDisks will be set to zero; dataReplicationInfo.lagDuration and dataReplicationInfo.lagDuration will be nullified. |

### FinalizeCutover
| Method | Path | Description |
|--------|------|-------------|
| POST | /FinalizeCutover | Finalizes the cutover immediately for specific Source Servers. All AWS resources created by Application Migration Service for enabling the replication of these source servers will be terminated / deleted within 90 minutes. Launched Test or Cutover instances will NOT be terminated. The AWS Replication Agent will receive a command to uninstall itself (within 10 minutes). The following properties of the SourceServer will be changed immediately: dataReplicationInfo.dataReplicationState will be changed to DISCONNECTED; The SourceServer.lifeCycle.state will be changed to CUTOVER; The totalStorageBytes property fo each of dataReplicationInfo.replicatedDisks will be set to zero; dataReplicationInfo.lagDuration and dataReplicationInfo.lagDuration will be nullified. |

### GetLaunchConfiguration
| Method | Path | Description |
|--------|------|-------------|
| POST | /GetLaunchConfiguration | Lists all LaunchConfigurations available, filtered by Source Server IDs. |

### GetReplicationConfiguration
| Method | Path | Description |
|--------|------|-------------|
| POST | /GetReplicationConfiguration | Lists all ReplicationConfigurations, filtered by Source Server ID. |

### InitializeService
| Method | Path | Description |
|--------|------|-------------|
| POST | /InitializeService | Initialize Application Migration Service. |

### ListApplications
| Method | Path | Description |
|--------|------|-------------|
| POST | /ListApplications | Retrieves all applications or multiple applications by ID. |

### ListConnectors
| Method | Path | Description |
|--------|------|-------------|
| POST | /ListConnectors | List Connectors. |

### ListExportErrors
| Method | Path | Description |
|--------|------|-------------|
| POST | /ListExportErrors | List export errors. |

### ListExports
| Method | Path | Description |
|--------|------|-------------|
| POST | /ListExports | List exports. |

### ListImportErrors
| Method | Path | Description |
|--------|------|-------------|
| POST | /ListImportErrors | List import errors. |

### ListImports
| Method | Path | Description |
|--------|------|-------------|
| POST | /ListImports | List imports. |

### ListManagedAccounts
| Method | Path | Description |
|--------|------|-------------|
| POST | /ListManagedAccounts | List Managed Accounts. |

### ListSourceServerActions
| Method | Path | Description |
|--------|------|-------------|
| POST | /ListSourceServerActions | List source server post migration custom actions. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags/{resourceArn} | List all tags for your Application Migration Service resources. |
| POST | /tags/{resourceArn} | Adds or overwrites only the specified tags for the specified Application Migration Service resource or resources. When you specify an existing tag key, the value is overwritten with the new value. Each resource can have a maximum of 50 tags. Each tag consists of a key and optional value. |
| DELETE | /tags/{resourceArn} | Deletes the specified set of tags from the specified set of Application Migration Service resources. |

### ListTemplateActions
| Method | Path | Description |
|--------|------|-------------|
| POST | /ListTemplateActions | List template post migration custom actions. |

### ListWaves
| Method | Path | Description |
|--------|------|-------------|
| POST | /ListWaves | Retrieves all waves or multiple waves by ID. |

### MarkAsArchived
| Method | Path | Description |
|--------|------|-------------|
| POST | /MarkAsArchived | Archives specific Source Servers by setting the SourceServer.isArchived property to true for specified SourceServers by ID. This command only works for SourceServers with a lifecycle. state which equals DISCONNECTED or CUTOVER. |

### PauseReplication
| Method | Path | Description |
|--------|------|-------------|
| POST | /PauseReplication | Pause Replication. |

### PutSourceServerAction
| Method | Path | Description |
|--------|------|-------------|
| POST | /PutSourceServerAction | Put source server post migration custom action. |

### PutTemplateAction
| Method | Path | Description |
|--------|------|-------------|
| POST | /PutTemplateAction | Put template post migration custom action. |

### RemoveSourceServerAction
| Method | Path | Description |
|--------|------|-------------|
| POST | /RemoveSourceServerAction | Remove source server post migration custom action. |

### RemoveTemplateAction
| Method | Path | Description |
|--------|------|-------------|
| POST | /RemoveTemplateAction | Remove template post migration custom action. |

### ResumeReplication
| Method | Path | Description |
|--------|------|-------------|
| POST | /ResumeReplication | Resume Replication. |

### RetryDataReplication
| Method | Path | Description |
|--------|------|-------------|
| POST | /RetryDataReplication | Causes the data replication initiation sequence to begin immediately upon next Handshake for specified SourceServer IDs, regardless of when the previous initiation started. This command will not work if the SourceServer is not stalled or is in a DISCONNECTED or STOPPED state. |

### StartCutover
| Method | Path | Description |
|--------|------|-------------|
| POST | /StartCutover | Launches a Cutover Instance for specific Source Servers. This command starts a LAUNCH job whose initiatedBy property is StartCutover and changes the SourceServer.lifeCycle.state property to CUTTING_OVER. |

### StartExport
| Method | Path | Description |
|--------|------|-------------|
| POST | /StartExport | Start export. |

### StartImport
| Method | Path | Description |
|--------|------|-------------|
| POST | /StartImport | Start import. |

### StartReplication
| Method | Path | Description |
|--------|------|-------------|
| POST | /StartReplication | Starts replication for SNAPSHOT_SHIPPING agents. |

### StartTest
| Method | Path | Description |
|--------|------|-------------|
| POST | /StartTest | Launches a Test Instance for specific Source Servers. This command starts a LAUNCH job whose initiatedBy property is StartTest and changes the SourceServer.lifeCycle.state property to TESTING. |

### StopReplication
| Method | Path | Description |
|--------|------|-------------|
| POST | /StopReplication | Stop Replication. |

### TerminateTargetInstances
| Method | Path | Description |
|--------|------|-------------|
| POST | /TerminateTargetInstances | Starts a job that terminates specific launched EC2 Test and Cutover instances. This command will not work for any Source Server with a lifecycle.state of TESTING, CUTTING_OVER, or CUTOVER. |

### UnarchiveApplication
| Method | Path | Description |
|--------|------|-------------|
| POST | /UnarchiveApplication | Unarchive application. |

### UnarchiveWave
| Method | Path | Description |
|--------|------|-------------|
| POST | /UnarchiveWave | Unarchive wave. |

### UpdateApplication
| Method | Path | Description |
|--------|------|-------------|
| POST | /UpdateApplication | Update application. |

### UpdateConnector
| Method | Path | Description |
|--------|------|-------------|
| POST | /UpdateConnector | Update Connector. |

### UpdateLaunchConfiguration
| Method | Path | Description |
|--------|------|-------------|
| POST | /UpdateLaunchConfiguration | Updates multiple LaunchConfigurations by Source Server ID.  bootMode valid values are LEGACY_BIOS | UEFI |

### UpdateLaunchConfigurationTemplate
| Method | Path | Description |
|--------|------|-------------|
| POST | /UpdateLaunchConfigurationTemplate | Updates an existing Launch Configuration Template by ID. |

### UpdateReplicationConfiguration
| Method | Path | Description |
|--------|------|-------------|
| POST | /UpdateReplicationConfiguration | Allows you to update multiple ReplicationConfigurations by Source Server ID. |

### UpdateReplicationConfigurationTemplate
| Method | Path | Description |
|--------|------|-------------|
| POST | /UpdateReplicationConfigurationTemplate | Updates multiple ReplicationConfigurationTemplates by ID. |

### UpdateSourceServer
| Method | Path | Description |
|--------|------|-------------|
| POST | /UpdateSourceServer | Update Source Server. |

### UpdateSourceServerReplicationType
| Method | Path | Description |
|--------|------|-------------|
| POST | /UpdateSourceServerReplicationType | Allows you to change between the AGENT_BASED replication type and the SNAPSHOT_SHIPPING replication type. |

### UpdateWave
| Method | Path | Description |
|--------|------|-------------|
| POST | /UpdateWave | Update wave. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a ArchiveApplication?" -> POST /ArchiveApplication
- "Create a ArchiveWave?" -> POST /ArchiveWave
- "Create a AssociateApplication?" -> POST /AssociateApplications
- "Create a AssociateSourceServer?" -> POST /AssociateSourceServers
- "Create a ChangeServerLifeCycleState?" -> POST /ChangeServerLifeCycleState
- "Create a CreateApplication?" -> POST /CreateApplication
- "Create a CreateConnector?" -> POST /CreateConnector
- "Create a CreateLaunchConfigurationTemplate?" -> POST /CreateLaunchConfigurationTemplate
- "Create a CreateReplicationConfigurationTemplate?" -> POST /CreateReplicationConfigurationTemplate
- "Create a CreateWave?" -> POST /CreateWave
- "Create a DeleteApplication?" -> POST /DeleteApplication
- "Create a DeleteConnector?" -> POST /DeleteConnector
- "Create a DeleteJob?" -> POST /DeleteJob
- "Create a DeleteLaunchConfigurationTemplate?" -> POST /DeleteLaunchConfigurationTemplate
- "Create a DeleteReplicationConfigurationTemplate?" -> POST /DeleteReplicationConfigurationTemplate
- "Create a DeleteSourceServer?" -> POST /DeleteSourceServer
- "Create a DeleteVcenterClient?" -> POST /DeleteVcenterClient
- "Create a DeleteWave?" -> POST /DeleteWave
- "Create a DescribeJobLogItem?" -> POST /DescribeJobLogItems
- "Create a DescribeJob?" -> POST /DescribeJobs
- "Create a DescribeLaunchConfigurationTemplate?" -> POST /DescribeLaunchConfigurationTemplates
- "Create a DescribeReplicationConfigurationTemplate?" -> POST /DescribeReplicationConfigurationTemplates
- "Create a DescribeSourceServer?" -> POST /DescribeSourceServers
- "List all DescribeVcenterClients?" -> GET /DescribeVcenterClients
- "Create a DisassociateApplication?" -> POST /DisassociateApplications
- "Create a DisassociateSourceServer?" -> POST /DisassociateSourceServers
- "Create a DisconnectFromService?" -> POST /DisconnectFromService
- "Create a FinalizeCutover?" -> POST /FinalizeCutover
- "Create a GetLaunchConfiguration?" -> POST /GetLaunchConfiguration
- "Create a GetReplicationConfiguration?" -> POST /GetReplicationConfiguration
- "Create a InitializeService?" -> POST /InitializeService
- "Create a ListApplication?" -> POST /ListApplications
- "Create a ListConnector?" -> POST /ListConnectors
- "Create a ListExportError?" -> POST /ListExportErrors
- "Create a ListExport?" -> POST /ListExports
- "Create a ListImportError?" -> POST /ListImportErrors
- "Create a ListImport?" -> POST /ListImports
- "Create a ListManagedAccount?" -> POST /ListManagedAccounts
- "Create a ListSourceServerAction?" -> POST /ListSourceServerActions
- "Get tag details?" -> GET /tags/{resourceArn}
- "Create a ListTemplateAction?" -> POST /ListTemplateActions
- "Create a ListWave?" -> POST /ListWaves
- "Create a MarkAsArchived?" -> POST /MarkAsArchived
- "Create a PauseReplication?" -> POST /PauseReplication
- "Create a PutSourceServerAction?" -> POST /PutSourceServerAction
- "Create a PutTemplateAction?" -> POST /PutTemplateAction
- "Create a RemoveSourceServerAction?" -> POST /RemoveSourceServerAction
- "Create a RemoveTemplateAction?" -> POST /RemoveTemplateAction
- "Create a ResumeReplication?" -> POST /ResumeReplication
- "Create a RetryDataReplication?" -> POST /RetryDataReplication
- "Create a StartCutover?" -> POST /StartCutover
- "Create a StartExport?" -> POST /StartExport
- "Create a StartImport?" -> POST /StartImport
- "Create a StartReplication?" -> POST /StartReplication
- "Create a StartTest?" -> POST /StartTest
- "Create a StopReplication?" -> POST /StopReplication
- "Create a TerminateTargetInstance?" -> POST /TerminateTargetInstances
- "Create a UnarchiveApplication?" -> POST /UnarchiveApplication
- "Create a UnarchiveWave?" -> POST /UnarchiveWave
- "Delete a tag?" -> DELETE /tags/{resourceArn}
- "Create a UpdateApplication?" -> POST /UpdateApplication
- "Create a UpdateConnector?" -> POST /UpdateConnector
- "Create a UpdateLaunchConfiguration?" -> POST /UpdateLaunchConfiguration
- "Create a UpdateLaunchConfigurationTemplate?" -> POST /UpdateLaunchConfigurationTemplate
- "Create a UpdateReplicationConfiguration?" -> POST /UpdateReplicationConfiguration
- "Create a UpdateReplicationConfigurationTemplate?" -> POST /UpdateReplicationConfigurationTemplate
- "Create a UpdateSourceServer?" -> POST /UpdateSourceServer
- "Create a UpdateSourceServerReplicationType?" -> POST /UpdateSourceServerReplicationType
- "Create a UpdateWave?" -> POST /UpdateWave
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
