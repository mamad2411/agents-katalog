---
name: amazon-appstream
description: "Amazon AppStream API skill. Use when working with Amazon AppStream for root. Covers 79 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon AppStream
API version: 2016-12-01

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST / -- create first resource

## Endpoints

79 endpoints across 1 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| POST | / | Associates the specified app block builder with the specified app block. |
| POST | / | Associates the specified application with the specified fleet. This is only supported for Elastic fleets. |
| POST | / | Associates an application to entitle. |
| POST | / | Associates the specified fleet with the specified stack. |
| POST | / | Associates the specified users with the specified stacks. Users in a user pool cannot be assigned to stacks with fleets that are joined to an Active Directory domain. |
| POST | / | Disassociates the specified users from the specified stacks. |
| POST | / | Copies the image within the same region or to a new region within the same AWS account. Note that any tags you added to the image will not be copied. |
| POST | / | Creates an app block. App blocks are an Amazon AppStream 2.0 resource that stores the details about the virtual hard disk in an S3 bucket. It also stores the setup script with details about how to mount the virtual hard disk. The virtual hard disk includes the application binaries and other files necessary to launch your applications. Multiple applications can be assigned to a single app block. This is only supported for Elastic fleets. |
| POST | / | Creates an app block builder. |
| POST | / | Creates a URL to start a create app block builder streaming session. |
| POST | / | Creates an application. Applications are an Amazon AppStream 2.0 resource that stores the details about how to launch applications on Elastic fleet streaming instances. An application consists of the launch details, icon, and display name. Applications are associated with an app block that contains the application binaries and other files. The applications assigned to an Elastic fleet are the applications users can launch.  This is only supported for Elastic fleets. |
| POST | / | Creates a Directory Config object in AppStream 2.0. This object includes the configuration information required to join fleets and image builders to Microsoft Active Directory domains. |
| POST | / | Creates a new entitlement. Entitlements control access to specific applications within a stack, based on user attributes. Entitlements apply to SAML 2.0 federated user identities. Amazon AppStream 2.0 user pool and streaming URL users are entitled to all applications in a stack. Entitlements don't apply to the desktop stream view application, or to applications managed by a dynamic app provider using the Dynamic Application Framework. |
| POST | / | Creates a fleet. A fleet consists of streaming instances that your users access for their applications and desktops. |
| POST | / | Creates an image builder. An image builder is a virtual machine that is used to create an image. The initial state of the builder is PENDING. When it is ready, the state is RUNNING. |
| POST | / | Creates a URL to start an image builder streaming session. |
| POST | / | Creates a stack to start streaming applications to users. A stack consists of an associated fleet, user access policies, and storage configurations. |
| POST | / | Creates a temporary URL to start an AppStream 2.0 streaming session for the specified user. A streaming URL enables application streaming to be tested without user setup. |
| POST | / | Creates custom branding that customizes the appearance of the streaming application catalog page. |
| POST | / | Creates a new image with the latest Windows operating system updates, driver updates, and AppStream 2.0 agent software. For more information, see the "Update an Image by Using Managed AppStream 2.0 Image Updates" section in Administer Your AppStream 2.0 Images, in the Amazon AppStream 2.0 Administration Guide. |
| POST | / | Creates a usage report subscription. Usage reports are generated daily. |
| POST | / | Creates a new user in the user pool. |
| POST | / | Deletes an app block. |
| POST | / | Deletes an app block builder. An app block builder can only be deleted when it has no association with an app block. |
| POST | / | Deletes an application. |
| POST | / | Deletes the specified Directory Config object from AppStream 2.0. This object includes the information required to join streaming instances to an Active Directory domain. |
| POST | / | Deletes the specified entitlement. |
| POST | / | Deletes the specified fleet. |
| POST | / | Deletes the specified image. You cannot delete an image when it is in use. After you delete an image, you cannot provision new capacity using the image. |
| POST | / | Deletes the specified image builder and releases the capacity. |
| POST | / | Deletes permissions for the specified private image. After you delete permissions for an image, AWS accounts to which you previously granted these permissions can no longer use the image. |
| POST | / | Deletes the specified stack. After the stack is deleted, the application streaming environment provided by the stack is no longer available to users. Also, any reservations made for application streaming sessions for the stack are released. |
| POST | / | Deletes custom branding that customizes the appearance of the streaming application catalog page. |
| POST | / | Disables usage report generation. |
| POST | / | Deletes a user from the user pool. |
| POST | / | Retrieves a list that describes one or more app block builder associations. |
| POST | / | Retrieves a list that describes one or more app block builders. |
| POST | / | Retrieves a list that describes one or more app blocks. |
| POST | / | Retrieves a list that describes one or more application fleet associations. Either ApplicationArn or FleetName must be specified. |
| POST | / | Retrieves a list that describes one or more applications. |
| POST | / | Retrieves a list that describes one or more specified Directory Config objects for AppStream 2.0, if the names for these objects are provided. Otherwise, all Directory Config objects in the account are described. These objects include the configuration information required to join fleets and image builders to Microsoft Active Directory domains.  Although the response syntax in this topic includes the account password, this password is not returned in the actual response. |
| POST | / | Retrieves a list that describes one of more entitlements. |
| POST | / | Retrieves a list that describes one or more specified fleets, if the fleet names are provided. Otherwise, all fleets in the account are described. |
| POST | / | Retrieves a list that describes one or more specified image builders, if the image builder names are provided. Otherwise, all image builders in the account are described. |
| POST | / | Retrieves a list that describes the permissions for shared AWS account IDs on a private image that you own. |
| POST | / | Retrieves a list that describes one or more specified images, if the image names or image ARNs are provided. Otherwise, all images in the account are described. |
| POST | / | Retrieves a list that describes the streaming sessions for a specified stack and fleet. If a UserId is provided for the stack and fleet, only streaming sessions for that user are described. If an authentication type is not provided, the default is to authenticate users using a streaming URL. |
| POST | / | Retrieves a list that describes one or more specified stacks, if the stack names are provided. Otherwise, all stacks in the account are described. |
| POST | / | Retrieves a list that describes the theme for a specified stack. A theme is custom branding that customizes the appearance of the streaming application catalog page. |
| POST | / | Retrieves a list that describes one or more usage report subscriptions. |
| POST | / | Retrieves a list that describes the UserStackAssociation objects. You must specify either or both of the following:   The stack name   The user name (email address of the user associated with the stack) and the authentication type for the user |
| POST | / | Retrieves a list that describes one or more specified users in the user pool. |
| POST | / | Disables the specified user in the user pool. Users can't sign in to AppStream 2.0 until they are re-enabled. This action does not delete the user. |
| POST | / | Disassociates a specified app block builder from a specified app block. |
| POST | / | Disassociates the specified application from the fleet. |
| POST | / | Deletes the specified application from the specified entitlement. |
| POST | / | Disassociates the specified fleet from the specified stack. |
| POST | / | Enables a user in the user pool. After being enabled, users can sign in to AppStream 2.0 and open applications from the stacks to which they are assigned. |
| POST | / | Immediately stops the specified streaming session. |
| POST | / | Retrieves the name of the fleet that is associated with the specified stack. |
| POST | / | Retrieves the name of the stack with which the specified fleet is associated. |
| POST | / | Retrieves a list of entitled applications. |
| POST | / | Retrieves a list of all tags for the specified AppStream 2.0 resource. You can tag AppStream 2.0 image builders, images, fleets, and stacks. For more information about tags, see Tagging Your Resources in the Amazon AppStream 2.0 Administration Guide. |
| POST | / | Starts an app block builder. An app block builder can only be started when it's associated with an app block. Starting an app block builder starts a new instance, which is equivalent to an elastic fleet instance with application builder assistance functionality. |
| POST | / | Starts the specified fleet. |
| POST | / | Starts the specified image builder. |
| POST | / | Stops an app block builder. Stopping an app block builder terminates the instance, and the instance state is not persisted. |
| POST | / | Stops the specified fleet. |
| POST | / | Stops the specified image builder. |
| POST | / | Adds or overwrites one or more tags for the specified AppStream 2.0 resource. You can tag AppStream 2.0 image builders, images, fleets, and stacks. Each tag consists of a key and an optional value. If a resource already has a tag with the same key, this operation updates its value. To list the current tags for your resources, use ListTagsForResource. To disassociate tags from your resources, use UntagResource. For more information about tags, see Tagging Your Resources in the Amazon AppStream 2.0 Administration Guide. |
| POST | / | Disassociates one or more specified tags from the specified AppStream 2.0 resource. To list the current tags for your resources, use ListTagsForResource. For more information about tags, see Tagging Your Resources in the Amazon AppStream 2.0 Administration Guide. |
| POST | / | Updates an app block builder. If the app block builder is in the STARTING or STOPPING state, you can't update it. If the app block builder is in the RUNNING state, you can only update the DisplayName and Description. If the app block builder is in the STOPPED state, you can update any attribute except the Name. |
| POST | / | Updates the specified application. |
| POST | / | Updates the specified Directory Config object in AppStream 2.0. This object includes the configuration information required to join fleets and image builders to Microsoft Active Directory domains. |
| POST | / | Updates the specified entitlement. |
| POST | / | Updates the specified fleet. If the fleet is in the STOPPED state, you can update any attribute except the fleet name. If the fleet is in the RUNNING state, you can update the following based on the fleet type:   Always-On and On-Demand fleet types You can update the DisplayName, ComputeCapacity, ImageARN, ImageName, IdleDisconnectTimeoutInSeconds, and DisconnectTimeoutInSeconds attributes.   Elastic fleet type You can update the DisplayName, IdleDisconnectTimeoutInSeconds, DisconnectTimeoutInSeconds, MaxConcurrentSessions, SessionScriptS3Location and UsbDeviceFilterStrings attributes.   If the fleet is in the STARTING or STOPPED state, you can't update it. |
| POST | / | Adds or updates permissions for the specified private image. |
| POST | / | Updates the specified fields for the specified stack. |
| POST | / | Updates custom branding that customizes the appearance of the streaming application catalog page. |

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
