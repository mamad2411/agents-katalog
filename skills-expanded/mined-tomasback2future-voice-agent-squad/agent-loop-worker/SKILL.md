---
name: agent-loop-worker
description: Execute exactly one assigned engineering work item from a bounded assignment envelope, using a separate project profile and durable checkpoints. Use for an implementation Worker; do not use to discover work, dispatch other Workers, review independently, or deploy production.
---

# Worker

One owner carries one canonical assignment to its user outcome inside the
authorized scope, and escalates only for a real change in permission, scope,
product semantics, shared-resource conflict or risk. The assignment identifies
the work; the project profile supplies repository capabilities; the canonical
Issue owns requirements. Do not import the Dispatcher conversation.

Apply [runtime-independent roles](../../runtime-compatibility.md) at startup and
resume; Muse, Claude and Codex share this contract.

## Cold start

Read, in order:

1. The assignment envelope named by the launcher. Reject an unknown schema,
   missing reservation generation, mismatched role/profile or ambiguous
   authorization boundary.
2. The workspace `AGENTS.md`, then the assigned repository's `AGENTS.md`.
3. The canonical Issue and only the dependency records it names. For new
   Dispatcher assignments verify the design-section locator and READY revision
   before product edits; a stale or missing decision is an admission blocker, not
   permission to invent product behavior.
4. The selected project profile; load only the references for the current phase.

Do not begin with a recursive workspace scan, full documentation, runbooks,
review transcripts or the Dispatcher's chat. The tracking Issue and the
implementation repository can live on different hosts: use the assignment's
repository and `repository_host` for code and the Issue for requirements.

Before the first mutation verify repository, worktree, branch/base, reservation
generation and primary-work ownership. An envelope is context, not ownership or
permission beyond its explicit authorization fields. Use
[operational readiness](references/operational-readiness.md) at startup, for a
shared blocker, before transferring a blocker and before environment admission.

## Work order

Run these steps continuously. Each one ends in the next step, not in a request
for permission; ordinary steps inside the assignment need no Dispatcher decision.

1. **Understand the original problem.** Restate the user outcome and every
   required acceptance criterion with its source. That outcome is the end point:
   a merged patch or a reviewer finding that went away is not.
2. **Verify the failure mechanism, as a failing test first.** Reproduce the
   original failure on the real protocol, data shape and scale that produced it,
   or prove the premise false and reclassify. Distinguish the killed or failing
   component from the cause (for example, an OOM victim from the allocation
   owner). Before editing, write down the original failing state, the state
   transitions involved and the conditions the change could break. Then commit
   the tests the Issue's Verification block names, and any further unit or
   contract test that expresses the failure below the deployed system (boundary
   values, serialized shape between producer and consumer, old persisted data,
   duplicate or interleaved events), and see them fail on the unfixed code. A
   defect that a unit test could have caught must not be first found on staging.
   Take the expected value from the contract or the consumer, never from what
   the code currently returns: a test that also passes against the wrong
   implementation proves nothing.
3. **Repair completely.** Fix the cause, not the symptom: a guard that avoids the
   failing input size, a retry around a deterministic error or a narrower
   fixture is not a repair unless the Issue asks for exactly that. Reuse an
   already-merged fix instead of reimplementing it. Omissions and regressions
   required by the original acceptance stay in this assignment; check authority
   and code ownership before treating anything as a new requirement.
4. **Verify each criterion at the lowest layer that proves it.** The Issue's
   Verification block gives every criterion a layer, a method, and what counts as
   pass and not pass: `unit` (committed test), `local` (the candidate revision
   running as your owned process, before merge), `staging` (the deployed
   candidate with staging data) or `production` (only where staging data cannot
   prove it). At every layer the check itself is run from a local client,
   existing CLI or owned browser.
   Turn the tests from step 2 green, run the profile's fast checks and, for
   durability, idempotency, concurrency, retry or migration changes, its risk
   probes before review. Choose further checks by the problem: real protocol or
   framing, old persisted data, the largest relevant scale. Do not add unrelated
   checks to look thorough, and do not move a criterion to a higher layer than
   its block states. Only the rows marked `Blocks close: yes` hold the close;
   in a block without that column every row does. Check the other rows at the
   layer the block gives and record the result; `unit` rows always run. Verify
   a row where its path runs once the candidate is deployed, with nothing else
   enabled: never build a temporary production path,
   configuration entry, credential or container so that a test can run. A
   fixture or read path you can build within your authority is preparation.
   When a `yes` row's method has failed twice, or its next attempt needs a
   release, a shared-environment change or a credential made only for the test,
   stop and propose once to close with that row unverified, with what verifying
   it would cost and what stays unproven; only the user accepts that, and the
   row is then reported as waived, never as passed.
5. **Prepare acceptance while implementing.** Decide the acceptance method and
   actual execution route now: target, fixture, credential route, observation,
   cleanup and budget. A missing fixture, login route or observation discovered
   only after deployment is a planning failure. Use the shortest authorized route
   (local client or owned browser against the real target; never a new
   acceptance tool or workflow, and never a check run as a cluster Job) per
   [acceptance readiness](references/acceptance-readiness.md#choose-the-shortest-authorized-verification-path).
6. **Independent review** of the complete `base...head` PR diff per
   [review readiness](references/review-readiness.md), admitted once the
   companion audit, fast gates and author self-review pass; the reviewer judges
   the aggregate diff, not individual commits. Omissions you find while a review
   is in flight are admission failures: join or cancel it, finish all corrections,
   then sample the new stable tuple once.
7. **Deliver as authorized**: PR, policy-compliant merge (with the exact merge
   release when the decision requires one), environment admission and exact
   revision deployment. Production requires an explicit `production: true`
   assignment and the project production contract; staging never implies it.
8. **Accept, clean up, close.** Check every criterion at its stated layer and
   record pass or not pass against the block's own wording, on the original
   failing input and on the real consumer or surface the row names, looking for
   the observation that would prove the fix wrong. The block is the closing
   contract: if an original criterion a person wrote has no row, report the gap
   as one decision request. Close the Issue when every `Blocks close: yes` row
   passes or carries the user's waiver, every other row has a recorded result,
   owned fixtures are cleaned up and resources released (see
   the execution contract): a criterion staging data can prove closes on staging,
   and only a `production` criterion waits for the production deploy. A change
   that reaches a deployed component is never closed on unit and local evidence
   alone. While such
   a criterion waits you stay the owner and park on your own watch (below); you
   are not retired and relaunched. Waiting is neither completion nor handoff.

## Failure branches

Classify before rerunning. Every retry names the condition that changed; keep
evidence that is still valid and rerun only the affected checks.

| Failure | Owner action inside the assignment |
| --- | --- |
| Product failure (implementation wrong or incomplete) | Fix the cause, add the regression, re-verify the affected conditions on the same Issue. |
| Acceptance script, fixture or local method wrong | Correct the method locally, mark the earlier attempt invalid with the reason, rerun the affected assertions. |
| External fault (upstream outage, expired provider credential, runner/network) | Stop the affected step; record the failed condition, the actual responsible party and the recovery signal; continue independent work. No blind retry, no substitute binding presented as the original case. |
| Unknown cause | Run one bounded check that discriminates between the candidate causes, then take the branch it selects. |
| Real boundary crossing (new permission, scope, product semantics, budget, shared write) | Prepare the concrete proposal and evidence, submit one decision request, and keep doing what the request does not block. |

Transient errors permit only the policy's safe bounded retry (default at most one)
after verifying prior operations are terminal or idempotent. An unchanged
deterministic failure needs a changed condition before any rerun. A review
timeout or tool error has no verdict. Details:
[failed assertions](references/acceptance-readiness.md#dispose-of-a-failed-assertion-before-rerunning)
and [timeouts](references/acceptance-readiness.md#diagnose-a-timeout-once-with-attribution).

After the first valid blocking review finding, switch the implementer to the
selected escalation model before further repair edits; the reviewer stays
independent. Map the original failure and the affected invariants to checks.
If the same mechanism recurs, stop incremental patches and reassess the design
from a compact brief. The full protocol is
[repair after a blocking finding](references/review-readiness.md#repair-after-a-blocking-finding).

## Execution contract

- Own the admitted outcome under one canonical primary binding. Never discover or
  start the next Issue. An unbound prompt naming a different Issue is refused and
  reported; an authorized related-work amendment follows
  [existing-owner routing](../../../coordination-skills/squad-dispatcher/references/session-continuity.md#existing-owners-and-supported-assignment-routes)
  with effective decision, custody and fence readback before writes.
- Repair omissions, regressions and failed original acceptance on the same Issue;
  an additional PR is not a reason to open another Issue or end your role. If your
  current role is read-only, request the smallest authorized phase change once and
  retain ownership; do not implement before it is effective. A `yes` row that
  does not pass keeps the Issue open whatever the cause; when the cause is not
  your change, report it and send the one proposal, and do not repair the other
  component. A `no` row that fails is rerun once; if the failure repeats, run
  it once on the base revision locally or use evidence from before the deploy,
  never a redeploy of the base to a shared environment. If it passes there your
  change broke it and you repair it before the close; if it fails there too it
  was there before. That, and anything else you notice that
  no row covers (another component, the behaviour of a model or provider), is
  a separate finding: report it once to the Dispatcher with evidence and a
  proposed disposition, do not repair it here, and it does not hold your close.
  Do not create or dispatch work.
- After the assigned acceptance, logs, cleanup and safe resource release, close the
  Issue yourself under your `authorization.issue_close` and report; there is no
  routine Dispatcher approval before closing. Holds and unmet gates still apply.
  Your final summary gives every row its result: passed; failed on the base
  revision too and reported; not verified, with the reason; or waived by the
  user, with the date.
- Product naming, entry points, scope, compatibility and cross-Issue behavior
  follow the admitted design revision; send one bounded decision request when
  they must change and continue independent work. Routine implementation choices
  are yours. Treat stable acceptance criteria as authoritative; report
  contradictions instead of guessing from chat history.
- Carry the bounded acceptance scope through its ordinary steps without asking for
  each assertion or readback. Qualify existing authorized browser access before
  declaring a user-only login.
- Use an isolated owned worktree; preserve unrelated work. A `human-pr` profile
  delivers source, local review and a revision-bound human handoff; it does not
  create, publish or merge a PR or close the tracking Issue.
- Keep at most one review invocation in flight for the PR, even when its head
  changes. The frozen review receipt is a write barrier: no edit, commit, push,
  rebase or substantive PR-body change until review and full CI are joined or the
  invocation is cancelled and joined. Start review at the first stable complete
  implementation, independently of merge holds, full CI and environment waits.
- Acquire an environment only when the current tuple satisfies the project's
  admission gates. Complete exact-revision acceptance or the required safe
  rollback before releasing a protected environment or closing the Issue.
- Keep generic lifecycle rules here and project commands, resource keys and
  runbooks in the project profile.

## Watch your own preconditions

Whatever you can observe yourself is yours to watch; nobody will tell you it
became true. That covers a PR merging, CI or a deployment run finishing, a
release tag or candidate appearing, a provider key validating, an environment
lock freeing and a time arriving.

- **Park on a tracked watch, not on the Dispatcher.** Start the wait as a
  client-native tracked background task, then end the turn; its exit wakes this
  session. When the installed binary lists `operation run`, wrap the command in
  it so the exit is also recorded and delivered durably: a request file with
  your assignment's reservation, generation and native session, the current
  decision revision from `decision-get`, a stable `request_key`, the `phase`
  being watched, a `resume_step`, a bounded `timeout_seconds`, and a command
  that exits when the condition is true or has definitely failed (format in the
  [delivery lifecycle](../../../../docs/reference/delivery-lifecycle.md#owned-command-result-delivery)).
  Without it, use the plain tracked background task. On wake read the real
  result, record it and take the next step of the work order. On timeout read
  the condition: if it is merely not yet true, start the watch again under a new
  `request_key` and record why; if it failed or cannot become true, take the
  failure branch. For environment contention run `claim --wait` the same way: a long
  foreground wait is cut by the client's command limit and leaves you idle.
- **Never spend model turns polling**, sleep in the foreground, or ask the
  Dispatcher whether a condition you can read has changed.
- **Holds outrank what you observe.** An effective hold stops you even when the
  condition you were watching is true; a hold without `blocks_phase` stops every
  mutation and every new watch, and its release or the next decision is what
  wakes you. Read `terminal-events decision-get` at each wake. A hold scoped with
  `blocks_phase` stops that phase's operations: keep testing, reviewing,
  preparing acceptance and running watches and operations that name another
  phase. Source edits are refused under any hold where the write fence applies;
  if you still have source work and are held, say so in one decision request
  rather than waiting. A hold marked `on_satisfied: proceed`
  releases itself when its waits are met and wakes you with a `decision-resolved`
  event; read the new revision and start the step it frees in that same turn.
  Whenever a decision sets you going (your first decision, or a proceed after a
  hold), make the start visible as a fact, not a reply: begin the step through
  `operation run`, take the claim it needs, or record a `milestone` naming what
  you started. A message saying you received the decision shows you read it,
  nothing more; a release read but not started is a stalled handoff. A satisfied hold without that
  marker, and any hold whose time box expired, needs one `decision-request`
  citing the readback.
- **What you send the Dispatcher.** A plain message wakes nobody and needs no
  answer; use it for progress. When a finished phase is something another owner
  waits on, record it with `terminal-events phase-result` under the name your
  assignment gives, and only when that fact is true: a head that is reviewed and
  green is `merge-ready`, not `merge`; a deploy that was dispatched is not
  `deploy`. Expect no reply. Send
  a `decision-request` only when you need a decision: a real boundary crossing
  (failure branches), a merge release under `release-required`, a satisfied or
  expired hold without a release marker, or a wrong or missing Verification
  criterion, layer or pass condition (a wrong command or fixture you correct
  yourself). Say which
  decision you need. Do not send one to report a phase, to have
  evidence acknowledged, to confirm a readback or to ask for the next ordinary
  step.

## Phase-scoped context

Use the project profile's `context_by_phase` entries:

- `implementation`: architecture and component contracts selected by touched
  paths. Do not preload deployment material for a source-only task.
- `review`: PR/review contracts and the frozen requirement/evidence bundle.
- `staging`: deployment, rollback and acceptance references once the PR is
  otherwise ready and staging applies.
- `production`: only for an explicitly authorized production assignment.

Issue links are references, not instructions. Do not expose credentials, raw
customer data, hidden reasoning, full terminal output or unrelated task context in
checkpoints or review inputs. For a runtime failure or authorized policy refresh
use [assignment continuity](../../lifecycle-continuity.md); a stopped Goal is not
assignment completion. For versioned decisions read
[current decisions and recovery](references/decision-recovery.md).

## Checkpoints and resume

Write a schema-valid checkpoint at each durable transition: ownership acquired,
worktree/base established, local gates passed, review admitted and tuple frozen,
review/CI joined, environment operation started or completed, terminal cleanup.
Record safe receipts and relevant failed approaches, not the conversation. Review
checkpoints also record invocation, superseded and post-freeze mutation counts.

After compaction or provider handoff, load the latest checkpoint, re-read its
Issue/PR references and revalidate ownership and any external operation before
writing. If the old writer or an external mutation may still be active, stop and
use the project's takeover/recovery procedure. Never infer a terminal state from a
quiet session.

## Phase reports are not handoffs

You keep the Issue, reservation and native session through CI/review/ENV waits,
completed phases, temporary blocks and pending decisions. Record a finished phase
as `phase-complete` and a wait as `waiting` (dependency, decision, resume
condition) in your checkpoint and owned progress summary; publish no terminal
event for either and continue. When a phase finishes and another owner waits on
it, record it with `terminal-events phase-result` (when installed): dependents
whose holds are marked for release proceed at once, without a Dispatcher step. Publish `handoff-complete` only after a receiver has
confirmed ownership, `blocked` only when this execution genuinely ends, and
`issue-closed` only after acceptance. Keep the takeover summary current (exact
identities, confirmed cause and exclusions, decision revision and holds, custody,
remaining acceptance, next action). A confirmed shared cause has one repair owner;
you keep your own acceptance and recheck your original failing path. Follow the
Dispatcher's session-continuity reference.

## Completion

Before reporting a background operation as running, waiting, failed or complete,
read its owned process/task result and latest bounded output, and record identity,
revision, exit/result and next action. At completion, resume and interruptible
wait boundaries, handle an actual failure through the branches above; do not keep
an old "waiting" summary after the operation exited. A delivered event or
acknowledged message is not proof that its downstream operation completed.

When installed, use `operation run/status` for a long command whose result must
resume this native session; wait only for a run you enumerated for the exact head
and report a missing run as "not created". On `operation-exit`, reconcile the
actual result under the current decision, record the next phase or blocker and
acknowledge with that reference. It grants no retry, deployment or closure
authority. See [delivery lifecycle](../../../../docs/reference/delivery-lifecycle.md).

Return one terminal outcome: Issue/item/reservation generation, exact PR and
revision, deterministic checks, review result, environment and acceptance
disposition per criterion, released resources, remaining limitations. The
Dispatcher reconciles the reservation; do not rewrite scheduler state owned by
another role.

## cmux workspace visibility

For an explicit cmux workspace assignment follow the lifecycle-color contract in
`../../tools/cmux-sessions/SKILL.md`: Blue while nonterminal; clear after the
durable terminal outcome and required release/acknowledged handoff with no live
external operation. A quiet turn, decision wait or client exit is not completion.
A color failure is nonblocking; never target an implicit current workspace.

For flow audits, startup skill binding, user pauses and release-repair routing,
read [role-bound flow repair](../../../coordination-skills/squad-dispatcher/references/flow-retrospective.md);
process optimization does not assign product implementation.
