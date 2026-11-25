---
name: amazon-guardduty
description: "Amazon GuardDuty API skill. Use when working with Amazon GuardDuty for detector, malware-protection-plan, invitation. Covers 74 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon GuardDuty
API version: 2017-11-28

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /invitation/count -- verify access
3. POST /detector/{detectorId}/administrator -- create first administrator

## Endpoints

74 endpoints across 7 groups. See references/api-spec.lap for full details.

### detector
| Method | Path | Description |
|--------|------|-------------|
| POST | /detector/{detectorId}/administrator | Accepts the invitation to be a member account and get monitored by a GuardDuty administrator account that sent the invitation. |
| POST | /detector/{detectorId}/master | Accepts the invitation to be monitored by a GuardDuty administrator account. |
| POST | /detector/{detectorId}/findings/archive | Archives GuardDuty findings that are specified by the list of finding IDs.  Only the administrator account can archive findings. Member accounts don't have permission to archive findings from their accounts. |
| POST | /detector | Creates a single GuardDuty detector. A detector is a resource that represents the GuardDuty service. To start using GuardDuty, you must create a detector in each Region where you enable the service. You can have only one detector per account per Region. All data sources are enabled in a new detector by default.   When you don't specify any features, with an exception to RUNTIME_MONITORING, all the optional features are enabled by default.   When you specify some of the features, any feature that is not specified in the API call gets enabled by default, with an exception to RUNTIME_MONITORING.    Specifying both EKS Runtime Monitoring (EKS_RUNTIME_MONITORING) and Runtime Monitoring (RUNTIME_MONITORING) will cause an error. You can add only one of these two features because Runtime Monitoring already includes the threat detection for Amazon EKS resources. For more information, see Runtime Monitoring. There might be regional differences because some data sources might not be available in all the Amazon Web Services Regions where GuardDuty is presently supported. For more information, see Regions and endpoints. |
| POST | /detector/{detectorId}/filter | Creates a filter using the specified finding criteria. The maximum number of saved filters per Amazon Web Services account per Region is 100. For more information, see Quotas for GuardDuty. |
| POST | /detector/{detectorId}/ipset | Creates a new IPSet, which is called a trusted IP list in the console user interface. An IPSet is a list of IP addresses that are trusted for secure communication with Amazon Web Services infrastructure and applications. GuardDuty doesn't generate findings for IP addresses that are included in IPSets. Only users from the administrator account can use this operation. |
| POST | /detector/{detectorId}/member | Creates member accounts of the current Amazon Web Services account by specifying a list of Amazon Web Services account IDs. This step is a prerequisite for managing the associated member accounts either by invitation or through an organization. As a delegated administrator, using CreateMembers will enable GuardDuty in the added member accounts, with the exception of the organization delegated administrator account. A delegated administrator must enable GuardDuty prior to being added as a member. When you use CreateMembers as an Organizations delegated administrator, GuardDuty applies your organization's auto-enable settings to the member accounts in this request, irrespective of the accounts being new or existing members. For more information about the existing auto-enable settings for your organization, see DescribeOrganizationConfiguration. If you disassociate a member account that was added by invitation, the member account details obtained from this API, including the associated email addresses, will be retained. This is done so that the delegated administrator can invoke the InviteMembers API without the need to invoke the CreateMembers API again. To remove the details associated with a member account, the delegated administrator must invoke the DeleteMembers API.  When the member accounts added through Organizations are later disassociated, you (administrator) can't invite them by calling the InviteMembers API. You can create an association with these member accounts again only by calling the CreateMembers API. |
| POST | /detector/{detectorId}/publishingDestination | Creates a publishing destination to export findings to. The resource to export findings to must exist before you use this operation. |
| POST | /detector/{detectorId}/findings/create | Generates sample findings of types specified by the list of finding types. If 'NULL' is specified for findingTypes, the API generates sample findings of all supported finding types. |
| POST | /detector/{detectorId}/threatintelset | Creates a new ThreatIntelSet. ThreatIntelSets consist of known malicious IP addresses. GuardDuty generates findings based on ThreatIntelSets. Only users of the administrator account can use this operation. |
| DELETE | /detector/{detectorId} | Deletes an Amazon GuardDuty detector that is specified by the detector ID. |
| DELETE | /detector/{detectorId}/filter/{filterName} | Deletes the filter specified by the filter name. |
| DELETE | /detector/{detectorId}/ipset/{ipSetId} | Deletes the IPSet specified by the ipSetId. IPSets are called trusted IP lists in the console user interface. |
| POST | /detector/{detectorId}/member/delete | Deletes GuardDuty member accounts (to the current GuardDuty administrator account) specified by the account IDs. With autoEnableOrganizationMembers configuration for your organization set to ALL, you'll receive an error if you attempt to disable GuardDuty for a member account in your organization. |
| DELETE | /detector/{detectorId}/publishingDestination/{destinationId} | Deletes the publishing definition with the specified destinationId. |
| DELETE | /detector/{detectorId}/threatintelset/{threatIntelSetId} | Deletes the ThreatIntelSet specified by the ThreatIntelSet ID. |
| POST | /detector/{detectorId}/malware-scans | Returns a list of malware scans. Each member account can view the malware scans for their own accounts. An administrator can view the malware scans for all the member accounts. There might be regional differences because some data sources might not be available in all the Amazon Web Services Regions where GuardDuty is presently supported. For more information, see Regions and endpoints. |
| GET | /detector/{detectorId}/admin | Returns information about the account selected as the delegated administrator for GuardDuty. There might be regional differences because some data sources might not be available in all the Amazon Web Services Regions where GuardDuty is presently supported. For more information, see Regions and endpoints. |
| GET | /detector/{detectorId}/publishingDestination/{destinationId} | Returns information about the publishing destination specified by the provided destinationId. |
| POST | /detector/{detectorId}/administrator/disassociate | Disassociates the current GuardDuty member account from its administrator account. When you disassociate an invited member from a GuardDuty delegated administrator, the member account details obtained from the CreateMembers API, including the associated email addresses, are retained. This is done so that the delegated administrator can invoke the InviteMembers API without the need to invoke the CreateMembers API again. To remove the details associated with a member account, the delegated administrator must invoke the DeleteMembers API.  With autoEnableOrganizationMembers configuration for your organization set to ALL, you'll receive an error if you attempt to disable GuardDuty in a member account. |
| POST | /detector/{detectorId}/master/disassociate | Disassociates the current GuardDuty member account from its administrator account. When you disassociate an invited member from a GuardDuty delegated administrator, the member account details obtained from the CreateMembers API, including the associated email addresses, are retained. This is done so that the delegated administrator can invoke the InviteMembers API without the need to invoke the CreateMembers API again. To remove the details associated with a member account, the delegated administrator must invoke the DeleteMembers API. |
| POST | /detector/{detectorId}/member/disassociate | Disassociates GuardDuty member accounts (from the current administrator account) specified by the account IDs. When you disassociate an invited member from a GuardDuty delegated administrator, the member account details obtained from the CreateMembers API, including the associated email addresses, are retained. This is done so that the delegated administrator can invoke the InviteMembers API without the need to invoke the CreateMembers API again. To remove the details associated with a member account, the delegated administrator must invoke the DeleteMembers API.  With autoEnableOrganizationMembers configuration for your organization set to ALL, you'll receive an error if you attempt to disassociate a member account before removing them from your organization. If you disassociate a member account that was added by invitation, the member account details obtained from this API, including the associated email addresses, will be retained. This is done so that the delegated administrator can invoke the InviteMembers API without the need to invoke the CreateMembers API again. To remove the details associated with a member account, the delegated administrator must invoke the DeleteMembers API.  When the member accounts added through Organizations are later disassociated, you (administrator) can't invite them by calling the InviteMembers API. You can create an association with these member accounts again only by calling the CreateMembers API. |
| GET | /detector/{detectorId}/administrator | Provides the details of the GuardDuty administrator account associated with the current GuardDuty member account.  If the organization's management account or a delegated administrator runs this API, it will return success (HTTP 200) but no content. |
| POST | /detector/{detectorId}/coverage/statistics | Retrieves aggregated statistics for your account. If you are a GuardDuty administrator, you can retrieve the statistics for all the resources associated with the active member accounts in your organization who have enabled Runtime Monitoring and have the GuardDuty security agent running on their resources. |
| GET | /detector/{detectorId} | Retrieves an Amazon GuardDuty detector specified by the detectorId. There might be regional differences because some data sources might not be available in all the Amazon Web Services Regions where GuardDuty is presently supported. For more information, see Regions and endpoints. |
| GET | /detector/{detectorId}/filter/{filterName} | Returns the details of the filter specified by the filter name. |
| POST | /detector/{detectorId}/findings/get | Describes Amazon GuardDuty findings specified by finding IDs. |
| POST | /detector/{detectorId}/findings/statistics | Lists Amazon GuardDuty findings statistics for the specified detector ID. There might be regional differences because some flags might not be available in all the Regions where GuardDuty is currently supported. For more information, see Regions and endpoints. |
| GET | /detector/{detectorId}/ipset/{ipSetId} | Retrieves the IPSet specified by the ipSetId. |
| GET | /detector/{detectorId}/malware-scan-settings | Returns the details of the malware scan settings. There might be regional differences because some data sources might not be available in all the Amazon Web Services Regions where GuardDuty is presently supported. For more information, see Regions and endpoints. |
| GET | /detector/{detectorId}/master | Provides the details for the GuardDuty administrator account associated with the current GuardDuty member account. |
| POST | /detector/{detectorId}/member/detector/get | Describes which data sources are enabled for the member account's detector. There might be regional differences because some data sources might not be available in all the Amazon Web Services Regions where GuardDuty is presently supported. For more information, see Regions and endpoints. |
| POST | /detector/{detectorId}/member/get | Retrieves GuardDuty member accounts (of the current GuardDuty administrator account) specified by the account IDs. |
| POST | /detector/{detectorId}/freeTrial/daysRemaining | Provides the number of days left for each data source used in the free trial period. |
| GET | /detector/{detectorId}/threatintelset/{threatIntelSetId} | Retrieves the ThreatIntelSet that is specified by the ThreatIntelSet ID. |
| POST | /detector/{detectorId}/usage/statistics | Lists Amazon GuardDuty usage statistics over the last 30 days for the specified detector ID. For newly enabled detectors or data sources, the cost returned will include only the usage so far under 30 days. This may differ from the cost metrics in the console, which project usage over 30 days to provide a monthly cost estimate. For more information, see Understanding How Usage Costs are Calculated. |
| POST | /detector/{detectorId}/member/invite | Invites Amazon Web Services accounts to become members of an organization administered by the Amazon Web Services account that invokes this API. If you are using Amazon Web Services Organizations to manage your GuardDuty environment, this step is not needed. For more information, see Managing accounts with organizations. To invite Amazon Web Services accounts, the first step is to ensure that GuardDuty has been enabled in the potential member accounts. You can now invoke this API to add accounts by invitation. The invited accounts can either accept or decline the invitation from their GuardDuty accounts. Each invited Amazon Web Services account can choose to accept the invitation from only one Amazon Web Services account. For more information, see Managing GuardDuty accounts by invitation. After the invite has been accepted and you choose to disassociate a member account (by using DisassociateMembers) from your account, the details of the member account obtained by invoking CreateMembers, including the associated email addresses, will be retained. This is done so that you can invoke InviteMembers without the need to invoke CreateMembers again. To remove the details associated with a member account, you must also invoke DeleteMembers.  If you disassociate a member account that was added by invitation, the member account details obtained from this API, including the associated email addresses, will be retained. This is done so that the delegated administrator can invoke the InviteMembers API without the need to invoke the CreateMembers API again. To remove the details associated with a member account, the delegated administrator must invoke the DeleteMembers API.  When the member accounts added through Organizations are later disassociated, you (administrator) can't invite them by calling the InviteMembers API. You can create an association with these member accounts again only by calling the CreateMembers API. |
| POST | /detector/{detectorId}/coverage | Lists coverage details for your GuardDuty account. If you're a GuardDuty administrator, you can retrieve all resources associated with the active member accounts in your organization. Make sure the accounts have Runtime Monitoring enabled and GuardDuty agent running on their resources. |
| GET | /detector | Lists detectorIds of all the existing Amazon GuardDuty detector resources. |
| GET | /detector/{detectorId}/filter | Returns a paginated list of the current filters. |
| POST | /detector/{detectorId}/findings | Lists GuardDuty findings for the specified detector ID. There might be regional differences because some flags might not be available in all the Regions where GuardDuty is currently supported. For more information, see Regions and endpoints. |
| GET | /detector/{detectorId}/ipset | Lists the IPSets of the GuardDuty service specified by the detector ID. If you use this operation from a member account, the IPSets returned are the IPSets from the associated administrator account. |
| GET | /detector/{detectorId}/member | Lists details about all member accounts for the current GuardDuty administrator account. |
| GET | /detector/{detectorId}/publishingDestination | Returns a list of publishing destinations associated with the specified detectorId. |
| GET | /detector/{detectorId}/threatintelset | Lists the ThreatIntelSets of the GuardDuty service specified by the detector ID. If you use this operation from a member account, the ThreatIntelSets associated with the administrator account are returned. |
| POST | /detector/{detectorId}/member/start | Turns on GuardDuty monitoring of the specified member accounts. Use this operation to restart monitoring of accounts that you stopped monitoring with the StopMonitoringMembers operation. |
| POST | /detector/{detectorId}/member/stop | Stops GuardDuty monitoring for the specified member accounts. Use the StartMonitoringMembers operation to restart monitoring for those accounts. With autoEnableOrganizationMembers configuration for your organization set to ALL, you'll receive an error if you attempt to stop monitoring the member accounts in your organization. |
| POST | /detector/{detectorId}/findings/unarchive | Unarchives GuardDuty findings specified by the findingIds. |
| POST | /detector/{detectorId} | Updates the GuardDuty detector specified by the detector ID. Specifying both EKS Runtime Monitoring (EKS_RUNTIME_MONITORING) and Runtime Monitoring (RUNTIME_MONITORING) will cause an error. You can add only one of these two features because Runtime Monitoring already includes the threat detection for Amazon EKS resources. For more information, see Runtime Monitoring. There might be regional differences because some data sources might not be available in all the Amazon Web Services Regions where GuardDuty is presently supported. For more information, see Regions and endpoints. |
| POST | /detector/{detectorId}/filter/{filterName} | Updates the filter specified by the filter name. |
| POST | /detector/{detectorId}/findings/feedback | Marks the specified GuardDuty findings as useful or not useful. |
| POST | /detector/{detectorId}/ipset/{ipSetId} | Updates the IPSet specified by the IPSet ID. |
| POST | /detector/{detectorId}/malware-scan-settings | Updates the malware scan settings. There might be regional differences because some data sources might not be available in all the Amazon Web Services Regions where GuardDuty is presently supported. For more information, see Regions and endpoints. |
| POST | /detector/{detectorId}/member/detector/update | Contains information on member accounts to be updated. Specifying both EKS Runtime Monitoring (EKS_RUNTIME_MONITORING) and Runtime Monitoring (RUNTIME_MONITORING) will cause an error. You can add only one of these two features because Runtime Monitoring already includes the threat detection for Amazon EKS resources. For more information, see Runtime Monitoring. There might be regional differences because some data sources might not be available in all the Amazon Web Services Regions where GuardDuty is presently supported. For more information, see Regions and endpoints. |
| POST | /detector/{detectorId}/admin | Configures the delegated administrator account with the provided values. You must provide a value for either autoEnableOrganizationMembers or autoEnable, but not both.  Specifying both EKS Runtime Monitoring (EKS_RUNTIME_MONITORING) and Runtime Monitoring (RUNTIME_MONITORING) will cause an error. You can add only one of these two features because Runtime Monitoring already includes the threat detection for Amazon EKS resources. For more information, see Runtime Monitoring. There might be regional differences because some data sources might not be available in all the Amazon Web Services Regions where GuardDuty is presently supported. For more information, see Regions and endpoints. |
| POST | /detector/{detectorId}/publishingDestination/{destinationId} | Updates information about the publishing destination specified by the destinationId. |
| POST | /detector/{detectorId}/threatintelset/{threatIntelSetId} | Updates the ThreatIntelSet specified by the ThreatIntelSet ID. |

### malware-protection-plan
| Method | Path | Description |
|--------|------|-------------|
| POST | /malware-protection-plan | Creates a new Malware Protection plan for the protected resource. When you create a Malware Protection plan, the Amazon Web Services service terms for GuardDuty Malware Protection apply. For more information, see Amazon Web Services service terms for GuardDuty Malware Protection. |
| DELETE | /malware-protection-plan/{malwareProtectionPlanId} | Deletes the Malware Protection plan ID associated with the Malware Protection plan resource. Use this API only when you no longer want to protect the resource associated with this Malware Protection plan ID. |
| GET | /malware-protection-plan/{malwareProtectionPlanId} | Retrieves the Malware Protection plan details associated with a Malware Protection plan ID. |
| GET | /malware-protection-plan | Lists the Malware Protection plan IDs associated with the protected resources in your Amazon Web Services account. |
| PATCH | /malware-protection-plan/{malwareProtectionPlanId} | Updates an existing Malware Protection plan resource. |

### invitation
| Method | Path | Description |
|--------|------|-------------|
| POST | /invitation/decline | Declines invitations sent to the current member account by Amazon Web Services accounts specified by their account IDs. |
| POST | /invitation/delete | Deletes invitations sent to the current member account by Amazon Web Services accounts specified by their account IDs. |
| GET | /invitation/count | Returns the count of all GuardDuty membership invitations that were sent to the current member account except the currently accepted invitation. |
| GET | /invitation | Lists all GuardDuty membership invitations that were sent to the current Amazon Web Services account. |

### admin
| Method | Path | Description |
|--------|------|-------------|
| POST | /admin/disable | Removes the existing GuardDuty delegated administrator of the organization. Only the organization's management account can run this API operation. |
| POST | /admin/enable | Designates an Amazon Web Services account within the organization as your GuardDuty delegated administrator. Only the organization's management account can run this API operation. |
| GET | /admin | Lists the accounts designated as GuardDuty delegated administrators. Only the organization's management account can run this API operation. |

### organization
| Method | Path | Description |
|--------|------|-------------|
| GET | /organization/statistics | Retrieves how many active member accounts have each feature enabled within GuardDuty. Only a delegated GuardDuty administrator of an organization can run this API. When you create a new organization, it might take up to 24 hours to generate the statistics for the entire organization. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags/{resourceArn} | Lists tags for a resource. Tagging is currently supported for detectors, finding filters, IP sets, threat intel sets, and publishing destination, with a limit of 50 tags per resource. When invoked, this operation returns all assigned tags for a given resource. |
| POST | /tags/{resourceArn} | Adds tags to a resource. |
| DELETE | /tags/{resourceArn} | Removes tags from a resource. |

### malware-scan
| Method | Path | Description |
|--------|------|-------------|
| POST | /malware-scan/start | Initiates the malware scan. Invoking this API will automatically create the Service-linked role in the corresponding account. When the malware scan starts, you can use the associated scan ID to track the status of the scan. For more information, see DescribeMalwareScans. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a administrator?" -> POST /detector/{detectorId}/administrator
- "Create a master?" -> POST /detector/{detectorId}/master
- "Create a archive?" -> POST /detector/{detectorId}/findings/archive
- "Create a detector?" -> POST /detector
- "Create a filter?" -> POST /detector/{detectorId}/filter
- "Create a ipset?" -> POST /detector/{detectorId}/ipset
- "Create a malware-protection-plan?" -> POST /malware-protection-plan
- "Create a member?" -> POST /detector/{detectorId}/member
- "Create a publishingDestination?" -> POST /detector/{detectorId}/publishingDestination
- "Create a create?" -> POST /detector/{detectorId}/findings/create
- "Create a threatintelset?" -> POST /detector/{detectorId}/threatintelset
- "Create a decline?" -> POST /invitation/decline
- "Delete a detector?" -> DELETE /detector/{detectorId}
- "Delete a filter?" -> DELETE /detector/{detectorId}/filter/{filterName}
- "Delete a ipset?" -> DELETE /detector/{detectorId}/ipset/{ipSetId}
- "Create a delete?" -> POST /invitation/delete
- "Delete a malware-protection-plan?" -> DELETE /malware-protection-plan/{malwareProtectionPlanId}
- "Create a delete?" -> POST /detector/{detectorId}/member/delete
- "Delete a publishingDestination?" -> DELETE /detector/{detectorId}/publishingDestination/{destinationId}
- "Delete a threatintelset?" -> DELETE /detector/{detectorId}/threatintelset/{threatIntelSetId}
- "Create a malware-scan?" -> POST /detector/{detectorId}/malware-scans
- "List all admin?" -> GET /detector/{detectorId}/admin
- "Get publishingDestination details?" -> GET /detector/{detectorId}/publishingDestination/{destinationId}
- "Create a disable?" -> POST /admin/disable
- "Create a disassociate?" -> POST /detector/{detectorId}/administrator/disassociate
- "Create a disassociate?" -> POST /detector/{detectorId}/master/disassociate
- "Create a disassociate?" -> POST /detector/{detectorId}/member/disassociate
- "Create a enable?" -> POST /admin/enable
- "List all administrator?" -> GET /detector/{detectorId}/administrator
- "Create a statistic?" -> POST /detector/{detectorId}/coverage/statistics
- "Get detector details?" -> GET /detector/{detectorId}
- "Get filter details?" -> GET /detector/{detectorId}/filter/{filterName}
- "Create a get?" -> POST /detector/{detectorId}/findings/get
- "Create a statistic?" -> POST /detector/{detectorId}/findings/statistics
- "Get ipset details?" -> GET /detector/{detectorId}/ipset/{ipSetId}
- "List all count?" -> GET /invitation/count
- "Get malware-protection-plan details?" -> GET /malware-protection-plan/{malwareProtectionPlanId}
- "List all malware-scan-settings?" -> GET /detector/{detectorId}/malware-scan-settings
- "List all master?" -> GET /detector/{detectorId}/master
- "Create a get?" -> POST /detector/{detectorId}/member/detector/get
- "Create a get?" -> POST /detector/{detectorId}/member/get
- "List all statistics?" -> GET /organization/statistics
- "Create a daysRemaining?" -> POST /detector/{detectorId}/freeTrial/daysRemaining
- "Get threatintelset details?" -> GET /detector/{detectorId}/threatintelset/{threatIntelSetId}
- "Create a statistic?" -> POST /detector/{detectorId}/usage/statistics
- "Create a invite?" -> POST /detector/{detectorId}/member/invite
- "Create a coverage?" -> POST /detector/{detectorId}/coverage
- "List all detector?" -> GET /detector
- "List all filter?" -> GET /detector/{detectorId}/filter
- "Create a finding?" -> POST /detector/{detectorId}/findings
- "List all ipset?" -> GET /detector/{detectorId}/ipset
- "List all invitation?" -> GET /invitation
- "List all malware-protection-plan?" -> GET /malware-protection-plan
- "List all member?" -> GET /detector/{detectorId}/member
- "List all admin?" -> GET /admin
- "List all publishingDestination?" -> GET /detector/{detectorId}/publishingDestination
- "Get tag details?" -> GET /tags/{resourceArn}
- "List all threatintelset?" -> GET /detector/{detectorId}/threatintelset
- "Create a start?" -> POST /malware-scan/start
- "Create a start?" -> POST /detector/{detectorId}/member/start
- "Create a stop?" -> POST /detector/{detectorId}/member/stop
- "Create a unarchive?" -> POST /detector/{detectorId}/findings/unarchive
- "Delete a tag?" -> DELETE /tags/{resourceArn}
- "Create a feedback?" -> POST /detector/{detectorId}/findings/feedback
- "Partially update a malware-protection-plan?" -> PATCH /malware-protection-plan/{malwareProtectionPlanId}
- "Create a malware-scan-setting?" -> POST /detector/{detectorId}/malware-scan-settings
- "Create a update?" -> POST /detector/{detectorId}/member/detector/update
- "Create a admin?" -> POST /detector/{detectorId}/admin
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
