---
name: amazon-workmail
description: "Amazon WorkMail API skill. Use when working with Amazon WorkMail for root. Covers 84 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon WorkMail
API version: 2017-10-01

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST / -- create first resource

## Endpoints

84 endpoints across 1 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| POST | / | Adds a member (user or group) to the resource's set of delegates. |
| POST | / | Adds a member (user or group) to the group's set. |
| POST | / | Assumes an impersonation role for the given WorkMail organization. This method returns an authentication token you can use to make impersonated calls. |
| POST | / | Cancels a mailbox export job.  If the mailbox export job is near completion, it might not be possible to cancel it. |
| POST | / | Adds an alias to the set of a given member (user or group) of WorkMail. |
| POST | / | Creates an AvailabilityConfiguration for the given WorkMail organization and domain. |
| POST | / | Creates a group that can be used in WorkMail by calling the RegisterToWorkMail operation. |
| POST | / | Creates an impersonation role for the given WorkMail organization.  Idempotency ensures that an API request completes no more than one time. With an idempotent request, if the original request completes successfully, any subsequent retries also complete successfully without performing any further actions. |
| POST | / | Creates a new mobile device access rule for the specified WorkMail organization. |
| POST | / | Creates a new WorkMail organization. Optionally, you can choose to associate an existing AWS Directory Service directory with your organization. If an AWS Directory Service directory ID is specified, the organization alias must match the directory alias. If you choose not to associate an existing directory with your organization, then we create a new WorkMail directory for you. For more information, see Adding an organization in the WorkMail Administrator Guide. You can associate multiple email domains with an organization, then choose your default email domain from the WorkMail console. You can also associate a domain that is managed in an Amazon Route 53 public hosted zone. For more information, see Adding a domain and Choosing the default domain in the WorkMail Administrator Guide. Optionally, you can use a customer managed key from AWS Key Management Service (AWS KMS) to encrypt email for your organization. If you don't associate an AWS KMS key, WorkMail creates a default, AWS managed key for you. |
| POST | / | Creates a new WorkMail resource. |
| POST | / | Creates a user who can be used in WorkMail by calling the RegisterToWorkMail operation. |
| POST | / | Deletes an access control rule for the specified WorkMail organization.  Deleting already deleted and non-existing rules does not produce an error. In those cases, the service sends back an HTTP 200 response with an empty HTTP body. |
| POST | / | Remove one or more specified aliases from a set of aliases for a given user. |
| POST | / | Deletes the AvailabilityConfiguration for the given WorkMail organization and domain. |
| POST | / | Deletes the email monitoring configuration for a specified organization. |
| POST | / | Deletes a group from WorkMail. |
| POST | / | Deletes an impersonation role for the given WorkMail organization. |
| POST | / | Deletes permissions granted to a member (user or group). |
| POST | / | Deletes the mobile device access override for the given WorkMail organization, user, and device.  Deleting already deleted and non-existing overrides does not produce an error. In those cases, the service sends back an HTTP 200 response with an empty HTTP body. |
| POST | / | Deletes a mobile device access rule for the specified WorkMail organization.  Deleting already deleted and non-existing rules does not produce an error. In those cases, the service sends back an HTTP 200 response with an empty HTTP body. |
| POST | / | Deletes an WorkMail organization and all underlying AWS resources managed by WorkMail as part of the organization. You can choose whether to delete the associated directory. For more information, see Removing an organization in the WorkMail Administrator Guide. |
| POST | / | Deletes the specified resource. |
| POST | / | Deletes the specified retention policy from the specified organization. |
| POST | / | Deletes a user from WorkMail and all subsequent systems. Before you can delete a user, the user state must be DISABLED. Use the DescribeUser action to confirm the user state. Deleting a user is permanent and cannot be undone. WorkMail archives user mailboxes for 30 days before they are permanently removed. |
| POST | / | Mark a user, group, or resource as no longer used in WorkMail. This action disassociates the mailbox and schedules it for clean-up. WorkMail keeps mailboxes for 30 days before they are permanently removed. The functionality in the console is Disable. |
| POST | / | Removes a domain from WorkMail, stops email routing to WorkMail, and removes the authorization allowing WorkMail use. SES keeps the domain because other applications may use it. You must first remove any email address used by WorkMail entities before you remove the domain. |
| POST | / | Describes the current email monitoring configuration for a specified organization. |
| POST | / | Returns basic details about an entity in WorkMail. |
| POST | / | Returns the data available for the group. |
| POST | / | Lists the settings in a DMARC policy for a specified organization. |
| POST | / | Describes the current status of a mailbox export job. |
| POST | / | Provides more information regarding a given organization based on its identifier. |
| POST | / | Returns the data available for the resource. |
| POST | / | Provides information regarding the user. |
| POST | / | Removes a member from the resource's set of delegates. |
| POST | / | Removes a member from a group. |
| POST | / | Gets the effects of an organization's access control rules as they apply to a specified IPv4 address, access protocol action, and user ID or impersonation role ID. You must provide either the user ID or impersonation role ID. Impersonation role ID can only be used with Action EWS. |
| POST | / | Gets the default retention policy details for the specified organization. |
| POST | / | Gets the impersonation role details for the given WorkMail organization. |
| POST | / | Tests whether the given impersonation role can impersonate a target user. |
| POST | / | Gets details for a mail domain, including domain records required to configure your domain with recommended security. |
| POST | / | Requests a user's mailbox details for a specified organization and user. |
| POST | / | Simulates the effect of the mobile device access rules for the given attributes of a sample access event. Use this method to test the effects of the current set of mobile device access rules for the WorkMail organization for a particular user's attributes. |
| POST | / | Gets the mobile device access override for the given WorkMail organization, user, and device. |
| POST | / | Lists the access control rules for the specified organization. |
| POST | / | Creates a paginated call to list the aliases associated with a given entity. |
| POST | / | List all the AvailabilityConfiguration's for the given WorkMail organization. |
| POST | / | Returns an overview of the members of a group. Users and groups can be members of a group. |
| POST | / | Returns summaries of the organization's groups. |
| POST | / | Returns all the groups to which an entity belongs. |
| POST | / | Lists all the impersonation roles for the given WorkMail organization. |
| POST | / | Lists the mail domains in a given WorkMail organization. |
| POST | / | Lists the mailbox export jobs started for the specified organization within the last seven days. |
| POST | / | Lists the mailbox permissions associated with a user, group, or resource mailbox. |
| POST | / | Lists all the mobile device access overrides for any given combination of WorkMail organization, user, or device. |
| POST | / | Lists the mobile device access rules for the specified WorkMail organization. |
| POST | / | Returns summaries of the customer's organizations. |
| POST | / | Lists the delegates associated with a resource. Users and groups can be resource delegates and answer requests on behalf of the resource. |
| POST | / | Returns summaries of the organization's resources. |
| POST | / | Lists the tags applied to an WorkMail organization resource. |
| POST | / | Returns summaries of the organization's users. |
| POST | / | Adds a new access control rule for the specified organization. The rule allows or denies access to the organization for the specified IPv4 addresses, access protocol actions, user IDs and impersonation IDs. Adding a new rule with the same name as an existing rule replaces the older rule. |
| POST | / | Creates or updates the email monitoring configuration for a specified organization. |
| POST | / | Enables or disables a DMARC policy for a given organization. |
| POST | / | Sets permissions for a user, group, or resource. This replaces any pre-existing permissions. |
| POST | / | Creates or updates a mobile device access override for the given WorkMail organization, user, and device. |
| POST | / | Puts a retention policy to the specified organization. |
| POST | / | Registers a new domain in WorkMail and SES, and configures it for use by WorkMail. Emails received by SES for this domain are routed to the specified WorkMail organization, and WorkMail has permanent permission to use the specified domain for sending your users' emails. |
| POST | / | Registers an existing and disabled user, group, or resource for WorkMail use by associating a mailbox and calendaring capabilities. It performs no change if the user, group, or resource is enabled and fails if the user, group, or resource is deleted. This operation results in the accumulation of costs. For more information, see Pricing. The equivalent console functionality for this operation is Enable. Users can either be created by calling the CreateUser API operation or they can be synchronized from your directory. For more information, see DeregisterFromWorkMail. |
| POST | / | Allows the administrator to reset the password for a user. |
| POST | / | Starts a mailbox export job to export MIME-format email messages and calendar items from the specified mailbox to the specified Amazon Simple Storage Service (Amazon S3) bucket. For more information, see Exporting mailbox content in the WorkMail Administrator Guide. |
| POST | / | Applies the specified tags to the specified WorkMailorganization resource. |
| POST | / | Performs a test on an availability provider to ensure that access is allowed. For EWS, it verifies the provided credentials can be used to successfully log in. For Lambda, it verifies that the Lambda function can be invoked and that the resource access policy was configured to deny anonymous access. An anonymous invocation is one done without providing either a SourceArn or SourceAccount header.  The request must contain either one provider definition (EwsProvider or LambdaProvider) or the DomainName parameter. If the DomainName parameter is provided, the configuration stored under the DomainName will be tested. |
| POST | / | Untags the specified tags from the specified WorkMail organization resource. |
| POST | / | Updates an existing AvailabilityConfiguration for the given WorkMail organization and domain. |
| POST | / | Updates the default mail domain for an organization. The default mail domain is used by the WorkMail AWS Console to suggest an email address when enabling a mail user. You can only have one default domain. |
| POST | / | Updates attibutes in a group. |
| POST | / | Updates an impersonation role for the given WorkMail organization. |
| POST | / | Updates a user's current mailbox quota for a specified organization and user. |
| POST | / | Updates a mobile device access rule for the specified WorkMail organization. |
| POST | / | Updates the primary email for a user, group, or resource. The current email is moved into the list of aliases (or swapped between an existing alias and the current primary email), and the email provided in the input is promoted as the primary. |
| POST | / | Updates data for the resource. To have the latest information, it must be preceded by a DescribeResource call. The dataset in the request should be the one expected when performing another DescribeResource call. |
| POST | / | Updates data for the user. To have the latest information, it must be preceded by a DescribeUser call. The dataset in the request should be the one expected when performing another DescribeUser call. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
