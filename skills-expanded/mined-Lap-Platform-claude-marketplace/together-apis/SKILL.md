---
name: together-apis
description: "Together APIs API skill. Use when working with Together APIs for deployments, voices, videos. Covers 91 endpoints."
version: 1.0.0
generator: lapsh
---

# Together APIs
API version: 2.0.0

## Auth
Bearer bearer

## Base URL
https://api.together.xyz/v1

## Setup
1. Set Authorization header with your Bearer token
2. GET /deployments -- verify access
3. POST /deployments -- create first deployments

## Endpoints

91 endpoints across 24 groups. See references/api-spec.lap for full details.

### deployments
| Method | Path | Description |
|--------|------|-------------|
| GET | /deployments | Get the list of deployments |
| POST | /deployments | Create a new deployment |
| DELETE | /deployments/{id} | Delete a deployment |
| GET | /deployments/{id} | Get a deployment by ID or name |
| PATCH | /deployments/{id} | Update a deployment |
| GET | /deployments/{id}/logs | Get logs for a deployment |
| GET | /deployments/secrets | Get the list of project secrets |
| POST | /deployments/secrets | Create a new secret |
| DELETE | /deployments/secrets/{id} | Delete a secret |
| GET | /deployments/secrets/{id} | Get a secret by ID or name |
| PATCH | /deployments/secrets/{id} | Update a secret |
| GET | /deployments/storage/{filename} | Download a file |
| GET | /deployments/storage/volumes | Get the list of project volumes |
| POST | /deployments/storage/volumes | Create a new volume |
| DELETE | /deployments/storage/volumes/{id} | Delete a volume |
| GET | /deployments/storage/volumes/{id} | Get a volume by ID or name |
| PATCH | /deployments/storage/volumes/{id} | Update a volume |

### voices
| Method | Path | Description |
|--------|------|-------------|
| GET | /voices | Fetch available voices for each model |

### videos
| Method | Path | Description |
|--------|------|-------------|
| GET | /videos/{id} | Fetch video metadata |
| POST | /videos | Create video |

### chat
| Method | Path | Description |
|--------|------|-------------|
| POST | /chat/completions | Create chat completion |

### completions
| Method | Path | Description |
|--------|------|-------------|
| POST | /completions | Create completion |

### embeddings
| Method | Path | Description |
|--------|------|-------------|
| POST | /embeddings | Create embedding |

### models
| Method | Path | Description |
|--------|------|-------------|
| GET | /models | List all models |
| POST | /models | Upload a custom model or adapter |

### jobs
| Method | Path | Description |
|--------|------|-------------|
| GET | /jobs/{jobId} | Get job status |
| GET | /jobs | List all jobs |

### images
| Method | Path | Description |
|--------|------|-------------|
| POST | /images/generations | Create image |

### files
| Method | Path | Description |
|--------|------|-------------|
| GET | /files | List all files |
| GET | /files/{id} | Retrieve file metadata |
| DELETE | /files/{id} | Delete a file |
| GET | /files/{id}/content | Get file contents |
| POST | /files/upload | Upload a file |

### fine-tunes
| Method | Path | Description |
|--------|------|-------------|
| POST | /fine-tunes | Create job |
| GET | /fine-tunes | List all jobs |
| POST | /fine-tunes/estimate-price | Estimate price |
| GET | /fine-tunes/{id} | List job |
| DELETE | /fine-tunes/{id} | Delete a fine-tune job |
| GET | /fine-tunes/{id}/events | List job events |
| GET | /fine-tunes/{id}/checkpoints | List checkpoints |
| POST | /fine-tunes/{id}/cancel | Cancel job |

### finetune
| Method | Path | Description |
|--------|------|-------------|
| GET | /finetune/download | Download model |

### rerank
| Method | Path | Description |
|--------|------|-------------|
| POST | /rerank | Create a rerank request |

### audio
| Method | Path | Description |
|--------|------|-------------|
| POST | /audio/speech | Create audio generation request |
| GET | /audio/speech/websocket | Real-time text-to-speech via WebSocket |
| POST | /audio/transcriptions | Create audio transcription request |
| POST | /audio/translations | Create audio translation request |

### compute
| Method | Path | Description |
|--------|------|-------------|
| GET | /compute/clusters | List all GPU clusters. |
| POST | /compute/clusters | Create GPU Cluster |
| GET | /compute/clusters/{cluster_id} | Get GPU cluster by cluster ID |
| PUT | /compute/clusters/{cluster_id} | Update a GPU Cluster. |
| DELETE | /compute/clusters/{cluster_id} | Delete GPU cluster by cluster ID |
| GET | /compute/regions | List regions and corresponding supported driver versions |
| GET | /compute/clusters/storage/volumes | List all shared volumes. |
| PUT | /compute/clusters/storage/volumes | Update a shared volume. |
| POST | /compute/clusters/storage/volumes | Create a shared volume. |
| GET | /compute/clusters/storage/volumes/{volume_id} | Get shared volume by volume Id. |
| DELETE | /compute/clusters/storage/volumes/{volume_id} | Delete shared volume by volume id. |

### clusters
| Method | Path | Description |
|--------|------|-------------|
| GET | /clusters/availability-zones | List all available availability zones. |

### endpoints
| Method | Path | Description |
|--------|------|-------------|
| GET | /endpoints | List all endpoints, can be filtered by type |
| POST | /endpoints | Create a dedicated endpoint, it will start automatically |
| GET | /endpoints/{endpointId} | Get endpoint by ID |
| PATCH | /endpoints/{endpointId} | Update endpoint, this can also be used to start or stop a dedicated endpoint |
| DELETE | /endpoints/{endpointId} | Delete endpoint |

### hardware
| Method | Path | Description |
|--------|------|-------------|
| GET | /hardware | List available hardware configurations |

### tci
| Method | Path | Description |
|--------|------|-------------|
| POST | /tci/execute | Executes the given code snippet and returns the output. Without a session_id, a new session will be created to run the code. If you do pass in a valid session_id, the code will be run in that session. This is useful for running multiple code snippets in the same environment, because dependencies and similar things are persisted |
| GET | /tci/sessions | Lists all your currently active sessions. |

### batches
| Method | Path | Description |
|--------|------|-------------|
| GET | /batches | List batch jobs |
| POST | /batches | Create a batch job |
| GET | /batches/{id} | Get a batch job |
| POST | /batches/{id}/cancel | Cancel a batch job |

### evaluation
| Method | Path | Description |
|--------|------|-------------|
| POST | /evaluation | Create an evaluation job |
| GET | /evaluation | Get all evaluation jobs |
| GET | /evaluation/model-list | Get model list |
| GET | /evaluation/{id} | Get evaluation job details |
| GET | /evaluation/{id}/status | Get evaluation job status and results |

### realtime
| Method | Path | Description |
|--------|------|-------------|
| GET | /realtime | Real-time audio transcription via WebSocket |

### queue
| Method | Path | Description |
|--------|------|-------------|
| POST | /queue/cancel | Cancel a queued job |
| GET | /queue/metrics | Get queue metrics |
| GET | /queue/status | Get job status |
| POST | /queue/submit | Submit a queued job |

### rl
| Method | Path | Description |
|--------|------|-------------|
| GET | /rl/training-sessions | List training sessions |
| POST | /rl/training-sessions | Create training session |
| GET | /rl/training-sessions/{session_id} | Get training session |
| GET | /rl/training-sessions/{session_id}/operations/forward-backward/{operation_id} | Get forward-backward operation |
| GET | /rl/training-sessions/{session_id}/operations/optim-step/{operation_id} | Get optim-step operation |
| GET | /rl/training-sessions/{session_id}/operations/sample/{operation_id} | Get sample operation |
| POST | /rl/training-sessions/{session_id}/operations/forward-backward | Forward-backward pass |
| POST | /rl/training-sessions/{session_id}/operations/optim-step | Optimizer step |
| POST | /rl/training-sessions/{session_id}/operations/sample | Sample |
| POST | /rl/training-sessions/{session_id}/stop | Stop training session |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all deployments?" -> GET /deployments
- "Create a deployment?" -> POST /deployments
- "Delete a deployment?" -> DELETE /deployments/{id}
- "Get deployment details?" -> GET /deployments/{id}
- "Partially update a deployment?" -> PATCH /deployments/{id}
- "List all logs?" -> GET /deployments/{id}/logs
- "List all secrets?" -> GET /deployments/secrets
- "Create a secret?" -> POST /deployments/secrets
- "Delete a secret?" -> DELETE /deployments/secrets/{id}
- "Get secret details?" -> GET /deployments/secrets/{id}
- "Partially update a secret?" -> PATCH /deployments/secrets/{id}
- "Get storage details?" -> GET /deployments/storage/{filename}
- "List all volumes?" -> GET /deployments/storage/volumes
- "Create a volume?" -> POST /deployments/storage/volumes
- "Delete a volume?" -> DELETE /deployments/storage/volumes/{id}
- "Get volume details?" -> GET /deployments/storage/volumes/{id}
- "Partially update a volume?" -> PATCH /deployments/storage/volumes/{id}
- "List all voices?" -> GET /voices
- "Get video details?" -> GET /videos/{id}
- "Create a video?" -> POST /videos
- "Create a completion?" -> POST /chat/completions
- "Create a completion?" -> POST /completions
- "Create a embedding?" -> POST /embeddings
- "List all models?" -> GET /models
- "Create a model?" -> POST /models
- "Get job details?" -> GET /jobs/{jobId}
- "List all jobs?" -> GET /jobs
- "Create a generation?" -> POST /images/generations
- "List all files?" -> GET /files
- "Get file details?" -> GET /files/{id}
- "Delete a file?" -> DELETE /files/{id}
- "List all content?" -> GET /files/{id}/content
- "Create a upload?" -> POST /files/upload
- "Create a fine-tune?" -> POST /fine-tunes
- "List all fine-tunes?" -> GET /fine-tunes
- "Create a estimate-price?" -> POST /fine-tunes/estimate-price
- "Get fine-tune details?" -> GET /fine-tunes/{id}
- "Delete a fine-tune?" -> DELETE /fine-tunes/{id}
- "List all events?" -> GET /fine-tunes/{id}/events
- "List all checkpoints?" -> GET /fine-tunes/{id}/checkpoints
- "List all download?" -> GET /finetune/download
- "Create a cancel?" -> POST /fine-tunes/{id}/cancel
- "Create a rerank?" -> POST /rerank
- "Create a speech?" -> POST /audio/speech
- "List all websocket?" -> GET /audio/speech/websocket
- "Create a transcription?" -> POST /audio/transcriptions
- "Create a translation?" -> POST /audio/translations
- "List all clusters?" -> GET /compute/clusters
- "Create a cluster?" -> POST /compute/clusters
- "Get cluster details?" -> GET /compute/clusters/{cluster_id}
- "Update a cluster?" -> PUT /compute/clusters/{cluster_id}
- "Delete a cluster?" -> DELETE /compute/clusters/{cluster_id}
- "List all regions?" -> GET /compute/regions
- "List all volumes?" -> GET /compute/clusters/storage/volumes
- "Create a volume?" -> POST /compute/clusters/storage/volumes
- "Get volume details?" -> GET /compute/clusters/storage/volumes/{volume_id}
- "Delete a volume?" -> DELETE /compute/clusters/storage/volumes/{volume_id}
- "List all availability-zones?" -> GET /clusters/availability-zones
- "List all endpoints?" -> GET /endpoints
- "Create a endpoint?" -> POST /endpoints
- "Get endpoint details?" -> GET /endpoints/{endpointId}
- "Partially update a endpoint?" -> PATCH /endpoints/{endpointId}
- "Delete a endpoint?" -> DELETE /endpoints/{endpointId}
- "List all hardware?" -> GET /hardware
- "Create a execute?" -> POST /tci/execute
- "List all sessions?" -> GET /tci/sessions
- "List all batches?" -> GET /batches
- "Create a batche?" -> POST /batches
- "Get batche details?" -> GET /batches/{id}
- "Create a cancel?" -> POST /batches/{id}/cancel
- "Create a evaluation?" -> POST /evaluation
- "List all evaluation?" -> GET /evaluation
- "List all model-list?" -> GET /evaluation/model-list
- "Get evaluation details?" -> GET /evaluation/{id}
- "List all status?" -> GET /evaluation/{id}/status
- "List all realtime?" -> GET /realtime
- "Create a cancel?" -> POST /queue/cancel
- "List all metrics?" -> GET /queue/metrics
- "List all status?" -> GET /queue/status
- "Create a submit?" -> POST /queue/submit
- "List all training-sessions?" -> GET /rl/training-sessions
- "Create a training-session?" -> POST /rl/training-sessions
- "Get training-session details?" -> GET /rl/training-sessions/{session_id}
- "Get forward-backward details?" -> GET /rl/training-sessions/{session_id}/operations/forward-backward/{operation_id}
- "Get optim-step details?" -> GET /rl/training-sessions/{session_id}/operations/optim-step/{operation_id}
- "Get sample details?" -> GET /rl/training-sessions/{session_id}/operations/sample/{operation_id}
- "Create a forward-backward?" -> POST /rl/training-sessions/{session_id}/operations/forward-backward
- "Create a optim-step?" -> POST /rl/training-sessions/{session_id}/operations/optim-step
- "Create a sample?" -> POST /rl/training-sessions/{session_id}/operations/sample
- "Create a stop?" -> POST /rl/training-sessions/{session_id}/stop
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
