---
name: aws-resource-groups
description: "AWS Resource Groups API skill. Use when working with AWS Resource Groups for groups, delete-group, get-account-settings. Covers 18 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS Resource Groups
API version: 2017-11-27

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /resources/{Arn}/tags -- verify access
3. POST /groups -- create first groups

## Endpoints

18 endpoints across 15 groups. See references/api-spec.lap for full details.

### groups
| Method | Path | Description |
|--------|------|-------------|
| POST | /groups | Creates a resource group with the specified name and description. You can optionally include either a resource query or a service configuration. For more information about constructing a resource query, see Build queries and groups in Resource Groups in the Resource Groups User Guide. For more information about service-linked groups and service configurations, see Service configurations for Resource Groups.  Minimum permissions  To run this command, you must have the following permissions:    resource-groups:CreateGroup |

### delete-group
| Method | Path | Description |
|--------|------|-------------|
| POST | /delete-group | Deletes the specified resource group. Deleting a resource group does not delete any resources that are members of the group; it only deletes the group structure.  Minimum permissions  To run this command, you must have the following permissions:    resource-groups:DeleteGroup |

### get-account-settings
| Method | Path | Description |
|--------|------|-------------|
| POST | /get-account-settings | Retrieves the current status of optional features in Resource Groups. |

### get-group
| Method | Path | Description |
|--------|------|-------------|
| POST | /get-group | Returns information about a specified resource group.  Minimum permissions  To run this command, you must have the following permissions:    resource-groups:GetGroup |

### get-group-configuration
| Method | Path | Description |
|--------|------|-------------|
| POST | /get-group-configuration | Retrieves the service configuration associated with the specified resource group. For details about the service configuration syntax, see Service configurations for Resource Groups.  Minimum permissions  To run this command, you must have the following permissions:    resource-groups:GetGroupConfiguration |

### get-group-query
| Method | Path | Description |
|--------|------|-------------|
| POST | /get-group-query | Retrieves the resource query associated with the specified resource group. For more information about resource queries, see Create a tag-based group in Resource Groups.  Minimum permissions  To run this command, you must have the following permissions:    resource-groups:GetGroupQuery |

### resources
| Method | Path | Description |
|--------|------|-------------|
| GET | /resources/{Arn}/tags | Returns a list of tags that are associated with a resource group, specified by an ARN.  Minimum permissions  To run this command, you must have the following permissions:    resource-groups:GetTags |
| POST | /resources/search | Returns a list of Amazon Web Services resource identifiers that matches the specified query. The query uses the same format as a resource query in a CreateGroup or UpdateGroupQuery operation.  Minimum permissions  To run this command, you must have the following permissions:    resource-groups:SearchResources     cloudformation:DescribeStacks     cloudformation:ListStackResources     tag:GetResources |
| PUT | /resources/{Arn}/tags | Adds tags to a resource group with the specified ARN. Existing tags on a resource group are not changed if they are not specified in the request parameters.  Do not store personally identifiable information (PII) or other confidential or sensitive information in tags. We use tags to provide you with billing and administration services. Tags are not intended to be used for private or sensitive data.   Minimum permissions  To run this command, you must have the following permissions:    resource-groups:Tag |
| PATCH | /resources/{Arn}/tags | Deletes tags from a specified resource group.  Minimum permissions  To run this command, you must have the following permissions:    resource-groups:Untag |

### group-resources
| Method | Path | Description |
|--------|------|-------------|
| POST | /group-resources | Adds the specified resources to the specified group.  You can use this operation with only resource groups that are configured with the following types:    AWS::EC2::HostManagement     AWS::EC2::CapacityReservationPool    Other resource group type and resource types aren't currently supported by this operation.   Minimum permissions  To run this command, you must have the following permissions:    resource-groups:GroupResources |

### list-group-resources
| Method | Path | Description |
|--------|------|-------------|
| POST | /list-group-resources | Returns a list of ARNs of the resources that are members of a specified resource group.  Minimum permissions  To run this command, you must have the following permissions:    resource-groups:ListGroupResources     cloudformation:DescribeStacks     cloudformation:ListStackResources     tag:GetResources |

### groups-list
| Method | Path | Description |
|--------|------|-------------|
| POST | /groups-list | Returns a list of existing Resource Groups in your account.  Minimum permissions  To run this command, you must have the following permissions:    resource-groups:ListGroups |

### put-group-configuration
| Method | Path | Description |
|--------|------|-------------|
| POST | /put-group-configuration | Attaches a service configuration to the specified group. This occurs asynchronously, and can take time to complete. You can use GetGroupConfiguration to check the status of the update.  Minimum permissions  To run this command, you must have the following permissions:    resource-groups:PutGroupConfiguration |

### ungroup-resources
| Method | Path | Description |
|--------|------|-------------|
| POST | /ungroup-resources | Removes the specified resources from the specified group. This operation works only with static groups that you populated using the GroupResources operation. It doesn't work with any resource groups that are automatically populated by tag-based or CloudFormation stack-based queries.  Minimum permissions  To run this command, you must have the following permissions:    resource-groups:UngroupResources |

### update-account-settings
| Method | Path | Description |
|--------|------|-------------|
| POST | /update-account-settings | Turns on or turns off optional features in Resource Groups. The preceding example shows that the request to turn on group lifecycle events is IN_PROGRESS. You can call the GetAccountSettings operation to check for completion by looking for GroupLifecycleEventsStatus to change to ACTIVE. |

### update-group
| Method | Path | Description |
|--------|------|-------------|
| POST | /update-group | Updates the description for an existing group. You cannot update the name of a resource group.  Minimum permissions  To run this command, you must have the following permissions:    resource-groups:UpdateGroup |

### update-group-query
| Method | Path | Description |
|--------|------|-------------|
| POST | /update-group-query | Updates the resource query of a group. For more information about resource queries, see Create a tag-based group in Resource Groups.  Minimum permissions  To run this command, you must have the following permissions:    resource-groups:UpdateGroupQuery |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a group?" -> POST /groups
- "Create a delete-group?" -> POST /delete-group
- "Create a get-account-setting?" -> POST /get-account-settings
- "Create a get-group?" -> POST /get-group
- "Create a get-group-configuration?" -> POST /get-group-configuration
- "Create a get-group-query?" -> POST /get-group-query
- "List all tags?" -> GET /resources/{Arn}/tags
- "Create a group-resource?" -> POST /group-resources
- "Create a list-group-resource?" -> POST /list-group-resources
- "Create a groups-list?" -> POST /groups-list
- "Create a put-group-configuration?" -> POST /put-group-configuration
- "Create a search?" -> POST /resources/search
- "Create a ungroup-resource?" -> POST /ungroup-resources
- "Create a update-account-setting?" -> POST /update-account-settings
- "Create a update-group?" -> POST /update-group
- "Create a update-group-query?" -> POST /update-group-query
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
