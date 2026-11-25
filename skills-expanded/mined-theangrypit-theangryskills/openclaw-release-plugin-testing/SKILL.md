---
name: openclaw-release-plugin-testing
description: "Use when proving OpenClaw plugin lifecycle, clean-package behavior, config round-trip, bootstrap or external SDK compatibility."
---

# Release Openclaw Plugin Testing

Codex adaptation of the pinned OpenClaw source. Repository-specific commands apply only to a verified OpenClaw checkout; portable debugger commands apply to their selected process.

## Prove the shipped composition
Use the selected OpenClaw checkout, root/scoped instructions and current package scripts. Read the packaged source's confidence matrices and Package Acceptance branches for bundled lifecycle, config discovery, doctor idempotence, bootstrap, artifact capture and external SDK consumers.

Choose the smallest relevant package/plugin lane using `$openclaw-testing`. Test in a clean task-owned HOME/state root with a free port; install, inspect, enable, disable and uninstall only isolated fixture plugins unless a task explicitly selects another target. Preserve the actual operator config, databases, live Gateway and unrelated processes.

Separate source tests from packed-artifact proof, metadata snapshots from real bootstrap and synthetic channel/provider checks from authorized live probes. A green unit suite does not qualify a release artifact. `doctor` repairs/migrations and package installs require their actual isolated scope or operator approval; the reference is not permission to repair live state.

Verify config discovery and round-trip without leaking credentials, then exercise representative external public-SDK consumers where the change can affect them. Use synthetic fixture secrets; hydrate real provider/channel credentials only through an authorized existing route. No publication or release operation is authorized by this skill.

Report artifact identity, exact command/commit, matrix coverage, fixture/live distinction, lifecycle cleanup and remaining gaps. Stop optional expansion once the changed contract and required gates are sufficiently proven.

## Selective installation

This workflow requires these installed companion skills: `$openclaw-testing`. The installer does not resolve them automatically; select these names together or verify they are already installed.

## Source procedures and boundary

Read [the packaged upstream entrypoint](references/upstream/SKILL.source.md) when using this workflow; its supporting files remain beside it. This root owns Codex invocation, target resolution and authorization. Upstream examples are reference procedures, not grants of access, installation, deployment, publication or another model/provider. Use native Codex tools where capable and preserve an actual refusal. The operator's chosen model, project instructions and source-trust policy remain authoritative.

For repository-owned dependencies and original relative links, use [the source link map](references/upstream-link-map.json) against the verified checkout or its pinned GitHub reference. The pack does not claim that a linked release/channel skill or runtime is installed. Inspect the current owning source before executing a version-sensitive example.

[Provenance and adaptation record](PROVENANCE.md) identifies the source commit, retained resources and changes.
