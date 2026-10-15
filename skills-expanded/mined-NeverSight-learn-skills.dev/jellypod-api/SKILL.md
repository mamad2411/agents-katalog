---
name: jellypod-api
description: >-
  How to use the Jellypod API to create AI-powered podcasts programmatically —
  creating hosts, uploading sources, generating episodes, and publishing. Use
  this skill whenever someone wants to build with the Jellypod API, integrate
  Jellypod into an application, generate podcast content programmatically,
  automate podcast production, or interact with any Jellypod endpoint. Also use
  when someone mentions AI podcasts, podcast generation APIs, or turning text
  into podcast episodes via code.
---

# Jellypod API

Jellypod is an AI podcast studio. Users describe an episode in plain language, attach source material (URLs, PDFs, YouTube videos, text), and Jellypod's content engine researches the topic, writes a multi-host script, and produces full audio. Think of it as a podcast production team that works in minutes instead of weeks.

The API gives you programmatic access to that same pipeline: create AI hosts with distinct personalities and voices, upload research sources, generate episodes from a prompt, and publish to Spotify, Apple Podcasts, YouTube, and a Jellypod-hosted website — all from code.

**Base URL:** `https://api.jellypod.com/v1`

**API Docs:** [https://jellypod.com/docs/api](https://jellypod.com/docs/api)

**OpenAPI Spec:** [https://jellypod.com/docs/api/openapi.yaml](https://jellypod.com/docs/api/openapi.yaml) — If you need exact request/response schemas, field constraints, or run into something this guide doesn't cover, fetch the full spec for the complete contract on every endpoint.

## Authentication

All requests require a Bearer token via the `Authorization` header:

```
Authorization: Bearer sk_live_...
```

API keys are organization-scoped. Create and manage them from the Jellypod dashboard under **Settings > API Keys**.

## Core Concepts

Before diving into endpoints, here's the mental model:

- **Podcast** — A series. It has a title, description, hosts, and settings. Think of it as the container.
- **Episode** — An individual entry in a podcast. Each has its own audio, video, script, and can be published independently.
- **Host** — An AI persona that narrates episodes. Hosts have names, backstories, personalities, and voices. A podcast can have multiple hosts who have natural conversations.
- **Voice** — A TTS voice from the voice library. 100+ professional voices across 30+ languages, plus cloned voices. All voices can speak any language, but sound most natural in their native one.
- **Source** — Reference material (URL, YouTube video, text, or file upload) that Jellypod uses as research context when generating episodes.
- **Credits** — The platform currency. Credits are consumed when episodes are generated. Check your balance via the Account endpoint.

## Important: Async Operations

Episode generation, batch podcast generation, and source processing are **asynchronous**. These endpoints return `202 Accepted` with a resource ID. You need to **poll** the corresponding GET endpoint to check status.

For episode generation, poll `GET /episodes/{id}` every ~5 seconds. The response includes a `generation` object with `phase` and `progress_pct` while generating. When done, `status` changes to `draft` and `audio_url` is populated. Generation typically takes 2-8 minutes depending on length and sources.

There is a concurrent limit of **5 episodes generating simultaneously** per organization. Exceeding this returns `429` with error code `concurrent_limit_exceeded`.

## Pagination

List endpoints use cursor-based pagination. Pass `cursor` and `limit` (1-100, default 20) as query parameters. Responses include a `pagination` object:

```json
{
  "has_more": true,
  "next_cursor": "abc123"
}
```

Pass `next_cursor` as `cursor` in the next request. When `has_more` is `false`, you've reached the end.

## Rate Limiting

Every response includes `RateLimit-Limit`, `RateLimit-Remaining`, and `RateLimit-Reset` headers. When rate limited, you get `429` with a `Retry-After` header.

---

## Endpoints

### Hosts

Hosts are the AI personalities that narrate your episodes. Each host has a name, backstory (their background and speaking style), an optional title (like "Tech Journalist"), a personality description, and a voice from the library.

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/hosts` | List hosts (paginated) |
| `POST` | `/hosts` | Create a host |
| `GET` | `/hosts/{host_id}` | Get a host |
| `PATCH` | `/hosts/{host_id}` | Update a host (partial) |
| `DELETE` | `/hosts/{host_id}` | Archive a host |

**Create a host:**

```bash
curl -X POST https://api.jellypod.com/v1/hosts \
  -H "Authorization: Bearer sk_live_..." \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alex Chen",
    "backstory": "Alex is a veteran technology reporter who has covered Silicon Valley for over a decade. Known for asking tough questions and breaking down complex topics.",
    "voice_id": 42,
    "title": "Tech Journalist",
    "personality": "Curious, articulate, slightly skeptical",
    "voice_model": "horizon"
  }'
```

Required fields: `name`, `backstory` (10-3000 chars), `voice_id`. The `voice_model` defaults to `horizon` (the latest high-quality model). Host IDs are short strings like `xK9mQ2pL` (not UUIDs).

Archived hosts (via DELETE) used in existing episodes are soft-deleted, not permanently removed.

### Voices

Browse the voice library to find the right voice for your hosts.

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/voices` | List voices (paginated, filterable) |
| `GET` | `/voices/{voice_id}` | Get a voice |

**Filters on list:** `language` (ISO 639-1 code like `en`, `ja`), `gender` (`male`, `female`, `other`), `voice_type` (`professional`, `clone`, `design`).

Voice IDs are integers, not strings.

### Sources

Sources are reference material that Jellypod uses when generating episodes. Upload URLs, YouTube videos, text, or files (PDF, DOCX, PPTX, CSV, markdown, plain text — max 10 MB).

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/sources` | List sources (filterable by `type` and `status`) |
| `POST` | `/sources` | Create a source (async — returns `202`) |
| `GET` | `/sources/{source_id}` | Get a source (poll for processing status) |
| `DELETE` | `/sources/{source_id}` | Delete a source |

**Create a URL source:**

```bash
curl -X POST https://api.jellypod.com/v1/sources \
  -H "Authorization: Bearer sk_live_..." \
  -H "Content-Type: application/json" \
  -d '{
    "type": "url",
    "url": "https://example.com/article",
    "title": "Research Article"
  }'
```

**Create a text source:**

```json
{
  "type": "text",
  "content": "Your research text here...",
  "title": "Meeting Notes"
}
```

**Upload a file** (multipart/form-data):

```bash
curl -X POST https://api.jellypod.com/v1/sources \
  -H "Authorization: Bearer sk_live_..." \
  -F "file=@report.pdf" \
  -F "title=Q1 Report"
```

Source types: `url`, `youtube`, `text`, `file`. Processing status: `awaiting_upload` > `processing` > `completed` (or `error`). Source IDs are UUIDs.

### Episodes

Episodes are where the magic happens. Give Jellypod a prompt and optional sources, and it researches, writes a script, and generates full audio.

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/podcasts/{podcast_id}/episodes/generate` | Generate an episode (async — `202`) |
| `GET` | `/episodes` | List episodes (filterable by `podcast_id`, `status`) |
| `GET` | `/episodes/{episode_id}` | Get an episode (poll generation status) |
| `DELETE` | `/episodes/{episode_id}` | Delete an episode |
| `PUT` | `/episodes/{episode_id}/image` | Upload cover image |
| `POST` | `/episodes/{episode_id}/publish` | Publish or schedule |
| `POST` | `/episodes/{episode_id}/unpublish` | Revert to draft |

**Generate an episode:**

```bash
curl -X POST https://api.jellypod.com/v1/podcasts/{podcast_id}/episodes/generate \
  -H "Authorization: Bearer sk_live_..." \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explore the latest developments in AI agents and how they are changing software development workflows.",
    "options": {
      "episode_length": "medium",
      "web_search": true
    }
  }'
```

Only `prompt` is required. Optional fields:
- `host_ids` — Override podcast-level hosts for this episode (short IDs)
- `source_ids` — Attach sources as research context (UUIDs)
- `title` — Override the auto-generated title
- `options.episode_length` — `short` (5-7 min), `medium` (8-12 min), `long` (16-20 min)
- `options.web_search` — Enable web research (default `true`)

**Publish an episode:**

```bash
# Publish immediately
curl -X POST https://api.jellypod.com/v1/episodes/{episode_id}/publish \
  -H "Authorization: Bearer sk_live_..."

# Schedule for later
curl -X POST https://api.jellypod.com/v1/episodes/{episode_id}/publish \
  -H "Authorization: Bearer sk_live_..." \
  -H "Content-Type: application/json" \
  -d '{"scheduled_time": "2026-04-01T12:00:00Z"}'
```

The episode must be in `draft` status with audio generated. Publishing triggers video rendering and distribution. Episode statuses: `generating` > `draft` > `scheduled`/`published` (or `failed` from `generating`).

**Upload cover image** (raw bytes):

```bash
curl -X PUT https://api.jellypod.com/v1/episodes/{episode_id}/image \
  -H "Authorization: Bearer sk_live_..." \
  -H "Content-Type: image/png" \
  --data-binary @cover.png
```

Supported: JPEG, PNG, WebP. Max 10 MB.

### Podcasts

Podcasts are series containers. You can create one manually or use the generate endpoint to create a podcast and batch-generate episodes in one shot.

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/podcasts` | List podcasts (paginated) |
| `POST` | `/podcasts` | Create a podcast (metadata only) |
| `GET` | `/podcasts/{podcast_id}` | Get a podcast (includes episode IDs) |
| `PATCH` | `/podcasts/{podcast_id}` | Update a podcast (partial) |
| `DELETE` | `/podcasts/{podcast_id}` | Delete podcast + all episodes (irreversible) |
| `PUT` | `/podcasts/{podcast_id}/image` | Upload cover image |
| `POST` | `/podcasts/generate` | Generate a podcast with episodes (async — `202`) |

Every organization starts with a default podcast called "My First Podcast." You can use it immediately to generate episodes without creating a new podcast first — just grab its ID from `GET /podcasts`.

**Create a podcast:**

```bash
curl -X POST https://api.jellypod.com/v1/podcasts \
  -H "Authorization: Bearer sk_live_..." \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The AI Revolution",
    "description": "A deep dive into how artificial intelligence is transforming industries.",
    "host_ids": ["xK9mQ2pL"],
    "language": "en",
    "show_order": "episodic",
    "show_visibility": "public"
  }'
```

Required: `title`, `host_ids` (at least one). A cover image is auto-generated in the background.

**Generate an entire podcast with episodes:**

```bash
curl -X POST https://api.jellypod.com/v1/podcasts/generate \
  -H "Authorization: Bearer sk_live_..." \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A podcast series exploring the history of computing, from Turing machines to modern AI.",
    "host_ids": ["xK9mQ2pL", "r7T3nW5j"],
    "options": {
      "num_episodes": 4,
      "episode_length": "medium",
      "web_search": true
    }
  }'
```

This is the power endpoint. It creates the podcast, plans episode topics via LLM, and kicks off audio generation for all episodes. The initial response (~5-15 seconds) returns the podcast with LLM-generated titles. Audio generation continues asynchronously (5-30 min total). Poll individual episodes for progress.

You can omit `title` and `description` to have the LLM generate them from your prompt. At least one of `prompt` or `source_ids` is required. Max 8 episodes per batch.

Podcast settings: `show_order` (`episodic` or `serial`), `show_visibility` (`public`, `private`, `unlisted`), `language` (ISO 639-1 code, default `en`).

Each podcast gets an auto-generated website URL (e.g., `https://the-ai-revolution-a1b2c3.jellypod.com`) and RSS feed.

### Account

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/account` | Get org info, credit balance, plan |

Plans: `free`, `starter`, `creator`, `business`, `enterprise`. The response includes your current credit balance.

Note: `audio_url` on episodes requires the `download_audio` entitlement (Starter plan or above). Free plan users get `null` for this field.

---

## Typical Workflow

Here's the standard flow for generating a podcast episode programmatically:

1. **Browse voices** — `GET /voices?language=en&gender=female` to find the right voice
2. **Create hosts** — `POST /hosts` with a name, backstory, and the voice ID
3. **Create a podcast** — `POST /podcasts` with your hosts
4. **Upload sources** (optional) — `POST /sources` with URLs, text, or files, then poll until `completed`
5. **Generate an episode** — `POST /podcasts/{id}/episodes/generate` with a prompt and optional source IDs
6. **Poll for completion** — `GET /episodes/{id}` every 5 seconds until status is `draft`
7. **Publish** — `POST /episodes/{id}/publish`

Every organization starts with two default hosts and a default podcast ("My First Podcast"). Run `GET /hosts` and `GET /podcasts` to see them. If the defaults work for you, skip straight to step 4 (or use `POST /podcasts/generate` to create a new podcast and batch-generate episodes in one call).

## Error Handling

All errors return a consistent structure:

```json
{
  "error": {
    "code": "validation_error",
    "message": "backstory must be at least 10 characters",
    "request_id": "req_abc123",
    "details": [
      {"field": "backstory", "message": "must be at least 10 characters"}
    ]
  }
}
```

Error codes: `bad_request`, `validation_error`, `unauthorized`, `insufficient_credits`, `not_found`, `unprocessable_entity`, `rate_limited`, `concurrent_limit_exceeded`, `internal_error`.

The `details` array is only present for `validation_error` and contains field-level issues.
