---
name: drift-dev
description: Implement AI-assisted code changes without introducing LLM-drift. Use when the user invokes $drift-dev, asks to edit Drift-protected code, fixes a Drift violation, changes critical behavior, or needs implementation that preserves locked contracts, SSOT provenance, and required proof.
---

# Drift Dev

Use this skill during implementation. The LLM-drift risk is that the agent hardcodes a value that must come from an SSOT, weakens a locked contract, hides unsupported flow behind a helper, or changes more behavior than the user requested.

The goal is to make the smallest correct code change while preserving local contracts and ending with actionable proof.

## Workflow

1. If the change starts from a product/user prompt, read `{{DRIFT_COMMAND}} context --task "<user prompt>"` before planning or ask `$drift-cm` for it.
2. Read `{{DRIFT_COMMAND}} context <file>` before editing known target files.
3. Identify locked contracts, SSOTs, and invariants that constrain the change.
4. If the request conflicts with a locked contract, stop and report the conflict before editing.
5. Edit code without changing locked contracts unless the user explicitly requested an intentional contract change.
6. Preserve SSOT provenance. Prefer direct values from declared sources or verified helpers over local copies, fallbacks, or hardcoded values.
7. If contracted files changed, run or report `{{DRIFT_COMMAND}} diff --summary` before finalizing.
8. Run the required Drift checks, usually `{{DRIFT_COMMAND}} check --changed` for focused work or `{{DRIFT_COMMAND}} check` for broader changes.
9. If Drift checks fail, run or report `{{DRIFT_COMMAND}} explain` or `{{DRIFT_COMMAND}} explain <contract-id>` before proposing a fix.
10. For PR handoff, include `{{DRIFT_COMMAND}} proof --git-base <ref>` when a Git base is available.
11. If a locked contract must intentionally change, prepare `{{DRIFT_COMMAND}} accept <contract-id> --reason "<reason>"` but do not use it as a workaround for accidental drift.

## Commands

Use the configured Drift command prefix:

```txt
{{DRIFT_COMMAND}}
```

Build concrete Drift commands by appending the subcommand, for example `{{DRIFT_COMMAND}} context --task "<user prompt>"`, `{{DRIFT_COMMAND}} context <file>`, `{{DRIFT_COMMAND}} coverage`, `{{DRIFT_COMMAND}} diff --summary`, `{{DRIFT_COMMAND}} check --changed`, `{{DRIFT_COMMAND}} explain <contract-id>`, `{{DRIFT_COMMAND}} proof --git-base <ref>`, or `{{DRIFT_COMMAND}} accept <contract-id> --reason "<reason>"`.

For non-Drift checks, inspect the target project's scripts first and only run commands that exist in that project.

## Rules

```txt
- Do not remove or weaken @drift contracts to make checks pass.
- Do not inline values that must come from an SSOT.
- Do not bypass drift/ssot-flow by mentioning the SSOT without deriving the sink from it.
- Do not use accept for accidental drift or unclear product intent.
- Keep edits tightly scoped to the requested behavior.
```

## Output

Return an `Implementation Handoff` with:

```txt
Changed files:
Contract impact:
Drift diff:
Checks:
Explain diagnostics:
PR proof:
Remaining risks:
```

Read `references/pre-edit-checklist.md` before editing and `references/post-edit-checklist.md` before final response.
Read `references/examples.md` when the user asks for examples, adoption guidance, or greenfield/brownfield workflows.
