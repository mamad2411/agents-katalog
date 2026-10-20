---
name: bolt-forge-consent-training-corpus
description: Applies Bolt.new's Bolt Forge (Sept 14, 2026 research preview) — the first consumer-scale consent-based data-for-compute barter in a coding-agent product — where users trade anonymized build sessions (secrets stripped, validated pipeline) for up to 50× usage allocation, feeding a signed DPA-governed pipeline to Arcee AI to train a trillion-parameter-class open-weight model. Use when [designing consent-gated data-for-compute exchanges, pricing training-data access in barter form, evaluating "allocation instead of credits" pricing, or auditing the anonymization pipeline of an opt-in training corpus]. NOT for [per-token data marketplace pricing (see prompt-data-barter-pricing-muse-spark), enterprise VPC-hosted fine-tuning (see smaug-fine-tuned-agentic-models), or the usage-vs-revenue gap analysis (see mozilla-open-source-ai-state-2026)].
---

# Bolt Forge: Consent-Gated Data-for-Compute Barter in a Consumer Coding Agent

## Overview
Bolt Forge (launched Sept 14,  opted-in Forge sessions flow through an anonymization pipeline (secrets stripped, validated against seeded test data) into a signed data processing agreement with Arcee AI — an open-model lab behind Apache-2.0 Trinity models — to train a trillion-parameter-class open-weight model whose weights publish back. **The allocation is the payment**: builders get ~91% of the top paid model's quality (92.2 vs 101.0 on Bolt's Build Index) at up to 50× the usage, and the product pays for it by converting consented user sessions into a training corpus for open weights.

## When to Use
- Designing a consent-gated "trade your sessions for compute" product surface
- Auditing an opt-in training-corpus pipeline (consent UX, anonymization, DPA, publish-back)
- Evaluating "allocation instead of per-token credits" as a pricing model for agentic coding products
- Deciding which workloads belong on open models vs paid premium agents

## Core Process / Workflow
1. **Three-agent product line with a consent gate as the pricing lever.** Forge sits beside two private agents (Standard/Max) that never train on user data. The consent screen fires **every time** a user enters Forge; declining keeps them in their usual agents, nothing shared. Consent is a per-session gate, not a buried ToS.
2. **Anonymize before it leaves.** Prompts, code, and fix traces are stripped of secrets/PII by default before leaving the platform; the pipeline is validated against seeded test data.
3. **Governed handoff to a data-processing partner.** Arcee AI receives anonymized sessions under a signed DPA; the resulting model is Apache-2.0-class open-weight and publishes its weights.
4. **Publish-back closes the loop.** What builders help train, they can download and run. The corpus builds a public asset, not a private moat.
5. **The trade table.** What Forge buys: brainstorms/MVPs stop competing with production credits; 91% of top-model quality at Pro-tier inclusion; one monthly bar (no daily limits, hard stop, no overage billing); and a stake in the trained weights.
6. **What it buys the vendor.** Predictable reserved-capacity cost structure + consented corpus for open-model training + a research-preview signal (Bolt Lite waitlist closing Oct 14).

## Key Evidence
- Launch: Sept 14, 2026 research preview; open-model lineup GLM 5.3 Flash (default), GLM 5.3, Kimi K3, DeepSeek v4 Pro (experimental).
- Quality trade: open models score 92.2 vs 101.0 for the top paid model on Bolt's Build Index — **~91% of the top paid model's score** (Sept 2026).
- Allocation: up to 50× more usage at no extra cost for individual Pro plans through Oct 14; single monthly bar, no daily limits, hard stop instead of overage.
- Cost structure: Forge runs on Bolt's own reserved hardware + WebContainers browser runtime — fixed, predictable cost makes the allocation economically possible.
- Context: Stanford HAI AI Index 2025 — inference costs fell **280× in 18 months**, the collapse that makes a 50× allocation economically possible; Arcee's Trinity family is Apache-2.0.
- Data partner: signed DPA with Arcee AI; first training run in October 2026.

## Pairs-with
- `prompt-data-barter-pricing-muse-spark` (per-token data pricing; Forge is the **consent-gated barter** form)
- `privacy-first-ai-pipeline-defense` (anonymization-first posture this operationalizes)
- `consent-fatigue-progressive-permissioning` (per-session consent UX)
- `federated-consent-architecture-agent-systems` (consent-bearing data surfaces in agent products)
- `privacy-preserving-local-ai` (the fully-local alternative this complements)
- `smaug-fine-tuned-agentic-models` (enterprise fine-tune on agent traces — the B2B sibling)
- `mozilla-open-source-ai-state-2026` (harness-layer thesis this instantiates)

## A-Tech Alignment
- **Open source:** weights publish back; Arcee's Trinity family is Apache-2.0; the consent-gated barter pattern is implementable by any OSS product.
- **Privacy:** per-session consent, secrets/PII stripped by default, DPA-governed transfer, validated pipeline — the cleanest consent-first data-for-compute design in the coding-agent market.
- **Financial freedom:** "allocation instead of credits" lets solo builders experiment at 50× volume without overage bills; the trade is visible at the point of consent.
- **Practical:** the five-step Forge workflow is a template for any agent product considering a data-for-compute surface.

## Honesty Caveats
- Research preview through Oct 14, 2026; the Forge allocation is a launch offer, not a permanent pricing commitment.
- Open models in Forge are experimental inside Bolt; the vendor's own guidance says keep complex production work in the Standard/Max agents.
- Kimi K3 and DeepSeek v4 Pro burn through the allocation faster than the GLM pair — the 50× framing is an upper bound, not a guaranteed multiplier.
- Forge can't take PDF uploads yet; production builds stay on private agents.
- The "91%" quality claim is Bolt's own Build Index benchmark, not an independent evaluation.

*Sources: Bolt.new Forge launch post (Sept 14, 2026); Bolt Build Index (Sept 2026); Arcee AI partnership disclosures; Stanford HAI AI Index 2025.*