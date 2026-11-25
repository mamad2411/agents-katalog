---
name: openclaw-python-debugpy
description: "Use when Python debugging needs pdb, post-mortem state, breakpoints, a headless debugpy session or exact-PID attach."
---

# Python Debugpy

Codex adaptation of the pinned OpenClaw source. Repository-specific commands apply only to a verified OpenClaw checkout; portable debugger commands apply to their selected process.

## Choose the debugger
Start with the smallest command that reaches the failure. Use `python3 -m pdb script.py` without source edits, `breakpoint()` for a task-owned source change, or post-mortem pdb for an unhandled exception. Use debugpy only when remote/headless attach or a service startup race needs it.

Read the packaged source for command forms and debugger navigation. Check the active Python environment and installed debugpy first; its upstream conditional pip-install example is not installation permission. Do not add debugpy to project dependencies or change ptrace/container privileges unless that change is authorized.

Confirm the exact PID and owner before attach, keep ports on loopback, and use distinct ports where needed. PID attach injects code and may pause the target: preserve shared-process boundaries. Do not use a debugger to bypass a refused credential, filesystem or network action.

Before finishing, resume retained processes, remove task-added debugging statements, and rerun the normal project proof without a debugger. Report the failing frame, observed values with private data excluded, root cause and normal command result. A successful attach is not verification of the fix.

## Selective installation

No mandatory installed companion from this pack is required. Checkout/runtime prerequisites and the conditional source references still apply.

## Source procedures and boundary

Read [the packaged upstream entrypoint](references/upstream/SKILL.source.md) when using this workflow; its supporting files remain beside it. This root owns Codex invocation, target resolution and authorization. Upstream examples are reference procedures, not grants of access, installation, deployment, publication or another model/provider. Use native Codex tools where capable and preserve an actual refusal. The operator's chosen model, project instructions and source-trust policy remain authoritative.

For repository-owned dependencies and original relative links, use [the source link map](references/upstream-link-map.json) against the verified checkout or its pinned GitHub reference. The pack does not claim that a linked release/channel skill or runtime is installed. Inspect the current owning source before executing a version-sensitive example.

[Provenance and adaptation record](PROVENANCE.md) identifies the source commit, retained resources and changes.
