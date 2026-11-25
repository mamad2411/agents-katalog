---
name: message-market-match-scanner
description: |
  Scores alignment between a user's existing messaging assets and the
  target market's actual language, beliefs, and buying triggers, then
  prescribes specific rewrites. Use when a user shares copy, a landing
  page, email sequence, or ad creative and asks "does this resonate",
  "why aren't conversions happening", "improve message-market fit", or
  "fix my messaging". Diagnoses copy fit — for visual attention on the
  same asset use attention-heatmap.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="message-market-match-scanner")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to load the user's ICA definitions, prior messaging audits, known audience language patterns, and any established brand voice guidelines.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- **Messaging asset(s)**: Share the copy, landing page, ad creative, email sequence, or sales page to scan (text, URL, or screenshot)
- **ICA segment**: Which specific audience segment is this messaging targeting? (If FutureProof context already contains ICA definitions, present them for confirmation)
- **Channel and stage**: Where does this asset appear in the buyer journey? (cold traffic ad, nurture email, sales page, retargeting, etc.)
- **Performance data** (if available): Current conversion rate, click-through rate, bounce rate, or qualitative feedback indicating underperformance
- **Voice-of-customer sources**: Do they have access to customer interviews, reviews, support tickets, survey responses, or community threads that reveal how the ICA actually describes their problem?

If voice-of-customer data is unavailable, flag this as a critical gap and note that the scan will rely on inferred language patterns from FutureProof context and best-practice heuristics.

## Step 3: Build the Market Language Baseline

Before scoring the messaging, construct a **Market Language Map** — a structured reference of how the ICA actually thinks and speaks:

1. **Pain articulation inventory** — Extract the exact phrases, metaphors, and emotional descriptors the ICA uses to describe the problem (sourced from voice-of-customer data, FutureProof context, or reasoned inference). Distinguish between *surface-level frustrations* (symptoms they complain about) and *deep drivers* (fears, identity threats, aspirations they may not verbalise publicly)
2. **Belief audit** — Identify the 3–5 pre-existing beliefs the ICA holds that either enable or block purchase. Categorise each as:
   - **Enabling belief** (already true, messaging should reinforce)
   - **Blocking belief** (must be dissolved before conversion)
   - **Missing belief** (must be installed through the messaging sequence)
3. **Sophistication and awareness calibration** — Place the ICA on Eugene Schwartz's awareness spectrum (Unaware → Problem-Aware → Solution-Aware → Product-Aware → Most Aware) and on the market sophistication scale (1–5). This determines the appropriate headline strategy and proof burden
4. **Competitive frame** — Identify the 2–3 alternatives the ICA is mentally comparing against (including inaction) and the decision criteria they weight most heavily

Apply any user-specific `instructions` from FutureProof context to adjust assumptions, tone preferences, or industry-specific norms.

## Step 4: Execute the Message-Market Match Scan

Score the messaging asset across eight diagnostic dimensions, each on a 1–10 scale:

### Dimension 1: Language Fidelity
Does the copy use the ICA's own words, or does it default to internal jargon, industry abstractions, or marketer-speak? Flag every instance where the asset's language diverges from the Market Language Map.

### Dimension 2: Problem Articulation Depth
Does the messaging name the problem at the level the ICA *feels* it — not just at the level the business *solves* it? Score the ratio of surface symptoms to deep drivers referenced.

### Dimension 3: Belief Sequence Integrity
Does the messaging address blocking beliefs before asking for commitment? Are enabling beliefs reinforced at the right moments? Are missing beliefs installed through evidence rather than assertion?

### Dimension 4: Awareness-Level Calibration
Is the headline strategy, lead-in, and proof structure appropriate for the ICA's actual awareness level? A product-aware audience receiving an unaware-level education piece signals mismatch, and vice versa.

### Dimension 5: Specificity and Tangibility
Are claims concrete (numbers, timelines, named outcomes) or abstract ("transform your business," "unlock your potential")? Score the ratio of specific-to-vague claims.

### Dimension 6: Competitive Differentiation
Does the messaging create a clear *category of one*, or could a prospect swap in a competitor's name without noticing? Evaluate the mechanism, origin story, or unique framing that separates the offer.

### Dimension 7: Emotional-Logical Balance
Does the asset sequence emotion and logic correctly for the channel and funnel stage? Cold traffic requires emotional entry; bottom-of-funnel requires logical justification. Score appropriateness to context.

### Dimension 8: Action Friction
Is the call-to-action congruent with the prospect's current commitment tolerance? Does the ask match the trust level established? Evaluate micro-commitments, risk reversal, and next-step clarity.

For each dimension, provide:
- Numerical score (1–10)
- 1–2 specific evidence citations from the asset
- The precise gap between what the copy says and what the Market Language Map demands

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


Produce a **Message-Market Match Report** with the following sections:

### A. Match Score Dashboard
| Dimension | Score (1–10) | Priority |
|---|---|---|
| Language Fidelity | — | — |
| Problem Articulation Depth | — | — |
| Belief Sequence Integrity | — | — |
| Awareness-Level Calibration | — | — |
| Specificity and Tangibility | — | — |
| Competitive Differentiation | — | — |
| Emotional-Logical Balance | — | — |
| Action Friction | — | — |
| **Composite Match Score** | **—/80** | — |

Priority classification: 🔴 Critical (score ≤ 4), 🟡 Improvement (score 5–7), 🟢 Strong (score ≥ 8)

### B. Market Language Map (Reference Document)
Deliver the baseline constructed in Step 3 as a standalone reference the user can reuse across future messaging projects.

### C. Critical Fixes (Top 3 Highest-Impact Rewrites)
For each fix:
- **Current copy**: exact excerpt from the asset
- **Diagnosis**: why it breaks message-market match, referencing the specific dimension
- **Rewritten copy**: full replacement text calibrated to the Market Language Map
- **Expected impact**: the conversion lever this addresses

### D. Full Rewrite of Weakest Section
Identify the single section with the lowest composite contribution to match score and rewrite it in full — preserving brand voice (from FutureProof context or user input) while maximising ICA resonance.

### E. Channel-Specific Deployment Notes
Provide 2–3 tactical notes on how the revised messaging should be adapted for the specific channel (character limits, scroll behaviour, audience temperature, platform norms).

## Step 6: Propose Experiments

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:save_experiment(skill="message-market-match-scanner", experiment={
  hypothesis: "Replacing marketer-speak headline with ICA-verbatim pain language increases click-through rate on primary CTA",
  variants: ["control: current headline and subhead", "variant: headline using exact ICA phrase from voice-of-customer data with specificity-enhanced subhead"],
  measurement: "Click-through rate and scroll depth on landing page over 14-day test window (minimum 1,000 visitors per variant)",
  expected_impact: "20–35% improvement in headline-to-CTA click-through based on language fidelity gap severity"
})
```

```
FutureProof:save_experiment(skill="message-market-match-scanner", experiment={
  hypothesis: "Inserting a blocking-belief dissolution paragraph before the offer reveal reduces page abandonment at the pricing section",
  variants: ["control: current page flow", "variant: belief-bridging paragraph inserted between social proof block and pricing section"],
  measurement: "Scroll-to-pricing completion rate and checkout initiation rate over 14-day test window",
  expected_impact: "10–20% reduction in pricing-section abandonment"
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
FutureProof:request_research(skill="message-market-match-scanner",
  query="Current voice-of-customer language patterns, objection themes, and decision triggers in [user's ICA market/industry] from review sites, Reddit, community forums, and published buyer psychology research 2024–2025",
  reason="Refresh the Market Language Map with current ICA vocabulary and emerging belief shifts to maintain message-market match accuracy across future scans"
)
```

## Step 8: Save Session

```
FutureProof:save_session(skill="message-market-match-scanner", session={
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