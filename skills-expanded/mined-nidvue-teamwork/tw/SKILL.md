---
name: tw
description: "Nidvue Teamwork - run a user prompt to completion with an autonomous multi-agent company: CEO, CTO, COO, CFO, Architect, Product Manager, Project Manager, Designer, Release Engineer, Technical Writer, Data Engineer, Developer(s), Tester(s), Reviewer and Security Auditor. Use when the user invokes /tw, asks for a team of sub-agents with roles, wants an org chart of agents that plans, builds, tests and iterates until the goal is met, or wants long-running parallel work with per-agent memory. The user talks only to the CEO; every other agent communicates internally."
compatibility: "python3 3.11 or newer on PATH - the engine is stdlib-only, so there is no pip install and no venv; git is required for every branch, commit and PR operation."
---

# Nidvue Teamwork - `tw` skill

> **Nidvue Teamwork** is the product brand; `tw` is the skill the host loads and
> the command it maps, while `teamwork` stays the CLI, package and workspace
> identifier. This is a **skill**, not a standalone application: the engine is a
> stdlib-only tool the skill calls, and every agent runs through the
> host's own LLM API with a model configured per agent (`references/Concurrency.md`).

Turn one prompt into a functioning, self-organising team that keeps working until
the goal is verified. The user talks **only to the CEO**. The CEO decomposes the
goal, spawns the roles, and keeps developer/tester/designer lanes running in
parallel. Nothing is ever declared done on an unverified claim.

## Usage

```
use the tw skill: <prompt>       # any host: the skill is loaded by its description
/tw <prompt>                     # where the host maps skills to commands
/tw --team <Name>                # use a specific per-team tree
```

Anything else after the prompt is an instruction to the CEO in plain language
("resume the existing team", "only staff developer and reviewer", "four
developers"): the CEO honours it when writing the roster and `Plan.md`. Only
`--project` and `--team` are CLI flags.

The prompt is the product brief. The CEO **researches it in one or more rounds
and enhances it before decomposing**, and when it is genuinely ambiguous in a way
that changes what gets built the CEO **asks with options instead of guessing**:
`ask add --question '<it>' --option '<a>' --option '<b>' --recommend 1` records
the choice, and a `blocks` question holds `loop` at CONTINUE until the user
answers (`ask answer Q-0001 --choice 2 --by user`). Questions are consolidated
into one round, never drip-fed per lane.

The skill is **agent-agnostic and remote-agnostic**: it runs on any agent host
that loads a skill directory, or that can run `teamwork.py` and read `AGENTS.md`,
and against GitHub, GitLab, Bitbucket, Gitea/Forgejo, Azure DevOps or a bare
server. The protocol is identical; only the six host operations and the integrity
settings are adapted (`references/Adapters.md`, `references/Remotes.md`).

## Non-negotiable contract

1. **One voice to the user.** Only the CEO reports, asks and accepts.
2. **Run to completion.** Work ends only when every criterion is verified by executed evidence. Blocked is not done, and idle with executable work left is a bug.
3. **Evidence or `UNVERIFIED`.** No claim without a path/command/revision/result; the engine refuses `done` without one.
4. **Independent parallel lanes.** Freeze interfaces first, then developer, tester and designer run concurrently on the same contract.
5. **Code, then tests, then docs.** Documentation never blocks code or tests.
6. **Role-shared state, private workspace.** Memory and queue belong to the ROLE; charter, worklog, inbox, artifacts, reports and scratch are private.
7. **Red lines are absolute.** Unsafe, irreversible or fabricated work stops the lane and escalates (`references/Evidence.md`).
8. **Nothing unnecessary is kept.** No duplicate docs, scratch, build output or secrets.
9. **Style is automated.** The canonical formatter, linter and type checker (Python: `ruff format` + `ruff check` + `mypy`) run before the commit and gate the merge; never hand-format, never weaken a rule to pass.
10. **Names are deliberate.** Team directories are PascalCase, files follow the ecosystem, Python modules `lower_snake_case`, tool-mandated files never renamed.
11. **History is minimal and modular.** `<type>(<area>): <summary>` plus `Role`, `Producers`, `Goal`, `Deliverable`, `Why`, `Status`, `Result`; squash to one commit per task before review; never rebase or force-push shared history.
12. **Each agent's model is its own.** The skill ships no model and calls no LLM API; the user's configured model is the default and automatic routing is off by default. Switching needs an explicit demand: `model auto --apply --allow-switch --reason '<who asked>'` (`references/Concurrency.md`).
13. **Warnings are errors.** The toolchain fails on them; fix the cause, suppress narrowly with a reason. CI annotations count too.
14. **Independence is structural.** Verification lanes run the user's default model; a different model per lane is an explicit demand, not a background switch. One task owns one branch; duplicate work is a defect.
15. **No lane wars.** Never deny a peer a process, worktree, lease or file; resolve by a measurable contest or the CEO.
16. **Consensus is not evidence.** A single source is provisional and lowering a gate to agree is collusion.

## The org

Sixteen charters, one per role, at `roles/<role>.md`; instance names are `<role>` or
`<role>-<n>`, the CEO is the leader session and is never spawned. Three roles own
more than their charter's headline: the **Designer** owns every visual asset, raster
and vector (recorded in `Design.md`), the **Release Engineer** owns repository and CI
integrity (branch protection, required checks, merge strategy, protected tags, on any
git host), and the **Reviewer** (`reviewer-1..N`, several may run **in parallel**)
owns the pass/merge right - deep independent review of every deliverable from one
shared queue, one claim per deliverable, never the author. **Review is a parallel
lane** and a pass is the merge.
Who owns what and who reports to whom: `AGENTS.md` (`## Team and reporting lines`);
handoffs and decision rights: `references/Roles.md`.

### Who reports to whom

```text
CEO - user interface, arbitration, final acceptance
|- CTO - technology strategy, engineering standards, the build/release policy
|  |- Architect, Developer-1..N, Tester-1..N, Release Engineer, Data Engineer
|- COO - process, risk, throughput
|  |- Project Manager
|- Product Manager - research, requirements, acceptance criteria
|  |- Designer, Technical Writer
|- CFO - cost, budget, unit economics
|- Reviewer-1..N - independent review, the only pass/merge right
`- Security Auditor - audits everyone, CTO included
```

One parent per role, and the parent owns the standard the child is judged by.
**Escalate up your own line first** (`Architect` -> `CTO` -> `CEO`); go sideways
only for a fact or artifact a peer holds. Three roles stay directly under the CEO
because their job is to disagree with everyone else: the Reviewer merges the work
it reviews, so no reviewed lane can manage it; the Security Auditor audits the
CTO; the CFO holds the cap that binds the team. `ROLE_PARENT` in
`src/teamwork/config.py` is the single source of truth - `teamwork.py map` renders
the tree and `tests/unit/test_reporting_hierarchy.py` fails when a doc drifts.

### Staff the smallest roster that still closes the gates

Start from a tier instead of listing fifteen roles. `init --roster slim` is the
default; `--agents` overrides it for a roster you name exactly.

| Tier | Instances | Startup read |
|---|---|---|
| `slim` (default) | 6 | 252 kB |
| `standard` | 10 | 403 kB |
| `full` | 17 | 653 kB |

Startup read = every instance's `AGENTS.md` plus its own role charter, summed -
2.2x what `slim` costs. A role earns a seat only if it owns a deliverable, a test
layer and a decision right no other role holds; everything else is a **lane, not a
role** (no charter, no queue, no memory set). Which role a slim tier drops and where
that work goes: `references/Roles.md`.

Two rules keep a slim roster honest:

- `tests plan` only requires the layers of **staffed** roles.
- The tribunal never falls below two members: with no CTO/CFO staffed the Reviewer
  takes the neutral seat (`TRIBUNAL_MIN_SIGNERS`), and **a party to a dispute can
  never rule it**. A vacant manager escalates to the CEO for the duration.

`init` warns when a gate-critical role is missing. **The Reviewer is not optional**,
and two Reviewer lanes are the minimum: the queue fans one deliverable per lane, a
re-submitted fix is re-reviewed as a delta, and a second lane gives a sampled or
high-risk deliverable an independent verdict. A pass merges - the lane that verified
the revision lands it.

## Workspace layout

Two separate worlds: the team's own tree is **hidden** and local; project output is committed. All team-created names are **PascalCase**.

```text
<project>/
├── AGENTS.md                         # team constitution (managed block, auto-loaded)
├── .agents/skills/tw-<name>/SKILL.md # team skills
├── docs/Team/                        # Project, Plan, Board, Archive, Decisions,
│                                     # Architecture, Research, Design, Risks,
│                                     # Costs, Release, AuditManifest.json/.md
├── <code/> <tests/>                  # committed project output
└── .pi/Teamwork/Teams/<Team>/        # hidden, gitignored team tree
    ├── TeamMap.md  Settings.json  Criteria.md  Tests.md  TestPlan.md
    ├── Reviews.md  Disputes.md  Skills.md  Knowledge.md  Ledger.jsonl
    ├── Global/                       # CEO-owned GlobalMemory.md (+ Archive)
    ├── Roles/<Role>/                 # SHARED: Short/Long/Archived memory,
    │                                 # Role.md, Lessons.md, TaskQueue.md
    ├── Agents/<Instance>/            # private: StartHere, WorkLog, Inbox,
    │                                 # Artifacts/, Reports/, Scratch/
    └── Runtime/                      # LedgerHead, GraphBaseline, Locks/, Worktrees/, Slots/
```

Every team gets its own `<Team>` tree, named after the project or by `--team`/`TEAMWORK_TEAM`, so several teams in one repository never collide. Memory and the queue belong to the ROLE: `Developer-1` and `Developer-2` share `Roles/Developer/` and claim from one queue.

Any role scales with `instance add <role> --count N`. Only one instance of a role revises its memory at a time: `memory claim <role> --by <instance>` takes the pen, `memory release` returns it, and a single `remember` holds it only for its own duration. A long lease is contested, not waited out: a peer runs `memory contest <role> --by <instance> --reason '<why>'` and the **CTO** rules with `memory extend` or `memory revoke`. Detail: `references/State.md`.
## Bootstrap procedure (CEO)

Run these in order. Use `SKILL` for this skill's directory.

### 1-4. Intake, workspace, plan and staffing

These run once per project, so their detail is on demand: read
[references/Bootstrap.md](references/Bootstrap.md) before you create a
workspace, freeze interfaces or restaff. The order is fixed:

1. **Intake** - record the prompt verbatim, deep-research its intention in one
   or more rounds, **enhance the prompt** from what the research found, and ask
   the user rather than guess at any ambiguity that changes what gets built
   (`prompt record`, `ask add`). Then rewrite it into a systematic,
   parallel-ready brief with the `tw-brief-intake` skill: objective,
   deliverables, acceptance criteria, interfaces to freeze and the proposed
   lanes. Every criterion becomes a record, and the first one is refused until
   an enhanced prompt is recorded.
2. **Workspace, repository, constitution** - the tree, the managed block, the
   team settings.
3. **Plan and freeze interfaces** - the parallelism gate; no squad starts on a
   moving interface.
4. **Staff and dispatch** - the smallest roster that closes every gate.

Then run the loop (section 5) and close (section 6).

### 5. Run the loop

One iteration is: re-plan -> dispatch -> work in parallel -> independent review ->
rework -> integrate. Repeat until `teamwork.py loop` reports STOP.

- Teammates auto-claim the highest-priority unblocked task; when one finishes it
  submits for review and takes the next.
- **Every deliverable is second-reviewed by the Reviewer**, independently: code,
  tests, docs, design, research, cost models, risk registers. A fail returns it to
  the owner with findings; the owner fixes, re-checks and re-submits. Failures are
  counted: at 3 the Reviewer must open a dispute so the tribunal rules
  (`references/Dissent.md`), and `loop` blocks STOP until it does.
- **Every agent tests its own layer** (`goal` CEO, `requirements` Product Manager,
  `plan` Project Manager, `tech` CTO, `release` Release Engineer, `data` Data
  Engineer, `process` COO, `cost` CFO, `system` Architect, `ui` Designer, `docs`
  Technical Writer, `unit` Developer, `integration` Tester, `acceptance` Reviewer,
  `security` Security Auditor). `tests plan` shows the matrix and gaps; `loop`
  blocks STOP while a required layer is missing or failing.
- **Review is a parallel lane.** `reviewer-1..N` claim different deliverables from
  the shared queue; one claim per deliverable, high-risk work gets two Reviewers,
  nobody reviews their own work, findings union, and a pass is the merge.
- The CEO keeps the interface contract stable and arbitrates; the Project Manager
  chases stalled tasks and refreshes `Plan.md`/`Board.md`; the COO keeps `Risks.md`
  honest; the Product Manager keeps `Research.md` current.
- The team is self-managing: the CEO resolves internal conflicts and disputes
  without the user, who hears only an authorization, a goal/scope/budget change, a
  blocking ambiguity, or the final report.

Before every close:

```sh
python3 "$SKILL/scripts/teamwork.py" criteria list && python3 "$SKILL/scripts/teamwork.py" tests plan
python3 "$SKILL/scripts/teamwork.py" board && python3 "$SKILL/scripts/teamwork.py" review --queue
python3 "$SKILL/scripts/teamwork.py" coordination --strict && python3 "$SKILL/scripts/teamwork.py" audit
python3 "$SKILL/scripts/teamwork.py" links && python3 "$SKILL/scripts/teamwork.py" pulse --commit
python3 "$SKILL/scripts/teamwork.py" graph audit && python3 "$SKILL/scripts/teamwork.py" parallel
python3 "$SKILL/scripts/teamwork.py" loop
```

Report to the user at milestones: what changed, evidence, blockers, next.

### 5a. Parallelism is the default, not the reward

A team that runs one lane at a time is a slow single agent with extra records.

| Rule | Mechanism | Why |
|---|---|---|
| A lane holds more than one unit | `LANE_WIP` (2): one deliverable in review plus the next in progress | a lane waiting for its own review is idle capacity |
| `pulse` fills capacity, not idle lanes | it assigns `LANE_WIP - held` per lane | one-task-per-idle-lane capped the team |
| A dependency can release early | `deps: role:T-id@review` or `@started` | the downstream lane needs a frozen interface |
| Reviews are the exception | one claim per Reviewer lane; run several lanes | a deep review is not divisible |

Capacity is bounded by the provider caps in `Settings.json`, never by the lane
count: Ollama Cloud 64, DeepSeek 2500, OpenAI 64, Anthropic 64. `pulse` defers
assignments beyond the free-slot count and prints the shortfall.

**Delegation is recursive, and the CEO does not do a lane's work.** The CEO's output
is the decomposition, the dispatch, the arbitration and the final claim; every unit
goes to a lane. A Team Leader spawns its squad, and a lane whose slice will not fit
its budget splits it into sub-tasks and dispatches them. The chain ends at a small
task one lane can finish and get verdict-ed inside its budget, and at an independent
verifier: no lane reviews, tests or merges its own work.

### 5b. Keep the lanes full: swarm is the default mode

After dispatching, the CEO **re-wakes on an interval**, finds idle lanes and hands
them runnable work. Swarm is the default: `pulse --commit` sizes and runs the
engine's swarm on that wake.

```sh
python3 "$SKILL/scripts/teamwork.py" pulse --commit --interval 5   # dispatch + one swarm run
python3 "$SKILL/scripts/teamwork.py" pulse --commit --no-spawn     # the plan only, no lane
python3 "$SKILL/scripts/teamwork.py" swarm run --dry-run           # the measured policy
python3 "$SKILL/scripts/teamwork.py" lane status --live
```

Exit 3 means "nothing to dispatch". A review claim is a renewable profile lease
(`ReviewLeaseMinutes`, default 20; x1 fast, x2 standard, x4 deep), separate from the
90-minute slot TTL: verdict with `--result`, extend with `--renew`, or `--release`.

- **The wave is sized by the work.** `swarm run` weighs what is in hand (1 prose,
  2 code, 3 security/release/data, +1 bug) and starts `ceil(weight / 3)` lanes,
  bounded by free slots and `LaneMax`; budgets follow the unit (10 calls/10 min
  prose, 16/25 code, 24/40 deep). An unfinished assignment gets a bounded retry, a
  claim with no live lane is adopted, and a `review` deliverable becomes a Reviewer
  lane. `lane status|logs|stop|reap` is the inspection surface.
- **Async by default.** `swarm run` dispatches one wave and returns - never waits.
  `--wait` (implied by `--waves N`) is the CI drain, not the live loop.
- **The roster follows the work.** `pulse --commit` adds an instance per `LANE_WIP`
  units of ready work and one Reviewer per unclaimed deliverable, spreads the units
  round-robin, and folds seats it cannot feed (`instance prune`). `--no-scale` opts
  out; an `observe`/`off` wake changes nothing.
- **Busy means leased, claimed or doing.** Everything else is idle and must be fed.
  The CEO is never folded.

Interval: `PulseMinutes` (default 5). Runtime, launchers and degraded modes:
`references/Concurrency.md`, `references/Adapters.md`.

### 5c. Push in stages, and certify both signals

- **Release Engineer - push after review, stage by stage.** Only the Release
  Engineer pushes, and only a revision the Reviewer passed with no open finding.
  **A stage ends with a push, not with a merge**: push each reviewed stage so the
  remote never drifts. Before the push, build, tests, `privacy_scan.py --tree
  --history` and the link check are green on exactly that revision; after it, watch
  CI and confirm green **on that SHA**. A red run is routed from the log (code ->
  Developer, test -> Tester, contract -> Architect, workflow/packaging/flake ->
  Release Engineer, scope -> CEO) and re-run. A code-scanning `error`/`critical`/
  `high` alert is red; `teamwork code-scanning --commit` files a `P0` task with the
  file's owner. Force-push and published-history rewrites need the CEO's
  authorization; tags and releases are the CEO's step.
- **Tester - certify local *and* CI.** Run the layers locally, then confirm the same
  result in CI on the pushed revision, job by job across the OS and Python matrix. A
  green local run with a red CI run is a failure, and so is the reverse; file every
  failure to its owner with the command, expected vs actual, log, SHA and run id.
- **CI triggers are path-filtered: code in, prose and media out.** Docs and images
  get a cheap docs workflow (link health, privacy scan, `mkdocs build --strict`);
  anything that ships always runs the full matrix. Keep the two lists in sync.
- **Everyone keeps the tree clean.** No explanatory comment
  (`scripts/check_comments.py` fails the gate), no commented-out code, no `TODO`
  without a tracked task; delete temp and stale files in the same task (`clean` for
  your lane, `--all` for its `Scratch/`); one canonical home per file.

Both duties are evidence: `tests plan` and the task record name the local result
**and** the CI run (id + conclusion) for the certified revision. Detail:
`references/Engineering.md`.

### 5d. Any agent host, any git host

- **Agent host.** The engine, workspace, criteria, two-stage gate, ledger and test
  matrix are host-independent. Only six
  operations need a mechanism - spawn a teammate, delegate one-shot work, message
  an agent, inspect state, re-wake on a schedule, close the team - and the engine
  provides all six itself: `lane start|list|status|logs|wait|stop|reap`, the
  `Inbox.md` mailbox, and `swarm run`. A
  host is only the CLI that turns a packet into an agent run; the launcher table,
  the `LaneCommand` template and the degraded modes are in `references/Adapters.md`.
  Name the operation, never a host tool. With no launcher the protocol still
  completes - one agent wearing the hats sequentially, with the same gates.
- **Git host.** The Release Engineer guarantees repository and CI integrity on any
  host: a protected default branch, **no force-push**, no deletion, required status
  checks on the exact revision, at least one non-author approval, the host merge
  button off - the Reviewer merges locally and the source branch is deleted
  (`pr merge --squash` is the one-commit path) - protected `v*` tags created only by
  the CEO, and least-privilege CI with no secret in the tree. Record the host's
  actual settings and re-read them to detect drift. Per-host mapping:
  `references/Remotes.md`.

### 5e. Keep the installed skill on the remote's `main`

The host loads a **copy** of the skill, so a copy that drifts from `origin/main` silently keeps reading an old protocol. `teamwork.py refresh` fast-forwards a checkout source and mirrors the bundle into the skills directory; `--check` reports drift and exits 1 when stale, `--dry-run` prints the plan. A dirty checkout is mirrored, never reset. Run it at startup and after every push, and reload the skill afterwards. The same command also installs the **lane display** - the extension that draws the live wave - because a skills directory is never read as an extension directory, so shipping the file is not loading it. `init` does it too, by default: bootstrapping in a host that has an agent directory draws the wave without another command, and `init --no-ui` or `TEAMWORK_UI=off` opts out. `ui status` reports both halves without writing, `--no-ui` keeps a mirror-only run, and `--check` fails when the host would draw nothing. Full behaviour: `references/Adapters.md`.
### 5f. Keep lanes decorrelated

Identical lanes make identical mistakes: same model, same context, same queue.

- Different models across Reviewer, Tester or Security Auditor lanes are an explicit
  demand, never a background change: the user asks, then the CEO runs
  `model auto --apply --allow-switch --reason '<who asked>'` with
  `TEAMWORK_MODEL_ALT`. `coordination` reports `C-DIV-MODEL` when every verification
  lane shares one model; the remedy is to ask the user, not to switch on your own.
- `coordination --strict` is the milestone gate: duplicate branch/task, echoed
  evidence, reviewer monoculture, abandoned PRs, merge collapse, slot starvation.
  `--commit` records it; exit 1 means a high finding is open.
- A conflict is resolved by a measurable contest or the CEO, never by denying a peer
  a resource. `reclaim` refuses a live lane; `--force <reason>` is only for a
  confirmed dead one.
- The Reviewer reads the artifact before the author's summary and records its own
  run; identical evidence is `C-TRUST-ECHO`.
- A user-facing deliverable is **shown** at the milestone.

Mechanisms: `references/Coordination.md`.

### 5g. Keep reviews fast

The Reviewer is the gate every lane waits on; its queue, not its depth, is the
throughput limit.

- `review --queue` sorts by priority then age and prints the profile, claim state and
  capacity. Add a Reviewer lane when the unclaimed queue is deeper than twice the
  lanes; a deep review is not divisible.
- `review <role> <T-id> --packet` gives the profile, changed files, self-check, gates
  and checklist in one screen; start there.
- The profile is inferred from the diff: `fast` for prose (link check, docs/contract
  tests, privacy scan), `standard` for code (suite, lint, type-check), `deep` for
  security/release/data/workflow. `task add --review-profile` overrides it.
- A claim is a **profile-aware renewable lease** (`ReviewLeaseMinutes`, default 20;
  x1/x2/x4), not the slot TTL. `review --next --by <lane>` claims and packets in one
  step; `--renew` extends; do not hold a claim while writing prose. `coordination`
  reports claim-to-verdict p50/p90 and expired claims.

### 5h. Verify once, credit the rest

Most of a slow review repeats work another role already did at the same revision.
Independence is about the **author**, not about repeating a peer: a recorded result
from another role at the revision under review is a fact to cite, and
`review --packet` lists it.

| Rule | What it means |
|---|---|
| one run per fact per revision | a recorded `tests run --rev` or CI run on the pushed SHA is not re-run; cite it with `--credit` |
| the irreducible core | requirement conformance, the reviewer's own `acceptance` layer, every `uncovered` criterion, one sampled credit |
| creditable | a `passing` record at this revision, by a role other than the author's, with the command written down |
| recorded, not implied | `--credit TS-0006` writes `credited: ...`; a stale, failing, author-role or unknown record is refused with the reason |
| read the machine verdict | lint, format, type-check, suite, links, privacy, security scan are read once; re-running a green record is `C-REVIEW-DUP` |
| a fix is a delta review | a fail stores the revision; re-review the delta, the failed criterion and one fresh credit |
| full re-review only on a contract change | a new deliverable, a frozen interface, a security/release/data/workflow path, or a larger diff |
| budget | fast 10 / standard 20 / deep 40 minutes; when spent and unverifiable, fail naming the missing evidence |
| batch the context | same author + area + profile may be one sitting - one claim and one verdict each |

`coordination` reports the credit ratio, delta re-reviews, `C-REVIEW-DUP` and
`C-REVIEW-NOCREDIT`. Every author records `--rev <sha>` and `--artifact`: an
unrecorded run is a run the Reviewer has to repeat.

### 5i. The throughput contract

Speed is a property of the structure, not of working harder. Measured on this
project's trail at one ledger cut, `n=1615`: **44** review failures over **66**
review targets (one role + task), 26 needing more than one verdict, 11 three or
more. Two readings put locally-catchable failures at **16-24 of 44**, but the split
is **contested**, so the contract does not rest on it: every fail records whether the
author had a green `preflight` at that revision (`mechanical: no|unknown|n/a`),
measuring it prospectively. `teamwork.py throughput` re-reads the current cut.

The ten rules and what each forbids are the `## Throughput contract (hard)` table in
`AGENTS.md`; `preflight <role> <T-id>` turns six of them into one fail-closed command
(identity, commit count, every `@<sha>` reachable, evidence and note name the branch
head, `merge-tree` clean, board drift, then the project gate).

**Feature teams are live** (`references/Roles.md`): one open feature per leader and
its squad, teams in parallel, Architect and Project Manager shared services. `feature
check` applies five rules - shared writable path, in-flight dependency, one open
feature per leader, owned-path shape, duplicate id - and a feature cannot leave
`proposed` without a frozen interface (`feature set <F-nnnn> --state ready` refuses
one). `preflight`, a review pass and the merge all run it.

### 5j. Learning is part of the work

A failure you do not record is one the team pays for twice.

- **A lesson (`L-`)** after a failed self-check, review or any mistake worth not
  repeating, closed with the cheapest rung that stops it recurring: `lesson fix
  --check '<cmd>'` (run on the spot, must exit 0) or `--no-check '<why>'`. Prose
  alone is refused.
- **A `tw-` mistake skill** when the fix is a flow: `skill create --kind mistake
  --from-lesson L-nnnn`.
- **A knowledge record (`K-`)** for a durable fact, command or gotcha. Search before
  asking, supersede rather than contradict, never store a secret.
- **The skill library is managed, not just grown.** Every agent creates, updates,
  enhances and **removes** skills; every skill is feature-unique, so search for
  overlap and consolidate rather than duplicate.

Classify a finding first - tool defect, process, doc drift, governance or knowledge -
and run `tw-self-evolve` at every milestone close. A tool defect takes a code task
with a failing reproduction, never a lesson. Commands and rungs: `AGENTS.md`
(`## Learning from your own work`); detail: `references/State.md`.

### 5k. The context tree

`ctx://` is one read-only view over memory, lessons, knowledge, skills, docs and
tasks; every node resolves to an existing file or record and no sidecar is written.
L0 is the one-line summary, L1 the record fields or child list, L2 the full record.
Use `context ls`, `tree`, `read <uri>`, `find "<query>" [--scope <uri>]`, `stats`,
`digest <T-id>`. Retrieve by id, never by whole file. For one file the same
discipline is `tw read <path> --query '<needle>'`: under 4 KiB it returns the
whole file, above it only the matching line ranges with `path:line` provenance
inside a byte budget, and `--lines`/`--full` are the verify and native fallbacks.
`context` never replaces `load`, the gates or the evidence rule. Detail:
`references/State.md`.

### 5l. Throughput and the token budget

- **Right-size the roster.** `slim` is default; add an instance for a named
  deliverable, retire an idle one (move-only to `Runtime/Retired/<Instance>/`).
- **Read by id, never by history.** `archive --task <T-id>`, `decision list`,
  `board`, `trace <id>` answer a question; a whole `Archive.md` is ~0.63M tokens
  against a ~0.11-0.15M startup, and `Decisions.md`, `Plan.md` and a `TaskQueue.md`
  are the same trap.
- **Make the first pass review-ready**, then let the Reviewer cite the Tester's run
  (`--credit`) instead of repeating it (5h).
- **Keep the budget token-true.** `harness budget` measures what `load` prints,
  `--recallable` what it never prints; the cap is `AlwaysOnBudgetKb` (122880 B) -
  trim the surface, never raise the cap.
- **Split at the slice warning.** `preflight` warns past 6 files/300 lines (`fast`),
  12/600 (`standard`), 24/1200 (`deep`).

The rules and the per-surface budget: `AGENTS.md` (`## Context and token economy`).

### 5m. The intern protocol

The model is an intern: introduce the work, give it one job, prove the job, and
remove every manual relay. Full text: `references/Roles.md`; the audit is the
`tw-team-designer` team skill.

| Rule | It forbids |
|---|---|
| no human relay | the user copying a fact between agents or re-stating repository state; record it (`attention add`) and automate it |
| teach once, encode it | a repeatable method living only in the conversation; `skill create`/`skill share` in the same task |
| least privilege, one job, one proof | granting every connector; every deliverable names its verifier and proof |
| onboard, then restate | planning before the agent restated goal, acceptance and non-goals |
| proactivity is a record | silent autonomy; an idle lane proposes one automation/risk via `attention add` or a task |
| routine hygiene | a schedule with no trigger, budget and stop condition |

Do not give a bot its own email or external accounts: that is external and
irreversible. Adopt the smallest team that reliably does the work, with a proof per
seat.

### 5n. Agents talk to each other: the mailbox

An agent that needs another agent to do, check or answer something sends a
**message**: not a task, not a worklog entry. Queued, prioritised, preemptible, so a
request never costs the recipient its current work.

```sh
python3 "$SKILL/scripts/teamwork.py" message send --from <you> --to <instance> \
    --priority urgent|high|normal|low --subject '<one line>' [--body '<detail>'] \
    [--task <T-id>] [--reply-to <M-id>]
python3 "$SKILL/scripts/teamwork.py" message inbox --for <instance> [--all] [--json]
python3 "$SKILL/scripts/teamwork.py" message take <M-id> --for <instance> --by <you>
python3 "$SKILL/scripts/teamwork.py" message done <M-id> --for <instance> --by <you> --result '<what you did + evidence>'
```

| Priority | What the recipient does |
|---|---|
| `urgent` | the supervisor stops the lane, marks the task `paused`, runs a mailbox lane; `lane resume <T-id>` puts it back |
| `high` | read before the next new task |
| `normal` / `low` | read in order, at the next step or when idle |

- **The queue is in the packet**: every lane packet opens with `## Messages for
  you`, so no polling is needed.
- **One taker**: `message take` makes exactly one lane process it; `message done`
  closes it with the result the sender reads.
- **The task is paused, not lost**: a paused task blocks `loop` until it resumes.
- **The trail is the ledger**: `message.send|take|done` and `lane.preempt`.

Use it for a review finding the author must act on now, a fact another role holds, an
interface change that invalidates a peer's work, a hand-off. Not to assign work
(`task add`), not to report progress (the worklog), never to ask the user. Detail:
`references/State.md`.

### 5o. Loops inside a node, the graph between them

A loop makes one unit correct without you; the graph decides which units exist, in
what order, and where you sign off. Skip one and it returns as manual work: no loop,
you read every output; no graph, you approve every step. Detail: `references/Loops.md`.

| Question | Command |
|---|---|
| what runs in parallel, what gates the finish, what an arrow costs | `graph` |
| does cutting this dependency shorten the run | `graph --cut '<dep> <- <task>'` |
| is the graph even runnable (cycle, dangling dep, duplicate id) | `graph --check` |
| is an open-ended hunt done, and has it already thrown this away | `hunt '<topic>' --run '<cmd>'` |

- **Test every arrow by naming the payload.** `graph` lists edges whose ends share
  no feature, area or tag as *unproved*: name what travels along it or cut it.
- **A cycle needs five things**: a dry test, a round limit, a budget, memory of past
  attempts and a person paged on a stall. `hunt` owns all five and exits 1 when the
  loop is stalled rather than converged.
- **Send back the unit, not the batch.** `review --result fail --scope '<what the
  fix may touch>'`; the retried lane packet opens with the finding and the scope.
- **No model where code will do.** Classifying evidence, sorting, dedupe and the
  undo class are code (`grades.py`); a model there is slower and occasionally wrong.

### 6. Close

When the queue is empty and `loop` is about to report STOP, load `tw-ceo-audit-close` and follow it exactly: freeze the revision, verify the chain before the gates, check the archive against the tree, export the manifest last, and report from records. An unnamed skill is dead text nobody loads, and `harness lint` fails a tree that has one.

Completion gate - all of:

- [ ] Every acceptance criterion in `docs/Team/Project.md` has evidence from a revision.
- [ ] Every deliverable passed a self-check and an independent Reviewer verdict with reproducible evidence, and appears in `docs/Team/Archive.md`.
- [ ] Every required test layer passes, run by its owning role (`tests plan` reports no gaps).
- [ ] No open high-severity security finding; no unresolved red-line escalation.
- [ ] Every task branch is reviewed, merged into `main` and deleted.
- [ ] Every staffed role designed, implemented and ran its own test layer.
- [ ] `ledger verify` is intact, `audit` reports no provenance gap, and the `ledger export` manifest is committed.
- [ ] `loop` reports STOP and `audit` reports zero problems.
- [ ] Docs match merged code; no scratch or temp files; nothing unnecessary committed.
- [ ] Final report: deliverable, how to run it, evidence table, limitations, follow-ups.

Then end every live lane with `lane stop <run>` and run `lane reap`: it reconciles a lane that died without an outcome, frees its slot and recycles the seat of a finished lane under the roster policy - never the CEO, one instance of each gate role kept (move-only to `Runtime/Retired/`; `--keep` leaves the instances staffed). Confirm `loop` still reports STOP on the final head, and deliver the report.
## Reference files (read on demand)

`SKILL.md` is the operating procedure; policy detail lives in `references/`. Read
the one you need instead of the whole skill.

| File | Read it for |
|---|---|
| `references/Bootstrap.md` | intake, workspace, plan, staffing, close |
| `references/Evidence.md` | evidence shape, claim discipline, red lines, escalation |
| `references/Dissent.md` | independent decisions, the 3-round cap, the tribunal |
| `references/State.md` | memory, lessons, knowledge, context tree, queue, mailbox |
| `references/Concurrency.md` | caps, slot leases, lanes, scale, model routing |
| `references/Coordination.md` | multi-agent failure modes and their mechanisms |
| `references/Docs.md` | markdown structure, concision, bidirectional links |
| `references/Engineering.md` | identity, commit style, LFS, branches/PRs/merges, worktrees |
| `references/Roles.md` | the roster, handoffs, decision rights, the intern protocol |
| `references/Testing.md` | the role-owned test layers, dedupe, required coverage |
| `references/Audit.md` | provenance, the ledger, internal and external audit |
| `references/Adapters.md` | host operations, installation, refresh, degraded modes |
| `references/Remotes.md` | git-host integrity: protection, checks, merge, tags |
| `references/Loops.md` | loops, the task graph, failure routing, who signs off |

## Companion skill: `tw-learn`

One flow is a whole skill of its own, installed beside this one as the
`tw-learn` skill (`/tw-learn`): study an outside article, repository,
file or block of code systematically, compare it against this system, and adopt the
**mechanism** rather than the expression. Load it when a prompt says "learn from
this repo", "study how X does it", "compare us against Y" or "what should we adopt
from Z".

It exists because the default failure is the wrong one: a team handed an external
system copies the visible half and calls it learning. The skill pins the target to a
revision, records the licence before the code, forces the comparison onto one axis
at a time, requires a decision with a falsifier, and forbids the paste. A study with
no verdict, no contrast and no revision is a summary, not a deliverable.

`skills/tw-learn/SKILL.md` in this checkout is the source; `make sync-skill`
mirrors it to `<skills>/tw-learn` and `sync-check` fails on drift, the same
way the main bundle is kept true.

## The bus and the claim register

`message send --to <Instance>` writes the team mailbox. The four bus addresses cross a
checkout, and are matched when a reader reads, so an announcement is one file for N
readers:

| `--to` | scope | closable by |
|---|---|---|
| `*` | every session on the bus | the sender, or `--ttl` expiry |
| `role:<role>` | every instance of that role | the sender, or `--ttl` expiry |
| `team:<Name>` | every session of that team | the sender, or `--ttl` expiry |
| `session:<PI_SESSION_ID>` | one session, take-able | the recipient |

```sh
teamwork.py message send --from <you> --to role:developer --subject '<one line>' --ttl 60
teamwork.py claim add --by <you> --path src/teamwork/engine.py --ttl 120
teamwork.py claim check src/teamwork/engine.py | claim list | claim release <C-id>
```

A live, unexpired claim on the same path, task or area refuses the new claim and names
the holder; the TTL (default 120 minutes) frees it when the holder dies. The
`teamwork-bus.ts` extension registers `session:<PI_SESSION_ID>` at `session_start`,
delivers pending mail at `before_agent_start`, and refuses a `write` to a claimed path.
Full contract: `docs/Team/Architecture.md` section 18.

## Two-stage quality gate

Two gates, in order. **Self-check** (the author) re-reads the diff, *runs* a test and
records it. **Independent review** (the Reviewer) judges it against the requirement
and either passes it (task `done`, archived, merged) or fails it back to the owner.

```text
todo -> doing -> selfcheck -> review -> done (merged into main by the Reviewer)
         |        ^            |
   branch start   |            v  (fail)
                  +-------- doing
```

**Evidence is graded and a pass reads the grade.** `strong` = a program produced it
(`-> 12 passed`, `exit 0`, `# issues: 0`); `medium` = a pointer a reader can follow
(`path:line`, `TS-0006 @rev`); `weak` = a command with no result; `noise` = a
self-assessment ("looks good", "verified") and it is **refused** on a passing
self-check and on a passing verdict.

**A closed lane has no score to lower.** `preflight` sorts the diff by how hard it is
to undo: `closed` (migration/schema, payment, secret/auth, a workflow that fires on
merge, a release exception, any deleted file) fails until the CEO records
`task set <role> <T-id> --by ceo --authorize '<who said yes + evidence>'`;
`evidence` (constitution, frozen contract, record layer, build config) warns.

- `review` is refused until `self_check: passed`; a passing self-check needs a real
  `--test` line. Evidence travels as a packet: `--baseline`, `--artifact` (hashed
  into the ledger), `--replay`.
- A `--bug` task needs a `tests repro` record of the failing run first.
- Only the owner self-checks, only the Reviewer reviews, and a pass merges at once.
  An author never closes a `review=required` task.
- A re-submitted fix is a **delta**: findings, changed files, the failed criterion
  re-run, one fresh credit. At 3 failures the Reviewer opens a dispute.
**The reviewer judges the artefact, not the author.** The verdict walks six ordered
criteria - delivery and conformance, fidelity, internal consistency, operational
fitness, finish, evidence reproduces - and stops at the first failure; the full rubric
is the `## Ordered criteria` section of `roles/reviewer.md`. Length and polish are not
merits, a shorter exact answer beats a longer one with a gap, "this needs no change"
is a real verdict, and the downside weighs as heavily as the upside.

Full sequence, the rubric and the closed-lane table: `references/Roles.md`
(Submission) and `roles/reviewer.md` (`## Ordered criteria`).

## Self-management charter

The team manages and corrects itself. The user is not part of the loop.

- The CEO resolves priority and scope conflicts, design disagreements, blocked
  tasks and duplicate work internally, records the decision, and moves on.
- Escalations go to the tribunal (CEO + CTO + CFO) after 3 rounds of dispute,
  never to the user mid-flight.
- The user is contacted **only** for: authorization of an irreversible/external
  or red-line action; a change to the goal, budget or non-negotiable constraints;
  a genuine ambiguity that changes what gets built and cannot be resolved from
  the repository, research or a recorded assumption; and the final report.
- Every other decision is made, recorded in `Decisions.md` / global memory, and
  implemented.

## Stop condition

`teamwork.py loop` is the mechanical stop check. It reports CONTINUE with reasons
while any of these hold, and STOP only when none do:

- an acceptance criterion record is missing, pending or unverified (`criteria`);
- a required test layer for an area is missing or not passing, or a staffed role
  has designed no test at all (`tests plan`);
- any task is `todo`, `doing`, `selfcheck`, `blocked` or `review`;
- any `review=required` deliverable is not `review_status: passed`;
- any task branch is not merged into `main`, or a merged branch still exists;
- a gate override is in force, or a memory entry has no `by` provenance;
- any dispute is unresolved (an escalated one needs its tribunal);
- the audit trail is missing, altered or truncated (`ledger verify`).

The human checkboxes in `Project.md`/`Plan.md` are advisory; the machine records
above are what actually gate completion. Run `audit` as well before reporting:
it covers the same ground plus links, LFS, duplicates and ownership sanity.

## Quick reference

```sh
S=<this skill dir>/scripts/teamwork.py

# bootstrap and shared state
python3 $S init --roster slim                      # --agents for an exact list
python3 $S agents-md && python3 $S repo && python3 $S map
python3 $S prompt record --original "<user prompt verbatim>" \
    --round "<what the research round found + evidence>" \
    --enhanced "<the improved prompt the plan decomposes>" --by ceo
python3 $S ask add --question "<the ambiguity>" --option "<a>" --option "<b>" --recommend 1 --by ceo
python3 $S ask answer Q-0001 --choice 2 --by user --note "<the user's reason>"
python3 $S criteria add --id AC-1 --text "<verifiable statement>" --owner developer --by ceo
python3 $S tests require --area auth --layers unit,integration,acceptance --by ceo --reason "core"
python3 $S tests add --layer unit --area auth --command "go test ./internal/auth"
python3 $S tests run TS-0001 --by developer-1 --result pass --evidence "<cmd> @<rev> -> <result>"

# work: own branch -> commit -> self-check -> PR -> review -> Reviewer merge
python3 $S task next developer-1
python3 $S branch start --agent developer-1 --task T-0007 [--worktree]
python3 $S commit --role developer --type feat --task T-0007 --area auth \
    --goal "..." --deliverable "..." --why "..." --status "..." --result "<cmd> @<rev> -> result" --all
python3 $S selfcheck developer T-0007 --by developer-1 --note "<what you re-read>" \
    --test "<cmd> @<rev> -> <result>"
python3 $S pr open --agent developer-1 --task T-0007
python3 $S review developer T-0007 --by reviewer-1 --result pass --evidence "<verify cmd @<rev> -> result>"

# scale, coordinate and learn
python3 $S graph && python3 $S graph audit            # what fires next, on which state, and at what cost
python3 $S graph baseline --record '<cmd> -> <result>' --tokens N --by ceo
python3 $S instance add architect --count 2 && python3 $S instance list
python3 $S memory claim architect --by Architect-2 --reason "rewrite the contract" \
    && python3 $S memory release architect --by Architect-2
python3 $S skill create --name tw-<kebab-name> --role developer --by developer-1 --for "<when to use>"
python3 $S skill share tw-<kebab-name> --by developer-1
python3 $S dispute open --by developer-1 --against architect --topic "..." --evidence "..."
python3 $S slot acquire --agent developer-3 --provider deepseek --task T-0012

# run the lanes and close
python3 $S swarm run --dry-run && python3 $S swarm run && python3 $S lane status --live
python3 $S lane stop L-0001 --reason "<why>" && python3 $S lane reap   # recycles the finished seats

# close and audit
python3 $S board && python3 $S pulse --commit && python3 $S parallel
python3 $S coordination --strict && python3 $S audit && python3 $S links && python3 $S loop
python3 $S ledger verify && python3 $S ledger export && python3 $S trace T-0007
```

Team lifecycle: `lane start` staffs a lane, `Inbox.md` coordinates it, `lane status|logs` inspects it, `pulse --commit` runs the swarm on every wake (the default) and `swarm run` runs it by hand, and `lane stop` closes them. Per-host launchers and the `LaneCommand` template: `references/Adapters.md`.
