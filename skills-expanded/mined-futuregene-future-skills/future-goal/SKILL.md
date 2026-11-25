---
version: 5.5.0
name: future-goal
description: FutureOS goal control plane — manage long-running goals, todos, human gates, workers, monitors, validated completion, multi-model ensembles (one brief run by different models, judged blind, then synthesized — "让不同模型分别做再合成", "取长补短"), and exploration mode (a scout returns a direction proposal instead of an artifact — "该往哪个方向走"). Use for cross-session work, ongoing task status, "keep working", "run overnight", or /future-goal; an explicit /future-goal that carries work dispatches that work to workers instead of doing it inline. A message with no work to dispatch needs no goal.
allowed-tools: Bash(future:*)
category: tools
---

# Goal Control Plane

A durable goal and kanban, not an autonomous policy engine. The kernel enforces
state/lease/acceptance consistency; the agent chooses strategies and judges
results. Persistent evidence is authoritative; chat/session context is a cache.

## 1. Inspect and agree on the operating contract

**Dispatch rule — read this before choosing a workflow.** A `/future-goal`
token is a request to run the work it accompanies as a supervised goal, not a
request to read this file and then answer inline. It needs no verb and no
argument: the task is whatever the message asks for, so a bare `/future-goal`
appended to a task is a full invocation. An explicit invocation overrides the
smallest-workflow choice in step 3 — choose the smallest workflow that still
puts the work in a worker session.

- A phrase naming a count ("multiple workers", "a few agents", "three
  reviewers", "in parallel") sets the minimum number of workers. With no
  count, use your own decomposition: two or more when the work has genuinely
  independent parts.
- You own decomposition, dispatch, acceptance and synthesis. Do not claim an
  `advancement` todo and finish the work in this session — one session wearing
  both hats is the outcome this rule exists to prevent. `coordination` tasks,
  synthesis and reviewing artifacts stay with you.
- Only two things justify doing the work inline: the message carries no work
  to do (a question about the goal itself), or the user says not to create a
  goal. "It is just one task" is not a justification while work is attached.
  If the work genuinely cannot be split, still run one worker and say in one
  line why, instead of doing it here and calling the skill unnecessary.

1. Run `future goal status` in the project directory. Resume a matching goal;
   do not create duplicates. A message with no work to dispatch needs no goal
   (see the dispatch rule above).
2. State the objective, deliverables, acceptance checks, operating budget,
   escalation conditions and worker configuration. Ask for confirmation when
   these were not already specified.
   - **Convention (what you should choose):** the default worker model AND
     thinking level are this session's own — the CLI now enforces that by
     inheriting from the supervisor. Check availability with `future models`.
   - **CLI behaviour (what actually happens):** a worker INHERITS the model and
     thinking level of the goal's supervising session. With neither flag,
     `future goal run` reads the session recorded by `supervisor register
     --session-id …` and applies its configuration to the fresh worker session,
     printing `⚙ worker … (inherited from supervisor)`; when the goal has no
     supervisor session to read it falls back to the agent's own defaults
     (`future models` prints the default model) and says so on the same line.
     Pass `--model` / `--thinking-level` only when the task genuinely needs a
     different level, and state the reason in the same breath: an override is
     printed as `⚙ worker … (override; supervisor was …)` and stamped into the
     run header as `model_source=override`, so an unexplained one is visible to
     whoever reads the run log next. A `--resume-session` relaunch keeps that
     session's own configuration unless a flag overrides it. `--max-turns`
     (default 6) is the caller's choice and is never inherited.
   - **Provenance is recorded, not assumed:** every run header carries `model`,
     `thinking_level` and `model_source` (`supervisor` / `override` / `default`
     / `session`). A missing field means an older log, never "nothing was
     overridden".
   - Never change a user-pinned model, thinking level, budget or acceptance
     standard without permission.
3. Choose the smallest adequate workflow — every one of these dispatches at
   least one worker session, and Light is one worker, not this session:
   - **Light:** one worker and targeted checks; no automatic research swarm.
   - **Standard:** implementation/exploration plus a separate verification task.
   - **Heavy:** genuinely different method families in parallel, synthesis and
     independent validation; justify the communication cost.
   - **Ensemble:** one frozen brief, several genuinely different *models*, blind
     judging and synthesis (§7). Choose it when the user asks for cross-model
     combination ("让不同模型分别做再合成", "取长补短", "1+1>2", "多专家") or
     when a high-value deliverable's quality justifies N independent candidates.
     Different methods or prompts on ONE model is Heavy, not Ensemble; N runs of
     the same model is neither — say which of the three you are doing.
   - **Exploration:** when the next step is a CHOICE rather than execution, the
     unit of work is a scout and the deliverable is a direction proposal, not an
     artifact (§8). Use it when a stalled slice needs a different direction or
     when the user asks "which way should we go".
4. Set budget checkpoints in wall time, cost and/or attempts. `--max-turns`
   bounds outer loop iterations, NOT tokens or inner model/tool calls. Do not
   advertise a hard monetary cap unless the underlying runtime enforces it.

State root = process cwd + `.future/goal/`, or `FUTURE_GOAL_ROOT`. `init --cwd
DIR` records the project anchor; it does not relocate the ledger. Add the state
directory to `.gitignore`. Use `future goal <command> [<verb>] --help` for exact
flags; a leading group name is optional, so `future goal goal init` and
`future goal init` are the same command. Unsupported flags are errors. Before
using this version, check that `supervisor steer --help` lists `--interrupt` and
`supervisor watch --help` exists. If not, update the executable; do not apply
the old interrupt semantics or write new-schema events with an older binary.
Agent transport discovery is shared with the CLI; tests must use an isolated
root and fresh agent endpoint.

## 2. Create and wire the work

```bash
future goal init --objective "..."
future goal supervisor register --goal G --session-id YOUR_CURRENT_SESSION_ID
future goal todo add --goal G --text "..." --owner worker-a --verify "cargo check -p X"
future goal todo add --goal G --text "Read work/a.md and independently verify ..." --blocks T1 --owner reviewer
future goal todo add --goal G --text "Final review and handoff" --class coordination --blocks T1,T2
```

Copy YOUR session ID from the environment, not an old worker's session. Re-register
when continuing in another session. The bootstrap todo from `goal init` is
intentional: complete its connection check or supersede it with a stated reason.

- `todo add` succeeds with `todo <id> added to <goal> ✔`, not `created`.
  Check the exit status, then extract with `todo\s+(todo_[0-9a-f]+)\s+added`.
  Require exactly one match; on failure STOP instead of passing output/empty
  variables into `--blocks`.
- `--blocks` on an advancement task names prerequisites. On a gate/blocker it
  names dependents. Create referenced todos first. Add/update reject unknown
  references, self-links and cycles before writing; do not rely on this with
  older executables. Final verification must depend on ALL producing tasks.
  `todo update --goal G --todo-id T --blocks A,B` REPLACES the set;
  `--blocks ""` clears it; omitting the flag preserves it. Repair legacy dangling
  references one todo at a time with update, then run `task-graph --goal G` before
  dispatch. A graph error is not proof that an older worker will refuse to run.
- `--owner A` is durable assignment, independent of lease expiration. Leave it
  unset only for intentionally shared work. Use a unique agent ID per concurrent
  run. `coordination` tasks are supervisor bookkeeping, never worker frontier
  items. Class is immutable; supersede and recreate a misclassified task.
- Every handoff names durable artifact paths in the successor's task text.
  Envelope snippets are bounded summaries, not full knowledge transfer. Every
  direct upstream gets an index entry, but full evidence/artifacts must be read;
  superseded work is not a verified result.
- Freeze acceptance criteria before implementation. Both automatic and manual
  advancement completion check nonempty evidence and every `--acceptance "a,b"`
  token. A normal model return cannot bypass this floor; rejected handoffs stay
  open with a diagnostic. This only checks token presence, not factual correctness.
  Keep required evidence in the final handoff, not only early narration.
  A file-existence check validates
  existence, not the quality of a report. Attach `--verify` for deterministic
  checks, and assign scientific/content correctness to a reviewer.
- Validators have an independent 120-second default timeout, bounded output
  capture, and process-tree cleanup. Set `FUTURE_GOAL_VALIDATOR_TIMEOUT_SECS`
  to a positive number for known longer checks. Commands use `sh -c` on Unix
  and `cmd.exe /D /S /C` on Windows; write platform-appropriate commands or call
  a portable validation program.

## 3. Dispatch without becoming a polling agent

A goal with todos and no `future goal run` is a plan, not progress. Dispatch
before reporting readiness, and treat each agent id showing up in
`future goal worker list` as the proof that work actually left this session.

Declare each task's complete write set with `todo add --required-write-scope`:
comma-separated file/directory paths, relative to the goal's recorded cwd (NOT
where the worker or inspecting CLI happens to run). Task scopes override the
agent's fallback `--workspace` for that task. If omitted, the agent declaration
applies; auto-registration defaults it to the entire process cwd. The guard
checks live task scopes atomically with lease acquisition, so disjoint tasks can
share a checkout without forcing. These declarations are not a filesystem sandbox.

```bash
future goal todo add --goal G --text "Write papers/a.md" --owner worker-a --required-write-scope papers/a.md
future goal todo add --goal G --text "Write papers/b.md" --owner worker-b --required-write-scope papers/b.md
```

Do not give every worker the shared parent `papers/` when they only write distinct
files: directory/descendant scopes overlap. Shared read-only resources are not
write scopes. Include ALL actual writes (logs, indexes, caches too); serialize or
separate real shared writes rather than hiding them from the declaration.

Version check: `todo add --help` must describe scopes as relative to goal cwd.
Older binaries only record `required_write_scope` and ignore it in the guard;
upgrade, or explicitly onboard each agent with its complete disjoint fallback:
`agent onboard --goal G --agent-id worker-a --workspace papers/a.md` (`--workspace`
is relative to the onboarding CLI cwd). Absolute task paths alone do not fix an
older guard. Check startup errors in worker logs, not just the `ended` status.

```bash
future goal run --goal G --agent-id worker-a --model M --thinking-level L --max-turns 1
future goal worker list --goal G
future goal worker tail --goal G --agent-id worker-a --lines 30
```

`run` detaches by default and prints its PID/log path. Verify the worker started;
then let event notifications wake you. The CLI also launches an independent,
non-LLM watchdog. It notices dead holders even if the LAST worker dies, persists
notifications before connecting to the agent, coalesces them into batches (up to
32 notes each), and retries undelivered batches. It does not choose a model,
replan, or relaunch work.

While you are busy, the batches that arrive queue behind your run and fold into
ONE next turn: a single prompt can carry several `[future-goal] goal G: …`
sections, one per batch. Reconcile it as one reading of the current board, not as
one question per section — act once on the state you observe, and do not restart a
worker merely because an old report is in the bundle. Batches arriving while you
are idle still get their own turn, and a folded batch is acknowledged as `merged`
(never silently dropped), so `supervisor events` stays complete.

- `supervisor register` also ensures this watcher exists. After a host reboot or
  a watcher failure, resume supervision with `supervisor watch --goal G` (foreground;
  run under the host service manager for boot persistence). `--once` performs one
  reconciliation. There is no promise of surviving power loss without a host service.
- `FUTURE_GOAL_NO_DETACH=1` is for foreground embedding/tests; `--detach` is an
  internal child marker, not a user request to background the command.
- Notifications are triggers, not authority. Automatic completion produces a JSON
  `task_delivery` receipt with goal/todo/agent/run/session IDs, validation, recent
  evidence, full-text journal path and `pending_other_todos` across all owners.
  It means `awaiting_review`, not a scientific pass or global completion. On
  wakeup, read current status, the batch and decisive artifacts. Old completion/
  death reports may refer to a superseded run; do not blindly restart them. A
  bundled prompt is several batches of accumulated event history, so reconcile
  against `status` and `delivery status` rather than treating each section as
  fresh news.
- Do not spend LLM calls on repeated sleeps and status polling. Use the watchdog,
  an external event source, or a blocking deterministic monitor. Combine necessary
  observations into one read and return until a decision is needed.
- A live log is PER TURN. `worker tail` resolves the current one. New journals
  retain full reply `text_chunk.text`; bounded memory/ledger summaries keep recent
  text, not just the opening plan. A frozen old `.live.jsonl` or its final error
  line does not prove the worker process died. Read the receipt's exact run, not
  whichever session file was most recently modified.
- Each launch defaults to a fresh session. To resume, explicitly pin that
  worker's session with `--resume-session ID`; a missing session falls back to
  fresh. Never use another worker's goal-level retention value blindly.
- `--max-incomplete-retries` bounds incomplete-stream retries (default 3).
  Infrastructure errors are not failed scientific hypotheses. Use evidence and
  failure classification to decide retry versus repair; nonzero exit is not
  necessarily a budget stop.

External scoring, remote experiment results or GPU readiness need an explicitly
owned monitor/adapter with the existing request ID, result endpoint, next check,
actual wakeup mechanism, timeout and resource allowance. The watchdog does not
query these services; `report` remains pull-only. Persist a receipt once and query
it rather than repeating a side-effecting submission. If no persistent monitor is
running, disclose that. Completed delivery plus queued scoring is still unverified.

## 4. Observe three different things

| Layer | Evidence | Interpretation |
|---|---|---|
| Liveness | PID, lease, stream connectivity | Can this worker still execute? |
| Activity | actual tool execution, usage and elapsed time | Is it doing something? |
| Progress | new artifact, validation result, measured improvement, rejected hypothesis | Is the objective advancing? |

`write/edit` starts are only an artifact-activity proxy; generic `shell` calls
are not automatically writes. Provider `input` and `execution` events must not
be double-counted. Reading/research can be productive without writes, and file
churn can be useless. No-write signals are advisory, not proof of a stuck model.

At a checkpoint, ask: what changed since the previous attempt, what evidence
supports it, what remains uncertain, and why is another attempt worth its cost?
Request a durable milestone with `future goal report` when appropriate; never
force dummy file writes to satisfy a detector. Compare supervisor overhead,
useful verified outputs, repeated work and human interventions, not raw turns.

## 5. Guide, interrupt, escalate

```bash
# Routine guidance: next boundary, no discarded in-flight reasoning
future goal supervisor steer --goal G --agent-id worker-a --instruction "Read the new measurement before retrying"
# Urgent correction / stop-loss: actually interrupts the running session
future goal supervisor steer --goal G --agent-id worker-a --interrupt --instruction "Stop using the invalid dataset; use the corrected input"
future goal worker stop --goal G --agent-id worker-a
```

Steering is recipient-scoped; broadcasts are acknowledged independently by each
worker. IDs distinguish same-second instructions. Acknowledgement follows durable
completed-turn writeback; a crash can replay guidance. Make instructions idempotent,
not "perform this irreversible action once". New instructions replace older ones
only in the same target scope. A stopped run still needs a relaunch if work remains.

Routine `todo update --text` also takes effect at the next boundary. Model/thinking
changes require a new configuration/session, not steer. Seek user consent for a
change to confirmed configuration. Preserve useful context via durable handoffs.

Worker uncertainty goes to the supervisor first. The supervisor decides whether a
human decision is needed. A gate freezes only its dependents; `--global-gate` is an
explicit goal-wide freeze. Independent work can run AND complete. Resolve gates
with `gate resolve`, not `todo complete`. Use user-actions for nonblocking requests.

`goal cancel`, `goal delete`, `todo supersede` and `worker stop` own lifecycle
cleanup; do not kill unrelated agents. Workspace guards prevent conflicting
writers; `--force-workspace` is only justified with proven disjoint write sets.
Record the exact paths and override rationale in a durable note before forcing;
the ledger records effective paths and a `forced` marker, not your rationale.
Prefer correcting declarations over bypassing the guard. Completed tasks release
leases; known-dead holders are ignored where PID probing is supported. Manual
claims without a host PID remain protected until release/expiry.

## 6. Review and close honestly

Handoff schema (put results first in the artifact, not just a notification):

- Actual task/run identity, input/candidate/validator versions and result status.
- Deliverable paths, original evidence references and reproduction commands.
- New evidence/metrics versus the previous attempt.
- Rejected approaches and why, including counterexamples.
- Assumptions, uncertainties and acceptance gaps.
- Next useful check and expected resource cost.

`todo complete` requires nonempty evidence and `--successor T` or `--no-follow-up`.
Manual completion intentionally does NOT execute `--verify`; review it as a manual
judgment/override, never claim the machine check ran. `--force` is an explicit
operator override, not a standard worker completion path. A rejected validator
means inspect the output and diagnostics; changing the validator requires a
justified contract correction, never lowering the bar to get a pass.

Delivery is initially `delivered`, not verified. Read/reproduce the artifacts and
record `delivery record --outcome verified|failed|rework`. The watcher also flags
pending verification after five minutes even when no more turns occur. A successful
review must name its evidence; receipt presence alone does not prove correctness.

Closing one slice does not invent successor edges to other runnable work.
Explicit follow-up tasks belong in the task graph; inspect all owner-scoped,
blocked/deferred and verification work before global closeout.
Use `frontier show` to verify terminal closure. If the budget expires or further
attempts have low expected value, stop workers, preserve the best artifacts, and
report **not achieved / partial / blocked / awaiting decision** with the gap. Do
not close unresolved acceptance gaps or label a paused goal successful. Obtain
approval to expand budgets. "All methods impossible" is not a prerequisite for
honestly stopping an open-ended research task.

## 7. Ensemble across models

An **ensemble** goal is ONE deliverable produced by several *different models*
from the same brief, then merged by the orchestrator into a single better result.
Models differ in what they saw and practised during training, so their weak and
strong spots differ too; combination pays only where those spots differ and the
comparison is neutral. Four conditions carry it — one frozen brief, genuinely
different minds, blind judging, evidence-based synthesis — and each has a
predictable way to fail:

1. **Freeze the brief before dispatch.** Write `ensemble/brief.md`: objective,
   deliverable path and format, constraints, and the acceptance checks that will
   decide between candidates. Every candidate gets that same text (name the file
   and paste it); any deviation (a model without image input, a different tool
   allowance) goes into the brief, never improvised per worker. Freezing the
   criteria before reading any candidate is what keeps the comparison honest: a
   checklist written after the best answer arrives scores that answer highest.
2. **Roster genuinely different models.** `future models` shows the registry and
   each model's context/thinking ceiling. Prefer different families and the
   strengths the deliverable needs (code-specialised vs long-context reasoning vs
   writing), and record the roster with the reason per model. Two siblings of one
   family mostly duplicate each other — say the roster is not diverse instead of
   calling it an ensemble. Keep thinking level and turn budget equal unless effort
   asymmetry is itself the experiment, and record that too. Cost is roughly
   N × candidate + judge + synthesis + verification per round, so state N and the
   budget in the operating contract (§1) and add no round without a checkpoint.
3. **Isolate candidates.** One owner, one todo, one output directory per
   candidate, declared as that task's entire write scope:

   ```bash
   future goal todo add --goal G --owner cand-a --class advancement \
     --text "Candidate A: from ensemble/brief.md write ensemble/a/solution.py and ensemble/a/notes.md; do not read or edit ensemble/b/ or the brief" \
     --required-write-scope ensemble/a/ --verify "python ensemble/a/check.py"
   future goal run --goal G --agent-id cand-a --model M_A --thinking-level high --max-turns 1
   ```

   Mutual blindness is the diversity being purchased: each task text forbids
   reading another candidate's directory or editing the brief, and two candidates
   writing one path is a scope conflict, not collaboration. Candidates are not
   told which models the others are.
4. **Judge blind, then synthesize.** Build one judging packet: outputs relabelled
   `C1..Cn` (model, agent id and path stripped, order shuffled), the frozen brief
   and its checklist. Give it to a judge that is not among the candidates when the
   roster allows it, and ask for per-criterion scores with supporting evidence plus
   "what is uniquely right, and what fails uniquely, in this candidate" — not one
   overall winner, because the synthesis needs the pieces. Then this session (or
   one dedicated synthesis worker with its own write scope) produces the
   deliverable: start from the strongest candidate and graft, rather than
   averaging. Resolve disagreements in the order the brief fixes — hard acceptance
   checks, then correctness, then style — never merging two contradictory answers
   into one that satisfies neither; re-run the deterministic checks after every
   graft into code or data.
5. **Require the synthesis to beat the best candidate.** Run the frozen checks on
   the synthesized artifact and on the single best candidate, then compare the
   judged criteria. If synthesis does not clearly win, ship the best candidate and
   report that — ties are common, and pretending otherwise discards the evidence
   the ensemble was paid for. Record per candidate: model, thinking level,
   run/session id, path, check result, judged strengths and failures, and what was
   grafted from where. That attribution is what makes the next roster choice
   better than a guess.

Close as §6 requires (one delivery record per candidate, evidence naming the
checks actually run), and keep the candidate directories until the final artifact
is verified — they are the reproduction evidence for the comparison, not scratch
space. Brief, task-text, judging-packet and provenance templates:
`references/ensemble.md`.

## 8. Exploration mode: a scout delivers a direction, not an artifact

When the question is *which way to go* rather than *do this*, the unit of work is
a **scout** (`todo add --class scout`) and its deliverable is a **direction
proposal**: a small set of candidate directions, each with acceptance items and
its own termination condition.

- `--kill-when "stop exploring this direction when <X>"` is REQUIRED. A scout
  without a termination condition is an unbounded budget sink, so `todo add`
  refuses it. The kill_when reaches the worker through the turn envelope.
- The worker records the proposal with one command (the envelope prints this
  exact line, including the field syntax — do not improvise it):
  `future goal direction propose --goal G --scout-todo T --trigger stall --question "..." --observation "..." --evidence PATH --candidate "title|class|route|kill_when|acceptance1;acceptance2"`
  `class` is `scout` (a deeper exploration; then `kill_when` is required) or
  `advancement` (kill_when may be empty, acceptance carries the contract);
  `route` is `fork` or `revise:<TODO_ID>`. The legacy four-field spec
  `title|route|kill_when|acceptance` still means `class=advancement`.
- **A proposal never creates a todo.** `direction accept --proposal P --candidate
  C` is the decision that turns a candidate into work (`advancement`) or a deeper
  exploration (`scout`); `revise:T` makes the new todo continue AFTER T
  (`blocked_by_gate = T`) instead of editing T in place. The todo carries
  `origin_proposal`, and `status --format json` exposes it — that is the only
  machine-readable link from the decision to the work.
- Completion gate: `todo complete` refuses a scout that no proposal names. Check
  the ledger with `direction list`; `reject` requires a reason; `expire` frees the
  direction, and an expired or rejected proposal cannot be accepted.
- The scout turn is a READ-ONLY contract: no edits to existing files, no
  implementation, and the only permitted writes are evidence notes inside the
  declared scope (none declared means no file writes at all). Its fixed text is
  capped at 1500 bytes because every scout turn re-sends it, so add constraints
  instead of prose.
- Known limitation: dedupe normalizes titles only (English verb prefixes plus
  containment), so a Chinese and an English phrasing of one direction are not
  recognised as duplicates.
- When a slice stalls twice, the kernel raises an `exploration_gap` obligation —
  a report that the goal owes an exploration, not an automatically created scout.
  Creating the scout is your call.
