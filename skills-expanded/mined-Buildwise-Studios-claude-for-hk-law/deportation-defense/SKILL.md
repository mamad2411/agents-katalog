---
name: deportation-defense
description: >
  Guide legal practitioners through deportation risk assessment, representation, and defense under sections 20–25 of the Immigration Ordinance (Cap 115), including deportation order challenges, Immigration Tribunal appeals, and judicial review.
---
# Deportation Defense — Skill

## Purpose

Guide legal practitioners through deportation risk assessment, representation, and defense under sections 20–25 of the Immigration Ordinance (Cap 115), including deportation order challenges, Immigration Tribunal appeals, and judicial review.

## Scope

- Grounds for deportation (ss.20–25 Cap 115)
- Deportation vs removal distinction
- Notice of Intention to Make a Deportation Order
- Representations and mitigation
- Deportation Order consequences
- Appeal to the Immigration Tribunal
- Judicial review of deportation decisions
- Post-deportation return bans

## Workflow

### 1. Identify the Legal Basis

Determine whether the matter involves deportation or removal:

| Ground | Deportation (s.20–25) | Removal (s.53) |
|--------|----------------------|----------------|
| **Trigger** | Criminal conviction (2+ years); conducive to public good | Overstay; illegal entry; breach of conditions |
| **Decision-maker** | Chief Executive or Director of Immigration | Director of Immigration |
| **Consequences** | Deportation Order; permanent return ban | Removal Order; no automatic return ban |
| **Appeal** | Immigration Tribunal (28 days) | No statutory appeal; judicial review only |

### 2. Assess Risk Factors

**High-risk indicators:**
- Offence punishable by 2+ years imprisonment (automatic consideration)
- Serious crime: drugs, violence, organised crime, sexual offences
- Multiple convictions (even if each below 2 years)
- Document fraud or identity deception
- Adverse security assessment
- Deportation history from any jurisdiction

**Mitigating factors:**
- Length of lawful residence in HK
- Family ties (spouse, children, dependent relatives)
- Employment and community ties
- Age at entry (long-term resident since childhood)
- Health conditions (medical needs, risk of harm if deported)
- Human rights considerations (Art 8 ECHR / BL Art 28)
- Risk of persecution or torture on return

### 3. Notice of Intention

- **Form and timing:** Director issues a formal letter inviting representations
- **Representation period:** Usually 28 days (may be shortened in urgent cases)
- **Contents:** Statement of grounds, supporting evidence (conviction record, immigration history)
- **Detention pending decision:** May apply under s.25(1) — applicant may be detained

### 4. Drafting Representations

**Structure:**
1. Preliminary submissions (jurisdiction, procedural fairness)
2. Factual background (immigration history, criminal proceedings, family circumstances)
3. Mitigation arguments (personal circumstances, rehabilitation, character evidence)
4. Human rights analysis (proportionality, family life, non-refoulement)
5. Supporting evidence (affidavits, letters, medical reports, employment records)
6. Proposed alternative (supervision, reporting conditions, time-limited permission)

**Key arguments:**
- **Proportionality:** Deportation must be proportionate to the offence
- **Family life:** Art 23 BL / Art 8 ECHR principles; **The "B" v Secretary for Security [2019]** factors
- **Rehabilitation:** Evidence of reform, good conduct, remorse
- **Non-refoulement:** Credible risk of torture or inhuman treatment on return (BL Art 28, CAT)
- **Delay:** Lapse of time since the offence may weigh against deportation

### 5. Deportation Order

- Issued by the Chief Executive (s.20: criminal conviction grounds)
- Issued by the Director of Immigration (s.25: conducive to public good)
- Order takes effect from date of service
- Person may be detained pending removal
- Return ban: indefinite (no statutory right of return)

### 6. Appeal to the Immigration Tribunal

- **Notice of appeal:** Within 14 days of the Deportation Order (shorter than standard 28 days)
- **Grounds:** Error of fact, procedural unfairness, irrationality, failure to consider relevant factors
- **Hearing:** Oral hearing (usually held); legal representation permitted
- **Bail pending appeal:** May be granted (discretionary; strict conditions)
- **Decision:** Tribunal may affirm, vary, or quash the order

### 7. Judicial Review

- **Grounds:** Illegality, irrationality, procedural impropriety, legitimate expectation
- **Leave requirement:** O.53 RHC; must establish arguable case
- **Bail pending JR:** Application to CFI
- **Expedited hearing:** Available in detention cases

## Key Case Law

- **Secretary for Security v Tang Kwok Wah (2002)** — proportionality in deportation
- **The "B" v Secretary for Security [2019] HKCFI** — family life factors in deportation
- **R v Director of Immigration, ex parte Ng Kam-hung [1996]** — standard of review
- **Re Aziz Ul Haq [2010] HKCA** — non-refoulement and CAT obligations
- **Wong Hau v Torture Claims Appeal Board [2020]** — risk on return analysis

## Practice Notes

- Distinguish between deportation and removal at the earliest stage — they have very different consequences
- The 14-day appeal window for deportation is non-extendable — act immediately
- Detention reviews should be pursued aggressively — challenge unlawful detention
- For clients without HKID, consider whether they are eligible for a Recognizance Paper if not detained
- Collect mitigation evidence early — before the Deportation Order is signed
- Human rights arguments under BL Art 28 (freedom from torture) may be stronger than Art 8 (family life) in drug/trafficking cases
- Post-deportation: No automatic right of return — application for permission required (ad hoc, rarely granted)


## HK primary sources (run before citing)

Run from the **cloned `claude-for-hk-law` repo root** (see `references/hk-primary-sources-setup.md`). Before citing a Cap, rule, or case, run scripts **in this session** and tag: `[HK e-Legislation / DOJ open data]`, `[HKLII search]`, `[Judiciary site search]`, or `[model knowledge — verify]`. No HKLII/CLIC MCP is shipped.

```bash
python3 scripts/download_legislation_list.py --cap <cap>
python3 scripts/download_legislation_text.py <cap>
python3 scripts/hklii_search.py "<query>" --cases --limit 10
python3 scripts/judiciary_search.py "<query>" --limit 10
```
