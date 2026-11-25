---
name: privacy-engineering
description: Covers the engineering side of privacy, including privacy by design pragmatically, data minimization, the DPIA/PIA process, when to reach for which privacy-enhancing technology (pseudonymization, differential privacy, etc.), and the NIST Privacy Framework. Use when the user asks how to build privacy into a product, run a DPIA, minimize or de-identify personal data, or choose a PET.
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# Privacy engineering

This is the **build** side: how to design and ship systems that handle personal data safely. The **law** (GDPR/NIS2/DORA triggers, clocks, penalties) lives in `load_skill privacy-eu`: cross-link, don't repeat it here. Privacy engineering = making the legal obligation true in the code and data flows.

## Privacy-by-design, pragmatically (Cavoukian's 7, de-jargoned)

1. **Proactive not reactive**: design the control in, don't bolt it on post-incident.
2. **Privacy as the default**: opt-in, minimal collection, tightest sharing by default. The user does nothing and is still protected.
3. **Embedded in design**: a backlog item with an owner, not a sign-off gate.
4. **Full functionality (positive-sum)**: reject the false "privacy vs. utility" trade; find the design that does both.
5. **End-to-end lifecycle protection**: collect → process → store → share → **delete**. Retention + deletion are part of the design, not an afterthought.
6. **Visibility & transparency**: make data flows auditable; what you claim in the privacy notice must match what the code does.
7. **Respect for the user**: honor access/deletion/portability rights as product features, not legal chores.
   Operationalize via: a **data-flow map / RoPA**, **purpose limitation** tags on each field, and a **retention schedule** enforced by automated deletion jobs.

## Data minimization (the highest-leverage control)

- **Don't collect it** → nothing to breach, report, or delete. The cheapest control by far.
- Per field ask: do we need it, for what purpose, for how long? No purpose → drop it.
- **De-identify early**: tokenize/pseudonymize at ingestion so downstream systems never see raw identifiers.
- **Aggregate / sample** when you only need statistics, not rows.
- **Short retention** with automated expiry beats indefinite storage "just in case."

## DPIA / PIA process

A DPIA is **mandatory** when processing is "likely to result in high risk". Art. 35(3) auto-triggers: large-scale **special-category** data, **systematic monitoring** of public areas, or **automated profiling with legal/significant effect**. EDPB lists 9 risk criteria; **≥2 → do a DPIA**. Run it _before_ processing, early in design. verify: https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/accountability-and-governance/data-protection-impact-assessments-dpias/when-do-we-need-to-do-a-dpia/

Steps: 1) **Describe** the processing + data flows systematically. 2) **Necessity & proportionality**: is there a less-invasive way? 3) **Assess risks** to data subjects (likelihood × severity). 4) **Mitigations**: controls, PETs, safeguards. 5) **Residual risk** sign-off; consult the DPA if still high. Treat it as a living doc; re-run on material change. (Legal obligation/timelines: `load_skill privacy-eu`.)

## PETs: when to reach for which

- **Tokenization / pseudonymization**: swap identifiers for non-sensitive tokens, reversible via a guarded vault. Use for **operational systems** that must still join/lookup records (payments, healthcare IDs). Still personal data under GDPR if re-identifiable; not a get-out-of-jail card.
- **k-anonymity (+ l-diversity / t-closeness)**: generalize quasi-identifiers so each record hides in a group of ≥k. Use for **static dataset release/sharing**. Pick k for the utility/risk balance; weak against homogeneity + background-knowledge attacks; layer l-diversity.
- **Differential privacy**: add calibrated noise; bounds what any single record leaks (ε budget). Use for **aggregate stats / analytics / ML training** where you publish results, not rows. Accept some accuracy loss; tune ε.
- **Federated learning**: train across decentralized data, raw data never centralizes. Use for **cross-org / on-device ML** (healthcare, mobile). Combine with DP: gradients/updates still leak; FL alone isn't private.
- **Synthetic data**: model-generated stand-in for dev/test/sharing when real data isn't needed. Validate it doesn't memorize/leak originals.
- **Confidential compute** (homomorphic encryption, secure MPC, TEEs): compute on encrypted/partitioned data. Heavier; reach for it when you must process data you're not allowed to see in clear (cross-party analytics, regulated joins).
  Rule: **minimize first** (cheapest), then de-identify (tokenize/k-anon), then add noise/decentralize (DP/FL), then confidential compute (last resort, costly).

## NIST Privacy Framework

Voluntary, risk-based, **CSF-compatible** companion for privacy risk. v1.0 (2020) → **v1.1**: realigns to **CSF 2.0**, adds a **Govern** function and an **AI + privacy** section; use guidelines moved to an online FAQ. (Still an **Initial Public Draft**: IPD released Apr 2025, comments closed Jun 2025; not finalized as of mid-2026, so cite it as draft and confirm status.) verify: https://www.nist.gov/privacy-framework/new-projects/privacy-framework-version-11

- Functions: **Identify-P, Govern-P, Control-P, Communicate-P, Protect-P**: pair it with CSF so one program covers privacy _and_ security risk (overlap: data inventory, access control, incident response).
- Use it to structure the program; use the **DPIA** to assess a specific processing activity; use **PETs** as the mitigations.

## Pairs with

- The regulation/obligation/clock side: `load_skill privacy-eu` (don't duplicate law here).
- Mapping privacy controls onto your CSF/ISO set: `load_skill control-mapping`.
- Building privacy controls into the pipeline (secrets, data-handling gates): `load_skill devsecops`.
