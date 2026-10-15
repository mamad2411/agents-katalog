---
name: personalization-memory
description: Maintain automatic personalization writeback from agent trajectories, logs, sidecar artifacts, and repeated user preferences. Use when a task produces reusable preferences, lessons, private user memory, project contracts, or candidate public skill rules without interrupting the user.
argument-hint: "[project-root] [--scan-trajectories] [--writeback] [--promote]"
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Personalization Memory

Turn repeated interaction traces into durable preferences without making the main agent stop and ask the user for every memory update. This skill is the writeback layer for "the system gets more personal over time."

## Skill Directory Layout

```text
<installed-skill-dir>/
├── SKILL.md
├── references/
│   ├── trajectory-scanner.md
│   └── writeback-policy.md
└── templates/
    └── preference-ledger.md
```

## Core Contract

- Do not ask the user just to decide whether a routine preference should be remembered.
- Prefer low-cost sidecar scanning for synthesis from logs, trajectories, diffs, sidecar outputs, review bundles, and project memory.
- Never copy raw private conversations, raw logs, credentials, local-only paths, or collaborator messages into public repo memory.
- Store the smallest reusable lesson, not the whole episode.
- Treat personalization as a promotion ladder: observation -> candidate -> preference -> project contract -> reusable skill-rule candidate.
- Public skill changes require the same normal repo validation, commit, push, and reinstall flow as other skill changes.

## When to Use

Use this skill when:

- the user says a workflow should become personalized, automatic, remembered, or learned from trajectories
- the agent notices repeated preferences such as "do not ask me", "commit/push first", "use Overleaf compile", "prefer screenshots/page bundles", "use sidecar for low-risk scans"
- another skill finishes meaningful work and there are reusable workflow, writing, figure, LaTeX, Git, review, or compute lessons
- Codex or Claude Code trajectory logs should be scanned into candidate preferences
- project memory needs to separate private user facts from shared project contracts and public skill rules

Pair with `sidecar-task-runner` for the low-cost scan and with `research-project-memory` when accepted project-level conclusions must update `memory/`.

## Progressive Loading

- Read `references/writeback-policy.md` before deciding where a preference belongs.
- Read `references/trajectory-scanner.md` before launching a sidecar scan over logs, trajectories, sidecar artifacts, or repo history.
- Use `templates/preference-ledger.md` when a project lacks a preference ledger.

## Workflow

1. **Collect artifact inputs.** Prefer sanitized artifacts: `memory/`, recent `git diff`, `.agent/sidecars/*/decision.md`, `.agent/code-reviews/*/fix-log.md`, `.agent/layout-issues/*/manifest.md`, paper/code `.agent/` state, and explicit user-stated preferences in the current task summary.
2. **Run a low-cost scan when useful.** Use `sidecar-task-runner` with the `personalization-scanner` preset for nontrivial history or trajectory scans. The scanner outputs candidates; it must not directly edit memory.
3. **Classify each candidate.** Assign scope: `private-user`, `project`, `public-skill-candidate`, or `discard`. Assign type: `workflow`, `writing`, `layout`, `figure-style`, `code-review`, `git`, `compute`, `toolchain`, or `collaboration`.
4. **Apply confidence gates.** One observed episode can become a lesson. Repeated episodes or explicit user wording can become a preference. Project contracts need project-specific evidence. Public skill rules need maintainer intent or repeated cross-project evidence.
5. **Write to the right layer.** Use `references/writeback-policy.md` routing. Write short entries with date, source artifact, confidence, and target scope.
6. **Report only the useful summary.** Tell the user what was remembered or which candidates were deferred. Do not ask for confirmation unless the next step would publish private or public-facing policy.

## Default Targets

- Private user preferences: the current agent's private memory area, such as `~/.codex/memories/`, especially for workstation facts, tool aliases, local paths, preferred interaction style, and personal workflow defaults.
- Project preferences: `memory/`, `paper/.agent/`, `code/.agent/`, or `slides/.agent/`, especially for contracts shared by all agents in the project.
- Local scan artifacts: `.agent/sidecars/<task-id>/` or `.agent/personalization/<run-id>/`; keep them untracked unless sanitized and intentionally committed.
- Public reusable skill rules: `skills/<skill-name>/SKILL.md` or `skills/<skill-name>/references/` only during an explicit skill-maintenance task.

## Candidate Record

Use concise records:

```text
- Preference: <one reusable behavior>
- Scope: private-user | project | public-skill-candidate | discard
- Type: workflow | writing | layout | figure-style | code-review | git | compute | toolchain | collaboration
- Evidence: <artifact path or summarized user statement>
- Confidence: observed | repeated | user-stated | inferred
- Target: <memory file or skill file>
- Action: write | defer | promote | reject
```

## Safety Rules

- Do not store private raw trajectory text when a derived rule is enough.
- Do not promote collaborator-specific comments, voice transcriptions, screenshots, or local file paths into public skills.
- Do not let a sidecar write final public memory without main-agent review.
- If a candidate conflicts with existing memory, mark it as `candidate` and leave a short note rather than overwriting the older rule.
- If a preference would change external behavior such as pushing, tagging, releasing, submitting jobs, or publishing issues, record the preference but keep the existing human gate.
