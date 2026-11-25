---
name: amazon-simple-email-service
description: "Amazon Simple Email Service API skill. Use when working with Amazon Simple Email Service for email. Covers 92 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon Simple Email Service
API version: 2019-09-27

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /v2/email/account -- verify access
3. POST /v2/email/metrics/batch -- create first batch

## Endpoints

92 endpoints across 1 groups. See references/api-spec.lap for full details.

### email
| Method | Path | Description |
|--------|------|-------------|
| POST | /v2/email/metrics/batch | Retrieves batches of metric data collected based on your sending activity. You can execute this operation no more than 16 times per second, and with at most 160 queries from the batches per second (cumulative). |
| PUT | /v2/email/export-jobs/{JobId}/cancel | Cancels an export job. |
| POST | /v2/email/configuration-sets | Create a configuration set. Configuration sets are groups of rules that you can apply to the emails that you send. You apply a configuration set to an email by specifying the name of the configuration set when you call the Amazon SES API v2. When you apply a configuration set to an email, all of the rules in that configuration set are applied to the email. |
| POST | /v2/email/configuration-sets/{ConfigurationSetName}/event-destinations | Create an event destination. Events include message sends, deliveries, opens, clicks, bounces, and complaints. Event destinations are places that you can send information about these events to. For example, you can send event data to Amazon EventBridge and associate a rule to send the event to the specified target. A single configuration set can include more than one event destination. |
| POST | /v2/email/contact-lists/{ContactListName}/contacts | Creates a contact, which is an end-user who is receiving the email, and adds them to a contact list. |
| POST | /v2/email/contact-lists | Creates a contact list. |
| POST | /v2/email/custom-verification-email-templates | Creates a new custom verification email template. For more information about custom verification email templates, see Using custom verification email templates in the Amazon SES Developer Guide. You can execute this operation no more than once per second. |
| POST | /v2/email/dedicated-ip-pools | Create a new pool of dedicated IP addresses. A pool can include one or more dedicated IP addresses that are associated with your Amazon Web Services account. You can associate a pool with a configuration set. When you send an email that uses that configuration set, the message is sent from one of the addresses in the associated pool. |
| POST | /v2/email/deliverability-dashboard/test | Create a new predictive inbox placement test. Predictive inbox placement tests can help you predict how your messages will be handled by various email providers around the world. When you perform a predictive inbox placement test, you provide a sample message that contains the content that you plan to send to your customers. Amazon SES then sends that message to special email addresses spread across several major email providers. After about 24 hours, the test is complete, and you can use the GetDeliverabilityTestReport operation to view the results of the test. |
| POST | /v2/email/identities | Starts the process of verifying an email identity. An identity is an email address or domain that you use when you send email. Before you can use an identity to send email, you first have to verify it. By verifying an identity, you demonstrate that you're the owner of the identity, and that you've given Amazon SES API v2 permission to send email from the identity. When you verify an email address, Amazon SES sends an email to the address. Your email address is verified as soon as you follow the link in the verification email.  When you verify a domain without specifying the DkimSigningAttributes object, this operation provides a set of DKIM tokens. You can convert these tokens into CNAME records, which you then add to the DNS configuration for your domain. Your domain is verified when Amazon SES detects these records in the DNS configuration for your domain. This verification method is known as Easy DKIM. Alternatively, you can perform the verification process by providing your own public-private key pair. This verification method is known as Bring Your Own DKIM (BYODKIM). To use BYODKIM, your call to the CreateEmailIdentity operation has to include the DkimSigningAttributes object. When you specify this object, you provide a selector (a component of the DNS record name that identifies the public key to use for DKIM authentication) and a private key. When you verify a domain, this operation provides a set of DKIM tokens, which you can convert into CNAME tokens. You add these CNAME tokens to the DNS configuration for your domain. Your domain is verified when Amazon SES detects these records in the DNS configuration for your domain. For some DNS providers, it can take 72 hours or more to complete the domain verification process. Additionally, you can associate an existing configuration set with the email identity that you're verifying. |
| POST | /v2/email/identities/{EmailIdentity}/policies/{PolicyName} | Creates the specified sending authorization policy for the given identity (an email address or a domain).  This API is for the identity owner only. If you have not verified the identity, this API will return an error.  Sending authorization is a feature that enables an identity owner to authorize other senders to use its identities. For information about using sending authorization, see the Amazon SES Developer Guide. You can execute this operation no more than once per second. |
| POST | /v2/email/templates | Creates an email template. Email templates enable you to send personalized email to one or more destinations in a single API operation. For more information, see the Amazon SES Developer Guide. You can execute this operation no more than once per second. |
| POST | /v2/email/export-jobs | Creates an export job for a data source and destination. You can execute this operation no more than once per second. |
| POST | /v2/email/import-jobs | Creates an import job for a data destination. |
| DELETE | /v2/email/configuration-sets/{ConfigurationSetName} | Delete an existing configuration set.  Configuration sets are groups of rules that you can apply to the emails you send. You apply a configuration set to an email by including a reference to the configuration set in the headers of the email. When you apply a configuration set to an email, all of the rules in that configuration set are applied to the email. |
| DELETE | /v2/email/configuration-sets/{ConfigurationSetName}/event-destinations/{EventDestinationName} | Delete an event destination.  Events include message sends, deliveries, opens, clicks, bounces, and complaints. Event destinations are places that you can send information about these events to. For example, you can send event data to Amazon EventBridge and associate a rule to send the event to the specified target. |
| DELETE | /v2/email/contact-lists/{ContactListName}/contacts/{EmailAddress} | Removes a contact from a contact list. |
| DELETE | /v2/email/contact-lists/{ContactListName} | Deletes a contact list and all of the contacts on that list. |
| DELETE | /v2/email/custom-verification-email-templates/{TemplateName} | Deletes an existing custom verification email template. For more information about custom verification email templates, see Using custom verification email templates in the Amazon SES Developer Guide. You can execute this operation no more than once per second. |
| DELETE | /v2/email/dedicated-ip-pools/{PoolName} | Delete a dedicated IP pool. |
| DELETE | /v2/email/identities/{EmailIdentity} | Deletes an email identity. An identity can be either an email address or a domain name. |
| DELETE | /v2/email/identities/{EmailIdentity}/policies/{PolicyName} | Deletes the specified sending authorization policy for the given identity (an email address or a domain). This API returns successfully even if a policy with the specified name does not exist.  This API is for the identity owner only. If you have not verified the identity, this API will return an error.  Sending authorization is a feature that enables an identity owner to authorize other senders to use its identities. For information about using sending authorization, see the Amazon SES Developer Guide. You can execute this operation no more than once per second. |
| DELETE | /v2/email/templates/{TemplateName} | Deletes an email template. You can execute this operation no more than once per second. |
| DELETE | /v2/email/suppression/addresses/{EmailAddress} | Removes an email address from the suppression list for your account. |
| GET | /v2/email/account | Obtain information about the email-sending status and capabilities of your Amazon SES account in the current Amazon Web Services Region. |
| GET | /v2/email/deliverability-dashboard/blacklist-report | Retrieve a list of the blacklists that your dedicated IP addresses appear on. |
| GET | /v2/email/configuration-sets/{ConfigurationSetName} | Get information about an existing configuration set, including the dedicated IP pool that it's associated with, whether or not it's enabled for sending email, and more.  Configuration sets are groups of rules that you can apply to the emails you send. You apply a configuration set to an email by including a reference to the configuration set in the headers of the email. When you apply a configuration set to an email, all of the rules in that configuration set are applied to the email. |
| GET | /v2/email/configuration-sets/{ConfigurationSetName}/event-destinations | Retrieve a list of event destinations that are associated with a configuration set.  Events include message sends, deliveries, opens, clicks, bounces, and complaints. Event destinations are places that you can send information about these events to. For example, you can send event data to Amazon EventBridge and associate a rule to send the event to the specified target. |
| GET | /v2/email/contact-lists/{ContactListName}/contacts/{EmailAddress} | Returns a contact from a contact list. |
| GET | /v2/email/contact-lists/{ContactListName} | Returns contact list metadata. It does not return any information about the contacts present in the list. |
| GET | /v2/email/custom-verification-email-templates/{TemplateName} | Returns the custom email verification template for the template name you specify. For more information about custom verification email templates, see Using custom verification email templates in the Amazon SES Developer Guide. You can execute this operation no more than once per second. |
| GET | /v2/email/dedicated-ips/{IP} | Get information about a dedicated IP address, including the name of the dedicated IP pool that it's associated with, as well information about the automatic warm-up process for the address. |
| GET | /v2/email/dedicated-ip-pools/{PoolName} | Retrieve information about the dedicated pool. |
| GET | /v2/email/dedicated-ips | List the dedicated IP addresses that are associated with your Amazon Web Services account. |
| GET | /v2/email/deliverability-dashboard | Retrieve information about the status of the Deliverability dashboard for your account. When the Deliverability dashboard is enabled, you gain access to reputation, deliverability, and other metrics for the domains that you use to send email. You also gain the ability to perform predictive inbox placement tests. When you use the Deliverability dashboard, you pay a monthly subscription charge, in addition to any other fees that you accrue by using Amazon SES and other Amazon Web Services services. For more information about the features and cost of a Deliverability dashboard subscription, see Amazon SES Pricing. |
| GET | /v2/email/deliverability-dashboard/test-reports/{ReportId} | Retrieve the results of a predictive inbox placement test. |
| GET | /v2/email/deliverability-dashboard/campaigns/{CampaignId} | Retrieve all the deliverability data for a specific campaign. This data is available for a campaign only if the campaign sent email by using a domain that the Deliverability dashboard is enabled for. |
| GET | /v2/email/deliverability-dashboard/statistics-report/{Domain} | Retrieve inbox placement and engagement rates for the domains that you use to send email. |
| GET | /v2/email/identities/{EmailIdentity} | Provides information about a specific identity, including the identity's verification status, sending authorization policies, its DKIM authentication status, and its custom Mail-From settings. |
| GET | /v2/email/identities/{EmailIdentity}/policies | Returns the requested sending authorization policies for the given identity (an email address or a domain). The policies are returned as a map of policy names to policy contents. You can retrieve a maximum of 20 policies at a time.  This API is for the identity owner only. If you have not verified the identity, this API will return an error.  Sending authorization is a feature that enables an identity owner to authorize other senders to use its identities. For information about using sending authorization, see the Amazon SES Developer Guide. You can execute this operation no more than once per second. |
| GET | /v2/email/templates/{TemplateName} | Displays the template object (which includes the subject line, HTML part and text part) for the template you specify. You can execute this operation no more than once per second. |
| GET | /v2/email/export-jobs/{JobId} | Provides information about an export job. |
| GET | /v2/email/import-jobs/{JobId} | Provides information about an import job. |
| GET | /v2/email/insights/{MessageId}/ | Provides information about a specific message, including the from address, the subject, the recipient address, email tags, as well as events associated with the message. You can execute this operation no more than once per second. |
| GET | /v2/email/suppression/addresses/{EmailAddress} | Retrieves information about a specific email address that's on the suppression list for your account. |
| GET | /v2/email/configuration-sets | List all of the configuration sets associated with your account in the current region.  Configuration sets are groups of rules that you can apply to the emails you send. You apply a configuration set to an email by including a reference to the configuration set in the headers of the email. When you apply a configuration set to an email, all of the rules in that configuration set are applied to the email. |
| GET | /v2/email/contact-lists | Lists all of the contact lists available. |
| POST | /v2/email/contact-lists/{ContactListName}/contacts/list | Lists the contacts present in a specific contact list. |
| GET | /v2/email/custom-verification-email-templates | Lists the existing custom verification email templates for your account in the current Amazon Web Services Region. For more information about custom verification email templates, see Using custom verification email templates in the Amazon SES Developer Guide. You can execute this operation no more than once per second. |
| GET | /v2/email/dedicated-ip-pools | List all of the dedicated IP pools that exist in your Amazon Web Services account in the current Region. |
| GET | /v2/email/deliverability-dashboard/test-reports | Show a list of the predictive inbox placement tests that you've performed, regardless of their statuses. For predictive inbox placement tests that are complete, you can use the GetDeliverabilityTestReport operation to view the results. |
| GET | /v2/email/deliverability-dashboard/domains/{SubscribedDomain}/campaigns | Retrieve deliverability data for all the campaigns that used a specific domain to send email during a specified time range. This data is available for a domain only if you enabled the Deliverability dashboard for the domain. |
| GET | /v2/email/identities | Returns a list of all of the email identities that are associated with your Amazon Web Services account. An identity can be either an email address or a domain. This operation returns identities that are verified as well as those that aren't. This operation returns identities that are associated with Amazon SES and Amazon Pinpoint. |
| GET | /v2/email/templates | Lists the email templates present in your Amazon SES account in the current Amazon Web Services Region. You can execute this operation no more than once per second. |
| POST | /v2/email/list-export-jobs | Lists all of the export jobs. |
| POST | /v2/email/import-jobs/list | Lists all of the import jobs. |
| POST | /v2/email/vdm/recommendations | Lists the recommendations present in your Amazon SES account in the current Amazon Web Services Region. You can execute this operation no more than once per second. |
| GET | /v2/email/suppression/addresses | Retrieves a list of email addresses that are on the suppression list for your account. |
| GET | /v2/email/tags | Retrieve a list of the tags (keys and values) that are associated with a specified resource. A tag is a label that you optionally define and associate with a resource. Each tag consists of a required tag key and an optional associated tag value. A tag key is a general label that acts as a category for more specific tag values. A tag value acts as a descriptor within a tag key. |
| PUT | /v2/email/account/dedicated-ips/warmup | Enable or disable the automatic warm-up feature for dedicated IP addresses. |
| POST | /v2/email/account/details | Update your Amazon SES account details. |
| PUT | /v2/email/account/sending | Enable or disable the ability of your account to send email. |
| PUT | /v2/email/account/suppression | Change the settings for the account-level suppression list. |
| PUT | /v2/email/account/vdm | Update your Amazon SES account VDM attributes. You can execute this operation no more than once per second. |
| PUT | /v2/email/configuration-sets/{ConfigurationSetName}/delivery-options | Associate a configuration set with a dedicated IP pool. You can use dedicated IP pools to create groups of dedicated IP addresses for sending specific types of email. |
| PUT | /v2/email/configuration-sets/{ConfigurationSetName}/reputation-options | Enable or disable collection of reputation metrics for emails that you send using a particular configuration set in a specific Amazon Web Services Region. |
| PUT | /v2/email/configuration-sets/{ConfigurationSetName}/sending | Enable or disable email sending for messages that use a particular configuration set in a specific Amazon Web Services Region. |
| PUT | /v2/email/configuration-sets/{ConfigurationSetName}/suppression-options | Specify the account suppression list preferences for a configuration set. |
| PUT | /v2/email/configuration-sets/{ConfigurationSetName}/tracking-options | Specify a custom domain to use for open and click tracking elements in email that you send. |
| PUT | /v2/email/configuration-sets/{ConfigurationSetName}/vdm-options | Specify VDM preferences for email that you send using the configuration set. You can execute this operation no more than once per second. |
| PUT | /v2/email/dedicated-ips/{IP}/pool | Move a dedicated IP address to an existing dedicated IP pool.  The dedicated IP address that you specify must already exist, and must be associated with your Amazon Web Services account.  The dedicated IP pool you specify must already exist. You can create a new pool by using the CreateDedicatedIpPool operation. |
| PUT | /v2/email/dedicated-ip-pools/{PoolName}/scaling | Used to convert a dedicated IP pool to a different scaling mode.   MANAGED pools cannot be converted to STANDARD scaling mode. |
| PUT | /v2/email/dedicated-ips/{IP}/warmup |  |
| PUT | /v2/email/deliverability-dashboard | Enable or disable the Deliverability dashboard. When you enable the Deliverability dashboard, you gain access to reputation, deliverability, and other metrics for the domains that you use to send email. You also gain the ability to perform predictive inbox placement tests. When you use the Deliverability dashboard, you pay a monthly subscription charge, in addition to any other fees that you accrue by using Amazon SES and other Amazon Web Services services. For more information about the features and cost of a Deliverability dashboard subscription, see Amazon SES Pricing. |
| PUT | /v2/email/identities/{EmailIdentity}/configuration-set | Used to associate a configuration set with an email identity. |
| PUT | /v2/email/identities/{EmailIdentity}/dkim | Used to enable or disable DKIM authentication for an email identity. |
| PUT | /v1/email/identities/{EmailIdentity}/dkim/signing | Used to configure or change the DKIM authentication settings for an email domain identity. You can use this operation to do any of the following:   Update the signing attributes for an identity that uses Bring Your Own DKIM (BYODKIM).   Update the key length that should be used for Easy DKIM.   Change from using no DKIM authentication to using Easy DKIM.   Change from using no DKIM authentication to using BYODKIM.   Change from using Easy DKIM to using BYODKIM.   Change from using BYODKIM to using Easy DKIM. |
| PUT | /v2/email/identities/{EmailIdentity}/feedback | Used to enable or disable feedback forwarding for an identity. This setting determines what happens when an identity is used to send an email that results in a bounce or complaint event. If the value is true, you receive email notifications when bounce or complaint events occur. These notifications are sent to the address that you specified in the Return-Path header of the original email. You're required to have a method of tracking bounces and complaints. If you haven't set up another mechanism for receiving bounce or complaint notifications (for example, by setting up an event destination), you receive an email notification when these events occur (even if this setting is disabled). |
| PUT | /v2/email/identities/{EmailIdentity}/mail-from | Used to enable or disable the custom Mail-From domain configuration for an email identity. |
| PUT | /v2/email/suppression/addresses | Adds an email address to the suppression list for your account. |
| POST | /v2/email/outbound-bulk-emails | Composes an email message to multiple destinations. |
| POST | /v2/email/outbound-custom-verification-emails | Adds an email address to the list of identities for your Amazon SES account in the current Amazon Web Services Region and attempts to verify it. As a result of executing this operation, a customized verification email is sent to the specified address. To use this operation, you must first create a custom verification email template. For more information about creating and using custom verification email templates, see Using custom verification email templates in the Amazon SES Developer Guide. You can execute this operation no more than once per second. |
| POST | /v2/email/outbound-emails | Sends an email message. You can use the Amazon SES API v2 to send the following types of messages:    Simple – A standard email message. When you create this type of message, you specify the sender, the recipient, and the message body, and Amazon SES assembles the message for you.    Raw – A raw, MIME-formatted email message. When you send this type of email, you have to specify all of the message headers, as well as the message body. You can use this message type to send messages that contain attachments. The message that you specify has to be a valid MIME message.    Templated – A message that contains personalization tags. When you send this type of email, Amazon SES API v2 automatically replaces the tags with values that you specify. |
| POST | /v2/email/tags | Add one or more tags (keys and values) to a specified resource. A tag is a label that you optionally define and associate with a resource. Tags can help you categorize and manage resources in different ways, such as by purpose, owner, environment, or other criteria. A resource can have as many as 50 tags. Each tag consists of a required tag key and an associated tag value, both of which you define. A tag key is a general label that acts as a category for more specific tag values. A tag value acts as a descriptor within a tag key. |
| POST | /v2/email/templates/{TemplateName}/render | Creates a preview of the MIME content of an email when provided with a template and a set of replacement data. You can execute this operation no more than once per second. |
| DELETE | /v2/email/tags | Remove one or more tags (keys and values) from a specified resource. |
| PUT | /v2/email/configuration-sets/{ConfigurationSetName}/event-destinations/{EventDestinationName} | Update the configuration of an event destination for a configuration set.  Events include message sends, deliveries, opens, clicks, bounces, and complaints. Event destinations are places that you can send information about these events to. For example, you can send event data to Amazon EventBridge and associate a rule to send the event to the specified target. |
| PUT | /v2/email/contact-lists/{ContactListName}/contacts/{EmailAddress} | Updates a contact's preferences for a list.  You must specify all existing topic preferences in the TopicPreferences object, not just the ones that need updating; otherwise, all your existing preferences will be removed. |
| PUT | /v2/email/contact-lists/{ContactListName} | Updates contact list metadata. This operation does a complete replacement. |
| PUT | /v2/email/custom-verification-email-templates/{TemplateName} | Updates an existing custom verification email template. For more information about custom verification email templates, see Using custom verification email templates in the Amazon SES Developer Guide. You can execute this operation no more than once per second. |
| PUT | /v2/email/identities/{EmailIdentity}/policies/{PolicyName} | Updates the specified sending authorization policy for the given identity (an email address or a domain). This API returns successfully even if a policy with the specified name does not exist.  This API is for the identity owner only. If you have not verified the identity, this API will return an error.  Sending authorization is a feature that enables an identity owner to authorize other senders to use its identities. For information about using sending authorization, see the Amazon SES Developer Guide. You can execute this operation no more than once per second. |
| PUT | /v2/email/templates/{TemplateName} | Updates an email template. Email templates enable you to send personalized email to one or more destinations in a single API operation. For more information, see the Amazon SES Developer Guide. You can execute this operation no more than once per second. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a batch?" -> POST /v2/email/metrics/batch
- "Create a configuration-set?" -> POST /v2/email/configuration-sets
- "Create a event-destination?" -> POST /v2/email/configuration-sets/{ConfigurationSetName}/event-destinations
- "Create a contact?" -> POST /v2/email/contact-lists/{ContactListName}/contacts
- "Create a contact-list?" -> POST /v2/email/contact-lists
- "Create a custom-verification-email-template?" -> POST /v2/email/custom-verification-email-templates
- "Create a dedicated-ip-pool?" -> POST /v2/email/dedicated-ip-pools
- "Create a test?" -> POST /v2/email/deliverability-dashboard/test
- "Create a identity?" -> POST /v2/email/identities
- "Create a template?" -> POST /v2/email/templates
- "Create a export-job?" -> POST /v2/email/export-jobs
- "Create a import-job?" -> POST /v2/email/import-jobs
- "Delete a configuration-set?" -> DELETE /v2/email/configuration-sets/{ConfigurationSetName}
- "Delete a event-destination?" -> DELETE /v2/email/configuration-sets/{ConfigurationSetName}/event-destinations/{EventDestinationName}
- "Delete a contact?" -> DELETE /v2/email/contact-lists/{ContactListName}/contacts/{EmailAddress}
- "Delete a contact-list?" -> DELETE /v2/email/contact-lists/{ContactListName}
- "Delete a custom-verification-email-template?" -> DELETE /v2/email/custom-verification-email-templates/{TemplateName}
- "Delete a dedicated-ip-pool?" -> DELETE /v2/email/dedicated-ip-pools/{PoolName}
- "Delete a identity?" -> DELETE /v2/email/identities/{EmailIdentity}
- "Delete a policy?" -> DELETE /v2/email/identities/{EmailIdentity}/policies/{PolicyName}
- "Delete a template?" -> DELETE /v2/email/templates/{TemplateName}
- "Delete a address?" -> DELETE /v2/email/suppression/addresses/{EmailAddress}
- "List all account?" -> GET /v2/email/account
- "List all blacklist-report?" -> GET /v2/email/deliverability-dashboard/blacklist-report
- "Get configuration-set details?" -> GET /v2/email/configuration-sets/{ConfigurationSetName}
- "List all event-destinations?" -> GET /v2/email/configuration-sets/{ConfigurationSetName}/event-destinations
- "Get contact details?" -> GET /v2/email/contact-lists/{ContactListName}/contacts/{EmailAddress}
- "Get contact-list details?" -> GET /v2/email/contact-lists/{ContactListName}
- "Get custom-verification-email-template details?" -> GET /v2/email/custom-verification-email-templates/{TemplateName}
- "Get dedicated-ip details?" -> GET /v2/email/dedicated-ips/{IP}
- "Get dedicated-ip-pool details?" -> GET /v2/email/dedicated-ip-pools/{PoolName}
- "List all dedicated-ips?" -> GET /v2/email/dedicated-ips
- "List all deliverability-dashboard?" -> GET /v2/email/deliverability-dashboard
- "Get test-report details?" -> GET /v2/email/deliverability-dashboard/test-reports/{ReportId}
- "Get campaign details?" -> GET /v2/email/deliverability-dashboard/campaigns/{CampaignId}
- "Get statistics-report details?" -> GET /v2/email/deliverability-dashboard/statistics-report/{Domain}
- "Get identity details?" -> GET /v2/email/identities/{EmailIdentity}
- "List all policies?" -> GET /v2/email/identities/{EmailIdentity}/policies
- "Get template details?" -> GET /v2/email/templates/{TemplateName}
- "Get export-job details?" -> GET /v2/email/export-jobs/{JobId}
- "Get import-job details?" -> GET /v2/email/import-jobs/{JobId}
- "Get insight details?" -> GET /v2/email/insights/{MessageId}/
- "Get address details?" -> GET /v2/email/suppression/addresses/{EmailAddress}
- "List all configuration-sets?" -> GET /v2/email/configuration-sets
- "List all contact-lists?" -> GET /v2/email/contact-lists
- "Create a list?" -> POST /v2/email/contact-lists/{ContactListName}/contacts/list
- "List all custom-verification-email-templates?" -> GET /v2/email/custom-verification-email-templates
- "List all dedicated-ip-pools?" -> GET /v2/email/dedicated-ip-pools
- "List all test-reports?" -> GET /v2/email/deliverability-dashboard/test-reports
- "List all campaigns?" -> GET /v2/email/deliverability-dashboard/domains/{SubscribedDomain}/campaigns
- "List all identities?" -> GET /v2/email/identities
- "List all templates?" -> GET /v2/email/templates
- "Create a list-export-job?" -> POST /v2/email/list-export-jobs
- "Create a list?" -> POST /v2/email/import-jobs/list
- "Create a recommendation?" -> POST /v2/email/vdm/recommendations
- "List all addresses?" -> GET /v2/email/suppression/addresses
- "List all tags?" -> GET /v2/email/tags
- "Create a detail?" -> POST /v2/email/account/details
- "Create a outbound-bulk-email?" -> POST /v2/email/outbound-bulk-emails
- "Create a outbound-custom-verification-email?" -> POST /v2/email/outbound-custom-verification-emails
- "Create a outbound-email?" -> POST /v2/email/outbound-emails
- "Create a tag?" -> POST /v2/email/tags
- "Create a render?" -> POST /v2/email/templates/{TemplateName}/render
- "Update a event-destination?" -> PUT /v2/email/configuration-sets/{ConfigurationSetName}/event-destinations/{EventDestinationName}
- "Update a contact?" -> PUT /v2/email/contact-lists/{ContactListName}/contacts/{EmailAddress}
- "Update a contact-list?" -> PUT /v2/email/contact-lists/{ContactListName}
- "Update a custom-verification-email-template?" -> PUT /v2/email/custom-verification-email-templates/{TemplateName}
- "Update a policy?" -> PUT /v2/email/identities/{EmailIdentity}/policies/{PolicyName}
- "Update a template?" -> PUT /v2/email/templates/{TemplateName}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
