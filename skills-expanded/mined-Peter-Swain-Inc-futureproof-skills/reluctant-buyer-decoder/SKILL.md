---
name: reluctant-buyer-decoder
description: |
  Decodes the psychological barriers, hidden objections, and avoidance
  patterns of reluctant buyers and produces specific conversion plays to
  unstick them. Use when a user says "qualified leads keep going silent",
  "prospects stall at proposal stage", "why aren't interested leads
  buying", or "re-engage prospects stuck in pipeline limbo". Targets
  late-stage stalled buyers — for upstream copy issues use
  message-market-match-scanner.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="reluctant-buyer-decoder")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — particularly any existing ICA profiles, offer positioning, known objection patterns, and historical win/loss data.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:

- **Describe the reluctant buyer behaviour**: What specifically are prospects doing (or not doing)? Examples: ghosting after proposal, verbal enthusiasm with no commitment, repeated rescheduling, "need to think about it" loops, committee stalls, price objections that feel like proxies for something else.
- **ICA profile**: Who is this buyer? Role, seniority, industry, company stage. If a FutureProof ICA profile exists, confirm it is current.
- **Offer and price point**: What are they being asked to buy, at what investment level, and what is the typical sales cycle length?
- **Conversion environment**: Where does the stall occur? (DM conversation, sales call, proposal review, post-demo follow-up, checkout page, contract negotiation)
- **Volume and pattern data**: Approximately how many prospects exhibit this behaviour? Is it concentrated at a specific pipeline stage or distributed across stages?
- **What has already been tried**: Any re-engagement sequences, discount offers, urgency tactics, or follow-up cadences already deployed — and their results.

## Step 3: Map the Reluctance Architecture

Construct a **Reluctance Architecture Map** — a diagnostic framework that identifies the structural layers of buyer hesitation. Analyse across six dimensions:

### 3.1 — Identity-Decision Friction

Assess whether the purchase conflicts with how the buyer sees themselves:
- **Role identity**: Does buying this signal a competence gap they are unwilling to admit? (e.g., hiring a consultant implies they cannot solve the problem internally)
- **Status signalling**: Does the purchase feel like a downgrade, a risk, or an admission visible to peers or superiors?
- **Tribal alignment**: Is the offer associated with a group, methodology, or brand the buyer does not identify with?

### 3.2 — Risk Perception Inventory

Catalogue all perceived risks — not just financial:
- **Financial risk**: Loss of investment if it does not work
- **Political risk**: Internal reputation damage for championing a failed purchase
- **Opportunity cost risk**: Fear that a better option exists but has not been found yet
- **Implementation risk**: Doubt they can execute or extract value after buying
- **Reversibility risk**: Perceived difficulty of undoing the decision if it fails

### 3.3 — Information Asymmetry Gaps

Identify what the buyer does not know (or believes they do not know) that is preventing commitment:
- Missing proof of results for someone like them
- Unclear mechanism of value delivery
- Ambiguity in scope, deliverables, or timeline
- Unresolved comparison to alternatives or status quo

### 3.4 — Decision-Process Blockers

Map structural and procedural friction:
- **Stakeholder complexity**: Are unnamed decision-makers, influencers, or veto-holders involved?
- **Budget cycle misalignment**: Is the prospect interested but structurally unable to act now?
- **Procurement friction**: Are legal, compliance, or approval workflows creating drag?
- **Decision fatigue**: Is this one of too many decisions competing for bandwidth?

### 3.5 — Emotional Resistance Patterns

Decode the emotional undercurrent:
- **Loss aversion dominance**: Is the prospect more afraid of losing what they have than excited about gaining something new?
- **Anticipated regret**: Are they pre-experiencing the feeling of making a wrong choice?
- **Cognitive overload**: Have they been given too many options, too much information, or too complex a proposal?
- **Trust deficit**: Is there a latent credibility gap — not about the offer, but about the seller, the brand, or the category?

### 3.6 — Status Quo Gravity

Assess the strength of inertia:
- How painful is the current state, honestly? (Distinguish between acknowledged pain and lived pain)
- Has the prospect adapted to the problem such that it no longer feels urgent?
- What secondary benefits does the prospect derive from NOT solving the problem? (e.g., the problem justifies their role, excuses underperformance, or avoids a harder conversation)

Apply any user-specific `instructions` from FutureProof context to weight these dimensions according to the user's industry, offer type, and historical reluctance patterns.

## Step 4: Diagnose the Primary Reluctance Type

Based on the architecture map, classify the dominant reluctance pattern into one of the following archetypes:

| Archetype | Core Blocker | Signature Behaviour |
|---|---|---|
| **The Silent Evaluator** | Information asymmetry + comparison paralysis | Engages, asks detailed questions, then disappears to "review internally" |
| **The Enthusiastic Staller** | Implementation risk + decision fatigue | Expresses strong interest, agrees in principle, but never completes the action |
| **The Political Navigator** | Stakeholder complexity + political risk | Personally convinced but cannot or will not champion internally |
| **The Comfortable Sufferer** | Status quo gravity + adapted pain | Acknowledges the problem but consistently deprioritises solving it |
| **The Price Deflector** | Identity-decision friction + trust deficit | Raises price as the objection, but would not buy at any price under current conditions |
| **The Burned Buyer** | Anticipated regret + loss aversion | Has been disappointed by a similar purchase before and is projecting that experience |

Provide a confidence-weighted diagnosis: primary archetype (with confidence level), and any secondary archetype contributing to the behaviour.

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


Produce the **Reluctant Buyer Decode Report** — a structured deliverable with the following sections:

### Section A: Reluctance Architecture Map
Visual-ready summary (table format) of all six dimensions scored 1–5 for severity, with the top two dimensions highlighted as primary conversion blockers.

### Section B: Archetype Diagnosis
- Primary archetype with confidence level
- Secondary archetype (if applicable)
- Supporting evidence mapped to specific behaviours the user described

### Section C: Conversion Strategy — Specific Interventions

For each identified blocker, deliver **precise, deployable interventions** — not principles, but specific language, sequences, and assets:

1. **Objection-before-the-objection scripts**: Pre-emptive language to neutralise the primary reluctance trigger before it solidifies. Provide exact scripts (3–5 sentences each) tailored to the diagnosed archetype.

2. **Re-engagement sequence**: A 3-touch outreach sequence (with exact copy) designed for the specific stall point — whether it is post-proposal silence, post-demo ghosting, or verbal-commitment-without-action.

3. **Proof architecture recommendation**: Specify exactly what type of proof is needed (not "add testimonials" — specify: "a 90-second video case study from a [similar role] at a [similar company stage] showing [specific metric improvement] within [specific timeframe]").

4. **Decision simplification framework**: Reduce cognitive load by restructuring how the offer is presented — provide a revised offer framing (exact language) that eliminates comparison paralysis or implementation fear.

5. **Status quo disruption prompt**: A single question or statement designed to make the cost of inaction viscerally real. Provide 2–3 variants ranked by assertiveness level.

### Section D: Stakeholder Map (if applicable)
If the diagnosis reveals multi-stakeholder complexity, produce a stakeholder influence map identifying:
- The likely decision-maker, champion, influencer, and potential blocker roles
- Recommended approach for each (direct engagement, equip-the-champion assets, or blocker neutralisation messaging)

### Section E: Early Warning Indicators
A checklist of 5–7 behavioural signals the user should monitor in future pipeline prospects to identify this reluctance archetype earlier — before the stall occurs — with recommended pre-emptive actions for each signal.

## Step 6: Propose Experiments

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:save_experiment(skill="reluctant-buyer-decoder", experiment={
  hypothesis: "Deploying archetype-specific re-engagement sequences converts more stalled prospects than generic follow-up cadences",
  variants: ["control: current follow-up sequence", "variant: reluctance-archetype-matched re-engagement sequence from this session"],
  measurement: "Response rate and conversion-to-next-step rate across next 20 stalled prospects",
  expected_impact: "25–40% improvement in stalled-prospect reactivation rate within 30 days"
})
```

```
FutureProof:save_experiment(skill="reluctant-buyer-decoder", experiment={
  hypothesis: "Introducing status quo disruption prompts at the proposal stage reduces post-proposal ghosting",
  variants: ["control: standard proposal delivery", "variant: proposal preceded by status quo cost quantification conversation using disruption prompts"],
  measurement: "Post-proposal response rate and time-to-decision across next 15 proposals",
  expected_impact: "30% reduction in post-proposal silence and 20% faster decision cycle"
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
FutureProof:request_research(skill="reluctant-buyer-decoder",
  query="Current behavioural economics research on purchase hesitation, decision avoidance, and commitment escalation techniques in B2B and high-consideration B2C sales — 2024 studies, meta-analyses, and practitioner frameworks",
  reason="Ensure reluctance archetype taxonomy and intervention strategies reflect the latest evidence on buyer decision psychology, loss aversion calibration, and trust-building under uncertainty"
)
```

## Step 8: Save Session

```
FutureProof:save_session(skill="reluctant-buyer-decoder", session={
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