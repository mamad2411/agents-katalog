---
name: youtube-research
description: Research topics across YouTube videos efficiently using Scribefy's MCP tools — search for candidates, vet them with free metadata before spending credits, extract transcripts selectively, and synthesize timestamped answers. Use when researching a topic on YouTube, summarizing or comparing videos, pulling quotes or data from video content, or building anything on top of video transcripts.
license: MIT
---

# YouTube Research with Scribefy

You have four Scribefy tools. Three are free; one costs credits. The core
discipline of this skill: **spend free calls to make every paid call count.**

| Tool | Cost | Use for |
|---|---|---|
| `search_videos` | Free | Finding candidate videos by query |
| `get_video_metadata` | Free | Vetting a candidate before extraction |
| `get_related_videos` | Free | Expanding from a good seed video |
| `extract_transcript` | 1–8 credits by video length — **cached extracts are FREE** | The actual transcript |

## The workflow

### 1. Search wide (free)

Run `search_videos` with 2–3 different phrasings of the question — YouTube
search rewards different keyword angles ("PO3 trading strategy" vs "power of
three ICT explained"). Collect ~5–10 candidates.

### 2. Vet before you spend (free)

Call `get_video_metadata` on the shortlist. Decide using:

- **Duration** — extraction cost scales with length (1 credit for short
  videos up to 8 for very long ones). A focused 12-minute video usually beats
  a 3-hour podcast that mentions the topic once.
- **Caption tracks** — the metadata lists every track and marks it
  ✏ authored or ⚙ auto-generated. Authored captions give cleaner text.
  **No caption tracks listed → do not attempt extraction** (it will fail
  with `NO_CAPTIONS`); pick another candidate.
- **Recency and channel** — for fast-moving topics, check the upload date
  before trusting the content.

### 3. Extract selectively (paid — usually 1–2 videos, not 10)

Call `extract_transcript` on the best 1–2 candidates first. Read them. Only
extract more if the question is still open.

- **Cached transcripts cost 0 credits** — popular videos are often already
  cached, and re-extracting the same video is always free. Never hesitate to
  re-pull a video you've extracted before.
- For non-English videos, pass the language code of the caption track you
  saw in metadata. Extract in the original language and translate in-chat —
  that preserves nuance better than hunting for a translated track.

### 4. Synthesize with timestamps

Transcripts arrive as timestamped segments. When answering, cite moments as
`[mm:ss]` next to claims so the user can jump straight to them in the video.
For multi-video research, attribute each point to its video title.

## Multi-video research pattern

For "what do people say about X" questions:

1. `search_videos` (2–3 phrasings) → candidate pool
2. `get_video_metadata` on each → build a quick table: title / channel /
   duration / captions / date
3. Pick the 2–3 strongest, state the expected credit cost, extract
4. Synthesize a comparison: agreements, contradictions, unique points —
   each cited with video + timestamp

To go deeper from one good video, walk the recommendation graph with
`get_related_videos` (free) instead of re-searching.

## Error handling

| Error | Meaning | Do |
|---|---|---|
| `NO_CAPTIONS` | Video has no caption tracks (or YouTube serves none to extractors — common for music videos) | Skip it; pick the next candidate. No credits were charged. |
| Video unavailable | Private, removed, region-locked, or a mistyped ID | Verify the URL; pick another candidate |
| Insufficient credits | Balance too low for this video's length | Tell the user the cost vs balance; suggest a shorter video or scribefy.app/pricing |

## Cost etiquette

Before extracting anything long (cost ≥ 4), tell the user the credit cost
from the metadata and confirm. Never bulk-extract a whole search result list
— vet, rank, extract the minimum, expand only if needed.
