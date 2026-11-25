---
name: aws-elemental-mediaconvert
description: "AWS Elemental MediaConvert API skill. Use when working with AWS Elemental MediaConvert for 2017-08-29. Covers 29 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS Elemental MediaConvert
API version: 2017-08-29

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /2017-08-29/policy -- verify access
3. POST /2017-08-29/certificates -- create first certificates

## Endpoints

29 endpoints across 1 groups. See references/api-spec.lap for full details.

### 2017-08-29
| Method | Path | Description |
|--------|------|-------------|
| POST | /2017-08-29/certificates | Associates an AWS Certificate Manager (ACM) Amazon Resource Name (ARN) with AWS Elemental MediaConvert. |
| DELETE | /2017-08-29/jobs/{id} | Permanently cancel a job. Once you have canceled a job, you can't start it again. |
| POST | /2017-08-29/jobs | Create a new transcoding job. For information about jobs and job settings, see the User Guide at http://docs.aws.amazon.com/mediaconvert/latest/ug/what-is.html |
| POST | /2017-08-29/jobTemplates | Create a new job template. For information about job templates see the User Guide at http://docs.aws.amazon.com/mediaconvert/latest/ug/what-is.html |
| POST | /2017-08-29/presets | Create a new preset. For information about job templates see the User Guide at http://docs.aws.amazon.com/mediaconvert/latest/ug/what-is.html |
| POST | /2017-08-29/queues | Create a new transcoding queue. For information about queues, see Working With Queues in the User Guide at https://docs.aws.amazon.com/mediaconvert/latest/ug/working-with-queues.html |
| DELETE | /2017-08-29/jobTemplates/{name} | Permanently delete a job template you have created. |
| DELETE | /2017-08-29/policy | Permanently delete a policy that you created. |
| DELETE | /2017-08-29/presets/{name} | Permanently delete a preset you have created. |
| DELETE | /2017-08-29/queues/{name} | Permanently delete a queue you have created. |
| POST | /2017-08-29/endpoints | Send a request with an empty body to the regional API endpoint to get your account API endpoint. Note that DescribeEndpoints is no longer required. We recommend that you send your requests directly to the regional endpoint instead. |
| DELETE | /2017-08-29/certificates/{arn} | Removes an association between the Amazon Resource Name (ARN) of an AWS Certificate Manager (ACM) certificate and an AWS Elemental MediaConvert resource. |
| GET | /2017-08-29/jobs/{id} | Retrieve the JSON for a specific transcoding job. |
| GET | /2017-08-29/jobTemplates/{name} | Retrieve the JSON for a specific job template. |
| GET | /2017-08-29/policy | Retrieve the JSON for your policy. |
| GET | /2017-08-29/presets/{name} | Retrieve the JSON for a specific preset. |
| GET | /2017-08-29/queues/{name} | Retrieve the JSON for a specific queue. |
| GET | /2017-08-29/jobTemplates | Retrieve a JSON array of up to twenty of your job templates. This will return the templates themselves, not just a list of them. To retrieve the next twenty templates, use the nextToken string returned with the array |
| GET | /2017-08-29/jobs | Retrieve a JSON array of up to twenty of your most recently created jobs. This array includes in-process, completed, and errored jobs. This will return the jobs themselves, not just a list of the jobs. To retrieve the twenty next most recent jobs, use the nextToken string returned with the array. |
| GET | /2017-08-29/presets | Retrieve a JSON array of up to twenty of your presets. This will return the presets themselves, not just a list of them. To retrieve the next twenty presets, use the nextToken string returned with the array. |
| GET | /2017-08-29/queues | Retrieve a JSON array of up to twenty of your queues. This will return the queues themselves, not just a list of them. To retrieve the next twenty queues, use the nextToken string returned with the array. |
| GET | /2017-08-29/tags/{arn} | Retrieve the tags for a MediaConvert resource. |
| PUT | /2017-08-29/policy | Create or change your policy. For more information about policies, see the user guide at http://docs.aws.amazon.com/mediaconvert/latest/ug/what-is.html |
| GET | /2017-08-29/search | Retrieve a JSON array that includes job details for up to twenty of your most recent jobs. Optionally filter results further according to input file, queue, or status. To retrieve the twenty next most recent jobs, use the nextToken string returned with the array. |
| POST | /2017-08-29/tags | Add tags to a MediaConvert queue, preset, or job template. For information about tagging, see the User Guide at https://docs.aws.amazon.com/mediaconvert/latest/ug/tagging-resources.html |
| PUT | /2017-08-29/tags/{arn} | Remove tags from a MediaConvert queue, preset, or job template. For information about tagging, see the User Guide at https://docs.aws.amazon.com/mediaconvert/latest/ug/tagging-resources.html |
| PUT | /2017-08-29/jobTemplates/{name} | Modify one of your existing job templates. |
| PUT | /2017-08-29/presets/{name} | Modify one of your existing presets. |
| PUT | /2017-08-29/queues/{name} | Modify one of your existing queues. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a certificate?" -> POST /2017-08-29/certificates
- "Delete a job?" -> DELETE /2017-08-29/jobs/{id}
- "Create a job?" -> POST /2017-08-29/jobs
- "Create a jobTemplate?" -> POST /2017-08-29/jobTemplates
- "Create a preset?" -> POST /2017-08-29/presets
- "Create a queue?" -> POST /2017-08-29/queues
- "Delete a jobTemplate?" -> DELETE /2017-08-29/jobTemplates/{name}
- "Delete a preset?" -> DELETE /2017-08-29/presets/{name}
- "Delete a queue?" -> DELETE /2017-08-29/queues/{name}
- "Create a endpoint?" -> POST /2017-08-29/endpoints
- "Delete a certificate?" -> DELETE /2017-08-29/certificates/{arn}
- "Get job details?" -> GET /2017-08-29/jobs/{id}
- "Get jobTemplate details?" -> GET /2017-08-29/jobTemplates/{name}
- "List all policy?" -> GET /2017-08-29/policy
- "Get preset details?" -> GET /2017-08-29/presets/{name}
- "Get queue details?" -> GET /2017-08-29/queues/{name}
- "List all jobTemplates?" -> GET /2017-08-29/jobTemplates
- "List all jobs?" -> GET /2017-08-29/jobs
- "List all presets?" -> GET /2017-08-29/presets
- "List all queues?" -> GET /2017-08-29/queues
- "Get tag details?" -> GET /2017-08-29/tags/{arn}
- "List all search?" -> GET /2017-08-29/search
- "Create a tag?" -> POST /2017-08-29/tags
- "Update a tag?" -> PUT /2017-08-29/tags/{arn}
- "Update a jobTemplate?" -> PUT /2017-08-29/jobTemplates/{name}
- "Update a preset?" -> PUT /2017-08-29/presets/{name}
- "Update a queue?" -> PUT /2017-08-29/queues/{name}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
