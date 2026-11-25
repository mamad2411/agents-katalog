---
name: pr-resolve
description: Resolve pull request review comments with disciplined triage, scoped fixes, thread closure, and final validation.
---

> All `docs/` paths in this skill refer to the plugin-level `docs/` directory (`../../docs/` relative to this file), not a `docs/` directory inside this skill folder.

## Purpose

Use this skill when a developer wants to work through pull request or branch review feedback in a disciplined loop. It is for review resolution, not first-pass implementation, and assumes there is already an active branch or review surface with a set of comments or threads to evaluate.

Persistent team, squad, or fleet-style long-lived orchestration is out of scope for this skill. Use a separate orchestration layer if persistent coordination is needed.

## When to Use It

Activate when the developer asks for things like:

- "work through the review comments"
- "decide which comments should actually be fixed"
- "address the review feedback and close the threads"
- "reply to the comments we are declining"

## Project-Specific Inputs

Before you start, identify:

- the active branch or review surface;
- the review platform or source system in use, such as GitHub, Azure DevOps, or a local review artifact;
- where review comments and threads are collected;
- how that platform models discussion items, thread states, and resolution actions;
- the repository's validation commands;
- how the team expects resolved comments to be replied to and closed;
- whether the repository allows parallel fix tracks or prefers serial review fixes.

## Default Roles

Use separate roles: an **implementer** that makes accepted fixes, and a **reviewer** that inspects each fix and the final integrated result.

Spawn each role as the plugin's named role agent — `flow:implementer` for fixes, `flow:reviewer` for review (read-only tools — the separation is structural). Both runtimes resolve these plugin-qualified names; they differ only in spawn mechanics, with Claude Code using the Agent tool and Copilot CLI spawning subagents. Copilot's `/subagents` does not surface plugin-provided role agents, so per-role overrides there go in `.copilot/models.yaml`. Pass the implementer the exact fix scope and constraints, and the reviewer the resulting diff and the review criteria.

Both roles may receive the discovery brief (see Workflow Step 1) as factual context — file lists, task boundaries, validation commands, and comparison baseline. Do not pass one role's conclusions or assessments to the other; the reviewer must form an independent judgment from the diff.

### Escalation: Fleet / Agent Team Mode

If the active runtime offers a higher-cost orchestration mode such as a Fleet command or Claude Code agent teams, treat it as an optional escalation for large review batches only — default to standard implementer and reviewer agents first, and tell the developer why the larger team would help before spending the extra tokens.

Escalate only when many accepted review items can be fixed independently, the review surface is large enough that a single implementer would become a bottleneck, specialized fix or audit roles would materially improve coverage, and the developer explicitly opts in. If team mode is approved, still keep one durable triage view and one final reviewer accountable for the integrated result.

### Model Selection

Resolve the active model for each role using this priority chain:

1. **Project config** — look for the runtime-specific config file in the current project root:
   - Copilot CLI: `.copilot/models.yaml`
   - Claude Code: `.claude/models.yaml`

   These are plain YAML files (no markdown, no fenced blocks). Read the `implementer`, `reviewer`, and `scout` keys directly. If a key is absent, fall back to the baked-in default for that role — do not re-prompt for a key that is missing.

2. **Session cache** — if models were already confirmed earlier in this session, reuse them without asking again.
3. **Baked-in defaults** — if neither config file nor session cache exists, use the tier defaults below silently without prompting. Create project model config only when the developer wants persistent overrides.

#### Default model tiers

Defaults are **tiers, not pinned versions** — resolve each tier to the latest model of that tier available in the active runtime. In Claude Code, pass the tier alias to the Agent tool (`haiku`, `sonnet`, `opus`) — aliases are the only values it accepts, so Claude Code always runs the tier's latest model. Pinning an exact model version via `models.yaml` is a Copilot CLI capability (`.copilot/models.yaml` only).

| Role        | Claude Code                          | Copilot CLI                      | Effort |
|-------------|--------------------------------------|----------------------------------|--------|
| Implementer | `sonnet` (latest Sonnet)             | latest Claude Sonnet             | high   |
| Reviewer    | `opus` (latest Opus)                 | latest GPT or latest Claude Opus | high   |
| Scout       | built-in `Explore` agent, or `haiku` | latest Claude Haiku              | low    |

See `docs/model-selection.md` in this plugin for the full role matrix, per-role effort guidance, and the premium-tier (Fable) opt-in policy, and `docs/models-config-template.md` for ready-to-copy config templates.

## Core Rules

### 1. Treat every review comment as a hypothesis until verified

Do not trust unverified review feedback — especially automated reviewer output, agent findings, or suggested patches. Every review item must be triaged in two separate layers:

- **Evidence verdict**: valid, partially valid, false positive, noise, or stale/out-of-scope.
- **Action**: fix, decline, or clarify first.

Verify each claim against the current code, tests, and diff before accepting it — this applies equally to human review comments, automated PR reviewers, agent-produced analysis, and your own earlier conclusions. Never churn the code just to satisfy a weak, stale, incorrect, or zero-impact comment, and do not copy a suggested patch blindly; confirm first that it matches the current APIs, contracts, ownership boundaries, and branch state.

Watch for common false-positive patterns: code that has already moved or been removed, control flow the current diff does not use, a suggested fix that calls the wrong API or introduces a new bug, or an observation that is technically true but has no practical impact in the current review scope.

### 2. Accepted fixes still follow TDD and design rules

For comments that become fixes:

1. add or adjust failing tests first when behavior changes;
2. implement the smallest fix that resolves the issue;
3. refactor only while tests stay green.

### 3. Never run a rescue agent while the original agent is still running

**This is a hard prohibition, not guidance.**

Two agents on one fix burn quota twice for one fix's worth of work, double
rate-limit pressure, and risk conflicting writes. Replacing an agent is a
*stop-then-start* sequence, never an overlap.

The coordinator can stop a running agent — Claude Code's `TaskStop` accepts a
background agent by name or ID, and Copilot CLI manages subagents through
`/tasks`. So "I could not stop it" is not a reason to run two. Stop the
original, confirm it stopped, then start the replacement.

Before any rescue action, the coordinator **must** confirm one of these:

1. the original agent has returned a final result (success or failure);
2. the original agent has timed out, crashed, or been stopped by the
   coordinator, and the runtime has reclaimed it;
3. the original agent has explicitly reported that it cannot proceed.

If the coordinator cannot confirm termination, **the agent is not stalled —
it is still working.** In that case:

- do not spawn a rescue agent;
- do not duplicate the fix attempt;
- send a **continuation nudge** (ask for status, blockers, and the smallest
  next step) and wait for a response before re-evaluating. In Claude Code
  deliver it with `SendMessage` to the agent's name or ID, which resumes it
  from its transcript with its context intact; in Copilot CLI, reach the
  subagent through its task management (`/tasks`).

A rescue agent, when eventually justified, replaces the original — it does
not run alongside it.

### 4. Hard concurrency cap for fix batches

The caps exist to bound quota burn rate — concurrent agents consume 5-hour and
weekly usage limits in parallel. When delegating to `/flow:parallel-impl` for
independent fix batches (Workflow Step 3), the same `max-parallel-tracks` cap
applies. Read the cap from `.flow/defaults.json` →
`concurrency.max-parallel-tracks` (default: **3**), and cap concurrent
reviewers with `concurrency.max-parallel-reviews` (default: **3**) — a
top-tier reviewer is the most expensive agent this workflow spawns. The
developer may override either cap with an explicit instruction.

Fix batches that are not delegated to the parallel-impl (e.g.,
serial fixes handled directly by this skill) are not subject to the cap but
should still avoid launching more concurrent agents than necessary.

### 5. Close the loop on every discussion item

Every review thread or platform-equivalent discussion item should end in one of these states:

- fixed and resolved;
- declined with a clear rationale;
- intentionally left open because a real blocker remains.

Do not stop with code changes only.

When the platform separates **replying** from **resolving / closing** a thread,
do both. A silent resolve is incomplete, and a reply without the matching
resolve / close action is incomplete unless a real blocker keeps the discussion
intentionally open.

#### Platform-specific thread resolution

**GitHub** — Review comments live inside *review threads*. Replying to a
comment (`POST /repos/{owner}/{repo}/pulls/{pull}/comments/{id}/replies`)
does **not** resolve the thread. To resolve a thread, use the GraphQL
mutation `resolveReviewThread(input: { threadId: $threadId })` where
`$threadId` is the thread's `PRRT_*` node ID (not the comment's
`PRRC_*` node ID). Obtain thread IDs via:

```
gh api graphql -f query='
query {
  repository(owner: "OWNER", name: "REPO") {
    pullRequest(number: PR_NUMBER) {
      reviewThreads(first: 100) {
        pageInfo { hasNextPage endCursor }
        nodes { id isResolved comments(first: 1) { nodes { body path } } }
      }
    }
  }
}'
```

Replace `OWNER`, `REPO`, and `PR_NUMBER` with actual values. To resolve:

```
gh api graphql -f query='
mutation {
  resolveReviewThread(input: { threadId: "PRRT_..." }) {
    thread { isResolved }
  }
}'
```

**GitHub GraphQL review threads**: `reviewThreads(first: 100)` is cursor-based.
If the PR has more than 100 threads, request `pageInfo { hasNextPage endCursor }`
and continue with `after: endCursor` until all threads are fetched.

**GitHub REST comments endpoints**: comment list endpoints default to 30 results
per page. Always paginate with `--paginate` or set `per_page=100` to avoid
missing comments.

**Azure DevOps** — Review comments live inside *threads* with a `status`
field. To resolve a thread, PATCH
`/{org}/{project}/_apis/git/repositories/{repo}/pullRequests/{pr}/threads/{threadId}?api-version=7.1`
with `{ "status": "fixed" }` (or `"closed"`, `"wontFix"`, `"byDesign"` as
appropriate). Reply first via the `comments` sub-resource, then update the
thread status.

**Both platforms**: always reply first, then resolve/close. The reply
provides the human-readable rationale; the resolution updates the
machine-readable state.

### 6. SESSION.md writes at gate boundaries

This skill writes `.agent/SESSION.md` at two points: **triage complete**
(Workflow Step 2) and **each fix batch complete** (the Fix gate). Use the
canonical field set from `docs/session-md-schema.md`; only these four fields
differ between the two writes:

| Gate | `current-phase` | `next-action` | `## Decisions` | `## Files Touched` |
|------|-----------------|---------------|----------------|--------------------|
| Triage complete | `triage-complete` | `begin fix batch 1` | each item's evidence verdict and action (accepted / declined / clarify-first) | files read so far |
| Fix batch complete | `fix-batch-[N]-complete` | `begin next fix batch or run post-fix validation` | items fixed in this batch, items still pending | files changed in this batch |

The rest is constant: `current-task` is the overall PR review task,
`workspace` is the active branch or PR reference, `last-updated` is the
current ISO-8601 datetime, `## Open Questions` holds items needing developer
clarification, `## Blockers` holds active blockers (empty if none), and
`## Failed Hypotheses` stays empty — it does not apply to this skill.

If a write fails, log a warning and continue. A failed SESSION.md write never
blocks triage or fix-batch completion.

## Workflow

### 1. Gather review context

Before making changes: collect open review threads, comment chains, or equivalent discussion items plus relevant general comments; read the current code and nearby tests; confirm the latest branch diff and validation status; and determine whether the current PR or branch still represents the intended scope by inspecting the title, description, comments, recent commits, and actual diff.

Do not act on comment text alone if the code has moved.

Default to self-service scope verification. Do **not** ask the developer to
confirm that the PR still represents intended scope unless the evidence remains
genuinely ambiguous after inspecting the review surface. Ask only when:

- the PR title, description, comments, and diff point to conflicting goals;
- the branch appears to contain unrelated extra work and the in-scope subset is
  not defensible;
- reviewers are clearly talking about different intended outcomes;
- recent commits or force-pushes removed the original review basis and the new
  scope cannot be inferred reliably.

If only part of the surface is ambiguous, continue with the unambiguous subset
and surface the ambiguous remainder explicitly instead of blocking the whole
review batch.

#### Bounded discovery brief

Before triaging, use the **scout** model (see Model Selection) to produce a short discovery brief covering the review surface and comparison baseline, relevant files and validation commands, task boundaries (what is in scope vs. out of scope for this review batch), and any open questions requiring developer input. Use the discovery brief template from `docs/workflow-artifact-templates.md` with `Task shape: review-resolution-batch`.

**Skip condition**: Skip discovery when the review batch is already narrow and fully scoped — a single comment on a single file, or a batch where every item was already triaged in a prior pass. When skipped, record the skip reason in the brief.

Pass the completed brief to the coordinator for triage and as factual context to implementers and reviewers in subsequent steps. Do not allow the brief to persist beyond the current review batch.

### 2. Triage review items

For each item: verify the claim against the current code, tests, and review surface; if the comment includes a suggested fix, evaluate that fix separately for correctness and scope; and record the **evidence verdict** (the five values from Core Rule 1) plus the underlying concern, if any — a correctness issue, a security issue, a missing or weak test, a contract mismatch, an architecture concern, or stale/already-fixed/out-of-scope.

Then decide the **action** — fix, decline, or clarify first — using these defaults unless the current code proves otherwise:

- **valid** -> usually fix;
- **partially valid** -> fix only the verified core issue, not the reviewer's
  full proposed scope;
- **false positive**, **noise**, or **stale/out-of-scope** -> usually decline
  with a concrete explanation;
- **unclear evidence or ownership** -> clarify first.

Process accepted items in this default priority order: security issues, correctness issues, contract mismatches, missing or weak tests, architecture concerns, then lower-priority polish.

On a large review surface, triage can be fanned out. In Claude Code this is the one place `subagent_type: "fork"` fits — the coordinator has already read the threads, and a fork inherits that context instead of re-reading it. Fan out triage only; **never fork a reviewer**, whose entire value is judging the diff independently of the coordinator's conclusions (see `docs/model-selection.md`, "Delegation hazards").

### SESSION.md write — triage complete

Once every review item is triaged, write `.agent/SESSION.md` using the
triage-complete row of Core Rule 6.

### 3. Batch independent fixes when safe

If multiple accepted fixes are independent:

1. group them into separate fix tracks;
2. keep tightly coupled fixes serial;
3. invoke `/flow:parallel-impl` for each independent fix batch;
4. use Fleet or agent-team mode only for batches that were explicitly approved for the higher-cost path.

If review items interact heavily, resolve them serially.

### 4. Implement each accepted fix

For every accepted fix: give the implementer the exact review item, the evidence verdict, the intended resolution, the affected files, the needed tests, and the scope boundary; require minimal, focused changes only; and for partially valid comments, implement only the verified issue and ignore any unverified or over-broad suggested fix.

### 5. Review each fix

After each fix, have a separate reviewer inspect the resulting diff and ask for **full coverage, not self-filtered severity**: report every issue found, each tagged with severity and confidence — the reviewer must not decide what is "worth reporting". Focus areas: correctness regressions, missing edge-case coverage, contract drift, security concerns, and material design regressions.

Then triage the findings as coordinator: substantive issues enter the resend loop below; style-only nits and low-confidence noise are dropped at triage.

#### Bounded fix-review resend loop

When the reviewer finds substantive issues in a fix, return the fix to the implementer with the specific issues and the reviewer's expected resolution; the implementer revises and resubmits; the reviewer re-inspects the revised diff.

Allow at most **2 resend attempts** per fix. If the fix still has unresolved substantive issues after the second resend, either escalate to the developer with a summary of the disagreement or stall, including what was attempted in each round, or re-scope the fix to a smaller, defensible change that both sides accept.

Do not loop indefinitely. A fix that cannot converge in two rounds needs human judgment or a narrower scope.

#### Rescue policy for stalled fixes

A fix is only stalled when the implementer agent has **explicitly reported a
blocker**, **terminated without completing**, or failed to show any progress
across at least **3** consecutive coordinator checks (or the configured
`concurrency.rescue-min-stall-checks` value from
`.flow/defaults.json`). A slow-but-progressing agent is **not** stalled.

Apply the nudge-before-rescue sequence from Core Rule 3 before treating a fix as rescue-eligible: send a continuation nudge; if the agent responds and resumes work, reset the stall counter and let it continue. Only proceed once the nudge gets no response (confirmed timeout) or the agent explicitly reports it cannot proceed. When rescue is justified:

1. pause the fix and capture what was attempted and where it stalled;
2. prefer **same-agent continuation** with a narrowed scope first;
3. only spawn a replacement agent if the original has terminated and its
   context is irrecoverable (see Core Rule 3);
4. if re-scoping is not viable, escalate to the developer with a clear
   description of the blocker.

Do not allow a single stalled fix to block the rest of the review batch. Move
to the next independent fix and return to the stalled item after the developer
provides guidance or approves the re-scoped change.

#### Disagreement resolution: fix-vs-decline conflict

When the reviewer and implementer disagree on whether a comment should be fixed or declined, record the disagreement with each side's rationale and allow one re-review round where both sides see the other's reasoning. If the conflict persists after that re-review, escalate to the developer with both rationales and the comment context.

Do not allow a fix-vs-decline disagreement to stall the rest of the batch. Move to the next independent item and return to the disputed comment after escalation or re-scoping resolves it.

### 6. Reply to and resolve review threads

After each fix or decline, perform **two actions per thread** — reply then
resolve. Never skip either step.

1. **Reply** — post a short, concrete comment on the thread:
   - if fixed: what changed and the commit SHA;
   - if declined: the concrete reason (false positive, noise, stale, out of scope);
   - if clarification needed: the question, and leave the thread open intentionally.

2. **Resolve the thread** — use the platform-specific mechanism described in
   Core Rule 5 ("Platform-specific thread resolution"):
   - GitHub: `resolveReviewThread` GraphQL mutation with the thread's `PRRT_*` ID;
   - Azure DevOps: PATCH the thread status to `fixed`, `closed`, `wontFix`, or `byDesign`.

Silent declines are not allowed — a reply without thread resolution is incomplete, and a thread resolution without a reply is incomplete.

When collecting threads, paginate as described in Core Rule 5 (GitHub REST
defaults to 30 per page; use `--paginate` or `per_page=100`), and always
resolve using thread IDs (`PRRT_*`) obtained via the GraphQL `reviewThreads`
query — comment IDs (`PRRC_*`) cannot be used with `resolveReviewThread`.

### 7. Final validation

After all relevant review items are handled:

1. run the repository's real quality gates;
2. verify any new behavior has test coverage;
3. invoke `/flow:pr-ready` on the stable diff;
4. publish one durable review-resolution summary using the review-resolution summary template from `docs/workflow-artifact-templates.md`. The summary MUST capture decisions, validation outcome, and remaining concerns;
5. include a workflow outcome-measures block in the summary using the outcome-measures template from `docs/workflow-artifact-templates.md`. The block MUST include at minimum: `discovery-reuse`, `rescue-attempts`, and `re-review-loops`.

### 8. Commit and push by default when the branch changed

If accepted fixes changed the branch, the default finish is to create a scoped commit covering the accepted review-resolution changes, push the updated branch or PR head, and keep the review discussion state synchronized with the pushed diff.

Only skip commit and push when the developer explicitly requested a local-only pass, no repository files changed, or repository policy requires a separate human-owned publish step. Do not leave accepted fixes uncommitted by default.

### 9. End with a brief chat summary

Before stopping, provide a concise developer-facing summary in chat covering:

- the issues reviewed and their verdicts;
- what was fixed, declined, or left open intentionally;
- whether replies were posted and threads were resolved / closed;
- commit / push status;
- any remaining blocker or follow-up.

## Example Review-Resolution Summary

Use a durable summary shape so another reviewer or contributor can quickly see what was fixed, declined, or left open. For example:

```text
Review surface: PR 128 against main
Reviewer source: Azure DevOps PR review
Decisions:
- comment-14 | valid | correctness | fixed | Added a null-input guard and coverage for the empty payload path
- comment-19 | partially valid | test | fixed | Coverage concern was real, but the suggested API-level fix was wrong; strengthened the regression test without changing the contract
- comment-23 | false positive | stale-or-out-of-scope | declined | Current diff already removed the old helper the comment referred to
Validation: npm test, npm run validate:plugin — pass
Remaining concerns: waiting on reviewer confirmation for one clarify-first thread about ownership of normalization
Outcome measures:
  discovery-reuse: yes
  rescue-attempts: 0
  re-review-loops:
    comment-14: 0
    comment-19: 1
    comment-23: 0
```

Prefer the repository's canonical review-resolution artifact template when one exists.

### Example Thread Responses

Use short, concrete replies that make the outcome obvious, then apply the matching platform action. For example:

- fixed: `Fixed in 9ab12cd by tightening the null-path guard and adding coverage for the empty-input case.`
- declined: `Declining this one — the current contract intentionally allows duplicate labels during draft creation, and the suggested change would narrow behavior we still rely on.`
- clarify first: `I could address this either in the serializer or in the caller. Which boundary did you intend to own the normalization rule?`

### Example Developer-Facing Chat Summary

Keep the final handoff short and concrete. For example:

- `Resolved 3 review items: fixed 2 valid issues, declined 1 false positive, replied on all 3 threads, and resolved the 2 closed items. Pushed as 9ab12cd; one clarify-first thread remains open pending API ownership guidance.`

## Required Gates

### Comment gate

A comment is not complete until:

- it was triaged explicitly;
- an evidence verdict was recorded explicitly;
- fix, decline, or clarify-first was chosen;
- a reply was posted for fixed or declined items;
- the **thread** (not the comment) was resolved using the platform's thread
  resolution API, or intentionally left open with a stated blocker.
  On GitHub this means `resolveReviewThread` with the `PRRT_*` thread ID.
  On Azure DevOps this means PATCHing the thread status.

### Fix gate

A fix is not complete until:

- tests changed first when applicable;
- the issue is actually resolved;
- review finds no unresolved substantive issue;
- touched files stay scoped to the real concern.

### SESSION.md write — fix batch complete

After the Fix gate passes for a batch, write `.agent/SESSION.md` using the
fix-batch-complete row of Core Rule 6.

### Review batch gate — resolution loop complete

Before declaring the resolution loop done, confirm ALL of the following.

**Per-thread gate**
- [ ] Every review thread has a recorded resolution state: ACCEPTED or DECLINED — PASS / FAIL
  (A thread with no recorded state is a failing item — silent declines are not permitted.)
- [ ] Every review thread has a recorded evidence verdict: valid, partially valid, false positive, noise, or stale/out-of-scope — PASS / FAIL
- [ ] Declined threads have a recorded reason visible in the resolution artifact — PASS / FAIL
- [ ] Fixed or declined threads have both a reply and a matching resolve / close action when the platform supports both — PASS / FAIL

**Post-fix gate**
- [ ] Post-fix validation ran on the final diff and exited 0 — PASS / FAIL
- [ ] No previously-passing tests now fail — PASS / FAIL
- [ ] The final readiness workflow (`/flow:pr-ready`) has run on the stable diff — PASS / FAIL
- [ ] Durable resolution summary artifact has been produced using the template from `docs/workflow-artifact-templates.md` — PASS / FAIL
- [ ] If code changed, the branch update was committed and pushed unless local-only was explicitly requested — PASS / FAIL
- [ ] A brief developer-facing chat summary of issues and resolutions was delivered — PASS / FAIL

If any item is FAIL: list the unresolved thread IDs or failing validation
output, report the remaining issues explicitly, and do not declare the loop
done.

## Stop Conditions

- the review surface has moved enough that the original comments are no longer reliable;
- accepted fixes begin conflicting on the same files or contract;
- reviewer and implementer still disagree after exhausting the bounded resend loop, rescue policy, and disagreement resolution — two resend attempts were made, re-scoping was attempted or ruled out, and any fix-vs-decline conflict was escalated after one re-review;
- required validation commands or thread-resolution expectations are still unknown;
- the developer asks to stop.

Before stopping for a disagreement or stall, follow the full progression:
bounded resend loop (Step 5) → continuation nudge → rescue policy →
disagreement resolution for fix-vs-decline conflicts. Do not skip the nudge
step and do not spawn a rescue agent while the original agent is still
running (Core Rule 3). Only stop after these options are exhausted or the
developer explicitly declines re-scoping.

When a stop condition is met, stop batching, restate the blocker, and continue only after the review surface is stable again.
