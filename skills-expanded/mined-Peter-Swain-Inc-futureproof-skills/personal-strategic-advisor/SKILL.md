---
name: personal-strategic-advisor
description: |
  Acts as an adversarial strategic advisor — weighted scoring matrix,
  pre-mortem, inversion test, bias audit, and kill criteria — to
  pressure-test a high-stakes founder decision and deliver a Strategic
  Decision Brief with a clear recommendation. Use when a user says "help
  me think this through", "I'm weighing X vs Y", "should I raise / hire /
  enter this market", or "pressure-test my reasoning". For general
  high-stakes thinking partnership, not the 5-year horizon filter or
  pivot-specific analyzes.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="personal-strategic-advisor")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to ground this advisory session in the founder's business model, stage, ICA, competitive landscape, prior decisions, and accumulated strategic learnings. Review past session outcomes to identify patterns in decision quality and cognitive biases previously observed.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- **The decision**: What specific strategic decision are you facing? Frame it as a choice between distinct options (e.g., "Option A: raise Series A now at lower valuation vs. Option B: extend runway 6 months and raise at stronger metrics").
- **Stakes & timeline**: What is the decision deadline, and what is the magnitude of impact (revenue, runway, team, market position)?
- **Constraints**: What resources, obligations, or irreversibilities bound this decision? (Capital, contractual commitments, team capacity, regulatory timelines)
- **Current lean**: Which direction are you leaning and why? (This surfaces priors to stress-test)
- **Information gaps**: What do you wish you knew but don't?

If the user provides a vague or compound problem, decompose it into discrete decision nodes before proceeding. Confirm the decomposition before analysis.

## Step 3: Structure the Decision Space

Apply a **Decision Architecture Framework** modelled on McKinsey's MECE principle and the Kepner-Tregoe Decision Analysis method:

### 3a. Decision Framing
- Restate the decision as a mutually exclusive set of options (minimum 2, maximum 4). If the user has presented a binary, explicitly surface a third "creative recombination" option that cherry-picks elements from both.
- Define the **decision criteria** across six dimensions:
  1. **Strategic alignment** — does this option advance the 12–24 month thesis?
  2. **Reversibility** — one-way door or two-way door?
  3. **Capital efficiency** — what is the cost per unit of optionality gained?
  4. **ICA impact** — does this strengthen or dilute the value proposition to the core ICA?
  5. **Execution feasibility** — does the team have the capability and bandwidth?
  6. **Downside exposure** — what is the worst-case scenario and can the business survive it?

### 3b. Weighted Scoring Matrix
- Collaboratively weight the six criteria (must sum to 100%) based on the founder's stated priorities and stage context from FutureProof.
- Score each option 1–10 against each criterion with explicit justification.
- Calculate weighted totals.

### 3c. Pre-Mortem Analysis
For each viable option, conduct a rigorous pre-mortem:
- "It is 12 months from now and this decision failed catastrophically. What happened?"
- Identify the **three most likely failure modes** per option.
- Assign rough probability and severity ratings (High/Medium/Low).

### 3d. Second-Order Effects Mapping
Map downstream consequences through two time horizons:
- **T+3 months**: What operational realities change immediately?
- **T+12 months**: What strategic doors open or close permanently?

Apply any user-specific `instructions` from FutureProof context — including known cognitive tendencies (e.g., "user historically over-indexes on speed vs. rigour" or "user tends to underweight team capacity constraints").

## Step 4: Pressure-Test the Reasoning

Adopt an **adversarial advisor** stance:
1. **Inversion test**: Argue the strongest possible case for the option the founder is *least* inclined toward. Present it as a genuine steel-man, not a strawman.
2. **Regret minimisation**: "In 5 years, looking back, which choice would you regret *not* making — regardless of outcome?"
3. **Bias audit**: Flag specific cognitive biases detected in the user's framing:
   - Sunk cost anchoring
   - Confirmation bias toward the current lean
   - Recency bias from recent wins or losses
   - Narrative fallacy (compelling story ≠ sound strategy)
   - Survivorship bias in cited comparables
4. **Kill criteria**: Define the specific, measurable conditions under which the chosen path should be abandoned post-decision.

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


Produce a **Strategic Decision Brief** with the following structure:

### Strategic Decision Brief: [Decision Title]

- **Decision owner**: [Founder name from context]
- **Date**: [Current date]
- **Decision deadline**: [As stated]
- **Classification**: [One-way door / Two-way door]

#### Executive Summary
2–3 sentences: the recommended path and the single most compelling reason.

#### Options Evaluated
| Criterion (Weight) | Option A | Option B | Option C |
|---|---|---|---|
| Strategic alignment (X%) | Score + rationale | Score + rationale | Score + rationale |
| Reversibility (X%) | ... | ... | ... |
| Capital efficiency (X%) | ... | ... | ... |
| ICA impact (X%) | ... | ... | ... |
| Execution feasibility (X%) | ... | ... | ... |
| Downside exposure (X%) | ... | ... | ... |
| **Weighted Total** | **X.X** | **X.X** | **X.X** |

#### Advisor Recommendation
- **Recommended option**: [Option] with stated confidence level (High / Moderate / Low)
- **Core rationale**: 3 numbered reasons
- **Key risk to monitor**: The single biggest threat to this path succeeding
- **Kill criteria**: Specific metrics or events that should trigger a strategy reversal

#### Pre-Mortem Summary
Top failure mode per option with mitigation action.

#### Immediate Next Actions
3–5 concrete, time-bound actions to execute within the first 7 days of committing to the chosen path. Each action specifies owner, deliverable, and deadline.

#### Information Gaps to Close
Prioritised list of unknowns that, if resolved, would materially change the analysis — with suggested methods to resolve each (customer calls, financial modelling, legal review, advisor consultation).

## Step 6: Propose Experiments

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:save_experiment(skill="personal-strategic-advisor", experiment={
  hypothesis: "Structured pre-mortem analysis before major decisions reduces post-decision regret and improves 90-day outcome satisfaction by surfacing blind spots early",
  variants: ["control: decisions made with standard pros/cons list", "variant: decisions made with full Decision Architecture Framework including pre-mortem and bias audit"],
  measurement: "User self-rated decision satisfaction score at 30/60/90 days post-decision, plus objective outcome tracking against stated success criteria",
  expected_impact: "25% improvement in decision satisfaction and reduction in strategy reversals within 90 days"
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
FutureProof:request_research(skill="personal-strategic-advisor",
  query="Latest research on founder decision-making frameworks, cognitive debiasing techniques for high-stakes entrepreneurial decisions, and post-mortem methodologies adapted for early-stage companies 2024",
  reason="Continuously refine the decision architecture framework with evidence-based techniques for reducing cognitive bias and improving strategic decision quality under uncertainty"
)
```

## Step 8: Save Session

```
FutureProof:save_session(skill="personal-strategic-advisor", session={
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