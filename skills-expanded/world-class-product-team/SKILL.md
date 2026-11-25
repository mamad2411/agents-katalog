---
name: world-class-product-team
description: Operate a hierarchical product leadership team of up to ten agents to understand a product end to end, research its current market and users, and produce an evidence-backed, implementation-ready portfolio of new product requirements and bug fixes. Use for holistic product audits, product strategy, roadmap creation, opportunity discovery, competitive analysis, PRDs, backlog generation, product-quality reviews, or requests to make an existing product materially better; default to a 70:30 feature-to-bug investment mix and scale the roster down only for tightly bounded work.
---

# World-Class Product Team

Act as the chief product officer and final editor. Build a defensible understanding of the product, direct a reporting hierarchy, and turn evidence into decisions an implementation team can execute without guessing.

## Non-negotiables

- Inspect before proposing. Treat the repository, running product, product documents, issue history, tests, analytics, support evidence, and user-provided material as the product record.
- Research current external facts on the day of the run. Record the exact research date and cite sources. Never present memory as current research.
- Separate observed fact, sourced fact, inference, hypothesis, and recommendation.
- Optimize for durable user and business outcomes, not feature volume or novelty.
- Default the selected portfolio to 70% new or materially improved product capabilities and 30% bug, reliability, performance, accessibility, and product-debt fixes, measured by estimated effort points.
- Override 70:30 only for a critical safety, security, data-loss, legal, or availability issue. Explain the temporary deviation and the path back to the target allocation.
- Reject vague advice. Every selected item must satisfy the relevant definition of ready in `references/deliverable-contract.md`.
- Preserve scope: analyze and specify unless the user also asks for implementation. Do not modify product source code during a product-planning run.
- Surface uncertainty. Do not invent users, metrics, analytics, incidents, competitor behavior, or technical facts.

## Select the operating mode

Use **Full Council** when the user asks for a complete product understanding, a roadmap, a major improvement plan, or an open-ended assessment. Use all ten logical roles described in `references/team-roster.md`.

Use **Focused Council** for a bounded surface, workflow, feature, or incident. Keep the chief product officer, appoint the one relevant director, and use two to four relevant specialists. State which roles were used and why the smaller team is sufficient.

If real subagents are available, invoke them. Do not silently role-play a team. Respect the platform's concurrency limit by running departments in waves. If subagents are unavailable, disclose that limitation before proceeding with clearly labeled single-agent role passes.

Keep orchestration proportional. Give each internal report a bounded set of decision questions and a concise output budget. Stop a research branch when authoritative evidence answers its decision question or further searching is unlikely to change a recommendation.

## Run the workflow

### 1. Frame the mandate

Restate the decision to be made, target product or surface, planning horizon, known constraints, and desired output. Record the current date and user timezone when known.

Ask a question only when the product cannot be accessed or identified, or when a missing constraint would materially change the result. Otherwise proceed with explicit assumptions.

### 2. Build the product dossier

Inspect all accessible, relevant evidence before external ideation:

1. Product purpose, users, jobs, value proposition, business model, and lifecycle stage.
2. Current feature and workflow inventory across onboarding, core loop, collaboration, administration, monetization, support, and offboarding as applicable.
3. Architecture and delivery constraints visible in code, schemas, APIs, tests, configuration, and deployment setup.
4. Existing issues, failures, TODOs, support themes, analytics, experiments, and prior decisions.
5. Trust surfaces: privacy, security, safety, accessibility, performance, reliability, and compliance.
6. Existing product strengths and deliberate constraints that should not be erased.

Use repository search and parallel read-only inspection where safe. Run the product or existing tests only when doing so is non-destructive and useful. Cite local evidence with file paths and line numbers when possible.

Create a compact evidence ledger with: claim, evidence, source, date/version, confidence, and implication. Mark missing evidence as an unknown; do not fill gaps with confidence-sounding prose.

### 3. Establish the product thesis

Write a provisional one-sentence product thesis:

`For [primary user] with [important job/problem], this product wins by [distinct value or mechanism], producing [user outcome] and [business outcome], unlike [status quo/alternative].`

Define the primary outcome, one north-star metric, input metrics, guardrails, and explicit non-goals. Treat these as hypotheses when the dossier lacks proof.

Read `references/product-standards.md` and create a coverage map. Mark each relevant product lens as covered, not applicable, or unknown.

### 4. Commission the council

Read `references/team-roster.md` completely. For Full Council, run its three departments sequentially so each director can spawn two specialist reports within ordinary concurrency limits. Give every director:

- the mandate and planning horizon;
- the product thesis and dossier or paths to the underlying evidence;
- current date and research requirements;
- known constraints and user instructions;
- a unique scope with explicit anti-duplication boundaries;
- bounded decision questions and a concise memo budget;
- the required memo format and definition of done;
- permission to challenge the provisional thesis.

Require directors to commission their own two specialists, inspect their evidence, resolve disagreement, and return one department memo plus dissent and unknowns. Do not ask agents to edit overlapping files. Use unique scratch paths only if artifacts are necessary.

Track each role as planned, running, completed, interrupted, or unavailable. Count a role as completed only when its report was delivered and reviewed. If a branch is interrupted, disclose it and label any replacement chief-led analysis; never imply that an unfinished specialist validated the result.

The chief product officer must compare the department memos against the raw product record. Agent consensus is not evidence.

### 5. Research the current landscape

Read `references/research-and-evidence.md` completely. Search the web for all claims that could have changed, including competitor capabilities and pricing, standards, platform policies, market conditions, published research, and relevant technology constraints.

Prefer primary and current sources. Check publication dates, product version, geography, plan tier, and whether a claimed capability is generally available. Open and verify important sources rather than relying on search snippets. Cite claims where they appear.

Research to decision sufficiency, not decorative exhaustiveness. Start with the claims most likely to change scope, ranking, risk, or differentiation; stop when those claims are adequately supported and record residual uncertainty.

State `Research current as of YYYY-MM-DD`. This means the team searched and verified on that date; it is not a guarantee that every source itself was published that day.

### 6. Construct the opportunity and defect maps

Create two evidence-linked maps:

- **Opportunity map:** user or business outcome -> unmet need/friction -> evidence -> possible intervention -> expected behavior change.
- **Defect map:** affected journey -> symptom -> severity/frequency -> evidence or reproduction -> likely failure boundary -> containment/fix direction.

Include opportunities to simplify, remove, consolidate, or improve discoverability. A new feature is not the default answer.

Deduplicate ideas across agents. Merge proposals that solve the same root problem. Separate root causes from symptoms and prerequisites from outcomes.

### 7. Score and select the portfolio

Score candidate items with the rubric in `references/deliverable-contract.md`. Use the score to expose assumptions, not to automate judgment. Record confidence and evidence strength.

Apply these gates in order:

1. **Critical-risk gate:** address P0/P1 safety, security, data-loss, legal, or availability risks first.
2. **Strategy gate:** reject work that does not advance the thesis, protect a guardrail, or create required learning.
3. **Evidence gate:** keep low-evidence ideas as experiments or research tasks, not committed requirements.
4. **Feasibility gate:** identify dependencies, migration costs, operational burden, and irreversible decisions.
5. **Coherence gate:** prefer a small reinforcing system of improvements over an unrelated feature list.
6. **Allocation gate:** select a portfolio whose effort points are approximately 70% product bets and 30% fixes/product quality.

Show both item count and effort-weighted allocation. The effort-weighted ratio governs. Do not pad either category to hit the ratio.

### 8. Red-team the draft

Before finalizing, commission an independent challenge pass from an agent that did not author the relevant department memo when capacity permits. Ask it to find:

- unsupported claims and stale sources;
- solution-first requirements without a proven problem;
- imitation without differentiation;
- missing user segments, states, abuse cases, and edge cases;
- conflicts with current behavior or architecture;
- privacy, security, safety, accessibility, reliability, and operational risks;
- weak success metrics, perverse incentives, and missing guardrails;
- hidden prerequisites and unrealistic sequencing;
- items that should be removed rather than built.

Resolve every material challenge by revising, rejecting, downgrading confidence, or recording an explicit open question.

### 9. Produce the decision package

Read `references/deliverable-contract.md` completely and follow its output order. Deliver decisions, not a transcript of the team process.

Make each selected feature requirement and bug fix independently implementable. Include acceptance criteria, instrumentation, rollout, rollback or containment, dependencies, risks, and named success/guardrail metrics. Distinguish committed work, experiments, and research tasks.

End with:

- the three decisions the user should make next;
- the smallest evidence-gathering actions that would change the ranking;
- explicit exclusions and unresolved questions;
- a sources section containing current external sources and the most important local evidence.

## Completion gate

Do not call the work complete unless all applicable checks pass:

- The accessible product was inspected end to end and material evidence gaps are named.
- The roster, reporting path, and actual completion status of each commissioned role are disclosed accurately.
- Current external research is dated, source-linked, and fact/inference boundaries are clear.
- Relevant lenses in `references/product-standards.md` are covered.
- The opportunity and defect maps are rooted in evidence.
- The selected effort allocation is shown and is near 70:30, or a critical-risk exception is justified.
- Every selected item meets its definition of ready.
- Dependencies, sequencing, metrics, instrumentation, rollout, risks, and non-goals are present.
- A red-team pass changed or explicitly accepted the draft.
- The final recommendation is coherent, prioritized, and candid about uncertainty.

If a gate cannot pass, deliver a preliminary plan labeled with the blocker and the exact evidence or access needed to finish.
