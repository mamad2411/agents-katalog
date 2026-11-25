---
name: sidecar-task-runner
description: Run artifact-driven sidecar agent tasks through one-shot Codex CLI sessions. Use when a main agent should delegate bounded scans, drafts, audits, pre-reviews, or mechanical repo tasks to a fast isolated sidecar model such as gpt-5.3-codex-spark while keeping final decisions with the main agent.
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Sidecar Task Runner

Use this skill to run bounded helper tasks from a main agent without sharing the main conversation as the task state. The sidecar produces artifacts; the main agent verifies, integrates, rejects, or escalates them.

## Skill Directory Layout

```text
<installed-skill-dir>/
├── SKILL.md
├── templates/
│   ├── precommit-classifier.md
│   └── personalization-scanner.md
└── scripts/
    └── prepare_sidecar_task.py
```

## Core Contract

- The main agent owns planning, integration, final judgment, and user-facing actions.
- The sidecar gets a small prompt artifact, not the main chat transcript.
- Default to `gpt-5.3-codex-spark` for fast local scans, first drafts, pre-reviews, consistency checks, and other low/medium-risk tasks.
- Prefer deterministic scripts and direct shell commands for facts; use the sidecar for synthesis, ranking, summarization, mismatch detection, and candidate text.
- Default sandbox is `read-only`. Use `workspace-write` only when the sidecar must write its own artifacts or make explicitly bounded edits.
- Keep human gates before external or irreversible actions such as `git tag`, `git push`, release upload, job submission, or public issue creation.
- Do not use a sidecar as the only reviewer for high-risk algorithm design, core correctness, security/privacy, final merge approval, or final submission decisions.

## Artifact Layout

Use a repo-local directory:

```text
.agent/sidecars/<task-id>/
├── prompt.md
├── input-manifest.md
├── output.md
├── findings.md
├── decision.md
├── model.md
└── model.json
```

Meanings:

- `prompt.md`: exact prompt given to the sidecar.
- `input-manifest.md`: files, commands, diffs, or project state the sidecar may inspect.
- `output.md`: raw sidecar final response, usually written with `codex exec -o`.
- `findings.md`: distilled findings if the sidecar writes structured results.
- `decision.md`: main-agent decision after reading the sidecar output.
- `model.md`: human-readable command, model, sandbox, and token notes.
- `model.json`: structured run metadata for token and lifecycle audits.

## Prepare A Task

Create the artifact directory with:

```bash
python3 <installed-skill-dir>/scripts/prepare_sidecar_task.py \
  --repo . \
  --task-id <task-id> \
  --title "<short task title>" \
  --phase tooling \
  --task-type audit \
  --prompt-file <prompt-file>
```

If no prompt file exists, pass `--prompt "<task instructions>"`.

For a fast precommit classification sidecar, use the bundled preset:

```bash
python3 <installed-skill-dir>/scripts/prepare_sidecar_task.py \
  --repo . \
  --title "Precommit classifier" \
  --phase maintenance \
  --task-type audit \
  --preset precommit-classifier \
  --input "git status --short" \
  --input "git diff"
```

For a personalization scan that extracts reusable preferences from sanitized artifacts without asking the user:

```bash
python3 <installed-skill-dir>/scripts/prepare_sidecar_task.py \
  --repo . \
  --title "Personalization scan" \
  --phase maintenance \
  --task-type audit \
  --preset personalization-scanner \
  --input "memory/current-status.md" \
  --input ".agent/sidecars/*/decision.md"
```

## Run Codex Spark

For a read-only sidecar:

```bash
codex exec --ephemeral \
  -m gpt-5.3-codex-spark \
  -C . \
  -s read-only \
  -o .agent/sidecars/<task-id>/output.md \
  "$(cat .agent/sidecars/<task-id>/prompt.md)"
```

For a sidecar that must write its own `findings.md` or make tightly scoped artifact edits:

```bash
codex exec --ephemeral \
  -m gpt-5.3-codex-spark \
  -C . \
  -s workspace-write \
  -o .agent/sidecars/<task-id>/output.md \
  "$(cat .agent/sidecars/<task-id>/prompt.md)"
```

Avoid `codex resume`, `codex fork`, `claude --continue`, or `claude --resume` for first-pass sidecar work. Those are continuation mechanisms, not clean sidecar boundaries.

## Prompt Requirements

Every sidecar prompt should state:

- task goal and non-goals
- files or directories it may inspect
- whether code edits are allowed
- required output path and format
- escalation criteria for strong reviewer or main-agent judgment
- privacy boundary: do not copy raw private logs or unrelated conversation text into repo artifacts

Keep prompts narrow. If the task needs several independent analyses, create separate sidecar runs rather than one broad prompt.

## Model Routing

Good Spark sidecar tasks:

- first-pass code review before a strong review
- precommit path classification: Fast Path, Skill Path, Code Path, or Risk Path
- personalization scans over trajectories, sidecar artifacts, diffs, and memory to propose reusable preferences
- git milestone proposal from recent commits and docs
- README / AGENTS / CLAUDE consistency scan
- test-gap scan after a focused implementation
- experiment log triage and config mismatch inventory
- evidence inventory across CSVs, reports, tables, and figures
- reviewer-comment clustering and action-item extraction
- citation placeholder or TODO scans

Use the main agent or a stronger fresh reviewer for:

- core algorithm design decisions
- final code approval for high-risk changes
- security, privacy, or data-governance decisions
- large refactors with unclear blast radius
- final paper positioning, rebuttal strategy, or submission judgment

## Precommit Classifier Contract

Use the `precommit-classifier` preset when a commit/push closeout would otherwise be slowed down by deciding which gates to run. The sidecar inspects only read-only Git state and affected public repo files, then recommends:

- the commit path: Fast Path, Skill Path, Code Path, or Risk Path
- the minimal validation commands
- whether reinstall is needed
- whether reinstall can be limited to specific changed skills

The main agent must still stage files, commit, push, reinstall, and report the outcome. A sidecar must not perform external or irreversible actions.

## Personalization Scanner Contract

Use the `personalization-scanner` preset when a main agent wants low-cost automatic memory writeback candidates from trajectories or repo artifacts. The sidecar may inspect only explicitly listed inputs and returns candidate preferences with scope, confidence, evidence, suggested target, and privacy notes.

The main agent must still decide what to write, keep private facts out of public repo memory, and perform any project-memory or skill-repo edits. The sidecar must not ask the user, quote raw logs, or promote public skill rules by itself. After accepting sidecar output, the main agent writes: accepted findings to the relevant memory board (claim/risk/action/decision), gate decision to `decision.md`, and sidecar token metadata stays in `.agent/sidecars/<task-id>/model.json` — not in project memory.

## Token Telemetry

Because `--ephemeral` may avoid normal persisted session logs, record run metadata in `model.json`. If Codex CLI reports token usage in the terminal, copy the numeric fields into `model.json` or `model.md` before running `token-usage-auditor`.

If exact usage is unavailable, leave usage values as `null` and record:

```text
Token usage: unavailable from ephemeral run output.
```

Never store raw prompts from private chat logs just to recover token counts.
