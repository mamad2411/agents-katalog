---

name: supadata-transcript
description: supadata-transcript lets the user pull transcript data from supported media sources so they can read, analyze, quote, summarize, repurpose, or mine spoken content without manually transcribing it, which is especially useful for turning videos, interviews, and recorded conversations into searchable text that can feed content creation or research workflows.
version: 1.0.0
maintainer: James (OpenClaw agent)
requires:
  tools:
    - curl
  env:
    - SUPADATA_API_KEY

---
Get transcripts from videos on YouTube, TikTok, Twitter, Instagram, Facebook, or from direct file URLs using the Supadata API.

## What This Skill Does

This skill supadata-transcript lets the user pull transcript data from supported media sources so they can read, analyze, quote, summarize, repurpose, or mine spoken content without manually transcribing it, which is especially useful for turning videos, interviews, and recorded conversations into searchable text that can feed content creation or research workflows.

## Configuration

**API Key**: `sd_5a855a75e509786200517d1f50dd40e7` (stored in `.secrets/supadata.env`)

**Base URL**: `https://api.supadata.ai/v1`

**Authentication**: Include `x-api-key` header with every request.

## Workflow

### Step 1: Transcribe a video

Use the provided script to fetch a transcript:

```bash
bash ~/.openclaw/workspace/skills/supadata-transcript/scripts/transcribe.sh "https://youtu.be/VIDEO_ID"
```

**Optional flags:**
- `--lang en` — Specify language (ISO 639-1 code, e.g., `en`, `es`, `zh-TW`)
- `--text` — Return plain text instead of timestamped chunks
- `--mode native` — Only fetch native transcript (no AI generation)
- `--mode generate` — Always generate transcript using AI
- `--mode auto` — Try native first, fallback to AI (default)
- `--chunk-size 1000` — Max characters per chunk (default: 1000, range: 50-10000)

**Examples:**

```bash
# Basic transcription (auto mode, timestamped chunks)
bash ~/.openclaw/workspace/skills/supadata-transcript/scripts/transcribe.sh "https://youtu.be/dQw4w9WgXcQ"

# Plain text transcript in Spanish
bash ~/.openclaw/workspace/skills/supadata-transcript/scripts/transcribe.sh "https://youtu.be/dQw4w9WgXcQ" --lang es --text

# Force AI-generated transcript
bash ~/.openclaw/workspace/skills/supadata-transcript/scripts/transcribe.sh "https://youtu.be/dQw4w9WgXcQ" --mode generate

# Native-only transcript (fails if no native transcript exists)
bash ~/.openclaw/workspace/skills/supadata-transcript/scripts/transcribe.sh "https://youtu.be/dQw4w9WgXcQ" --mode native
```

### Step 2: Handle async jobs

For large videos, the API returns a `jobId` instead of immediate results. The script automatically polls for completion.

**Manual job status check:**

```bash
curl -X GET "https://api.supadata.ai/v1/transcript/JOB_ID" \
  -H "x-api-key: sd_5a855a75e509786200517d1f50dd40e7" \
  -H "Content-Type: application/json"
```

## Supported Platforms

- **YouTube** (youtu.be, youtube.com)
- **TikTok**
- **Twitter/X**
- **Instagram**
- **Facebook**
- **Direct file URLs** (MP3, MP4, WAV, etc.)

## Transcript Modes

| Mode | Behavior |
|------|----------|
| `native` | Only fetch existing platform transcript (fails if unavailable) |
| `auto` | Try native first, fallback to AI generation if unavailable (default) |
| `generate` | Always generate transcript using AI (even if native exists) |

**Note**: For file URLs, mode is always `generate`.

## Response Format

### Timestamped chunks (default)

```json
{
  "content": [
    {
      "text": "Hello everyone...",
      "offset": 0,
      "duration": 1500,
      "lang": "en"
    },
    {
      "text": "Welcome to the video...",
      "offset": 1500,
      "duration": 2000,
      "lang": "en"
    }
  ],
  "lang": "en",
  "availableLangs": ["en", "es", "zh-TW"]
}
```

### Plain text (`--text` flag)

```json
{
  "content": "Hello everyone... Welcome to the video...",
  "lang": "en",
  "availableLangs": ["en", "es", "zh-TW"]
}
```

### Async job response

```json
{
  "jobId": "123e4567-e89b-12d3-a456-426614174000"
}
```

## Error Handling

| Error Code | Description | Fix |
|------------|-------------|-----|
| `invalid-request` | Malformed request | Check URL format and parameters |
| `transcript-unavailable` | No transcript available | Try `--mode generate` to create one with AI |
| `not-found` | Video not found | Verify the URL is correct |
| `unauthorized` | Invalid API key | Check `.secrets/supadata.env` |
| `limit-exceeded` | Rate limit or plan limit | Wait or upgrade plan |
| `upgrade-required` | Feature requires paid plan | Upgrade Supadata plan |

## Rate Limits

- Rate limits vary by subscription plan
- When exceeded, API returns `429` status
- Script includes exponential backoff for job polling

## Output

The script saves transcripts to:
- Timestamped: `<video-id>_transcript.json`
- Plain text: `<video-id>_transcript.txt`

Or prints to stdout if no output file is specified.

## Examples

### Example 1: YouTube transcript with timestamps

```bash
bash ~/.openclaw/workspace/skills/supadata-transcript/scripts/transcribe.sh \
  "https://youtu.be/dQw4w9WgXcQ"
```

**Output**: JSON with `offset`, `duration`, and `text` for each segment.

### Example 2: Plain text transcript in Spanish

```bash
bash ~/.openclaw/workspace/skills/supadata-transcript/scripts/transcribe.sh \
  "https://youtu.be/dQw4w9WgXcQ" \
  --lang es \
  --text
```

**Output**: Single string with full transcript in Spanish.

### Example 3: TikTok video transcript

```bash
bash ~/.openclaw/workspace/skills/supadata-transcript/scripts/transcribe.sh \
  "https://www.tiktok.com/@user/video/1234567890"
```

### Example 4: AI-generated transcript from Instagram Reel

```bash
bash ~/.openclaw/workspace/skills/supadata-transcript/scripts/transcribe.sh \
  "https://www.instagram.com/reel/ABC123/" \
  --mode generate
```

## Integration Notes

- Always use `--text` flag when you want a clean transcript for further processing (summaries, analysis, etc.)
- Use timestamped chunks when you need to reference specific moments in the video
- For multi-language videos, check `availableLangs` and request specific language with `--lang`
- The API automatically handles job polling for large videos (no manual intervention needed)

## API Reference

Full API documentation: https://docs.supadata.ai/api-reference/endpoint/transcript/transcript
