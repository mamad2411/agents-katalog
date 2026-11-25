---
name: transcript-clean
description: Turn a raw ASR transcript into clean, speaker-labeled, timestamped text that the rest of the pack can read reliably.
metadata: { "openclaw": { "emoji": "🧹" } }
---

# Transcript Clean

Raw transcripts from Whisper, Descript, Otter, Riverside, or YouTube auto-captions are messy: filler words, false starts, `Speaker 1 / Speaker 2` labels, mangled names, and 400-word run-on blocks. This skill turns any of them into one **canonical transcript** — the single clean file every other skill in the Content Engine pack reads.

## When to use (trigger phrases)

Use this skill when the user says:

- "clean up this transcript"
- "fix the transcript / label the speakers"
- "here's the raw captions, make it readable"
- "prep this episode transcript for show notes / clips"
- "convert this SRT/VTT to a clean transcript"

## How it works

1. **Identify the input format.** Detect one of: SRT, WebVTT (`.vtt`), Whisper/Descript JSON, or plain text. Timed formats look like `00:00:12,340 --> 00:00:15,900`. Keep the timestamps — downstream clip-finding depends on them.
2. **Parse to segments.** Reduce every format to a list of `{ start, speaker, text }`. For SRT/VTT you can strip the cue numbers and arrows; for JSON read the `segments`/`words` array. If the source has no timestamps, keep the text but warn the user that clip-finder will be approximate.
3. **Resolve speakers.** ASR gives `SPEAKER_00`, `Speaker 1`, etc. Ask the user once: *"Who is Speaker 1 / Speaker 2?"* Then map every label to a real name (e.g. `Host — Ryan`, `Guest — Dr. Chen`). If diarization is obviously wrong (one speaker's lines bleed into another mid-sentence), fix the boundary using conversational cues (questions vs. answers).
4. **Build a name & term glossary.** ASR reliably mangles proper nouns, product names, and jargon. Ask the user for a short glossary (`"it's 'Convex' not 'convicts', 'x402' not 'x 4 0 2'"`) and apply it as a find-and-replace across the whole transcript. This one step saves every downstream skill.
5. **Light-clean the prose — do not rewrite it.** Remove filler (`um`, `uh`, `you know`, `like` used as filler), collapse stutters and false starts (`I think— I think we should` → `I think we should`), and fix obvious punctuation. **Keep the speaker's actual words and voice.** Never paraphrase, never "improve" the argument. When in doubt, leave it.
6. **Re-paragraph.** Break the wall of text into paragraphs at every speaker change and roughly every 30–60 seconds of a single speaker. Prepend a `[HH:MM:SS]` timestamp to each paragraph so clips and chapters can anchor to it.
7. **Offer a verbatim mode.** If the user is producing an accessibility transcript or legal record, ask before removing filler — some use cases need it word-for-word. Default is "readable clean," verbatim on request.
8. **Write the canonical file.** Save as `transcript.clean.md` next to the source (or wherever the user keeps the episode). Report a short diff summary: input format, duration, speaker count, words removed.

## Output

A single markdown file in this canonical shape:

```markdown
# The Cold Start Problem — Ep. 42 with Dr. Chen
Duration: 58:12 · Speakers: Host — Ryan, Guest — Dr. Chen

[00:00:00] **Ryan:** Welcome back. Today I'm talking to Dr. Chen about why most
consumer apps die in the first ninety days, and what the survivors do differently.

[00:00:19] **Dr. Chen:** Thanks for having me. The thing nobody tells you is that
retention is a distribution problem, not a product problem. You can have a great
product and still churn everyone if the first session doesn't land.

[00:01:04] **Ryan:** Say more about "the first session doesn't land" —
```

Plus a one-line report back to the user, e.g.:
`Cleaned VTT → transcript.clean.md · 58:12 · 2 speakers · removed 214 filler words · applied 6 glossary fixes (Convex, x402, Dr. Chen…).`

## Notes

- **This skill does not transcribe audio or video.** It expects text in. If the user only has a recording, run a transcription skill first (e.g. the `openai-whisper` OpenClaw skill, or Descript/Riverside export) and hand the result here.
- **Fidelity over polish.** The most common failure is an over-eager rewrite that changes what the guest actually said. Clean the noise, keep the substance. If you find yourself rephrasing a sentence, stop.
- **Preserve timestamps at all costs.** If the source is plain text with no timing, tell the user clip timestamps will be estimated, not exact.
- **The glossary is worth the interruption.** One pass of corrected names/terms here prevents the same error showing up in show notes, clips, the newsletter, and the thumbnail title.
- Non-English or code-switched audio: keep the original language; don't silently translate. Ask if a translated version is wanted as a separate file.
