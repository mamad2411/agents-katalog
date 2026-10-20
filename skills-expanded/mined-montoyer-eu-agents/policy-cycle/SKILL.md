---
name: policy-cycle
description: >
  Use when modelling the complete EU policy lifecycle for a given policy area.
  Runs all seven phases in sequence — agenda-setting, problem analysis, preparation
  (Better Regulation), proposal and adoption, legislative process, implementation,
  and monitoring/evaluation — following the Commission's Better Regulation
  Guidelines. Orchestrates sub-skills (consultation, impact-assessment,
  treaty-check, inter-service-consultation, legislative-proposal,
  college-deliberation, legislative-cycle, infringement, better-regulation) and
  voices the relevant institutional actors at each phase. Produces a structured
  lifecycle document suitable for use as a policy brief, training simulation, or
  initiative planning tool.
license: MIT
metadata:
  author: EC-Skills-Library
  version: "1.0.0"
  domain: eu-legislative
  triggers: >
    policy cycle, full lifecycle, agenda-setting, roadmap, inception impact
    assessment, RSB opinion, transposition, implementation, ex-post evaluation,
    REFIT, monitoring framework, policy planning, end-to-end initiative
  role: orchestrator
  scope: policy-cycle
  output-format: lifecycle-document
  institution: European Commission
  related-skills: impact-assessment, consultation, treaty-check, legislative-proposal,
    better-regulation, inter-service-consultation, legislative-cycle, infringement
---

# Policy Cycle Orchestrator — European Commission

Senior Commission policy coordinator applying the full Better Regulation
lifecycle to a given policy area. Does not substitute for the specialist
sub-skills invoked at each phase, but coordinates their outputs into a coherent
end-to-end narrative, surfaces inter-phase dependencies, and flags decision
points requiring political or legal clearance.

The cycle is iterative: every evaluation feeds back into agenda-setting. Model
this loop explicitly — do not present the cycle as linear.

---

## Core Workflow

**Input:** `<policy area>` — a sector, problem, or initiative title.

Run all seven phases in sequence. For each phase: state the actors, summarise
the institutional steps, produce the phase output, and signal any blocker before
advancing.

---

### Phase 1 — Agenda-setting

**Actors:** President of the Commission, coordinating EVP, full College.

1. Frame the strategic context: map the policy area to the current Political
   Guidelines and the Commission Work Programme (CWP). Identify the relevant
   Commissioner portfolio(s) and EVP coordination line.
2. Articulate the policy need: why is EU-level action on the agenda now?
   (political mandate, crisis, external pressure, evaluation trigger, treaty
   obligation, international commitment.)
3. Draft a **CWP entry** (one paragraph: initiative title, type of act,
   indicative timeline, lead DG, contributing DGs).
4. Draft a **Roadmap** (one page): political context, problem in outline,
   possible action, indicative timetable, consultation strategy.

**Phase output:**
- CWP entry
- Roadmap for the initiative

**Blocker check:** If the policy area falls outside the Commission's treaty
competence, flag and stop. Recommend referral to member states or intergovernmental
action.

---

### Phase 2 — Problem analysis and inception

**Actors:** Lead DG, inter-DG steering group, Legal Service (early alert).

1. Draft an **Inception Impact Assessment** (proportionate pre-screening):
   - Problem definition: what market failure, regulatory gap, or public policy
     failure justifies EU action?
   - Subsidiarity pre-check: could member states address this without EU action?
   - Possible EU action: legislative / non-legislative / no action.
   - Key impacts likely: economic, social, environmental — qualitative at this stage.
   - Who to consult and how.
2. Open a **4-week feedback period**: summarise likely stakeholder positions
   (supporters, opponents, swing groups).
3. Refine scope based on feedback.

**Phase output:**
- Inception Impact Assessment
- 4-week feedback summary

**Blocker check:** If subsidiarity pre-check is negative (member states can act
adequately), recommend non-legislative action. Flag `[review — political judgement
required]`.

---

### Phase 3 — Preparation (Better Regulation process)

**Actors:** Lead DG analysts, external contractor (if applicable), RSB, all DGs
via ISC pre-screening.

Run the following sub-processes:

**3a. Public consultation** — 12-week open public consultation.
Summarise: number of respondents, breakdown by stakeholder category, key
positions for and against, areas of consensus, contested points.

**3b. Targeted consultations** — expert groups, workshops, Eurostat data review.
Summarise additional evidence gathered.

**3c. Impact Assessment** — full SWD with:
- Problem definition (drivers, affected parties, scale)
- Baseline (no-action scenario)
- Policy options (minimum 3, including non-legislative)
- Impact analysis per option: economic, social, environmental
- SME test
- Do No Significant Harm (DNSH) assessment
- Comparison matrix
- Preferred option with proportionality statement
- Monitoring framework (indicators, milestones, data sources)

**3d. RSB review** — Regulatory Scrutiny Board opinion:
- Positive → proceed.
- Positive with reservations → revise IA on flagged points, proceed.
- Negative → IA must be revised and resubmitted; do not advance to Phase 4 until
  a positive or positive-with-reservations opinion is obtained.

Model the RSB opinion for the policy area presented: identify the most likely
RSB concerns (typically: problem evidence, baseline, option range, quantification,
SME test).

**3e. Treaty check** — legal basis confirmed: TFEU/TEU article, subsidiarity
(Art. 5(3) TEU), proportionality (Art. 5(4) TEU), Charter compatibility.

**3f. Inter-service consultation** — route to all affected DGs. Summarise:
- DGs in agreement
- DGs with reservations (list reservation points)
- DGs with opposition (list blocking points)
- Legal Service position

**Phase output:**
- SWD (Impact Assessment)
- Consultation synthesis note
- RSB opinion (modelled)
- Treaty check note
- ISC synthesis note

**Blocker check:** RSB negative opinion or Legal Service opposition blocks
advance to Phase 4. Surface both explicitly.

---

### Phase 4 — Proposal and adoption

**Actors:** Lead DG, Commissioner's cabinet, College of Commissioners.

1. Draft the **legislative proposal** (regulation or directive as appropriate):
   - Legal basis
   - Recitals (context, legal basis, subsidiarity, proportionality)
   - Operative articles
   - Explanatory Memorandum
2. Prepare the **College briefing note**: political context, key choices,
   expected reactions from EP and Council, communication strategy.
3. College deliberation: model Commissioner positions across portfolios — flag
   any intra-College tension (e.g., Competition vs. Industrial Policy, Environment
   vs. Internal Market). President arbitrates if positions diverge.
4. Formal College adoption. Record: unanimous / by written procedure / with
   reservations noted.
5. COM proposal published: `COM([year]) [number] final` — transmitted to EP
   and Council.

**Phase output:**
- Draft legislative proposal
- Explanatory Memorandum
- College briefing note
- College adoption record
- COM reference number (indicative)

---

### Phase 5 — Legislative process

**Procedure:** Ordinary Legislative Procedure (OLP) unless a special procedure
applies — identify and justify any deviation.

Run the OLP in summary:
1. EP first reading — committee lead, rapporteur, key political group positions,
   EP amendments, plenary position.
2. Council first reading — working party, presidency, QMV arithmetic (where
   applicable), general approach.
3. Trilogue (if positions diverge): key open issues, compromise trajectory,
   indicative deal timeline.
4. EP/Council second reading or conciliation if needed.
5. Final adoption — OJ reference (indicative).

Flag any risk of: EP veto, Council blocking minority, treaty base challenge,
subsidiarity reasoned opinions from national parliaments (Protocol No. 2).

**Phase output:**
- OLP stage-by-stage summary
- Key institutional positions
- Adopted text reference: `[OJ L/C — verify]`

---

### Phase 6 — Implementation

**Actors:** Member states (directives), Commission (regulations, delegated/implementing
acts), national competent authorities, Commission monitoring unit.

1. **Transposition** (directives only):
   - State the transposition deadline.
   - Model transposition status matrix: early transposers / on-track / at-risk /
     non-transposers.
   - For at-risk or non-transposing states: signal infringement procedure trigger
     (Art. 258 TFEU pre-litigation letter, then reasoned opinion, then CJEU
     referral under Art. 260(3) TFEU with financial penalty).

2. **Delegated acts** (Art. 290 TFEU): list the enabling provisions in the adopted
   act; model the timeline for adoption; note EP + Council scrutiny period.

3. **Implementing acts** (Art. 291 TFEU): identify the comitology procedure
   applicable (advisory / examination / special examination); model committee
   opinion and adoption.

4. **Guidance**: list guidance documents, FAQ, and notices the Commission should
   publish to support uniform application.

5. **Enforcement**: identify the Commission's monitoring tools (reporting
   obligations, infringement alerts, Single Market scoreboard, sectoral dashboards).

**Phase output:**
- Transposition status matrix
- Delegated and implementing acts schedule
- Guidance documents list
- Enforcement monitoring plan

**Blocker check:** Persistent non-transposition or non-application → open
infringement file. Flag `[review — legal uncertainty]` where liability is unclear.

---

### Phase 7 — Monitoring and evaluation

**Timing:** Ex-post evaluation typically 3–5 years after entry into force.

1. **Monitoring**: track key indicators defined in the legislative text
   (monitoring framework from Phase 3c). Report on: effectiveness, efficiency,
   coherence, relevance, EU added value.

2. **Ex-post evaluation (REFIT)**: apply the five REFIT criteria:
   - Effectiveness: did the measure achieve its objectives?
   - Efficiency: at what cost?
   - Relevance: are the objectives still current?
   - Coherence: does the measure interact well with related EU law?
   - EU added value: could member states have achieved the same result alone?

3. **Stakeholder consultation on evaluation results** (public consultation,
   targeted workshops).

4. **Evaluation SWD**: Staff Working Document presenting findings.

5. **Commission decision on follow-up**: maintain / amend / repeal / replace.
   - If amendment → new policy cycle begins (return to Phase 1 with the
     evaluation as the trigger).

**Phase output:**
- Monitoring indicators scorecard
- REFIT evaluation summary (five criteria)
- Evaluation SWD outline
- Commission follow-up decision (options)

---

## Feedback Loop

```
Evaluation ──────────────────────────────────► Agenda-setting (new cycle)
     ▲                                                      │
     │                                                      ▼
  Monitoring ◄── Implementation ◄── Adoption ◄── Preparation
```

The EU policy cycle is iterative. Every evaluation is a potential trigger for a
new initiative. Model this loop explicitly: at the close of Phase 7, identify
which findings, if any, warrant a new cycle and at what indicative horizon.

---

## Output Format

Structure the lifecycle document as follows:

```
POLICY CYCLE — [POLICY AREA]
[marking: none / SENSITIVE]
Lead DG: [DG]     Commissioner: [portfolio]     Date: [date]

━━━ PHASE 1 — AGENDA-SETTING ━━━
[CWP entry]
[Roadmap]

━━━ PHASE 2 — PROBLEM ANALYSIS ━━━
[Inception IA]
[Feedback summary]

━━━ PHASE 3 — PREPARATION ━━━
[Consultation synthesis]
[IA summary]
[RSB opinion]
[Treaty check]
[ISC synthesis]

━━━ PHASE 4 — PROPOSAL AND ADOPTION ━━━
[Legislative proposal outline]
[EM summary]
[College record]

━━━ PHASE 5 — LEGISLATIVE PROCESS ━━━
[OLP stage summary]
[Adopted text reference]

━━━ PHASE 6 — IMPLEMENTATION ━━━
[Transposition matrix]
[DA/IA schedule]
[Enforcement plan]

━━━ PHASE 7 — MONITORING AND EVALUATION ━━━
[Monitoring scorecard]
[REFIT summary]
[Follow-up decision]

━━━ FEEDBACK LOOP ━━━
[Trigger assessment for next cycle]
```

---

## Trust and Attribution

Apply inline attribution tags throughout:

| Tag | When |
|---|---|
| `[EUR-Lex — verify current version]` | Any treaty article, regulation, directive, or decision citation |
| `[CJEU — verify Curia reference]` | Any case law citation |
| `[model knowledge — verify]` | Any fact, figure, or institutional detail from training data |
| `[Eurostat YYYY-MM — verify]` | Any statistical data |
| `[review — political judgement required]` | Strategic calls, negotiating positions, political sensitivity |
| `[review — legal uncertainty]` | Unsettled law, contested legal basis, novel interpretation |
| `[review — RSB quality threshold not met]` | IA that would not survive RSB scrutiny |

---

DRAFT — For review by an EU official before use. Not an official Commission position.
