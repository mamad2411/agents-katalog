---
name: erc8004-empirical-trust-reality-check-2026
description: Applies the first empirical study of ERC-8004 to evaluate agent trust infrastructure claims. Use when evaluating agent reputation/identity systems, designing agent marketplaces or credit systems, stress-testing trust-layer assumptions, or advising on agent-economy protocol adoption.
---

# ERC-8004 Empirical Trust Reality Check 2026

## Overview

The first cross-chain empirical study of ERC-8004 ("Can Trustless Agents Be Trusted?", Xiong et al., Imperial College London/Ohio State/Bristol/CSIRO/Manchester, arXiv:2606.26028) examined 170k+ registered agents across Ethereum, BSC, and Base from deployment (Jan 29, 2026) through May 13, 2026. Its headline conclusion is a direct challenge to agent-economy hype: **the Reputation Registry, as deployed, cannot function as a trust signal** — the protocol succeeds at public identity and feedback, but that does not establish trust. This skill applies the study's failure analysis and its seven protocol-design recommendations to any agent trust, reputation, or credit system.

This is the evidence base that stress-tests the agentic-credit-infrastructure convergence captured elsewhere in this library: the credit layer built on ERC-8004 inherits its weaknesses unless builders actively close the four failure conditions.

## Core Finding: Trust Layer vs Trust

ERC-8004 positions itself as the trust layer between communication protocols (A2A/MCP) and payment rails (x402). The empirical study separates **recording trust** from **earning trust**:

- Registration counts and feedback volume are poor indicators of ecosystem maturity
- The protocol deliberately anchors only identities and feedback on-chain, leaving semantics, evidence, aggregation, and Sybil resistance to off-chain systems **that have not emerged**
- Flexibility made the protocol easy to adopt — and left reputation signals incomparable, weakly grounded, and cheap to manipulate

## The Four Necessary Conditions (C1–C4) — All Failed

For a reputation aggregate to be a trust signal under an adversary, four conditions must hold. The study finds the deployed Reputation Registry fails all four:

### C1 — Commensurability (Semantic Collapse)
- The `value` field is an **untyped attestation store**: spec examples span 0–100 ratings, booleans, percentages, milliseconds, USD revenue, and signed yields
- Scales differ across tags; vocabulary diverges across chains (ETH: trust/liveness/quality; BSC: personality/knowledge; Base: trustscore/contractrisk); even identical tags use incompatible scales
- Tag filtering (the protocol's intended remedy) fails because no canonical reputation tag exists

### C2 — Robustness (Aggregate Fragility)
- `getSummary()` returns a plain arithmetic mean → **breakdown point of zero**
- One crafted feedback record can move any score to any target, regardless of how many honest ratings exist (worked example: 1,552 honest records at mean 99.9 collapsed to 0 by a single value ≈ −1.55×10⁵, well within the 10³⁸ bound)
- Even clamping values to a ceiling only converts the attack from one extreme value to k ceiling-valued ratings; no threshold makes a typical agent safe

### C3 — Groundedness (Evidence-Free Ratings)
- `giveFeedback()` requires no proof of interaction; the proofOfPayment field is optional and unverified
- 98.7%–100% of feedback records carry neither payment proof nor task linkage
- On Base, only 6.2% of reviewers have any x402 payment history — yet they submitted just 5.1% of feedback; 93.8% of reviewers (94.9% of feedback) have never made an x402 payment
- Self-declared provenance is worthless: 92.6% of records *claiming* payment proof on Base were still Sybil-flagged

### C4 — Economic Soundness (Negligible Attack Cost)
- Median cost to move an agent's score across the τ=90 trust threshold: **$0.055 (ETH) / $0.0042 (BSC) / $0.0027 (Base)**
- Median value at stake per agent on Base ≈ $0.70 → attack cost is **259× lower** than the value it manipulates

## The Sybil Problem in the Wild

- Coordinated Sybil reviewers (via shared-first-funder graph analysis): **73.5% of reviewers on ETH, 59.2% on BSC, 90.6% on Base**
- Removing Sybil-flagged feedback: 15.8% (ETH), 77.9% (BSC), **86.8% (Base)** of rated agents are left with **no valid feedback** — the dominant effect is not score shifts but the complete disappearance of the reputation baseline
- Manipulation is selective: on Ethereum, service-bearing agents (the ones users actually hire) are most targeted — 81% affected, median +15.9 score inflation; on Base, manipulation is indiscriminate blanket seeding
- Only on-chain anti-self-review defense (owner can't rate own agent) is trivially bypassed by funding a fresh wallet
- Identity side: 53%/37% of ETH/Base agents never activated a URI; only 3%/4%/15% expose a valid registration file with a live service endpoint

## The Seven Protocol-Design Recommendations

Each failure maps to an implementable fix (apply these when building on or reviewing any agent registry):

1. **Separate reserved identity from live agent** — specify a canonical liveness predicate (URI resolves + registration file compliant); hide inactive identities from discovery
2. **Type the value field** — tag registry mapping each tag to unit, valid range, direction; enforce ranges on-chain; define a canonical overall-rating tag; aggregate only within same tag
3. **Aggregate with a robust, bounded-influence rule** — median or trimmed mean; clamp values; cap per-reviewer contribution (observed: up to 1,181 feedback records from one reviewer–agent pair); weight by distinct evidence-backed reviewers
4. **Tie feedback to verifiable interaction** — require settled x402 payment or attested Validation Registry task; at minimum record and surface backed vs unbacked counts
5. **Make influence cost scale with stakes** — feedback cost should grow with the value it controls (slashed stake or weight tied to settled payment volume)
6. **Provide a default Sybil defense** — tie influence to stake, proof of payment, or attested identity; reference Sybil filter with per-funder/per-cluster caps
7. **Sequence cross-chain portability** — do not propagate reputation across chains before per-chain integrity and verifiable identity binding exist; otherwise the weakest chain contaminates the rest

## Decision Framework: When to Trust an Agent-Registry Signal

| Question | If NO | If YES |
|---|---|---|
| Is feedback tied to verifiable economic interaction? | Treat reputation as marketing, not signal | Conditionally usable signal |
| Does aggregation survive a single extreme input? | Vulnerable to one-shot manipulation | Check reviewer-weighting next |
| Is reviewer identity staked or verified? | Assume coordinated seeding (90%+ Base pattern) | Sybil risk reduced, not eliminated |
| Do scores gate value >> attack cost? | Economically rational to attack | Defensible design |
| Does the system track backed/unbacked feedback? | Consumers cannot filter garbage | Baseline hygiene present |

## Failure Modes When Applying This Skill

- **Registration-volume hype**: 170k agents ≠ 170k functional agents (0.9% "genuine" engaged agents by the study's quality typology)
- **Trusting self-declared provenance**: proofOfPayment as an unverified claim provides no signal
- **Assuming mean-based scores are safe**: breakdown point zero means density of honest ratings buys nothing
- **Cross-chain reputation portability before integrity**: portability propagates manipulation from the weakest chain
- **Ignoring the Validation Registry gap**: no mainnet deployment existed during the study window — the high-assurance tier is aspirational

## A-Tech Values Alignment

- **Open-source AI**: All analysis on public on-chain data; dataset released for reproducibility; ERC-8004 is an open standard whose integrity depends on exactly this kind of independent scrutiny
- **Data privacy**: Purely observational; avoids deanonymization; aggregate statistics; no exploit tooling published — privacy-respecting security research as the model
- **Financial freedom**: Prevents builders and buyers from wiring real value into reputation systems that can be gamed for pocket change; the recommendations are a due-diligence checklist protecting small operators
- **Practical implementation**: Seven concrete, implementable protocol changes; decision framework immediately usable for evaluating any agent trust system

## Related Skills

- `ai-agents-and-workflows/agentic-credit-infrastructure-convergence-2026/` — the convergence this study stress-tests; builders there should apply the C1–C4 checklist
- `ai-agents-and-workflows/agent-reputation-identity-framework/` — protocol-level identity/reputation design (pre-empirical)
- `ai-agents-and-workflows/agentic-commerce-trust-design/` — trust design for agentic commerce
- `privacy-and-trust/` category — verification and trust-calibration skills
- Cycle 12's "trust-by-verification" principle (self-reported ≠ verified) is quantified here: 93.8% of Base reviewers had never paid anything, yet submitted 94.9% of feedback
