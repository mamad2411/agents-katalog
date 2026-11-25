---
name: openai-api
description: "OpenAI API skill. Use when working with OpenAI for assistants, audio, batches. Covers 148 endpoints."
version: 1.0.0
generator: lapsh
---

# OpenAI API
API version: 2.3.0

## Auth
Bearer bearer

## Base URL
https://api.openai.com/v1

## Setup
1. Set Authorization header with your Bearer token
2. GET /assistants -- verify access
3. POST /assistants -- create first assistants

## Endpoints

148 endpoints across 18 groups. See references/api-spec.lap for full details.

### assistants
| Method | Path | Description |
|--------|------|-------------|
| GET | /assistants | Returns a list of assistants. |
| POST | /assistants | Create an assistant with a model and instructions. |
| GET | /assistants/{assistant_id} | Retrieves an assistant. |
| POST | /assistants/{assistant_id} | Modifies an assistant. |
| DELETE | /assistants/{assistant_id} | Delete an assistant. |

### audio
| Method | Path | Description |
|--------|------|-------------|
| POST | /audio/speech | Generates audio from the input text. |
| POST | /audio/transcriptions | Transcribes audio into the input language. |
| POST | /audio/translations | Translates audio into English. |

### batches
| Method | Path | Description |
|--------|------|-------------|
| POST | /batches | Creates and executes a batch from an uploaded file of requests |
| GET | /batches | List your organization's batches. |
| GET | /batches/{batch_id} | Retrieves a batch. |
| POST | /batches/{batch_id}/cancel | Cancels an in-progress batch. The batch will be in status `cancelling` for up to 10 minutes, before changing to `cancelled`, where it will have partial results (if any) available in the output file. |

### chat
| Method | Path | Description |
|--------|------|-------------|
| GET | /chat/completions | List stored Chat Completions. Only Chat Completions that have been stored |
| POST | /chat/completions | **Starting a new project?** We recommend trying [Responses](/docs/api-reference/responses) |
| GET | /chat/completions/{completion_id} | Get a stored chat completion. Only Chat Completions that have been created |
| POST | /chat/completions/{completion_id} | Modify a stored chat completion. Only Chat Completions that have been |
| DELETE | /chat/completions/{completion_id} | Delete a stored chat completion. Only Chat Completions that have been |
| GET | /chat/completions/{completion_id}/messages | Get the messages in a stored chat completion. Only Chat Completions that |

### completions
| Method | Path | Description |
|--------|------|-------------|
| POST | /completions | Creates a completion for the provided prompt and parameters. |

### embeddings
| Method | Path | Description |
|--------|------|-------------|
| POST | /embeddings | Creates an embedding vector representing the input text. |

### evals
| Method | Path | Description |
|--------|------|-------------|
| GET | /evals | List evaluations for a project. |
| POST | /evals | Create the structure of an evaluation that can be used to test a model's performance. |
| GET | /evals/{eval_id} | Get an evaluation by ID. |
| POST | /evals/{eval_id} | Update certain properties of an evaluation. |
| DELETE | /evals/{eval_id} | Delete an evaluation. |
| GET | /evals/{eval_id}/runs | Get a list of runs for an evaluation. |
| POST | /evals/{eval_id}/runs | Create a new evaluation run. This is the endpoint that will kick off grading. |
| GET | /evals/{eval_id}/runs/{run_id} | Get an evaluation run by ID. |
| POST | /evals/{eval_id}/runs/{run_id} | Cancel an ongoing evaluation run. |
| DELETE | /evals/{eval_id}/runs/{run_id} | Delete an eval run. |
| GET | /evals/{eval_id}/runs/{run_id}/output_items | Get a list of output items for an evaluation run. |
| GET | /evals/{eval_id}/runs/{run_id}/output_items/{output_item_id} | Get an evaluation run output item by ID. |

### files
| Method | Path | Description |
|--------|------|-------------|
| GET | /files | Returns a list of files. |
| POST | /files | Upload a file that can be used across various endpoints. Individual files can be up to 512 MB, and the size of all files uploaded by one organization can be up to 100 GB. |
| DELETE | /files/{file_id} | Delete a file. |
| GET | /files/{file_id} | Returns information about a specific file. |
| GET | /files/{file_id}/content | Returns the contents of the specified file. |

### fine_tuning
| Method | Path | Description |
|--------|------|-------------|
| GET | /fine_tuning/checkpoints/{fine_tuned_model_checkpoint}/permissions | **NOTE:** This endpoint requires an [admin API key](../admin-api-keys). |
| POST | /fine_tuning/checkpoints/{fine_tuned_model_checkpoint}/permissions | **NOTE:** Calling this endpoint requires an [admin API key](../admin-api-keys). |
| DELETE | /fine_tuning/checkpoints/{fine_tuned_model_checkpoint}/permissions/{permission_id} | **NOTE:** This endpoint requires an [admin API key](../admin-api-keys). |
| POST | /fine_tuning/jobs | Creates a fine-tuning job which begins the process of creating a new model from a given dataset. |
| GET | /fine_tuning/jobs | List your organization's fine-tuning jobs |
| GET | /fine_tuning/jobs/{fine_tuning_job_id} | Get info about a fine-tuning job. |
| POST | /fine_tuning/jobs/{fine_tuning_job_id}/cancel | Immediately cancel a fine-tune job. |
| GET | /fine_tuning/jobs/{fine_tuning_job_id}/checkpoints | List checkpoints for a fine-tuning job. |
| GET | /fine_tuning/jobs/{fine_tuning_job_id}/events | Get status updates for a fine-tuning job. |

### images
| Method | Path | Description |
|--------|------|-------------|
| POST | /images/edits | Creates an edited or extended image given one or more source images and a prompt. This endpoint only supports `gpt-image-1` and `dall-e-2`. |
| POST | /images/generations | Creates an image given a prompt. [Learn more](/docs/guides/images). |
| POST | /images/variations | Creates a variation of a given image. This endpoint only supports `dall-e-2`. |

### models
| Method | Path | Description |
|--------|------|-------------|
| GET | /models | Lists the currently available models, and provides basic information about each one such as the owner and availability. |
| GET | /models/{model} | Retrieves a model instance, providing basic information about the model such as the owner and permissioning. |
| DELETE | /models/{model} | Delete a fine-tuned model. You must have the Owner role in your organization to delete a model. |

### moderations
| Method | Path | Description |
|--------|------|-------------|
| POST | /moderations | Classifies if text and/or image inputs are potentially harmful. Learn |

### organization
| Method | Path | Description |
|--------|------|-------------|
| GET | /organization/admin_api_keys | List organization API keys |
| POST | /organization/admin_api_keys | Create an organization admin API key |
| GET | /organization/admin_api_keys/{key_id} | Retrieve a single organization API key |
| DELETE | /organization/admin_api_keys/{key_id} | Delete an organization admin API key |
| GET | /organization/audit_logs | List user actions and configuration changes within this organization. |
| GET | /organization/certificates | List uploaded certificates for this organization. |
| POST | /organization/certificates | Upload a certificate to the organization. This does **not** automatically activate the certificate. |
| POST | /organization/certificates/activate | Activate certificates at the organization level. |
| POST | /organization/certificates/deactivate | Deactivate certificates at the organization level. |
| GET | /organization/certificates/{certificate_id} | Get a certificate that has been uploaded to the organization. |
| POST | /organization/certificates/{certificate_id} | Modify a certificate. Note that only the name can be modified. |
| DELETE | /organization/certificates/{certificate_id} | Delete a certificate from the organization. |
| GET | /organization/costs | Get costs details for the organization. |
| GET | /organization/invites | Returns a list of invites in the organization. |
| POST | /organization/invites | Create an invite for a user to the organization. The invite must be accepted by the user before they have access to the organization. |
| GET | /organization/invites/{invite_id} | Retrieves an invite. |
| DELETE | /organization/invites/{invite_id} | Delete an invite. If the invite has already been accepted, it cannot be deleted. |
| GET | /organization/projects | Returns a list of projects. |
| POST | /organization/projects | Create a new project in the organization. Projects can be created and archived, but cannot be deleted. |
| GET | /organization/projects/{project_id} | Retrieves a project. |
| POST | /organization/projects/{project_id} | Modifies a project in the organization. |
| GET | /organization/projects/{project_id}/api_keys | Returns a list of API keys in the project. |
| GET | /organization/projects/{project_id}/api_keys/{key_id} | Retrieves an API key in the project. |
| DELETE | /organization/projects/{project_id}/api_keys/{key_id} | Deletes an API key from the project. |
| POST | /organization/projects/{project_id}/archive | Archives a project in the organization. Archived projects cannot be used or updated. |
| GET | /organization/projects/{project_id}/certificates | List certificates for this project. |
| POST | /organization/projects/{project_id}/certificates/activate | Activate certificates at the project level. |
| POST | /organization/projects/{project_id}/certificates/deactivate | Deactivate certificates at the project level. |
| GET | /organization/projects/{project_id}/rate_limits | Returns the rate limits per model for a project. |
| POST | /organization/projects/{project_id}/rate_limits/{rate_limit_id} | Updates a project rate limit. |
| GET | /organization/projects/{project_id}/service_accounts | Returns a list of service accounts in the project. |
| POST | /organization/projects/{project_id}/service_accounts | Creates a new service account in the project. This also returns an unredacted API key for the service account. |
| GET | /organization/projects/{project_id}/service_accounts/{service_account_id} | Retrieves a service account in the project. |
| DELETE | /organization/projects/{project_id}/service_accounts/{service_account_id} | Deletes a service account from the project. |
| GET | /organization/projects/{project_id}/users | Returns a list of users in the project. |
| POST | /organization/projects/{project_id}/users | Adds a user to the project. Users must already be members of the organization to be added to a project. |
| GET | /organization/projects/{project_id}/users/{user_id} | Retrieves a user in the project. |
| POST | /organization/projects/{project_id}/users/{user_id} | Modifies a user's role in the project. |
| DELETE | /organization/projects/{project_id}/users/{user_id} | Deletes a user from the project. |
| GET | /organization/usage/audio_speeches | Get audio speeches usage details for the organization. |
| GET | /organization/usage/audio_transcriptions | Get audio transcriptions usage details for the organization. |
| GET | /organization/usage/code_interpreter_sessions | Get code interpreter sessions usage details for the organization. |
| GET | /organization/usage/completions | Get completions usage details for the organization. |
| GET | /organization/usage/embeddings | Get embeddings usage details for the organization. |
| GET | /organization/usage/images | Get images usage details for the organization. |
| GET | /organization/usage/moderations | Get moderations usage details for the organization. |
| GET | /organization/usage/vector_stores | Get vector stores usage details for the organization. |
| GET | /organization/users | Lists all of the users in the organization. |
| GET | /organization/users/{user_id} | Retrieves a user by their identifier. |
| POST | /organization/users/{user_id} | Modifies a user's role in the organization. |
| DELETE | /organization/users/{user_id} | Deletes a user from the organization. |

### realtime
| Method | Path | Description |
|--------|------|-------------|
| POST | /realtime/sessions | Create an ephemeral API token for use in client-side applications with the |
| POST | /realtime/transcription_sessions | Create an ephemeral API token for use in client-side applications with the |

### responses
| Method | Path | Description |
|--------|------|-------------|
| POST | /responses | Creates a model response. Provide [text](/docs/guides/text) or |
| GET | /responses/{response_id} | Retrieves a model response with the given ID. |
| DELETE | /responses/{response_id} | Deletes a model response with the given ID. |
| GET | /responses/{response_id}/input_items | Returns a list of input items for a given response. |

### threads
| Method | Path | Description |
|--------|------|-------------|
| POST | /threads | Create a thread. |
| POST | /threads/runs | Create a thread and run it in one request. |
| GET | /threads/{thread_id} | Retrieves a thread. |
| POST | /threads/{thread_id} | Modifies a thread. |
| DELETE | /threads/{thread_id} | Delete a thread. |
| GET | /threads/{thread_id}/messages | Returns a list of messages for a given thread. |
| POST | /threads/{thread_id}/messages | Create a message. |
| GET | /threads/{thread_id}/messages/{message_id} | Retrieve a message. |
| POST | /threads/{thread_id}/messages/{message_id} | Modifies a message. |
| DELETE | /threads/{thread_id}/messages/{message_id} | Deletes a message. |
| GET | /threads/{thread_id}/runs | Returns a list of runs belonging to a thread. |
| POST | /threads/{thread_id}/runs | Create a run. |
| GET | /threads/{thread_id}/runs/{run_id} | Retrieves a run. |
| POST | /threads/{thread_id}/runs/{run_id} | Modifies a run. |
| POST | /threads/{thread_id}/runs/{run_id}/cancel | Cancels a run that is `in_progress`. |
| GET | /threads/{thread_id}/runs/{run_id}/steps | Returns a list of run steps belonging to a run. |
| GET | /threads/{thread_id}/runs/{run_id}/steps/{step_id} | Retrieves a run step. |
| POST | /threads/{thread_id}/runs/{run_id}/submit_tool_outputs | When a run has the `status: "requires_action"` and `required_action.type` is `submit_tool_outputs`, this endpoint can be used to submit the outputs from the tool calls once they're all completed. All outputs must be submitted in a single request. |

### uploads
| Method | Path | Description |
|--------|------|-------------|
| POST | /uploads | Creates an intermediate [Upload](/docs/api-reference/uploads/object) object |
| POST | /uploads/{upload_id}/cancel | Cancels the Upload. No Parts may be added after an Upload is cancelled. |
| POST | /uploads/{upload_id}/complete | Completes the [Upload](/docs/api-reference/uploads/object). |
| POST | /uploads/{upload_id}/parts | Adds a [Part](/docs/api-reference/uploads/part-object) to an [Upload](/docs/api-reference/uploads/object) object. A Part represents a chunk of bytes from the file you are trying to upload. |

### vector_stores
| Method | Path | Description |
|--------|------|-------------|
| GET | /vector_stores | Returns a list of vector stores. |
| POST | /vector_stores | Create a vector store. |
| GET | /vector_stores/{vector_store_id} | Retrieves a vector store. |
| POST | /vector_stores/{vector_store_id} | Modifies a vector store. |
| DELETE | /vector_stores/{vector_store_id} | Delete a vector store. |
| POST | /vector_stores/{vector_store_id}/file_batches | Create a vector store file batch. |
| GET | /vector_stores/{vector_store_id}/file_batches/{batch_id} | Retrieves a vector store file batch. |
| POST | /vector_stores/{vector_store_id}/file_batches/{batch_id}/cancel | Cancel a vector store file batch. This attempts to cancel the processing of files in this batch as soon as possible. |
| GET | /vector_stores/{vector_store_id}/file_batches/{batch_id}/files | Returns a list of vector store files in a batch. |
| GET | /vector_stores/{vector_store_id}/files | Returns a list of vector store files. |
| POST | /vector_stores/{vector_store_id}/files | Create a vector store file by attaching a [File](/docs/api-reference/files) to a [vector store](/docs/api-reference/vector-stores/object). |
| GET | /vector_stores/{vector_store_id}/files/{file_id} | Retrieves a vector store file. |
| DELETE | /vector_stores/{vector_store_id}/files/{file_id} | Delete a vector store file. This will remove the file from the vector store but the file itself will not be deleted. To delete the file, use the [delete file](/docs/api-reference/files/delete) endpoint. |
| POST | /vector_stores/{vector_store_id}/files/{file_id} | Update attributes on a vector store file. |
| GET | /vector_stores/{vector_store_id}/files/{file_id}/content | Retrieve the parsed contents of a vector store file. |
| POST | /vector_stores/{vector_store_id}/search | Search a vector store for relevant chunks based on a query and file attributes filter. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all assistants?" -> GET /assistants
- "Create a assistant?" -> POST /assistants
- "Get assistant details?" -> GET /assistants/{assistant_id}
- "Delete a assistant?" -> DELETE /assistants/{assistant_id}
- "Create a speech?" -> POST /audio/speech
- "Create a transcription?" -> POST /audio/transcriptions
- "Create a translation?" -> POST /audio/translations
- "Create a batche?" -> POST /batches
- "List all batches?" -> GET /batches
- "Get batche details?" -> GET /batches/{batch_id}
- "Create a cancel?" -> POST /batches/{batch_id}/cancel
- "List all completions?" -> GET /chat/completions
- "Create a completion?" -> POST /chat/completions
- "Get completion details?" -> GET /chat/completions/{completion_id}
- "Delete a completion?" -> DELETE /chat/completions/{completion_id}
- "List all messages?" -> GET /chat/completions/{completion_id}/messages
- "Create a completion?" -> POST /completions
- "Create a embedding?" -> POST /embeddings
- "List all evals?" -> GET /evals
- "Create a eval?" -> POST /evals
- "Get eval details?" -> GET /evals/{eval_id}
- "Delete a eval?" -> DELETE /evals/{eval_id}
- "List all runs?" -> GET /evals/{eval_id}/runs
- "Create a run?" -> POST /evals/{eval_id}/runs
- "Get run details?" -> GET /evals/{eval_id}/runs/{run_id}
- "Delete a run?" -> DELETE /evals/{eval_id}/runs/{run_id}
- "List all output_items?" -> GET /evals/{eval_id}/runs/{run_id}/output_items
- "Get output_item details?" -> GET /evals/{eval_id}/runs/{run_id}/output_items/{output_item_id}
- "List all files?" -> GET /files
- "Create a file?" -> POST /files
- "Delete a file?" -> DELETE /files/{file_id}
- "Get file details?" -> GET /files/{file_id}
- "List all content?" -> GET /files/{file_id}/content
- "List all permissions?" -> GET /fine_tuning/checkpoints/{fine_tuned_model_checkpoint}/permissions
- "Create a permission?" -> POST /fine_tuning/checkpoints/{fine_tuned_model_checkpoint}/permissions
- "Delete a permission?" -> DELETE /fine_tuning/checkpoints/{fine_tuned_model_checkpoint}/permissions/{permission_id}
- "Create a job?" -> POST /fine_tuning/jobs
- "List all jobs?" -> GET /fine_tuning/jobs
- "Get job details?" -> GET /fine_tuning/jobs/{fine_tuning_job_id}
- "Create a cancel?" -> POST /fine_tuning/jobs/{fine_tuning_job_id}/cancel
- "List all checkpoints?" -> GET /fine_tuning/jobs/{fine_tuning_job_id}/checkpoints
- "List all events?" -> GET /fine_tuning/jobs/{fine_tuning_job_id}/events
- "Create a edit?" -> POST /images/edits
- "Create a generation?" -> POST /images/generations
- "Create a variation?" -> POST /images/variations
- "List all models?" -> GET /models
- "Get model details?" -> GET /models/{model}
- "Delete a model?" -> DELETE /models/{model}
- "Create a moderation?" -> POST /moderations
- "List all admin_api_keys?" -> GET /organization/admin_api_keys
- "Create a admin_api_key?" -> POST /organization/admin_api_keys
- "Get admin_api_key details?" -> GET /organization/admin_api_keys/{key_id}
- "Delete a admin_api_key?" -> DELETE /organization/admin_api_keys/{key_id}
- "List all audit_logs?" -> GET /organization/audit_logs
- "List all certificates?" -> GET /organization/certificates
- "Create a certificate?" -> POST /organization/certificates
- "Create a activate?" -> POST /organization/certificates/activate
- "Create a deactivate?" -> POST /organization/certificates/deactivate
- "Get certificate details?" -> GET /organization/certificates/{certificate_id}
- "Delete a certificate?" -> DELETE /organization/certificates/{certificate_id}
- "List all costs?" -> GET /organization/costs
- "List all invites?" -> GET /organization/invites
- "Create a invite?" -> POST /organization/invites
- "Get invite details?" -> GET /organization/invites/{invite_id}
- "Delete a invite?" -> DELETE /organization/invites/{invite_id}
- "List all projects?" -> GET /organization/projects
- "Create a project?" -> POST /organization/projects
- "Get project details?" -> GET /organization/projects/{project_id}
- "List all api_keys?" -> GET /organization/projects/{project_id}/api_keys
- "Get api_key details?" -> GET /organization/projects/{project_id}/api_keys/{key_id}
- "Delete a api_key?" -> DELETE /organization/projects/{project_id}/api_keys/{key_id}
- "Create a archive?" -> POST /organization/projects/{project_id}/archive
- "List all certificates?" -> GET /organization/projects/{project_id}/certificates
- "Create a activate?" -> POST /organization/projects/{project_id}/certificates/activate
- "Create a deactivate?" -> POST /organization/projects/{project_id}/certificates/deactivate
- "List all rate_limits?" -> GET /organization/projects/{project_id}/rate_limits
- "List all service_accounts?" -> GET /organization/projects/{project_id}/service_accounts
- "Create a service_account?" -> POST /organization/projects/{project_id}/service_accounts
- "Get service_account details?" -> GET /organization/projects/{project_id}/service_accounts/{service_account_id}
- "Delete a service_account?" -> DELETE /organization/projects/{project_id}/service_accounts/{service_account_id}
- "List all users?" -> GET /organization/projects/{project_id}/users
- "Create a user?" -> POST /organization/projects/{project_id}/users
- "Get user details?" -> GET /organization/projects/{project_id}/users/{user_id}
- "Delete a user?" -> DELETE /organization/projects/{project_id}/users/{user_id}
- "List all audio_speeches?" -> GET /organization/usage/audio_speeches
- "List all audio_transcriptions?" -> GET /organization/usage/audio_transcriptions
- "List all code_interpreter_sessions?" -> GET /organization/usage/code_interpreter_sessions
- "List all completions?" -> GET /organization/usage/completions
- "List all embeddings?" -> GET /organization/usage/embeddings
- "List all images?" -> GET /organization/usage/images
- "List all moderations?" -> GET /organization/usage/moderations
- "List all vector_stores?" -> GET /organization/usage/vector_stores
- "List all users?" -> GET /organization/users
- "Get user details?" -> GET /organization/users/{user_id}
- "Delete a user?" -> DELETE /organization/users/{user_id}
- "Create a session?" -> POST /realtime/sessions
- "Create a transcription_session?" -> POST /realtime/transcription_sessions
- "Create a response?" -> POST /responses
- "Get response details?" -> GET /responses/{response_id}
- "Delete a response?" -> DELETE /responses/{response_id}
- "List all input_items?" -> GET /responses/{response_id}/input_items
- "Create a thread?" -> POST /threads
- "Create a run?" -> POST /threads/runs
- "Get thread details?" -> GET /threads/{thread_id}
- "Delete a thread?" -> DELETE /threads/{thread_id}
- "List all messages?" -> GET /threads/{thread_id}/messages
- "Create a message?" -> POST /threads/{thread_id}/messages
- "Get message details?" -> GET /threads/{thread_id}/messages/{message_id}
- "Delete a message?" -> DELETE /threads/{thread_id}/messages/{message_id}
- "List all runs?" -> GET /threads/{thread_id}/runs
- "Create a run?" -> POST /threads/{thread_id}/runs
- "Get run details?" -> GET /threads/{thread_id}/runs/{run_id}
- "Create a cancel?" -> POST /threads/{thread_id}/runs/{run_id}/cancel
- "List all steps?" -> GET /threads/{thread_id}/runs/{run_id}/steps
- "Get step details?" -> GET /threads/{thread_id}/runs/{run_id}/steps/{step_id}
- "Create a submit_tool_output?" -> POST /threads/{thread_id}/runs/{run_id}/submit_tool_outputs
- "Create a upload?" -> POST /uploads
- "Create a cancel?" -> POST /uploads/{upload_id}/cancel
- "Create a complete?" -> POST /uploads/{upload_id}/complete
- "Create a part?" -> POST /uploads/{upload_id}/parts
- "List all vector_stores?" -> GET /vector_stores
- "Create a vector_store?" -> POST /vector_stores
- "Get vector_store details?" -> GET /vector_stores/{vector_store_id}
- "Delete a vector_store?" -> DELETE /vector_stores/{vector_store_id}
- "Create a file_batche?" -> POST /vector_stores/{vector_store_id}/file_batches
- "Get file_batche details?" -> GET /vector_stores/{vector_store_id}/file_batches/{batch_id}
- "Create a cancel?" -> POST /vector_stores/{vector_store_id}/file_batches/{batch_id}/cancel
- "List all files?" -> GET /vector_stores/{vector_store_id}/file_batches/{batch_id}/files
- "List all files?" -> GET /vector_stores/{vector_store_id}/files
- "Create a file?" -> POST /vector_stores/{vector_store_id}/files
- "Get file details?" -> GET /vector_stores/{vector_store_id}/files/{file_id}
- "Delete a file?" -> DELETE /vector_stores/{vector_store_id}/files/{file_id}
- "List all content?" -> GET /vector_stores/{vector_store_id}/files/{file_id}/content
- "Create a search?" -> POST /vector_stores/{vector_store_id}/search
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
