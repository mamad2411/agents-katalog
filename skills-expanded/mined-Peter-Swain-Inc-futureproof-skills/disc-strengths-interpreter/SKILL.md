---
name: disc-strengths-interpreter
description: |
  Interprets DISC assessment results into actionable behavioral profiles for
  individuals and teams with communication strategy, team composition analysis,
  and management guidance. Use when the user shares DISC scores or a profile
  report and says "interpret my DISC results", "what does this DISC profile
  mean", "analyze our team's DISC mix", or "how do I communicate with a high-D".
  For DISC-specific interpretation, not generic performance feedback.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="disc-strengths-interpreter")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — including any previously profiled team members, organisational culture notes, leadership development frameworks, or role-specific behavioural benchmarks the user has established.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- Share the DISC assessment results (scores, profile type, or full report) for the individual(s) to interpret
- What is the interpretation context? Select one or more:
  - **Individual development** — personal growth plan, coaching debrief
  - **Team composition** — mapping strengths, identifying gaps, resolving friction
  - **Hiring/role fit** — benchmarking candidate profile against role behavioural demands
  - **Communication strategy** — tailoring engagement approach for a specific stakeholder
  - **Leadership development** — identifying leadership style, derailers, and stretch areas
- What is the individual's role, seniority level, and functional area?
- Are there specific interpersonal dynamics, team conflicts, or performance concerns driving this request?
- Has the organisation established any behavioural competency frameworks or values to interpret against?

## Step 3: Do the Work

### 3A: Profile Deconstruction

Parse the DISC scores across all four dimensions and classify:

1. **Primary style** — the dominant behavioural driver (D, I, S, or C)
2. **Secondary style** — the supporting behavioural influence
3. **Adapted vs. natural profile** — if both are provided, identify the behavioural stretch the individual is performing in their current role (the gap between "who they are" and "who they become at work")
4. **Intensity mapping** — classify each dimension as High (70+), Moderate (40–69), or Low (0–39) and note extreme scores (85+ or below 15) as behavioural amplifiers warranting specific attention

### 3B: Behavioural Intelligence Analysis

For each DISC dimension, produce a layered interpretation:

| Dimension | Analysis Layer |
|-----------|---------------|
| **Dominance (D)** | Decision-making velocity, conflict orientation, autonomy needs, risk tolerance, response under pressure |
| **Influence (I)** | Persuasion style, collaboration preference, recognition needs, communication volume, emotional expressiveness |
| **Steadiness (S)** | Change tolerance, team loyalty, pace preference, conflict avoidance tendencies, need for psychological safety |
| **Conscientiousness (C)** | Quality standards, analytical depth, rule adherence, decision paralysis risk, feedback sensitivity |

### 3C: Strengths & Derailer Mapping

For the individual's specific profile blend, identify:

1. **Core strengths** — the 5 highest-leverage behavioural assets this profile brings to their role
2. **Predictable derailers** — the 3 most likely behavioural failure modes under stress, fatigue, or organisational ambiguity (mapped to Hogan-equivalent derailer archetypes where applicable)
3. **Blind spots** — behavioural tendencies this profile is least likely to self-recognise
4. **Energy drivers vs. energy drains** — work conditions that fuel sustained performance versus those that accelerate burnout

### 3D: Context-Specific Application

Based on the user's stated interpretation context, perform the relevant deep analysis:

**If Individual Development:**
- Map profile against role behavioural demands and identify alignment gaps
- Produce a targeted development priority matrix (high impact / high feasibility quadrant)
- Specify coaching conversation starters calibrated to the individual's communication style

**If Team Composition:**
- Plot all team members on a DISC quadrant map
- Identify style concentration risks (e.g., all-High-D leadership team with no S/C counterbalance)
- Flag specific dyad friction risks (profile pairs with predictable tension patterns)
- Recommend structural interventions: meeting design, decision protocols, communication norms

**If Hiring/Role Fit:**
- Construct a behavioural benchmark for the target role using functional area norms
- Score candidate profile fit across each dimension with a tolerance band (not binary pass/fail)
- Identify onboarding and management adjustments required if the candidate is hired despite profile gaps

**If Communication Strategy:**
- Produce a stakeholder communication playbook: preferred channels, message framing, meeting structure, persuasion sequence, and phrases to use/avoid
- Map influence levers ranked by effectiveness for this specific profile

**If Leadership Development:**
- Classify leadership style archetype (e.g., Directive Commander, Inspirational Mobiliser, Servant Stabiliser, Analytical Architect)
- Identify the leadership competencies this profile naturally accelerates versus those requiring deliberate compensatory strategies
- Specify the 2–3 highest-ROI leadership behaviours to develop in the next 90 days

### 3E: Apply FutureProof Context

Integrate any user-specific `instructions` from FutureProof context:
- Align interpretation language with the organisation's competency framework or values taxonomy
- Reference previously profiled team members to build cumulative team intelligence
- Apply any organisational culture modifiers (e.g., "this is a high-autonomy culture, so low-D scores are less of a concern than in hierarchical environments")

## Step 4: Deliver Output

Produce a **DISC Behavioural Intelligence Brief** with the following structure:

### Section 1: Profile Summary
- Name / Role / Assessment Date
- DISC scores (D/I/S/C) with natural and adapted profiles if available
- Primary–Secondary style label (e.g., "DC — The Challenger-Analyst")
- One-paragraph executive narrative of the individual's behavioural signature

### Section 2: Strengths Portfolio
- Top 5 behavioural strengths with workplace manifestation examples
- Conditions under which each strength is maximised

### Section 3: Derailer Risk Register
| Derailer | Trigger Condition | Observable Behaviour | Mitigation Strategy |
|----------|-------------------|----------------------|---------------------|
| (e.g., Steamrolling) | (High-pressure deadline with ambiguous authority) | (Bypasses consultation, makes unilateral decisions) | (Pre-agree decision rights; scheduled check-ins) |

### Section 4: Context-Specific Deliverable
- The relevant deep-analysis output from Step 3D, formatted as a standalone actionable document:
  - **Individual Development** → 90-Day Behavioural Development Plan
  - **Team Composition** → Team DISC Map & Dynamics Report
  - **Hiring/Role Fit** → Candidate-Role Fit Scorecard with Interview Probe Questions
  - **Communication Strategy** → Stakeholder Communication Playbook (1-page)
  - **Leadership Development** → Leadership Style Profile & Growth Roadmap

### Section 5: Manager / Coach Guidance
- How to deliver these insights to the individual in a psychologically safe manner
- Conversation framework calibrated to the individual's DISC profile (e.g., for High-C: lead with data, provide written summary in advance; for High-I: make it conversational, affirm contributions first)
- Three coaching questions designed to prompt self-discovery rather than prescriptive feedback

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
FutureProof:save_experiment(skill="disc-strengths-interpreter", experiment={
  hypothesis: "Tailoring 1:1 meeting structure to each direct report's DISC profile increases manager-rated engagement scores within 60 days",
  variants: ["control: uniform 1:1 format across all reports", "variant: DISC-adapted 1:1 format per individual profile"],
  measurement: "Manager subjective engagement rating (1-10) per direct report at 30 and 60 days; qualitative notes on conversation quality",
  expected_impact: "20% improvement in average engagement rating; reduction in reported communication friction"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="disc-strengths-interpreter",
  query="Latest meta-analyses on DISC assessment predictive validity for role performance, emerging integration frameworks combining DISC with CliftonStrengths and Hogan derailers, and 2024 best practices for using behavioural assessments in hybrid/remote team composition",
  reason="Ensure interpretation methodology reflects current industrial-organisational psychology evidence base and accounts for distributed work dynamics that alter behavioural expression"
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
FutureProof:save_session(skill="disc-strengths-interpreter", session={
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