---
name: gdpr-pia
description: Data Protection Impact Assessment (DPIA / GEB) workflow against AVG Art 35 — trigger check (AP criteria and WP 248), systematic description, necessity, risk analysis from the data subject's perspective, measures and residual risk, prior consultation with the Autoriteit Persoonsgegevens.
---

# AVG / GDPR Data Protection Impact Assessment

> **Disclaimer**: this is not legal advice. A DPIA is a legally sensitive document that exposes the organization to AP supervision and potentially civil claims. This skill structures the analysis; final qualifications (lawful basis, proportionality balancing, residual-risk acceptance) belong with the FG/DPO and/or privacy counsel.

## When to use

Art 35 AVG requires a Data Protection Impact Assessment (DPIA, in NL also "gegevensbeschermingseffectbeoordeling" or GEB) for processing operations posing a high risk to data subjects. This skill helps with the trigger check, drafting, and prior consultation of the AP when the residual risk remains high.

Triggers on:

- A question like "do we need a DPIA for this", "is this processing high-risk under the AVG", "help me draft a DPIA", "how do we do prior consultation with the AP", "DPIA template".
- A new or substantially changed processing of personal data: new SaaS introduction, AI/ML application that profiles, camera systems, biometrics, health data, large-scale data, employee monitoring, or processing in countries without an adequacy decision.
- A handoff from `risk-register` when privacy risk is part of it, or from `vendor-questionnaire` when a processor newly comes into scope.
- An FG/DPO question during supervisory or audit preparation.

### When NOT (handoff)

- Breach notifications (Art 33/34 AVG) → `ir-runbook` with a separate AP reporting procedure. DPIA is preventive, breach reporting is reactive.
- Negotiating data-processing agreements (Art 28) → legal expertise, optionally `vendor-questionnaire` for the security side.
- International transfers (Chapter V AVG) outside the EU/EEA → a separate Transfer Impact Assessment (TIA), requires Schrems II analysis. This skill touches on it but does not cover it fully.
- General security measures (Art 32) outside DPIA context → `secure-coding`, `security-review`, etc.
- Technical implementation of minimization/pseudonymization → `secure-coding` + the relevant framework skill. This skill demands that you do it, not how.
- Policy drafting (privacy policy, processing-register template) → `policy-drafter`.

## Approach

Seven phases. Phase 1 (trigger check) decides whether you go further at all; phase 6 (AP consultation) only when residual risk is high.

### 1. Trigger check: is a DPIA required?

Art 35(1) AVG: a DPIA is required for "a high risk to the rights and freedoms of natural persons". Three routes to that conclusion:

**Route A — the three trigger categories from Art 35(3):**

- Systematic and extensive evaluation of personal aspects based on automated processing (incl. profiling) with legal effects or similarly significant effects.
- Large-scale processing of special categories of personal data (Art 9: e.g. health, race, religion, sexual orientation, biometric data for unique identification, genetic) or criminal data (Art 10).
- Systematic large-scale monitoring of publicly accessible areas.

**Route B — WP 248 rev.01 (EDPB guidance, formerly Article 29 Working Party).** Nine criteria where **two or more** indicate a DPIA:

1. Evaluation or scoring (incl. profiling).
2. Automated decision-making with legal or similarly significant effect.
3. Systematic monitoring.
4. Sensitive data or data of a highly personal nature.
5. Processed at large scale.
6. Matching or combining datasets.
7. Data on vulnerable data subjects.
8. Innovative use or application of new technological or organizational solutions.
9. Processing that itself prevents data subjects from exercising a right or using a contract.

**Route C — AP list under Art 35(4).** The Autoriteit Persoonsgegevens publishes a list of processing operations for which a DPIA is explicitly required. `[verify the current list at autoriteitpersoonsgegevens.nl]` — changes periodically. Typically contains: covert observations, large-scale processing of health data, flexible-deployment systems, blacklists, etc.

Output of phase 1: one of three outcomes — *required* (under Art 35(3), 2+ criteria from WP 248, or the AP list), *recommended* (1 criterion plus doubt), *not required* (clearly below). For *not required*: motivate and archive, because the AP can ask.

### 2. Systematic description of the processing

Art 35(7)(a). Factual basis for the rest of the DPIA.

- **Purpose and lawful basis** (Art 6 + Art 9 if special categories).
- **Categories of data subjects**: customers, employees, children, patients, etc. Watch for vulnerable categories.
- **Categories of personal data**: ordinary / special / criminal. Which fields, with which sensitivity.
- **Recipients**: internal departments, processors, third parties, government. Per recipient: what they receive and why.
- **Retention periods** per data category.
- **Technical and organizational context**: data flows (source system → pipeline → storage → analysis → output), hosting locations, access paths.
- **Transfers outside EEA**: which country, which transfer ground (Art 45 adequacy / Art 46 SCC / Art 49 derogation).

DFD-style schemas help here (same approach as `threat-modeler` Question 1). One diagram plus an inventory table.

### 3. Necessity and proportionality

Art 35(7)(b). This is where DPIAs are often handled too lightly.

- **Necessity**: is this processing really needed for the stated purpose? Alternatives considered? Less invasive variants possible (aggregated data, pseudonymization, shorter retention)?
- **Proportionality**: is the impact on data subjects in proportion to the interest served? Is the involvement of chain partners weighed in? Would a reasonable person understand and accept this processing in this context?
- **Concrete data minimization**: which fields are actually needed, which can go? Often shifting boundaries between "nice to have" and "need".
- **Retention periods**: why exactly this period, not shorter? Is there a mandatory statutory term? If so: which.

This part must be critical. A DPIA that says "yes it is necessary" without naming alternatives is a DPIA the AP will send back.

### 4. Risk analysis — from the data subject's perspective

Art 35(7)(c). Core reframe: the risks are for the **data subject**, not for the organization. This is the difference between a DPIA and an organizational risk analysis.

Three categories of impact on data subjects:

- **Loss of confidentiality**: unauthorized access to data. Consequence: discrimination, identity theft, financial harm, reputational harm, stigmatization.
- **Loss of integrity**: unauthorized modification of data. Consequence: wrong decisions against the data subject (credit, benefit, care).
- **Loss of availability**: data unavailable when needed. Consequence: service stalls, rights cannot be exercised.

Per threat: sources (internal actor, external attacker, accident, third-party recipient), likelihood (high/medium/low, with rationale), severity for the data subject (high/medium/low, with concretely described consequence).

Output: a threat register comparable to `threat-modeler`, but with **impact on the data subject** as the main dimension, not organizational impact.

### 5. Measures and residual risk

Art 35(7)(d). Per threat:

- **Existing measures**: what is already present (technical + organizational). Refer to Art 32 AVG (security) and the concrete implementation (see `secure-coding`, `security-review`, `iso27001` Annex A controls).
- **Additional measures**: what is added on the basis of this DPIA. Which threat they mitigate, and how much reduction in likelihood/severity.
- **Residual risk**: after all measures, what remains? High, medium, or low.

The combination of (severity × likelihood) after measures decides whether you go to phase 6.

### 6. Prior consultation with the AP (only when residual risk is high)

Art 36 AVG. If the residual risk after measures stays high, the controller MUST consult the AP before processing starts.

Procedure:

- A formal request via the AP's online form with the full DPIA as an annex plus additional context (responsibilities, the FG/DPO involved, the chosen measures, why the residual risk cannot be further mitigated).
- The AP has up to 8 weeks to issue written advice (extendable by 6 weeks for complexity). Do not start processing before advice is received or the deadline has passed.
- The AP's advice is binding in the sense that the AP can take enforcement action on disregard. In practice, organizations work with the AP on the recommended changes.

The question "high-residual-risk" is itself a qualification. When in doubt: consult. Underestimation is more expensive than over-consulting.

### 7. Verification-loop and maintenance

Layer 1: scope (all data flows included in the DPIA, no shadow processing forgotten?), assumptions (is the lawful basis really solid, or did "legitimate interest" simply appear without weighing?), gaps (route-A trigger check done, not just route-B counted?). Layer 2: AVG article numbers correct, `[verify]` markers on every reference to "the AP list of mandatory DPIAs" because that list is updated, WP 248 rev.01 correctly attributed (EDPB-endorsed), no invented AP/court rulings.

**A DPIA is not a static document.** On a material change in processing (new dataset added, new recipient, new technology) a new or supplemented DPIA is required. An annual review even without change is best practice.

## Output

A DPIA report, not just a summary. Structure (also see the AP template as a reference):

```
Data Protection Impact Assessment — <processing>
Version: 1.0 | Date: YYYY-MM-DD | Drafted by: <name + role, with FG/DPO: <name>>

1. Trigger and scope
   Trigger:       <Art 35(3) / WP 248 / AP list — specific criteria>
   Reason:        <new processing | change | review>
   Controller:    <entity>
   Processor(s): <list with AVG Art 28 agreement>

2. Systematic description
   Purpose:       <explicit>
   Lawful basis:  <Art 6(1)(a-f), for special also Art 9(2)>
   Data subjects: <categories, incl. vulnerable>
   Data:          <categories, fields, sensitivity>
   Recipients:    <list + role>
   Retention:     <per category, with rationale>
   Transfer:      <EEA | third country with ground + safeguards>
   DFD / diagram: <visual or textual>

3. Necessity and proportionality
   Necessity:          <argumentation with alternatives review>
   Proportionality:    <weighing>
   Minimization:       <which fields, pseudonymization, anonymization>
   Retention rationale:<...>

4. Risk analysis (data-subject perspective)
   Per threat: source, likelihood, severity, concrete consequence for the data subject.

5. Measures
   Per threat: existing + additional measures, post-mitigation likelihood/severity.
   Residual-risk conclusion: high | medium | low.

6. Prior AP consultation
   Required?:     <yes when residual risk is high | no>
   Status:        <submitted date | advice received date | n/a>

7. Approval + maintenance
   Approver:      <accountable manager + FG/DPO sign-off>
   Review date:   <annually + on change>

Verification-loop: ...
```

## References

- **AVG (Regulation (EU) 2016/679)** — [https://eur-lex.europa.eu/eli/reg/2016/679](https://eur-lex.europa.eu/eli/reg/2016/679). Official text; Art 35 and Art 36 are primary.
- **Uitvoeringswet AVG (UAVG)** — [https://wetten.overheid.nl/BWBR0040940](https://wetten.overheid.nl/BWBR0040940). NL implementing law.
- **Autoriteit Persoonsgegevens — DPIA page** — [https://www.autoriteitpersoonsgegevens.nl/themas/basis-avg/avg-algemeen/data-protection-impact-assessment-dpia](https://www.autoriteitpersoonsgegevens.nl/themas/basis-avg/avg-algemeen/data-protection-impact-assessment-dpia).
- **AP — list of mandatory DPIAs** — [https://www.autoriteitpersoonsgegevens.nl/](https://www.autoriteitpersoonsgegevens.nl/). Search for "lijst dpia". `[verify current version]`.
- **EDPB — WP 248 rev.01 DPIA Guidelines** — [https://edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-data-protection-impact-assessment-dpia_en](https://edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-data-protection-impact-assessment-dpia_en). EDPB-endorsed guidance.
- **CNIL PIA software** — [https://www.cnil.fr/en/open-source-pia-software-helps-carry-out-data-protection-impact-assessment](https://www.cnil.fr/en/open-source-pia-software-helps-carry-out-data-protection-impact-assessment). Open-source tool for PIA drafting, free to use outside France.
- **EDPB Guidelines 03/2022 — transparency requirements** — [https://edpb.europa.eu/](https://edpb.europa.eu/).
- **Schrems II (C-311/18)** — [https://curia.europa.eu/juris/documents.jsf?num=C-311/18](https://curia.europa.eu/juris/documents.jsf?num=C-311/18). For international transfer assessments.

## Categories

- grc
