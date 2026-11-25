---
name: orchestrate-resolve-pr-comments
description: Orchestrate PR comment resolution with triage, review, implementation, code review, push, and replies through agent-orchestrator. Use when user says "orchestrate resolve PR comments", "agent PR feedback loop", or wants worker-assisted PR comment resolution.
---

# Orchestrate Resolve PR Comments

Coordinate resolution of pull request feedback using the repository
`resolve-pr-comments` workflow as the triage source of truth. The supervisor
coordinates worker runs and does not directly edit source, commit, push, or post
GitHub replies. The resolution map drives implementation and final replies.

Read your repository's agent-orchestrator setup docs (MCP server config,
profiles manifest, package diagnostics) before starting.

## Route And Profile Selection

- Use the validated `pr-comment-triage` profile alias for fetching comments,
  independently assessing them, and creating/updating the resolution map.
- Use the validated `pr-comment-reviewer` profile alias for reviewing the
  resolution map before implementation.
- Use the validated `implementation` profile alias for implementing approved
  resolution-map fixes.
- Use the validated `code-review` profile alias for reviewing implemented fixes.
- Use the validated `pr-comment-responder` profile alias for posting replies and
  resolving GitHub threads after fixes are committed and pushed.
- Do not hard-code provider, model, effort, service tier, or context settings in
  this skill. The user controls concrete settings in the profiles manifest.
- If required profile aliases are unavailable, stop and ask the user to
  configure valid profiles before starting worker runs.
- If the user asks the supervisor to repair a worker profile, use
  `list_worker_profiles` diagnostics and `upsert_worker_profile`. Do not start a
  worker just to edit the profiles manifest.

## Review Comment Decision Gate

PR review comments are inputs to triage, not permission to change the feature's
approved behavior. Classify every proposed resolution before implementation:

- **Routine fix:** small bugfixes, local code changes, tests, docs, reply text,
  or behavior-preserving security hardening within the approved PR scope. Workers
  should resolve these without interrupting the human.
- **Decline or defer:** incorrect comments, out-of-scope polish, duplicate
  feedback, or follow-up candidates. Record the rationale and draft reply.
- **Human approval required:** any resolution that changes product/user-facing
  behavior, public CLI/MCP/API contracts, worker orchestration flow,
  permission/tool surfaces, security boundaries, release/publish behavior,
  dependency policy, accepted risk, or removes/degrades a requested capability.
  Put these in **Open Human Decisions** with concrete options before
  implementation.
- **Human-authored comments are pre-approved.** When the deciding human is the
  author of a PR review/conversation comment that requests a behavior, scope, or
  contract change, classify the resolution as **Fix** rather than **Human
  Approval Required**. The author has already made the call by raising the
  comment. Note the author identity in the resolution-map analysis so the
  reviewer can verify it.
- **Repository-rule mandates count as approval for the surface they govern.**
  When a public-contract or boundary change is explicitly required by an
  in-scope repository rule (e.g., an `AGENTS.md` file, a rule under
  `.agents/rules/`, or `CLAUDE.md`), classify as **Fix** and cite the rule by
  path. Do not extend this carve-out to changes the rule does not directly
  mandate.

When a review comment exposes a real risk in an approved behavior, first look
for a fix that preserves that behavior. If the proposed fix changes behavior or
removes a capability, ask the human whether to preserve the original behavior
with a safer implementation, accept the behavior change, or defer.

## Reviewer Prompt Anti-Patterns

Reviewer workers are capable agents with access to the repository's PR-comment
and review skills. The supervisor's reviewer prompt should be a slim handoff:
artifact paths, upstream worker output when useful, PR/diff scope, and the
relevant repository workflow to use.

Avoid these reviewer-prompt failure modes:

- **Plan-compliance-only framing:** do not ask only whether the map or
  implementation follows the previous worker's plan. Ask for an independent
  repository review with the map or plan as context.
- **Dimension lists:** do not recreate the triage or code-review rubric in the
  prompt. Point to `resolve-pr-comments`, `/review`, `/review-pr`, or the
  relevant repository skill instead.
- **Hint laundering:** do not summarize triage or implementer claims as facts.
  Pass upstream output verbatim when it matters.
- **Positive framing:** do not state intended resolutions or implemented fixes as
  something to confirm. Let the reviewer derive gaps from PR comments, maps,
  diffs, and repository rules.

If the supervisor notices a genuinely task-specific concern that is not already
in the PR comments, resolution map, diff, upstream worker output, or repository
rules, surface it to the human as an **Open Human Decision**. Do not smuggle it
into the reviewer prompt as a checklist item.

## Workflow

1. **Preflight.** Confirm the target workspace cwd, current branch, PR number or
   URL, profiles file, and working tree state. Treat unrelated dirty files as
   user-owned. If risky dirty files exist, stop and ask before proceeding.
2. **Start triage as a fresh run.** Start `pr-comment-triage` with
   `start_run` using `profile`, `profiles_file`, and supervisor cwd. Ask it to
   use the repository `resolve-pr-comments` skill to:
   - identify the PR from the prompt, branch, or GitHub metadata;
   - fetch PR metadata, changed files, reviews, review comments, review
     threads, and conversation comments;
   - fetch the current CI/check status for the PR head from GitHub or the
     repository's configured CI provider, including failing, cancelled, skipped,
     and pending checks;
   - filter already resolved threads, bot noise, and prior AI replies with
     hidden correlation markers;
   - independently verify AI reviewer comments against the code;
   - create or update `plans/{branch-name}/resolution-map.md`;
   - override any interactive "one comment at a time" behavior in the base
     workflow: triage every actionable comment in one pass, do not stop after
     each comment, and do not ask the human questions during initial triage;
   - make routine decisions itself when safe: fix as suggested, obvious
     behavior-preserving alternative fix, decline incorrect comments with
     rationale, defer clearly out-of-scope polish, or mark follow-up issue
     candidates without creating issues yet;
   - collect unresolved uncertainties as **Reviewer Questions** in the
     resolution map instead of asking the human directly; reserve **Open Human
     Decisions** only for questions that remain after reviewer review;
   - treat verified bugs, regressions, test gaps, and plan-compliance gaps that
     are within the PR's approved scope as fix items by default, even when the
     fix is non-trivial, as long as the fix preserves the approved behavior and
     requested capability;
   - include failing CI/checks as fix items by default when they are caused by
     the PR or by ordinary repository drift that must be cleaned up before the
     PR can merge; classify unrelated infrastructure outages or external
     service incidents separately with evidence and a draft reply/status note;
   - mark any proposed behavior, public-contract, workflow, permission/tool
     surface, security-boundary, release/publish, dependency-policy, or
     capability-removal change as **Human Approval Required** instead of an
     implementation item, subject to the Review Comment Decision Gate carve-outs
     (human-authored comments and repository-rule mandates are pre-approved as
     Fix even when they touch the surfaces above);
   - include reply drafts and enough implementation detail for a fresh
     implementer to work from the map without re-reading the triage transcript.
3. **Review the resolution map as a fresh run.** Start `pr-comment-reviewer`
   with fresh context: PR identifier, branch, resolution-map path, triage output,
   repository instructions, current diff or diff command, and current CI/check
   summary. Ask it to independently review the map using the repository
   `resolve-pr-comments` workflow and project rules as context. It should answer
   Reviewer Questions it can answer from the PR, map, diff, CI/check output, and
   repository context; report blocking map defects, true Open Human Decisions,
   and materially useful feedback; and say whether the map is ready for the Step
   5 human-approval checkpoint. Do not add a supervisor-authored checklist or
   summary of triage claims.
4. **Iterate triage/reviewer.** Send reviewer feedback to the existing triage
   session with `send_followup`; then ask the existing map reviewer to re-review.
   Continue until the reviewer says the map is ready for the Step 5
   human-approval checkpoint, regardless of whether Open Human Decisions
   remain. Implementation never starts before Step 5.
5. **Present resolution map summary for human approval.** Before
   implementation, present a concise summary of the resolution map for human
   review. This is a hard go/no-go checkpoint — do not start implementation
   until the human approves. The summary must let a human who has not read
   the PR diff approve, redirect, or abort the plan.

   Format the summary like this:

   - **Header line**: PR number, branch, totals (fix / decline / defer /
     human-approval) and CI/check status.
   - **Body, grouped by business intent (not by file or comment ID)**:
     cluster entries that share a single business motivation — for example
     "tighten scanner submit contract", "fix domain event durability gap",
     "improve replay UX", "test coverage gaps". Two sentences per cluster:
     - WHAT changes, in user-facing or business terms.
     - WHY — the underlying reason (verified bug, regulatory requirement, UX
       defect, audit-trail gap, contract hardening, etc.).
     If the cluster touches shared infrastructure, cross-cutting
     abstractions, pipeline behaviors, base classes, public contracts, or
     anything consumed by code outside the immediate PR scope, add a third
     bullet: BLAST RADIUS — name the consumers and what could change for
     them.
   - **Open Human Decisions** as a numbered list with options and
     consequences. Include behavior, public-contract, workflow,
     permission/tool-surface, release/publish, dependency-policy,
     accepted-risk, or capability-removal changes even if both workers
     recommend them, subject to the Review Comment Decision Gate carve-outs
     (human-authored comments and repository-rule mandates are pre-approved
     as Fix and do not need to appear here). Follow-up issue creation for
     items in `defer` status or implementer-declined-for-scope items is
     pre-authorized at Step 11 and does NOT need to appear here — list it
     under Open Human Decisions only when the issue body itself encodes a
     new product or scope decision (e.g. a new public contract, a
     dependency policy change, a deprecation announcement) that goes
     beyond capturing the deferred work.
   - **Architectural sanity-check callouts**: a short list of entries whose
     fix introduces new abstractions, modifies cross-cutting behavior, or
     adds a code path that may duplicate an existing platform mechanism.
     Phrase each as a one-line question the human can answer fast — for
     example "does this overlap with an existing pipeline/middleware?", "is
     this re-implementing something the existing transactional or
     event-dispatch machinery already handles?", "does this add a new
     public contract that duplicates an existing one?". Do not require
     code knowledge to answer; phrase in terms of platform concepts the
     human already owns.
   - End the summary with: **Proceed to implementation? (yes / change X /
     abort)**.

   Sizing: aim for under roughly 40 lines total for a typical PR. Avoid line
   numbers, type names, namespaces, and function signatures unless they
   carry business meaning. The goal is "human can decide go/no-go in one
   screen", not "human re-reads the diff".

   Do not start implementation until the human says proceed. If the human
   redirects specific items, send the redirection back to the existing
   triage session as a follow-up, then re-present the updated summary. Even
   when no Open Human Decisions remain and no architectural sanity-check
   callouts apply, the summary still gets presented — every PR gets an
   explicit go/no-go gate.
6. **Start implementation as a fresh run.** Start `implementation` with the
   approved resolution map, PR identifier, branch, and repo instructions. Ask it
   to implement only approved fix actions from the map, skip deferred/declined
   items and human-approval-required changes that were not explicitly approved,
   update plan evidence, run relevant verification, re-check or clearly account
   for previously failing CI/checks where possible, and avoid GitHub replies. Do
   not commit or push yet.
7. **Review implemented fixes as a fresh run.** Start `code-review` with fresh
   context: resolution map path, implementer output, current working tree diff,
   PR identifier, and repository instructions. Ask it to use the repository
   `/review` or `/review-pr` workflow as appropriate, with the resolution map as
   context. It should report blocking findings first, then non-blocking
   suggestions and test gaps, and state whether the implementation is ready. Do
   not add a per-fix verification checklist or summarize implementer claims as
   facts.
8. **Iterate implementation/review.** Send blocking or material reviewer
   feedback to the existing implementer session. Then send the implementer's
   response back to the existing code-review session. Continue until both align.
9. **Final human-decision checkpoint (safety net).** Step 5 is the primary
   go/no-go gate. Use Step 9 only if implementation or code review
   introduced new or changed Open Human Decisions, architectural concerns,
   or scope/behavior questions beyond what the human already approved at
   Step 5. If nothing new emerged, say `Open Human Decisions: none.` Do not
   hide release, dependency, external-write, or behavior-changing decisions
   under residual risks.
10. **Commit and push through a worker.** After alignment and final human
    decisions are answered or explicitly deferred, ask the implementer to commit
    and push only intended PR-comment-resolution files and plan evidence. Always
    include the final `plans/{branch-name}/resolution-map.md` and relevant
    `plans/{branch-name}/plans/` evidence files; these are part of the PR comment
    resolution record and should be pushed unless the human explicitly excludes
    them. The supervisor must not commit or push directly. The implementer must
    report the commit SHA, pushed branch/ref, verification evidence, files
    committed, files intentionally left uncommitted, and residual risks.
11. **Create follow-up issues for deferred and material out-of-scope
    declines.** After the commit/push lands, walk the resolution map and
    create GitHub follow-up issues for:
    - Every entry whose decision is `defer`. Bundle multiple defers into
      one issue when they share a single root cause (e.g., "OpenAPI
      generator pipeline" rather than per-property issues); otherwise
      file one issue per defer.
    - Implementer-declined non-blocking suggestions where the recorded
      rationale is "would balloon scope" or "out of this PR's scope"
      rather than "incorrect comment / false positive". Bundle these
      into a single tech-debt issue scoped to the current PR (e.g.,
      "PR #N test-coverage follow-ups") — do NOT file one issue per
      declined suggestion.

    Each issue body must include:
    - Link back to the originating PR by URL, and to specific PR comment
      URLs when available.
    - A concise statement of what the work is and why it was deferred or
      declined-for-scope (the original rationale verbatim is fine).
    - The proposed approach if the resolution map captured one.
    - The affected files / surfaces.

    Issue creation runs through a `generalist` worker (`gh issue create`).
    The supervisor does NOT call GitHub directly. Do not pause to ask
    the human to approve each issue body — the user has authorized this
    step in advance for any item in `defer` status or any
    declined-for-scope item the implementer recorded a rationale for.
    Pause only if a `defer` lacks enough context to write a sensible
    issue body, or if the supervisor uncovers a new product/scope
    decision while drafting.

    After issues are filed, the supervisor records the issue numbers
    and URLs and uses them in Step 12's responder run so defer replies
    on PR comments can reference the tracking issue (e.g., "Deferred to
    issue #N") instead of vague "follow-up PR" wording.

    If there are NO defers and NO declined-for-scope suggestions in this
    cohort, this step is a no-op — record `Follow-up issues: none.` in
    the handoff and proceed to Step 12.
12. **Reply and resolve after push.** Start `pr-comment-responder` only after the
    commit is pushed. Give it the final resolution map, pushed commit/branch,
    PR identifier, and repository `resolve-pr-comments` reply rules. It may
    automatically post replies and resolve threads according to the approved
    resolution map without asking again, provided the map's final
    `Open Human Decisions` section is `none` or all listed decisions were
    explicitly answered/deferred by the human. It should:
    - post the pre-drafted replies with hidden/correlation markers;
    - resolve only threads marked resolved or declined;
    - leave deferred or escalated threads open unless the map says otherwise;
    - report each reply posted, each thread resolved, and each skipped thread.
    - For entries in `defer` status, the reply must reference the follow-up
      issue created in Step 11 by number and URL — e.g., "Deferred to issue
      #N <link>" — so the trail is discoverable from the PR side. The
      resolution map's reply draft will need updating to swap any
      "follow-up PR" placeholder for the actual issue reference; the
      responder is authorized to do this substitution at post time when
      the supervisor passes the issue numbers in.
13. **Finish with a handoff.** Tell the human the pushed commit, PR URL,
    responder outcome, verification evidence, residual risks, final working tree
    state, and final **Open Human Decisions** section.

## Follow-Up Prompts

Use the role-specific prompt templates in `references/follow-up-prompts.md`.

## Human Escalation Criteria

Escalate only true decisions the workers cannot safely decide from the PR,
resolution map, approved plan, and repository context: product/scope changes,
requested behavior changes, plan/acceptance ambiguity, security/release policy,
permission/tool-surface or public-contract changes, dependency/external-service
approval, removal/degradation of a requested capability, accepted-risk changes,
or material disagreement between workers. The Review Comment Decision Gate
carve-outs apply here: human-authored comments and repository-rule mandates are
pre-approved as Fix and must not be escalated even when they touch the surfaces
above.

Do **not** escalate verified bugs, regressions, missing tests, or
plan-compliance gaps merely because the fix is non-trivial, touches important
code, or was labeled major by a reviewer. If the comment points to behavior the
approved plan already requires, or a defect in the implementation under review,
the default decision is to fix it in the PR. Escalate only if fixing it would
require changing the approved behavior, expanding scope beyond the PR/plan,
choosing between materially different product semantics, or accepting a known
deviation.

Follow-up issue creation for items in `defer` status or
implementer-declined-for-scope items is pre-authorized at Step 11 and is
not an escalation. The supervisor files those issues through a
`generalist` worker without prompting the human. Escalate only when the
issue body itself encodes a new product or scope decision (e.g. a new
public contract, a dependency policy change, a deprecation announcement)
that goes beyond capturing the deferred work.

Do **not** silently implement a review-suggested behavior/scope/tooling change
merely because it is framed as a bugfix, simplification, or security hardening.
Review feedback can require a fix, but the chosen fix must preserve approved
behavior unless the human approves changing it.

The Step 5 resolution-map summary is the primary surface for architectural
sanity checks the workers cannot self-detect, such as a fix that duplicates
an existing platform mechanism (e.g., an existing middleware/pipeline, an
existing transactional or event-dispatch system, an existing public
contract). Workers must not silently implement those changes — they belong
in the Step 5 architectural sanity-check callouts so the human can redirect
before code is written.

Routine code fixes, obvious alternatives, verified in-scope bugs, and incorrect
comments should be handled by the workers and recorded in the resolution map.

Do not interrupt the flow for each individual decision unless continuing
would cause wasted work or unsafe changes. Prefer collecting all
uncertainties into the resolution map as Reviewer Questions, having the
resolution-map reviewer answer them first, then presenting the bundled
Step 5 resolution-map summary — including business-intent clusters,
architectural sanity-check callouts, and any remaining Open Human
Decisions — to the human in one batched go/no-go checkpoint before
implementation.

## Critical Rules

- Resolution map first; implementation second; GitHub replies last.
- The human gets a resolution-map summary checkpoint before implementation,
  not just an Open Human Decisions list. Even a clean map needs an explicit
  go/no-go gate framed in business terms with WHY for each cluster.
- Review comments are not permission to change approved behavior, scope,
  permission/tool surfaces, public contracts, workflow, or requested
  capabilities.
- Pre-approved exceptions: human-authored comments and repository-rule-mandated
  changes are Fix items per the Review Comment Decision Gate, even when they
  touch the surfaces above.
- Do not post replies or resolve threads before fixes are committed and pushed.
- The responder may post/resolve automatically after push only according to the
  approved final resolution map.
- Initial triage must not use one-comment-at-a-time human interaction; it should
  triage all comments and batch uncertainties for reviewer review.
- The resolution-map reviewer should answer reviewer-answerable questions before
  any human decision checkpoint.
- Step 5's resolution-map summary always includes business-intent clusters
  with WHAT/WHY (and BLAST RADIUS where it applies), architectural
  sanity-check callouts, and an Open Human Decisions section. Even when
  Open Human Decisions is `none`, the summary is still presented.
- The Step 9 safety-net checkpoint, when used, must include a final Open
  Human Decisions section. If none remain, say `Open Human Decisions: none.`
- Defer is a promise to track the work, not to silently drop it. Any
  resolution-map entry classified `defer` MUST result in a tracked
  GitHub issue (filed in Step 11) before the responder posts its reply.
  Same for non-blocking suggestions the implementer declined as
  out-of-scope rather than as false positives — these go into a
  tech-debt issue per PR. Do not skip Step 11 to "save time."
