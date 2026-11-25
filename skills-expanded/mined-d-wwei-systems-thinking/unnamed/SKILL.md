---
name: 系统性思考
description: "系统性思考——看到反馈循环、涌现、杠杆点的系统性视野。"
---

# Systems Thinking

A cognitive base that shifts reasoning from linear cause-effect chains to feedback-driven structural analysis.

Not tied to any domain — applies equally to engineering, business, personal decisions, and policy analysis. Stacks with any domain skill. Core rules live in `cognitive-protocol.md` (~30 lines, always-on). This file is the full reference framework.

---

## 1. Cognitive Shifts

### Shift 1: Events → Structure

Default: React to events ("sales dropped," "the deploy broke," "a competitor launched"). Ask "what happened?" and propose a fix for that specific event.

Target: Ask "what structure produces events like this?" Identify the feedback loop, stock/flow dynamic, or archetype that generates the event repeatedly. Fix the structure, not the instance.

- When the user reports a problem, resist jumping to solutions. First ask: what pattern is this event part of? What structure would keep producing this pattern even if the current actors changed?
- Map at least one level deeper than the presenting problem before proposing an intervention.

### Shift 2: Linear Causality → Circular Causality

Default: Trace A → B → C → D in a straight line. Treat the last item as the "root cause" or the first item as the "fix."

Target: Look for where D feeds back to influence A. If a loop exists, the behavior of the system is qualitatively different from a chain — it self-reinforces or self-corrects.

- For every causal chain longer than 3 links, explicitly check: does the end feed back to the beginning?
- If no loop exists, state it: "This is a linear chain, not a systemic structure." That is a valid finding.
- If a loop exists, classify it: reinforcing (amplifies deviation) or balancing (resists deviation).

### Shift 3: Snapshots → Dynamics

Default: Describe the current state. "Revenue is $X." "Team size is Y." "Customer satisfaction is Z." Treat these as static facts.

Target: Distinguish stocks (things that accumulate) from flows (rates of change). Ask: what is the inflow? What is the outflow? How long does it take for a change in flow to visibly move the stock?

- Every quantity has a time dimension. Name it: is this growing, shrinking, oscillating, or in equilibrium?
- Estimate delays between intervention and visible effect. Interventions without delay estimates are guesses.

### Shift 4: Implicit Boundaries → Explicit Boundaries

Default: Analyze "the problem" without stating what is inside and outside the scope of analysis. Unconsciously inherit the boundary from the problem statement.

Target: Consciously draw the system boundary. Name what you are including, what you are excluding, and what changes if the boundary shifts.

- The boundary is a design choice, not a fact. Different boundaries reveal different structures.
- Too narrow: you treat your own consequences as external events. Too wide: nothing is actionable.

### Shift 5: Parameters → Leverage Hierarchy

Default: Propose interventions at the most accessible level — change a number, adjust a setting, add a resource.

Target: Before recommending, classify the intervention on Meadows' hierarchy. Ask whether a higher-tier intervention exists that would be more effective per unit of effort.

- Parameters (numbers, budgets, headcount) are the weakest levers. Information flows, rules, goals, and paradigms are progressively stronger.
- The counterintuitive trap: people find leverage points intuitively but push them in the wrong direction. Always state your direction and why the reverse is wrong.

---

## 2. Information Filter

### FEEDBACK SIGNALS — Trace and classify

Any information suggesting circular causality: "the more we do X, the more Y happens, which makes us do more X." Immediately classify as reinforcing or balancing loop. Map the full cycle. Identify what would break or strengthen the loop.

### ACCUMULATION SIGNALS — Distinguish stock from flow

Any quantity that "increases" or "decreases." Before acting on it, determine: is the stock changing, or is the flow rate changing? A rising stock with a decreasing inflow is about to plateau. A stable stock with rising outflow is about to collapse. The trajectory matters more than the current level.

### DELAY SIGNALS — Estimate and flag

Any situation where an action was taken and "nothing happened" or where effects appeared "suddenly." Check for delays. Map the delay chain: perception delay → response delay → delivery delay. If total delay exceeds the decision cycle, the system will oscillate — flag this explicitly.

### BOUNDARY SIGNALS — Test and adjust

Any claim about "the cause" of a problem. Ask: is this cause inside or outside the system boundary? If outside, either widen the boundary to include it or acknowledge it as an exogenous constraint. If inside, trace it further — is it part of a loop?

### EMERGENCE SIGNALS — Recognize and resist decomposition

Any property that exists at the system level but not in any component: culture, morale, market dynamics, traffic patterns. Do not look for "which part causes this." Instead, identify which interaction pattern produces it. The fix is in the pattern of connection, not in any single node.

---

## 3. Anti-Pattern Checklist

### 1. Factor Listing
Listing causes without causal arrows. "The problem is caused by A, B, C, D, and E." → Rewrite: draw directed connections between factors. Which influences which? Do any form loops?

### 2. Hollow Holism
Saying "it's all connected" or "we need a holistic approach" without specifying mechanisms. → Rewrite: connected HOW? Through what mechanism? With what delay? Reinforcing or balancing?

### 3. Chain Masquerade
Presenting a linear causal chain (A→B→C→D) as "systems thinking" by adding the word "systemic." → Rewrite: check for feedback. If D does not feed back to A, call it a chain and analyze accordingly.

### 4. Boundary Inflation
Expanding the system boundary until it includes everything ("to really solve this we need to change society"). → Rewrite: narrow to what you can influence within the relevant time horizon.

### 5. Map-as-Insight
Drawing an elaborate causal loop diagram and treating the diagram itself as the conclusion. → Rewrite: from this map, name the dominant loop, the highest-leverage intervention, and the predicted behavior over time.

### 6. Delay Blindness
Evaluating an intervention's success before the system's characteristic delay has elapsed. → Rewrite: state the expected delay and when results should become visible.

### 7. Leverage Inversion
Finding the right leverage point but pushing it in the wrong direction. → Rewrite: state both directions, explain which is correct, and why intuition might favor the wrong one.

### 8. Vocabulary Compliance
Using systems-thinking words (feedback, emergence, leverage, nonlinear) without performing the corresponding cognitive operations. → Rewrite: for each term used, show the specific work. "Feedback loop" requires naming the loop. "Emergence" requires identifying the interaction pattern. "Leverage" requires placing the intervention on the hierarchy.

---

## 4. Composing with Domain Skills

### Composition principles

1. **Systems thinking is the structural layer; domain skills provide content.** When analyzing a codebase, domain skill says what functions do; systems thinking asks how they interact, where feedback loops exist, and where delays cause problems.
2. **Activate systems thinking when the problem involves interaction effects.** If a problem is purely about one component in isolation, systems thinking adds overhead without value. If two or more components interact and produce unexpected behavior, systems thinking is the right lens.
3. **Systems thinking does not replace domain expertise.** It cannot tell you what the correct parameter value is — only whether changing parameters is the right tier of intervention.

### Stacking examples

- **With coding skill**: Before refactoring, map the dependency feedback loops. Which modules have circular dependencies? Which changes propagate through the system? Where are the delays (build times, deployment cycles) that affect developer behavior?
- **With business/strategy skill**: Before setting goals, identify the dominant reinforcing and balancing loops in the business model. Which loop is currently dominant? What would shift dominance? Where is the leverage — in the product, the distribution, the pricing, or the paradigm?
- **With writing skill**: When explaining a complex topic, structure the explanation around feedback loops rather than linear sequences. Show the reader how the system behaves over time, not just what it looks like now.
- **Standalone**: When the user asks "why does X keep happening?" — this is a structural question. Map the loop that reproduces X. Find what sustains it.

### Relationship to Tacit Knowledge

**Complementary, different axis.** Tacit Knowledge governs output quality — judgment-first, information hierarchy, insider perspective. Systems thinking governs causal reasoning — feedback loops, stocks/flows, delays, leverage. They stack without conflict:
- Tacit Knowledge ensures the ANSWER is sharp and actionable.
- Systems thinking ensures the ANALYSIS behind the answer captures structural dynamics.
- Load order: Tacit Knowledge first (it shapes all output), Systems Thinking second (it shapes the reasoning that produces the output).
- Combined effect: responses that lead with structural diagnosis (systems thinking) expressed as sharp, judgment-first output (tacit knowledge).

### Relationship to First Principles

**Complementary, sequential.** First Principles decomposes to verified atoms. Systems Thinking maps how those atoms interact. Use First Principles to verify components are sound, then Systems Thinking to check that their assembly produces the desired behavior. First Principles without Systems Thinking: correct parts, bad interactions. Systems Thinking without First Principles: elegant structure built on unexamined assumptions.

### Relationship to Cross-Domain Connector

**Reinforcing, overlapping.** Cross-Domain Connector extracts abstract structures and scans other fields. Systems Thinking provides a specific vocabulary for dynamic structures (feedback loops, archetypes, leverage points). When CDC identifies an abstract structure, Systems Thinking can often name the specific archetype and predict its behavior.

---

## 5. Intensity Calibration

### Full intensity — Diagnosing recurring problems, policy design, organizational change

Map all feedback loops. Classify stocks and flows. Estimate delays. Draw explicit boundaries. Identify leverage tier. Check for archetype matches. Predict behavior over time.

### Medium intensity — Technical decisions, product strategy, planning

Identify the dominant feedback loop. Check for delays between intervention and effect. Classify the proposed intervention on the leverage hierarchy. Skip full stock/flow mapping unless quantities are central to the decision.

### Low intensity — Quick questions, single-component issues, well-bounded tasks

Check whether feedback loops are relevant. If the problem is genuinely linear and single-component, say so and proceed without systems framing. Don't force loop-finding on problems that don't have loops.

---

## 6. Extended Layer

The core protocol (`cognitive-protocol.md`) covers feedback loops, stocks/flows, delays, boundaries, and leverage hierarchy. The extended protocol (`extended-protocol.md`) adds six capabilities that the core does not cover. It is loaded on demand for deeper analysis — not always-on.

### What the extended layer adds

The core protocol operates **within** a systems paradigm. The extended layer operates **on** the paradigm — it questions the analysis itself, detects qualitative transformations, and handles situations where systems modeling is the wrong tool.

### Source traditions

The extended protocol synthesizes insights from three traditions, stripped of theory names and converted to operational instructions:

**Dialectical analysis** (Mao Zedong's 《矛盾论》and 《实践论》): contributed the concepts of principal contradiction (the dominant tension driving a system's evolution), principal aspect (which side of a tension determines the system's nature), antagonistic vs non-antagonistic tensions, phase/stage diagnosis, and practice-theory verification. Key difference from core protocol: feedback loops are mechanisms; contradictions are engines of qualitative transformation.

**Eastern epistemology** (Buddhist 缘起性空, Daoist 无为/反/阴阳): contributed reification detection (noticing when a process is treated as a fixed entity), observer inclusion (the analyst is part of the system), framework transcendence (holding frameworks without attachment), wu-wei intervention (removing obstacles instead of applying force), reversal anticipation (trends contain seeds of their opposite), over-optimization detection, and emptiness-as-generative (analyzing spaces between components). Key difference: the core protocol treats system components as having stable identities; these traditions question whether identities exist independently of relationships.

**Cross-domain systems theory** (Cynefin/Snowden, Panarchy/Holling, Normal Accidents/Perrow, Goodhart's Law, Legibility/Scott, Minsky Hypothesis, Ecological Rationality/Gigerenzer, Safety-II/Hollnagel, Phase Transitions, Schelling's Micromotives): contributed meta-domain diagnosis (when NOT to use systems thinking), adaptive lifecycle phases, architectural impossibility detection, metric corruption detection, legibility-as-damage, stability-as-fragility-incubator, and knowing when less analysis outperforms more.

### Extended anti-patterns

Five additional anti-patterns are documented in `anti-patterns.md` (patterns 9-13), covering failures specific to the extended layer: Template Application, Stability Blindness, Force-First Intervention, Analysis-as-Avoidance, and Metric Corruption.

### When to load the extended layer

- **Always load** for: organizational change, policy design, multi-stakeholder conflicts, situations where previous systems analyses failed
- **Optionally load** for: recurring problems that resist structural intervention, situations involving qualitative transformation or phase shifts
- **Skip** for: standard technical problems, well-bounded systems, situations where the core protocol is sufficient

### Intensity calibration (extended)

**Full extended**: Run all six extended sections. Used when core-protocol analysis produces unsatisfying or circular results — a signal that the gaps the extended layer fills are relevant.

**Selective**: Load only the section relevant to the current gap. "Diagnose before modeling" for uncertain situations. "Find the driving tension" for multi-conflict situations. "Audit the analysis itself" after completing any deep analysis.