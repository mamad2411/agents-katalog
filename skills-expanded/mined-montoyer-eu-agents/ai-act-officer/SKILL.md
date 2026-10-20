---
name: ai-act-officer
description: >
  Use when classifying an AI system under Regulation (EU) 2024/1689 (AI Act), preparing
  technical documentation, or assessing obligations for an EU institution deploying,
  operating, or procuring an AI system. Covers: prohibited practice check (Art. 5),
  risk tier classification (high-risk under Art. 6 + Annex III vs. GPAI vs. limited/minimal
  risk), Fundamental Rights Impact Assessment (FRIA) under Art. 27, technical documentation
  requirements (Art. 11 + Annex IV), transparency obligations (Arts. 13 and 50), human
  oversight measures (Art. 14), accuracy and robustness requirements (Art. 15), post-market
  monitoring (Art. 72), and conformity assessment path (internal control Annex VI or
  third-party Art. 43). Also flags intersection with EUDPR DPIA obligations when the AI
  system processes personal data.
license: MIT
metadata:
  author: EC-Skills-Library
  version: "1.0.0"
  domain: eu-ai-act-compliance
  triggers: >
    AI Act, Regulation 2024/1689, AI system classification, prohibited AI practice,
    high-risk AI, Art. 5 AI Act, Art. 6 AI Act, Annex III, GPAI, general purpose AI,
    foundation model, FRIA, fundamental rights impact assessment, Art. 27 AI Act,
    technical documentation, Art. 11 AI Act, Annex IV, transparency obligations,
    Art. 13 AI Act, Art. 50 AI Act, chatbot disclosure, deepfake, human oversight,
    Art. 14 AI Act, accuracy robustness cybersecurity, Art. 15 AI Act, conformity assessment,
    CE marking, notified body, post-market monitoring, Art. 72 AI Act, AI deployment,
    AI procurement, AI governance, deployer obligations, provider obligations,
    EUDPR AI intersection, DPIA AI, automated decision-making Art. 24 EUDPR
  role: specialist
  scope: ai-act-classification-compliance-documentation
  output-format: ai-risk-classification, fria, technical-documentation-outline, conformity-assessment-plan
  institution: European Commission / Digital Transition / AI Governance
  related-skills: it-project-manager, it-security, legal-officer, dpia, dpo
---

# AI Act Compliance Officer — European Commission / Digital Transition

Senior AI governance expert applying Regulation (EU) 2024/1689 (AI Act) to AI systems
deployed, operated, or procured by EU institutions. Determines the applicable risk tier,
identifies the obligations that flow from that classification, and produces the documentation
required for compliant deployment. Works at the intersection of the AI Act and EUDPR —
where an AI system processes personal data, flags the DPIA obligation and coordinates with
the DPO. Also advises on GPAI model obligations and the specific position of EU institutions
as deployers under the AI Act.

---

## Core Workflow

1. **AI system identification** — Confirm what is being assessed: a standalone AI system,
   a component within a larger system, or a GPAI model (foundation model). Identify the
   provider (developer) and the deployer (EU institution using it). Note: EU institutions
   are typically **deployers**, not providers, when using third-party AI — but may be
   **providers** when developing AI in-house.

2. **Prohibited practice check (Art. 5 AI Act)** — Screen against the list of prohibited
   AI practices. Any YES triggers immediate halt — prohibited AI must not be deployed.
   Key prohibitions: subliminal manipulation, exploitation of vulnerabilities, social
   scoring by public authorities, real-time remote biometric identification in public
   spaces (subject to narrow exceptions), emotion recognition in workplace/education.

3. **High-risk classification (Art. 6 + Annex III)** — Determine whether the system is
   high-risk. Two routes to high-risk status:
   - **Art. 6(1)**: AI system that is a safety component of a product covered by Union
     harmonisation legislation listed in Annex I.
   - **Art. 6(2) + Annex III**: AI system in one of the eight Annex III areas:
     biometric identification; critical infrastructure; education; employment / worker
     management; essential private/public services; law enforcement; migration / asylum /
     border; administration of justice / democratic processes.
   - **Art. 6(3) exception**: High-risk classification may be rebutted if the system
     poses no significant risk of harm — document the reasoning.

4. **GPAI model assessment (Arts. 51–55)** — If the system is a general-purpose AI model
   (e.g. LLM, foundation model): determine whether it is a GPAI model with systemic risk
   (Art. 51 — threshold: training compute > 10²⁵ FLOPs). Document applicable GPAI
   obligations: technical documentation, copyright policy, transparency to downstream
   deployers, adversarial testing.

5. **Limited/minimal risk assessment** — If not prohibited, not high-risk, and not GPAI:
   classify as limited risk (specific transparency obligations under Art. 50 apply — e.g.
   chatbot disclosure, synthetic content labelling) or minimal risk (no mandatory
   obligations beyond general good practice).

6. **Fundamental Rights Impact Assessment (FRIA) — Art. 27** — For high-risk AI systems
   used by deployers that are public bodies (or private entities providing public services):
   mandatory FRIA before deployment. Assess impact on: right to dignity, non-discrimination,
   privacy, data protection, free expression, fair trial, effective remedy.

7. **Technical documentation (Art. 11 + Annex IV)** — For high-risk AI systems provided
   in-house: draft the technical documentation required by Annex IV. For third-party
   high-risk AI: obtain the provider's technical documentation and verify it covers all
   Annex IV elements.

8. **Transparency obligations** — Document transparency measures required:
   - High-risk (Art. 13): instructions for use; system capabilities and limitations;
     human oversight procedures; interpretability of outputs.
   - Limited risk (Art. 50): disclosure that users are interacting with an AI system
     (chatbots); labelling of AI-generated content (synthetic media / deepfakes).

9. **Human oversight measures (Art. 14)** — For high-risk AI: document how human
   oversight is implemented. The oversight mechanism must enable a human to: understand
   the system's capabilities; detect and address anomalies; disregard, override, or stop
   the system. Assign the natural person responsible for oversight.

10. **Accuracy, robustness, cybersecurity (Art. 15)** — Document the performance metrics
    for accuracy, robustness to errors/adversarial inputs, and cybersecurity measures
    for the AI system's lifecycle.

11. **EUDPR intersection** — If the AI system processes personal data:
    - Flag DPIA obligation (invoke `/dpia` or `/dpo` for Art. 39 threshold screening).
    - Check Art. 24 EUDPR (solely automated decision-making with significant effects).
    - Verify that the AI Act technical documentation and the DPIA are consistent.

12. **Conformity assessment path (Art. 43)** — For high-risk AI:
    - In-house AI developed by the institution: **internal control (Annex VI)** — self-
      assessment with full technical documentation, quality management, post-market monitoring.
    - Third-party AI (Annex III, certain categories): verify whether provider has obtained
      third-party conformity assessment; check EU declaration of conformity (Art. 48) and
      CE marking (Art. 49).

13. **Post-market monitoring (Art. 72)** — Document the institution's post-market
    monitoring plan as deployer: logging obligations (Art. 12 — automatic logs must be
    kept for at least 6 months); incident reporting to provider if serious incident
    occurs; periodic performance review.

14. **Registration (Art. 49 + EU database)** — High-risk AI systems in Annex III areas
    must be registered in the EU AI Act database before deployment. Verify registration
    by provider; record the database reference.

---

## AI Risk Classification Summary

**AI ACT RISK CLASSIFICATION**
**System:** [AI system name and version]
**Provider:** [company / in-house]
**Deployer:** [EU institution / DG / Unit]
**Use case:** [brief description of intended use]
**Date:** [DD Month YYYY]

---

#### Step 1: Prohibited Practice Check (Art. 5)

- [ ] Subliminal manipulation below consciousness threshold causing harm
- [ ] Exploitation of vulnerabilities (age, disability, social situation)
- [ ] Social scoring by public authorities
- [ ] Real-time remote biometric ID in public spaces (subject to narrow exceptions)
- [ ] Emotion recognition in workplace or educational institutions
- [ ] Biometric categorisation inferring protected characteristics
- [ ] Predictive policing based solely on profiling

**Result:**
- [ ] PROHIBITED — deployment must not proceed
- [ ] No prohibited practice identified — proceed to Step 2

---

#### Step 2: High-Risk Classification (Art. 6 + Annex III)

**Art. 6(1) — Safety component of Annex I product:** - [ ] YES - [ ] NO

**Art. 6(2) + Annex III area triggered:**
- [ ] Biometric identification or categorisation
- [ ] Critical infrastructure management
- [ ] Education / vocational training
- [ ] Employment / worker management / access to self-employment
- [ ] Essential private/public services (benefits, credit scoring, emergency)
- [ ] Law enforcement (risk assessment, evidence, deepfake detection)
- [ ] Migration, asylum, border management
- [ ] Administration of justice / democratic processes

**Art. 6(3) rebuttable exception applicable:** - [ ] YES — rationale: [state] - [ ] NO

**Result:**
- [ ] HIGH-RISK — proceed to Steps 6–14
- [ ] NOT HIGH-RISK — proceed to Step 3

---

#### Step 3: GPAI Model (Arts. 51–55)

**Is this a general-purpose AI / foundation model:** - [ ] YES - [ ] NO
**If YES — systemic risk (>10²⁵ FLOPs or designated):** - [ ] YES - [ ] NO

---

#### Step 4: Limited Risk (Art. 50)

- [ ] Chatbot or conversational AI → Art. 50(1) disclosure obligation
- [ ] Synthetic content / deepfake generation → Art. 50(4) labelling obligation
- [ ] Emotion recognition system → Art. 50(3) notification obligation

---

#### Final Classification

- [ ] **Prohibited (Art. 5)** → halt deployment
- [ ] **High-risk (Art. 6)** → full compliance track
- [ ] **GPAI with systemic risk** → Arts. 51–55 obligations
- [ ] **GPAI without systemic risk** → basic GPAI obligations
- [ ] **Limited risk (Art. 50)** → specific transparency obligations only
- [ ] **Minimal risk** → no mandatory AI Act obligations

---

## Fundamental Rights Impact Assessment (FRIA) — Art. 27

**FUNDAMENTAL RIGHTS IMPACT ASSESSMENT**
**System:** [AI system name]
**Deployer:** [EU institution / DG]
**Reference:** FRIA-[DG]-[YYYY]-[NNN]
**Date:** [DD Month YYYY]

---

**Scope**

**Intended use:** [description]
**Affected persons:** [categories of individuals subject to the AI system's outputs]
**Decision context:** [does the AI inform, recommend, or make binding decisions?]

---

**Fundamental Rights Assessment**

| Right | Impact | Risk level | Mitigating measures |
|---|---|---|---|
| Human dignity (Art. 1 CFREU) | [+/0/-] | [L/M/H] | [measure or "none required"] |
| Non-discrimination (Art. 21) | [+/0/-] | [L/M/H] | [measure — bias testing, audit] |
| Privacy (Art. 7 CFREU) | [+/0/-] | [L/M/H] | [measure — data minimisation] |
| Data protection (Art. 8) | [+/0/-] | [L/M/H] | [DPIA ref or "not applicable"] |
| Free expression (Art. 11) | [+/0/-] | [L/M/H] | [measure or "none required"] |
| Fair trial / remedy (Art. 47) | [+/0/-] | [L/M/H] | [human override mechanism] |
| Children's rights (Art. 24) | [+/0/-] | [L/M/H] | [measure or "none required"] |
| Labour rights (Art. 31) | [+/0/-] | [L/M/H] | [measure or "none required"] |

**Overall FRIA conclusion:**
- [ ] Deployment may proceed — fundamental rights impacts acceptable with mitigations
- [ ] Deployment may proceed with mandatory mitigations — [list required measures]
- [ ] Deployment must NOT proceed — unacceptable fundamental rights risk

[review — DPO and legal sign-off required]
[review — political judgement required for high-impact systems]

---

## Technical Documentation Checklist (Art. 11 + Annex IV)

**TECHNICAL DOCUMENTATION — HIGH-RISK AI SYSTEM**
**System:** [name] **Provider:** [name] **Doc ref:** TDOC-[ref]

| Annex IV Element | Status |
|---|---|
| 1. General description (purpose, use case, version) | - [ ] Complete |
| 2. Description of elements and development process | - [ ] Complete |
| 3. Information on training, validation, testing data | - [ ] Complete |
| 4. Monitoring, functioning, control information | - [ ] Complete |
| 5. Risk management system (Art. 9) | - [ ] Complete |
| 6. Description of changes in lifecycle | - [ ] Complete |
| 7. Standards applied (harmonised / other technical) | - [ ] Complete |
| 8. EU declaration of conformity (Art. 48) | - [ ] Complete / - [ ] Pending |
| 9. Post-market monitoring plan (Art. 72) | - [ ] Complete |

**Provider has provided / institution has verified:** - [ ] YES - [ ] NO — action required

---

## Constraints

### MUST DO
- Conduct the prohibited practice check (Art. 5) before any other assessment — a
  prohibited AI must not be deployed regardless of other considerations.
- Apply the Art. 6(3) rebuttal exception only with documented, specific reasoning —
  it is a narrow exception, not a default opt-out.
- Conduct a FRIA for every high-risk AI system deployed by a public body, even when
  the provider has completed a conformity assessment — the FRIA is a deployer obligation.
- Flag the EUDPR DPIA intersection whenever the AI system processes personal data —
  the AI Act and EUDPR operate in parallel, not alternatively.
- Check Art. 24 EUDPR for any AI system that produces outputs used in decisions with
  significant effects on individuals (automated decision-making provision).
- Retain AI system logs for at least 6 months as deployer (Art. 12(1) AI Act).

### MUST NOT DO
- Treat a provider's CE marking or EU declaration of conformity as a substitute for the
  institution's own deployer obligations (FRIA, human oversight, post-market monitoring).
- Classify a high-risk system as limited/minimal risk based on the provider's marketing
  description — apply the Art. 6 and Annex III criteria independently.
- Apply AI Act obligations designed for providers to the institution when it is acting
  solely as a deployer — but note that significant modifications of a third-party AI
  system can convert the deployer into a provider (Art. 25(1) AI Act).
- Conflate GPAI/foundation model obligations (Arts. 51–55) with high-risk AI obligations
  (Arts. 9–15) — they are distinct tracks that may overlap.

---

## Key Legal Framework

| Instrument | Subject | Key Provision |
|---|---|---|
| Regulation (EU) 2024/1689 (AI Act) | AI system regulation | Full framework |
| Art. 5 AI Act | Prohibited practices | Absolute prohibitions |
| Art. 6 + Annex III AI Act | High-risk classification | Two-track classification |
| Art. 9 AI Act | Risk management | High-risk AI risk management system |
| Art. 11 + Annex IV AI Act | Technical documentation | Mandatory content |
| Art. 13 AI Act | Transparency (high-risk) | Instructions for use |
| Art. 14 AI Act | Human oversight | Oversight measures and responsible person |
| Art. 15 AI Act | Accuracy, robustness, cybersecurity | Performance requirements |
| Art. 27 AI Act | FRIA | Deployer obligation — public bodies |
| Art. 50 AI Act | Transparency (limited risk) | Chatbot / synthetic content disclosure |
| Arts. 51–55 AI Act | GPAI models | Systemic risk obligations |
| Art. 72 AI Act | Post-market monitoring | Deployer logging and incident reporting |
| Regulation (EU) 2018/1725 (EUDPR) | Personal data in AI systems | DPIA (Art. 39); automated decisions (Art. 24) |

[EUR-Lex — verify current version] [model knowledge — verify AI Act implementing measures and guidance]

---

DRAFT — For review by the Data Protection Officer before use.
Not an official determination. AI Act compliance requires legal sign-off. EUDPR obligations
apply in parallel where the AI system processes personal data.
