---
name: muse-google-veo-web
description: "Generate video with Google Veo through the web app (Google Flow) on a Google AI Pro subscription: project setup, Veo prompting, browser-driven generation, full-duration QA, and stitching. Use when the backend is Veo via the browser rather than an API."
---

# Muse Google Veo Web

End-to-end video production with Google's Veo through the web interface
(Google Flow) on a Google AI Pro subscription. This skill covers the full
loop most web-based Veo projects need: setting up the account and project,
writing prompts Veo responds to, driving generation in the browser,
verifying every clip across its full duration, and stitching the result.
It is backend-specific on purpose: the rest of the pack stays
model-neutral, and this is where the Flow particulars live.

## The workflow

1. **Set up the project** (`references/flow-generation.md`). Pro
   subscription, one Flow project per video project, one Google account
   for the whole job. Know your monthly credit allowance before you plan
   the clip count.
2. **Plan the clip list.** One clip per story beat, 8 seconds each: that is
   Veo's web sweet spot. Never stretch a handful of clips across minutes
   by looping; if the clip count gets heavy, trim the story, not the
   coverage.
3. **Lock references first.** Anything that must stay consistent across
   clips (characters, products, logos, locations) gets a reference sheet
   image before any clip is generated. Flow's Ingredients-to-Video mode
   takes reference images; attach them on every generation.
4. **Write the prompts** (`references/veo-prompting.md`). Five-part Veo
   formula: Cinematography, Subject, Action, Context, Style & Ambiance,
   plus Preserve/Avoid slots. For text-to-video, paste locked descriptions
   verbatim, never paraphrased. For Ingredients-to-Video, attach the reference
   and describe only the shot and motion; do not restate what the image
   already shows (repetition invites drift).
5. **Generate in the browser** (`references/browser-ops.md`). Queue clips
   sequentially in one session. Renders take a long time; a full batch
   runs for hours in the background, which is normal.
6. **QA every clip across its full duration** (`references/web-qa.md`).
   Sample frames across the whole clip, classify failures, fix or
   regenerate with an attempt budget, then cut what won't pass.
7. **Download and assemble.** Take the highest quality Flow offers, strip
   native audio if post handles the sound, and stitch with the
   `assembly-and-delivery` skill (`scripts/concat.py`).

## Rules that don't bend

- **Reference images on every Ingredients-to-Video generation.** No
  ingredients, no consistency. The model does not remember across clips;
  you reattach every time. Pure text-to-video one-offs with no continuity
  burden are exempt.
- **Full-duration verification.** An 8-second clip is 8 seconds of chances
  to break. Check frames across all of it before it touches the timeline.
- **One clip per beat.** Looping a few clips across minutes reads as cheap
  the moment anyone notices, and they notice.
- **Cheap tier for iteration, expensive tier for finals.** Draft and
  explore on the cheap tier; spend the expensive tier only on clips that
  already passed QA. Verify current credit costs before budgeting; they
  change.
- **Decide audio upfront.** Either keep Veo's native audio (dialogue,
  ambience) or strip it and do all sound in post. Mixing both without a
  plan gives doubled ambience and sync drift.
