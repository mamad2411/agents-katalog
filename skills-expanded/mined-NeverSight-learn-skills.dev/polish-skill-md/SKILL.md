---
name: polish-skill-md
description: 'Use when polishing, linting, reviewing, or rewriting an existing SKILL.md: tighten its description, fix pattern drift, split an overgrown manifest into companion files, or audit a skill before publishing. Do not use for brand-new skill scaffolding, general Markdown cleanup, or ordinary code/docs edits.'
---

# Polish `SKILL.md`

Rewrite an existing `SKILL.md` into a tighter, better-triggered skill manifest. This skill is a **Reviewer + Generator + Pipeline**: inspect the current manifest against an external rubric, rewrite it to match the template, then verify discovery.

---

## Use When

Use when the user asks to:

- polish, refine, tighten, lint, or review an existing `SKILL.md`
- rewrite a skill `description` so it triggers on the right requests
- split an overgrown `SKILL.md` into `references/`, `assets/`, or `scripts/`
- realign a skill to the five design patterns before publishing

Do **not** use for:

- creating a brand-new skill from a blank page
- editing ordinary application code, `AGENTS.md`, or `DESIGN.md`
- generic Markdown cleanup when the file is not a skill manifest

---

## Operating Modes

- **`review`** - diagnose only. Return findings, section classifications, and a revision plan. Do not edit files.
- **`polish`** - apply the revision plan. Edit `SKILL.md` and split content into companion files when needed.

If intent is ambiguous, default to **`review`**.

---

## Pipeline

`intake → classify → review ──[GATE: in review mode stop after the plan; in polish mode proceed only if no open questions remain]──▶ revise → verify`

1. **Intake** - read the target `SKILL.md` and list sibling `references/`, `assets/`, and `scripts/` files.
2. **Classify** - compare the skill's claimed pattern(s) with the body it actually implements.
3. **Review** - apply the rubric and produce a keep / tighten / split / delete plan.
4. **Gate** - in `review` mode, stop and return the plan. In `polish` mode, proceed only if the plan is unambiguous; otherwise downgrade to `review` and ask.
5. **Revise** - rewrite the manifest to match the workflow template and move overflow into companion files.
6. **Verify** - run the checklist and confirm discovery.

---

## Execution

Load on demand:

1. **Pattern mapping and Gate Test:** [references/patterns.md](./references/patterns.md) - load during `classify`.
2. **Severity order and review checklist:** [references/rubric.md](./references/rubric.md) - load during `review`.
3. **Revision order and SKILL.md template:** [references/workflow.md](./references/workflow.md) - load during `revise`.
4. **Filler / vocabulary tightening:** [references/word-tightening.md](./references/word-tightening.md) - load after structural edits, before final verification.
5. **Source citations:** [references/sources.md](./references/sources.md) - load only if you need to defend a claim or escalate a finding.

Always run `classify` before `review`. Always run `review` before `revise`.

---

## Core Rules

- **Description drives triggering.** Write for user intent, not implementation details. Keep it imperative, concrete, and ≤ 1024 chars. Include both positive triggers and negative scope.
- **Preserve the skill name.** Do not rename `name` unless the user explicitly asks.
- **Fix drift before style.** Pattern drift, broken gates, and missing load cues outrank wording polish.
- **Use progressive disclosure.** Keep `SKILL.md` concise; move overflow into `references/`, `assets/`, or `scripts/` and add explicit load cues.
- **Keep one default.** Do not present menus of equal options.
- **Tighten last.** Do not shorten away imperatives, numeric thresholds, gates, or negative scope.
- **Point instead of copying.** Prefer reference files, templates, scripts, and source links over duplicated prose.

---

## Deliverables

### `review` mode

Return:

- claimed vs actual pattern(s)
- description triggering analysis
- rubric findings, ordered by severity
- keep / tighten / split / delete classification for each major section
- proposed new structure (`SKILL.md` outline + companion files)
- open questions blocking `polish`

Do **not** edit files.

### `polish` mode

Deliver:

- a rewritten `SKILL.md` that matches the template in [references/workflow.md](./references/workflow.md)
- new or updated `references/`, `assets/`, or `scripts/` files when the plan requires them
- a short changelog covering what was kept, tightened, split, or deleted, and why
- the verification checklist below, ticked

---

## Verification

- [ ] YAML front matter has `name` (kebab-case) and `description` (imperative, ≤ 1024 chars).
- [ ] `description` names concrete trigger contexts and at least one negative scope.
- [ ] `SKILL.md` stays within the repo target size and pushes overflow to companion files.
- [ ] Every companion file is linked from `SKILL.md` with a when-to-load cue.
- [ ] Every major section maps to Reviewer, Generator, Pipeline, or explicit meta guidance.
- [ ] No giant inline templates or scripts remain in `SKILL.md`.
- [ ] No menu of equal options remains; the default path is obvious.
- [ ] `npx skills add "<repo-root>" --list` discovers the polished skill.

---

## Final Standard

Result: a `SKILL.md` a cold agent can classify quickly, execute in order, and polish without rereading the whole directory.
