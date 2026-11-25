---
name: swarm-complexity-audit
description: Read-only audit of an AI-driven software, research, benchmark, or data-production project that sorts its complexity into what the goal and trust chain actually require and what is accidental, speculative, control debt, or scale-induced, then outputs delete / merge / defer / keep / solidify decisions. Use when the user asks "is this complexity necessary", "audit my pipeline", says there are too many stages or they are babysitting the system, or asks whether to solidify the current system or go back to a golden path / micro-batch.
---

# Project complexity audit

**What this is:** a diagnosis of which complexity in an AI-driven project is required by its goal and trust chain, and which comes from architecture choices, premature generalization, control-plane debt, or an urge to scale. The output is a set of delete and solidify decisions. It is not a design for a bigger platform.

**Core principle:** justify complexity item by item; never defend the system as a whole. Prefer deleting, merging, doing it by hand, or deferring over adding abstractions. But never use "simplification" as cover for removing a trust boundary that protects a headline claim.

Full rationale for the surrounding workflow: [MANUAL.md](https://github.com/cogito233/swarm-oversight-harness/blob/main/MANUAL.md).

## When to use

Use it when any of these is true:

- The system "runs", but someone has to stay on call for it.
- Stages, queues, artifacts, and config keep growing.
- The project has run for a long time, and most of the work now goes into maintaining it rather than producing conclusions or deliverables.
- It is unclear whether a sandbox, verifier, judge, service, or middle layer is needed.
- You want more throughput, but unknown failures and human interventions are still frequent.
- AI makes new components cheap to build, but maintaining and understanding them keeps getting harder.
- You need to decide whether to solidify the current system or fall back to a golden path / micro-batch.

## How to run it (as the agent)

1. **Run the audit yourself, read-only**, following the phases in "Audit procedure" below. Do not edit code, refactor, install dependencies, or start expensive runs.
2. **Collect the input pack first** (below). If the user has not supplied the goal and evidence, do a read-only inventory and ask for what is missing. Do not infer the project's goal from the shape of the code and then draw conclusions from it.
3. **Round one is audit only.** The human signs off on each delete / merge / defer / keep / solidify decision; each accepted item then gets its own SPEC before anyone changes code.
4. **For high-risk deletions, propose a small ablation or shadow run.** Do not recommend tearing something out on intuition.
5. If the user would rather hand the audit to another agent, give them the copyable prompt (the "Audit procedure" section is written so it can be pasted as-is).

### Minimum input pack

At a minimum:

```text
Project root:
goal / the question the project must answer now:
Final deliverable and who uses it:
Most important headline claim or success criterion:
Pipeline entry and exit points:
Logs / manifest / summary of a recent representative run:
The 3 things that currently consume the most human attention:
```

Also useful, if available:

- CHARTER / SPEC / STATE / DECISIONS;
- stage definitions, CLI entry points, schemas, sample artifacts;
- run statistics from a small batch of 10–50 items;
- failure taxonomy, retry and quarantine records;
- number and duration of human interventions;
- the trust chain the final paper, benchmark, or product claim depends on.

---

## Audit procedure (also usable as a copyable prompt)

```text
You are a "project complexity auditor", not an architecture showcase consultant. Do a read-only audit of this project and answer: among the existing stages, services, queues, states, artifacts, config, verifiers, and human supervision, which complexity is necessary; which can be deleted, merged, done by hand, or deferred; and which is necessary but implemented so weakly that it outsources operational responsibility to human attention.

Your goal is not to make the system as elegant as possible, and do not default to recommending Airflow, Kubernetes, microservices, an event bus, a generic plugin system, or re-platforming. Default preference: delete > merge > use an existing mechanism > a small explicit state machine > new infrastructure. AI makes writing code cheap; it does not make owning code cheap over time.

[Project inputs]
- Project root: <PATH>
- goal / the single current research question: <fill in>
- Final deliverable and its users: <fill in>
- Most important headline claim / success criterion: <fill in>
- Entry and exit points: <fill in>
- Representative run / logs / manifest: <fill in paths>
- The 3 things consuming the most human attention right now: <fill in>
- Time, compute, and people constraints: <fill in; in particular, say whether one person maintains it>

[Working rules]
1. Before starting, read the project's AGENTS.md / CLAUDE.md / README / CHARTER / SPEC / STATE / DECISIONS and the files directly tied to the pipeline entry points. Do not scan unrelated directories.
2. Stay read-only throughout. Do not edit, refactor, install dependencies, trigger expensive runs, or start large-scale evaluations. If an experiment is needed to decide something, write the smallest ablation design; do not run it.
3. Separate "the final goal needs some guarantee" from "how the guarantee is currently implemented". A necessary guarantee does not make the current stage, service, or abstraction necessary.
4. Do not accept "we might need it later", "more general", "more scalable", or "better decoupled" as reasons to exist, unless there is evidence from the current workload, a past incident, or a committed requirement.
5. Do not delete trust boundaries for the sake of simplicity either. If a step prevents a rare failure that would contaminate the final benchmark, paper headline, or user data, judge it by expected loss, not by how often it fires.
6. Every judgment must cite a repo path, config, log, run statistic, or explicit user input. Label facts, inferences, and unknowns separately. If evidence is missing, write "unknown"; do not fill in a story.
7. If the project goal is unclear or there are several conflicting goals, first report "cannot audit complexity: the objective is not fixed", and list the fewest questions a human must decide. Do not pretend you can judge necessity anyway.
8. Distinguish reasonable manual failure-mode discovery during the initial build from workflow debt paid repeatedly once things are stable. Handling a first-time unknown error by hand is fine; if a repeated error is still found and recovered by a person, that is control-plane debt.
9. Audit ownership cost, not code size. Check in particular: who keeps the state, who notices failures, who recovers, who verifies, who absorbs silent contamination, and who will understand it three months from now.
10. Do not give advice in abstract adjectives. Every recommendation must say what to delete / merge / defer / keep / solidify, what it protects, what it sacrifices, and how to verify it.

[Phase 1: Reconstruct the goal and the trust chain]
Do not propose solutions yet. First output:
A. A one-sentence goal.
B. The minimum trust chain by which the final deliverable moves from "candidate" to "trusted".
C. 3–7 headline claims / invariants that must be protected.
D. Explicit non-goals: what does not need to be supported now.
E. If the user did not provide the above, point out candidate evidence and conflicts in the repo, but do not quietly decide for the user.

[Phase 2: Map what exists, not the ideal architecture]
Reconstruct from actual code and run materials:
- Stage DAG / pipeline: each stage's inputs, outputs, success criterion, and where failures go;
- State ownership: where each item's authoritative state lives;
- Artifact lineage: how source, commit, config, pipeline version, and outputs are linked;
- Control plane: scheduling, retries, recovery, quarantine, alerts, human gates;
- Trust boundaries: which results are self-certified by the same generator, which are independently verified;
- Human interruption points: why each human intervention happens and whether it changes a decision.

Show this as a compact diagram plus tables. If the same state has several sources, or state lives only in a terminal or someone's head, flag it in red as "state debt".

[Phase 3: Classify each piece of complexity]
Put every stage, long-running service, queue, artifact/schema, major state, config dimension, verifier, and human gate into one of these classes:

1. ESSENTIAL: required by the goal or the trust chain; deleting it breaks an explicit claim.
2. ACCIDENTAL: the guarantee may be needed, but the current split, interface, or implementation adds extra complexity.
3. SPECULATIVE: generalized for a future need that has not happened and is not committed.
4. CONTROL_DEBT: the data plane works, but missing state, recovery, isolation, or summaries force a human to stay on call.
5. SCALE_INDUCED: only needed once the current or a larger scale crosses a threshold; judge whether that threshold has been reached.
6. UNKNOWN: not enough evidence; needs a minimal experiment or a human decision.

For each item, fill in:
- name and path;
- the final claim it serves;
- the specific failure mode it prevents;
- the observable consequence of deleting it;
- current frequency or evidence;
- a cheaper alternative mechanism;
- class and confidence;
- recommended action: KEEP / DELETE / MERGE / MANUALIZE / DEFER / SOLIDIFY;
- the smallest experiment that would verify that action.

Check these complexity multipliers in particular:
- a stage with only thin transformation logic that owns its own state;
- the same sandbox / environment built repeatedly;
- several schedulers, queues, or databases jointly owning the same item;
- intermediate artifacts converted between formats over and over;
- more config options than real experimental variables;
- several backends supported when only one is actually used;
- a one-off research slice turned into a standing platform;
- a downstream step that already catches the same error an upstream stage exists to prevent;
- a verifier that shares a source with the generator, certifies itself, or can be gamed;
- human attention being interrupted in a streaming fashion just because machine execution streams.

[Phase 4: Estimate single-owner cost]
Do not report only LOC. Inventory the project's "operational surface":
- number of stages;
- states per stage and total state transitions;
- number of artifact / schema types;
- identifiable failure classes and number of unknowns;
- number of recovery paths;
- peak in-flight items;
- number of human gates;
- human interventions and minutes per 100 items (if data is missing, mark unknown and suggest how to sample it);
- number of key questions that can only be answered by digging through logs;
- bus factor and key tacit knowledge.

Answer:
1. Can one person own this system for the long term, not just get it running for now?
2. Is the human currently mostly making high-value semantic judgments, or acting as a database / state machine / scheduler / alerting system?
3. What happens if the maintainer is away for two hours, two days, two weeks?
4. Which three complexity items take the most supervisory attention (not the most code)?

[Phase 5: Propose three versions, not one "big refactor"]
Give three comparable options:

A. MINIMAL GOLDEN PATH
- To answer the single current question, what is the minimum set of stages and trust boundaries to keep?
- Which steps fall back to a single command, manual work, or a 10-item micro-batch?
- How much state, how many artifacts, and how many long-running services can be removed?

B. SOLID SOLO PIPELINE
- Keep the capabilities needed now, but add the minimum control plane one person needs to own it: single-item replay, persistent state, idempotent / immutable artifacts, quarantine, summaries, actionable alerts.
- Add no platform capability beyond the current workload.

C. SCALE PATH (only if evidence supports it)
- Above which quantitative threshold does heavier scheduling, concurrency, or infrastructure become worth it?
- Write the trigger threshold; do not write "once we get bigger".

For each option compare: claims protected, expected yield, human minutes per 100 items, risk of silent contamination, implementation cost, long-term ownership cost, reversibility.

[Phase 6: Prioritize execution]
Give at most 5 actions, ordered as:
1. complexity that can be deleted right away without harming the trust chain;
2. stages / states / artifacts that can be merged;
3. the generalization most worth deferring;
4. the largest control-plane debt;
5. scale-up that is allowed only after the away-from-desk test passes.

For each action write:
- exact change boundary;
- why now;
- what not to do;
- acceptance metric;
- how to roll back;
- how much it is expected to reduce human interventions or state space.

[Required validation]
1. 10-item micro-batch: measure stage yield, failure taxonomy, human interventions / minutes, number of unknowns.
2. Delete / merge ablation: on the same small batch, change only one structural factor; do not overwrite headline results.
3. Two-hour away-from-desk test: normal items keep going, abnormal ones are safely quarantined, nothing is silently contaminated, and on return the summary alone is enough to decide.
4. Recovery drill: kill a stage midway; verify it recovers from persistent state without overwriting analyzed artifacts.
5. Trust-chain spot-check: sample accepted items and confirm the simplification has not let the generator certify itself or let the verifier miss key failures.

[Final output format]
# Complexity audit conclusion

## 1. Verdict
- One sentence: which combination of necessary complexity / accidental complexity / premature generalization / control-plane debt / scale mismatch this mainly is.
- Whether to keep building the big system, solidify first, or fall back to a micro-batch.
- Highest risks: one for silent errors, one for human attention.

## 2. Goal and minimum trust chain
<goal, claims, non-goals, trust-chain diagram>

## 3. Current-state map
<actual stage DAG, state and artifact ownership>

## 4. Complexity ledger
<per-item classification table with paths, evidence, actions, confidence>

## 5. Single-owner cost
<operational surface, human interventions, away-from-desk scenarios>

## 6. Three target shapes
<Minimal Golden Path / Solid Solo Pipeline / Scale Path comparison>

## 7. Five recommended actions
<prioritized, executable, reversible>

## 8. Questions a human must decide
<only questions that change the goal or a trust boundary and cannot be settled from repo facts>

## 9. Minimal validation plan
<10-item batch, ablation, away-from-desk and recovery tests>

End with a "cut summary":
- DELETE:
- MERGE:
- MANUALIZE:
- DEFER:
- KEEP:
- SOLIDIFY:

Do not close with "needs further research". Even when evidence is thin, state the most reasonable provisional judgment, the missing evidence, and the smallest action that would obtain it.
```

---

## Four questions for the human reviewing the output

The audit agent may itself lean toward architecture styles it knows well. Before signing off, ask:

1. **Is what gets deleted an implementation, or a trust guarantee?** If the latter, where is the replacement mechanism?
2. **Does the new control plane actually reduce on-call work, or does it create another system that needs someone on call?**
3. **Is the claimed scale backed by a threshold from current data, or by a "might happen later" story?**
4. **Do the recommendations move human time from state tracking to semantic judgment?** If not, the complexity has only moved.

## Pass criteria

An audit's output is worth accepting only if:

- every kept item links to a final claim or a specific failure mode;
- every deleted item has a counterfactual and a minimal validation;
- no small problem was replaced by a heavier platform;
- current needs are clearly separated from future trigger thresholds;
- there is a quantified baseline of human interventions;
- the plan includes an away-from-desk test and a recovery drill;
- what ultimately shrinks is the operational surface and supervisory attention, not just LOC.
