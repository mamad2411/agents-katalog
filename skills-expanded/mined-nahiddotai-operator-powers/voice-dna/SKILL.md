---
name: voice-dna
description: Extract a portable writing voice from real samples when the user asks the AI to sound like them, learn their style, build a voice guide, or diagnose voice drift.
---

# Voice DNA

## The Job

Turn available samples of the user's real writing into a portable writing-voice skill they own. Three to five varied samples produce stronger evidence, but thin evidence does not block the job.

## Why the Deliverable Is a Skill File

A style summary gets pasted once and lost. A skill file is reusable infrastructure for tools that support skills. The voice rules are portable, but installation locations and supported formats differ by tool. The user leaves with an editable asset, not advice.

## How to Run It

1. Collect whatever genuine writing is available. Good samples include emails they sent, posts, messages to colleagues, and anything written mostly in their own words. Aim for 3 to 5 samples across at least two contexts, but continue when there is less:
   - `Strong evidence`: 3 to 5 varied samples. Build the full profile.
   - `Provisional evidence`: 1 to 2 samples, short samples, or one context. Build a usable starter profile, label confidence, and identify what needs confirmation.
   - `No existing sample`: ask the user to write one short natural message or answer two or three prompts in their own words, then build a provisional profile.
   AI-assisted samples can contribute only when the user identifies which parts still sound like them. Do not reject the entire job because the evidence is thin.

2. Analyze across these dimensions, quoting evidence from the samples for each finding:
   - **Register**: how they sound in one sentence, stated as a comparison ("a sharp friend explaining over coffee", not "conversational").
   - **Rhythm**: sentence length distribution, where they break paragraphs, whether they front-load the point or build to it.
   - **Vocabulary fingerprint**: 5 to 8 words or constructions they reach for; 3 to 5 they never use.
   - **Signature moves**: repeatable patterns supported by the samples ("opens with the objection a reader is already thinking", not "engaging openings"). Do not force three when the evidence supports fewer.
   - **Never rules**: 3 to 5 things that would instantly break the voice, including punctuation habits (some people never use semicolons; some never write one-sentence paragraphs).
   - **Formatting habits**: lists vs prose, line breaks, capitalization quirks, emoji policy.
   Separate **voice constants** that appear across contexts from **context-specific habits** such as formal client-email structure or casual social-post fragments.

3. Show the analysis, confidence for each major finding, and the gaps. Let the user correct it. They know their voice; the samples are evidence, not verdict. Fold in their corrections.

4. Generate the deliverable: a complete, valid skill file named after them (for example `jamie-writing-voice`), with:
   - YAML frontmatter: lowercase-hyphen `name` (64 chars max), `description` under 1024 characters that says when to apply the voice.
   - Body sections: Voice summary, Confidence and evidence, Voice constants, Context-specific habits, Rhythm rules, Vocabulary (use / never), Signature moves, Never rules, and one short before/after example pair drawn from their own samples (generic AI phrasing vs their phrasing).
   - For a provisional profile, mark uncertain rules as provisional inside the file so it remains useful without pretending the evidence is complete.

5. Prove it works: write one short paragraph on a topic they pick, once in default AI voice and once through their new skill, side by side. Let them feel the difference. If it misses, adjust the skill file and show the diff.

6. Tell them how to install it for the tool they actually use. Verify that tool's current skill format and location when possible rather than claiming every tool installs skills identically. The file is theirs: portable in substance, editable, and not dependent on this plugin.

## Boundaries

- The analysis and the generated file stay in the conversation and on the user's machine; nothing is sent anywhere.
- Never invent patterns the samples don't show. Thin evidence gets flagged as thin ("only one sample shows this; confirm it's really you").
- Never refuse to create a starter Voice DNA only because the user has fewer than three samples.
- Never claim the skill file captures everything; voice drifts, and the file is editable. Suggest re-running after a few months of real use.
- Keep one core voice per run. Record context-specific variations inside it; split into separate skills only when the voices genuinely diverge and the user wants that separation.

Inspired by the emerging voice-analysis skill pattern in the Claude skills ecosystem; rebuilt for non-technical writers with a portable skill file as the deliverable.
