---
name: code-authoring
description: Bounded code authoring and editing with source-first analysis, risk and execution gates, and validation truth. Use when the user asks to write, edit, refactor, or fix code in a repository.
disable-model-invocation: true
---

# code-authoring

Apply this skill for any explicit code-writing or code-editing request.

Required gate sequence before any file mutation:

1. Risk classification (`prompts/150_global_risk_gate.md`).
2. Intent and stage routing (`prompts/151_intent_stage_router.md`).
3. No-assumption contract (`prompts/153_assumption_ban_contract.md`).
4. Execution control (`prompts/154_execution_control.md`).
5. Tool permission policy (`prompts/155_tool_permission_policy.md`).
6. Human approval protocol when destructive (`prompts/156_human_approval_protocol.md`).
7. Secret-aware behavior if credentials may be touched (`prompts/158_secret_and_runtime_credentials.md`).

Authoring contract (`prompts/14_bounded_code_authoring.md`):

- Inspect the actual repository, language, framework, conventions, and existing tests before writing.
- Stay inside the requested scope. Do not silently refactor unrelated code, change deps, or touch generated files.
- Prefer minimal diffs unless a refactor is explicitly authorized.
- Write or update tests when behavior changes.
- Cite the source paths you read and the diffs you produced.
- Run validators that exist in the repo (lint, test, build, type-check); report each command and pass or fail.
- Never claim validation that did not actually run.

Diff-mode and patch-mode constraints:

- For surgical edits use `prompts/144_diff_only_code_authoring.md` and `prompts/145_minimal_patch_mode.md`.
- For large changes, reduce per `prompts/146_large_diff_reduction.md` and classify risk per `prompts/147_patch_risk_classifier.md`.

Refactor flows: pair with `refactor-strict` skill and `prompts/11_refactoring_execution_bounded.md`.

Hard stops:

- Destructive Git or release operation requested → escalate via `prompts/156_human_approval_protocol.md`.
- Apparent secret value in code or input → switch to `prompts/158_secret_and_runtime_credentials.md`.
- Implementation cannot be done without source the user did not provide → return a `minimum_input_request` instead of guessing.

Output:

- Exact file paths changed.
- Behavior changed.
- Tests added or updated.
- Validation run (with exact commands and exit status).
- Validation not run (with reason).
- Assumptions, blockers, and rollback notes.
