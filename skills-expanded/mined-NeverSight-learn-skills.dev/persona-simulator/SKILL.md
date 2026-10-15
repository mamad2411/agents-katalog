---
name: persona-simulator
description: Create high-fidelity simulations of specific individuals' perspectives in Advisory, Anticipatory, or Collaborative modes. Use to consult simulated mentors, anticipate stakeholder reactions, or prepare for collaboration. Integrates with background-research and epistemic-analysis skills.
user-invocable: false
effort: max
---

> **Note:** This skill provides reference material for the `persona-simulator` agent. For interactive persona simulation, invoke the agent directly with `@persona-simulator` or ask Claude to "simulate [name]". The agent handles the interactive dialogue; this file provides the data-gathering framework and persona templates.


# Persona Simulator Skill

Create high-fidelity agents modeling specific individuals' perspectives. Unlike temperament-based epistemic agents (which represent cognitive styles), persona agents model actual people based on accumulated knowledge of their professional identity, behavioral patterns, situational context, and relational dynamics.

## Trigger Patterns

| Pattern | Mode | Action |
|---------|------|--------|
| "what would [name] advise", "how would [name] coach me", "[name]'s advice on", "ask [name] about", "what does my mentor think", "[name] as mentor" | Advisory | Simulate as trusted advisor |
| "how would [name] react", "what will [name] say", "[name]'s perspective on", "simulate [name]", "anticipate [name]'s", "prepare for [name]", "run this by [name]", "get buy-in from [name]" | Anticipatory | Simulate as evaluator/stakeholder |
| "how can [name] and I align", "[name] as collaborator", "coordinate with [name]", "work with [name] on", "partner with [name]" | Collaborative | Simulate as ally/partner |
| "create persona for [name]", "build [name] persona" | Prompt for mode | Elicit mode selection |

## The Three Simulation Modes

### Mode 1: Advisory (Trusted Advisor / Coach)

**When to use:** Simulating mentors, sponsors, trusted colleagues who want you to succeed

**Stance:** The simulated person is on your side, offering candid guidance

**Simulation behavior:**
- Offers direct, candid advice
- Draws on their experience and mental models
- Points out what you might be missing
- Challenges you constructively
- Affirms where your instincts are sound

**Unique fidelity requirements (Layer 7):**
- Coaching style (Socratic? Direct? Supportive-then-challenging?)
- Mental models and frameworks they apply
- Experience base that shapes their advice
- What they typically push you on
- What they typically affirm

### Mode 2: Anticipatory (Stakeholder / Evaluator)

**When to use:** Preparing for meetings, presentations, proposals where someone will evaluate or respond

**Stance:** The simulated person is assessing what you're presenting

**Simulation behavior:**
- Evaluates from their perspective and priorities
- Raises concerns they would naturally have
- Asks questions typical of their style
- Identifies what would make them say yes/no
- Signals approval or disapproval as they would

**Unique fidelity requirements:**
- Evaluation criteria they apply
- Questions they typically ask
- What makes them skeptical
- What builds their confidence
- How they signal concerns

### Mode 3: Collaborative (Ally / Partner)

**When to use:** Coordinating with teammates, co-leads, partners who share objectives

**Stance:** The simulated person is working with you toward shared goals

**Simulation behavior:**
- Surfaces their priorities for alignment
- Identifies potential friction points early
- Suggests how to coordinate effectively
- Highlights where your approaches complement
- Flags where you might inadvertently conflict

**Unique fidelity requirements:**
- Their working style preferences
- How they like to divide responsibilities
- Communication rhythms they prefer
- Decisions they want input on vs. delegate
- How they handle disagreement with allies

---

## Complete Workflow

### Step 1: Identify Target & Mode

**Confirm before proceeding:**
- Full name of person to simulate
- Simulation mode (Advisory / Anticipatory / Collaborative)
- Specific context or question to address

**Mode inference rules:**
```
"What would X advise..." → Advisory
"How should I approach X about..." → Advisory (seeking guidance)
"What does my mentor think..." → Advisory
"How would X react to..." → Anticipatory
"What concerns will X raise..." → Anticipatory
"Anticipate X's response to..." → Anticipatory
"Prepare for meeting with X..." → Anticipatory
"Get buy-in from X..." → Anticipatory
"How can X and I align on..." → Collaborative
"What would X want me to consider..." → Collaborative
"Partner with X on..." → Collaborative
```

**If mode unclear:** Ask user which stance is appropriate for their need.

### Step 2: Automated Data Gathering

Resolve data using this priority order:

**Expert library (check first):**
```
1. Search vault-os/references/expert-library/ for [lastname-firstname].md
2. If found: load the pre-built mental model file directly — skip web research steps
3. Expert files contain: core frameworks, signature questions, characteristic advice, limitations
4. Experts can be simulated in any mode (Advisory, Anticipatory, Collaborative)
```

If not a known expert, invoke `background-research/SKILL.md` to collect:

**Local search:**
```
1. Prior persona files if they exist
2. Existing people/contact profiles
3. Meeting transcripts mentioning this person
4. Interaction notes in any project or reference directories
```

**CRM/contact tool lookup (optional — use available tools):**
```
Check any available CRM or contact tools for:
- Contact details (title, socials, notes)
- Relationship history, last contact, frequency
- Engagement history and notes
```

**Web research (fill gaps + public profile):**
```
1. LinkedIn profile and career history
2. News mentions (recent 12 months)
3. Speaking/publications
4. Public interviews/quotes
```

### Step 3: Information Inventory & Gap Analysis

Present structured inventory to user:

```markdown
## Data Inventory for [Name]
## Requested Mode: [Advisory/Anticipatory/Collaborative]

| Layer | Status | Confidence | Key Data Points |
|-------|--------|------------|-----------------|
| 1. Professional Identity | [✓/⚠/✗] | [Level] | [summary] |
| 2. Behavioral Patterns | [✓/⚠/✗] | [Level] | [summary] |
| 3. Revealed Priorities | [✓/⚠/✗] | [Level] | [summary] |
| 4. Situational Context | [✓/⚠/✗] | [Level] | [summary] |
| 5. Relational Dynamics | [✓/⚠/✗] | [Level] | [summary] |
| 6. Known Blindspots | [✓/⚠/✗] | [Level] | [summary] |
| 7. Advisory Profile* | [✓/⚠/✗] | [Level] | [summary] |

*Layer 7 shown only for Advisory mode

## Critical Gaps
- [List gaps that matter for requested mode]

## Recommendation
[Proceed / Gather more data / Mode may be inappropriate]
```

### Step 4: Guided Elicitation

Fill gaps with mode-specific questions from `elicitation-framework.md`:

**For all modes:**
- Behavioral patterns questions
- Revealed priorities questions
- Situational context questions
- Relational dynamics questions

**Advisory mode adds (Layer 7):**
- "How does [Name] typically give you feedback?"
- "What frameworks or mental models do they often reference?"
- "What do they usually push you on?"
- "What do they typically affirm about your approach?"

**Anticipatory mode adds:**
- "What questions do they typically ask in evaluations?"
- "What makes them skeptical? What builds confidence?"
- "How do they signal concerns?"

**Collaborative mode adds:**
- "How do they like to divide responsibilities?"
- "What decisions do they want input on vs. delegate?"
- "How do they handle disagreement with teammates?"

### Step 5: Transcript Analysis (if provided)

If meeting transcripts are available, extract using `transcript-analysis.md`:

**For all modes:**
- Linguistic patterns and characteristic phrases
- Question types they ask
- How they respond to challenge
- Energy patterns (what engages, what bores)

**Advisory mode extraction:**
- How they give feedback (examples from transcripts)
- Mental models they reference
- Advice-giving patterns

**Anticipatory mode extraction:**
- Evaluation questions they ask
- Skepticism signals
- What prompts approval vs. concern

**Collaborative mode extraction:**
- Coordination patterns
- How they divide work
- Disagreement handling with partners

### Step 6: Temperament Mapping

Map to epistemic color framework for baseline orientation:

```markdown
Based on observations, [Name] appears to be:
- **Primary:** [Color] — [How this manifests in their behavior]
- **Secondary:** [Color] — [How this manifests in their behavior]

This suggests they will approach [mode-specific behavior]:
- [Advisory]: Give advice that [color-informed prediction]
- [Anticipatory]: Evaluate based on [color-informed criteria]
- [Collaborative]: Coordinate by [color-informed preference]
```

**Temperament-behavior connections:**
| Temperament | Advisory Style | Evaluation Focus | Collaboration Mode |
|-------------|---------------|------------------|-------------------|
| Green | Analytical, frameworks-first | Logic, strategy, root cause | Independent then sync |
| Gold | Structured, actionable | Process, accountability, risk | Clear roles, defined ownership |
| Blue | Supportive, values-centered | People impact, relationships | High-touch, frequent check-ins |
| Orange | Direct, action-oriented | Speed, results, opportunity | Move fast, delegate broadly |

### Step 7: Persona Draft Generation

Generate structured persona using `persona-template.md`:

**Include:**
- Mode-appropriate simulation instructions
- Mode-appropriate limitations disclosure
- All fidelity layers with confidence ratings
- Relationship health tracking fields

**Initialize tracking:**
```yaml
simulation_invocations: 0
real_interactions_logged: [from interaction logs]
last_real_interaction: [from interaction logs]
relationship_health: healthy
```

### Step 8: User Validation

Present draft for review with mode-specific validation questions:

**Advisory mode:**
> "Does this capture how [Name] coaches you? Does the advice pattern feel authentic to their style?"

**Anticipatory mode:**
> "Does this capture how [Name] evaluates proposals? Are these the questions and concerns they'd actually raise?"

**Collaborative mode:**
> "Does this capture how [Name] works with partners? Are these their real coordination preferences and potential friction points?"

**Iterate until user confirms fidelity.**

### Step 9: Agent File Output

Save persona to:
```
~/.claude/agents/persona-[lastname-firstname]-[mode].md
```

Or if multi-mode persona:
```
~/.claude/agents/persona-[lastname-firstname].md
```
With `supported_modes` field listing available modes.

---

## Mode Inference Examples

| User Prompt | Inferred Mode | Rationale |
|-------------|---------------|-----------|
| "What would Manager A think about this approach?" | Ambiguous | Could be advisory (seeking guidance) or anticipatory (predicting reaction) - ask to clarify |
| "How should I pitch this to the CFO?" | Anticipatory | Preparing for evaluation |
| "What would my mentor say I'm missing?" | Advisory | Seeking coaching input |
| "Colleague C and I need to divide this project - what would she want?" | Collaborative | Coordinating with partner |
| "How will stakeholders react in the review meeting?" | Anticipatory | Preparing for assessment |
| "I want to internalize how Advisor B thinks about this" | Advisory | Absorbing mentor perspective |

---

## Integration with Other Skills

### With background-research

Invoked automatically in Step 2 to gather:
- Professional profile
- Interaction history
- Web presence
- Vault notes

### With epistemic-analysis

Can be combined for layered analysis:

**Pattern 1: Persona + Epistemic**
```
"What would [Name] advise, then stress-test with epistemic analysis"
→ [Name]'s advisory perspective + five temperament lenses
```

**Pattern 2: Multi-Stakeholder Anticipatory**
```
"How would the CFO, CTO, and COO each react?"
→ Three anticipatory personas in parallel
```

**Pattern 3: Full Analysis**
```
"Get [Name]'s coaching, then see how the client would react, then run through all colors"
→ Advisory persona → Anticipatory persona → Epistemic analysis
```

### Synthesis Guidance

When combining persona and epistemic outputs:

**Sequencing options:**
1. **Persona first, then epistemic:** Get specific individual perspective, then stress-test with temperament diversity
2. **Epistemic first, then persona:** Get broad analysis, then check how specific stakeholder would view it
3. **Parallel, then synthesize:** Run both simultaneously, then identify convergence/divergence

**Handling disagreement:**
- If persona and epistemic agent disagree, note both perspectives
- Persona insight: "[Name] would likely..." (specific individual)
- Epistemic insight: "A Green/analytical perspective would..." (temperament pattern)
- Resolution: "[Name]'s Green temperament aligns with the analytical lens, but their specific experience in [X] might lead them to weigh [Y] differently"

**Synthesis output template:**
```markdown
## Combined Analysis: [Topic]

### Persona Perspective: [Name]
[Key insight from persona simulation]

### Epistemic Perspectives
[Summary of relevant color insights]

### Convergence
[Where persona and epistemic agree]

### Divergence
[Where they differ and why]

### Integrated Recommendation
[Synthesis weighing both individual-specific and temperament-general insights]
```

---

## Relationship Health Monitoring

Track simulation-to-interaction ratio per persona:

**Warning triggers:**
- Simulation invocations 5+ without real interaction logged
- More than 60 days since last real interaction
- Ratio of simulations to real interactions > 3:1

**Warning message:**
> "You've been consulting this simulation frequently without recent real interaction with [Name]. Consider reaching out—the real relationship is more valuable than the simulation."

**Update tracking after each use:**
```yaml
simulation_invocations: +1
# Check if new real interaction logged in CRM or contact tools
# Update relationship_health status accordingly
```

---

## Ethical Guardrails

### Intent Monitoring

If user language suggests manipulation:
- "How do I get them to..."
- "How can I make them..."
- "What buttons can I push..."

**Redirect:**
> "I can help you understand [Name]'s perspective and prepare for genuine dialogue. I won't help plan manipulation or deception. What outcome are you hoping to achieve through authentic engagement?"

### Mode Appropriateness Check

Before simulating:
- Advisory persona for someone who isn't actually a mentor → Confirm mode
- Anticipatory persona for a close collaborator → Confirm adversarial framing appropriate
- Collaborative persona for someone you're in conflict with → Surface tension

### Confidence Boundaries

- In LOW confidence areas: Express uncertainty explicitly
- In INSUFFICIENT confidence areas: Refuse to simulate, suggest data gathering
- In stale personas (>180 days): Strong warning about currency

---

## Quality Criteria

A well-executed persona simulation:

**Fidelity:**
- Each layer has documented evidence basis
- Confidence levels calibrated appropriately
- Mode-specific profile captures behavioral nuances
- Temperament mapping informs predictions

**Utility:**
- Simulation provides actionable insight for user's specific question
- Responses feel authentic to the person being simulated
- Uncertainty expressed where appropriate
- Relationship health maintained

**Ethics:**
- Purpose is preparation, not manipulation
- Limitations disclosed appropriately
- Real relationship primacy reinforced
- Guardrails functioning

---

## Reference Files

- `elicitation-framework.md` - Questions by layer and mode
- `persona-template.md` - Full persona structure
- `confidence-framework.md` - ICD-203 inspired calibration
- `ethical-framework.md` - Mode-specific ethics and guardrails
- `transcript-analysis.md` - Pattern extraction guide
- `examples/example-advisor.md` - Advisory mode persona
- `examples/example-stakeholder.md` - Anticipatory mode persona
- `examples/example-collaborator.md` - Collaborative mode persona
