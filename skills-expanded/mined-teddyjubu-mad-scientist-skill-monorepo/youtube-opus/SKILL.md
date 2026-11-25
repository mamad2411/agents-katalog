---

name: youtube-opus-skill
description: youtube-opus-skill lets the user take YouTube content and turn it into high-value short-form opportunities by extracting strong moments, shaping clips, and preparing content for wider distribution, making it useful when they want to squeeze more reach, engagement, and downstream content assets out of a longer YouTube video.

---
## What This Skill Does

This skill youtube-opus-skill lets the user take YouTube content and turn it into high-value short-form opportunities by extracting strong moments, shaping clips, and preparing content for wider distribution, making it useful when they want to squeeze more reach, engagement, and downstream content assets out of a longer YouTube video.

## Overview
When Charles provides a YouTube video URL with the phrase "Opus clip skool" (or similar), extract the URL and send it to OpusClip via Zapier MCP to create short viral clips. Return the OpusClip URL where the clips can be accessed.

## Trigger Phrases
- "Opus clip skool"
- "use Opus clip" 
- "process with Opus"
- "generate clips from this YouTube"
- "send to OpusClip"
- "clip this YouTube"
- "make viral clips from this"

## MCP Configuration
- **Endpoint**: https://mcp.zapier.com/api/v1/connect
- **Token**: ODAzNmQ3ZWYtMzI1YS00YTNhLTk0OTktMTM1NDUyZGQwM2Q0OktYVzFDV3BoaitFcEhER2gxN3FYSHdLMVIyWHlNM3d2a1J5YlNvRHNId3M9

## Workflow

1. **Extract YouTube URL** from user message
2. **Run**: `node scripts/send_to_opusclip.js "<YOUTUBE_URL>"`
3. **Parse result** for clip URL
4. **Reply** with the OpusClip URL

## Script Execution

```bash
node scripts/send_to_opusclip.js "https://youtube.com/watch?v=ABC123"
```

**Output format**:
```json
{
  "success": true,
  "videoUrl": "https://youtube.com/watch?v=ABC123",
  "clipUrl": "https://opusclip.com/clips/project-xyz123",
  "status": "processing"
}
```

## Completion Reply

> "Done! 🎬 Sent to OpusClip.
> 
> **Original**: {videoUrl}
> **Clips**: {clipUrl}
> 
> Your viral clips are being generated. Check the link above for the results."

## Error Handling

If MCP connection fails:
> "⚠️ Could not connect to OpusClip MCP. Check your Zapier connection and try again."

If URL extraction fails:
> "⚠️ I didn't find a valid YouTube URL. Please include the full YouTube link."
