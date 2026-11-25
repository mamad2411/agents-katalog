---
name: dissertation-agent-self-debug
description: Diagnose and recover from dissertation agent failures such as false runs, repeated tool loops, stale assumptions, context drift, wrong-window behavior, or environment-state mismatches before retrying.
---

# Dissertation Agent Self Debug

Use this skill when the agent appears stuck, repeats actions, claims work without evidence, uses the wrong window role, misreads local state, or drifts from the user's actual dissertation maintenance task.

## Purpose

Adapt ECC agent-introspection debugging to this dissertation system. The goal is controlled recovery: capture the failure, classify the cause, verify the real state, take the smallest safe action, and record a prevention note if needed.

## Activate For

- false-run suspicion: claims a file was checked or edited without evidence
- repeated tool calls with no progress
- wrong-window behavior: Production work in Maintenance Window or system maintenance in Production Window
- context drift from current task
- stale memory conflicting with local files
- missing files after an expected write
- tool or browser state mismatch
- source-layer and visible-surface mismatch, such as a commit/tag/file existing while the rendered GitHub, Obsidian, browser, Word/PDF, or release page still shows stale or incomplete information
- user reports that the system feels unreliable

## Four-Phase Loop

### 1. Failure Capture

Record:

- task goal
- last successful step
- failed or suspicious behavior
- files/tools involved
- current assumption that needs verification
- whether participant data or formal documents are involved

Use:

```text
Failure capture:
- Task:
- Symptom:
- Last verified step:
- Suspect assumption:
- Files/tools:
- Risk level:
```

### 2. Root-Cause Diagnosis

Classify the issue:

| Pattern | Likely Cause | Check |
|---|---|---|
| false completion | answer based on memory, not local evidence | inspect actual file/path/output |
| loop / no progress | repeated plan or repeated command | inspect recent actions and stop retries |
| context drift | old task or old window role dominates | restate current user request and window role |
| stale memory | TASK_STATE or wiki outdated | compare local files and latest task entry |
| wrong source | inferred facts used as confirmed facts | run source-first gate |
| tool state mismatch | browser, cwd, renderer, Obsidian, or config not as assumed | verify actual surface |
| surface mismatch | source layer changed but user-visible surface was not checked | compare file/git state with rendered page, app view, exported file, or public repo surface |

### 3. Contained Recovery

Take the smallest safe action:

1. restate the current objective in one sentence
2. verify the real file/tool state
3. narrow to one failing surface
4. fix only confirmed issues
5. update `research-wiki/TASK_STATE.md` if the failure affects future work

Do not claim that hidden state was reset unless an actual tool action proves it.

When the failure involves public release, Obsidian, browser, Word/PDF, Canvas, or GitHub visibility, verify the user-visible surface before saying the issue is fixed. A local file, commit, tag, or script output is not enough if the user's concern is what they can see in an app or public page.

### 4. Debug Report

For non-trivial failures, write or report:

```text
Agent self-debug report:
- Failure:
- Root cause:
- Recovery action:
- Evidence:
- Result:
- Preventive rule:
```

## Guardrails

- Do not hide failures behind confident summaries.
- Do not retry the same action repeatedly.
- Do not modify formal dissertation documents during a system debug unless the user explicitly asks.
- Do not store raw participant data in debug notes.
