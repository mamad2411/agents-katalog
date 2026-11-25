---
name: elastic-load-balancing
description: "Elastic Load Balancing API skill. Use when working with Elastic Load Balancing for root. Covers 48 endpoints."
version: 1.0.0
generator: lapsh
---

# Elastic Load Balancing
API version: 2015-12-01

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST / -- create first resource

## Endpoints

48 endpoints across 1 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| POST | / | Adds the specified SSL server certificate to the certificate list for the specified HTTPS or TLS listener. If the certificate in already in the certificate list, the call is successful but the certificate is not added again. For more information, see HTTPS listeners in the Application Load Balancers Guide or TLS listeners in the Network Load Balancers Guide. |
| POST | / | Adds the specified tags to the specified Elastic Load Balancing resource. You can tag your Application Load Balancers, Network Load Balancers, Gateway Load Balancers, target groups, trust stores, listeners, and rules. Each tag consists of a key and an optional value. If a resource already has a tag with the same key, AddTags updates its value. |
| POST | / | Adds the specified revocation file to the specified trust store. |
| POST | / | Creates a listener for the specified Application Load Balancer, Network Load Balancer, or Gateway Load Balancer. For more information, see the following:    Listeners for your Application Load Balancers     Listeners for your Network Load Balancers     Listeners for your Gateway Load Balancers    This operation is idempotent, which means that it completes at most one time. If you attempt to create multiple listeners with the same settings, each call succeeds. |
| POST | / | Creates an Application Load Balancer, Network Load Balancer, or Gateway Load Balancer. For more information, see the following:    Application Load Balancers     Network Load Balancers     Gateway Load Balancers    This operation is idempotent, which means that it completes at most one time. If you attempt to create multiple load balancers with the same settings, each call succeeds. |
| POST | / | Creates a rule for the specified listener. The listener must be associated with an Application Load Balancer. Each rule consists of a priority, one or more actions, and one or more conditions. Rules are evaluated in priority order, from the lowest value to the highest value. When the conditions for a rule are met, its actions are performed. If the conditions for no rules are met, the actions for the default rule are performed. For more information, see Listener rules in the Application Load Balancers Guide. |
| POST | / | Creates a target group. For more information, see the following:    Target groups for your Application Load Balancers     Target groups for your Network Load Balancers     Target groups for your Gateway Load Balancers    This operation is idempotent, which means that it completes at most one time. If you attempt to create multiple target groups with the same settings, each call succeeds. |
| POST | / | Creates a trust store. |
| POST | / | Deletes the specified listener. Alternatively, your listener is deleted when you delete the load balancer to which it is attached. |
| POST | / | Deletes the specified Application Load Balancer, Network Load Balancer, or Gateway Load Balancer. Deleting a load balancer also deletes its listeners. You can't delete a load balancer if deletion protection is enabled. If the load balancer does not exist or has already been deleted, the call succeeds. Deleting a load balancer does not affect its registered targets. For example, your EC2 instances continue to run and are still registered to their target groups. If you no longer need these EC2 instances, you can stop or terminate them. |
| POST | / | Deletes the specified rule. You can't delete the default rule. |
| POST | / | Deletes a shared trust store association. |
| POST | / | Deletes the specified target group. You can delete a target group if it is not referenced by any actions. Deleting a target group also deletes any associated health checks. Deleting a target group does not affect its registered targets. For example, any EC2 instances continue to run until you stop or terminate them. |
| POST | / | Deletes a trust store. |
| POST | / | Deregisters the specified targets from the specified target group. After the targets are deregistered, they no longer receive traffic from the load balancer. The load balancer stops sending requests to targets that are deregistering, but uses connection draining to ensure that in-flight traffic completes on the existing connections. This deregistration delay is configured by default but can be updated for each target group. For more information, see the following:     Deregistration delay in the Application Load Balancers User Guide      Deregistration delay in the Network Load Balancers User Guide      Deregistration delay in the Gateway Load Balancers User Guide    Note: If the specified target does not exist, the action returns successfully. |
| POST | / | Describes the current Elastic Load Balancing resource limits for your Amazon Web Services account. For more information, see the following:    Quotas for your Application Load Balancers     Quotas for your Network Load Balancers     Quotas for your Gateway Load Balancers |
| POST | / | Describes the attributes for the specified listener. |
| POST | / | Describes the default certificate and the certificate list for the specified HTTPS or TLS listener. If the default certificate is also in the certificate list, it appears twice in the results (once with IsDefault set to true and once with IsDefault set to false). For more information, see SSL certificates in the Application Load Balancers Guide or Server certificates in the Network Load Balancers Guide. |
| POST | / | Describes the specified listeners or the listeners for the specified Application Load Balancer, Network Load Balancer, or Gateway Load Balancer. You must specify either a load balancer or one or more listeners. |
| POST | / | Describes the attributes for the specified Application Load Balancer, Network Load Balancer, or Gateway Load Balancer. For more information, see the following:    Load balancer attributes in the Application Load Balancers Guide     Load balancer attributes in the Network Load Balancers Guide     Load balancer attributes in the Gateway Load Balancers Guide |
| POST | / | Describes the specified load balancers or all of your load balancers. |
| POST | / | Describes the specified rules or the rules for the specified listener. You must specify either a listener or one or more rules. |
| POST | / | Describes the specified policies or all policies used for SSL negotiation. For more information, see Security policies in the Application Load Balancers Guide or Security policies in the Network Load Balancers Guide. |
| POST | / | Describes the tags for the specified Elastic Load Balancing resources. You can describe the tags for one or more Application Load Balancers, Network Load Balancers, Gateway Load Balancers, target groups, listeners, or rules. |
| POST | / | Describes the attributes for the specified target group. For more information, see the following:    Target group attributes in the Application Load Balancers Guide     Target group attributes in the Network Load Balancers Guide     Target group attributes in the Gateway Load Balancers Guide |
| POST | / | Describes the specified target groups or all of your target groups. By default, all target groups are described. Alternatively, you can specify one of the following to filter the results: the ARN of the load balancer, the names of one or more target groups, or the ARNs of one or more target groups. |
| POST | / | Describes the health of the specified targets or all of your targets. |
| POST | / | Describes all resources associated with the specified trust store. |
| POST | / | Describes the revocation files in use by the specified trust store or revocation files. |
| POST | / | Describes all trust stores for the specified account. |
| POST | / | Retrieves the resource policy for a specified resource. |
| POST | / | Retrieves the ca certificate bundle. This action returns a pre-signed S3 URI which is active for ten minutes. |
| POST | / | Retrieves the specified revocation file. This action returns a pre-signed S3 URI which is active for ten minutes. |
| POST | / | Replaces the specified properties of the specified listener. Any properties that you do not specify remain unchanged. Changing the protocol from HTTPS to HTTP, or from TLS to TCP, removes the security policy and default certificate properties. If you change the protocol from HTTP to HTTPS, or from TCP to TLS, you must add the security policy and default certificate properties. To add an item to a list, remove an item from a list, or update an item in a list, you must provide the entire list. For example, to add an action, specify a list with the current actions plus the new action. |
| POST | / | Modifies the specified attributes of the specified listener. |
| POST | / | Modifies the specified attributes of the specified Application Load Balancer, Network Load Balancer, or Gateway Load Balancer. If any of the specified attributes can't be modified as requested, the call fails. Any existing attributes that you do not modify retain their current values. |
| POST | / | Replaces the specified properties of the specified rule. Any properties that you do not specify are unchanged. To add an item to a list, remove an item from a list, or update an item in a list, you must provide the entire list. For example, to add an action, specify a list with the current actions plus the new action. |
| POST | / | Modifies the health checks used when evaluating the health state of the targets in the specified target group. |
| POST | / | Modifies the specified attributes of the specified target group. |
| POST | / | Update the ca certificate bundle for the specified trust store. |
| POST | / | Registers the specified targets with the specified target group. If the target is an EC2 instance, it must be in the running state when you register it. By default, the load balancer routes requests to registered targets using the protocol and port for the target group. Alternatively, you can override the port for a target when you register it. You can register each EC2 instance or IP address with the same target group multiple times using different ports. With a Network Load Balancer, you cannot register instances by instance ID if they have the following instance types: C1, CC1, CC2, CG1, CG2, CR1, CS1, G1, G2, HI1, HS1, M1, M2, M3, and T1. You can register instances of these types by IP address. |
| POST | / | Removes the specified certificate from the certificate list for the specified HTTPS or TLS listener. |
| POST | / | Removes the specified tags from the specified Elastic Load Balancing resources. You can remove the tags for one or more Application Load Balancers, Network Load Balancers, Gateway Load Balancers, target groups, listeners, or rules. |
| POST | / | Removes the specified revocation file from the specified trust store. |
| POST | / | Sets the type of IP addresses used by the subnets of the specified load balancer. |
| POST | / | Sets the priorities of the specified rules. You can reorder the rules as long as there are no priority conflicts in the new order. Any existing rules that you do not specify retain their current priority. |
| POST | / | Associates the specified security groups with the specified Application Load Balancer or Network Load Balancer. The specified security groups override the previously associated security groups. You can't perform this operation on a Network Load Balancer unless you specified a security group for the load balancer when you created it. You can't associate a security group with a Gateway Load Balancer. |
| POST | / | Enables the Availability Zones for the specified public subnets for the specified Application Load Balancer, Network Load Balancer or Gateway Load Balancer. The specified subnets replace the previously enabled subnets. When you specify subnets for a Network Load Balancer, or Gateway Load Balancer you must include all subnets that were enabled previously, with their existing configurations, plus any additional subnets. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
