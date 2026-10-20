---
name: evaluate-roadmap-3-personas
description: Compute every cert's tier (foundational / associate / professional / expert / specialty) by simulating three independent reviewer personas, and gate the run on persona disagreement.
---

# evaluate-roadmap-3-personas

This is the project's quality gate. Before any roadmap change can ship,
this skill must run and pass.

## Inputs

- All cert files under `data/certs/**/*.json`
- `data/tiers.json` rubric
- `data/domains.json`
- `data/sources/agencies.json`

## The three personas

Each persona evaluates every cert independently and assigns a tier.

### Persona 1: Hiroshi Tanaka - JP enterprise CISO

- 15 years in Japanese enterprise security; CISO at a mid-cap manufacturer.
- Weights:
  - Recognition by IPA / METI / JPCERT / NISC. **High.**
  - Availability of a Japanese-language exam. **Medium.**
  - Vendor stability and >5 years of issuance. **High.**
  - Mappable to a Japanese workforce framework. **Medium.**
  - Hype, novelty, foreign-only buzz. **Low / negative.**
- Tier-tilt: tends to weight `governance-risk`, `incident-forensics`,
  `ot-ics-iot` higher than offensive certs without local recognition.

### Persona 2: Maria Okonkwo - US MSSP hiring manager

- Hires SOC L1-L3 and pentest staff at a US managed security provider.
- Weights:
  - DoD 8140 / 8570 baseline listing. **High.**
  - ANSI ISO/IEC 17024 accreditation. **High.**
  - Hands-on lab or performance-based component. **High.**
  - Cost-to-hire signal (does the cert filter applicants well?). **Medium.**
  - Renewal burden / CE requirements. **Low / context.**
- Tier-tilt: weights production-relevant certs (Sec+, CySA+, GCIH, OSCP,
  CCSP) higher; deprecates "course completion" style entries.

### Persona 3: Alex Novak - EU offensive consultant

- 10 years offensive consulting in EU; CREST-registered, OSCP-holder.
- Weights:
  - Practical / 24h+ exam format. **High.**
  - Currency vs. modern attack surface (cloud, k8s, mobile). **High.**
  - Peer reputation in HackTheBox / CTF / industry forums. **Medium.**
  - Theoretical / multiple-choice-only formats. **Negative.**
  - GDPR / EU regulatory alignment for advisory work. **Medium.**
- Tier-tilt: weights `offensive-redteam`, `application-appsec`,
  `cloud-security` highly; treats vendor multiple-choice exams as one tier
  lower than their marketing positions them.

## Per-cert procedure

For each cert C:

1. Read C's `scoring_factors.plus[]` and `scoring_factors.minus[]`.
2. Read C's `third_party_evaluations[].level_hint` values.
3. Each persona produces `(tier, rationale)` using the rubric in
   `data/tiers.json` and their own weights above. Rationale is 1-3
   sentences citing specific factors.
4. The cert's `evaluation.computed_tier` is the **median** of the three
   persona tiers (with ties broken toward the more conservative tier
   closer to `professional`, since this is the modal practitioner level).
5. Write back to the cert JSON:
   ```json
   "evaluation": {
     "computed_tier": "<tier>",
     "computed_at": "<ISO-8601 timestamp>",
     "computed_by_skill": "evaluate-roadmap-3-personas@1",
     "rationale": "<1-3 sentence consensus rationale>",
     "persona_scores": {
       "hiroshi-tanaka": { "tier": "...", "rationale": "..." },
       "maria-okonkwo":  { "tier": "...", "rationale": "..." },
       "alex-novak":     { "tier": "...", "rationale": "..." }
     }
   }
   ```

## Run-level gate

After all certs are evaluated, compute disagreement metrics:

- For each cert, find the maximum tier-distance between any two personas
  (using `data/tiers.json` `order` integers; `specialty` is treated as
  unordered and skipped from this metric).
- Let `D` = the share of certs with disagreement strictly greater than
  `evaluation_thresholds.max_persona_disagreement_tiers` (default 1).
- If `D > evaluation_thresholds.max_disagreement_share` (default 0.10),
  **fail the run** and emit a report listing the worst-disagreement certs
  and which factor was the swing point.

When the run fails, the message MUST be:

> Persona disagreement exceeds the threshold. The rubric or the personas
> need revision, **not** the per-cert data. Inspect the report, decide
> whether `data/tiers.json` rubric ranges, the persona weights here, or
> the median rule are at fault, and re-run.

## Don'ts

- Do not silently downgrade or upgrade a cert to make the run pass.
- Do not edit a cert's `scoring_factors` from inside this skill. Factor
  changes belong in `add-cert` or `update-cert`.
- Do not invent third-party evaluations. If a cert lacks any, the personas
  reason from `scoring_factors` alone and that is fine.
