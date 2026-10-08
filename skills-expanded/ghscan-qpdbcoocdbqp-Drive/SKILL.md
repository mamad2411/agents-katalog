---
name: find-all-in-episode
description: "Locates and returns the latest episode title, episode number, and summary for the All-In podcast using Hermes browser tools only."
version: 1.2.0
author: User
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Podcast, Latest, Episode, Audio, Search]
    related_tools:
      - browser_navigate
      - browser_snapshot
      - browser_cdp
      - browser_tools
      - web_extract
constraints:
  - "Do NOT use python or generate custom extraction scripts for parsing."
  - "All extraction MUST be completed directly using Hermes browser_tools and DOM inspection."
  - "Only retrieve the most recent episode information."
  - "Ignore older episodes and unrelated page content."
---

# 🎧 Podcast Episode Finder

This skill retrieves the latest episode metadata from the All-In Podcast episodes archive.

## Usage

Run `find-all-in-episode` to automatically fetch:

- Latest episode title
- Episode number
- Short summary / description
- Episode URL (if available)

## Workflow

### 1. Navigate

Use:

- `browser_navigate`

Open:

`https://allin.com/episodes`

---

### 2. Extract Latest Episode (Browser Tools Only)

Use Hermes-native browser inspection tools only:

- `browser_snapshot`
- `browser_tools`
- `browser_cdp`
- `web_extract`

Requirements:

- Identify the FIRST / MOST RECENT episode card or listing on the page.
- Extract only:
  - Episode number
  - Episode title
  - Short description / summary
  - Link URL (if present)

Do NOT:

- Iterate through older episodes
- Use Python
- Inject custom scraping frameworks
- Rewrite extraction logic in external scripts

Preferred strategy:

1. Capture page structure with `browser_snapshot`
2. Locate the first episode container
3. Read DOM text directly using `browser_tools`
4. Return normalized structured output

---

### 3. Output Format

Return results in this structure:

```json
{
  "podcast": "All-In",
  "episode_number": "E###",
  "title": "Episode title",
  "summary": "Brief episode summary",
  "url": "https://..."
}
````

If extraction fails, return:

```json
{
  "error": "Unable to locate latest episode information."
}
```
