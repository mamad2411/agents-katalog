---
name: aws-directory-service
description: "AWS Directory Service API skill. Use when working with AWS Directory Service for root. Covers 67 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS Directory Service
API version: 2015-04-16

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST / -- create first resource

## Endpoints

67 endpoints across 1 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| POST | / | Accepts a directory sharing request that was sent from the directory owner account. |
| POST | / | If the DNS server for your self-managed domain uses a publicly addressable IP address, you must add a CIDR address block to correctly route traffic to and from your Microsoft AD on Amazon Web Services. AddIpRoutes adds this address block. You can also use AddIpRoutes to facilitate routing traffic that uses public IP ranges from your Microsoft AD on Amazon Web Services to a peer VPC.  Before you call AddIpRoutes, ensure that all of the required permissions have been explicitly granted through a policy. For details about what permissions are required to run the AddIpRoutes operation, see Directory Service API Permissions: Actions, Resources, and Conditions Reference. |
| POST | / | Adds two domain controllers in the specified Region for the specified directory. |
| POST | / | Adds or overwrites one or more tags for the specified directory. Each directory can have a maximum of 50 tags. Each tag consists of a key and optional value. Tag keys must be unique to each resource. |
| POST | / | Cancels an in-progress schema extension to a Microsoft AD directory. Once a schema extension has started replicating to all domain controllers, the task can no longer be canceled. A schema extension can be canceled during any of the following states; Initializing, CreatingSnapshot, and UpdatingSchema. |
| POST | / | Creates an AD Connector to connect to a self-managed directory. Before you call ConnectDirectory, ensure that all of the required permissions have been explicitly granted through a policy. For details about what permissions are required to run the ConnectDirectory operation, see Directory Service API Permissions: Actions, Resources, and Conditions Reference. |
| POST | / | Creates an alias for a directory and assigns the alias to the directory. The alias is used to construct the access URL for the directory, such as http://&lt;alias&gt;.awsapps.com.  After an alias has been created, it cannot be deleted or reused, so this operation should only be used when absolutely necessary. |
| POST | / | Creates an Active Directory computer object in the specified directory. |
| POST | / | Creates a conditional forwarder associated with your Amazon Web Services directory. Conditional forwarders are required in order to set up a trust relationship with another domain. The conditional forwarder points to the trusted domain. |
| POST | / | Creates a Simple AD directory. For more information, see Simple Active Directory in the Directory Service Admin Guide. Before you call CreateDirectory, ensure that all of the required permissions have been explicitly granted through a policy. For details about what permissions are required to run the CreateDirectory operation, see Directory Service API Permissions: Actions, Resources, and Conditions Reference. |
| POST | / | Creates a subscription to forward real-time Directory Service domain controller security logs to the specified Amazon CloudWatch log group in your Amazon Web Services account. |
| POST | / | Creates a Microsoft AD directory in the Amazon Web Services Cloud. For more information, see Managed Microsoft AD in the Directory Service Admin Guide. Before you call CreateMicrosoftAD, ensure that all of the required permissions have been explicitly granted through a policy. For details about what permissions are required to run the CreateMicrosoftAD operation, see Directory Service API Permissions: Actions, Resources, and Conditions Reference. |
| POST | / | Creates a snapshot of a Simple AD or Microsoft AD directory in the Amazon Web Services cloud.  You cannot take snapshots of AD Connector directories. |
| POST | / | Directory Service for Microsoft Active Directory allows you to configure trust relationships. For example, you can establish a trust between your Managed Microsoft AD directory, and your existing self-managed Microsoft Active Directory. This would allow you to provide users and groups access to resources in either domain, with a single set of credentials. This action initiates the creation of the Amazon Web Services side of a trust relationship between an Managed Microsoft AD directory and an external domain. You can create either a forest trust or an external trust. |
| POST | / | Deletes a conditional forwarder that has been set up for your Amazon Web Services directory. |
| POST | / | Deletes an Directory Service directory. Before you call DeleteDirectory, ensure that all of the required permissions have been explicitly granted through a policy. For details about what permissions are required to run the DeleteDirectory operation, see Directory Service API Permissions: Actions, Resources, and Conditions Reference. |
| POST | / | Deletes the specified log subscription. |
| POST | / | Deletes a directory snapshot. |
| POST | / | Deletes an existing trust relationship between your Managed Microsoft AD directory and an external domain. |
| POST | / | Deletes from the system the certificate that was registered for secure LDAP or client certificate authentication. |
| POST | / | Removes the specified directory as a publisher to the specified Amazon SNS topic. |
| POST | / | Displays information about the certificate registered for secure LDAP or client certificate authentication. |
| POST | / | Retrieves information about the type of client authentication for the specified directory, if the type is specified. If no type is specified, information about all client authentication types that are supported for the specified directory is retrieved. Currently, only SmartCard is supported. |
| POST | / | Obtains information about the conditional forwarders for this account. If no input parameters are provided for RemoteDomainNames, this request describes all conditional forwarders for the specified directory ID. |
| POST | / | Obtains information about the directories that belong to this account. You can retrieve information about specific directories by passing the directory identifiers in the DirectoryIds parameter. Otherwise, all directories that belong to the current account are returned. This operation supports pagination with the use of the NextToken request and response parameters. If more results are available, the DescribeDirectoriesResult.NextToken member contains a token that you pass in the next call to DescribeDirectories to retrieve the next set of items. You can also specify a maximum number of return results with the Limit parameter. |
| POST | / | Provides information about any domain controllers in your directory. |
| POST | / | Obtains information about which Amazon SNS topics receive status messages from the specified directory. If no input parameters are provided, such as DirectoryId or TopicName, this request describes all of the associations in the account. |
| POST | / | Describes the status of LDAP security for the specified directory. |
| POST | / | Provides information about the Regions that are configured for multi-Region replication. |
| POST | / | Retrieves information about the configurable settings for the specified directory. |
| POST | / | Returns the shared directories in your account. |
| POST | / | Obtains information about the directory snapshots that belong to this account. This operation supports pagination with the use of the NextToken request and response parameters. If more results are available, the DescribeSnapshots.NextToken member contains a token that you pass in the next call to DescribeSnapshots to retrieve the next set of items. You can also specify a maximum number of return results with the Limit parameter. |
| POST | / | Obtains information about the trust relationships for this account. If no input parameters are provided, such as DirectoryId or TrustIds, this request describes all the trust relationships belonging to the account. |
| POST | / | Describes the updates of a directory for a particular update type. |
| POST | / | Disables alternative client authentication methods for the specified directory. |
| POST | / | Deactivates LDAP secure calls for the specified directory. |
| POST | / | Disables multi-factor authentication (MFA) with the Remote Authentication Dial In User Service (RADIUS) server for an AD Connector or Microsoft AD directory. |
| POST | / | Disables single-sign on for a directory. |
| POST | / | Enables alternative client authentication methods for the specified directory. |
| POST | / | Activates the switch for the specific directory to always use LDAP secure calls. |
| POST | / | Enables multi-factor authentication (MFA) with the Remote Authentication Dial In User Service (RADIUS) server for an AD Connector or Microsoft AD directory. |
| POST | / | Enables single sign-on for a directory. Single sign-on allows users in your directory to access certain Amazon Web Services services from a computer joined to the directory without having to enter their credentials separately. |
| POST | / | Obtains directory limit information for the current Region. |
| POST | / | Obtains the manual snapshot limits for a directory. |
| POST | / | For the specified directory, lists all the certificates registered for a secure LDAP or client certificate authentication. |
| POST | / | Lists the address blocks that you have added to a directory. |
| POST | / | Lists the active log subscriptions for the Amazon Web Services account. |
| POST | / | Lists all schema extensions applied to a Microsoft AD Directory. |
| POST | / | Lists all tags on a directory. |
| POST | / | Registers a certificate for a secure LDAP or client certificate authentication. |
| POST | / | Associates a directory with an Amazon SNS topic. This establishes the directory as a publisher to the specified Amazon SNS topic. You can then receive email or text (SMS) messages when the status of your directory changes. You get notified if your directory goes from an Active status to an Impaired or Inoperable status. You also receive a notification when the directory returns to an Active status. |
| POST | / | Rejects a directory sharing request that was sent from the directory owner account. |
| POST | / | Removes IP address blocks from a directory. |
| POST | / | Stops all replication and removes the domain controllers from the specified Region. You cannot remove the primary Region with this operation. Instead, use the DeleteDirectory API. |
| POST | / | Removes tags from a directory. |
| POST | / | Resets the password for any user in your Managed Microsoft AD or Simple AD directory. You can reset the password for any user in your directory with the following exceptions:   For Simple AD, you cannot reset the password for any user that is a member of either the Domain Admins or Enterprise Admins group except for the administrator user.   For Managed Microsoft AD, you can only reset the password for a user that is in an OU based off of the NetBIOS name that you typed when you created your directory. For example, you cannot reset the password for a user in the Amazon Web Services Reserved OU. For more information about the OU structure for an Managed Microsoft AD directory, see What Gets Created in the Directory Service Administration Guide. |
| POST | / | Restores a directory using an existing directory snapshot. When you restore a directory from a snapshot, any changes made to the directory after the snapshot date are overwritten. This action returns as soon as the restore operation is initiated. You can monitor the progress of the restore operation by calling the DescribeDirectories operation with the directory identifier. When the DirectoryDescription.Stage value changes to Active, the restore operation is complete. |
| POST | / | Shares a specified directory (DirectoryId) in your Amazon Web Services account (directory owner) with another Amazon Web Services account (directory consumer). With this operation you can use your directory from any Amazon Web Services account and from any Amazon VPC within an Amazon Web Services Region. When you share your Managed Microsoft AD directory, Directory Service creates a shared directory in the directory consumer account. This shared directory contains the metadata to provide access to the directory within the directory owner account. The shared directory is visible in all VPCs in the directory consumer account. The ShareMethod parameter determines whether the specified directory can be shared between Amazon Web Services accounts inside the same Amazon Web Services organization (ORGANIZATIONS). It also determines whether you can share the directory with any other Amazon Web Services account either inside or outside of the organization (HANDSHAKE). The ShareNotes parameter is only used when HANDSHAKE is called, which sends a directory sharing request to the directory consumer. |
| POST | / | Applies a schema extension to a Microsoft AD directory. |
| POST | / | Stops the directory sharing between the directory owner and consumer accounts. |
| POST | / | Updates a conditional forwarder that has been set up for your Amazon Web Services directory. |
| POST | / | Updates the directory for a particular update type. |
| POST | / | Adds or removes domain controllers to or from the directory. Based on the difference between current value and new value (provided through this API call), domain controllers will be added or removed. It may take up to 45 minutes for any new domain controllers to become fully active once the requested number of domain controllers is updated. During this time, you cannot make another update request. |
| POST | / | Updates the Remote Authentication Dial In User Service (RADIUS) server information for an AD Connector or Microsoft AD directory. |
| POST | / | Updates the configurable settings for the specified directory. |
| POST | / | Updates the trust that has been set up between your Managed Microsoft AD directory and an self-managed Active Directory. |
| POST | / | Directory Service for Microsoft Active Directory allows you to configure and verify trust relationships. This action verifies a trust relationship between your Managed Microsoft AD directory and an external domain. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
