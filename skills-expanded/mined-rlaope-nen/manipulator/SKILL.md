---
name: manipulator
description: Orchestration engineering for multi-agent and deep-research work — decomposition, routing, prompt design, and verified delegation. Use when the user says "plan this", "break this down", "delegate", "orchestrate", "subagent", "task distribution", "parallel workstreams", "split this across agents", "hand this to three agents", "write a prompt for", or "research X thoroughly"; when work must be divided into workstreams that different agents or people can own; when they ask which model or agent should handle something; when work is multi-step and ambiguous enough that one agent charging ahead would guess wrong; when several independent investigations could run in parallel; or when a subagent has reported "done" and someone is about to believe it.
---

## Stance

操作系 Manipulation is the discipline of controlling other wills precisely — and precision is the entire game. An orchestrator produces nothing directly; its output is exactly as good as the instructions it wraps around other agents and the verification it applies to what comes back. The subagent you dispatch has no memory of your conversation, no access to your intent, and no shame about returning confident garbage. Whatever you did not write into the dispatch does not exist for that agent.

Without this discipline, delegation becomes theater. Vague prompts go out, plausible prose comes back, "done" is accepted because checking feels like distrust, and the orchestrator ends up laundering unverified work into a final answer with its own credibility stamped on top. The delegation is not the hard part. The contract and the audit are the work.

## Boundaries

If the question is still *what* to pursue — which opportunity matters, how to frame the idea, where the impact point is — stop. That is emitter's job. You decompose and route a goal that has already been chosen; planning the execution of an unchosen goal produces an exquisite breakdown of the wrong thing. Come back when there is a decided objective to distribute.

If the whole task collapses into one deep dive on one external mechanism — why does this library behave this way, what is this undocumented API actually doing — stop pretending it needs orchestration. That is specialist's job, and it should be dispatched as a single unit or simply done. You earn your existence when there are several such units with real routing and integration decisions between them; a coordinator over one worker is pure overhead.

If the routing table itself comes up empty — the same need keeps recurring and no existing skill covers it — stop dispatching. That is hatsu's job: forging the missing ability into a skill of its own. Orchestration distributes work across abilities that exist; it cannot conjure the one that doesn't. Come back when the new skill is forged and trial-fired, and route through it.

If the question is only which ability should engage on the single request in front of you — sensing, not decomposing — that is en's field. En reads the problem shape and engages the right disciplines; you take over the moment the routed work must be split into units, dispatched across agents, and verified.

The acceptance criteria you attach to each dispatched unit are that unit's vows, and their form is vow's discipline: falsifiable, declared before the unit starts, audited on return. Write criteria to that standard, and reject any delegate's "done" that arrives without its audit — verification cannot run on pledges nothing can check.

## Method

1. **Decompose into independently verifiable units.** Each unit must have an output you can judge without running any other unit — a document with named required fields, a passing command, a table with specified columns. "Look into the auth options" is not a unit; "return the token-refresh flow for providers A and B with doc links and version numbers" is. If you cannot say what a unit's *checkable* output looks like, you have not finished decomposing.

2. **Classify serial vs parallel by real data dependency, not habit.** B is serial after A only if B consumes A's output. Everything else runs concurrently, in one dispatch batch. Transcripts full of sequential Task calls between independent units are the most common orchestration defect there is — pure wall-clock waste that no one decided on purpose.

3. **Route each unit by difficulty and required context, not by default.** Bulk retrieval and mechanical checks go to a fast, cheap model; synthesis, judgment, and anything with traps goes to a strong one. Routing is also about context: decide what each agent needs to see and put exactly that in the prompt — starved agents guess, and drowned agents drift.

4. **Write acceptance criteria before dispatch, inside the dispatch.** A numbered list of what the return must contain, concrete enough that a third party could grade the return against it. Criteria written after the return is graded on a curve toward whatever came back. This is the step people skip, and it is the one that makes step 6 possible at all.

5. **Make every dispatch prompt self-contained.** The subagent sees nothing but what you send: no "as discussed above", no implied constraints, no ambient repo context you forgot it lacks. State the task, the context it needs, the criteria, and the exact output format. A prompt you would not be able to execute cold is a prompt no subagent can execute either.

6. **Verify returns against the criteria — inspect artifacts, never accept claims.** "Done" is an assertion, not evidence. Walk each criterion against the actual return; open the file, run the command, count the fields. A return that fails gets a rework dispatch quoting the specific unmet criteria — not a from-scratch redo, and never a silent patch-over by you.

7. **Synthesize only from verified returns.** Integration starts when every unit has passed its criteria, and the synthesis cites the artifacts, not the agents' summaries of them. If you find yourself smoothing over a gap during synthesis, a unit failed verification and you are covering for it. Go back to step 6.

## Worked trace

Task: "research thoroughly whether we should replace Elasticsearch with OpenSearch or Typesense for product search — 40M documents, ~90 queries/sec peak." Step 1, decompose by candidate, because per-candidate findings are independently checkable and share no data: three research units plus one serial synthesis unit that consumes all three. Step 2: units R1–R3 are parallel; only synthesis is serial. Step 3, routing: R1–R3 are retrieval-heavy with citation discipline — sonnet-class agents; synthesis weighs tradeoffs against our constraints — opus-class. Step 4 and 5, one dispatch template, instantiated three times and sent in a single parallel batch:

```
Task for agent R2 (model: sonnet) — Typesense evaluation

Context: replacing product search. 40M docs (~2.1KB avg), 90 qps peak,
p95 must stay under 120ms, team of 3 backend engineers, no dedicated
search infra role. Current: Elasticsearch 7.17, self-hosted, 3 nodes.

Return a markdown doc with EXACTLY these sections:
1. Version evaluated (must be current stable, with release date)
2. Scale fit: documented limits or case studies near 40M docs / 90 qps,
   each with a source URL
3. Operational cost: managed pricing at our scale, or self-host node
   spec estimate, with arithmetic shown
4. Migration surface: reindexing path from ES 7.17, query API deltas
   that would touch our code
5. Dealbreaker check: any hard miss on faceting, typo tolerance,
   or synonym support — cite docs, not blog posts
6. "How this candidate loses": the strongest honest case against it

Acceptance criteria: every factual claim in sections 1-5 carries a URL;
version numbers on all capability claims; no section empty; section 3
shows a monthly dollar figure.
```

The three returns land in ~7 minutes of wall clock instead of ~20 serial. Step 6, verification — criterion by criterion, artifact open:

```
R1 (OpenSearch):  6/6 sections, 14 claims / 14 URLs, $1,410/mo shown  PASS
R3 (Elasticsearch stay-put): 6/6, 11/11 URLs, $0 delta + upgrade cost  PASS
R2 (Typesense):   section 2 cites "handles large datasets" from the
                  marketing page, no number near 40M docs; section 3
                  says "pricing scales reasonably" — no dollar figure.
                  Criteria 2 and 3 UNMET.                              FAIL
```

Rework dispatch to R2, scoped to the failure: "Sections 2 and 3 do not meet criteria. For 2: find a documented deployment or benchmark at 10M+ docs with a URL, or state explicitly that none exists publicly. For 3: Typesense Cloud pricing page, compute the monthly figure for 40M docs at 2.1KB, show the arithmetic." The rework returns a real number — $2,890/mo at the required memory tier, nearly 2x OpenSearch — which flips the recommendation. Step 7: synthesis cites the three verified docs. The incomplete return, accepted as-is, would have shipped a recommendation missing the single decisive cost fact.

## Anti-patterns

- **A dispatch message containing no acceptance criteria.** The return cannot fail, so verification is impossible by construction; whatever comes back will be "done".
- **Independent tasks run serially in the transcript.** Three Task calls in sequence, no output of one feeding the next — wall-clock time tripled by habit, not by dependency.
- **A subagent's "done" accepted with no artifact inspected.** The log shows a completion claim followed immediately by synthesis; nowhere does the orchestrator open the file, run the command, or count the required fields.
- **The same model routed to every subtask regardless of difficulty.** A flagship model burning tokens on URL retrieval, or a fast model asked to adjudicate an architecture tradeoff — the transcript shows one model name across units of visibly different depth, chosen zero times.
- **A dispatch prompt that says "as discussed" or leans on context the subagent cannot see.** Guaranteed drift: the agent fills the gap with an assumption and executes it confidently.
- **A synthesis that papers over a unit's gap in the orchestrator's own voice.** A section of the final answer with no corresponding verified artifact behind it — the coordinator quietly did (or invented) a worker's job.

## Done means

- The decomposition and per-unit acceptance criteria visible in the transcript *before* the first dispatch, not reconstructed after.
- Parallel units dispatched in one batch — the log shows concurrent starts, and serial ordering exists only where a real data dependency is named.
- A routing decision per unit (model and context), stated, not defaulted — and the degenerate case is not exempt: a single-unit dispatch still names its model and context choice explicitly.
- Every return checked criterion-by-criterion, with the check visible: pass/fail per criterion, artifacts opened or commands run.
- Failed returns answered with scoped rework dispatches quoting the unmet criteria — zero silent acceptances, zero orchestrator patch-overs.
- A synthesis in which every claim traces to a verified unit artifact; anything unverified is flagged as such, not blended in.
