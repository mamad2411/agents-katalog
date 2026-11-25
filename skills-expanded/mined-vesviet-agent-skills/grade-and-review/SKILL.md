---
name: grade-and-review
description: Evaluate learner work and provide constructive feedback on the designated grading scale. Use when grading assignments, reviewing student submissions, or providing improvement guidance at any educational level.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code]
---

# Grade And Review

Use this skill to evaluate student submissions against **BKT-informed 4-tier criterion-referenced rubrics**, eliminate AI grading hallucinations via verifiable line citations and executable verification, diagnose cognitive error categories (including AI-mediated errors), and deliver evidence-based growth-mindset feedback enforcing the Rule of One with Socratic hint ladder.

## When to Use

- evaluating student exercises, code repositories, or open-ended design submissions
- grading against **BKT-weighted 4-tier analytic rubrics** (Beginning, Developing, Proficient, Advanced)
- diagnosing cognitive failure modes (conceptual vs procedural vs boundary vs overload vs **AI-mediated**)
- authoring **evidence-based growth-mindset feedback** using "not-yet" framing + metacognitive strategy training
- emitting verified machine-readable assessment contracts under **EU AI Act High-Risk AI Governance** (Annex III, 3a)

## Core Rules

- score submissions using **BKT-Informed 4-Tier Criterion-Referenced Rubrics** (Beginning 0–49%, Developing 50–69%, Proficient 70–89%, Advanced 90–100%) with mastery-weighted criteria and dynamic thresholds per skill; never assign holistic single-number grades (see [`references/analytic-rubrics-and-grading-hallucination-defense.md`](references/analytic-rubrics-and-grading-hallucination-defense.md))
- enforce the **Anti-Hallucination Line Citation Protocol**: every point deduction must explicitly quote the student's submission line number and verbatim text/code snippet; unanchored critiques or fabricated errors are strictly prohibited
- enforce **Executable Verification Pipeline**: code must pass sandboxed test suite; prose must have concrete derivations; both validated before scoring
- apply the **AI Fluency Detection Filter**: detect LLM-generated patterns (excessive coherence without rigor, hallucinated citations, missing derivations); cap fluency-only work at Level 2 (Developing)
- diagnose underlying cognitive failure modes using the **Extended 5-Tier Cognitive Error Taxonomy**: Conceptual Misunderstanding, Procedural Execution Error, Boundary Blindspot, Cognitive Overload, **AI-Mediated Errors** (hallucination acceptance, automation bias, prompt dependency, verification skipping) (see [`references/cognitive-error-analysis-and-socratic-feedback.md`](references/cognitive-error-analysis-and-socratic-feedback.md))
- deliver **Evidence-Based Growth-Mindset Feedback**: metacognitive strategy training (plan/monitor/evaluate, +7 months EEF), specific feedback practices ("Your argument needs counter-example in paragraph two"), safe error culture — not posters/language alone
- strictly enforce the **Rule of One + Socratic Ladder**: restrict corrective remediation to exactly one high-impact actionable step + 3-level hint escalation (Constraint Focus → Conceptual Prompt → Isomorphic Mini-Problem)
- comply with **EU AI Act High-Risk AI Governance** (Annex III, 3a): AI grading outputs are advisory; release requires verified human educator sign-off (`reviewed_by`, `verification_status: "verified_and_approved"`); **conformity assessment completed** (internal Annex VI or third-party Annex VII); **human oversight model** (HITL/HOTL/HIC) with competent personnel; **automation bias mitigation** (verification steps, override/stop, bias awareness); **Article 12 record-keeping** (automatic logging of all grading events); **Article 13 transparency** (deployer instructions, limitations, accuracy variations); **Article 26 deployer obligations** (monitoring, incident reporting, 6-month log retention)

## Suggested Process

1. **Submission Inspection & Line-by-Line Review**: Compare student code/work step-by-step against BKT-weighted rubric criteria.
2. **Executable Verification**: Sandbox code execution with test suite; validate prose derivations; record pass/fail.
3. **AI Fluency Detection**: Scan for LLM pattern markers (coherence without rigor, hallucinated citations, missing concrete derivations).
4. **Score Against BKT-Weighted 4-Tier Descriptors**: Mastery posteriors weight criteria; assign points; record mandatory verbatim quotes and line numbers for deductions.
5. **Diagnose Cognitive Error Category**: Classify as conceptual, procedural, boundary, overload, or AI-mediated (hallucination acceptance, automation bias, prompt dependency, verification skipping).
6. **Draft Evidence-Based Feedback**: Process praise, "not-yet" framing, metacognitive strategy recommendation, single highest-impact action step + 3-level Socratic hint ladder.
7. **Human Educator Verification Gate**: Verify citations, executable proofs, fluency detection, BKT weighting against raw source; approve assessment metadata with conformity assessment reference.
8. **Emit Assessment Contracts**: Serialize results to schema-validated `learning-assessment-report.json` and `learning-handoff.json`.

### In-Depth Reference Guides

- **Rubrics & Hallucination Defense**: [`references/analytic-rubrics-and-grading-hallucination-defense.md`](references/analytic-rubrics-and-grading-hallucination-defense.md) — 4-tier rubric matrices, line citation protocol, executable verification, AI fluency detection, **BKT-informed weighting**, EU AI Act compliance.
- **Cognitive Error Analysis & Socratic Feedback**: [`references/cognitive-error-analysis-and-socratic-feedback.md`](references/cognitive-error-analysis-and-socratic-feedback.md) — Extended error taxonomy (+ AI-mediated), Dweck evidence-based growth mindset, not-yet framing, Rule of One, Socratic hint ladder.

## Checklist

- [ ] Submissions evaluated against **BKT-informed 4-tier analytic rubrics** with mastery-weighted criteria and dynamic thresholds.
- [ ] Every score deduction includes verified submission line reference and verbatim quote.
- [ ] **Executable verification pipeline** passed: sandbox code execution + test suite + derivation validation.
- [ ] **AI fluency detection** applied: LLM pattern markers scanned, fluency-only work capped at Developing (Level 2).
- [ ] Primary cognitive error category diagnosed from **Extended 5-Tier Taxonomy** (conceptual, procedural, boundary, overload, AI-mediated).
- [ ] Feedback delivers **evidence-based growth mindset**: metacognitive strategy training, specific feedback, safe error culture — not posters alone.
- [ ] **Rule of One + Socratic Ladder** enforced: exactly one actionable step + 3-level hint escalation.
- [ ] **EU AI Act High-Risk compliance verified**: Conformity assessment completed (internal Annex VI / third-party Annex VII), human oversight model (HITL/HOTL/HIC), automation bias mitigation, Article 12 logging, Article 13 transparency, Article 26 deployer duties, CE marking.
- [ ] Mandatory audit metadata populated: `graded_by_ai`, `reviewed_by`, `verification_status`, `conformity_assessment_ref`, `human_oversight_model`, `bkt_mastery_posteriors`, `stanbkt_uncertainty`.
- [ ] Student personal data anonymized using pseudonymous tokens (`student_token`, e.g., `STU-8f2e-2027`).
- [ ] **StanBKT uncertainty quantification**: Bayesian posteriors for score confidence intervals.
- [ ] **Cognitive diagnostic dashboard** data: per-skill mastery, error category, ZPD progression, growth mindset indicators.

## Output Contracts

When the assessment result is handed off to a gradebook, LMS, student, or cross-agent workflow, emit:

- **`contracts/schemas/learning-assessment-report.json`** — primary contract populating `student_token`, `overall_score`, `rubric_breakdown` (with line citations + executable verification), `cognitive_error_diagnosis`, `growth_mindset_feedback`, `zpd_progression`, `bkt_mastery_posteriors`, `stanbkt_uncertainty` (Bayesian confidence intervals), `ai_fluency_detection` (LLM pattern markers), `audit_metadata`, and `conformity_assessment_ref` (High-Risk grading system compliance metadata).
- **`contracts/schemas/learning-handoff.json`** — secondary contract for multi-agent educational state, learning plan progression, curriculum handoffs, and Socratic tutoring hint ladders.
- For human-readable reports, emit markdown assessment summaries with BKT mastery trajectories, executable verification results, fluency detection flags, Socratic hint ladders, compliance evidence.

## Failure Modes

- **EU AI Act deployment violation**: Grading system used without conformity assessment. Mitigation: Deployment gate, CE marking check, technical documentation validation.
- **Automation bias in human review**: Educator over-trusts AI grading. Mitigation: HITL design, explicit disagreement workflow, bias awareness training.
- **BKT grading miscalibration**: Mastery posteriors don't match actual performance. Mitigation: StanBKT posterior predictive checks, periodic recalibration.
- **AI fluency false positive**: Human work flagged as AI-generated. Mitigation: Multi-marker detection, human review override, false positive rate monitoring.
- **Executable verification gap**: Code passes tests but has conceptual errors. Mitigation: Hybrid verification (tests + conceptual rubric + derivation check).
- **Record-keeping failure**: Missing logs for audit. Mitigation: Automatic immutable logging, tamper-evident storage, Article 12 compliance.
- **Grading hallucination**: AI deducts points for non-existent mistakes. Mitigation: Line citation verification gate; reject unanchored deductions.
- **Superficial fluency trap**: Awarding advanced grades for articulate but non-working code. Mitigation: Executable verification + AI fluency detection + conceptual rubric.
- **Feedback avalanche**: Overwhelming learner with 5–10 simultaneous critiques. Mitigation: Rule of One + Socratic Ladder enforcement.
- **Growth mindset superficiality**: "Not yet" language without strategy training. Mitigation: Metacognitive strategy integration, specific feedback templates.
- **Socratic ladder bypass**: AI tutor gives direct answers. Mitigation: Prompt locking, single-question enforcement, escalation monitoring.
- **Fixed-mindset praise**: Telling students "you are a natural genius." Mitigation: Process/effort praise enforcement, metacognitive focus.

## Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: Never include real student PII; enforce pseudonymous student tokens (`STU-...`).
- **ASI04 Supply Chain**: Validate automated grading scripts, test runners, BKT inference, fluency detection against trusted manifests.
- **ASI05 RCE Guard**: Execute student code only in isolated sandbox containers with resource limits; sanitize all inputs.
- **ASI07 Inter-Agent Communication**: Emit structured, schema-valid JSON assessment contracts for all cross-role payloads.
- **ASI09 Human-Agent Trust Exploitation**: Surface AI assistance honestly; require educator sign-off; surface residual risk honestly; don't claim "accurate grading" without human verification.

## Related Skills

- **create-exercises**: Generate targeted follow-up practice addressing diagnosed cognitive errors.
- **design-learning-plan**: Update learner ZPD progression and spaced repetition intervals based on evaluation data.

Last updated: 2026-09-25