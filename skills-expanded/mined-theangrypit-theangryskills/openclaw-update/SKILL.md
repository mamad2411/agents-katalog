---
name: openclaw-update
description: "Use when explicitly asked to update one existing OpenClaw installation through its verified owner while preserving state."
---

# Openclaw Update

Codex adaptation of the pinned OpenClaw source. Explicit operator selection is required for live update/connection actions.

## Resolve and retain the existing update owner
Read the selected installation's existing owner runbook; record host, runtime user, profile/state/config roots, running binary/version, service manager and update owner. Inspect actual runtime state before choosing commands. A global CLI or the current checkout may describe another installation.

Read the packaged source for supported update-owner routes, interruption/recovery and post-update verification. Map upstream team-server/live-updater references to the selected local owner; do not create another deployer, scheduler, installation or authentication profile. No host, model or credential is selected by this skill.

Preserve configuration, session history, databases, credentials and unrelated work. Inspect `openclaw update status --json` through the actual owner to establish the intended target. Dirty-source reconciliation, stashing, restarts, migrations and security/credential changes retain the applicable exact-target authorization. Do not overwrite local edits to make an update work.

Use the supported managed update/Doctor path only in its authorized scope. For LaunchAgent self-stop refusal, hand off normal execution through the existing manager/external route; do not invent a new service or headless workaround. For macOS signing, follow the selected installation's documented signing and authentication path; preserve native Keychain permissions and signing controls.

After the selected update, inspect that same binary/process, `health --json`, deep status and a task-relevant real flow where available. Verify state preservation and target-version readback. Keep package/version success separate from live runtime recovery and pending plugin migrations. Report exact owner, versions, proof and remaining gaps; an update command exit alone is not completion.

## Selective installation

No mandatory installed companion from this pack is required. Checkout/runtime prerequisites and the conditional source references still apply.

## Source procedures and boundary

Read [the packaged upstream entrypoint](references/upstream/SKILL.source.md) when using this workflow; its supporting files remain beside it. This root owns Codex invocation, target resolution and authorization. Upstream examples are reference procedures, not grants of access, installation, deployment, publication or another model/provider. Use native Codex tools where capable and preserve an actual refusal. The operator's chosen model, project instructions and source-trust policy remain authoritative.

For repository-owned dependencies and original relative links, use [the source link map](references/upstream-link-map.json) against the verified checkout or its pinned GitHub reference. The pack does not claim that a linked release/channel skill or runtime is installed. Inspect the current owning source before executing a version-sensitive example.

[Provenance and adaptation record](PROVENANCE.md) identifies the source commit, retained resources and changes.
