---
title: Builder Skill
---

---
name: neuro-builder
description: Generates structured, evidence-based clinical decision support recommendations for neurological diagnoses. Use when creating clinical workup plans, treatment protocols, or diagnostic recommendations for neurologists. Triggers on requests for clinical recommendations, diagnostic workups, treatment plans for neurological conditions, or references to teleneurohospitalist content.
---

# Neuro Clinical Recommendation Builder

Generate comprehensive, structured clinical decision support content for neurological diagnoses across care settings (ED, Hospital, ICU, Outpatient, Rehab).

## Diagnosis Scoping Rules

Identify the clinical scenario from the diagnosis modifier:

| Modifier | Interpretation |
|----------|----------------|
| "[Condition] - Exacerbation" or "Acute [Condition]" | Focus on acute management; maintenance therapy mentioned but not detailed |
| "[Condition] - New Diagnosis" | Include full workup, differential, AND long-term treatment options |
| "[Condition] - Chronic/Maintenance" | Focus on long-term management, monitoring, lifestyle |
| "[Condition] - Refractory" | Include second-line and rare therapies prominently |

If modifier is ambiguous, generate for the most common clinical scenario AND note what would differ for other scenarios.

## CRITICAL: Comprehensive Setting Coverage

**Every recommendation must be evaluated for ALL applicable settings.** Patients with the same diagnosis may present to ED, hospital, outpatient clinic, or ICU. The plan must be complete and actionable regardless of where the patient is seen.

**For each test, study, or treatment, ask:**
1. Is this applicable in the ED? What priority?
2. Is this applicable on the hospital floor? What priority?
3. Is this applicable in outpatient clinic? What priority?
4. Is this applicable in ICU? What priority?

**Use "-" only when truly not applicable** (e.g., prolactin level only useful if drawn within 20 minutes of seizure Ã¢â€ â€™ "-" for OPD). Do NOT use "-" for "less common" or "usually done elsewhere."

**Common gaps to avoid:**
- Labs missing OPD tags (outpatient neurologists need to order workups too)
- Imaging missing OPD tags (MRI often ordered from clinic)
- Treatments missing HOSP tags (maintenance meds continue inpatient)
- Referrals missing ED tags (some consults start in ED)

## Output Structure

Generate output using this exact structure. **Sections 1-4 are primary action items; Sections 5-8 are reference/supporting information** (may be collapsed by default in clinical tools).

```
DIAGNOSIS: [Name]
ICD-10: [Code(s)]
SCOPE: [Brief statement of what this template covers and excludes]

**PRIORITY KEY:** STAT = Immediate | URGENT = Within hours | ROUTINE = Standard | EXT = Extended/atypical cases | - = Not applicable to this setting

Ã¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢Â
SECTION A: ACTION ITEMS
Ã¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢Â

## 1. LABORATORY WORKUP

### 1A. Essential/Core Labs

| Test | ED | HOSP | OPD | ICU | Rationale | Target Finding |
|------|:--:|:----:|:---:|:---:|-----------|----------------|

### 1B. Extended Workup (Second-line)

| Test | ED | HOSP | OPD | ICU | Rationale | Target Finding |
|------|:--:|:----:|:---:|:---:|-----------|----------------|

### 1C. Rare/Specialized (Refractory or Atypical)

| Test | ED | HOSP | OPD | ICU | Rationale | Target Finding |
|------|:--:|:----:|:---:|:---:|-----------|----------------|

## 2. DIAGNOSTIC IMAGING & STUDIES

### 2A. Essential/First-line

| Study | ED | HOSP | OPD | ICU | Timing | Target Finding | Contraindications |
|-------|:--:|:----:|:---:|:---:|--------|----------------|-------------------|

### 2B. Extended

| Study | ED | HOSP | OPD | ICU | Timing | Target Finding | Contraindications |
|-------|:--:|:----:|:---:|:---:|--------|----------------|-------------------|

### 2C. Rare/Specialized

| Study | ED | HOSP | OPD | ICU | Timing | Target Finding | Contraindications |
|-------|:--:|:----:|:---:|:---:|--------|----------------|-------------------|

## 3. TREATMENT

**CRITICAL: Each medication must be on its own row with complete prescribing information. Do NOT group drugs together.**

### 3A. Acute/Emergent

| Treatment | ED | HOSP | OPD | ICU | Dosing | Contraindications | Monitoring |
|-----------|:--:|:----:|:---:|:---:|--------|-------------------|------------|

### 3B. Symptomatic Treatments

| Treatment | Indication | ED | HOSP | OPD | ICU | Dosing | Contraindications | Monitoring |
|-----------|------------|:--:|:----:|:---:|:---:|--------|-------------------|------------|

### 3C. Second-line/Refractory

| Treatment | ED | HOSP | OPD | ICU | Dosing | Contraindications | Monitoring |
|-----------|:--:|:----:|:---:|:---:|--------|-------------------|------------|

### 3D. Disease-Modifying or Chronic Therapies (if applicable)

| Treatment | Route | ED | HOSP | OPD | ICU | Dosing | Pre-Treatment Requirements | Contraindications | Monitoring |
|-----------|-------|:--:|:----:|:---:|:---:|--------|---------------------------|-------------------|------------|

## Treatment Section Guidance

### CRITICAL: Individual Drug Rows

**Every medication must be listed on its own row.** Do NOT group drugs together (e.g., "SSRIs" or "beta-blockers"). Each drug needs complete prescribing information.

Ã¢ÂÅ’ **Wrong:**
```
| SSRIs | Depression | - | ROUTINE | ROUTINE | - | Per drug | Various | Monitor mood |
```

Ã¢Å“â€¦ **Correct:**
```
| Sertraline | Depression | - | ROUTINE | ROUTINE | - | Start 50 mg daily; increase by 25-50 mg q1-2wk; max 200 mg | Concurrent MAOIs | Suicidality monitoring |
| Escitalopram | Depression | - | ROUTINE | ROUTINE | - | Start 10 mg daily; max 20 mg | Concurrent MAOIs; QT prolongation | QTc if risk factors |
```

### Dosing Requirements

Every drug row must include:

| Element | Example |
|---------|---------|
| Starting dose | "Start 5 mg TID" or "Start 300 mg qHS" |
| Titration schedule | "increase by 5 mg/dose every 3 days" or "increase by 300 mg every 1-3 days" |
| Target dose (if applicable) | "target 900-1800 mg TID" |
| Maximum dose | "max 80 mg/day" or "max 3600 mg/day" |
| Frequency | "BID", "TID", "once daily", "every other day" |
| Special instructions | "take with food", "avoid afternoon dosing", "exactly 12 hours apart" |

### Symptomatic Treatment Categories

For chronic neurological conditions, consider including treatments for these symptom categories where applicable:

| Category | Common in... | Example Drugs |
|----------|--------------|---------------|
| Spasticity | MS, stroke, SCI, TBI | Baclofen, tizanidine, dantrolene, botulinum toxin |
| Neuropathic pain | Neuropathy, MS, post-stroke | Gabapentin, pregabalin, duloxetine, amitriptyline, carbamazepine |
| Spasms/cramps | ALS, neuropathy | Baclofen, quinine (limited), mexiletine |
| Bladder urgency | MS, Parkinson, stroke | Oxybutynin, solifenacin, mirabegron |
| Urinary retention | MS, autonomic neuropathy | Tamsulosin, bethanechol |
| Constipation | Parkinson, neuropathy, opioid use | PEG 3350, senna, bisacodyl, lubiprostone |
| Fatigue | MS, myasthenia, post-stroke | Amantadine, modafinil, methylphenidate |
| Depression | Any chronic neuro condition | Sertraline, escitalopram, bupropion, venlafaxine |
| Anxiety | Any chronic neuro condition | SSRIs, buspirone, hydroxyzine |
| Insomnia | Parkinson, dementia, chronic pain | Trazodone, melatonin, mirtazapine |
| Tremor | MS, essential tremor, Parkinson | Propranolol, primidone, clonazepam (not for Parkinson resting tremor) |
| Sialorrhea | ALS, Parkinson | Glycopyrrolate, atropine drops, botulinum toxin |
| Pseudobulbar affect | ALS, MS, stroke, TBI | Dextromethorphan-quinidine |
| Cognitive impairment | Dementia, MS | Donepezil, memantine, rivastigmine |
| Orthostatic hypotension | Autonomic neuropathy, Parkinson | Midodrine, fludrocortisone, droxidopa |

### Disease-Modifying Therapy (DMT) Section

Use Section 3D with expanded columns when the diagnosis has chronic disease-modifying treatments:

**Applies to:** MS, myasthenia gravis, CIDP, neuromyelitis optica, autoimmune encephalitis, etc.

**Additional columns for DMTs:**
- **Route:** PO, SC, IM, IV, other
- **Pre-Treatment Requirements:** Labs, imaging, vaccinations, genetic testing, specialist clearances

**Each DMT row must include:**
- Specific brand and generic name
- Exact dosing with titration schedule (if any)
- Complete pre-treatment workup
- All contraindications
- Monitoring schedule with frequencies (e.g., "JCV antibody q6mo", "CBC monthly Ãƒâ€” 48 months")
- REMS program requirements where applicable

### Setting-Specific Treatment Notes

| Setting | Treatment Considerations |
|---------|-------------------------|
| **ED** | Acute treatments only; avoid initiating chronic therapies; can continue home meds |
| **HOSP** | Continue home meds; can initiate symptomatic treatments; DMTs typically NOT started inpatient |
| **OPD** | Primary setting for DMT initiation; chronic disease management; titration of symptomatic meds |
| **ICU** | Critical care interventions; may need to hold certain home meds; avoid drugs that worsen hemodynamics |

## 4. OTHER RECOMMENDATIONS

### 4A. Referrals & Consults

| Recommendation | ED | HOSP | OPD | ICU | Indication |
|----------------|:--:|:----:|:---:|:---:|------------|

### 4B. Patient Instructions

| Recommendation | ED | HOSP | OPD |
|----------------|:--:|:----:|:---:|

### 4C. Lifestyle & Prevention

| Recommendation | ED | HOSP | OPD |
|----------------|:--:|:----:|:---:|

Ã¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢Â
SECTION B: REFERENCE (Expand as Needed)
Ã¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢Â

## 5. DIFFERENTIAL DIAGNOSIS

| Alternative Diagnosis | Key Distinguishing Features | Tests to Differentiate |
|-----------------------|----------------------------|------------------------|

## 6. MONITORING PARAMETERS

*Venue column indicates where monitoring is typically ordered/initiated. Most monitoring continues in outpatient setting.*

| Parameter | ED | HOSP | OPD | ICU | Frequency | Target/Threshold | Action if Abnormal |
|-----------|:--:|:----:|:---:|:---:|-----------|------------------|-------------------|

## 7. DISPOSITION CRITERIA

| Disposition | Criteria |
|-------------|----------|
| Discharge home | [criteria] |
| Admit to floor | [criteria] |
| Admit to ICU | [criteria] |
| Transfer to higher level | [criteria] |

## 8. EVIDENCE & REFERENCES

| Recommendation | Evidence Level | Source |
|----------------|----------------|--------|
```

## Setting Definitions

| Setting | Definition | Typical Priorities |
|---------|------------|-------------------|
| **ED** | Emergency Department - acute presentation, limited time | STAT, URGENT |
| **HOSP** | Inpatient floor - admitted, can wait hours | STAT, URGENT, ROUTINE |
| **OPD** | Outpatient clinic - scheduled visit, days-weeks available | ROUTINE, EXT |
| **ICU** | Intensive Care Unit - critically ill, continuous monitoring | STAT, URGENT |

## Priority Definitions

| Priority | Timeframe | Use When |
|----------|-----------|----------|
| **STAT** | Immediate (minutes) | Life-threatening, time-sensitive |
| **URGENT** | Within hours | Important but not immediately life-threatening |
| **ROUTINE** | Standard timing (days) | Important but not time-sensitive |
| **EXT** | Extended workup | Atypical cases, refractory, specialized |
| **-** | Not applicable | Truly not relevant to this setting |

## Writing Style: Directive Language

All recommendations must be written as **checkbox-ready directives** - clear orders from one physician to another or to the patient. These will be selected and sent directly in clinical communications.

**DO NOT write:**
- "Consider physical therapy for balance issues"
- "Patient may benefit from neurology follow-up"
- "Smoking cessation should be encouraged"

**DO write:**
- "Physical therapy consult for gait and balance training"
- "Neurology follow-up in 2-4 weeks"
- "Smoking cessation"
- "Avoid driving until cleared by neurology"
- "Vitamin D 2000 IU daily"
- "MRI brain with and without contrast"

**Formatting rules:**
- Start with the action or service, not the rationale
- Use imperative verb forms or noun phrases
- Keep recommendations concise (aim for <10 words when possible)
- Rationale goes in the designated column, not the recommendation itself

## Section 4 Guidance: Diagnosis-Specific Content Required

**CRITICAL:** Section 4 content must be customized to the specific diagnosis. Do not copy generic content between templates. Each neurological condition has unique referral needs, patient education requirements, and lifestyle factors.

### 4A. Referrals & Consults

Include diagnosis-appropriate referrals. Common categories:

| Category | Examples |
|----------|----------|
| Rehabilitation | PT (gait, balance, strengthening), OT (ADLs, hand function), Speech (swallow, cognition, communication) |
| Subspecialty | Neuromuscular, neuro-ophthalmology, epilepsy, movement disorders, neuro-oncology |
| Medical specialties | Hematology/oncology, rheumatology, endocrinology, cardiology, pulmonology |
| Supportive | Pain management, psychiatry/psychology, social work, palliative care, genetic counseling |
| Primary care | PCP follow-up, podiatry, wound care, nutrition |

### 4B. Patient Instructions

Include actionable, diagnosis-specific instructions:

| Category | Content Type |
|----------|--------------|
| Return precautions | Specific symptoms requiring ED return |
| Activity guidance | Driving, work, exercise restrictions |
| Medication guidance | Titration expectations, what not to stop abruptly, timing |
| Self-monitoring | What to watch for, symptom diaries, when to call |
| Safety | Fall prevention, seizure precautions, heat/cold exposure |

### 4C. Lifestyle Modifications

Include modifiable risk factors and preventive measures specific to the condition:

| Category | Examples |
|----------|----------|
| Substance use | Alcohol cessation, smoking cessation |
| Metabolic | Glycemic control, blood pressure targets, lipid management |
| Activity | Exercise type and intensity, activity pacing |
| Diet/supplements | Specific vitamins, dietary modifications |
| Environmental | Heat avoidance, pressure point protection, home safety |
| Sleep | Sleep hygiene, CPAP compliance |

## Builder Principles

1. **Ensure comprehensive setting coverage** - every applicable setting must be tagged
2. **List each medication individually** - never group drugs; each drug gets its own row with complete dosing
3. **Include complete prescribing information** - starting dose, titration, max dose, contraindications, monitoring
4. Include evidence grading where available (Class I-III, Level A-C)
5. Note contraindications and monitoring requirements for all treatments
6. Be specific with dosing when standard protocols exist
7. Include red flags and escalation triggers
8. Acknowledge limitations of evidence where relevant
9. Maintain objectivity - no promotional language
10. Write all recommendations as directives, not suggestions
11. Include relevant referrals (PT, OT, Speech, subspecialty consults) and patient instructions
12. **Validate coverage:** Before finalizing, confirm each section has appropriate entries for ED, HOSP, OPD, and ICU where applicable
13. **Cover symptomatic treatments comprehensively** - include all symptom categories relevant to the diagnosis (pain, spasticity, bladder, mood, etc.)

## Setting Coverage Checklist (Validate Before Output)

Before delivering the recommendation, verify:

**Labs:**
- [ ] Can this patient present to outpatient clinic? Ã¢â€ â€™ OPD labs included?
- [ ] Can this patient be admitted? Ã¢â€ â€™ HOSP labs appropriate?
- [ ] Can this be an emergency? Ã¢â€ â€™ ED labs with STAT priorities?

**Imaging:**
- [ ] Is outpatient imaging an option? Ã¢â€ â€™ OPD column populated?
- [ ] Urgent inpatient imaging needed? Ã¢â€ â€™ HOSP column populated?

**Treatments:**
- [ ] Maintenance meds applicable in hospital? Ã¢â€ â€™ HOSP column populated?
- [ ] Acute treatments applicable in ED? Ã¢â€ â€™ ED column with STAT/URGENT?

**Referrals:**
- [ ] Can consults be initiated from ED? Ã¢â€ â€™ ED column where appropriate?
- [ ] Outpatient follow-up referrals? Ã¢â€ â€™ OPD column populated?

**Monitoring (Section 6):**
- [ ] Venue columns included for all monitoring parameters?
- [ ] Critical safety monitoring (respiratory, cardiac) has ED/ICU coverage?
- [ ] Longitudinal monitoring has OPD coverage?

## Section 6 Monitoring Parameters Guidance

Section 6 uses venue columns differently than action sections. For monitoring, the venue indicates **where monitoring is typically ordered or initiated**, not where it is performed longitudinally.

| Venue | Meaning for Monitoring |
|-------|----------------------|
| **ED** | Check this parameter in ED if patient presents acutely |
| **HOSP** | Order/initiate during hospitalization |
| **OPD** | Order/continue in outpatient follow-up |
| **ICU** | Critical monitoring in intensive care |

### Examples

| Parameter Type | Typical Venues | Rationale |
|---------------|----------------|-----------|
| HbA1c | HOSP, OPD | Longitudinal; not urgent |
| Pain scores | ED, HOSP, OPD, ICU | Assess everywhere |
| Creatinine clearance | ED, HOSP, OPD, ICU | Critical for medication dosing |
| ECG (if on QT-prolonging drug) | ED, HOSP, OPD, ICU | Safety everywhere |
| Respiratory function (NIF, FVC) | ED, HOSP, ICU | Critical for GBS/myasthenic crisis |
| Annual screening tests | OPD only | Longitudinal care |

### Critical Safety Monitoring

Always include venue-appropriate critical monitoring for conditions with acute decompensation risk:

| Condition | Critical Monitoring | Must Include |
|-----------|--------------------|--------------| 
| GBS, CIDP, MG | Respiratory function (FVC, NIF) | ED: STAT, HOSP: STAT, ICU: STAT |
| Seizure | Seizure recurrence, mental status | ED: STAT, HOSP: ROUTINE, ICU: STAT |
| Stroke | Neuro checks, BP | ED: STAT, HOSP: STAT, ICU: STAT |
| High-dose steroids | Glucose, BP, mood | ED: STAT, HOSP: ROUTINE, ICU: STAT |


## Reference Examples

See `references/ms-exacerbation-v2.md` for a complete example of Builder output that has been validated through the Checker/Rebuilder workflow.

## Lumbar Puncture Guidance

When LP is indicated for a diagnosis, include a dedicated LP subsection within Section 2 (Imaging & Studies) using this structure:

```
### LUMBAR PUNCTURE

**Indication:** [Why LP is being done]
**Timing:** [Urgent vs routine, any prerequisites]
**Volume Required:** [Standard 10-15cc OR therapeutic 30-50cc for NPH]

**Studies to Order:**
| Study | Priority | Rationale |
|-------|----------|-----------|
| Core studies (always) | STAT | Cell count x2, protein, glucose, gram stain, culture |
| [Diagnosis-specific] | [Priority] | [Rationale] |

**Special Handling:** [Time-sensitive, temperature requirements]
```

See `references/lp-reference.md` for comprehensive LP panels organized by diagnosis, including:
- Core studies (always order)
- Diagnosis-specific panels (MS, meningitis, GBS, SAH, malignancy, autoimmune)
- Advanced molecular testing (BioFire ME Panel, mNGS/Delve Detect, CSF cfDNA for tumors)
- Therapeutic LP protocols (NPH, IIH)

## Change Log

**v2.1 (January 13, 2026)**
- Added comprehensive Treatment Section Guidance
- Renamed Section 3B from "First-line Maintenance" to "Symptomatic Treatments" with Indication column
- Added requirement: each medication on individual row (no grouping)
- Added dosing requirements checklist (start, titrate, max, frequency)
- Added symptomatic treatment categories table with examples
- Added DMT section guidance with expanded columns (Route, Pre-Treatment Requirements)
- Added setting-specific treatment considerations
- Updated Section 3D template with Route and Pre-Treatment columns
- Updated Builder Principles (#2, #3, #13 for medication comprehensiveness)

**v2.0 (January 13, 2026)**
- Changed to Option A format: multi-column setting-priority matrix (ED | HOSP | OPD | ICU)
- Added comprehensive setting coverage requirements and validation checklist
- Added explicit instructions to avoid common coverage gaps
- Added setting and priority definition tables
- Reorganized for clarity and JSON conversion compatibility

**v1.0 (January 13, 2026)**
- Initial version

**v2.2 (January 14, 2026)**
- Added venue columns (ED, HOSP, OPD, ICU) to Section 6 Monitoring Parameters template
- Added "Section 6 Monitoring Parameters Guidance" explaining venue interpretation for monitoring
- Added Monitoring checklist item to Setting Coverage Checklist
- Added Critical Safety Monitoring table for conditions with acute decompensation risk
- Venue for monitoring indicates where monitoring is ordered/initiated (not necessarily performed)
