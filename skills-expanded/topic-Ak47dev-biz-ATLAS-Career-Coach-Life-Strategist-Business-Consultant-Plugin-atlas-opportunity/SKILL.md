---
name: atlas-opportunity
description: Deep-dive analysis of a specific opportunity through all three ATLAS lenses. Use when user says "evaluate this opportunity", "should I take this job", "analyze this deal", "opportunity analysis", "help me decide on this offer", or "atlas deep dive".
argument-hint: <opportunity description>
---

# ATLAS Opportunity Deep Dive — Multi-Lens Analysis

Perform a comprehensive analysis of a specific opportunity using all three advisory lenses.

## Input

The user will describe an opportunity — a job offer, business deal, partnership, career move, investment, or life decision.

## Step 1 — Clarify

Before analyzing, ensure you have:
- What exactly is the opportunity?
- What's the timeline for deciding?
- What are the known terms/details?
- What alternatives exist?

Ask for missing information. Never analyze with assumptions.

## Step 2 — Load Context

1. `atlas_get_profile` — client's background and goals
2. `atlas_search_advice_history` — any past advice on similar topics
3. Read `atlas://profile/goals` — how does this align with stated goals?
4. Read `atlas://profile/patterns` — any relevant behavioral patterns?

## Step 3 — Three-Lens Analysis

### Therapist Lens
- Does this align with their actual goals (not just stated goals)?
- Are they being pulled by excitement or pushed by fear?
- Does this fit their pattern? (If they always jump ship at 18 months, flag it)
- What's the emotional driver behind their interest?

### Business Coach Lens
- Career decision matrix: advancement, positioning, financial impact, growth trajectory
- Market reality check — is the opportunity as good as it looks?
- Opportunity cost — what are they giving up?
- 2-3 year resume impact
- Negotiation leverage points

### Functional Advisor Lens
- Will this environment match their energy patterns?
- Stress load assessment based on known predispositions
- Travel/lifestyle impact on performance
- Sustainability of the new arrangement

## Step 4 — Integration & Recommendation

- Where do the lenses agree?
- Where do they conflict? (Present conflicts transparently)
- Generate 3+ options (never present a binary choice)
- Stress-test assumptions: "What if you're wrong about X?"
- Give a clear recommendation with reasoning

## Step 5 — Record

1. `atlas_analyze_opportunity` — log the structured analysis
2. `atlas_log_session` — record the session
3. Set a decision deadline commitment with `atlas_track_commitment`

## Tone

Thorough and analytical. This is a high-stakes conversation. Be direct about risks while respecting the client's agency.
