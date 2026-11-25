---
name: aigov-vendor-ai-review
version: 1.0.0
description: Review a third-party AI product's contract, DPA, and documentation for governance and liability risk before procurement or renewal.
author: matrixx0070
tags: [ai-governance, vendor-review, contracts, liability, dpa, supply-chain]
capabilities: []
---

## When to use

Use this before you buy, pilot, or renew a third-party or embedded AI product — an API, a SaaS feature with AI inside, or a model you call — when you need to know what governance and liability risk the terms carry. It reads the contract/MSA, the DPA, and the vendor's documentation to answer: what do they train on, who owns inputs and outputs, who indemnifies whom, and who wears the EU AI Act obligations. The output is a clause red-flag table with an ask and a fallback for each.

**Not for:** sorting whether a use case is high-risk in the first place (use aigov-use-case-triage), running the deep impact assessment on your own deployment (use aigov-aia-generation), building the register of AI you already run (use aigov-ai-inventory), mapping regulatory duties to internal controls (use aigov-reg-gap-analysis), authoring policy (use aigov-policy-starter), or standing up the matter file for a specific engagement (use aigov-matter-workspace).

This skill is decision-support, not legal advice. Clause flags and suggested fallbacks are negotiation inputs; a qualified attorney must review the actual contract and any redlines before you sign, rely on, or file anything with legal stakes.

## Method

1. Gather the full set: MSA/order form, DPA, AI-specific terms/AUP, security docs, model/system card, and any subprocessor list — flag missing artifacts as gaps.
2. Classify the relationship under the EU AI Act: is the vendor the provider and you the deployer, or does your configuration make you a provider? **Decision:** if your use pushes you into provider duties (substantial modification, own branding, high-risk purpose), the review scope widens sharply — flag and escalate.
3. Trace the data path: what the vendor trains or fine-tunes on (your data? your prompts? outputs?), retention, deletion on exit, and any human review of your content.
4. Trace IP: who owns inputs, who owns outputs, and whether outputs carry an infringement indemnity.
5. Score risk allocation: warranty scope vs disclaimers, indemnification (IP, data breach), liability caps and carve-outs, and model-substitution/deprecation notice.
6. Check operational governance: security controls, subprocessors and change notice, compliance attestations, and audit rights. **Decision:** if the use is high-risk (per triage) but the vendor refuses provider duties or audit, mark not-ready and escalate.
7. Emit the red-flag table: each flag with the ask (what you want) and the fallback (minimum acceptable), plus an overall go / conditions / no-go.

## Example

Vendor API for a customer-support assistant. DPA silently allows "use of Customer Data to improve the Services" → training on your prompts. Output terms: "as-is, no IP indemnity." Liability capped at 1 month of fees with a data-breach carve-out absent. EU AI Act: vendor disclaims any provider role. Red flags: training-on-prompts (ask: opt-out + no-train default; fallback: contractual no-train for prompt data), output infringement (ask: IP indemnity; fallback: warranty + defense cooperation), cap (ask: super-cap for breach/IP; fallback: 12-month fees floor with breach carve-out). Overall: conditions — do not sign until training and cap are fixed; attorney to redline.

## Pitfalls

- **Reading the MSA, ignoring the DPA and AUP.** The training-rights and retention landmines usually live in the data-processing addendum, not the headline contract.
- **Accepting "we don't train on your data" verbally.** If it isn't a binding, default-on contractual term, it isn't a control.
- **Ignoring model-substitution clauses.** A vendor swapping the underlying model with no notice can break your validation and compliance posture overnight.
- **Letting the vendor disclaim its EU AI Act provider role by fiat.** Role allocation follows the facts and the Act; a one-line disclaimer does not move duties onto you cleanly, and it does not relieve you of deployer obligations.

## Output format

```
VENDOR AI REVIEW (decision-support, not legal advice) — <vendor/product> — <date>
DOCS REVIEWED: MSA[ ] DPA[ ] AI-terms[ ] security[ ] model-card[ ] subprocessors[ ]  | MISSING: <...>
EU AI ACT ROLE: vendor=provider? <y/n>  you=deployer/provider? <which>  RISK TIER (from triage): <...>

CLAUSE RED-FLAG TABLE
| Clause | Finding | Severity | Ask | Fallback |
|--------|---------|:--------:|-----|----------|
| Training on your data | <...> | H/M/L | <...> | <...> |
| Output IP / indemnity  | <...> | | | |
| Liability cap/carve-out | <...> | | | |
| Model substitution/notice | <...> | | | |
| Retention / deletion / exit | <...> | | | |

OVERALL: go | conditions | no-go
CONDITIONS TO CLEAR: <blocking items>
ATTORNEY ESCALATION: <redlines / role-allocation / high-risk items>
```

## Reference

Vendor AI review is governed by two lenses: contract clause flags (with a bias toward training-data and liability terms) and NIST AI RMF GOVERN's third-party/supply-chain risk. Clause names below are common patterns; the operative language always controls, so counsel must read the actual document.

### Training-data and data-rights flags

| Flag | Why it matters | Ask / fallback |
|------|----------------|----------------|
| **Training on customer data/prompts** | Your inputs improve the vendor's model; possible leakage of secrets across tenants | Ask: no-train by default, contractual, all data types. Fallback: opt-out + no-train for prompts and outputs |
| **Retention & deletion** | Data lingers past need; unclear exit deletion | Ask: defined retention + deletion on termination with certification. Fallback: deletion within N days on request |
| **Human review of content** | Staff/labelers see your data | Ask: disclose + restrict + confidentiality. Fallback: opt-out of human review for sensitive data |
| **Subprocessors** | Data flows to unnamed fourth parties | Ask: published list + change notice + flow-down terms. Fallback: notice and right to object |

### IP and liability clause flags

| Flag | Why it matters | Ask / fallback |
|------|----------------|----------------|
| **Output IP ownership** | Ambiguity over who owns generated outputs | Ask: customer owns outputs. Fallback: broad license + no vendor claim to your outputs |
| **Output infringement indemnity** | Generated output may infringe third-party IP | Ask: IP indemnity covering outputs. Fallback: defense cooperation + warranty against known infringement |
| **Warranty disclaimers** | "As-is" shifts all quality/accuracy risk to you | Ask: accuracy/performance warranty + SLA. Fallback: fitness warranty for the documented purpose |
| **Liability cap** | Cap too low to cover realistic breach/IP loss | Ask: super-cap or uncapped for breach/IP/confidentiality. Fallback: 12-month-fees floor with breach carve-out |
| **Liability carve-outs** | Breach/IP/confidentiality wrongly inside the cap | Ask: standard carve-outs above the cap. Fallback: at minimum data-breach and IP indemnity carved out |
| **Model substitution/deprecation** | Vendor swaps or retires the model without notice, breaking validation | Ask: material-change + deprecation notice (e.g. 90 days) + version pinning. Fallback: notice + right to terminate on material change |
| **Confidentiality** | Prompts/outputs not treated as confidential | Ask: your inputs/outputs are Confidential Information. Fallback: mutual NDA covering all submitted data |

### EU AI Act role allocation (provider vs deployer)

The **provider** develops/places the system on the market and carries the heavy duties (conformity assessment, risk management, technical documentation, logging, post-market monitoring). The **deployer** uses it and carries operational duties (use per instructions, human oversight, input-data relevance, monitoring, some transparency). Roles follow the facts: substantially modifying a high-risk system, putting your name on it, or repurposing it to a high-risk use can make **you** a provider regardless of a contractual disclaimer. Confirm which role each party holds, get the provider to accept its duties in writing (documentation, conformity evidence, instructions for use), and do not let a boilerplate disclaimer silently push provider obligations onto you.

### Mapping to NIST AI RMF GOVERN (third-party / supply-chain)

GOVERN is the RMF function that establishes accountability and risk culture, and it explicitly covers third-party and supply-chain risk. For a vendor review that means: documented policies for acquiring AI, mechanisms to inventory and monitor third-party components (link to aigov-ai-inventory), contractual allocation of responsibilities, and the ability to hold vendors accountable through attestations and audit rights. A vendor that cannot evidence its own governance (model card, security attestations, subprocessor transparency, incident notice) is itself a GOVERN gap.

### Compliance attestations and exit

Ask for current security attestations (e.g. SOC 2 / ISO 27001), data-residency commitments, incident-notification timelines, and audit or audit-report rights. On exit, require data return/deletion certification, portability of your configuration/fine-tunes where applicable, and reasonable transition assistance — lock-in with no export path is a governance and liability risk in its own right. All of the above are negotiation inputs; a qualified attorney must review the contract and redlines before signing.
