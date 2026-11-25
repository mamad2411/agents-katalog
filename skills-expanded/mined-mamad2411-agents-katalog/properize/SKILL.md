---
name: properize
description: >-
  Promote a quick-and-dirty prototype to an lgtm-hq-standard repo - commit WIP
  lint-clean, grill the design, spec the backlog as milestone/epic/issue tree,
  then implement issue by issue. Use when asked to properize, productionize,
  or turn a prototype into a proper project.
---

# Properize

Turn "I hacked this together for myself, it's AI slop, but I want it proper
now" into a repo that meets lgtm-hq standards. This skill **sequences** other
skills into one pipeline — it composes `commit`, design grilling, `issue`,
and `implement-issues`/`pr`, it does not replace them. Never skip a stage or
collapse two stages into one session; each stage produces an artifact
(commits, a design decision, an issue tree) the next stage depends on.

## The mistake this skill prevents

The default failure mode is jumping straight from "make this proper" to
writing a full implementation plan and executing it in one pass — no
commit checkpoint, no design interrogation, no issue trail. That produces an
unreviewable mega-diff and bakes in whatever the prototype already got wrong.
Do NOT do this. Do: commit → grill → recon → spec → implement, one stage at a
time, stopping between stages for the artifacts to exist and be reviewable.

## Pipeline

### 1. Commit the WIP first

Before any design discussion, get the current state to a lint-clean,
committed baseline:

- Drive `uv run lintro chk` to 0 issues. Fix real bugs the gate surfaces
  (missing imports, undefined names, missing arguments, type errors,
  dead-code/unused-variable warnings) rather than suppressing them — a lint
  gate on a prototype routinely finds actual bugs, not just style nits.
- Land signed, semantic commits **grouped by domain**, not one giant commit.
  For example: a `cleanup` pass, then commits per feature area (e.g.
  `discover`, `playlists`), then `app-infra`, then a trailing `chore` for
  anything left over. Follow the `commit` skill for message format and
  signing.
- Do not refactor or redesign here — only make the WIP lint-clean and
  historied. Design changes belong in the next stage.

### 2. Grill the design

Stress-test the **full** design before writing any spec. Prefer the external
`grilling` skill when it is installed (e.g. mattpocock/grilling via the
vendor catalog); otherwise run the same interview inline. One question at a
time, waiting for an answer before the next — do not batch questions.
Recommend an answer with each question. Cover at least:

- Audience and multi-tenancy (single-user tool vs. shared service?)
- Data storage (what DB, migrations, backups?)
- Auth (who can access it, how?)
- Background jobs / scheduling
- Configuration and secrets management
- Deployment target and process
- Documentation expectations (README, ADRs?)
- Scope freeze — what's explicitly out of scope for v1
- Observability (logging, metrics, error tracking)
- Testing strategy and coverage bar
- Issue granularity for the next stage (how small is "one PR"?)

Do not proceed to standards recon until these questions have answers. If the
user defers a question, record the deferral explicitly rather than assuming
a default.

### 3. Standards recon (before writing issues)

Run this recon **after grilling and before stage 4** so branch rulesets and CI
requirements shape the backlog. Treat it as a checklist of repeatable
commands, not a judgment call:

- Fetch `winnow` workflows as the gold-standard CI reference (full workflow
  set).
- Fetch `lgtm-ci` reusable workflows pinned to a release SHA (plus the
  tooling-ref pin), not a floating tag.
- Fetch the org's rulesets for the target repo (`checks-<repo>`) via
  `gh api repos/<owner>/<repo>/rulesets` (or the org-level ruleset endpoint)
  so branch-protection requirements are known before issues are written.
- Bring in the standard community-files set: `.editorconfig`, `SECURITY.md`,
  Renovate config, gitleaks config, and equivalents already used across
  lgtm-hq repos.
- Make `lintro` the sole lint/format entry point — no bare `ruff`/`eslint`/
  etc. invocations left in scripts or CI.
- Wire releases through the version-PR + auto-tag flow used elsewhere in
  lgtm-hq, not manual tagging.

Do not create milestones, epics, or issues until this recon is complete.

### 4. Spec the backlog as milestones, epics, and issues

Turn the grilled design into a milestone → epic → issue tree:

- **Milestones** group epics by release/phase.
- **Epics** group issues by feature area.
- **Issues** are one-PR-sized. Every code issue gets an AI Implementation
  Prompt comment in the `issue` skill's format (see `skills/issue/SKILL.md`),
  so any issue is fan-out-ready for `implement-issues` without rework.
- Generalize the issue-generation script pattern (Python + `gh` calls
  creating milestones, epics, and issues from a structured spec) into a
  repo-agnostic template rather than a one-off script tied to this repo's
  domain. Keep the domain content (titles, bodies, prompts) separate from the
  generation mechanics so the template is reusable on the next prototype.

### 5. Implement, issue by issue

Only after the tree exists: implement issues one at a time, small PRs, per
the `pr` skill (or hand the whole ready backlog to `implement-issues` for
parallel, worktree-isolated lanes). Never batch unrelated issues into one PR
to save time — the point of stage 4 was to make each unit reviewable on its
own.

## Guardrails

- **Stage order is not negotiable.** Do not run standards recon before the
  design has been grilled, do not spec issues before recon is done, and do
  not implement before the issue tree exists.
- **Stop between stages.** Each stage's artifact (commit history, recorded
  design decisions, recon notes, the issue tree) should be reviewable before
  the next stage starts — do not silently chain all five stages into one
  unattended run.
- A stage that cannot stay green (lint, tests, or an unanswered blocking
  design question) **stops and reports** rather than pushing through.
- This skill never merges — implementation PRs follow the normal review and
  merge process for the target repo.
