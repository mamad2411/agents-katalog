---
name: deep-study
version: 4
description: >-
  Guided study of a research `REPORT.md` — a codebase report (`.plans/research/<topic>/`) or a topic report (`.plans/research-with-instructions/<topic>/`). Walks the user section by section, opens each cited `file:line` or source URL, paraphrases it, checks in before advancing. Hard-stops if no report exists — consumes a report, never writes one. Auto-discovers either location or takes an explicit path. Triggers: "study this report", "study the report on X", `/deep-study`. Stateless, read-only.
---

# Deep Study

A guided, user-paced walk through a research `REPORT.md` — either codebase research at `.plans/research/<topic>/REPORT.md` (citations are `file:line` locations in the repo) or topic research at `.plans/research-with-instructions/<topic>/REPORT.md` (citations are source URLs, page titles, or Context7 doc IDs). For each finding, opens the cited location, paraphrases what it says, and checks in before moving on. Read-only and stateless — every session is independent and writes nothing.

## Core rules

1. **Read-only.** Never modify any file.
2. **Stateless.** Don't write `STUDY.md`, `NOTES.md`, or any state artefact. The conversation is the only progress tracker.
3. **Cite while you walk.** For every finding, open and paraphrase from the actual cited source — the `file:line` in the codebase, or the URL / doc for a topic-research report — never from `REPORT.md` alone. Reports drift; the cited source is the source of truth.
4. **One section at a time.** Walk top-level finding sections in order. Don't try to cover the whole report in one breath.
5. **User-paced.** After each section, check in via `AskUserQuestion` (continue / dig deeper / skip / ask). Don't barrel through.
6. **Validate citations as you go.** If a cited file is missing, or the lines no longer match what the report describes, surface it explicitly — don't silently paper over.
7. **Don't produce a report inline.** If no report exists, tell the user this skill studies an existing research report and one must exist first — don't generate one.
8. **Walk in terse mode.** Switch to terse output before the first section so paraphrases stay tight (one to two sentences per citation, no decorative formatting, no padding) — see step 0. High signal, low noise — the user is here to study code, not read prose.

## Workflow

### 0. Enter terse mode

Before anything else, switch to terse output for the rest of this session (unless the user opts out). Keep complete sentences and proper grammar, but cut filler, hedging, pleasantries, restated questions, closing flourishes, and decorative formatting. Concretely for this walkthrough: one-to-two-sentence paraphrases per citation; no decorative headers, bullets, or bold where a sentence works; no padding ("it is worth noting that", "as you can see"); no self-narration ("let me walk you through"). High signal, low noise.

### 1. Locate the report

- If the user passed an explicit path (in their message or as `/deep-study <path>`), use it.
- Otherwise, list every `.plans/research/*/REPORT.md` **and** every `.plans/research-with-instructions/*/REPORT.md`. If exactly one exists, pick it and tell the user (note which kind — codebase or topic research). If multiple exist, ask which to study via `AskUserQuestion` — one option per topic slug, labelled with its kind.
- If none exist in either location, tell the user no report was found at `.plans/research/*/REPORT.md` or `.plans/research-with-instructions/*/REPORT.md` (or the path they gave), explain that this skill walks an existing research report and one must exist first, and stop without producing further output.
- Read the picked `REPORT.md` fully (it is intended to be small). Note its kind: a codebase report cites `file:line` locations; a topic report cites URLs, page titles, and Context7 doc IDs — this determines how you visit citations in step 3.

### 2. Orient

- Show the user the report's original question, the executive summary, and the list of top-level finding sections (one bullet per section).
- Ask via `AskUserQuestion` where to start: front-to-back, a specific section, or a named theme. Recommend front-to-back.

### 3. Walk

For each chosen section, in order:

1. **Introduce the finding's claim.** Quote or briefly paraphrase the report's text to set up context. Hold final judgment until the citations are visited — the report's framing is a starting point, not a conclusion.
2. **Visit each citation.** For every reference in the section:
   - **Codebase report** — `path/to/file.ext:lineno` (or `:start-end`): open the file at the cited range with `Read`, then explain in your own words what the cited code does and how it supports the finding. If the file is missing or the cited range no longer matches the description, say so plainly and continue with what's actually there.
   - **Topic report** — a URL, page title, or Context7 doc ID: fetch the source with `WebFetch` (or resolve the Context7 ID and query its docs), then explain in your own words what the source says and how it supports the finding. If the URL is dead or the content no longer matches, say so plainly and continue with the report's own text, flagging that it is now unverified.
   - Note any stale, missing, or unreachable citation for the wrap-up.
3. **Section check-in.** When the section is fully walked, ask via `AskUserQuestion`:
   - `"Continue to the next section (Recommended)"`
   - `"Dig deeper here — open a related file"`
   - `"Skip ahead — pick a different section"`
   - `"Question first — I want to ask about this section"`

If the user picks "dig deeper", read the related file they name (or the most-cited adjacent file) and paraphrase. Then re-offer the same check-in. After three consecutive "dig deeper" rounds on the same section, gently suggest moving to the next section instead of re-offering the dig-deeper option.

### 4. Wrap up

When all chosen sections have been walked, or the user signals "done":

- Offer a one-paragraph recap of what was covered, drawn from the conversation — do not write a file.
- List any citations that were stale, missing, or unreadable so the user knows where the report needs revisiting.
- Remind the user that nothing was persisted: if they want notes, they should capture them outside this skill.

## What NOT to do

- Don't modify any file.
- Don't write progress, notes, or state files — this skill is stateless.
- Don't paraphrase a finding without opening the cited source. Always visit the code (codebase report) or fetch the URL / doc (topic report).
- Don't summarise the whole report in one turn. Walk it section by section.
- Don't advance past a section without a check-in. The user paces this, not you.
- Don't generate a research report yourself. If one doesn't exist yet, say so and stop — this skill only consumes reports.

## Companion files

- [EXAMPLE.md](EXAMPLE.md) — turn-by-turn walkthrough showing the locate → orient → walk → check-in cadence on a real-shaped report.
