---
name: youtube-transcripts
description: 'Read and search YouTube videos through VidWords. Use when the user supplies a YouTube URL, a bare 11-character video id, a youtu.be or Shorts link, or a channel handle, and wants any of: the transcript or subtitles (TXT/SRT/VTT), what a video says about a topic, a quote with a citable timestamp, only the words spoken between two timecodes such as "10:20 to 11:00", or the same question answered across many videos in a channel or playlist.'
---

# Reading YouTube videos

A model cannot watch a video, but it can read a transcript carrying timestamps it
is able to cite. So the useful unit here is not "a transcript" — it is a grounded
answer with a link the user can click and check.

Prefer returning **a quote plus its deep link** over a wall of text.

## Endpoint

Hosted MCP server, no integration code:

```
POST https://vidwords.com/mcp
Authorization: Basic <api-token>
```

`Basic`, **not** `Bearer`, and the token is not a base64 pair — send it verbatim.
Create one on https://vidwords.com/api-keys (the value is shown once, at creation).
Free tier included; the account's email must be verified or every call returns 403.
Clients that support MCP OAuth (Claude, ChatGPT, Cursor, VS Code, Codex) need no
token at all: give them the URL and the user signs in.

There is a plain REST equivalent at `POST https://vidwords.com/api/transcripts`
if MCP is not available to you — see https://vidwords.com/api-docs.

## Choosing a tool

**Check the Library first.** `search_library` searches every transcript the account
has already saved, and `list_library` lists those videos — both free. If the user
asks about something they watched or researched before, the answer is often
already there, and fetching the video again would only repeat work.

```json
{ "query": "pricing model" }
```

**`search_transcript` is the default for a video's own words.** Reach for it whenever the question is
"what does this video say about X".

```json
{ "video": "dQw4w9WgXcQ", "query": "pricing model" }
```

It returns the matching moments, each with `timestamp`, `startSeconds` and a
`youtube.com/watch?v=…&t=…s` url. Cite those urls.

`get_transcript` returns the whole text and costs the same — one Cloud Request
for a video the account does not have yet, nothing for one it does. A two-hour interview
is ~20,000 words of which perhaps 300 answer the question, and the other 19,700
compete for your attention and degrade the answer. Use it only when the full text
is genuinely the deliverable: an export, a diff, a corpus.

```json
{ "videos": ["dQw4w9WgXcQ", "9bZkp7q19f0"], "lang": "en" }
```

## Ask for a span, not a whole video

Both tools take optional `from`/`to` timecodes. Accepted forms: seconds (`615`),
`m:ss` (`10:20`), `h:mm:ss` (`1:02:13`) — the same formats the tools print back,
so a timestamp from one answer can be pasted into the next question.

```json
{ "video": "dQw4w9WgXcQ", "query": "revenue", "from": "10:20", "to": "11:00" }
```

When the user names a time span, **pass it** rather than fetching everything and
filtering yourself. It costs the same either way, but it keeps your context clear
and the reply focused.

## Page a long transcript

When you do need the whole text of a long video, pass `maxChars`. A result cut
short has `truncated: true` and `nextFrom` (seconds) — send that back as `from`
for the next page. Pages after the first are re-reads of a video the account
already has, so they are free; each result's `charged` field says so.

## Which language you got

A caption track's language is not necessarily the one spoken: an auto-generated
track transcribes the speech, an uploaded one may be a translation. Read
`selectionReason` before telling the user what language a video is in:

- `spoken_language` or `requested` — the track is what it says.
- `caption_fallback` — **no track is known to match the speech**; English was
  picked for readability. Do not report its `language` as the video's language.
- `spokenLanguage` is the spoken language when known, `null` when not.

To get the words actually spoken when every caption is a translation, pass
`source: "audio"` to `get_transcript`. It is paid (AI Units per minute of video,
plus the Cloud Request) and passing it is the user's consent, so ask first.
`list_languages` shows a video's tracks for free when we already hold them.

A timecode that cannot be parsed is refused **before** anything is fetched, so a
typo costs nothing. It never silently widens to the whole video.

## One call across a channel

`search_transcript` accepts a list of up to 25 videos. Use it to answer "what has
this channel said about X" without a round trip per video:

```json
{ "video": ["ID_1", "ID_2", "ID_3"], "query": "acquisition" }
```

Get the ids from `list_channel_videos` first (1 Cloud Request; needs a Starter
plan or better). Each new video in the list bills the usual 1 Cloud Request. If one video is
unavailable it comes back as its own row with an `error` — the rest were fetched
and charged for, so read them rather than discarding the call.

## Returning to an existing AI Watch analysis

For “show my last analysis”, call `get_analysis` without an `analysisId`. It opens
this account's latest finished analysis for free. Use `list_analyses` to find an
older result or filter by video; its entries include IDs, status and result links.
`list_library` also returns `latestAnalysis.analysisId` for clients with an older
cached tool list. Retrieve the result before offering to run a new paid analysis.

The result contains complete JSON text and `structuredContent`. Compatible MCP
Apps hosts render an interactive card with **Show full analysis**. If the host
cannot render the card, present the requested sections and timestamp links from
the text result; do not claim the analysis is unavailable.

## When the question is about something SHOWN, not said

`analyze_video` reads the video's **frames** — slides, charts, on-screen text,
demonstrations — and verifies every citation against stored evidence. Then
`get_analysis` reads the result and `ask_video` asks a question against it,
returning either an answer with verified citations or an explicit statement that
the evidence is insufficient. It will refuse rather than guess; treat a refusal as
the correct answer, not a failure to retry.

A fresh analysis spends 1 Cloud Request (for the transcript) plus AI Units per
minute of video — 2.8 for Quick, 4 for a standard run, 30 for Deep. Deep runs on
any plan with enough AI Units. Before a long video or a Deep run, call
`analyze_video` with `estimateOnly: true`: free, it starts nothing, and returns
`cloudRequests`, `aiUnits` and `maxAiUnits`. A video with no captions is still
analysed — from its picture and soundtrack, at no extra charge. Only pass
`transcribeAudio: true` when the user wants a word-for-word transcript as well:
that adds 3 AI Units per minute of video, and the estimate then reports
`audioTranscription: "unknown"` (captions not held yet) with `maxAiUnits`
including the transcription. Budget with `maxAiUnits` and tell the user before
you start, as an estimate rather than a cap: the transcription charge follows
the transcribed audio, which can run a minute past the listed duration. Analysis is asynchronous: start the job, then call
`get_analysis` with `waitSeconds` (up to 25) so the server holds the call until it
is ready, instead of polling in a tight loop.

## Costs, so you can budget

| call | cost |
|---|---|
| `search_transcript`, `get_transcript` | 1 Cloud Request per video the account does not have yet; free for one it does |
| `search_library`, `list_library`, `list_analyses`, `list_languages`, `list_watchlists`, `watchlist_activity`, `account`, `get_analysis` | free |
| `list_channel_videos` | 1 Cloud Request |
| `analyze_video` | 1 Cloud Request + AI Units per minute: Quick 2.8, Standard 4, Deep 30 (a captionless video costs nothing extra; `transcribeAudio: true` adds 3 per minute — see `maxAiUnits`); starting the same analysis again on the account (same video, mode and range) and `estimateOnly` are free |
| `ask_video` | 6 AI Units per question |
| audio transcription (`transcribeAudio`, `source: "audio"`) | 3 AI Units per minute of video, plus the Cloud Request |

Failed lookups — no captions, invalid id, a language the video lacks — are free.
Call `account` to read the plan and both balances before a large job.

## Errors worth acting on

Errors arrive as readable JSON inside a successful tool result, so you can
recover instead of retrying blindly:

- `insufficient_credits` — carries `needed` and `available`. Tell the user the
  shortfall; do not retry the same call.
- `invalid_timecode` — carries `field` and `value`. Fix the timecode and retry.
- `invalid_id` — the string was not a YouTube URL or id. Re-read the user's input.
- `language_unavailable` — the video has no track in the `lang` you asked for. It
  carries `availableLanguages`; pick one, or offer `source: "audio"` if none is
  auto-generated. Nothing was charged.
- `audio_not_allowed` — transcribing audio needs a paid plan or purchased AI
  Units. Tell the user; do not retry.
- `plan_required` — the account's plan does not include that call.
- `email_unverified` (HTTP 403) — the account exists but has not confirmed its
  email. Nothing can be spent until it does; say so rather than retrying.

## Limits, stated plainly

- Public videos. A video with no captions can be transcribed from its audio
  (`transcribeAudio: true`, 3 AI Units per minute) on a paid plan or with
  purchased AI Units; without that, `get_transcript` reports no transcript —
  but `analyze_video` can still analyse it from its picture and soundtrack.
- Max 25 videos per call.
- Rate limit per minute by plan: Free 60, Starter 200, Pro 500, Team 1,000.
- Rows are the creator's words. Quoting and analysis are normal use; republishing
  a whole transcript as your own content is not.
- Not affiliated with YouTube or Google.
