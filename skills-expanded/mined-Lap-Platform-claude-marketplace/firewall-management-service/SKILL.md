---
name: firewall-management-service
description: "Firewall Management Service API skill. Use when working with Firewall Management Service for root. Covers 42 endpoints."
version: 1.0.0
generator: lapsh
---

# Firewall Management Service
API version: 2018-01-01

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST / -- create first resource

## Endpoints

42 endpoints across 1 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| POST | / | Sets a Firewall Manager default administrator account. The Firewall Manager default administrator account can manage third-party firewalls and has full administrative scope that allows administration of all policy types, accounts, organizational units, and Regions. This account must be a member account of the organization in Organizations whose resources you want to protect. For information about working with Firewall Manager administrator accounts, see Managing Firewall Manager administrators in the Firewall Manager Developer Guide. |
| POST | / | Sets the Firewall Manager policy administrator as a tenant administrator of a third-party firewall service. A tenant is an instance of the third-party firewall service that's associated with your Amazon Web Services customer account. |
| POST | / | Associate resources to a Firewall Manager resource set. |
| POST | / | Disassociates resources from a Firewall Manager resource set. |
| POST | / | Permanently deletes an Firewall Manager applications list. |
| POST | / | Deletes an Firewall Manager association with the IAM role and the Amazon Simple Notification Service (SNS) topic that is used to record Firewall Manager SNS logs. |
| POST | / | Permanently deletes an Firewall Manager policy. |
| POST | / | Permanently deletes an Firewall Manager protocols list. |
| POST | / | Deletes the specified ResourceSet. |
| POST | / | Disassociates an Firewall Manager administrator account. To set a different account as an Firewall Manager administrator, submit a PutAdminAccount request. To set an account as a default administrator account, you must submit an AssociateAdminAccount request. Disassociation of the default administrator account follows the first in, last out principle. If you are the default administrator, all Firewall Manager administrators within the organization must first disassociate their accounts before you can disassociate your account. |
| POST | / | Disassociates a Firewall Manager policy administrator from a third-party firewall tenant. When you call DisassociateThirdPartyFirewall, the third-party firewall vendor deletes all of the firewalls that are associated with the account. |
| POST | / | Returns the Organizations account that is associated with Firewall Manager as the Firewall Manager default administrator. |
| POST | / | Returns information about the specified account's administrative scope. The administrative scope defines the resources that an Firewall Manager administrator can manage. |
| POST | / | Returns information about the specified Firewall Manager applications list. |
| POST | / | Returns detailed compliance information about the specified member account. Details include resources that are in and out of compliance with the specified policy.  The reasons for resources being considered compliant depend on the Firewall Manager policy type. |
| POST | / | Information about the Amazon Simple Notification Service (SNS) topic that is used to record Firewall Manager SNS logs. |
| POST | / | Returns information about the specified Firewall Manager policy. |
| POST | / | If you created a Shield Advanced policy, returns policy-level attack summary information in the event of a potential DDoS attack. Other policy types are currently unsupported. |
| POST | / | Returns information about the specified Firewall Manager protocols list. |
| POST | / | Gets information about a specific resource set. |
| POST | / | The onboarding status of a Firewall Manager admin account to third-party firewall vendor tenant. |
| POST | / | Retrieves violations for a resource based on the specified Firewall Manager policy and Amazon Web Services account. |
| POST | / | Returns a AdminAccounts object that lists the Firewall Manager administrators within the organization that are onboarded to Firewall Manager by AssociateAdminAccount. This operation can be called only from the organization's management account. |
| POST | / | Lists the accounts that are managing the specified Organizations member account. This is useful for any member account so that they can view the accounts who are managing their account. This operation only returns the managing administrators that have the requested account within their AdminScope. |
| POST | / | Returns an array of AppsListDataSummary objects. |
| POST | / | Returns an array of PolicyComplianceStatus objects. Use PolicyComplianceStatus to get a summary of which member accounts are protected by the specified policy. |
| POST | / | Returns an array of resources in the organization's accounts that are available to be associated with a resource set. |
| POST | / | Returns a MemberAccounts object that lists the member accounts in the administrator's Amazon Web Services organization. Either an Firewall Manager administrator or the organization's management account can make this request. |
| POST | / | Returns an array of PolicySummary objects. |
| POST | / | Returns an array of ProtocolsListDataSummary objects. |
| POST | / | Returns an array of resources that are currently associated to a resource set. |
| POST | / | Returns an array of ResourceSetSummary objects. |
| POST | / | Retrieves the list of tags for the specified Amazon Web Services resource. |
| POST | / | Retrieves a list of all of the third-party firewall policies that are associated with the third-party firewall administrator's account. |
| POST | / | Creates or updates an Firewall Manager administrator account. The account must be a member of the organization that was onboarded to Firewall Manager by AssociateAdminAccount. Only the organization's management account can create an Firewall Manager administrator account. When you create an Firewall Manager administrator account, the service checks to see if the account is already a delegated administrator within Organizations. If the account isn't a delegated administrator, Firewall Manager calls Organizations to delegate the account within Organizations. For more information about administrator accounts within Organizations, see Managing the Amazon Web Services Accounts in Your Organization. |
| POST | / | Creates an Firewall Manager applications list. |
| POST | / | Designates the IAM role and Amazon Simple Notification Service (SNS) topic that Firewall Manager uses to record SNS logs. To perform this action outside of the console, you must first configure the SNS topic's access policy to allow the SnsRoleName to publish SNS logs. If the SnsRoleName provided is a role other than the AWSServiceRoleForFMS service-linked role, this role must have a trust relationship configured to allow the Firewall Manager service principal fms.amazonaws.com to assume this role. For information about configuring an SNS access policy, see Service roles for Firewall Manager in the Firewall Manager Developer Guide. |
| POST | / | Creates an Firewall Manager policy. A Firewall Manager policy is specific to the individual policy type. If you want to enforce multiple policy types across accounts, you can create multiple policies. You can create more than one policy for each type.  If you add a new account to an organization that you created with Organizations, Firewall Manager automatically applies the policy to the resources in that account that are within scope of the policy.  Firewall Manager provides the following types of policies:     WAF policy - This policy applies WAF web ACL protections to specified accounts and resources.     Shield Advanced policy - This policy applies Shield Advanced protection to specified accounts and resources.     Security Groups policy - This type of policy gives you control over security groups that are in use throughout your organization in Organizations and lets you enforce a baseline set of rules across your organization.     Network ACL policy - This type of policy gives you control over the network ACLs that are in use throughout your organization in Organizations and lets you enforce a baseline set of first and last network ACL rules across your organization.     Network Firewall policy - This policy applies Network Firewall protection to your organization's VPCs.     DNS Firewall policy - This policy applies Amazon Route 53 Resolver DNS Firewall protections to your organization's VPCs.     Third-party firewall policy - This policy applies third-party firewall protections. Third-party firewalls are available by subscription through the Amazon Web Services Marketplace console at Amazon Web Services Marketplace.    Palo Alto Networks Cloud NGFW policy - This policy applies Palo Alto Networks Cloud Next Generation Firewall (NGFW) protections and Palo Alto Networks Cloud NGFW rulestacks to your organization's VPCs.    Fortigate CNF policy - This policy applies Fortigate Cloud Native Firewall (CNF) protections. Fortigate CNF is a cloud-centered solution that blocks Zero-Day threats and secures cloud infrastructures with industry-leading advanced threat prevention, smart web application firewalls (WAF), and API protection. |
| POST | / | Creates an Firewall Manager protocols list. |
| POST | / | Creates the resource set. An Firewall Manager resource set defines the resources to import into an Firewall Manager policy from another Amazon Web Services service. |
| POST | / | Adds one or more tags to an Amazon Web Services resource. |
| POST | / | Removes one or more tags from an Amazon Web Services resource. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
