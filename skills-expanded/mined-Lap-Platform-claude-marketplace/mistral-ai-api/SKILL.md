---
name: mistral-ai-api
description: "Mistral AI API skill. Use when working with Mistral AI for models, conversations, agents. Covers 71 endpoints."
version: 1.0.0
generator: lapsh
---

# Mistral AI API
API version: 1.0.0

## Auth
Bearer bearer

## Base URL
https://api.mistral.ai

## Setup
1. Set Authorization header with your Bearer token
2. GET /v1/models -- verify access
3. POST /v1/conversations -- create first conversations

## Endpoints

71 endpoints across 15 groups. See references/api-spec.lap for full details.

### models
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/models | List Models |
| GET | /v1/models/{model_id} | Retrieve Model |
| DELETE | /v1/models/{model_id} | Delete Model |

### conversations
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/conversations | Create a conversation and append entries to it. |
| GET | /v1/conversations | List all created conversations. |
| GET | /v1/conversations/{conversation_id} | Retrieve a conversation information. |
| DELETE | /v1/conversations/{conversation_id} | Delete a conversation. |
| POST | /v1/conversations/{conversation_id} | Append new entries to an existing conversation. |
| GET | /v1/conversations/{conversation_id}/history | Retrieve all entries in a conversation. |
| GET | /v1/conversations/{conversation_id}/messages | Retrieve all messages in a conversation. |
| POST | /v1/conversations/{conversation_id}/restart | Restart a conversation starting from a given entry. |
| POST | /v1/conversations/{conversation_id}#stream | Append new entries to an existing conversation. |
| POST | /v1/conversations/{conversation_id}/restart#stream | Restart a conversation starting from a given entry. |

### agents
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/agents | Create a agent that can be used within a conversation. |
| GET | /v1/agents | List agent entities. |
| GET | /v1/agents/{agent_id} | Retrieve an agent entity. |
| PATCH | /v1/agents/{agent_id} | Update an agent entity. |
| DELETE | /v1/agents/{agent_id} | Delete an agent entity. |
| PATCH | /v1/agents/{agent_id}/version | Update an agent version. |
| GET | /v1/agents/{agent_id}/versions | List all versions of an agent. |
| GET | /v1/agents/{agent_id}/versions/{version} | Retrieve a specific version of an agent. |
| PUT | /v1/agents/{agent_id}/aliases | Create or update an agent version alias. |
| GET | /v1/agents/{agent_id}/aliases | List all aliases for an agent. |
| POST | /v1/agents/completions | Agents Completion |

### conversations#stream
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/conversations#stream | Create a conversation and append entries to it. |

### files
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/files | Upload File |
| GET | /v1/files | List Files |
| GET | /v1/files/{file_id} | Retrieve File |
| DELETE | /v1/files/{file_id} | Delete File |
| GET | /v1/files/{file_id}/content | Download File |
| GET | /v1/files/{file_id}/url | Get Signed Url |

### fine_tuning
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/fine_tuning/jobs | Get Fine Tuning Jobs |
| POST | /v1/fine_tuning/jobs | Create Fine Tuning Job |
| GET | /v1/fine_tuning/jobs/{job_id} | Get Fine Tuning Job |
| POST | /v1/fine_tuning/jobs/{job_id}/cancel | Cancel Fine Tuning Job |
| POST | /v1/fine_tuning/jobs/{job_id}/start | Start Fine Tuning Job |
| PATCH | /v1/fine_tuning/models/{model_id} | Update Fine Tuned Model |
| POST | /v1/fine_tuning/models/{model_id}/archive | Archive Fine Tuned Model |
| DELETE | /v1/fine_tuning/models/{model_id}/archive | Unarchive Fine Tuned Model |

### batch
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/batch/jobs | Get Batch Jobs |
| POST | /v1/batch/jobs | Create Batch Job |
| GET | /v1/batch/jobs/{job_id} | Get Batch Job |
| POST | /v1/batch/jobs/{job_id}/cancel | Cancel Batch Job |

### chat
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/chat/completions | Chat Completion |
| POST | /v1/chat/moderations | Chat Moderations |
| POST | /v1/chat/classifications | Chat Classifications |

### fim
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/fim/completions | Fim Completion |

### embeddings
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/embeddings | Embeddings |

### moderations
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/moderations | Moderations |

### ocr
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/ocr | OCR |

### classifications
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/classifications | Classifications |

### audio
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/audio/transcriptions | Create Transcription |
| POST | /v1/audio/transcriptions#stream | Create Streaming Transcription (SSE) |

### libraries
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/libraries | List all libraries you have access to. |
| POST | /v1/libraries | Create a new Library. |
| GET | /v1/libraries/{library_id} | Detailed information about a specific Library. |
| DELETE | /v1/libraries/{library_id} | Delete a library and all of it's document. |
| PUT | /v1/libraries/{library_id} | Update a library. |
| GET | /v1/libraries/{library_id}/documents | List documents in a given library. |
| POST | /v1/libraries/{library_id}/documents | Upload a new document. |
| GET | /v1/libraries/{library_id}/documents/{document_id} | Retrieve the metadata of a specific document. |
| PUT | /v1/libraries/{library_id}/documents/{document_id} | Update the metadata of a specific document. |
| DELETE | /v1/libraries/{library_id}/documents/{document_id} | Delete a document. |
| GET | /v1/libraries/{library_id}/documents/{document_id}/text_content | Retrieve the text content of a specific document. |
| GET | /v1/libraries/{library_id}/documents/{document_id}/status | Retrieve the processing status of a specific document. |
| GET | /v1/libraries/{library_id}/documents/{document_id}/signed-url | Retrieve the signed URL of a specific document. |
| GET | /v1/libraries/{library_id}/documents/{document_id}/extracted-text-signed-url | Retrieve the signed URL of text extracted from a given document. |
| POST | /v1/libraries/{library_id}/documents/{document_id}/reprocess | Reprocess a document. |
| GET | /v1/libraries/{library_id}/share | List all of the access to this library. |
| PUT | /v1/libraries/{library_id}/share | Create or update an access level. |
| DELETE | /v1/libraries/{library_id}/share | Delete an access level. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all models?" -> GET /v1/models
- "Get model details?" -> GET /v1/models/{model_id}
- "Delete a model?" -> DELETE /v1/models/{model_id}
- "Create a conversation?" -> POST /v1/conversations
- "List all conversations?" -> GET /v1/conversations
- "Get conversation details?" -> GET /v1/conversations/{conversation_id}
- "Delete a conversation?" -> DELETE /v1/conversations/{conversation_id}
- "List all history?" -> GET /v1/conversations/{conversation_id}/history
- "List all messages?" -> GET /v1/conversations/{conversation_id}/messages
- "Create a restart?" -> POST /v1/conversations/{conversation_id}/restart
- "Create a agent?" -> POST /v1/agents
- "List all agents?" -> GET /v1/agents
- "Get agent details?" -> GET /v1/agents/{agent_id}
- "Partially update a agent?" -> PATCH /v1/agents/{agent_id}
- "Delete a agent?" -> DELETE /v1/agents/{agent_id}
- "List all versions?" -> GET /v1/agents/{agent_id}/versions
- "Get version details?" -> GET /v1/agents/{agent_id}/versions/{version}
- "List all aliases?" -> GET /v1/agents/{agent_id}/aliases
- "Create a conversations#stream?" -> POST /v1/conversations#stream
- "Create a restart#stream?" -> POST /v1/conversations/{conversation_id}/restart#stream
- "Create a file?" -> POST /v1/files
- "Search files?" -> GET /v1/files
- "Get file details?" -> GET /v1/files/{file_id}
- "Delete a file?" -> DELETE /v1/files/{file_id}
- "List all content?" -> GET /v1/files/{file_id}/content
- "List all url?" -> GET /v1/files/{file_id}/url
- "List all jobs?" -> GET /v1/fine_tuning/jobs
- "Create a job?" -> POST /v1/fine_tuning/jobs
- "Get job details?" -> GET /v1/fine_tuning/jobs/{job_id}
- "Create a cancel?" -> POST /v1/fine_tuning/jobs/{job_id}/cancel
- "Create a start?" -> POST /v1/fine_tuning/jobs/{job_id}/start
- "Partially update a model?" -> PATCH /v1/fine_tuning/models/{model_id}
- "Create a archive?" -> POST /v1/fine_tuning/models/{model_id}/archive
- "List all jobs?" -> GET /v1/batch/jobs
- "Create a job?" -> POST /v1/batch/jobs
- "Get job details?" -> GET /v1/batch/jobs/{job_id}
- "Create a cancel?" -> POST /v1/batch/jobs/{job_id}/cancel
- "Create a completion?" -> POST /v1/chat/completions
- "Create a completion?" -> POST /v1/fim/completions
- "Create a completion?" -> POST /v1/agents/completions
- "Create a embedding?" -> POST /v1/embeddings
- "Create a moderation?" -> POST /v1/moderations
- "Create a moderation?" -> POST /v1/chat/moderations
- "Create a ocr?" -> POST /v1/ocr
- "Create a classification?" -> POST /v1/classifications
- "Create a classification?" -> POST /v1/chat/classifications
- "Create a transcription?" -> POST /v1/audio/transcriptions
- "Create a transcriptions#stream?" -> POST /v1/audio/transcriptions#stream
- "List all libraries?" -> GET /v1/libraries
- "Create a library?" -> POST /v1/libraries
- "Get library details?" -> GET /v1/libraries/{library_id}
- "Delete a library?" -> DELETE /v1/libraries/{library_id}
- "Update a library?" -> PUT /v1/libraries/{library_id}
- "Search documents?" -> GET /v1/libraries/{library_id}/documents
- "Create a document?" -> POST /v1/libraries/{library_id}/documents
- "Get document details?" -> GET /v1/libraries/{library_id}/documents/{document_id}
- "Update a document?" -> PUT /v1/libraries/{library_id}/documents/{document_id}
- "Delete a document?" -> DELETE /v1/libraries/{library_id}/documents/{document_id}
- "List all text_content?" -> GET /v1/libraries/{library_id}/documents/{document_id}/text_content
- "List all status?" -> GET /v1/libraries/{library_id}/documents/{document_id}/status
- "List all signed-url?" -> GET /v1/libraries/{library_id}/documents/{document_id}/signed-url
- "List all extracted-text-signed-url?" -> GET /v1/libraries/{library_id}/documents/{document_id}/extracted-text-signed-url
- "Create a reprocess?" -> POST /v1/libraries/{library_id}/documents/{document_id}/reprocess
- "List all share?" -> GET /v1/libraries/{library_id}/share
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
