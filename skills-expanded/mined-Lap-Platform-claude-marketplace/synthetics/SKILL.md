---
name: synthetics
description: "Synthetics API skill. Use when working with Synthetics for group, canary, canaries. Covers 21 endpoints."
version: 1.0.0
generator: lapsh
---

# Synthetics
API version: 2017-10-11

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /canary/{name} -- verify access
3. POST /canary -- create first canary

## Endpoints

21 endpoints across 7 groups. See references/api-spec.lap for full details.

### group
| Method | Path | Description |
|--------|------|-------------|
| PATCH | /group/{groupIdentifier}/associate | Associates a canary with a group. Using groups can help you with managing and automating your canaries, and you can also view aggregated run results and statistics for all canaries in a group.  You must run this operation in the Region where the canary exists. |
| POST | /group | Creates a group which you can use to associate canaries with each other, including cross-Region canaries. Using groups can help you with managing and automating your canaries, and you can also view aggregated run results and statistics for all canaries in a group.  Groups are global resources. When you create a group, it is replicated across Amazon Web Services Regions, and you can view it and add canaries to it from any Region. Although the group ARN format reflects the Region name where it was created, a group is not constrained to any Region. This means that you can put canaries from multiple Regions into the same group, and then use that group to view and manage all of those canaries in a single view. Groups are supported in all Regions except the Regions that are disabled by default. For more information about these Regions, see Enabling a Region. Each group can contain as many as 10 canaries. You can have as many as 20 groups in your account. Any single canary can be a member of up to 10 groups. |
| DELETE | /group/{groupIdentifier} | Deletes a group. The group doesn't need to be empty to be deleted. If there are canaries in the group, they are not deleted when you delete the group.  Groups are a global resource that appear in all Regions, but the request to delete a group must be made from its home Region. You can find the home Region of a group within its ARN. |
| PATCH | /group/{groupIdentifier}/disassociate | Removes a canary from a group. You must run this operation in the Region where the canary exists. |
| GET | /group/{groupIdentifier} | Returns information about one group. Groups are a global resource, so you can use this operation from any Region. |
| POST | /group/{groupIdentifier}/resources | This operation returns a list of the ARNs of the canaries that are associated with the specified group. |

### canary
| Method | Path | Description |
|--------|------|-------------|
| POST | /canary | Creates a canary. Canaries are scripts that monitor your endpoints and APIs from the outside-in. Canaries help you check the availability and latency of your web services and troubleshoot anomalies by investigating load time data, screenshots of the UI, logs, and metrics. You can set up a canary to run continuously or just once.  Do not use CreateCanary to modify an existing canary. Use UpdateCanary instead. To create canaries, you must have the CloudWatchSyntheticsFullAccess policy. If you are creating a new IAM role for the canary, you also need the iam:CreateRole, iam:CreatePolicy and iam:AttachRolePolicy permissions. For more information, see Necessary Roles and Permissions. Do not include secrets or proprietary information in your canary names. The canary name makes up part of the Amazon Resource Name (ARN) for the canary, and the ARN is included in outbound calls over the internet. For more information, see Security Considerations for Synthetics Canaries. |
| DELETE | /canary/{name} | Permanently deletes the specified canary. If you specify DeleteLambda to true, CloudWatch Synthetics also deletes the Lambda functions and layers that are used by the canary. Other resources used and created by the canary are not automatically deleted. After you delete a canary that you do not intend to use again, you should also delete the following:   The CloudWatch alarms created for this canary. These alarms have a name of Synthetics-SharpDrop-Alarm-MyCanaryName .   Amazon S3 objects and buckets, such as the canary's artifact location.   IAM roles created for the canary. If they were created in the console, these roles have the name  role/service-role/CloudWatchSyntheticsRole-MyCanaryName .   CloudWatch Logs log groups created for the canary. These logs groups have the name /aws/lambda/cwsyn-MyCanaryName .    Before you delete a canary, you might want to use GetCanary to display the information about this canary. Make note of the information returned by this operation so that you can delete these resources after you delete the canary. |
| GET | /canary/{name} | Retrieves complete information about one canary. You must specify the name of the canary that you want. To get a list of canaries and their names, use DescribeCanaries. |
| POST | /canary/{name}/runs | Retrieves a list of runs for a specified canary. |
| POST | /canary/{name}/start | Use this operation to run a canary that has already been created. The frequency of the canary runs is determined by the value of the canary's Schedule. To see a canary's schedule, use GetCanary. |
| POST | /canary/{name}/stop | Stops the canary to prevent all future runs. If the canary is currently running,the run that is in progress completes on its own, publishes metrics, and uploads artifacts, but it is not recorded in Synthetics as a completed run. You can use StartCanary to start it running again with the canary’s current schedule at any point in the future. |
| PATCH | /canary/{name} | Updates the configuration of a canary that has already been created. You can't use this operation to update the tags of an existing canary. To change the tags of an existing canary, use TagResource. |

### canaries
| Method | Path | Description |
|--------|------|-------------|
| POST | /canaries | This operation returns a list of the canaries in your account, along with full details about each canary. This operation supports resource-level authorization using an IAM policy and the Names parameter. If you specify the Names parameter, the operation is successful only if you have authorization to view all the canaries that you specify in your request. If you do not have permission to view any of the canaries, the request fails with a 403 response. You are required to use the Names parameter if you are logged on to a user or role that has an IAM policy that restricts which canaries that you are allowed to view. For more information, see  Limiting a user to viewing specific canaries. |
| POST | /canaries/last-run | Use this operation to see information from the most recent run of each canary that you have created. This operation supports resource-level authorization using an IAM policy and the Names parameter. If you specify the Names parameter, the operation is successful only if you have authorization to view all the canaries that you specify in your request. If you do not have permission to view any of the canaries, the request fails with a 403 response. You are required to use the Names parameter if you are logged on to a user or role that has an IAM policy that restricts which canaries that you are allowed to view. For more information, see  Limiting a user to viewing specific canaries. |

### runtime-versions
| Method | Path | Description |
|--------|------|-------------|
| POST | /runtime-versions | Returns a list of Synthetics canary runtime versions. For more information, see  Canary Runtime Versions. |

### resource
| Method | Path | Description |
|--------|------|-------------|
| POST | /resource/{resourceArn}/groups | Returns a list of the groups that the specified canary is associated with. The canary that you specify must be in the current Region. |

### groups
| Method | Path | Description |
|--------|------|-------------|
| POST | /groups | Returns a list of all groups in the account, displaying their names, unique IDs, and ARNs. The groups from all Regions are returned. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags/{resourceArn} | Displays the tags associated with a canary or group. |
| POST | /tags/{resourceArn} | Assigns one or more tags (key-value pairs) to the specified canary or group.  Tags can help you organize and categorize your resources. You can also use them to scope user permissions, by granting a user permission to access or change only resources with certain tag values. Tags don't have any semantic meaning to Amazon Web Services and are interpreted strictly as strings of characters. You can use the TagResource action with a resource that already has tags. If you specify a new tag key for the resource, this tag is appended to the list of tags associated with the resource. If you specify a tag key that is already associated with the resource, the new tag value that you specify replaces the previous value for that tag. You can associate as many as 50 tags with a canary or group. |
| DELETE | /tags/{resourceArn} | Removes one or more tags from the specified resource. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a canary?" -> POST /canary
- "Create a group?" -> POST /group
- "Delete a canary?" -> DELETE /canary/{name}
- "Delete a group?" -> DELETE /group/{groupIdentifier}
- "Create a canary?" -> POST /canaries
- "Create a last-run?" -> POST /canaries/last-run
- "Create a runtime-version?" -> POST /runtime-versions
- "Get canary details?" -> GET /canary/{name}
- "Create a run?" -> POST /canary/{name}/runs
- "Get group details?" -> GET /group/{groupIdentifier}
- "Create a group?" -> POST /resource/{resourceArn}/groups
- "Create a resource?" -> POST /group/{groupIdentifier}/resources
- "Create a group?" -> POST /groups
- "Get tag details?" -> GET /tags/{resourceArn}
- "Create a start?" -> POST /canary/{name}/start
- "Create a stop?" -> POST /canary/{name}/stop
- "Delete a tag?" -> DELETE /tags/{resourceArn}
- "Partially update a canary?" -> PATCH /canary/{name}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
