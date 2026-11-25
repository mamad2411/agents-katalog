---
name: meeting-live-questions
description: Generate sharp, well-timed questions from a live meeting transcript while a call is running. Used by the vexa-live webhook route, or when the user asks mid-call "what should I ask?".
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [meetings, calls, questions, realtime]
    related_skills: [meeting-bot-ops, meeting-briefing, meeting-notes]
---

# Live Meeting Questions

Fresh transcript from a call Hermes is attending has arrived. Give the user
the questions worth asking *now*, before the moment passes. The user reads
these on their phone mid-conversation: one glance, then speak.

## Input

From the webhook payload (when triggered by the `vexa-live` route):

- `meeting_id`, `platform`, `bot_name`
- `new_text` — transcript since the last check
- `meeting_file` — running transcript Markdown
  (`~/.hermes/data/vexa-transcripts/<meeting_id>.md`)

When invoked by hand (no payload), or when `meeting_file` is missing: get
the meeting with `mcp__vexa__get_bot_status`, then
`mcp__vexa__get_meeting_transcript`; treat the last ~3 minutes as `new_text`.

## Procedure (keep it fast — at most 3 tool calls)

1. **Triage the delta.** Greetings, audio checks, logistics, small talk, or
   under ~2 sentences of substance → reply exactly `NO_QUESTIONS`. Stop.
2. **Load context only if it changes the questions:**
   - The running transcript (`meeting_file`) for what was said earlier.
   - A briefing for this meeting, if one exists: the meeting's `briefing`
     metadata, or the newest file in `~/.hermes/data/meeting-briefings/`
     whose name matches a speaker or company. It holds the user's goal for
     the call and the counterpart's background.
   - Questions already delivered: your earlier turns in this webhook session.
     Never repeat or rephrase one already sent.
3. **Find the gaps.** Ranked, highest value first:
   1. A number, date, owner or scope stated vaguely ("soon", "a few", "the
      team") — pin it down.
   2. A decision being skipped or assumed — make it explicit.
   3. A contradiction with something said earlier or in the briefing.
   4. A commitment with no owner or deadline.
   5. A risk, dependency or objection mentioned in passing and dropped.
   6. Something that moves the user's goal for the call forward (from the
      briefing: budget, timeline, decision-maker, next step).
4. **Write 1–3 questions.** Fewer if the last delivery already had some and
   the topic hasn't changed. One strong question beats three fine ones.

## Question quality bar

- Speakable as-is, under ~25 words, in the **language the meeting is held
  in** (Spanish call → Spanish question).
- Anchored to what was just said: reuse their words ("You said 'next
  quarter' — is that a hard date for go-live?").
- Open or pinning, never yes/no fishing, never leading or confrontational.
- Not answerable by a web search; not already answered in the transcript.
- Speaker named when the transcript gives a name. Empty speaker → "they".
- Misheard-looking names/numbers: ask about the thing, don't quote the
  garbled value.

## Output

Plain text, no headers. Each question on its own line, then a short
reason after ` — ` so the user knows why now:

```
Q: <question> — <why, ≤8 words>
Q: <question> — <why, ≤8 words>
```

Or exactly `NO_QUESTIONS`. If you cannot tell what is being discussed, one
line saying so. Your reply is the delivered message: no preamble, no
sign-off. Never call `mcp__vexa__speak_in_meeting`.
