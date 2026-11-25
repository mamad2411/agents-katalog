---
name: aws-audit-manager
description: "AWS Audit Manager API skill. Use when working with AWS Audit Manager for assessments, assessmentFrameworks, controls. Covers 62 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS Audit Manager
API version: 2017-07-25

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /account/status -- verify access
3. POST /assessments/{assessmentId}/delegations -- create first delegations

## Endpoints

62 endpoints across 14 groups. See references/api-spec.lap for full details.

### assessments
| Method | Path | Description |
|--------|------|-------------|
| PUT | /assessments/{assessmentId}/associateToAssessmentReport | Associates an evidence folder to an assessment report in an Audit Manager assessment. |
| PUT | /assessments/{assessmentId}/batchAssociateToAssessmentReport | Associates a list of evidence to an assessment report in an Audit Manager assessment. |
| POST | /assessments/{assessmentId}/delegations | Creates a batch of delegations for an assessment in Audit Manager. |
| PUT | /assessments/{assessmentId}/delegations | Deletes a batch of delegations for an assessment in Audit Manager. |
| PUT | /assessments/{assessmentId}/batchDisassociateFromAssessmentReport | Disassociates a list of evidence from an assessment report in Audit Manager. |
| POST | /assessments/{assessmentId}/controlSets/{controlSetId}/controls/{controlId}/evidence | Adds one or more pieces of evidence to a control in an Audit Manager assessment.  You can import manual evidence from any S3 bucket by specifying the S3 URI of the object. You can also upload a file from your browser, or enter plain text in response to a risk assessment question.  The following restrictions apply to this action:    manualEvidence can be only one of the following: evidenceFileName, s3ResourcePath, or textResponse    Maximum size of an individual evidence file: 100 MB   Number of daily manual evidence uploads per control: 100   Supported file formats: See Supported file types for manual evidence in the Audit Manager User Guide    For more information about Audit Manager service restrictions, see Quotas and restrictions for Audit Manager. |
| POST | /assessments | Creates an assessment in Audit Manager. |
| POST | /assessments/{assessmentId}/reports | Creates an assessment report for the specified assessment. |
| DELETE | /assessments/{assessmentId} | Deletes an assessment in Audit Manager. |
| DELETE | /assessments/{assessmentId}/reports/{assessmentReportId} | Deletes an assessment report in Audit Manager.  When you run the DeleteAssessmentReport operation, Audit Manager attempts to delete the following data:   The specified assessment report that’s stored in your S3 bucket   The associated metadata that’s stored in Audit Manager   If Audit Manager can’t access the assessment report in your S3 bucket, the report isn’t deleted. In this event, the DeleteAssessmentReport operation doesn’t fail. Instead, it proceeds to delete the associated metadata only. You must then delete the assessment report from the S3 bucket yourself.  This scenario happens when Audit Manager receives a 403 (Forbidden) or 404 (Not Found) error from Amazon S3. To avoid this, make sure that your S3 bucket is available, and that you configured the correct permissions for Audit Manager to delete resources in your S3 bucket. For an example permissions policy that you can use, see Assessment report destination permissions in the Audit Manager User Guide. For information about the issues that could cause a 403 (Forbidden) or 404 (Not Found) error from Amazon S3, see List of Error Codes in the Amazon Simple Storage Service API Reference. |
| PUT | /assessments/{assessmentId}/disassociateFromAssessmentReport | Disassociates an evidence folder from the specified assessment report in Audit Manager. |
| GET | /assessments/{assessmentId} | Gets information about a specified assessment. |
| GET | /assessments/{assessmentId}/reports/{assessmentReportId}/url | Gets the URL of an assessment report in Audit Manager. |
| GET | /assessments/{assessmentId}/changelogs | Gets a list of changelogs from Audit Manager. |
| GET | /assessments/{assessmentId}/controlSets/{controlSetId}/evidenceFolders/{evidenceFolderId}/evidence/{evidenceId} | Gets information about a specified evidence item. |
| GET | /assessments/{assessmentId}/controlSets/{controlSetId}/evidenceFolders/{evidenceFolderId}/evidence | Gets all evidence from a specified evidence folder in Audit Manager. |
| GET | /assessments/{assessmentId}/controlSets/{controlSetId}/evidenceFolders/{evidenceFolderId} | Gets an evidence folder from a specified assessment in Audit Manager. |
| GET | /assessments/{assessmentId}/evidenceFolders | Gets the evidence folders from a specified assessment in Audit Manager. |
| GET | /assessments/{assessmentId}/evidenceFolders-by-assessment-control/{controlSetId}/{controlId} | Gets a list of evidence folders that are associated with a specified control in an Audit Manager assessment. |
| GET | /assessments | Returns a list of current and past assessments from Audit Manager. |
| PUT | /assessments/{assessmentId} | Edits an Audit Manager assessment. |
| PUT | /assessments/{assessmentId}/controlSets/{controlSetId}/controls/{controlId} | Updates a control within an assessment in Audit Manager. |
| PUT | /assessments/{assessmentId}/controlSets/{controlSetId}/status | Updates the status of a control set in an Audit Manager assessment. |
| PUT | /assessments/{assessmentId}/status | Updates the status of an assessment in Audit Manager. |

### assessmentFrameworks
| Method | Path | Description |
|--------|------|-------------|
| POST | /assessmentFrameworks | Creates a custom framework in Audit Manager. |
| DELETE | /assessmentFrameworks/{frameworkId} | Deletes a custom framework in Audit Manager. |
| GET | /assessmentFrameworks/{frameworkId} | Gets information about a specified framework. |
| GET | /assessmentFrameworks | Returns a list of the frameworks that are available in the Audit Manager framework library. |
| POST | /assessmentFrameworks/{frameworkId}/shareRequests | Creates a share request for a custom framework in Audit Manager.  The share request specifies a recipient and notifies them that a custom framework is available. Recipients have 120 days to accept or decline the request. If no action is taken, the share request expires. When you create a share request, Audit Manager stores a snapshot of your custom framework in the US East (N. Virginia) Amazon Web Services Region. Audit Manager also stores a backup of the same snapshot in the US West (Oregon) Amazon Web Services Region. Audit Manager deletes the snapshot and the backup snapshot when one of the following events occurs:   The sender revokes the share request.   The recipient declines the share request.   The recipient encounters an error and doesn't successfully accept the share request.   The share request expires before the recipient responds to the request.   When a sender resends a share request, the snapshot is replaced with an updated version that corresponds with the latest version of the custom framework.  When a recipient accepts a share request, the snapshot is replicated into their Amazon Web Services account under the Amazon Web Services Region that was specified in the share request.   When you invoke the StartAssessmentFrameworkShare API, you are about to share a custom framework with another Amazon Web Services account. You may not share a custom framework that is derived from a standard framework if the standard framework is designated as not eligible for sharing by Amazon Web Services, unless you have obtained permission to do so from the owner of the standard framework. To learn more about which standard frameworks are eligible for sharing, see Framework sharing eligibility in the Audit Manager User Guide. |
| PUT | /assessmentFrameworks/{frameworkId} | Updates a custom framework in Audit Manager. |

### controls
| Method | Path | Description |
|--------|------|-------------|
| POST | /controls | Creates a new custom control in Audit Manager. |
| DELETE | /controls/{controlId} | Deletes a custom control in Audit Manager.   When you invoke this operation, the custom control is deleted from any frameworks or assessments that it’s currently part of. As a result, Audit Manager will stop collecting evidence for that custom control in all of your assessments. This includes assessments that you previously created before you deleted the custom control. |
| GET | /controls/{controlId} | Gets information about a specified control. |
| GET | /controls | Returns a list of controls from Audit Manager. |
| PUT | /controls/{controlId} | Updates a custom control in Audit Manager. |

### assessmentFrameworkShareRequests
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /assessmentFrameworkShareRequests/{requestId} | Deletes a share request for a custom framework in Audit Manager. |
| GET | /assessmentFrameworkShareRequests | Returns a list of sent or received share requests for custom frameworks in Audit Manager. |
| PUT | /assessmentFrameworkShareRequests/{requestId} | Updates a share request for a custom framework in Audit Manager. |

### account
| Method | Path | Description |
|--------|------|-------------|
| POST | /account/deregisterAccount | Deregisters an account in Audit Manager.   Before you deregister, you can use the UpdateSettings API operation to set your preferred data retention policy. By default, Audit Manager retains your data. If you want to delete your data, you can use the DeregistrationPolicy attribute to request the deletion of your data.  For more information about data retention, see Data Protection in the Audit Manager User Guide. |
| POST | /account/deregisterOrganizationAdminAccount | Removes the specified Amazon Web Services account as a delegated administrator for Audit Manager.  When you remove a delegated administrator from your Audit Manager settings, you continue to have access to the evidence that you previously collected under that account. This is also the case when you deregister a delegated administrator from Organizations. However, Audit Manager stops collecting and attaching evidence to that delegated administrator account moving forward.  Keep in mind the following cleanup task if you use evidence finder: Before you use your management account to remove a delegated administrator, make sure that the current delegated administrator account signs in to Audit Manager and disables evidence finder first. Disabling evidence finder automatically deletes the event data store that was created in their account when they enabled evidence finder. If this task isn’t completed, the event data store remains in their account. In this case, we recommend that the original delegated administrator goes to CloudTrail Lake and manually deletes the event data store. This cleanup task is necessary to ensure that you don't end up with multiple event data stores. Audit Manager ignores an unused event data store after you remove or change a delegated administrator account. However, the unused event data store continues to incur storage costs from CloudTrail Lake if you don't delete it.  When you deregister a delegated administrator account for Audit Manager, the data for that account isn’t deleted. If you want to delete resource data for a delegated administrator account, you must perform that task separately before you deregister the account. Either, you can do this in the Audit Manager console. Or, you can use one of the delete API operations that are provided by Audit Manager.  To delete your Audit Manager resource data, see the following instructions:     DeleteAssessment (see also: Deleting an assessment in the Audit Manager User Guide)    DeleteAssessmentFramework (see also: Deleting a custom framework in the Audit Manager User Guide)    DeleteAssessmentFrameworkShare (see also: Deleting a share request in the Audit Manager User Guide)    DeleteAssessmentReport (see also: Deleting an assessment report in the Audit Manager User Guide)    DeleteControl (see also: Deleting a custom control in the Audit Manager User Guide)   At this time, Audit Manager doesn't provide an option to delete evidence for a specific delegated administrator. Instead, when your management account deregisters Audit Manager, we perform a cleanup for the current delegated administrator account at the time of deregistration. |
| GET | /account/status | Gets the registration status of an account in Audit Manager. |
| GET | /account/organizationAdminAccount | Gets the name of the delegated Amazon Web Services administrator account for a specified organization. |
| POST | /account/registerAccount | Enables Audit Manager for the specified Amazon Web Services account. |
| POST | /account/registerOrganizationAdminAccount | Enables an Amazon Web Services account within the organization as the delegated administrator for Audit Manager. |

### delegations
| Method | Path | Description |
|--------|------|-------------|
| GET | /delegations | Gets a list of delegations from an audit owner to a delegate. |

### evidenceFileUploadUrl
| Method | Path | Description |
|--------|------|-------------|
| GET | /evidenceFileUploadUrl | Creates a presigned Amazon S3 URL that can be used to upload a file as manual evidence. For instructions on how to use this operation, see Upload a file from your browser  in the Audit Manager User Guide. The following restrictions apply to this operation:   Maximum size of an individual evidence file: 100 MB   Number of daily manual evidence uploads per control: 100   Supported file formats: See Supported file types for manual evidence in the Audit Manager User Guide    For more information about Audit Manager service restrictions, see Quotas and restrictions for Audit Manager. |

### insights
| Method | Path | Description |
|--------|------|-------------|
| GET | /insights | Gets the latest analytics data for all your current active assessments. |
| GET | /insights/assessments/{assessmentId} | Gets the latest analytics data for a specific active assessment. |
| GET | /insights/controls-by-assessment | Lists the latest analytics data for controls within a specific control domain and a specific active assessment.  Control insights are listed only if the control belongs to the control domain and assessment that was specified. Moreover, the control must have collected evidence on the lastUpdated date of controlInsightsByAssessment. If neither of these conditions are met, no data is listed for that control. |
| GET | /insights/control-domains | Lists the latest analytics data for control domains across all of your active assessments.  Audit Manager supports the control domains that are provided by Amazon Web Services Control Catalog. For information about how to find a list of available control domains, see  ListDomains  in the Amazon Web Services Control Catalog API Reference.  A control domain is listed only if at least one of the controls within that domain collected evidence on the lastUpdated date of controlDomainInsights. If this condition isn’t met, no data is listed for that control domain. |
| GET | /insights/control-domains-by-assessment | Lists analytics data for control domains within a specified active assessment. Audit Manager supports the control domains that are provided by Amazon Web Services Control Catalog. For information about how to find a list of available control domains, see  ListDomains  in the Amazon Web Services Control Catalog API Reference.  A control domain is listed only if at least one of the controls within that domain collected evidence on the lastUpdated date of controlDomainInsights. If this condition isn’t met, no data is listed for that domain. |
| GET | /insights/controls | Lists the latest analytics data for controls within a specific control domain across all active assessments.  Control insights are listed only if the control belongs to the control domain that was specified and the control collected evidence on the lastUpdated date of controlInsightsMetadata. If neither of these conditions are met, no data is listed for that control. |

### services
| Method | Path | Description |
|--------|------|-------------|
| GET | /services | Gets a list of the Amazon Web Services from which Audit Manager can collect evidence.  Audit Manager defines which Amazon Web Services are in scope for an assessment. Audit Manager infers this scope by examining the assessment’s controls and their data sources, and then mapping this information to one or more of the corresponding Amazon Web Services that are in this list.  For information about why it's no longer possible to specify services in scope manually, see I can't edit the services in scope for my assessment in the Troubleshooting section of the Audit Manager user guide. |

### settings
| Method | Path | Description |
|--------|------|-------------|
| GET | /settings/{attribute} | Gets the settings for a specified Amazon Web Services account. |
| PUT | /settings | Updates Audit Manager settings for the current account. |

### assessmentReports
| Method | Path | Description |
|--------|------|-------------|
| GET | /assessmentReports | Returns a list of assessment reports created in Audit Manager. |
| POST | /assessmentReports/integrity | Validates the integrity of an assessment report in Audit Manager. |

### dataSourceKeywords
| Method | Path | Description |
|--------|------|-------------|
| GET | /dataSourceKeywords | Returns a list of keywords that are pre-mapped to the specified control data source. |

### notifications
| Method | Path | Description |
|--------|------|-------------|
| GET | /notifications | Returns a list of all Audit Manager notifications. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags/{resourceArn} | Returns a list of tags for the specified resource in Audit Manager. |
| POST | /tags/{resourceArn} | Tags the specified resource in Audit Manager. |
| DELETE | /tags/{resourceArn} | Removes a tag from a resource in Audit Manager. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a delegation?" -> POST /assessments/{assessmentId}/delegations
- "Create a evidence?" -> POST /assessments/{assessmentId}/controlSets/{controlSetId}/controls/{controlId}/evidence
- "Create a assessment?" -> POST /assessments
- "Create a assessmentFramework?" -> POST /assessmentFrameworks
- "Create a report?" -> POST /assessments/{assessmentId}/reports
- "Create a control?" -> POST /controls
- "Delete a assessment?" -> DELETE /assessments/{assessmentId}
- "Delete a assessmentFramework?" -> DELETE /assessmentFrameworks/{frameworkId}
- "Delete a assessmentFrameworkShareRequest?" -> DELETE /assessmentFrameworkShareRequests/{requestId}
- "Delete a report?" -> DELETE /assessments/{assessmentId}/reports/{assessmentReportId}
- "Delete a control?" -> DELETE /controls/{controlId}
- "Create a deregisterAccount?" -> POST /account/deregisterAccount
- "Create a deregisterOrganizationAdminAccount?" -> POST /account/deregisterOrganizationAdminAccount
- "List all status?" -> GET /account/status
- "Get assessment details?" -> GET /assessments/{assessmentId}
- "Get assessmentFramework details?" -> GET /assessmentFrameworks/{frameworkId}
- "List all url?" -> GET /assessments/{assessmentId}/reports/{assessmentReportId}/url
- "List all changelogs?" -> GET /assessments/{assessmentId}/changelogs
- "Get control details?" -> GET /controls/{controlId}
- "List all delegations?" -> GET /delegations
- "Get evidence details?" -> GET /assessments/{assessmentId}/controlSets/{controlSetId}/evidenceFolders/{evidenceFolderId}/evidence/{evidenceId}
- "List all evidence?" -> GET /assessments/{assessmentId}/controlSets/{controlSetId}/evidenceFolders/{evidenceFolderId}/evidence
- "List all evidenceFileUploadUrl?" -> GET /evidenceFileUploadUrl
- "Get evidenceFolder details?" -> GET /assessments/{assessmentId}/controlSets/{controlSetId}/evidenceFolders/{evidenceFolderId}
- "List all evidenceFolders?" -> GET /assessments/{assessmentId}/evidenceFolders
- "Get evidenceFolders-by-assessment-control details?" -> GET /assessments/{assessmentId}/evidenceFolders-by-assessment-control/{controlSetId}/{controlId}
- "List all insights?" -> GET /insights
- "Get assessment details?" -> GET /insights/assessments/{assessmentId}
- "List all organizationAdminAccount?" -> GET /account/organizationAdminAccount
- "List all services?" -> GET /services
- "Get setting details?" -> GET /settings/{attribute}
- "List all controls-by-assessment?" -> GET /insights/controls-by-assessment
- "List all assessmentFrameworkShareRequests?" -> GET /assessmentFrameworkShareRequests
- "List all assessmentFrameworks?" -> GET /assessmentFrameworks
- "List all assessmentReports?" -> GET /assessmentReports
- "List all assessments?" -> GET /assessments
- "List all control-domains?" -> GET /insights/control-domains
- "List all control-domains-by-assessment?" -> GET /insights/control-domains-by-assessment
- "List all controls?" -> GET /insights/controls
- "List all controls?" -> GET /controls
- "List all dataSourceKeywords?" -> GET /dataSourceKeywords
- "List all notifications?" -> GET /notifications
- "Get tag details?" -> GET /tags/{resourceArn}
- "Create a registerAccount?" -> POST /account/registerAccount
- "Create a registerOrganizationAdminAccount?" -> POST /account/registerOrganizationAdminAccount
- "Create a shareRequest?" -> POST /assessmentFrameworks/{frameworkId}/shareRequests
- "Delete a tag?" -> DELETE /tags/{resourceArn}
- "Update a assessment?" -> PUT /assessments/{assessmentId}
- "Update a control?" -> PUT /assessments/{assessmentId}/controlSets/{controlSetId}/controls/{controlId}
- "Update a assessmentFramework?" -> PUT /assessmentFrameworks/{frameworkId}
- "Update a assessmentFrameworkShareRequest?" -> PUT /assessmentFrameworkShareRequests/{requestId}
- "Update a control?" -> PUT /controls/{controlId}
- "Create a integrity?" -> POST /assessmentReports/integrity
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
