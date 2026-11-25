---
name: openclaw-node-inspect-debugger
description: "Use when debugging Node.js breakpoints, async hangs, hidden locals, heap retention or CPU hot paths with the inspector."
---

# Node Inspect Debugger

Codex adaptation of the pinned OpenClaw source. Repository-specific commands apply only to a verified OpenClaw checkout; portable debugger commands apply to their selected process.

## Reach the failing frame
Choose the smallest reproduction first. Prefer `node inspect path/to/script.js`; for TypeScript use the project's existing TS loader with `--inspect-brk`. Debug one test file with one worker and the owning repository wrapper. Inspect current Node/tool help before relying on version-sensitive flags.

Read the packaged source for inspector REPL commands, breakpoints, source maps, scripted CDP, CPU profiles and heap snapshots. Confirm PID, process owner, exact code and inspector target before attaching to a running process. Signalling or injecting a debugger into a shared process requires the applicable owner authorization; a debugging skill grants none.

Bind inspector ports to loopback, select distinct ports for distinct targets, and do not expose a debugging endpoint or install CDP tooling implicitly. Reuse an existing dependency when suitable. Keep profiles and potentially private heap captures in task-owned storage and out of public diffs.

After the session, resume a process that should continue, release only owned resources, remove temporary breakpoints from intended changes, and rerun the normal failing command without the debugger. Report the reproduced boundary, captured evidence, fix and normal proof; an inspector connection alone is not a repaired bug.

## Selective installation

No mandatory installed companion from this pack is required. Checkout/runtime prerequisites and the conditional source references still apply.

## Source procedures and boundary

Read [the packaged upstream entrypoint](references/upstream/SKILL.source.md) when using this workflow; its supporting files remain beside it. This root owns Codex invocation, target resolution and authorization. Upstream examples are reference procedures, not grants of access, installation, deployment, publication or another model/provider. Use native Codex tools where capable and preserve an actual refusal. The operator's chosen model, project instructions and source-trust policy remain authoritative.

For repository-owned dependencies and original relative links, use [the source link map](references/upstream-link-map.json) against the verified checkout or its pinned GitHub reference. The pack does not claim that a linked release/channel skill or runtime is installed. Inspect the current owning source before executing a version-sensitive example.

[Provenance and adaptation record](PROVENANCE.md) identifies the source commit, retained resources and changes.
