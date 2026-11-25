---
name: orchestrate-create-plan
description: Orchestrate an issue-based planning loop with plan creator and reviewer workers through agent-orchestrator. Use when user says "orchestrate create plan", "agent plan loop", or wants worker-assisted plan creation.
---
<!-- Generated from .agents/ by scripts/sync-ai-workspace.mjs. Do not edit directly. -->


# Orchestrate Create Plan

Coordinate a plan-creation loop for a GitHub issue. The plan creator owns the
plan and should use the repository create-plan skill or workflow when available;
the reviewer studies the issue, answers most clarification questions, and
critiques drafts until the plan is complete.

Read your repository's agent-orchestrator setup docs (MCP server config,
profiles manifest, package diagnostics) before starting.

## Route And Profile Selection

- Use the validated `plan-creator` profile alias for the plan creator.
- Use the validated `plan-reviewer` profile alias for the reviewer.
- Do not hard-code provider, model, effort, service tier, or context settings in
  this skill. The user controls those concrete settings in the profiles
  manifest.
- Start worker runs with `start_run` using `profile`, `profiles_file`, and the
  target workspace cwd from supervisor context.
- If the required validated profile aliases are unavailable, stop and ask the
  user to configure valid profiles before starting worker runs.
- If the user asks the supervisor to repair a worker profile, use
  `list_worker_profiles` diagnostics and `upsert_worker_profile`. Do not start a
  worker just to edit the profiles manifest.

## Decision Classification And Approval

Classify worker proposals before accepting them into the plan:

- **Routine planning detail:** fills in implementation steps, chooses local
  code structure, selects existing repository commands, or plans small bugfixes
  while preserving the user's stated goal and accepted behavior. Do not ask the
  human for these.
- **Human approval required:** changes product scope, user-facing behavior,
  public CLI/MCP/API contracts, worker orchestration flow, permission/tool
  surfaces, security boundaries, release/publish behavior, dependency policy, or
  substitutes a named technology/API/SDK/capability. Promote these to **Open
  Human Decisions** before accepting the change.

Do not let reviewer/creator agreement, security hardening, simplification, or
"safer" implementation language override the user's requested behavior. First
ask whether the desired behavior can be preserved with a safer implementation.
If preserving it may be impossible or materially changes tradeoffs, ask the
human with concrete options.

## Reviewer Prompt Anti-Patterns

Reviewer workers are capable agents with access to the repository's planning
skills and rules. The supervisor's reviewer prompt should be a slim handoff:
artifact paths, upstream worker output when useful, the issue or scope to
review, and the relevant repository workflow to use.

Avoid these reviewer-prompt failure modes:

- **Plan-compliance-only framing:** do not ask only whether the draft matches
  what the plan creator said. Ask for an independent plan review with the issue
  and repository context available.
- **Dimension lists:** do not recreate the planning/review rubric in the prompt.
  Point to the repository create-plan workflow and project rules instead.
- **Hint laundering:** do not summarize plan-creator claims as facts. Pass the
  creator output verbatim when it matters.
- **Positive framing:** do not state intended plan properties as something to
  confirm. Let the reviewer derive gaps and decisions from the issue, draft, and
  repository rules.

If the supervisor notices a genuinely task-specific concern that is not already
in the issue, plan draft, upstream worker output, or repository rules, surface it
to the human as an **Open Human Decision**. Do not smuggle it into the reviewer
prompt as a checklist item.

## Workflow

1. **Confirm the branch and issue target.** Identify the current branch before
   asking the human for an issue. Prefer the supervisor context when it already
   contains the target workspace branch; otherwise ask the plan creator or a
   lightweight worker to inspect the repository branch with the repo's normal
   git tooling. If the branch name contains an issue number or issue slug,
   derive the GitHub issue target from it and have workers fetch/read that
   issue. Ask the human for an issue URL/number only when the branch and user
   request do not identify one clearly.
2. **Start workers through agent-orchestrator.** Start or resume worker runs via
   agent-orchestrator MCP tools, using the selected validated profile alias
   settings for each route and the target workspace cwd from supervisor context.
   Wait for each worker response, inspect the output, and send follow-up prompts
   through the same worker sessions as the loop continues.
   For the initial draft, the plan creator and plan reviewer are sequential:
   start the plan creator, wait for its plan artifact and final output, then
   start or follow up the reviewer with that artifact path and creator output.
   Do not use a single `spawn_workers`/parallel group for creator + reviewer on
   the initial draft, because the reviewer can race the draft write and return a
   stale missing-artifact verdict.
   Use bounded waits and adaptive check-ins: first wait about 30 seconds to catch
   startup, auth, model, quota, or protocol failures, then inspect
   `get_run_status` and recent events. Compare `last_activity_at`,
   `last_activity_source`, `latest_error`, `timeout_reason`, and
   `terminal_reason` with the previous check-in. If activity is advancing and no
   fatal latest error is present, back off toward roughly 2 minutes, 5 minutes,
   and then a 10-15 minute ceiling appropriate for the task. Do not cancel a
   worker only because elapsed wall-clock time is high; cancel or escalate only
   on explicit user request, clear no-activity evidence past the idle window, a
   fatal latest error, or a deliberate stop/restart recovery path. For known
   quiet work, choose a larger `idle_timeout_seconds` when starting the run.
3. **Start the plan creator.** Ask the plan creator to create an implementation
    plan for the issue using the repository create-plan skill or workflow if
    available. Instruct it to:
    - inspect the issue and relevant repository context;
    - override any interactive clarification loop in the base create-plan
      workflow: do not stop to ask the human questions during initial drafting;
    - make routine planning decisions itself when the issue, repository context,
      existing patterns, or approved project rules provide enough evidence;
    - collect unresolved uncertainties as **Reviewer Questions** in the plan for
      the plan reviewer to answer first, not as direct human prompts;
    - record explicit behavior invariants and **Human Approval Triggers** when
      the issue or user request depends on a specific workflow, permission
      surface, public contract, integration, or capability;
    - write or update the repository-native plan in the location selected by
      the create-plan workflow;
    - clearly separate confirmed decisions, assumptions, Reviewer Questions,
      Open Human Decisions, risks, and implementation tasks, using `none` for
      empty sections.
4. **Start the reviewer only after the draft exists.** Give the reviewer the
    issue, current plan draft path, plan creator output, current branch, and
    repository instructions. Ask it to independently review the draft using the
    repository create-plan workflow and project rules as context. It should
    answer Reviewer Questions it can answer from the issue and repository
    context, identify blocking plan defects or true Open Human Decisions,
    provide concise feedback for the plan creator, and say whether the plan is
    ready. Do not add a supervisor-authored checklist or summary of plan-creator
    claims.
5. **Bridge questions without defaulting to the human.** When the plan creator
    records Reviewer Questions, send them to the reviewer first. The reviewer
    should answer or resolve every question it can, then identify only the
    residual **Open Human Decisions**. Only ask the human when both conditions
    are true:
    - the question affects product requirements, user-facing behavior, scope, or
      acceptance criteria; and
    - the reviewer is not confident answering from the issue and repository
      context.
6. **Escalate material behavior or scope changes before alignment.** If either
   worker proposes a material scope substitution, behavior change, permission or
   tool-surface change, public contract change, release/publish policy change,
   or removal/degradation of a requested capability, pause the loop and ask the
   human before accepting it. Present the original intent, proposed replacement,
   why the worker recommends changing it, whether there is an option that
   preserves the original behavior safely, risks/tradeoffs, and a clear choice.
   Do not let reviewer/creator agreement override human intent for product
   scope, acceptance criteria, named technologies, workflow behavior, permission
   surfaces, or user-facing behavior.
7. **Iterate to alignment.** Pass reviewer answers and feedback to the plan
    creator, wait for an updated plan, then send the updated plan back to the
    reviewer. If any Reviewer Questions remain, the reviewer must either answer
    them, mark them non-blocking assumptions, or promote them to Open Human
    Decisions with a concise reason and concrete options. Continue until:
    - the reviewer says the plan is ready or has no blocking feedback; and
    - the plan creator agrees Reviewer Questions are resolved, explicitly
      documented as assumptions, or promoted to Open Human Decisions.
8. **Avoid over-specifying implementation.** The final plan should be complete
   enough to guide a developer, with clear scope, decisions, risks, tasks,
   acceptance criteria, and quality gates, but should not micromanage every
   implementation detail.
9. **Commit and push the plan through the plan creator.** Repository-native plan
   files and plan index files created by the create-plan workflow are normal
   workflow artifacts. After the reviewer and plan creator agree the plan is
   ready, ask the plan creator to commit and push only those plan workflow files
   unless the human says otherwise. The supervisor must not commit or push
   directly. The plan creator should report the commit SHA, pushed branch, and
   exact files included.
10. **Finish with an online handoff.** Give the human the GitHub URL for the
   pushed online plan, plus a concise summary of the plan, key decisions,
   assumptions, risks, and any human scope decisions made. Do not directly edit
   source files or implement the plan from the supervisor.

## Follow-Up Prompts

Use short, role-specific follow-ups during the loop:

- To the reviewer: "Review the updated plan for the issue using the repository
  create-plan workflow and project rules as context. Inputs: issue, plan draft
  path, and plan creator output. Treat creator output as claims, not facts.
  Answer Reviewer Questions you can answer from the issue and repository
  context. Report blocking plan defects, true Open Human Decisions, materially
  useful feedback, and whether the plan is ready."
- To the plan creator: "Incorporate the reviewer feedback, update the plan, and
  list any remaining Reviewer Questions and Open Human Decisions. Do not ask the
  human directly. Only keep questions open when they materially affect
  implementation, approved behavior, permission/tool surfaces, public contracts,
  or product requirements and the reviewer could not answer them."
- To the plan creator after approval: "The reviewer says the plan is ready.
  Commit and push only the create-plan workflow artifacts for this plan and the
  branch index. Do not include source changes. Report the commit SHA, pushed
  branch, files committed, and the GitHub URL for the plan."

## Human Escalation Criteria

Escalate to the user only for unclear product requirements that the reviewer
cannot answer confidently, such as final scope boundaries, user-facing behavior,
business rules, acceptance criteria, or tradeoffs that require product judgment.

Always escalate proposed material scope substitutions, behavior changes,
permission/tool-surface changes, public contract changes, release/publish policy
changes, or removals/degradations of requested capabilities, even when the
reviewer and plan creator agree. The escalation must include the argument for
changing scope and the consequences of preserving the original behavior.
