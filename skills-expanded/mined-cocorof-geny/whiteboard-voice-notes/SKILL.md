---
name: whiteboard-voice-notes
description: When the user shares a voice recording on the whiteboard, naturally recognize the auto-generated transcript and bring it up in conversation. If the transcript is missing/empty or the user explicitly asks for re-transcription, recover it with the whiteboard_transcribe tool.
allowed_tools:
  - whiteboard_transcribe
  - opsidian_read
  - knowledge_read
execution_mode: inline
examples:
  - "Did you listen to what I just recorded?"
  - "What do you think of this voice memo?"
  - "Transcribe it again."
---

# Whiteboard: Voice Notes — React to voice notes and re-transcribe when needed

Use this skill when the user shares a microphone recording (`microphone_record` capture) or an audio file (`.webm`/`.mp3`/`.m4a`/...).

## ⚠️ Most important: distinguish ambient vs deliberate

You **must check** the `ambient` field of the `[USER_SHARED]` payload (or `share_source == "vtuber_stt_stream"` / `metadata.source == "vtuber_stt_stream"`). The two cases mean completely different things:

### A. `ambient: true` (= speech the STT mode happened to pick up)

- The user did *not* speak directly to you. The mic just overheard a remark nearby.
- It could be the user talking to themselves / a conversation with someone else / singing / TV sound / cursing.
- **Default behavior: stay silent.** Don't respond; just accumulate the spotlight context.
- **Respond only when one of these three holds**:
  1. Your own name was called (the persona name / your nickname).
  2. A clear direct question to you (ends in `?` and points at you).
  3. A clear reaction to your previous statement ("yeah, right", "no, that's not it", etc.).
- If you do need to respond, keep it to **a short 1–2 sentence acknowledgment**. Use an **overheard tone** like "I just heard you say [content]..." / "I heard [X] over there". Never use phrasings like "thanks for sharing" / "the memo you sent me".
- When several ambient items are sitting in the spotlight at the same time within one burst, **look at the whole thing and react just once**. Don't reply to each utterance.

### B. `ambient: false` (= the user shared deliberately)

- The user recorded a memo and sent it (`microphone_record` + Share-with-VTuber), pressed the Share button, or explicitly shared a note.
- React as usual. Tone: "I listened to the memo you just recorded" / "Looking at the [X] you shared…".

## Background knowledge: auto-transcription has already run

The W2 PostCaptureHook automatically invokes Whisper-large-v3 on every `type=audio` capture. The result is placed as a quote block at the very top of the note body:

```
> **Transcript (ko):** 안녕하세요, 오늘 회의에서 이야기 나눈 ...

(original body below)
```

So **in most cases you don't need to call the tool.** The transcript is already in the spotlight or the `[USER_SHARED]` payload.

## Reaction ladder

### Step 1: Is the transcript already in the body?

If the `excerpt` in `[Spotlight Context]` or the `excerpt` in `[USER_SHARED]` starts with `> **Transcript (...)**`:

- Use that content directly to voice your opinion naturally.
- Look at the transcript's language code (`ko` / `en` / `ja` / ...) and respond in a tone that matches.
- **Don't quote the transcript verbatim** — paraphrase, or just the key points.

### Step 2: Is the transcript missing or empty?

If any of the following applies, call `whiteboard_transcribe(capture_id="...")`:

| Situation | Action |
|---|---|
| No transcript in the `excerpt` (hook failed or old capture) | `whiteboard_transcribe(capture_id="...")` |
| Transcript is clearly truncated (e.g. only "..." is visible) | Call it likewise |
| User explicitly requests "transcribe it again", "re-transcribe", "transcribe again", etc. | Call it, reflecting the user's intent (e.g. pinning the language) |
| User specifies a particular language ("in Korean", "in English") | Be explicit, like `whiteboard_transcribe(capture_id="...", language="ko")` |

Get the `capture_id` from the `capture_id` field of the `[USER_SHARED]` payload, or from the identifier of the `[Spotlight Context]` item. You can also call it with `attachment_path`, but `capture_id` is more reliable.

### Step 3: Interpreting the tool result

`whiteboard_transcribe` response:

```json
{
  "text": "...",
  "language": "ko",
  "duration_seconds": 12.3,
  "source": "whisper",
  "attachment_path": "_attachments/voice-2026-05-13.webm"
}
```

React differently depending on the `source` value:

- `"whisper"` + `text` present → normal. Use it naturally as in Step 1.
- `"unavailable"` → the STT service is temporarily down. **Don't suggest retrying**; route around it, e.g. "the transcription server isn't responding for a moment right now — can you say it again in text?".
- `"disabled"` → the host has turned STT off. Explain to the user "voice memos aren't being auto-transcribed today" and prompt for text input.
- `"not_found"` → the capture_id is wrong. Clarify with the user, e.g. "which voice memo do you mean?".

### Step 4: Read if you need more context

There may be separate text in the note body beyond the transcript (e.g. the user added a hand-written note after recording). If needed, check the full body with `opsidian_read(filename="inbox/...")`.

## Example responses

**Good example** (transcript already in spotlight):
> "I listened to the recording — sounds like the meeting got into reprioritizing things. Did you land on a decision about the retry logic?"

**Good example** (user requested re-transcription):
> *(after calling whiteboard_transcribe(capture_id="01HXY...", language="en"))*
> "I re-transcribed it in English: 'We need to ship by Friday and the API rate limit ...' — the deadline part comes through more clearly than the first time I heard it."

**Good example** (service unavailable):
> "I got the voice memo, but the transcription server happens to be unresponsive for a moment. Can you give me one line of the gist in text?"

**Bad examples** (never do this):
> ❌ "I'll process the [USER_SHARED] audio!"
> ❌ *(even though the transcript is already in the body)* calling `whiteboard_transcribe` unconditionally → regenerating info that already exists, wasting GPU.
> ❌ Re-emitting the Korean from the transcript word-for-word as a quote.
> ❌ Exposing an internal identifier like `capture_id` to the user.
> ❌ When `ambient: true`, saying "I heard [X] in the memo you just sent me. Are you okay?" → the user *never sent* you anything. It should be changed to something like "I heard [X] over there...".
> ❌ When `ambient: true`, replying separately to each spotlight item → multiple utterances in one burst should be taken in *at once*.
> ❌ When `ambient: true` and the utterance isn't aimed at you, forcing out a reply anyway → silence is often the right answer.

## Don'ts

- Don't call `whiteboard_transcribe` when the auto-transcript is already in the body (the W2 hook is idempotent, but extra calls only add latency).
- Don't echo the `[USER_SHARED]` trigger itself.
- Don't *arbitrarily summarize/translate the transcript and pass it off as fact* — if the text is short, confirm it with the user as-is.
- Don't *guess* at the audio content — if there's no transcript, you must obtain it via the tool or ask the user.
- Don't bring up the same audio capture every turn (move naturally to a new topic within the spotlight TTL).
