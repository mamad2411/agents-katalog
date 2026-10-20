---
description: Mandatory code review gate; persist REVIEW.md and diffs under docs/reviews
alwaysApply: true
---

# Wave close review

A wave is **not complete** when the last sub-task is coded. Run this gate before “Wave N concluída”, “DoD met”, or Wave N+1. Full protocol: `.cursorrules` §9 and §13.

## Sequence

1. Freeze (no new features). Re-read the wave DoD in `docs/IMPLEMENTATION_PLAN.md`.
2. Diff what actually changed.
3. Independent subagents (they did not write the code): DoD gaps, trust/IPC, cross-package contracts, tests, later-wave correlations.
4. You also walk the §9.4 checklist (product intent).
5. Fix **Blocker + High**. Medium unless the user defers. Low = residual risk.
6. Re-typecheck / re-test. Delta-review non-trivial fixes.
7. **Persist** `docs/reviews/WXX/REVIEW.md` + `DIFF.patch` (+ `DIFF-post-review.patch` if you fixed findings). Write missing ADRs to `docs/ADR/`.
8. Report in chat with paths. Then close the wave.

Chat is not a substitute for files on disk. Do not delete old review folders.

## Hunt for

Gaps vs DoD; TODOs standing in for features; later-wave code that snuck in; missing schema **hooks**; DTO drift; untyped IPC; secrets in renderer/logs; silent fallback; new send paths bypassing caps; missing i18n; no tests for new contracts; empty/error/offline crashes; undocumented architecture decisions (missing ADR).

Reviewers do not implement. You synthesize, fix, and **write the docs**. Do not skip the gate if a review subagent is unavailable — review with file reads and say so.
