---
name: aws-codepipeline
description: "AWS CodePipeline API skill. Use when working with AWS CodePipeline for root. Covers 43 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS CodePipeline
API version: 2015-07-09

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST / -- create first resource

## Endpoints

43 endpoints across 1 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| POST | / | Returns information about a specified job and whether that job has been received by the job worker. Used for custom actions only. |
| POST | / | Confirms a job worker has received the specified job. Used for partner actions only. |
| POST | / | Creates a new custom action that can be used in all pipelines associated with the Amazon Web Services account. Only used for custom actions. |
| POST | / | Creates a pipeline.  In the pipeline structure, you must include either artifactStore or artifactStores in your pipeline, but you cannot use both. If you create a cross-region action in your pipeline, you must use artifactStores. |
| POST | / | Marks a custom action as deleted. PollForJobs for the custom action fails after the action is marked for deletion. Used for custom actions only.  To re-create a custom action after it has been deleted you must use a string in the version field that has never been used before. This string can be an incremented version number, for example. To restore a deleted custom action, use a JSON file that is identical to the deleted action, including the original string in the version field. |
| POST | / | Deletes the specified pipeline. |
| POST | / | Deletes a previously created webhook by name. Deleting the webhook stops CodePipeline from starting a pipeline every time an external event occurs. The API returns successfully when trying to delete a webhook that is already deleted. If a deleted webhook is re-created by calling PutWebhook with the same name, it will have a different URL. |
| POST | / | Removes the connection between the webhook that was created by CodePipeline and the external tool with events to be detected. Currently supported only for webhooks that target an action type of GitHub. |
| POST | / | Prevents artifacts in a pipeline from transitioning to the next stage in the pipeline. |
| POST | / | Enables artifacts in a pipeline to transition to a stage in a pipeline. |
| POST | / | Returns information about an action type created for an external provider, where the action is to be used by customers of the external provider. The action can be created with any supported integration model. |
| POST | / | Returns information about a job. Used for custom actions only.  When this API is called, CodePipeline returns temporary credentials for the S3 bucket used to store artifacts for the pipeline, if the action requires access to that S3 bucket for input or output artifacts. This API also returns any secret values defined for the action. |
| POST | / | Returns the metadata, structure, stages, and actions of a pipeline. Can be used to return the entire structure of a pipeline in JSON format, which can then be modified and used to update the pipeline structure with UpdatePipeline. |
| POST | / | Returns information about an execution of a pipeline, including details about artifacts, the pipeline execution ID, and the name, version, and status of the pipeline. |
| POST | / | Returns information about the state of a pipeline, including the stages and actions.  Values returned in the revisionId and revisionUrl fields indicate the source revision information, such as the commit ID, for the current state. |
| POST | / | Requests the details of a job for a third party action. Used for partner actions only.  When this API is called, CodePipeline returns temporary credentials for the S3 bucket used to store artifacts for the pipeline, if the action requires access to that S3 bucket for input or output artifacts. This API also returns any secret values defined for the action. |
| POST | / | Lists the action executions that have occurred in a pipeline. |
| POST | / | Gets a summary of all CodePipeline action types associated with your account. |
| POST | / | Gets a summary of the most recent executions for a pipeline.  When applying the filter for pipeline executions that have succeeded in the stage, the operation returns all executions in the current pipeline version beginning on February 1, 2024. |
| POST | / | Gets a summary of all of the pipelines associated with your account. |
| POST | / | Lists the rule executions that have occurred in a pipeline configured for conditions with rules. |
| POST | / | Lists the rules for the condition. |
| POST | / | Gets the set of key-value pairs (metadata) that are used to manage the resource. |
| POST | / | Gets a listing of all the webhooks in this Amazon Web Services Region for this account. The output lists all webhooks and includes the webhook URL and ARN and the configuration for each webhook.  If a secret token was provided, it will be redacted in the response. |
| POST | / | Used to override a stage condition. |
| POST | / | Returns information about any jobs for CodePipeline to act on. PollForJobs is valid only for action types with "Custom" in the owner field. If the action type contains AWS or ThirdParty in the owner field, the PollForJobs action returns an error.  When this API is called, CodePipeline returns temporary credentials for the S3 bucket used to store artifacts for the pipeline, if the action requires access to that S3 bucket for input or output artifacts. This API also returns any secret values defined for the action. |
| POST | / | Determines whether there are any third party jobs for a job worker to act on. Used for partner actions only.  When this API is called, CodePipeline returns temporary credentials for the S3 bucket used to store artifacts for the pipeline, if the action requires access to that S3 bucket for input or output artifacts. |
| POST | / | Provides information to CodePipeline about new revisions to a source. |
| POST | / | Provides the response to a manual approval request to CodePipeline. Valid responses include Approved and Rejected. |
| POST | / | Represents the failure of a job as returned to the pipeline by a job worker. Used for custom actions only. |
| POST | / | Represents the success of a job as returned to the pipeline by a job worker. Used for custom actions only. |
| POST | / | Represents the failure of a third party job as returned to the pipeline by a job worker. Used for partner actions only. |
| POST | / | Represents the success of a third party job as returned to the pipeline by a job worker. Used for partner actions only. |
| POST | / | Defines a webhook and returns a unique webhook URL generated by CodePipeline. This URL can be supplied to third party source hosting providers to call every time there's a code change. When CodePipeline receives a POST request on this URL, the pipeline defined in the webhook is started as long as the POST request satisfied the authentication and filtering requirements supplied when defining the webhook. RegisterWebhookWithThirdParty and DeregisterWebhookWithThirdParty APIs can be used to automatically configure supported third parties to call the generated webhook URL.  When creating CodePipeline webhooks, do not use your own credentials or reuse the same secret token across multiple webhooks. For optimal security, generate a unique secret token for each webhook you create. The secret token is an arbitrary string that you provide, which GitHub uses to compute and sign the webhook payloads sent to CodePipeline, for protecting the integrity and authenticity of the webhook payloads. Using your own credentials or reusing the same token across multiple webhooks can lead to security vulnerabilities.   If a secret token was provided, it will be redacted in the response. |
| POST | / | Configures a connection between the webhook that was created and the external tool with events to be detected. |
| POST | / | You can retry a stage that has failed without having to run a pipeline again from the beginning. You do this by either retrying the failed actions in a stage or by retrying all actions in the stage starting from the first action in the stage. When you retry the failed actions in a stage, all actions that are still in progress continue working, and failed actions are triggered again. When you retry a failed stage from the first action in the stage, the stage cannot have any actions in progress. Before a stage can be retried, it must either have all actions failed or some actions failed and some succeeded. |
| POST | / | Rolls back a stage execution. |
| POST | / | Starts the specified pipeline. Specifically, it begins processing the latest commit to the source location specified as part of the pipeline. |
| POST | / | Stops the specified pipeline execution. You choose to either stop the pipeline execution by completing in-progress actions without starting subsequent actions, or by abandoning in-progress actions. While completing or abandoning in-progress actions, the pipeline execution is in a Stopping state. After all in-progress actions are completed or abandoned, the pipeline execution is in a Stopped state. |
| POST | / | Adds to or modifies the tags of the given resource. Tags are metadata that can be used to manage a resource. |
| POST | / | Removes tags from an Amazon Web Services resource. |
| POST | / | Updates an action type that was created with any supported integration model, where the action type is to be used by customers of the action type provider. Use a JSON file with the action definition and UpdateActionType to provide the full structure. |
| POST | / | Updates a specified pipeline with edits or changes to its structure. Use a JSON file with the pipeline structure and UpdatePipeline to provide the full structure of the pipeline. Updating the pipeline increases the version number of the pipeline by 1. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
