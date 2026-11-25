---
name: mongodb-atlas-administration-api
description: "MongoDB Atlas Administration API skill. Use when working with MongoDB Atlas Administration for api. Covers 504 endpoints."
version: 1.0.0
generator: lapsh
---

# MongoDB Atlas Administration API
API version: 2.0

## Auth
Bearer digest | OAuth2

## Base URL
https://cloud.mongodb.com

## Setup
1. Set Authorization header with your Bearer token
2. GET /api/atlas/v2 -- verify access
3. POST /api/atlas/v2/federationSettings/{federationSettingsId}/connectedOrgConfigs/{orgId}/roleMappings -- create first roleMappings

## Endpoints

504 endpoints across 1 groups. See references/api-spec.lap for full details.

### api
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/atlas/v2 | Return the Status of This MongoDB Application |
| GET | /api/atlas/v2/alertConfigs/matchers/fieldNames | Return All Alert Configuration Matchers Field Names |
| GET | /api/atlas/v2/clusters | Return All Authorized Clusters in All Projects |
| GET | /api/atlas/v2/eventTypes | Return All Event Types |
| DELETE | /api/atlas/v2/federationSettings/{federationSettingsId} | Delete One Federation Settings Instance |
| GET | /api/atlas/v2/federationSettings/{federationSettingsId}/connectedOrgConfigs | Return All Organization Configurations from One Federation |
| DELETE | /api/atlas/v2/federationSettings/{federationSettingsId}/connectedOrgConfigs/{orgId} | Remove One Organization Configuration from One Federation |
| GET | /api/atlas/v2/federationSettings/{federationSettingsId}/connectedOrgConfigs/{orgId} | Return One Organization Configuration from One Federation |
| PATCH | /api/atlas/v2/federationSettings/{federationSettingsId}/connectedOrgConfigs/{orgId} | Update One Organization Configuration in One Federation |
| GET | /api/atlas/v2/federationSettings/{federationSettingsId}/connectedOrgConfigs/{orgId}/roleMappings | Return All Role Mappings from One Organization |
| POST | /api/atlas/v2/federationSettings/{federationSettingsId}/connectedOrgConfigs/{orgId}/roleMappings | Create One Role Mapping in One Organization Configuration |
| DELETE | /api/atlas/v2/federationSettings/{federationSettingsId}/connectedOrgConfigs/{orgId}/roleMappings/{id} | Remove One Role Mapping from One Organization |
| GET | /api/atlas/v2/federationSettings/{federationSettingsId}/connectedOrgConfigs/{orgId}/roleMappings/{id} | Return One Role Mapping from One Organization |
| PUT | /api/atlas/v2/federationSettings/{federationSettingsId}/connectedOrgConfigs/{orgId}/roleMappings/{id} | Update One Role Mapping in One Organization |
| GET | /api/atlas/v2/federationSettings/{federationSettingsId}/identityProviders | Return All Identity Providers in One Federation |
| POST | /api/atlas/v2/federationSettings/{federationSettingsId}/identityProviders | Create One Identity Provider |
| DELETE | /api/atlas/v2/federationSettings/{federationSettingsId}/identityProviders/{identityProviderId} | Delete One Identity Provider |
| GET | /api/atlas/v2/federationSettings/{federationSettingsId}/identityProviders/{identityProviderId} | Return One Identity Provider by ID |
| PATCH | /api/atlas/v2/federationSettings/{federationSettingsId}/identityProviders/{identityProviderId} | Update One Identity Provider |
| DELETE | /api/atlas/v2/federationSettings/{federationSettingsId}/identityProviders/{identityProviderId}/jwks | Revoke JWKS from One OIDC Identity Provider |
| GET | /api/atlas/v2/federationSettings/{federationSettingsId}/identityProviders/{identityProviderId}/metadata.xml | Return Metadata of One Identity Provider |
| GET | /api/atlas/v2/groups | Return All Projects |
| POST | /api/atlas/v2/groups | Create One Project |
| DELETE | /api/atlas/v2/groups/{groupId} | Remove One Project |
| GET | /api/atlas/v2/groups/{groupId} | Return One Project |
| PATCH | /api/atlas/v2/groups/{groupId} | Update One Project |
| POST | /api/atlas/v2/groups/{groupId}/access | Add One MongoDB Cloud User to One Project |
| GET | /api/atlas/v2/groups/{groupId}/accessList | Return All Project IP Access List Entries |
| POST | /api/atlas/v2/groups/{groupId}/accessList | Add Entries to Project IP Access List |
| DELETE | /api/atlas/v2/groups/{groupId}/accessList/{entryValue} | Remove One Entry from One Project IP Access List |
| GET | /api/atlas/v2/groups/{groupId}/accessList/{entryValue} | Return One Project IP Access List Entry |
| GET | /api/atlas/v2/groups/{groupId}/accessList/{entryValue}/status | Return Status of One Project IP Access List Entry |
| GET | /api/atlas/v2/groups/{groupId}/activityFeed | Return Pre-Filtered Activity Feed Link for One Project |
| GET | /api/atlas/v2/groups/{groupId}/aiModelApiKeys | Return AI Model API Keys for One Group |
| POST | /api/atlas/v2/groups/{groupId}/aiModelApiKeys | Create New AI Model API Key |
| DELETE | /api/atlas/v2/groups/{groupId}/aiModelApiKeys/{apiKeyId} | Delete Existing AI Model API Key |
| GET | /api/atlas/v2/groups/{groupId}/aiModelApiKeys/{apiKeyId} | Return Single AI Model API Key for One Group |
| PATCH | /api/atlas/v2/groups/{groupId}/aiModelApiKeys/{apiKeyId} | Update Existing AI Model API Key |
| GET | /api/atlas/v2/groups/{groupId}/aiModelRateLimits | Return AI Model Rate Limits for One Group |
| GET | /api/atlas/v2/groups/{groupId}/aiModelRateLimits/{modelGroupName} | Return Single AI Model Rate Limit for One Group |
| PATCH | /api/atlas/v2/groups/{groupId}/aiModelRateLimits/{modelGroupName} | Update AI Model Rate Limit |
| POST | /api/atlas/v2/groups/{groupId}/aiModelRateLimits:reset | Reset AI Model Rate Limits for Group |
| GET | /api/atlas/v2/groups/{groupId}/alertConfigs | Return All Alert Configurations in One Project |
| POST | /api/atlas/v2/groups/{groupId}/alertConfigs | Create One Alert Configuration in One Project |
| DELETE | /api/atlas/v2/groups/{groupId}/alertConfigs/{alertConfigId} | Remove One Alert Configuration from One Project |
| GET | /api/atlas/v2/groups/{groupId}/alertConfigs/{alertConfigId} | Return One Alert Configuration from One Project |
| PATCH | /api/atlas/v2/groups/{groupId}/alertConfigs/{alertConfigId} | Toggle State of One Alert Configuration in One Project |
| PUT | /api/atlas/v2/groups/{groupId}/alertConfigs/{alertConfigId} | Update One Alert Configuration in One Project |
| GET | /api/atlas/v2/groups/{groupId}/alertConfigs/{alertConfigId}/alerts | Return All Open Alerts for One Alert Configuration |
| GET | /api/atlas/v2/groups/{groupId}/alerts | Return All Alerts from One Project |
| GET | /api/atlas/v2/groups/{groupId}/alerts/{alertId} | Return One Alert from One Project |
| PATCH | /api/atlas/v2/groups/{groupId}/alerts/{alertId} | Acknowledge One Alert from One Project |
| GET | /api/atlas/v2/groups/{groupId}/alerts/{alertId}/alertConfigs | Return All Alert Configurations Set for One Alert |
| GET | /api/atlas/v2/groups/{groupId}/apiKeys | Return All Organization API Keys Assigned to One Project |
| POST | /api/atlas/v2/groups/{groupId}/apiKeys | Create and Assign One Organization API Key to One Project |
| DELETE | /api/atlas/v2/groups/{groupId}/apiKeys/{apiUserId} | Unassign One Organization API Key from One Project |
| PATCH | /api/atlas/v2/groups/{groupId}/apiKeys/{apiUserId} | Update Organization API Key Roles for One Project |
| POST | /api/atlas/v2/groups/{groupId}/apiKeys/{apiUserId} | Assign One Organization API Key to One Project |
| GET | /api/atlas/v2/groups/{groupId}/auditLog | Return Auditing Configuration for One Project |
| PATCH | /api/atlas/v2/groups/{groupId}/auditLog | Update Auditing Configuration for One Project |
| GET | /api/atlas/v2/groups/{groupId}/awsCustomDNS | Return One Custom DNS Configuration for Atlas Clusters on AWS |
| PATCH | /api/atlas/v2/groups/{groupId}/awsCustomDNS | Update State of One Custom DNS Configuration for Atlas Clusters on AWS |
| GET | /api/atlas/v2/groups/{groupId}/backup/{cloudProvider}/privateEndpoints | Return Object Storage Private Endpoints for Cloud Backups for One Cloud Provider in One Project |
| POST | /api/atlas/v2/groups/{groupId}/backup/{cloudProvider}/privateEndpoints | Create One Object Storage Private Endpoint for Cloud Backups for One Cloud Provider in One Project |
| DELETE | /api/atlas/v2/groups/{groupId}/backup/{cloudProvider}/privateEndpoints/{endpointId} | Delete One Object Storage Private Endpoint for Cloud Backups for One Cloud Provider from One Project |
| GET | /api/atlas/v2/groups/{groupId}/backup/{cloudProvider}/privateEndpoints/{endpointId} | Return One Object Storage Private Endpoint for Cloud Backups for One Cloud Provider in One Project |
| GET | /api/atlas/v2/groups/{groupId}/backup/exportBuckets | Return All Snapshot Export Buckets |
| POST | /api/atlas/v2/groups/{groupId}/backup/exportBuckets | Create One Snapshot Export Bucket |
| DELETE | /api/atlas/v2/groups/{groupId}/backup/exportBuckets/{exportBucketId} | Delete One Snapshot Export Bucket |
| GET | /api/atlas/v2/groups/{groupId}/backup/exportBuckets/{exportBucketId} | Return One Snapshot Export Bucket |
| PATCH | /api/atlas/v2/groups/{groupId}/backup/exportBuckets/{exportBucketId} | Update One Export Bucket Private Networking Settings |
| DELETE | /api/atlas/v2/groups/{groupId}/backupCompliancePolicy | Disable Backup Compliance Policy Settings |
| GET | /api/atlas/v2/groups/{groupId}/backupCompliancePolicy | Return Backup Compliance Policy Settings |
| PUT | /api/atlas/v2/groups/{groupId}/backupCompliancePolicy | Update Backup Compliance Policy Settings |
| GET | /api/atlas/v2/groups/{groupId}/cloudProviderAccess | Return All Cloud Provider Access Roles |
| POST | /api/atlas/v2/groups/{groupId}/cloudProviderAccess | Create One Cloud Provider Access Role |
| DELETE | /api/atlas/v2/groups/{groupId}/cloudProviderAccess/{cloudProvider}/{roleId} | Deauthorize One Cloud Provider Access Role |
| GET | /api/atlas/v2/groups/{groupId}/cloudProviderAccess/{roleId} | Return One Cloud Provider Access Role |
| PATCH | /api/atlas/v2/groups/{groupId}/cloudProviderAccess/{roleId} | Authorize One Cloud Provider Access Role |
| GET | /api/atlas/v2/groups/{groupId}/clusters | Return All Clusters in One Project |
| POST | /api/atlas/v2/groups/{groupId}/clusters | Create One Cluster in One Project |
| DELETE | /api/atlas/v2/groups/{groupId}/clusters/{clusterName} | Remove One Cluster from One Project |
| GET | /api/atlas/v2/groups/{groupId}/clusters/{clusterName} | Return One Cluster from One Project |
| PATCH | /api/atlas/v2/groups/{groupId}/clusters/{clusterName} | Update One Cluster in One Project |
| GET | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/{clusterView}/{databaseName}/{collectionName}/collStats/measurements | Return Cluster-Level Query Latency |
| GET | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/{clusterView}/collStats/namespaces | Return Ranked Namespaces from One Cluster |
| GET | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/autoScalingConfiguration | Return Auto Scaling Configuration for One Sharded Cluster |
| GET | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/backup/exports | Return All Snapshot Export Jobs |
| POST | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/backup/exports | Create One Snapshot Export Job |
| GET | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/backup/exports/{exportId} | Return One Snapshot Export Job |
| GET | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/backup/restoreJobs | Return All Restore Jobs for One Cluster |
| POST | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/backup/restoreJobs | Create One Restore Job of One Cluster |
| DELETE | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/backup/restoreJobs/{restoreJobId} | Cancel One Restore Job for One Cluster |
| GET | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/backup/restoreJobs/{restoreJobId} | Return One Restore Job for One Cluster |
| DELETE | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/backup/schedule | Remove All Cloud Backup Schedules |
| GET | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/backup/schedule | Return One Cloud Backup Schedule |
| PATCH | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/backup/schedule | Update Cloud Backup Schedule for One Cluster |
| GET | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/backup/snapshots | Return All Replica Set Cloud Backups |
| POST | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/backup/snapshots | Take One On-Demand Snapshot |
| DELETE | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/backup/snapshots/{snapshotId} | Remove One Replica Set Cloud Backup |
| GET | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/backup/snapshots/{snapshotId} | Return One Replica Set Cloud Backup |
| PATCH | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/backup/snapshots/{snapshotId} | Update Expiration Date for One Cloud Backup |
| DELETE | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/backup/snapshots/shardedCluster/{snapshotId} | Remove One Sharded Cluster Cloud Backup |
| GET | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/backup/snapshots/shardedCluster/{snapshotId} | Return One Sharded Cluster Cloud Backup |
| GET | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/backup/snapshots/shardedClusters | Return All Sharded Cluster Cloud Backups |
| POST | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/backup/tenant/download | Download One M2 or M5 Cluster Snapshot |
| POST | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/backup/tenant/restore | Create One Restore Job for One M2 or M5 Cluster |
| GET | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/backup/tenant/restores | Return All Restore Jobs for One M2 or M5 Cluster |
| GET | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/backup/tenant/restores/{restoreId} | Return One Restore Job for One M2 or M5 Cluster |
| GET | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/backup/tenant/snapshots | Return All Snapshots for One M2 or M5 Cluster |
| GET | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/backup/tenant/snapshots/{snapshotId} | Return One Snapshot of One M2 or M5 Cluster |
| GET | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/backupCheckpoints | Return All Legacy Backup Checkpoints |
| GET | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/backupCheckpoints/{checkpointId} | Return One Legacy Backup Checkpoint |
| GET | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/collStats/pinned | Return Pinned Namespaces |
| PATCH | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/collStats/pinned | Add Pinned Namespaces |
| PUT | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/collStats/pinned | Pin Namespaces |
| PATCH | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/collStats/unpin | Unpin Namespaces |
| POST | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/fts/indexes | Create One Atlas Search Index |
| GET | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/fts/indexes/{databaseName}/{collectionName} | Return All Atlas Search Indexes for One Collection |
| DELETE | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/fts/indexes/{indexId} | Remove One Atlas Search Index |
| GET | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/fts/indexes/{indexId} | Return One Atlas Search Index |
| PATCH | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/fts/indexes/{indexId} | Update One Atlas Search Index |
| GET | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/globalWrites | Return One Managed Namespace in One Global Cluster |
| DELETE | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/globalWrites/customZoneMapping | Remove All Custom Zone Mappings from One Global Cluster |
| POST | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/globalWrites/customZoneMapping | Add One Custom Zone Mapping to One Global Cluster |
| DELETE | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/globalWrites/managedNamespaces | Remove One Managed Namespace from One Global Cluster |
| POST | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/globalWrites/managedNamespaces | Create One Managed Namespace in One Global Cluster |
| POST | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/index | Create One Rolling Index |
| GET | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/onlineArchives | Return All Online Archives for One Cluster |
| POST | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/onlineArchives | Create One Online Archive |
| DELETE | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/onlineArchives/{archiveId} | Remove One Online Archive |
| GET | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/onlineArchives/{archiveId} | Return One Online Archive |
| PATCH | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/onlineArchives/{archiveId} | Update One Online Archive |
| GET | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/onlineArchives/queryLogs.gz | Download Online Archive Query Logs |
| DELETE | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/outageSimulation | End One Outage Simulation |
| GET | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/outageSimulation | Return One Outage Simulation |
| POST | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/outageSimulation | Start One Outage Simulation |
| GET | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/performanceAdvisor/dropIndexSuggestions | Return All Suggested Indexes to Drop |
| GET | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/performanceAdvisor/schemaAdvice | Return Schema Advice |
| GET | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/performanceAdvisor/suggestedIndexes | Return All Suggested Indexes |
| GET | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/processArgs | Return Advanced Configuration Options for One Cluster |
| PATCH | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/processArgs | Update Advanced Configuration Options for One Cluster |
| GET | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/queryShapeInsights/{queryShapeHash}/details | Return Query Shape Details |
| GET | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/queryShapeInsights/summaries | Return Query Statistic Summaries |
| GET | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/queryShapes | Return All Query Shapes |
| GET | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/queryShapes/{queryShapeHash} | Return One Query Shape |
| PATCH | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/queryShapes/{queryShapeHash} | Update Query Shape Rejection Status |
| POST | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/restartPrimaries | Test Failover for One Cluster |
| GET | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/restoreJobs | Return All Legacy Backup Restore Jobs |
| POST | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/restoreJobs | Create One Legacy Backup Restore Job |
| GET | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/restoreJobs/{jobId} | Return One Legacy Backup Restore Job |
| DELETE | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/search/deployment | Delete Search Nodes |
| GET | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/search/deployment | Return All Search Nodes |
| PATCH | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/search/deployment | Update Search Nodes |
| POST | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/search/deployment | Create Search Nodes |
| GET | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/search/indexes | Return All Atlas Search Indexes for One Cluster |
| POST | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/search/indexes | Create One Atlas Search Index |
| GET | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/search/indexes/{databaseName}/{collectionName} | Return All Atlas Search Indexes for One Collection |
| DELETE | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/search/indexes/{databaseName}/{collectionName}/{indexName} | Remove One Atlas Search Index by Name |
| GET | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/search/indexes/{databaseName}/{collectionName}/{indexName} | Return One Atlas Search Index by Name |
| PATCH | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/search/indexes/{databaseName}/{collectionName}/{indexName} | Update One Atlas Search Index by Name |
| DELETE | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/search/indexes/{indexId} | Remove One Atlas Search Index by ID |
| GET | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/search/indexes/{indexId} | Return One Atlas Search Index by ID |
| PATCH | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/search/indexes/{indexId} | Update One Atlas Search Index by ID |
| GET | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/snapshotSchedule | Return One Snapshot Schedule |
| PATCH | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/snapshotSchedule | Update Snapshot Schedule for One Cluster |
| GET | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/snapshots | Return All Legacy Backup Snapshots |
| DELETE | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/snapshots/{snapshotId} | Remove One Legacy Backup Snapshot |
| GET | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/snapshots/{snapshotId} | Return One Legacy Backup Snapshot |
| PATCH | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/snapshots/{snapshotId} | Update Expiration Date for One Legacy Backup Snapshot |
| GET | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/status | Return Status of All Cluster Operations |
| POST | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}:grantMongoDBEmployeeAccess | Grant MongoDB Employee Cluster Access for One Cluster |
| POST | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}:pinFeatureCompatibilityVersion | Pin Feature Compatibility Version for One Cluster in One Project |
| POST | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}:revokeMongoDBEmployeeAccess | Revoke MongoDB Employee Cluster Access for One Cluster |
| POST | /api/atlas/v2/groups/{groupId}/clusters/{clusterName}:unpinFeatureCompatibilityVersion | Unpin Feature Compatibility Version for One Cluster in One Project |
| GET | /api/atlas/v2/groups/{groupId}/clusters/{hostName}/logs/{logName}.gz | Download Logs for One Cluster Host in One Project |
| GET | /api/atlas/v2/groups/{groupId}/clusters/provider/regions | Return All Cloud Provider Regions |
| POST | /api/atlas/v2/groups/{groupId}/clusters/tenantUpgrade | Upgrade One Shared-Tier Cluster |
| POST | /api/atlas/v2/groups/{groupId}/clusters/tenantUpgradeToServerless | Upgrade One Shared-Tier Cluster to One Serverless Instance |
| GET | /api/atlas/v2/groups/{groupId}/collStats/metrics | Return All Metric Names |
| GET | /api/atlas/v2/groups/{groupId}/containers | Return All Network Peering Containers in One Project for One Cloud Provider |
| POST | /api/atlas/v2/groups/{groupId}/containers | Create One Network Peering Container |
| DELETE | /api/atlas/v2/groups/{groupId}/containers/{containerId} | Remove One Network Peering Container |
| GET | /api/atlas/v2/groups/{groupId}/containers/{containerId} | Return One Network Peering Container |
| PATCH | /api/atlas/v2/groups/{groupId}/containers/{containerId} | Update One Network Peering Container |
| GET | /api/atlas/v2/groups/{groupId}/containers/all | Return All Network Peering Containers in One Project |
| GET | /api/atlas/v2/groups/{groupId}/customDBRoles/roles | Return All Custom Roles in One Project |
| POST | /api/atlas/v2/groups/{groupId}/customDBRoles/roles | Create One Custom Role |
| DELETE | /api/atlas/v2/groups/{groupId}/customDBRoles/roles/{roleName} | Remove One Custom Role from One Project |
| GET | /api/atlas/v2/groups/{groupId}/customDBRoles/roles/{roleName} | Return One Custom Role in One Project |
| PATCH | /api/atlas/v2/groups/{groupId}/customDBRoles/roles/{roleName} | Update One Custom Role in One Project |
| GET | /api/atlas/v2/groups/{groupId}/dataFederation | Return All Federated Database Instances in One Project |
| POST | /api/atlas/v2/groups/{groupId}/dataFederation | Create One Federated Database Instance in One Project |
| DELETE | /api/atlas/v2/groups/{groupId}/dataFederation/{tenantName} | Remove One Federated Database Instance from One Project |
| GET | /api/atlas/v2/groups/{groupId}/dataFederation/{tenantName} | Return One Federated Database Instance in One Project |
| PATCH | /api/atlas/v2/groups/{groupId}/dataFederation/{tenantName} | Update One Federated Database Instance in One Project |
| GET | /api/atlas/v2/groups/{groupId}/dataFederation/{tenantName}/limits | Return All Query Limits for One Federated Database Instance |
| DELETE | /api/atlas/v2/groups/{groupId}/dataFederation/{tenantName}/limits/{limitName} | Delete One Query Limit for One Federated Database Instance |
| GET | /api/atlas/v2/groups/{groupId}/dataFederation/{tenantName}/limits/{limitName} | Return One Federated Database Instance Query Limit for One Project |
| PATCH | /api/atlas/v2/groups/{groupId}/dataFederation/{tenantName}/limits/{limitName} | Configure One Query Limit for One Federated Database Instance |
| GET | /api/atlas/v2/groups/{groupId}/dataFederation/{tenantName}/queryLogs.gz | Download Query Logs for One Federated Database Instance |
| GET | /api/atlas/v2/groups/{groupId}/databaseUsers | Return All Database Users in One Project |
| POST | /api/atlas/v2/groups/{groupId}/databaseUsers | Create One Database User in One Project |
| DELETE | /api/atlas/v2/groups/{groupId}/databaseUsers/{databaseName}/{username} | Remove One Database User from One Project |
| GET | /api/atlas/v2/groups/{groupId}/databaseUsers/{databaseName}/{username} | Return One Database User from One Project |
| PATCH | /api/atlas/v2/groups/{groupId}/databaseUsers/{databaseName}/{username} | Update One Database User in One Project |
| GET | /api/atlas/v2/groups/{groupId}/databaseUsers/{username}/certs | Return All X.509 Certificates Assigned to One Database User |
| POST | /api/atlas/v2/groups/{groupId}/databaseUsers/{username}/certs | Create One X.509 Certificate for One Database User |
| GET | /api/atlas/v2/groups/{groupId}/dbAccessHistory/clusters/{clusterName} | Return Database Access History for One Cluster by Cluster Name |
| GET | /api/atlas/v2/groups/{groupId}/dbAccessHistory/processes/{hostname} | Return Database Access History for One Cluster by Hostname |
| GET | /api/atlas/v2/groups/{groupId}/encryptionAtRest | Return One Configuration for Encryption at Rest Using Customer-Managed Keys for One Project |
| PATCH | /api/atlas/v2/groups/{groupId}/encryptionAtRest | Update Encryption at Rest Configuration in One Project |
| GET | /api/atlas/v2/groups/{groupId}/encryptionAtRest/{cloudProvider}/privateEndpoints | Return Private Endpoints for Encryption at Rest Using Customer Key Management for One Cloud Provider in One Project |
| POST | /api/atlas/v2/groups/{groupId}/encryptionAtRest/{cloudProvider}/privateEndpoints | Create One Private Endpoint for Encryption at Rest Using Customer Key Management for One Cloud Provider in One Project |
| DELETE | /api/atlas/v2/groups/{groupId}/encryptionAtRest/{cloudProvider}/privateEndpoints/{endpointId} | Delete One Private Endpoint for Encryption at Rest Using Customer Key Management for One Cloud Provider from One Project |
| GET | /api/atlas/v2/groups/{groupId}/encryptionAtRest/{cloudProvider}/privateEndpoints/{endpointId} | Return One Private Endpoint for Encryption at Rest Using Customer Key Management for One Cloud Provider in One Project |
| GET | /api/atlas/v2/groups/{groupId}/events | Return Events from One Project |
| GET | /api/atlas/v2/groups/{groupId}/events/{eventId} | Return One Event from One Project |
| GET | /api/atlas/v2/groups/{groupId}/flexClusters | Return All Flex Clusters from One Project |
| POST | /api/atlas/v2/groups/{groupId}/flexClusters | Create One Flex Cluster in One Project |
| DELETE | /api/atlas/v2/groups/{groupId}/flexClusters/{name} | Remove One Flex Cluster from One Project |
| GET | /api/atlas/v2/groups/{groupId}/flexClusters/{name} | Return One Flex Cluster from One Project |
| PATCH | /api/atlas/v2/groups/{groupId}/flexClusters/{name} | Update One Flex Cluster in One Project |
| POST | /api/atlas/v2/groups/{groupId}/flexClusters/{name}/backup/download | Download One Flex Cluster Snapshot |
| GET | /api/atlas/v2/groups/{groupId}/flexClusters/{name}/backup/restoreJobs | Return All Restore Jobs for One Flex Cluster |
| POST | /api/atlas/v2/groups/{groupId}/flexClusters/{name}/backup/restoreJobs | Create One Restore Job for One Flex Cluster |
| GET | /api/atlas/v2/groups/{groupId}/flexClusters/{name}/backup/restoreJobs/{restoreJobId} | Return One Restore Job for One Flex Cluster |
| GET | /api/atlas/v2/groups/{groupId}/flexClusters/{name}/backup/snapshots | Return All Snapshots for One Flex Cluster |
| GET | /api/atlas/v2/groups/{groupId}/flexClusters/{name}/backup/snapshots/{snapshotId} | Return One Snapshot for One Flex Cluster |
| POST | /api/atlas/v2/groups/{groupId}/flexClusters:tenantUpgrade | Upgrade One Flex Cluster |
| GET | /api/atlas/v2/groups/{groupId}/hosts/{processId}/fts/metrics | Return All Atlas Search Metric Types for One Process |
| GET | /api/atlas/v2/groups/{groupId}/hosts/{processId}/fts/metrics/indexes/{databaseName}/{collectionName}/{indexName}/measurements | Return Atlas Search Metrics for One Index in One Namespace |
| GET | /api/atlas/v2/groups/{groupId}/hosts/{processId}/fts/metrics/indexes/{databaseName}/{collectionName}/measurements | Return All Atlas Search Index Metrics for One Namespace |
| GET | /api/atlas/v2/groups/{groupId}/hosts/{processId}/fts/metrics/measurements | Return Atlas Search Hardware and Status Metrics |
| GET | /api/atlas/v2/groups/{groupId}/integrations | Return All Active Third-Party Service Integrations |
| DELETE | /api/atlas/v2/groups/{groupId}/integrations/{integrationType} | Remove One Third-Party Service Integration |
| GET | /api/atlas/v2/groups/{groupId}/integrations/{integrationType} | Return One Third-Party Service Integration |
| POST | /api/atlas/v2/groups/{groupId}/integrations/{integrationType} | Create One Third-Party Service Integration |
| PUT | /api/atlas/v2/groups/{groupId}/integrations/{integrationType} | Update One Third-Party Service Integration |
| GET | /api/atlas/v2/groups/{groupId}/invites | Return All Invitations in One Project |
| PATCH | /api/atlas/v2/groups/{groupId}/invites | Update One Invitation in One Project |
| POST | /api/atlas/v2/groups/{groupId}/invites | Create Invitation for One MongoDB Cloud User in One Project |
| DELETE | /api/atlas/v2/groups/{groupId}/invites/{invitationId} | Remove One Invitation from One Project |
| GET | /api/atlas/v2/groups/{groupId}/invites/{invitationId} | Return One Invitation in One Project by Invitation ID |
| PATCH | /api/atlas/v2/groups/{groupId}/invites/{invitationId} | Update One Invitation in One Project by Invitation ID |
| GET | /api/atlas/v2/groups/{groupId}/ipAddresses | Return All IP Addresses for One Project |
| GET | /api/atlas/v2/groups/{groupId}/limits | Return All Limits for One Project |
| DELETE | /api/atlas/v2/groups/{groupId}/limits/{limitName} | Remove One Project Limit |
| GET | /api/atlas/v2/groups/{groupId}/limits/{limitName} | Return One Limit for One Project |
| PATCH | /api/atlas/v2/groups/{groupId}/limits/{limitName} | Set One Project Limit |
| POST | /api/atlas/v2/groups/{groupId}/liveMigrations | Create One Migration for One Local Managed Cluster to MongoDB Atlas |
| GET | /api/atlas/v2/groups/{groupId}/liveMigrations/{liveMigrationId} | Return One Migration Job |
| PUT | /api/atlas/v2/groups/{groupId}/liveMigrations/{liveMigrationId}/cutover | Cut Over One Migrated Cluster |
| POST | /api/atlas/v2/groups/{groupId}/liveMigrations/validate | Validate One Migration Request |
| GET | /api/atlas/v2/groups/{groupId}/liveMigrations/validate/{validationId} | Return One Migration Validation Job |
| GET | /api/atlas/v2/groups/{groupId}/logIntegrations | Return All Active Log Integrations |
| POST | /api/atlas/v2/groups/{groupId}/logIntegrations | Create One Log Integration |
| DELETE | /api/atlas/v2/groups/{groupId}/logIntegrations/{id} | Remove One Log Integration |
| GET | /api/atlas/v2/groups/{groupId}/logIntegrations/{id} | Return One Log Integration |
| PUT | /api/atlas/v2/groups/{groupId}/logIntegrations/{id} | Update One Log Integration |
| DELETE | /api/atlas/v2/groups/{groupId}/maintenanceWindow | Reset One Maintenance Window for One Project |
| GET | /api/atlas/v2/groups/{groupId}/maintenanceWindow | Return One Maintenance Window for One Project |
| PATCH | /api/atlas/v2/groups/{groupId}/maintenanceWindow | Update One Maintenance Window for One Project |
| POST | /api/atlas/v2/groups/{groupId}/maintenanceWindow/autoDefer | Toggle Automatic Deferral of Maintenance for One Project |
| POST | /api/atlas/v2/groups/{groupId}/maintenanceWindow/defer | Defer One Maintenance Window for One Project |
| GET | /api/atlas/v2/groups/{groupId}/managedSlowMs | Return Managed Slow Operation Threshold Status |
| DELETE | /api/atlas/v2/groups/{groupId}/managedSlowMs/disable | Disable Managed Slow Operation Threshold |
| POST | /api/atlas/v2/groups/{groupId}/managedSlowMs/enable | Enable Managed Slow Operation Threshold |
| GET | /api/atlas/v2/groups/{groupId}/mongoDBVersions | Return All Available MongoDB LTS Versions for Clusters in One Project |
| GET | /api/atlas/v2/groups/{groupId}/peers | Return All Network Peering Connections in One Project |
| POST | /api/atlas/v2/groups/{groupId}/peers | Create One Network Peering Connection |
| DELETE | /api/atlas/v2/groups/{groupId}/peers/{peerId} | Remove One Network Peering Connection |
| GET | /api/atlas/v2/groups/{groupId}/peers/{peerId} | Return One Network Peering Connection in One Project |
| PATCH | /api/atlas/v2/groups/{groupId}/peers/{peerId} | Update One Network Peering Connection |
| GET | /api/atlas/v2/groups/{groupId}/pipelines | Return All Data Lake Pipelines in One Project |
| POST | /api/atlas/v2/groups/{groupId}/pipelines | Create One Data Lake Pipeline |
| DELETE | /api/atlas/v2/groups/{groupId}/pipelines/{pipelineName} | Remove One Data Lake Pipeline |
| GET | /api/atlas/v2/groups/{groupId}/pipelines/{pipelineName} | Return One Data Lake Pipeline |
| PATCH | /api/atlas/v2/groups/{groupId}/pipelines/{pipelineName} | Update One Data Lake Pipeline |
| GET | /api/atlas/v2/groups/{groupId}/pipelines/{pipelineName}/availableSchedules | Return All Ingestion Schedules for One Data Lake Pipeline |
| GET | /api/atlas/v2/groups/{groupId}/pipelines/{pipelineName}/availableSnapshots | Return All Backup Snapshots for One Data Lake Pipeline |
| POST | /api/atlas/v2/groups/{groupId}/pipelines/{pipelineName}/pause | Pause One Data Lake Pipeline |
| POST | /api/atlas/v2/groups/{groupId}/pipelines/{pipelineName}/resume | Resume One Data Lake Pipeline |
| GET | /api/atlas/v2/groups/{groupId}/pipelines/{pipelineName}/runs | Return All Data Lake Pipeline Runs in One Project |
| DELETE | /api/atlas/v2/groups/{groupId}/pipelines/{pipelineName}/runs/{pipelineRunId} | Delete One Pipeline Run Dataset |
| GET | /api/atlas/v2/groups/{groupId}/pipelines/{pipelineName}/runs/{pipelineRunId} | Return One Data Lake Pipeline Run |
| POST | /api/atlas/v2/groups/{groupId}/pipelines/{pipelineName}/trigger | Trigger On-Demand Snapshot Ingestion |
| GET | /api/atlas/v2/groups/{groupId}/privateEndpoint/{cloudProvider}/endpointService | Return All Private Endpoint Services for One Provider |
| DELETE | /api/atlas/v2/groups/{groupId}/privateEndpoint/{cloudProvider}/endpointService/{endpointServiceId} | Remove One Private Endpoint Service for One Provider |
| GET | /api/atlas/v2/groups/{groupId}/privateEndpoint/{cloudProvider}/endpointService/{endpointServiceId} | Return One Private Endpoint Service for One Provider |
| POST | /api/atlas/v2/groups/{groupId}/privateEndpoint/{cloudProvider}/endpointService/{endpointServiceId}/endpoint | Create One Private Endpoint for One Provider |
| DELETE | /api/atlas/v2/groups/{groupId}/privateEndpoint/{cloudProvider}/endpointService/{endpointServiceId}/endpoint/{endpointId} | Remove One Private Endpoint for One Provider |
| GET | /api/atlas/v2/groups/{groupId}/privateEndpoint/{cloudProvider}/endpointService/{endpointServiceId}/endpoint/{endpointId} | Return One Private Endpoint for One Provider |
| POST | /api/atlas/v2/groups/{groupId}/privateEndpoint/endpointService | Create One Private Endpoint Service for One Provider |
| GET | /api/atlas/v2/groups/{groupId}/privateEndpoint/regionalMode | Return Regionalized Private Endpoint Status |
| PATCH | /api/atlas/v2/groups/{groupId}/privateEndpoint/regionalMode | Toggle Regionalized Private Endpoint Status |
| GET | /api/atlas/v2/groups/{groupId}/privateEndpoint/serverless/instance/{instanceName}/endpoint | Return All Private Endpoints for One Serverless Instance |
| POST | /api/atlas/v2/groups/{groupId}/privateEndpoint/serverless/instance/{instanceName}/endpoint | Create One Private Endpoint for One Serverless Instance |
| DELETE | /api/atlas/v2/groups/{groupId}/privateEndpoint/serverless/instance/{instanceName}/endpoint/{endpointId} | Remove One Private Endpoint for One Serverless Instance |
| GET | /api/atlas/v2/groups/{groupId}/privateEndpoint/serverless/instance/{instanceName}/endpoint/{endpointId} | Return One Private Endpoint for One Serverless Instance |
| PATCH | /api/atlas/v2/groups/{groupId}/privateEndpoint/serverless/instance/{instanceName}/endpoint/{endpointId} | Update One Private Endpoint for One Serverless Instance |
| GET | /api/atlas/v2/groups/{groupId}/privateIpMode | Verify Connect via Peering-Only Mode for One Project |
| PATCH | /api/atlas/v2/groups/{groupId}/privateIpMode | Disable Connect via Peering-Only Mode for One Project |
| GET | /api/atlas/v2/groups/{groupId}/privateNetworkSettings/endpointIds | Return All Federated Database Instance and Online Archive Private Endpoints in One Project |
| POST | /api/atlas/v2/groups/{groupId}/privateNetworkSettings/endpointIds | Create One Federated Database Instance and Online Archive Private Endpoint for One Project |
| DELETE | /api/atlas/v2/groups/{groupId}/privateNetworkSettings/endpointIds/{endpointId} | Remove One Federated Database Instance and Online Archive Private Endpoint from One Project |
| GET | /api/atlas/v2/groups/{groupId}/privateNetworkSettings/endpointIds/{endpointId} | Return One Federated Database Instance and Online Archive Private Endpoint in One Project |
| GET | /api/atlas/v2/groups/{groupId}/processes | Return All MongoDB Processes in One Project |
| GET | /api/atlas/v2/groups/{groupId}/processes/{processId} | Return One MongoDB Process by ID |
| GET | /api/atlas/v2/groups/{groupId}/processes/{processId}/{databaseName}/{collectionName}/collStats/measurements | Return Host-Level Query Latency |
| GET | /api/atlas/v2/groups/{groupId}/processes/{processId}/collStats/namespaces | Return Ranked Namespaces from One Host |
| GET | /api/atlas/v2/groups/{groupId}/processes/{processId}/databases | Return Available Databases for One MongoDB Process |
| GET | /api/atlas/v2/groups/{groupId}/processes/{processId}/databases/{databaseName} | Return One Database for One MongoDB Process |
| GET | /api/atlas/v2/groups/{groupId}/processes/{processId}/databases/{databaseName}/measurements | Return Measurements for One Database in One MongoDB Process |
| GET | /api/atlas/v2/groups/{groupId}/processes/{processId}/disks | Return Available Disks for One MongoDB Process |
| GET | /api/atlas/v2/groups/{groupId}/processes/{processId}/disks/{partitionName} | Return Measurements for One Disk |
| GET | /api/atlas/v2/groups/{groupId}/processes/{processId}/disks/{partitionName}/measurements | Return Measurements of One Disk for One MongoDB Process |
| GET | /api/atlas/v2/groups/{groupId}/processes/{processId}/measurements | Return Measurements for One MongoDB Process |
| GET | /api/atlas/v2/groups/{groupId}/processes/{processId}/performanceAdvisor/namespaces | Return All Namespaces for One Host |
| GET | /api/atlas/v2/groups/{groupId}/processes/{processId}/performanceAdvisor/slowQueryLogs | Return Slow Queries |
| GET | /api/atlas/v2/groups/{groupId}/processes/{processId}/performanceAdvisor/suggestedIndexes | Return All Suggested Indexes |
| DELETE | /api/atlas/v2/groups/{groupId}/pushBasedLogExport | Disable Push-Based Log Export for One Project |
| GET | /api/atlas/v2/groups/{groupId}/pushBasedLogExport | Return One Push-Based Log Export Configuration in One Project |
| PATCH | /api/atlas/v2/groups/{groupId}/pushBasedLogExport | Update One Push-Based Log Export Configuration in One Project |
| POST | /api/atlas/v2/groups/{groupId}/pushBasedLogExport | Create One Push-Based Log Export Configuration in One Project |
| POST | /api/atlas/v2/groups/{groupId}/sampleDatasetLoad/{name} | Load Sample Dataset into One Cluster |
| GET | /api/atlas/v2/groups/{groupId}/sampleDatasetLoad/{sampleDatasetId} | Return Status of Sample Dataset Load for One Cluster |
| GET | /api/atlas/v2/groups/{groupId}/sandbox/{sandboxConfigId}:generateClusterDescription | Return Cluster Description from Sandbox Template Configuration |
| GET | /api/atlas/v2/groups/{groupId}/serverless | Return All Serverless Instances in One Project |
| POST | /api/atlas/v2/groups/{groupId}/serverless | Create One Serverless Instance in One Project |
| GET | /api/atlas/v2/groups/{groupId}/serverless/{clusterName}/backup/restoreJobs | Return All Restore Jobs for One Serverless Instance |
| POST | /api/atlas/v2/groups/{groupId}/serverless/{clusterName}/backup/restoreJobs | Create One Restore Job for One Serverless Instance |
| GET | /api/atlas/v2/groups/{groupId}/serverless/{clusterName}/backup/restoreJobs/{restoreJobId} | Return One Restore Job for One Serverless Instance |
| GET | /api/atlas/v2/groups/{groupId}/serverless/{clusterName}/backup/snapshots | Return All Snapshots of One Serverless Instance |
| GET | /api/atlas/v2/groups/{groupId}/serverless/{clusterName}/backup/snapshots/{snapshotId} | Return One Snapshot of One Serverless Instance |
| GET | /api/atlas/v2/groups/{groupId}/serverless/{clusterName}/performanceAdvisor/autoIndexing | Return Serverless Auto-Indexing Status |
| POST | /api/atlas/v2/groups/{groupId}/serverless/{clusterName}/performanceAdvisor/autoIndexing | Set Serverless Auto-Indexing Status |
| DELETE | /api/atlas/v2/groups/{groupId}/serverless/{name} | Remove One Serverless Instance from One Project |
| GET | /api/atlas/v2/groups/{groupId}/serverless/{name} | Return One Serverless Instance from One Project |
| PATCH | /api/atlas/v2/groups/{groupId}/serverless/{name} | Update One Serverless Instance in One Project |
| GET | /api/atlas/v2/groups/{groupId}/serviceAccounts | Return All Project Service Accounts |
| POST | /api/atlas/v2/groups/{groupId}/serviceAccounts | Create One Project Service Account |
| DELETE | /api/atlas/v2/groups/{groupId}/serviceAccounts/{clientId} | Remove One Project Service Account |
| GET | /api/atlas/v2/groups/{groupId}/serviceAccounts/{clientId} | Return One Project Service Account |
| PATCH | /api/atlas/v2/groups/{groupId}/serviceAccounts/{clientId} | Update One Project Service Account |
| GET | /api/atlas/v2/groups/{groupId}/serviceAccounts/{clientId}/accessList | Return All Access List Entries for One Project Service Account |
| POST | /api/atlas/v2/groups/{groupId}/serviceAccounts/{clientId}/accessList | Add Access List Entries for One Project Service Account |
| DELETE | /api/atlas/v2/groups/{groupId}/serviceAccounts/{clientId}/accessList/{ipAddress} | Remove One Access List Entry from One Project Service Account |
| POST | /api/atlas/v2/groups/{groupId}/serviceAccounts/{clientId}/secrets | Create One Project Service Account Secret |
| DELETE | /api/atlas/v2/groups/{groupId}/serviceAccounts/{clientId}/secrets/{secretId} | Delete One Project Service Account Secret |
| POST | /api/atlas/v2/groups/{groupId}/serviceAccounts/{clientId}:invite | Assign One Service Account to One Project |
| GET | /api/atlas/v2/groups/{groupId}/settings | Return Project Settings |
| PATCH | /api/atlas/v2/groups/{groupId}/settings | Update Project Settings |
| GET | /api/atlas/v2/groups/{groupId}/standbyLinks | Return All Standby Links for One Project |
| POST | /api/atlas/v2/groups/{groupId}/standbyLinks | Create Standby Link |
| DELETE | /api/atlas/v2/groups/{groupId}/standbyLinks/{standbyLinkId} | Delete Standby Link |
| GET | /api/atlas/v2/groups/{groupId}/standbyLinks/{standbyLinkId} | Return One Standby Link |
| GET | /api/atlas/v2/groups/{groupId}/standbyLinks/{standbyLinkId}/failovers | Return All Standby Link Failovers |
| POST | /api/atlas/v2/groups/{groupId}/standbyLinks/{standbyLinkId}/failovers | Create Standby Link Failover |
| GET | /api/atlas/v2/groups/{groupId}/standbyLinks/{standbyLinkId}/failovers/{failoverId} | Return One Standby Link Failover |
| GET | /api/atlas/v2/groups/{groupId}/streams | Return All Stream Workspaces in One Project |
| POST | /api/atlas/v2/groups/{groupId}/streams | Create One Stream Workspace |
| DELETE | /api/atlas/v2/groups/{groupId}/streams/{tenantName} | Delete One Stream Workspace |
| GET | /api/atlas/v2/groups/{groupId}/streams/{tenantName} | Return One Stream Workspace |
| PATCH | /api/atlas/v2/groups/{groupId}/streams/{tenantName} | Update One Stream Workspace |
| GET | /api/atlas/v2/groups/{groupId}/streams/{tenantName}/auditLogs | Download Audit Logs for One Atlas Stream Processing Workspace |
| GET | /api/atlas/v2/groups/{groupId}/streams/{tenantName}/connections | Return All Connections of the Stream Workspaces |
| POST | /api/atlas/v2/groups/{groupId}/streams/{tenantName}/connections | Create One Stream Connection |
| DELETE | /api/atlas/v2/groups/{groupId}/streams/{tenantName}/connections/{connectionName} | Delete One Stream Connection |
| GET | /api/atlas/v2/groups/{groupId}/streams/{tenantName}/connections/{connectionName} | Return One Stream Connection |
| PATCH | /api/atlas/v2/groups/{groupId}/streams/{tenantName}/connections/{connectionName} | Update One Stream Connection |
| POST | /api/atlas/v2/groups/{groupId}/streams/{tenantName}/processor | Create One Stream Processor |
| DELETE | /api/atlas/v2/groups/{groupId}/streams/{tenantName}/processor/{processorName} | Delete One Stream Processor |
| GET | /api/atlas/v2/groups/{groupId}/streams/{tenantName}/processor/{processorName} | Return One Stream Processor |
| PATCH | /api/atlas/v2/groups/{groupId}/streams/{tenantName}/processor/{processorName} | Update One Stream Processor |
| POST | /api/atlas/v2/groups/{groupId}/streams/{tenantName}/processor/{processorName}:start | Start One Stream Processor |
| POST | /api/atlas/v2/groups/{groupId}/streams/{tenantName}/processor/{processorName}:startWith | Start One Stream Processor With Options |
| POST | /api/atlas/v2/groups/{groupId}/streams/{tenantName}/processor/{processorName}:stop | Stop One Stream Processor |
| GET | /api/atlas/v2/groups/{groupId}/streams/{tenantName}/processors | Return All Stream Processors in One Stream Workspace |
| GET | /api/atlas/v2/groups/{groupId}/streams/{tenantName}:downloadOperationalLogs | Download Operational Logs for One Atlas Stream Processing Workspace |
| GET | /api/atlas/v2/groups/{groupId}/streams/accountDetails | Return Account ID and VPC ID for One Project and Region |
| GET | /api/atlas/v2/groups/{groupId}/streams/activeVpcPeeringConnections | Return All Active Incoming VPC Peering Connections |
| GET | /api/atlas/v2/groups/{groupId}/streams/privateLinkConnections | Return All Private Link Connections |
| POST | /api/atlas/v2/groups/{groupId}/streams/privateLinkConnections | Create One Private Link Connection |
| DELETE | /api/atlas/v2/groups/{groupId}/streams/privateLinkConnections/{connectionId} | Delete One Private Link Connection |
| GET | /api/atlas/v2/groups/{groupId}/streams/privateLinkConnections/{connectionId} | Return One Private Link Connection |
| GET | /api/atlas/v2/groups/{groupId}/streams/vpcPeeringConnections | Return All VPC Peering Connections |
| DELETE | /api/atlas/v2/groups/{groupId}/streams/vpcPeeringConnections/{id} | Delete One VPC Peering Connection |
| POST | /api/atlas/v2/groups/{groupId}/streams/vpcPeeringConnections/{id}:accept | Accept One Incoming VPC Peering Connection |
| POST | /api/atlas/v2/groups/{groupId}/streams/vpcPeeringConnections/{id}:reject | Reject One Incoming VPC Peering Connection |
| POST | /api/atlas/v2/groups/{groupId}/streams:withSampleConnections | Create One Stream Workspace with Sample Connections |
| GET | /api/atlas/v2/groups/{groupId}/teams | Return All Teams in One Project |
| POST | /api/atlas/v2/groups/{groupId}/teams | Add Multiple Teams to One Project |
| DELETE | /api/atlas/v2/groups/{groupId}/teams/{teamId} | Remove One Team from One Project |
| GET | /api/atlas/v2/groups/{groupId}/teams/{teamId} | Return One Team in One Project |
| PATCH | /api/atlas/v2/groups/{groupId}/teams/{teamId} | Update Team Roles in One Project |
| GET | /api/atlas/v2/groups/{groupId}/userSecurity | Return LDAP or X.509 Configuration |
| PATCH | /api/atlas/v2/groups/{groupId}/userSecurity | Update LDAP or X.509 Configuration |
| DELETE | /api/atlas/v2/groups/{groupId}/userSecurity/customerX509 | Disable Customer-Managed X.509 |
| DELETE | /api/atlas/v2/groups/{groupId}/userSecurity/ldap/userToDNMapping | Remove LDAP User to DN Mapping |
| POST | /api/atlas/v2/groups/{groupId}/userSecurity/ldap/verify | Verify LDAP Configuration in One Project |
| GET | /api/atlas/v2/groups/{groupId}/userSecurity/ldap/verify/{requestId} | Return Status of LDAP Configuration Verification in One Project |
| GET | /api/atlas/v2/groups/{groupId}/users | Return All MongoDB Cloud Users in One Project |
| POST | /api/atlas/v2/groups/{groupId}/users | Add One MongoDB Cloud User to One Project |
| DELETE | /api/atlas/v2/groups/{groupId}/users/{userId} | Remove One MongoDB Cloud User from One Project |
| GET | /api/atlas/v2/groups/{groupId}/users/{userId} | Return One MongoDB Cloud User in One Project |
| PUT | /api/atlas/v2/groups/{groupId}/users/{userId}/roles | Update Project Roles for One MongoDB Cloud User |
| POST | /api/atlas/v2/groups/{groupId}/users/{userId}:addRole | Add One Project Role to One MongoDB Cloud User |
| POST | /api/atlas/v2/groups/{groupId}/users/{userId}:removeRole | Remove One Project Role from One MongoDB Cloud User |
| POST | /api/atlas/v2/groups/{groupId}:migrate | Migrate One Project to Another Organization |
| GET | /api/atlas/v2/groups/byName/{groupName} | Return One Project by Name |
| GET | /api/atlas/v2/orgs | Return All Organizations |
| POST | /api/atlas/v2/orgs | Create One Organization |
| DELETE | /api/atlas/v2/orgs/{orgId} | Remove One Organization |
| GET | /api/atlas/v2/orgs/{orgId} | Return One Organization |
| PATCH | /api/atlas/v2/orgs/{orgId} | Update One Organization |
| GET | /api/atlas/v2/orgs/{orgId}/activityFeed | Return Pre-Filtered Activity Feed Link for One Organization |
| GET | /api/atlas/v2/orgs/{orgId}/aiModelApiKeys | Return AI Model API Keys for One Organization |
| GET | /api/atlas/v2/orgs/{orgId}/aiModelApiKeys/{apiKeyId} | Return Single AI Model API Key for One Organization |
| GET | /api/atlas/v2/orgs/{orgId}/aiModelRateLimits | Return AI Model Rate Limits for One Organization |
| GET | /api/atlas/v2/orgs/{orgId}/aiModelRateLimits/{modelGroupName} | Return Single AI Model Rate Limit for One Organization |
| GET | /api/atlas/v2/orgs/{orgId}/apiKeys | Return All Organization API Keys |
| POST | /api/atlas/v2/orgs/{orgId}/apiKeys | Create One Organization API Key |
| DELETE | /api/atlas/v2/orgs/{orgId}/apiKeys/{apiUserId} | Remove One Organization API Key |
| GET | /api/atlas/v2/orgs/{orgId}/apiKeys/{apiUserId} | Return One Organization API Key |
| PATCH | /api/atlas/v2/orgs/{orgId}/apiKeys/{apiUserId} | Update One Organization API Key |
| GET | /api/atlas/v2/orgs/{orgId}/apiKeys/{apiUserId}/accessList | Return All Access List Entries for One Organization API Key |
| POST | /api/atlas/v2/orgs/{orgId}/apiKeys/{apiUserId}/accessList | Create One Access List Entry for One Organization API Key |
| DELETE | /api/atlas/v2/orgs/{orgId}/apiKeys/{apiUserId}/accessList/{ipAddress} | Remove One Access List Entry for One Organization API Key |
| GET | /api/atlas/v2/orgs/{orgId}/apiKeys/{apiUserId}/accessList/{ipAddress} | Return One Access List Entry for One Organization API Key |
| GET | /api/atlas/v2/orgs/{orgId}/associatedInvoices | Return Associated Invoices |
| POST | /api/atlas/v2/orgs/{orgId}/billing/costExplorer/usage | Create One Cost Explorer Query Process |
| GET | /api/atlas/v2/orgs/{orgId}/billing/costExplorer/usage/{token} | Return Usage Details for One Cost Explorer Query |
| GET | /api/atlas/v2/orgs/{orgId}/events | Return Events from One Organization |
| GET | /api/atlas/v2/orgs/{orgId}/events/{eventId} | Return One Event from One Organization |
| GET | /api/atlas/v2/orgs/{orgId}/federationSettings | Return Federation Settings for One Organization |
| GET | /api/atlas/v2/orgs/{orgId}/groups | Return All Projects in One Organization |
| GET | /api/atlas/v2/orgs/{orgId}/invites | Return All Invitations in One Organization |
| PATCH | /api/atlas/v2/orgs/{orgId}/invites | Update One Invitation in One Organization |
| POST | /api/atlas/v2/orgs/{orgId}/invites | Create Invitation for One MongoDB Cloud User in One Organization |
| DELETE | /api/atlas/v2/orgs/{orgId}/invites/{invitationId} | Remove One Invitation from One Organization |
| GET | /api/atlas/v2/orgs/{orgId}/invites/{invitationId} | Return One Invitation in One Organization by Invitation ID |
| PATCH | /api/atlas/v2/orgs/{orgId}/invites/{invitationId} | Update One Invitation in One Organization by Invitation ID |
| GET | /api/atlas/v2/orgs/{orgId}/invoices | Return All Invoices for One Organization |
| GET | /api/atlas/v2/orgs/{orgId}/invoices/{invoiceId} | Return One Invoice for One Organization |
| GET | /api/atlas/v2/orgs/{orgId}/invoices/{invoiceId}/csv | Return One Invoice as CSV for One Organization |
| GET | /api/atlas/v2/orgs/{orgId}/invoices/{invoiceId}/lineItems:search | Return All Line Items for One Invoice by Invoice ID |
| POST | /api/atlas/v2/orgs/{orgId}/invoices/{invoiceId}:generateAndDownloadReport | Generate and Download Invoice Report |
| GET | /api/atlas/v2/orgs/{orgId}/invoices/pending | Return All Pending Invoices for One Organization |
| GET | /api/atlas/v2/orgs/{orgId}/liveMigrations/availableProjects | Return All Projects Available for Migration |
| DELETE | /api/atlas/v2/orgs/{orgId}/liveMigrations/linkTokens | Remove One Link-Token |
| POST | /api/atlas/v2/orgs/{orgId}/liveMigrations/linkTokens | Create One Link-Token |
| GET | /api/atlas/v2/orgs/{orgId}/nonCompliantResources | Return All Non-Compliant Resources |
| GET | /api/atlas/v2/orgs/{orgId}/resourcePolicies | Return All Atlas Resource Policies |
| POST | /api/atlas/v2/orgs/{orgId}/resourcePolicies | Create One Atlas Resource Policy |
| DELETE | /api/atlas/v2/orgs/{orgId}/resourcePolicies/{resourcePolicyId} | Delete One Atlas Resource Policy |
| GET | /api/atlas/v2/orgs/{orgId}/resourcePolicies/{resourcePolicyId} | Return One Atlas Resource Policy |
| PATCH | /api/atlas/v2/orgs/{orgId}/resourcePolicies/{resourcePolicyId} | Update One Atlas Resource Policy |
| POST | /api/atlas/v2/orgs/{orgId}/resourcePolicies:validate | Validate One Atlas Resource Policy |
| GET | /api/atlas/v2/orgs/{orgId}/sandboxConfig | Return Sandbox Configuration IDs for an Organization |
| POST | /api/atlas/v2/orgs/{orgId}/sandboxConfig | Create One Sandbox Configuration for an Organization |
| DELETE | /api/atlas/v2/orgs/{orgId}/sandboxConfig/{sandboxConfigId} | Delete the Default Sandbox Configuration and Disable Sandbox |
| GET | /api/atlas/v2/orgs/{orgId}/sandboxConfig/{sandboxConfigId} | Return Default Sandbox Configuration for One Organization |
| PATCH | /api/atlas/v2/orgs/{orgId}/sandboxConfig/{sandboxConfigId} | Update an Existing Sandbox Configuration |
| GET | /api/atlas/v2/orgs/{orgId}/serviceAccounts | Return All Organization Service Accounts |
| POST | /api/atlas/v2/orgs/{orgId}/serviceAccounts | Create One Organization Service Account |
| DELETE | /api/atlas/v2/orgs/{orgId}/serviceAccounts/{clientId} | Delete One Organization Service Account |
| GET | /api/atlas/v2/orgs/{orgId}/serviceAccounts/{clientId} | Return One Organization Service Account |
| PATCH | /api/atlas/v2/orgs/{orgId}/serviceAccounts/{clientId} | Update One Organization Service Account |
| GET | /api/atlas/v2/orgs/{orgId}/serviceAccounts/{clientId}/accessList | Return All Access List Entries for One Organization Service Account |
| POST | /api/atlas/v2/orgs/{orgId}/serviceAccounts/{clientId}/accessList | Add Access List Entries for One Organization Service Account |
| DELETE | /api/atlas/v2/orgs/{orgId}/serviceAccounts/{clientId}/accessList/{ipAddress} | Remove One Access List Entry from One Organization Service Account |
| GET | /api/atlas/v2/orgs/{orgId}/serviceAccounts/{clientId}/groups | Return All Service Account Project Assignments |
| POST | /api/atlas/v2/orgs/{orgId}/serviceAccounts/{clientId}/secrets | Create One Organization Service Account Secret |
| DELETE | /api/atlas/v2/orgs/{orgId}/serviceAccounts/{clientId}/secrets/{secretId} | Delete One Organization Service Account Secret |
| GET | /api/atlas/v2/orgs/{orgId}/settings | Return Settings for One Organization |
| PATCH | /api/atlas/v2/orgs/{orgId}/settings | Update Settings for One Organization |
| GET | /api/atlas/v2/orgs/{orgId}/teams | Return All Teams in One Organization |
| POST | /api/atlas/v2/orgs/{orgId}/teams | Create One Team in One Organization |
| DELETE | /api/atlas/v2/orgs/{orgId}/teams/{teamId} | Remove One Team from One Organization |
| GET | /api/atlas/v2/orgs/{orgId}/teams/{teamId} | Return One Team by ID |
| PATCH | /api/atlas/v2/orgs/{orgId}/teams/{teamId} | Rename One Team |
| GET | /api/atlas/v2/orgs/{orgId}/teams/{teamId}/users | Return All MongoDB Cloud Users Assigned to One Team |
| POST | /api/atlas/v2/orgs/{orgId}/teams/{teamId}/users | Assign MongoDB Cloud Users in One Organization to One Team |
| DELETE | /api/atlas/v2/orgs/{orgId}/teams/{teamId}/users/{userId} | Remove One MongoDB Cloud User from One Team |
| POST | /api/atlas/v2/orgs/{orgId}/teams/{teamId}:addUser | Add One MongoDB Cloud User to One Team |
| POST | /api/atlas/v2/orgs/{orgId}/teams/{teamId}:removeUser | Remove One MongoDB Cloud User from One Team |
| GET | /api/atlas/v2/orgs/{orgId}/teams/byName/{teamName} | Return One Team by Name |
| GET | /api/atlas/v2/orgs/{orgId}/users | Return All MongoDB Cloud Users in One Organization |
| POST | /api/atlas/v2/orgs/{orgId}/users | Add One MongoDB Cloud User to One Organization |
| DELETE | /api/atlas/v2/orgs/{orgId}/users/{userId} | Remove One MongoDB Cloud User from One Organization |
| GET | /api/atlas/v2/orgs/{orgId}/users/{userId} | Return One MongoDB Cloud User in One Organization |
| PATCH | /api/atlas/v2/orgs/{orgId}/users/{userId} | Update One MongoDB Cloud User in One Organization |
| PUT | /api/atlas/v2/orgs/{orgId}/users/{userId}/roles | Update Organization Roles for One MongoDB Cloud User |
| POST | /api/atlas/v2/orgs/{orgId}/users/{userId}:addRole | Add One Organization Role to One MongoDB Cloud User |
| POST | /api/atlas/v2/orgs/{orgId}/users/{userId}:removeRole | Remove One Organization Role from One MongoDB Cloud User |
| GET | /api/atlas/v2/rateLimits | Return All Rate Limits |
| GET | /api/atlas/v2/rateLimits/{endpointSetId} | Return One Rate Limit |
| GET | /api/atlas/v2/skus | Return All Stock Keeping Units |
| GET | /api/atlas/v2/skus/{skuId} | Return One Stock Keeping Unit |
| GET | /api/atlas/v2/unauth/controlPlaneIPAddresses | Return All Control Plane IP Addresses |
| POST | /api/atlas/v2/users | Create One MongoDB Cloud User |
| GET | /api/atlas/v2/users/{userId} | Return One MongoDB Cloud User by ID |
| GET | /api/atlas/v2/users/byName/{userName} | Return One MongoDB Cloud User by Username |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all atlas?" -> GET /api/atlas/v2
- "List all fieldNames?" -> GET /api/atlas/v2/alertConfigs/matchers/fieldNames
- "List all clusters?" -> GET /api/atlas/v2/clusters
- "List all eventTypes?" -> GET /api/atlas/v2/eventTypes
- "Delete a federationSetting?" -> DELETE /api/atlas/v2/federationSettings/{federationSettingsId}
- "List all connectedOrgConfigs?" -> GET /api/atlas/v2/federationSettings/{federationSettingsId}/connectedOrgConfigs
- "Delete a connectedOrgConfig?" -> DELETE /api/atlas/v2/federationSettings/{federationSettingsId}/connectedOrgConfigs/{orgId}
- "Get connectedOrgConfig details?" -> GET /api/atlas/v2/federationSettings/{federationSettingsId}/connectedOrgConfigs/{orgId}
- "Partially update a connectedOrgConfig?" -> PATCH /api/atlas/v2/federationSettings/{federationSettingsId}/connectedOrgConfigs/{orgId}
- "List all roleMappings?" -> GET /api/atlas/v2/federationSettings/{federationSettingsId}/connectedOrgConfigs/{orgId}/roleMappings
- "Create a roleMapping?" -> POST /api/atlas/v2/federationSettings/{federationSettingsId}/connectedOrgConfigs/{orgId}/roleMappings
- "Delete a roleMapping?" -> DELETE /api/atlas/v2/federationSettings/{federationSettingsId}/connectedOrgConfigs/{orgId}/roleMappings/{id}
- "Get roleMapping details?" -> GET /api/atlas/v2/federationSettings/{federationSettingsId}/connectedOrgConfigs/{orgId}/roleMappings/{id}
- "Update a roleMapping?" -> PUT /api/atlas/v2/federationSettings/{federationSettingsId}/connectedOrgConfigs/{orgId}/roleMappings/{id}
- "List all identityProviders?" -> GET /api/atlas/v2/federationSettings/{federationSettingsId}/identityProviders
- "Create a identityProvider?" -> POST /api/atlas/v2/federationSettings/{federationSettingsId}/identityProviders
- "Delete a identityProvider?" -> DELETE /api/atlas/v2/federationSettings/{federationSettingsId}/identityProviders/{identityProviderId}
- "Get identityProvider details?" -> GET /api/atlas/v2/federationSettings/{federationSettingsId}/identityProviders/{identityProviderId}
- "Partially update a identityProvider?" -> PATCH /api/atlas/v2/federationSettings/{federationSettingsId}/identityProviders/{identityProviderId}
- "List all metadata.xml?" -> GET /api/atlas/v2/federationSettings/{federationSettingsId}/identityProviders/{identityProviderId}/metadata.xml
- "List all groups?" -> GET /api/atlas/v2/groups
- "Create a group?" -> POST /api/atlas/v2/groups
- "Delete a group?" -> DELETE /api/atlas/v2/groups/{groupId}
- "Get group details?" -> GET /api/atlas/v2/groups/{groupId}
- "Partially update a group?" -> PATCH /api/atlas/v2/groups/{groupId}
- "Create a access?" -> POST /api/atlas/v2/groups/{groupId}/access
- "List all accessList?" -> GET /api/atlas/v2/groups/{groupId}/accessList
- "Create a accessList?" -> POST /api/atlas/v2/groups/{groupId}/accessList
- "Delete a accessList?" -> DELETE /api/atlas/v2/groups/{groupId}/accessList/{entryValue}
- "Get accessList details?" -> GET /api/atlas/v2/groups/{groupId}/accessList/{entryValue}
- "List all status?" -> GET /api/atlas/v2/groups/{groupId}/accessList/{entryValue}/status
- "List all activityFeed?" -> GET /api/atlas/v2/groups/{groupId}/activityFeed
- "List all aiModelApiKeys?" -> GET /api/atlas/v2/groups/{groupId}/aiModelApiKeys
- "Create a aiModelApiKey?" -> POST /api/atlas/v2/groups/{groupId}/aiModelApiKeys
- "Delete a aiModelApiKey?" -> DELETE /api/atlas/v2/groups/{groupId}/aiModelApiKeys/{apiKeyId}
- "Get aiModelApiKey details?" -> GET /api/atlas/v2/groups/{groupId}/aiModelApiKeys/{apiKeyId}
- "Partially update a aiModelApiKey?" -> PATCH /api/atlas/v2/groups/{groupId}/aiModelApiKeys/{apiKeyId}
- "List all aiModelRateLimits?" -> GET /api/atlas/v2/groups/{groupId}/aiModelRateLimits
- "Get aiModelRateLimit details?" -> GET /api/atlas/v2/groups/{groupId}/aiModelRateLimits/{modelGroupName}
- "Partially update a aiModelRateLimit?" -> PATCH /api/atlas/v2/groups/{groupId}/aiModelRateLimits/{modelGroupName}
- "Create a aiModelRateLimits:reset?" -> POST /api/atlas/v2/groups/{groupId}/aiModelRateLimits:reset
- "List all alertConfigs?" -> GET /api/atlas/v2/groups/{groupId}/alertConfigs
- "Create a alertConfig?" -> POST /api/atlas/v2/groups/{groupId}/alertConfigs
- "Delete a alertConfig?" -> DELETE /api/atlas/v2/groups/{groupId}/alertConfigs/{alertConfigId}
- "Get alertConfig details?" -> GET /api/atlas/v2/groups/{groupId}/alertConfigs/{alertConfigId}
- "Partially update a alertConfig?" -> PATCH /api/atlas/v2/groups/{groupId}/alertConfigs/{alertConfigId}
- "Update a alertConfig?" -> PUT /api/atlas/v2/groups/{groupId}/alertConfigs/{alertConfigId}
- "List all alerts?" -> GET /api/atlas/v2/groups/{groupId}/alertConfigs/{alertConfigId}/alerts
- "List all alerts?" -> GET /api/atlas/v2/groups/{groupId}/alerts
- "Get alert details?" -> GET /api/atlas/v2/groups/{groupId}/alerts/{alertId}
- "Partially update a alert?" -> PATCH /api/atlas/v2/groups/{groupId}/alerts/{alertId}
- "List all alertConfigs?" -> GET /api/atlas/v2/groups/{groupId}/alerts/{alertId}/alertConfigs
- "List all apiKeys?" -> GET /api/atlas/v2/groups/{groupId}/apiKeys
- "Create a apiKey?" -> POST /api/atlas/v2/groups/{groupId}/apiKeys
- "Delete a apiKey?" -> DELETE /api/atlas/v2/groups/{groupId}/apiKeys/{apiUserId}
- "Partially update a apiKey?" -> PATCH /api/atlas/v2/groups/{groupId}/apiKeys/{apiUserId}
- "List all auditLog?" -> GET /api/atlas/v2/groups/{groupId}/auditLog
- "List all awsCustomDNS?" -> GET /api/atlas/v2/groups/{groupId}/awsCustomDNS
- "List all privateEndpoints?" -> GET /api/atlas/v2/groups/{groupId}/backup/{cloudProvider}/privateEndpoints
- "Create a privateEndpoint?" -> POST /api/atlas/v2/groups/{groupId}/backup/{cloudProvider}/privateEndpoints
- "Delete a privateEndpoint?" -> DELETE /api/atlas/v2/groups/{groupId}/backup/{cloudProvider}/privateEndpoints/{endpointId}
- "Get privateEndpoint details?" -> GET /api/atlas/v2/groups/{groupId}/backup/{cloudProvider}/privateEndpoints/{endpointId}
- "List all exportBuckets?" -> GET /api/atlas/v2/groups/{groupId}/backup/exportBuckets
- "Create a exportBucket?" -> POST /api/atlas/v2/groups/{groupId}/backup/exportBuckets
- "Delete a exportBucket?" -> DELETE /api/atlas/v2/groups/{groupId}/backup/exportBuckets/{exportBucketId}
- "Get exportBucket details?" -> GET /api/atlas/v2/groups/{groupId}/backup/exportBuckets/{exportBucketId}
- "Partially update a exportBucket?" -> PATCH /api/atlas/v2/groups/{groupId}/backup/exportBuckets/{exportBucketId}
- "List all backupCompliancePolicy?" -> GET /api/atlas/v2/groups/{groupId}/backupCompliancePolicy
- "List all cloudProviderAccess?" -> GET /api/atlas/v2/groups/{groupId}/cloudProviderAccess
- "Create a cloudProviderAccess?" -> POST /api/atlas/v2/groups/{groupId}/cloudProviderAccess
- "Delete a cloudProviderAccess?" -> DELETE /api/atlas/v2/groups/{groupId}/cloudProviderAccess/{cloudProvider}/{roleId}
- "Get cloudProviderAccess details?" -> GET /api/atlas/v2/groups/{groupId}/cloudProviderAccess/{roleId}
- "Partially update a cloudProviderAccess?" -> PATCH /api/atlas/v2/groups/{groupId}/cloudProviderAccess/{roleId}
- "List all clusters?" -> GET /api/atlas/v2/groups/{groupId}/clusters
- "Create a cluster?" -> POST /api/atlas/v2/groups/{groupId}/clusters
- "Delete a cluster?" -> DELETE /api/atlas/v2/groups/{groupId}/clusters/{clusterName}
- "Get cluster details?" -> GET /api/atlas/v2/groups/{groupId}/clusters/{clusterName}
- "Partially update a cluster?" -> PATCH /api/atlas/v2/groups/{groupId}/clusters/{clusterName}
- "List all measurements?" -> GET /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/{clusterView}/{databaseName}/{collectionName}/collStats/measurements
- "List all namespaces?" -> GET /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/{clusterView}/collStats/namespaces
- "List all autoScalingConfiguration?" -> GET /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/autoScalingConfiguration
- "List all exports?" -> GET /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/backup/exports
- "Create a export?" -> POST /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/backup/exports
- "Get export details?" -> GET /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/backup/exports/{exportId}
- "List all restoreJobs?" -> GET /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/backup/restoreJobs
- "Create a restoreJob?" -> POST /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/backup/restoreJobs
- "Delete a restoreJob?" -> DELETE /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/backup/restoreJobs/{restoreJobId}
- "Get restoreJob details?" -> GET /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/backup/restoreJobs/{restoreJobId}
- "List all schedule?" -> GET /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/backup/schedule
- "List all snapshots?" -> GET /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/backup/snapshots
- "Create a snapshot?" -> POST /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/backup/snapshots
- "Delete a snapshot?" -> DELETE /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/backup/snapshots/{snapshotId}
- "Get snapshot details?" -> GET /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/backup/snapshots/{snapshotId}
- "Partially update a snapshot?" -> PATCH /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/backup/snapshots/{snapshotId}
- "Delete a shardedCluster?" -> DELETE /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/backup/snapshots/shardedCluster/{snapshotId}
- "Get shardedCluster details?" -> GET /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/backup/snapshots/shardedCluster/{snapshotId}
- "List all shardedClusters?" -> GET /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/backup/snapshots/shardedClusters
- "Create a download?" -> POST /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/backup/tenant/download
- "Create a restore?" -> POST /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/backup/tenant/restore
- "List all restores?" -> GET /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/backup/tenant/restores
- "Get restore details?" -> GET /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/backup/tenant/restores/{restoreId}
- "List all snapshots?" -> GET /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/backup/tenant/snapshots
- "Get snapshot details?" -> GET /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/backup/tenant/snapshots/{snapshotId}
- "List all backupCheckpoints?" -> GET /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/backupCheckpoints
- "Get backupCheckpoint details?" -> GET /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/backupCheckpoints/{checkpointId}
- "List all pinned?" -> GET /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/collStats/pinned
- "Create a indexe?" -> POST /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/fts/indexes
- "Get indexe details?" -> GET /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/fts/indexes/{databaseName}/{collectionName}
- "Delete a indexe?" -> DELETE /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/fts/indexes/{indexId}
- "Get indexe details?" -> GET /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/fts/indexes/{indexId}
- "Partially update a indexe?" -> PATCH /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/fts/indexes/{indexId}
- "List all globalWrites?" -> GET /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/globalWrites
- "Create a customZoneMapping?" -> POST /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/globalWrites/customZoneMapping
- "Create a managedNamespace?" -> POST /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/globalWrites/managedNamespaces
- "Create a index?" -> POST /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/index
- "List all onlineArchives?" -> GET /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/onlineArchives
- "Create a onlineArchive?" -> POST /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/onlineArchives
- "Delete a onlineArchive?" -> DELETE /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/onlineArchives/{archiveId}
- "Get onlineArchive details?" -> GET /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/onlineArchives/{archiveId}
- "Partially update a onlineArchive?" -> PATCH /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/onlineArchives/{archiveId}
- "List all queryLogs.gz?" -> GET /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/onlineArchives/queryLogs.gz
- "List all outageSimulation?" -> GET /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/outageSimulation
- "Create a outageSimulation?" -> POST /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/outageSimulation
- "List all dropIndexSuggestions?" -> GET /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/performanceAdvisor/dropIndexSuggestions
- "List all schemaAdvice?" -> GET /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/performanceAdvisor/schemaAdvice
- "List all suggestedIndexes?" -> GET /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/performanceAdvisor/suggestedIndexes
- "List all processArgs?" -> GET /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/processArgs
- "List all details?" -> GET /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/queryShapeInsights/{queryShapeHash}/details
- "List all summaries?" -> GET /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/queryShapeInsights/summaries
- "List all queryShapes?" -> GET /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/queryShapes
- "Get queryShape details?" -> GET /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/queryShapes/{queryShapeHash}
- "Partially update a queryShape?" -> PATCH /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/queryShapes/{queryShapeHash}
- "Create a restartPrimary?" -> POST /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/restartPrimaries
- "List all restoreJobs?" -> GET /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/restoreJobs
- "Create a restoreJob?" -> POST /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/restoreJobs
- "Get restoreJob details?" -> GET /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/restoreJobs/{jobId}
- "List all deployment?" -> GET /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/search/deployment
- "Create a deployment?" -> POST /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/search/deployment
- "List all indexes?" -> GET /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/search/indexes
- "Create a indexe?" -> POST /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/search/indexes
- "Get indexe details?" -> GET /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/search/indexes/{databaseName}/{collectionName}
- "Delete a indexe?" -> DELETE /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/search/indexes/{databaseName}/{collectionName}/{indexName}
- "Get indexe details?" -> GET /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/search/indexes/{databaseName}/{collectionName}/{indexName}
- "Partially update a indexe?" -> PATCH /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/search/indexes/{databaseName}/{collectionName}/{indexName}
- "Delete a indexe?" -> DELETE /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/search/indexes/{indexId}
- "Get indexe details?" -> GET /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/search/indexes/{indexId}
- "Partially update a indexe?" -> PATCH /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/search/indexes/{indexId}
- "List all snapshotSchedule?" -> GET /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/snapshotSchedule
- "List all snapshots?" -> GET /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/snapshots
- "Delete a snapshot?" -> DELETE /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/snapshots/{snapshotId}
- "Get snapshot details?" -> GET /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/snapshots/{snapshotId}
- "Partially update a snapshot?" -> PATCH /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/snapshots/{snapshotId}
- "List all status?" -> GET /api/atlas/v2/groups/{groupId}/clusters/{clusterName}/status
- "Get log details?" -> GET /api/atlas/v2/groups/{groupId}/clusters/{hostName}/logs/{logName}.gz
- "List all regions?" -> GET /api/atlas/v2/groups/{groupId}/clusters/provider/regions
- "Create a tenantUpgrade?" -> POST /api/atlas/v2/groups/{groupId}/clusters/tenantUpgrade
- "Create a tenantUpgradeToServerless?" -> POST /api/atlas/v2/groups/{groupId}/clusters/tenantUpgradeToServerless
- "List all metrics?" -> GET /api/atlas/v2/groups/{groupId}/collStats/metrics
- "List all containers?" -> GET /api/atlas/v2/groups/{groupId}/containers
- "Create a container?" -> POST /api/atlas/v2/groups/{groupId}/containers
- "Delete a container?" -> DELETE /api/atlas/v2/groups/{groupId}/containers/{containerId}
- "Get container details?" -> GET /api/atlas/v2/groups/{groupId}/containers/{containerId}
- "Partially update a container?" -> PATCH /api/atlas/v2/groups/{groupId}/containers/{containerId}
- "List all all?" -> GET /api/atlas/v2/groups/{groupId}/containers/all
- "List all roles?" -> GET /api/atlas/v2/groups/{groupId}/customDBRoles/roles
- "Create a role?" -> POST /api/atlas/v2/groups/{groupId}/customDBRoles/roles
- "Delete a role?" -> DELETE /api/atlas/v2/groups/{groupId}/customDBRoles/roles/{roleName}
- "Get role details?" -> GET /api/atlas/v2/groups/{groupId}/customDBRoles/roles/{roleName}
- "Partially update a role?" -> PATCH /api/atlas/v2/groups/{groupId}/customDBRoles/roles/{roleName}
- "List all dataFederation?" -> GET /api/atlas/v2/groups/{groupId}/dataFederation
- "Create a dataFederation?" -> POST /api/atlas/v2/groups/{groupId}/dataFederation
- "Delete a dataFederation?" -> DELETE /api/atlas/v2/groups/{groupId}/dataFederation/{tenantName}
- "Get dataFederation details?" -> GET /api/atlas/v2/groups/{groupId}/dataFederation/{tenantName}
- "Partially update a dataFederation?" -> PATCH /api/atlas/v2/groups/{groupId}/dataFederation/{tenantName}
- "List all limits?" -> GET /api/atlas/v2/groups/{groupId}/dataFederation/{tenantName}/limits
- "Delete a limit?" -> DELETE /api/atlas/v2/groups/{groupId}/dataFederation/{tenantName}/limits/{limitName}
- "Get limit details?" -> GET /api/atlas/v2/groups/{groupId}/dataFederation/{tenantName}/limits/{limitName}
- "Partially update a limit?" -> PATCH /api/atlas/v2/groups/{groupId}/dataFederation/{tenantName}/limits/{limitName}
- "List all queryLogs.gz?" -> GET /api/atlas/v2/groups/{groupId}/dataFederation/{tenantName}/queryLogs.gz
- "List all databaseUsers?" -> GET /api/atlas/v2/groups/{groupId}/databaseUsers
- "Create a databaseUser?" -> POST /api/atlas/v2/groups/{groupId}/databaseUsers
- "Delete a databaseUser?" -> DELETE /api/atlas/v2/groups/{groupId}/databaseUsers/{databaseName}/{username}
- "Get databaseUser details?" -> GET /api/atlas/v2/groups/{groupId}/databaseUsers/{databaseName}/{username}
- "Partially update a databaseUser?" -> PATCH /api/atlas/v2/groups/{groupId}/databaseUsers/{databaseName}/{username}
- "List all certs?" -> GET /api/atlas/v2/groups/{groupId}/databaseUsers/{username}/certs
- "Create a cert?" -> POST /api/atlas/v2/groups/{groupId}/databaseUsers/{username}/certs
- "Get cluster details?" -> GET /api/atlas/v2/groups/{groupId}/dbAccessHistory/clusters/{clusterName}
- "Get process details?" -> GET /api/atlas/v2/groups/{groupId}/dbAccessHistory/processes/{hostname}
- "List all encryptionAtRest?" -> GET /api/atlas/v2/groups/{groupId}/encryptionAtRest
- "List all privateEndpoints?" -> GET /api/atlas/v2/groups/{groupId}/encryptionAtRest/{cloudProvider}/privateEndpoints
- "Create a privateEndpoint?" -> POST /api/atlas/v2/groups/{groupId}/encryptionAtRest/{cloudProvider}/privateEndpoints
- "Delete a privateEndpoint?" -> DELETE /api/atlas/v2/groups/{groupId}/encryptionAtRest/{cloudProvider}/privateEndpoints/{endpointId}
- "Get privateEndpoint details?" -> GET /api/atlas/v2/groups/{groupId}/encryptionAtRest/{cloudProvider}/privateEndpoints/{endpointId}
- "List all events?" -> GET /api/atlas/v2/groups/{groupId}/events
- "Get event details?" -> GET /api/atlas/v2/groups/{groupId}/events/{eventId}
- "List all flexClusters?" -> GET /api/atlas/v2/groups/{groupId}/flexClusters
- "Create a flexCluster?" -> POST /api/atlas/v2/groups/{groupId}/flexClusters
- "Delete a flexCluster?" -> DELETE /api/atlas/v2/groups/{groupId}/flexClusters/{name}
- "Get flexCluster details?" -> GET /api/atlas/v2/groups/{groupId}/flexClusters/{name}
- "Partially update a flexCluster?" -> PATCH /api/atlas/v2/groups/{groupId}/flexClusters/{name}
- "Create a download?" -> POST /api/atlas/v2/groups/{groupId}/flexClusters/{name}/backup/download
- "List all restoreJobs?" -> GET /api/atlas/v2/groups/{groupId}/flexClusters/{name}/backup/restoreJobs
- "Create a restoreJob?" -> POST /api/atlas/v2/groups/{groupId}/flexClusters/{name}/backup/restoreJobs
- "Get restoreJob details?" -> GET /api/atlas/v2/groups/{groupId}/flexClusters/{name}/backup/restoreJobs/{restoreJobId}
- "List all snapshots?" -> GET /api/atlas/v2/groups/{groupId}/flexClusters/{name}/backup/snapshots
- "Get snapshot details?" -> GET /api/atlas/v2/groups/{groupId}/flexClusters/{name}/backup/snapshots/{snapshotId}
- "Create a flexClusters:tenantUpgrade?" -> POST /api/atlas/v2/groups/{groupId}/flexClusters:tenantUpgrade
- "List all metrics?" -> GET /api/atlas/v2/groups/{groupId}/hosts/{processId}/fts/metrics
- "List all measurements?" -> GET /api/atlas/v2/groups/{groupId}/hosts/{processId}/fts/metrics/indexes/{databaseName}/{collectionName}/{indexName}/measurements
- "List all measurements?" -> GET /api/atlas/v2/groups/{groupId}/hosts/{processId}/fts/metrics/indexes/{databaseName}/{collectionName}/measurements
- "List all measurements?" -> GET /api/atlas/v2/groups/{groupId}/hosts/{processId}/fts/metrics/measurements
- "List all integrations?" -> GET /api/atlas/v2/groups/{groupId}/integrations
- "Delete a integration?" -> DELETE /api/atlas/v2/groups/{groupId}/integrations/{integrationType}
- "Get integration details?" -> GET /api/atlas/v2/groups/{groupId}/integrations/{integrationType}
- "Update a integration?" -> PUT /api/atlas/v2/groups/{groupId}/integrations/{integrationType}
- "List all invites?" -> GET /api/atlas/v2/groups/{groupId}/invites
- "Create a invite?" -> POST /api/atlas/v2/groups/{groupId}/invites
- "Delete a invite?" -> DELETE /api/atlas/v2/groups/{groupId}/invites/{invitationId}
- "Get invite details?" -> GET /api/atlas/v2/groups/{groupId}/invites/{invitationId}
- "Partially update a invite?" -> PATCH /api/atlas/v2/groups/{groupId}/invites/{invitationId}
- "List all ipAddresses?" -> GET /api/atlas/v2/groups/{groupId}/ipAddresses
- "List all limits?" -> GET /api/atlas/v2/groups/{groupId}/limits
- "Delete a limit?" -> DELETE /api/atlas/v2/groups/{groupId}/limits/{limitName}
- "Get limit details?" -> GET /api/atlas/v2/groups/{groupId}/limits/{limitName}
- "Partially update a limit?" -> PATCH /api/atlas/v2/groups/{groupId}/limits/{limitName}
- "Create a liveMigration?" -> POST /api/atlas/v2/groups/{groupId}/liveMigrations
- "Get liveMigration details?" -> GET /api/atlas/v2/groups/{groupId}/liveMigrations/{liveMigrationId}
- "Create a validate?" -> POST /api/atlas/v2/groups/{groupId}/liveMigrations/validate
- "Get validate details?" -> GET /api/atlas/v2/groups/{groupId}/liveMigrations/validate/{validationId}
- "List all logIntegrations?" -> GET /api/atlas/v2/groups/{groupId}/logIntegrations
- "Create a logIntegration?" -> POST /api/atlas/v2/groups/{groupId}/logIntegrations
- "Delete a logIntegration?" -> DELETE /api/atlas/v2/groups/{groupId}/logIntegrations/{id}
- "Get logIntegration details?" -> GET /api/atlas/v2/groups/{groupId}/logIntegrations/{id}
- "Update a logIntegration?" -> PUT /api/atlas/v2/groups/{groupId}/logIntegrations/{id}
- "List all maintenanceWindow?" -> GET /api/atlas/v2/groups/{groupId}/maintenanceWindow
- "Create a autoDefer?" -> POST /api/atlas/v2/groups/{groupId}/maintenanceWindow/autoDefer
- "Create a defer?" -> POST /api/atlas/v2/groups/{groupId}/maintenanceWindow/defer
- "List all managedSlowMs?" -> GET /api/atlas/v2/groups/{groupId}/managedSlowMs
- "Create a enable?" -> POST /api/atlas/v2/groups/{groupId}/managedSlowMs/enable
- "List all mongoDBVersions?" -> GET /api/atlas/v2/groups/{groupId}/mongoDBVersions
- "List all peers?" -> GET /api/atlas/v2/groups/{groupId}/peers
- "Create a peer?" -> POST /api/atlas/v2/groups/{groupId}/peers
- "Delete a peer?" -> DELETE /api/atlas/v2/groups/{groupId}/peers/{peerId}
- "Get peer details?" -> GET /api/atlas/v2/groups/{groupId}/peers/{peerId}
- "Partially update a peer?" -> PATCH /api/atlas/v2/groups/{groupId}/peers/{peerId}
- "List all pipelines?" -> GET /api/atlas/v2/groups/{groupId}/pipelines
- "Create a pipeline?" -> POST /api/atlas/v2/groups/{groupId}/pipelines
- "Delete a pipeline?" -> DELETE /api/atlas/v2/groups/{groupId}/pipelines/{pipelineName}
- "Get pipeline details?" -> GET /api/atlas/v2/groups/{groupId}/pipelines/{pipelineName}
- "Partially update a pipeline?" -> PATCH /api/atlas/v2/groups/{groupId}/pipelines/{pipelineName}
- "List all availableSchedules?" -> GET /api/atlas/v2/groups/{groupId}/pipelines/{pipelineName}/availableSchedules
- "List all availableSnapshots?" -> GET /api/atlas/v2/groups/{groupId}/pipelines/{pipelineName}/availableSnapshots
- "Create a pause?" -> POST /api/atlas/v2/groups/{groupId}/pipelines/{pipelineName}/pause
- "Create a resume?" -> POST /api/atlas/v2/groups/{groupId}/pipelines/{pipelineName}/resume
- "List all runs?" -> GET /api/atlas/v2/groups/{groupId}/pipelines/{pipelineName}/runs
- "Delete a run?" -> DELETE /api/atlas/v2/groups/{groupId}/pipelines/{pipelineName}/runs/{pipelineRunId}
- "Get run details?" -> GET /api/atlas/v2/groups/{groupId}/pipelines/{pipelineName}/runs/{pipelineRunId}
- "Create a trigger?" -> POST /api/atlas/v2/groups/{groupId}/pipelines/{pipelineName}/trigger
- "List all endpointService?" -> GET /api/atlas/v2/groups/{groupId}/privateEndpoint/{cloudProvider}/endpointService
- "Delete a endpointService?" -> DELETE /api/atlas/v2/groups/{groupId}/privateEndpoint/{cloudProvider}/endpointService/{endpointServiceId}
- "Get endpointService details?" -> GET /api/atlas/v2/groups/{groupId}/privateEndpoint/{cloudProvider}/endpointService/{endpointServiceId}
- "Create a endpoint?" -> POST /api/atlas/v2/groups/{groupId}/privateEndpoint/{cloudProvider}/endpointService/{endpointServiceId}/endpoint
- "Delete a endpoint?" -> DELETE /api/atlas/v2/groups/{groupId}/privateEndpoint/{cloudProvider}/endpointService/{endpointServiceId}/endpoint/{endpointId}
- "Get endpoint details?" -> GET /api/atlas/v2/groups/{groupId}/privateEndpoint/{cloudProvider}/endpointService/{endpointServiceId}/endpoint/{endpointId}
- "Create a endpointService?" -> POST /api/atlas/v2/groups/{groupId}/privateEndpoint/endpointService
- "List all regionalMode?" -> GET /api/atlas/v2/groups/{groupId}/privateEndpoint/regionalMode
- "List all endpoint?" -> GET /api/atlas/v2/groups/{groupId}/privateEndpoint/serverless/instance/{instanceName}/endpoint
- "Create a endpoint?" -> POST /api/atlas/v2/groups/{groupId}/privateEndpoint/serverless/instance/{instanceName}/endpoint
- "Delete a endpoint?" -> DELETE /api/atlas/v2/groups/{groupId}/privateEndpoint/serverless/instance/{instanceName}/endpoint/{endpointId}
- "Get endpoint details?" -> GET /api/atlas/v2/groups/{groupId}/privateEndpoint/serverless/instance/{instanceName}/endpoint/{endpointId}
- "Partially update a endpoint?" -> PATCH /api/atlas/v2/groups/{groupId}/privateEndpoint/serverless/instance/{instanceName}/endpoint/{endpointId}
- "List all privateIpMode?" -> GET /api/atlas/v2/groups/{groupId}/privateIpMode
- "List all endpointIds?" -> GET /api/atlas/v2/groups/{groupId}/privateNetworkSettings/endpointIds
- "Create a endpointId?" -> POST /api/atlas/v2/groups/{groupId}/privateNetworkSettings/endpointIds
- "Delete a endpointId?" -> DELETE /api/atlas/v2/groups/{groupId}/privateNetworkSettings/endpointIds/{endpointId}
- "Get endpointId details?" -> GET /api/atlas/v2/groups/{groupId}/privateNetworkSettings/endpointIds/{endpointId}
- "List all processes?" -> GET /api/atlas/v2/groups/{groupId}/processes
- "Get process details?" -> GET /api/atlas/v2/groups/{groupId}/processes/{processId}
- "List all measurements?" -> GET /api/atlas/v2/groups/{groupId}/processes/{processId}/{databaseName}/{collectionName}/collStats/measurements
- "List all namespaces?" -> GET /api/atlas/v2/groups/{groupId}/processes/{processId}/collStats/namespaces
- "List all databases?" -> GET /api/atlas/v2/groups/{groupId}/processes/{processId}/databases
- "Get database details?" -> GET /api/atlas/v2/groups/{groupId}/processes/{processId}/databases/{databaseName}
- "List all measurements?" -> GET /api/atlas/v2/groups/{groupId}/processes/{processId}/databases/{databaseName}/measurements
- "List all disks?" -> GET /api/atlas/v2/groups/{groupId}/processes/{processId}/disks
- "Get disk details?" -> GET /api/atlas/v2/groups/{groupId}/processes/{processId}/disks/{partitionName}
- "List all measurements?" -> GET /api/atlas/v2/groups/{groupId}/processes/{processId}/disks/{partitionName}/measurements
- "List all measurements?" -> GET /api/atlas/v2/groups/{groupId}/processes/{processId}/measurements
- "List all namespaces?" -> GET /api/atlas/v2/groups/{groupId}/processes/{processId}/performanceAdvisor/namespaces
- "List all slowQueryLogs?" -> GET /api/atlas/v2/groups/{groupId}/processes/{processId}/performanceAdvisor/slowQueryLogs
- "List all suggestedIndexes?" -> GET /api/atlas/v2/groups/{groupId}/processes/{processId}/performanceAdvisor/suggestedIndexes
- "List all pushBasedLogExport?" -> GET /api/atlas/v2/groups/{groupId}/pushBasedLogExport
- "Create a pushBasedLogExport?" -> POST /api/atlas/v2/groups/{groupId}/pushBasedLogExport
- "Get sampleDatasetLoad details?" -> GET /api/atlas/v2/groups/{groupId}/sampleDatasetLoad/{sampleDatasetId}
- "Get sandbox details?" -> GET /api/atlas/v2/groups/{groupId}/sandbox/{sandboxConfigId}:generateClusterDescription
- "List all serverless?" -> GET /api/atlas/v2/groups/{groupId}/serverless
- "Create a serverless?" -> POST /api/atlas/v2/groups/{groupId}/serverless
- "List all restoreJobs?" -> GET /api/atlas/v2/groups/{groupId}/serverless/{clusterName}/backup/restoreJobs
- "Create a restoreJob?" -> POST /api/atlas/v2/groups/{groupId}/serverless/{clusterName}/backup/restoreJobs
- "Get restoreJob details?" -> GET /api/atlas/v2/groups/{groupId}/serverless/{clusterName}/backup/restoreJobs/{restoreJobId}
- "List all snapshots?" -> GET /api/atlas/v2/groups/{groupId}/serverless/{clusterName}/backup/snapshots
- "Get snapshot details?" -> GET /api/atlas/v2/groups/{groupId}/serverless/{clusterName}/backup/snapshots/{snapshotId}
- "List all autoIndexing?" -> GET /api/atlas/v2/groups/{groupId}/serverless/{clusterName}/performanceAdvisor/autoIndexing
- "Create a autoIndexing?" -> POST /api/atlas/v2/groups/{groupId}/serverless/{clusterName}/performanceAdvisor/autoIndexing
- "Delete a serverless?" -> DELETE /api/atlas/v2/groups/{groupId}/serverless/{name}
- "Get serverless details?" -> GET /api/atlas/v2/groups/{groupId}/serverless/{name}
- "Partially update a serverless?" -> PATCH /api/atlas/v2/groups/{groupId}/serverless/{name}
- "List all serviceAccounts?" -> GET /api/atlas/v2/groups/{groupId}/serviceAccounts
- "Create a serviceAccount?" -> POST /api/atlas/v2/groups/{groupId}/serviceAccounts
- "Delete a serviceAccount?" -> DELETE /api/atlas/v2/groups/{groupId}/serviceAccounts/{clientId}
- "Get serviceAccount details?" -> GET /api/atlas/v2/groups/{groupId}/serviceAccounts/{clientId}
- "Partially update a serviceAccount?" -> PATCH /api/atlas/v2/groups/{groupId}/serviceAccounts/{clientId}
- "List all accessList?" -> GET /api/atlas/v2/groups/{groupId}/serviceAccounts/{clientId}/accessList
- "Create a accessList?" -> POST /api/atlas/v2/groups/{groupId}/serviceAccounts/{clientId}/accessList
- "Delete a accessList?" -> DELETE /api/atlas/v2/groups/{groupId}/serviceAccounts/{clientId}/accessList/{ipAddress}
- "Create a secret?" -> POST /api/atlas/v2/groups/{groupId}/serviceAccounts/{clientId}/secrets
- "Delete a secret?" -> DELETE /api/atlas/v2/groups/{groupId}/serviceAccounts/{clientId}/secrets/{secretId}
- "List all settings?" -> GET /api/atlas/v2/groups/{groupId}/settings
- "List all standbyLinks?" -> GET /api/atlas/v2/groups/{groupId}/standbyLinks
- "Create a standbyLink?" -> POST /api/atlas/v2/groups/{groupId}/standbyLinks
- "Delete a standbyLink?" -> DELETE /api/atlas/v2/groups/{groupId}/standbyLinks/{standbyLinkId}
- "Get standbyLink details?" -> GET /api/atlas/v2/groups/{groupId}/standbyLinks/{standbyLinkId}
- "List all failovers?" -> GET /api/atlas/v2/groups/{groupId}/standbyLinks/{standbyLinkId}/failovers
- "Create a failover?" -> POST /api/atlas/v2/groups/{groupId}/standbyLinks/{standbyLinkId}/failovers
- "Get failover details?" -> GET /api/atlas/v2/groups/{groupId}/standbyLinks/{standbyLinkId}/failovers/{failoverId}
- "List all streams?" -> GET /api/atlas/v2/groups/{groupId}/streams
- "Create a stream?" -> POST /api/atlas/v2/groups/{groupId}/streams
- "Delete a stream?" -> DELETE /api/atlas/v2/groups/{groupId}/streams/{tenantName}
- "Get stream details?" -> GET /api/atlas/v2/groups/{groupId}/streams/{tenantName}
- "Partially update a stream?" -> PATCH /api/atlas/v2/groups/{groupId}/streams/{tenantName}
- "List all auditLogs?" -> GET /api/atlas/v2/groups/{groupId}/streams/{tenantName}/auditLogs
- "List all connections?" -> GET /api/atlas/v2/groups/{groupId}/streams/{tenantName}/connections
- "Create a connection?" -> POST /api/atlas/v2/groups/{groupId}/streams/{tenantName}/connections
- "Delete a connection?" -> DELETE /api/atlas/v2/groups/{groupId}/streams/{tenantName}/connections/{connectionName}
- "Get connection details?" -> GET /api/atlas/v2/groups/{groupId}/streams/{tenantName}/connections/{connectionName}
- "Partially update a connection?" -> PATCH /api/atlas/v2/groups/{groupId}/streams/{tenantName}/connections/{connectionName}
- "Create a processor?" -> POST /api/atlas/v2/groups/{groupId}/streams/{tenantName}/processor
- "Delete a processor?" -> DELETE /api/atlas/v2/groups/{groupId}/streams/{tenantName}/processor/{processorName}
- "Get processor details?" -> GET /api/atlas/v2/groups/{groupId}/streams/{tenantName}/processor/{processorName}
- "Partially update a processor?" -> PATCH /api/atlas/v2/groups/{groupId}/streams/{tenantName}/processor/{processorName}
- "List all processors?" -> GET /api/atlas/v2/groups/{groupId}/streams/{tenantName}/processors
- "Get stream details?" -> GET /api/atlas/v2/groups/{groupId}/streams/{tenantName}:downloadOperationalLogs
- "List all accountDetails?" -> GET /api/atlas/v2/groups/{groupId}/streams/accountDetails
- "List all activeVpcPeeringConnections?" -> GET /api/atlas/v2/groups/{groupId}/streams/activeVpcPeeringConnections
- "List all privateLinkConnections?" -> GET /api/atlas/v2/groups/{groupId}/streams/privateLinkConnections
- "Create a privateLinkConnection?" -> POST /api/atlas/v2/groups/{groupId}/streams/privateLinkConnections
- "Delete a privateLinkConnection?" -> DELETE /api/atlas/v2/groups/{groupId}/streams/privateLinkConnections/{connectionId}
- "Get privateLinkConnection details?" -> GET /api/atlas/v2/groups/{groupId}/streams/privateLinkConnections/{connectionId}
- "List all vpcPeeringConnections?" -> GET /api/atlas/v2/groups/{groupId}/streams/vpcPeeringConnections
- "Delete a vpcPeeringConnection?" -> DELETE /api/atlas/v2/groups/{groupId}/streams/vpcPeeringConnections/{id}
- "Create a streams:withSampleConnection?" -> POST /api/atlas/v2/groups/{groupId}/streams:withSampleConnections
- "List all teams?" -> GET /api/atlas/v2/groups/{groupId}/teams
- "Create a team?" -> POST /api/atlas/v2/groups/{groupId}/teams
- "Delete a team?" -> DELETE /api/atlas/v2/groups/{groupId}/teams/{teamId}
- "Get team details?" -> GET /api/atlas/v2/groups/{groupId}/teams/{teamId}
- "Partially update a team?" -> PATCH /api/atlas/v2/groups/{groupId}/teams/{teamId}
- "List all userSecurity?" -> GET /api/atlas/v2/groups/{groupId}/userSecurity
- "Create a verify?" -> POST /api/atlas/v2/groups/{groupId}/userSecurity/ldap/verify
- "Get verify details?" -> GET /api/atlas/v2/groups/{groupId}/userSecurity/ldap/verify/{requestId}
- "List all users?" -> GET /api/atlas/v2/groups/{groupId}/users
- "Create a user?" -> POST /api/atlas/v2/groups/{groupId}/users
- "Delete a user?" -> DELETE /api/atlas/v2/groups/{groupId}/users/{userId}
- "Get user details?" -> GET /api/atlas/v2/groups/{groupId}/users/{userId}
- "Get byName details?" -> GET /api/atlas/v2/groups/byName/{groupName}
- "List all orgs?" -> GET /api/atlas/v2/orgs
- "Create a org?" -> POST /api/atlas/v2/orgs
- "Delete a org?" -> DELETE /api/atlas/v2/orgs/{orgId}
- "Get org details?" -> GET /api/atlas/v2/orgs/{orgId}
- "Partially update a org?" -> PATCH /api/atlas/v2/orgs/{orgId}
- "List all activityFeed?" -> GET /api/atlas/v2/orgs/{orgId}/activityFeed
- "List all aiModelApiKeys?" -> GET /api/atlas/v2/orgs/{orgId}/aiModelApiKeys
- "Get aiModelApiKey details?" -> GET /api/atlas/v2/orgs/{orgId}/aiModelApiKeys/{apiKeyId}
- "List all aiModelRateLimits?" -> GET /api/atlas/v2/orgs/{orgId}/aiModelRateLimits
- "Get aiModelRateLimit details?" -> GET /api/atlas/v2/orgs/{orgId}/aiModelRateLimits/{modelGroupName}
- "List all apiKeys?" -> GET /api/atlas/v2/orgs/{orgId}/apiKeys
- "Create a apiKey?" -> POST /api/atlas/v2/orgs/{orgId}/apiKeys
- "Delete a apiKey?" -> DELETE /api/atlas/v2/orgs/{orgId}/apiKeys/{apiUserId}
- "Get apiKey details?" -> GET /api/atlas/v2/orgs/{orgId}/apiKeys/{apiUserId}
- "Partially update a apiKey?" -> PATCH /api/atlas/v2/orgs/{orgId}/apiKeys/{apiUserId}
- "List all accessList?" -> GET /api/atlas/v2/orgs/{orgId}/apiKeys/{apiUserId}/accessList
- "Create a accessList?" -> POST /api/atlas/v2/orgs/{orgId}/apiKeys/{apiUserId}/accessList
- "Delete a accessList?" -> DELETE /api/atlas/v2/orgs/{orgId}/apiKeys/{apiUserId}/accessList/{ipAddress}
- "Get accessList details?" -> GET /api/atlas/v2/orgs/{orgId}/apiKeys/{apiUserId}/accessList/{ipAddress}
- "List all associatedInvoices?" -> GET /api/atlas/v2/orgs/{orgId}/associatedInvoices
- "Create a usage?" -> POST /api/atlas/v2/orgs/{orgId}/billing/costExplorer/usage
- "Get usage details?" -> GET /api/atlas/v2/orgs/{orgId}/billing/costExplorer/usage/{token}
- "List all events?" -> GET /api/atlas/v2/orgs/{orgId}/events
- "Get event details?" -> GET /api/atlas/v2/orgs/{orgId}/events/{eventId}
- "List all federationSettings?" -> GET /api/atlas/v2/orgs/{orgId}/federationSettings
- "List all groups?" -> GET /api/atlas/v2/orgs/{orgId}/groups
- "List all invites?" -> GET /api/atlas/v2/orgs/{orgId}/invites
- "Create a invite?" -> POST /api/atlas/v2/orgs/{orgId}/invites
- "Delete a invite?" -> DELETE /api/atlas/v2/orgs/{orgId}/invites/{invitationId}
- "Get invite details?" -> GET /api/atlas/v2/orgs/{orgId}/invites/{invitationId}
- "Partially update a invite?" -> PATCH /api/atlas/v2/orgs/{orgId}/invites/{invitationId}
- "List all invoices?" -> GET /api/atlas/v2/orgs/{orgId}/invoices
- "Get invoice details?" -> GET /api/atlas/v2/orgs/{orgId}/invoices/{invoiceId}
- "List all csv?" -> GET /api/atlas/v2/orgs/{orgId}/invoices/{invoiceId}/csv
- "List all lineItems:search?" -> GET /api/atlas/v2/orgs/{orgId}/invoices/{invoiceId}/lineItems:search
- "List all pending?" -> GET /api/atlas/v2/orgs/{orgId}/invoices/pending
- "List all availableProjects?" -> GET /api/atlas/v2/orgs/{orgId}/liveMigrations/availableProjects
- "Create a linkToken?" -> POST /api/atlas/v2/orgs/{orgId}/liveMigrations/linkTokens
- "List all nonCompliantResources?" -> GET /api/atlas/v2/orgs/{orgId}/nonCompliantResources
- "List all resourcePolicies?" -> GET /api/atlas/v2/orgs/{orgId}/resourcePolicies
- "Create a resourcePolicy?" -> POST /api/atlas/v2/orgs/{orgId}/resourcePolicies
- "Delete a resourcePolicy?" -> DELETE /api/atlas/v2/orgs/{orgId}/resourcePolicies/{resourcePolicyId}
- "Get resourcePolicy details?" -> GET /api/atlas/v2/orgs/{orgId}/resourcePolicies/{resourcePolicyId}
- "Partially update a resourcePolicy?" -> PATCH /api/atlas/v2/orgs/{orgId}/resourcePolicies/{resourcePolicyId}
- "Create a resourcePolicies:validate?" -> POST /api/atlas/v2/orgs/{orgId}/resourcePolicies:validate
- "List all sandboxConfig?" -> GET /api/atlas/v2/orgs/{orgId}/sandboxConfig
- "Create a sandboxConfig?" -> POST /api/atlas/v2/orgs/{orgId}/sandboxConfig
- "Delete a sandboxConfig?" -> DELETE /api/atlas/v2/orgs/{orgId}/sandboxConfig/{sandboxConfigId}
- "Get sandboxConfig details?" -> GET /api/atlas/v2/orgs/{orgId}/sandboxConfig/{sandboxConfigId}
- "Partially update a sandboxConfig?" -> PATCH /api/atlas/v2/orgs/{orgId}/sandboxConfig/{sandboxConfigId}
- "List all serviceAccounts?" -> GET /api/atlas/v2/orgs/{orgId}/serviceAccounts
- "Create a serviceAccount?" -> POST /api/atlas/v2/orgs/{orgId}/serviceAccounts
- "Delete a serviceAccount?" -> DELETE /api/atlas/v2/orgs/{orgId}/serviceAccounts/{clientId}
- "Get serviceAccount details?" -> GET /api/atlas/v2/orgs/{orgId}/serviceAccounts/{clientId}
- "Partially update a serviceAccount?" -> PATCH /api/atlas/v2/orgs/{orgId}/serviceAccounts/{clientId}
- "List all accessList?" -> GET /api/atlas/v2/orgs/{orgId}/serviceAccounts/{clientId}/accessList
- "Create a accessList?" -> POST /api/atlas/v2/orgs/{orgId}/serviceAccounts/{clientId}/accessList
- "Delete a accessList?" -> DELETE /api/atlas/v2/orgs/{orgId}/serviceAccounts/{clientId}/accessList/{ipAddress}
- "List all groups?" -> GET /api/atlas/v2/orgs/{orgId}/serviceAccounts/{clientId}/groups
- "Create a secret?" -> POST /api/atlas/v2/orgs/{orgId}/serviceAccounts/{clientId}/secrets
- "Delete a secret?" -> DELETE /api/atlas/v2/orgs/{orgId}/serviceAccounts/{clientId}/secrets/{secretId}
- "List all settings?" -> GET /api/atlas/v2/orgs/{orgId}/settings
- "List all teams?" -> GET /api/atlas/v2/orgs/{orgId}/teams
- "Create a team?" -> POST /api/atlas/v2/orgs/{orgId}/teams
- "Delete a team?" -> DELETE /api/atlas/v2/orgs/{orgId}/teams/{teamId}
- "Get team details?" -> GET /api/atlas/v2/orgs/{orgId}/teams/{teamId}
- "Partially update a team?" -> PATCH /api/atlas/v2/orgs/{orgId}/teams/{teamId}
- "List all users?" -> GET /api/atlas/v2/orgs/{orgId}/teams/{teamId}/users
- "Create a user?" -> POST /api/atlas/v2/orgs/{orgId}/teams/{teamId}/users
- "Delete a user?" -> DELETE /api/atlas/v2/orgs/{orgId}/teams/{teamId}/users/{userId}
- "Get byName details?" -> GET /api/atlas/v2/orgs/{orgId}/teams/byName/{teamName}
- "List all users?" -> GET /api/atlas/v2/orgs/{orgId}/users
- "Create a user?" -> POST /api/atlas/v2/orgs/{orgId}/users
- "Delete a user?" -> DELETE /api/atlas/v2/orgs/{orgId}/users/{userId}
- "Get user details?" -> GET /api/atlas/v2/orgs/{orgId}/users/{userId}
- "Partially update a user?" -> PATCH /api/atlas/v2/orgs/{orgId}/users/{userId}
- "List all rateLimits?" -> GET /api/atlas/v2/rateLimits
- "Get rateLimit details?" -> GET /api/atlas/v2/rateLimits/{endpointSetId}
- "List all skus?" -> GET /api/atlas/v2/skus
- "Get skus details?" -> GET /api/atlas/v2/skus/{skuId}
- "List all controlPlaneIPAddresses?" -> GET /api/atlas/v2/unauth/controlPlaneIPAddresses
- "Create a user?" -> POST /api/atlas/v2/users
- "Get user details?" -> GET /api/atlas/v2/users/{userId}
- "Get byName details?" -> GET /api/atlas/v2/users/byName/{userName}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
