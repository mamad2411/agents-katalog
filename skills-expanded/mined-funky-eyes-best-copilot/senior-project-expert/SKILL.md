---
name: senior-project-expert
description: "Compatibility entrypoint for runtimes that resolve the Senior Project Expert name as a skill instead of the Senior Project Expert agent. Runs the same init preflight before PM/coordinator workflow."
---

# Senior Project Expert Compatibility Skill

This is a compatibility alias, not a second role definition. Prefer the real Senior Project Expert agent when the runtime supports agents. If this skill is loaded instead, execute the same lightweight init gate before any target-repository work.

## Boot Sequence

1. Load or invoke `core-workflow-contract` and `senior-project-expert-workflow`.
2. Run `repo-init-gate` before classification, broad search, planning, review, dispatch, or implementation.
3. Prefer the helper when shell execution is available:
   `repo-init-gate/scripts/run-preflight.sh <target-root> claude`.
4. If helper execution is unavailable, read only target-root `best-copilot.md`, parse only YAML frontmatter, compare the `version` to the current `repo-init-gate` contract, and emit `## Repo Init Gate`.
5. If the sentinel is current, record `INIT_SCAN=SKIP_SENTINEL_READY` and continue with `senior-project-expert-workflow`.
6. If the sentinel is missing, unreadable, invalid, stale, or explicit repair was requested, run the scan bootstrap helper or load `repo-init-scan` on demand. Continue only after `required_artifacts_verified: yes`, `sentinel_written: yes`, and `next_task_ready: yes`.

`Skill(...) Successfully loaded` is not execution evidence. The transcript must show the gate result, and scan output only when the gate fails. Do not load or run `repo-init-scan` on a current sentinel.

## After The Gate

Follow `senior-project-expert-workflow`: classify, freeze the shared six-block packet, choose named specialist lanes where needed, fan in structured handbacks, verify before completion, and use the native continuation/closeout gate when available.

For non-micro target-repository work, keep the visible trail compact:

```text
INIT_GATE -> [INIT_SCAN if needed] -> CLASSIFY -> FREEZE_PACKET -> LANE_SELECTION -> EXECUTOR_LANES -> FAN_IN -> NEXT_GATE
```
