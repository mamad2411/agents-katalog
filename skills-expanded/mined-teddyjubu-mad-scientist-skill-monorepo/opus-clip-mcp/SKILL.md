---

name: opus-clip-mcp
description: opus-clip-mcp lets the user create short-form video clips from longer video content using an Opus-style clipping workflow, helping them identify strong moments, cut usable segments, and prepare social-ready clips that are better suited for platforms like TikTok, Instagram Reels, and YouTube Shorts than the original long-form format.

---
Send YouTube videos to OpusClip for automated video clipping via the Zapier MCP integration.

## What This Skill Does

This skill opus-clip-mcp lets the user create short-form video clips from longer video content using an Opus-style clipping workflow, helping them identify strong moments, cut usable segments, and prepare social-ready clips that are better suited for platforms like TikTok, Instagram Reels, and YouTube Shorts than the original long-form format.

## Quick Start

To clip a YouTube video, use the `scripts/clip_video.sh` script:

```bash
./scripts/clip_video.sh <youtube_url>
```

Or make the MCP call directly:

```bash
curl -s -N -X POST "https://mcp.zapier.com/api/v1/connect" \
  -H "Authorization: Bearer ODAzNmQ3ZWYtMzI1YS00YTNhLTk0OTktMTM1NDUyZGQwM2Q0OktYVzFDV3BoaitFcEhER2gxN3FYSHdLMVIyWHlNM3d2a1J5YlNvRHNId3M9" \
  -H "Accept: application/json, text/event-stream" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "opusclip_clip_your_video",
      "arguments": {
        "instructions": "Create clipped segments from this YouTube video",
        "videoUrl": "YOUTUBE_URL_HERE",
        "output_hint": "return the project ID, status, and any available clip URLs"
      }
    },
    "id": 1
  }'
```

## Workflow

1. **Extract the YouTube URL** from the user's message
2. **Run the script** or call the MCP endpoint directly
3. **Parse the response** to get:
   - `projectId` - The OpusClip project ID for tracking
   - `status` - Job status (SUCCESS, PENDING, etc.)
   - `feedbackUrl` - Link to view execution details
4. **Notify the user** with project details and confirmation

## Response Format

The MCP returns an SSE (Server-Sent Event) response with JSON inside:

```json
{
  "result": {
    "content": [{
      "type": "text",
      "text": "{\"results\":{\"projectId\":\"Pxxxx\",\"status\":null}}"
    }]
  }
}
```

Extract `projectId` and report it to the user. Processing may take time; clips will be available in the OpusClip dashboard once complete.

## Available MCP Tools

| Tool | Purpose |
|------|---------|
| `opusclip_clip_your_video` | Create project to generate short clips from long videos |
| `opusclip_get_clips` | Retrieve clips from an existing project |
| `opusclip_get_transcript_of_project` | Get full transcript of a project |
| `opusclip_get_transcript_of_clips` | Get transcript for specific clips |
| `opusclip_add_captions_to_your_video` | Generate captions for a video |
| `opusclip_transcribe_your_video` | Get full transcript (without clipping) |

## Notes

- Load the MCP token from the environment or a local `.env`; never hardcode Zapier-generated tokens in committed scripts.
- Processing time varies based on video length
- Results appear in the OpusClip dashboard, not immediately in the response
- The `projectId` can be used to check status later via other MCP tools
