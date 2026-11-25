---
name: aws-importexport
description: "AWS Import/Export API skill. Use when working with AWS Import/Export for ?Operation=CancelJob, ?Operation=CreateJob, ?Operation=GetShippingLabel. Covers 6 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS Import/Export
API version: 2010-06-01

## Auth
No authentication required.

## Base URL
Not specified.

## Setup
1. No auth setup needed
3. POST /?Operation=CancelJob -- create first ?Operation=CancelJob

## Endpoints

6 endpoints across 6 groups. See references/api-spec.lap for full details.

### ?Operation=CancelJob
| Method | Path | Description |
|--------|------|-------------|
| POST | /?Operation=CancelJob | This operation cancels a specified job. Only the job owner can cancel it. The operation fails if the job has already started or is complete. |

### ?Operation=CreateJob
| Method | Path | Description |
|--------|------|-------------|
| POST | /?Operation=CreateJob | This operation initiates the process of scheduling an upload or download of your data. You include in the request a manifest that describes the data transfer specifics. The response to the request includes a job ID, which you can use in other operations, a signature that you use to identify your storage device, and the address where you should ship your storage device. |

### ?Operation=GetShippingLabel
| Method | Path | Description |
|--------|------|-------------|
| POST | /?Operation=GetShippingLabel | This operation generates a pre-paid UPS shipping label that you will use to ship your device to AWS for processing. |

### ?Operation=GetStatus
| Method | Path | Description |
|--------|------|-------------|
| POST | /?Operation=GetStatus | This operation returns information about a job, including where the job is in the processing pipeline, the status of the results, and the signature value associated with the job. You can only return information about jobs you own. |

### ?Operation=ListJobs
| Method | Path | Description |
|--------|------|-------------|
| POST | /?Operation=ListJobs | This operation returns the jobs associated with the requester. AWS Import/Export lists the jobs in reverse chronological order based on the date of creation. For example if Job Test1 was created 2009Dec30 and Test2 was created 2010Feb05, the ListJobs operation would return Test2 followed by Test1. |

### ?Operation=UpdateJob
| Method | Path | Description |
|--------|------|-------------|
| POST | /?Operation=UpdateJob | You use this operation to change the parameters specified in the original manifest file by supplying a new manifest file. The manifest file attached to this request replaces the original manifest file. You can only use the operation after a CreateJob request but before the data transfer starts and you can only use it on jobs you own. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a ?Operation=CancelJob?" -> POST /?Operation=CancelJob
- "Create a ?Operation=CreateJob?" -> POST /?Operation=CreateJob
- "Create a ?Operation=GetShippingLabel?" -> POST /?Operation=GetShippingLabel
- "Create a ?Operation=GetStatus?" -> POST /?Operation=GetStatus
- "Create a ?Operation=ListJob?" -> POST /?Operation=ListJobs
- "Create a ?Operation=UpdateJob?" -> POST /?Operation=UpdateJob

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object
- Error responses use types: BucketPermissionException, CanceledJobIdException, CreateJobQuotaExceededException, ExpiredJobIdException, InvalidAccessKeyIdException, InvalidAddressException, InvalidCustomsException, InvalidFileSystemException, InvalidJobIdException, InvalidManifestFieldException, InvalidParameterException, InvalidVersionException, MalformedManifestException, MissingCustomsException, MissingManifestFieldException, MissingParameterException, MultipleRegionsException, NoSuchBucketException, UnableToCancelJobIdException, UnableToUpdateJobIdException

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
