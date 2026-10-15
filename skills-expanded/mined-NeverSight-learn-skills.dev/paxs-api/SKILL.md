---
name: paxs-api
description: Connect to PAXS AI platform to create meetings, upload recordings, and generate transcriptions and meeting notes. Use this skill when a user wants to transcribe audio, create meeting notes, or interact with the PAXS platform.
---

# PAXS AI Platform Integration

You help users connect to and use the PAXS AI platform for transcription, meeting notes, and meeting management.

## Authentication

PAXS uses OAuth2 with Google login. Before calling any API, check if the user has a valid access token.

### If No Token Exists

1. Generate a state parameter: a random string for CSRF protection
2. Present the user with an authorization link:

```
https://dzd.paxs.ai/api/oauth/provider/authorize?redirect_uri={CALLBACK_URL}&response_type=code&state={STATE}
```

3. After the user clicks and authorizes, they will be redirected to the callback URL with `?code=xxx&state=xxx`
4. Exchange the code for tokens:

```
POST https://dzd.paxs.ai/api/oauth/provider/token
Content-Type: application/json

{
  "grant_type": "authorization_code",
  "code": "<CODE>",
  "redirect_uri": "<CALLBACK_URL>"
}
```

Response:
```json
{
  "access_token": "...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "refresh_token": "...",
  "scope": "session media analysis user:read"
}
```

5. Store the tokens in `.claude/skills/paxs-api/.tokens.json`:

```json
{
  "access_token": "...",
  "refresh_token": "..."
}
```

### Token Storage

- Tokens are stored at `.claude/skills/paxs-api/.tokens.json`
- Always read tokens from this file before making API calls
- After obtaining or refreshing tokens, update this file immediately

### If Token Expired (401 Response)

Refresh the token:

```
POST https://dzd.paxs.ai/api/oauth/provider/token
Content-Type: application/json

{
  "grant_type": "refresh_token",
  "refresh_token": "<REFRESH_TOKEN>"
}
```

The response returns new access_token and refresh_token. Always store the latest tokens.

### Token Lifetime

- Access token: 1 hour
- Refresh token: 30 days

## Supported File Formats

**Audio:** MP3, WAV, FLAC, MPA, AAC, Opus, M4A
**Video:** MPEG, MP4, FLV, WebM, WMV, 3GP

Before uploading, validate the file extension. Reject unsupported formats with a clear error message listing the accepted formats above.

## API Reference

All API calls require the header: `Authorization: Bearer <ACCESS_TOKEN>`

Base URL: `https://dzd.paxs.ai` (hardcoded for local development)

### Get Current User

```
GET /api/users/me
```

Use this to verify the token works and get the user's profile.

### Create a Meeting

```
POST /api/sessions
Content-Type: application/json

{
  "title": "Meeting title",
  "description": "Optional description",
  "attendees": [
    {"email": "user@example.com", "displayName": "User Name", "role": "participant", "source": "manual"},
    {"email": "other@example.com", "displayName": "Other Person", "role": "participant", "source": "manual"}
  ]
}
```

**Attendee fields:**

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `email` | string | **Yes** | — | Attendee email (cannot be empty) |
| `displayName` | string | **Yes** | — | Attendee display name (cannot be empty) |
| `role` | string | No | `"Unknown"` | Attendee role |
| `source` | string | No | `"manual"` | Source: `"manual"`, `"event"`, or `"zoom_participant"` |

**Important:** `attendees` is required when creating a meeting. The user must provide at least the attendee list. If the user does not provide attendees, ask them before proceeding.

Returns the created meeting with an `id`.

### Upload a Recording

```
POST /api/recordings?session_id={SESSION_ID}
Content-Type: multipart/form-data

file: <audio/video file>
```

Returns the attachment with an `id`.

**Important:** The `session_id` must be sent as a form field (not a query parameter).

**Constraints:**
- **One recording per meeting** — Each meeting can only have one active recording. Uploading a new recording replaces the existing one.
- **Auto-pipeline** — After a successful upload, the backend automatically triggers the full analysis pipeline: transcription first, then meeting note upon transcription completion. No manual analysis request is needed.
- **MIME type required** — When uploading via curl, specify the correct MIME type (e.g., `file=@recording.wav;type=audio/wav`). Without it, the server rejects the file.
- If the user provides multiple audio files, create a separate meeting for each file.

### Request Analysis

```
POST /api/analysis/request
Content-Type: application/json

{
  "session_id": "<SESSION_ID>",
  "attachment_id": "<ATTACHMENT_ID>",
  "analysis_types": ["transcription", "meeting note"],
  "instruction": "Generate a detailed meeting summary",
  "meeting_type": "group"
}
```

Available analysis types:
- `transcription` — Speech-to-text
- `meeting note` — Meeting summary (requires `instruction`)
- `key_points` — Extract key discussion points
- `sentiment` — Sentiment analysis

Meeting types: `group`, `team`, `department`, `cross_functional`, `organization`, `company`

Note: If requesting `meeting note`, the `instruction` field is required.

**Dependency handling**: The backend automatically resolves dependencies between analysis types. For example, passing `["transcription", "meeting note"]` in a single request will automatically complete transcription first, then generate the meeting note. No need to make separate requests or wait between them.

### Get Recording Analysis

```
GET /api/recordings/{RECORDING_ID}/analysis?session_id={SESSION_ID}
```

Returns all analysis reports for a recording. Each report has a `status` field:
- `pending` — Not yet started
- `processing` — In progress
- `completed` — Done, results available
- `failed` — Analysis failed

Optional query parameters:
- `analysis_type` — Filter by specific type (e.g., `transcription`, `meeting note`)

### Polling Strategy

Analysis is asynchronous. After uploading a recording, poll this endpoint:

1. Wait 5 seconds before the first poll
2. Poll every 5 seconds: `GET /api/recordings/{RECORDING_ID}/analysis?session_id={SESSION_ID}`
3. Check the `status` of each analysis type in the response
4. Stop when transcription status is `completed` or `failed`
5. Timeout after 5 minutes (60 polls)

### List meeting

```
GET /api/sessions?page=1&page_size=20
```

### Get meeting Details

```
GET /api/sessions/{SESSION_ID}
```

## One-Shot Mode

When a user provides audio file(s), automatically handle the entire pipeline. The user must provide:
- **Audio file(s)** — local path or URL
- **Attendees** — list of participants with at least `email` and `displayName`

If attendees are not provided, ask the user before proceeding.

### Single File

1. Validate file format (must be a supported audio/video format)
2. Load tokens from `.claude/skills/paxs-api/.tokens.json` (run OAuth if missing)
3. Create a meeting with the filename as title and the provided attendees
4. Upload the recording (backend auto-triggers transcription → meeting note pipeline)
5. Poll analysis status every 5 seconds via `GET /api/recordings/{RECORDING_ID}/analysis?session_id={SESSION_ID}`
6. If transcription fails, retry upload up to 3 times. After 3 failures, notify the user.
7. Once completed, return the results to the user

### Multiple Files

Each file gets its own meeting (one recording per meeting). Process sequentially:

1. Validate all file formats first — reject any unsupported files before starting
2. For each file, repeat the single file flow (steps 2-7)
3. Present results grouped by file

## Workflow

When a user wants to transcribe or analyze a meeting recording:

1. **Load tokens** — Read `.claude/skills/paxs-api/.tokens.json` for stored credentials
2. **Authenticate** — If no tokens, run the OAuth flow via `oauth_callback_server.py`; if token expired (401), refresh it
3. **Collect inputs** — Ensure the user has provided: audio file + attendees list (ask if missing)
4. **Validate file** — Check the file extension is a supported format before proceeding
5. **Create meeting** — `POST /api/sessions` with title and attendees (attendees required)
6. **Upload recording** — `POST /api/recordings` with the audio file as multipart form data (include `session_id` as form field and correct MIME type)
7. **Monitor** — The backend auto-triggers: transcription → meeting note. Poll via `GET /api/recordings/{RECORDING_ID}/analysis?session_id={SESSION_ID}` every 5 seconds.
8. **Retry on failure** — If transcription fails, retry the upload (max 3 attempts). After 3 failures, notify the user with the error details.

## Error Handling

- `401 Unauthorized` → Token expired, refresh it
- `403 Forbidden` → Insufficient scope or permissions
- `400 Bad Request` → Check request parameters
- `404 Not Found` → Resource does not exist

## Guidelines

- Always read tokens from `.claude/skills/paxs-api/.tokens.json` before making API calls
- When the token expires (401), automatically refresh, update `.tokens.json`, and retry
- Present the authorization link clearly and explain what it does
- Always require attendees when creating a meeting — ask the user if not provided
- After uploading a recording, the backend handles the full pipeline automatically (transcription → meeting note)
- Do not manually call `/api/analysis/request` in the standard flow — only use it for on-demand analysis types like `key_points` or `sentiment`
- Poll every 5 seconds until completed (max 5 minutes)
- On transcription failure, retry upload up to 3 times before notifying the user
- When uploading via curl, always include the correct MIME type for the file
