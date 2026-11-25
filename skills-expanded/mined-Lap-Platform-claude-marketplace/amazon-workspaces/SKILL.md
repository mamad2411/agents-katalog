---
name: amazon-workspaces
description: "Amazon WorkSpaces API skill. Use when working with Amazon WorkSpaces for root. Covers 88 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon WorkSpaces
API version: 2015-04-08

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST / -- create first resource

## Endpoints

88 endpoints across 1 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| POST | / | Accepts the account link invitation.  There's currently no unlinking capability after you accept the account linking invitation. |
| POST | / | Associates the specified connection alias with the specified directory to enable cross-Region redirection. For more information, see  Cross-Region Redirection for Amazon WorkSpaces.  Before performing this operation, call  DescribeConnectionAliases to make sure that the current state of the connection alias is CREATED. |
| POST | / | Associates the specified IP access control group with the specified directory. |
| POST | / | Associates the specified application to the specified WorkSpace. |
| POST | / | Adds one or more rules to the specified IP access control group. This action gives users permission to access their WorkSpaces from the CIDR address ranges specified in the rules. |
| POST | / | Copies the specified image from the specified Region to the current Region. For more information about copying images, see  Copy a Custom WorkSpaces Image. In the China (Ningxia) Region, you can copy images only within the same Region. In Amazon Web Services GovCloud (US), to copy images to and from other Regions, contact Amazon Web Services Support.  Before copying a shared image, be sure to verify that it has been shared from the correct Amazon Web Services account. To determine if an image has been shared and to see the ID of the Amazon Web Services account that owns an image, use the DescribeWorkSpaceImages and DescribeWorkspaceImagePermissions API operations. |
| POST | / | Creates the account link invitation. |
| POST | / | Creates a client-add-in for Amazon Connect within a directory. You can create only one Amazon Connect client add-in within a directory. This client add-in allows WorkSpaces users to seamlessly connect to Amazon Connect. |
| POST | / | Creates the specified connection alias for use with cross-Region redirection. For more information, see  Cross-Region Redirection for Amazon WorkSpaces. |
| POST | / | Creates an IP access control group. An IP access control group provides you with the ability to control the IP addresses from which users are allowed to access their WorkSpaces. To specify the CIDR address ranges, add rules to your IP access control group and then associate the group with your directory. You can add rules when you create the group or at any time using AuthorizeIpRules. There is a default IP access control group associated with your directory. If you don't associate an IP access control group with your directory, the default group is used. The default group includes a default rule that allows users to access their WorkSpaces from anywhere. You cannot modify the default IP access control group for your directory. |
| POST | / | Creates a standby WorkSpace in a secondary Region. |
| POST | / | Creates the specified tags for the specified WorkSpaces resource. |
| POST | / | Creates a new updated WorkSpace image based on the specified source image. The new updated WorkSpace image has the latest drivers and other updates required by the Amazon WorkSpaces components. To determine which WorkSpace images need to be updated with the latest Amazon WorkSpaces requirements, use  DescribeWorkspaceImages.    Only Windows 10, Windows Server 2016, and Windows Server 2019 WorkSpace images can be programmatically updated at this time.   Microsoft Windows updates and other application updates are not included in the update process.   The source WorkSpace image is not deleted. You can delete the source image after you've verified your new updated image and created a new bundle. |
| POST | / | Creates the specified WorkSpace bundle. For more information about creating WorkSpace bundles, see  Create a Custom WorkSpaces Image and Bundle. |
| POST | / | Creates a new WorkSpace image from an existing WorkSpace. |
| POST | / | Creates one or more WorkSpaces. This operation is asynchronous and returns before the WorkSpaces are created.    The MANUAL running mode value is only supported by Amazon WorkSpaces Core. Contact your account team to be allow-listed to use this value. For more information, see Amazon WorkSpaces Core.   You don't need to specify the PCOIP protocol for Linux bundles because WSP is the default protocol for those bundles.   User-decoupled WorkSpaces are only supported by Amazon WorkSpaces Core.   Review your running mode to ensure you are using one that is optimal for your needs and budget. For more information on switching running modes, see  Can I switch between hourly and monthly billing? |
| POST | / | Creates a pool of WorkSpaces. |
| POST | / | Deletes the account link invitation. |
| POST | / | Deletes customized client branding. Client branding allows you to customize your WorkSpace's client login portal. You can tailor your login portal company logo, the support email address, support link, link to reset password, and a custom message for users trying to sign in. After you delete your customized client branding, your login portal reverts to the default client branding. |
| POST | / | Deletes a client-add-in for Amazon Connect that is configured within a directory. |
| POST | / | Deletes the specified connection alias. For more information, see  Cross-Region Redirection for Amazon WorkSpaces.   If you will no longer be using a fully qualified domain name (FQDN) as the registration code for your WorkSpaces users, you must take certain precautions to prevent potential security issues. For more information, see  Security Considerations if You Stop Using Cross-Region Redirection.   To delete a connection alias that has been shared, the shared account must first disassociate the connection alias from any directories it has been associated with. Then you must unshare the connection alias from the account it has been shared with. You can delete a connection alias only after it is no longer shared with any accounts or associated with any directories. |
| POST | / | Deletes the specified IP access control group. You cannot delete an IP access control group that is associated with a directory. |
| POST | / | Deletes the specified tags from the specified WorkSpaces resource. |
| POST | / | Deletes the specified WorkSpace bundle. For more information about deleting WorkSpace bundles, see  Delete a Custom WorkSpaces Bundle or Image. |
| POST | / | Deletes the specified image from your account. To delete an image, you must first delete any bundles that are associated with the image and unshare the image if it is shared with other accounts. |
| POST | / | Deploys associated applications to the specified WorkSpace |
| POST | / | Deregisters the specified directory. This operation is asynchronous and returns before the WorkSpace directory is deregistered. If any WorkSpaces are registered to this directory, you must remove them before you can deregister the directory.  Simple AD and AD Connector are made available to you free of charge to use with WorkSpaces. If there are no WorkSpaces being used with your Simple AD or AD Connector directory for 30 consecutive days, this directory will be automatically deregistered for use with Amazon WorkSpaces, and you will be charged for this directory as per the Directory Service pricing terms. To delete empty directories, see  Delete the Directory for Your WorkSpaces. If you delete your Simple AD or AD Connector directory, you can always create a new one when you want to start using WorkSpaces again. |
| POST | / | Retrieves a list that describes the configuration of Bring Your Own License (BYOL) for the specified account. |
| POST | / | Retrieves a list that describes modifications to the configuration of Bring Your Own License (BYOL) for the specified account. |
| POST | / | Describes the associations between the application and the specified associated resources. |
| POST | / | Describes the specified applications by filtering based on their compute types, license availability, operating systems, and owners. |
| POST | / | Describes the associations between the applications and the specified bundle. |
| POST | / | Describes the specified client branding. Client branding allows you to customize the log in page of various device types for your users. You can add your company logo, the support email address, support link, link to reset password, and a custom message for users trying to sign in.  Only device types that have branding information configured will be shown in the response. |
| POST | / | Retrieves a list that describes one or more specified Amazon WorkSpaces clients. |
| POST | / | Retrieves a list of Amazon Connect client add-ins that have been created. |
| POST | / | Describes the permissions that the owner of a connection alias has granted to another Amazon Web Services account for the specified connection alias. For more information, see  Cross-Region Redirection for Amazon WorkSpaces. |
| POST | / | Retrieves a list that describes the connection aliases used for cross-Region redirection. For more information, see  Cross-Region Redirection for Amazon WorkSpaces. |
| POST | / | Describes the associations between the applications and the specified image. |
| POST | / | Describes one or more of your IP access control groups. |
| POST | / | Describes the specified tags for the specified WorkSpaces resource. |
| POST | / | Describes the associations betweens applications and the specified WorkSpace. |
| POST | / | Retrieves a list that describes the available WorkSpace bundles. You can filter the results using either bundle ID or owner, but not both. |
| POST | / | Describes the available directories that are registered with Amazon WorkSpaces. |
| POST | / | Describes the permissions that the owner of an image has granted to other Amazon Web Services accounts for an image. |
| POST | / | Retrieves a list that describes one or more specified images, if the image identifiers are provided. Otherwise, all images in the account are described. |
| POST | / | Describes the snapshots for the specified WorkSpace. |
| POST | / | Describes the specified WorkSpaces. You can filter the results by using the bundle identifier, directory identifier, or owner, but you can specify only one filter at a time. |
| POST | / | Describes the connection status of the specified WorkSpaces. |
| POST | / | Retrieves a list that describes the streaming sessions for a specified pool. |
| POST | / | Describes the specified WorkSpaces Pools. |
| POST | / | Disassociates a connection alias from a directory. Disassociating a connection alias disables cross-Region redirection between two directories in different Regions. For more information, see  Cross-Region Redirection for Amazon WorkSpaces.  Before performing this operation, call  DescribeConnectionAliases to make sure that the current state of the connection alias is CREATED. |
| POST | / | Disassociates the specified IP access control group from the specified directory. |
| POST | / | Disassociates the specified application from a WorkSpace. |
| POST | / | Retrieves account link information. |
| POST | / | Imports client branding. Client branding allows you to customize your WorkSpace's client login portal. You can tailor your login portal company logo, the support email address, support link, link to reset password, and a custom message for users trying to sign in. After you import client branding, the default branding experience for the specified platform type is replaced with the imported experience    You must specify at least one platform type when importing client branding.   You can import up to 6 MB of data with each request. If your request exceeds this limit, you can import client branding for different platform types using separate requests.   In each platform type, the SupportEmail and SupportLink parameters are mutually exclusive. You can specify only one parameter for each platform type, but not both.   Imported data can take up to a minute to appear in the WorkSpaces client. |
| POST | / | Imports the specified Windows 10 or 11 Bring Your Own License (BYOL) image into Amazon WorkSpaces. The image must be an already licensed Amazon EC2 image that is in your Amazon Web Services account, and you must own the image. For more information about creating BYOL images, see  Bring Your Own Windows Desktop Licenses. |
| POST | / | Lists all account links. |
| POST | / | Retrieves a list of IP address ranges, specified as IPv4 CIDR blocks, that you can use for the network management interface when you enable Bring Your Own License (BYOL).  This operation can be run only by Amazon Web Services accounts that are enabled for BYOL. If your account isn't enabled for BYOL, you'll receive an AccessDeniedException error. The management network interface is connected to a secure Amazon WorkSpaces management network. It is used for interactive streaming of the WorkSpace desktop to Amazon WorkSpaces clients, and to allow Amazon WorkSpaces to manage the WorkSpace. |
| POST | / | Migrates a WorkSpace from one operating system or bundle type to another, while retaining the data on the user volume. The migration process recreates the WorkSpace by using a new root volume from the target bundle image and the user volume from the last available snapshot of the original WorkSpace. During migration, the original D:\Users\%USERNAME% user profile folder is renamed to D:\Users\%USERNAME%MMddyyTHHmmss%.NotMigrated. A new D:\Users\%USERNAME%\ folder is generated by the new OS. Certain files in the old user profile are moved to the new user profile. For available migration scenarios, details about what happens during migration, and best practices, see Migrate a WorkSpace. |
| POST | / | Modifies the configuration of Bring Your Own License (BYOL) for the specified account. |
| POST | / | Modifies the properties of the certificate-based authentication you want to use with your WorkSpaces. |
| POST | / | Modifies the properties of the specified Amazon WorkSpaces clients. |
| POST | / | Modifies multiple properties related to SAML 2.0 authentication, including the enablement status, user access URL, and relay state parameter name that are used for configuring federation with an SAML 2.0 identity provider. |
| POST | / | Modifies the self-service WorkSpace management capabilities for your users. For more information, see Enable Self-Service WorkSpace Management Capabilities for Your Users. |
| POST | / | Modifies the specified streaming properties. |
| POST | / | Specifies which devices and operating systems users can use to access their WorkSpaces. For more information, see  Control Device Access. |
| POST | / | Modify the default properties used to create WorkSpaces. |
| POST | / | Modifies the specified WorkSpace properties. For important information about how to modify the size of the root and user volumes, see  Modify a WorkSpace.   The MANUAL running mode value is only supported by Amazon WorkSpaces Core. Contact your account team to be allow-listed to use this value. For more information, see Amazon WorkSpaces Core. |
| POST | / | Sets the state of the specified WorkSpace. To maintain a WorkSpace without being interrupted, set the WorkSpace state to ADMIN_MAINTENANCE. WorkSpaces in this state do not respond to requests to reboot, stop, start, rebuild, or restore. An AutoStop WorkSpace in this state is not stopped. Users cannot log into a WorkSpace in the ADMIN_MAINTENANCE state. |
| POST | / | Reboots the specified WorkSpaces. You cannot reboot a WorkSpace unless its state is AVAILABLE, UNHEALTHY, or REBOOTING. Reboot a WorkSpace in the REBOOTING state only if your WorkSpace has been stuck in the REBOOTING state for over 20 minutes. This operation is asynchronous and returns before the WorkSpaces have rebooted. |
| POST | / | Rebuilds the specified WorkSpace. You cannot rebuild a WorkSpace unless its state is AVAILABLE, ERROR, UNHEALTHY, STOPPED, or REBOOTING. Rebuilding a WorkSpace is a potentially destructive action that can result in the loss of data. For more information, see Rebuild a WorkSpace. This operation is asynchronous and returns before the WorkSpaces have been completely rebuilt. |
| POST | / | Registers the specified directory. This operation is asynchronous and returns before the WorkSpace directory is registered. If this is the first time you are registering a directory, you will need to create the workspaces_DefaultRole role before you can register a directory. For more information, see  Creating the workspaces_DefaultRole Role. |
| POST | / | Rejects the account link invitation. |
| POST | / | Restores the specified WorkSpace to its last known healthy state. You cannot restore a WorkSpace unless its state is  AVAILABLE, ERROR, UNHEALTHY, or STOPPED. Restoring a WorkSpace is a potentially destructive action that can result in the loss of data. For more information, see Restore a WorkSpace. This operation is asynchronous and returns before the WorkSpace is completely restored. |
| POST | / | Removes one or more rules from the specified IP access control group. |
| POST | / | Starts the specified WorkSpaces. You cannot start a WorkSpace unless it has a running mode of AutoStop or Manual and a state of STOPPED. |
| POST | / | Starts the specified pool. You cannot start a pool unless it has a running mode of AutoStop and a state of STOPPED. |
| POST | / | Stops the specified WorkSpaces. You cannot stop a WorkSpace unless it has a running mode of AutoStop or Manual and a state of AVAILABLE, IMPAIRED, UNHEALTHY, or ERROR. |
| POST | / | Stops the specified pool. You cannot stop a WorkSpace pool unless it has a running mode of AutoStop and a state of AVAILABLE, IMPAIRED, UNHEALTHY, or ERROR. |
| POST | / | Terminates the specified WorkSpaces.  Terminating a WorkSpace is a permanent action and cannot be undone. The user's data is destroyed. If you need to archive any user data, contact Amazon Web Services Support before terminating the WorkSpace.  You can terminate a WorkSpace that is in any state except SUSPENDED. This operation is asynchronous and returns before the WorkSpaces have been completely terminated. After a WorkSpace is terminated, the TERMINATED state is returned only briefly before the WorkSpace directory metadata is cleaned up, so this state is rarely returned. To confirm that a WorkSpace is terminated, check for the WorkSpace ID by using  DescribeWorkSpaces. If the WorkSpace ID isn't returned, then the WorkSpace has been successfully terminated.  Simple AD and AD Connector are made available to you free of charge to use with WorkSpaces. If there are no WorkSpaces being used with your Simple AD or AD Connector directory for 30 consecutive days, this directory will be automatically deregistered for use with Amazon WorkSpaces, and you will be charged for this directory as per the Directory Service pricing terms. To delete empty directories, see  Delete the Directory for Your WorkSpaces. If you delete your Simple AD or AD Connector directory, you can always create a new one when you want to start using WorkSpaces again. |
| POST | / | Terminates the specified pool. |
| POST | / | Terminates the pool session. |
| POST | / | Updates a Amazon Connect client add-in. Use this action to update the name and endpoint URL of a Amazon Connect client add-in. |
| POST | / | Shares or unshares a connection alias with one account by specifying whether that account has permission to associate the connection alias with a directory. If the association permission is granted, the connection alias is shared with that account. If the association permission is revoked, the connection alias is unshared with the account. For more information, see  Cross-Region Redirection for Amazon WorkSpaces.    Before performing this operation, call  DescribeConnectionAliases to make sure that the current state of the connection alias is CREATED.   To delete a connection alias that has been shared, the shared account must first disassociate the connection alias from any directories it has been associated with. Then you must unshare the connection alias from the account it has been shared with. You can delete a connection alias only after it is no longer shared with any accounts or associated with any directories. |
| POST | / | Replaces the current rules of the specified IP access control group with the specified rules. |
| POST | / | Updates a WorkSpace bundle with a new image. For more information about updating WorkSpace bundles, see  Update a Custom WorkSpaces Bundle.  Existing WorkSpaces aren't automatically updated when you update the bundle that they're based on. To update existing WorkSpaces that are based on a bundle that you've updated, you must either rebuild the WorkSpaces or delete and recreate them. |
| POST | / | Shares or unshares an image with one account in the same Amazon Web Services Region by specifying whether that account has permission to copy the image. If the copy image permission is granted, the image is shared with that account. If the copy image permission is revoked, the image is unshared with the account. After an image has been shared, the recipient account can copy the image to other Regions as needed. In the China (Ningxia) Region, you can copy images only within the same Region. In Amazon Web Services GovCloud (US), to copy images to and from other Regions, contact Amazon Web Services Support. For more information about sharing images, see  Share or Unshare a Custom WorkSpaces Image.    To delete an image that has been shared, you must unshare the image before you delete it.   Sharing Bring Your Own License (BYOL) images across Amazon Web Services accounts isn't supported at this time in Amazon Web Services GovCloud (US). To share BYOL images across accounts in Amazon Web Services GovCloud (US), contact Amazon Web Services Support. |
| POST | / | Updates the specified pool. |

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
