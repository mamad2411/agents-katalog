---
name: youtube-info
description: Extract description and captions/transcript from a YouTube video without opening the browser. Use when the user asks what a video is about, wants a summary, or asks about video content. Accepts a YouTube URL (use the URL returned by youtube-search if available) or a plain search query. Never call youtube-search before this — it opens the browser unnecessarily.
metadata:
  openclaw:
    emoji: "📄"
    always: true
---

# YouTube Info

Fetches the description and full transcript (captions) from a YouTube video so the assistant can answer questions about the video's content.

## Input

A YouTube URL, video ID (11-char), or search query (falls back to top search result).

## Output

- Video title, channel, duration
- Full description (inline)
- Transcript saved to a temp file — path returned in result. Use read_file on that path to access transcript content when the user asks about video content, wants a summary, or wants to take notes.
