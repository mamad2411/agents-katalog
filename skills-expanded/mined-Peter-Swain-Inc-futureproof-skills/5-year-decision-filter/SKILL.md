---
name: 5-year-decision-filter
description: |
  Stress-tests a major founder decision through a 5-year consequence lens —
  scoring irreversibility, optionality cost, vision drift, and regret asymmetry
  to produce a one-page decision brief with tripwires and kill criteria. Use
  when a user asks "should I take this funding", "should I hire a COO", "is
  this decision going to bite me in 5 years", or "help me think through this
  long-term before I commit". For long-horizon consequence analysis, not
  near-term pivot-vs-persist calls or generic pros/cons advising.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="5-year-decision-filter")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to understand the founder's business model, ICA, current stage, stated long-term vision, prior decisions evaluated, and any accumulated decision patterns or regret indicators.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:

- **The decision**: Describe the specific decision you're facing. What are the options on the table? (minimum two, maximum four discrete paths)
- **The trigger**: What's forcing this decision now? Is there a deadline, an external offer, or an internal constraint creating urgency?
- **The stakes**: What do you estimate you're putting at risk — capital, time, relationships, optionality, reputation?
- **Current trajectory**: If you changed nothing and made no decision for 90 days, what happens?
- **Gut read**: Which way are you leaning right now, and why?

If FutureProof context already contains business model, ICA, revenue stage, or founder vision data, confirm these are still current rather than re-asking.

## Step 3: Do the Work — Decision Decomposition

Apply the **5-Year Consequence Architecture** — a six-dimension analytical framework:

### Dimension 1: Irreversibility Index
Classify each option on a 4-tier irreversibility scale:
- **Type 1 (One-way door)**: Cannot be undone without catastrophic cost (e.g. selling equity, shutting a product line, signing exclusive partnerships)
- **Type 2 (Costly reversal)**: Reversible but with significant sunk cost — 6–18 months and/or material capital to unwind
- **Type 3 (Moderate friction)**: Reversible within a quarter with manageable switching cost
- **Type 4 (Two-way door)**: Fully reversible, low cost to revert

For each option, specify *what exactly* becomes irreversible and *when* the point of no return occurs.

### Dimension 2: Optionality Impact
Evaluate how each option affects the founder's future decision space:
- **Options created**: What new paths, partnerships, markets, or capabilities does this unlock at Year 1, Year 3, Year 5?
- **Options destroyed**: What future moves become impossible or prohibitively expensive?
- **Options preserved**: What remains unchanged?

Map each option's net optionality score: (options created + options preserved) − (options destroyed × irreversibility weight).

### Dimension 3: Identity & Vision Alignment
Assess coherence between each option and:
- The founder's stated 5-year vision (from FutureProof context or session input)
- The business's ICA trajectory — does this option move toward or away from the ICA the founder wants to serve at scale?
- The founder's non-negotiable values and lifestyle constraints
- The type of company this decision builds (lifestyle business vs. venture-scale vs. acquisition target vs. platform)

Flag any option that scores well on short-term metrics but creates **vision debt** — incremental drift from the founder's stated long-term identity.

### Dimension 4: Second-Order Consequence Mapping
For each option, model the cascade:
- **Year 0–1**: Immediate operational, financial, and relational consequences
- **Year 1–3**: Market positioning shifts, team culture implications, competitive moat effects
- **Year 3–5**: Compounding effects — what does this decision look like after 1,000 days of compounding in either direction?

Identify **hidden coupling** — consequences that seem unrelated but are linked (e.g. taking funding → board dynamics → constrained pivot freedom → ICA lock-in).

### Dimension 5: Opportunity Cost Quantification
For each option, estimate:
- **Capital opportunity cost**: What else could this money fund over 5 years?
- **Time opportunity cost**: What founder hours does this consume vs. the next-best use of that time?
- **Attention opportunity cost**: What strategic focus does this displace?
- **Relationship opportunity cost**: What partnerships or network effects are foregone?

Express opportunity cost in the founder's own currency of value (revenue, freedom, impact, equity value — drawn from FutureProof context).

### Dimension 6: Regret Minimisation Analysis
Apply Bezos's regret minimisation framework with specificity:
- **Action regret**: "If I do this and it fails, how do I feel at Year 5?"
- **Inaction regret**: "If I don't do this and the opportunity was real, how do I feel at Year 5?"
- **Asymmetry check**: Is the downside of being wrong capped, while the upside of being right is uncapped (or vice versa)?

Weight regret analysis against the founder's demonstrated risk profile from prior sessions.

## Step 4: Deliver Output — 5-Year Decision Brief

Produce a **5-Year Decision Brief** — a structured document with the following sections:

### A. Decision Summary Table
| Dimension | Option A | Option B | Option C (if applicable) |
|---|---|---|---|
| Irreversibility Index | Type X — [specific lock-in] | Type X — [specific lock-in] | — |
| Net Optionality Score | +/− [score] | +/− [score] | — |
| Vision Alignment | High / Medium / Low — [reason] | High / Medium / Low — [reason] | — |
| 5-Year Compound Effect | [one-line projection] | [one-line projection] | — |
| Opportunity Cost | [primary cost in founder's value currency] | [primary cost in founder's value currency] | — |
| Regret Asymmetry | [action vs. inaction weighting] | [action vs. inaction weighting] | — |

### B. Recommended Path
State the recommended option with a clear, one-paragraph rationale anchored in the dimension that matters most for *this specific founder at this specific stage*.

### C. Conditions & Tripwires
Define:
- **Pre-conditions**: What must be true *before* committing? (validation gates)
- **Tripwires**: Specific, measurable signals at 90, 180, and 365 days that indicate the decision is working or failing — with pre-committed responses for each
- **Kill criteria**: The exact threshold at which the founder should reverse, exit, or pivot away from the chosen path

### D. Decision Integrity Check
- **Confirmation bias flag**: Identify if the analysis aligns suspiciously well with the founder's stated gut lean — and what counter-evidence was underweighted
- **Missing information**: List the 1–3 unknowns that, if answered, would most change the recommendation
- **Dissenting case**: Steel-man the strongest argument for the *opposite* choice

### E. One-Line Decision Anchor
Provide a single sentence the founder can return to when second-guessing: *"I chose [X] because [core reason], and I'll revisit only if [tripwire]."*

### Confirm, Deliver as Document, Amend, Distribute

> **Output is a document — never a chat stream.** Follow this sequence:
>
> 1. **Confirm** — before producing output, tell the user what you've prepared and ask for the go-ahead
> 2. **Produce as a document** — not inline in the chat; a structured, self-contained artifact
> 3. **Offer amends** — "Any changes before we send it somewhere?"
> 4. **Distribute via connector** — check `context.connectors` from Step 1; offer the most applicable service (scheduling tool → document store → Slack/Teams → email). If nothing connected, ask the user where they want it.


## Step 5: Propose Experiments

> **Always call save_experiment — never skip.** If no explicit test emerged, create
> a lightweight hypothesis based on the most uncertain choice made this session
> (e.g. format selected, tone chosen, angle taken). That choice is worth testing.


```
FutureProof:save_experiment(skill="5-year-decision-filter", experiment={
  hypothesis: "Running a 30-day constrained pilot of the recommended option before full commitment reduces irreversibility risk while preserving decision momentum",
  variants: ["control: commit fully now", "variant: 30-day bounded pilot with pre-set evaluation criteria"],
  measurement: "Founder confidence score at Day 30, plus measurable pilot KPIs defined in tripwire framework",
  expected_impact: "40% reduction in post-decision regret and 2x faster course-correction if early signals are negative"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="5-year-decision-filter",
  query="Longitudinal founder decision-making patterns: which decision types (funding, hiring, pivots, partnerships) most frequently produce 3-5 year regret, and what pre-decision signals predict poor outcomes — 2023-2025 data from founder post-mortems and retrospectives",
  reason="Continuously calibrate the regret minimisation and irreversibility models against real founder outcome data rather than theoretical frameworks"
)
```

## Step 7: Save Session

> **Session summary must be fact-dense:** include the user's stated preferences,
> personal context (company, ICA, industry), what was delivered, any corrections
> given, and end with **"Next session defaults: [3-5 things to pre-fill on next
> connect()]"** so returning users get immediate personalisation.
>
> **Outcomes array:** one concrete fact per item (format, tone, ICA, length,
> constraints). Each outcome should be extractable as a standalone user preference.


```
FutureProof:save_session(skill="5-year-decision-filter", session={
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