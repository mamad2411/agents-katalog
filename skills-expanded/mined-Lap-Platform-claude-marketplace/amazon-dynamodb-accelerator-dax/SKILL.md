---
name: amazon-dynamodb-accelerator-dax
description: "Amazon DynamoDB Accelerator (DAX) API skill. Use when working with Amazon DynamoDB Accelerator (DAX) for root. Covers 21 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon DynamoDB Accelerator (DAX)
API version: 2017-04-19

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST / -- create first resource

## Endpoints

21 endpoints across 1 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| POST | / | Creates a DAX cluster. All nodes in the cluster run the same DAX caching software. |
| POST | / | Creates a new parameter group. A parameter group is a collection of parameters that you apply to all of the nodes in a DAX cluster. |
| POST | / | Creates a new subnet group. |
| POST | / | Removes one or more nodes from a DAX cluster.  You cannot use DecreaseReplicationFactor to remove the last node in a DAX cluster. If you need to do this, use DeleteCluster instead. |
| POST | / | Deletes a previously provisioned DAX cluster. DeleteCluster deletes all associated nodes, node endpoints and the DAX cluster itself. When you receive a successful response from this action, DAX immediately begins deleting the cluster; you cannot cancel or revert this action. |
| POST | / | Deletes the specified parameter group. You cannot delete a parameter group if it is associated with any DAX clusters. |
| POST | / | Deletes a subnet group.  You cannot delete a subnet group if it is associated with any DAX clusters. |
| POST | / | Returns information about all provisioned DAX clusters if no cluster identifier is specified, or about a specific DAX cluster if a cluster identifier is supplied. If the cluster is in the CREATING state, only cluster level information will be displayed until all of the nodes are successfully provisioned. If the cluster is in the DELETING state, only cluster level information will be displayed. If nodes are currently being added to the DAX cluster, node endpoint information and creation time for the additional nodes will not be displayed until they are completely provisioned. When the DAX cluster state is available, the cluster is ready for use. If nodes are currently being removed from the DAX cluster, no endpoint information for the removed nodes is displayed. |
| POST | / | Returns the default system parameter information for the DAX caching software. |
| POST | / | Returns events related to DAX clusters and parameter groups. You can obtain events specific to a particular DAX cluster or parameter group by providing the name as a parameter. By default, only the events occurring within the last 24 hours are returned; however, you can retrieve up to 14 days' worth of events if necessary. |
| POST | / | Returns a list of parameter group descriptions. If a parameter group name is specified, the list will contain only the descriptions for that group. |
| POST | / | Returns the detailed parameter list for a particular parameter group. |
| POST | / | Returns a list of subnet group descriptions. If a subnet group name is specified, the list will contain only the description of that group. |
| POST | / | Adds one or more nodes to a DAX cluster. |
| POST | / | List all of the tags for a DAX cluster. You can call ListTags up to 10 times per second, per account. |
| POST | / | Reboots a single node of a DAX cluster. The reboot action takes place as soon as possible. During the reboot, the node status is set to REBOOTING.   RebootNode restarts the DAX engine process and does not remove the contents of the cache. |
| POST | / | Associates a set of tags with a DAX resource. You can call TagResource up to 5 times per second, per account. |
| POST | / | Removes the association of tags from a DAX resource. You can call UntagResource up to 5 times per second, per account. |
| POST | / | Modifies the settings for a DAX cluster. You can use this action to change one or more cluster configuration parameters by specifying the parameters and the new values. |
| POST | / | Modifies the parameters of a parameter group. You can modify up to 20 parameters in a single request by submitting a list parameter name and value pairs. |
| POST | / | Modifies an existing subnet group. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
