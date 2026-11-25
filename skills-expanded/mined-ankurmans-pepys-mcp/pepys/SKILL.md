---
name: pepys
description: Use when the user wants to transcribe audio or video, get a speaker-labeled/diarized transcript, generate timed SRT or VTT captions, transcribe a podcast episode or a whole RSS/Apple Podcasts feed, paste a YouTube/Drive/Dropbox link to transcribe, search inside a long transcript, ask a question about a transcript, or check their Pepys credit balance. Trigger phrases include "transcribe this", "transcribe this podcast", "get captions for this video", "diarize this recording", "what did they say about X in this transcript", "export this as SRT/VTT".
author: Pepys
version: 1.0.0
---

# Pepys

Pepys (https://pepys.co) turns audio and video into accurate, speaker-labeled, timestamped
transcripts. It never trains on your audio. Usage bills to the connected account's Pepys
credits (1 credit = 1 minute; the free tier includes 60 minutes).

## Connecting

This plugin bundles the `pepys` MCP server (`.mcp.json`, `https://pepys.co/api/mcp`). The
first time a tool is called, Claude Code opens an OAuth sign-in to the user's Pepys account –
no API key needed. If the user doesn't have a Pepys account yet, signing in also creates one.

## What you can do

- **Transcribe** a file, a pasted link (YouTube, a podcast episode or RSS feed, a Google
  Drive/Dropbox share), or a local file the agent is holding.
- **Diarize** (label who said what), **summarize**, **generate chapters**, or **translate**
  a transcript – pass the corresponding option on `transcribe`. Diarization and other advanced
  options require an account entitlement; a non-entitled account gets a clear message rather
  than a silent failure.
- **Batch-transcribe** an entire podcast feed, or just its latest N episodes.
- **Export** a finished transcript as SRT, VTT, TXT, Markdown, or JSON, with correct caption
  timing.
- **Search** inside a long transcript for a phrase without loading the whole thing into
  context, or **ask a question** about it and get back only citation-backed, verified claims.
- **List** recent jobs or podcast-feed episodes, and **check the credit balance** before
  starting a large batch.

Always poll `get_transcription` after starting a job – pass `wait_ms: 25000` for short clips so
it comes back in one call instead of a manual polling loop.

## Example prompts

- "Transcribe this podcast episode and give me a summary: https://feeds.example.com/show.rss"
- "Transcribe this YouTube video with speaker labels: https://youtube.com/watch?v=..."
- "In my last transcript, find every place someone mentions pricing and give me the exact timestamps."
- "Export my most recent transcription as an SRT file."
- "How much Pepys credit do I have left?"

## Notes

- Read-only tools (`get_transcription`, `list_transcriptions`, `list_podcast_episodes`,
  `export_transcript`, `search_transcript`, `ask_transcription`, `get_credit_balance`) never
  spend credits or mutate account data.
- `transcribe`, `upload_file`, and `transcribe_podcast_feed` create new jobs/objects and may
  spend credits; none of them delete or overwrite anything.
- The Pepys MCP server does not initiate purchases or link to checkout – it only reports
  balance and entitlement state.
