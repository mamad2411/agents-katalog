---
name: aws-iot
description: "AWS IoT API skill. Use when working with AWS IoT for accept-certificate-transfer, billing-groups, thing-groups. Covers 255 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS IoT
API version: 2015-05-28

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /audit/configuration -- verify access
3. POST /jobs/{jobId}/targets -- create first targets

## Endpoints

255 endpoints across 69 groups. See references/api-spec.lap for full details.

### accept-certificate-transfer
| Method | Path | Description |
|--------|------|-------------|
| PATCH | /accept-certificate-transfer/{certificateId} | Accepts a pending certificate transfer. The default state of the certificate is INACTIVE. To check for pending certificate transfers, call ListCertificates to enumerate your certificates. Requires permission to access the AcceptCertificateTransfer action. |

### billing-groups
| Method | Path | Description |
|--------|------|-------------|
| PUT | /billing-groups/addThingToBillingGroup | Adds a thing to a billing group. Requires permission to access the AddThingToBillingGroup action. |
| POST | /billing-groups/{billingGroupName} | Creates a billing group. Requires permission to access the CreateBillingGroup action. |
| DELETE | /billing-groups/{billingGroupName} | Deletes the billing group. Requires permission to access the DeleteBillingGroup action. |
| GET | /billing-groups/{billingGroupName} | Returns information about a billing group. Requires permission to access the DescribeBillingGroup action. |
| GET | /billing-groups | Lists the billing groups you have created. Requires permission to access the ListBillingGroups action. |
| GET | /billing-groups/{billingGroupName}/things | Lists the things you have added to the given billing group. Requires permission to access the ListThingsInBillingGroup action. |
| PUT | /billing-groups/removeThingFromBillingGroup | Removes the given thing from the billing group. Requires permission to access the RemoveThingFromBillingGroup action.  This call is asynchronous. It might take several seconds for the detachment to propagate. |
| PATCH | /billing-groups/{billingGroupName} | Updates information about the billing group. Requires permission to access the UpdateBillingGroup action. |

### thing-groups
| Method | Path | Description |
|--------|------|-------------|
| PUT | /thing-groups/addThingToThingGroup | Adds a thing to a thing group. Requires permission to access the AddThingToThingGroup action. |
| POST | /thing-groups/{thingGroupName} | Create a thing group.  This is a control plane operation. See Authorization for information about authorizing control plane actions. If the ThingGroup that you create has the exact same attributes as an existing ThingGroup, you will get a 200 success response.   Requires permission to access the CreateThingGroup action. |
| DELETE | /thing-groups/{thingGroupName} | Deletes a thing group. Requires permission to access the DeleteThingGroup action. |
| GET | /thing-groups/{thingGroupName} | Describe a thing group. Requires permission to access the DescribeThingGroup action. |
| GET | /thing-groups | List the thing groups in your account. Requires permission to access the ListThingGroups action. |
| GET | /thing-groups/{thingGroupName}/things | Lists the things in the specified group. Requires permission to access the ListThingsInThingGroup action. |
| PUT | /thing-groups/removeThingFromThingGroup | Remove the specified thing from the specified group. You must specify either a thingGroupArn or a thingGroupName to identify the thing group and either a thingArn or a thingName to identify the thing to remove from the thing group.  Requires permission to access the RemoveThingFromThingGroup action. |
| PATCH | /thing-groups/{thingGroupName} | Update a thing group. Requires permission to access the UpdateThingGroup action. |
| PUT | /thing-groups/updateThingGroupsForThing | Updates the groups to which the thing belongs. Requires permission to access the UpdateThingGroupsForThing action. |

### jobs
| Method | Path | Description |
|--------|------|-------------|
| POST | /jobs/{jobId}/targets | Associates a group with a continuous job. The following criteria must be met:    The job must have been created with the targetSelection field set to "CONTINUOUS".   The job status must currently be "IN_PROGRESS".   The total number of targets associated with a job must not exceed 100.   Requires permission to access the AssociateTargetsWithJob action. |
| PUT | /jobs/{jobId}/cancel | Cancels a job. Requires permission to access the CancelJob action. |
| PUT | /jobs/{jobId} | Creates a job. Requires permission to access the CreateJob action. |
| DELETE | /jobs/{jobId} | Deletes a job and its related job executions. Deleting a job may take time, depending on the number of job executions created for the job and various other factors. While the job is being deleted, the status of the job will be shown as "DELETION_IN_PROGRESS". Attempting to delete or cancel a job whose status is already "DELETION_IN_PROGRESS" will result in an error. Only 10 jobs may have status "DELETION_IN_PROGRESS" at the same time, or a LimitExceededException will occur. Requires permission to access the DeleteJob action. |
| GET | /jobs/{jobId} | Describes a job. Requires permission to access the DescribeJob action. |
| GET | /jobs/{jobId}/job-document | Gets a job document. Requires permission to access the GetJobDocument action. |
| GET | /jobs/{jobId}/things | Lists the job executions for a job. Requires permission to access the ListJobExecutionsForJob action. |
| GET | /jobs | Lists jobs. Requires permission to access the ListJobs action. |
| PATCH | /jobs/{jobId} | Updates supported fields of the specified job. Requires permission to access the UpdateJob action. |

### target-policies
| Method | Path | Description |
|--------|------|-------------|
| PUT | /target-policies/{policyName} | Attaches the specified policy to the specified principal (certificate or other credential). Requires permission to access the AttachPolicy action. |
| POST | /target-policies/{policyName} | Detaches a policy from the specified target.  Because of the distributed nature of Amazon Web Services, it can take up to five minutes after a policy is detached before it's ready to be deleted.  Requires permission to access the DetachPolicy action. |

### principal-policies
| Method | Path | Description |
|--------|------|-------------|
| PUT | /principal-policies/{policyName} | Attaches the specified policy to the specified principal (certificate or other credential).  Note: This action is deprecated and works as expected for backward compatibility, but we won't add enhancements. Use AttachPolicy instead. Requires permission to access the AttachPrincipalPolicy action. |
| DELETE | /principal-policies/{policyName} | Removes the specified policy from the specified certificate.  Note: This action is deprecated and works as expected for backward compatibility, but we won't add enhancements. Use DetachPolicy instead. Requires permission to access the DetachPrincipalPolicy action. |
| GET | /principal-policies | Lists the policies attached to the specified principal. If you use an Cognito identity, the ID must be in AmazonCognito Identity format.  Note: This action is deprecated and works as expected for backward compatibility, but we won't add enhancements. Use ListAttachedPolicies instead. Requires permission to access the ListPrincipalPolicies action. |

### security-profiles
| Method | Path | Description |
|--------|------|-------------|
| PUT | /security-profiles/{securityProfileName}/targets | Associates a Device Defender security profile with a thing group or this account. Each thing group or account can have up to five security profiles associated with it. Requires permission to access the AttachSecurityProfile action. |
| POST | /security-profiles/{securityProfileName} | Creates a Device Defender security profile. Requires permission to access the CreateSecurityProfile action. |
| DELETE | /security-profiles/{securityProfileName} | Deletes a Device Defender security profile. Requires permission to access the DeleteSecurityProfile action. |
| GET | /security-profiles/{securityProfileName} | Gets information about a Device Defender security profile. Requires permission to access the DescribeSecurityProfile action. |
| DELETE | /security-profiles/{securityProfileName}/targets | Disassociates a Device Defender security profile from a thing group or from this account. Requires permission to access the DetachSecurityProfile action. |
| GET | /security-profiles | Lists the Device Defender security profiles you've created. You can filter security profiles by dimension or custom metric. Requires permission to access the ListSecurityProfiles action.   dimensionName and metricName cannot be used in the same request. |
| GET | /security-profiles/{securityProfileName}/targets | Lists the targets (thing groups) associated with a given Device Defender security profile. Requires permission to access the ListTargetsForSecurityProfile action. |
| PATCH | /security-profiles/{securityProfileName} | Updates a Device Defender security profile. Requires permission to access the UpdateSecurityProfile action. |

### things
| Method | Path | Description |
|--------|------|-------------|
| PUT | /things/{thingName}/principals | Attaches the specified principal to the specified thing. A principal can be X.509 certificates, Amazon Cognito identities or federated identities. Requires permission to access the AttachThingPrincipal action. |
| PUT | /things/{thingName}/jobs/{jobId}/cancel | Cancels the execution of a job for a given thing. Requires permission to access the CancelJobExecution action. |
| POST | /things/{thingName} | Creates a thing record in the registry. If this call is made multiple times using the same thing name and configuration, the call will succeed. If this call is made with the same thing name but different configuration a ResourceAlreadyExistsException is thrown.  This is a control plane operation. See Authorization for information about authorizing control plane actions.  Requires permission to access the CreateThing action. |
| DELETE | /things/{thingName}/jobs/{jobId}/executionNumber/{executionNumber} | Deletes a job execution. Requires permission to access the DeleteJobExecution action. |
| DELETE | /things/{thingName} | Deletes the specified thing. Returns successfully with no error if the deletion is successful or you specify a thing that doesn't exist. Requires permission to access the DeleteThing action. |
| GET | /things/{thingName}/jobs/{jobId} | Describes a job execution. Requires permission to access the DescribeJobExecution action. |
| GET | /things/{thingName} | Gets information about the specified thing. Requires permission to access the DescribeThing action. |
| DELETE | /things/{thingName}/principals | Detaches the specified principal from the specified thing. A principal can be X.509 certificates, IAM users, groups, and roles, Amazon Cognito identities or federated identities.  This call is asynchronous. It might take several seconds for the detachment to propagate.  Requires permission to access the DetachThingPrincipal action. |
| GET | /things/{thingName}/jobs | Lists the job executions for the specified thing. Requires permission to access the ListJobExecutionsForThing action. |
| GET | /things/{thingName}/thing-groups | List the thing groups to which the specified thing belongs. Requires permission to access the ListThingGroupsForThing action. |
| GET | /things/{thingName}/principals | Lists the principals associated with the specified thing. A principal can be X.509 certificates, IAM users, groups, and roles, Amazon Cognito identities or federated identities. Requires permission to access the ListThingPrincipals action. |
| GET | /things | Lists your things. Use the attributeName and attributeValue parameters to filter your things. For example, calling ListThings with attributeName=Color and attributeValue=Red retrieves all things in the registry that contain an attribute Color with the value Red. For more information, see List Things from the Amazon Web Services IoT Core Developer Guide. Requires permission to access the ListThings action.  You will not be charged for calling this API if an Access denied error is returned. You will also not be charged if no attributes or pagination token was provided in request and no pagination token and no results were returned. |
| POST | /things | Provisions a thing in the device registry. RegisterThing calls other IoT control plane APIs. These calls might exceed your account level  IoT Throttling Limits and cause throttle errors. Please contact Amazon Web Services Customer Support to raise your throttling limits if necessary. Requires permission to access the RegisterThing action. |
| PATCH | /things/{thingName} | Updates the data for a thing. Requires permission to access the UpdateThing action. |

### audit
| Method | Path | Description |
|--------|------|-------------|
| PUT | /audit/mitigationactions/tasks/{taskId}/cancel | Cancels a mitigation action task that is in progress. If the task is not in progress, an InvalidRequestException occurs. Requires permission to access the CancelAuditMitigationActionsTask action. |
| PUT | /audit/tasks/{taskId}/cancel | Cancels an audit that is in progress. The audit can be either scheduled or on demand. If the audit isn't in progress, an "InvalidRequestException" occurs. Requires permission to access the CancelAuditTask action. |
| POST | /audit/suppressions/create | Creates a Device Defender audit suppression.  Requires permission to access the CreateAuditSuppression action. |
| POST | /audit/scheduledaudits/{scheduledAuditName} | Creates a scheduled audit that is run at a specified time interval. Requires permission to access the CreateScheduledAudit action. |
| DELETE | /audit/configuration | Restores the default settings for Device Defender audits for this account. Any configuration data you entered is deleted and all audit checks are reset to disabled.  Requires permission to access the DeleteAccountAuditConfiguration action. |
| POST | /audit/suppressions/delete | Deletes a Device Defender audit suppression.  Requires permission to access the DeleteAuditSuppression action. |
| DELETE | /audit/scheduledaudits/{scheduledAuditName} | Deletes a scheduled audit. Requires permission to access the DeleteScheduledAudit action. |
| GET | /audit/configuration | Gets information about the Device Defender audit settings for this account. Settings include how audit notifications are sent and which audit checks are enabled or disabled. Requires permission to access the DescribeAccountAuditConfiguration action. |
| GET | /audit/findings/{findingId} | Gets information about a single audit finding. Properties include the reason for noncompliance, the severity of the issue, and the start time when the audit that returned the finding. Requires permission to access the DescribeAuditFinding action. |
| GET | /audit/mitigationactions/tasks/{taskId} | Gets information about an audit mitigation task that is used to apply mitigation actions to a set of audit findings. Properties include the actions being applied, the audit checks to which they're being applied, the task status, and aggregated task statistics. |
| POST | /audit/suppressions/describe | Gets information about a Device Defender audit suppression. |
| GET | /audit/tasks/{taskId} | Gets information about a Device Defender audit. Requires permission to access the DescribeAuditTask action. |
| GET | /audit/scheduledaudits/{scheduledAuditName} | Gets information about a scheduled audit. Requires permission to access the DescribeScheduledAudit action. |
| POST | /audit/findings | Lists the findings (results) of a Device Defender audit or of the audits performed during a specified time period. (Findings are retained for 90 days.) Requires permission to access the ListAuditFindings action. |
| GET | /audit/mitigationactions/executions | Gets the status of audit mitigation action tasks that were executed. Requires permission to access the ListAuditMitigationActionsExecutions action. |
| GET | /audit/mitigationactions/tasks | Gets a list of audit mitigation action tasks that match the specified filters. Requires permission to access the ListAuditMitigationActionsTasks action. |
| POST | /audit/suppressions/list | Lists your Device Defender audit listings.  Requires permission to access the ListAuditSuppressions action. |
| GET | /audit/tasks | Lists the Device Defender audits that have been performed during a given time period. Requires permission to access the ListAuditTasks action. |
| GET | /audit/relatedResources | The related resources of an Audit finding. The following resources can be returned from calling this API:   DEVICE_CERTIFICATE   CA_CERTIFICATE   IOT_POLICY   COGNITO_IDENTITY_POOL   CLIENT_ID   ACCOUNT_SETTINGS   ROLE_ALIAS   IAM_ROLE   ISSUER_CERTIFICATE    This API is similar to DescribeAuditFinding's RelatedResources but provides pagination and is not limited to 10 resources. When calling DescribeAuditFinding for the intermediate CA revoked for active device certificates check, RelatedResources will not be populated. You must use this API, ListRelatedResourcesForAuditFinding, to list the certificates. |
| GET | /audit/scheduledaudits | Lists all of your scheduled audits. Requires permission to access the ListScheduledAudits action. |
| POST | /audit/mitigationactions/tasks/{taskId} | Starts a task that applies a set of mitigation actions to the specified target. Requires permission to access the StartAuditMitigationActionsTask action. |
| POST | /audit/tasks | Starts an on-demand Device Defender audit. Requires permission to access the StartOnDemandAuditTask action. |
| PATCH | /audit/configuration | Configures or reconfigures the Device Defender audit settings for this account. Settings include how audit notifications are sent and which audit checks are enabled or disabled. Requires permission to access the UpdateAccountAuditConfiguration action. |
| PATCH | /audit/suppressions/update | Updates a Device Defender audit suppression. |
| PATCH | /audit/scheduledaudits/{scheduledAuditName} | Updates a scheduled audit, including which checks are performed and how often the audit takes place. Requires permission to access the UpdateScheduledAudit action. |

### cancel-certificate-transfer
| Method | Path | Description |
|--------|------|-------------|
| PATCH | /cancel-certificate-transfer/{certificateId} | Cancels a pending transfer for the specified certificate.  Note Only the transfer source account can use this operation to cancel a transfer. (Transfer destinations can use RejectCertificateTransfer instead.) After transfer, IoT returns the certificate to the source account in the INACTIVE state. After the destination account has accepted the transfer, the transfer cannot be cancelled. After a certificate transfer is cancelled, the status of the certificate changes from PENDING_TRANSFER to INACTIVE. Requires permission to access the CancelCertificateTransfer action. |

### detect
| Method | Path | Description |
|--------|------|-------------|
| PUT | /detect/mitigationactions/tasks/{taskId}/cancel | Cancels a Device Defender ML Detect mitigation action.  Requires permission to access the CancelDetectMitigationActionsTask action. |
| GET | /detect/mitigationactions/tasks/{taskId} | Gets information about a Device Defender ML Detect mitigation action.  Requires permission to access the DescribeDetectMitigationActionsTask action. |
| GET | /detect/mitigationactions/executions | Lists mitigation actions executions for a Device Defender ML Detect Security Profile.  Requires permission to access the ListDetectMitigationActionsExecutions action. |
| GET | /detect/mitigationactions/tasks | List of Device Defender ML Detect mitigation actions tasks.  Requires permission to access the ListDetectMitigationActionsTasks action. |
| PUT | /detect/mitigationactions/tasks/{taskId} | Starts a Device Defender ML Detect mitigation actions task.  Requires permission to access the StartDetectMitigationActionsTask action. |

### default-authorizer
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /default-authorizer | Clears the default authorizer. Requires permission to access the ClearDefaultAuthorizer action. |
| GET | /default-authorizer | Describes the default authorizer. Requires permission to access the DescribeDefaultAuthorizer action. |
| POST | /default-authorizer | Sets the default authorizer. This will be used if a websocket connection is made without specifying an authorizer. Requires permission to access the SetDefaultAuthorizer action. |

### confirmdestination
| Method | Path | Description |
|--------|------|-------------|
| GET | /confirmdestination/{confirmationToken+} | Confirms a topic rule destination. When you create a rule requiring a destination, IoT sends a confirmation message to the endpoint or base address you specify. The message includes a token which you pass back when calling ConfirmTopicRuleDestination to confirm that you own or have access to the endpoint. Requires permission to access the ConfirmTopicRuleDestination action. |

### authorizer
| Method | Path | Description |
|--------|------|-------------|
| POST | /authorizer/{authorizerName} | Creates an authorizer. Requires permission to access the CreateAuthorizer action. |
| DELETE | /authorizer/{authorizerName} | Deletes an authorizer. Requires permission to access the DeleteAuthorizer action. |
| GET | /authorizer/{authorizerName} | Describes an authorizer. Requires permission to access the DescribeAuthorizer action. |
| POST | /authorizer/{authorizerName}/test | Tests a custom authorization behavior by invoking a specified custom authorizer. Use this to test and debug the custom authorization behavior of devices that connect to the IoT device gateway. Requires permission to access the TestInvokeAuthorizer action. |
| PUT | /authorizer/{authorizerName} | Updates an authorizer. Requires permission to access the UpdateAuthorizer action. |

### certificates
| Method | Path | Description |
|--------|------|-------------|
| POST | /certificates | Creates an X.509 certificate using the specified certificate signing request.  Requires permission to access the CreateCertificateFromCsr action.   The CSR must include a public key that is either an RSA key with a length of at least 2048 bits or an ECC key from NIST P-256, NIST P-384, or NIST P-521 curves. For supported certificates, consult  Certificate signing algorithms supported by IoT.    Reusing the same certificate signing request (CSR) results in a distinct certificate.  You can create multiple certificates in a batch by creating a directory, copying multiple .csr files into that directory, and then specifying that directory on the command line. The following commands show how to create a batch of certificates given a batch of CSRs. In the following commands, we assume that a set of CSRs are located inside of the directory my-csr-directory: On Linux and OS X, the command is:   $ ls my-csr-directory/ | xargs -I {} aws iot create-certificate-from-csr --certificate-signing-request file://my-csr-directory/{}  This command lists all of the CSRs in my-csr-directory and pipes each CSR file name to the aws iot create-certificate-from-csr Amazon Web Services CLI command to create a certificate for the corresponding CSR.  You can also run the aws iot create-certificate-from-csr part of the command in parallel to speed up the certificate creation process:  $ ls my-csr-directory/ | xargs -P 10 -I {} aws iot create-certificate-from-csr --certificate-signing-request file://my-csr-directory/{}   On Windows PowerShell, the command to create certificates for all CSRs in my-csr-directory is:  &gt; ls -Name my-csr-directory | %{aws iot create-certificate-from-csr --certificate-signing-request file://my-csr-directory/$_}   On a Windows command prompt, the command to create certificates for all CSRs in my-csr-directory is:  &gt; forfiles /p my-csr-directory /c "cmd /c aws iot create-certificate-from-csr --certificate-signing-request file://@path" |
| DELETE | /certificates/{certificateId} | Deletes the specified certificate. A certificate cannot be deleted if it has a policy or IoT thing attached to it or if its status is set to ACTIVE. To delete a certificate, first use the DetachPolicy action to detach all policies. Next, use the UpdateCertificate action to set the certificate to the INACTIVE status. Requires permission to access the DeleteCertificate action. |
| GET | /certificates/{certificateId} | Gets information about the specified certificate. Requires permission to access the DescribeCertificate action. |
| GET | /certificates | Lists the certificates registered in your Amazon Web Services account. The results are paginated with a default page size of 25. You can use the returned marker to retrieve additional results. Requires permission to access the ListCertificates action. |
| PUT | /certificates/{certificateId} | Updates the status of the specified certificate. This operation is idempotent. Requires permission to access the UpdateCertificate action. Certificates must be in the ACTIVE state to authenticate devices that use a certificate to connect to IoT. Within a few minutes of updating a certificate from the ACTIVE state to any other state, IoT disconnects all devices that used that certificate to connect. Devices cannot use a certificate that is not in the ACTIVE state to reconnect. |

### certificate-providers
| Method | Path | Description |
|--------|------|-------------|
| POST | /certificate-providers/{certificateProviderName} | Creates an Amazon Web Services IoT Core certificate provider. You can use Amazon Web Services IoT Core certificate provider to customize how to sign a certificate signing request (CSR) in IoT fleet provisioning. For more information, see Customizing certificate signing using Amazon Web Services IoT Core certificate provider from Amazon Web Services IoT Core Developer Guide. Requires permission to access the CreateCertificateProvider action.  After you create a certificate provider, the behavior of  CreateCertificateFromCsr API for fleet provisioning will change and all API calls to CreateCertificateFromCsr will invoke the certificate provider to create the certificates. It can take up to a few minutes for this behavior to change after a certificate provider is created. |
| DELETE | /certificate-providers/{certificateProviderName} | Deletes a certificate provider. Requires permission to access the DeleteCertificateProvider action.  If you delete the certificate provider resource, the behavior of CreateCertificateFromCsr will resume, and IoT will create certificates signed by IoT from a certificate signing request (CSR). |
| GET | /certificate-providers/{certificateProviderName} | Describes a certificate provider. Requires permission to access the DescribeCertificateProvider action. |
| GET | /certificate-providers/ | Lists all your certificate providers in your Amazon Web Services account. Requires permission to access the ListCertificateProviders action. |
| PUT | /certificate-providers/{certificateProviderName} | Updates a certificate provider. Requires permission to access the UpdateCertificateProvider action. |

### custom-metric
| Method | Path | Description |
|--------|------|-------------|
| POST | /custom-metric/{metricName} | Use this API to define a Custom Metric published by your devices to Device Defender.  Requires permission to access the CreateCustomMetric action. |
| DELETE | /custom-metric/{metricName} | Deletes a Device Defender detect custom metric.  Requires permission to access the DeleteCustomMetric action.  Before you can delete a custom metric, you must first remove the custom metric from all security profiles it's a part of. The security profile associated with the custom metric can be found using the ListSecurityProfiles API with metricName set to your custom metric name. |
| GET | /custom-metric/{metricName} | Gets information about a Device Defender detect custom metric.  Requires permission to access the DescribeCustomMetric action. |
| PATCH | /custom-metric/{metricName} | Updates a Device Defender detect custom metric.  Requires permission to access the UpdateCustomMetric action. |

### dimensions
| Method | Path | Description |
|--------|------|-------------|
| POST | /dimensions/{name} | Create a dimension that you can use to limit the scope of a metric used in a security profile for IoT Device Defender. For example, using a TOPIC_FILTER dimension, you can narrow down the scope of the metric only to MQTT topics whose name match the pattern specified in the dimension. Requires permission to access the CreateDimension action. |
| DELETE | /dimensions/{name} | Removes the specified dimension from your Amazon Web Services accounts. Requires permission to access the DeleteDimension action. |
| GET | /dimensions/{name} | Provides details about a dimension that is defined in your Amazon Web Services accounts. Requires permission to access the DescribeDimension action. |
| GET | /dimensions | List the set of dimensions that are defined for your Amazon Web Services accounts. Requires permission to access the ListDimensions action. |
| PATCH | /dimensions/{name} | Updates the definition for a dimension. You cannot change the type of a dimension after it is created (you can delete it and recreate it). Requires permission to access the UpdateDimension action. |

### domainConfigurations
| Method | Path | Description |
|--------|------|-------------|
| POST | /domainConfigurations/{domainConfigurationName} | Creates a domain configuration. Requires permission to access the CreateDomainConfiguration action. |
| DELETE | /domainConfigurations/{domainConfigurationName} | Deletes the specified domain configuration. Requires permission to access the DeleteDomainConfiguration action. |
| GET | /domainConfigurations/{domainConfigurationName} | Gets summary information about a domain configuration. Requires permission to access the DescribeDomainConfiguration action. |
| GET | /domainConfigurations | Gets a list of domain configurations for the user. This list is sorted alphabetically by domain configuration name. Requires permission to access the ListDomainConfigurations action. |
| PUT | /domainConfigurations/{domainConfigurationName} | Updates values stored in the domain configuration. Domain configurations for default endpoints can't be updated. Requires permission to access the UpdateDomainConfiguration action. |

### dynamic-thing-groups
| Method | Path | Description |
|--------|------|-------------|
| POST | /dynamic-thing-groups/{thingGroupName} | Creates a dynamic thing group. Requires permission to access the CreateDynamicThingGroup action. |
| DELETE | /dynamic-thing-groups/{thingGroupName} | Deletes a dynamic thing group. Requires permission to access the DeleteDynamicThingGroup action. |
| PATCH | /dynamic-thing-groups/{thingGroupName} | Updates a dynamic thing group. Requires permission to access the UpdateDynamicThingGroup action. |

### fleet-metric
| Method | Path | Description |
|--------|------|-------------|
| PUT | /fleet-metric/{metricName} | Creates a fleet metric. Requires permission to access the CreateFleetMetric action. |
| DELETE | /fleet-metric/{metricName} | Deletes the specified fleet metric. Returns successfully with no error if the deletion is successful or you specify a fleet metric that doesn't exist. Requires permission to access the DeleteFleetMetric action. |
| GET | /fleet-metric/{metricName} | Gets information about the specified fleet metric. Requires permission to access the DescribeFleetMetric action. |
| PATCH | /fleet-metric/{metricName} | Updates the data for a fleet metric. Requires permission to access the UpdateFleetMetric action. |

### job-templates
| Method | Path | Description |
|--------|------|-------------|
| PUT | /job-templates/{jobTemplateId} | Creates a job template. Requires permission to access the CreateJobTemplate action. |
| DELETE | /job-templates/{jobTemplateId} | Deletes the specified job template. |
| GET | /job-templates/{jobTemplateId} | Returns information about a job template. |
| GET | /job-templates | Returns a list of job templates. Requires permission to access the ListJobTemplates action. |

### keys-and-certificate
| Method | Path | Description |
|--------|------|-------------|
| POST | /keys-and-certificate | Creates a 2048-bit RSA key pair and issues an X.509 certificate using the issued public key. You can also call CreateKeysAndCertificate over MQTT from a device, for more information, see Provisioning MQTT API.  Note This is the only time IoT issues the private key for this certificate, so it is important to keep it in a secure location. Requires permission to access the CreateKeysAndCertificate action. |

### mitigationactions
| Method | Path | Description |
|--------|------|-------------|
| POST | /mitigationactions/actions/{actionName} | Defines an action that can be applied to audit findings by using StartAuditMitigationActionsTask. Only certain types of mitigation actions can be applied to specific check names. For more information, see Mitigation actions. Each mitigation action can apply only one type of change. Requires permission to access the CreateMitigationAction action. |
| DELETE | /mitigationactions/actions/{actionName} | Deletes a defined mitigation action from your Amazon Web Services accounts. Requires permission to access the DeleteMitigationAction action. |
| GET | /mitigationactions/actions/{actionName} | Gets information about a mitigation action. Requires permission to access the DescribeMitigationAction action. |
| GET | /mitigationactions/actions | Gets a list of all mitigation actions that match the specified filter criteria. Requires permission to access the ListMitigationActions action. |
| PATCH | /mitigationactions/actions/{actionName} | Updates the definition for the specified mitigation action. Requires permission to access the UpdateMitigationAction action. |

### otaUpdates
| Method | Path | Description |
|--------|------|-------------|
| POST | /otaUpdates/{otaUpdateId} | Creates an IoT OTA update on a target group of things or groups. Requires permission to access the CreateOTAUpdate action. |
| DELETE | /otaUpdates/{otaUpdateId} | Delete an OTA update. Requires permission to access the DeleteOTAUpdate action. |
| GET | /otaUpdates/{otaUpdateId} | Gets an OTA update. Requires permission to access the GetOTAUpdate action. |
| GET | /otaUpdates | Lists OTA updates. Requires permission to access the ListOTAUpdates action. |

### packages
| Method | Path | Description |
|--------|------|-------------|
| PUT | /packages/{packageName} | Creates an IoT software package that can be deployed to your fleet. Requires permission to access the CreatePackage and GetIndexingConfiguration actions. |
| PUT | /packages/{packageName}/versions/{versionName} | Creates a new version for an existing IoT software package. Requires permission to access the CreatePackageVersion and GetIndexingConfiguration actions. |
| DELETE | /packages/{packageName} | Deletes a specific version from a software package.  Note: All package versions must be deleted before deleting the software package. Requires permission to access the DeletePackageVersion action. |
| DELETE | /packages/{packageName}/versions/{versionName} | Deletes a specific version from a software package.  Note: If a package version is designated as default, you must remove the designation from the software package using the UpdatePackage action. |
| GET | /packages/{packageName} | Gets information about the specified software package. Requires permission to access the GetPackage action. |
| GET | /packages/{packageName}/versions/{versionName} | Gets information about the specified package version.  Requires permission to access the GetPackageVersion action. |
| GET | /packages/{packageName}/versions | Lists the software package versions associated to the account. Requires permission to access the ListPackageVersions action. |
| GET | /packages | Lists the software packages associated to the account. Requires permission to access the ListPackages action. |
| PATCH | /packages/{packageName} | Updates the supported fields for a specific software package. Requires permission to access the UpdatePackage and GetIndexingConfiguration actions. |
| PATCH | /packages/{packageName}/versions/{versionName} | Updates the supported fields for a specific package version. Requires permission to access the UpdatePackageVersion and GetIndexingConfiguration actions. |

### policies
| Method | Path | Description |
|--------|------|-------------|
| POST | /policies/{policyName} | Creates an IoT policy. The created policy is the default version for the policy. This operation creates a policy version with a version identifier of 1 and sets 1 as the policy's default version. Requires permission to access the CreatePolicy action. |
| POST | /policies/{policyName}/version | Creates a new version of the specified IoT policy. To update a policy, create a new policy version. A managed policy can have up to five versions. If the policy has five versions, you must use DeletePolicyVersion to delete an existing version before you create a new one. Optionally, you can set the new version as the policy's default version. The default version is the operative version (that is, the version that is in effect for the certificates to which the policy is attached). Requires permission to access the CreatePolicyVersion action. |
| DELETE | /policies/{policyName} | Deletes the specified policy. A policy cannot be deleted if it has non-default versions or it is attached to any certificate. To delete a policy, use the DeletePolicyVersion action to delete all non-default versions of the policy; use the DetachPolicy action to detach the policy from any certificate; and then use the DeletePolicy action to delete the policy. When a policy is deleted using DeletePolicy, its default version is deleted with it.  Because of the distributed nature of Amazon Web Services, it can take up to five minutes after a policy is detached before it's ready to be deleted.  Requires permission to access the DeletePolicy action. |
| DELETE | /policies/{policyName}/version/{policyVersionId} | Deletes the specified version of the specified policy. You cannot delete the default version of a policy using this action. To delete the default version of a policy, use DeletePolicy. To find out which version of a policy is marked as the default version, use ListPolicyVersions. Requires permission to access the DeletePolicyVersion action. |
| GET | /policies/{policyName} | Gets information about the specified policy with the policy document of the default version. Requires permission to access the GetPolicy action. |
| GET | /policies/{policyName}/version/{policyVersionId} | Gets information about the specified policy version. Requires permission to access the GetPolicyVersion action. |
| GET | /policies | Lists your policies. Requires permission to access the ListPolicies action. |
| GET | /policies/{policyName}/version | Lists the versions of the specified policy and identifies the default version. Requires permission to access the ListPolicyVersions action. |
| PATCH | /policies/{policyName}/version/{policyVersionId} | Sets the specified version of the specified policy as the policy's default (operative) version. This action affects all certificates to which the policy is attached. To list the principals the policy is attached to, use the ListPrincipalPolicies action. Requires permission to access the SetDefaultPolicyVersion action. |

### provisioning-templates
| Method | Path | Description |
|--------|------|-------------|
| POST | /provisioning-templates/{templateName}/provisioning-claim | Creates a provisioning claim. Requires permission to access the CreateProvisioningClaim action. |
| POST | /provisioning-templates | Creates a provisioning template. Requires permission to access the CreateProvisioningTemplate action. |
| POST | /provisioning-templates/{templateName}/versions | Creates a new version of a provisioning template. Requires permission to access the CreateProvisioningTemplateVersion action. |
| DELETE | /provisioning-templates/{templateName} | Deletes a provisioning template. Requires permission to access the DeleteProvisioningTemplate action. |
| DELETE | /provisioning-templates/{templateName}/versions/{versionId} | Deletes a provisioning template version. Requires permission to access the DeleteProvisioningTemplateVersion action. |
| GET | /provisioning-templates/{templateName} | Returns information about a provisioning template. Requires permission to access the DescribeProvisioningTemplate action. |
| GET | /provisioning-templates/{templateName}/versions/{versionId} | Returns information about a provisioning template version. Requires permission to access the DescribeProvisioningTemplateVersion action. |
| GET | /provisioning-templates/{templateName}/versions | A list of provisioning template versions. Requires permission to access the ListProvisioningTemplateVersions action. |
| GET | /provisioning-templates | Lists the provisioning templates in your Amazon Web Services account. Requires permission to access the ListProvisioningTemplates action. |
| PATCH | /provisioning-templates/{templateName} | Updates a provisioning template. Requires permission to access the UpdateProvisioningTemplate action. |

### role-aliases
| Method | Path | Description |
|--------|------|-------------|
| POST | /role-aliases/{roleAlias} | Creates a role alias. Requires permission to access the CreateRoleAlias action. |
| DELETE | /role-aliases/{roleAlias} | Deletes a role alias Requires permission to access the DeleteRoleAlias action. |
| GET | /role-aliases/{roleAlias} | Describes a role alias. Requires permission to access the DescribeRoleAlias action. |
| GET | /role-aliases | Lists the role aliases registered in your account. Requires permission to access the ListRoleAliases action. |
| PUT | /role-aliases/{roleAlias} | Updates a role alias. Requires permission to access the UpdateRoleAlias action. |

### streams
| Method | Path | Description |
|--------|------|-------------|
| POST | /streams/{streamId} | Creates a stream for delivering one or more large files in chunks over MQTT. A stream transports data bytes in chunks or blocks packaged as MQTT messages from a source like S3. You can have one or more files associated with a stream. Requires permission to access the CreateStream action. |
| DELETE | /streams/{streamId} | Deletes a stream. Requires permission to access the DeleteStream action. |
| GET | /streams/{streamId} | Gets information about a stream. Requires permission to access the DescribeStream action. |
| GET | /streams | Lists all of the streams in your Amazon Web Services account. Requires permission to access the ListStreams action. |
| PUT | /streams/{streamId} | Updates an existing stream. The stream version will be incremented by one. Requires permission to access the UpdateStream action. |

### thing-types
| Method | Path | Description |
|--------|------|-------------|
| POST | /thing-types/{thingTypeName} | Creates a new thing type. Requires permission to access the CreateThingType action. |
| DELETE | /thing-types/{thingTypeName} | Deletes the specified thing type. You cannot delete a thing type if it has things associated with it. To delete a thing type, first mark it as deprecated by calling DeprecateThingType, then remove any associated things by calling UpdateThing to change the thing type on any associated thing, and finally use DeleteThingType to delete the thing type. Requires permission to access the DeleteThingType action. |
| POST | /thing-types/{thingTypeName}/deprecate | Deprecates a thing type. You can not associate new things with deprecated thing type. Requires permission to access the DeprecateThingType action. |
| GET | /thing-types/{thingTypeName} | Gets information about the specified thing type. Requires permission to access the DescribeThingType action. |
| GET | /thing-types | Lists the existing thing types. Requires permission to access the ListThingTypes action. |

### rules
| Method | Path | Description |
|--------|------|-------------|
| POST | /rules/{ruleName} | Creates a rule. Creating rules is an administrator-level action. Any user who has permission to create rules will be able to access data processed by the rule. Requires permission to access the CreateTopicRule action. |
| DELETE | /rules/{ruleName} | Deletes the rule. Requires permission to access the DeleteTopicRule action. |
| POST | /rules/{ruleName}/disable | Disables the rule. Requires permission to access the DisableTopicRule action. |
| POST | /rules/{ruleName}/enable | Enables the rule. Requires permission to access the EnableTopicRule action. |
| GET | /rules/{ruleName} | Gets information about the rule. Requires permission to access the GetTopicRule action. |
| GET | /rules | Lists the rules for the specific topic. Requires permission to access the ListTopicRules action. |
| PATCH | /rules/{ruleName} | Replaces the rule. You must specify all parameters for the new rule. Creating rules is an administrator-level action. Any user who has permission to create rules will be able to access data processed by the rule. Requires permission to access the ReplaceTopicRule action. |

### destinations
| Method | Path | Description |
|--------|------|-------------|
| POST | /destinations | Creates a topic rule destination. The destination must be confirmed prior to use. Requires permission to access the CreateTopicRuleDestination action. |
| DELETE | /destinations/{arn+} | Deletes a topic rule destination. Requires permission to access the DeleteTopicRuleDestination action. |
| GET | /destinations/{arn+} | Gets information about a topic rule destination. Requires permission to access the GetTopicRuleDestination action. |
| GET | /destinations | Lists all the topic rule destinations in your Amazon Web Services account. Requires permission to access the ListTopicRuleDestinations action. |
| PATCH | /destinations | Updates a topic rule destination. You use this to change the status, endpoint URL, or confirmation URL of the destination. Requires permission to access the UpdateTopicRuleDestination action. |

### cacertificate
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /cacertificate/{caCertificateId} | Deletes a registered CA certificate. Requires permission to access the DeleteCACertificate action. |
| GET | /cacertificate/{caCertificateId} | Describes a registered CA certificate. Requires permission to access the DescribeCACertificate action. |
| POST | /cacertificate | Registers a CA certificate with Amazon Web Services IoT Core. There is no limit to the number of CA certificates you can register in your Amazon Web Services account. You can register up to 10 CA certificates with the same CA subject field per Amazon Web Services account. Requires permission to access the RegisterCACertificate action. |
| PUT | /cacertificate/{caCertificateId} | Updates a registered CA certificate. Requires permission to access the UpdateCACertificate action. |

### registrationcode
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /registrationcode | Deletes a CA certificate registration code. Requires permission to access the DeleteRegistrationCode action. |
| GET | /registrationcode | Gets a registration code used to register a CA certificate with IoT. IoT will create a registration code as part of this API call if the registration code doesn't exist or has been deleted. If you already have a registration code, this API call will return the same registration code. Requires permission to access the GetRegistrationCode action. |

### v2LoggingLevel
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /v2LoggingLevel | Deletes a logging level. Requires permission to access the DeleteV2LoggingLevel action. |
| GET | /v2LoggingLevel | Lists logging levels. Requires permission to access the ListV2LoggingLevels action. |
| POST | /v2LoggingLevel | Sets the logging level. Requires permission to access the SetV2LoggingLevel action. |

### endpoint
| Method | Path | Description |
|--------|------|-------------|
| GET | /endpoint | Returns or creates a unique endpoint specific to the Amazon Web Services account making the call.  The first time DescribeEndpoint is called, an endpoint is created. All subsequent calls to DescribeEndpoint return the same endpoint.  Requires permission to access the DescribeEndpoint action. |

### event-configurations
| Method | Path | Description |
|--------|------|-------------|
| GET | /event-configurations | Describes event configurations. Requires permission to access the DescribeEventConfigurations action. |
| PATCH | /event-configurations | Updates the event configurations. Requires permission to access the UpdateEventConfigurations action. |

### indices
| Method | Path | Description |
|--------|------|-------------|
| GET | /indices/{indexName} | Describes a search index. Requires permission to access the DescribeIndex action. |
| POST | /indices/buckets | Aggregates on indexed data with search queries pertaining to particular fields.  Requires permission to access the GetBucketsAggregation action. |
| POST | /indices/cardinality | Returns the approximate count of unique values that match the query. Requires permission to access the GetCardinality action. |
| POST | /indices/percentiles | Groups the aggregated values that match the query into percentile groupings. The default percentile groupings are: 1,5,25,50,75,95,99, although you can specify your own when you call GetPercentiles. This function returns a value for each percentile group specified (or the default percentile groupings). The percentile group "1" contains the aggregated field value that occurs in approximately one percent of the values that match the query. The percentile group "5" contains the aggregated field value that occurs in approximately five percent of the values that match the query, and so on. The result is an approximation, the more values that match the query, the more accurate the percentile values. Requires permission to access the GetPercentiles action. |
| POST | /indices/statistics | Returns the count, average, sum, minimum, maximum, sum of squares, variance, and standard deviation for the specified aggregated field. If the aggregation field is of type String, only the count statistic is returned. Requires permission to access the GetStatistics action. |
| GET | /indices | Lists the search indices. Requires permission to access the ListIndices action. |
| POST | /indices/search | The query search index. Requires permission to access the SearchIndex action. |

### managed-job-templates
| Method | Path | Description |
|--------|------|-------------|
| GET | /managed-job-templates/{templateName} | View details of a managed job template. |
| GET | /managed-job-templates | Returns a list of managed job templates. |

### thing-registration-tasks
| Method | Path | Description |
|--------|------|-------------|
| GET | /thing-registration-tasks/{taskId} | Describes a bulk thing provisioning task. Requires permission to access the DescribeThingRegistrationTask action. |
| GET | /thing-registration-tasks/{taskId}/reports | Information about the thing registration tasks. |
| GET | /thing-registration-tasks | List bulk thing provisioning tasks. Requires permission to access the ListThingRegistrationTasks action. |
| POST | /thing-registration-tasks | Creates a bulk thing provisioning task. Requires permission to access the StartThingRegistrationTask action. |
| PUT | /thing-registration-tasks/{taskId}/cancel | Cancels a bulk thing provisioning task. Requires permission to access the StopThingRegistrationTask action. |

### behavior-model-training
| Method | Path | Description |
|--------|------|-------------|
| GET | /behavior-model-training/summaries | Returns a Device Defender's ML Detect Security Profile training model's status.  Requires permission to access the GetBehaviorModelTrainingSummaries action. |

### effective-policies
| Method | Path | Description |
|--------|------|-------------|
| POST | /effective-policies | Gets a list of the policies that have an effect on the authorization behavior of the specified device when it connects to the IoT device gateway. Requires permission to access the GetEffectivePolicies action. |

### indexing
| Method | Path | Description |
|--------|------|-------------|
| GET | /indexing/config | Gets the indexing configuration. Requires permission to access the GetIndexingConfiguration action. |
| POST | /indexing/config | Updates the search configuration. Requires permission to access the UpdateIndexingConfiguration action. |

### loggingOptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /loggingOptions | Gets the logging options. NOTE: use of this command is not recommended. Use GetV2LoggingOptions instead. Requires permission to access the GetLoggingOptions action. |
| POST | /loggingOptions | Sets the logging options. NOTE: use of this command is not recommended. Use SetV2LoggingOptions instead. Requires permission to access the SetLoggingOptions action. |

### package-configuration
| Method | Path | Description |
|--------|------|-------------|
| GET | /package-configuration | Gets information about the specified software package's configuration. Requires permission to access the GetPackageConfiguration action. |
| PATCH | /package-configuration | Updates the software package configuration. Requires permission to access the UpdatePackageConfiguration and iam:PassRole actions. |

### v2LoggingOptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2LoggingOptions | Gets the fine grained logging options. Requires permission to access the GetV2LoggingOptions action. |
| POST | /v2LoggingOptions | Sets the logging options for the V2 logging service. Requires permission to access the SetV2LoggingOptions action. |

### active-violations
| Method | Path | Description |
|--------|------|-------------|
| GET | /active-violations | Lists the active violations for a given Device Defender security profile. Requires permission to access the ListActiveViolations action. |

### attached-policies
| Method | Path | Description |
|--------|------|-------------|
| POST | /attached-policies/{target} | Lists the policies attached to the specified thing group. Requires permission to access the ListAttachedPolicies action. |

### authorizers
| Method | Path | Description |
|--------|------|-------------|
| GET | /authorizers/ | Lists the authorizers registered in your account. Requires permission to access the ListAuthorizers action. |

### cacertificates
| Method | Path | Description |
|--------|------|-------------|
| GET | /cacertificates | Lists the CA certificates registered for your Amazon Web Services account. The results are paginated with a default page size of 25. You can use the returned marker to retrieve additional results. Requires permission to access the ListCACertificates action. |

### certificates-by-ca
| Method | Path | Description |
|--------|------|-------------|
| GET | /certificates-by-ca/{caCertificateId} | List the device certificates signed by the specified CA certificate. Requires permission to access the ListCertificatesByCA action. |

### custom-metrics
| Method | Path | Description |
|--------|------|-------------|
| GET | /custom-metrics | Lists your Device Defender detect custom metrics.  Requires permission to access the ListCustomMetrics action. |

### fleet-metrics
| Method | Path | Description |
|--------|------|-------------|
| GET | /fleet-metrics | Lists all your fleet metrics.  Requires permission to access the ListFleetMetrics action. |

### metric-values
| Method | Path | Description |
|--------|------|-------------|
| GET | /metric-values | Lists the values reported for an IoT Device Defender metric (device-side metric, cloud-side metric, or custom metric) by the given thing during the specified time period. |

### certificates-out-going
| Method | Path | Description |
|--------|------|-------------|
| GET | /certificates-out-going | Lists certificates that are being transferred but not yet accepted. Requires permission to access the ListOutgoingCertificates action. |

### policy-principals
| Method | Path | Description |
|--------|------|-------------|
| GET | /policy-principals | Lists the principals associated with the specified policy.  Note: This action is deprecated and works as expected for backward compatibility, but we won't add enhancements. Use ListTargetsForPolicy instead. Requires permission to access the ListPolicyPrincipals action. |

### principals
| Method | Path | Description |
|--------|------|-------------|
| GET | /principals/things | Lists the things associated with the specified principal. A principal can be X.509 certificates, IAM users, groups, and roles, Amazon Cognito identities or federated identities.  Requires permission to access the ListPrincipalThings action. |

### security-profiles-for-target
| Method | Path | Description |
|--------|------|-------------|
| GET | /security-profiles-for-target | Lists the Device Defender security profiles attached to a target (thing group). Requires permission to access the ListSecurityProfilesForTarget action. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags | Lists the tags (metadata) you have assigned to the resource. Requires permission to access the ListTagsForResource action. |
| POST | /tags | Adds to or modifies the tags of the given resource. Tags are metadata which can be used to manage a resource. Requires permission to access the TagResource action. |

### policy-targets
| Method | Path | Description |
|--------|------|-------------|
| POST | /policy-targets/{policyName} | List targets for the specified policy. Requires permission to access the ListTargetsForPolicy action. |

### violation-events
| Method | Path | Description |
|--------|------|-------------|
| GET | /violation-events | Lists the Device Defender security profile violations discovered during the given time period. You can use filters to limit the results to those alerts issued for a particular security profile, behavior, or thing (device). Requires permission to access the ListViolationEvents action. |

### violations
| Method | Path | Description |
|--------|------|-------------|
| POST | /violations/verification-state/{violationId} | Set a verification state and provide a description of that verification state on a violation (detect alarm). |

### certificate
| Method | Path | Description |
|--------|------|-------------|
| POST | /certificate/register | Registers a device certificate with IoT in the same certificate mode as the signing CA. If you have more than one CA certificate that has the same subject field, you must specify the CA certificate that was used to sign the device certificate being registered. Requires permission to access the RegisterCertificate action. |
| POST | /certificate/register-no-ca | Register a certificate that does not have a certificate authority (CA). For supported certificates, consult  Certificate signing algorithms supported by IoT. |

### reject-certificate-transfer
| Method | Path | Description |
|--------|------|-------------|
| PATCH | /reject-certificate-transfer/{certificateId} | Rejects a pending certificate transfer. After IoT rejects a certificate transfer, the certificate status changes from PENDING_TRANSFER to INACTIVE. To check for pending certificate transfers, call ListCertificates to enumerate your certificates. This operation can only be called by the transfer destination. After it is called, the certificate will be returned to the source's account in the INACTIVE state. Requires permission to access the RejectCertificateTransfer action. |

### test-authorization
| Method | Path | Description |
|--------|------|-------------|
| POST | /test-authorization | Tests if a specified principal is authorized to perform an IoT action on a specified resource. Use this to test and debug the authorization behavior of devices that connect to the IoT device gateway. Requires permission to access the TestAuthorization action. |

### transfer-certificate
| Method | Path | Description |
|--------|------|-------------|
| PATCH | /transfer-certificate/{certificateId} | Transfers the specified certificate to the specified Amazon Web Services account. Requires permission to access the TransferCertificate action. You can cancel the transfer until it is acknowledged by the recipient. No notification is sent to the transfer destination's account. It is up to the caller to notify the transfer target. The certificate being transferred must not be in the ACTIVE state. You can use the UpdateCertificate action to deactivate it. The certificate must not have any policies attached to it. You can use the DetachPolicy action to detach them. |

### untag
| Method | Path | Description |
|--------|------|-------------|
| POST | /untag | Removes the given tags (metadata) from the resource. Requires permission to access the UntagResource action. |

### security-profile-behaviors
| Method | Path | Description |
|--------|------|-------------|
| POST | /security-profile-behaviors/validate | Validates a Device Defender security profile behaviors specification. Requires permission to access the ValidateSecurityProfileBehaviors action. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Partially update a accept-certificate-transfer?" -> PATCH /accept-certificate-transfer/{certificateId}
- "Create a target?" -> POST /jobs/{jobId}/targets
- "Update a target-policy?" -> PUT /target-policies/{policyName}
- "Update a principal-policy?" -> PUT /principal-policies/{policyName}
- "Partially update a cancel-certificate-transfer?" -> PATCH /cancel-certificate-transfer/{certificateId}
- "Get confirmdestination details?" -> GET /confirmdestination/{confirmationToken+}
- "Create a create?" -> POST /audit/suppressions/create
- "Create a certificate?" -> POST /certificates
- "Update a fleet-metric?" -> PUT /fleet-metric/{metricName}
- "Update a job?" -> PUT /jobs/{jobId}
- "Update a job-template?" -> PUT /job-templates/{jobTemplateId}
- "Create a keys-and-certificate?" -> POST /keys-and-certificate
- "Update a package?" -> PUT /packages/{packageName}
- "Update a version?" -> PUT /packages/{packageName}/versions/{versionName}
- "Create a version?" -> POST /policies/{policyName}/version
- "Create a provisioning-claim?" -> POST /provisioning-templates/{templateName}/provisioning-claim
- "Create a provisioning-template?" -> POST /provisioning-templates
- "Create a version?" -> POST /provisioning-templates/{templateName}/versions
- "Create a destination?" -> POST /destinations
- "Create a delete?" -> POST /audit/suppressions/delete
- "Delete a authorizer?" -> DELETE /authorizer/{authorizerName}
- "Delete a billing-group?" -> DELETE /billing-groups/{billingGroupName}
- "Delete a cacertificate?" -> DELETE /cacertificate/{caCertificateId}
- "Delete a certificate?" -> DELETE /certificates/{certificateId}
- "Delete a certificate-provider?" -> DELETE /certificate-providers/{certificateProviderName}
- "Delete a custom-metric?" -> DELETE /custom-metric/{metricName}
- "Delete a dimension?" -> DELETE /dimensions/{name}
- "Delete a domainConfiguration?" -> DELETE /domainConfigurations/{domainConfigurationName}
- "Delete a dynamic-thing-group?" -> DELETE /dynamic-thing-groups/{thingGroupName}
- "Delete a fleet-metric?" -> DELETE /fleet-metric/{metricName}
- "Delete a job?" -> DELETE /jobs/{jobId}
- "Delete a executionNumber?" -> DELETE /things/{thingName}/jobs/{jobId}/executionNumber/{executionNumber}
- "Delete a job-template?" -> DELETE /job-templates/{jobTemplateId}
- "Delete a action?" -> DELETE /mitigationactions/actions/{actionName}
- "Delete a otaUpdate?" -> DELETE /otaUpdates/{otaUpdateId}
- "Delete a package?" -> DELETE /packages/{packageName}
- "Delete a version?" -> DELETE /packages/{packageName}/versions/{versionName}
- "Delete a policy?" -> DELETE /policies/{policyName}
- "Delete a version?" -> DELETE /policies/{policyName}/version/{policyVersionId}
- "Delete a provisioning-template?" -> DELETE /provisioning-templates/{templateName}
- "Delete a version?" -> DELETE /provisioning-templates/{templateName}/versions/{versionId}
- "Delete a role-aliase?" -> DELETE /role-aliases/{roleAlias}
- "Delete a scheduledaudit?" -> DELETE /audit/scheduledaudits/{scheduledAuditName}
- "Delete a security-profile?" -> DELETE /security-profiles/{securityProfileName}
- "Delete a stream?" -> DELETE /streams/{streamId}
- "Delete a thing?" -> DELETE /things/{thingName}
- "Delete a thing-group?" -> DELETE /thing-groups/{thingGroupName}
- "Delete a thing-type?" -> DELETE /thing-types/{thingTypeName}
- "Delete a rule?" -> DELETE /rules/{ruleName}
- "Delete a destination?" -> DELETE /destinations/{arn+}
- "Create a deprecate?" -> POST /thing-types/{thingTypeName}/deprecate
- "List all configuration?" -> GET /audit/configuration
- "Get finding details?" -> GET /audit/findings/{findingId}
- "Get task details?" -> GET /audit/mitigationactions/tasks/{taskId}
- "Create a describe?" -> POST /audit/suppressions/describe
- "Get task details?" -> GET /audit/tasks/{taskId}
- "Get authorizer details?" -> GET /authorizer/{authorizerName}
- "Get billing-group details?" -> GET /billing-groups/{billingGroupName}
- "Get cacertificate details?" -> GET /cacertificate/{caCertificateId}
- "Get certificate details?" -> GET /certificates/{certificateId}
- "Get certificate-provider details?" -> GET /certificate-providers/{certificateProviderName}
- "Get custom-metric details?" -> GET /custom-metric/{metricName}
- "List all default-authorizer?" -> GET /default-authorizer
- "Get task details?" -> GET /detect/mitigationactions/tasks/{taskId}
- "Get dimension details?" -> GET /dimensions/{name}
- "Get domainConfiguration details?" -> GET /domainConfigurations/{domainConfigurationName}
- "List all endpoint?" -> GET /endpoint
- "List all event-configurations?" -> GET /event-configurations
- "Get fleet-metric details?" -> GET /fleet-metric/{metricName}
- "Get indice details?" -> GET /indices/{indexName}
- "Get job details?" -> GET /jobs/{jobId}
- "Get job details?" -> GET /things/{thingName}/jobs/{jobId}
- "Get job-template details?" -> GET /job-templates/{jobTemplateId}
- "Get managed-job-template details?" -> GET /managed-job-templates/{templateName}
- "Get action details?" -> GET /mitigationactions/actions/{actionName}
- "Get provisioning-template details?" -> GET /provisioning-templates/{templateName}
- "Get version details?" -> GET /provisioning-templates/{templateName}/versions/{versionId}
- "Get role-aliase details?" -> GET /role-aliases/{roleAlias}
- "Get scheduledaudit details?" -> GET /audit/scheduledaudits/{scheduledAuditName}
- "Get security-profile details?" -> GET /security-profiles/{securityProfileName}
- "Get stream details?" -> GET /streams/{streamId}
- "Get thing details?" -> GET /things/{thingName}
- "Get thing-group details?" -> GET /thing-groups/{thingGroupName}
- "Get thing-registration-task details?" -> GET /thing-registration-tasks/{taskId}
- "Get thing-type details?" -> GET /thing-types/{thingTypeName}
- "Delete a principal-policy?" -> DELETE /principal-policies/{policyName}
- "Create a disable?" -> POST /rules/{ruleName}/disable
- "Create a enable?" -> POST /rules/{ruleName}/enable
- "List all summaries?" -> GET /behavior-model-training/summaries
- "Create a bucket?" -> POST /indices/buckets
- "Create a cardinality?" -> POST /indices/cardinality
- "Create a effective-policy?" -> POST /effective-policies
- "List all config?" -> GET /indexing/config
- "List all job-document?" -> GET /jobs/{jobId}/job-document
- "List all loggingOptions?" -> GET /loggingOptions
- "Get otaUpdate details?" -> GET /otaUpdates/{otaUpdateId}
- "Get package details?" -> GET /packages/{packageName}
- "List all package-configuration?" -> GET /package-configuration
- "Get version details?" -> GET /packages/{packageName}/versions/{versionName}
- "Create a percentile?" -> POST /indices/percentiles
- "Get policy details?" -> GET /policies/{policyName}
- "Get version details?" -> GET /policies/{policyName}/version/{policyVersionId}
- "List all registrationcode?" -> GET /registrationcode
- "Create a statistic?" -> POST /indices/statistics
- "Get rule details?" -> GET /rules/{ruleName}
- "Get destination details?" -> GET /destinations/{arn+}
- "List all v2LoggingOptions?" -> GET /v2LoggingOptions
- "List all active-violations?" -> GET /active-violations
- "Create a finding?" -> POST /audit/findings
- "List all executions?" -> GET /audit/mitigationactions/executions
- "List all tasks?" -> GET /audit/mitigationactions/tasks
- "Create a list?" -> POST /audit/suppressions/list
- "List all tasks?" -> GET /audit/tasks
- "List all authorizers?" -> GET /authorizers/
- "List all billing-groups?" -> GET /billing-groups
- "List all cacertificates?" -> GET /cacertificates
- "List all certificate-providers?" -> GET /certificate-providers/
- "List all certificates?" -> GET /certificates
- "Get certificates-by-ca details?" -> GET /certificates-by-ca/{caCertificateId}
- "List all custom-metrics?" -> GET /custom-metrics
- "List all executions?" -> GET /detect/mitigationactions/executions
- "List all tasks?" -> GET /detect/mitigationactions/tasks
- "List all dimensions?" -> GET /dimensions
- "List all domainConfigurations?" -> GET /domainConfigurations
- "List all fleet-metrics?" -> GET /fleet-metrics
- "List all indices?" -> GET /indices
- "List all things?" -> GET /jobs/{jobId}/things
- "List all jobs?" -> GET /things/{thingName}/jobs
- "List all job-templates?" -> GET /job-templates
- "List all jobs?" -> GET /jobs
- "List all managed-job-templates?" -> GET /managed-job-templates
- "List all metric-values?" -> GET /metric-values
- "List all actions?" -> GET /mitigationactions/actions
- "List all otaUpdates?" -> GET /otaUpdates
- "List all certificates-out-going?" -> GET /certificates-out-going
- "List all versions?" -> GET /packages/{packageName}/versions
- "List all packages?" -> GET /packages
- "List all policies?" -> GET /policies
- "List all policy-principals?" -> GET /policy-principals
- "List all version?" -> GET /policies/{policyName}/version
- "List all principal-policies?" -> GET /principal-policies
- "List all things?" -> GET /principals/things
- "List all versions?" -> GET /provisioning-templates/{templateName}/versions
- "List all provisioning-templates?" -> GET /provisioning-templates
- "List all relatedResources?" -> GET /audit/relatedResources
- "List all role-aliases?" -> GET /role-aliases
- "List all scheduledaudits?" -> GET /audit/scheduledaudits
- "List all security-profiles?" -> GET /security-profiles
- "List all security-profiles-for-target?" -> GET /security-profiles-for-target
- "List all streams?" -> GET /streams
- "List all tags?" -> GET /tags
- "List all targets?" -> GET /security-profiles/{securityProfileName}/targets
- "List all thing-groups?" -> GET /thing-groups
- "List all thing-groups?" -> GET /things/{thingName}/thing-groups
- "List all principals?" -> GET /things/{thingName}/principals
- "List all reports?" -> GET /thing-registration-tasks/{taskId}/reports
- "List all thing-registration-tasks?" -> GET /thing-registration-tasks
- "List all thing-types?" -> GET /thing-types
- "List all things?" -> GET /things
- "List all things?" -> GET /billing-groups/{billingGroupName}/things
- "List all things?" -> GET /thing-groups/{thingGroupName}/things
- "List all destinations?" -> GET /destinations
- "List all rules?" -> GET /rules
- "List all v2LoggingLevel?" -> GET /v2LoggingLevel
- "List all violation-events?" -> GET /violation-events
- "Create a cacertificate?" -> POST /cacertificate
- "Create a register?" -> POST /certificate/register
- "Create a register-no-ca?" -> POST /certificate/register-no-ca
- "Create a thing?" -> POST /things
- "Partially update a reject-certificate-transfer?" -> PATCH /reject-certificate-transfer/{certificateId}
- "Partially update a rule?" -> PATCH /rules/{ruleName}
- "Create a search?" -> POST /indices/search
- "Create a default-authorizer?" -> POST /default-authorizer
- "Partially update a version?" -> PATCH /policies/{policyName}/version/{policyVersionId}
- "Create a loggingOption?" -> POST /loggingOptions
- "Create a v2LoggingLevel?" -> POST /v2LoggingLevel
- "Create a v2LoggingOption?" -> POST /v2LoggingOptions
- "Update a task?" -> PUT /detect/mitigationactions/tasks/{taskId}
- "Create a task?" -> POST /audit/tasks
- "Create a thing-registration-task?" -> POST /thing-registration-tasks
- "Create a tag?" -> POST /tags
- "Create a test-authorization?" -> POST /test-authorization
- "Create a test?" -> POST /authorizer/{authorizerName}/test
- "Partially update a transfer-certificate?" -> PATCH /transfer-certificate/{certificateId}
- "Create a untag?" -> POST /untag
- "Update a authorizer?" -> PUT /authorizer/{authorizerName}
- "Partially update a billing-group?" -> PATCH /billing-groups/{billingGroupName}
- "Update a cacertificate?" -> PUT /cacertificate/{caCertificateId}
- "Update a certificate?" -> PUT /certificates/{certificateId}
- "Update a certificate-provider?" -> PUT /certificate-providers/{certificateProviderName}
- "Partially update a custom-metric?" -> PATCH /custom-metric/{metricName}
- "Partially update a dimension?" -> PATCH /dimensions/{name}
- "Update a domainConfiguration?" -> PUT /domainConfigurations/{domainConfigurationName}
- "Partially update a dynamic-thing-group?" -> PATCH /dynamic-thing-groups/{thingGroupName}
- "Partially update a fleet-metric?" -> PATCH /fleet-metric/{metricName}
- "Create a config?" -> POST /indexing/config
- "Partially update a job?" -> PATCH /jobs/{jobId}
- "Partially update a action?" -> PATCH /mitigationactions/actions/{actionName}
- "Partially update a package?" -> PATCH /packages/{packageName}
- "Partially update a version?" -> PATCH /packages/{packageName}/versions/{versionName}
- "Partially update a provisioning-template?" -> PATCH /provisioning-templates/{templateName}
- "Update a role-aliase?" -> PUT /role-aliases/{roleAlias}
- "Partially update a scheduledaudit?" -> PATCH /audit/scheduledaudits/{scheduledAuditName}
- "Partially update a security-profile?" -> PATCH /security-profiles/{securityProfileName}
- "Update a stream?" -> PUT /streams/{streamId}
- "Partially update a thing?" -> PATCH /things/{thingName}
- "Partially update a thing-group?" -> PATCH /thing-groups/{thingGroupName}
- "Create a validate?" -> POST /security-profile-behaviors/validate
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
