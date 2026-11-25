---
name: orchestrate-implement-plan
description: Orchestrate implementation of an approved repository plan with implementer and reviewer workers through agent-orchestrator. Use when user says "orchestrate implement plan", "agent implementation loop", or wants worker-assisted implementation.
---

# Orchestrate Implement Plan

Coordinate implementation of an approved repository-native plan. The implementer
owns code changes and should use the repository `implement-plan` workflow or
skill when available. The reviewer independently audits the resulting diff,
with the approved plan as context. The supervisor coordinates the loop through
worker runs and does not directly edit source, commit, or push.

Read your repository's agent-orchestrator setup docs (MCP server config,
profiles manifest, package diagnostics) before starting.

## Route And Profile Selection

- Use the validated `implementation` profile alias for the implementer.
- Use the validated `code-review` profile alias for the reviewer.
- Do not hard-code provider, model, effort, service tier, or context settings in
  this skill. The user controls those concrete settings in the profiles
  manifest.
- If the required validated profile aliases are unavailable, stop and ask the
  user to configure valid profiles before starting worker runs.
- If the user asks the supervisor to repair a worker profile, use
  `list_worker_profiles` diagnostics and `upsert_worker_profile`. Do not start a
  worker just to edit the profiles manifest.

## Context Isolation Rules

- Start the implementer as a **new worker run**. Do not resume the plan-creation
  worker or include the plan-creation transcript. The approved plan and current
  repository state should be sufficient context.
- After the implementer finishes the initial implementation pass, start the
  reviewer as a **new worker run**. Do not resume plan-creation workers or reuse
  the supervisor's plan-creation discussion as reviewer context.
- During implementation review iterations, reuse the same implementer and
  reviewer sessions with follow-up prompts. The implementer keeps the context of
  the full implementation, and the reviewer keeps the context of prior findings
  and fixes.

## Change Classification And Approval

Classify every implementer proposal and reviewer finding before turning it into
work:

- **Routine fix:** small bugfixes, local implementation corrections, tests,
  docs, evidence updates, and refactors that preserve the approved plan,
  accepted behavior, public contracts, permission/tool surfaces, and user-facing
  workflow. Workers should handle these without interrupting the human.
- **Human approval required:** any change that modifies or removes an approved
  capability, changes product or user-facing behavior, alters CLI/MCP/API
  contracts, changes worker orchestration flow, permission/tool surfaces,
  security boundaries, release/publish behavior, dependency policy, or replaces
  a named technology/API/SDK. These must become **Open Human Decisions** before
  implementation.

Security or code-review feedback is not permission to change scope by itself.
When a finding exposes risk in an approved behavior, first look for a fix that
preserves the behavior. If the available fix would materially change behavior or
tooling, pause and ask the human with options.

## Reviewer Prompt Anti-Patterns

Reviewer workers are capable agents with access to the repository's review
skills and rules. The supervisor's reviewer prompt should be a slim handoff:
artifact paths, upstream worker output when useful, the diff or scope to review,
and the relevant repository workflow to use.

Avoid these reviewer-prompt failure modes:

- **Plan-compliance-only framing:** do not ask only whether the implementation
  satisfies the plan. Ask for an independent repository review with the plan as
  context.
- **Dimension lists:** do not recreate the review rubric in the prompt. Point to
  `/review`, `/review-pr`, or the relevant repository skill instead.
- **Hint laundering:** do not summarize implementer claims as facts. Pass the
  implementer output verbatim when it matters.
- **Positive framing:** do not state intended behavior as something to confirm.
  Let the reviewer derive behavior from the diff, plan, and repository rules.

If the supervisor notices a genuinely task-specific concern that is not already
in the plan, diff, upstream worker output, or repository rules, surface it to the
human as an **Open Human Decision**. Do not smuggle it into the reviewer prompt
as a checklist item.

## Workflow

1. **Preflight the workspace.** Confirm the target workspace cwd from supervisor
   context and check the current branch/status through a lightweight worker or
   the implementer. Treat existing uncommitted changes as user-owned unless they
   were created in the current orchestration. If unrelated or risky dirty files
   exist, stop and ask the human before implementation begins.
2. **Start the implementer.** Start a new worker run via agent-orchestrator MCP
   `start_run` using the `implementation` profile alias, the configured
   `profiles_file`, and the target workspace cwd. Ask it to:
   - follow the repository `implement-plan` workflow or skill;
   - locate the current branch plan/index using the repository workflow;
   - read `AGENTS.md`, relevant `.agents/rules/`, the approved plan, affected
     source, tests, and docs;
   - implement tasks narrowly and update plan evidence as required by the
     repository workflow;
   - preserve the plan's approved behavior, public contracts, orchestration
     workflow, and permission/tool surfaces unless the human explicitly approves
     changing them;
   - stop and report an **Open Human Decision** if a safe fix appears to require
     changing approved behavior or removing/degrading a requested capability;
   - run the narrowest meaningful verification, then broader checks if feasible;
   - avoid committing, pushing, or changing unrelated files during this pass;
   - report changed files, task status, verification commands/results, residual
     risks, and blockers.
3. **Monitor responsibly.** Use bounded waits and adaptive check-ins. First wait
   briefly to catch startup, auth, model, quota, or protocol failures, then
   inspect status/events as needed. Do not cancel a worker only because elapsed
   wall-clock time is high; cancel or escalate only on explicit human request,
   clear idle/fatal evidence, or a deliberate stop/restart recovery path.
4. **Start the reviewer after implementation.** Start a new worker run via
   `start_run` using the `code-review` profile alias, the configured
   `profiles_file`, and the target workspace cwd. Give the reviewer only the
   approved plan path, current branch, repository instructions, implementer's
   final output, and current working tree diff or diff command. Ask it to use
   the repository `/review` workflow or skill if available, with the plan and
   implementer output as context rather than conclusions. The reviewer should
   report blocking findings first, then non-blocking suggestions and test gaps,
   and say explicitly whether the implementation is ready. Do not add a custom
   verification checklist or supervisor-authored summary of what the
   implementation is supposed to have preserved.
5. **Iterate with existing sessions.** If the reviewer has blocking or material
   feedback, classify it first. Send routine fixes to the existing implementer
   session with `send_followup`. If the feedback would change approved behavior,
   scope, public contracts, permission/tool surfaces, security boundaries,
   release/publish behavior, dependency policy, or remove/degrade a requested
   capability, pause and ask the human before asking the implementer to make
   that change. For routine fixes, ask the implementer to fix the findings,
   update plan evidence, rerun the relevant verification, and report what
   changed. Then send the implementer's response back to the existing reviewer
   session with `send_followup` for re-review. Pass the implementer response
   verbatim and ask for a fresh judgment on the updated diff, not confirmation
   of the supervisor's expectations. Continue until:
   - the reviewer says there are no blocking findings and the implementation is
     ready; and
   - the implementer agrees all review feedback has been addressed or explicitly
     documented as a non-blocking residual risk.
6. **Escalate only true blockers.** Human escalation is not needed for ordinary
   implementation tradeoffs or behavior-preserving review fixes. Ask the human
   only when the plan cannot be implemented as written, a required
   product/scope/behavior decision blocks progress, a permission/tool-surface or
   public-contract change is proposed, a requested capability would be removed
   or degraded, a dependency or external-service action needs approval, or
   workers disagree on a material issue they cannot resolve from the plan and
   repo.
7. **Collect remaining human decisions before commit.** Before asking for the
   final commit/push, explicitly list every unresolved human decision at the end
   of the status update, even when the workers consider the implementation
   otherwise ready. Include dependency/version choices, audit or verification
   policy decisions, external-service approvals, release-readiness exceptions,
   and any deferred scope/product choices. Ask the human to answer these in one
   pass so the implementation can be finished cleanly. Do not bury these items
   under residual risks or treat a failing release-quality gate as merely
   informational.
8. **Commit and push through the implementer after alignment and decisions.** Once implementer
   and reviewer are aligned and both approve the current implementation, ask the
   implementer to commit and push the implementation only after required human
   decisions have been answered or explicitly deferred by the human. The
   supervisor must not commit or push directly. The implementer should include
   only intended implementation files and plan evidence files, exclude
   unrelated/user-owned changes, and report the commit SHA, pushed branch, files
   committed, and any files intentionally left uncommitted.
9. **Finish with a handoff.** Tell the human the pushed branch/commit, concise
   implementation summary, reviewer outcome, verification evidence, residual
   risks or deferred work, whether any local uncommitted files remain, and a
   final **Open Human Decisions** section. If there are no remaining decisions,
   say "Open Human Decisions: none." If decisions remain, list each one with the
   available options and the consequence of leaving it open.

## Follow-Up Prompts

- Initial implementer: "Use the repository `implement-plan` workflow. Locate
  the approved plan for the current branch, implement it task by task, update
  plan evidence, run relevant verification, and report changed files, results,
  risks, and blockers. Preserve approved behavior, public contracts,
  orchestration workflow, and permission/tool surfaces. If a safe fix appears to
  require changing any of those, stop and report an Open Human Decision with
  options. Do not commit or push yet."
- Initial reviewer: "Use the repository `/review` workflow or skill to review
  the current working tree diff. Inputs: approved plan path, current branch, and
  the implementer's final output. Treat those inputs as context, not as
  conclusions. Report blocking findings first, then non-blocking suggestions and
  test gaps. Say explicitly whether the implementation is ready."
- Reviewer feedback to implementer: "Address the reviewer feedback below in
  this existing implementation session. Keep changes scoped and preserve
  approved behavior, public contracts, workflow, and permission/tool surfaces
  unless the human explicitly approved a change. Update plan evidence, rerun
  relevant verification, and report what changed plus any remaining risks."
- Implementer response to reviewer: "Re-review the updated diff in this
  existing review session. Inputs: prior reviewer findings and the implementer's
  response below. Treat the response as claims to verify. Report remaining
  blockers, new blockers, non-blocking suggestions, and whether it is ready."
- Human decision summary: "The implementation is otherwise ready. Before commit
  and push, here are the remaining human decisions needed to finish cleanly:
  [numbered list with options and consequences]. Please answer each item or
  explicitly defer it."
- Final commit request to implementer: "The reviewer says the implementation is
  ready, the human has answered or explicitly deferred remaining human decisions,
  and you agree the plan feedback is addressed. Commit and push only the intended
  implementation and plan evidence files. Exclude unrelated or user-owned
  changes. Report commit SHA, pushed branch, files committed, and any files left
  uncommitted."

## Human Escalation Criteria

Escalate only when implementation is blocked by something the plan and
repository context cannot resolve, such as a required product/scope decision,
behavior change, permission/tool-surface or public-contract change, dependency
change approval, external-service write, persistent failing quality gate that
changes acceptance, removal/degradation of a requested capability, or an
irreconcilable material disagreement between implementer and reviewer.

Do **not** escalate small bugfixes, local implementation corrections, tests, or
docs that preserve the approved behavior. Do **not** silently implement a
review-suggested behavior/scope/tooling change merely because it is framed as a
bugfix, simplification, or security hardening; promote it to **Open Human
Decisions** first.

Do **not** escalate merely to run existing repository setup, build, test, or
verification commands such as `pnpm install --frozen-lockfile`, `pnpm build`,
`pnpm test`, or `pnpm verify`. Those commands are normal implementation
management when they use the repository's existing lockfile/scripts and do not
add, remove, or change dependencies. Escalate only if a worker needs to modify
dependency manifests/lockfiles, install a new dependency, publish, run an
external-service write, or change the planned acceptance criteria.

When a release-quality gate fails because of a dependency, audit, packaging, or
policy issue, treat it as an open human decision unless the approved plan already
authorizes the exact remediation. Surface it in the final **Open Human
Decisions** list before commit/push instead of leaving it only as a residual
risk.
