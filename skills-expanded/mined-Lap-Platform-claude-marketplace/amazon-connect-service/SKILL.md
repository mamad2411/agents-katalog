---
name: amazon-connect-service
description: "Amazon Connect Service API skill. Use when working with Amazon Connect Service for evaluation-forms, analytics-data, instance. Covers 255 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon Connect Service
API version: 2017-08-08

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /instance -- verify access
3. POST /evaluation-forms/{InstanceId}/{EvaluationFormId}/activate -- create first activate

## Endpoints

255 endpoints across 66 groups. See references/api-spec.lap for full details.

### evaluation-forms
| Method | Path | Description |
|--------|------|-------------|
| POST | /evaluation-forms/{InstanceId}/{EvaluationFormId}/activate | Activates an evaluation form in the specified Amazon Connect instance. After the evaluation form is activated, it is available to start new evaluations based on the form. |
| PUT | /evaluation-forms/{InstanceId} | Creates an evaluation form in the specified Amazon Connect instance. The form can be used to define questions related to agent performance, and create sections to organize such questions. Question and section identifiers cannot be duplicated within the same evaluation form. |
| POST | /evaluation-forms/{InstanceId}/{EvaluationFormId}/deactivate | Deactivates an evaluation form in the specified Amazon Connect instance. After a form is deactivated, it is no longer available for users to start new evaluations based on the form. |
| DELETE | /evaluation-forms/{InstanceId}/{EvaluationFormId} | Deletes an evaluation form in the specified Amazon Connect instance.    If the version property is provided, only the specified version of the evaluation form is deleted.   If no version is provided, then the full form (all versions) is deleted. |
| GET | /evaluation-forms/{InstanceId}/{EvaluationFormId} | Describes an evaluation form in the specified Amazon Connect instance. If the version property is not provided, the latest version of the evaluation form is described. |
| GET | /evaluation-forms/{InstanceId}/{EvaluationFormId}/versions | Lists versions of an evaluation form in the specified Amazon Connect instance. |
| GET | /evaluation-forms/{InstanceId} | Lists evaluation forms in the specified Amazon Connect instance. |
| PUT | /evaluation-forms/{InstanceId}/{EvaluationFormId} | Updates details about a specific evaluation form version in the specified Amazon Connect instance. Question and section identifiers cannot be duplicated within the same evaluation form. This operation does not support partial updates. Instead it does a full update of evaluation form content. |

### analytics-data
| Method | Path | Description |
|--------|------|-------------|
| PUT | /analytics-data/instance/{InstanceId}/association | This API is in preview release for Amazon Connect and is subject to change. Associates the specified dataset for a Amazon Connect instance with the target account. You can associate only one dataset in a single call. |
| PUT | /analytics-data/instance/{InstanceId}/associations | This API is in preview release for Amazon Connect and is subject to change. Associates a list of analytics datasets for a given Amazon Connect instance to a target account. You can associate multiple datasets in a single call. |
| POST | /analytics-data/instance/{InstanceId}/associations | This API is in preview release for Amazon Connect and is subject to change. Removes a list of analytics datasets associated with a given Amazon Connect instance. You can disassociate multiple datasets in a single call. |
| POST | /analytics-data/instance/{InstanceId}/association | This API is in preview release for Amazon Connect and is subject to change. Removes the dataset ID associated with a given Amazon Connect instance. |
| GET | /analytics-data/instance/{InstanceId}/association | This API is in preview release for Amazon Connect and is subject to change. Lists the association status of requested dataset ID for a given Amazon Connect instance. |

### instance
| Method | Path | Description |
|--------|------|-------------|
| PUT | /instance/{InstanceId}/approved-origin | This API is in preview release for Amazon Connect and is subject to change. Associates an approved origin to an Amazon Connect instance. |
| PUT | /instance/{InstanceId}/bot | This API is in preview release for Amazon Connect and is subject to change. Allows the specified Amazon Connect instance to access the specified Amazon Lex or Amazon Lex V2 bot. |
| PUT | /instance/{InstanceId}/storage-config | This API is in preview release for Amazon Connect and is subject to change. Associates a storage resource type for the first time. You can only associate one type of storage configuration in a single call. This means, for example, that you can't define an instance with multiple S3 buckets for storing chat transcripts. This API does not create a resource that doesn't exist. It only associates it to the instance. Ensure that the resource being specified in the storage configuration, like an S3 bucket, exists when being used for association. |
| PUT | /instance/{InstanceId}/lambda-function | This API is in preview release for Amazon Connect and is subject to change. Allows the specified Amazon Connect instance to access the specified Lambda function. |
| PUT | /instance/{InstanceId}/lex-bot | This API is in preview release for Amazon Connect and is subject to change. Allows the specified Amazon Connect instance to access the specified Amazon Lex V1 bot. This API only supports the association of Amazon Lex V1 bots. |
| PUT | /instance/{InstanceId}/security-key | This API is in preview release for Amazon Connect and is subject to change. Associates a security key to the instance. |
| PUT | /instance | This API is in preview release for Amazon Connect and is subject to change. Initiates an Amazon Connect instance with all the supported channels enabled. It does not attach any storage, such as Amazon Simple Storage Service (Amazon S3) or Amazon Kinesis. It also does not allow for any configurations on features, such as Contact Lens for Amazon Connect.  For more information, see Create an Amazon Connect instance in the Amazon Connect Administrator Guide. Amazon Connect enforces a limit on the total number of instances that you can create or delete in 30 days. If you exceed this limit, you will get an error message indicating there has been an excessive number of attempts at creating or deleting instances. You must wait 30 days before you can restart creating and deleting instances in your account. |
| PUT | /instance/{InstanceId}/integration-associations | Creates an Amazon Web Services resource association with an Amazon Connect instance. |
| PUT | /instance/{InstanceId}/task/template | Creates a new task template in the specified Amazon Connect instance. |
| PUT | /instance/{InstanceId}/integration-associations/{IntegrationAssociationId}/use-cases | Creates a use case for an integration association. |
| DELETE | /instance/{InstanceId} | This API is in preview release for Amazon Connect and is subject to change. Deletes the Amazon Connect instance. For more information, see Delete your Amazon Connect instance in the Amazon Connect Administrator Guide. Amazon Connect enforces a limit on the total number of instances that you can create or delete in 30 days. If you exceed this limit, you will get an error message indicating there has been an excessive number of attempts at creating or deleting instances. You must wait 30 days before you can restart creating and deleting instances in your account. |
| DELETE | /instance/{InstanceId}/integration-associations/{IntegrationAssociationId} | Deletes an Amazon Web Services resource association from an Amazon Connect instance. The association must not have any use cases associated with it. |
| DELETE | /instance/{InstanceId}/task/template/{TaskTemplateId} | Deletes the task template. |
| DELETE | /instance/{InstanceId}/integration-associations/{IntegrationAssociationId}/use-cases/{UseCaseId} | Deletes a use case from an integration association. |
| GET | /instance/{InstanceId} | This API is in preview release for Amazon Connect and is subject to change. Returns the current state of the specified instance identifier. It tracks the instance while it is being created and returns an error status, if applicable.  If an instance is not created successfully, the instance status reason field returns details relevant to the reason. The instance in a failed state is returned only for 24 hours after the CreateInstance API was invoked. |
| GET | /instance/{InstanceId}/attribute/{AttributeType} | This API is in preview release for Amazon Connect and is subject to change. Describes the specified instance attribute. |
| GET | /instance/{InstanceId}/storage-config/{AssociationId} | This API is in preview release for Amazon Connect and is subject to change. Retrieves the current storage configurations for the specified resource type, association ID, and instance ID. |
| DELETE | /instance/{InstanceId}/approved-origin | This API is in preview release for Amazon Connect and is subject to change. Revokes access to integrated applications from Amazon Connect. |
| POST | /instance/{InstanceId}/bot | This API is in preview release for Amazon Connect and is subject to change. Revokes authorization from the specified instance to access the specified Amazon Lex or Amazon Lex V2 bot. |
| DELETE | /instance/{InstanceId}/storage-config/{AssociationId} | This API is in preview release for Amazon Connect and is subject to change. Removes the storage type configurations for the specified resource type and association ID. |
| DELETE | /instance/{InstanceId}/lambda-function | This API is in preview release for Amazon Connect and is subject to change. Remove the Lambda function from the dropdown options available in the relevant flow blocks. |
| DELETE | /instance/{InstanceId}/lex-bot | This API is in preview release for Amazon Connect and is subject to change. Revokes authorization from the specified instance to access the specified Amazon Lex bot. |
| DELETE | /instance/{InstanceId}/security-key/{AssociationId} | This API is in preview release for Amazon Connect and is subject to change. Deletes the specified security key. |
| GET | /instance/{InstanceId}/task/template/{TaskTemplateId} | Gets details about a specific task template in the specified Amazon Connect instance. |
| GET | /instance/{InstanceId}/approved-origins | This API is in preview release for Amazon Connect and is subject to change. Returns a paginated list of all approved origins associated with the instance. |
| GET | /instance/{InstanceId}/bots | This API is in preview release for Amazon Connect and is subject to change. For the specified version of Amazon Lex, returns a paginated list of all the Amazon Lex bots currently associated with the instance. Use this API to returns both Amazon Lex V1 and V2 bots. |
| GET | /instance/{InstanceId}/attributes | This API is in preview release for Amazon Connect and is subject to change. Returns a paginated list of all attribute types for the given instance. |
| GET | /instance/{InstanceId}/storage-configs | This API is in preview release for Amazon Connect and is subject to change. Returns a paginated list of storage configs for the identified instance and resource type. |
| GET | /instance | This API is in preview release for Amazon Connect and is subject to change. Return a list of instances which are in active state, creation-in-progress state, and failed state. Instances that aren't successfully created (they are in a failed state) are returned only for 24 hours after the CreateInstance API was invoked. |
| GET | /instance/{InstanceId}/integration-associations | Provides summary information about the Amazon Web Services resource associations for the specified Amazon Connect instance. |
| GET | /instance/{InstanceId}/lambda-functions | This API is in preview release for Amazon Connect and is subject to change. Returns a paginated list of all Lambda functions that display in the dropdown options in the relevant flow blocks. |
| GET | /instance/{InstanceId}/lex-bots | This API is in preview release for Amazon Connect and is subject to change. Returns a paginated list of all the Amazon Lex V1 bots currently associated with the instance. To return both Amazon Lex V1 and V2 bots, use the ListBots API. |
| GET | /instance/{InstanceId}/security-keys | This API is in preview release for Amazon Connect and is subject to change. Returns a paginated list of all security keys associated with the instance. |
| GET | /instance/{InstanceId}/task/template | Lists task templates for the specified Amazon Connect instance. |
| GET | /instance/{InstanceId}/integration-associations/{IntegrationAssociationId}/use-cases | Lists the use cases for the integration association. |
| POST | /instance/{InstanceId}/replicate | Replicates an Amazon Connect instance in the specified Amazon Web Services Region and copies configuration information for Amazon Connect resources across Amazon Web Services Regions.  For more information about replicating an Amazon Connect instance, see Create a replica of your existing Amazon Connect instance in the Amazon Connect Administrator Guide. |
| POST | /instance/{InstanceId}/attribute/{AttributeType} | This API is in preview release for Amazon Connect and is subject to change. Updates the value for the specified attribute type. |
| POST | /instance/{InstanceId}/storage-config/{AssociationId} | This API is in preview release for Amazon Connect and is subject to change. Updates an existing configuration for a resource type. This API is idempotent. |
| POST | /instance/{InstanceId}/task/template/{TaskTemplateId} | Updates details about a specific task template in the specified Amazon Connect instance. This operation does not support partial updates. Instead it does a full update of template content. |

### default-vocabulary
| Method | Path | Description |
|--------|------|-------------|
| PUT | /default-vocabulary/{InstanceId}/{LanguageCode} | Associates an existing vocabulary as the default. Contact Lens for Amazon Connect uses the vocabulary in post-call and real-time analysis sessions for the given language. |

### flow-associations
| Method | Path | Description |
|--------|------|-------------|
| PUT | /flow-associations/{InstanceId} | Associates a connect resource to a flow. |
| DELETE | /flow-associations/{InstanceId}/{ResourceId}/{ResourceType} | Disassociates a connect resource from a flow. |
| GET | /flow-associations/{InstanceId}/{ResourceId}/{ResourceType} | Retrieves the flow associated for a given resource. |

### phone-number
| Method | Path | Description |
|--------|------|-------------|
| PUT | /phone-number/{PhoneNumberId}/contact-flow | Associates a flow with a phone number claimed to your Amazon Connect instance.  If the number is claimed to a traffic distribution group, and you are calling this API using an instance in the Amazon Web Services Region where the traffic distribution group was created, you can use either a full phone number ARN or UUID value for the PhoneNumberId URI request parameter. However, if the number is claimed to a traffic distribution group and you are calling this API using an instance in the alternate Amazon Web Services Region associated with the traffic distribution group, you must provide a full phone number ARN. If a UUID is provided in this scenario, you will receive a ResourceNotFoundException. |
| POST | /phone-number/claim | Claims an available phone number to your Amazon Connect instance or traffic distribution group. You can call this API only in the same Amazon Web Services Region where the Amazon Connect instance or traffic distribution group was created. For more information about how to use this operation, see Claim a phone number in your country and Claim phone numbers to traffic distribution groups in the Amazon Connect Administrator Guide.   You can call the SearchAvailablePhoneNumbers API for available phone numbers that you can claim. Call the DescribePhoneNumber API to verify the status of a previous ClaimPhoneNumber operation.  If you plan to claim and release numbers frequently, contact us for a service quota exception. Otherwise, it is possible you will be blocked from claiming and releasing any more numbers until up to 180 days past the oldest number released has expired. By default you can claim and release up to 200% of your maximum number of active phone numbers. If you claim and release phone numbers using the UI or API during a rolling 180 day cycle that exceeds 200% of your phone number service level quota, you will be blocked from claiming any more numbers until 180 days past the oldest number released has expired.  For example, if you already have 99 claimed numbers and a service level quota of 99 phone numbers, and in any 180 day period you release 99, claim 99, and then release 99, you will have exceeded the 200% limit. At that point you are blocked from claiming any more numbers until you open an Amazon Web Services support ticket. |
| GET | /phone-number/{PhoneNumberId} | Gets details and status of a phone number that’s claimed to your Amazon Connect instance or traffic distribution group.  If the number is claimed to a traffic distribution group, and you are calling in the Amazon Web Services Region where the traffic distribution group was created, you can use either a phone number ARN or UUID value for the PhoneNumberId URI request parameter. However, if the number is claimed to a traffic distribution group and you are calling this API in the alternate Amazon Web Services Region associated with the traffic distribution group, you must provide a full phone number ARN. If a UUID is provided in this scenario, you will receive a ResourceNotFoundException. |
| DELETE | /phone-number/{PhoneNumberId}/contact-flow | Removes the flow association from a phone number claimed to your Amazon Connect instance.  If the number is claimed to a traffic distribution group, and you are calling this API using an instance in the Amazon Web Services Region where the traffic distribution group was created, you can use either a full phone number ARN or UUID value for the PhoneNumberId URI request parameter. However, if the number is claimed to a traffic distribution group and you are calling this API using an instance in the alternate Amazon Web Services Region associated with the traffic distribution group, you must provide a full phone number ARN. If a UUID is provided in this scenario, you will receive a ResourceNotFoundException. |
| POST | /phone-number/import | Imports a claimed phone number from an external service, such as Amazon Pinpoint, into an Amazon Connect instance. You can call this API only in the same Amazon Web Services Region where the Amazon Connect instance was created.  Call the DescribePhoneNumber API to verify the status of a previous ImportPhoneNumber operation.   If you plan to claim or import numbers and then release numbers frequently, contact us for a service quota exception. Otherwise, it is possible you will be blocked from claiming and releasing any more numbers until up to 180 days past the oldest number released has expired.   By default you can claim or import and then release up to 200% of your maximum number of active phone numbers. If you claim or import and then release phone numbers using the UI or API during a rolling 180 day cycle that exceeds 200% of your phone number service level quota, you will be blocked from claiming or importing any more numbers until 180 days past the oldest number released has expired.  For example, if you already have 99 claimed or imported numbers and a service level quota of 99 phone numbers, and in any 180 day period you release 99, claim 99, and then release 99, you will have exceeded the 200% limit. At that point you are blocked from claiming any more numbers until you open an Amazon Web Services Support ticket. |
| POST | /phone-number/list | Lists phone numbers claimed to your Amazon Connect instance or traffic distribution group. If the provided TargetArn is a traffic distribution group, you can call this API in both Amazon Web Services Regions associated with traffic distribution group. For more information about phone numbers, see Set Up Phone Numbers for Your Contact Center in the Amazon Connect Administrator Guide.    When given an instance ARN, ListPhoneNumbersV2 returns only the phone numbers claimed to the instance.   When given a traffic distribution group ARN ListPhoneNumbersV2 returns only the phone numbers claimed to the traffic distribution group. |
| DELETE | /phone-number/{PhoneNumberId} | Releases a phone number previously claimed to an Amazon Connect instance or traffic distribution group. You can call this API only in the Amazon Web Services Region where the number was claimed.  To release phone numbers from a traffic distribution group, use the ReleasePhoneNumber API, not the Amazon Connect admin website. After releasing a phone number, the phone number enters into a cooldown period for up to 180 days. It cannot be searched for or claimed again until the period has ended. If you accidentally release a phone number, contact Amazon Web Services Support.  If you plan to claim and release numbers frequently, contact us for a service quota exception. Otherwise, it is possible you will be blocked from claiming and releasing any more numbers until up to 180 days past the oldest number released has expired. By default you can claim and release up to 200% of your maximum number of active phone numbers. If you claim and release phone numbers using the UI or API during a rolling 180 day cycle that exceeds 200% of your phone number service level quota, you will be blocked from claiming any more numbers until 180 days past the oldest number released has expired.  For example, if you already have 99 claimed numbers and a service level quota of 99 phone numbers, and in any 180 day period you release 99, claim 99, and then release 99, you will have exceeded the 200% limit. At that point you are blocked from claiming any more numbers until you open an Amazon Web Services support ticket. |
| POST | /phone-number/search-available | Searches for available phone numbers that you can claim to your Amazon Connect instance or traffic distribution group. If the provided TargetArn is a traffic distribution group, you can call this API in both Amazon Web Services Regions associated with the traffic distribution group. |
| PUT | /phone-number/{PhoneNumberId} | Updates your claimed phone number from its current Amazon Connect instance or traffic distribution group to another Amazon Connect instance or traffic distribution group in the same Amazon Web Services Region.  After using this API, you must verify that the phone number is attached to the correct flow in the target instance or traffic distribution group. You need to do this because the API switches only the phone number to a new instance or traffic distribution group. It doesn't migrate the flow configuration of the phone number, too. You can call DescribePhoneNumber API to verify the status of a previous UpdatePhoneNumber operation. |
| PUT | /phone-number/{PhoneNumberId}/metadata | Updates a phone number’s metadata.  To verify the status of a previous UpdatePhoneNumberMetadata operation, call the DescribePhoneNumber API. |

### queues
| Method | Path | Description |
|--------|------|-------------|
| POST | /queues/{InstanceId}/{QueueId}/associate-quick-connects | This API is in preview release for Amazon Connect and is subject to change. Associates a set of quick connects with a queue. |
| PUT | /queues/{InstanceId} | This API is in preview release for Amazon Connect and is subject to change. Creates a new queue for the specified Amazon Connect instance.    If the phone number is claimed to a traffic distribution group that was created in the same Region as the Amazon Connect instance where you are calling this API, then you can use a full phone number ARN or a UUID for OutboundCallerIdNumberId. However, if the phone number is claimed to a traffic distribution group that is in one Region, and you are calling this API from an instance in another Amazon Web Services Region that is associated with the traffic distribution group, you must provide a full phone number ARN. If a UUID is provided in this scenario, you will receive a ResourceNotFoundException.   Only use the phone number ARN format that doesn't contain instance in the path, for example, arn:aws:connect:us-east-1:1234567890:phone-number/uuid. This is the same ARN format that is returned when you call the ListPhoneNumbersV2 API.   If you plan to use IAM policies to allow/deny access to this API for phone number resources claimed to a traffic distribution group, see Allow or Deny queue API actions for phone numbers in a replica Region. |
| DELETE | /queues/{InstanceId}/{QueueId} | Deletes a queue. It isn't possible to delete a queue by using the Amazon Connect admin website. |
| GET | /queues/{InstanceId}/{QueueId} | This API is in preview release for Amazon Connect and is subject to change. Describes the specified queue. |
| POST | /queues/{InstanceId}/{QueueId}/disassociate-quick-connects | This API is in preview release for Amazon Connect and is subject to change. Disassociates a set of quick connects from a queue. |
| GET | /queues/{InstanceId}/{QueueId}/quick-connects | This API is in preview release for Amazon Connect and is subject to change. Lists the quick connects associated with a queue. |
| POST | /queues/{InstanceId}/{QueueId}/hours-of-operation | This API is in preview release for Amazon Connect and is subject to change. Updates the hours of operation for the specified queue. |
| POST | /queues/{InstanceId}/{QueueId}/max-contacts | This API is in preview release for Amazon Connect and is subject to change. Updates the maximum number of contacts allowed in a queue before it is considered full. |
| POST | /queues/{InstanceId}/{QueueId}/name | This API is in preview release for Amazon Connect and is subject to change. Updates the name and description of a queue. At least Name or Description must be provided. |
| POST | /queues/{InstanceId}/{QueueId}/outbound-caller-config | This API is in preview release for Amazon Connect and is subject to change. Updates the outbound caller ID name, number, and outbound whisper flow for a specified queue.    If the phone number is claimed to a traffic distribution group that was created in the same Region as the Amazon Connect instance where you are calling this API, then you can use a full phone number ARN or a UUID for OutboundCallerIdNumberId. However, if the phone number is claimed to a traffic distribution group that is in one Region, and you are calling this API from an instance in another Amazon Web Services Region that is associated with the traffic distribution group, you must provide a full phone number ARN. If a UUID is provided in this scenario, you will receive a ResourceNotFoundException.   Only use the phone number ARN format that doesn't contain instance in the path, for example, arn:aws:connect:us-east-1:1234567890:phone-number/uuid. This is the same ARN format that is returned when you call the ListPhoneNumbersV2 API.   If you plan to use IAM policies to allow/deny access to this API for phone number resources claimed to a traffic distribution group, see Allow or Deny queue API actions for phone numbers in a replica Region. |
| POST | /queues/{InstanceId}/{QueueId}/status | This API is in preview release for Amazon Connect and is subject to change. Updates the status of the queue. |

### routing-profiles
| Method | Path | Description |
|--------|------|-------------|
| POST | /routing-profiles/{InstanceId}/{RoutingProfileId}/associate-queues | Associates a set of queues with a routing profile. |
| PUT | /routing-profiles/{InstanceId} | Creates a new routing profile. |
| DELETE | /routing-profiles/{InstanceId}/{RoutingProfileId} | Deletes a routing profile. |
| GET | /routing-profiles/{InstanceId}/{RoutingProfileId} | Describes the specified routing profile. |
| POST | /routing-profiles/{InstanceId}/{RoutingProfileId}/disassociate-queues | Disassociates a set of queues from a routing profile. |
| GET | /routing-profiles/{InstanceId}/{RoutingProfileId}/queues | Lists the queues associated with a routing profile. |
| POST | /routing-profiles/{InstanceId}/{RoutingProfileId}/agent-availability-timer | Whether agents with this routing profile will have their routing order calculated based on time since their last inbound contact or longest idle time. |
| POST | /routing-profiles/{InstanceId}/{RoutingProfileId}/concurrency | Updates the channels that agents can handle in the Contact Control Panel (CCP) for a routing profile. |
| POST | /routing-profiles/{InstanceId}/{RoutingProfileId}/default-outbound-queue | Updates the default outbound queue of a routing profile. |
| POST | /routing-profiles/{InstanceId}/{RoutingProfileId}/name | Updates the name and description of a routing profile. The request accepts the following data in JSON format. At least Name or Description must be provided. |
| POST | /routing-profiles/{InstanceId}/{RoutingProfileId}/queues | Updates the properties associated with a set of queues for a routing profile. |

### traffic-distribution-group
| Method | Path | Description |
|--------|------|-------------|
| PUT | /traffic-distribution-group/{TrafficDistributionGroupId}/user | Associates an agent with a traffic distribution group. |
| PUT | /traffic-distribution-group | Creates a traffic distribution group given an Amazon Connect instance that has been replicated.   The SignInConfig distribution is available only on a default TrafficDistributionGroup (see the IsDefault parameter in the TrafficDistributionGroup data type). If you call UpdateTrafficDistribution with a modified SignInConfig and a non-default TrafficDistributionGroup, an InvalidRequestException is returned.  For more information about creating traffic distribution groups, see Set up traffic distribution groups in the Amazon Connect Administrator Guide. |
| DELETE | /traffic-distribution-group/{TrafficDistributionGroupId} | Deletes a traffic distribution group. This API can be called only in the Region where the traffic distribution group is created. For more information about deleting traffic distribution groups, see Delete traffic distribution groups in the Amazon Connect Administrator Guide. |
| GET | /traffic-distribution-group/{TrafficDistributionGroupId} | Gets details and status of a traffic distribution group. |
| DELETE | /traffic-distribution-group/{TrafficDistributionGroupId}/user | Disassociates an agent from a traffic distribution group. |
| GET | /traffic-distribution-group/{TrafficDistributionGroupId}/user | Lists traffic distribution group users. |

### users
| Method | Path | Description |
|--------|------|-------------|
| POST | /users/{InstanceId}/{UserId}/associate-proficiencies | &gt;Associates a set of proficiencies with a user. |
| PUT | /users/{InstanceId} | Creates a user account for the specified Amazon Connect instance.  Certain UserIdentityInfo parameters are required in some situations. For example, Email is required if you are using SAML for identity management. FirstName and LastName are required if you are using Amazon Connect or SAML for identity management.  For information about how to create users using the Amazon Connect admin website, see Add Users in the Amazon Connect Administrator Guide. |
| DELETE | /users/{InstanceId}/{UserId} | Deletes a user account from the specified Amazon Connect instance. For information about what happens to a user's data when their account is deleted, see Delete Users from Your Amazon Connect Instance in the Amazon Connect Administrator Guide.  After calling DeleteUser, call DeleteQuickConnect to delete any records related to the deleted users. This will help you:   Avoid dangling resources that impact your service quotas.   Remove deleted users so they don't appear to agents as transfer options.   Avoid the disruption of other Amazon Connect processes, such as instance replication and syncing if you're using Amazon Connect Global Resiliency. |
| GET | /users/{InstanceId}/{UserId} | Describes the specified user. You can find the instance ID in the Amazon Connect console (it’s the final part of the ARN). The console does not display the user IDs. Instead, list the users and note the IDs provided in the output. |
| POST | /users/{InstanceId}/{UserId}/disassociate-proficiencies | Disassociates a set of proficiencies from a user. |
| POST | /users/{InstanceId}/{UserId}/contact | Dismisses contacts from an agent’s CCP and returns the agent to an available state, which allows the agent to receive a new routed contact. Contacts can only be dismissed if they are in a MISSED, ERROR, ENDED, or REJECTED state in the Agent Event Stream. |
| GET | /users/{InstanceId}/{UserId}/proficiencies | Lists proficiencies associated with a user. |
| PUT | /users/{InstanceId}/{UserId}/status | Changes the current status of a user or agent in Amazon Connect. If the agent is currently handling a contact, this sets the agent's next status. For more information, see Agent status and Set your next status in the Amazon Connect Administrator Guide. |
| POST | /users/{InstanceId}/{UserId}/hierarchy | Assigns the specified hierarchy group to the specified user. |
| POST | /users/{InstanceId}/{UserId}/identity-info | Updates the identity information for the specified user.  We strongly recommend limiting who has the ability to invoke UpdateUserIdentityInfo. Someone with that ability can change the login credentials of other users by changing their email address. This poses a security risk to your organization. They can change the email address of a user to the attacker's email address, and then reset the password through email. For more information, see Best Practices for Security Profiles in the Amazon Connect Administrator Guide. |
| POST | /users/{InstanceId}/{UserId}/phone-config | Updates the phone configuration settings for the specified user. |
| POST | /users/{InstanceId}/{UserId}/proficiencies | Updates the properties associated with the proficiencies of a user. |
| POST | /users/{InstanceId}/{UserId}/routing-profile | Assigns the specified routing profile to the specified user. |
| POST | /users/{InstanceId}/{UserId}/security-profiles | Assigns the specified security profiles to the specified user. |

### attached-files
| Method | Path | Description |
|--------|------|-------------|
| POST | /attached-files/{InstanceId} | Allows you to retrieve metadata about multiple attached files on an associated resource. Each attached file provided in the input list must be associated with the input AssociatedResourceArn. |
| POST | /attached-files/{InstanceId}/{FileId} | Allows you to confirm that the attached file has been uploaded using the pre-signed URL provided in the StartAttachedFileUpload API. |
| DELETE | /attached-files/{InstanceId}/{FileId} | Deletes an attached file along with the underlying S3 Object.  The attached file is permanently deleted if S3 bucket versioning is not enabled. |
| GET | /attached-files/{InstanceId}/{FileId} | Provides a pre-signed URL for download of an approved attached file. This API also returns metadata about the attached file. It will only return a downloadURL if the status of the attached file is APPROVED. |
| PUT | /attached-files/{InstanceId} | Provides a pre-signed Amazon S3 URL in response for uploading your content.  You may only use this API to upload attachments to an Amazon Connect Case. |

### flow-associations-batch
| Method | Path | Description |
|--------|------|-------------|
| POST | /flow-associations-batch/{InstanceId} | Retrieve the flow associations for the given resources. |

### contact
| Method | Path | Description |
|--------|------|-------------|
| PUT | /contact/batch/{InstanceId} | Only the Amazon Connect outbound campaigns service principal is allowed to assume a role in your account and call this API.  Allows you to create a batch of contacts in Amazon Connect. The outbound campaigns capability ingests dial requests via the PutDialRequestBatch API. It then uses BatchPutContact to create contacts corresponding to those dial requests. If agents are available, the dial requests are dialed out, which results in a voice call. The resulting voice call uses the same contactId that was created by BatchPutContact. |
| POST | /contact/create-participant | Adds a new participant into an on-going chat contact. For more information, see Customize chat flow experiences by integrating custom participants. |
| POST | /contact/persistent-contact-association/{InstanceId}/{InitialContactId} | Enables rehydration of chats for the lifespan of a contact. For more information about chat rehydration, see Enable persistent chat in the Amazon Connect Administrator Guide. |
| GET | /contact/attributes/{InstanceId}/{InitialContactId} | Retrieves the contact attributes for the specified contact. |
| GET | /contact/references/{InstanceId}/{ContactId} | This API is in preview release for Amazon Connect and is subject to change. For the specified referenceTypes, returns a list of references associated with the contact. References are links to documents that are related to a contact, such as emails, attachments, or URLs. |
| POST | /contact/list-real-time-analysis-segments-v2/{InstanceId}/{ContactId} | Provides a list of analysis segments for a real-time analysis session. |
| POST | /contact/monitor | Initiates silent monitoring of a contact. The Contact Control Panel (CCP) of the user specified by userId will be set to silent monitoring mode on the contact. |
| POST | /contact/pause | Allows pausing an ongoing task contact. |
| POST | /contact/resume | Allows resuming a task contact in a paused state. |
| POST | /contact/resume-recording | When a contact is being recorded, and the recording has been suspended using SuspendContactRecording, this API resumes recording whatever recording is selected in the flow configuration: call, screen, or both. If only call recording or only screen recording is enabled, then it would resume. Voice and screen recordings are supported. |
| PUT | /contact/chat | Initiates a flow to start a new chat for the customer. Response of this API provides a token required to obtain credentials from the CreateParticipantConnection API in the Amazon Connect Participant Service. When a new chat contact is successfully created, clients must subscribe to the participant’s connection for the created chat within 5 minutes. This is achieved by invoking CreateParticipantConnection with WEBSOCKET and CONNECTION_CREDENTIALS.  A 429 error occurs in the following situations:   API rate limit is exceeded. API TPS throttling returns a TooManyRequests exception.   The quota for concurrent active chats is exceeded. Active chat throttling returns a LimitExceededException.   If you use the ChatDurationInMinutes parameter and receive a 400 error, your account may not support the ability to configure custom chat durations. For more information, contact Amazon Web Services Support.  For more information about chat, see the following topics in the Amazon Connect Administrator Guide:     Concepts: Web and mobile messaging capabilities in Amazon Connect     Amazon Connect Chat security best practices |
| POST | /contact/start-recording | Starts recording the contact:    If the API is called before the agent joins the call, recording starts when the agent joins the call.   If the API is called after the agent joins the call, recording starts at the time of the API call.   StartContactRecording is a one-time action. For example, if you use StopContactRecording to stop recording an ongoing call, you can't use StartContactRecording to restart it. For scenarios where the recording has started and you want to suspend and resume it, such as when collecting sensitive information (for example, a credit card number), use SuspendContactRecording and ResumeContactRecording. You can use this API to override the recording behavior configured in the Set recording behavior block. Only voice recordings are supported at this time. |
| POST | /contact/start-streaming | Initiates real-time message streaming for a new chat contact.  For more information about message streaming, see Enable real-time chat message streaming in the Amazon Connect Administrator Guide. For more information about chat, see the following topics in the Amazon Connect Administrator Guide:     Concepts: Web and mobile messaging capabilities in Amazon Connect     Amazon Connect Chat security best practices |
| PUT | /contact/outbound-voice | Places an outbound call to a contact, and then initiates the flow. It performs the actions in the flow that's specified (in ContactFlowId). Agents do not initiate the outbound API, which means that they do not dial the contact. If the flow places an outbound call to a contact, and then puts the contact in queue, the call is then routed to the agent, like any other inbound case. There is a 60-second dialing timeout for this operation. If the call is not connected after 60 seconds, it fails.  UK numbers with a 447 prefix are not allowed by default. Before you can dial these UK mobile numbers, you must submit a service quota increase request. For more information, see Amazon Connect Service Quotas in the Amazon Connect Administrator Guide.    Campaign calls are not allowed by default. Before you can make a call with TrafficType = CAMPAIGN, you must submit a service quota increase request to the quota Amazon Connect campaigns. |
| PUT | /contact/task | Initiates a flow to start a new task contact. For more information about task contacts, see Concepts: Tasks in Amazon Connect in the Amazon Connect Administrator Guide.  When using PreviousContactId and RelatedContactId input parameters, note the following:    PreviousContactId    Any updates to user-defined task contact attributes on any contact linked through the same PreviousContactId will affect every contact in the chain.   There can be a maximum of 12 linked task contacts in a chain. That is, 12 task contacts can be created that share the same PreviousContactId.      RelatedContactId    Copies contact attributes from the related task contact to the new contact.   Any update on attributes in a new task contact does not update attributes on previous contact.   There’s no limit on the number of task contacts that can be created that use the same RelatedContactId.     In addition, when calling StartTaskContact include only one of these parameters: ContactFlowID, QuickConnectID, or TaskTemplateID. Only one parameter is required as long as the task template has a flow configured to run it. If more than one parameter is specified, or only the TaskTemplateID is specified but it does not have a flow configured, the request returns an error because Amazon Connect cannot identify the unique flow to run when the task is created. A ServiceQuotaExceededException occurs when the number of open tasks exceeds the active tasks quota or there are already 12 tasks referencing the same PreviousContactId. For more information about service quotas for task contacts, see Amazon Connect service quotas in the Amazon Connect Administrator Guide. |
| PUT | /contact/webrtc | Places an inbound in-app, web, or video call to a contact, and then initiates the flow. It performs the actions in the flow that are specified (in ContactFlowId) and present in the Amazon Connect instance (specified as InstanceId). |
| POST | /contact/stop | Ends the specified contact. Use this API to stop queued callbacks. It does not work for voice contacts that use the following initiation methods:   DISCONNECT   TRANSFER   QUEUE_TRANSFER   EXTERNAL_OUTBOUND   MONITOR   Chat and task contacts can be terminated in any state, regardless of initiation method. |
| POST | /contact/stop-recording | Stops recording a call when a contact is being recorded. StopContactRecording is a one-time action. If you use StopContactRecording to stop recording an ongoing call, you can't use StartContactRecording to restart it. For scenarios where the recording has started and you want to suspend it for sensitive information (for example, to collect a credit card number), and then restart it, use SuspendContactRecording and ResumeContactRecording. Only voice recordings are supported at this time. |
| POST | /contact/stop-streaming | Ends message streaming on a specified contact. To restart message streaming on that contact, call the StartContactStreaming API. |
| POST | /contact/suspend-recording | When a contact is being recorded, this API suspends recording whatever is selected in the flow configuration: call, screen, or both. If only call recording or only screen recording is enabled, then it would be suspended. For example, you might suspend the screen recording while collecting sensitive information, such as a credit card number. Then use ResumeContactRecording to restart recording the screen. The period of time that the recording is suspended is filled with silence in the final recording. Voice and screen recordings are supported. |
| POST | /contact/tags | Adds the specified tags to the contact resource. For more information about this API is used, see Set up granular billing for a detailed view of your Amazon Connect usage. |
| POST | /contact/transfer | Transfers contacts from one agent or queue to another agent or queue at any point after a contact is created. You can transfer a contact to another queue by providing the flow which orchestrates the contact to the destination queue. This gives you more control over contact handling and helps you adhere to the service level agreement (SLA) guaranteed to your customers. Note the following requirements:   Transfer is supported for only TASK contacts.   Do not use both QueueId and UserId in the same call.   The following flow types are supported: Inbound flow, Transfer to agent flow, and Transfer to queue flow.   The TransferContact API can be called only on active contacts.   A contact cannot be transferred more than 11 times. |
| DELETE | /contact/tags/{InstanceId}/{ContactId} | Removes the specified tags from the contact resource. For more information about this API is used, see Set up granular billing for a detailed view of your Amazon Connect usage. |
| POST | /contact/attributes | Creates or updates user-defined contact attributes associated with the specified contact. You can create or update user-defined attributes for both ongoing and completed contacts. For example, while the call is active, you can update the customer's name or the reason the customer called. You can add notes about steps that the agent took during the call that display to the next agent that takes the call. You can also update attributes for a contact using data from your CRM application and save the data with the contact in Amazon Connect. You could also flag calls for additional analysis, such as legal review or to identify abusive callers. Contact attributes are available in Amazon Connect for 24 months, and are then deleted. For information about contact record retention and the maximum size of the contact record attributes section, see Feature specifications in the Amazon Connect Administrator Guide. |
| POST | /contact/schedule | Updates the scheduled time of a task contact that is already scheduled. |
| PUT | /contact/participant-role-config/{InstanceId}/{ContactId} | Updates timeouts for when human chat participants are to be considered idle, and when agents are automatically disconnected from a chat due to idleness. You can set four timers:   Customer idle timeout   Customer auto-disconnect timeout   Agent idle timeout   Agent auto-disconnect timeout   For more information about how chat timeouts work, see Set up chat timeouts for human participants. |

### agent-status
| Method | Path | Description |
|--------|------|-------------|
| PUT | /agent-status/{InstanceId} | This API is in preview release for Amazon Connect and is subject to change. Creates an agent status for the specified Amazon Connect instance. |
| GET | /agent-status/{InstanceId}/{AgentStatusId} | This API is in preview release for Amazon Connect and is subject to change. Describes an agent status. |
| GET | /agent-status/{InstanceId} | This API is in preview release for Amazon Connect and is subject to change. Lists agent statuses. |
| POST | /agent-status/{InstanceId}/{AgentStatusId} | This API is in preview release for Amazon Connect and is subject to change. Updates agent status. |

### contact-flows
| Method | Path | Description |
|--------|------|-------------|
| PUT | /contact-flows/{InstanceId} | Creates a flow for the specified Amazon Connect instance. You can also create and update flows using the Amazon Connect Flow language. |
| DELETE | /contact-flows/{InstanceId}/{ContactFlowId} | Deletes a flow for the specified Amazon Connect instance. |
| GET | /contact-flows/{InstanceId}/{ContactFlowId} | Describes the specified flow. You can also create and update flows using the Amazon Connect Flow language. Use the $SAVED alias in the request to describe the SAVED content of a Flow. For example, arn:aws:.../contact-flow/{id}:$SAVED. Once a contact flow is published, $SAVED needs to be supplied to view saved content that has not been published. In the response, Status indicates the flow status as either SAVED or PUBLISHED. The PUBLISHED status will initiate validation on the content. SAVED does not initiate validation of the content. SAVED | PUBLISHED |
| POST | /contact-flows/{InstanceId}/{ContactFlowId}/content | Updates the specified flow. You can also create and update flows using the Amazon Connect Flow language. Use the $SAVED alias in the request to describe the SAVED content of a Flow. For example, arn:aws:.../contact-flow/{id}:$SAVED. Once a contact flow is published, $SAVED needs to be supplied to view saved content that has not been published. |
| POST | /contact-flows/{InstanceId}/{ContactFlowId}/metadata | Updates metadata about specified flow. |
| POST | /contact-flows/{InstanceId}/{ContactFlowId}/name | The name of the flow. You can also create and update flows using the Amazon Connect Flow language. |

### contact-flow-modules
| Method | Path | Description |
|--------|------|-------------|
| PUT | /contact-flow-modules/{InstanceId} | Creates a flow module for the specified Amazon Connect instance. |
| DELETE | /contact-flow-modules/{InstanceId}/{ContactFlowModuleId} | Deletes the specified flow module. |
| GET | /contact-flow-modules/{InstanceId}/{ContactFlowModuleId} | Describes the specified flow module. Use the $SAVED alias in the request to describe the SAVED content of a Flow. For example, arn:aws:.../contact-flow/{id}:$SAVED. Once a contact flow is published, $SAVED needs to be supplied to view saved content that has not been published. |
| POST | /contact-flow-modules/{InstanceId}/{ContactFlowModuleId}/content | Updates specified flow module for the specified Amazon Connect instance.  Use the $SAVED alias in the request to describe the SAVED content of a Flow. For example, arn:aws:.../contact-flow/{id}:$SAVED. Once a contact flow is published, $SAVED needs to be supplied to view saved content that has not been published. |
| POST | /contact-flow-modules/{InstanceId}/{ContactFlowModuleId}/metadata | Updates metadata about specified flow module. |

### hours-of-operations
| Method | Path | Description |
|--------|------|-------------|
| PUT | /hours-of-operations/{InstanceId} | This API is in preview release for Amazon Connect and is subject to change. Creates hours of operation. |
| DELETE | /hours-of-operations/{InstanceId}/{HoursOfOperationId} | This API is in preview release for Amazon Connect and is subject to change. Deletes an hours of operation. |
| GET | /hours-of-operations/{InstanceId}/{HoursOfOperationId} | This API is in preview release for Amazon Connect and is subject to change. Describes the hours of operation. |
| POST | /hours-of-operations/{InstanceId}/{HoursOfOperationId} | This API is in preview release for Amazon Connect and is subject to change. Updates the hours of operation. |

### predefined-attributes
| Method | Path | Description |
|--------|------|-------------|
| PUT | /predefined-attributes/{InstanceId} | Creates a new predefined attribute for the specified Amazon Connect instance. Predefined attributes are attributes in an Amazon Connect instance that can be used to route contacts to an agent or pools of agents within a queue. For more information, see Create predefined attributes for routing contacts to agents. |
| DELETE | /predefined-attributes/{InstanceId}/{Name} | Deletes a predefined attribute from the specified Amazon Connect instance. |
| GET | /predefined-attributes/{InstanceId}/{Name} | Describes a predefined attribute for the specified Amazon Connect instance. Predefined attributes are attributes in an Amazon Connect instance that can be used to route contacts to an agent or pools of agents within a queue. For more information, see Create predefined attributes for routing contacts to agents. |
| GET | /predefined-attributes/{InstanceId} | Lists predefined attributes for the specified Amazon Connect instance. Predefined attributes are attributes in an Amazon Connect instance that can be used to route contacts to an agent or pools of agents within a queue. For more information, see Create predefined attributes for routing contacts to agents. |
| POST | /predefined-attributes/{InstanceId}/{Name} | Updates a predefined attribute for the specified Amazon Connect instance. Predefined attributes are attributes in an Amazon Connect instance that can be used to route contacts to an agent or pools of agents within a queue. For more information, see Create predefined attributes for routing contacts to agents. |

### prompts
| Method | Path | Description |
|--------|------|-------------|
| PUT | /prompts/{InstanceId} | Creates a prompt. For more information about prompts, such as supported file types and maximum length, see Create prompts in the Amazon Connect Administrator Guide. |
| DELETE | /prompts/{InstanceId}/{PromptId} | Deletes a prompt. |
| GET | /prompts/{InstanceId}/{PromptId} | Describes the prompt. |
| GET | /prompts/{InstanceId}/{PromptId}/file | Gets the prompt file. |
| POST | /prompts/{InstanceId}/{PromptId} | Updates a prompt. |

### quick-connects
| Method | Path | Description |
|--------|------|-------------|
| PUT | /quick-connects/{InstanceId} | Creates a quick connect for the specified Amazon Connect instance. |
| DELETE | /quick-connects/{InstanceId}/{QuickConnectId} | Deletes a quick connect.   After calling DeleteUser, it's important to call DeleteQuickConnect to delete any records related to the deleted users. This will help you:   Avoid dangling resources that impact your service quotas.   Remove deleted users so they don't appear to agents as transfer options.   Avoid the disruption of other Amazon Connect processes, such as instance replication and syncing if you're using Amazon Connect Global Resiliency. |
| GET | /quick-connects/{InstanceId}/{QuickConnectId} | Describes the quick connect. |
| GET | /quick-connects/{InstanceId} | Provides information about the quick connects for the specified Amazon Connect instance. |
| POST | /quick-connects/{InstanceId}/{QuickConnectId}/config | Updates the configuration settings for the specified quick connect. |
| POST | /quick-connects/{InstanceId}/{QuickConnectId}/name | Updates the name and description of a quick connect. The request accepts the following data in JSON format. At least Name or Description must be provided. |

### rules
| Method | Path | Description |
|--------|------|-------------|
| POST | /rules/{InstanceId} | Creates a rule for the specified Amazon Connect instance. Use the Rules Function language to code conditions for the rule. |
| DELETE | /rules/{InstanceId}/{RuleId} | Deletes a rule for the specified Amazon Connect instance. |
| GET | /rules/{InstanceId}/{RuleId} | Describes a rule for the specified Amazon Connect instance. |
| GET | /rules/{InstanceId} | List all rules for the specified Amazon Connect instance. |
| PUT | /rules/{InstanceId}/{RuleId} | Updates a rule for the specified Amazon Connect instance. Use the Rules Function language to code conditions for the rule. |

### security-profiles
| Method | Path | Description |
|--------|------|-------------|
| PUT | /security-profiles/{InstanceId} | Creates a security profile. For information about security profiles, see Security Profiles in the Amazon Connect Administrator Guide. For a mapping of the API name and user interface name of the security profile permissions, see List of security profile permissions. |
| DELETE | /security-profiles/{InstanceId}/{SecurityProfileId} | Deletes a security profile. |
| GET | /security-profiles/{InstanceId}/{SecurityProfileId} | Gets basic information about the security profile. For information about security profiles, see Security Profiles in the Amazon Connect Administrator Guide. For a mapping of the API name and user interface name of the security profile permissions, see List of security profile permissions. |
| POST | /security-profiles/{InstanceId}/{SecurityProfileId} | Updates a security profile. For information about security profiles, see Security Profiles in the Amazon Connect Administrator Guide. For a mapping of the API name and user interface name of the security profile permissions, see List of security profile permissions. |

### user-hierarchy-groups
| Method | Path | Description |
|--------|------|-------------|
| PUT | /user-hierarchy-groups/{InstanceId} | Creates a new user hierarchy group. |
| DELETE | /user-hierarchy-groups/{InstanceId}/{HierarchyGroupId} | Deletes an existing user hierarchy group. It must not be associated with any agents or have any active child groups. |
| GET | /user-hierarchy-groups/{InstanceId}/{HierarchyGroupId} | Describes the specified hierarchy group. |
| POST | /user-hierarchy-groups/{InstanceId}/{HierarchyGroupId}/name | Updates the name of the user hierarchy group. |

### views
| Method | Path | Description |
|--------|------|-------------|
| PUT | /views/{InstanceId} | Creates a new view with the possible status of SAVED or PUBLISHED. The views will have a unique name for each connect instance. It performs basic content validation if the status is SAVED or full content validation if the status is set to PUBLISHED. An error is returned if validation fails. It associates either the $SAVED qualifier or both of the $SAVED and $LATEST qualifiers with the provided view content based on the status. The view is idempotent if ClientToken is provided. |
| PUT | /views/{InstanceId}/{ViewId}/versions | Publishes a new version of the view identifier. Versions are immutable and monotonically increasing. It returns the highest version if there is no change in content compared to that version. An error is displayed if the supplied ViewContentSha256 is different from the ViewContentSha256 of the $LATEST alias. |
| DELETE | /views/{InstanceId}/{ViewId} | Deletes the view entirely. It deletes the view and all associated qualifiers (versions and aliases). |
| DELETE | /views/{InstanceId}/{ViewId}/versions/{ViewVersion} | Deletes the particular version specified in ViewVersion identifier. |
| GET | /views/{InstanceId}/{ViewId} | Retrieves the view for the specified Amazon Connect instance and view identifier. The view identifier can be supplied as a ViewId or ARN.  $SAVED needs to be supplied if a view is unpublished. The view identifier can contain an optional qualifier, for example, &lt;view-id&gt;:$SAVED, which is either an actual version number or an Amazon Connect managed qualifier $SAVED | $LATEST. If it is not supplied, then $LATEST is assumed for customer managed views and an error is returned if there is no published content available. Version 1 is assumed for Amazon Web Services managed views. |
| GET | /views/{InstanceId}/{ViewId}/versions | Returns all the available versions for the specified Amazon Connect instance and view identifier. Results will be sorted from highest to lowest. |
| GET | /views/{InstanceId} | Returns views in the given instance. Results are sorted primarily by type, and secondarily by name. |
| POST | /views/{InstanceId}/{ViewId} | Updates the view content of the given view identifier in the specified Amazon Connect instance. It performs content validation if Status is set to SAVED and performs full content validation if Status is PUBLISHED. Note that the $SAVED alias' content will always be updated, but the $LATEST alias' content will only be updated if Status is PUBLISHED. |
| POST | /views/{InstanceId}/{ViewId}/metadata | Updates the view metadata. Note that either Name or Description must be provided. |

### vocabulary
| Method | Path | Description |
|--------|------|-------------|
| POST | /vocabulary/{InstanceId} | Creates a custom vocabulary associated with your Amazon Connect instance. You can set a custom vocabulary to be your default vocabulary for a given language. Contact Lens for Amazon Connect uses the default vocabulary in post-call and real-time contact analysis sessions for that language. |
| GET | /vocabulary/{InstanceId}/{VocabularyId} | Describes the specified vocabulary. |

### contact-evaluations
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /contact-evaluations/{InstanceId}/{EvaluationId} | Deletes a contact evaluation in the specified Amazon Connect instance. |
| GET | /contact-evaluations/{InstanceId}/{EvaluationId} | Describes a contact evaluation in the specified Amazon Connect instance. |
| GET | /contact-evaluations/{InstanceId} | Lists contact evaluations in the specified Amazon Connect instance. |
| PUT | /contact-evaluations/{InstanceId} | Starts an empty evaluation in the specified Amazon Connect instance, using the given evaluation form for the particular contact. The evaluation form version used for the contact evaluation corresponds to the currently activated version. If no version is activated for the evaluation form, the contact evaluation cannot be started.   Evaluations created through the public API do not contain answer values suggested from automation. |
| POST | /contact-evaluations/{InstanceId}/{EvaluationId}/submit | Submits a contact evaluation in the specified Amazon Connect instance. Answers included in the request are merged with existing answers for the given evaluation. If no answers or notes are passed, the evaluation is submitted with the existing answers and notes. You can delete an answer or note by passing an empty object ({}) to the question identifier.  If a contact evaluation is already in submitted state, this operation will trigger a resubmission. |
| POST | /contact-evaluations/{InstanceId}/{EvaluationId} | Updates details about a contact evaluation in the specified Amazon Connect instance. A contact evaluation must be in draft state. Answers included in the request are merged with existing answers for the given evaluation. An answer or note can be deleted by passing an empty object ({}) to the question identifier. |

### vocabulary-remove
| Method | Path | Description |
|--------|------|-------------|
| POST | /vocabulary-remove/{InstanceId}/{VocabularyId} | Deletes the vocabulary that has the given identifier. |

### authentication-profiles
| Method | Path | Description |
|--------|------|-------------|
| GET | /authentication-profiles/{InstanceId}/{AuthenticationProfileId} | This API is in preview release for Amazon Connect and is subject to change. To request access to this API, contact Amazon Web Services Support. Describes the target authentication profile. |
| POST | /authentication-profiles/{InstanceId}/{AuthenticationProfileId} | This API is in preview release for Amazon Connect and is subject to change. To request access to this API, contact Amazon Web Services Support. Updates the selected authentication profile. |

### contacts
| Method | Path | Description |
|--------|------|-------------|
| GET | /contacts/{InstanceId}/{ContactId} | This API is in preview release for Amazon Connect and is subject to change. Describes the specified contact.   Contact information remains available in Amazon Connect for 24 months, and then it is deleted. Only data from November 12, 2021, and later is returned by this API. |
| POST | /contacts/{InstanceId}/{ContactId} | This API is in preview release for Amazon Connect and is subject to change. Adds or updates user-defined contact information associated with the specified contact. At least one field to be updated must be present in the request.  You can add or update user-defined contact information for both ongoing and completed contacts. |
| POST | /contacts/{InstanceId}/{ContactId}/routing-data | Updates routing priority and age on the contact (QueuePriority and QueueTimeAdjustmentInSeconds). These properties can be used to change a customer's position in the queue. For example, you can move a contact to the back of the queue by setting a lower routing priority relative to other contacts in queue; or you can move a contact to the front of the queue by increasing the routing age which will make the contact look artificially older and therefore higher up in the first-in-first-out routing order. Note that adjusting the routing age of a contact affects only its position in queue, and not its actual queue wait time as reported through metrics. These properties can also be updated by using the Set routing priority / age flow block.  Either QueuePriority or QueueTimeAdjustmentInSeconds should be provided within the request body, but not both. |

### user-hierarchy-structure
| Method | Path | Description |
|--------|------|-------------|
| GET | /user-hierarchy-structure/{InstanceId} | Describes the hierarchy structure of the specified Amazon Connect instance. |
| POST | /user-hierarchy-structure/{InstanceId} | Updates the user hierarchy structure: add, remove, and rename user hierarchy levels. |

### metrics
| Method | Path | Description |
|--------|------|-------------|
| POST | /metrics/current/{InstanceId} | Gets the real-time metric data from the specified Amazon Connect instance. For a description of each metric, see Real-time Metrics Definitions in the Amazon Connect Administrator Guide. |
| POST | /metrics/userdata/{InstanceId} | Gets the real-time active user data from the specified Amazon Connect instance. |
| POST | /metrics/historical/{InstanceId} | Gets historical metric data from the specified Amazon Connect instance. For a description of each historical metric, see Historical Metrics Definitions in the Amazon Connect Administrator Guide.  We recommend using the GetMetricDataV2 API. It provides more flexibility, features, and the ability to query longer time ranges than GetMetricData. Use it to retrieve historical agent and contact metrics for the last 3 months, at varying intervals. You can also use it to build custom dashboards to measure historical queue and agent performance. For example, you can track the number of incoming contacts for the last 7 days, with data split by day, to see how contact volume changed per day of the week. |
| POST | /metrics/data | Gets metric data from the specified Amazon Connect instance.   GetMetricDataV2 offers more features than GetMetricData, the previous version of this API. It has new metrics, offers filtering at a metric level, and offers the ability to filter and group data by channels, queues, routing profiles, agents, and agent hierarchy levels. It can retrieve historical data for the last 3 months, at varying intervals.  For a description of the historical metrics that are supported by GetMetricDataV2 and GetMetricData, see Historical metrics definitions in the Amazon Connect Administrator Guide. |

### user
| Method | Path | Description |
|--------|------|-------------|
| GET | /user/federate/{InstanceId} | Supports SAML sign-in for Amazon Connect. Retrieves a token for federation. The token is for the Amazon Connect user which corresponds to the IAM credentials that were used to invoke this action.  For more information about how SAML sign-in works in Amazon Connect, see Configure SAML with IAM for Amazon Connect in the Amazon Connect Administrator Guide.   This API doesn't support root users. If you try to invoke GetFederationToken with root credentials, an error message similar to the following one appears:   Provided identity: Principal: .... User: .... cannot be used for federation with Amazon Connect |

### traffic-distribution
| Method | Path | Description |
|--------|------|-------------|
| GET | /traffic-distribution/{Id} | Retrieves the current traffic distribution for a given traffic distribution group. |
| PUT | /traffic-distribution/{Id} | Updates the traffic distribution for a given traffic distribution group.   The SignInConfig distribution is available only on a default TrafficDistributionGroup (see the IsDefault parameter in the TrafficDistributionGroup data type). If you call UpdateTrafficDistribution with a modified SignInConfig and a non-default TrafficDistributionGroup, an InvalidRequestException is returned.  For more information about updating a traffic distribution group, see Update telephony traffic distribution across Amazon Web Services Regions  in the Amazon Connect Administrator Guide. |

### authentication-profiles-summary
| Method | Path | Description |
|--------|------|-------------|
| GET | /authentication-profiles-summary/{InstanceId} | This API is in preview release for Amazon Connect and is subject to change. To request access to this API, contact Amazon Web Services Support. Provides summary information about the authentication profiles in a specified Amazon Connect instance. |

### contact-flow-modules-summary
| Method | Path | Description |
|--------|------|-------------|
| GET | /contact-flow-modules-summary/{InstanceId} | Provides information about the flow modules for the specified Amazon Connect instance. |

### contact-flows-summary
| Method | Path | Description |
|--------|------|-------------|
| GET | /contact-flows-summary/{InstanceId} | Provides information about the flows for the specified Amazon Connect instance. You can also create and update flows using the Amazon Connect Flow language. For more information about flows, see Flows in the Amazon Connect Administrator Guide. |

### default-vocabulary-summary
| Method | Path | Description |
|--------|------|-------------|
| POST | /default-vocabulary-summary/{InstanceId} | Lists the default vocabularies for the specified Amazon Connect instance. |

### flow-associations-summary
| Method | Path | Description |
|--------|------|-------------|
| GET | /flow-associations-summary/{InstanceId} | List the flow association based on the filters. |

### hours-of-operations-summary
| Method | Path | Description |
|--------|------|-------------|
| GET | /hours-of-operations-summary/{InstanceId} | Provides information about the hours of operation for the specified Amazon Connect instance. For more information about hours of operation, see Set the Hours of Operation for a Queue in the Amazon Connect Administrator Guide. |

### phone-numbers-summary
| Method | Path | Description |
|--------|------|-------------|
| GET | /phone-numbers-summary/{InstanceId} | Provides information about the phone numbers for the specified Amazon Connect instance.  For more information about phone numbers, see Set Up Phone Numbers for Your Contact Center in the Amazon Connect Administrator Guide.    We recommend using ListPhoneNumbersV2 to return phone number types. ListPhoneNumbers doesn't support number types UIFN, SHARED, THIRD_PARTY_TF, and THIRD_PARTY_DID. While it returns numbers of those types, it incorrectly lists them as TOLL_FREE or DID.    The phone number Arn value that is returned from each of the items in the PhoneNumberSummaryList cannot be used to tag phone number resources. It will fail with a ResourceNotFoundException. Instead, use the ListPhoneNumbersV2 API. It returns the new phone number ARN that can be used to tag phone number resources. |

### prompts-summary
| Method | Path | Description |
|--------|------|-------------|
| GET | /prompts-summary/{InstanceId} | Provides information about the prompts for the specified Amazon Connect instance. |

### queues-summary
| Method | Path | Description |
|--------|------|-------------|
| GET | /queues-summary/{InstanceId} | Provides information about the queues for the specified Amazon Connect instance. If you do not specify a QueueTypes parameter, both standard and agent queues are returned. This might cause an unexpected truncation of results if you have more than 1000 agents and you limit the number of results of the API call in code. For more information about queues, see Queues: Standard and Agent in the Amazon Connect Administrator Guide. |

### routing-profiles-summary
| Method | Path | Description |
|--------|------|-------------|
| GET | /routing-profiles-summary/{InstanceId} | Provides summary information about the routing profiles for the specified Amazon Connect instance. For more information about routing profiles, see Routing Profiles and Create a Routing Profile in the Amazon Connect Administrator Guide. |

### security-profiles-applications
| Method | Path | Description |
|--------|------|-------------|
| GET | /security-profiles-applications/{InstanceId}/{SecurityProfileId} | Returns a list of third-party applications in a specific security profile. |

### security-profiles-permissions
| Method | Path | Description |
|--------|------|-------------|
| GET | /security-profiles-permissions/{InstanceId}/{SecurityProfileId} | Lists the permissions granted to a security profile. For information about security profiles, see Security Profiles in the Amazon Connect Administrator Guide. For a mapping of the API name and user interface name of the security profile permissions, see List of security profile permissions. |

### security-profiles-summary
| Method | Path | Description |
|--------|------|-------------|
| GET | /security-profiles-summary/{InstanceId} | Provides summary information about the security profiles for the specified Amazon Connect instance. For more information about security profiles, see Security Profiles in the Amazon Connect Administrator Guide. For a mapping of the API name and user interface name of the security profile permissions, see List of security profile permissions. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags/{resourceArn} | Lists the tags for the specified resource. For sample policies that use tags, see Amazon Connect Identity-Based Policy Examples in the Amazon Connect Administrator Guide. |
| POST | /tags/{resourceArn} | Adds the specified tags to the specified resource. Some of the supported resource types are agents, routing profiles, queues, quick connects, contact flows, agent statuses, hours of operation, phone numbers, security profiles, and task templates. For a complete list, see Tagging resources in Amazon Connect. For sample policies that use tags, see Amazon Connect Identity-Based Policy Examples in the Amazon Connect Administrator Guide. |
| DELETE | /tags/{resourceArn} | Removes the specified tags from the specified resource. |

### traffic-distribution-groups
| Method | Path | Description |
|--------|------|-------------|
| GET | /traffic-distribution-groups | Lists traffic distribution groups. |

### user-hierarchy-groups-summary
| Method | Path | Description |
|--------|------|-------------|
| GET | /user-hierarchy-groups-summary/{InstanceId} | Provides summary information about the hierarchy groups for the specified Amazon Connect instance. For more information about agent hierarchies, see Set Up Agent Hierarchies in the Amazon Connect Administrator Guide. |

### users-summary
| Method | Path | Description |
|--------|------|-------------|
| GET | /users-summary/{InstanceId} | Provides summary information about the users for the specified Amazon Connect instance. |

### search-agent-statuses
| Method | Path | Description |
|--------|------|-------------|
| POST | /search-agent-statuses | Searches AgentStatuses in an Amazon Connect instance, with optional filtering. |

### search-contact-flow-modules
| Method | Path | Description |
|--------|------|-------------|
| POST | /search-contact-flow-modules | Searches the flow modules in an Amazon Connect instance, with optional filtering. |

### search-contact-flows
| Method | Path | Description |
|--------|------|-------------|
| POST | /search-contact-flows | Searches the contact flows in an Amazon Connect instance, with optional filtering. |

### search-contacts
| Method | Path | Description |
|--------|------|-------------|
| POST | /search-contacts | Searches contacts in an Amazon Connect instance. |

### search-hours-of-operations
| Method | Path | Description |
|--------|------|-------------|
| POST | /search-hours-of-operations | Searches the hours of operation in an Amazon Connect instance, with optional filtering. |

### search-predefined-attributes
| Method | Path | Description |
|--------|------|-------------|
| POST | /search-predefined-attributes | Searches predefined attributes that meet certain criteria. Predefined attributes are attributes in an Amazon Connect instance that can be used to route contacts to an agent or pools of agents within a queue. For more information, see Create predefined attributes for routing contacts to agents. |

### search-prompts
| Method | Path | Description |
|--------|------|-------------|
| POST | /search-prompts | Searches prompts in an Amazon Connect instance, with optional filtering. |

### search-queues
| Method | Path | Description |
|--------|------|-------------|
| POST | /search-queues | Searches queues in an Amazon Connect instance, with optional filtering. |

### search-quick-connects
| Method | Path | Description |
|--------|------|-------------|
| POST | /search-quick-connects | Searches quick connects in an Amazon Connect instance, with optional filtering. |

### search-resource-tags
| Method | Path | Description |
|--------|------|-------------|
| POST | /search-resource-tags | Searches tags used in an Amazon Connect instance using optional search criteria. |

### search-routing-profiles
| Method | Path | Description |
|--------|------|-------------|
| POST | /search-routing-profiles | Searches routing profiles in an Amazon Connect instance, with optional filtering. |

### search-security-profiles
| Method | Path | Description |
|--------|------|-------------|
| POST | /search-security-profiles | Searches security profiles in an Amazon Connect instance, with optional filtering. For information about security profiles, see Security Profiles in the Amazon Connect Administrator Guide. For a mapping of the API name and user interface name of the security profile permissions, see List of security profile permissions. |

### search-user-hierarchy-groups
| Method | Path | Description |
|--------|------|-------------|
| POST | /search-user-hierarchy-groups | Searches UserHierarchyGroups in an Amazon Connect instance, with optional filtering.  The UserHierarchyGroup with "LevelId": "0" is the foundation for building levels on top of an instance. It is not user-definable, nor is it visible in the UI. |

### search-users
| Method | Path | Description |
|--------|------|-------------|
| POST | /search-users | Searches users in an Amazon Connect instance, with optional filtering.    AfterContactWorkTimeLimit is returned in milliseconds. |

### vocabulary-summary
| Method | Path | Description |
|--------|------|-------------|
| POST | /vocabulary-summary/{InstanceId} | Searches for vocabularies within a specific Amazon Connect instance using State, NameStartsWith, and LanguageCode. |

### chat-integration-event
| Method | Path | Description |
|--------|------|-------------|
| POST | /chat-integration-event | Processes chat integration events from Amazon Web Services or external integrations to Amazon Connect. A chat integration event includes:   SourceId, DestinationId, and Subtype: a set of identifiers, uniquely representing a chat    ChatEvent: details of the chat action to perform such as sending a message, event, or disconnecting from a chat   When a chat integration event is sent with chat identifiers that do not map to an active chat contact, a new chat contact is also created before handling chat action.  Access to this API is currently restricted to Amazon Pinpoint for supporting SMS integration. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a activate?" -> POST /evaluation-forms/{InstanceId}/{EvaluationFormId}/activate
- "Update a default-vocabulary?" -> PUT /default-vocabulary/{InstanceId}/{LanguageCode}
- "Update a flow-association?" -> PUT /flow-associations/{InstanceId}
- "Create a associate-quick-connect?" -> POST /queues/{InstanceId}/{QueueId}/associate-quick-connects
- "Create a associate-queue?" -> POST /routing-profiles/{InstanceId}/{RoutingProfileId}/associate-queues
- "Create a associate-proficiency?" -> POST /users/{InstanceId}/{UserId}/associate-proficiencies
- "Create a association?" -> POST /analytics-data/instance/{InstanceId}/associations
- "Update a batch?" -> PUT /contact/batch/{InstanceId}
- "Create a claim?" -> POST /phone-number/claim
- "Update a agent-status?" -> PUT /agent-status/{InstanceId}
- "Update a contact-flow?" -> PUT /contact-flows/{InstanceId}
- "Update a contact-flow-module?" -> PUT /contact-flow-modules/{InstanceId}
- "Update a evaluation-form?" -> PUT /evaluation-forms/{InstanceId}
- "Update a hours-of-operation?" -> PUT /hours-of-operations/{InstanceId}
- "Create a create-participant?" -> POST /contact/create-participant
- "Update a predefined-attribute?" -> PUT /predefined-attributes/{InstanceId}
- "Update a prompt?" -> PUT /prompts/{InstanceId}
- "Update a queue?" -> PUT /queues/{InstanceId}
- "Update a quick-connect?" -> PUT /quick-connects/{InstanceId}
- "Update a routing-profile?" -> PUT /routing-profiles/{InstanceId}
- "Update a security-profile?" -> PUT /security-profiles/{InstanceId}
- "Update a user?" -> PUT /users/{InstanceId}
- "Update a user-hierarchy-group?" -> PUT /user-hierarchy-groups/{InstanceId}
- "Update a view?" -> PUT /views/{InstanceId}
- "Create a deactivate?" -> POST /evaluation-forms/{InstanceId}/{EvaluationFormId}/deactivate
- "Delete a attached-file?" -> DELETE /attached-files/{InstanceId}/{FileId}
- "Delete a contact-evaluation?" -> DELETE /contact-evaluations/{InstanceId}/{EvaluationId}
- "Delete a contact-flow?" -> DELETE /contact-flows/{InstanceId}/{ContactFlowId}
- "Delete a contact-flow-module?" -> DELETE /contact-flow-modules/{InstanceId}/{ContactFlowModuleId}
- "Delete a evaluation-form?" -> DELETE /evaluation-forms/{InstanceId}/{EvaluationFormId}
- "Delete a hours-of-operation?" -> DELETE /hours-of-operations/{InstanceId}/{HoursOfOperationId}
- "Delete a instance?" -> DELETE /instance/{InstanceId}
- "Delete a integration-association?" -> DELETE /instance/{InstanceId}/integration-associations/{IntegrationAssociationId}
- "Delete a predefined-attribute?" -> DELETE /predefined-attributes/{InstanceId}/{Name}
- "Delete a prompt?" -> DELETE /prompts/{InstanceId}/{PromptId}
- "Delete a queue?" -> DELETE /queues/{InstanceId}/{QueueId}
- "Delete a quick-connect?" -> DELETE /quick-connects/{InstanceId}/{QuickConnectId}
- "Delete a routing-profile?" -> DELETE /routing-profiles/{InstanceId}/{RoutingProfileId}
- "Delete a rule?" -> DELETE /rules/{InstanceId}/{RuleId}
- "Delete a security-profile?" -> DELETE /security-profiles/{InstanceId}/{SecurityProfileId}
- "Delete a template?" -> DELETE /instance/{InstanceId}/task/template/{TaskTemplateId}
- "Delete a traffic-distribution-group?" -> DELETE /traffic-distribution-group/{TrafficDistributionGroupId}
- "Delete a use-case?" -> DELETE /instance/{InstanceId}/integration-associations/{IntegrationAssociationId}/use-cases/{UseCaseId}
- "Delete a user?" -> DELETE /users/{InstanceId}/{UserId}
- "Delete a user-hierarchy-group?" -> DELETE /user-hierarchy-groups/{InstanceId}/{HierarchyGroupId}
- "Delete a view?" -> DELETE /views/{InstanceId}/{ViewId}
- "Delete a version?" -> DELETE /views/{InstanceId}/{ViewId}/versions/{ViewVersion}
- "Get agent-status details?" -> GET /agent-status/{InstanceId}/{AgentStatusId}
- "Get authentication-profile details?" -> GET /authentication-profiles/{InstanceId}/{AuthenticationProfileId}
- "Get contact details?" -> GET /contacts/{InstanceId}/{ContactId}
- "Get contact-evaluation details?" -> GET /contact-evaluations/{InstanceId}/{EvaluationId}
- "Get contact-flow details?" -> GET /contact-flows/{InstanceId}/{ContactFlowId}
- "Get contact-flow-module details?" -> GET /contact-flow-modules/{InstanceId}/{ContactFlowModuleId}
- "Get evaluation-form details?" -> GET /evaluation-forms/{InstanceId}/{EvaluationFormId}
- "Get hours-of-operation details?" -> GET /hours-of-operations/{InstanceId}/{HoursOfOperationId}
- "Get instance details?" -> GET /instance/{InstanceId}
- "Get attribute details?" -> GET /instance/{InstanceId}/attribute/{AttributeType}
- "Get storage-config details?" -> GET /instance/{InstanceId}/storage-config/{AssociationId}
- "Get phone-number details?" -> GET /phone-number/{PhoneNumberId}
- "Get predefined-attribute details?" -> GET /predefined-attributes/{InstanceId}/{Name}
- "Get prompt details?" -> GET /prompts/{InstanceId}/{PromptId}
- "Get queue details?" -> GET /queues/{InstanceId}/{QueueId}
- "Get quick-connect details?" -> GET /quick-connects/{InstanceId}/{QuickConnectId}
- "Get routing-profile details?" -> GET /routing-profiles/{InstanceId}/{RoutingProfileId}
- "Get rule details?" -> GET /rules/{InstanceId}/{RuleId}
- "Get security-profile details?" -> GET /security-profiles/{InstanceId}/{SecurityProfileId}
- "Get traffic-distribution-group details?" -> GET /traffic-distribution-group/{TrafficDistributionGroupId}
- "Get user details?" -> GET /users/{InstanceId}/{UserId}
- "Get user-hierarchy-group details?" -> GET /user-hierarchy-groups/{InstanceId}/{HierarchyGroupId}
- "Get user-hierarchy-structure details?" -> GET /user-hierarchy-structure/{InstanceId}
- "Get view details?" -> GET /views/{InstanceId}/{ViewId}
- "Get vocabulary details?" -> GET /vocabulary/{InstanceId}/{VocabularyId}
- "Create a association?" -> POST /analytics-data/instance/{InstanceId}/association
- "Create a bot?" -> POST /instance/{InstanceId}/bot
- "Delete a flow-association?" -> DELETE /flow-associations/{InstanceId}/{ResourceId}/{ResourceType}
- "Delete a storage-config?" -> DELETE /instance/{InstanceId}/storage-config/{AssociationId}
- "Create a disassociate-quick-connect?" -> POST /queues/{InstanceId}/{QueueId}/disassociate-quick-connects
- "Create a disassociate-queue?" -> POST /routing-profiles/{InstanceId}/{RoutingProfileId}/disassociate-queues
- "Delete a security-key?" -> DELETE /instance/{InstanceId}/security-key/{AssociationId}
- "Create a disassociate-proficiency?" -> POST /users/{InstanceId}/{UserId}/disassociate-proficiencies
- "Create a contact?" -> POST /users/{InstanceId}/{UserId}/contact
- "Get attached-file details?" -> GET /attached-files/{InstanceId}/{FileId}
- "Get attribute details?" -> GET /contact/attributes/{InstanceId}/{InitialContactId}
- "Get federate details?" -> GET /user/federate/{InstanceId}
- "Get flow-association details?" -> GET /flow-associations/{InstanceId}/{ResourceId}/{ResourceType}
- "Create a data?" -> POST /metrics/data
- "List all file?" -> GET /prompts/{InstanceId}/{PromptId}/file
- "Get template details?" -> GET /instance/{InstanceId}/task/template/{TaskTemplateId}
- "Get traffic-distribution details?" -> GET /traffic-distribution/{Id}
- "Create a import?" -> POST /phone-number/import
- "Get agent-status details?" -> GET /agent-status/{InstanceId}
- "List all association?" -> GET /analytics-data/instance/{InstanceId}/association
- "List all approved-origins?" -> GET /instance/{InstanceId}/approved-origins
- "Get authentication-profiles-summary details?" -> GET /authentication-profiles-summary/{InstanceId}
- "List all bots?" -> GET /instance/{InstanceId}/bots
- "Get contact-evaluation details?" -> GET /contact-evaluations/{InstanceId}
- "Get contact-flow-modules-summary details?" -> GET /contact-flow-modules-summary/{InstanceId}
- "Get contact-flows-summary details?" -> GET /contact-flows-summary/{InstanceId}
- "Get reference details?" -> GET /contact/references/{InstanceId}/{ContactId}
- "List all versions?" -> GET /evaluation-forms/{InstanceId}/{EvaluationFormId}/versions
- "Get evaluation-form details?" -> GET /evaluation-forms/{InstanceId}
- "Get flow-associations-summary details?" -> GET /flow-associations-summary/{InstanceId}
- "Get hours-of-operations-summary details?" -> GET /hours-of-operations-summary/{InstanceId}
- "List all attributes?" -> GET /instance/{InstanceId}/attributes
- "List all storage-configs?" -> GET /instance/{InstanceId}/storage-configs
- "List all instance?" -> GET /instance
- "List all integration-associations?" -> GET /instance/{InstanceId}/integration-associations
- "List all lambda-functions?" -> GET /instance/{InstanceId}/lambda-functions
- "List all lex-bots?" -> GET /instance/{InstanceId}/lex-bots
- "Get phone-numbers-summary details?" -> GET /phone-numbers-summary/{InstanceId}
- "Create a list?" -> POST /phone-number/list
- "Get predefined-attribute details?" -> GET /predefined-attributes/{InstanceId}
- "Get prompts-summary details?" -> GET /prompts-summary/{InstanceId}
- "List all quick-connects?" -> GET /queues/{InstanceId}/{QueueId}/quick-connects
- "Get queues-summary details?" -> GET /queues-summary/{InstanceId}
- "Get quick-connect details?" -> GET /quick-connects/{InstanceId}
- "List all queues?" -> GET /routing-profiles/{InstanceId}/{RoutingProfileId}/queues
- "Get routing-profiles-summary details?" -> GET /routing-profiles-summary/{InstanceId}
- "Get rule details?" -> GET /rules/{InstanceId}
- "List all security-keys?" -> GET /instance/{InstanceId}/security-keys
- "Get security-profiles-application details?" -> GET /security-profiles-applications/{InstanceId}/{SecurityProfileId}
- "Get security-profiles-permission details?" -> GET /security-profiles-permissions/{InstanceId}/{SecurityProfileId}
- "Get security-profiles-summary details?" -> GET /security-profiles-summary/{InstanceId}
- "Get tag details?" -> GET /tags/{resourceArn}
- "List all template?" -> GET /instance/{InstanceId}/task/template
- "List all user?" -> GET /traffic-distribution-group/{TrafficDistributionGroupId}/user
- "List all traffic-distribution-groups?" -> GET /traffic-distribution-groups
- "List all use-cases?" -> GET /instance/{InstanceId}/integration-associations/{IntegrationAssociationId}/use-cases
- "Get user-hierarchy-groups-summary details?" -> GET /user-hierarchy-groups-summary/{InstanceId}
- "List all proficiencies?" -> GET /users/{InstanceId}/{UserId}/proficiencies
- "Get users-summary details?" -> GET /users-summary/{InstanceId}
- "List all versions?" -> GET /views/{InstanceId}/{ViewId}/versions
- "Get view details?" -> GET /views/{InstanceId}
- "Create a monitor?" -> POST /contact/monitor
- "Create a pause?" -> POST /contact/pause
- "Delete a phone-number?" -> DELETE /phone-number/{PhoneNumberId}
- "Create a replicate?" -> POST /instance/{InstanceId}/replicate
- "Create a resume?" -> POST /contact/resume
- "Create a resume-recording?" -> POST /contact/resume-recording
- "Create a search-agent-statuse?" -> POST /search-agent-statuses
- "Create a search-available?" -> POST /phone-number/search-available
- "Create a search-contact-flow-module?" -> POST /search-contact-flow-modules
- "Create a search-contact-flow?" -> POST /search-contact-flows
- "Create a search-contact?" -> POST /search-contacts
- "Create a search-hours-of-operation?" -> POST /search-hours-of-operations
- "Create a search-predefined-attribute?" -> POST /search-predefined-attributes
- "Create a search-prompt?" -> POST /search-prompts
- "Create a search-queue?" -> POST /search-queues
- "Create a search-quick-connect?" -> POST /search-quick-connects
- "Create a search-resource-tag?" -> POST /search-resource-tags
- "Create a search-routing-profile?" -> POST /search-routing-profiles
- "Create a search-security-profile?" -> POST /search-security-profiles
- "Create a search-user-hierarchy-group?" -> POST /search-user-hierarchy-groups
- "Create a search-user?" -> POST /search-users
- "Create a chat-integration-event?" -> POST /chat-integration-event
- "Update a attached-file?" -> PUT /attached-files/{InstanceId}
- "Update a contact-evaluation?" -> PUT /contact-evaluations/{InstanceId}
- "Create a start-recording?" -> POST /contact/start-recording
- "Create a start-streaming?" -> POST /contact/start-streaming
- "Create a stop?" -> POST /contact/stop
- "Create a stop-recording?" -> POST /contact/stop-recording
- "Create a stop-streaming?" -> POST /contact/stop-streaming
- "Create a submit?" -> POST /contact-evaluations/{InstanceId}/{EvaluationId}/submit
- "Create a suspend-recording?" -> POST /contact/suspend-recording
- "Create a tag?" -> POST /contact/tags
- "Create a transfer?" -> POST /contact/transfer
- "Delete a tag?" -> DELETE /contact/tags/{InstanceId}/{ContactId}
- "Delete a tag?" -> DELETE /tags/{resourceArn}
- "Create a attribute?" -> POST /contact/attributes
- "Create a content?" -> POST /contact-flows/{InstanceId}/{ContactFlowId}/content
- "Create a metadata?" -> POST /contact-flows/{InstanceId}/{ContactFlowId}/metadata
- "Create a content?" -> POST /contact-flow-modules/{InstanceId}/{ContactFlowModuleId}/content
- "Create a metadata?" -> POST /contact-flow-modules/{InstanceId}/{ContactFlowModuleId}/metadata
- "Create a name?" -> POST /contact-flows/{InstanceId}/{ContactFlowId}/name
- "Create a routing-data?" -> POST /contacts/{InstanceId}/{ContactId}/routing-data
- "Create a schedule?" -> POST /contact/schedule
- "Update a evaluation-form?" -> PUT /evaluation-forms/{InstanceId}/{EvaluationFormId}
- "Update a participant-role-config?" -> PUT /contact/participant-role-config/{InstanceId}/{ContactId}
- "Update a phone-number?" -> PUT /phone-number/{PhoneNumberId}
- "Create a hours-of-operation?" -> POST /queues/{InstanceId}/{QueueId}/hours-of-operation
- "Create a max-contact?" -> POST /queues/{InstanceId}/{QueueId}/max-contacts
- "Create a name?" -> POST /queues/{InstanceId}/{QueueId}/name
- "Create a outbound-caller-config?" -> POST /queues/{InstanceId}/{QueueId}/outbound-caller-config
- "Create a status?" -> POST /queues/{InstanceId}/{QueueId}/status
- "Create a config?" -> POST /quick-connects/{InstanceId}/{QuickConnectId}/config
- "Create a name?" -> POST /quick-connects/{InstanceId}/{QuickConnectId}/name
- "Create a agent-availability-timer?" -> POST /routing-profiles/{InstanceId}/{RoutingProfileId}/agent-availability-timer
- "Create a concurrency?" -> POST /routing-profiles/{InstanceId}/{RoutingProfileId}/concurrency
- "Create a default-outbound-queue?" -> POST /routing-profiles/{InstanceId}/{RoutingProfileId}/default-outbound-queue
- "Create a name?" -> POST /routing-profiles/{InstanceId}/{RoutingProfileId}/name
- "Create a queue?" -> POST /routing-profiles/{InstanceId}/{RoutingProfileId}/queues
- "Update a rule?" -> PUT /rules/{InstanceId}/{RuleId}
- "Update a traffic-distribution?" -> PUT /traffic-distribution/{Id}
- "Create a hierarchy?" -> POST /users/{InstanceId}/{UserId}/hierarchy
- "Create a name?" -> POST /user-hierarchy-groups/{InstanceId}/{HierarchyGroupId}/name
- "Create a identity-info?" -> POST /users/{InstanceId}/{UserId}/identity-info
- "Create a phone-config?" -> POST /users/{InstanceId}/{UserId}/phone-config
- "Create a proficiency?" -> POST /users/{InstanceId}/{UserId}/proficiencies
- "Create a routing-profile?" -> POST /users/{InstanceId}/{UserId}/routing-profile
- "Create a security-profile?" -> POST /users/{InstanceId}/{UserId}/security-profiles
- "Create a metadata?" -> POST /views/{InstanceId}/{ViewId}/metadata
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
