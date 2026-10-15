---
name: framevideo-voiceover-ssml
description: Create narration from project subtitles or AI analysis output, then author SSML-style voice scripts with phoneme, break, and ttnumber markup for FrameVideo voiceovers. Use when the user wants subtitles linked to voice generation, automatic narration from transcript/content, pronunciation fixes, pause insertion, or text normalization before TTS.
---

# FrameVideo Voiceover SSML

Use this skill when the voice track should come from project subtitles, transcript words, or AI analysis text instead of a hand-written script.

## Workflow

1. Find the source text in this order:
   - project subtitles / transcript
   - AI analysis / extracted scene copy
   - existing narration draft
2. Turn that source into a speakable voice script.
3. Keep SSML-style markup in the authoring layer:
   - `phoneme` for pronunciation fixes
   - `break` for pauses
   - `ttnumber` for custom number reading
4. Send the marked script to a TTS provider only if it supports the tags.
5. Save both:
   - the marked source script
   - the provider-safe fallback text when needed
6. Write the generated audio back into the project voiceover flow, then sync transcript/captions from the result.

## Use the right source

- Prefer project subtitles or transcript first.
- If subtitles are too terse, expand them with the AI analysis text that already exists for the project.
- Keep the spoken wording close to the visible content unless the user asks for a stronger ad-style rewrite.

## Markup rules

- Use `phoneme` only for words that TTS misreads.
- Use `break` for intentional pauses, not every comma.
- Use `ttnumber` for product numbers, dates, pricing, or counts that should be spoken differently from how they appear.
- Keep the original text readable; markup should clarify delivery, not obscure meaning.

## Provider behavior

- If the TTS backend supports SSML-like tags, pass them through unchanged.
- If the backend does not support them, strip the tags into a clean fallback script before generation.
- Keep the original marked script next to the fallback so the audio can be regenerated later.

## Project writeback

- Treat generated narration as a project asset, not a one-off export.
- Reuse the project's existing voiceover, transcript, and caption paths.
- Keep the access-token header contract used by the Chanjing voice APIs.

## Read these references

- [references/workflow.md](references/workflow.md)
- [references/ssml.md](references/ssml.md)

