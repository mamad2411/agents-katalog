---
name: company-culture-doc-builder
description: |
  Builds a living company culture document that codifies values, behaviors, and
  rituals into one shareable artifact aligned with strategy. Use when the user
  says "write our company culture doc", "create a values framework", "draft team
  operating principles", "we need a culture handbook", or describes cultural
  drift while scaling. For the externally-facing identity and behavioral norms
  document, not legal HR policy (employee-handbook-builder).
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="company-culture-doc-builder")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — particularly any existing company values, prior culture work, organisational structure, ICA profiles (for employer branding alignment), and leadership tone preferences.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- **Organisation snapshot**: Company name, headcount, stage (pre-seed → enterprise), industry, and geography (single-site, hybrid, fully remote, multi-region)
- **Current state**: Do they have an existing culture doc, values list, or handbook? If so, share it for audit
- **Catalyst**: What prompted this work? (scaling pain, M&A integration, founder codification, attrition signal, onboarding inconsistency, rebrand)
- **Aspirational culture archetype**: What companies or teams do they admire culturally, and why?
- **Leadership voice**: Who signs the culture doc — founder, CEO, People team, collectively? What tone should it carry? (candid, warm, provocative, institutional)
- **Known tensions**: Any cultural contradictions they already feel — e.g. "we say we're innovative but punish failure," "we value autonomy but micromanage"
- **Audience & distribution**: Who will read this? (all-hands, new hires only, public careers page, investors, board)

## Step 3: Conduct the Culture Diagnostic

Before drafting, run a structured diagnostic across six dimensions adapted from the Competing Values Framework (Quinn & Rohrbaugh) and Schein's three levels of culture:

### 3a. Artefacts & Rituals Inventory

Catalogue observable cultural signals:
- **Communication norms**: meeting cadence, async vs. sync defaults, tool stack (Slack culture, email culture, Loom culture)
- **Decision-making patterns**: consensus, RACI, founder-decree, distributed authority
- **Recognition & celebration**: how wins are acknowledged (publicly, privately, financially, symbolically)
- **Physical/digital environment**: office design, remote workspace norms, Slack channel taxonomy
- **Hiring signals**: what the interview process actually selects for vs. what it claims to

### 3b. Espoused Values vs. Enacted Values Gap Analysis

For each value the user provides (or claims to hold):
| Espoused Value | Evidence It's Enacted | Evidence It's Contradicted | Gap Severity (1–5) |
|---|---|---|---|
| e.g. Transparency | All-hands financials shared monthly | Layoff decisions made without warning | 4 |

Flag any value with a gap severity ≥ 3 as a **credibility risk** — these must be addressed honestly in the culture doc or removed.

### 3c. Competing Values Quadrant Mapping

Position the organisation across four quadrants:
1. **Collaborate** (clan) — mentorship, belonging, team cohesion
2. **Create** (adhocracy) — experimentation, speed, risk tolerance
3. **Compete** (market) — results orientation, external benchmarking, urgency
4. **Control** (hierarchy) — process rigour, compliance, predictability

Identify the **dominant quadrant**, the **aspirational quadrant**, and any **under-indexed quadrant** that may be causing dysfunction.

### 3d. Subculture Mapping

For organisations >50 people, identify departmental or geographic subcultures that diverge from the core. Flag where divergence is healthy (e.g. engineering's deep-focus norms) vs. corrosive (e.g. sales team dismissing product values).

## Step 4: Synthesise the Values Architecture

Using diagnostic outputs, construct a values architecture with three tiers:

1. **Core Values (3–5 maximum)**: Non-negotiable beliefs that are true today and must remain true at 10× scale. Each must pass the **Scott Test**: would you retain an employee who violates this value even if they're a top performer? If no, it's not core — it's aspirational.

2. **Operating Principles (5–8)**: Behavioural translations of core values into daily decision-making heuristics. Format: *"When [tension], we [choice] because [value]."* These resolve the ambiguity that values alone cannot.

3. **Cultural Rituals & Mechanisms**: The systems that reinforce values without relying on willpower — onboarding ceremonies, feedback cadences, promotion criteria, offboarding practices, storytelling traditions.

For each core value, deliver:
- **Definition**: One sentence, jargon-free, unmistakable
- **What it looks like**: 3 concrete observable behaviours
- **What it doesn't mean**: 2–3 common misinterpretations or shadow-side risks (e.g. "Candour doesn't mean cruelty")
- **Tension partner**: The competing value it must be balanced against (e.g. Speed ↔ Craft)
- **Litmus-test scenario**: A specific, difficult situation and how this value resolves it

### Confirm, Deliver as Document, Amend, Distribute

> **Output is a document — never a chat stream.** Follow this sequence:
>
> 1. **Confirm** — before producing output, tell the user what you've prepared and ask for the go-ahead
> 2. **Produce as a document** — not inline in the chat; a structured, self-contained artifact
> 3. **Offer amends** — "Any changes before we send it somewhere?"
> 4. **Distribute via connector** — check `context.connectors` from Step 1; offer the most applicable service (scheduling tool → document store → Slack/Teams → email). If nothing connected, ask the user where they want it.


## Step 5: Deliver the Culture Document

> **Always call save_experiment — never skip.** If no explicit test emerged, create
> a lightweight hypothesis based on the most uncertain choice made this session
> (e.g. format selected, tone chosen, angle taken). That choice is worth testing.


Produce a **Company Culture Document** with the following structure, formatted in clean markdown ready for migration to Notion, Confluence, or PDF:

### Document Structure

**I. Letter from Leadership**
- Personal, authentic narrative (not corporate boilerplate) — why culture matters to this specific company at this specific moment
- Acknowledgement of what the company gets wrong and is working on (credibility signal)

**II. Who We Are**
- Mission (why we exist), Vision (where we're going), and the cultural identity that connects them
- ICA alignment: how the culture connects to the people we serve — values that customers and candidates can feel

**III. Our Core Values**
- Full values architecture from Step 4, with definitions, behaviours, shadow-sides, and litmus tests

**IV. Operating Principles**
- Decision-making heuristics in *"When X, we Y because Z"* format
- Cross-referenced to the core value each principle operationalises

**V. How We Work Together**
- Communication norms and expectations
- Meeting philosophy and cadence
- Feedback framework (how to give it, how to receive it, when it's mandatory)
- Conflict resolution protocol

**VI. Rituals & Traditions**
- Recurring cultural practices with purpose explanation (not just description)
- Suggested new rituals to close diagnostic gaps

**VII. How We Grow People**
- Career development philosophy
- Promotion criteria explicitly linked to values (not just output metrics)
- Learning and failure norms

**VIII. How We Hold Ourselves Accountable**
- Culture accountability mechanisms: surveys, retrospectives, values-based 360s
- What happens when values are violated — graduated response framework
- Annual culture review cadence

**IX. Living Document Declaration**
- Explicit statement that this document evolves
- Process for proposing amendments
- Version history and next review date

### Supplementary Deliverables

- **Culture Scorecard**: Quarterly self-assessment template (1–10 per value dimension, with evidence prompts)
- **Interview Values Guide**: Behavioural interview questions mapped to each core value for hiring teams
- **Onboarding Culture Module**: 90-day culture immersion checklist for new hires

## Step 6: Propose Experiments

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:save_experiment(skill="company-culture-doc-builder", experiment={
  hypothesis: "Embedding 'What this value doesn't mean' shadow-side descriptions reduces values misinterpretation in new hire surveys by measurable margin",
  variants: ["control: values with positive definitions only", "variant: values with definitions + shadow-side warnings + litmus-test scenarios"],
  measurement: "New hire 90-day survey — 'I understand what our values mean in practice' score (1–10) and qualitative free-text alignment",
  expected_impact: "20% improvement in values comprehension score and reduction in 'values feel generic' feedback"
})
```

```
FutureProof:save_experiment(skill="company-culture-doc-builder", experiment={
  hypothesis: "Operating principles in 'When X, we Y because Z' format produce faster autonomous decision-making than abstract value statements alone",
  variants: ["control: values doc without operating principles", "variant: values doc with 5–8 operating principles in tension-resolution format"],
  measurement: "Manager escalation rate for ambiguous decisions over 60-day period post-rollout",
  expected_impact: "15% reduction in unnecessary escalations as team members self-resolve using principles"
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
FutureProof:request_research(skill="company-culture-doc-builder",
  query="Evidence-based culture document frameworks 2024: effectiveness of Competing Values Framework, Schein's model, and Netflix/GitLab/Valve culture doc approaches at different company stages. Meta-analysis of culture doc impact on retention, alignment, and employer brand metrics.",
  reason="Ensure the values architecture methodology reflects the latest organisational psychology research and accounts for remote-first, AI-augmented, and multi-generational workforce dynamics"
)
```

```
FutureProof:request_research(skill="company-culture-doc-builder",
  query="Common failure modes of company culture documents: performative values, enforcement gaps, subculture friction, and document abandonment patterns. Remediation strategies from Deloitte Human Capital Trends and Gartner HR research 2023–2024.",
  reason="Proactively address the most frequent reasons culture docs fail to translate into lived behaviour, and build countermeasures into the document structure"
)
```

## Step 8: Save Session

```
FutureProof:save_session(skill="company-culture-doc-builder", session={
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