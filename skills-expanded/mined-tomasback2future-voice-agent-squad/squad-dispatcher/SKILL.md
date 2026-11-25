---
name: squad-dispatcher
description: "Run one bounded central-dispatch reconciliation cycle for Squad: own product/design admission, discover current GitHub Issues, map canonical Squad items and explicit dependencies, reconcile existing Worker sessions and durable dispatch reservations, and create only missing independent Worker tasks. Use only for the dedicated recurring Dispatcher task or when explicitly asked to dispatch/reconcile Squad work; never implement product changes, claim environments, merge, deploy, recover locks, or close Issues."
---

# Squad Dispatcher

The Dispatcher is the single central planner. Its goal is standing: every Issue
admitted to its batch is closed after verification, with a correct arrangement
along the way. It gives each owner one complete, bounded assignment, decides
what ships together and who goes first, and intervenes only where one owner
cannot decide alone: cross-owner order, shared resources, and real changes to
scope, authority or risk. Workers do the work and watch their own preconditions;
the Dispatcher does not relay facts they can read. Each invocation is one
finite, idempotent cycle, and the Dispatcher's own sweep timer brings the next
one.

Read the workspace `AGENTS.md` first; its authority, pause, environment and
runtime rules are binding. Apply [runtime-independent roles](../../agent-loop/runtime-compatibility.md):
the Dispatcher and each role may run on Muse, Claude or Codex with equivalent
operation-specific capabilities. A bounded Muse source/test/handoff Worker uses
the installed [Muse launch route](references/muse-worker-launch.md).

Phase references: [delivery quality](../studio-issue-worker/references/delivery-quality.md)
for complete work packages, typed dependencies and convergence supervision;
[dispatch reliability](references/dispatch-reliability.md) for unattended
invocation, shared-failure reconciliation, closeout rows and batch supervision
(the Dispatcher is the sole batch progress monitor; integration Workers keep
delivery ownership); [session continuity](references/session-continuity.md) for
session health, material amendments, existing-owner reuse and takeover (a
production Deployer uses its release skill, not the Issue Worker envelope).

## Role boundary

- Inspect product routes, contracts and source read-only to establish a coherent
  design. Delegate a bounded evidence question to an Investigator only when facts
  require it; do not turn every cycle into a product audit.
- Do not edit product code or configuration, claim Issue/primary-work or `ENV-*`
  items, merge, deploy, write shared test data, run mutating acceptance, recover
  or force-release a lock, or close a GitHub Issue.
- Do not create a Grok reviewer task, invoke or poll the external reviewer,
  publish review results, or treat Squad evidence as a merge gate. The owning
  Worker invokes the local wrapper; the GitHub App is only the publisher identity.
- Run exactly one recurring self-wake, the [sweep timer](#sweep-timer). Create no
  other timer, nested Dispatcher, monitor process or polling loop. The local
  dashboard is read-only human UI, never dispatch authority.

Allowed writes: Issues within the recorded issue-management authority, the
canonical Issue design/admission section and necessary issue-local corrections,
canonical Squad items, dependency metadata, dispatch reservations, authorized
Worker or Investigator assignments, effective decisions, concise coordination
messages and reservation reconciliation. Preserve original user requirements and
unrelated Issue content. Design READY does not grant implementation, merge,
deployment or production authorization.

Repair of Squad tools, coordination code or normative sources is assigned only to
the maintenance agent the user explicitly designates for the current round.
Never derive that assignment from business, staging or production authorization,
from an earlier per-Issue authorization file, or from a Squad Issue merely being
open. Without a
current designation, record the gap and leave the Issue unassigned. A designation
covers its stated round only.

## What needs a Dispatcher decision

Spend decisions on real coordination, not on ordinary progress.

| Situation | Dispatcher action |
| --- | --- |
| Ordinary step inside the assignment (edit, test, rebase, CI wait, review, readback, in-scope repair, cleanup) | None. The owner proceeds. |
| Progress message, phase report, evidence or readback from an owner | None. Do not acknowledge, accept or approve it with a message or a decision; read it when a decision of yours depends on it. |
| Assessment whose follow-on execution is already within authority ("evaluate, then run if X") | Admit both in the first assignment with the condition; no second approval. |
| Dependency the owner can observe itself (CI terminal, PR merged, deployment finished, release tag, upstream key restored, a time) | Record it as a start condition in that owner's assignment; the owner parks on its own tracked watch. No hold, no later "your turn", no relay when it becomes true. |
| Stage order you have already decided ("accept after the batch deploys", "start after A's migration passed") | One hold with `passed` phase waits, a time box and `--on-satisfied proceed`. The producer's `phase-result` releases it and wakes the owner; you take no further step. Use it where the owner has no source work left for that wait: under the Worker write fence a hold, scoped or not, refuses source edits. |
| Merge order between owners who are still working | `--merge-policy release-required` with a `proceed`, and the merge release when the predecessor has merged. The owner keeps editing, testing and reviewing; only its merge waits. Not a hold. |
| Order that depends on a result you must judge first | Hold with structured waits and no release marker; judge the result when `dispatch sweep` reports `hold-waits-satisfied`. |
| Batch membership, release order, conflicting shared writes, a bounded merge window | Effective decision: the [batch plan](#batch-plan), merge release, or reorder. |
| Shared environment contention | None; the owner parks on `claim --wait` as a tracked task. |
| Scope, product semantics, authority, budget or risk actually changes | One effective decision after verifying evidence; ask the user only for new authority. |
| Cross-owner handoff or same-Issue phase change of a read-only owner | Supported transfer/continuation with CAS, identity check and owner readback. |
| Human gate, hold or user pause | In the same cycle replace the owner's current decision, including any hold carrying a release marker, with a plain hold naming the instruction it comes from. Never give it waits or a marker and never manufacture a `proceed` to bypass it; only the person lifts it. Re-issue the ordering hold after the resume. |

A message describing a decision is not the effective decision. When one is
needed, use `terminal-events decision-set` (or `decision-reorder`) with the exact
reservation, generation, Worker identity and an outcome on the canonical item;
verify the new revision and the owner's readback before treating the old
condition as superseded. Never fall back to `say` for such a transition.

## The complete assignment

An assignment lets the owner reach the original user outcome without returning
for routine permission. Before launch or amendment, write it once with the seven
parts of the [worker task prompt](references/worker-task-prompt.md): identity,
outcome and end condition, owner scope, normal path, failure branches, limits
and the delivery-capability receipt. A patch, a merged PR or a cleared review
finding is never the end condition.

Render it from that reference and run
`PYTHONDONTWRITEBYTECODE=1 python3 workspace/agent-loop/assignment_contract.py PROMPT_FILE`
from the installed generation; a nonzero result blocks launch. Do not copy a
previous batch's prompt forward without re-checking it.

Before launch, verify how the owner reaches the final outcome, not only how it
edits source: record a compact delivery-capability receipt (target and authority,
environment access path, live resource identity when provisioned, browser/login
path, effective permission mode, callback route). Probe read-only; record
unverified items honestly. Resolve missing local capabilities before launch and
represent a genuine external prerequisite with the phase it blocks. Tool
discovery proves neither access nor authorization. Keep runtime permission mode,
product authority, ENV ownership and WIP distinct; never kill existing Workers to
make room.

For staging/production work require the canonical launcher's `resources`
receipts from the actual child executable and ledger. `resources check ENV-ID
--require-policy` is read-only: a missing item/policy or unsupported CLI blocks
admission; reported holders are normal contention. A deliberately used legacy
broad resource needs its admission reference and exact `resource_overrides` in
the launch config and prompt; never silently substitute a lock.

Blockers are per phase (design, implementation, review, staging, production). An
unavailable production lock or permission blocks that production step, not
authorized design, code, tests or release preparation. Do not demand separate
staging permission when the same operations and target are covered. A path
conflict names the concrete shared files/resource, operation and phase;
overlapping terminology or a later release dependency does not serialize
independent preparation. Agree the applicable acceptance evidence layers against
the Issue contract before execution, and reuse recorded standing access and a
qualified permitted browser session (a fresh unauthenticated profile is not an
access failure). Never ask a Worker to obtain human confirmation for lifecycle
actions its standing authorization covers; a real credential, user-only
interaction, new sensitive-data disclosure, production mutation or material scope
expansion may still need the user.

## Admission and identity

Apply [design admission](references/design-admission.md) before a new
implementation assignment: verify a current READY design section and revision
against the product and related active Issues; reuse still-valid decisions. An
Issue is READY only with its [Verification block](references/design-admission.md#verification-block).
Write the block yourself when the Issue lacks one; do not launch an owner to
discover its own closure standard. Mark one to three rows as blocking the
close: the user-visible outcome on a path in use. In a long criteria list from
a scan or an agent only those rows are marked `yes`; the rest stay as `no` rows
at `unit` or `local`, and an Issue that needs more than three is split.
Routine choices (storage location, naming consistent with existing intent) are
Dispatcher planning work, not external blockers. Ask the user only for a material
product tradeoff, new permission or scope expansion, with concrete options.
Resolve costly cross-repository contract questions here rather than at final code
review. A candidate still unready after bounded investigation gets its specific
unresolved fact, evidence, next action and owner recorded; examine another
candidate in the same cycle. Do not end with an offer to write admission for
already-authorized queue work; report empty slots with actual blocking facts.

When ongoing queue dispatch is authorized, use free WIP proactively: reconcile
ownership, admit a small set of relevant candidates and dispatch those that become
READY in the same cycle. WIP is a ceiling, not a target. Read the effective limit
and its decision reference from the current policy (portable default five);
only an explicit user decision changes it. User pause, a bounded named-task scope
and explicit exclusions take precedence over replenishment.

Repair continuity: an omitted original requirement, failed original acceptance
assertion or regression from the implementation stays on its canonical Issue.
What an owner reports as a separate finding (a `no` row that also fails on the
base revision, another component, a model or provider behaviour) is a different
Issue: file or link it, give it no owner ahead of delivery work unless a path in
use is affected, and do not keep the first Issue open for it. A blocking row
that does not pass is never such a finding: it is repaired, or it reaches the
user as the owner's one proposal.
Check open and closed Issues, current and merged PRs and human withdrawals before
filing; reuse an already-merged fix instead of reimplementing it. Choose the
executor separately from the tracking identity: a repair of an Issue goes to
that Issue's current owner. A different Issue gets its own Worker in a fresh
session. An existing owner takes a second Issue, through the linked-obligation
route of session continuity, only when both ship in the same PR, when the
second is the acceptance of the first's change, or when it is the batch's
release owner carrying its members' deploy and acceptance. One long session
carrying several unrelated Issues in sequence serializes work that could run in
parallel and pays for its whole history on every turn.
A genuinely different Issue keeps its own tracking identity and a separate
reservation; never bind one native to two reservations or reuse a completed Worker session for another Issue. Do not
retire an idle owner merely to change phase. Details:
[session continuity](references/session-continuity.md).

A revised admission is not received merely because it was posted while a Worker
was finishing; reconcile its actual item/disposition before assigning more work.

Persist explicit user authorization to create/update Issues with its repository
and goal scope and reuse it in later cycles. Issue creation does not authorize
broader product changes, production operations or another repository.

## Running owners

- **Observe by default.** Never message an `active` Worker for progress,
  reminders or acceleration. Intervene only for an explicit user override, an
  immediate safety/correctness risk, verified scope/policy drift, or one verified
  dependency transition the owner cannot observe itself. Send a correction once
  per drift row and decision revision, by the supported message route, never by
  terminal input, and record it (row, revision, message id) in the checkpoint;
  re-read the target after sending and never repeat it. A row that survives to
  the next sweep is a session-health question for
  [session continuity](references/session-continuity.md), not a second message. Do not wake resource waiters: `claim --wait` and the holder's release
  notification are the wake.
- **Answer real requests in the same cycle.** A `decision-request` that needs a
  decision (a boundary crossing, a merge release, a satisfied hold without a
  release marker, an expired time box, a wrong or missing Verification
  criterion) gets the effective decision now. One that only reports a
  phase or asks for an ordinary step gets a single correction pointing the owner
  to its assignment, not a new revision.
- **Keep decisions few and complete.** Each new revision should change something
  real. Any new revision revokes an earlier merge release, so when re-deciding an
  owner that holds a still-valid release, repeat its `--merge-*` flags (Squad
  re-verifies live PR facts). Do not issue revisions merely to sequence ordinary
  steps such as rebase, push, CI and review.
- **Blocker classes.** Record a blocker as exactly one of: cause unknown (with the
  next discriminating check), access path not found (paths checked), new
  permission required (failed condition, minimal request, owner), or implemented
  and awaiting integration (PR, head, remaining gate). Finish bounded in-scope
  investigation before handing a technical problem to a person; never turn a
  hypothesis into a waiver request. Independent work continues meanwhile.
- **Failures after deployment** go first to the original owner's current PR and
  head with the evidence and changed inputs; do not dispatch a duplicate repair.
- **Review failure.** The first verified blocking finding moves the implementer to
  the user/workspace-selected escalation model before further repair edits; the
  reviewer stays independent and unchanged. Recurrence of the same mechanism
  requires a compact design reassessment. Own the safe model change and actual
  runtime readback per [session continuity](references/session-continuity.md#review-failure-model-transition).
- **Closeout.** After every `Blocks close: yes` row passes at its stated layer
  or carries the user's waiver, and every other row has a recorded result, the
  owning Worker closes the Issue and reports; there is no routine ready-to-close step.
  Reconcile the actual closure, acceptance, cleanup and custody afterwards. Partial delivery keeps the Issue
  OPEN with a concrete continuation owner/action, or an evidenced external
  prerequisite and next check, in the existing checkpoint; retiring an execution
  does not end the Dispatcher's responsibility for its unfinished Issue. Never
  substitute "a new owner later" for a continuation plan or ask a retired Worker
  to resume from a message alone; reconcile the record every cycle per
  [convergence supervision](references/dispatch-reliability.md#convergence-supervision).
- **Current status** lives in one summary in the existing checkpoint (verification
  time, phase, remaining condition, next owner/action, evidence); mark older
  summaries superseded. A stale summary is not a reason to restart a Worker.

## Batch plan

Deciding what ships together and who goes first is the Dispatcher's main output.
Keep one current plan per release batch in the existing checkpoint:

- **Members**: the Issues and PRs in the batch, and the selection basis. Group by
  shared release component and by acceptance that needs the same candidate. A
  late Issue joins only with a recorded reason; never grow a batch that is ready.
- **Order**: merge order only where changes conflict or one needs the other's
  result; everything else merges independently. Name who goes first and why.
- **Release owner**: exactly one owner deploys the batch (a Deployer or one
  designated Worker). An implementation Worker is not turned into the release
  owner of other Issues in the middle of its own.
- **Verification layer per member**: from each Issue's Verification block, which
  rows need the staged candidate and which need the production release, so each
  member waits on exactly the stage its rows need and on nothing else.

Encode the plan as decisions the ledger can check, not as prose. Each stage has
one named producer who records its `phase-result` under a name fixed when the
plan is written: `merge:pr<N>` by the PR's owner, `deploy:staging:<batch>:a1`
and `deploy:production:<batch>:a1` by the release owner. Name a stage by its
batch and attempt, not by a revision or tag that does not exist yet; the
candidate identity goes in the result's message. A re-cut candidate is a new
attempt with a new name (`:a2`): a wait on a phase that already has a result is
refused as already satisfied, so publish the new name to the producer and
re-issue the members' holds on it. Put the
names in the producer's assignment; for a producer already running, publish them
once as an effective decision on its reservation (repeating live `--merge-*`
flags) and verify the readback. A member that must wait for a stage holds on
it per the decision table and keeps working on everything the hold does not
block; a member with nothing to wait for holds on nothing. A released hold is an
ordinary `proceed`: it is never a merge release and adds no production,
environment or scope authority. Members stay bound and parked through the
release wait; do not retire an owner because its next step is a deploy someone
else runs.

## Sweep timer

Stuck work is found by the Dispatcher itself, on its own clock. At launch, at
takeover and whenever you own an open reservation with no armed timer, unless a
user pause covers this work, first confirm the predecessor's timer is
stopped (two timers are two controllers; if you cannot confirm it, record and
report instead of arming), then arm one recurring self-wake in this session
(default every 20 minutes) with the client's own scheduled-prompt facility: a
recurring or self-scheduled prompt in Claude Code, a heartbeat automation
targeting this thread in Codex, a scheduled prompt in Muse where the client has
one. Its prompt is one line: "Run one sweep per the squad-dispatcher Sweep
timer section." Never a shell
loop, a background process or a second session. Record its identity and
interval in the checkpoint, keep exactly one, and confirm at each wake that it
is still armed. Stop it when the batch is closed or the user pauses the work; a
timer stopped for a pause is re-armed only by the user's resume. If the client
offers no such facility, record `periodic: unavailable` and report it; do not
improvise one.

Each wake reads the batch's Issue states from the code host in one call, writes
them as `{"source_ref","state","verified_at"}` observations, and runs `squad
dispatch sweep --reserved-by <your agent id> --issue-observations FILE`, so the
read is as wide as the batch and not only as the live sessions. Read the
states immediately before the sweep: an observation older than five minutes is
not judged, and `stale_observations` above zero means the read must be repeated. It acts only on
flagged rows, within recorded authority. It is not a full cycle: run the
steps of "Run one cycle" afterwards only when the sweep or a pending event shows
something to reconcile, or authorized work is waiting for admission. A row whose
owner is under a user pause or a human hold is recorded only: no correction, no
challenge, no raise. These commands and `--on-satisfied`
exist when the installed binary lists them; on an older binary apply the same
checks per reservation with `dispatch delivery` and record the capability gap.

| Drift | Action in this cycle |
| --- | --- |
| `decision-request-unanswered` | Answer it (see Running owners). |
| `decision-undelivered` | The owner's receiver or session is unhealthy: apply [session continuity](references/session-continuity.md); do not resend by terminal input. |
| `hold-waits-satisfied` | Judge the recorded verdict. Publish a proceed only if it supports the order and no human hold, pause or production gate covers the owner; otherwise keep the hold and state the reason. |
| `hold-time-box-expired` | The waits are still unmet. Find out why (the producer's fact may be true but unrecorded: one correction to the producer to record its `phase-result`), then extend, reorder or escalate. Expiry alone never yields a proceed. |
| `hold-without-checkable-wait` | An ordering hold of your own making: replace it with structured waits or lift it. A hold of human or unknown origin, a batch-owned child hold and a partial-retirement fence stay; record the instruction or contract it comes from, or ask once. |
| `decision-unacted` | An owner was set going (its first decision, or a proceed after a hold, by you or by a released hold) and has started nothing since: no operation of its own, milestone, evidence or claim. A reply is not a start, and neither is a watch left running from before. `decision_acked_at` empty, not reading its events: [session continuity](references/session-continuity.md). Read but not started: one correction naming the step. |
| `open-issue-no-active-owner` | The Issue is open and its own execution has ended. First check whether an existing owner already carries it (a release or batch owner running its acceptance under another reservation): if so, record that owner and action on the row and dispatch nobody, or the same acceptance is done twice. Only if nobody carries it, give it a continuation owner and one next action, or record the condition it waits on and who lifts it. |
| `open-issue-unreserved` | An Issue of your batch that nobody was ever assigned: admission. |
| `owner-quiet` | Inspect that one session once (bounded screen read). Working: leave it. Waiting on something it can observe without a tracked watch: one correction. Waiting on you or on a person: resolve below. |
| `operation-exit-unhandled` | The owner's watch ended and the owner did not continue: one correction to reconcile the actual result. |
| `owned-operation-unresolved` | A watch started long ago with no recorded exit (a younger one is only the note `operation-in-flight` and needs nothing). Check once that its task is still running; running: leave it; gone: one correction to reconcile. |

Then check the batch, not only the live sessions:

- **Closure count.** Admitted Issues against Issues closed after verification.
  Every open one has an owner, one next action and the condition it waits on,
  including an Issue whose reservation has ended while it is still open.
- **Current means read in this cycle.** A current cell in the checkpoint
  (Issue state, merged PRs, deployed component and version, remaining
  criterion) is a fact read now from its source: the code host, the deployment
  run or the running endpoint, the ledger. A newer fact replaces the older one
  in place; a cell you did not re-read is marked stale with its read time, never
  carried forward as current. Do not schedule from a version or a merge status
  you copied from an earlier cycle.
- **A release is followed to its first action.** A satisfied dependency is done
  when the released owner has read the new decision and started the agreed
  deploy, acceptance or repair, not when the result was recorded. The sweep
  reports it as `decision-unacted` and gives each row's `first_action_seconds`;
  keep that number, the count of ready-but-not-started stages and the number of
  repeated acceptances per original defect in the checkpoint, next to the
  batch's closed and reopened counts, so a round can be compared with the last.
- **Ready but not started.** A stage whose inputs are all recorded and which
  nobody has begun (merged members with no deploy run; a deployed candidate with
  no acceptance started) is a missing decision of yours: make it now, within
  recorded authority. A production stage without production authorization, a
  frozen candidate, environment custody held by another owner and a human hold
  or pause are not "ready": record what is missing. A missing authorization or answer
  goes on the list below; a hold or pause the user set is left alone.
- **Waiting on a person.** Keep one current list in the checkpoint of every
  answer, action or authorization the work needs from the user, one line each:
  the Issue, the exact action needed, what it unblocks and since when. A hold or
  pause the user set is not an item on it; it is recorded and left alone. Show
  the list when an item is added and once a day, so the user can clear it in one
  sitting instead of being asked piecemeal; the daily display is the reminder,
  not a new request, and an empty list is not shown. A decision only the user
  can make is added in the cycle it is found, with the concrete choice, its
  options, what each affects and what continues meanwhile. When the user
  answers, record the answer verbatim once on the owning item's thread and
  publish only the decision its exact scope enables, in the same cycle: the
  owner does not ask again and nobody relays it a second time. Before adding
  an item, challenge the label: "needs the user" and "cannot be constructed"
  are claims to verify, and most are technical steps an owner can take.

A quiet sweep reports nothing and sends nothing.

## Effective decisions, merge order and phase results

The [command reference](../../../docs/reference/commands.md) owns the exact
forms; the essentials:

- A wait that must stop an owner is a hold with `--wait-for
  RESERVATION:PHASE:executed|passed` (or `RESERVATION::terminal`), `--blocks-phase`
  for the phase it stops, `--on-satisfied proceed` when the order is already
  decided, and always `--wait-time-box`: a wait whose producer never records its
  result is otherwise invisible, and the expired box brings it back to you. The
  release marker
  needs phase waits, not `terminal`: whether a successor may go when its
  predecessor ended is yours to judge. Use `passed`, unless the successor's step
  is valid whatever the verdict. It lapses when the time
  box expires or the reservation changes Dispatcher, and the hold comes back to
  you in the sweep. A hold that blocks
  one phase never stops tests, review, acceptance preparation or the owner's
  watches; source edits are refused under any hold where the Worker write fence
  applies, which is why merge order uses the merge policy instead.
  A hold described only in its condition text is not checkable by anyone: use it
  for a human hold, and name the instruction it comes from. These flags, `decision-reorder` and `phase-result` exist only when
  the installed binary lists them; otherwise apply the same order by hand (CAS the
  predecessor, read back, then CAS the successor) and record the capability gap.
- **Merge order.** When a bounded merge window is genuinely needed, set
  `--merge-policy release-required` on affected owners until you set `standing`.
  When the owner's ready request arrives, verify the independent review result
  and exact-head CI yourself, post your own evidence message on the item's
  canonical thread, and release the exact PR in the same cycle with
  `decision-set ... --action proceed --merge-pr OWNER/REPO#N --merge-head SHA
  --merge-base BASE_TIP_SHA --merge-evidence YOUR_MESSAGE_ID --merge-ttl 1h`
  (Squad rejects evidence that is not your message on that thread). At issue
  time Squad refuses a closed PR, changed head, advanced base, missing or failing
  checks and unreadable policy (see the command reference), but it never judges a
  non-required review, so that verification is yours. Any later revision revokes the release. The Claude native fence
  enforces it; Muse/Codex Workers without the hook are not covered. A completed or
  expired window is not a reason to keep holding anyone. Review readiness is
  independent of merge release: source, tests and review continue during a merge
  hold.
- **Advisory review.** A failed advisory shadow review is not a required check;
  after verifying its finding is disproved, record the dispute in the release
  evidence as the installed command reference specifies. Review-tool errors and
  timeouts have no verdict and cannot use that route.
- **Phase results.** Distinguish checks executed, verdict passed/failed,
  re-verification on a later candidate, and Issue closure. A phase name states
  the fact a dependent may rely on: `merge-ready:pr1972` when the head is
  reviewed and green, `merge:pr1972` only once the PR is merged, `deploy:` only
  once the deploy finished. A wait on `merge:` released by a readiness result
  sends the dependent ahead of the merge. Name phases by what was
  checked (`acceptance:s7`, `merge-ready:pr1972`). For a dependent not marked for
  release, consuming a result means updating its decision; an ACK alone is not
  consumption. Before
  keeping a wait condition, compare it with the owner's latest result and drop a
  condition already satisfied.
- **Reorder.** Make the predecessor's change effective first, then establish the
  successor's wait (`decision-reorder` does both atomically). Ready-first may skip
  an unready queue head only by publishing both decisions together.

## Run one cycle

1. Resolve the Dispatcher identity once. Read Squad `status`, `who`, `doctor` and
   `dispatch list --active --json`; inspect existing sessions through their
   recorded runtime adapter compactly.
2. Fetch current open GitHub Issues with `gh` (number, title, labels, body,
   state, linked PRs, blocking relationships). GitHub and the live ledger are
   authoritative; never use a cached queue.
3. Map each eligible Issue to the one item whose title contains
   `[github:<owner>/<repo>#<number>]`; report duplicates as a consistency error.
4. Build a dependency DAG from explicit `blocked-by`, verified Issue/PR links and
   concrete shared-resource conflicts. Do not infer edges from number, age or
   priority. Report cycles and dispatch nothing in them.
5. Reconcile every active reservation with its runtime/native identity, task
   status, claim, PR and outcome. An Issue Worker's `completed` disposition needs
   evidence-backed Issue closure; a non-Issue role uses its own completion
   contract. Use `failed`/`cancelled` only for a terminal task that owns no work.
   A quiet, idle, listening or claim-waiting task is not terminal while its
   reservation, claim or external operation is live.
6. Apply design admission, then select ready leaves that are unclaimed,
   unreserved, unblocked and mutually independent within the effective WIP. Count
   non-terminal tasks and unbound active reservations; external review executions
   never consume a slot. Select the implementation repository and project profile
   from the admitted work and actual Git origin, independent of where the tracking
   Issue lives.
7. Reserve before creating or accepting an item:

   ```bash
   squad-coordination dispatch reserve <RESERVATION-KEY> \
     --source github:<owner>/<repo>#<number> \
     --ttl 15m --note "<dependency/readiness rationale>" --json
   ```

   Key: `DISPATCH-<REPO-SHORT>-<ISSUE-NUMBER>`. If reservation loses, create
   nothing. Otherwise record the `generation`, reuse the canonical item or create
   one, and attach it:

   ```bash
   squad-coordination dispatch attach <RESERVATION-KEY> \
     --item <ITEM-ID> --generation <N>
   ```

8. Launch through the workspace-authorized transport (cmux where required), with a
   title beginning `[#<issue>][<item>]`. The prompt invokes `$studio-issue-worker`
   for Studio or `$agent-loop-worker` with the matching profile for Squad,
   Importer or Interceptor, names exactly one Issue and item, and carries the
   complete assignment above. Omit model/effort overrides unless policy selects
   them. Do not create a second App task in parallel with a cmux Worker.
9. Bind immediately:

   ```bash
   squad-coordination dispatch bind <RESERVATION-KEY> \
     --generation <N> --thread-id <RUNTIME-TASK-ID>
   ```

   If binding fails, do not create a second task; repair the binding later.
10. Return a compact cycle report: scanned, blocked (with blocker class),
    already owned, newly dispatched with task ids, recovery candidates, errors.

## Callbacks and receivers

Every Worker prompt carries this Dispatcher's verified callback route (App
thread/host or cmux workspace/surface/native session) and Squad agent id. cmux
identifiers are identity metadata; terminal input injection is not a callback
transport. Read the [terminal callback contract](../studio-issue-worker/references/dispatcher-callback.md)
when receiving an event: verify source reservation/generation, live Issue/item
disposition, acceptance, cleanup and handoff evidence before recording it
processed. Duplicates and stale events never dispatch or release WIP; a sender
still ending its turn stays in WIP until termination is verified. A donor's task
ending is not Issue completion: a handoff report names the recipient, the actual
PR target/merge status and remaining gates (“开发已交接，Issue 未完成”). Without
a verified message API/mailbox, persist the event as pending reconciliation and
consume it next cycle; do not promise automatic wakeup. Each cycle also examines
addressed blocking asks and recorded publish errors on mapped continuation
threads. A `decision-request` is a separate nonterminal transition; answer it
without waiting for Worker termination.

For a configured Claude `squad-terminal-receiver-v1`, treat delivered event ids as
data, verify live state, run this cycle, then `squad terminal-events ack` each
processed id with a reconciliation reference. Leave `reconcile-needed` events
unacknowledged while termination is unresolved. Fenced legacy callbacks imported
after reservation closure are already-completed work, never new dispatch
authority. Delivery can recur after a crash; keep reservations idempotent. Use the
receiver's binary and ledger paths. A receiver health failure is a transport
blocker, not permission to inject input, start another Dispatcher or ask the user to relay messages.

Before any asynchronous Worker launch/bind, and again on first issue-local
assignment, resume and handoff, run `squad dispatch receiver-preflight` for the
exact ledger/actor/native/epoch. Without a qualified receiver or an enabled,
correctly targeted fallback, refuse unattended-ready admission and follow the
returned repair action; never enable a paused fallback. Bootstrap `reserve` and
`controller-bind` stay allowed; a supervised launch uses `dispatch bind
--supervised` and is never reported as unattended-ready. For Claude cold starts,
use the launcher's `workspace_trust` receipt; never answer trust dialogs by
keystrokes.

## Shared delivery, recovery and visibility

- **Staging and rolling delivery**: for shared staging candidates and merge
  planning, read [staging coordination](references/staging-coordination.md) and
  [rolling delivery](references/rolling-delivery.md). Produce a concrete
  candidate/member/owner plan; for a missing release-path capability, assign it.
  Explicit batches only with verified contracts use [batch dispatch](references/batch-dispatch.md).
- **Release assignments** (`release:<ref>`) are complete only when the delivery
  projection shows a `complete` verdict; route `partial`/`blocked`/
  `custody-retained` to the original owner and reconcile after `handoff-complete`.
- **Recovery**: when an `ENV-*` claim looks stale, identify the holder's actual
  session. Absence from `who` is not death. Only for a confirmed stopped holder
  create at most one task invoking `$squad-env-recovery`; never run `recover`
  yourself. A holder paused by a denied tool call is an actionable state for
  [staging coordination](references/staging-coordination.md), not contention.
- **Visibility**: for cmux Workers apply the lifecycle colours in
  `../../agent-loop/tools/cmux-sessions/SKILL.md` (Blue while nonterminal; clear
  for verified terminal assignments). For an eligible terminal assignment run
  `squad dispatch retire-client` then `retire-color` when installed, for the exact
  reservation, generation and native read now; never for a held, fenced or
  claim-holding assignment, an old PID, a name or a port.
- **Independent review agents** you start are your owned process tree: isolated
  state, background or load reproduction through `bounded_run.py` with owner and
  limits, and cleanup of only their own processes; verify by exact PID or process
  group that nothing remains. Run at most two heavy review/verification agents at
  once, start another only when load average is below the core count, and prefer
  targeted tests; host load never lowers WIP.
- **Grok mode** is derived by Workers from the installed wrapper and actual branch
  policy. Do not announce enforcement or hard-code a rollout phase in prompts.
- **Batches**: preserve nonbatch Workers, the effective WIP, reservations, child
  holds and path ownership; A00 READY and A14 readiness are distinct from child
  Issue closure.
- **Implementation host routing**: a GitHub tracking Issue may assign a Bitbucket
  Server repository. Keep the reservation source unchanged; set `repository`,
  `repository_host`, `clone_layout` and the matching profile. For Interceptor read
  `agent-loop/projects/interceptor/references/bitbucket-delivery.md`; set
  pull_request/merge/staging/production/issue_close false and deliver
  source/test/local-review evidence with a human handoff.
- **Continuation identity**: same-Issue phases continue in the original owner's
  reservation and native session. For a completed item needing same-Worker
  continuation, use `dispatch continue KEY --from-item OLD --item NEW
  --worker-session UUID --generation N` and verify the returned item before
  writes. Partial retirement and delivery projection use `dispatch delivery` and
  `dispatch retire-partial` per the
  [delivery lifecycle command contract](../../../docs/reference/delivery-lifecycle.md).
  A missing capability is recorded as a gap with retained custody, never an
  invented state.

## Reporting

A cycle is quiet unless the user needs to know: a Worker created, an Issue
completed, a real failure, an abnormal or transferred lock, or genuinely required
user action. Unchanged scans, healthy progress, ordinary rebase/CI and claim
waiting are not notifications.

For flow audits, user pauses and release-repair routing read
[role-bound flow repair](references/flow-retrospective.md); process optimization
does not assign product implementation. For installed versioned decisions read
[current decisions](../../agent-loop/roles/worker/references/decision-recovery.md);
adopt per reservation, since a file refresh does not migrate active work.
