---
name: hyrox-training-plan
description: "Generate evidence-bounded HYROX training plans and daily sessions. Use for: programming Open, Pro, Elite 15, Doubles, or Relay preparation; applying periodization and validated race standards; and incorporating non-prescriptive nutrition, sleep, recovery, and pacing guidance with transparent evidence labels."
---

# HYROX Training Plan Generator

Generate plans for a running-focused hybrid race without treating every coach claim as science. HYROX-direct evidence is still limited: the first physiological study involved 11 recreational athletes in a simulated Individual Open competition. It found that running occupied more time than stations and that VO2max and endurance-training volume correlated with faster completion; it did **not** establish a universal program, fixed zone target, or nutrition protocol.[1]

## Non-Negotiable Evidence Policy

Classify every rationale and user-facing recommendation as one of the following:

| Label | Meaning | Permitted agent behavior |
|---|---|---|
| `HYROX_DIRECT` | Official HYROX standard or research in HYROX/simulated HYROX | State the finding with its population and limitation. |
| `TRANSFER_EVIDENCE` | Adjacent endurance, strength, concurrent-training, nutrition, or sleep research | Explain that it informs HYROX planning but is not HYROX-proven. |
| `COACH_PRACTICE` | A credentialed coach or athlete’s transcript-derived method | Offer as an optional, test-and-monitor method only. |
| `CLINICAL_REFERRAL` | Medical, injury, eating, sleep-disorder, medication, or supplement-risk issue | Stop personal prescription and direct the athlete to the appropriate qualified professional. |

Never turn a `TRANSFER_EVIDENCE` or `COACH_PRACTICE` item into a mandatory rule. Never invent a citation, transcript quotation, source credential, dose, race standard, or physiological threshold.

## Reference Loading Order

Read the files needed for the task, in this order:

1. `references/training-principles.json` — Core physiological and programming constraints.
2. `references/race-standards.json` — Correct race format, distances, and division-specific loads.
3. `references/periodization-models.json` and `references/session-types.json` — Macrocycle and session design.
4. `references/plan-template.json` — Accepted inputs and weekly-template guardrails.
5. `references/multidomain-evidence.json` — Nutrition, sleep, recovery, injury-risk, and supplement boundaries.
6. `references/pacing-strategy.json` — Race pacing and station management ideas.
7. `references/expert-video-synthesis.md` — Transcript-audited coach methods and use limits.
8. `references/evidence-verification-notes.md` — Primary-source limitations and claim-verification method.
9. `references/output-card-format.md` — Only when generating visual cards.

## Intake and Safety Gate

Before creating a personalized plan, collect the minimum information needed to avoid false precision.

| Area | Ask for | If missing or concerning |
|---|---|---|
| Race | Division, date, format, target outcome, known standards | Use only official standards; do not guess. |
| Training | Current weekly running/strength work, recent load, history, time, equipment, movement competency | Start conservatively and use substitutions. |
| Readiness | Sleep trend, stress, soreness, current pain, session-RPE preference | Offer a readiness-adjusted option; never diagnose from a wearable. |
| Nutrition | Diet constraints, session context, prior GI tolerance | Give general education only if medical/dietetic context is incomplete. |
| Supplements | Age, medications, health status, anti-doping obligations, prior tolerance | Use `CLINICAL_REFERRAL` or qualified dietitian/physician review when relevant. |

Do not provide individualized medical, clinical nutrition, injury diagnosis, return-to-sport clearance, medication, or supplement dosing advice. Trigger `CLINICAL_REFERRAL` for acute injury, pain that changes gait, chest pain, fainting, persistent gastrointestinal symptoms, suspected eating disorder/low energy availability, pregnancy/postpartum, medication interactions, or persistent sleep problems.

## Planning Workflow

### 1. Build the race-aware macrocycle

Use Base → Build → Peak → Taper, but adjust phase duration for the athlete’s race date, baseline, and tolerance. Include lower-stress weeks as a planning option or response to accumulated fatigue; never claim that a fixed deload calendar is mandatory. The existing 8–16 week guidance remains a scaffold, not a substitute for coaching judgment.

### 2. Allocate the weekly stress budget

Prioritize aerobic capacity and running economy while maintaining enough strength endurance for the race loads. The HYROX physiological study supports an endurance emphasis, but its small simulated sample cannot support a universal “60% of all sessions” rule.[1] Apply the intensity and session rules in `training-principles.json` as guardrails, then explain any adjustment.

Separate or sequence demanding strength and high-intensity endurance thoughtfully. Treat minimum separation times as transfer-based scheduling heuristics, not universal biological cutoffs. Avoid adding multiple new overloads in the same week (for example, more running volume, heavier sleds, and a new HIIT session).

### 3. Add specific station and compromised-running work

During Build and Peak, use station complexes and compromised running only at a dose the athlete can recover from. Progress one or two new station-load exposures at a time, then assess next-day symptoms, technique, and subsequent run quality. This is `COACH_PRACTICE` informed by expert transcripts, not a requirement for every session.[2]

### 4. Integrate nutrition, sleep, and recovery safely

Use `multidomain-evidence.json` for all non-training content.

- **Nutrition:** Treat fueling as a trainable behavior. For extended high-intensity sessions, ask about existing tolerance and offer a small practice experiment; label carbohydrate and protein guidance as `TRANSFER_EVIDENCE`.[3]
- **Sleep:** Use repeated sleep disruption as a readiness flag and offer an easier or lower-impact alternative. Do not prescribe universal sleep hours, interpret a wearable clinically, or auto-cancel a session after one poor night.[4]
- **Recovery and injury risk:** Progress load gradually, maintain strength appropriately, and use symptom trends to trigger review. Do not claim that a fixed 10% increase, an ACWR cutoff, or any single metric predicts injury.[5] [6]
- **Supplements:** Keep them optional. Do not make any product, stack, brand, or dose part of a default plan. An athlete subject to anti-doping rules needs qualified review and batch-testing awareness.[7]

### 5. Format the plan with transparency

Every session must state its purpose, objective load, RPE/pace cue where appropriate, modification option, and evidence label. Use `HYROX_DIRECT`, `TRANSFER_EVIDENCE`, or `COACH_PRACTICE` in a compact rationale line.

For a visual weekly overview or daily card, follow `references/output-card-format.md`. Do not put health diagnoses, supplement protocols, or unqualified nutrition prescriptions on cards.

## Example Prompt Pattern

> “Create a 12-week Men’s Open HYROX plan for an intermediate athlete with six available sessions per week. Read the required references. Label every rationale as HYROX_DIRECT, TRANSFER_EVIDENCE, or COACH_PRACTICE. Include a sleep/readiness adjustment and a fueling-practice option, but do not make medical, dietetic, or supplement prescriptions. Validate race standards and the final JSON plan.”

## Validation

Run the evidence-pack and plan validators from the repository root:

```bash
python3 scripts/validate_evidence_pack.py
python3 scripts/validate_plan.py examples/sample-12-week-plan.json
```

The evidence validator checks traceable source records and claim boundaries. The plan validator checks only structural and programming guardrails. Passing either validator does **not** prove a plan is safe, individualized, medically appropriate, or optimized for a particular athlete.

## References

[1] Brandt T, et al. [Acute physiological responses and performance determinants in HYROX](https://doi.org/10.3389/fphys.2025.1519240). *Frontiers in Physiology*. 2025.

[2] [Expert Video Synthesis and Use Policy](references/expert-video-synthesis.md).

[3] Kerksick CM, et al. [International society of sports nutrition position stand: nutrient timing](https://doi.org/10.1186/s12970-017-0189-4). *JISSN*. 2017.

[4] Walsh NP, et al. [Sleep and the athlete: narrative review and 2021 expert consensus recommendations](https://doi.org/10.1136/bjsports-2020-102025). *BJSM*. 2021.

[5] Gabbett TJ. [Load Management: What It Is and What It Is Not!](https://doi.org/10.1177/19417381231179946). *Sports Health*. 2023.

[6] Lauersen JB, et al. [Strength training as superior, dose-dependent and safe prevention of acute and overuse sports injuries](https://doi.org/10.1136/bjsports-2018-099078). *BJSM*. 2018.

[7] Maughan RJ, et al. [IOC consensus statement: dietary supplements and the high-performance athlete](https://doi.org/10.1136/bjsports-2018-099027). *BJSM*. 2018.
