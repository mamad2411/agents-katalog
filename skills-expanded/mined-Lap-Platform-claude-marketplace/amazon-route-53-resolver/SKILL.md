---
name: amazon-route-53-resolver
description: "Amazon Route 53 Resolver API skill. Use when working with Amazon Route 53 Resolver for root. Covers 68 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon Route 53 Resolver
API version: 2018-04-01

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST / -- create first resource

## Endpoints

68 endpoints across 1 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| POST | / | Associates a FirewallRuleGroup with a VPC, to provide DNS filtering for the VPC. |
| POST | / | Adds IP addresses to an inbound or an outbound Resolver endpoint. If you want to add more than one IP address, submit one AssociateResolverEndpointIpAddress request for each IP address. To remove an IP address from an endpoint, see DisassociateResolverEndpointIpAddress. |
| POST | / | Associates an Amazon VPC with a specified query logging configuration. Route 53 Resolver logs DNS queries that originate in all of the Amazon VPCs that are associated with a specified query logging configuration. To associate more than one VPC with a configuration, submit one AssociateResolverQueryLogConfig request for each VPC.  The VPCs that you associate with a query logging configuration must be in the same Region as the configuration.  To remove a VPC from a query logging configuration, see DisassociateResolverQueryLogConfig. |
| POST | / | Associates a Resolver rule with a VPC. When you associate a rule with a VPC, Resolver forwards all DNS queries for the domain name that is specified in the rule and that originate in the VPC. The queries are forwarded to the IP addresses for the DNS resolvers that are specified in the rule. For more information about rules, see CreateResolverRule. |
| POST | / | Creates an empty firewall domain list for use in DNS Firewall rules. You can populate the domains for the new list with a file, using ImportFirewallDomains, or with domain strings, using UpdateFirewallDomains. |
| POST | / | Creates a single DNS Firewall rule in the specified rule group, using the specified domain list. |
| POST | / | Creates an empty DNS Firewall rule group for filtering DNS network traffic in a VPC. You can add rules to the new rule group by calling CreateFirewallRule. |
| POST | / | Creates a Route 53 Resolver on an Outpost. |
| POST | / | Creates a Resolver endpoint. There are two types of Resolver endpoints, inbound and outbound:   An inbound Resolver endpoint forwards DNS queries to the DNS service for a VPC from your network.   An outbound Resolver endpoint forwards DNS queries from the DNS service for a VPC to your network. |
| POST | / | Creates a Resolver query logging configuration, which defines where you want Resolver to save DNS query logs that originate in your VPCs. Resolver can log queries only for VPCs that are in the same Region as the query logging configuration. To specify which VPCs you want to log queries for, you use AssociateResolverQueryLogConfig. For more information, see AssociateResolverQueryLogConfig.  You can optionally use Resource Access Manager (RAM) to share a query logging configuration with other Amazon Web Services accounts. The other accounts can then associate VPCs with the configuration. The query logs that Resolver creates for a configuration include all DNS queries that originate in all VPCs that are associated with the configuration. |
| POST | / | For DNS queries that originate in your VPCs, specifies which Resolver endpoint the queries pass through, one domain name that you want to forward to your network, and the IP addresses of the DNS resolvers in your network. |
| POST | / | Deletes the specified domain list. |
| POST | / | Deletes the specified firewall rule. |
| POST | / | Deletes the specified firewall rule group. |
| POST | / | Deletes a Resolver on the Outpost. |
| POST | / | Deletes a Resolver endpoint. The effect of deleting a Resolver endpoint depends on whether it's an inbound or an outbound Resolver endpoint:    Inbound: DNS queries from your network are no longer routed to the DNS service for the specified VPC.    Outbound: DNS queries from a VPC are no longer routed to your network. |
| POST | / | Deletes a query logging configuration. When you delete a configuration, Resolver stops logging DNS queries for all of the Amazon VPCs that are associated with the configuration. This also applies if the query logging configuration is shared with other Amazon Web Services accounts, and the other accounts have associated VPCs with the shared configuration. Before you can delete a query logging configuration, you must first disassociate all VPCs from the configuration. See DisassociateResolverQueryLogConfig. If you used Resource Access Manager (RAM) to share a query logging configuration with other accounts, you must stop sharing the configuration before you can delete a configuration. The accounts that you shared the configuration with can first disassociate VPCs that they associated with the configuration, but that's not necessary. If you stop sharing the configuration, those VPCs are automatically disassociated from the configuration. |
| POST | / | Deletes a Resolver rule. Before you can delete a Resolver rule, you must disassociate it from all the VPCs that you associated the Resolver rule with. For more information, see DisassociateResolverRule. |
| POST | / | Disassociates a FirewallRuleGroup from a VPC, to remove DNS filtering from the VPC. |
| POST | / | Removes IP addresses from an inbound or an outbound Resolver endpoint. If you want to remove more than one IP address, submit one DisassociateResolverEndpointIpAddress request for each IP address. To add an IP address to an endpoint, see AssociateResolverEndpointIpAddress. |
| POST | / | Disassociates a VPC from a query logging configuration.  Before you can delete a query logging configuration, you must first disassociate all VPCs from the configuration. If you used Resource Access Manager (RAM) to share a query logging configuration with other accounts, VPCs can be disassociated from the configuration in the following ways:   The accounts that you shared the configuration with can disassociate VPCs from the configuration.   You can stop sharing the configuration. |
| POST | / | Removes the association between a specified Resolver rule and a specified VPC.  If you disassociate a Resolver rule from a VPC, Resolver stops forwarding DNS queries for the domain name that you specified in the Resolver rule. |
| POST | / | Retrieves the configuration of the firewall behavior provided by DNS Firewall for a single VPC from Amazon Virtual Private Cloud (Amazon VPC). |
| POST | / | Retrieves the specified firewall domain list. |
| POST | / | Retrieves the specified firewall rule group. |
| POST | / | Retrieves a firewall rule group association, which enables DNS filtering for a VPC with one rule group. A VPC can have more than one firewall rule group association, and a rule group can be associated with more than one VPC. |
| POST | / | Returns the Identity and Access Management (Amazon Web Services IAM) policy for sharing the specified rule group. You can use the policy to share the rule group using Resource Access Manager (RAM). |
| POST | / | Gets information about a specified Resolver on the Outpost, such as its instance count and type, name, and the current status of the Resolver. |
| POST | / | Retrieves the behavior configuration of Route 53 Resolver behavior for a single VPC from Amazon Virtual Private Cloud. |
| POST | / | Gets DNSSEC validation information for a specified resource. |
| POST | / | Gets information about a specified Resolver endpoint, such as whether it's an inbound or an outbound Resolver endpoint, and the current status of the endpoint. |
| POST | / | Gets information about a specified Resolver query logging configuration, such as the number of VPCs that the configuration is logging queries for and the location that logs are sent to. |
| POST | / | Gets information about a specified association between a Resolver query logging configuration and an Amazon VPC. When you associate a VPC with a query logging configuration, Resolver logs DNS queries that originate in that VPC. |
| POST | / | Gets information about a query logging policy. A query logging policy specifies the Resolver query logging operations and resources that you want to allow another Amazon Web Services account to be able to use. |
| POST | / | Gets information about a specified Resolver rule, such as the domain name that the rule forwards DNS queries for and the ID of the outbound Resolver endpoint that the rule is associated with. |
| POST | / | Gets information about an association between a specified Resolver rule and a VPC. You associate a Resolver rule and a VPC using AssociateResolverRule. |
| POST | / | Gets information about the Resolver rule policy for a specified rule. A Resolver rule policy includes the rule that you want to share with another account, the account that you want to share the rule with, and the Resolver operations that you want to allow the account to use. |
| POST | / | Imports domain names from a file into a domain list, for use in a DNS firewall rule group.  Each domain specification in your domain list must satisfy the following requirements:    It can optionally start with * (asterisk).   With the exception of the optional starting asterisk, it must only contain the following characters: A-Z, a-z, 0-9, - (hyphen).   It must be from 1-255 characters in length. |
| POST | / | Retrieves the firewall configurations that you have defined. DNS Firewall uses the configurations to manage firewall behavior for your VPCs.  A single call might return only a partial list of the configurations. For information, see MaxResults. |
| POST | / | Retrieves the firewall domain lists that you have defined. For each firewall domain list, you can retrieve the domains that are defined for a list by calling ListFirewallDomains.  A single call to this list operation might return only a partial list of the domain lists. For information, see MaxResults. |
| POST | / | Retrieves the domains that you have defined for the specified firewall domain list.  A single call might return only a partial list of the domains. For information, see MaxResults. |
| POST | / | Retrieves the firewall rule group associations that you have defined. Each association enables DNS filtering for a VPC with one rule group.  A single call might return only a partial list of the associations. For information, see MaxResults. |
| POST | / | Retrieves the minimal high-level information for the rule groups that you have defined.  A single call might return only a partial list of the rule groups. For information, see MaxResults. |
| POST | / | Retrieves the firewall rules that you have defined for the specified firewall rule group. DNS Firewall uses the rules in a rule group to filter DNS network traffic for a VPC.  A single call might return only a partial list of the rules. For information, see MaxResults. |
| POST | / | Lists all the Resolvers on Outposts that were created using the current Amazon Web Services account. |
| POST | / | Retrieves the Resolver configurations that you have defined. Route 53 Resolver uses the configurations to manage DNS resolution behavior for your VPCs. |
| POST | / | Lists the configurations for DNSSEC validation that are associated with the current Amazon Web Services account. |
| POST | / | Gets the IP addresses for a specified Resolver endpoint. |
| POST | / | Lists all the Resolver endpoints that were created using the current Amazon Web Services account. |
| POST | / | Lists information about associations between Amazon VPCs and query logging configurations. |
| POST | / | Lists information about the specified query logging configurations. Each configuration defines where you want Resolver to save DNS query logs and specifies the VPCs that you want to log queries for. |
| POST | / | Lists the associations that were created between Resolver rules and VPCs using the current Amazon Web Services account. |
| POST | / | Lists the Resolver rules that were created using the current Amazon Web Services account. |
| POST | / | Lists the tags that you associated with the specified resource. |
| POST | / | Attaches an Identity and Access Management (Amazon Web Services IAM) policy for sharing the rule group. You can use the policy to share the rule group using Resource Access Manager (RAM). |
| POST | / | Specifies an Amazon Web Services account that you want to share a query logging configuration with, the query logging configuration that you want to share, and the operations that you want the account to be able to perform on the configuration. |
| POST | / | Specifies an Amazon Web Services rule that you want to share with another account, the account that you want to share the rule with, and the operations that you want the account to be able to perform on the rule. |
| POST | / | Adds one or more tags to a specified resource. |
| POST | / | Removes one or more tags from a specified resource. |
| POST | / | Updates the configuration of the firewall behavior provided by DNS Firewall for a single VPC from Amazon Virtual Private Cloud (Amazon VPC). |
| POST | / | Updates the firewall domain list from an array of domain specifications. |
| POST | / | Updates the specified firewall rule. |
| POST | / | Changes the association of a FirewallRuleGroup with a VPC. The association enables DNS filtering for the VPC. |
| POST | / | You can use UpdateOutpostResolver to update the instance count, type, or name of a Resolver on an Outpost. |
| POST | / | Updates the behavior configuration of Route 53 Resolver behavior for a single VPC from Amazon Virtual Private Cloud. |
| POST | / | Updates an existing DNSSEC validation configuration. If there is no existing DNSSEC validation configuration, one is created. |
| POST | / | Updates the name, or endpoint type for an inbound or an outbound Resolver endpoint. You can only update between IPV4 and DUALSTACK, IPV6 endpoint type can't be updated to other type. |
| POST | / | Updates settings for a specified Resolver rule. ResolverRuleId is required, and all other parameters are optional. If you don't specify a parameter, it retains its current value. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
