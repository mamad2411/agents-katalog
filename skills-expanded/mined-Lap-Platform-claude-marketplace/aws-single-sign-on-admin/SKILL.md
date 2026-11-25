---
name: aws-single-sign-on-admin
description: "AWS Single Sign-On Admin API skill. Use when working with AWS Single Sign-On Admin for root. Covers 73 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS Single Sign-On Admin
API version: 2020-07-20

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST / -- create first resource

## Endpoints

73 endpoints across 1 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| POST | / | Attaches the specified customer managed policy to the specified PermissionSet. |
| POST | / | Attaches an Amazon Web Services managed policy ARN to a permission set.  If the permission set is already referenced by one or more account assignments, you will need to call  ProvisionPermissionSet  after this operation. Calling ProvisionPermissionSet applies the corresponding IAM policy updates to all assigned accounts. |
| POST | / | Assigns access to a principal for a specified Amazon Web Services account using a specified permission set.  The term principal here refers to a user or group that is defined in IAM Identity Center.   As part of a successful CreateAccountAssignment call, the specified permission set will automatically be provisioned to the account in the form of an IAM policy. That policy is attached to the IAM role created in IAM Identity Center. If the permission set is subsequently updated, the corresponding IAM policies attached to roles in your accounts will not be updated automatically. In this case, you must call  ProvisionPermissionSet  to make these updates.    After a successful response, call DescribeAccountAssignmentCreationStatus to describe the status of an assignment creation request. |
| POST | / | Creates an application in IAM Identity Center for the given application provider. |
| POST | / | Grant application access to a user or group. |
| POST | / | Creates an instance of IAM Identity Center for a standalone Amazon Web Services account that is not managed by Organizations or a member Amazon Web Services account in an organization. You can create only one instance per account and across all Amazon Web Services Regions. The CreateInstance request is rejected if the following apply:    The instance is created within the organization management account.   An instance already exists in the same account. |
| POST | / | Enables the attributes-based access control (ABAC) feature for the specified IAM Identity Center instance. You can also specify new attributes to add to your ABAC configuration during the enabling process. For more information about ABAC, see Attribute-Based Access Control in the IAM Identity Center User Guide.  After a successful response, call DescribeInstanceAccessControlAttributeConfiguration to validate that InstanceAccessControlAttributeConfiguration was created. |
| POST | / | Creates a permission set within a specified IAM Identity Center instance.  To grant users and groups access to Amazon Web Services account resources, use  CreateAccountAssignment . |
| POST | / | Creates a connection to a trusted token issuer in an instance of IAM Identity Center. A trusted token issuer enables trusted identity propagation to be used with applications that authenticate outside of Amazon Web Services. This trusted token issuer describes an external identity provider (IdP) that can generate claims or assertions in the form of access tokens for a user. Applications enabled for IAM Identity Center can use these tokens for authentication. |
| POST | / | Deletes a principal's access from a specified Amazon Web Services account using a specified permission set.  After a successful response, call DescribeAccountAssignmentDeletionStatus to describe the status of an assignment deletion request. |
| POST | / | Deletes the association with the application. The connected service resource still exists. |
| POST | / | Deletes an IAM Identity Center access scope from an application. |
| POST | / | Revoke application access to an application by deleting application assignments for a user or group. |
| POST | / | Deletes an authentication method from an application. |
| POST | / | Deletes a grant from an application. |
| POST | / | Deletes the inline policy from a specified permission set. |
| POST | / | Deletes the instance of IAM Identity Center. Only the account that owns the instance can call this API. Neither the delegated administrator nor member account can delete the organization instance, but those roles can delete their own instance. |
| POST | / | Disables the attributes-based access control (ABAC) feature for the specified IAM Identity Center instance and deletes all of the attribute mappings that have been configured. Once deleted, any attributes that are received from an identity source and any custom attributes you have previously configured will not be passed. For more information about ABAC, see Attribute-Based Access Control in the IAM Identity Center User Guide. |
| POST | / | Deletes the specified permission set. |
| POST | / | Deletes the permissions boundary from a specified PermissionSet. |
| POST | / | Deletes a trusted token issuer configuration from an instance of IAM Identity Center.  Deleting this trusted token issuer configuration will cause users to lose access to any applications that are configured to use the trusted token issuer. |
| POST | / | Describes the status of the assignment creation request. |
| POST | / | Describes the status of the assignment deletion request. |
| POST | / | Retrieves the details of an application associated with an instance of IAM Identity Center. |
| POST | / | Retrieves a direct assignment of a user or group to an application. If the user doesn’t have a direct assignment to the application, the user may still have access to the application through a group. Therefore, don’t use this API to test access to an application for a user. Instead use ListApplicationAssignmentsForPrincipal. |
| POST | / | Retrieves details about a provider that can be used to connect an Amazon Web Services managed application or customer managed application to IAM Identity Center. |
| POST | / | Returns the details of an instance of IAM Identity Center. The status can be one of the following:    CREATE_IN_PROGRESS - The instance is in the process of being created. When the instance is ready for use, DescribeInstance returns the status of ACTIVE. While the instance is in the CREATE_IN_PROGRESS state, you can call only DescribeInstance and DeleteInstance operations.    DELETE_IN_PROGRESS - The instance is being deleted. Returns AccessDeniedException after the delete operation completes.     ACTIVE - The instance is active. |
| POST | / | Returns the list of IAM Identity Center identity store attributes that have been configured to work with attributes-based access control (ABAC) for the specified IAM Identity Center instance. This will not return attributes configured and sent by an external identity provider. For more information about ABAC, see Attribute-Based Access Control in the IAM Identity Center User Guide. |
| POST | / | Gets the details of the permission set. |
| POST | / | Describes the status for the given permission set provisioning request. |
| POST | / | Retrieves details about a trusted token issuer configuration stored in an instance of IAM Identity Center. Details include the name of the trusted token issuer, the issuer URL, and the path of the source attribute and the destination attribute for a trusted token issuer configuration. |
| POST | / | Detaches the specified customer managed policy from the specified PermissionSet. |
| POST | / | Detaches the attached Amazon Web Services managed policy ARN from the specified permission set. |
| POST | / | Retrieves the authorized targets for an IAM Identity Center access scope for an application. |
| POST | / | Retrieves the configuration of PutApplicationAssignmentConfiguration. |
| POST | / | Retrieves details about an authentication method used by an application. |
| POST | / | Retrieves details about an application grant. |
| POST | / | Obtains the inline policy assigned to the permission set. |
| POST | / | Obtains the permissions boundary for a specified PermissionSet. |
| POST | / | Lists the status of the Amazon Web Services account assignment creation requests for a specified IAM Identity Center instance. |
| POST | / | Lists the status of the Amazon Web Services account assignment deletion requests for a specified IAM Identity Center instance. |
| POST | / | Lists the assignee of the specified Amazon Web Services account with the specified permission set. |
| POST | / | Retrieves a list of the IAM Identity Center associated Amazon Web Services accounts that the principal has access to. |
| POST | / | Lists all the Amazon Web Services accounts where the specified permission set is provisioned. |
| POST | / | Lists the access scopes and authorized targets associated with an application. |
| POST | / | Lists Amazon Web Services account users that are assigned to an application. |
| POST | / | Lists the applications to which a specified principal is assigned. |
| POST | / | Lists all of the authentication methods supported by the specified application. |
| POST | / | List the grants associated with an application. |
| POST | / | Lists the application providers configured in the IAM Identity Center identity store. |
| POST | / | Lists all applications associated with the instance of IAM Identity Center. When listing applications for an instance in the management account, member accounts must use the applicationAccount parameter to filter the list to only applications created from that account. |
| POST | / | Lists all customer managed policies attached to a specified PermissionSet. |
| POST | / | Lists the details of the organization and account instances of IAM Identity Center that were created in or visible to the account calling this API. |
| POST | / | Lists the Amazon Web Services managed policy that is attached to a specified permission set. |
| POST | / | Lists the status of the permission set provisioning requests for a specified IAM Identity Center instance. |
| POST | / | Lists the PermissionSets in an IAM Identity Center instance. |
| POST | / | Lists all the permission sets that are provisioned to a specified Amazon Web Services account. |
| POST | / | Lists the tags that are attached to a specified resource. |
| POST | / | Lists all the trusted token issuers configured in an instance of IAM Identity Center. |
| POST | / | The process by which a specified permission set is provisioned to the specified target. |
| POST | / | Adds or updates the list of authorized targets for an IAM Identity Center access scope for an application. |
| POST | / | Configure how users gain access to an application. If AssignmentsRequired is true (default value), users don’t have access to the application unless an assignment is created using the CreateApplicationAssignment API. If false, all users have access to the application. If an assignment is created using CreateApplicationAssignment., the user retains access if AssignmentsRequired is set to true. |
| POST | / | Adds or updates an authentication method for an application. |
| POST | / | Adds a grant to an application. |
| POST | / | Attaches an inline policy to a permission set.  If the permission set is already referenced by one or more account assignments, you will need to call  ProvisionPermissionSet  after this action to apply the corresponding IAM policy updates to all assigned accounts. |
| POST | / | Attaches an Amazon Web Services managed or customer managed policy to the specified PermissionSet as a permissions boundary. |
| POST | / | Associates a set of tags with a specified resource. |
| POST | / | Disassociates a set of tags from a specified resource. |
| POST | / | Updates application properties. |
| POST | / | Update the details for the instance of IAM Identity Center that is owned by the Amazon Web Services account. |
| POST | / | Updates the IAM Identity Center identity store attributes that you can use with the IAM Identity Center instance for attributes-based access control (ABAC). When using an external identity provider as an identity source, you can pass attributes through the SAML assertion as an alternative to configuring attributes from the IAM Identity Center identity store. If a SAML assertion passes any of these attributes, IAM Identity Center replaces the attribute value with the value from the IAM Identity Center identity store. For more information about ABAC, see Attribute-Based Access Control in the IAM Identity Center User Guide. |
| POST | / | Updates an existing permission set. |
| POST | / | Updates the name of the trusted token issuer, or the path of a source attribute or destination attribute for a trusted token issuer configuration.  Updating this trusted token issuer configuration might cause users to lose access to any applications that are configured to use the trusted token issuer. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
