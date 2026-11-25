---
name: aws-signer
description: "AWS Signer API skill. Use when working with AWS Signer for signing-profiles, signing-jobs, revocations. Covers 19 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS Signer
API version: 2017-08-25

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /revocations -- verify access
3. POST /signing-profiles/{profileName}/permissions -- create first permissions

## Endpoints

19 endpoints across 5 groups. See references/api-spec.lap for full details.

### signing-profiles
| Method | Path | Description |
|--------|------|-------------|
| POST | /signing-profiles/{profileName}/permissions | Adds cross-account permissions to a signing profile. |
| DELETE | /signing-profiles/{profileName} | Changes the state of an ACTIVE signing profile to CANCELED. A canceled profile is still viewable with the ListSigningProfiles operation, but it cannot perform new signing jobs, and is deleted two years after cancelation. |
| GET | /signing-profiles/{profileName} | Returns information on a specific signing profile. |
| GET | /signing-profiles/{profileName}/permissions | Lists the cross-account permissions associated with a signing profile. |
| GET | /signing-profiles | Lists all available signing profiles in your AWS account. Returns only profiles with an ACTIVE status unless the includeCanceled request field is set to true. If additional jobs remain to be listed, AWS Signer returns a nextToken value. Use this value in subsequent calls to ListSigningJobs to fetch the remaining values. You can continue calling ListSigningJobs with your maxResults parameter and with new values that Signer returns in the nextToken parameter until all of your signing jobs have been returned. |
| PUT | /signing-profiles/{profileName} | Creates a signing profile. A signing profile is a code-signing template that can be used to carry out a pre-defined signing job. |
| DELETE | /signing-profiles/{profileName}/permissions/{statementId} | Removes cross-account permissions from a signing profile. |
| PUT | /signing-profiles/{profileName}/revoke | Changes the state of a signing profile to REVOKED. This indicates that signatures generated using the signing profile after an effective start date are no longer valid. |

### signing-jobs
| Method | Path | Description |
|--------|------|-------------|
| GET | /signing-jobs/{jobId} | Returns information about a specific code signing job. You specify the job by using the jobId value that is returned by the StartSigningJob operation. |
| GET | /signing-jobs | Lists all your signing jobs. You can use the maxResults parameter to limit the number of signing jobs that are returned in the response. If additional jobs remain to be listed, AWS Signer returns a nextToken value. Use this value in subsequent calls to ListSigningJobs to fetch the remaining values. You can continue calling ListSigningJobs with your maxResults parameter and with new values that Signer returns in the nextToken parameter until all of your signing jobs have been returned. |
| PUT | /signing-jobs/{jobId}/revoke | Changes the state of a signing job to REVOKED. This indicates that the signature is no longer valid. |
| POST | /signing-jobs/with-payload | Signs a binary payload and returns a signature envelope. |
| POST | /signing-jobs | Initiates a signing job to be performed on the code provided. Signing jobs are viewable by the ListSigningJobs operation for two years after they are performed. Note the following requirements:     You must create an Amazon S3 source bucket. For more information, see Creating a Bucket in the Amazon S3 Getting Started Guide.    Your S3 source bucket must be version enabled.   You must create an S3 destination bucket. AWS Signer uses your S3 destination bucket to write your signed code.   You specify the name of the source and destination buckets when calling the StartSigningJob operation.   You must ensure the S3 buckets are from the same Region as the signing profile. Cross-Region signing isn't supported.   You must also specify a request token that identifies your request to Signer.   You can call the DescribeSigningJob and the ListSigningJobs actions after you call StartSigningJob. For a Java example that shows how to use this action, see StartSigningJob. |

### revocations
| Method | Path | Description |
|--------|------|-------------|
| GET | /revocations | Retrieves the revocation status of one or more of the signing profile, signing job, and signing certificate. |

### signing-platforms
| Method | Path | Description |
|--------|------|-------------|
| GET | /signing-platforms/{platformId} | Returns information on a specific signing platform. |
| GET | /signing-platforms | Lists all signing platforms available in AWS Signer that match the request parameters. If additional jobs remain to be listed, Signer returns a nextToken value. Use this value in subsequent calls to ListSigningJobs to fetch the remaining values. You can continue calling ListSigningJobs with your maxResults parameter and with new values that Signer returns in the nextToken parameter until all of your signing jobs have been returned. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags/{resourceArn} | Returns a list of the tags associated with a signing profile resource. |
| POST | /tags/{resourceArn} | Adds one or more tags to a signing profile. Tags are labels that you can use to identify and organize your AWS resources. Each tag consists of a key and an optional value. To specify the signing profile, use its Amazon Resource Name (ARN). To specify the tag, use a key-value pair. |
| DELETE | /tags/{resourceArn} | Removes one or more tags from a signing profile. To remove the tags, specify a list of tag keys. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a permission?" -> POST /signing-profiles/{profileName}/permissions
- "Delete a signing-profile?" -> DELETE /signing-profiles/{profileName}
- "Get signing-job details?" -> GET /signing-jobs/{jobId}
- "List all revocations?" -> GET /revocations
- "Get signing-platform details?" -> GET /signing-platforms/{platformId}
- "Get signing-profile details?" -> GET /signing-profiles/{profileName}
- "List all permissions?" -> GET /signing-profiles/{profileName}/permissions
- "List all signing-jobs?" -> GET /signing-jobs
- "List all signing-platforms?" -> GET /signing-platforms
- "List all signing-profiles?" -> GET /signing-profiles
- "Get tag details?" -> GET /tags/{resourceArn}
- "Update a signing-profile?" -> PUT /signing-profiles/{profileName}
- "Delete a permission?" -> DELETE /signing-profiles/{profileName}/permissions/{statementId}
- "Create a with-payload?" -> POST /signing-jobs/with-payload
- "Create a signing-job?" -> POST /signing-jobs
- "Delete a tag?" -> DELETE /tags/{resourceArn}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
