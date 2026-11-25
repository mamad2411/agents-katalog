---
name: aws-network-firewall
description: "AWS Network Firewall API skill. Use when working with AWS Network Firewall for root. Covers 36 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS Network Firewall
API version: 2020-11-12

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST / -- create first resource

## Endpoints

36 endpoints across 1 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| POST | / | Associates a FirewallPolicy to a Firewall.  A firewall policy defines how to monitor and manage your VPC network traffic, using a collection of inspection rule groups and other settings. Each firewall requires one firewall policy association, and you can use the same firewall policy for multiple firewalls. |
| POST | / | Associates the specified subnets in the Amazon VPC to the firewall. You can specify one subnet for each of the Availability Zones that the VPC spans.  This request creates an Network Firewall firewall endpoint in each of the subnets. To enable the firewall's protections, you must also modify the VPC's route tables for each subnet's Availability Zone, to redirect the traffic that's coming into and going out of the zone through the firewall endpoint. |
| POST | / | Creates an Network Firewall Firewall and accompanying FirewallStatus for a VPC.  The firewall defines the configuration settings for an Network Firewall firewall. The settings that you can define at creation include the firewall policy, the subnets in your VPC to use for the firewall endpoints, and any tags that are attached to the firewall Amazon Web Services resource.  After you create a firewall, you can provide additional settings, like the logging configuration.  To update the settings for a firewall, you use the operations that apply to the settings themselves, for example UpdateLoggingConfiguration, AssociateSubnets, and UpdateFirewallDeleteProtection.  To manage a firewall's tags, use the standard Amazon Web Services resource tagging operations, ListTagsForResource, TagResource, and UntagResource. To retrieve information about firewalls, use ListFirewalls and DescribeFirewall. |
| POST | / | Creates the firewall policy for the firewall according to the specifications.  An Network Firewall firewall policy defines the behavior of a firewall, in a collection of stateless and stateful rule groups and other settings. You can use one firewall policy for multiple firewalls. |
| POST | / | Creates the specified stateless or stateful rule group, which includes the rules for network traffic inspection, a capacity setting, and tags.  You provide your rule group specification in your request using either RuleGroup or Rules. |
| POST | / | Creates an Network Firewall TLS inspection configuration. Network Firewall uses TLS inspection configurations to decrypt your firewall's inbound and outbound SSL/TLS traffic. After decryption, Network Firewall inspects the traffic according to your firewall policy's stateful rules, and then re-encrypts it before sending it to its destination. You can enable inspection of your firewall's inbound traffic, outbound traffic, or both. To use TLS inspection with your firewall, you must first import or provision certificates using ACM, create a TLS inspection configuration, add that configuration to a new firewall policy, and then associate that policy with your firewall. To update the settings for a TLS inspection configuration, use UpdateTLSInspectionConfiguration. To manage a TLS inspection configuration's tags, use the standard Amazon Web Services resource tagging operations, ListTagsForResource, TagResource, and UntagResource. To retrieve information about TLS inspection configurations, use ListTLSInspectionConfigurations and DescribeTLSInspectionConfiguration.  For more information about TLS inspection configurations, see Inspecting SSL/TLS traffic with TLS inspection configurations in the Network Firewall Developer Guide. |
| POST | / | Deletes the specified Firewall and its FirewallStatus. This operation requires the firewall's DeleteProtection flag to be FALSE. You can't revert this operation.  You can check whether a firewall is in use by reviewing the route tables for the Availability Zones where you have firewall subnet mappings. Retrieve the subnet mappings by calling DescribeFirewall. You define and update the route tables through Amazon VPC. As needed, update the route tables for the zones to remove the firewall endpoints. When the route tables no longer use the firewall endpoints, you can remove the firewall safely. To delete a firewall, remove the delete protection if you need to using UpdateFirewallDeleteProtection, then delete the firewall by calling DeleteFirewall. |
| POST | / | Deletes the specified FirewallPolicy. |
| POST | / | Deletes a resource policy that you created in a PutResourcePolicy request. |
| POST | / | Deletes the specified RuleGroup. |
| POST | / | Deletes the specified TLSInspectionConfiguration. |
| POST | / | Returns the data objects for the specified firewall. |
| POST | / | Returns the data objects for the specified firewall policy. |
| POST | / | Returns the logging configuration for the specified firewall. |
| POST | / | Retrieves a resource policy that you created in a PutResourcePolicy request. |
| POST | / | Returns the data objects for the specified rule group. |
| POST | / | High-level information about a rule group, returned by operations like create and describe. You can use the information provided in the metadata to retrieve and manage a rule group. You can retrieve all objects for a rule group by calling DescribeRuleGroup. |
| POST | / | Returns the data objects for the specified TLS inspection configuration. |
| POST | / | Removes the specified subnet associations from the firewall. This removes the firewall endpoints from the subnets and removes any network filtering protections that the endpoints were providing. |
| POST | / | Retrieves the metadata for the firewall policies that you have defined. Depending on your setting for max results and the number of firewall policies, a single call might not return the full list. |
| POST | / | Retrieves the metadata for the firewalls that you have defined. If you provide VPC identifiers in your request, this returns only the firewalls for those VPCs. Depending on your setting for max results and the number of firewalls, a single call might not return the full list. |
| POST | / | Retrieves the metadata for the rule groups that you have defined. Depending on your setting for max results and the number of rule groups, a single call might not return the full list. |
| POST | / | Retrieves the metadata for the TLS inspection configurations that you have defined. Depending on your setting for max results and the number of TLS inspection configurations, a single call might not return the full list. |
| POST | / | Retrieves the tags associated with the specified resource. Tags are key:value pairs that you can use to categorize and manage your resources, for purposes like billing. For example, you might set the tag key to "customer" and the value to the customer name or ID. You can specify one or more tags to add to each Amazon Web Services resource, up to 50 tags for a resource. You can tag the Amazon Web Services resources that you manage through Network Firewall: firewalls, firewall policies, and rule groups. |
| POST | / | Creates or updates an IAM policy for your rule group or firewall policy. Use this to share rule groups and firewall policies between accounts. This operation works in conjunction with the Amazon Web Services Resource Access Manager (RAM) service to manage resource sharing for Network Firewall.  Use this operation to create or update a resource policy for your rule group or firewall policy. In the policy, you specify the accounts that you want to share the resource with and the operations that you want the accounts to be able to perform.  When you add an account in the resource policy, you then run the following Resource Access Manager (RAM) operations to access and accept the shared rule group or firewall policy.     GetResourceShareInvitations - Returns the Amazon Resource Names (ARNs) of the resource share invitations.     AcceptResourceShareInvitation - Accepts the share invitation for a specified resource share.    For additional information about resource sharing using RAM, see Resource Access Manager User Guide. |
| POST | / | Adds the specified tags to the specified resource. Tags are key:value pairs that you can use to categorize and manage your resources, for purposes like billing. For example, you might set the tag key to "customer" and the value to the customer name or ID. You can specify one or more tags to add to each Amazon Web Services resource, up to 50 tags for a resource. You can tag the Amazon Web Services resources that you manage through Network Firewall: firewalls, firewall policies, and rule groups. |
| POST | / | Removes the tags with the specified keys from the specified resource. Tags are key:value pairs that you can use to categorize and manage your resources, for purposes like billing. For example, you might set the tag key to "customer" and the value to the customer name or ID. You can specify one or more tags to add to each Amazon Web Services resource, up to 50 tags for a resource. You can manage tags for the Amazon Web Services resources that you manage through Network Firewall: firewalls, firewall policies, and rule groups. |
| POST | / | Modifies the flag, DeleteProtection, which indicates whether it is possible to delete the firewall. If the flag is set to TRUE, the firewall is protected against deletion. This setting helps protect against accidentally deleting a firewall that's in use. |
| POST | / | Modifies the description for the specified firewall. Use the description to help you identify the firewall when you're working with it. |
| POST | / | A complex type that contains settings for encryption of your firewall resources. |
| POST | / | Updates the properties of the specified firewall policy. |
| POST | / | Modifies the flag, ChangeProtection, which indicates whether it is possible to change the firewall. If the flag is set to TRUE, the firewall is protected from changes. This setting helps protect against accidentally changing a firewall that's in use. |
| POST | / | Sets the logging configuration for the specified firewall.  To change the logging configuration, retrieve the LoggingConfiguration by calling DescribeLoggingConfiguration, then change it and provide the modified object to this update call. You must change the logging configuration one LogDestinationConfig at a time inside the retrieved LoggingConfiguration object.  You can perform only one of the following actions in any call to UpdateLoggingConfiguration:    Create a new log destination object by adding a single LogDestinationConfig array element to LogDestinationConfigs.   Delete a log destination object by removing a single LogDestinationConfig array element from LogDestinationConfigs.   Change the LogDestination setting in a single LogDestinationConfig array element.   You can't change the LogDestinationType or LogType in a LogDestinationConfig. To change these settings, delete the existing LogDestinationConfig object and create a new one, using two separate calls to this update operation. |
| POST | / | Updates the rule settings for the specified rule group. You use a rule group by reference in one or more firewall policies. When you modify a rule group, you modify all firewall policies that use the rule group.  To update a rule group, first call DescribeRuleGroup to retrieve the current RuleGroup object, update the object as needed, and then provide the updated object to this call. |
| POST | / |  |
| POST | / | Updates the TLS inspection configuration settings for the specified TLS inspection configuration. You use a TLS inspection configuration by referencing it in one or more firewall policies. When you modify a TLS inspection configuration, you modify all firewall policies that use the TLS inspection configuration.  To update a TLS inspection configuration, first call DescribeTLSInspectionConfiguration to retrieve the current TLSInspectionConfiguration object, update the object as needed, and then provide the updated object to this call. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
