---
name: aws-resource-access-manager
description: "AWS Resource Access Manager API skill. Use when working with AWS Resource Access Manager for acceptresourceshareinvitation, associateresourceshare, associateresourcesharepermission. Covers 34 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS Resource Access Manager
API version: 2018-01-04

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST /acceptresourceshareinvitation -- create first acceptresourceshareinvitation

## Endpoints

34 endpoints across 34 groups. See references/api-spec.lap for full details.

### acceptresourceshareinvitation
| Method | Path | Description |
|--------|------|-------------|
| POST | /acceptresourceshareinvitation | Accepts an invitation to a resource share from another Amazon Web Services account. After you accept the invitation, the resources included in the resource share are available to interact with in the relevant Amazon Web Services Management Consoles and tools. |

### associateresourceshare
| Method | Path | Description |
|--------|------|-------------|
| POST | /associateresourceshare | Adds the specified list of principals and list of resources to a resource share. Principals that already have access to this resource share immediately receive access to the added resources. Newly added principals immediately receive access to the resources shared in this resource share. |

### associateresourcesharepermission
| Method | Path | Description |
|--------|------|-------------|
| POST | /associateresourcesharepermission | Adds or replaces the RAM permission for a resource type included in a resource share. You can have exactly one permission associated with each resource type in the resource share. You can add a new RAM permission only if there are currently no resources of that resource type currently in the resource share. |

### createpermission
| Method | Path | Description |
|--------|------|-------------|
| POST | /createpermission | Creates a customer managed permission for a specified resource type that you can attach to resource shares. It is created in the Amazon Web Services Region in which you call the operation. |

### createpermissionversion
| Method | Path | Description |
|--------|------|-------------|
| POST | /createpermissionversion | Creates a new version of the specified customer managed permission. The new version is automatically set as the default version of the customer managed permission. New resource shares automatically use the default permission. Existing resource shares continue to use their original permission versions, but you can use ReplacePermissionAssociations to update them. If the specified customer managed permission already has the maximum of 5 versions, then you must delete one of the existing versions before you can create a new one. |

### createresourceshare
| Method | Path | Description |
|--------|------|-------------|
| POST | /createresourceshare | Creates a resource share. You can provide a list of the Amazon Resource Names (ARNs) for the resources that you want to share, a list of principals you want to share the resources with, and the permissions to grant those principals.  Sharing a resource makes it available for use by principals outside of the Amazon Web Services account that created the resource. Sharing doesn't change any permissions or quotas that apply to the resource in the account that created it. |

### deletepermission
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /deletepermission | Deletes the specified customer managed permission in the Amazon Web Services Region in which you call this operation. You can delete a customer managed permission only if it isn't attached to any resource share. The operation deletes all versions associated with the customer managed permission. |

### deletepermissionversion
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /deletepermissionversion | Deletes one version of a customer managed permission. The version you specify must not be attached to any resource share and must not be the default version for the permission. If a customer managed permission has the maximum of 5 versions, then you must delete at least one version before you can create another. |

### deleteresourceshare
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /deleteresourceshare | Deletes the specified resource share.  This doesn't delete any of the resources that were associated with the resource share; it only stops the sharing of those resources through this resource share. |

### disassociateresourceshare
| Method | Path | Description |
|--------|------|-------------|
| POST | /disassociateresourceshare | Removes the specified principals or resources from participating in the specified resource share. |

### disassociateresourcesharepermission
| Method | Path | Description |
|--------|------|-------------|
| POST | /disassociateresourcesharepermission | Removes a managed permission from a resource share. Permission changes take effect immediately. You can remove a managed permission from a resource share only if there are currently no resources of the relevant resource type currently attached to the resource share. |

### enablesharingwithawsorganization
| Method | Path | Description |
|--------|------|-------------|
| POST | /enablesharingwithawsorganization | Enables resource sharing within your organization in Organizations. This operation creates a service-linked role called AWSServiceRoleForResourceAccessManager that has the IAM managed policy named AWSResourceAccessManagerServiceRolePolicy attached. This role permits RAM to retrieve information about the organization and its structure. This lets you share resources with all of the accounts in the calling account's organization by specifying the organization ID, or all of the accounts in an organizational unit (OU) by specifying the OU ID. Until you enable sharing within the organization, you can specify only individual Amazon Web Services accounts, or for supported resource types, IAM roles and users. You must call this operation from an IAM role or user in the organization's management account. |

### getpermission
| Method | Path | Description |
|--------|------|-------------|
| POST | /getpermission | Retrieves the contents of a managed permission in JSON format. |

### getresourcepolicies
| Method | Path | Description |
|--------|------|-------------|
| POST | /getresourcepolicies | Retrieves the resource policies for the specified resources that you own and have shared. |

### getresourceshareassociations
| Method | Path | Description |
|--------|------|-------------|
| POST | /getresourceshareassociations | Retrieves the lists of resources and principals that associated for resource shares that you own. |

### getresourceshareinvitations
| Method | Path | Description |
|--------|------|-------------|
| POST | /getresourceshareinvitations | Retrieves details about invitations that you have received for resource shares. |

### getresourceshares
| Method | Path | Description |
|--------|------|-------------|
| POST | /getresourceshares | Retrieves details about the resource shares that you own or that are shared with you. |

### listpendinginvitationresources
| Method | Path | Description |
|--------|------|-------------|
| POST | /listpendinginvitationresources | Lists the resources in a resource share that is shared with you but for which the invitation is still PENDING. That means that you haven't accepted or rejected the invitation and the invitation hasn't expired. |

### listpermissionassociations
| Method | Path | Description |
|--------|------|-------------|
| POST | /listpermissionassociations | Lists information about the managed permission and its associations to any resource shares that use this managed permission. This lets you see which resource shares use which versions of the specified managed permission. |

### listpermissionversions
| Method | Path | Description |
|--------|------|-------------|
| POST | /listpermissionversions | Lists the available versions of the specified RAM permission. |

### listpermissions
| Method | Path | Description |
|--------|------|-------------|
| POST | /listpermissions | Retrieves a list of available RAM permissions that you can use for the supported resource types. |

### listprincipals
| Method | Path | Description |
|--------|------|-------------|
| POST | /listprincipals | Lists the principals that you are sharing resources with or that are sharing resources with you. |

### listreplacepermissionassociationswork
| Method | Path | Description |
|--------|------|-------------|
| POST | /listreplacepermissionassociationswork | Retrieves the current status of the asynchronous tasks performed by RAM when you perform the ReplacePermissionAssociationsWork operation. |

### listresourcesharepermissions
| Method | Path | Description |
|--------|------|-------------|
| POST | /listresourcesharepermissions | Lists the RAM permissions that are associated with a resource share. |

### listresourcetypes
| Method | Path | Description |
|--------|------|-------------|
| POST | /listresourcetypes | Lists the resource types that can be shared by RAM. |

### listresources
| Method | Path | Description |
|--------|------|-------------|
| POST | /listresources | Lists the resources that you added to a resource share or the resources that are shared with you. |

### promotepermissioncreatedfrompolicy
| Method | Path | Description |
|--------|------|-------------|
| POST | /promotepermissioncreatedfrompolicy | When you attach a resource-based policy to a resource, RAM automatically creates a resource share of featureSet=CREATED_FROM_POLICY with a managed permission that has the same IAM permissions as the original resource-based policy. However, this type of managed permission is visible to only the resource share owner, and the associated resource share can't be modified by using RAM. This operation creates a separate, fully manageable customer managed permission that has the same IAM permissions as the original resource-based policy. You can associate this customer managed permission to any resource shares. Before you use PromoteResourceShareCreatedFromPolicy, you should first run this operation to ensure that you have an appropriate customer managed permission that can be associated with the promoted resource share.    The original CREATED_FROM_POLICY policy isn't deleted, and resource shares using that original policy aren't automatically updated.   You can't modify a CREATED_FROM_POLICY resource share so you can't associate the new customer managed permission by using ReplacePermsissionAssociations. However, if you use PromoteResourceShareCreatedFromPolicy, that operation automatically associates the fully manageable customer managed permission to the newly promoted STANDARD resource share.   After you promote a resource share, if the original CREATED_FROM_POLICY managed permission has no other associations to A resource share, then RAM automatically deletes it. |

### promoteresourcesharecreatedfrompolicy
| Method | Path | Description |
|--------|------|-------------|
| POST | /promoteresourcesharecreatedfrompolicy | When you attach a resource-based policy to a resource, RAM automatically creates a resource share of featureSet=CREATED_FROM_POLICY with a managed permission that has the same IAM permissions as the original resource-based policy. However, this type of managed permission is visible to only the resource share owner, and the associated resource share can't be modified by using RAM. This operation promotes the resource share to a STANDARD resource share that is fully manageable in RAM. When you promote a resource share, you can then manage the resource share in RAM and it becomes visible to all of the principals you shared it with.  Before you perform this operation, you should first run PromotePermissionCreatedFromPolicyto ensure that you have an appropriate customer managed permission that can be associated with this resource share after its is promoted. If this operation can't find a managed permission that exactly matches the existing CREATED_FROM_POLICY permission, then this operation fails. |

### rejectresourceshareinvitation
| Method | Path | Description |
|--------|------|-------------|
| POST | /rejectresourceshareinvitation | Rejects an invitation to a resource share from another Amazon Web Services account. |

### replacepermissionassociations
| Method | Path | Description |
|--------|------|-------------|
| POST | /replacepermissionassociations | Updates all resource shares that use a managed permission to a different managed permission. This operation always applies the default version of the target managed permission. You can optionally specify that the update applies to only resource shares that currently use a specified version. This enables you to update to the latest version, without changing the which managed permission is used. You can use this operation to update all of your resource shares to use the current default version of the permission by specifying the same value for the fromPermissionArn and toPermissionArn parameters. You can use the optional fromPermissionVersion parameter to update only those resources that use a specified version of the managed permission to the new managed permission.  To successfully perform this operation, you must have permission to update the resource-based policy on all affected resource types. |

### setdefaultpermissionversion
| Method | Path | Description |
|--------|------|-------------|
| POST | /setdefaultpermissionversion | Designates the specified version number as the default version for the specified customer managed permission. New resource shares automatically use this new default permission. Existing resource shares continue to use their original permission version, but you can use ReplacePermissionAssociations to update them. |

### tagresource
| Method | Path | Description |
|--------|------|-------------|
| POST | /tagresource | Adds the specified tag keys and values to a resource share or managed permission. If you choose a resource share, the tags are attached to only the resource share, not to the resources that are in the resource share. The tags on a managed permission are the same for all versions of the managed permission. |

### untagresource
| Method | Path | Description |
|--------|------|-------------|
| POST | /untagresource | Removes the specified tag key and value pairs from the specified resource share or managed permission. |

### updateresourceshare
| Method | Path | Description |
|--------|------|-------------|
| POST | /updateresourceshare | Modifies some of the properties of the specified resource share. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a acceptresourceshareinvitation?" -> POST /acceptresourceshareinvitation
- "Create a associateresourceshare?" -> POST /associateresourceshare
- "Create a associateresourcesharepermission?" -> POST /associateresourcesharepermission
- "Create a createpermission?" -> POST /createpermission
- "Create a createpermissionversion?" -> POST /createpermissionversion
- "Create a createresourceshare?" -> POST /createresourceshare
- "Create a disassociateresourceshare?" -> POST /disassociateresourceshare
- "Create a disassociateresourcesharepermission?" -> POST /disassociateresourcesharepermission
- "Create a enablesharingwithawsorganization?" -> POST /enablesharingwithawsorganization
- "Create a getpermission?" -> POST /getpermission
- "Create a getresourcepolicy?" -> POST /getresourcepolicies
- "Create a getresourceshareassociation?" -> POST /getresourceshareassociations
- "Create a getresourceshareinvitation?" -> POST /getresourceshareinvitations
- "Create a getresourceshare?" -> POST /getresourceshares
- "Create a listpendinginvitationresource?" -> POST /listpendinginvitationresources
- "Create a listpermissionassociation?" -> POST /listpermissionassociations
- "Create a listpermissionversion?" -> POST /listpermissionversions
- "Create a listpermission?" -> POST /listpermissions
- "Create a listprincipal?" -> POST /listprincipals
- "Create a listreplacepermissionassociationswork?" -> POST /listreplacepermissionassociationswork
- "Create a listresourcesharepermission?" -> POST /listresourcesharepermissions
- "Create a listresourcetype?" -> POST /listresourcetypes
- "Create a listresource?" -> POST /listresources
- "Create a promotepermissioncreatedfrompolicy?" -> POST /promotepermissioncreatedfrompolicy
- "Create a promoteresourcesharecreatedfrompolicy?" -> POST /promoteresourcesharecreatedfrompolicy
- "Create a rejectresourceshareinvitation?" -> POST /rejectresourceshareinvitation
- "Create a replacepermissionassociation?" -> POST /replacepermissionassociations
- "Create a setdefaultpermissionversion?" -> POST /setdefaultpermissionversion
- "Create a tagresource?" -> POST /tagresource
- "Create a untagresource?" -> POST /untagresource
- "Create a updateresourceshare?" -> POST /updateresourceshare
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
