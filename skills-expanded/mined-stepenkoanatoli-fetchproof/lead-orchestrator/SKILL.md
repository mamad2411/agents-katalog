---
name: "lead-orchestrator"
description: Run substantial work as a lead engineer who plans, researches external facts through Fetchproof before designing, freezes shared contracts, delegates independent units to parallel sub-agents on the model most likely to succeed at each role, has fresh-eyed reviewers try to break the result, and ships only what was verified. Every phase checkpoints to an on-disk run ledger, so a run that stops - usage limit, context reset, crash - is resumed from its last checkpoint, never repeated. Use it whenever a task is multi-step or multi-file in any project or language - a plan task, a feature, a batch of bug fixes, a migration, a refactor, a PR to deliver, "implement task N", "ship this", "break this into units" - when the user asks to orchestrate, use sub-agents, work in parallel, research before building, go faster without losing quality, be careful, or when they say "continue", "resume", "pick up where it stopped", "where were we". Skip it for one-step edits and quick questions.
---
<!-- Modified by Fetchproof on 2026-10-22: received as lead-orchestrator 2.0 (the owner's claude.ai account copy, dated 2026-10-04), which replaces the StepenkoAnatoli/SkillsMDs 3f2d2fc baseline (ADR-0190); the kit's old name, Research-Kit, is Fetchproof here, as are the paths and variables that spelled it (ADR-0186). -->

# Lead Orchestrator

## Purpose

Deliver multi-step engineering work faster and to a higher standard by separating four
responsibilities: **planning and integration** (the lead), **research** (facts outside the
repository, collected as evidence), **execution** (builders working in parallel), and
**verification** (independent reviewers). The lead owns the outcome. A sub-agent's report is
evidence to be checked, never a conclusion to be repeated.

The run itself is durable. Every phase leaves its deliverable on disk and records a checkpoint
in the **run ledger**, so an interruption costs the work since the last checkpoint and nothing
more. Credits spent, commits made and reviews passed are never paid for twice.

## Quick reference

| Phase | Name                        | Executed by            | Parallel | Deliverable on disk (checkpoint)                    |
|-------|-----------------------------|------------------------|----------|-----------------------------------------------------|
| R     | Orient and resume           | Lead                   | No       | `RUN.md` read or created; next action chosen        |
| 0     | Project facts               | Lead                   | No       | "Orchestrator facts" current; baseline; kit READY   |
| 1a    | Discovery (internal)        | Explorers              | Yes      | Area summaries saved under `reports/`               |
| 1b    | Research (external)         | Researchers            | Yes      | Fetchproof project per topic: preflight PASS, `BRIEF.md` |
| 2     | Plan and freeze contracts   | Lead                   | No       | Task statement; work breakdown; every brief written; contracts committed |
| 3     | Build                       | Builders               | Yes      | One commit per unit, with accepted report           |
| 4a    | Unit review (pipelined)     | Unit reviewer          | Yes      | Findings per landed unit, dispositioned             |
| 4b    | Integration review          | Reviewers              | Yes      | Cross-unit findings, mutation sweep, invariants     |
| 5     | Documentation               | Documentation agent    | Yes      | Specs, architecture and plan updated                |
| 6     | Integration and delivery    | Lead                   | No       | Gate passed against baseline; final report; `RUN.md` COMPLETE |

## Operating principles

1. **Parallelize only what is independent.** Units run concurrently only when they own disjoint
   files and build on frozen contracts. Contention between agents costs more than it saves.
2. **Facts outside the repository are fetched, never guessed.** API limits, pricing, licence
   terms, platform capabilities and third-party behaviour are collected through Fetchproof as
   cited evidence before they shape a design. See `references/fetchproof.md`.
3. **Freeze interfaces before implementation.** The lead defines shared types, schemas, error codes
   and signatures first, so builders never wait on, or guess at, each other.
4. **Separate building from reviewing.** No agent reviews its own work. Independent review is the
   main defence against confident but wrong output.
5. **Evidence over assertion.** "Verified" means a command was run and its result observed. Every
   new test must be shown to fail without the change it guards - with the guard the test names
   removed, on the test's own input. A test that stays green with its guard removed proves
   nothing, however many other rules happen to catch that input.
6. **Protect the lead's context.** Delegate wide reading, collection and long-running loops;
   consume summaries. Reports go to disk; the lead reads their structured sections. The lead's
   context is for decisions.
7. **Everything needed to continue is on disk.** State that lives only in the conversation is
   lost when the conversation is. Plans, briefs, reports, decisions and the next action are
   written to the run folder as they happen, not reconstructed afterwards.
8. **Careful before fast.** Speed comes from overlap, scope and preparation, never from skipping
   a step. Builders look before they change, verify instead of assume, and report mistakes
   plainly. See `references/careful-execution.md`.
9. **Report honestly.** State what was not verified, what went wrong, and what remains open.

## Model selection and capacity

The lead chooses the model for each sub-agent. The deciding criterion is the probability that
the agent succeeds at its role; cost and speed are secondary and never override it.

- **Default to the most capable model available** in this environment for every role. When a
  more capable model becomes available, prefer it; when the environment does not permit model
  selection, use what it provides and note that in the report.
- **Always the most capable model** for: the lead's own reasoning; researchers; builders of any
  unit touching data, money, auth, deletion, concurrency, migrations or external services; every
  reviewer. Review and research are where capability shows up most directly as defects caught or
  missed.
- **A faster model is acceptable only** for a role where capability cannot affect correctness:
  a read-only explorer listing files and symbols, a documentation agent applying mechanical
  updates against a checklist, or a bulk repetition run of an existing test. If there is any
  doubt, use the most capable model.
- **On failure, escalate the model first.** If a sub-agent on a lesser model returns a weak or
  failed result, re-run the same brief on the most capable model before spending a retry on
  anything else.
- Record the model used by every sub-agent in `RUN.md` and the final report.
- Default concurrency: up to **5** sub-agents. Reduce it for small tasks, when tests share
  resources that cannot be isolated, or when researchers share a metered collection budget.
- Sub-agents have no access to this conversation. Every brief must be self-contained. Use the
  templates in `references/agent-briefs.md`.

## Engagement levels

Select the lightest level that matches the risk. Escalate as soon as higher risk becomes apparent.
Phase 1b applies at any level whenever the research trigger (below) is met. The run ledger is
kept at every level above Direct.

| Level  | Use when                                                                                   | Phases                                        |
|--------|--------------------------------------------------------------------------------------------|-----------------------------------------------|
| Direct | One-step change, verifiable in minutes, low risk, no external facts                        | None; work directly, following `references/careful-execution.md` |
| Light  | Several files in one area; moderate risk                                                   | R, 1b if triggered, 2, 3, 4a (one unit reviewer covers spec and breaking), 6 |
| Full   | Multiple areas, unfamiliar code, or high risk: data, money, auth, deletion, concurrency, migrations, external services, user-facing releases | All phases; 4a per unit and 4b with all four reviewers |

**Research trigger.** Phase 1b is required when the design or implementation depends on a fact
that the repository cannot answer: an API's behaviour or limits, pricing, what a licence permits,
whether a platform can do what the design assumes, a third-party library's behaviour at a given
version, a legal or regulatory rule, an external data format. If an existing research project
already covers the fact with a passing gate, reuse its brief instead of collecting again.

## The run ledger

Every orchestrated task has a **run folder** - by default `docs/orchestration/<YYYY-MM-DD>-<task-slug>/`,
or the convention recorded in the project facts - holding:

| File or folder        | Content                                                                 |
|-----------------------|-------------------------------------------------------------------------|
| `RUN.md`              | The ledger: status, **next action**, task statement, baseline, units with status and commit, reviews, findings with dispositions, decisions, log |
| `briefs/<id>.md`      | Every brief, written in Phase 2 before anything is launched              |
| `reports/<id>-<n>.md` | Every sub-agent return, saved verbatim before the lead evaluates it     |

`RUN.md` is the single source of truth for where the run stands. It is written at every
**checkpoint**: after orientation; at every phase exit; when a brief is launched; when a report is
saved; when a unit is accepted or integrated (with the commit); when a finding is dispositioned;
before any launch once the conversation has grown long; and at completion. Writing it takes
seconds; not having it costs the whole run. Commit the run folder on the working branch alongside
the work it describes unless the project forbids it (then keep it in an ignored folder and say so
in the report). Schema, status vocabulary and the resume procedure are in
`references/run-ledger.md`.

**When a limit approaches** - the environment warns about usage or context, or the conversation
is long - checkpoint first, launch second. A run cut off between checkpoints loses only what was
in flight, and in-flight work survives anyway: builders commit to their own branches, research
pages are cached and ledgered, and reviews are saved as they return.

## Roles

| Role               | Responsibility                                               | Write access                      |
|--------------------|--------------------------------------------------------------|-----------------------------------|
| Lead               | Plan, contracts, briefs, triage, integration, ledger, final report | Working branch, run folder, plan, contracts |
| Explorer           | Map code, tests and contracts for one area                   | None                              |
| Researcher         | Run Fetchproof phase 1 for one topic to a passing gate and a brief | The research project folder only; no product code |
| Builder            | Implement one unit, test-first, with evidence, from the brief | Owned files, own branch          |
| Unit reviewer      | Spec check and adverse-condition probe of one landed unit    | Tests and scratch files only      |
| Spec reviewer      | Compare the integrated change with task, plan, specification, design and research brief | None |
| Breaker            | Find failures across units under adverse conditions, with reproductions | Tests and scratch files only |
| Mutation auditor   | Prove the tests detect defects in the change                 | Temporary mutations, restored     |
| Invariant auditor  | Prove project invariants still hold                          | Checks and tests only             |
| Documentation      | Bring specs, architecture notes and plan up to date          | Documentation files               |

## Workflow

Each phase has entry criteria, actions, a checkpoint and an exit deliverable. A phase starts only
when the previous phase's deliverable exists on disk.

### Phase R: Orient and resume (every start)

- **Actions:** Before touching anything, look for an existing run folder for this task (the
  project's convention, `git log --all -- <run folder root>`, or the user's reference). If one
  exists, follow the resume procedure in `references/run-ledger.md`: read **Next action** and the
  unit table; verify every recorded commit, branch and worktree against `git log`, `git branch`
  and `git worktree list`; treat uncommitted changes as the interrupted unit's work in progress,
  never as state to trust; downgrade any status the disk does not confirm; re-run the key test of
  any unit accepted but not integrated. Then continue from Next action. If no run folder exists,
  create it with the task statement stub and the first Next action.
- **Checkpoint:** `RUN.md` with a log line "resumed at <checkpoint>" or "started".
- **Exit:** the lead knows what is done, what is in flight, and what comes next - from disk, not
  memory. Never redo a phase whose deliverable is on disk and verified.

### Phase 0: Project facts (once per project)

- **Entry:** first orchestrated task in this project, or the facts are stale.
- **Actions:** Look for an "Orchestrator facts" section in the project's agent instructions
  (CLAUDE.md, AGENTS.md or equivalent). If present, use it and correct anything outdated. If
  absent, discover the facts and add the section using `references/project-facts-template.md`.
  Run the full gate on the base branch and record the **baseline**: the base commit and the exact
  set of checks that already fail. Check Fetchproof readiness: run its `doctor` inside the
  project and record the result, the kit path, the machine role and the research folder
  convention (see `references/fetchproof.md`, "Readiness").
- **Checkpoint:** baseline (commit and failing set) recorded in `RUN.md`.
- **Exit:** a current facts section with gate commands, acceptance environment, baseline, sources
  of truth, conventions, invariants, run folder convention and Fetchproof facts. Tell the user
  it was added or changed.

The baseline is essential: without it, a regression cannot be distinguished from a pre-existing
failure. Re-measure it only when the base commit has moved; otherwise reuse it.

### Phase 1a: Discovery (parallel, read-only)

- **Entry:** the task touches code the lead has not already mapped in this session or in a saved
  report.
- **Actions:** Launch two or three explorers, one area each (for example: the module under change,
  its callers, the relevant tests and fixtures). Proceed as soon as the summaries needed for
  planning have arrived. Skip areas a saved explorer report already covers.
- **Checkpoint:** each summary saved under `reports/`.
- **Exit:** concise summaries with file paths, current behaviour, applicable contracts and risks.

### Phase 1b: Research (parallel per topic, Fetchproof)

- **Entry:** the research trigger is met and no passing research project already covers the fact.
  Fetchproof `doctor` ends with `READY` on this machine.
- **Actions:**
  - Define one research topic per independent question. Launch one researcher per topic, each in
    its own research project folder, following the kit's protocol in `references/fetchproof.md`:
    scaffold, decompose and classify the map, write the contract of unknowns and the plan, collect
    (dry run first), rewrite every finding with a quote, pass `preflight`, write the brief.
  - Give every researcher a page budget. Researchers share one collection budget and the kit's
    cache; they do not share folders. A researcher resuming a partial project spends nothing on
    pages already cached.
  - The lead reads each `BRIEF.md`, confirms `preflight` passes with exit 0, and checks that every
    blocking unknown is CLOSED with evidence or marked KNOWN-UNKNOWN with a day-one verification
    step. A brief that rests on an unproven unknown is returned to its researcher.
  - Run Phase 1a and 1b concurrently when both apply.
- **Checkpoint:** each research folder, its gate result and brief path recorded in `RUN.md`.
- **Exit:** for each topic, a committed research project with a passing gate and a brief. Research
  writes no product code.

### Phase 2: Plan and freeze contracts (lead only)

- **Entry:** sufficient understanding of the task and the affected code; every research brief
  the design depends on is passing.
- **Actions:**
  - Write the task statement: goal, success criteria, what is out of scope, and which brief each
    externally sourced design decision rests on.
  - Decompose the work into units. One unit is one commit and one reviewable change.
  - Assign each unit a disjoint set of files, its dependencies, and a wave number. Use the format
    below.
  - For each unit, write a two-line **pre-mortem**: the most likely ways this unit fails review
    (the edge case that gets missed, the caller that gets forgotten, the platform difference).
    The pre-mortem goes into the builder's acceptance criteria and the unit reviewer's focus.
  - Implement and commit the shared contracts (types, schemas, error codes, signatures, file
    formats). From this point, contract changes go through the lead only.
  - Write **every brief now** - builders, unit reviewers, integration reviewers, documentation -
    to `briefs/`, from `references/agent-briefs.md`. Launching later is then a file read, and a
    resumed run has its briefs waiting.
  - Raise all blocking questions with the user in a single message. For non-blocking unknowns,
    record the assumption in `RUN.md` and proceed.
- **Checkpoint:** task statement, work breakdown, contracts commit and brief paths in `RUN.md`.
- **Exit:** the task statement, the work breakdown, every brief on disk, and committed contracts.

**Work breakdown format**

| Unit | Description                | Owns                              | Depends on | Wave | Pre-mortem |
|------|----------------------------|-----------------------------------|------------|------|------------|
| U0   | Shared contracts           | `src/contracts/*`, `src/errors.ts` | -          | 0 (lead) | - |
| U1   | Pure planning function     | `src/plan.ts`, `tests/plan.test.ts` | U0        | 1    | empty plan; duplicate ids |
| U2   | Settings persistence       | `src/settings.ts`, `tests/settings.test.ts` | U0 | 1    | partial write on crash; path separators |
| U3   | Supervisor                 | `src/supervisor.ts`, `tests/supervisor.test.ts` | U1, U2 | 2 | restart mid-step; duplicate delivery |

### Phase 3: Build (parallel where independent)

- **Entry:** contracts committed; work breakdown complete; briefs on disk; research gate passing
  where required.
- **Actions:**
  - Launch all wave-1 builders at once. Start each later unit as soon as its own dependencies
    have landed, not when its whole wave has finished.
  - Give each builder the path of the research brief its unit depends on. Builders implement
    from the brief and never re-research: a builder who finds a fact missing reports which one,
    and the lead sends a researcher to collect it.
  - Isolate each builder: a dedicated git worktree and branch where available; a private
    temporary directory; separate ports, database files and other resources its tests use. Where
    worktrees are unavailable, enforce strict file ownership and serialize builders whose tests
    share resources.
  - Builders commit only to their own branch, and commit as they go: a builder's branch is its
    own checkpoint. A builder that stops is re-briefed with the **resume clause** (branch, commits
    present, tests present, what remains), never restarted from nothing.
  - While builders run, the lead does not idle and does not poll: it readies the next launches,
    reviews returned reports, and updates the ledger.
  - The lead saves each report to `reports/`, checks it against the acceptance rules below,
    re-runs the unit's key test, and cherry-picks onto the working branch in plan order.
- **Checkpoint:** every status change of a unit, with branch, commit and report path.
- **Exit:** every unit on the working branch with an accepted builder report.

### Phase 4a: Unit review (pipelined with the build)

- **Entry:** a unit is integrated on the working branch while other units are still building.
- **Actions:** Launch one unit reviewer per landed unit immediately (brief in
  `references/agent-briefs.md`), covering the spec check and the adverse-condition probe for that
  unit alone, with the unit's pre-mortem as its first focus. Findings are triaged as they arrive;
  S1 fixes go to a fix brief while later waves continue. At Light level this is the whole review.
- **Checkpoint:** each review's status, report path and findings.
- **Exit:** every landed unit reviewed and its findings dispositioned.

### Phase 4b: Integration review (parallel, Full level)

- **Entry:** all units are integrated on the working branch, so that interactions between units
  are covered.
- **Actions:** Launch the four reviewers (briefs in `references/agent-briefs.md`). None of them
  may have authored the code under review. Each states the commit and working directory it
  reviewed, and lists what it did **not** check.
  - **Spec reviewer:** divergences from task, plan, specification, design and research brief;
    decisions resting on an assumption rather than a cited claim; interactions no unit review saw.
  - **Breaker:** cross-unit failures under adverse conditions - termination and restart, races,
    retries and duplicates, malformed and oversized input, limits, platform and path differences.
    Every finding needs a reproduction. For every new filesystem test it also reads for what
    another platform would do (a link made outside the project's guard, a fixed host path, an
    assertion on a link's stored text, separators, case, line endings) and reports each as a
    finding even though the test is green on this host.
  - **Mutation auditor:** mutates each guard and invariant in the diff, and for every new test
    removes the guard that test names and runs that test alone; green is SURVIVED, whatever else
    catches the input, and the report names the input that would reach the guard.
  - **Invariant auditor:** demonstrates each project invariant still holds.
- **Checkpoint:** each review's status and report path; every finding with its disposition.
- **Exit:** every finding triaged and dispositioned (see Finding triage); every S1 fixed and
  re-reviewed.

### Phase 5: Documentation (parallel with Phase 4 once the code is stable)

- **Actions:** Update specifications, architecture notes and plan progress in the project's
  existing style. Every identifier mentioned must exist in the source; every link must resolve;
  differences between design and implementation are stated, not hidden; externally sourced
  facts cite the research brief.
- **Exit:** documentation consistent with the code; project documentation checks passing.

### Phase 6: Integration and delivery (lead)

- **Actions:**
  - Confirm all units are on the working branch in plan order with fixes applied.
  - Run the full gate on the final branch and compare results with the baseline exactly. Where a
    research project exists, run its `preflight` once more and include an `audit` snapshot in the
    report.
  - Write commits and the pull request using `references/report-templates.md`, unless the project
    defines its own conventions.
  - Push to the working branch only.
  - Where the gate has legs the lead's host cannot run (another operating system, another
    runtime version), list them under "Not verified here" and hold the merge until every leg is
    green. A leg that goes red after review is a review miss, not noise: fix it with the same
    discipline as a unit (red-first, the mutation shown, the fix through the gate), record it in
    the review's dispositions, and never patch the test until the leg happens to pass.
  - Remove or list every builder branch and worktree the run created.
- **Checkpoint:** `RUN.md` status COMPLETE, with the final report appended.
- **Exit:** the Definition of Done is met; the final report is delivered.

## Speed without loss

The critical path is shortened by overlap, scope and preparation. These are the only accepted
ways to go faster:

- **Prepare, then launch.** All briefs are written in Phase 2; launching is a file read.
- **Start on dependencies, not waves.** A unit starts the moment its own dependencies land.
- **Review as units land.** Unit review overlaps with the build of later waves; integration
  review runs once, on the integrated branch.
- **Scope the gate.** Per unit: the affected tests and checks. The full gate: at integration
  points and at delivery. Never per sub-agent round-trip.
- **Repeat only what can flake.** The 30-run repetition applies to tests that are concurrency-
  or timing-sensitive, not to the suite.
- **Reuse what is proven.** A baseline measured on an unchanged base commit, an explorer report
  already saved, a research project with a passing gate.
- **Return fast.** A report missing a required item is returned at once, unread beyond the gap.
- **Never idle.** While sub-agents run, the lead prepares, triages and checkpoints. It does not
  poll.

Never cut: test-first with the guard-removal proof, independent review, the gate against the
baseline, the research gate, the ledger checkpoint.

## Careful execution

Builders, fixers and the lead follow the discipline in `references/careful-execution.md`: read
the code and its callers before changing it; check a signature, flag or version in the installed
package or the repository rather than from memory; make the smallest change that does the job;
decide the failure path deliberately and never swallow an error; run the thing and read the
output, not the exit code; re-read the diff as a stranger's pull request; use **Verified**,
**Untested** and **Expect** as distinct words; and when a mistake is found, say it first, give its
impact and cause in a line each, fix the root, and re-verify. Every builder and fix brief carries
the discipline block, because sub-agents cannot see this skill. The lead's own version: "the
builder said it passed" means re-run it; "the reviewers found nothing" means read what they did
not check; "I will remember this" means write it to `RUN.md`; "the brief is obvious" means the
sub-agent knows nothing you did not write down.

## Handling sub-agent reports

- Save the report to `reports/` first, then evaluate it; record its path in `RUN.md`.
- Accept a builder report only if it contains: the commit ID; the working directory; the commands
  run with their results; for each new test, the guard it names and the removal of that guard
  that made it fail; the Verified / Untested / Mistakes sections; and a list of what could not be
  verified. Otherwise return it, naming the missing items.
- Accept a researcher report only if `preflight` exited 0, `BRIEF.md` exists, and every blocking
  unknown is CLOSED with an evidence row or KNOWN-UNKNOWN with a verification step.
- Spot-check: re-run the unit's key test, and one further claim chosen from the report. A report
  whose spot-check fails is returned whole.
- Treat any claim without a command and an observed result as unverified.
- Discard changes outside a unit's owned files. Re-brief the unit if the overreach revealed a
  real dependency.
- Reviewer findings are claims too. Confirm the reproduction of every S1 finding before issuing a
  fix brief.
- If a report exceeds its word limit, read only its structured sections.

## Engineering standards for builders

The full list, with the discipline block, is in the builder brief (`references/agent-briefs.md`)
and goes into every builder brief verbatim. The non-negotiables:

- Test first; show the test failing for the intended reason, and failing again with the guard it
  names removed, on its own input, before calling it a test.
- Real collaborators over mocks; substitute only at process or network boundaries.
- Repeat concurrency- and timing-sensitive tests (default 30 runs); any failure is a defect.
- Filesystem tests hold on every CI platform: the project's link guard, the scratch directory,
  lstat and real path - never a fixed host path or a link's stored text.
- Assert against actual output, never a value the test built and compares to itself.
- External behaviour comes from the research brief's claims, never from a hand-fetched page.
- Never weaken, skip or delete a test; never commit debug code, local flags or secrets.
- Commit to the unit's branch at every green step; run the gate for affected files before
  reporting; report mistakes made along the way.

## Finding triage

| Severity | Definition                                                                      | Action                                                             |
|----------|---------------------------------------------------------------------------------|--------------------------------------------------------------------|
| S1       | Incorrect results, data loss, security exposure, invariant at risk, flaky test, a new test that stays green with its guard removed, design built on an unproven external fact | Fix before delivery; issue a fix or research brief; re-review |
| S2       | Real defect with limited impact, or a divergence from specification or brief    | Fix now if contained; otherwise record in the plan with rationale  |
| S3       | Style, naming or minor improvement with no behavioural effect                   | Record under "Recorded for later", or fix if trivial               |
| Rejected | Not a defect                                                                    | Record the reason in one line                                      |

Every finding receives a disposition in `RUN.md`. None is dropped silently. Defects in
Fetchproof itself are recorded as findings with the exact command, output and exit code, and
reported to the user under "Kit findings"; they are never worked around by editing the kit's output.

## Failure modes and recovery

| What happened                                  | What survives                                   | What the lead does                                                     |
|------------------------------------------------|-------------------------------------------------|------------------------------------------------------------------------|
| A builder stops mid-unit                       | Its branch and commits; the brief on disk       | Re-brief with the resume clause; escalate the model first if it was lesser |
| The lead's session ends or its context resets  | `RUN.md`, briefs, reports, branches, commits    | Phase R: orient from disk, verify, continue from Next action           |
| A usage or rate limit stops the run            | Everything checkpointed; in-flight branches     | Nothing until the next session; then Phase R. Checkpoint before launches when a limit is near |
| The base branch moved                          | The old baseline, now stale                     | Re-measure the baseline; rebase the working branch; re-run unit reviews only for units the rebase touched |
| Two units need the same file                   | The plan                                        | Stop both; the lead changes the breakdown or sequences them; re-brief |
| The gate is red after integration              | Per-unit evidence                               | Bisect by unit commit; treat as a review miss; fix red-first           |
| A research project is INCOMPLETE or BLOCKED    | Its cache and ledger                            | Not a pass: return to the researcher or collect on the collector machine; builders wait |
| Fetchproof is not READY                      | Nothing to lose yet                             | Apply `doctor`'s fix; if it cannot be fixed here, record a kit finding and stop Phase 1b |
| An S1 arrives after documentation is done      | Everything                                      | Fix brief; re-review; re-run the documentation checks                  |

## Definition of Done

- [ ] All units on the working branch in plan order
- [ ] Full gate run on the final branch; failures equal the baseline exactly
- [ ] Every new test shown to fail with the guard it names removed, on its own input
- [ ] Concurrency- and timing-sensitive tests repeated without failure
- [ ] Where the research trigger applied: each research project committed with its ledger,
      `preflight` exit 0, brief present, and every design decision traceable to a claim
- [ ] Required reviewers completed; all S1 findings fixed and re-reviewed; all others dispositioned
- [ ] Invariants demonstrated to hold
- [ ] Documentation and plan updated
- [ ] Anything verifiable only elsewhere (for example, CI on another platform) explicitly listed,
      and every such leg green before a merge
- [ ] `RUN.md` status COMPLETE; every builder branch and worktree removed or listed

## Escalation and limits

- A failed unit receives at most two focused retries. After that, the lead completes it or reports
  it as blocked, with the reason, in `RUN.md`.
- Obtain explicit user approval before: merging; force-pushing a shared branch; deleting data;
  modifying production systems; changing an invariant; expanding scope beyond the task statement;
  spending a metered collection budget beyond the page budget agreed for the task.
- Never bypass a gate: no `--no-verify`, no gate-off files, no hand-written evidence.
- When the plan changes during execution, update it in `RUN.md` and state the reason in the final
  report.
- If the run cannot be finished in this session, leave `RUN.md` with an accurate Next action and
  tell the user exactly where it stopped. A partial run honestly recorded is a checkpoint; a
  partial run reported as complete is a defect.

## Final report

Deliver in this order, concisely (template in `references/report-templates.md`):

1. **Summary:** what was delivered, in one or two sentences; whether this run was fresh or resumed
2. **Changes:** one line per commit or unit, with the sub-agent role and model that produced it
3. **Verification:** commands run, test counts, repetition runs, mutations detected, baseline
   comparison, research gate result
4. **Not verified here:** what remains, and which environment or check must confirm it
5. **Defects found and fixed** during the work, including the lead's own mistakes
6. **Open items:** recorded findings, known unknowns, assumptions, decisions needed, kit findings
7. **Run ledger:** path, so the next session can continue or audit
8. **Recommended next step**

Never describe something as working unless it was checked.

## Environments without sub-agents

Execute the same phases sequentially and keep the roles distinct: complete research before
design, complete the build before review, then review the full diff from a clean reading, using
the reviewer briefs as checklists. Keep the ledger exactly as with sub-agents; it matters more,
because a single long session is more likely to be cut.

## Non-engineering work

The same structure applies to research, writing and analysis. Researchers collect sources by
sub-topic in parallel through Fetchproof where facts must be cited; the lead freezes the
outline as the contract; writers draft sections in parallel; an independent reviewer traces every
claim to its evidence row and identifies gaps and contradictions. "Verified" means each claim is
sourced.

## References

- `references/run-ledger.md`: run folder layout, `RUN.md` schema, checkpoint rules and the
  resume procedure. Read at every Phase R.
- `references/careful-execution.md`: the working discipline for builders, fixers and the lead,
  and the block to paste into briefs.
- `references/agent-briefs.md`: self-contained brief templates for every role, including the
  resume clause and the unit reviewer. Read before writing the first brief of a task.
- `references/fetchproof.md`: Fetchproof readiness check, protocol, commands, rules and
  exit codes. Read before Phase 0 and before briefing a researcher.
- `references/project-facts-template.md`: the per-project facts section created in Phase 0.
- `references/report-templates.md`: commit message, pull request and final report templates.
- `references/changelog.md`: dated lessons from runs of this skill and the rules each one changed.
