---
name: rdl-task-bridge
license: CC-BY-4.0
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
description: Bridge spec-kit tasks.md and plan.md into a feature-specific Superpowers SDD plan, then hand completed implementation to branch finishing.
compatibility: Bash 3.2+, awk, git; spec-kit T-number checkbox tasks; Superpowers task-brief with Task N headings (verify installed helper before use)
---

Use this at the spec-kit → `superpowers:subagent-driven-development` seam.
Verify the installed SDD skill and its `task-brief`/`sdd-workspace` contracts before
execution; upstream helpers can change. Canonical sources:
[Superpowers](https://github.com/obra/superpowers) and
[spec-kit](https://github.com/github/spec-kit).

1. Resolve the requested feature’s `tasks.md`, `plan.md`, `spec.md`, project
   constitution and approved analysis record to absolute paths. Read all five. Resolve
   unresolved requirements before dispatching implementers; the adapter adds no
   invented implementation steps or tests. If analysis exists only in the
   conversation, persist its findings, agreed remediations and actual approval
   in a feature-specific record before conversion. Do not invent an approval
   or substitute a placeholder when a source is missing.
2. Generate the combined plan with `bash <this-skill>/scripts/bridge.sh
   "$tasks" "$plan" "$spec" "$constitution" "$analysis"`.
   It emits `## Global Constraints` containing all five source documents and numbered `## Task N`
   sections, preserving original IDs, completion, phase/story/parallel metadata,
   continuation text and the complete source context. Non-task checkboxes remain
   context. Source files stay unchanged; missing/empty context and malformed,
   metadata-only or duplicate tasks fail closed.
3. Save stdout atomically under the target repo’s `.superpowers/plans/` as
   `speckit-<feature>-<identity>.md`. Compute `identity` with
   `printf '%s\n' "$tasks" | git hash-object --stdin` using the absolute task path;
   use the full hash. This basename, unlike `tasks.md`, isolates SDD workspaces
   even for same-named features in different repos/worktrees. On resume, compare
   the generated content with the saved plan and reconcile changed source tasks
   with the SDD ledger before replacing it. Never overwrite a hand-authored plan.
4. Pass **this single generated plan** to SDD. Run the installed `task-brief` on
   the first and last task, and `sdd-workspace` on the generated plan, to verify
   actual compatibility before implementation. Preserve the source-ID mapping
   in the ledger; completed source tasks are verification-only. SDD owns its
   per-task model choices and TDD. Update source checkboxes only after evidence
   confirms completion; source `tasks.md` remains the requirements record.
5. After implementation and the requested review pass, invoke the installed
   `superpowers:finishing-a-development-branch`. Carry forward existing commit,
   push and PR authorization and follow its branch lifecycle choices. Do not
   merge, discard work or remove worktrees without authorization. Resolve PR
   feedback through `git:pr-comments` when requested.

For optional durable GitHub tasks, use the target project’s installed
`speckit.taskstoissues` command after the user requests issue creation. Let that
command run its configured before/after hooks; do not fabricate hook execution.
Record issue URLs beside source IDs and reuse them on resume to avoid duplicates.
