---
name: youtube-search
description: Search YouTube and open the first matching video in the browser. Returns the video title and URL. Use when the user asks to play, watch, find, show, or search for something on YouTube. Do NOT use when the user only wants to know what a video is about — use youtube-info directly for that instead.
metadata:
  openclaw:
    emoji: "▶️"
    always: true
---

# YouTube Search

Searches YouTube for the user's query and opens the best matching video directly in the browser.

## Behavior

- Receives the user's search query as input
- Finds the top result on YouTube
- Opens it in the default browser
- Reports back the video title/URL

## No API key required — uses public YouTube search.
