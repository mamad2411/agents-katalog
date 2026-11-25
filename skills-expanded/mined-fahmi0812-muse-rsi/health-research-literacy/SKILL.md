---
name: health-research-literacy
description: Health research literacy — read and appraise medical literature, explain it in plain language.
---

# health-research-literacy

> Health research literacy — read and appraise medical literature, explain it in plain language.
> This skill is for **research and education only**. It is NOT clinical care.

## Hard guardrails (read first)

- **Never diagnose.** Never interpret a person's symptoms, test results, scans, or lab values.
- **Never recommend treatment.** No drug, dose, procedure, diet, or therapy advice for any individual.
- **Never handle patient data.** No medical records, no EHR/FHIR patient data, no personal health information.
- **Always cite sources and state uncertainty.** Every claim needs a source (guideline, systematic review, or peer-reviewed paper) and a confidence level.
- **Always say: consult a clinician.** Any question about a real person's health ends with a referral to a qualified clinician — never an answer.
- If a request asks for diagnosis, treatment, or patient-data handling, **refuse that part** and offer the research-literacy alternative instead (e.g. "here is how to read the guideline on this topic").

## When to use

- Reading a medical paper or guideline and explaining what it actually says.
- Comparing study designs and judging how strong the evidence is.
- Finding trustworthy sources: guidelines, systematic reviews, meta-analyses.
- Explaining a health topic in plain language for a general audience.

## Workflow

### 1. Identify the study design

| Design | What it can show | Key weakness |
|---|---|---|
| Systematic review / meta-analysis | Pooled evidence across studies | Only as good as the included studies |
| Randomised controlled trial (RCT) | Causal effect of an intervention | Small, short, or selected populations |
| Cohort study | Association over time | Confounding |
| Case-control study | Association, rare outcomes | Recall and selection bias |
| Case report / series | A signal worth studying | No comparison group — weakest evidence |

### 2. Appraise the evidence

- **Risk of bias:** randomisation, blinding, dropouts, selective reporting.
- **Certainty (GRADE-style):** high / moderate / low / very low — state it, do not hide it.
- **Effect size vs. hype:** report absolute numbers (e.g. "3 in 100 vs 5 in 100"), not only relative percentages.
- **Population:** who was studied? Age, setting, country. Do not generalise beyond them.
- **Funding and conflicts of interest:** note who funded the study.

### 3. Find the right source, in this order

1. Clinical practice guidelines (e.g. WHO, national guidelines).
2. Systematic reviews (Cochrane, PubMed, Epistemonikos).
3. Peer-reviewed papers (PubMed, Semantic Scholar).
4. Preprints and news — usable only as "early / unverified", never as proof.

### 4. Explain in plain language

- One sentence: what was studied, in whom, what was found.
- One sentence: how certain we are, and why.
- One sentence: what is still unknown.
- Link every claim to its source. No invented numbers, no invented citations.

## Checklist

- [ ] Source cited for every factual claim?
- [ ] Study design named and its limits stated?
- [ ] Certainty level stated (not implied)?
- [ ] Absolute numbers given, not only relative ones?
- [ ] "Consult a clinician" added where a real person's health is involved?
- [ ] No diagnosis, no treatment advice, no patient data anywhere?

## Related skills (link only, not copied)

- [Aperivue/medsci-skills](https://github.com/Aperivue/medsci-skills) — medical research (pending re-check, see docs/expansion.md).
- [aipoch/medical-research-skills](https://github.com/aipoch/medical-research-skills) — medical research (pending re-check).
- [PhenoML/ClaudeFHIRSkill](https://github.com/PhenoML/ClaudeFHIRSkill) — FHIR / health informatics (pending re-check).
- Lumitome has **no** health skill — this skill fills that gap.
