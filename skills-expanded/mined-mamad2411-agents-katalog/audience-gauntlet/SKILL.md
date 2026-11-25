---
name: audience-gauntlet
description: Run a proposal through 3-5 stakeholder personas in two passes — independent evaluation then cross-pollination — simulating how an evaluation board, leadership team, or decision-making group actually processes and reacts to ideas.
version: 1.0
last_modified: 2026-03-28
context: fork
agent: general-purpose
dependencies:
  - persona-simulator
tier: analysis
effort: max
---

# Audience Gauntlet Skill

## Purpose

Test whether a proposal, deliverable, or strategy will *land* with the people who matter — not by checking reasoning quality (that's epistemic analysis), but by simulating the political, relational, and positional dynamics of how real stakeholders evaluate and influence each other.

## When to Use

- Before submitting a proposal, capture paper, or BD deliverable
- Before presenting a strategy to leadership or a client
- When preparing for a meeting where multiple stakeholders will evaluate your position
- When you need to understand coalition dynamics, not just individual reactions
- When "is this logically sound?" matters less than "will the room say yes?"

## Trigger Patterns

- "run this through the gauntlet"
- "audience gauntlet on"
- "how would [group] react to this"
- "simulate the eval board"
- "simulate the room"
- "will this land with"
- "stakeholder stress test"
- "who would push back on this"

## How It Differs from Other Analysis Tools

| Tool | Tests | Best For |
|------|-------|----------|
| **Epistemic analysis** | Is the reasoning sound? | Decisions, strategies, frameworks |
| **Audience gauntlet** | Will the audience say yes? | Proposals, presentations, deliverables |
| **Persona simulator** | What would one person think? | Meeting prep, relationship strategy |
| **Red team pipeline** | How would an opponent attack? | Competitive BD, adversarial scenarios |

The audience gauntlet's unique value is **group dynamics**: personas don't just react independently — they see each other's reactions and shift positions, form coalitions, and surface concerns they wouldn't raise alone. This simulates how real rooms work.

## Orchestration Protocol

### Step 0: Define the Panel

The user provides:
1. **The artifact** — proposal, strategy, deliverable, or talking points to evaluate
2. **The panel** — 3-5 personas who will evaluate it. For each persona, the user provides:
   - Name (real person or role archetype)
   - Role and relationship to the artifact
   - What they optimize for / what they protect

If the user provides only a scenario (e.g., "simulate the source selection board"), help them define 3-5 panel members based on the context. Common panels:

| Scenario | Suggested Panel |
|----------|----------------|
| **Source selection** | Contracting Officer, Technical Evaluator, COR/Program Manager, Small Business Advisor, Past Performance Evaluator |
| **Leadership briefing** | Decision-maker, Budget holder, Technical lead, Operations/delivery lead, Risk/compliance |
| **Client meeting** | Client champion, Client skeptic, Technical gatekeeper, Budget authority |
| **Internal review** | Partner/sponsor, Delivery lead, Pricing analyst, Proposal manager |

Cap at 5 personas. More than 5 produces diminishing returns and hits rate limits.

### Step 1: Independent Evaluation (Pass 1)

Invoke persona-simulator agents in **Anticipatory mode**, batched per rate limit rules (max 3 simultaneous). Each agent uses `model: "sonnet"`.

**Wave 1** (first 3 personas):
```
For each persona in panel[0:3]:
  Agent(
    subagent_type: "persona-simulator",
    model: "sonnet",
    prompt: "
      AUDIENCE GAUNTLET — PASS 1 (Independent Evaluation)

      You are simulating [Name], [Role].
      Mode: Anticipatory (evaluator/stakeholder)

      Context about this person:
      [User-provided persona details + any available profile data]

      Your task: Evaluate the following [artifact type] from [Name]'s perspective.

      === ARTIFACT ===
      [The proposal/strategy/deliverable]
      === END ARTIFACT ===

      Respond with this structure:

      ## [Name] — Independent Assessment

      **Initial Reaction:** [1-2 sentences — gut response, first impression]

      **What I Like:** [What works from this person's perspective and priorities]

      **What Concerns Me:** [Specific concerns, ordered by severity]

      **Questions I'd Ask:** [2-3 questions this person would actually raise]

      **My Verdict:** [Support / Conditional Support / Oppose / Need More Info]
      - If conditional: what conditions?
      - If oppose: what would change my mind?

      **What I'd Say in the Room:** [1-2 sentences in this person's voice — how they'd actually express their position to colleagues]

      Stay in character. Do not break the simulation or add meta-commentary.
    "
  )
```

**Wave 2** (remaining personas, launched when any Wave 1 agent returns):
```
Same prompt structure for panel[3:5]
```

### Step 2: Cross-Pollination (Pass 2)

After all Pass 1 assessments are collected, re-invoke each persona with **everyone else's assessments visible**. This is the key innovation: personas now react to each other, not just to the artifact.

Batch in waves of 2-3, using `model: "sonnet"`.

```
For each persona:
  Agent(
    subagent_type: "persona-simulator",
    model: "sonnet",
    prompt: "
      AUDIENCE GAUNTLET — PASS 2 (Cross-Pollination)

      You are still [Name], [Role]. You evaluated [artifact] independently in Pass 1.

      YOUR PASS 1 ASSESSMENT:
      [Insert this persona's Pass 1 output]

      NOW, here is what the other panel members said:

      [Insert all OTHER personas' Pass 1 outputs]

      ---

      The panel is now discussing. Based on hearing everyone else's positions:

      ## [Name] — After Hearing the Room

      **What Shifted:** [Did any other persona's concern change your thinking? Be specific about whose argument moved you and why.]

      **What I'm Holding Firm On:** [What hasn't changed despite hearing others]

      **Coalitions I See:** [Who do you align with? Who are you opposed to? Are there natural alliances forming?]

      **New Concerns:** [Did someone else's question or objection surface something you hadn't considered?]

      **Updated Verdict:** [Same as before / Shifted — and in which direction]

      **What I'd Say Next in the Room:** [1-2 sentences — how you'd respond to the group discussion, in character]

      Stay in character. React as this person actually would when hearing colleagues' positions.
    "
  )
```

### Step 3: Synthesize the Room

After both passes, the orchestrator (main conversation) synthesizes:

#### 3a. Verdict Map

| Persona | Role | Pass 1 Verdict | Pass 2 Verdict | Shift? |
|---------|------|---------------|----------------|--------|
| [Name] | [Role] | [Verdict] | [Verdict] | [None / Toward support / Toward opposition] |

#### 3b. Coalition Map

Identify natural alliances and opposition blocks:
- **Support coalition:** [Who aligns and why]
- **Opposition coalition:** [Who aligns against and why]
- **Swing votes:** [Who shifted or remains undecided, and what would move them]

#### 3c. Critical Path to Yes

Based on the simulation, what's the minimum set of changes needed to get majority support?

1. [Change 1] — Would move [Persona] from [oppose/conditional] to [support]
2. [Change 2] — Addresses [Persona]'s primary concern
3. [Change 3] — Resolves the coalition tension between [X] and [Y]

#### 3d. Unresolvable Tensions

Are there positions that fundamentally conflict — where satisfying one persona necessarily alienates another? These are the real strategic tradeoffs the user must decide.

#### 3e. Strongest Objection

Which single objection, from which persona, is hardest to overcome? This is the thing most likely to kill the proposal in a real room.

### Step 4: Present Integrated Analysis

Use this template:

---

## Audience Gauntlet: [Artifact Name]

### Panel
| Persona | Role | Optimizes For |
|---------|------|--------------|
| [Name] | [Role] | [Priority] |

### Verdict Map
[Table from 3a]

### Coalition Dynamics
[From 3b — who aligns with whom, and the swing votes]

### Critical Path to Yes
[Numbered list from 3c — minimum changes for majority support]

### Unresolvable Tensions
[From 3d — tradeoffs the user must decide]

### Strongest Objection
[From 3e — the hardest single objection to overcome]

### Room Dynamics Summary
[2-3 paragraph synthesis: How would this actually play out? Where does consensus form? Where does it break down? What's the likely outcome if presented as-is?]

---

## Quality Criteria

A good audience gauntlet:
- Each persona raises concerns specific to their role and priorities (not generic)
- Pass 2 shows genuine position shifts — at least 1 persona changes verdict
- Coalition dynamics emerge that weren't obvious from individual assessments
- The critical path to yes is specific and actionable (not "make it better")
- Unresolvable tensions identify real tradeoffs, not solvable problems
- The strongest objection is the one the user didn't see coming

## When NOT to Use

- For testing reasoning quality → use epistemic analysis
- For simulating one person's reaction → use persona-simulator directly
- For competitive/adversarial analysis → use red team pipeline (when built)
- When you don't know who the audience is → define the panel first
- For low-stakes content where audience reaction doesn't matter

## Integration with Other Tools

| Sequence | When |
|----------|------|
| Epistemic analysis → Audience gauntlet | Test reasoning first, then test positioning |
| Audience gauntlet → Revision → Voice-preflight | Test audience, revise, then check voice |
| Background-research → Audience gauntlet | Research real personas before simulating them |
| Audience gauntlet → Persona-simulator (deep dive) | If one persona's reaction needs deeper exploration |

## Rate Limit Compliance

- Max 3 agents per wave (per your parallelization settings)
- All agents use `model: "sonnet"` (reasoning depth required)
- 5-persona panel = 5 Pass 1 agents + 5 Pass 2 agents = 10 total agent calls across 4+ waves
- Context scoping: each agent gets only the artifact + persona details + (Pass 2) other assessments
- If rate limited: reduce to 3-persona panel (still produces coalition dynamics)
