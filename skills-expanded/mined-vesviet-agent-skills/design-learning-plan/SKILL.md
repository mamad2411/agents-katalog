---
name: design-learning-plan
description: Create a structured, curriculum-aligned learning plan or syllabus following ZPD pathways, SMART objectives, and spaced repetition. Use when planning a study schedule, syllabus, exam preparation roadmap, or grade transition plan for any educational level.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code]
---

# Design Learning Plan

Use this skill to structure personalized, adaptive study plans adhering to Vygotsky's Zone of Proximal Development (ZPD), Cognitive Load Theory, quantitative SMART learning objectives, Ebbinghaus spaced retention schedules, **Bayesian Knowledge Tracing (BKT) mastery posteriors**, and **ES-LLMs adaptive tutoring architecture**.

## When to Use

- structuring curriculum-aligned syllabi and personalized study roadmaps
- designing multi-tier ZPD pathways (Tier 1 Universal, Tier 2 Targeted, Tier 3 Intensive)
- formulating quantitatively verifiable SMART learning objectives
- scheduling spaced repetition intervals (Days 1, 3, 7, 14, 30) and Feynman checkpoints
- planning grade-transition roadmaps with 15% consolidation buffers
- **BKT-powered adaptive sequencing** driven by per-skill mastery posteriors
- **ES-LLMs orchestrator coordination** of specialized tutoring agents

## Core Rules

- always map learning plans to explicit academic calendars; budget study blocks into realistic units (45–60 min) with strict **two-dimensional cognitive load limits** (intrinsic + extraneous, max 3–5 novel interacting elements per unit)
- formulate all milestone goals as **SMART Quantitative Learning Objectives** using active **Bloom 2026 AI-Age Taxonomy** verbs (including Orchestration level for human-AI collaboration), specific operational constraints, and numerical pass criteria (see [`references/zpd-pathways-and-smart-objectives.md`](references/zpd-pathways-and-smart-objectives.md))
- implement **Adaptive Scaffolding with BKT Integration**: differentiate instructional delivery across Tier 1 (Universal Core), Tier 2 (Targeted Scaffolding with faded worked examples), Tier 3 (Intensive Extension); scaffolding intensity modulated by BKT mastery probability, fading at threshold > 0.85
- schedule review milestones using **BKT-Driven Adaptive Spacing**: Ebbinghaus intervals (Days 1, 3, 7, 14, 30) dynamically modulated by individual pForget parameter and mastery posterior decay rates (see [`references/spaced-scheduling-and-socratic-scaffolding.md`](references/spaced-scheduling-and-socratic-scaffolding.md))
- allocate a **minimum 15% dedicated consolidation buffer** for grade-transition or prerequisite remediation plans
- embed **Feynman Technique checkpoints** at review milestones: require jargon-free, layperson explanations with physical analogies to expose hidden mental model gaps
- configure automated tutoring using **ES-LLMs Architecture**: deterministic rules-based orchestrator coordinating specialized agents (tutoring, assessment, feedback, scaffolding, motivation, ethics) with constraint enforcement (attempt-before-hint, hint caps); LLM restricted to surface realization
- **Growth Mindset Integration** (evidence-based): metacognitive strategy training (+7 months EEF), specific feedback practices, safe error culture — not posters/language alone
- **Peer Learning Matching**: social features for asynchronous practice matched by BKT skill similarity
- **RAG-Enhanced Content Retrieval**: accurate contextual information for adaptive content generation with citation requirements
- **EU AI Act High-Risk Compliance**: learning plan generators classified as High-Risk (Annex III, 3a); require conformity assessment (internal Annex VI or third-party Annex VII), human oversight design (HITL/HOTL/HIC), automation bias mitigation, Article 12 record-keeping, CE marking before deployment

## Suggested Process

1. **Intake & Diagnostic Assessment**: Determine target subject, curriculum standards, and learner baseline ability ($\theta$); initialize BKT student model per skill.
2. **Formulate SMART Objectives**: Construct quantitative, verifiable learning targets using Bloom 2026 verbs including Orchestration level.
3. **Architect Adaptive ZPD Scaffolding**: Design Tier 1/2/3 materials with scaffolding intensity driven by BKT mastery posteriors.
4. **Sequence Adaptive Spaced Review**: Map study blocks with intervals modulated by BKT pForget and mastery decay.
5. **Embed Feynman & Socratic Gates**: Define simplification checkpoints; configure ES-LLMs orchestrator with 3-level hint ladder and attempt-before-hint constraint.
6. **Integrate Growth Mindset & Peer Learning**: Metacognitive strategy training, specific feedback templates, BKT-based peer matching, RAG content retrieval.
7. **EU AI Act Compliance Verification**: Confirm conformity assessment, human oversight model, automation bias mitigation, Article 12 logging.
8. **Emit Machine-Readable Contracts**: Serialize plan parameters into schema-validated JSON contracts.

### In-Depth Reference Guides

- **ZPD Pathways & SMART Objectives**: [`references/zpd-pathways-and-smart-objectives.md`](references/zpd-pathways-and-smart-objectives.md) — Multi-tier scaffolding, Cognitive Load Theory, SMART formulas, **BKT integration**.
- **Spaced Scheduling & Socratic Scaffolding**: [`references/spaced-scheduling-and-socratic-scaffolding.md`](references/spaced-scheduling-and-socratic-scaffolding.md) — Ebbinghaus decay math, 15% buffer rules, Feynman audits, 3-level hint ladders, **BKT-driven adaptive spacing**.

## Checklist

- [ ] Target grade, proficiency tier, and curriculum standards explicitly verified.
- [ ] **Two-dimensional cognitive load budgeted**: intrinsic + extraneous measured per block; max 3–5 novel interacting elements per 45-min study block.
- [ ] All learning milestones contain quantitative SMART objectives with **Bloom 2026 AI-Age verbs (including Orchestration)** and measurable benchmarks.
- [ ] **Adaptive scaffolding**: Tier 1 universal, Tier 2 faded worked examples, Tier 3 extension; intensity modulated by BKT mastery probability, fading at > 0.85 threshold.
- [ ] **BKT-driven spaced repetition**: Review intervals adapted by mastery posterior decay and pForget parameter; not fixed Days 1,3,7,14,30.
- [ ] Minimum 15% dedicated consolidation buffer allocated for grade transitions or prerequisite gaps.
- [ ] Feynman simplification checkpoints embedded at milestones with jargon-free criteria and physical analogies.
- [ ] **ES-LLMs tutoring**: Deterministic orchestrator + specialized agents (tutoring, assessment, feedback, scaffolding, motivation, ethics); constraint enforcement (attempt-before-hint, hint caps); zero-direct-answer Socratic mode.
- [ ] **Growth mindset integration**: Metacognitive strategy training (plan/monitor/evaluate), specific feedback practices, safe error culture — not posters alone.
- [ ] **Peer learning matching**: Social features for asynchronous practice matched by BKT skill similarity.
- [ ] **RAG-enhanced content**: Accurate contextual retrieval with citation requirements, verified knowledge base.
- [ ] **Multi-modal pathways**: Code, diagram, text, oral, peer-collaborative formats per learning objective.
- [ ] **EU AI Act High-Risk compliance**: Conformity assessment completed (internal Annex VI or third-party Annex VII), human oversight model (HITL/HOTL/HIC), automation bias mitigation, Article 12 automatic logging, CE marking verified.
- [ ] Structured contracts emitted: `learning-handoff.json` (capturing BKT adaptation, ES-LLMs orchestrator config, cognitive load budgets, and EU AI Act compliance).

## Output Contracts

When the learning plan is handed off to an educator, automated tutor, or LMS, emit:

- **`contracts/schemas/learning-handoff.json`** — populating `artifact_type: "learning_plan"`, `zpd_assessment`, `smart_objectives`, `formative_scaffolding_tiers`, `spaced_repetition_schedule`, `bkt_mastery_posteriors`, `es_llms_orchestrator_config`, `cognitive_load_budget`, `growth_mindset_strategies`, `peer_matching_config`, and `eu_ai_act_compliance`.
- For human-readable reports, emit markdown learning plans with timeline tables, Feynman checkpoints, graduated hint prompts, BKT mastery trajectories, cognitive load budgets.

## Failure Modes

- **Vague qualitative objectives**: goals phrased as "understand concurrency." Mitigation: enforce SMART formula with verifiable passing thresholds.
- **Cognitive overload stacking**: introducing > 5 novel concepts in a single block. Mitigation: enforce element interactivity limits; decompose into sequenced sub-schemas.
- **Omission of consolidation buffer**: grade-transition plan skips review buffer, triggering cascading failure. Mitigation: mandate 15% dedicated buffer.
- **Spaced repetition rigidity**: fixed intervals ignore individual forgetting rates. Mitigation: BKT pForget parameter drives adaptive intervals.
- **Socratic bypass**: AI tutor emits complete code solutions. Mitigation: ES-LLMs orchestrator constraint enforcement (attempt-before-hint, hint caps), prompt locking.
- **BKT model drift**: Mastery posteriors become inaccurate over time. Mitigation: StanBKT posterior predictive checks, periodic recalibration with new data.
- **Orchestrator constraint violation**: Specialized agent bypasses safety rules. Mitigation: Deterministic rules-based orchestrator with attempt-before-hint, hint caps.
- **Growth mindset superficiality**: Posters without strategy training. Mitigation: Metacognitive strategy integration, specific feedback templates, error-safe culture.
- **EU AI Act deployment gap**: Plan generator used without conformity assessment. Mitigation: Compliance gate in deployment pipeline, CE marking verification.
- **Peer matching failure**: Mismatched skill levels. Mitigation: BKT-based similarity matching, async practice design.
- **RAG hallucination in content**: Inaccurate contextual retrieval. Mitigation: Verified knowledge base, citation requirements, human review gate.

## Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: Anonymize student identifiers; store learner cognitive profiles securely; pseudonymous tokens (`STU-...`).
- **ASI04 Supply Chain**: Validate automated scheduling tools, curriculum data sources, BKT inference, RAG retrieval against trusted manifests.
- **ASI05 RCE Guard**: Never construct plan schemas or tutor instructions from unvalidated external inputs; sanitize RAG retrieval.
- **ASI07 Inter-Agent Communication**: Serialize learning plans into schema-validated JSON contracts for all cross-role payloads.
- **ASI09 Human-Agent Trust Exploitation**: Transparently communicate AI tutor boundaries; require educator sign-off; surface residual risk honestly.

## Related Skills

- **create-exercises**: Generate DOK 1–4 assignments and AI-resistant problem sets matching plan milestones.
- **grade-and-review**: Assess student work using 4-tier analytic rubrics and diagnose cognitive errors.

Last updated: 2026-09-25