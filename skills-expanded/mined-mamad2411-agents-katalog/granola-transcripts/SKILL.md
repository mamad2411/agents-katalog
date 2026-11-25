---
name: granola-transcripts
description: Pull exact quotes and verbatim passages from Granola meeting transcripts, handle long transcripts, and fall back cleanly when the plan has no transcript access. Use when the user wants word-for-word content — "what exactly did they say", quotes for a doc, or verification of a claim from notes.
---

# Granola transcripts

`get_meeting_transcript` returns the raw transcript for one meeting id.
Paid plans only. Read [granola] first for auth and tool basics.

## Getting to the right transcript

1. Resolve the meeting id first (`list_meetings`, or the id already in hand
   from `get_meetings`). Never call the transcript tool without a confirmed
   id — transcripts are large and the rate budget is ~100 req/min.
2. `get_meeting_transcript` with that id.

## Quoting

- Quote verbatim, attribute to the speaker as labeled in the transcript, and
  include the meeting title + date with every quote.
- Transcription errors happen: if a quote will be used somewhere that
  matters, show it with surrounding context so the user can sanity-check.
- When the ask is "find where we said X", prefer `query_granola_meetings`
  to locate the meeting semantically, then pull that one transcript for the
  exact wording — cheaper than fetching several transcripts.

## Long transcripts

Work in one pass: extract the passages relevant to the ask (with speaker and
rough position), then answer from those. Do not re-fetch the same transcript
repeatedly; reuse what you already pulled.

## No transcript access

If the call is rejected (free plan or admin scope), say transcripts need a
paid Granola plan, then answer from `get_meetings` summarized + private
notes and label the result as notes-based, not verbatim.
