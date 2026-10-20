---
name: curriculum-review
description: Audit, review, and improve course curricula, lesson structures, and syllabi — especially technical and AI-coding education. Produces a freshness audit, pedagogy and sequencing critique, layout-change proposals, and a clear overhaul-vs-iterate verdict. Use whenever the user shares a course outline, lesson summary, module list, or syllabus and asks to review, improve, modernize, restructure, or expand it — including phrases like "is my course outdated", "suggest improvements to these lessons", "does this need an overhaul", or any mention of the Vibecoding platform course content.
---

# Curriculum Review

Review a course curriculum the way a curriculum designer and a subject-matter expert would together: verify the content is current, judge whether the pedagogy serves the actual audience, and give one clear structural verdict instead of a pile of loose observations.

## Inputs

Work from whatever structure document the user provides — a lesson summary, README tree, syllabus, or module outline. If only a content directory is given, map its hierarchy first (course → module → lesson) before judging anything; critique of a structure you haven't mapped is guesswork.

If the review targets the **Vibecoding platform** (Vibe Coding Academy, `Vibecoding_course-mb` repo, or its `LESSON_SUMMARY.md`), read `references/vibecoding-platform.md` for the audience profile and repo layout before starting.

## Step 1 — Anchor to the audience

Every structural judgment depends on who the learners are. Establish before reviewing:

- Learner profile: age/stage, prior knowledge, language (first or second), device access
- The transformation promised: what should a graduate be able to do?
- Business framing: free tiers, paid tiers, funnels, completion incentives

If the user hasn't said, ask — one short question, not a survey. A curriculum that is excellent for bootcamp adults can fail school leavers on a phone, so this step is not skippable.

## Step 2 — Freshness audit (research, don't recall)

Course content about AI tooling goes stale in months. Never judge a named tool's current state from memory — your knowledge may itself be the stale thing. For every tool, platform, or model the curriculum names (editors, AI assistants, sandboxes, deploy targets):

1. Web-search its current status: renamed? deprecated? superseded? free tier changed?
2. Search for what has *entered* the landscape since the content was written that the curriculum ignores (new tool categories, new workflows such as agentic coding or spec-driven development).
3. Record each finding with a source and date; separate **verified** changes from **suspected** ones the user should confirm.

Pedagogy can be stale too: flag places where the *approach taught* (not just the tool) no longer matches practice.

## Step 3 — Pedagogy and sequencing review

Walk the structure course by course, module by module. For each, check:

- **Prerequisite integrity** — is anything used before it is taught?
- **Depth calibration** — topics over/under-weighted for the audience's goal
- **Assessment cadence** — one final exam is a smell; look for checkpoints per module
- **Quick wins and motivation** — how many lessons until the learner *makes something real*? Long setup slogs before any payoff predict drop-off, especially for young or self-paced learners
- **Project realism** — do projects resemble what the audience will actually build or be hired to do?
- **Language and device accessibility** — reading level, translation coverage, and whether early content honors the devices learners actually have

## Step 4 — Verdict

Commit to exactly one:

- **Targeted updates** — structure sound; swap stale tools and patch gaps
- **Major restructure** — keep most content but reorder/merge/split modules
- **Complete overhaul** — the shape itself no longer fits the audience or landscape

Justify the verdict from findings, not vibes. If the repo contains unbuilt proposal drafts (alternate outlines, expansion plans), evaluate them against the verdict: adopt, adapt, or discard — with reasons.

## Output format

ALWAYS use this structure:

```
# Curriculum Review: [name]
## Executive summary        ← one paragraph + the verdict, stated first
## Freshness audit          ← verified vs. suspected, with sources
## Recommendations          ← table: 🔴 Critical / 🟡 Recommended / 🟢 Nice-to-have
                              each row: finding, why, rough effort
## Structural changes       ← proposed hierarchy changes; sketch new structure if overhaul
## Uncertainties            ← what you could not verify and how the user can
## Next step                ← the single first thing to fix
```

Be specific and opinionated: name actual tools, module titles, and orderings. "Consider updating the tools section" helps no one; "Replace the v0.dev lesson with X because Y (verified: source, date)" does.

## After the review

Offer, don't assume, the follow-ups: turning accepted recommendations into a rework plan, drafting replacement lessons, or re-running the review on a revised structure.
