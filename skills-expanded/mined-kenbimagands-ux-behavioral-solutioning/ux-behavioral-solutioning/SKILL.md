---
name: ux-behavioral-solutioning
description: Analyze user-provided customer/user journey maps, extract evidence-backed pain points, match relevant Magic Cards using hybrid behavioral reasoning, generate concrete UX design/tool interventions, and justify each intervention's functional position in the AAARRR Pirate Funnel. Use for UX research synthesis, journey-map solutioning, behavioral design ideation, and funnel positioning.
---

# UX-Behavioral-Solutioning

## Purpose
Turn a provided Customer Journey Map (CJM) or User Journey Map (UJM) into traceable, actionable UX interventions grounded in behavioral reasoning, then explain **how each intervention implements or supports a Pirate Funnel function**. Funnel positioning is a justification tool for researchers, **not a performance forecast**.

**Workflow:** Journey analysis → pain point extraction → hybrid Magic Card matching → actionable UX solutioning → functional AAARRR positioning.

## Reference files
- `references/magic-cards-knowledge-base.md`: supplied Magic Card definitions, mechanisms, and UX applications.
- `references/pirate-funnel-knowledge-base.md`: supplied six-stage AAARRR reference (Awareness, Acquisition, Activation, Retention, Revenue, Referral).
- `assets/solutioning-template.md`: expected deliverable.

Read both knowledge bases before matching or positioning. The card reference includes interpretive explanations and examples; do not treat inclusion as empirical proof or infer that a user exhibits a bias solely from a pain point.

## Phase 1 — Read and understand the journey
1. Accept journey maps in text, images, tables, documents, or structured notes; inspect the actual input before reasoning.
2. Extract the user's own journey stages, goals, actions, touchpoints, thoughts/feelings, and stated pain points, where available.
3. Preserve original journey order and terminology. Do **not** assume a proposed feature or referral program already exists.
4. Identify essential missing context (product, user segment, task, existing capabilities); ask only if the map cannot be interpreted without it. Otherwise mark gaps and proceed.
5. Separate **explicit map evidence**, **reasonable inference**, and **unknown**. Do not invent quotes, metrics, emotions, or behaviors.

## Phase 2 — Extract pain points
1. Extract each distinct friction or unmet need, retaining a pointer to its journey stage and original evidence.
2. For each pain point record: ID, stage/touchpoint, user action or goal, pain point, evidence, evidence status, and a **hypothesized** cause if warranted.
3. Distinguish observed symptom from pain point and from causal hypothesis. Avoid psychologizing operational, technical, or accessibility issues.
4. Merge true duplicates but do not merge unrelated frictions. If the input already contains pain points, preserve them before offering a normalized formulation.
5. Optionally flag important pain points for attention based on severity, task blockage, and evidence strength. Never invent numeric priority scores.

## Phase 3 — Hybrid behavioral matching
**Problem-first diagnosis followed by principle-driven exploration.**

For each pain point:
1. Describe the problem and plausible mechanisms **without** Magic Card labels.
2. Search the Magic Cards reference for candidates whose **behavioral mechanism**, not merely their title, fits the problem.
3. Explore alternate cards that illuminate different mechanisms or solution directions.
4. Evaluate each candidate on **behavioral relevance**, **evidence alignment**, and **solution potential** (qualitative high/medium/low with a short explanation).
5. Identify the **primary explanatory card** where supported, and optionally **supporting / solution-oriented cards**. A card that explains the problem and a card that informs the design can be different.
6. Name alternative explanations and uncertainty. If none fits, write **No suitable Magic Card match** and continue with ordinary UX reasoning.
7. Avoid redundant card stacking and false claims of causal or scientific validation.

## Phase 4 — Concrete UX solutioning
For each pain point generate **2–3 meaningfully different alternatives** when feasible, and recommend one with a short reason. Do not manufacture alternatives when only one sensible option exists.

**Required solution statement syntax:**
> **Add / Modify / Implement a [specific design component, feature, or tool] that [does a specific action] to support [user need or behavioral objective].**

Rules:
- Start with an implementation verb: **Add, Modify, Implement, Introduce, Integrate, Provide**.
- Name an identifiable UI component, interaction, tool, or service touchpoint; specify what it does **in this journey** and why.
- Prefer modifying an existing component when that better addresses the pain point; do not assume greenfield development.
- Ground each alternative in its Magic Card mechanism (or clear non-card UX reasoning); do not leap from a broad pain point to a generic tooltip.
- Distinguish proposed solutions from existing product features.
- Avoid vague statements like “improve engagement” or “make navigation intuitive.”
- Explain the recommendation through problem fit, behavioral fit, user value, and plausible feasibility. Mark unknown feasibility as unknown.
- Do not use deceptive scarcity, coercive nudges, hidden consent, or other dark patterns.

## Phase 5 — Pirate Funnel functional positioning
**Purpose: help UX researchers justify and position their design action.** This phase does not predict impact, require KPIs, or prioritize solutions by growth.

For **each proposed solution**:
1. Inspect the feature's **actual intended functionality** and the user action it enables.
2. Match it to **one primary** AAARRR function using the supplied Pirate Funnel reference:
   - **Awareness:** make potential users aware of the product or service.
   - **Acquisition:** help interested people begin engaging with or entering the product.
   - **Activation:** help users reach meaningful initial value.
   - **Retention:** help users return and continue deriving value.
   - **Revenue:** support purchasing, upgrading, or another revenue-generating action.
   - **Referral:** enable voluntary recommendation or invitation.
3. Write a **functional justification** of 1–2 sentences: **how the proposed design/tool performs or supports that funnel function**.
4. Add a secondary stage only if its distinct functional link is clear. If no direct fit exists, write **Indirect / unclear AAARRR relationship**.
5. Do not equate a journey-map stage with a funnel stage. Do not claim a solution *will increase* conversion, retention, or revenue; such outcomes require validation.

**Required Phase 5 columns:** `UX Solution | Pirate Funnel Function | Functional Justification`.

## Output
Use `assets/solutioning-template.md`. Preserve traceability with pain point IDs and solution IDs. The final output should clearly show:
- What the user experienced (evidence)
- What problem is being addressed (pain point)
- Why a behavioral principle is relevant (and any uncertainty)
- What **specific design/tool** should be added or modified, how it works, and why
- How that solution **implements/supports** a Pirate Funnel function

## Final quality checks
- Every extracted pain point links to the actual map; inferred items are labeled.
- Card matching relies on mechanisms rather than superficial keywords.
- Explanatory and solution-oriented cards are not conflated.
- Every solution uses the actionable statement format and is specific to the journey.
- Multiple alternatives are substantively different; recommendation is explained.
- Every AAARRR justification describes a **function**, not a speculative metric lift.
- No proposed feature is misrepresented as already existing.
