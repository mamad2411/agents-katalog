---
name: openclaw-test-heap-leaks
description: "Use when investigating OpenClaw Vitest OOMs, test RSS growth, heap retention or a runtime closure-leak regression."
---

# Openclaw Test Heap Leaks

Codex adaptation of the pinned OpenClaw source. Repository-specific commands apply only to a verified OpenClaw checkout; portable debugger commands apply to their selected process.

## Separate test retention from runtime leakage
Read `$openclaw-test-performance` for current workload/profiling routes, then the packaged source for heap collection, snapshot comparison and dedicated runtime validation. Match the real entrypoint, configuration, worker budget and PID before classifying growth.

RSS is triage evidence, not proof of a leak. A sampling `.heapprofile` is not a `.heapsnapshot`. Compare equivalent snapshots from the same PID, inspect positive allocation families, and use dominators/retainers to distinguish transformed module graphs from retained app objects, timers, handles, buffers and caches.

The bundled read-only snapshot helper is `references/upstream/scripts/heapsnapshot-delta.mjs`. Invoke it with Node and two task-owned snapshots, or its documented `--lane-dir` selection. It does not need to be installed into the OpenClaw repo. Heap captures can contain private data: keep them local/scoped and out of public changes.

For a runtime closure fix, use the selected checkout's dedicated producer described in the source, including its pre-fix/synthetic-leak sensitivity controls. Do not retrofit an unrelated harness merely to obtain a PASS. Fix process lifetime or cleanup at the evidenced owner, then repeat the same producer/workload and normal test proof.

Report same-PID/source identities, retained families, retainer support, overhead and leak classification as proven, likely or inconclusive. A lower peak RSS alone does not establish the runtime objects were released.

## Selective installation

This workflow requires these installed companion skills: `$openclaw-test-performance`, `$openclaw-testing`. The installer does not resolve them automatically; select these names together or verify they are already installed.

## Source procedures and boundary

Read [the packaged upstream entrypoint](references/upstream/SKILL.source.md) when using this workflow; its supporting files remain beside it. This root owns Codex invocation, target resolution and authorization. Upstream examples are reference procedures, not grants of access, installation, deployment, publication or another model/provider. Use native Codex tools where capable and preserve an actual refusal. The operator's chosen model, project instructions and source-trust policy remain authoritative.

For repository-owned dependencies and original relative links, use [the source link map](references/upstream-link-map.json) against the verified checkout or its pinned GitHub reference. The pack does not claim that a linked release/channel skill or runtime is installed. Inspect the current owning source before executing a version-sensitive example.

[Provenance and adaptation record](PROVENANCE.md) identifies the source commit, retained resources and changes.
