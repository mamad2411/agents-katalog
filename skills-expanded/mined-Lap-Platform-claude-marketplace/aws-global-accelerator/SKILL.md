---
name: aws-global-accelerator
description: "AWS Global Accelerator API skill. Use when working with AWS Global Accelerator for root. Covers 56 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS Global Accelerator
API version: 2018-08-08

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST / -- create first resource

## Endpoints

56 endpoints across 1 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| POST | / | Associate a virtual private cloud (VPC) subnet endpoint with your custom routing accelerator. The listener port range must be large enough to support the number of IP addresses that can be specified in your subnet. The number of ports required is: subnet size times the number of ports per destination EC2 instances. For example, a subnet defined as /24 requires a listener port range of at least 255 ports.  Note: You must have enough remaining listener ports available to map to the subnet ports, or the call will fail with a LimitExceededException. By default, all destinations in a subnet in a custom routing accelerator cannot receive traffic. To enable all destinations to receive traffic, or to specify individual port mappings that can receive traffic, see the  AllowCustomRoutingTraffic operation. |
| POST | / | Add endpoints to an endpoint group. The AddEndpoints API operation is the recommended option for adding endpoints. The alternative options are to add endpoints when you create an endpoint group (with the CreateEndpointGroup API) or when you update an endpoint group (with the UpdateEndpointGroup API).  There are two advantages to using AddEndpoints to add endpoints in Global Accelerator:   It's faster, because Global Accelerator only has to resolve the new endpoints that you're adding, rather than resolving new and existing endpoints.   It's more convenient, because you don't need to specify the current endpoints that are already in the endpoint group, in addition to the new endpoints that you want to add.   For information about endpoint types and requirements for endpoints that you can add to Global Accelerator, see  Endpoints for standard accelerators in the Global Accelerator Developer Guide. |
| POST | / | Advertises an IPv4 address range that is provisioned for use with your Amazon Web Services resources through bring your own IP addresses (BYOIP). It can take a few minutes before traffic to the specified addresses starts routing to Amazon Web Services because of propagation delays.  To stop advertising the BYOIP address range, use  WithdrawByoipCidr. For more information, see Bring your own IP addresses (BYOIP) in the Global Accelerator Developer Guide. |
| POST | / | Specify the Amazon EC2 instance (destination) IP addresses and ports for a VPC subnet endpoint that can receive traffic for a custom routing accelerator. You can allow traffic to all destinations in the subnet endpoint, or allow traffic to a specified list of destination IP addresses and ports in the subnet. Note that you cannot specify IP addresses or ports outside of the range that you configured for the endpoint group. After you make changes, you can verify that the updates are complete by checking the status of your accelerator: the status changes from IN_PROGRESS to DEPLOYED. |
| POST | / | Create an accelerator. An accelerator includes one or more listeners that process inbound connections and direct traffic to one or more endpoint groups, each of which includes endpoints, such as Network Load Balancers.   Global Accelerator is a global service that supports endpoints in multiple Amazon Web Services Regions but you must specify the US West (Oregon) Region to create, update, or otherwise work with accelerators. That is, for example, specify --region us-west-2 on Amazon Web Services CLI commands. |
| POST | / | Create a cross-account attachment in Global Accelerator. You create a cross-account attachment to specify the principals who have permission to work with resources in accelerators in their own account. You specify, in the same attachment, the resources that are shared. A principal can be an Amazon Web Services account number or the Amazon Resource Name (ARN) for an accelerator. For account numbers that are listed as principals, to work with a resource listed in the attachment, you must sign in to an account specified as a principal. Then, you can work with resources that are listed, with any of your accelerators. If an accelerator ARN is listed in the cross-account attachment as a principal, anyone with permission to make updates to the accelerator can work with resources that are listed in the attachment.  Specify each principal and resource separately. To specify two CIDR address pools, list them individually under Resources, and so on. For a command line operation, for example, you might use a statement like the following:   "Resources": [{"Cidr": "169.254.60.0/24"},{"Cidr": "169.254.59.0/24"}]  For more information, see  Working with cross-account attachments and resources in Global Accelerator in the  Global Accelerator Developer Guide. |
| POST | / | Create a custom routing accelerator. A custom routing accelerator directs traffic to one of possibly thousands of Amazon EC2 instance destinations running in a single or multiple virtual private clouds (VPC) subnet endpoints. Be aware that, by default, all destination EC2 instances in a VPC subnet endpoint cannot receive traffic. To enable all destinations to receive traffic, or to specify individual port mappings that can receive traffic, see the  AllowCustomRoutingTraffic operation.  Global Accelerator is a global service that supports endpoints in multiple Amazon Web Services Regions but you must specify the US West (Oregon) Region to create, update, or otherwise work with accelerators. That is, for example, specify --region us-west-2 on Amazon Web Services CLI commands. |
| POST | / | Create an endpoint group for the specified listener for a custom routing accelerator. An endpoint group is a collection of endpoints in one Amazon Web Services Region. |
| POST | / | Create a listener to process inbound connections from clients to a custom routing accelerator. Connections arrive to assigned static IP addresses on the port range that you specify. |
| POST | / | Create an endpoint group for the specified listener. An endpoint group is a collection of endpoints in one Amazon Web Services Region. A resource must be valid and active when you add it as an endpoint. For more information about endpoint types and requirements for endpoints that you can add to Global Accelerator, see  Endpoints for standard accelerators in the Global Accelerator Developer Guide. |
| POST | / | Create a listener to process inbound connections from clients to an accelerator. Connections arrive to assigned static IP addresses on a port, port range, or list of port ranges that you specify. |
| POST | / | Delete an accelerator. Before you can delete an accelerator, you must disable it and remove all dependent resources (listeners and endpoint groups). To disable the accelerator, update the accelerator to set Enabled to false.  When you create an accelerator, by default, Global Accelerator provides you with a set of two static IP addresses. Alternatively, you can bring your own IP address ranges to Global Accelerator and assign IP addresses from those ranges.  The IP addresses are assigned to your accelerator for as long as it exists, even if you disable the accelerator and it no longer accepts or routes traffic. However, when you delete an accelerator, you lose the static IP addresses that are assigned to the accelerator, so you can no longer route traffic by using them. As a best practice, ensure that you have permissions in place to avoid inadvertently deleting accelerators. You can use IAM policies with Global Accelerator to limit the users who have permissions to delete an accelerator. For more information, see Identity and access management in the Global Accelerator Developer Guide. |
| POST | / | Delete a cross-account attachment. When you delete an attachment, Global Accelerator revokes the permission to use the resources in the attachment from all principals in the list of principals. Global Accelerator revokes the permission for specific resources. For more information, see  Working with cross-account attachments and resources in Global Accelerator in the  Global Accelerator Developer Guide. |
| POST | / | Delete a custom routing accelerator. Before you can delete an accelerator, you must disable it and remove all dependent resources (listeners and endpoint groups). To disable the accelerator, update the accelerator to set Enabled to false.  When you create a custom routing accelerator, by default, Global Accelerator provides you with a set of two static IP addresses.  The IP addresses are assigned to your accelerator for as long as it exists, even if you disable the accelerator and it no longer accepts or routes traffic. However, when you delete an accelerator, you lose the static IP addresses that are assigned to the accelerator, so you can no longer route traffic by using them. As a best practice, ensure that you have permissions in place to avoid inadvertently deleting accelerators. You can use IAM policies with Global Accelerator to limit the users who have permissions to delete an accelerator. For more information, see Identity and access management in the Global Accelerator Developer Guide. |
| POST | / | Delete an endpoint group from a listener for a custom routing accelerator. |
| POST | / | Delete a listener for a custom routing accelerator. |
| POST | / | Delete an endpoint group from a listener. |
| POST | / | Delete a listener from an accelerator. |
| POST | / | Specify the Amazon EC2 instance (destination) IP addresses and ports for a VPC subnet endpoint that cannot receive traffic for a custom routing accelerator. You can deny traffic to all destinations in the VPC endpoint, or deny traffic to a specified list of destination IP addresses and ports. Note that you cannot specify IP addresses or ports outside of the range that you configured for the endpoint group. After you make changes, you can verify that the updates are complete by checking the status of your accelerator: the status changes from IN_PROGRESS to DEPLOYED. |
| POST | / | Releases the specified address range that you provisioned to use with your Amazon Web Services resources through bring your own IP addresses (BYOIP) and deletes the corresponding address pool.  Before you can release an address range, you must stop advertising it by using WithdrawByoipCidr and you must not have any accelerators that are using static IP addresses allocated from its address range.  For more information, see Bring your own IP addresses (BYOIP) in the Global Accelerator Developer Guide. |
| POST | / | Describe an accelerator. |
| POST | / | Describe the attributes of an accelerator. |
| POST | / | Gets configuration information about a cross-account attachment. |
| POST | / | Describe a custom routing accelerator. |
| POST | / | Describe the attributes of a custom routing accelerator. |
| POST | / | Describe an endpoint group for a custom routing accelerator. |
| POST | / | The description of a listener for a custom routing accelerator. |
| POST | / | Describe an endpoint group. |
| POST | / | Describe a listener. |
| POST | / | List the accelerators for an Amazon Web Services account. |
| POST | / | Lists the IP address ranges that were specified in calls to ProvisionByoipCidr, including the current state and a history of state changes. |
| POST | / | List the cross-account attachments that have been created in Global Accelerator. |
| POST | / | List the accounts that have cross-account resources. For more information, see  Working with cross-account attachments and resources in Global Accelerator in the  Global Accelerator Developer Guide. |
| POST | / | List the cross-account resources available to work with. |
| POST | / | List the custom routing accelerators for an Amazon Web Services account. |
| POST | / | List the endpoint groups that are associated with a listener for a custom routing accelerator. |
| POST | / | List the listeners for a custom routing accelerator. |
| POST | / | Provides a complete mapping from the public accelerator IP address and port to destination EC2 instance IP addresses and ports in the virtual public cloud (VPC) subnet endpoint for a custom routing accelerator. For each subnet endpoint that you add, Global Accelerator creates a new static port mapping for the accelerator. The port mappings don't change after Global Accelerator generates them, so you can retrieve and cache the full mapping on your servers.  If you remove a subnet from your accelerator, Global Accelerator removes (reclaims) the port mappings. If you add a subnet to your accelerator, Global Accelerator creates new port mappings (the existing ones don't change). If you add or remove EC2 instances in your subnet, the port mappings don't change, because the mappings are created when you add the subnet to Global Accelerator. The mappings also include a flag for each destination denoting which destination IP addresses and ports are allowed or denied traffic. |
| POST | / | List the port mappings for a specific EC2 instance (destination) in a VPC subnet endpoint. The response is the mappings for one destination IP address. This is useful when your subnet endpoint has mappings that span multiple custom routing accelerators in your account, or for scenarios where you only want to list the port mappings for a specific destination instance. |
| POST | / | List the endpoint groups that are associated with a listener. |
| POST | / | List the listeners for an accelerator. |
| POST | / | List all tags for an accelerator.  For more information, see Tagging in Global Accelerator in the Global Accelerator Developer Guide. |
| POST | / | Provisions an IP address range to use with your Amazon Web Services resources through bring your own IP addresses (BYOIP) and creates a corresponding address pool. After the address range is provisioned, it is ready to be advertised using  AdvertiseByoipCidr. For more information, see Bring your own IP addresses (BYOIP) in the Global Accelerator Developer Guide. |
| POST | / | Remove endpoints from a custom routing accelerator. |
| POST | / | Remove endpoints from an endpoint group.  The RemoveEndpoints API operation is the recommended option for removing endpoints. The alternative is to remove endpoints by updating an endpoint group by using the UpdateEndpointGroup API operation. There are two advantages to using AddEndpoints to remove endpoints instead:   It's more convenient, because you only need to specify the endpoints that you want to remove. With the UpdateEndpointGroup API operation, you must specify all of the endpoints in the endpoint group except the ones that you want to remove from the group.   It's faster, because Global Accelerator doesn't need to resolve any endpoints. With the UpdateEndpointGroup API operation, Global Accelerator must resolve all of the endpoints that remain in the group. |
| POST | / | Add tags to an accelerator resource.  For more information, see Tagging in Global Accelerator in the Global Accelerator Developer Guide. |
| POST | / | Remove tags from a Global Accelerator resource. When you specify a tag key, the action removes both that key and its associated value. The operation succeeds even if you attempt to remove tags from an accelerator that was already removed. For more information, see Tagging in Global Accelerator in the Global Accelerator Developer Guide. |
| POST | / | Update an accelerator to make changes, such as the following:    Change the name of the accelerator.   Disable the accelerator so that it no longer accepts or routes traffic, or so that you can delete it.   Enable the accelerator, if it is disabled.   Change the IP address type to dual-stack if it is IPv4, or change the IP address type to IPv4 if it's dual-stack.   Be aware that static IP addresses remain assigned to your accelerator for as long as it exists, even if you disable the accelerator and it no longer accepts or routes traffic. However, when you delete the accelerator, you lose the static IP addresses that are assigned to it, so you can no longer route traffic by using them.  Global Accelerator is a global service that supports endpoints in multiple Amazon Web Services Regions but you must specify the US West (Oregon) Region to create, update, or otherwise work with accelerators. That is, for example, specify --region us-west-2 on Amazon Web Services CLI commands. |
| POST | / | Update the attributes for an accelerator. |
| POST | / | Update a cross-account attachment to add or remove principals or resources. When you update an attachment to remove a principal (account ID or accelerator) or a resource, Global Accelerator revokes the permission for specific resources.  For more information, see  Working with cross-account attachments and resources in Global Accelerator in the  Global Accelerator Developer Guide. |
| POST | / | Update a custom routing accelerator. |
| POST | / | Update the attributes for a custom routing accelerator. |
| POST | / | Update a listener for a custom routing accelerator. |
| POST | / | Update an endpoint group. A resource must be valid and active when you add it as an endpoint. |
| POST | / | Update a listener. |
| POST | / | Stops advertising an address range that is provisioned as an address pool. You can perform this operation at most once every 10 seconds, even if you specify different address ranges each time. It can take a few minutes before traffic to the specified addresses stops routing to Amazon Web Services because of propagation delays. For more information, see Bring your own IP addresses (BYOIP) in the Global Accelerator Developer Guide. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
