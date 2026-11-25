---
name: myreels-api
description: Practical integration guide for the MyReels API. Use the live `GET /api/v1/models/api` endpoint to discover available models, parameters, defaults, options, and field descriptions before submitting generation tasks.
---

# MyReels API Integration Guide

### Prerequisites

- An active subscription is required for generation and task query endpoints.
- Create an AccessToken in [myreels.ai/developer](https://myreels.ai/developer).
- Result URLs are not stored for you permanently. Save them on your side.
- `GET https://api.myreels.ai/api/v1/models/api` was verified on March 18, 2026 and currently does not require `Authorization`.

### Installation

```bash
npx skills add https://github.com/myreelsai/skills --skill myreels-api -g
```

Remove `-g` for a project-level install.

### Authentication

Use:

```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### Recommended Flow

#### 0. Load live model metadata first

Before mapping user intent to request fields, call:

```http
GET https://api.myreels.ai/api/v1/models/api
```

Prioritize these fields:

- `modelName`
- `name`
- `tags`
- `description`
- `estimatedCost`
- `displayConfig.estimatedTime`
- `userInputSchema`
- `userInputSchema.<param>.label`
- `userInputSchema.<param>.description`
- `userInputSchema.<param>.default`
- `userInputSchema.<param>.options`

Display cost as points:

- use `estimatedCost` as the display points field

For natural-language requests such as "stronger motion", "disable prompt extension", or "higher human fidelity", map user intent from `label` and `description`, not from field names alone.

#### 1. Submit a task

```http
POST https://api.myreels.ai/generation/:modelName
Content-Type: application/json
Authorization: Bearer YOUR_ACCESS_TOKEN
```

`:modelName` must be the actual `modelName`, not the slug.

Example:

```json
{
  "prompt": "A cinematic portrait with soft studio lighting"
}
```

Example success response:

```json
{
  "status": "ok",
  "message": "Successfully created task",
  "data": { "taskID": "task_xxx" }
}
```

#### 2. Query task status

```http
GET https://api.myreels.ai/query/task/:taskID
Authorization: Bearer YOUR_ACCESS_TOKEN
```

Example completed response:

```json
{
  "status": "ok",
  "message": "Successfully obtained task info",
  "data": {
    "status": "completed",
    "progress": 100,
    "resultUrls": [{ "url": "https://cdn.example.com/result.png" }]
  }
}
```

Task states:

- `pending`
- `processing`
- `completed`
- `failed`

Polling guidance:

- image generation / image editing: 10 seconds
- video generation: 30 seconds to 1 minute

Query rate limit:

- 60 requests per minute

### Response Rules

- If the upstream response includes `code`, Worker uses it as the final HTTP status.
- If upstream does not include `code`, Worker falls back to the upstream HTTP status.
- Check the final HTTP status first.
- If the HTTP status is `2xx`, then inspect `status`.
- For task queries, check `data.status` after `status === "ok"`.

Public paths:

- `POST /generation/:modelName`
- `GET /query/task/:taskID`
- `GET|POST /api/v1/*`

### Model Categories

| Category | Tags | Description |
|------|------|------|
| Image and editing | `t2i` / `i2i` / `i2e` | text-to-image, image-to-image, image editing |
| Video | `t2v` / `i2v` | text-to-video, image-to-video, avatar/video motion |
| Speech and music | `t2a` / `m2a` | text-to-speech, music generation |

Use the live schema described in [references/models.md](references/models.md) for current models, parameters, defaults, options, and field descriptions.

### References

- [references/models.md](references/models.md)
- [references/code-examples.md](references/code-examples.md)
- [references/errors.md](references/errors.md)
