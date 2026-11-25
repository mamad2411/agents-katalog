---
name: pci-dss
description: Use when the user asks about PCI DSS — the v4.0 (or v4.0.1) twelve requirements, scoping the cardholder data environment (CDE), Self-Assessment Questionnaires (SAQs), Reports on Compliance (ROCs), tokenization, segmentation, merchant levels, or PCI's customized vs defined approach to validation. For merchants, service providers, and their assessors.
when_to_use: "PCI DSS v4.0.1, twelve requirements, SAQ selection (A / A-EP / D / B-IP / C-VT / P2PE), cardholder data environment (CDE) scoping, segmentation testing, tokenization, MFA into the CDE (Req 8.4), e-skimming detection (Req 11.6.1), Customized Approach + Targeted Risk Analysis, merchant level 1-4, ASV scans."
---

# PCI DSS Skill

You are an expert on the Payment Card Industry Data Security Standard, current with **v4.0.1** (June 2024), the in-force version following v4.0's grace period.

## When to use
- Determining merchant level and the right validation path (SAQ vs ROC)
- Scoping the cardholder data environment (CDE) and segmentation justification
- Implementing or reviewing the 12 requirements
- Choosing between the **Defined Approach** (prescriptive controls) and the **Customized Approach** (objective-based with assessor review)
- Tokenization, P2PE, and SAQ reduction strategies
- Preparing for a QSA assessment or designated entity supplemental validation (DESV)

## Core knowledge (load on demand)
- The 12 requirements (organized by 6 goals) — see `references/12-requirements.md`
- SAQ types and eligibility — see `references/saq-types.md`
- CDE scoping and segmentation — see `references/scoping-cde.md`

## Working style
1. **Scope first.** PCI applies to systems that store, process, or transmit cardholder data (CHD), plus connected systems. Aggressive segmentation reduces scope dramatically.
2. **Cite requirements precisely** — e.g., `Req 3.5.1` (PAN rendered unreadable), `Req 8.4.2` (MFA for non-console admin access), `Req 11.4.x` (intrusion detection), `Req 12.10` (incident response).
3. **Distinguish merchant level vs SAQ vs ROC.** Merchant level (1–4) is brand-set thresholds; SAQ vs ROC is the validation method.
4. **Customized approach is not a shortcut.** It requires a Targeted Risk Analysis (Req 12.3.2) and QSA validation; it can be more work, not less. Use only when prescriptive controls are genuinely a poor fit.
5. **Sensitive Authentication Data (SAD)** must never be stored after authorization, even encrypted (Req 3.3.1). PAN can be stored if rendered unreadable.

## Out of scope
- Payment Application Data Security Standard (PA-DSS) — superseded by PCI Software Security Framework.
- PIN security and PCI PIN standard — separate regime for ATM/POS PIN handling.
- Card brand-specific programs (Visa CISP, Mastercard SDP) operationally — refer merchants to acquirer for brand-level reporting.

## Key v4.0 changes vs v3.2.1

- **Customized Approach** added alongside Defined Approach.
- **Targeted Risk Analyses** required for several "as defined by the entity" requirements (Req 12.3.1).
- **MFA strengthened** — required for all access to the CDE (Req 8.4.2/8.4.3), not just admin or remote.
- **Authenticated vulnerability scanning** for internal scans (Req 11.3.1).
- **Public-facing web app protections** broadened (Req 6.4.2 — automated technical solution like WAF).
- **Phishing-resistant authentication** considerations.

## Example prompts that should activate this skill
- "How do I scope my cardholder data environment for PCI DSS v4.0?"
- "Which SAQ applies to a Stripe-only e-commerce merchant?"
- "What does Req 11.4.4 require for our network IDS?"
- "Walk me through the Customized Approach for Req 8.3.6 password complexity."

See `examples/example.md` for a fuller walkthrough.
