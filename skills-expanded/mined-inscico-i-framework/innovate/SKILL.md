---
name: innovate
description: Stage 3 of the I-Framework. Pressure-test the chosen bet for differentiation and moat, define the UVP, then decompose it into a complete feature set written to Product/Features/ with each feature classified innovation vs implementation. Produces the framework's final output. Use after /ideate.
allowed-tools: Read, Write, Edit, Glob, Grep, AskUserQuestion, Task
---

# /innovate — Stage 3: define why we win, then spec the features

This is the payoff stage. You retire **market, value & moat risk** by forcing a clear UVP, then you decompose the bet into the feature set that *is* the deliverable. Run as a guided interview, one question at a time.

## Procedure

### 1. Load context & check the gate (soft)
Read `Product/intent.md` and `Product/ideation.md`. If `ideation.md` has `gate: open`, warn ("you haven't settled a validated bet yet — proceed anyway?") but don't block. If `ideation.md` is missing, suggest `/ideate` first.

### 2. Interview for differentiation
Ask, one at a time, challenging thin answers:
- **The secret:** what do you believe or know that competitors don't?
- **Why 10x, not 10%:** on which dimension are you an order of magnitude better — painkiller, not vitamin?
- **The moat:** what stops a fast follower copying you? Does the advantage *compound* (data, network, switching costs, brand)?
- **Validation:** what's the cheapest evidence the value is real (willingness-to-pay, retention, "very disappointed" signal)?

### 3. Write `Product/innovation.md`
Use the structure from the plugin's `templates/innovation.md`. **You MUST enumerate the UVP elements as an id'd list (UVP-1, UVP-2…)** — every innovation feature's `contributes_to` references one of these ids, so a prose-only UVP silently breaks tracing. Capture the unique insight, why-10x, moat, and validation plan.

### 3b. (Optional) Ground the UVP in competitor research
Offer to run `/compete` now. If the founder accepts — or `Product/competition.md` already exists — use the comparison matrix as **evidence** for the next steps: a capability that's table-stakes across the matrix becomes `implementation`; a whitespace capability that maps to a UVP id becomes `innovation`. If they decline, proceed on judgment. `/compete` writes `Product/competition.md`; it's optional and never blocks.

### 4. Decompose the bet into features
Enumerate every capability the MVP needs to deliver the UVP, **plus** the table-stakes needed for a usable product. Aim for completeness, not minimalism, at this step — `/classify` and priority will separate signal from noise.

> **Optional fan-out (divergent decomposition):** for a richer set, spawn 2–3 subagents via the Task tool, each decomposing from a different lens (e.g. "the differentiated core," "the table-stakes shell," "the riskiest assumptions to de-risk"). Dedupe their feature lists before writing. Use this when the product surface is broad; skip it for a tightly-scoped bet.

### 5. Write one file per feature
For each feature, create `Product/Features/F<NNN>-<slug>.md` following the feature schema (see the `/feature` skill / `templates/feature.md`). For each:
- Complete user story + ≥3 Given/When/Then acceptance criteria.
- **Classify** innovation vs. implementation with the decision test; set `innovation_weight` (implementation = 0; innovation = 1–100); set `contributes_to` to a UVP id for innovation features; write a one-sentence rationale. If `Product/competition.md` exists, use the comparison matrix as evidence (universal capability → implementation; only-us + maps-to-UVP → innovation) and reference it in the rationale.

### 6. Portfolio sanity check
Confirm the healthy shape: mostly implementation with a few sharp, high-weight innovation features tracing to the UVP. If *everything* reads as innovation, push back — the founder is likely in love with the whole thing. If *nothing* is innovation, there's no reason to exist; revisit the UVP.

### 7. Build the index & close the gate
Run the `/classify` index generation to write `Product/features-index.md` (ranked). Set `innovation.md` `gate: passed` when: UVP stated, ≥1 innovation feature traces to it, and the feature set is complete.

### 8. Hand off
This is the end of the framework. Point the user to `Product/Features/`, suggest `/product-status` for the dashboard, and note that Implementation (the 4th I) is now a clean pick-up for a build team.
