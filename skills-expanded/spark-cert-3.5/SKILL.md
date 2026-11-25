---
name: spark-cert-3.5
description: Meta-skill orchestrator for preparing the Databricks Certified Associate Developer for Apache Spark 3.5 exam (Python). Coordinates the sub-skills apache-spark, spark-connect, pandas-on-spark, and spark-3.5-updates. Activates on requests like "let's study Spark", "review <topic>", "quiz on <topic>", "mock exam", "what do I still need to study", "weak spots", "progress check".
---

# spark-cert-3.5 — Study Orchestrator

## Purpose
Coordinate the underlying Spark sub-skills for effective, exam-targeted study of the Databricks Certified Associate Developer for Apache Spark 3.5. Track study progress. Generate practice material.

## Sub-skills consulted
- `apache-spark`: Damji book "Learning Spark, 2nd Edition" (Spark 3.0 baseline) → ch01–ch12
- `spark-connect`: exam Section 6
- `pandas-on-spark`: exam Section 7 (Pandas API on Spark)
- `spark-3.5-updates`: built-ins added in 3.1–3.5, AQE evolution post-3.0, Pandas UDF / Arrow APIs

## Exam topic map

| Sec | Topic | Primary source | Secondary |
|---|---|---|---|
| 1 | Architecture & Components | apache-spark/ch01, ch02 | — |
| 2 | DataFrame API basics | apache-spark/ch03, ch04 | — |
| 3 | DataFrame transformations + built-ins | apache-spark/ch05 | spark-3.5-updates (new built-ins) |
| 4 | Performance & tuning | apache-spark/ch07, ch12 | spark-3.5-updates (AQE post-3.0) |
| 5 | Structured Streaming | apache-spark/ch08 | — |
| 6 | Spark Connect | spark-connect (only) | — |
| 7 | Pandas API on Spark + Pandas UDF | pandas-on-spark + spark-3.5-updates | apache-spark/ch05 (baseline) |

## State file
Persistent state in `~/spark-cert/progress.md`. Update at every session.

## Workflows

### study <topic>
1. Identify section/topic from the exam topic map.
2. Consult the primary source plus any secondary source.
3. Produce output:
   - Concept (concise)
   - Code example (runnable)
   - 2 exam-style multiple-choice questions (4 options each)
   - 1 trap question (tests a common misconception)
4. Wait for the user's answers.
5. Explain mistakes, update `progress.md` (coverage % and weak spots when answers are wrong).

### quiz <topic> | quiz random
- 5–10 exam-style questions on the given topic, or random from the full syllabus.
- Format: stem + 4 options + correct answer + explanation.
- Track score in `progress.md` session log.

### mock-exam
- 45 questions distributed by syllabus weight.
- Indicative time limit: 90 minutes.
- Explicit caveat: this does NOT replace external mocks (Udemy / ExamTopics).
- Score + per-section breakdown.
- Identify weak sections and suggest follow-up study sessions.

### progress
- Show current state from `progress.md`.
- Highlight: overall coverage %, completed vs pending sections, top 3 weak spots.

### weak-spots
- List topics with low quiz scores or explicitly flagged.
- For each weak spot: focused practice (3 targeted questions).

### gap-check
- For each exam-guide objective, confirm at least one sub-skill covers it.
- Identify orphan objectives → suggest an external resource.

## Operating rules

1. **Output language**: English throughout (concepts, explanations, quizzes, code).
2. **Version awareness**: everything is anchored to Spark 3.5. When a sub-skill cites Spark 3.0 (book baseline), verify the delta in `spark-3.5-updates`.
3. **No duplication**: when a topic appears in `spark-3.5-updates` as a delta over `apache-spark`, cite both with cross-links — do not duplicate content.
4. **Concise default**: keep explanations brief and dense. Expand only on explicit request ("explain more", "go deeper").
5. **Honest signaling**: when a topic has weak coverage in the skills, say so explicitly.

## Anti-patterns

- Do not explain a topic without first consulting the relevant sub-skill.
- Do not invent questions on topics not covered by the sub-skills.
- Do not update `progress.md` without confirming with the user what was studied.
- Do not generate a mock exam without the limits caveat.

## Examples

User: "Let's study save modes"
→ Sec 2 → apache-spark/ch04 → explain the 4 modes → code example → 2 exam-Qs → 1 trap → update progress

User: "Quiz on AQE"
→ Sec 4 → apache-spark/ch12 + spark-3.5-updates → 5 questions mixing basics with post-3.0 additions → score

User: "What do I still need to study?"
→ progress → coverage + 3 top weak spots → suggest the next session
