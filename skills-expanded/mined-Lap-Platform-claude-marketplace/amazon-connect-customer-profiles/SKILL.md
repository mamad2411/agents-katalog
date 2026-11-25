---
name: amazon-connect-customer-profiles
description: "Amazon Connect Customer Profiles API skill. Use when working with Amazon Connect Customer Profiles for domains, templates, integrations. Covers 52 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon Connect Customer Profiles
API version: 2020-08-15

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /domains -- verify access
3. POST /domains/{DomainName}/profiles/keys -- create first keys

## Endpoints

52 endpoints across 4 groups. See references/api-spec.lap for full details.

### domains
| Method | Path | Description |
|--------|------|-------------|
| POST | /domains/{DomainName}/profiles/keys | Associates a new key value with a specific profile, such as a Contact Record ContactId. A profile object can have a single unique key and any number of additional keys that can be used to identify the profile that it belongs to. |
| POST | /domains/{DomainName}/calculated-attributes/{CalculatedAttributeName} | Creates a new calculated attribute definition. After creation, new object data ingested into Customer Profiles will be included in the calculated attribute, which can be retrieved for a profile using the GetCalculatedAttributeForProfile API. Defining a calculated attribute makes it available for all profiles within a domain. Each calculated attribute can only reference one ObjectType and at most, two fields from that ObjectType. |
| POST | /domains/{DomainName} | Creates a domain, which is a container for all customer data, such as customer profile attributes, object types, profile keys, and encryption keys. You can create multiple domains, and each domain can have multiple third-party integrations. Each Amazon Connect instance can be associated with only one domain. Multiple Amazon Connect instances can be associated with one domain. Use this API or UpdateDomain to enable identity resolution: set Matching to true. To prevent cross-service impersonation when you call this API, see Cross-service confused deputy prevention for sample policies that you should apply.   It is not possible to associate a Customer Profiles domain with an Amazon Connect Instance directly from the API. If you would like to create a domain and associate a Customer Profiles domain, use the Amazon Connect admin website. For more information, see Enable Customer Profiles. Each Amazon Connect instance can be associated with only one domain. Multiple Amazon Connect instances can be associated with one domain. |
| POST | /domains/{DomainName}/event-streams/{EventStreamName} | Creates an event stream, which is a subscription to real-time events, such as when profiles are created and updated through Amazon Connect Customer Profiles. Each event stream can be associated with only one Kinesis Data Stream destination in the same region and Amazon Web Services account as the customer profiles domain |
| POST | /domains/{DomainName}/workflows/integrations | Creates an integration workflow. An integration workflow is an async process which ingests historic data and sets up an integration for ongoing updates. The supported Amazon AppFlow sources are Salesforce, ServiceNow, and Marketo. |
| POST | /domains/{DomainName}/profiles | Creates a standard profile. A standard profile represents the following attributes for a customer profile in a domain. |
| DELETE | /domains/{DomainName}/calculated-attributes/{CalculatedAttributeName} | Deletes an existing calculated attribute definition. Note that deleting a default calculated attribute is possible, however once deleted, you will be unable to undo that action and will need to recreate it on your own using the CreateCalculatedAttributeDefinition API if you want it back. |
| DELETE | /domains/{DomainName} | Deletes a specific domain and all of its customer data, such as customer profile attributes and their related objects. |
| DELETE | /domains/{DomainName}/event-streams/{EventStreamName} | Disables and deletes the specified event stream. |
| POST | /domains/{DomainName}/integrations/delete | Removes an integration from a specific domain. |
| POST | /domains/{DomainName}/profiles/delete | Deletes the standard customer profile and all data pertaining to the profile. |
| POST | /domains/{DomainName}/profiles/keys/delete | Removes a searchable key from a customer profile. |
| POST | /domains/{DomainName}/profiles/objects/delete | Removes an object associated with a profile of a given ProfileObjectType. |
| DELETE | /domains/{DomainName}/object-types/{ObjectTypeName} | Removes a ProfileObjectType from a specific domain as well as removes all the ProfileObjects of that type. It also disables integrations from this specific ProfileObjectType. In addition, it scrubs all of the fields of the standard profile that were populated from this ProfileObjectType. |
| DELETE | /domains/{DomainName}/workflows/{WorkflowId} | Deletes the specified workflow and all its corresponding resources. This is an async process. |
| POST | /domains/{DomainName}/detect/object-types | The process of detecting profile object type mapping by using given objects. |
| POST | /domains/{DomainName}/identity-resolution-jobs/auto-merging-preview | Tests the auto-merging settings of your Identity Resolution Job without merging your data. It randomly selects a sample of matching groups from the existing matching results, and applies the automerging settings that you provided. You can then view the number of profiles in the sample, the number of matches, and the number of profiles identified to be merged. This enables you to evaluate the accuracy of the attributes in your matching list.  You can't view which profiles are matched and would be merged.  We strongly recommend you use this API to do a dry run of the automerging process before running the Identity Resolution Job. Include at least two matching attributes. If your matching list includes too few attributes (such as only FirstName or only LastName), there may be a large number of matches. This increases the chances of erroneous merges. |
| GET | /domains/{DomainName}/calculated-attributes/{CalculatedAttributeName} | Provides more information on a calculated attribute definition for Customer Profiles. |
| GET | /domains/{DomainName}/profile/{ProfileId}/calculated-attributes/{CalculatedAttributeName} | Retrieve a calculated attribute for a customer profile. |
| GET | /domains/{DomainName} | Returns information about a specific domain. |
| GET | /domains/{DomainName}/event-streams/{EventStreamName} | Returns information about the specified event stream in a specific domain. |
| GET | /domains/{DomainName}/identity-resolution-jobs/{JobId} | Returns information about an Identity Resolution Job in a specific domain.  Identity Resolution Jobs are set up using the Amazon Connect admin console. For more information, see Use Identity Resolution to consolidate similar profiles. |
| POST | /domains/{DomainName}/integrations | Returns an integration for a domain. |
| GET | /domains/{DomainName}/matches | Before calling this API, use CreateDomain or UpdateDomain to enable identity resolution: set Matching to true. GetMatches returns potentially matching profiles, based on the results of the latest run of a machine learning process.   The process of matching duplicate profiles. If Matching = true, Amazon Connect Customer Profiles starts a weekly batch process called Identity Resolution Job. If you do not specify a date and time for Identity Resolution Job to run, by default it runs every Saturday at 12AM UTC to detect duplicate profiles in your domains.  After the Identity Resolution Job completes, use the GetMatches API to return and review the results. Or, if you have configured ExportingConfig in the MatchingRequest, you can download the results from S3.  Amazon Connect uses the following profile attributes to identify matches:   PhoneNumber   HomePhoneNumber   BusinessPhoneNumber   MobilePhoneNumber   EmailAddress   PersonalEmailAddress   BusinessEmailAddress   FullName   For example, two or more profiles—with spelling mistakes such as John Doe and Jhn Doe, or different casing email addresses such as JOHN_DOE@ANYCOMPANY.COM and johndoe@anycompany.com, or different phone number formats such as 555-010-0000 and +1-555-010-0000—can be detected as belonging to the same customer John Doe and merged into a unified profile. |
| GET | /domains/{DomainName}/object-types/{ObjectTypeName} | Returns the object types for a specific domain. |
| POST | /domains/{DomainName}/matches | Returns a set of profiles that belong to the same matching group using the matchId or profileId. You can also specify the type of matching that you want for finding similar profiles using either RULE_BASED_MATCHING or ML_BASED_MATCHING. |
| GET | /domains/{DomainName}/workflows/{WorkflowId} | Get details of specified workflow. |
| GET | /domains/{DomainName}/workflows/{WorkflowId}/steps | Get granular list of steps in workflow. |
| GET | /domains/{DomainName}/calculated-attributes | Lists calculated attribute definitions for Customer Profiles |
| GET | /domains/{DomainName}/profile/{ProfileId}/calculated-attributes | Retrieve a list of calculated attributes for a customer profile. |
| GET | /domains | Returns a list of all the domains for an AWS account that have been created. |
| GET | /domains/{DomainName}/event-streams | Returns a list of all the event streams in a specific domain. |
| GET | /domains/{DomainName}/identity-resolution-jobs | Lists all of the Identity Resolution Jobs in your domain. The response sorts the list by JobStartTime. |
| GET | /domains/{DomainName}/integrations | Lists all of the integrations in your domain. |
| GET | /domains/{DomainName}/object-types | Lists all of the templates available within the service. |
| POST | /domains/{DomainName}/profiles/objects | Returns a list of objects associated with a profile of a given ProfileObjectType. |
| GET | /domains/{DomainName}/profiles/ruleBasedMatches | Returns a set of MatchIds that belong to the given domain. |
| POST | /domains/{DomainName}/workflows | Query to list all workflows. |
| POST | /domains/{DomainName}/profiles/objects/merge | Runs an AWS Lambda job that does the following:   All the profileKeys in the ProfileToBeMerged will be moved to the main profile.   All the objects in the ProfileToBeMerged will be moved to the main profile.   All the ProfileToBeMerged will be deleted at the end.   All the profileKeys in the ProfileIdsToBeMerged will be moved to the main profile.   Standard fields are merged as follows:   Fields are always "union"-ed if there are no conflicts in standard fields or attributeKeys.   When there are conflicting fields:   If no SourceProfileIds entry is specified, the main Profile value is always taken.    If a SourceProfileIds entry is specified, the specified profileId is always taken, even if it is a NULL value.       You can use MergeProfiles together with GetMatches, which returns potentially matching profiles, or use it with the results of another matching system. After profiles have been merged, they cannot be separated (unmerged). |
| PUT | /domains/{DomainName}/integrations | Adds an integration between the service and a third-party service, which includes Amazon AppFlow and Amazon Connect. An integration can belong to only one domain. To add or remove tags on an existing Integration, see  TagResource / UntagResource. |
| PUT | /domains/{DomainName}/profiles/objects | Adds additional objects to customer profiles of a given ObjectType. When adding a specific profile object, like a Contact Record, an inferred profile can get created if it is not mapped to an existing profile. The resulting profile will only have a phone number populated in the standard ProfileObject. Any additional Contact Records with the same phone number will be mapped to the same inferred profile. When a ProfileObject is created and if a ProfileObjectType already exists for the ProfileObject, it will provide data to a standard profile depending on the ProfileObjectType definition. PutProfileObject needs an ObjectType, which can be created using PutProfileObjectType. |
| PUT | /domains/{DomainName}/object-types/{ObjectTypeName} | Defines a ProfileObjectType. To add or remove tags on an existing ObjectType, see  TagResource/UntagResource. |
| POST | /domains/{DomainName}/profiles/search | Searches for profiles within a specific domain using one or more predefined search keys (e.g., _fullName, _phone, _email, _account, etc.) and/or custom-defined search keys. A search key is a data type pair that consists of a KeyName and Values list. This operation supports searching for profiles with a minimum of 1 key-value(s) pair and up to 5 key-value(s) pairs using either AND or OR logic. |
| PUT | /domains/{DomainName}/calculated-attributes/{CalculatedAttributeName} | Updates an existing calculated attribute definition. When updating the Conditions, note that increasing the date range of a calculated attribute will not trigger inclusion of historical data greater than the current date range. |
| PUT | /domains/{DomainName} | Updates the properties of a domain, including creating or selecting a dead letter queue or an encryption key. After a domain is created, the name can’t be changed. Use this API or CreateDomain to enable identity resolution: set Matching to true. To prevent cross-service impersonation when you call this API, see Cross-service confused deputy prevention for sample policies that you should apply.  To add or remove tags on an existing Domain, see TagResource/UntagResource. |
| PUT | /domains/{DomainName}/profiles | Updates the properties of a profile. The ProfileId is required for updating a customer profile. When calling the UpdateProfile API, specifying an empty string value means that any existing value will be removed. Not specifying a string value means that any value already there will be kept. |

### templates
| Method | Path | Description |
|--------|------|-------------|
| GET | /templates/{TemplateId} | Returns the template information for a specific object type. A template is a predefined ProfileObjectType, such as “Salesforce-Account” or “Salesforce-Contact.” When a user sends a ProfileObject, using the PutProfileObject API, with an ObjectTypeName that matches one of the TemplateIds, it uses the mappings from the template. |
| GET | /templates | Lists all of the template information for object types. |

### integrations
| Method | Path | Description |
|--------|------|-------------|
| POST | /integrations | Lists all of the integrations associated to a specific URI in the AWS account. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags/{resourceArn} | Displays the tags associated with an Amazon Connect Customer Profiles resource. In Connect Customer Profiles, domains, profile object types, and integrations can be tagged. |
| POST | /tags/{resourceArn} | Assigns one or more tags (key-value pairs) to the specified Amazon Connect Customer Profiles resource. Tags can help you organize and categorize your resources. You can also use them to scope user permissions by granting a user permission to access or change only resources with certain tag values. In Connect Customer Profiles, domains, profile object types, and integrations can be tagged. Tags don't have any semantic meaning to AWS and are interpreted strictly as strings of characters. You can use the TagResource action with a resource that already has tags. If you specify a new tag key, this tag is appended to the list of tags associated with the resource. If you specify a tag key that is already associated with the resource, the new tag value that you specify replaces the previous value for that tag. You can associate as many as 50 tags with a resource. |
| DELETE | /tags/{resourceArn} | Removes one or more tags from the specified Amazon Connect Customer Profiles resource. In Connect Customer Profiles, domains, profile object types, and integrations can be tagged. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a key?" -> POST /domains/{DomainName}/profiles/keys
- "Create a integration?" -> POST /domains/{DomainName}/workflows/integrations
- "Create a profile?" -> POST /domains/{DomainName}/profiles
- "Delete a calculated-attribute?" -> DELETE /domains/{DomainName}/calculated-attributes/{CalculatedAttributeName}
- "Delete a domain?" -> DELETE /domains/{DomainName}
- "Delete a event-stream?" -> DELETE /domains/{DomainName}/event-streams/{EventStreamName}
- "Create a delete?" -> POST /domains/{DomainName}/integrations/delete
- "Create a delete?" -> POST /domains/{DomainName}/profiles/delete
- "Create a delete?" -> POST /domains/{DomainName}/profiles/keys/delete
- "Create a delete?" -> POST /domains/{DomainName}/profiles/objects/delete
- "Delete a object-type?" -> DELETE /domains/{DomainName}/object-types/{ObjectTypeName}
- "Delete a workflow?" -> DELETE /domains/{DomainName}/workflows/{WorkflowId}
- "Create a object-type?" -> POST /domains/{DomainName}/detect/object-types
- "Create a auto-merging-preview?" -> POST /domains/{DomainName}/identity-resolution-jobs/auto-merging-preview
- "Get calculated-attribute details?" -> GET /domains/{DomainName}/calculated-attributes/{CalculatedAttributeName}
- "Get calculated-attribute details?" -> GET /domains/{DomainName}/profile/{ProfileId}/calculated-attributes/{CalculatedAttributeName}
- "Get domain details?" -> GET /domains/{DomainName}
- "Get event-stream details?" -> GET /domains/{DomainName}/event-streams/{EventStreamName}
- "Get identity-resolution-job details?" -> GET /domains/{DomainName}/identity-resolution-jobs/{JobId}
- "Create a integration?" -> POST /domains/{DomainName}/integrations
- "List all matches?" -> GET /domains/{DomainName}/matches
- "Get object-type details?" -> GET /domains/{DomainName}/object-types/{ObjectTypeName}
- "Get template details?" -> GET /templates/{TemplateId}
- "Create a matche?" -> POST /domains/{DomainName}/matches
- "Get workflow details?" -> GET /domains/{DomainName}/workflows/{WorkflowId}
- "List all steps?" -> GET /domains/{DomainName}/workflows/{WorkflowId}/steps
- "Create a integration?" -> POST /integrations
- "List all calculated-attributes?" -> GET /domains/{DomainName}/calculated-attributes
- "List all calculated-attributes?" -> GET /domains/{DomainName}/profile/{ProfileId}/calculated-attributes
- "List all domains?" -> GET /domains
- "List all event-streams?" -> GET /domains/{DomainName}/event-streams
- "List all identity-resolution-jobs?" -> GET /domains/{DomainName}/identity-resolution-jobs
- "List all integrations?" -> GET /domains/{DomainName}/integrations
- "List all templates?" -> GET /templates
- "List all object-types?" -> GET /domains/{DomainName}/object-types
- "Create a object?" -> POST /domains/{DomainName}/profiles/objects
- "List all ruleBasedMatches?" -> GET /domains/{DomainName}/profiles/ruleBasedMatches
- "Get tag details?" -> GET /tags/{resourceArn}
- "Create a workflow?" -> POST /domains/{DomainName}/workflows
- "Create a merge?" -> POST /domains/{DomainName}/profiles/objects/merge
- "Update a object-type?" -> PUT /domains/{DomainName}/object-types/{ObjectTypeName}
- "Create a search?" -> POST /domains/{DomainName}/profiles/search
- "Delete a tag?" -> DELETE /tags/{resourceArn}
- "Update a calculated-attribute?" -> PUT /domains/{DomainName}/calculated-attributes/{CalculatedAttributeName}
- "Update a domain?" -> PUT /domains/{DomainName}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
