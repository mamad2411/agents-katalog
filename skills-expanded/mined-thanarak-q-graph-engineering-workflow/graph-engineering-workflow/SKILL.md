---
name: graph-engineering-workflow
description: >
  Plan and verify bounded agent graphs for complex coding work. Use when a
  coding agent needs to coordinate independent implementation, research,
  verification, auditing, isolated writers, merge ownership, or targeted
  repair loops. Prefer a single loop for small or genuinely sequential tasks.
license: MIT
---

# Graph Engineering Workflow

## Purpose

Turn a coding request into a task graph of bounded agent loops, independent workers, fresh verifiers, evidence anchors, and explicit merge and repair rules. This is a graph-orchestration discipline, not a checklist and not a reason to spawn agents for every task.

The graph makes independent work wider; it does not make sequential work more complicated. A worker may contain its own loop: do the work, check it against a real anchor, repair it, and report an inspectable artifact.

## Task Routing

Use when the user asks to:

- implement a feature across independent files or components;
- fix or migrate many independent units;
- audit a repository, route set, module set, or data set;
- perform parallel research with evidence checking;
- run security, privacy, test, input, dependency, or code-quality audits;
- coordinate coding agents from Hermes, Codex, Claude Code, or another host.

Do not force this graph for a small, clear, single-file task or for work whose steps have real sequential dependencies. Use one agent loop when there is no meaningful fan-out.

## Operating Principles

These fourteen rules are the summary layer. Each names the section that specifies it, and that section is normative — when this list and a section appear to disagree, the section wins. The same precedence runs one level further out: where a rule is stated here and specified in a `references/` file, the reference wins, and any difference between them is a defect to fix rather than a choice to make.

1. **Architect before fan-out.** Identify the units of work, their inputs and outputs, and the exact dependencies between them. → *Graph Construction*
2. **Delete fake edges.** An edge exists only when downstream work must read upstream output. → *Apply the fake-edge test*
3. **Fan out only independent work.** → *Select topology*
4. **Make each worker bounded.** One job, one input, one output schema, one write boundary, an anchor, a stop condition. → *Define work units*
5. **Do not trust worker self-reports.** A verifier works from a fresh context and a real anchor. → *Audit Graph*
6. **Keep research claims traceable.** → *External Research Graph*
7. **One owner merges.** Parallel workers never jointly edit a shared artifact. → *Implementation Graph*
8. **Isolate writers.** → *Implementation Graph*
9. **Route repairs narrowly.** → *Repair and Conflict Routing*
10. **Cap the graph.** Every limit is an explicit positive value with a recorded observed count, and the budget names a unit this host can observe. → *State and Artifact Contract*
11. **Gate irreversible actions.** Commit, push, deploy, publish, delete, payment, and external send each need an explicit approval for that exact action, granted after the change exists. → *Graph Plan Output*
12. **Report evidence, not confidence.** Report on every outcome, including a capped or abandoned run. → *Default Response Shape*
13. **Close on a graded rubric.** Fix the criteria before the work starts; a fresh grader scores them against evidence. Every graph carries at least one outcome criterion. → *Acceptance Rubric*, *Fresh Grader Loop*
14. **Never infer a worker's success.** A worker that fails, returns nothing, or breaks its output contract has not done its unit. → *Define work units*

## User Interaction

When a request is ambiguous, ask one high-value question at a time before writing code. Ask about the missing behavior, scope, constraint, or success condition — not a generic “what is the pain point?”.

Where the decision has a bounded set of answers, offer no more than four choices plus a free-text alternative, let the user correct the choice, and do not hide a meaningful trade-off inside a default. Use the host's native choice mechanism where it has one, and a short numbered list otherwise.

After clarification, state the confirmed objective, scope, acceptance criteria, constraints, and unresolved questions. The acceptance criteria are what the outcome criteria C11+ are derived from, so confirm at least one even when the request is clear. A clear, low-risk request needs only a concise confirmation; a multi-writer, sensitive, or high-impact graph needs its graph plan approved before implementation.

## Skill Discovery and Routing

Run a short, read-only **Skill Discovery** before selecting the graph for any non-trivial request: inspect the skills available in this environment and match them to the request, the repository context, and the candidate nodes. Skip it when no companion skill would change the approach; a single-file fix does not need a routing pass.

Where the host exposes no skill inventory, do not guess at names and do not claim a routing pass happened. Record the discovery as skipped with that reason and run the base workflow.

Route in two layers: match a node to a known companion skill, then consider any available skill whose description is more specific to the language, framework, artifact, domain, tool, or risk than the known map.

This skill controls topology, ownership, isolation, limits, merge, repair, and reporting; a selected skill controls its domain workflow only. Pass a worker the skills selected for its node, with its task boundary and the reason for each. A missing companion skill is recorded as skipped and never blocks the run.

Read [references/skill-routing.md](references/skill-routing.md) for the routing map and the full rules on worker scope, grader routing, and unavailable skills.

## Graph Construction

### 1. Codebase Investigator (read-only)

For non-trivial repository work, run a **Codebase Investigator** before the graph is designed and before any external research. It maps repository and directory rules, relevant files and patterns, tests and verification commands, interfaces, schemas, dependencies, ownership boundaries, and the current diff and worktree state.

Its output is a compact repository map, candidate work units, known ownership conflicts, and unknowns that may justify external research. Do not modify files or inspect populated secret files during discovery.

For a task without a repository, replace this node with the smallest read-only context discovery that can identify work units and dependencies.

### 2. Define work units

Write each unit as a concrete job, not a vague persona. Examples:

- inspect one route file for missing authorization;
- implement the backend slice owned by `src/auth/`;
- run input and boundary tests for one parser.

Every unit must declare:

- input;
- output artifact or finding;
- evidence required;
- write boundary;
- owner;
- verifier;
- selected skills for this node, each with the reason it was chosen;
- retry and stop condition.

These are the fields C2 grades, so they live in the run record rather than only in the dispatch prompt.

**A worker's result is not assumed.** A worker that fails, times out, returns nothing, or breaks its declared output contract is recorded `failed` or `unusable_output` with a reason, then retried within `max_retries`, rerouted to another owner, or recorded as not done. Continuing as if the output arrived is the failure this rule exists to stop.

**Nested workers are still workers.** A subgraph owner may spawn workers up to `max_depth`, and every one counts against `max_workers`. The cap is on the graph, not on one level of it.

### 3. Apply the fake-edge test

For every proposed edge, answer:

> What exact output crosses this edge, and does the downstream job fail or become materially different without it?

Keep the edge only when the answer is concrete. If two jobs can start from the same state and do not write the same artifact, place them in the same parallel group.

### 4. Select topology

Choose the smallest topology that does the work:

- **single loop:** one worker owns a sequential task;
- **fan-out/fan-in:** independent workers run, then one owner aggregates;
- **conditional route:** a finding or score chooses the next path;
- **repair loop:** a failed anchor returns work to a bounded worker;
- **discovery expansion:** finders produce new units until the stop condition is met, each dispatch counting as one **wave** against `max_waves`;
- **audit fan-out:** independent audit dimensions inspect the same integrated artifact;
- **hierarchical graph:** a bounded subgraph owns one larger area.

A single loop is valid. A graph is justified by real width, independent verification, or a meaningful route—not by the number of boxes in a diagram.

## External Research Graph

Add external research only when the Codebase Investigator identifies an unresolved question that the repository cannot answer. Typical workers research requirements and APIs, dependencies, policy, or external security guidance.

Do not merge worker summaries just because they agree. A fresh research verifier inspects the cited source or code and checks whether the evidence supports the claim, whether the claim exceeds its evidence, whether sources conflict or are stale, whether identifiers, versions, and assumptions match, and whether the worker invented an uncited capability or result.

When findings conflict, preserve both claims and provenance, then route them to a conflict judge or a human decision. The merge owner must not silently choose one.

Each claim is returned in the fixed shape in [references/research-output.md](references/research-output.md).

## Implementation Graph

Split implementation only along real ownership boundaries. Examples are backend, frontend, migration, documentation, or test work when each can proceed without editing the same artifact.

Each implementation worker must:

1. receive a bounded task, its acceptance checks, and the skills selected for its node;
2. work in an isolated worktree, branch, or container when another worker writes concurrently;
3. never modify an artifact owned by another worker;
4. run local anchors — targeted tests, type checks, builds, linters;
5. return changed paths, commands run, real results, and unresolved issues.

Do not report a successful implementation from a worker's prose alone. Read the diff and inspect the command results.

## Audit Graph

After integration, select audit nodes by the change and its risk. Do not run every audit by habit, and prefer a deterministic anchor over an opinion every time.

An audit that reached no anchor is recorded with `result: unverified_review` and labeled that way in the report. The escape hatch is honest labeling, never an invented scanner output.

Read [references/audits.md](references/audits.md) for the audit dimensions and the anchors to prefer.

## Repair and Conflict Routing

The audit merge produces findings with severity, evidence, affected artifact, owner, and required rechecks. The repair router sends each to the responsible worker, and must not restart unrelated workers without a dependency reason.

```text
privacy audit: sensitive value written to debug log
  -> route to logging owner
  -> rerun privacy audit
  -> rerun affected functional/regression tests
```

If audits disagree, do not average the opinions. Route the conflict to an independent judge, a deterministic anchor, or a human gate, and record it unresolved if no authority can decide it.

## State and Artifact Contract

Keep the graph state structured and small. Do not copy every worker conversation into the parent context.

Two properties of that state are normative wherever it is kept. Limits are explicit positive values, each with an observed count recorded against it. And the run log is **appended during the run**, not composed after it: the acceptance grader reads it instead of the build transcript, so a record written afterward is an account of the work rather than evidence of it.

Read [references/state-contract.md](references/state-contract.md) for the full state schema before
dispatching a non-trivial graph, and again when recording limits, approvals, or acceptance results.

## Cross-Provider Use

Use the host's native execution mechanism, but keep the graph contract unchanged. A platform
limitation is never permission to claim a worker ran, a verifier checked something, or parallelism
occurred.

Read [references/hosts.md](references/hosts.md) for per-host execution, isolation, and grader
guidance before dispatching workers on a host you have not used in this session.

## Graph Plan Output

Before executing a non-trivial graph, show a compact plan, and ask for approval when the graph has
material scope, cost, security, privacy, data-loss, or multi-writer trade-offs. Do not ask for
approval merely to run a read-only inspection the user already requested.

The plan names every irreversible action the graph could reach — commit, push, deploy, publish,
delete, payment, external send — and each one still needs its own approval at the moment it is
reached, once the change exists and can be inspected.

Read [references/output-contracts.md](references/output-contracts.md) for the plan template.

## Acceptance Rubric

The graph is accepted only when a fresh grader passes **every applicable criterion** — `passed == applicable`. Each criterion is binary and must be answered with an evidence pointer: a `file:line`, a command and its output, or an artifact id.

**C1–C10 grade how the graph was run**: topology, bounded workers, isolation, research, audits, anchors, routing, limits, gates, and the report. They do not grade whether the work is correct — a graph that follows every rule while shipping the wrong behavior passes all ten.

**C11 upward grade the outcome**, one per acceptance criterion, derived from `task.acceptance_criteria` and never from what the workers happened to build. **Every graph carries at least one.** Where the user confirmed none, derive one from the request, state it in the graph plan, and grade it. A score built from C1–C10 alone is never an acceptance; it is a well-run graph whose outcome is ungraded, and it reports as `blocked`.

A process criterion the task does not exercise is marked `not_applicable` with a one-line reason and leaves the denominator, so a small graph may legitimately be accepted at 8/8. **An outcome criterion is never `not_applicable`**: dropping the user's own requirement out of the denominator is a rubric edit wearing a verdict's clothes.

Each criterion declares an evidence class: `artifact` and `rerun` the grader settles for itself, `record` it can only read from the run log. No arrangement of record-class passes opens the gate while an outcome criterion is failing.

Read [references/rubric.md](references/rubric.md) for the ten process criteria, their pass conditions and evidence classes, the outcome-criterion rules, and the one case in which a human decision may stand in for an independent grader.

## The Grading Loop

The rubric runs one way: a fresh grader scores it, every failure routes to its owner, and the next round re-grades everything. The loop is not optional and has no variant that grades without repairing. Independence comes from context isolation and ownership routing, not from banning repair — the grader itself never repairs anything.

A read-only score is still available, as a request rather than a mode. When the user asks to grade, score, audit, or review **without changing anything**, run exactly one round, repair nothing however small, record `gate: measured`, and hand the decision back to the user. If the user then asks for repairs, run the loop and say that it started.

Read [references/rubric.md](references/rubric.md) for what such a round must report, and for what "changing anything" does and does not cover.

Say in the graph plan whether the loop will run, and say the same in the final report.

## Fresh Grader Loop

The grader is a node in the graph, not a formality at the end of it.

1. **Grade with a fresh context.** The grader receives the rubric, the final artifacts, the diff, and the run record — never the build conversation. A grader that watched the work is not an independent check.
2. **Return a defect list, not a verdict.** Per criterion: id, class, evidence, and for a `fail` a severity of `blocker`, `major`, or `minor` plus the specific defect — plus the criteria it can see are unreachable. The grader returns no `score` or `gate`: a fresh context knows neither the round number nor the round budget, so the loop controller computes those from the verdicts and `max_grader_rounds`. Severity sets repair order; only pass/fail decides whether the gate opens.
3. **Route failures narrowly.** Each defect goes to the responsible worker through the repair router, not back through the whole graph.
4. **Re-grade the whole rubric.** The next round re-checks every criterion, so a fix cannot silently break one that already passed.
5. **Never edit the rubric mid-loop.** The criteria are fixed before the first round. If one turns out to be wrong, stop the loop and get the user's decision — do not soften it, drop it, or mark it not applicable to make the score rise.
6. **Stop at the cap.** The loop ends at a full applicable score or at `max_grader_rounds`. Hitting the cap with criteria still failing is a capped result, not a completed one: report the score, the open defects, and what remains.

```text
build -> fresh grader -> full score? -> yes -> human gate
                           |
                           no -> defect list -> narrow repair -> re-grade (round + 1)
                                                                   |
                                                        rounds spent -> capped: report and stop
```

The round's output shape is fixed: see [references/grader-output.md](references/grader-output.md).

For a small single-loop task this collapses to one grading pass over a short rubric. Do not spawn a grader graph for work a single fresh read can settle.

## Default Response Shape

Report one consolidated result, not a transcript from every worker. Never fabricate worker output,
test results, scan results, URLs, commits, or successful external actions. A capped run, an
abandoned run, and a run whose workers failed get the same report as any other: what did and did
not happen.

Read [references/output-contracts.md](references/output-contracts.md) for the required report contents.

## Pitfalls

The common failure modes — fake edges, unisolated writers, anchorless audits, self-graded
acceptance, a self-report treated as proof — are catalogued in
[references/pitfalls.md](references/pitfalls.md). Read it when a graph feels wrong but no rule has
obviously been broken.
