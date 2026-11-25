---
name: medical-deck
description: Use when someone asks for slides, a deck, a talk or a presentation on a medical or health-science topic (journal club, conference talk, lecture, grand rounds, guideline update, clinical case, M&M, thesis defence, patient education), or wants an existing medical deck rebuilt, restyled, translated or checked before presenting.
---

# Medical deck

## Overview

You are the orchestrator. A medical deck is finished only when every number on it can be
traced to a source the audience could check, and nothing on it looks machine-made. You do
not draft slides yourself in the first message, and you do not decide what the presenter
has not told you.

**Violating the letter of these stages is violating their spirit.** "Quick mode" makes each
stage shorter; it never removes one.

## Stages and gates

| # | Stage | Skill to load | Output (in the talk folder) | Gate |
|---|-------|---------------|------------------------------|------|
| 1 | Interview | deck-grilling | `brief.md` | user confirms the brief |
| 2 | Template (if one was given) | template-matching | `theme/theme.json`, thumbnails | — |
| 3 | Plan | deck-planning | `plan.md` | **user approves the plan** |
| 4 | Evidence | evidence-research | `evidence/references.json`, `evidence/claims.json` | no claim without a source |
| 5 | Figures | medical-figures | `figures/`, `figures/manifest.json` | provenance recorded |
| 6 | Build | html-deck-building or pptx-deck-building | `build/`, `out/` | renders without overflow |
| 7 | Audit | slop-audit and evidence-audit | `audit/*.md` | no blocking findings |
| 8 | Deliver | — | `out/` + summary | — |

**Your first reply to a new request is the interview and nothing else.** Load
deck-grilling, send its round of numbered questions, and end your turn. No talk folder, no
files, no literature search, no slides in that turn, however complete the request looks.
"5 slides on drug X, HTML, lots of charts" still leaves audience, duration, language,
template, sources and presenter open.

Once the user confirms the brief, create the talk folder: `./<short-slug>/` in the current
directory, holding `brief.md` and a `STATUS.md` that lists the stages, each marked `todo`,
`doing`, `done` or `blocked`. Update
it as you go; it is how a later session resumes. Write `done, approved` on the Plan row
only after the user says yes to `plan.md`: on Claude Code a hook keeps `build/` and `out/`
closed until then.

Stage 4 still runs when the user supplies the paper: their PDF becomes the source, and
claims are extracted from it with page/table/figure locators. Search only fills gaps.

## Dispatching stages

Give stages 4, 5, 6 and 7 each to a **fresh subagent** when your harness can dispatch one,
so each works from files, not from this conversation. Fill in the brief in
`roles/<role>.md` (paths, deck type, output format) and pass it as the subagent prompt:

| Stage | Role brief |
|-------|------------|
| 4 | `roles/evidence-researcher.md` |
| 5 | `roles/figure-maker.md` |
| 6 | `roles/deck-builder.md` |
| 7 | `roles/slop-reviewer.md` and `roles/evidence-reviewer.md` (independent, may run in parallel) |

How to dispatch on each harness:

- Claude Code: the Agent/Task tool, general-purpose subagent.
- Codex: `spawn_agent` (needs `[features] multi_agent = true`), then `wait_agent`.
- Antigravity: `invoke_subagent` with TypeName `self`.
- No subagent support: run the stage yourself, loading the skill it names.

To load a skill, call the Skill tool with its name. Where there is no Skill tool
(Antigravity), read that skill's `SKILL.md` with your file-read tool.

Stages 1, 3 and 8 stay with you: they need the user.

## Fix loop

Route each audit finding to the stage that owns it:

- wrong or unsupported number, overclaim, bad reference → stage 4, then rebuild;
- figure problem or missing licence → stage 5;
- slop, overflow, layout → stage 6.

Re-run only the audits whose inputs changed. After three loops with blocking findings
left, stop and show the user the open findings instead of looping again.

## Delivering

Tell the user: where the file is; slide count and run time; what was verified against full
text, abstract only, or not at all; figure credits and licences; open findings. Do not
describe a deck as checked if stage 7 did not run.

## Red flags: stop and go back a stage

| Thought | Reality |
|---------|---------|
| "I'll assume PPTX, they can tell me if not" | Format and template are the user's decisions. Ask (deck-grilling). |
| "The usual journal-club flow is fine" | The purpose (report, critique, change practice) changes the structure. Ask. |
| "The request already says topic, format and slide count" | Audience, duration, template, sources and presenter are still open. Ask, then wait. |
| "I'll ask the questions and start researching meanwhile" | The turn that asks ends there. Work done before the answers is built on guesses. |
| "They're in a hurry, skip the questions" | One round of numbered questions with recommended answers takes a minute. Ask it. |
| "I know this trial's numbers" | Memory is not a source. Stage 4. |
| "I'll add the PMID and mark it (verify)" | Identifiers come only from a lookup made in this session. |
| "The plan is obvious, start building" | No build before the user approves `plan.md`. |
| "The audit is a formality" | Stage 7 is the only thing standing between a wrong hazard ratio and a podium. |
