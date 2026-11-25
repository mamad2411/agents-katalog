---
name: aws-backup
description: "AWS Backup API skill. Use when working with AWS Backup for legal-holds, backup, backup-vaults. Covers 91 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS Backup
API version: 2018-11-15

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /global-settings -- verify access
3. POST /audit/frameworks -- create first frameworks

## Endpoints

91 endpoints across 15 groups. See references/api-spec.lap for full details.

### legal-holds
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /legal-holds/{legalHoldId} | Removes the specified legal hold on a recovery point. This action can only be performed by a user with sufficient permissions. |
| POST | /legal-holds/ | Creates a legal hold on a recovery point (backup). A legal hold is a restraint on altering or deleting a backup until an authorized user cancels the legal hold. Any actions to delete or disassociate a recovery point will fail with an error if one or more active legal holds are on the recovery point. |
| GET | /legal-holds/{legalHoldId}/ | This action returns details for a specified legal hold. The details are the body of a legal hold in JSON format, in addition to metadata. |
| GET | /legal-holds/ | This action returns metadata about active and previous legal holds. |
| GET | /legal-holds/{legalHoldId}/recovery-points | This action returns recovery point ARNs (Amazon Resource Names) of the specified legal hold. |

### backup
| Method | Path | Description |
|--------|------|-------------|
| PUT | /backup/plans/ | Creates a backup plan using a backup plan name and backup rules. A backup plan is a document that contains information that Backup uses to schedule tasks that create recovery points for resources. If you call CreateBackupPlan with a plan that already exists, you receive an AlreadyExistsException exception. |
| PUT | /backup/plans/{backupPlanId}/selections/ | Creates a JSON document that specifies a set of resources to assign to a backup plan. For examples, see Assigning resources programmatically. |
| DELETE | /backup/plans/{backupPlanId} | Deletes a backup plan. A backup plan can only be deleted after all associated selections of resources have been deleted. Deleting a backup plan deletes the current version of a backup plan. Previous versions, if any, will still exist. |
| DELETE | /backup/plans/{backupPlanId}/selections/{selectionId} | Deletes the resource selection associated with a backup plan that is specified by the SelectionId. |
| GET | /backup/plans/{backupPlanId}/toTemplate/ | Returns the backup plan that is specified by the plan ID as a backup template. |
| GET | /backup/plans/{backupPlanId}/ | Returns BackupPlan details for the specified BackupPlanId. The details are the body of a backup plan in JSON format, in addition to plan metadata. |
| POST | /backup/template/json/toPlan | Returns a valid JSON document specifying a backup plan or an error. |
| GET | /backup/template/plans/{templateId}/toPlan | Returns the template specified by its templateId as a backup plan. |
| GET | /backup/plans/{backupPlanId}/selections/{selectionId} | Returns selection metadata and a document in JSON format that specifies a list of resources that are associated with a backup plan. |
| GET | /backup/template/plans | Lists the backup plan templates. |
| GET | /backup/plans/{backupPlanId}/versions/ | Returns version metadata of your backup plans, including Amazon Resource Names (ARNs), backup plan IDs, creation and deletion dates, plan names, and version IDs. |
| GET | /backup/plans/ | Lists the active backup plans for the account. |
| GET | /backup/plans/{backupPlanId}/selections/ | Returns an array containing metadata of the resources associated with the target backup plan. |
| POST | /backup/plans/{backupPlanId} | Updates the specified backup plan. The new version is uniquely identified by its ID. |

### backup-vaults
| Method | Path | Description |
|--------|------|-------------|
| PUT | /backup-vaults/{backupVaultName} | Creates a logical container where backups are stored. A CreateBackupVault request includes a name, optionally one or more resource tags, an encryption key, and a request ID.  Do not include sensitive data, such as passport numbers, in the name of a backup vault. |
| DELETE | /backup-vaults/{backupVaultName} | Deletes the backup vault identified by its name. A vault can be deleted only if it is empty. |
| DELETE | /backup-vaults/{backupVaultName}/access-policy | Deletes the policy document that manages permissions on a backup vault. |
| DELETE | /backup-vaults/{backupVaultName}/vault-lock | Deletes Backup Vault Lock from a backup vault specified by a backup vault name. If the Vault Lock configuration is immutable, then you cannot delete Vault Lock using API operations, and you will receive an InvalidRequestException if you attempt to do so. For more information, see Vault Lock in the Backup Developer Guide. |
| DELETE | /backup-vaults/{backupVaultName}/notification-configuration | Deletes event notifications for the specified backup vault. |
| DELETE | /backup-vaults/{backupVaultName}/recovery-points/{recoveryPointArn} | Deletes the recovery point specified by a recovery point ID. If the recovery point ID belongs to a continuous backup, calling this endpoint deletes the existing continuous backup and stops future continuous backup. When an IAM role's permissions are insufficient to call this API, the service sends back an HTTP 200 response with an empty HTTP body, but the recovery point is not deleted. Instead, it enters an EXPIRED state.  EXPIRED recovery points can be deleted with this API once the IAM role has the iam:CreateServiceLinkedRole action. To learn more about adding this role, see  Troubleshooting manual deletions. If the user or role is deleted or the permission within the role is removed, the deletion will not be successful and will enter an EXPIRED state. |
| GET | /backup-vaults/{backupVaultName} | Returns metadata about a backup vault specified by its name. |
| GET | /backup-vaults/{backupVaultName}/recovery-points/{recoveryPointArn} | Returns metadata associated with a recovery point, including ID, status, encryption, and lifecycle. |
| POST | /backup-vaults/{backupVaultName}/recovery-points/{recoveryPointArn}/disassociate | Deletes the specified continuous backup recovery point from Backup and releases control of that continuous backup to the source service, such as Amazon RDS. The source service will continue to create and retain continuous backups using the lifecycle that you specified in your original backup plan. Does not support snapshot backup recovery points. |
| DELETE | /backup-vaults/{backupVaultName}/recovery-points/{recoveryPointArn}/parentAssociation | This action to a specific child (nested) recovery point removes the relationship between the specified recovery point and its parent (composite) recovery point. |
| GET | /backup-vaults/{backupVaultName}/access-policy | Returns the access policy document that is associated with the named backup vault. |
| GET | /backup-vaults/{backupVaultName}/notification-configuration | Returns event notifications for the specified backup vault. |
| GET | /backup-vaults/{backupVaultName}/recovery-points/{recoveryPointArn}/restore-metadata | Returns a set of metadata key-value pairs that were used to create the backup. |
| GET | /backup-vaults/ | Returns a list of recovery point storage containers along with information about them. |
| GET | /backup-vaults/{backupVaultName}/resources/ | This request lists the protected resources corresponding to each backup vault. |
| GET | /backup-vaults/{backupVaultName}/recovery-points/ | Returns detailed information about the recovery points stored in a backup vault. |
| PUT | /backup-vaults/{backupVaultName}/access-policy | Sets a resource-based policy that is used to manage access permissions on the target backup vault. Requires a backup vault name and an access policy document in JSON format. |
| PUT | /backup-vaults/{backupVaultName}/vault-lock | Applies Backup Vault Lock to a backup vault, preventing attempts to delete any recovery point stored in or created in a backup vault. Vault Lock also prevents attempts to update the lifecycle policy that controls the retention period of any recovery point currently stored in a backup vault. If specified, Vault Lock enforces a minimum and maximum retention period for future backup and copy jobs that target a backup vault.  Backup Vault Lock has been assessed by Cohasset Associates for use in environments that are subject to SEC 17a-4, CFTC, and FINRA regulations. For more information about how Backup Vault Lock relates to these regulations, see the Cohasset Associates Compliance Assessment.   For more information, see Backup Vault Lock. |
| PUT | /backup-vaults/{backupVaultName}/notification-configuration | Turns on notifications on a backup vault for the specified topic and events. |
| POST | /backup-vaults/{backupVaultName}/recovery-points/{recoveryPointArn} | Sets the transition lifecycle of a recovery point. The lifecycle defines when a protected resource is transitioned to cold storage and when it expires. Backup transitions and expires backups automatically according to the lifecycle that you define. Resource types that can transition to cold storage are listed in the Feature availability by resource table. Backup ignores this expression for other resource types. Backups transitioned to cold storage must be stored in cold storage for a minimum of 90 days. Therefore, the “retention” setting must be 90 days greater than the “transition to cold after days” setting. The “transition to cold after days” setting cannot be changed after a backup has been transitioned to cold.  If your lifecycle currently uses the parameters DeleteAfterDays and MoveToColdStorageAfterDays, include these parameters and their values when you call this operation. Not including them may result in your plan updating with null values.  This operation does not support continuous backups. |

### audit
| Method | Path | Description |
|--------|------|-------------|
| POST | /audit/frameworks | Creates a framework with one or more controls. A framework is a collection of controls that you can use to evaluate your backup practices. By using pre-built customizable controls to define your policies, you can evaluate whether your backup practices comply with your policies and which resources are not yet in compliance. |
| POST | /audit/report-plans | Creates a report plan. A report plan is a document that contains information about the contents of the report and where Backup will deliver it. If you call CreateReportPlan with a plan that already exists, you receive an AlreadyExistsException exception. |
| DELETE | /audit/frameworks/{frameworkName} | Deletes the framework specified by a framework name. |
| DELETE | /audit/report-plans/{reportPlanName} | Deletes the report plan specified by a report plan name. |
| GET | /audit/frameworks/{frameworkName} | Returns the framework details for the specified FrameworkName. |
| GET | /audit/report-jobs/{reportJobId} | Returns the details associated with creating a report as specified by its ReportJobId. |
| GET | /audit/report-plans/{reportPlanName} | Returns a list of all report plans for an Amazon Web Services account and Amazon Web Services Region. |
| GET | /audit/backup-job-summaries | This is a request for a summary of backup jobs created or running within the most recent 30 days. You can include parameters AccountID, State, ResourceType, MessageCategory, AggregationPeriod, MaxResults, or NextToken to filter results. This request returns a summary that contains Region, Account, State, ResourceType, MessageCategory, StartTime, EndTime, and Count of included jobs. |
| GET | /audit/copy-job-summaries | This request obtains a list of copy jobs created or running within the the most recent 30 days. You can include parameters AccountID, State, ResourceType, MessageCategory, AggregationPeriod, MaxResults, or NextToken to filter results. This request returns a summary that contains Region, Account, State, RestourceType, MessageCategory, StartTime, EndTime, and Count of included jobs. |
| GET | /audit/frameworks | Returns a list of all frameworks for an Amazon Web Services account and Amazon Web Services Region. |
| GET | /audit/report-jobs | Returns details about your report jobs. |
| GET | /audit/report-plans | Returns a list of your report plans. For detailed information about a single report plan, use DescribeReportPlan. |
| GET | /audit/restore-job-summaries | This request obtains a summary of restore jobs created or running within the the most recent 30 days. You can include parameters AccountID, State, ResourceType, AggregationPeriod, MaxResults, or NextToken to filter results. This request returns a summary that contains Region, Account, State, RestourceType, MessageCategory, StartTime, EndTime, and Count of included jobs. |
| POST | /audit/report-jobs/{reportPlanName} | Starts an on-demand report job for the specified report plan. |
| PUT | /audit/frameworks/{frameworkName} | Updates the specified framework. |
| PUT | /audit/report-plans/{reportPlanName} | Updates the specified report plan. |

### logically-air-gapped-backup-vaults
| Method | Path | Description |
|--------|------|-------------|
| PUT | /logically-air-gapped-backup-vaults/{backupVaultName} | Creates a logical container to where backups may be copied. This request includes a name, the Region, the maximum number of retention days, the minimum number of retention days, and optionally can include tags and a creator request ID.  Do not include sensitive data, such as passport numbers, in the name of a backup vault. |

### restore-testing
| Method | Path | Description |
|--------|------|-------------|
| PUT | /restore-testing/plans | Creates a restore testing plan. The first of two steps to create a restore testing plan. After this request is successful, finish the procedure using CreateRestoreTestingSelection. |
| PUT | /restore-testing/plans/{RestoreTestingPlanName}/selections | This request can be sent after CreateRestoreTestingPlan request returns successfully. This is the second part of creating a resource testing plan, and it must be completed sequentially. This consists of RestoreTestingSelectionName, ProtectedResourceType, and one of the following:    ProtectedResourceArns     ProtectedResourceConditions    Each protected resource type can have one single value. A restore testing selection can include a wildcard value ("*") for ProtectedResourceArns along with ProtectedResourceConditions. Alternatively, you can include up to 30 specific protected resource ARNs in ProtectedResourceArns. Cannot select by both protected resource types AND specific ARNs. Request will fail if both are included. |
| DELETE | /restore-testing/plans/{RestoreTestingPlanName} | This request deletes the specified restore testing plan. Deletion can only successfully occur if all associated restore testing selections are deleted first. |
| DELETE | /restore-testing/plans/{RestoreTestingPlanName}/selections/{RestoreTestingSelectionName} | Input the Restore Testing Plan name and Restore Testing Selection name. All testing selections associated with a restore testing plan must be deleted before the restore testing plan can be deleted. |
| GET | /restore-testing/inferred-metadata | This request returns the minimal required set of metadata needed to start a restore job with secure default settings. BackupVaultName and RecoveryPointArn are required parameters. BackupVaultAccountId is an optional parameter. |
| GET | /restore-testing/plans/{RestoreTestingPlanName} | Returns RestoreTestingPlan details for the specified RestoreTestingPlanName. The details are the body of a restore testing plan in JSON format, in addition to plan metadata. |
| GET | /restore-testing/plans/{RestoreTestingPlanName}/selections/{RestoreTestingSelectionName} | Returns RestoreTestingSelection, which displays resources and elements of the restore testing plan. |
| GET | /restore-testing/plans | Returns a list of restore testing plans. |
| GET | /restore-testing/plans/{RestoreTestingPlanName}/selections | Returns a list of restore testing selections. Can be filtered by MaxResults and RestoreTestingPlanName. |
| PUT | /restore-testing/plans/{RestoreTestingPlanName} | This request will send changes to your specified restore testing plan. RestoreTestingPlanName cannot be updated after it is created.  RecoveryPointSelection can contain:    Algorithm     ExcludeVaults     IncludeVaults     RecoveryPointTypes     SelectionWindowDays |
| PUT | /restore-testing/plans/{RestoreTestingPlanName}/selections/{RestoreTestingSelectionName} | Updates the specified restore testing selection. Most elements except the RestoreTestingSelectionName can be updated with this request. You can use either protected resource ARNs or conditions, but not both. |

### backup-jobs
| Method | Path | Description |
|--------|------|-------------|
| GET | /backup-jobs/{backupJobId} | Returns backup job details for the specified BackupJobId. |
| GET | /backup-jobs/ | Returns a list of existing backup jobs for an authenticated account for the last 30 days. For a longer period of time, consider using these monitoring tools. |
| PUT | /backup-jobs | Starts an on-demand backup job for the specified resource. |
| POST | /backup-jobs/{backupJobId} | Attempts to cancel a job to create a one-time backup of a resource. This action is not supported for the following services: Amazon FSx for Windows File Server, Amazon FSx for Lustre, Amazon FSx for NetApp ONTAP, Amazon FSx for OpenZFS, Amazon DocumentDB (with MongoDB compatibility), Amazon RDS, Amazon Aurora, and Amazon Neptune. |

### copy-jobs
| Method | Path | Description |
|--------|------|-------------|
| GET | /copy-jobs/{copyJobId} | Returns metadata associated with creating a copy of a resource. |
| GET | /copy-jobs/ | Returns metadata about your copy jobs. |
| PUT | /copy-jobs | Starts a job to create a one-time copy of the specified resource. Does not support continuous backups. |

### global-settings
| Method | Path | Description |
|--------|------|-------------|
| GET | /global-settings | Describes whether the Amazon Web Services account is opted in to cross-account backup. Returns an error if the account is not a member of an Organizations organization. Example: describe-global-settings --region us-west-2 |
| PUT | /global-settings | Updates whether the Amazon Web Services account is opted in to cross-account backup. Returns an error if the account is not an Organizations management account. Use the DescribeGlobalSettings API to determine the current settings. |

### resources
| Method | Path | Description |
|--------|------|-------------|
| GET | /resources/{resourceArn} | Returns information about a saved resource, including the last time it was backed up, its Amazon Resource Name (ARN), and the Amazon Web Services service type of the saved resource. |
| GET | /resources/ | Returns an array of resources successfully backed up by Backup, including the time the resource was saved, an Amazon Resource Name (ARN) of the resource, and a resource type. |
| GET | /resources/{resourceArn}/recovery-points/ | The information about the recovery points of the type specified by a resource Amazon Resource Name (ARN).  For Amazon EFS and Amazon EC2, this action only lists recovery points created by Backup. |
| GET | /resources/{resourceArn}/restore-jobs/ | This returns restore jobs that contain the specified protected resource. You must include ResourceArn. You can optionally include NextToken, ByStatus, MaxResults, ByRecoveryPointCreationDateAfter , and ByRecoveryPointCreationDateBefore. |

### account-settings
| Method | Path | Description |
|--------|------|-------------|
| GET | /account-settings | Returns the current service opt-in settings for the Region. If service opt-in is enabled for a service, Backup tries to protect that service's resources in this Region, when the resource is included in an on-demand backup or scheduled backup plan. Otherwise, Backup does not try to protect that service's resources in this Region. |
| PUT | /account-settings | Updates the current service opt-in settings for the Region. Use the DescribeRegionSettings API to determine the resource types that are supported. |

### restore-jobs
| Method | Path | Description |
|--------|------|-------------|
| GET | /restore-jobs/{restoreJobId} | Returns metadata associated with a restore job that is specified by a job ID. |
| GET | /restore-jobs/{restoreJobId}/metadata | This request returns the metadata for the specified restore job. |
| GET | /restore-jobs/ | Returns a list of jobs that Backup initiated to restore a saved resource, including details about the recovery process. |
| PUT | /restore-jobs/{restoreJobId}/validations | This request allows you to send your independent self-run restore test validation results. RestoreJobId and ValidationStatus are required. Optionally, you can input a ValidationStatusMessage. |
| PUT | /restore-jobs | Recovers the saved resource identified by an Amazon Resource Name (ARN). |

### supported-resource-types
| Method | Path | Description |
|--------|------|-------------|
| GET | /supported-resource-types | Returns the Amazon Web Services resource types supported by Backup. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags/{resourceArn}/ | Returns the tags assigned to the resource, such as a target recovery point, backup plan, or backup vault. |
| POST | /tags/{resourceArn} | Assigns a set of key-value pairs to a recovery point, backup plan, or backup vault identified by an Amazon Resource Name (ARN). This API is supported for recovery points for resource types including Aurora, Amazon DocumentDB. Amazon EBS, Amazon FSx, Neptune, and Amazon RDS. |

### untag
| Method | Path | Description |
|--------|------|-------------|
| POST | /untag/{resourceArn} | Removes a set of key-value pairs from a recovery point, backup plan, or backup vault identified by an Amazon Resource Name (ARN) This API is not supported for recovery points for resource types including Aurora, Amazon DocumentDB. Amazon EBS, Amazon FSx, Neptune, and Amazon RDS. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Delete a legal-hold?" -> DELETE /legal-holds/{legalHoldId}
- "Update a backup-vault?" -> PUT /backup-vaults/{backupVaultName}
- "Create a framework?" -> POST /audit/frameworks
- "Create a legal-hold?" -> POST /legal-holds/
- "Update a logically-air-gapped-backup-vault?" -> PUT /logically-air-gapped-backup-vaults/{backupVaultName}
- "Create a report-plan?" -> POST /audit/report-plans
- "Delete a plan?" -> DELETE /backup/plans/{backupPlanId}
- "Delete a selection?" -> DELETE /backup/plans/{backupPlanId}/selections/{selectionId}
- "Delete a backup-vault?" -> DELETE /backup-vaults/{backupVaultName}
- "Delete a framework?" -> DELETE /audit/frameworks/{frameworkName}
- "Delete a recovery-point?" -> DELETE /backup-vaults/{backupVaultName}/recovery-points/{recoveryPointArn}
- "Delete a report-plan?" -> DELETE /audit/report-plans/{reportPlanName}
- "Delete a plan?" -> DELETE /restore-testing/plans/{RestoreTestingPlanName}
- "Delete a selection?" -> DELETE /restore-testing/plans/{RestoreTestingPlanName}/selections/{RestoreTestingSelectionName}
- "Get backup-job details?" -> GET /backup-jobs/{backupJobId}
- "Get backup-vault details?" -> GET /backup-vaults/{backupVaultName}
- "Get copy-job details?" -> GET /copy-jobs/{copyJobId}
- "Get framework details?" -> GET /audit/frameworks/{frameworkName}
- "List all global-settings?" -> GET /global-settings
- "Get resource details?" -> GET /resources/{resourceArn}
- "Get recovery-point details?" -> GET /backup-vaults/{backupVaultName}/recovery-points/{recoveryPointArn}
- "List all account-settings?" -> GET /account-settings
- "Get report-job details?" -> GET /audit/report-jobs/{reportJobId}
- "Get report-plan details?" -> GET /audit/report-plans/{reportPlanName}
- "Get restore-job details?" -> GET /restore-jobs/{restoreJobId}
- "Create a disassociate?" -> POST /backup-vaults/{backupVaultName}/recovery-points/{recoveryPointArn}/disassociate
- "List all toTemplate?" -> GET /backup/plans/{backupPlanId}/toTemplate/
- "Get plan details?" -> GET /backup/plans/{backupPlanId}/
- "Create a toPlan?" -> POST /backup/template/json/toPlan
- "List all toPlan?" -> GET /backup/template/plans/{templateId}/toPlan
- "Get selection details?" -> GET /backup/plans/{backupPlanId}/selections/{selectionId}
- "List all access-policy?" -> GET /backup-vaults/{backupVaultName}/access-policy
- "List all notification-configuration?" -> GET /backup-vaults/{backupVaultName}/notification-configuration
- "Get legal-hold details?" -> GET /legal-holds/{legalHoldId}/
- "List all restore-metadata?" -> GET /backup-vaults/{backupVaultName}/recovery-points/{recoveryPointArn}/restore-metadata
- "List all metadata?" -> GET /restore-jobs/{restoreJobId}/metadata
- "List all inferred-metadata?" -> GET /restore-testing/inferred-metadata
- "Get plan details?" -> GET /restore-testing/plans/{RestoreTestingPlanName}
- "Get selection details?" -> GET /restore-testing/plans/{RestoreTestingPlanName}/selections/{RestoreTestingSelectionName}
- "List all supported-resource-types?" -> GET /supported-resource-types
- "List all backup-job-summaries?" -> GET /audit/backup-job-summaries
- "List all backup-jobs?" -> GET /backup-jobs/
- "List all plans?" -> GET /backup/template/plans
- "List all versions?" -> GET /backup/plans/{backupPlanId}/versions/
- "List all plans?" -> GET /backup/plans/
- "List all selections?" -> GET /backup/plans/{backupPlanId}/selections/
- "List all backup-vaults?" -> GET /backup-vaults/
- "List all copy-job-summaries?" -> GET /audit/copy-job-summaries
- "List all copy-jobs?" -> GET /copy-jobs/
- "List all frameworks?" -> GET /audit/frameworks
- "List all legal-holds?" -> GET /legal-holds/
- "List all resources?" -> GET /resources/
- "List all resources?" -> GET /backup-vaults/{backupVaultName}/resources/
- "List all recovery-points?" -> GET /backup-vaults/{backupVaultName}/recovery-points/
- "List all recovery-points?" -> GET /legal-holds/{legalHoldId}/recovery-points
- "List all recovery-points?" -> GET /resources/{resourceArn}/recovery-points/
- "List all report-jobs?" -> GET /audit/report-jobs
- "List all report-plans?" -> GET /audit/report-plans
- "List all restore-job-summaries?" -> GET /audit/restore-job-summaries
- "List all restore-jobs?" -> GET /restore-jobs/
- "List all restore-jobs?" -> GET /resources/{resourceArn}/restore-jobs/
- "List all plans?" -> GET /restore-testing/plans
- "List all selections?" -> GET /restore-testing/plans/{RestoreTestingPlanName}/selections
- "Get tag details?" -> GET /tags/{resourceArn}/
- "Update a framework?" -> PUT /audit/frameworks/{frameworkName}
- "Update a report-plan?" -> PUT /audit/report-plans/{reportPlanName}
- "Update a plan?" -> PUT /restore-testing/plans/{RestoreTestingPlanName}
- "Update a selection?" -> PUT /restore-testing/plans/{RestoreTestingPlanName}/selections/{RestoreTestingSelectionName}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
