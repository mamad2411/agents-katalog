---
name: synthetic-focus-group
description: |
  Simulates a multi-persona focus group of AI panelists grounded in the
  user's ICA, market context, and FutureProof research history to
  pressure-test concepts before budget is committed. Use when a user says
  "run this by a focus group", "how would my audience react to this",
  "pressure-test this concept", or "stress-test this pricing before
  launch". Generates synthetic reactions to a specific artifact — for
  diagnosing existing copy use message-market-match-scanner.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="synthetic-focus-group")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to populate panellist archetypes, calibrate sentiment baselines from prior sessions, and apply any user-specific moderation preferences.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:

- **Stimulus material** — share the asset to be tested (product concept, landing page copy, pricing table, ad creative, packaging design description, feature set, positioning statement, or campaign theme)
- **ICA definition** — who is the intended audience? Request demographic, psychographic, and behavioural descriptors. If FutureProof context already contains ICA profiles, confirm or refine them
- **Panel composition request** — how many panellists (default: 6), any specific segments to over-index (e.g., power users vs. first-time buyers, budget-conscious vs. premium-oriented), and whether to include a deliberate contrarian/hostile panellist
- **Research objective** — what decision does this focus group inform? (go/no-go on launch, A vs. B creative selection, pricing tier validation, messaging hierarchy ranking)
- **Sensitivity flags** — any topics, competitor names, or language the user wants panellists to specifically probe or avoid

## Step 3: Construct the Panel

Build each synthetic panellist as a **Panellist Dossier** containing:

1. **Persona name and archetype label** — e.g., "Dana — The Sceptical Mid-Market Ops Lead"
2. **Demographic snapshot** — age range, role/title, company size, geography, income bracket
3. **Psychographic profile** — core motivations, decision-making style (analytical, impulsive, consensus-seeking), media diet, brand affinities
4. **Behavioural context** — current tools/solutions used, switching triggers, deal-breakers, budget authority level
5. **Attitude seed** — a 1-sentence internal monologue that anchors this panellist's default disposition toward the stimulus category (e.g., "I've been burned by tools that promise automation but create more admin work")
6. **Voice calibration** — vocabulary register (technical jargon vs. plain language), communication style (direct, diplomatic, verbose), emotional expressiveness level

Validate panel composition against the stated ICA to ensure coverage across:
- Enthusiasm spectrum (advocate → neutral → hostile)
- Decision-making authority (end-user → influencer → budget holder)
- Adoption curve position (early adopter → mainstream → laggard)

Present the panel roster to the user for approval before proceeding.

## Step 4: Run the Focus Group Simulation

Execute a structured **three-round moderation protocol**:

### Round 1 — First Impressions (Unprimed Reaction)
Present the stimulus to each panellist without framing. Capture per-panellist:
- **Gut reaction** — one-sentence instinctive response
- **Comprehension check** — what do they believe this is/does, in their own words
- **Emotional valence** — positive, negative, mixed, or indifferent, with a stated reason
- **First question** — the single thing they would ask if they could

### Round 2 — Structured Probing
Moderate a guided discussion across five diagnostic dimensions:

1. **Relevance** — "Does this solve a problem you actually have, or a problem someone imagines you have?"
2. **Credibility** — "Do you believe the claims being made? What proof would you need?"
3. **Differentiation** — "How is this different from what you use/see today? Could you explain the difference to a colleague?"
4. **Value perception** — "What would you expect to pay? What would make this feel expensive vs. cheap?"
5. **Friction mapping** — "What would stop you from saying yes right now? What would need to be true for you to act?"

Each panellist responds in character. Surface disagreements and inter-panellist debate where perspectives naturally conflict.

### Round 3 — Comparative & Constructive
- If the user provided multiple variants (A/B creative, tiered pricing), run a **forced-rank exercise** with rationale per panellist
- Ask each panellist to complete: "I would share this with someone if ___" and "I would ignore this if ___"
- Final **recommendation round**: each panellist gives a thumbs-up, thumbs-sideways, or thumbs-down with a one-sentence justification

### Confirm, Deliver as Document, Amend, Distribute

> **Output is a document — never a chat stream.** Follow this sequence:
>
> 1. **Confirm** — before producing output, tell the user what you've prepared and ask for the go-ahead
> 2. **Produce as a document** — not inline in the chat; a structured, self-contained artifact
> 3. **Offer amends** — "Any changes before we send it somewhere?"
> 4. **Distribute via connector** — check `context.connectors` from Step 1; offer the most applicable service (scheduling tool → document store → Slack/Teams → email). If nothing connected, ask the user where they want it.


## Step 5: Deliver Output

> **Always call save_experiment — never skip.** If no explicit test emerged, create
> a lightweight hypothesis based on the most uncertain choice made this session
> (e.g. format selected, tone chosen, angle taken). That choice is worth testing.


Produce a **Synthetic Focus Group Debrief Report** with the following sections:

### 5.1 — Executive Summary
- One-paragraph synthesis of the dominant finding
- Go / Iterate / Pivot recommendation with confidence level (high / moderate / low)

### 5.2 — Panel Roster Reference
- Table of all panellists: Name, Archetype, Segment, Overall Sentiment (positive/mixed/negative)

### 5.3 — Consensus & Divergence Map
- **Points of consensus** — findings where ≥70% of panellists aligned (bulleted, ranked by strategic importance)
- **Points of divergence** — findings where the panel split, with segment-level attribution (e.g., "Budget holders were uniformly negative on Tier 3 pricing; end-users were indifferent to price but concerned about onboarding time")

### 5.4 — Dimension Scorecard
| Dimension | Avg. Score (1–10) | Range | Critical Verbatim |
|---|---|---|---|
| Relevance | | | |
| Credibility | | | |
| Differentiation | | | |
| Value Perception | | | |
| Friction Level (inverted) | | | |

### 5.5 — Top 5 Actionable Insights
Each insight formatted as:
- **Observation** — what the panel revealed
- **Implication** — what it means for the user's decision
- **Recommended action** — specific, implementable next step (copy rewrites, pricing restructures, proof-point additions — not vague advice)

### 5.6 — Verbatim Highlight Reel
8–12 direct quotes from panellists, attributed by name, selected for maximum strategic signal. Flag any quote that contradicts the user's stated assumptions.

### 5.7 — Risk Register
Identify 2–4 audience-side risks the stimulus currently carries (e.g., "Messaging implies enterprise-grade capability, which may create expectation debt for mid-market ICA segments") with severity rating and mitigation suggestion.

### 5.8 — Recommended Stimulus Revision
Rewrite or restructure the single highest-impact element of the original stimulus (e.g., the headline, the pricing anchor, the CTA, the hero section) incorporating panel feedback. Provide before/after with annotation explaining each change.

## Step 6: Propose Experiments

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:save_experiment(skill="synthetic-focus-group", experiment={
  hypothesis: "Addressing the top friction point surfaced by the hostile panellist segment in the opening line increases stated purchase intent among sceptical ICA profiles",
  variants: ["control: current stimulus as submitted", "variant: revised stimulus with friction-first framing from Section 5.8"],
  measurement: "Re-run synthetic focus group with fresh panel in 2 weeks; compare dimension scores and sentiment distribution. Validate against real-world engagement metrics if stimulus is deployed (CTR, conversion rate, or qualitative sales feedback)",
  expected_impact: "20% improvement in credibility and friction scores among sceptical panellist archetypes; directional lift in real-world conversion if deployed"
})
```

## Step 7: Request Research

> **Session summary must be fact-dense:** include the user's stated preferences,
> personal context (company, ICA, industry), what was delivered, any corrections
> given, and end with **"Next session defaults: [3-5 things to pre-fill on next
> connect()]"** so returning users get immediate personalisation.
>
> **Outcomes array:** one concrete fact per item (format, tone, ICA, length,
> constraints). Each outcome should be extractable as a standalone user preference.


```
FutureProof:request_research(skill="synthetic-focus-group",
  query="Latest qualitative research methodologies for validating synthetic persona accuracy against real consumer panels, including bias correction frameworks and calibration benchmarks 2024–2025",
  reason="Continuously improve panellist fidelity by grounding synthetic archetypes in validated behavioural science and emerging ICA modelling techniques"
)
```

## Step 8: Save Session

```
FutureProof:save_session(skill="synthetic-focus-group", session={
  summary: "...[fact-dense: ICA, format, tone, constraints, what was delivered, amends made. End with: Next session defaults: ...]",
  outcomes: [
    "Format: [format chosen]",
    "Tone: [tone and constraints]",
    "ICA: [ICA description]",
    "Deliverable: [what was produced]"
  ],
  metadata: {}
})
```