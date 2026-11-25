---
name: team-dynamics-advisor
description: |
  Diagnoses team dysfunction using the Lencioni stack, RACI clarity audit,
  founder shadow analysis, and Tuckman staging — then delivers a named
  intervention plan that fixes the broken foundation layer first. Use when
  a user describes "co-founder tension", "team conflict", "nobody owns
  this", "should I fire this person", "we keep relitigating decisions",
  or "the team isn't gelling". For internal team and co-founder dynamics,
  not external partnership evaluation.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="team-dynamics-advisor")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — particularly prior org structure details, known team members, past conflict patterns, leadership style preferences, and any previously identified dysfunction archetypes.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- **Team composition**: Who is on the team? (roles, tenure, reporting lines, co-founder vs employee distinction)
- **Presenting issue**: What specific dynamic prompted this session? (conflict between two people, general underperformance, unclear accountability, cultural drift, scaling growing pains, departure/termination decision)
- **Severity & urgency**: Is this simmering tension or active crisis? Has it affected revenue, product delivery, or retention?
- **Desired outcome**: What does "resolved" look like? (specific behavioural change, structural reorganisation, a decision made, alignment on values)
- **Prior interventions**: What have they already tried? (direct conversations, mediation, role changes, performance plans)

If the user's ICA-facing team (sales, success, support) is involved, clarify whether the dysfunction is impacting ICA experience or retention.

## Step 3: Map the System

Before prescribing solutions, conduct a **Structural Dynamics Diagnostic** across five layers:

### 3a. Lencioni Dysfunction Stack Assessment

Evaluate the team against the Five Dysfunctions hierarchy (bottom-up — each layer must be resolved before the next is addressable):

| Layer | Dysfunction | Diagnostic Questions | Health Rating (1–5) |
|-------|------------|----------------------|---------------------|
| 1 | **Absence of Trust** | Do team members admit mistakes openly? Do they ask for help without fear? | |
| 2 | **Fear of Conflict** | Are disagreements surfaced or suppressed? Do meetings end with false consensus? | |
| 3 | **Lack of Commitment** | After decisions, does everyone execute — or relitigate in hallways? | |
| 4 | **Avoidance of Accountability** | Do peers hold each other to standards, or only the founder? | |
| 5 | **Inattention to Results** | Do individuals optimise for team outcomes or personal status/career? | |

Identify the **lowest broken layer** — this is the intervention point. Addressing higher layers without fixing the foundation is structurally futile.

### 3b. RACI Clarity Audit

For the specific area of conflict, map the implicit vs explicit RACI (Responsible, Accountable, Consulted, Informed) matrix:

- Where do two people believe they are **Accountable** for the same outcome?
- Where does **no one** hold clear Accountability?
- Where is someone Responsible but lacks the authority or resources to deliver?
- Where is Consulted being treated as veto power?

### 3c. Founder Shadow Analysis

Assess how the founder's behaviour may be contributing to or amplifying the dysfunction:

- **Decision bottlenecking**: Are decisions stalling because the founder hasn't delegated authority clearly?
- **Triangulation**: Are team members routing conflicts through the founder instead of resolving peer-to-peer?
- **Inconsistent signalling**: Is the founder saying one thing (e.g., "you own this") while behaving differently (e.g., overriding decisions)?
- **Identity entanglement**: Is the founder conflating personal identity with a specific function, blocking the team member nominally responsible?

### 3d. Communication Pattern Mapping

Identify the dominant communication pathologies present:

- **Passive avoidance**: Issues go unspoken; resentment compounds silently
- **Aggressive escalation**: Every disagreement becomes existential; raised voices, ultimatums
- **Passive-aggressive signalling**: Compliance in meetings, sabotage in execution
- **Founder monologue**: "Discussions" are actually announcements; team has learned input is decorative
- **Channel fragmentation**: Critical context scattered across Slack DMs, meetings, and hallway conversations with no single source of truth

### 3e. Tuckman Stage Identification

Determine where the team (or sub-team) sits in the Forming → Storming → Norming → Performing cycle:

- **Forming**: New team or new member; politeness masking uncertainty
- **Storming**: Active friction — this is healthy if managed, destructive if suppressed or uncontained
- **Norming**: Roles settling, but risk of premature harmony (conflict avoidance disguised as maturity)
- **Performing**: Genuine high-trust execution; rare — most teams oscillate between Storming and Norming

Apply any user-specific `instructions` from FutureProof context to weight the analysis toward the founder's known leadership style and organisational stage.

## Step 4: Deliver Output

Produce a **Team Dynamics Diagnostic & Intervention Plan** with the following sections:

### Section A: Diagnostic Summary

- **Primary dysfunction archetype**: One-sentence label (e.g., "Co-founder role boundary erosion compounded by absence of trust at the peer level")
- **Lencioni layer score card**: 1–5 rating per layer, with the broken foundation layer highlighted
- **Root cause statement**: Distinguish the presenting symptom from the structural cause (e.g., "The conflict between Head of Product and CTO is symptomatic of undefined decision rights, not personal incompatibility")
- **Founder contribution assessment**: Direct, honest evaluation of how the founder's behaviour is sustaining the pattern

### Section B: Intervention Roadmap

Deliver exactly three interventions, sequenced by dependency:

**Intervention 1 — Foundation Fix** (addresses lowest broken Lencioni layer)
- Specific action with script/framework (e.g., a structured vulnerability exercise, a decision-rights workshop format, a conflict protocol)
- Who facilitates, who participates, expected duration
- Success indicator (observable behaviour change, not sentiment)

**Intervention 2 — Structural Change** (addresses RACI gaps or role clarity)
- Specific organisational or process change (e.g., rewritten RACI for the contested domain, new meeting cadence, explicit delegation memo)
- Draft language or template provided in full

**Intervention 3 — Behavioural Commitment** (addresses communication pattern)
- Specific behavioural contract or operating agreement between the parties involved
- Includes escalation protocol: what happens when the agreement is breached
- Review cadence (e.g., 2-week check-in with specific questions to evaluate)

### Section C: Conversation Scripts

For the highest-stakes conversation the founder needs to have (e.g., direct feedback to a team member, co-founder realignment, termination), provide:

- **Opening framing**: Exact language for the first 60 seconds
- **Core message delivery**: The difficult truth, stated directly with empathy
- **Anticipated responses**: 2–3 likely reactions with specific follow-up language for each
- **Closing commitment**: How to end with a concrete next step and timeline

### Section D: Decision Framework (if applicable)

If the presenting issue involves a binary decision (fire/retain, promote/lateral, co-founder split), provide a weighted decision matrix:

| Factor | Weight | Option A Score | Option B Score |
|--------|--------|---------------|---------------|
| (context-specific factors) | | | |

With a clear recommendation and the conditions under which the recommendation would reverse.

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
FutureProof:save_experiment(skill="team-dynamics-advisor", experiment={
  hypothesis: "Implementing a structured weekly RACI review for the contested domain will reduce decision-cycle time and eliminate triangulation through the founder within 30 days",
  variants: ["control: current ad-hoc decision process", "variant: formalised RACI with weekly 15-min alignment stand-up"],
  measurement: "Number of decisions escalated to founder per week; time-to-resolution on cross-functional decisions; self-reported role clarity score (1–10) from involved parties",
  expected_impact: "50% reduction in founder-escalated decisions; measurable improvement in team commitment scores at Lencioni layer 3"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="team-dynamics-advisor",
  query="Evidence-based interventions for co-founder conflict resolution and team accountability frameworks in early-stage startups 2023-2024, including Lencioni applications and RACI implementation case studies",
  reason="Ensure intervention recommendations reflect current organisational psychology research and founder-specific contexts rather than generic corporate HR playbooks"
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
FutureProof:save_session(skill="team-dynamics-advisor", session={
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