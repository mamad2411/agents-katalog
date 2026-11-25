---
name: aws-securityhub
description: "AWS SecurityHub API skill. Use when working with AWS SecurityHub for administrator, master, automationrules. Covers 79 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS SecurityHub
API version: 2018-10-26

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /accounts -- verify access
3. POST /administrator -- create first administrator

## Endpoints

79 endpoints across 21 groups. See references/api-spec.lap for full details.

### administrator
| Method | Path | Description |
|--------|------|-------------|
| POST | /administrator | Accepts the invitation to be a member account and be monitored by the Security Hub administrator account that the invitation was sent from. This operation is only used by member accounts that are not added through Organizations. When the member account accepts the invitation, permission is granted to the administrator account to view findings generated in the member account. |
| POST | /administrator/disassociate | Disassociates the current Security Hub member account from the associated administrator account. This operation is only used by accounts that are not part of an organization. For organization accounts, only the administrator account can disassociate a member account. |
| GET | /administrator | Provides the details for the Security Hub administrator account for the current member account. Can be used by both member accounts that are managed using Organizations and accounts that were invited manually. |

### master
| Method | Path | Description |
|--------|------|-------------|
| POST | /master | This method is deprecated. Instead, use AcceptAdministratorInvitation. The Security Hub console continues to use AcceptInvitation. It will eventually change to use AcceptAdministratorInvitation. Any IAM policies that specifically control access to this function must continue to use AcceptInvitation. You should also add AcceptAdministratorInvitation to your policies to ensure that the correct permissions are in place after the console begins to use AcceptAdministratorInvitation. Accepts the invitation to be a member account and be monitored by the Security Hub administrator account that the invitation was sent from. This operation is only used by member accounts that are not added through Organizations. When the member account accepts the invitation, permission is granted to the administrator account to view findings generated in the member account. |
| POST | /master/disassociate | This method is deprecated. Instead, use DisassociateFromAdministratorAccount. The Security Hub console continues to use DisassociateFromMasterAccount. It will eventually change to use DisassociateFromAdministratorAccount. Any IAM policies that specifically control access to this function must continue to use DisassociateFromMasterAccount. You should also add DisassociateFromAdministratorAccount to your policies to ensure that the correct permissions are in place after the console begins to use DisassociateFromAdministratorAccount. Disassociates the current Security Hub member account from the associated administrator account. This operation is only used by accounts that are not part of an organization. For organization accounts, only the administrator account can disassociate a member account. |
| GET | /master | This method is deprecated. Instead, use GetAdministratorAccount. The Security Hub console continues to use GetMasterAccount. It will eventually change to use GetAdministratorAccount. Any IAM policies that specifically control access to this function must continue to use GetMasterAccount. You should also add GetAdministratorAccount to your policies to ensure that the correct permissions are in place after the console begins to use GetAdministratorAccount. Provides the details for the Security Hub administrator account for the current member account. Can be used by both member accounts that are managed using Organizations and accounts that were invited manually. |

### automationrules
| Method | Path | Description |
|--------|------|-------------|
| POST | /automationrules/delete | Deletes one or more automation rules. |
| POST | /automationrules/get | Retrieves a list of details for automation rules based on rule Amazon Resource Names (ARNs). |
| PATCH | /automationrules/update | Updates one or more automation rules based on rule Amazon Resource Names (ARNs) and input parameters. |
| POST | /automationrules/create | Creates an automation rule based on input parameters. |
| GET | /automationrules/list | A list of automation rules and their metadata for the calling account. |

### standards
| Method | Path | Description |
|--------|------|-------------|
| POST | /standards/deregister | Disables the standards specified by the provided StandardsSubscriptionArns. For more information, see Security Standards section of the Security Hub User Guide. |
| POST | /standards/register | Enables the standards specified by the provided StandardsArn. To obtain the ARN for a standard, use the DescribeStandards operation. For more information, see the Security Standards section of the Security Hub User Guide. |
| GET | /standards | Returns a list of the available standards in Security Hub. For each standard, the results include the standard ARN, the name, and a description. |
| GET | /standards/controls/{StandardsSubscriptionArn+} | Returns a list of security standards controls. For each control, the results include information about whether it is currently enabled, the severity, and a link to remediation information. |
| POST | /standards/get | Returns a list of the standards that are currently enabled. |
| PATCH | /standards/control/{StandardsControlArn+} | Used to control whether an individual security standard control is enabled or disabled. |

### configurationPolicyAssociation
| Method | Path | Description |
|--------|------|-------------|
| POST | /configurationPolicyAssociation/batchget | Returns associations between an Security Hub configuration and a batch of target accounts, organizational units, or the root. Only the Security Hub delegated administrator can invoke this operation from the home Region. A configuration can refer to a configuration policy or to a self-managed configuration. |
| POST | /configurationPolicyAssociation/get | Returns the association between a configuration and a target account, organizational unit, or the root. The configuration can be a configuration policy or self-managed behavior. Only the Security Hub delegated administrator can invoke this operation from the home Region. |
| POST | /configurationPolicyAssociation/list | Provides information about the associations for your configuration policies and self-managed behavior. Only the Security Hub delegated administrator can invoke this operation from the home Region. |
| POST | /configurationPolicyAssociation/associate | Associates a target account, organizational unit, or the root with a specified configuration. The target can be associated with a configuration policy or self-managed behavior. Only the Security Hub delegated administrator can invoke this operation from the home Region. |
| POST | /configurationPolicyAssociation/disassociate | Disassociates a target account, organizational unit, or the root from a specified configuration. When you disassociate a configuration from its target, the target inherits the configuration of the closest parent. If there’s no configuration to inherit, the target retains its settings but becomes a self-managed account. A target can be disassociated from a configuration policy or self-managed behavior. Only the Security Hub delegated administrator can invoke this operation from the home Region. |

### securityControls
| Method | Path | Description |
|--------|------|-------------|
| POST | /securityControls/batchGet | Provides details about a batch of security controls for the current Amazon Web Services account and Amazon Web Services Region. |
| GET | /securityControls/definitions | Lists all of the security controls that apply to a specified standard. |

### associations
| Method | Path | Description |
|--------|------|-------------|
| POST | /associations/batchGet | For a batch of security controls and standards, identifies whether each control is currently enabled or disabled in a standard. |
| PATCH | /associations | For a batch of security controls and standards, this operation updates the enablement status of a control in a standard. |
| GET | /associations | Specifies whether a control is currently enabled or disabled in each enabled standard in the calling account. |

### findings
| Method | Path | Description |
|--------|------|-------------|
| POST | /findings/import | Imports security findings generated by a finding provider into Security Hub. This action is requested by the finding provider to import its findings into Security Hub.  BatchImportFindings must be called by one of the following:   The Amazon Web Services account that is associated with a finding if you are using the default product ARN or are a partner sending findings from within a customer's Amazon Web Services account. In these cases, the identifier of the account that you are calling BatchImportFindings from needs to be the same as the AwsAccountId attribute for the finding.   An Amazon Web Services account that Security Hub has allow-listed for an official partner integration. In this case, you can call BatchImportFindings from the allow-listed account and send findings from different customer accounts in the same batch.   The maximum allowed size for a finding is 240 Kb. An error is returned for any finding larger than 240 Kb. After a finding is created, BatchImportFindings cannot be used to update the following finding fields and objects, which Security Hub customers use to manage their investigation workflow.    Note     UserDefinedFields     VerificationState     Workflow    Finding providers also should not use BatchImportFindings to update the following attributes.    Confidence     Criticality     RelatedFindings     Severity     Types    Instead, finding providers use FindingProviderFields to provide values for these attributes. |
| PATCH | /findings/batchupdate | Used by Security Hub customers to update information about their investigation into a finding. Requested by administrator accounts or member accounts. Administrator accounts can update findings for their account and their member accounts. Member accounts can update findings for their account. Updates from BatchUpdateFindings do not affect the value of UpdatedAt for a finding. Administrator and member accounts can use BatchUpdateFindings to update the following finding fields and objects.    Confidence     Criticality     Note     RelatedFindings     Severity     Types     UserDefinedFields     VerificationState     Workflow    You can configure IAM policies to restrict access to fields and field values. For example, you might not want member accounts to be able to suppress findings or change the finding severity. See Configuring access to BatchUpdateFindings in the Security Hub User Guide. |
| POST | /findings | Returns a list of findings that match the specified criteria. If finding aggregation is enabled, then when you call GetFindings from the aggregation Region, the results include all of the matching findings from both the aggregation Region and the linked Regions. |
| PATCH | /findings | UpdateFindings is a deprecated operation. Instead of UpdateFindings, use the BatchUpdateFindings operation. The UpdateFindings operation updates the Note and RecordState of the Security Hub aggregated findings that the filter attributes specify. Any member account that can view the finding can also see the update to the finding. Finding updates made with UpdateFindings aren't persisted if the same finding is later updated by the finding provider through the BatchImportFindings operation. In addition, Security Hub doesn't record updates made with UpdateFindings in the finding history. |

### actionTargets
| Method | Path | Description |
|--------|------|-------------|
| POST | /actionTargets | Creates a custom action target in Security Hub. You can use custom actions on findings and insights in Security Hub to trigger target actions in Amazon CloudWatch Events. |
| DELETE | /actionTargets/{ActionTargetArn+} | Deletes a custom action target from Security Hub. Deleting a custom action target does not affect any findings or insights that were already sent to Amazon CloudWatch Events using the custom action. |
| POST | /actionTargets/get | Returns a list of the custom action targets in Security Hub in your account. |
| PATCH | /actionTargets/{ActionTargetArn+} | Updates the name and description of a custom action target in Security Hub. |

### configurationPolicy
| Method | Path | Description |
|--------|------|-------------|
| POST | /configurationPolicy/create | Creates a configuration policy with the defined configuration. Only the Security Hub delegated administrator can invoke this operation from the home Region. |
| DELETE | /configurationPolicy/{Identifier} | Deletes a configuration policy. Only the Security Hub delegated administrator can invoke this operation from the home Region. For the deletion to succeed, you must first disassociate a configuration policy from target accounts, organizational units, or the root by invoking the StartConfigurationPolicyDisassociation operation. |
| GET | /configurationPolicy/get/{Identifier} | Provides information about a configuration policy. Only the Security Hub delegated administrator can invoke this operation from the home Region. |
| GET | /configurationPolicy/list | Lists the configuration policies that the Security Hub delegated administrator has created for your organization. Only the delegated administrator can invoke this operation from the home Region. |
| PATCH | /configurationPolicy/{Identifier} | Updates a configuration policy. Only the Security Hub delegated administrator can invoke this operation from the home Region. |

### findingAggregator
| Method | Path | Description |
|--------|------|-------------|
| POST | /findingAggregator/create | Used to enable finding aggregation. Must be called from the aggregation Region. For more details about cross-Region replication, see Configuring finding aggregation in the Security Hub User Guide. |
| DELETE | /findingAggregator/delete/{FindingAggregatorArn+} | Deletes a finding aggregator. When you delete the finding aggregator, you stop finding aggregation. When you stop finding aggregation, findings that were already aggregated to the aggregation Region are still visible from the aggregation Region. New findings and finding updates are not aggregated. |
| GET | /findingAggregator/get/{FindingAggregatorArn+} | Returns the current finding aggregation configuration. |
| GET | /findingAggregator/list | If finding aggregation is enabled, then ListFindingAggregators returns the ARN of the finding aggregator. You can run this operation from any Region. |
| PATCH | /findingAggregator/update | Updates the finding aggregation configuration. Used to update the Region linking mode and the list of included or excluded Regions. You cannot use UpdateFindingAggregator to change the aggregation Region. You must run UpdateFindingAggregator from the current aggregation Region. |

### insights
| Method | Path | Description |
|--------|------|-------------|
| POST | /insights | Creates a custom insight in Security Hub. An insight is a consolidation of findings that relate to a security issue that requires attention or remediation. To group the related findings in the insight, use the GroupByAttribute. |
| DELETE | /insights/{InsightArn+} | Deletes the insight specified by the InsightArn. |
| GET | /insights/results/{InsightArn+} | Lists the results of the Security Hub insight specified by the insight ARN. |
| POST | /insights/get | Lists and describes insights for the specified insight ARNs. |
| PATCH | /insights/{InsightArn+} | Updates the Security Hub insight identified by the specified insight ARN. |

### members
| Method | Path | Description |
|--------|------|-------------|
| POST | /members | Creates a member association in Security Hub between the specified accounts and the account used to make the request, which is the administrator account. If you are integrated with Organizations, then the administrator account is designated by the organization management account.  CreateMembers is always used to add accounts that are not organization members. For accounts that are managed using Organizations, CreateMembers is only used in the following cases:   Security Hub is not configured to automatically add new organization accounts.   The account was disassociated or deleted in Security Hub.   This action can only be used by an account that has Security Hub enabled. To enable Security Hub, you can use the EnableSecurityHub operation. For accounts that are not organization members, you create the account association and then send an invitation to the member account. To send the invitation, you use the InviteMembers operation. If the account owner accepts the invitation, the account becomes a member account in Security Hub. Accounts that are managed using Organizations do not receive an invitation. They automatically become a member account in Security Hub.   If the organization account does not have Security Hub enabled, then Security Hub and the default standards are automatically enabled. Note that Security Hub cannot be enabled automatically for the organization management account. The organization management account must enable Security Hub before the administrator account enables it as a member account.   For organization accounts that already have Security Hub enabled, Security Hub does not make any other changes to those accounts. It does not change their enabled standards or controls.   A permissions policy is added that permits the administrator account to view the findings generated in the member account. To remove the association between the administrator and member accounts, use the DisassociateFromMasterAccount or DisassociateMembers operation. |
| POST | /members/delete | Deletes the specified member accounts from Security Hub. You can invoke this API only to delete accounts that became members through invitation. You can't invoke this API to delete accounts that belong to an Organizations organization. |
| POST | /members/disassociate | Disassociates the specified member accounts from the associated administrator account. Can be used to disassociate both accounts that are managed using Organizations and accounts that were invited manually. |
| POST | /members/get | Returns the details for the Security Hub member accounts for the specified account IDs. An administrator account can be either the delegated Security Hub administrator account for an organization or an administrator account that enabled Security Hub manually. The results include both member accounts that are managed using Organizations and accounts that were invited manually. |
| POST | /members/invite | Invites other Amazon Web Services accounts to become member accounts for the Security Hub administrator account that the invitation is sent from. This operation is only used to invite accounts that do not belong to an organization. Organization accounts do not receive invitations. Before you can use this action to invite a member, you must first use the CreateMembers action to create the member account in Security Hub. When the account owner enables Security Hub and accepts the invitation to become a member account, the administrator account can view the findings generated from the member account. |
| GET | /members | Lists details about all member accounts for the current Security Hub administrator account. The results include both member accounts that belong to an organization and member accounts that were invited manually. |

### invitations
| Method | Path | Description |
|--------|------|-------------|
| POST | /invitations/decline | Declines invitations to become a member account. A prospective member account uses this operation to decline an invitation to become a member. This operation is only called by member accounts that aren't part of an organization. Organization accounts don't receive invitations. |
| POST | /invitations/delete | Deletes invitations received by the Amazon Web Services account to become a member account. A Security Hub administrator account can use this operation to delete invitations sent to one or more member accounts. This operation is only used to delete invitations that are sent to member accounts that aren't part of an organization. Organization accounts don't receive invitations. |
| GET | /invitations/count | Returns the count of all Security Hub membership invitations that were sent to the current member account, not including the currently accepted invitation. |
| GET | /invitations | Lists all Security Hub membership invitations that were sent to the current Amazon Web Services account. This operation is only used by accounts that are managed by invitation. Accounts that are managed using the integration with Organizations do not receive invitations. |

### accounts
| Method | Path | Description |
|--------|------|-------------|
| GET | /accounts | Returns details about the Hub resource in your account, including the HubArn and the time when you enabled Security Hub. |
| DELETE | /accounts | Disables Security Hub in your account only in the current Amazon Web Services Region. To disable Security Hub in all Regions, you must submit one request per Region where you have enabled Security Hub. You can't disable Security Hub in an account that is currently the Security Hub administrator. When you disable Security Hub, your existing findings and insights and any Security Hub configuration settings are deleted after 90 days and cannot be recovered. Any standards that were enabled are disabled, and your administrator and member account associations are removed. If you want to save your existing findings, you must export them before you disable Security Hub. |
| POST | /accounts | Enables Security Hub for your account in the current Region or the Region you specify in the request. When you enable Security Hub, you grant to Security Hub the permissions necessary to gather findings from other services that are integrated with Security Hub. When you use the EnableSecurityHub operation to enable Security Hub, you also automatically enable the following standards:   Center for Internet Security (CIS) Amazon Web Services Foundations Benchmark v1.2.0   Amazon Web Services Foundational Security Best Practices   Other standards are not automatically enabled.  To opt out of automatically enabled standards, set EnableDefaultStandards to false. After you enable Security Hub, to enable a standard, use the BatchEnableStandards operation. To disable a standard, use the BatchDisableStandards operation. To learn more, see the setup information in the Security Hub User Guide. |
| PATCH | /accounts | Updates configuration options for Security Hub. |

### organization
| Method | Path | Description |
|--------|------|-------------|
| GET | /organization/configuration | Returns information about the way your organization is configured in Security Hub. Only the Security Hub administrator account can invoke this operation. |
| POST | /organization/admin/disable | Disables a Security Hub administrator account. Can only be called by the organization management account. |
| POST | /organization/admin/enable | Designates the Security Hub administrator account for an organization. Can only be called by the organization management account. |
| GET | /organization/admin | Lists the Security Hub administrator accounts. Can only be called by the organization management account. |
| POST | /organization/configuration | Updates the configuration of your organization in Security Hub. Only the Security Hub administrator account can invoke this operation. |

### products
| Method | Path | Description |
|--------|------|-------------|
| GET | /products | Returns information about product integrations in Security Hub. You can optionally provide an integration ARN. If you provide an integration ARN, then the results only include that integration. If you do not provide an integration ARN, then the results include all of the available product integrations. |

### productSubscriptions
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /productSubscriptions/{ProductSubscriptionArn+} | Disables the integration of the specified product with Security Hub. After the integration is disabled, findings from that product are no longer sent to Security Hub. |
| POST | /productSubscriptions | Enables the integration of a partner product with Security Hub. Integrated products send findings to Security Hub. When you enable a product integration, a permissions policy that grants permission for the product to send findings to Security Hub is applied. |
| GET | /productSubscriptions | Lists all findings-generating solutions (products) that you are subscribed to receive findings from in Security Hub. |

### findingHistory
| Method | Path | Description |
|--------|------|-------------|
| POST | /findingHistory/get | Returns history for a Security Hub finding in the last 90 days. The history includes changes made to any fields in the Amazon Web Services Security Finding Format (ASFF). |

### securityControl
| Method | Path | Description |
|--------|------|-------------|
| GET | /securityControl/definition | Retrieves the definition of a security control. The definition includes the control title, description, Region availability, parameter definitions, and other details. |
| PATCH | /securityControl/update | Updates the properties of a security control. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags/{ResourceArn} | Returns a list of tags associated with a resource. |
| POST | /tags/{ResourceArn} | Adds one or more tags to a resource. |
| DELETE | /tags/{ResourceArn} | Removes one or more tags from a resource. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a administrator?" -> POST /administrator
- "Create a master?" -> POST /master
- "Create a delete?" -> POST /automationrules/delete
- "Create a deregister?" -> POST /standards/deregister
- "Create a register?" -> POST /standards/register
- "Create a get?" -> POST /automationrules/get
- "Create a batchget?" -> POST /configurationPolicyAssociation/batchget
- "Create a batchGet?" -> POST /securityControls/batchGet
- "Create a batchGet?" -> POST /associations/batchGet
- "Create a import?" -> POST /findings/import
- "Create a actionTarget?" -> POST /actionTargets
- "Create a create?" -> POST /automationrules/create
- "Create a create?" -> POST /configurationPolicy/create
- "Create a create?" -> POST /findingAggregator/create
- "Create a insight?" -> POST /insights
- "Create a member?" -> POST /members
- "Create a decline?" -> POST /invitations/decline
- "Delete a actionTarget?" -> DELETE /actionTargets/{ActionTargetArn+}
- "Delete a configurationPolicy?" -> DELETE /configurationPolicy/{Identifier}
- "Delete a delete?" -> DELETE /findingAggregator/delete/{FindingAggregatorArn+}
- "Delete a insight?" -> DELETE /insights/{InsightArn+}
- "Create a delete?" -> POST /invitations/delete
- "Create a delete?" -> POST /members/delete
- "Create a get?" -> POST /actionTargets/get
- "List all accounts?" -> GET /accounts
- "List all configuration?" -> GET /organization/configuration
- "List all products?" -> GET /products
- "List all standards?" -> GET /standards
- "Get control details?" -> GET /standards/controls/{StandardsSubscriptionArn+}
- "Delete a productSubscription?" -> DELETE /productSubscriptions/{ProductSubscriptionArn+}
- "Create a disable?" -> POST /organization/admin/disable
- "Create a disassociate?" -> POST /administrator/disassociate
- "Create a disassociate?" -> POST /master/disassociate
- "Create a disassociate?" -> POST /members/disassociate
- "Create a productSubscription?" -> POST /productSubscriptions
- "Create a enable?" -> POST /organization/admin/enable
- "Create a account?" -> POST /accounts
- "List all administrator?" -> GET /administrator
- "Get get details?" -> GET /configurationPolicy/get/{Identifier}
- "Create a get?" -> POST /configurationPolicyAssociation/get
- "Create a get?" -> POST /standards/get
- "Get get details?" -> GET /findingAggregator/get/{FindingAggregatorArn+}
- "Create a get?" -> POST /findingHistory/get
- "Create a finding?" -> POST /findings
- "Get result details?" -> GET /insights/results/{InsightArn+}
- "Create a get?" -> POST /insights/get
- "List all count?" -> GET /invitations/count
- "List all master?" -> GET /master
- "Create a get?" -> POST /members/get
- "List all definition?" -> GET /securityControl/definition
- "Create a invite?" -> POST /members/invite
- "List all list?" -> GET /automationrules/list
- "List all list?" -> GET /configurationPolicy/list
- "Create a list?" -> POST /configurationPolicyAssociation/list
- "List all productSubscriptions?" -> GET /productSubscriptions
- "List all list?" -> GET /findingAggregator/list
- "List all invitations?" -> GET /invitations
- "List all members?" -> GET /members
- "List all admin?" -> GET /organization/admin
- "List all definitions?" -> GET /securityControls/definitions
- "List all associations?" -> GET /associations
- "Get tag details?" -> GET /tags/{ResourceArn}
- "Create a associate?" -> POST /configurationPolicyAssociation/associate
- "Create a disassociate?" -> POST /configurationPolicyAssociation/disassociate
- "Delete a tag?" -> DELETE /tags/{ResourceArn}
- "Partially update a actionTarget?" -> PATCH /actionTargets/{ActionTargetArn+}
- "Partially update a configurationPolicy?" -> PATCH /configurationPolicy/{Identifier}
- "Partially update a insight?" -> PATCH /insights/{InsightArn+}
- "Create a configuration?" -> POST /organization/configuration
- "Partially update a control?" -> PATCH /standards/control/{StandardsControlArn+}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
