---
name: council
description: Multi-perspective debate where specialized personas discuss topics in rounds, surface insights through intellectual friction. USE WHEN council, debate, multiple perspectives, should we, decision, trade-offs, weigh options, pros and cons, architectural decision.
---

# Council: Multi-Perspective Debate

Multi-perspective debate system where specialized personas discuss topics in rounds, respond to each other's points, and surface insights through intellectual friction. Collaborative-adversarial: debate to find the best path, not to destroy ideas.

## Customization

Check for user customizations at:
`~/.augment/USER/SKILLCUSTOMIZATIONS/Council/PREFERENCES.md`

If this file exists, load and apply preferences found there. They override defaults below.

## Key Distinction

- **Council** = collaborative-adversarial (debate to find best path). Produces visible transcripts.
- **Red Team** = purely adversarial (attack the idea). Produces steelman + counter-argument.

Use Council for decisions. Use Red Team for stress-testing.

## Council Members

Adopt each perspective sequentially. Each member brings a structurally different viewpoint.

### Default Members

| Persona | Perspective | Focus |
|---------|-------------|-------|
| **Architect** | System design, patterns, long-term implications | Scalability, maintainability, structural integrity |
| **Designer** | UX, user needs, accessibility | User experience, simplicity, human factors |
| **Engineer** | Implementation reality, tech debt | Practical constraints, maintenance burden, cost |
| **Researcher** | Data, precedent, external examples | Evidence, what others have done, prior art |

### Optional Members (add as needed)

| Persona | Perspective | When to Add |
|---------|-------------|-------------|
| **Security** | Risk, attack surface, compliance | Auth, data handling, API design |
| **Fresh Eyes** | Naive questions, first impressions | Complex UX, onboarding flows |
| **Writer** | Communication, documentation clarity | Public-facing work, docs |

## Two Modes

### Mode 1: Full Debate (3 Rounds)

Use for important decisions, architectural choices, and anything with significant trade-offs.

#### Round 1: Initial Positions

Adopt each persona sequentially. Each gives their take from their specialized perspective. No interaction yet -- just establishing positions.

**For each persona (50-150 words each):**
- State your key concern, recommendation, or insight
- Speak from your specialized perspective
- Be specific and substantive

#### Round 2: Responses and Challenges

Adopt each persona again. This time, each responds to specific points from Round 1.

**For each persona (50-150 words each):**
- Reference specific points others made ("I disagree with Architect's point about X because...")
- Challenge assumptions or add nuance
- Build on points you agree with
- The value is in genuine intellectual friction -- engage with actual arguments

#### Round 3: Synthesis

Adopt each persona a final time. Each identifies areas of agreement, remaining disagreement, and their final recommendation.

**For each persona (50-150 words each):**
- Where does the council agree?
- Where do you still disagree?
- What is your final recommendation given the full discussion?
- Be honest about remaining disagreements -- forced consensus is worse than acknowledged tension

#### Council Synthesis

After all three rounds, produce a unified synthesis:

```markdown
## Council Debate: [Topic]

### Round 1: Initial Positions
**Architect:** [Position]
**Designer:** [Position]
**Engineer:** [Position]
**Researcher:** [Position]

### Round 2: Responses and Challenges
**Architect:** [Response referencing others' points]
**Designer:** [Response referencing others' points]
**Engineer:** [Response referencing others' points]
**Researcher:** [Response referencing others' points]

### Round 3: Synthesis
**Architect:** [Final position]
**Designer:** [Final position]
**Engineer:** [Final position]
**Researcher:** [Final position]

### Council Synthesis

**Areas of Convergence:**
- [Points where multiple members agreed]

**Remaining Disagreements:**
- [Points still contested, with trade-offs acknowledged]

**Recommended Path:**
[Synthesized recommendation based on convergence and weight of arguments]
```

### Mode 2: Quick Consensus (1 Round)

Use for sanity checks, fast validation, and low-stakes decisions.

**For each persona (30-50 words each):**
- Give your immediate take from your specialized perspective
- Be direct and specific
- Key concern, insight, or recommendation only

```markdown
## Quick Council: [Topic]

### Perspectives
**Architect:** [Brief take]
**Designer:** [Brief take]
**Engineer:** [Brief take]
**Researcher:** [Brief take]

### Quick Summary
**Consensus:** [Do they generally agree? On what?]
**Concerns:** [Any red flags raised?]
**Recommendation:** [Proceed / Reconsider / Need full debate]
```

**Escalation:** If Quick Consensus reveals significant disagreement or complex trade-offs, escalate to Full Debate.

## Output Requirements

| Mode | Words Per Persona Per Round | Tone |
|------|----------------------------|------|
| Full Debate | 50-150 | Professional, direct, genuine challenges |
| Quick Consensus | 30-50 | Concise, specific, no filler |

**Must Include (Full Debate):** Specific references to other personas' points in Rounds 2 and 3.

**Must Avoid:** Generic opinions, restating positions without engagement, performative agreement.

## Examples

**Architecture decision:**
"Council: Should we use WebSockets or SSE for real-time updates?"
--> Full Debate with 3 rounds

**Quick validation:**
"Quick council check: Is this API design reasonable?"
--> Quick Consensus, single round

**Domain-specific:**
"Council with security: Evaluate this auth approach"
--> Full Debate with Security persona added

## Best Practices

1. Use Quick Consensus for sanity checks; Full Debate for important decisions
2. Add domain-specific personas as needed (security for auth, etc.)
3. Review the transcript -- insights emerge from the responses, not just initial positions
4. Trust multi-persona convergence when it occurs naturally
5. Acknowledge tensions honestly; do not force artificial agreement

## Anti-Patterns

- **Echo Chamber**: All personas agree too easily -- push for genuine disagreement
- **Surface-Level Takes**: Generic opinions without substantive engagement
- **Ignoring Responses**: Round 2/3 personas that do not reference others' actual points
- **Forced Consensus**: Papering over real trade-offs with vague compromise language
- **Persona Collapse**: All personas sounding the same instead of maintaining distinct perspectives
