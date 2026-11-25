---
name: aws-well-architected-tool
description: "AWS Well-Architected Tool API skill. Use when working with AWS Well-Architected Tool for workloads, lenses, profiles. Covers 72 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS Well-Architected Tool
API version: 2020-03-31

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /consolidatedReport -- verify access
3. POST /lenses/{LensAlias}/shares -- create first shares

## Endpoints

72 endpoints across 15 groups. See references/api-spec.lap for full details.

### workloads
| Method | Path | Description |
|--------|------|-------------|
| PATCH | /workloads/{WorkloadId}/associateLenses | Associate a lens to a workload. Up to 10 lenses can be associated with a workload in a single API operation. A maximum of 20 lenses can be associated with a workload.   Disclaimer  By accessing and/or applying custom lenses created by another Amazon Web Services user or account, you acknowledge that custom lenses created by other users and shared with you are Third Party Content as defined in the Amazon Web Services Customer Agreement. |
| PATCH | /workloads/{WorkloadId}/associateProfiles | Associate a profile with a workload. |
| POST | /workloads/{WorkloadId}/milestones | Create a milestone for an existing workload. |
| POST | /workloads | Create a new workload. The owner of a workload can share the workload with other Amazon Web Services accounts, users, an organization, and organizational units (OUs) in the same Amazon Web Services Region. Only the owner of a workload can delete it. For more information, see Defining a Workload in the Well-Architected Tool User Guide.  Either AwsRegions, NonAwsRegions, or both must be specified when creating a workload. You also must specify ReviewOwner, even though the parameter is listed as not being required in the following section.   When creating a workload using a review template, you must have the following IAM permissions:    wellarchitected:GetReviewTemplate     wellarchitected:GetReviewTemplateAnswer     wellarchitected:ListReviewTemplateAnswers     wellarchitected:GetReviewTemplateLensReview |
| POST | /workloads/{WorkloadId}/shares | Create a workload share. The owner of a workload can share it with other Amazon Web Services accounts and users in the same Amazon Web Services Region. Shared access to a workload is not removed until the workload invitation is deleted. If you share a workload with an organization or OU, all accounts in the organization or OU are granted access to the workload. For more information, see Sharing a workload in the Well-Architected Tool User Guide. |
| DELETE | /workloads/{WorkloadId} | Delete an existing workload. |
| DELETE | /workloads/{WorkloadId}/shares/{ShareId} | Delete a workload share. |
| PATCH | /workloads/{WorkloadId}/disassociateLenses | Disassociate a lens from a workload. Up to 10 lenses can be disassociated from a workload in a single API operation.  The Amazon Web Services Well-Architected Framework lens (wellarchitected) cannot be removed from a workload. |
| PATCH | /workloads/{WorkloadId}/disassociateProfiles | Disassociate a profile from a workload. |
| GET | /workloads/{WorkloadId}/lensReviews/{LensAlias}/answers/{QuestionId} | Get the answer to a specific question in a workload review. |
| GET | /workloads/{WorkloadId}/lensReviews/{LensAlias} | Get lens review. |
| GET | /workloads/{WorkloadId}/lensReviews/{LensAlias}/report | Get lens review report. |
| GET | /workloads/{WorkloadId}/milestones/{MilestoneNumber} | Get a milestone for an existing workload. |
| GET | /workloads/{WorkloadId} | Get an existing workload. |
| GET | /workloads/{WorkloadId}/lensReviews/{LensAlias}/answers | List of answers for a particular workload and lens. |
| POST | /workloads/{WorkloadId}/checks | List of Trusted Advisor check details by account related to the workload. |
| POST | /workloads/{WorkloadId}/checkSummaries | List of Trusted Advisor checks summarized for all accounts related to the workload. |
| GET | /workloads/{WorkloadId}/lensReviews/{LensAlias}/improvements | List the improvements of a particular lens review. |
| GET | /workloads/{WorkloadId}/lensReviews | List lens reviews for a particular workload. |
| POST | /workloads/{WorkloadId}/milestonesSummaries | List all milestones for an existing workload. |
| GET | /workloads/{WorkloadId}/shares | List the workload shares associated with the workload. |
| PATCH | /workloads/{WorkloadId}/lensReviews/{LensAlias}/answers/{QuestionId} | Update the answer to a specific question in a workload review. |
| POST | /workloads/{WorkloadId}/updateIntegration | Update integration features. |
| PATCH | /workloads/{WorkloadId}/lensReviews/{LensAlias} | Update lens review for a particular workload. |
| PATCH | /workloads/{WorkloadId} | Update an existing workload. |
| PATCH | /workloads/{WorkloadId}/shares/{ShareId} | Update a workload share. |
| PUT | /workloads/{WorkloadId}/lensReviews/{LensAlias}/upgrade | Upgrade lens review for a particular workload. |
| PUT | /workloads/{WorkloadId}/profiles/{ProfileArn}/upgrade | Upgrade a profile. |

### lenses
| Method | Path | Description |
|--------|------|-------------|
| POST | /lenses/{LensAlias}/shares | Create a lens share. The owner of a lens can share it with other Amazon Web Services accounts, users, an organization, and organizational units (OUs) in the same Amazon Web Services Region. Lenses provided by Amazon Web Services (Amazon Web Services Official Content) cannot be shared.  Shared access to a lens is not removed until the lens invitation is deleted. If you share a lens with an organization or OU, all accounts in the organization or OU are granted access to the lens. For more information, see Sharing a custom lens in the Well-Architected Tool User Guide.   Disclaimer  By sharing your custom lenses with other Amazon Web Services accounts, you acknowledge that Amazon Web Services will make your custom lenses available to those other accounts. Those other accounts may continue to access and use your shared custom lenses even if you delete the custom lenses from your own Amazon Web Services account or terminate your Amazon Web Services account. |
| POST | /lenses/{LensAlias}/versions | Create a new lens version. A lens can have up to 100 versions. Use this operation to publish a new lens version after you have imported a lens. The LensAlias is used to identify the lens to be published. The owner of a lens can share the lens with other Amazon Web Services accounts and users in the same Amazon Web Services Region. Only the owner of a lens can delete it. |
| DELETE | /lenses/{LensAlias} | Delete an existing lens. Only the owner of a lens can delete it. After the lens is deleted, Amazon Web Services accounts and users that you shared the lens with can continue to use it, but they will no longer be able to apply it to new workloads.    Disclaimer  By sharing your custom lenses with other Amazon Web Services accounts, you acknowledge that Amazon Web Services will make your custom lenses available to those other accounts. Those other accounts may continue to access and use your shared custom lenses even if you delete the custom lenses from your own Amazon Web Services account or terminate your Amazon Web Services account. |
| DELETE | /lenses/{LensAlias}/shares/{ShareId} | Delete a lens share. After the lens share is deleted, Amazon Web Services accounts, users, organizations, and organizational units (OUs) that you shared the lens with can continue to use it, but they will no longer be able to apply it to new workloads.   Disclaimer  By sharing your custom lenses with other Amazon Web Services accounts, you acknowledge that Amazon Web Services will make your custom lenses available to those other accounts. Those other accounts may continue to access and use your shared custom lenses even if you delete the custom lenses from your own Amazon Web Services account or terminate your Amazon Web Services account. |
| GET | /lenses/{LensAlias}/export | Export an existing lens. Only the owner of a lens can export it. Lenses provided by Amazon Web Services (Amazon Web Services Official Content) cannot be exported. Lenses are defined in JSON. For more information, see JSON format specification in the Well-Architected Tool User Guide.   Disclaimer  Do not include or gather personal identifiable information (PII) of end users or other identifiable individuals in or via your custom lenses. If your custom lens or those shared with you and used in your account do include or collect PII you are responsible for: ensuring that the included PII is processed in accordance with applicable law, providing adequate privacy notices, and obtaining necessary consents for processing such data. |
| GET | /lenses/{LensAlias} | Get an existing lens. |
| GET | /lenses/{LensAlias}/versionDifference | Get lens version differences. |
| GET | /lenses/{LensAlias}/shares | List the lens shares associated with the lens. |
| GET | /lenses | List the available lenses. |

### profiles
| Method | Path | Description |
|--------|------|-------------|
| POST | /profiles | Create a profile. |
| POST | /profiles/{ProfileArn}/shares | Create a profile share. |
| DELETE | /profiles/{ProfileArn} | Delete a profile.   Disclaimer  By sharing your profile with other Amazon Web Services accounts, you acknowledge that Amazon Web Services will make your profile available to those other accounts. Those other accounts may continue to access and use your shared profile even if you delete the profile from your own Amazon Web Services account or terminate your Amazon Web Services account. |
| DELETE | /profiles/{ProfileArn}/shares/{ShareId} | Delete a profile share. |
| GET | /profiles/{ProfileArn} | Get profile information. |
| GET | /profiles/{ProfileArn}/shares | List profile shares. |
| PATCH | /profiles/{ProfileArn} | Update a profile. |

### reviewTemplates
| Method | Path | Description |
|--------|------|-------------|
| POST | /reviewTemplates | Create a review template.   Disclaimer  Do not include or gather personal identifiable information (PII) of end users or other identifiable individuals in or via your review templates. If your review template or those shared with you and used in your account do include or collect PII you are responsible for: ensuring that the included PII is processed in accordance with applicable law, providing adequate privacy notices, and obtaining necessary consents for processing such data. |
| DELETE | /reviewTemplates/{TemplateArn} | Delete a review template. Only the owner of a review template can delete it. After the review template is deleted, Amazon Web Services accounts, users, organizations, and organizational units (OUs) that you shared the review template with will no longer be able to apply it to new workloads. |
| GET | /reviewTemplates/{TemplateArn} | Get review template. |
| GET | /reviewTemplates/{TemplateArn}/lensReviews/{LensAlias}/answers/{QuestionId} | Get review template answer. |
| GET | /reviewTemplates/{TemplateArn}/lensReviews/{LensAlias} | Get a lens review associated with a review template. |
| GET | /reviewTemplates/{TemplateArn}/lensReviews/{LensAlias}/answers | List the answers of a review template. |
| GET | /reviewTemplates | List review templates. |
| PATCH | /reviewTemplates/{TemplateArn} | Update a review template. |
| PATCH | /reviewTemplates/{TemplateArn}/lensReviews/{LensAlias}/answers/{QuestionId} | Update a review template answer. |
| PATCH | /reviewTemplates/{TemplateArn}/lensReviews/{LensAlias} | Update a lens review associated with a review template. |
| PUT | /reviewTemplates/{TemplateArn}/lensReviews/{LensAlias}/upgrade | Upgrade the lens review of a review template. |

### templates
| Method | Path | Description |
|--------|------|-------------|
| POST | /templates/shares/{TemplateArn} | Create a review template share. The owner of a review template can share it with other Amazon Web Services accounts, users, an organization, and organizational units (OUs) in the same Amazon Web Services Region.   Shared access to a review template is not removed until the review template share invitation is deleted. If you share a review template with an organization or OU, all accounts in the organization or OU are granted access to the review template.   Disclaimer  By sharing your review template with other Amazon Web Services accounts, you acknowledge that Amazon Web Services will make your review template available to those other accounts. |
| DELETE | /templates/shares/{TemplateArn}/{ShareId} | Delete a review template share. After the review template share is deleted, Amazon Web Services accounts, users, organizations, and organizational units (OUs) that you shared the review template with will no longer be able to apply it to new workloads. |
| GET | /templates/shares/{TemplateArn} | List review template shares. |

### consolidatedReport
| Method | Path | Description |
|--------|------|-------------|
| GET | /consolidatedReport | Get a consolidated report of your workloads. You can optionally choose to include workloads that have been shared with you. |

### global-settings
| Method | Path | Description |
|--------|------|-------------|
| GET | /global-settings | Global settings for all workloads. |
| PATCH | /global-settings | Update whether the Amazon Web Services account is opted into organization sharing and discovery integration features. |

### profileTemplate
| Method | Path | Description |
|--------|------|-------------|
| GET | /profileTemplate | Get profile template. |

### importLens
| Method | Path | Description |
|--------|------|-------------|
| PUT | /importLens | Import a new custom lens or update an existing custom lens. To update an existing custom lens, specify its ARN as the LensAlias. If no ARN is specified, a new custom lens is created. The new or updated lens will have a status of DRAFT. The lens cannot be applied to workloads or shared with other Amazon Web Services accounts until it's published with CreateLensVersion. Lenses are defined in JSON. For more information, see JSON format specification in the Well-Architected Tool User Guide. A custom lens cannot exceed 500 KB in size.   Disclaimer  Do not include or gather personal identifiable information (PII) of end users or other identifiable individuals in or via your custom lenses. If your custom lens or those shared with you and used in your account do include or collect PII you are responsible for: ensuring that the included PII is processed in accordance with applicable law, providing adequate privacy notices, and obtaining necessary consents for processing such data. |

### notifications
| Method | Path | Description |
|--------|------|-------------|
| POST | /notifications | List lens notifications. |

### profileNotifications
| Method | Path | Description |
|--------|------|-------------|
| GET | /profileNotifications/ | List profile notifications. |

### profileSummaries
| Method | Path | Description |
|--------|------|-------------|
| GET | /profileSummaries | List profiles. |

### shareInvitations
| Method | Path | Description |
|--------|------|-------------|
| GET | /shareInvitations | List the share invitations.  WorkloadNamePrefix, LensNamePrefix, ProfileNamePrefix, and TemplateNamePrefix are mutually exclusive. Use the parameter that matches your ShareResourceType. |
| PATCH | /shareInvitations/{ShareInvitationId} | Update a workload or custom lens share invitation.  This API operation can be called independently of any resource. Previous documentation implied that a workload ARN must be specified. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags/{WorkloadArn} | List the tags for a resource.  The WorkloadArn parameter can be a workload ARN, a custom lens ARN, a profile ARN, or review template ARN. |
| POST | /tags/{WorkloadArn} | Adds one or more tags to the specified resource.  The WorkloadArn parameter can be a workload ARN, a custom lens ARN, a profile ARN, or review template ARN. |
| DELETE | /tags/{WorkloadArn} | Deletes specified tags from a resource.  The WorkloadArn parameter can be a workload ARN, a custom lens ARN, a profile ARN, or review template ARN.  To specify multiple tags, use separate tagKeys parameters, for example:  DELETE /tags/WorkloadArn?tagKeys=key1&amp;tagKeys=key2 |

### workloadsSummaries
| Method | Path | Description |
|--------|------|-------------|
| POST | /workloadsSummaries | Paginated list of workloads. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a share?" -> POST /lenses/{LensAlias}/shares
- "Create a version?" -> POST /lenses/{LensAlias}/versions
- "Create a milestone?" -> POST /workloads/{WorkloadId}/milestones
- "Create a profile?" -> POST /profiles
- "Create a share?" -> POST /profiles/{ProfileArn}/shares
- "Create a reviewTemplate?" -> POST /reviewTemplates
- "Create a workload?" -> POST /workloads
- "Create a share?" -> POST /workloads/{WorkloadId}/shares
- "Delete a lens?" -> DELETE /lenses/{LensAlias}
- "Delete a share?" -> DELETE /lenses/{LensAlias}/shares/{ShareId}
- "Delete a profile?" -> DELETE /profiles/{ProfileArn}
- "Delete a share?" -> DELETE /profiles/{ProfileArn}/shares/{ShareId}
- "Delete a reviewTemplate?" -> DELETE /reviewTemplates/{TemplateArn}
- "Delete a share?" -> DELETE /templates/shares/{TemplateArn}/{ShareId}
- "Delete a workload?" -> DELETE /workloads/{WorkloadId}
- "Delete a share?" -> DELETE /workloads/{WorkloadId}/shares/{ShareId}
- "List all export?" -> GET /lenses/{LensAlias}/export
- "Get answer details?" -> GET /workloads/{WorkloadId}/lensReviews/{LensAlias}/answers/{QuestionId}
- "List all consolidatedReport?" -> GET /consolidatedReport
- "List all global-settings?" -> GET /global-settings
- "Get lens details?" -> GET /lenses/{LensAlias}
- "Get lensReview details?" -> GET /workloads/{WorkloadId}/lensReviews/{LensAlias}
- "List all report?" -> GET /workloads/{WorkloadId}/lensReviews/{LensAlias}/report
- "List all versionDifference?" -> GET /lenses/{LensAlias}/versionDifference
- "Get milestone details?" -> GET /workloads/{WorkloadId}/milestones/{MilestoneNumber}
- "Get profile details?" -> GET /profiles/{ProfileArn}
- "List all profileTemplate?" -> GET /profileTemplate
- "Get reviewTemplate details?" -> GET /reviewTemplates/{TemplateArn}
- "Get answer details?" -> GET /reviewTemplates/{TemplateArn}/lensReviews/{LensAlias}/answers/{QuestionId}
- "Get lensReview details?" -> GET /reviewTemplates/{TemplateArn}/lensReviews/{LensAlias}
- "Get workload details?" -> GET /workloads/{WorkloadId}
- "List all answers?" -> GET /workloads/{WorkloadId}/lensReviews/{LensAlias}/answers
- "Create a check?" -> POST /workloads/{WorkloadId}/checks
- "Create a checkSummary?" -> POST /workloads/{WorkloadId}/checkSummaries
- "List all improvements?" -> GET /workloads/{WorkloadId}/lensReviews/{LensAlias}/improvements
- "List all lensReviews?" -> GET /workloads/{WorkloadId}/lensReviews
- "List all shares?" -> GET /lenses/{LensAlias}/shares
- "List all lenses?" -> GET /lenses
- "Create a milestonesSummary?" -> POST /workloads/{WorkloadId}/milestonesSummaries
- "Create a notification?" -> POST /notifications
- "List all profileNotifications?" -> GET /profileNotifications/
- "List all shares?" -> GET /profiles/{ProfileArn}/shares
- "List all profileSummaries?" -> GET /profileSummaries
- "List all answers?" -> GET /reviewTemplates/{TemplateArn}/lensReviews/{LensAlias}/answers
- "List all reviewTemplates?" -> GET /reviewTemplates
- "List all shareInvitations?" -> GET /shareInvitations
- "Get tag details?" -> GET /tags/{WorkloadArn}
- "Get share details?" -> GET /templates/shares/{TemplateArn}
- "List all shares?" -> GET /workloads/{WorkloadId}/shares
- "Create a workloadsSummary?" -> POST /workloadsSummaries
- "Delete a tag?" -> DELETE /tags/{WorkloadArn}
- "Partially update a answer?" -> PATCH /workloads/{WorkloadId}/lensReviews/{LensAlias}/answers/{QuestionId}
- "Create a updateIntegration?" -> POST /workloads/{WorkloadId}/updateIntegration
- "Partially update a lensReview?" -> PATCH /workloads/{WorkloadId}/lensReviews/{LensAlias}
- "Partially update a profile?" -> PATCH /profiles/{ProfileArn}
- "Partially update a reviewTemplate?" -> PATCH /reviewTemplates/{TemplateArn}
- "Partially update a answer?" -> PATCH /reviewTemplates/{TemplateArn}/lensReviews/{LensAlias}/answers/{QuestionId}
- "Partially update a lensReview?" -> PATCH /reviewTemplates/{TemplateArn}/lensReviews/{LensAlias}
- "Partially update a shareInvitation?" -> PATCH /shareInvitations/{ShareInvitationId}
- "Partially update a workload?" -> PATCH /workloads/{WorkloadId}
- "Partially update a share?" -> PATCH /workloads/{WorkloadId}/shares/{ShareId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
