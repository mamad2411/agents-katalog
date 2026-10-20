---
name: flag-speculative-statements
description: "Label verified facts, estimates, heuristics, and predictions distinctly in an analytical response."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["epistemic-tagging", "fact-checking", "speculation", "verification", "critical-thinking", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Ask AI to Flag Speculative Statements (Epistemic Tagging) (AI Skill)

## Overview
Because AI models are trained to write in a consistent, authoritative tone, they deliver a verified historical date (*"The Apollo 11 moon landing was in 1969"*) and an unverified financial estimate (*"Competitor X generates $45M in ARR"*) using the exact same confident cadence.

The **Epistemic Tagging Protocol** forces the AI to prepend explicit visual markers (`[VERIFIED FACT]`, `[HEURISTIC / ESTIMATE]`, `[SPECULATION]`) to its claims, making uncertainty instantly recognizable.

---

## The 3-Tier Epistemic Tagging Schema

```
┌─────────────────────────────────────────────────────────────┐
│                 The Epistemic Tagging System                │
│                                                             │
│  [VERIFIED FACT]    ──► Established data, code syntax, or   │
│                         explicitly quoted text in source    │
│  [HEURISTIC]        ──► Industry rule-of-thumb or standard  │
│                         statistical pattern                 │
│  [SPECULATION]      ──► Educated guess, prediction, or      │
│                         unverified market projection        │
└─────────────────────────────────────────────────────────────┘
```

---

## Master Epistemic Tagging Prompt Templates

### Pattern 1: The Tagged Market & Intelligence Brief
Use for market research, competitor teardowns, and trend forecasting:

```markdown
Analyze [COMPETITOR / MARKET TREND / TOPIC].

Formatting Directive:
Every paragraph or major bullet point MUST begin with one of these 3 epistemic tags:
- `[VERIFIED FACT]`: If supported by public SEC filings, official documentation, or verified press releases.
- `[HEURISTIC / ESTIMATE]`: If derived from industry benchmarks or standard sizing models.
- `[SPECULATION]`: If based on rumors, future projections, or AI deduction.

Do not smooth over uncertainties with confident language.
```

---

### Pattern 2: The "Admit Unknowns" Guardrail
Use for scientific, technical, or regulatory inquiries:

```markdown
Answer [QUESTION].

Constraint:
If you are uncertain about any sub-component, write: `⚠️ [UNVERIFIED: Reason for uncertainty]`. 
Do not attempt to generate plausible-sounding guesses.
```

---

## Real-World Case Study

### Scenario: Estimating a Competitor's Tech Stack & Cloud Spend

#### Un-Tagged Output (Confusing Fiction with Fact)
> *"Company ABC runs on AWS EKS with Snowflake for their data warehouse. They spend approximately $250,000 per month on cloud infrastructure and have 45 backend engineers in Eastern Europe."*
> 
> ❌ *(The user has no idea which parts are verified truths vs wild guesses).*

#### Epistemically Tagged Output (Crystal Clear Calibration)
> - `[VERIFIED FACT]`: Company ABC lists open job requisitions requiring *AWS EKS, Terraform, and PostgreSQL* (Source: Official Careers Page, Aug 2024).
> - `[HEURISTIC / ESTIMATE]`: Based on standard B2B SaaS gross margins and their last reported 150-person headcount, estimated annual AWS cloud spend is between **$1.8M and $2.5M** (~$150k-$200k/mo).
> - `[SPECULATION]`: They are likely migrating away from Redshift to Snowflake based on recent LinkedIn hiring of two Snowflake Data Architects, but this has not been publicly confirmed.

---

## Summary Best Practices
- **Use for High-Stakes Presentations**: Epistemic tags allow executives to know immediately what data can be defended in front of a board vs what is an estimate.
- **Enforce visual brackets**: Tagging in brackets (`[FACT]`) makes scanning 10x faster than reading long qualifying phrases (*"It is worth noting that we estimate..."*).
