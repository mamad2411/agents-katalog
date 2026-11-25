---
name: vectara-rest-api
description: "Vectara REST API skill. Use when working with Vectara REST for compute-account-size, compute-corpus-size, create-api-key. Covers 29 endpoints."
version: 1.0.0
generator: lapsh
---

# Vectara REST API
API version: 1.0.0

## Auth
OAuth2 | ApiKey x-api-key in header

## Base URL
https://api.vectara.io

## Setup
1. Set your API key in the appropriate header
3. POST /v1/compute-account-size -- create first compute-account-size

## Endpoints

29 endpoints across 29 groups. See references/api-spec.lap for full details.

### compute-account-size
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/compute-account-size | Computes the amount of quota consumed across the entire Vectara account. |

### compute-corpus-size
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/compute-corpus-size | Computes the amount of quota consumed by a corpus. This capability is useful for administrators to track and monitor the amount |

### create-api-key
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/create-api-key | Creates an API key that you bind with a specific corpus or multiple corpora. You can create an API key that only gives access to query data (read-only) or an API key that gives access to both querying and serving (read-write). |

### create-corpus
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/create-corpus | Creates a corpus, which is a container to store data in. |

### delete-api-key
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/delete-api-key | Deletes API keys to help you manage the security and lifecycle of API keys in your application. |

### delete-conversations
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/delete-conversations | Delete conversations from the chat history corpus. This is useful for data management to help ensure that you maintain data hygiene and support compliance with data retention policies. |

### delete-corpus
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/delete-corpus | Deletes a corpus and all of the data contained inside of the corpus. |

### delete-doc
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/delete-doc | Delete documents from a corpus. |

### delete-turns
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/delete-turns | Deletes specific turns from a conversation within the chat history corpus. This enables developers to remove inaccurate or inappropriate responses from the conversation history. |

### disable-turns
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/disable-turns | Disables specific turns from a conversation within the chat history corpus. This is useful for excluding specific turns from a conversation. |

### enable-api-key
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/enable-api-key | Enables or disables a specific API key. |

### get-usage-metrics
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/get-usage-metrics | Displays usage information about indexing and query operations in a corpus. This helps administrators in analyzing and managing resource consumption more efficiently for specific corpora. |

### index
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/index | This is the "standard" Indexing API for indexing semi-structured, text-heavy "documents."  Indexing data into Vectara is typically very fast: within a few seconds. |

### list-api-keys
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/list-api-keys | Lists the API keys and the associated corpora names and IDs. |

### list-conversations
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/list-conversations | List all the conversations in a specific corpus. This data enables developers to monitor chatbot interactions and understand how users engage with the data. Pagination lets developers navigate through large datasets. |

### list-corpora
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/list-corpora | Lists all corpora accessible to the OAuth client. |

### list-documents
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/list-documents | Lists information about each document ingested into the corpus including the Document ID and metadata. This is useful for managing the lifecycle of documents and a quick way to check which documents are already in the index. |

### list-jobs
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/list-jobs | List the jobs associated with this account.  Jobs are background processes like [replacing the filterable metadata attributes](https://docs.vectara.com/docs/rest-api/replace-corpus-filter-attrs). |

### list-users
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/list-users | Lists the users in your account along with their corpus access and customer-level authorizations. |

### manage-user
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/manage-user | Lets you manage users in your account by adding, deleting, enabling, or disabling users. You can also reset their passwords and edit user roles. This endpoint can help you streamline your onboarding process by programmatically adding new users, assigning appropriate roles, and setting up permissions. |

### query
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/query | Search for relevant results, highlight relevant snippets, and do |

### read-conversations
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/read-conversations | Retrieves detailed information about specific conversations. This information enables developers to analyze the flow of user chats and understand the context of interactions, which helps in refining chatbot responses. You can read up to 100 conversations. |

### read-corpus
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/read-corpus | Displays detailed information about corpora within your account including basic information, metadata, and whether it is enabled or disabled. |

### replace-corpus-filter-attrs
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/replace-corpus-filter-attrs | Updates the filterable metadata fields for the corpus. |

### reset-corpus
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/reset-corpus | Resets a corpus by removing all of the documents inside of it. |

### stream-query
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/stream-query | Stream responses as you search for relevant results, highlight relevant snippets, and do |

### update-corpus-enablement
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/update-corpus-enablement | Lets you enable or disable a corpus. This is useful when you need to take the corpus offline without having to delete the corpus. |

### core
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/core/index | This API is intended to be used by experts.  It gives you fine-grained control over chunking |

### upload
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/upload | The File Upload API can be used to index binary files like PDFs, Word Documents, and similar. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a compute-account-size?" -> POST /v1/compute-account-size
- "Create a compute-corpus-size?" -> POST /v1/compute-corpus-size
- "Create a create-api-key?" -> POST /v1/create-api-key
- "Create a create-corpus?" -> POST /v1/create-corpus
- "Create a delete-api-key?" -> POST /v1/delete-api-key
- "Create a delete-conversation?" -> POST /v1/delete-conversations
- "Create a delete-corpus?" -> POST /v1/delete-corpus
- "Create a delete-doc?" -> POST /v1/delete-doc
- "Create a delete-turn?" -> POST /v1/delete-turns
- "Create a disable-turn?" -> POST /v1/disable-turns
- "Create a enable-api-key?" -> POST /v1/enable-api-key
- "Create a get-usage-metric?" -> POST /v1/get-usage-metrics
- "Create a index?" -> POST /v1/index
- "Create a list-api-key?" -> POST /v1/list-api-keys
- "Create a list-conversation?" -> POST /v1/list-conversations
- "Create a list-corpora?" -> POST /v1/list-corpora
- "Create a list-document?" -> POST /v1/list-documents
- "Create a list-job?" -> POST /v1/list-jobs
- "Create a list-user?" -> POST /v1/list-users
- "Create a manage-user?" -> POST /v1/manage-user
- "Create a query?" -> POST /v1/query
- "Create a read-conversation?" -> POST /v1/read-conversations
- "Create a read-corpus?" -> POST /v1/read-corpus
- "Create a replace-corpus-filter-attr?" -> POST /v1/replace-corpus-filter-attrs
- "Create a reset-corpus?" -> POST /v1/reset-corpus
- "Create a stream-query?" -> POST /v1/stream-query
- "Create a update-corpus-enablement?" -> POST /v1/update-corpus-enablement
- "Create a index?" -> POST /v1/core/index
- "Create a upload?" -> POST /v1/upload
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
