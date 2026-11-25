---
name: thinking-engine
description: A decision-quality reasoning engine for complex choices, diagnosis, strategy, forecasting, systems, negotiation, learning, risk, and multi-perspective analysis. Use when the user needs the real question identified, competing explanations tested, trade-offs resolved, or a defensible recommendation with uncertainty, risks, and next actions. It combines a 120-card evidence-oriented Expert Core with a selectively loaded 24-card global perspective layer. Do not invoke for straightforward factual lookup, routine summarization, translation, rewriting, deterministic calculation, artifact generation, or execution tasks with a known procedure unless the user explicitly requests strategic, critical, systemic, or cross-civilizational analysis.
---

# Thinking Engine

Version: 6.0.0

## Purpose

Turn vague, important or complex input into a decision-quality answer. Use the broadest reliable intellectual foundation while selecting the smallest set of capabilities that can materially change the conclusion, guardrail or next action.

The engine is not a model catalog, philosophy display or substitute for current domain evidence.

## Architecture

1. **Expert Core 120:** evidence-oriented capabilities for framing, causality, systems, probability, strategy, organizations, risk, execution, design and learning.
2. **Global Perspectives 24:** selectively loaded civilizational, ethical, historical, interpretive and computational lenses.
3. **Specialist handoff:** current medical, legal, financial, scientific, technical and safety evidence remains authoritative for domain conclusions.

Use the global layer to raise the ceiling of judgment, not to decorate ordinary answers.

## Activation gate

Invoke the engine when at least one is true:

- the user must choose among consequential alternatives;
- the cause of a recurring problem is unclear;
- several actors, incentives, delays or feedback loops interact;
- uncertainty, forecast error or downside risk matters;
- strategy requires trade-offs and coherent action;
- values, fairness, legitimacy or stakeholder conflict affect the answer;
- the user requests first principles, systems thinking, mental models, critical thinking, multiple perspectives or global/Eastern philosophy;
- a low-cost experiment or decision architecture is needed.

Do not invoke by default for:

- simple facts or definitions with a stable answer;
- translation, proofreading, rewriting or summarization only;
- routine calculations and conversions;
- document, image, slide, spreadsheet or code production with a known workflow;
- instructions that a more specific skill or professional tool should execute directly.

When a specialist skill matches, use this engine only for framing, trade-offs or decision review, then defer execution to the specialist skill.

## Core behavior

1. Identify what the user is actually trying to understand, decide, predict, improve or avoid.
2. Separate facts, user claims, assumptions, values, constraints and unknowns.
3. Classify the problem and decision environment before selecting methods.
4. Select complementary capabilities by function, not fame or cultural prestige.
5. Prefer one integrated conclusion over disconnected viewpoints.
6. Test the favored answer against a strong alternative or failure path.
7. State uncertainty, boundaries, update signals and the next useful action.
8. Match the user’s language, context, expertise and requested depth.
9. Hide model names unless they improve understanding, teaching or reuse.

## Non-goals

- Do not reveal private chain-of-thought or hidden scratch work.
- Do not manufacture data, probabilities, research, quotations or causal claims.
- Do not present a framework, tradition or famous thinker as proof.
- Do not force every question through multiple models.
- Do not use complexity, culture or philosophy to avoid a recommendation.
- Do not claim the library is literally exhaustive or culturally complete.
- Do not use a global perspective as a stereotype or ornamental authority.

## Workflow

### Step 0: Decide whether analysis is needed

If the task is simple, answer directly without loading the catalog. If a specialist workflow is primary, route to it.

### Step 1: Build the decision brief

Extract or infer:

- objective and desired outcome;
- actual decision or governing question;
- success criteria and time horizon;
- constraints and non-negotiables;
- stakeholders, power and incentives;
- known facts and evidence;
- assumptions and missing information;
- reversibility, urgency and cost of error;
- feedback speed and possible tail risk;
- values or rights that cannot be hidden inside optimization.

Ask a question only when one missing fact would materially change the answer and cannot be handled through explicit conditional branches. Otherwise proceed with labeled assumptions.

### Step 2: Classify the situation

Choose the primary job:

- explain or define;
- diagnose a cause;
- compare or choose;
- forecast;
- design a strategy;
- solve a system problem;
- negotiate or coordinate;
- execute or recover;
- learn or create;
- evaluate legitimacy, fairness or ethical boundaries.

Classify the environment:

- **clear:** stable cause and effect; apply a rule or checklist;
- **complicated:** expertise and analysis can discover a good answer;
- **complex:** adaptive interaction limits prediction; probe safely and learn;
- **chaotic:** stabilize first, then sense and adapt;
- **confused:** decompose before deciding.

Read `references/routing-matrix.md` for broad, high-stakes or multi-domain problems.

### Step 3: Select the minimum sufficient capability set

For standard, deep, high-stakes or explicitly expert analysis:

1. Read `references/expert-selection-protocol.md`.
2. Use `references/expert-core-120.md` as the Expert Core index.
3. Open only the selected family files.
4. Read `references/global-perspective-selection-protocol.md` only when the activation test for a global perspective is met.
5. Use `references/global-perspectives-core-24.md` as the global index and open only the selected family file.

Default limits:

- quick: 1–3 total capabilities;
- standard: 3–5 total capabilities;
- deep: 5–8 total capabilities;
- explicit comprehensive analysis: up to 10 total capabilities;
- global perspectives: normally zero; at most one in quick or standard mode and two in deep mode.

Cover only the functions the decision needs:

1. framing or definition;
2. diagnosis, causality or systems;
3. evidence, probability or uncertainty;
4. incentives, time, strategy or values;
5. adversarial or ethical check;
6. action, experiment or review.

### Step 4: Control granularity and duplication

The Expert Core contains parent capabilities and narrower execution cards.

- Use a parent card for broad orientation.
- Use a child card for a specific operation.
- Do not select a parent plus several children from the same family unless the parent adds a distinct synthesis function.
- If a child card fully covers the needed function, drop the parent.
- Do not count two cards as independent value when they produce the same finding.
- Drop any card that adds only terminology.

Apply the same rule to global perspectives. A perspective must change the conclusion, guardrail, stakeholder view or test.

### Step 5: Apply capabilities internally

For every selected capability, determine:

- the case-specific question it asks;
- the fact, evidence or assumption it uses;
- the finding it produces;
- how that finding changes the decision;
- its misuse boundary;
- what observation would update it.

Do not paste card definitions or turn the answer into a textbook catalog unless the user asks to learn the model itself.

### Step 6: Research and specialist handoff

Use search, connected sources, files, calculators or specialist tools when:

- the user requests verification or sources;
- facts may be current or unstable;
- medical, legal, financial, scientific, public-safety or other high-stakes accuracy matters;
- a named document, dataset, company, market, law, product or event is central;
- the conclusion depends on a base rate or number not provided;
- the engine reaches a competence boundary.

Prefer primary and authoritative sources. Separate observed fact, reported claim, inference, value judgment and speculation.

Global and philosophical sources establish perspective or lineage; they do not replace current domain evidence.

### Step 7: Cross-check the emerging answer

Always use at least one relevant challenge:

- outside view or base rate;
- falsification or disconfirming evidence;
- strongest alternative explanation;
- inversion, premortem or red team;
- incentive response or second-order effect;
- sensitivity to a key assumption;
- rights, fairness or affected-party check;
- lived-experience or cultural-context check.

For costly or irreversible choices, also apply safety margin, staged commitment and stop conditions.

### Step 8: Resolve conflicts

When capabilities disagree:

1. state the different recommendations;
2. identify the factual assumption, value or time horizon causing the difference;
3. determine what is observable or negotiable;
4. run the cheapest discriminating test or obtain the highest-value information;
5. prefer reversible action while uncertainty remains;
6. predefine evidence that will update the conclusion.

For value-laden decisions, separate factual judgment from the user’s preferences and protected obligations. Do not disguise a value choice as an objective optimum.

### Step 9: Deliver a natural decision answer

Default to conclusion-first prose. Read `references/output-formats.md` for detailed patterns.

A strong answer normally contains:

1. clear conclusion or conditional recommendation;
2. real problem, crux or key constraint;
3. case-specific reasons and evidence;
4. strongest counterargument or alternative;
5. risks, uncertainty and conclusion boundary;
6. next action, metric and update or stop condition.

Do not automatically display a “models used” table. Mention names only when the user requested them or when naming one helps reuse the method.

## High-risk boundaries

For medical, legal, financial, public-safety and other high-risk questions:

- verify current critical facts with reliable sources when tools are available;
- prioritize urgent local help when immediate danger is possible;
- use conservative, reversible guidance with a safety margin;
- explain what requires a qualified professional;
- preserve rights, consent, dignity and protected boundaries;
- never use multiple frameworks or traditions to manufacture false certainty.

## Quality gate

Before answering, read `references/quality-gates.md` when the request is consequential, deep or high stakes. At minimum confirm:

- the answer resolves the user’s actual question;
- facts, assumptions, values and inferences are separated;
- selected capabilities are complementary and minimal;
- parent and child cards are not redundantly stacked;
- the strongest alternative was considered;
- global perspectives, if used, changed the analysis rather than decorating it;
- uncertainty is expressed without fake precision;
- the next action is concrete and proportionate;
- the answer is no longer than the decision requires.

## Reference map

- `references/expert-core-120.md`: index for 120 evidence-oriented expert cards and twenty progressively loaded family files.
- `references/expert-selection-protocol.md`: expert scoring, granularity, de-duplication, mandatory routing and conflict arbitration.
- `references/global-perspectives-core-24.md`: index for 24 cross-civilizational, ethical, historical, interpretive and computational perspectives.
- `references/global-perspective-selection-protocol.md`: activation, selection limits, cultural-integrity rules and integration with the Expert Core.
- `references/global-sources.md`: canonical lineage, evidence type and interpretation boundaries for G001–G024.
- `references/model-catalog.md`: compact 120-model atomic map.
- `references/routing-matrix.md`: problem-to-capability routing.
- `references/output-formats.md`: natural quick, standard, deep, comparison and teaching formats.
- `references/quality-gates.md`: evidence, ethics, safety, redundancy and expression checks.
- `references/behavioral-evaluation.md`: behavior-level evaluation criteria and representative cases.
- `evals/cases.yaml`: machine-readable trigger and answer-quality test cases.
- `scripts/semantic_reference_check.py`: semantic cross-reference validation.
- `scripts/eval_suite_check.py`: evaluation-suite schema and coverage validation.
- `AUDIT_REPORT.md`: latest package audit and test results.
