---
name: openclaw-diagnose-gateway
description: "Use when diagnosing OpenClaw Gateway, config, channel, model, SecretRef or listener failures without changing state."
---

# Diagnose Gateway

Codex adaptation of the pinned OpenClaw source. Repository-specific commands apply only to a verified OpenClaw checkout; portable debugger commands apply to their selected process.

## Diagnose without repairing
Resolve the requested host, installation/profile, runtime user, state root and Gateway through the existing owner runbook. A shell executable does not establish that it owns the requested Gateway. Preserve named-machine access boundaries.

Run bounded checks through that installation: `openclaw doctor --lint`, `openclaw gateway status --deep`, `openclaw config validate`, `openclaw channels status`, and `openclaw models status`. Inspect channel logs or the exact listener only when the symptom needs them. Check current help if a command differs from the pinned source.

`doctor --lint` can exit 1 for findings; read the report and continue independent checks. Ordinary `doctor` and `doctor --non-interactive` may migrate state even without `--fix`; they are not substitutes for read-only diagnosis. Report redacted SecretRef owner state, never secret values. Correlate timestamps to identify the first failing boundary.

Use the packaged source playbook for condition signatures and the smallest read-only repeat/probe. Do not change config, approve devices, restart services, kill listeners or run a fix under a diagnostic request. Report observed state, causal evidence, inconclusive checks and the exact next authorized repair. Incidental diagnostic logs/cache bookkeeping are distinct from configuration or state repair.

## Selective installation

No mandatory installed companion from this pack is required. Checkout/runtime prerequisites and the conditional source references still apply.

## Source procedures and boundary

Read [the packaged upstream entrypoint](references/upstream/SKILL.source.md) when using this workflow; its supporting files remain beside it. This root owns Codex invocation, target resolution and authorization. Upstream examples are reference procedures, not grants of access, installation, deployment, publication or another model/provider. Use native Codex tools where capable and preserve an actual refusal. The operator's chosen model, project instructions and source-trust policy remain authoritative.

For repository-owned dependencies and original relative links, use [the source link map](references/upstream-link-map.json) against the verified checkout or its pinned GitHub reference. The pack does not claim that a linked release/channel skill or runtime is installed. Inspect the current owning source before executing a version-sensitive example.

[Provenance and adaptation record](PROVENANCE.md) identifies the source commit, retained resources and changes.
