---
name: redmonk-open-weight-decision-lenses
description: Applies RedMonk's "How to Think About Open Weight Models" (Stephen O'Grady, Sept 3 2026) — an eight-lens analytical framework (geography, licensing, capabilities, risks, economics, release timing, size, distillation) for evaluating any open-weight strategy or claim. Use when [drafting or auditing open-weight strategy content, evaluating a lab's release posture, explaining open-vs-closed dynamics, assessing distillation risk or licensing moves, or structuring a talk/blog on open AI economics]. NOT for [model benchmark selection, fine-tuning methodology, or inference hosting choices].
---

# The RedMonk Eight-Lens Framework for Open-Weight Models

## Overview
RedMonk's Sept 2026 analysis provides the field's clearest evaluation rubric for open-weight AI: models are too complex for one-dimensional open/closed judgments, but eight recurring lenses — geography, licensing, capabilities, risks, economics, release timing, size, and distillation — capture most strategic variance. The framework's baseline: the open-vs-closed race effectively began Dec 25, 2024 (DeepSeek's release; 33 days later NVIDIA shed >$0.5T of market cap), and open weights have since crossed the "good enough" threshold set by Nov 2025's Opus/ChatGPT capability jump.

## When to Use
- Structuring analysis, content, or talks about any open-weight release or lab strategy
- Auditing a lab's posture (e.g., why did this lab regress from open to closed?)
- Explaining geopolitical, licensing, or economic dynamics of open AI
- Evaluating distillation claims (which read on every other lens)
- NOT for: choosing inference providers; benchmark methodology; fine-tuning technique

## The Eight Lenses (with 2026 reference data)

### 1. Geography
With rare exceptions (Inkling/Thinking Machines, NVIDIA Nemotron), the largest and best-performing open-weight models of 2026 are Chinese in origin. OpenRouter enterprise token share from Chinese models: ~4.5% (early 2025) → **63% (a month ago)**. Downstream politics: late-July White House floated banning US companies from using Chinese models (Treasury Secretary + Science Advisor, <1 week after Kimi K3's release); within days NVIDIA's Huang posted his first-ever tweet — a letter against restrictions signed by Dell, HF, IBM, Linux Foundation, Microsoft, Mistral, Y Combinator, then OpenAI/Google; 235 companies total. Anthropic notably absent.
**Lens question:** where was this model built, and what does that imply for policy exposure and developer affinity?

### 2. Licensing
The Linux Foundation submitted OpenMDW-1.1 to the OSI in mid-August (governs 19 NVIDIA models + BAAI/IBM/Poolside); approval uncertain — 90+ message debate over triggers and definitions. Deeper problem: it is **not settled law that copyright applies to weights**, so copyright-based open-source licenses may be inapplicable — which is why distillation complaints run on ToS-violation grounds, not copyright. Of 96 models RedMonk tracks, 51% are open in some fashion. Release terms are unstable per vendor: OpenAI went open (GPT-2) → closed (GPT-3) → open (gpt-oss, 2025); Meta open-weight Llama → closed Muse Spark (promised to open, hasn't); Moonshot open K2 → restrictive K3; Alibaba opened Qwen 3.8-Max at 27B under Apache while its 2.4T cousin stays source-available-restrictive.
**Lens question:** which license, and is the vendor's open/closed line stable across versions and sizes?

### 3. Capabilities
Closed still leads some benchmarks (SWE-bench Verified: OpenAI Sol > Anthropic Opus 4.8 > K3, ~12% gap; Vals Index v2 agentic: Opus 5 first, K3 tenth). But the operative threshold is Nov 2025's capability jump: on Artificial Analysis's Intelligence Index, K3 trails Fable 5 / GPT-5.6 Sol yet is **comparable to Opus 4.8 and ChatGPT 5.5** — "good enough" arrived roughly a month before publication. In long-running agentic benchmarks (Elo, ProgramBench, SWE Marathon), open-weight models often place first. Infra limits remain (K3's 2.8T params impractical locally); economics favor open (~half the cost of Opus 4.8, ~⅓ of Fable 5).
**Lens question:** is this model past the "good enough" line for the intended workload — or are we benchmark-worshipping?

### 4. Risks
Anthropic's stated objection to open weights is guardrail absence (declined to open "Mythos"; biotech/nuclear concerns arguably overstated given practical barriers — even if malware creation cost goes to zero). Symmetric risk: during HF's defense against rogue OpenAI elements, frontier models *declined to assist* (guardrails); HF had to turn to unrestricted open-weight GLM to defend itself. And: models are software; software is inherently attainable. Open weights are not a genie that goes back in the bottle.
**Lens question:** what is the realistic risk profile — and what does the defensive-use case look like?

### 5. Economics
AWS CEO Matt Garman (re:Invent 2025): "If I spent billions to build it, I wouldn't give it away." Like open source before it, **open weights are a tactic, not a business model**. Four sustaining patterns:
- *Market creation* — IBM (services attach), NVIDIA (hardware attach via Nemotron), Alibaba/Google (cloud pull)
- *Subsidization* — high-margin ad businesses (Google, Meta) footing model costs
- *Venture funding* — Anthropic/OpenAI must grow at margins while fending off cheaper models; open-weight startups (DeepSeek, Moonshot) face the same questions harder
- *Nation-state support* — China's $8B National AI Industry Investment Fund subsidizes Alibaba/DeepSeek/Moonshot/Z.ai as instruments of its 2030 AI-superiority goal; "price dumping" accusations don't definitionally stick to open weights
**Lens question:** who is paying for this open release, and what does their business need it to do?

### 6. Release Timing
Weight-release lag has shifted from safety-driven to commercially motivated and is lengthening: Meta went same-day (Llama 2/3B) → 96 days (3.1) → indefinite (Behemoth never released); Muse Glimmer (Apache, distilled from Spark) announced with weights "coming soon" — pre-empted by a newer model also promising "soon." Current norm: **Chinese weights 10–14 days; US models 100+ days or never.** Watch whether the Chinese lag stretches.
**Lens question:** announced ≠ released — when do (did?) the weights actually ship?

### 7. Size
Chinese open models skew large (GLM, Kimi, Qwen: 70B+; K3 at 2.8T targets frontier competition and is near-impossible to run locally). US open models skew smaller/local (gpt-oss, Glimmer, Gemma, Granite 30B-and-under for on-prem enterprise). Driven by intent: frontier competition vs. enterprise deployment.
**Lens question:** is this model designed to compete at the frontier or to be deployed locally — and does that match your use?

### 8. Distillation
Training one model on another's outputs. Benign self-distillation is universal (Gemma←Gemini; Glimmer←Spark; Haiku←Opus). Distilling a *competitor* is at best frowned upon, at worst illegal — enforceable mostly as ToS violation, which is why licenses increasingly carry explicit distillation bans. Distillation reads on every other lens: geography (US accusations aimed at Chinese models), licensing (ToS not copyright), capabilities (open gains may partly be distilled), risks (capability without guardrails), economics (potentially massive cost implications), release timing (US reticence partly fear of distillation), size (self-distillation improves small models).
**Lens question:** if capability gains look suspiciously fast, what is the distillation story?

## The Net
Models change by the day; these lenses are a transient rubric, not a permanent map. Their value: any open-weight claim, release, or strategy can be stress-tested in minutes across eight dimensions instead of argued in one.

## Quick-Apply Worksheet
For a given model/release, score 1–5 (or note N/A) per lens:
1. Geography & policy exposure: ___
2. License type + stability across versions: ___
3. Past the Nov-2025 "good enough" threshold for the workload?: ___
4. Risk profile incl. defensive use: ___
5. Economics — who funds it and why: ___
6. Announced vs. released — timing gap: ___
7. Size/intent match (frontier vs. local): ___
8. Distillation exposure (as source or as target): ___

## Honest Caveats
- Author discloses RedMonk customers (Amazon, Google, IBM, Microsoft) — noted in-source.
- Point estimates (63% OpenRouter share, benchmark placements) are single-source snapshots; cross-check against mozilla-open-source-ai-state-2026 triangulation and open-weight-adoption-milestone-2026 before quoting in client work.
- The framework itself is the deliverable; specific 2026 numbers will date quickly.

## A-Tech Alignment
- **Open source:** a ready-made evaluation vocabulary for the channel's core beat — upgrades any open-weight take from opinion to structured analysis.
- **Privacy:** the licensing lens (unsettled weight copyright; ToS-based restrictions) is directly relevant to data-rights reasoning.
- **Financial freedom:** the economics lens ("tactic, not business model" + four sustaining patterns) is the sober counterweight to both hype and dismissal.
- **Practical:** the 8-lens worksheet is a repeatable scoring tool for content, advisory, and procurement conversations.

## Related Skills
- `k2-horizon-open-science-fleet-2026` — Tier-3 openness case study that scores well on every lens
- `open-weight-adoption-milestone-2026` / `mozilla-open-source-ai-state-2026` — quantitative adoption/revenue evidence to pair with the lenses
- `license-axis-business-type` / `metered-open-license-revenue-share-2026` — deep-dives on the licensing lens
- `openai-cursor-severance-case-2026` — the closed-API-dependency counterpart
- `china-open-source-llm-arr-tracker` — the economics lens, China open-source edition