---
name: agent-graph
description: Execute a short TODO as a real parallel dependency graph with native CLI makers, independent reviewers, targeted repairs and a small resumable state. No planning or acceptance contracts for new tasks.
---

# Agent Graph: TODO 1.0.1

For substantial delegated work with real dependencies or parallel scopes: one
task list, one scheduler, one maker/reviewer pair per task. A small independent
delegated change uses todo_pair.py without the graph scheduler. Old contracted
runs keep their old runner.

For task teams, relevant node knowledge, completeness monitoring and partial UAT,
read [references/team-flow.md](references/team-flow.md). These are support roles
inside this scheduler, not extra standing model loops. Partial UAT does not
replace final acceptance. Client/contact knowledge never authorizes contact.

## Historical knowledge scout (one per Graph)

Every new Graph carries exactly one plan-level historical scout
(`role: "scout"`, `mode: "advisory"`) declared by `historical_scout` in the
TODO. See [references/history-scout.md](references/history-scout.md). The
public `run` entry rejects an absent or duplicate scout before any native model
starts. Context consumers depend on that scout; there are no per-node scouts,
no repeated councils, no index/vault rescans and no extra approval/receipt
ceremony. A deterministic pre-check skips the scout model when discovery has
no independently reviewed/verified candidate; otherwise one maker selects and
deterministic grounding accepts it, without a model reviewer.
Resume reuses an accepted scout without redoing discovery. The pair
path stays lean; `legacy-test` is limited to explicit test adapters and cannot
bypass the new native Graph rule. Cross-project
historical context is bounded untrusted evidence attached separately from
strict same-project operational node briefs; it never grants access or
authorization. Parent reads the canonical Hub/gateway once and supplies config
and context receipt; the scout does not impersonate the parent.

## Run

For nontrivial executor selection, use the bounded JEV advisor described in
[references/jev-routing.md](references/jev-routing.md). It reads selected live
Fleet profiles/quotas, proposes diverse maker/reviewer choices and can draft a
new TODO. Skip it for obvious small tasks. It never dispatches work or changes
scope, checks, permissions or scheduler concurrency. A failed advice call falls
back to ordinary parent planning, never to an unbudgeted model API.

Bind executable advice to the minimized task, the actual TODO node and the
current candidate snapshot; do not apply an old report to a changed task. The
production wrapper also supports guarded escalation advice (see
[references/jev-escalation.md](references/jev-escalation.md)). Owner/business decisions and hard action gates
remain deterministic; JEV may suggest a technical architect, never permission.
Use one consultation per unchanged dilemma and reuse its report while fresh.
Office carries the result; a Wake handler must not call JEV again automatically.

Prepare one todo.json using references/todo-example.json. Parent must supply
a detached Git worktree containing all required input files before coding.
Disjoint tasks can share that isolated worktree; overlapping scopes/resources
are serialized. Scope is coordination, not an OS sandbox. Never point makers
at production or the user's active checkout.

For a classified top-level delivery/repair, the existing TODO plan also carries
`completion: {task_kind, task_family, episode_role, eligible, exception}`;
`uat_required` is optional and stays unknown when omitted. Reuse the parent's
existing `context_receipt`, `context_receipt_agent`, and native
`context_receipt_session`. The normal CLI terminal path emits bounded metadata
into the existing TODO telemetry outbox; a final COMPLETE Hub `record-session`
resolves it automatically. This adds no manual closeout step or planner call.
Missing/ambiguous bindings, audit/status/worker episodes, and blocked plans
skip safely. See `delivery-audit/references/integration.md` for coverage and
activation status; an accepted candidate alone is not delivery.

For one small independent delegated task use `scripts/todo_pair.py --todo
<todo.json> --run-dir <absolute-evidence-dir>` instead of graph scheduling.
It executes the same maker/checks/reviewer loop. Graph is for useful parallelism
or dependencies, not a mandatory ceremony for one pair.

```powershell
python "<skill-dir>/scripts/todo_graph.py" validate --todo <todo.json>
python "<skill-dir>/scripts/todo_graph.py" graph --todo <todo.json>
python "<skill-dir>/scripts/todo_graph.py" run --todo <todo.json> --run-dir <absolute-evidence-dir>
python "<skill-dir>/scripts/todo_graph.py" inspect --todo <todo.json> --run-dir <absolute-evidence-dir>
python "<skill-dir>/scripts/todo_graph.py" resolve-interrupted --todo <todo.json> --run-dir <absolute-evidence-dir> --inspection <inspection.json>
```

`--run-dir` must be an absolute path. A relative path is refused; it is not
resolved against the current working directory.

The Python scheduler launches ready tasks, waits without model polling and
starts dependents only after product acceptance. It does not call fidelity,
sufficiency, approve, init with planning-contract, acceptance-contract or
quality-contract. Do not create those artifacts for this path.

## Durable execution (durable_supervisor.py)

`scripts/durable_supervisor.py` is the durable front door for Arbor campaigns.
It is not a second scheduler and owns no second work-state registry: it
validates one `arbor-campaign/v1` document, translates its units into a single
`todo_graph` plan, and delegates execution, interruption inspection, recovery
and cancellation to `todo_graph` (`run`, `inspect_run`, `resolve_interrupted`,
`cancel_tasks`). The campaign directory holds `campaign.json`,
`durable-state.json` (owner fencing), the delegated Graph state, per-unit
`results/<unit_id>.json` (`arbor-unit-result/v1`) and append-only
`experience.jsonl` (`arbor-experience/v1`).

Campaign interface:

```powershell
python "<skill-dir>/scripts/durable_supervisor.py" validate-campaign --campaign <campaign.json>
python "<skill-dir>/scripts/durable_supervisor.py" run --campaign <campaign.json> --campaign-dir <absolute-evidence-dir>
python "<skill-dir>/scripts/durable_supervisor.py" resume --campaign <campaign.json> --campaign-dir <absolute-evidence-dir>
python "<skill-dir>/scripts/durable_supervisor.py" status --campaign <campaign.json> --campaign-dir <absolute-evidence-dir>
python "<skill-dir>/scripts/durable_supervisor.py" cancel --campaign <campaign.json> --campaign-dir <absolute-evidence-dir>
python "<skill-dir>/scripts/durable_supervisor.py" spawn-detached --campaign <campaign.json> --campaign-dir <absolute-evidence-dir>
```

An `arbor-campaign/v1` document declares `campaign_id`, `goal`, `workspace`,
`baseline_ref`, required nonempty `lockbox_ref`, `tree_budget` and `units[]`. Each unit
is one root task with `unit_id`, literal `scope`/`inputs`, `checks`,
`depends_on` and optional routing fields `maker`/`reviewer` (a single candidate, a list of candidates, or a model string) or the equivalent list forms `maker_candidates`/`reviewer_candidates` — there is no generic `candidates` field; the supervisor reads only those four names and falls back to a default fleet candidate when none is present. The supervisor keeps `lockbox_ref`
out of the maker-visible plan, state JSON and per-unit results; only the
deterministic isolation check (`ensure_lockbox_isolated`) may see it. scope (the write scope) and `inputs` (read inputs) are literal relative
paths (no globs). Only `scope` must fit `tree_budget.allowed_write_globs`;
`inputs` are not write-glob restricted. Both must stay relative without
traversal, and a unit may only use pools in `tree_budget.allowed_pools`.

`tree_budget` bounds the whole tree: `max_parallel`, `max_total_units`
(or `max_total_nodes`) and `max_depth`, which must be `1` for campaigns. A
child unit cannot raise these limits, widen its scope or pools, or dispatch
grandchildren; `todo_graph` rejects any child `tree_budget` expansion before
model execution. Cancelling a unit cancels its descendants through
`cancel_tasks`; campaign cancel claims supervisor ownership first, or files a
durable cancel request when a live owner must apply it itself.

Durability and recovery boundaries:

- Parent disconnect: `spawn-detached` starts the supervisor windowless
  (`HiddenLaunch.exe` when available, otherwise
  `CREATE_NO_WINDOW | DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP`) so the run
  survives the parent; state and results stay in the campaign directory.
  The detached child is fleet-native (`adapter=None`): it executes through
  the real Fleet bridge, so tests prove the windowless spawn/takeover and,
  separately, a detached worker running the same public `run_campaign`
  path to an independently verified result — never a synthetic adapter
  injected into `spawn-detached` itself.
- Worker restart: a saved maker receipt moves the node to `review_pending` and
  the reviewer resumes without re-invoking the maker or losing artifacts.
  A node interrupted before a trustworthy receipt is never replayed blindly;
  it is parked or blocked for inspection via `inspect_run` /
  `resolve_interrupted`.
- Supervisor restart: a new supervisor may take over an orphaned run only
  after the previous owner is proven dead, which increments the durable
  `generation`; a live or unverifiable owner refuses takeover.
- Pool loss: when one pool is cooling down, affected units surface as
  `RESUMABLE_POOL_WAIT` with `next_check_at` instead of failing. On resume
  after that time, the maker is skipped only when a trustworthy maker
  receipt/candidate was already preserved; the unit then re-enters
  review/acceptance without re-executing the maker. If the pool wait
  happened before any candidate was produced, resume re-runs the maker.
  While the queue is empty or a campaign is only waiting on pool cooldown,
  `model_calls == 0` — waiting never polls a model.
- Idempotency: durable events are recorded once per `event_id` in the shared `durable-events.json` registry (`todo_graph.record_durable_event`); re-delivering
  the same payload is a no-op and a different payload for the same `event_id`
  is rejected as a conflict. On the campaign path each unit carries a `dedupe_key` (explicit, or derived as `<campaign_id>:<unit_id>`); validation rejects blank keys and the same key on two units. `campaign_to_plan` copies the key into the plan task, and execution registers every unit key with a payload hash in that same registry before any maker runs, so a changed campaign re-delivered under the same key is blocked (`BLOCKED`, `model_calls == 0`) before any model call or file effect, while an identical re-delivery is a recorded duplicate. Per-unit results publish their `dedupe_key` and `durable_event_duplicate`.
  `experience.jsonl` entries are appended once per unit (append-only, never
  truncated), so repeated resume passes do not duplicate effects.

Model-call counters: `model_calls` in a `run`/`resume` response counts only the calls made by that current attempt, so `0` is correct for a rejected redelivery; `campaign_model_calls` in the same response is the campaign total, and `model_calls` returned by `status` (`campaign_status`, persisted in `durable-state.json`) is the durable cumulative campaign consumption. A conflict rejection makes no new calls and must not zero that history: absence of new calls is not zeroed campaign usage. The same rule applies to cancellation: `cancel_campaign` makes no model call, but it preserves the cumulative count (as both `model_calls` and `campaign_model_calls`, persisted in `durable-state.json`), and `campaign_status` reports the maximum of the stored count and the count evidenced by node history, so a stored zero can never override calls that already happened — for example when a campaign is cancelled after the maker ran and the reviewer was stopped by pool cooldown.

Acceptance for this layer is `tests/test_durable_execution.py`, which covers
normal execution with independent review, detached spawn, worker and
supervisor restart, idempotent events, `RESUMABLE_POOL_WAIT`, tree-budget
enforcement and cancellation, and zero model calls on an empty or
pool-waiting queue.

## Tier Routing (model classes)

`references/model-catalog.json` classifies every routed model as Director (D),
Manager (M), Kierownik (K), Worker (W) or DENY; `scripts/model_tiers.py`
applies it. A node may set `min_tier_execute` and `reviewer_min_tier`
(D/M/K/W; reviewer defaults to the maker floor; an unclassified model never
satisfies a declared floor). The bridge ranks qualified, allowed candidates by
the planner's fit score minus a penalty capped at the catalog
`similar_score_band` (10): decayed share of recent Fleet runs in the model's
tier (up to 15), Claude/Codex below Director (8) and, when a floor is declared,
5 per tier above it. A clearly better fit therefore still wins. DENY (exact
entries and `deny_model_patterns`, provider prefix ignored) is never picked, also
with the rollback switch. If no listed candidate is allowed, it substitutes from
the catalog, smallest sufficient tier first, under the same hard gates; BLOCKED
only when none qualifies. Quota percentages no longer rank candidates;
confirmed exhaustion still blocks. Picks are claimed for 1 h in
`~/.agents/model-tiers/picks.json` so parallel nodes spread. Every choice is
written to `tier-selection.json`. Recent use is divided by the plan size
(`policy.plan_weights`, owner-reported monthly price), so bigger subscriptions
carry proportionally more load. Architect escalation is Manager first, Director
only when no Manager qualifies; the model council ranks the same way. `python scripts/model_tiers.py shadow --todo
<todo.json>` previews choices; `usage` shows recent load. Rollback:
`AGENT_GRAPH_TIER_ROUTING=0` (legacy quota tie-break, DENY still filtered). JEV
applies the same band-capped reordering (up to 10 points) and excludes DENY;
reported fit scores are unchanged.
The catalog is curated from sources, not edited by a routing run.

Build ordinary TODO shortlists from the full `routing_enabled` pool, not a
Codex/Claude-only snapshot. Include qualified Google/Meta alternatives at their
actual fit score so the existing weighted ranking can use the larger paid plans.
A narrow supplied list remains narrow while any listed candidate qualifies;
the bridge only expands it on fallback. Tasks or plans may declare an optional
typed `candidate_policy` ("open" | "pin" | {"maker": "open"|"pin", "reviewer": "open"|"pin"}).
Absent policy preserves legacy semantics. Under `candidate_policy: "open"`, generic
candidate lists gain qualified same-class subscribed alternatives before ranking,
unlocking competition across paid plans without faking fit scores or prices.
Peers match the listed candidates' own tier, and scores are copied only within that tier.
Under `candidate_policy: "pin"`, exact-model diagnostics never substitute, including
on fallback (unavailability returns BLOCKED). Malformed policies fail fast.
Keep exact-model diagnostics pinned.
These are candidate-selection instructions, not a new planning or quota check.

Declared candidates must support the lane's `supported_modes` before native
Graph/Pair dispatch or bridge substitution; a malformed plan is an error.
Unknown/stale pools stay neutral: recency balances freshly available peers.
Fleet's existing per-pool cache consumes verified native completions younger
than 24 h and actual known-zero-token failures. Refusals across a shared pool
win over concurrent older runs regardless of profile order; expiry
only schedules a recheck. Local token ledgers are always advisory. Explicit
`fleet.py availability-recheck --agent muse|codebuddy` runs one content-free
native canary with one model step and zero tools; ambiguous failure retains
recheck-required without claiming exhaustion. Fleet views drive qualification,
substitution and advisor freshness; an optional snapshot cannot promote unknown.
These deterministic checks add no model calls, ordinary-session ritual,
registry or audit.

## Product Loop

Maker -> declared tests -> independent read-only reviewer. Reviewer checks the
actual artifact against done_when, including relevant security and regressions.
REPAIR returns only findings and failed tests. Every 3 rejected rounds, and on
stagnation (unchanged artifact and test outcomes, even with rephrased findings),
one read-only autopsy (Manager class, Director when no Manager qualifies) picks
CONTINUE (brief to the maker), SWAP_MAKER/SWAP_REVIEWER or OWNER_QUESTION
(WAITING_APPROVAL; `--retry-task` resumes); round count never blocks a node.
It grants no ACCEPT; its failure blocks. Rollback: `AGENT_GRAPH_AUTOPSY=0`.
There is no model-turn or token-estimate
cutoff in this scheduler. Native process timeouts and real provider limits remain.
Transport failures retain files and evidence; no automatic recoding.
Known handoff-unparsed maker work can continue as PARTIAL only after matching
local run/model/runtime/checkout/base/scope provenance and file hashes. Checks
and an independent reviewer still decide the product. Unknown provenance or
wrong identity remains blocked; the original Fleet ledger is unchanged.
Transport, artifact, acceptance and knowledge closeout are reported separately.
Format-only reviewer recovery reuses successful tests only while artifact and
check definitions remain identical; product changes require retest.
For interrupted RUNNING node inspection and hash-bound candidate resolution,
read [references/interrupted-recovery.md](references/interrupted-recovery.md).
For diff inventory, omission detection and review-anchor freshness use
`scripts/review_coverage.py` with
[references/review-coverage.md](references/review-coverage.md). It confirms
every changed file is reviewed or structurally excluded; it is not a substitute
for reading the code.

The bridge reuses the installed Fleet exact-model, quota, credential and native
adapter checks. Candidates come from actual available profiles, never invented
CLI flags or assumed model availability. Actual model_provider_id must differ
between maker and reviewer, including two models behind the same CLI.
Each worker prompt is capped at 48 KiB of UTF-8 before dispatch. Split an
oversized TODO slice or trim its evidence; do not silently truncate acceptance
criteria. The bridge passes the same cap to Fleet and surfaces its context
snowball warning and maximum measured step input in the node result. A warning
is telemetry, not automatic cancellation or proof of subscription cost.
Only adapters listed by the installed Fleet as tool-budget enforcing receive a
model-tool-call budget: maker 48/72/96 and reviewer 48/72/96 for
low/medium/high complexity (a reviewer reads as much as a maker, and Qwen
stops hard with exit 55 at its cap, so the old 20/30/40 lost verdicts). OpenClaw retains its smaller native per-mode cap;
MiMo retains its separate native step cap. Native ZCode/GLM-5.3 enforces a
cumulative scoped-read MCP budget; OpenCode is legacy with routing disabled.
Kimi and other unsupported transports receive no claimed cap. A TODO node may set
`max_model_tool_calls: {"maker": N, "reviewer": N}` (1..256) for a justified
exception; an override on a selected adapter that cannot enforce it is refused
before model execution. Fleet reports the effective cap and observed calls when
supported; unknown is not zero. Claude's bounded run uses stream-json, enabling per-step
context telemetry. A partial maker result still receives the declared checks and
product review; a blocked run retains its worktree. Inspect the evidence before
explicitly retrying with a larger budget or a narrower node.

## Safety and Completion

All tasks contain approval references for sensitive actions; only references to
existing explicit owner consent may be passed with --approved. A field is not
proof of consent. Parent must check intent and actual target; do not use this
runner for operations needing isolation it cannot provide.
Model prompts prohibit production, credentials and real-user side effects;
this version is for local candidate delivery, not automatic production rollout.

ACCEPTED_CANDIDATE means reviewed work in the isolated workspace. Integrate and
perform planned end-user/integration tests before announcing delivery. Existing
Fleet ledger may still say parent acceptance pending: do not overwrite history.
The TODO state and per-role receipts provide the new product evidence.
Keep evidence outside code. Changing approved artifacts invalidates their reuse.

Old agent_graph.py / graph_runner.py / execution-contract references are legacy
recovery tools. Do not initialize new contracted runs by habit.

## Lightweight Telemetry

The scheduler records metadata automatically under ~/.agents/telemetry/todo,
outside code. No extra model calls or quota polling. To inspect an existing run:
`python <skill-dir>/scripts/run_telemetry.py --run-dir <absolute-evidence-dir>`.
`--run-dir` must be absolute here too: the journal key is a hash of that path.
Worker seconds overlap; they are not project wall time. Missing usage is unknown.
Logger failure never changes product acceptance. Missing/truncated journals are
reported as incomplete. No prompt, file content, command arguments or exception
messages enter this journal. Files are bounded; existing evidence is not deleted.
`AGENT_TODO_TELEMETRY=off` disables only this optional measurement.
