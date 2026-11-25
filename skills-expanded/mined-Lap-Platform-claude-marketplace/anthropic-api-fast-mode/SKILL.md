---
name: anthropic-api-fast-mode
description: "Anthropic API + fast-mode API skill. Use when working with Anthropic API + fast-mode for messages, complete, models. Covers 47 endpoints."
version: 1.0.0
generator: lapsh
---

# Anthropic API + fast-mode
API version: 253

## Auth
ApiKey x-api-key in header

## Base URL
https://api.anthropic.com

## Setup
1. Set your API key in the appropriate header
2. GET /v1/models -- verify access
3. POST /v1/messages -- create first messages

## Endpoints

47 endpoints across 9 groups. See references/api-spec.lap for full details.

### messages
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/messages | Create a Message |
| POST | /v1/messages/batches | Create a Message Batch |
| GET | /v1/messages/batches | List Message Batches |
| GET | /v1/messages/batches/{message_batch_id} | Retrieve a Message Batch |
| DELETE | /v1/messages/batches/{message_batch_id} | Delete a Message Batch |
| POST | /v1/messages/batches/{message_batch_id}/cancel | Cancel a Message Batch |
| GET | /v1/messages/batches/{message_batch_id}/results | Retrieve Message Batch results |
| POST | /v1/messages/count_tokens | Count tokens in a Message |
| POST | /v1/messages/batches?beta=true | Create a Message Batch |
| GET | /v1/messages/batches?beta=true | List Message Batches |
| GET | /v1/messages/batches/{message_batch_id}?beta=true | Retrieve a Message Batch |
| DELETE | /v1/messages/batches/{message_batch_id}?beta=true | Delete a Message Batch |
| POST | /v1/messages/batches/{message_batch_id}/cancel?beta=true | Cancel a Message Batch |
| GET | /v1/messages/batches/{message_batch_id}/results?beta=true | Retrieve Message Batch results |
| POST | /v1/messages/count_tokens?beta=true | Count tokens in a Message |

### complete
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/complete | Create a Text Completion |

### models
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/models | List Models |
| GET | /v1/models/{model_id} | Get a Model |
| GET | /v1/models/{model_id}?beta=true | Get a Model |

### files
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/files | Upload File |
| GET | /v1/files | List Files |
| GET | /v1/files/{file_id} | Get File Metadata |
| DELETE | /v1/files/{file_id} | Delete File |
| GET | /v1/files/{file_id}/content | Download File |
| GET | /v1/files/{file_id}?beta=true | Get File Metadata |
| DELETE | /v1/files/{file_id}?beta=true | Delete File |
| GET | /v1/files/{file_id}/content?beta=true | Download File |

### skills
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/skills | Create Skill |
| GET | /v1/skills | List Skills |
| GET | /v1/skills/{skill_id} | Get Skill |
| DELETE | /v1/skills/{skill_id} | Delete Skill |
| POST | /v1/skills/{skill_id}/versions | Create Skill Version |
| GET | /v1/skills/{skill_id}/versions | List Skill Versions |
| GET | /v1/skills/{skill_id}/versions/{version} | Get Skill Version |
| DELETE | /v1/skills/{skill_id}/versions/{version} | Delete Skill Version |
| GET | /v1/skills/{skill_id}?beta=true | Get Skill |
| DELETE | /v1/skills/{skill_id}?beta=true | Delete Skill |
| POST | /v1/skills/{skill_id}/versions?beta=true | Create Skill Version |
| GET | /v1/skills/{skill_id}/versions?beta=true | List Skill Versions |
| GET | /v1/skills/{skill_id}/versions/{version}?beta=true | Get Skill Version |
| DELETE | /v1/skills/{skill_id}/versions/{version}?beta=true | Delete Skill Version |

### messages?beta=true
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/messages?beta=true | Create a Message |

### models?beta=true
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/models?beta=true | List Models |

### files?beta=true
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/files?beta=true | Upload File |
| GET | /v1/files?beta=true | List Files |

### skills?beta=true
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/skills?beta=true | Create Skill |
| GET | /v1/skills?beta=true | List Skills |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a message?" -> POST /v1/messages
- "Create a complete?" -> POST /v1/complete
- "List all models?" -> GET /v1/models
- "Get model details?" -> GET /v1/models/{model_id}
- "Create a batche?" -> POST /v1/messages/batches
- "List all batches?" -> GET /v1/messages/batches
- "Get batche details?" -> GET /v1/messages/batches/{message_batch_id}
- "Delete a batche?" -> DELETE /v1/messages/batches/{message_batch_id}
- "Create a cancel?" -> POST /v1/messages/batches/{message_batch_id}/cancel
- "List all results?" -> GET /v1/messages/batches/{message_batch_id}/results
- "Create a count_token?" -> POST /v1/messages/count_tokens
- "Create a file?" -> POST /v1/files
- "List all files?" -> GET /v1/files
- "Get file details?" -> GET /v1/files/{file_id}
- "Delete a file?" -> DELETE /v1/files/{file_id}
- "List all content?" -> GET /v1/files/{file_id}/content
- "Create a skill?" -> POST /v1/skills
- "List all skills?" -> GET /v1/skills
- "Get skill details?" -> GET /v1/skills/{skill_id}
- "Delete a skill?" -> DELETE /v1/skills/{skill_id}
- "Create a version?" -> POST /v1/skills/{skill_id}/versions
- "List all versions?" -> GET /v1/skills/{skill_id}/versions
- "Get version details?" -> GET /v1/skills/{skill_id}/versions/{version}
- "Delete a version?" -> DELETE /v1/skills/{skill_id}/versions/{version}
- "Create a messages?beta=true?" -> POST /v1/messages?beta=true
- "List all models?beta=true?" -> GET /v1/models?beta=true
- "Get model details?" -> GET /v1/models/{model_id}?beta=true
- "Create a batches?beta=true?" -> POST /v1/messages/batches?beta=true
- "List all batches?beta=true?" -> GET /v1/messages/batches?beta=true
- "Get batche details?" -> GET /v1/messages/batches/{message_batch_id}?beta=true
- "Delete a batche?" -> DELETE /v1/messages/batches/{message_batch_id}?beta=true
- "Create a cancel?beta=true?" -> POST /v1/messages/batches/{message_batch_id}/cancel?beta=true
- "List all results?beta=true?" -> GET /v1/messages/batches/{message_batch_id}/results?beta=true
- "Create a count_tokens?beta=true?" -> POST /v1/messages/count_tokens?beta=true
- "Create a files?beta=true?" -> POST /v1/files?beta=true
- "List all files?beta=true?" -> GET /v1/files?beta=true
- "Get file details?" -> GET /v1/files/{file_id}?beta=true
- "Delete a file?" -> DELETE /v1/files/{file_id}?beta=true
- "List all content?beta=true?" -> GET /v1/files/{file_id}/content?beta=true
- "Create a skills?beta=true?" -> POST /v1/skills?beta=true
- "List all skills?beta=true?" -> GET /v1/skills?beta=true
- "Get skill details?" -> GET /v1/skills/{skill_id}?beta=true
- "Delete a skill?" -> DELETE /v1/skills/{skill_id}?beta=true
- "Create a versions?beta=true?" -> POST /v1/skills/{skill_id}/versions?beta=true
- "List all versions?beta=true?" -> GET /v1/skills/{skill_id}/versions?beta=true
- "Get version details?" -> GET /v1/skills/{skill_id}/versions/{version}?beta=true
- "Delete a version?" -> DELETE /v1/skills/{skill_id}/versions/{version}?beta=true
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
