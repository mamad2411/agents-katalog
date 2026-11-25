---
name: create-exercises
description: Design educational assignments, practice tests, and quizzes following designated curriculum matrices, Webb's DOK 1-4, and cognitive models. Use when generating exercises, mock exams, or exam preparation materials for specific learning objectives.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code]
---

# Create Exercises

Use this skill to generate practical tasks, problem sets, and exams strictly following the educational standards, Depth of Knowledge (DOK) levels, and curriculum matrices specified for the target learners.

## When to Use

- generating practice tests, coding katas, or diagnostic quizzes
- engineering AI-resistant case studies and flawed artifacts for student debugging
- calibrating exercise sets to learner ZPD using Item Response Theory (IRT)
- mapping exercises to curriculum objectives and **Bloom 2026 AI-Age Taxonomy** (including Orchestration level)
- structuring granular partial-credit scoring matrices and answer keys

## Core Rules

- strictly adhere to the requested testing format (short quiz, unit test, mid-term, final) and target proficiency level; never use notations, formulas, or methods not yet taught in the target curriculum
- map every question to **Webb's Depth of Knowledge (DOK 1 to 4)** and **Bloom 2026 AI-Age Taxonomy**; declare target cognitive levels explicitly before generation; **Orchestration level** (above Create) required for human-AI collaboration tasks (see [`references/dok-and-ai-resistant-exercise-design.md`](references/dok-and-ai-resistant-exercise-design.md))
- implement **Cognitive Resilience Framework** (Westerbeek 2026): deliberate friction, bounded AI use, developmental window protection — exercises must scaffold the zone rather than replace learner operation within it; embed proprietary context, synthetic flaws/hallucinations for debugging, raw artifact telemetry, or oral defense prompts
- calibrate difficulty dynamically using **StanBKT Bayesian IRT** (hierarchical models, HMC/variational inference, Pathfinder, optimization) targeting a **70–80% student success moving average** across a rolling 10-item window with uncertainty quantification (see [`references/irt-calibration-and-scoring-matrices.md`](references/irt-calibration-and-scoring-matrices.md))
- award **granular partial credit** across conceptual setup (25%), execution logic (50%), and edge-case boundary verification (25%); strictly prohibit all-or-nothing scoring for constructed responses
- **AI-generated questions are drafts only**: all AI-generated exercises must pass a qualified human educator's review gate before assignment to students
- **EU AI Act High-Risk Compliance**: exercise generators classified as High-Risk (Annex III, 3a); require conformity assessment (internal Annex VI or third-party Annex VII), human oversight design (HITL/HOTL/HIC), automation bias mitigation, Article 12 record-keeping, CE marking before deployment
- keep a question-level changelog (`question_id`, `dok_level`, `bloom_2026_level`, `difficulty_param`, `irt_model_version`, `bayesian_posterior_samples`, `last_reviewed`, `human_review_status`, `conformity_assessment_ref`) for auditability

## Suggested Process

1. **Intake & Diagnostic Assessment**: Determine target subject, curriculum standards, and learner latent ability ($\theta$).
2. **Design Exercise Matrix**: Allocate items across Webb's DOK 1–4 and **Bloom 2026 (Remember, Understand, Apply, Analyze, Evaluate, Create, Orchestrate)**.
3. **Draft Cognitive Resilience Problems**: Engineer exercises with deliberate friction, bounded AI contexts, synthetic flaw injection (known LLM hallucination patterns), raw artifact telemetry, oral defense prompts.
4. **Calibrate StanBKT Parameters**: Hierarchical Bayesian inference with uncertainty quantification; model item difficulty ($\beta$) and discrimination ($\alpha$) to sustain 70–80% success in ZPD.
5. **Construct Scoring Barems**: Author granular partial-credit answer matrices (25% setup / 50% execution / 25% boundary).
6. **Human Educator Verification Gate**: Route drafted exercises for educator review and sign-off prior to student release.
7. **EU AI Act Compliance Verification**: Confirm conformity assessment, human oversight model, automation bias mitigation, record-keeping enabled.

### In-Depth Reference Guides

- **DOK & AI Resistance**: [`references/dok-and-ai-resistant-exercise-design.md`](references/dok-and-ai-resistant-exercise-design.md) — DOK 1–4 matrix, cognitive verb distribution, 5 AI-shortcut resistance archetypes, **Cognitive Resilience Framework**.
- **IRT Calibration & Scoring**: [`references/irt-calibration-and-scoring-matrices.md`](references/irt-calibration-and-scoring-matrices.md) — **StanBKT Bayesian inference** (HMC, variational, hierarchical), rolling moving average calibration, partial-credit barems, uncertainty quantification.

## Checklist

- [ ] Target grade, subject domain, and curriculum standards are verified before generation.
- [ ] Questions distributed across Webb's DOK 1–4 and **Bloom 2026 AI-Age Taxonomy (including Orchestration level)**.
- [ ] Problem prompts incorporate **Cognitive Resilience patterns**: deliberate friction, bounded AI use, developmental window protection, synthetic flaw injection with known hallucination patterns.
- [ ] Difficulty calibrated via **StanBKT Bayesian IRT** (hierarchical models, HMC/variational inference, posterior uncertainty) targeting 70–80% rolling success rate in ZPD.
- [ ] Constructed-response items have granular partial-credit scoring barems (25% setup / 50% execution / 25% boundary).
- [ ] No constructed-response items use all-or-nothing scoring.
- [ ] AI-generated exercise sets contain explicit human review gate metadata (`reviewed_by`, `verification_status`).
- [ ] **EU AI Act High-Risk metadata populated**: `ai_system_classification`, `conformity_assessment_type`, `human_oversight_model`, `automation_bias_mitigation`, `record_keeping_enabled`, `ce_marking_verified`.
- [ ] Human oversight design specified: **HITL / HOTL / HIC** per exercise type.
- [ ] **DOK-AI alignment verified**: questions survive AI tool access, multi-step reasoning required, Orchestration-level items for human-AI collaboration.
- [ ] **Adaptive exercise selection** using BKT mastery posteriors per skill.
- [ ] **Multi-modal formats**: code execution, diagram analysis, oral defense prompts, artifact debugging.
- [ ] Question-level changelog includes `irt_model_version`, `bayesian_posterior_samples`, `human_oversight_verified`, `conformity_assessment_ref`.

## Output Contracts

When the exercise set crosses a role boundary or is handed off to an LMS, tutoring engine, or teacher, emit:

- **`contracts/schemas/learning-handoff.json`** — populating `artifact_type: "exercises"`, `dok_level`, `bloom_2026_taxonomy_tier` (including Orchestration), `cognitive_resilience_mechanisms` (deliberate friction, bounded AI patterns), `stanbkt_irt_parameters` (Bayesian IRT parameters, posteriors, uncertainty quantification), `eu_ai_act_compliance` (High-Risk AI metadata), and adaptive exercise selection specifications.
- For human-readable formats, emit exercise matrix markdown with questions, DOK tags, Bloom 2026 tiers, IRT parameters, partial-credit barems, compliance metadata.
- Every AI-generated question set must record human review metadata before student assignment.

## Failure Modes

- **DOK level drift**: question's cognitive depth does not match declared DOK tier. Mitigation: verify active verbs and multi-step reasoning; reject rote questions labeled DOK 3/4.
- **AI orchestration gap**: students cannot effectively direct AI tools. Mitigation: explicit Orchestration-level exercises at Bloom 2026 Create/Evaluate level.
- **Cognitive atrophy**: over-reliance on AI erodes foundational skills. Mitigation: deliberate friction exercises with AI disabled/bounded.
- **IRT model misspecification**: wrong IRT model (1PL vs 2PL vs 3PL). Mitigation: StanBKT model comparison with posterior predictive checks.
- **EU AI Act non-compliance**: exercise generator deployed without conformity assessment. Mitigation: compliance metadata gate, CE marking verification.
- **Automation bias in grading**: educators over-trust AI exercise recommendations. Mitigation: HITL design, explicit override/stop mechanisms.
- **DOK inflation**: questions labeled DOK 3/4 but solvable by AI. Mitigation: AI-solving attempt verification before release.
- **Trivial LLM copy-paste vulnerability**: exercise solved instantly by generic AI. Mitigation: Cognitive Resilience Archetypes 1–5 (context-bound, synthetic flaw, raw telemetry, oral defense, proprietary context).

## Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: never include student personal identifiers or institutional credentials in exercise sets.
- **ASI04 Supply Chain**: validate automated test harnesses, IRT calculation modules, StanBKT inference against approved manifests.
- **ASI05 RCE Guard**: sanitize test execution environments when executing student-submitted code or tests.
- **ASI07 Inter-Agent Communication**: emit structured, schema-valid JSON contracts for all cross-role payloads.
- **ASI09 Human-Agent Trust Exploitation**: transparently declare AI provenance; require human educator sign-off; surface residual risk honestly.

## Related Skills

- **grade-and-review**: Evaluate completed exercises against 4-tier analytic rubrics and diagnose cognitive errors.
- **design-learning-plan**: Sequence exercises within broader adaptive ZPD pathways and spaced repetition schedules.

Last updated: 2026-09-25