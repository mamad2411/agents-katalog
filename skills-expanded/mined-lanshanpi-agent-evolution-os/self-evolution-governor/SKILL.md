---
name: self-evolution-governor
description: Use for durable self-improvement: corrections, failures, repeated workflows, memory cleanup, or skill changes. NOT for one-off facts. 触发：自进化、复盘、沉淀、遗忘、skill化。
---

# Self Evolution Governor

This skill governs durable self-improvement. Its job is to prevent uncontrolled memory/skill growth while still capturing useful learning.

## When to activate

Use this skill when:

- The user corrects the agent or expresses a stable preference.
- A task fails, is repeated, or requires rework.
- A new workflow is likely to recur.
- The agent wants to update `MEMORY.md`, `TOOLS.md`, `memory/user-model/`, `AGENTS.md`, `SOUL.md`, or any skill.
- The user discusses self-evolution, memory policy, forgetting, parameter tuning, or training data.
- A candidate should be promoted, archived, merged, or rejected.

Do **not** activate for ordinary one-off facts unless they will change future behavior.

## Required protocol

Before changing any durable core file, read:

1. `memory/evolution-os/policy.md`
2. Relevant existing target file, e.g. `MEMORY.md`, `TOOLS.md`, `memory/evolution.md`, target skill, or user-model file.

Then follow this flow:

```text
Signal → Candidate → Classify → Compress → Check duplicate/conflict → Choose target → Promote/Archive → Verify
```

## Default action: candidate first

New learnings default to `memory/evolution-os/inbox/` using the candidate schema in `memory/evolution-os/schemas/candidate-template.md`.

Only skip the inbox when all are true:

1. The user explicitly asked to update a specific file now.
2. The change is low/medium risk.
3. The target is obvious.
4. The content can be compressed and verified immediately.

## Classification guide

- Stable user preference → `memory/user-model/preferences.md` or `MEMORY.md` if globally important.
- Current project status → daily memory first; `MEMORY.md` only if cross-session important.
- Tool/API/local environment fact → `TOOLS.md`.
- Failure or user correction → `memory/hard-cases/` plus candidate if it changes protocol.
- Reusable 5+ step workflow or repeated 2+ times → skill draft.
- Self-evolution architecture/policy → `memory/evolution-os/` or `memory/evolution.md`.
- Training/fine-tuning data → `memory/evolution-os/training-corpus/`, only after validation.

## Core file gate

Before writing core files, answer internally:

1. Will this change future behavior?
2. Is there a more specific target than `MEMORY.md`?
3. Can it be one sentence?
4. Is it duplicate or conflicting?
5. Does it need decay/expiry?
6. Is it low, medium, or high risk?

High-risk changes require user confirmation:

- `AGENTS.md` / `SOUL.md`
- deleting core memory instead of archiving
- changing schedulers/permissions/external actions
- publishing plugins/skills externally
- parameter training or uploading training data

## Promotion rules

A candidate may be promoted when:

- It has a clear target.
- It is compressed.
- It has no unresolved conflict.
- It has an expiry or explicit `permanent` reason.
- It includes a verification step.

Promotion should leave a log in `memory/evolution-os/promoted/` when meaningful.

## Forgetting rules

Prefer degradation over deletion:

```text
active → archive → delete
```

Archive when:

- duplicated by a better rule
- project/tool state expired
- not used after decay window
- too verbose and replaced by distilled summary
- contradicted by newer user instruction

## Output after evolution work

Report briefly:

- Files changed
- What was captured/promoted/archived
- Verification performed
- Any blocked high-risk change
