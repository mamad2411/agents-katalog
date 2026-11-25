---
name: amazon-elastic-transcoder
description: "Amazon Elastic Transcoder API skill. Use when working with Amazon Elastic Transcoder for 2012-09-25. Covers 17 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon Elastic Transcoder
API version: 2012-09-25

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /2012-09-25/pipelines -- verify access
3. POST /2012-09-25/jobs -- create first jobs

## Endpoints

17 endpoints across 1 groups. See references/api-spec.lap for full details.

### 2012-09-25
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /2012-09-25/jobs/{Id} | The CancelJob operation cancels an unfinished job.  You can only cancel a job that has a status of Submitted. To prevent a pipeline from starting to process a job while you're getting the job identifier, use UpdatePipelineStatus to temporarily pause the pipeline. |
| POST | /2012-09-25/jobs | When you create a job, Elastic Transcoder returns JSON data that includes the values that you specified plus information about the job that is created. If you have specified more than one output for your jobs (for example, one output for the Kindle Fire and another output for the Apple iPhone 4s), you currently must use the Elastic Transcoder API to list the jobs (as opposed to the AWS Console). |
| POST | /2012-09-25/pipelines | The CreatePipeline operation creates a pipeline with settings that you specify. |
| POST | /2012-09-25/presets | The CreatePreset operation creates a preset with settings that you specify.  Elastic Transcoder checks the CreatePreset settings to ensure that they meet Elastic Transcoder requirements and to determine whether they comply with H.264 standards. If your settings are not valid for Elastic Transcoder, Elastic Transcoder returns an HTTP 400 response (ValidationException) and does not create the preset. If the settings are valid for Elastic Transcoder but aren't strictly compliant with the H.264 standard, Elastic Transcoder creates the preset and returns a warning message in the response. This helps you determine whether your settings comply with the H.264 standard while giving you greater flexibility with respect to the video that Elastic Transcoder produces.  Elastic Transcoder uses the H.264 video-compression format. For more information, see the International Telecommunication Union publication Recommendation ITU-T H.264: Advanced video coding for generic audiovisual services. |
| DELETE | /2012-09-25/pipelines/{Id} | The DeletePipeline operation removes a pipeline.  You can only delete a pipeline that has never been used or that is not currently in use (doesn't contain any active jobs). If the pipeline is currently in use, DeletePipeline returns an error. |
| DELETE | /2012-09-25/presets/{Id} | The DeletePreset operation removes a preset that you've added in an AWS region.  You can't delete the default presets that are included with Elastic Transcoder. |
| GET | /2012-09-25/jobsByPipeline/{PipelineId} | The ListJobsByPipeline operation gets a list of the jobs currently in a pipeline. Elastic Transcoder returns all of the jobs currently in the specified pipeline. The response body contains one element for each job that satisfies the search criteria. |
| GET | /2012-09-25/jobsByStatus/{Status} | The ListJobsByStatus operation gets a list of jobs that have a specified status. The response body contains one element for each job that satisfies the search criteria. |
| GET | /2012-09-25/pipelines | The ListPipelines operation gets a list of the pipelines associated with the current AWS account. |
| GET | /2012-09-25/presets | The ListPresets operation gets a list of the default presets included with Elastic Transcoder and the presets that you've added in an AWS region. |
| GET | /2012-09-25/jobs/{Id} | The ReadJob operation returns detailed information about a job. |
| GET | /2012-09-25/pipelines/{Id} | The ReadPipeline operation gets detailed information about a pipeline. |
| GET | /2012-09-25/presets/{Id} | The ReadPreset operation gets detailed information about a preset. |
| POST | /2012-09-25/roleTests | The TestRole operation tests the IAM role used to create the pipeline. The TestRole action lets you determine whether the IAM role you are using has sufficient permissions to let Elastic Transcoder perform tasks associated with the transcoding process. The action attempts to assume the specified IAM role, checks read access to the input and output buckets, and tries to send a test notification to Amazon SNS topics that you specify. |
| PUT | /2012-09-25/pipelines/{Id} | Use the UpdatePipeline operation to update settings for a pipeline.  When you change pipeline settings, your changes take effect immediately. Jobs that you have already submitted and that Elastic Transcoder has not started to process are affected in addition to jobs that you submit after you change settings. |
| POST | /2012-09-25/pipelines/{Id}/notifications | With the UpdatePipelineNotifications operation, you can update Amazon Simple Notification Service (Amazon SNS) notifications for a pipeline. When you update notifications for a pipeline, Elastic Transcoder returns the values that you specified in the request. |
| POST | /2012-09-25/pipelines/{Id}/status | The UpdatePipelineStatus operation pauses or reactivates a pipeline, so that the pipeline stops or restarts the processing of jobs. Changing the pipeline status is useful if you want to cancel one or more jobs. You can't cancel jobs after Elastic Transcoder has started processing them; if you pause the pipeline to which you submitted the jobs, you have more time to get the job IDs for the jobs that you want to cancel, and to send a CancelJob request. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Delete a job?" -> DELETE /2012-09-25/jobs/{Id}
- "Create a job?" -> POST /2012-09-25/jobs
- "Create a pipeline?" -> POST /2012-09-25/pipelines
- "Create a preset?" -> POST /2012-09-25/presets
- "Delete a pipeline?" -> DELETE /2012-09-25/pipelines/{Id}
- "Delete a preset?" -> DELETE /2012-09-25/presets/{Id}
- "Get jobsByPipeline details?" -> GET /2012-09-25/jobsByPipeline/{PipelineId}
- "Get jobsByStatus details?" -> GET /2012-09-25/jobsByStatus/{Status}
- "List all pipelines?" -> GET /2012-09-25/pipelines
- "List all presets?" -> GET /2012-09-25/presets
- "Get job details?" -> GET /2012-09-25/jobs/{Id}
- "Get pipeline details?" -> GET /2012-09-25/pipelines/{Id}
- "Get preset details?" -> GET /2012-09-25/presets/{Id}
- "Create a roleTest?" -> POST /2012-09-25/roleTests
- "Update a pipeline?" -> PUT /2012-09-25/pipelines/{Id}
- "Create a notification?" -> POST /2012-09-25/pipelines/{Id}/notifications
- "Create a status?" -> POST /2012-09-25/pipelines/{Id}/status
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
