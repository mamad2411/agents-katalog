---
name: cgagentharness-optimize
description: Find and implement evidence-backed Harness performance or maintainability improvements, with focused drafts when publication is requested.
---

# Optimize the harness

Read `AGENTS.md` and the affected contract in `INVARIANTS.md`. Establish the
checkout, dirty state, default branch and refreshed remote base; preserve
unrelated work. Inspect open PR files and heads before choosing findings.

## Earn the change

Inspect the requested scope, tracing production callers before proposing edits:

- `src/agentic`: exact edits, reviewed-tree approval and process lifecycle.
- Research: `src/server/chat_web/evidence.rs`, `src/common/pdf_text.rs`,
  `src/llm`; compare read counts, worker runs, model tokens and retained evidence.
- `desktop`, packaging scripts: native ownership, sidecar identity and provenance.
- Workflows/tests: meaningful coverage, platform boundaries and exact-head gates.
- Guidance: stale claims, broken references and duplicate owner sections.

For each finding, record the concrete trigger, location, impact and verification.
Large files or newer dependencies alone do not justify changes. Measure the
actual bottleneck on equivalent baseline/candidate workloads before claiming a
speedup. For repeated goal reads, separate cache reuse, refresh and digest
inference; check retained passages and citations as well as cost. Diagnose
baseline failures. Report a no-op if no change earns its place.

## Implement and verify

Group related changes to shared files into one concern. Independent drafts
start from current `origin/main` and target `main`; deliver dependent work after
its prerequisite lands, then refresh and check overlap again.

Use existing helpers and preserve security contracts. Follow `AGENTS.md` for
scoped static, runtime and native checks. Lint changed workflows and inspect
the scripts they invoke. State which surfaces you exercised.

For guidance, edit the owner, check references and lower trimmed word caps.

## Deliver within scope

When publication is requested, complete the commit, push and draft PR using the
repository template and validator. Otherwise deliver the local result. Verify
remote head and report current CI separately from review and mergeability;
monitor to completion when requested. Preserve the user's merge/release limits.
