---
name: orchestrate-create-test-plan
description: Orchestrate a branch-based test-plan creation loop with test-plan creator and reviewer workers through agent-orchestrator. Use when user says "orchestrate create test plan", "agent test plan loop", or wants worker-assisted creation of the runtime test plan consumed by /run-test-plan.
---

# Orchestrate Create Test Plan

Coordinate a test-plan-creation loop for the current branch. The test-plan
creator owns the `plans/{branch}/test-plan.md` artifact and should use the
repository `create-test-plan` skill or workflow when available; the reviewer
studies the implementation plan, branch diff, and current draft, answers most
clarification questions, and critiques drafts until the test plan is complete.

The output of this loop is the runtime test-plan runbook consumed by
`/run-test-plan` on the user's local machine. Quality of that runbook directly
determines how much real testing time the user spends per scenario, so coverage
gaps and broken setup SQL must be caught before the test plan is shipped.

Read your repository's agent-orchestrator setup docs (MCP server config,
profiles manifest, package diagnostics) before starting.

## Route And Profile Selection

- Use the validated `plan-creator` profile alias for the test-plan creator.
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

Classify worker proposals before accepting them into the test plan:

- **Routine planning detail:** fills in setup SQL, action steps, verification
  queries, scenario ordering, MCP tool selection, helper snippets, evidence
  surfaces, or fixes to existing scenarios while preserving the user's stated
  scope and accepted behavior. Do not ask the human for these.
- **Human approval required:** changes the test-plan scope, adds or removes a
  feature area not covered by the implementation plan or branch diff, requests
  staging access or real-money provider calls beyond what the implementation
  plan already approves, or substitutes a named technology, MCP tool, or
  capability with a different implementation surface. Promote these to **Open
  Human Decisions** before accepting the change.

Do not let reviewer/creator agreement, "test simplification", "avoiding flaky
scenarios", or "safer" framing override the user's intended coverage. First ask
whether the desired coverage can be preserved with a safer scenario shape. If
preserving it may be impossible or materially changes test value, ask the human
with concrete options.

## Reviewer Prompt Anti-Patterns

Reviewer workers are capable agents with access to the repository's test-plan
skills and rules. The supervisor's reviewer prompt should be a slim handoff:
artifact paths, upstream worker output when useful, the branch diff or scope to
review, and the relevant repository workflow to use.

Avoid these reviewer-prompt failure modes:

- **Plan-compliance-only framing:** do not ask only whether the test plan matches
  the implementation plan. Ask for an independent test-plan review with the plan
  and diff as context.
- **Dimension lists:** do not recreate the test-plan review rubric in the
  prompt. Point to the repository `create-test-plan` and `/run-test-plan`
  workflows and project rules instead.
- **Hint laundering:** do not summarize test-plan creator claims as facts. Pass
  the creator output verbatim when it matters.
- **Positive framing:** do not state intended coverage or setup behavior as
  something to confirm. Let the reviewer derive gaps from the branch diff, draft,
  and repository rules.

If the supervisor notices a genuinely task-specific concern that is not already
in the implementation plan, test-plan draft, diff, upstream worker output, or
repository rules, surface it to the human as an **Open Human Decision**. Do not
smuggle it into the reviewer prompt as a checklist item.

## Workflow

1. **Confirm the branch and test-plan target.** Identify the current branch
   before asking the human for context. Prefer the supervisor context when it
   already contains the target workspace branch; otherwise ask the test-plan
   creator or a lightweight worker to inspect the repository branch with the
   repo's normal git tooling. The test plan target is always
   `plans/{branch-name}/test-plan.md`. If the branch name contains an issue
   number or issue slug, surface it for context but do not require an issue —
   the test plan is keyed by branch, not by issue.
2. **Start workers through agent-orchestrator.** Start or resume worker runs via
   agent-orchestrator MCP tools, using the selected validated profile alias
   settings for each route and the target workspace cwd from supervisor context.
   Wait for each worker response, inspect the output, and send follow-up prompts
   through the same worker sessions as the loop continues.
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
3. **Start the test-plan creator.** Ask the test-plan creator to create the
   runtime test plan for the current branch using the repository
   `create-test-plan` skill or workflow if available. Instruct it to:
    - invoke the repository `create-test-plan` skill (not `create-plan`) and
      follow it faithfully, including any domain-specific runbook guidance the
      skill points at when the branch touches that domain;
    - read `plans/{branch}/plan.md`, all sub-plans, and `git diff main...HEAD`
      (file list and stat) to derive scope; defer to the base skill's behavior
      when the implementation plan is missing rather than inventing a stricter
      precondition;
    - read any existing `plans/{branch}/test-plan.md` first and resume/revise
      that file rather than overwriting, so prior critique iterations are
      preserved;
    - override any interactive clarification loop in the base create-test-plan
      workflow: do not stop to ask the human questions during initial drafting;
    - make routine scenario decisions itself when the implementation plan,
      branch diff, repository context, existing patterns, or approved project
      rules provide enough evidence;
    - verify setup and verification SQL against actual EF entity configurations
      and migrations before writing it (per the base skill's "Use real schema"
      rule);
    - collect unresolved uncertainties as **Reviewer Questions** in the test
      plan for the reviewer to answer first, not as direct human prompts;
    - record explicit behavior invariants and **Human Approval Triggers** when
      the implementation plan or user request depends on a specific staging
      access pattern, real-provider call, public callback route, or capability
      that materially affects how the test plan can be run;
    - clearly separate confirmed scenarios, assumptions, Reviewer Questions,
      Open Human Decisions, risks, and runbook structure (Prerequisites, MCP
      Tools, Runtime Variables, Helper Snippets, Evidence Surfaces, Scenario
      Coverage Map, Scenarios), using `none` for empty sections.
4. **Start the reviewer.** Give the reviewer the implementation plan path,
   current branch, branch diff or diff command, current test-plan draft path,
   test-plan creator output, and repository instructions. Ask it to independently
   review the runbook using the repository `create-test-plan` and
   `/run-test-plan` workflows and project rules as context. It should answer
   Reviewer Questions it can answer from the artifacts and repository context,
   identify blocking coverage, accuracy, or usability defects, identify true
   Open Human Decisions, provide concise feedback for the test-plan creator, and
   say whether the test plan is ready. Do not add a supervisor-authored scenario,
   SQL, financial-flow, or edge-case checklist.
5. **Bridge questions without defaulting to the human.** When the test-plan
    creator records Reviewer Questions, send them to the reviewer first. The
    reviewer should answer or resolve every question it can, then identify only
    the residual **Open Human Decisions**. Only ask the human when both
    conditions are true:
    - the question affects test scope, coverage, staging access, real-provider
      calls, or other capability surfaces; and
    - the reviewer is not confident answering from the implementation plan,
      branch diff, and repository context.
6. **Escalate material scope, capability, or access changes before alignment.**
   If either worker proposes a material scope substitution, addition of
   staging-only scenarios that require new credentials, addition of real-money
   or real-provider calls beyond what the implementation plan approves, public
   callback routing changes, or removal/degradation of a requested coverage
   area, pause the loop and ask the human before accepting it. Present the
   original intent, proposed replacement, why the worker recommends changing it,
   whether there is an option that preserves the original coverage safely,
   risks/tradeoffs, and a clear choice. Do not let reviewer/creator agreement
   override human intent for coverage, named tools, staging boundaries, or
   capability surfaces.
7. **Iterate to alignment.** Pass reviewer answers and feedback to the
    test-plan creator, wait for an updated test plan, then send the updated
    test plan back to the reviewer. If any Reviewer Questions remain, the
    reviewer must either answer them, mark them non-blocking assumptions, or
    promote them to Open Human Decisions with a concise reason and concrete
    options. Continue until:
    - the reviewer says the test plan is ready or has no blocking feedback,
      including no missing scenario coverage against the diff and no
      schema/SQL inaccuracies in setup/verify steps; and
    - the test-plan creator agrees Reviewer Questions are resolved, explicitly
      documented as assumptions, or promoted to Open Human Decisions.
8. **Avoid over-specifying scenarios.** The final test plan should be complete
   enough to guide an interactive `/run-test-plan` session, with clear
   prerequisites, MCP tools, runtime variables, helper snippets, evidence
   surfaces, a coverage map, and concrete scenarios containing setup, action,
   and verification, but should not micromanage every keystroke or assert on
   incidental UI text. Prefer agent-checkable verification (SQL queries, Redis
   reads, log/trace searches) over "visually confirm" steps.
9. **Commit and push the test plan through the test-plan creator.** The
   `plans/{branch}/test-plan.md` file (and any updates to the branch
   `plan.md` index needed to reference it) are normal workflow artifacts. After
   the reviewer and test-plan creator agree the test plan is ready, ask the
   test-plan creator to commit and push only those test-plan workflow files
   unless the human says otherwise. The supervisor must not commit or push
   directly. The test-plan creator should report the commit SHA, pushed branch,
   and exact files included.
10. **Finish with an online handoff.** Give the human the GitHub URL for the
   pushed online test plan, plus a concise summary of the scope covered, MCP
   tools required, prerequisites (including any tunnel or staging access),
   key scenarios, assumptions, risks, and any human scope/access decisions
   made. Do not directly edit source files, run apps, or implement scenarios
   from the supervisor.

## Follow-Up Prompts

Use short, role-specific follow-ups during the loop:

- To the reviewer: "Review the updated test plan for the current branch using
  the repository `create-test-plan` and `/run-test-plan` workflows and project
  rules as context. Inputs: implementation plan path, branch diff or diff
  command, test-plan draft path, and test-plan creator output. Treat creator
  output as claims, not facts. Answer Reviewer Questions you can answer from the
  artifacts and repository context. Report blocking coverage, accuracy, or
  usability defects, true Open Human Decisions, materially useful feedback, and
  whether the test plan is ready."
- To the test-plan creator: "Incorporate the reviewer feedback, update the
  test plan, and list any remaining Reviewer Questions and Open Human
  Decisions. Do not ask the human directly. Only keep questions open when they
  materially affect coverage, staging access, real-provider calls, or other
  capability surfaces and the reviewer could not answer them."
- To the test-plan creator after approval: "The reviewer says the test plan is
  ready. Commit and push only the create-test-plan workflow artifacts for this
  branch (`plans/{branch}/test-plan.md` and any branch `plan.md` index updates
  needed to reference it). Do not include source changes. Report the commit
  SHA, pushed branch, files committed, and the GitHub URL for the test plan."

## Human Escalation Criteria

Escalate to the user only for unclear coverage requirements, staging or
real-provider access, public callback routing, or other capability surfaces
that the reviewer cannot resolve confidently from the implementation plan,
branch diff, and repository context.

Always escalate proposed material scope substitutions, removals or degradations
of requested coverage, or additions of new capability surfaces (new staging
credentials, real-provider calls beyond what the implementation plan approves,
public callback routing changes), even when the reviewer and test-plan creator
agree. The escalation must include the argument for changing scope and the
consequences of preserving the original coverage.
