---
name: openclaw-test-performance
description: "Use when measuring and improving OpenClaw test/plugin-suite wall time, import costs, CPU or peak RSS with coverage preserved."
---

# Openclaw Test Performance

Codex adaptation of the pinned OpenClaw source. Repository-specific commands apply only to a verified OpenClaw checkout; portable debugger commands apply to their selected process.

## Measure the real suite shape
Resolve the selected checkout and scoped agent/plugin/channel/Gateway test instructions. Read the packaged source for grouped reports, extension batches, import-duration flags, profiling and package-boundary commands. Verify these entrypoints exist in the current checkout before running them.

Record a like-for-like baseline: command/config, exact commit, worker budget, machine/load, wall time, test/import time and peak RSS. Start with the smallest relevant file or plugin batch; for bundled plugin breadth, prefer the narrowest `pnpm test:extensions:batch <plugin[,plugin...]>` or plugin-inspector command before a full extension sweep. Collect broader ranking only for an explicit performance question that needs it. Distinguish harness noise and shared-worker module retention from a test body hotspot or app-object leak.

Repair the owning metadata/import/lifecycle/fixture cause, preserve the contract coverage and rerun the same workload. Do not delete expensive proof merely for speed. For growing memory read `$openclaw-test-heap-leaks`; for packaging-sensitive plugin changes read `$openclaw-release-plugin-testing`. Use `$openclaw-testing` and existing `$openclaw-crabbox` for runner choice.

Preserve dependency-install ownership and separate Vitest cache paths across concurrent checkouts. Missing dependencies require the applicable install authorization; upstream pnpm-install examples are not a grant. Do not benchmark a shared live Gateway under source-test authority.

Report before/after seconds, CPU and peak RSS, coverage changes, exact commands/commits and residual noise. A gain measured under different machine/load/worker conditions is not a proven optimization. Commit/push only when the task authorizes them.

## Selective installation

This workflow requires these installed companion skills: `$openclaw-testing`. The installer does not resolve them automatically; select these names together or verify they are already installed.

Conditional companions: `$openclaw-test-heap-leaks` for heap/RSS investigation; `$openclaw-release-plugin-testing` for package-artifact-sensitive plugin work; `$openclaw-crabbox` for selected remote proof. Select them only for that branch.

## Source procedures and boundary

Read [the packaged upstream entrypoint](references/upstream/SKILL.source.md) when using this workflow; its supporting files remain beside it. This root owns Codex invocation, target resolution and authorization. Upstream examples are reference procedures, not grants of access, installation, deployment, publication or another model/provider. Use native Codex tools where capable and preserve an actual refusal. The operator's chosen model, project instructions and source-trust policy remain authoritative.

For repository-owned dependencies and original relative links, use [the source link map](references/upstream-link-map.json) against the verified checkout or its pinned GitHub reference. The pack does not claim that a linked release/channel skill or runtime is installed. Inspect the current owning source before executing a version-sensitive example.

[Provenance and adaptation record](PROVENANCE.md) identifies the source commit, retained resources and changes.
