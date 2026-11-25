---
name: durable-learning-protocol
description: Governed long-term memory for AI agents: scores each candidate learning for confidence and usefulness, saves only what clears the bar, and keeps contexts in separate namespaces. Use when the user asks to capture, save, propose, audit, review, prune, or structure durable learnings; when an automation should preserve reusable knowledge; or at the end of substantive work where future assistants would benefit from persistent memory. Apply especially for preferences, workflows, pitfalls, tools, operational rules, and research findings that should carry across sessions while keeping separate contexts (for example work, personal, or one client) apart.
---

# Durable Learning Protocol

The store lives at `memory/learnings/<namespace>/<date>-<key>.json` under your workspace root, managed only by `scripts/learnings.py` (`add | list | retire | compile | prune`). Never hand-edit those files or read the compiled `_views/*.jsonl` whole; the `durable-learning` plugin's hooks block both and load the store at every session start.
Run `scripts/learnings.py` from your workspace root (or set `LEARNINGS_ROOT`); the store is resolved from the git top-level of the current directory.

## Overview

Use this skill to identify reusable learnings from a run and decide whether to save, stage, update, supersede, or reject them. Treat this as governed long-term agent memory: external persistent memory, not model training.

## Workflow

1. Review the task outcome and ask what would save the user time, prevent mistakes, improve future analysis, or preserve a stated preference.
2. Exclude one-off facts, temporary statuses, generic advice, secrets, account numbers, sensitive client details, and financial specifics unless the user explicitly requests preservation.
3. Keep contexts separate with `namespace`: `global` for rules that apply everywhere, plus one lowercase-hyphenated namespace per context (`work`, `personal`, `client-acme`). Reuse existing namespaces (`learnings.py list` shows them) before inventing one.
4. Classify each candidate by `memory_type` and practical `type`.
5. Score `confidence` and `usefulness` from 1-10.
6. Check for duplicate, conflicting, stale, or superseded existing learnings when a memory store or relevant wiki/note is available.
7. Save only when automatic saving is authorized and both scores are 8 or higher. Otherwise, propose the learning in a `Learnings To Save` section.

## Memory Types

- `semantic`: Stable facts, preferences, context boundaries, reusable source knowledge, or decision rules.
- `episodic`: A past event, task, example, or observed outcome that may help future work.
- `procedural`: A reusable workflow, operating rule, checklist, command sequence, or process.
- `investigation`: A research finding or hypothesis that should be checked again or carried forward.

## Practical Types

- `preference`: the user's stated preference, priority, working style, target geography, context boundary, or decision rule.
- `pattern`: A repeatable workflow, source pattern, signal, heuristic, or recurring analysis frame.
- `pitfall`: A recurring risk, trap, false assumption, compliance issue, or due-diligence warning.
- `tool`: A useful source, system, command, database, website, or workflow tool.
- `operational`: A project-specific process detail that saves time next run.
- `investigation`: A finding from research that should be checked again or carried forward.

## Memory Object

Use this JSON shape for saved or proposed learnings:

```json
{
  "namespace": "global|<your-namespace>",
  "memory_type": "semantic|episodic|procedural|investigation",
  "skill": "TASK_OR_ASSISTANT_NAME",
  "type": "preference|pattern|pitfall|tool|operational|investigation",
  "key": "short-kebab-case-key",
  "insight": "One clear sentence stating the reusable learning.",
  "confidence": 1-10,
  "usefulness": 1-10,
  "source": "user-stated|observed|inferred",
  "evidence": "Short note explaining why this should be remembered.",
  "files": [],
  "status": "active|superseded|deprecated|rejected",
  "lifecycle": "stable|review|expires",
  "review_after": "YYYY-MM-DD|null"
}
```

## Scoring Rules

- Use `source: "user-stated"` and higher confidence when the user explicitly said it.
- Use `source: "observed"` when the assistant saw it in files, tools, or repeated workflow behavior.
- Use `source: "inferred"` and lower confidence when it is a reasonable conclusion but not directly stated.
- Score `confidence` for truth/reliability.
- Score `usefulness` for likely future value.
- Save automatically only when the user has authorized automatic saving and both `confidence` and `usefulness` are 8 or higher.
- Propose instead of saving when either score is below 8, when sensitivity is unclear, or when write access is unavailable.

## Lifecycle Rules

- Use `stable` for durable preferences, recurring context boundaries, and long-lived operating rules.
- Use `review` for workflows, tools, or assumptions that may change.
- Use `expires` for time-sensitive research, temporary policies, deadlines, or market/program findings.
- Use `review_after` with a concrete date for time-sensitive or reviewable memory.
- Use `status: "superseded"` instead of duplicating a learning when a newer rule replaces an older one: add the new entry, then `learnings.py retire OLD_KEY --by NEW_KEY`.
- Use `status: "deprecated"` when a learning is retained for history but should not guide future work.
- Use `status: "rejected"` for proposed memory intentionally not saved as active.

## Output Pattern

When saving is not performed, end with:

```json
[
  {
    "namespace": "global",
    "memory_type": "procedural",
    "skill": "durable-learning-protocol",
    "type": "operational",
    "key": "example-key",
    "insight": "One reusable sentence.",
    "confidence": 8,
    "usefulness": 8,
    "source": "observed",
    "evidence": "Short reason.",
    "files": [],
    "status": "active",
    "lifecycle": "stable",
    "review_after": null
  }
]
```

Keep the section short: usually 2-5 learnings. If there are no worthwhile learnings, say so plainly.
