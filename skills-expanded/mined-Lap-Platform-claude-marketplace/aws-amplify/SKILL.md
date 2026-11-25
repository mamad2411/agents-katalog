---
name: aws-amplify
description: "AWS Amplify API skill. Use when working with AWS Amplify for apps, webhooks, artifacts. Covers 37 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS Amplify
API version: 2017-07-25

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /apps -- verify access
3. POST /apps -- create first apps

## Endpoints

37 endpoints across 4 groups. See references/api-spec.lap for full details.

### apps
| Method | Path | Description |
|--------|------|-------------|
| POST | /apps | Creates a new Amplify app. |
| POST | /apps/{appId}/backendenvironments | Creates a new backend environment for an Amplify app.  This API is available only to Amplify Gen 1 applications where the backend is created using Amplify Studio or the Amplify command line interface (CLI). This API isn’t available to Amplify Gen 2 applications. When you deploy an application with Amplify Gen 2, you provision the app's backend infrastructure using Typescript code. |
| POST | /apps/{appId}/branches | Creates a new branch for an Amplify app. |
| POST | /apps/{appId}/branches/{branchName}/deployments | Creates a deployment for a manually deployed Amplify app. Manually deployed apps are not connected to a repository.  The maximum duration between the CreateDeployment call and the StartDeployment call cannot exceed 8 hours. If the duration exceeds 8 hours, the StartDeployment call and the associated Job will fail. |
| POST | /apps/{appId}/domains | Creates a new domain association for an Amplify app. This action associates a custom domain with the Amplify app |
| POST | /apps/{appId}/webhooks | Creates a new webhook on an Amplify app. |
| DELETE | /apps/{appId} | Deletes an existing Amplify app specified by an app ID. |
| DELETE | /apps/{appId}/backendenvironments/{environmentName} | Deletes a backend environment for an Amplify app.  This API is available only to Amplify Gen 1 applications where the backend is created using Amplify Studio or the Amplify command line interface (CLI). This API isn’t available to Amplify Gen 2 applications. When you deploy an application with Amplify Gen 2, you provision the app's backend infrastructure using Typescript code. |
| DELETE | /apps/{appId}/branches/{branchName} | Deletes a branch for an Amplify app. |
| DELETE | /apps/{appId}/domains/{domainName} | Deletes a domain association for an Amplify app. |
| DELETE | /apps/{appId}/branches/{branchName}/jobs/{jobId} | Deletes a job for a branch of an Amplify app. |
| POST | /apps/{appId}/accesslogs | Returns the website access logs for a specific time range using a presigned URL. |
| GET | /apps/{appId} | Returns an existing Amplify app specified by an app ID. |
| GET | /apps/{appId}/backendenvironments/{environmentName} | Returns a backend environment for an Amplify app.  This API is available only to Amplify Gen 1 applications where the backend is created using Amplify Studio or the Amplify command line interface (CLI). This API isn’t available to Amplify Gen 2 applications. When you deploy an application with Amplify Gen 2, you provision the app's backend infrastructure using Typescript code. |
| GET | /apps/{appId}/branches/{branchName} | Returns a branch for an Amplify app. |
| GET | /apps/{appId}/domains/{domainName} | Returns the domain information for an Amplify app. |
| GET | /apps/{appId}/branches/{branchName}/jobs/{jobId} | Returns a job for a branch of an Amplify app. |
| GET | /apps | Returns a list of the existing Amplify apps. |
| GET | /apps/{appId}/branches/{branchName}/jobs/{jobId}/artifacts | Returns a list of artifacts for a specified app, branch, and job. |
| GET | /apps/{appId}/backendenvironments | Lists the backend environments for an Amplify app.  This API is available only to Amplify Gen 1 applications where the backend is created using Amplify Studio or the Amplify command line interface (CLI). This API isn’t available to Amplify Gen 2 applications. When you deploy an application with Amplify Gen 2, you provision the app's backend infrastructure using Typescript code. |
| GET | /apps/{appId}/branches | Lists the branches of an Amplify app. |
| GET | /apps/{appId}/domains | Returns the domain associations for an Amplify app. |
| GET | /apps/{appId}/branches/{branchName}/jobs | Lists the jobs for a branch of an Amplify app. |
| GET | /apps/{appId}/webhooks | Returns a list of webhooks for an Amplify app. |
| POST | /apps/{appId}/branches/{branchName}/deployments/start | Starts a deployment for a manually deployed app. Manually deployed apps are not connected to a repository.  The maximum duration between the CreateDeployment call and the StartDeployment call cannot exceed 8 hours. If the duration exceeds 8 hours, the StartDeployment call and the associated Job will fail. |
| POST | /apps/{appId}/branches/{branchName}/jobs | Starts a new job for a branch of an Amplify app. |
| DELETE | /apps/{appId}/branches/{branchName}/jobs/{jobId}/stop | Stops a job that is in progress for a branch of an Amplify app. |
| POST | /apps/{appId} | Updates an existing Amplify app. |
| POST | /apps/{appId}/branches/{branchName} | Updates a branch for an Amplify app. |
| POST | /apps/{appId}/domains/{domainName} | Creates a new domain association for an Amplify app. |

### webhooks
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /webhooks/{webhookId} | Deletes a webhook. |
| GET | /webhooks/{webhookId} | Returns the webhook information that corresponds to a specified webhook ID. |
| POST | /webhooks/{webhookId} | Updates a webhook. |

### artifacts
| Method | Path | Description |
|--------|------|-------------|
| GET | /artifacts/{artifactId} | Returns the artifact info that corresponds to an artifact id. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags/{resourceArn} | Returns a list of tags for a specified Amazon Resource Name (ARN). |
| POST | /tags/{resourceArn} | Tags the resource with a tag key and value. |
| DELETE | /tags/{resourceArn} | Untags a resource with a specified Amazon Resource Name (ARN). |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a app?" -> POST /apps
- "Create a backendenvironment?" -> POST /apps/{appId}/backendenvironments
- "Create a branche?" -> POST /apps/{appId}/branches
- "Create a deployment?" -> POST /apps/{appId}/branches/{branchName}/deployments
- "Create a domain?" -> POST /apps/{appId}/domains
- "Create a webhook?" -> POST /apps/{appId}/webhooks
- "Delete a app?" -> DELETE /apps/{appId}
- "Delete a backendenvironment?" -> DELETE /apps/{appId}/backendenvironments/{environmentName}
- "Delete a branche?" -> DELETE /apps/{appId}/branches/{branchName}
- "Delete a domain?" -> DELETE /apps/{appId}/domains/{domainName}
- "Delete a job?" -> DELETE /apps/{appId}/branches/{branchName}/jobs/{jobId}
- "Delete a webhook?" -> DELETE /webhooks/{webhookId}
- "Create a accesslog?" -> POST /apps/{appId}/accesslogs
- "Get app details?" -> GET /apps/{appId}
- "Get artifact details?" -> GET /artifacts/{artifactId}
- "Get backendenvironment details?" -> GET /apps/{appId}/backendenvironments/{environmentName}
- "Get branche details?" -> GET /apps/{appId}/branches/{branchName}
- "Get domain details?" -> GET /apps/{appId}/domains/{domainName}
- "Get job details?" -> GET /apps/{appId}/branches/{branchName}/jobs/{jobId}
- "Get webhook details?" -> GET /webhooks/{webhookId}
- "List all apps?" -> GET /apps
- "List all artifacts?" -> GET /apps/{appId}/branches/{branchName}/jobs/{jobId}/artifacts
- "List all backendenvironments?" -> GET /apps/{appId}/backendenvironments
- "List all branches?" -> GET /apps/{appId}/branches
- "List all domains?" -> GET /apps/{appId}/domains
- "List all jobs?" -> GET /apps/{appId}/branches/{branchName}/jobs
- "Get tag details?" -> GET /tags/{resourceArn}
- "List all webhooks?" -> GET /apps/{appId}/webhooks
- "Create a start?" -> POST /apps/{appId}/branches/{branchName}/deployments/start
- "Create a job?" -> POST /apps/{appId}/branches/{branchName}/jobs
- "Delete a tag?" -> DELETE /tags/{resourceArn}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
