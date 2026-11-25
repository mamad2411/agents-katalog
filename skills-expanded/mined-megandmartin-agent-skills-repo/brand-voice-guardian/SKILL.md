---
name: brand-voice-guardian
description: Loads a brand voice profile from a local voice.md file and scores or rewrites any draft against it using a 5-point voice rubric. Use when the user asks "does this sound like us", "check the tone", "rewrite this in our voice", "voice check", "on-brand?", or before any content skill ships copy under an established brand. Don't use for creating a voice profile from scratch — interview the user and write voice.md first, then run this skill.
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Content & Marketing, Brand Voice, Editing, QA]
    related_skills: [linkedin-content-pack, x-thread-builder, newsletter-assembler, content-repurposer]
    config:
      content.voice_path: "./voice.md"
---

# Brand Voice Guardian

Holds every draft to a written voice standard instead of vibes. Reads the brand's voice profile from a local file, scores the draft on a 5-point rubric with quoted evidence, and rewrites only what fails — preserving the author's facts and structure. The voice file is the source of truth; this skill never invents brand rules.

## When to Use

- A draft exists (post, thread, newsletter, page copy) and must match an established brand voice.
- The user asks for a tone check, voice score, or "make this sound like us".
- As the final gate after `linkedin-content-pack`, `x-thread-builder`, or `newsletter-assembler`.
- **Not for:** creating a voice profile from scratch (interview the user and write voice.md first, then run this skill), or fact-checking content (that's `deep-research-brief`).

## Quick Reference

| Action | Command / Call |
|---|---|
| Locate voice profile | Read path from skill config key `content.voice_path` (default `./voice.md`) |
| Load profile | `read_file` on the resolved path |
| Score draft | Apply the 5-point rubric below, 1–5 each, quote evidence |
| Compute total | `python3 -c "print(sum([4,3,5,4,4]))"` with your five scores |
| Rewrite | Fix only dimensions scoring ≤3; keep facts and structure intact |

## The 5-Point Voice Rubric

Score each 1 (off-brand) to 5 (exemplary), citing a quoted line from the draft as evidence:

1. **Vocabulary** — uses the brand's preferred words; avoids its banned words/jargon list.
2. **Rhythm** — sentence length and cadence match the profile (punchy vs. flowing).
3. **Stance** — attitude and point-of-view strength match (bold, warm, dry, etc.).
4. **Formality** — contractions, slang, and address ("you"/"we") match the profile.
5. **Signature moves** — the brand's recurring devices appear (or its anti-patterns don't).

## Procedure

1. **Precheck** — resolve `content.voice_path` from skill config; fall back to `./voice.md`. Confirm the file exists (`read_file`). If missing or empty, stop: tell the user the expected path and offer to draft a voice.md from 3 samples of their writing. Do not proceed on an imagined voice.
2. **Load** — read voice.md fully. Extract into working notes: preferred words, banned words, rhythm rules, stance, formality level, signature moves. If the file lacks one of the five dimensions, mark that dimension "not specified — skipped" rather than guessing.
3. **Gather** — get the draft text and its destination platform (platform norms can legitimately bend formality; note this before scoring).
4. **Score** — apply the rubric. For each dimension: score 1–5, one quoted line as evidence, one-line reason. Sum with python3 (Quick Reference). ≥20/25 = pass; 15–19 = targeted rewrite; <15 = full rewrite.
5. **Rewrite (if needed)** — fix only failing dimensions. Never change facts, claims, links, or the argument's order. Keep length within ±10% of the original unless the user asked for cuts.
6. **Deliver** — output the scorecard, then the rewrite (if any), then a one-line diff summary of what changed and why. Deliver as a draft; never publish or send anything.

## Output Template

```
# Voice Check: [draft title/first line]
**Profile:** [voice_path] | **Platform:** [where this will run]

| Dimension | Score | Evidence | Note |
|---|---|---|---|
| Vocabulary | x/5 | "..." | ... |
| Rhythm | x/5 | "..." | ... |
| Stance | x/5 | "..." | ... |
| Formality | x/5 | "..." | ... |
| Signature moves | x/5 | "..." | ... |
**Total: xx/25 — [PASS / TARGETED REWRITE / FULL REWRITE]**

## Rewrite
[revised draft, or "No rewrite needed"]

## What changed
- [dimension]: [one-line change summary]
```

## Pitfalls

- **Voice file missing or stale** — scoring against memory of the brand instead of the file. Recovery: step 1 is a hard gate; if the file can't be read this session, stop and say so. If the file contradicts recent published content, flag the conflict to the user instead of silently picking one.
- **Rewrite drift** — "fixing the voice" quietly changes claims, numbers, or the CTA. Recovery: after rewriting, diff the two versions line-by-line and confirm every fact, link, and number survived; restore anything that didn't.
- **Over-sanding** — rewriting a 22/25 draft anyway and flattening what made it good. Recovery: respect the thresholds in step 4; a pass ships with the scorecard and zero edits.
- **Platform-blind scoring** — docking formality points on an X post for contractions the platform expects. Recovery: capture the platform in step 3 and note in the scorecard where platform norms modified the reading of the profile.

## Verification

- [ ] Voice profile was read from the configured path this session (quote its path in output)
- [ ] All five dimensions scored with a direct quote from the draft as evidence
- [ ] Total computed via python3, thresholds applied as written
- [ ] Rewrite (if any) preserves every fact, number, link, and the CTA
- [ ] Output labeled as a draft; nothing was posted or sent
