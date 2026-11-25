---
name: epistemic-analysis
description: Invoke seven cognitive diversity agents in parallel, then cross-examine the sharpest tensions to surface blind spots, reveal tradeoffs, and strengthen decision-making through productive tension.
version: 3.2
last_modified: 2026-03-28
context: fork
agent: general-purpose
dependencies:
  - epistemic-green
  - epistemic-gold
  - epistemic-blue
  - epistemic-orange
  - epistemic-violet
  - epistemic-red
  - epistemic-white
tier: analysis
effort: max
---

# Epistemic Analysis Skill

## Purpose

Invoke seven cognitive diversity agents in parallel, then cross-examine the sharpest tensions to surface blind spots, reveal tradeoffs, and strengthen decision-making through productive tension.

## Trigger Patterns

Activate this skill when the user says any of:
- "perspective analysis"
- "stress test this"
- "red team this"
- "what am I missing"
- "run it through the colors"
- "epistemic analysis"
- "multiple perspectives on"
- "seven lenses on"
- "cognitive diversity check"

## The Seven Epistemic Agents

| Agent | Color | Core Orientation | What They Catch |
|-------|-------|-----------------|-----------------|
| `epistemic-green` | Green | Theory, logic, strategy | Logical gaps, unstated assumptions, root cause vs. symptom |
| `epistemic-gold` | Gold | Structure, plans, accountability | Missing ownership, timeline gaps, operational risks |
| `epistemic-blue` | Blue | People, relationships, values | Human costs, adoption barriers, stakeholder gaps |
| `epistemic-orange` | Orange | Action, pragmatism, speed | Over-engineering, missed opportunities, analysis paralysis |
| `epistemic-violet` | Violet | Lateral thinking, reframing | False constraints, unexplored options, wrong problem framing |
| `epistemic-red` | Red | Gut reactions, intuition, felt sense | Emotional resistance, enthusiasm gaps, things nobody wants to say |
| `epistemic-white` | White | Facts, data, information gaps | Unverified assumptions, missing evidence, claims without sources |

**Design note:** Red and White are inspired by De Bono's Six Thinking Hats but adapted to the temperament-lens architecture. Red is distinct from Blue (Red = your own gut reaction; Blue = other people's feelings). White is distinct from Green (White = facts without interpretation; Green = theory and analysis of facts).

## Orchestration Protocol

### Step 1: Batched Invocation

Invoke agents in waves of 3 to avoid API rate limits. All agents use `model: "sonnet"` — epistemic analysis requires reasoning depth that haiku cannot reliably provide.

**Wave 1:** Green, Gold, Blue (the three structural/analytical lenses)
```
Agent(subagent_type: "epistemic-green", model: "sonnet", prompt: "[scenario]")
Agent(subagent_type: "epistemic-gold", model: "sonnet", prompt: "[scenario]")
Agent(subagent_type: "epistemic-blue", model: "sonnet", prompt: "[scenario]")
```

**Wave 2** (launch when any Wave 1 agent returns): Orange, Violet, Red
```
Agent(subagent_type: "epistemic-orange", model: "sonnet", prompt: "[scenario]")
Agent(subagent_type: "epistemic-violet", model: "sonnet", prompt: "[scenario]")
Agent(subagent_type: "epistemic-red", model: "sonnet", prompt: "[scenario]")
```

**Wave 3** (launch when any Wave 2 agent returns): White
```
Agent(subagent_type: "epistemic-white", model: "sonnet", prompt: "[scenario]")
```

White runs last because its fact-check is most useful when you can compare it against the other six assessments during synthesis. If time is critical and no rate limit errors occurred in Waves 1-2, White can be included in Wave 2.

**Context scoping:** Each agent receives only the scenario/proposal to analyze — not the full conversation context or prior agent outputs. Keep prompts focused.

### Step 2: Collect Structured Outputs

Each agent returns a standardized assessment:
- What I Noticed (Red uses "Gut Reaction" first)
- What Concerns Me
- Questions I'd Want Answered
- Where I Likely Disagree With Others
- Bottom Line
- Confidence Level

White uses a distinct format: What We Know / What We Believe / What We're Assuming / Key Information Gaps.

### Step 3: Cross-Examination

After collecting all seven assessments, conduct a cross-examination round to surface second-order insights that only emerge when agents engage with each other's positions.

#### 3a. Identify the Top 3 Tensions

Read all seven assessments and identify the 3 sharpest productive tensions — places where agents most directly contradict each other. Prioritize tensions that:
- Represent genuine tradeoffs (not just different emphases)
- Would change the recommendation depending on which agent is right
- Involve 2+ agents with opposing positions

#### 3b. Re-invoke Disagreeing Agents

For each of the 3 tensions, re-invoke the 2 primary agents in conflict. Each receives:
- Their own original assessment
- The opposing agent's assessment on the contested point
- This instruction: "Read [Other Agent]'s position on [specific point of disagreement]. Respond directly in 3-5 sentences: Where are they right that you initially underweighted? Where do they remain wrong? What evidence or argument would change your mind?"

Each agent returns a brief **Cross-Examination Response** — not a full reassessment.

#### 3c. Violet Cross-Examines the Consensus

After bilateral cross-examination, distill the majority position into 2-3 sentences and feed it to Violet with this instruction: "Five of the six other agents converged on [consensus summary]. Respond in 3-5 sentences: Where is the consensus right? Where is it trapped in the frame it set up for itself? What option is everyone missing?"

This step exists because bilateral cross-examination sharpens positions *within* the existing frame, but Violet's value is breaking the frame itself. In the v3.0 test run, this produced the single strongest insight (the "reference artifact" model that none of the other six agents considered).

#### 3d. Note Position Shifts

Track whether any agent modified, sharpened, or held their position after seeing the counter-argument. Position shifts are high-signal — they reveal where an agent's initial assessment was incomplete. Also note whether Violet's consensus challenge introduced an option that changes the decision landscape.

**Skip cross-examination when:** Initial assessments show strong convergence (few real tensions), speed is critical, or stakes are low enough that parallel-only assessment suffices.

### Step 4: Synthesize Results

After cross-examination (or directly after Step 2 if skipped), synthesize:

#### 4a. Map Agreement (Convergence)
Identify concerns raised by 4+ agents. These are likely blind spots requiring attention regardless of perspective.

#### 4b. Map Disagreement (Productive Tensions)
Identify where agents explicitly disagree. For each tension:
- Which agents disagree?
- What's the underlying tradeoff?
- Is this a values difference or an information gap?
- Did cross-examination change either agent's position?

#### 4c. Surface Key Questions
Compile questions multiple agents raised. Prioritize questions that would change multiple agents' assessments. Give special weight to White's information gaps — these often resolve other agents' disagreements.

#### 4d. Identify Reframes
Note where Violet (or others) challenged the problem framing itself. These may be more valuable than solving the stated problem.

#### 4e. Check the Gut
Note Red's intuitive signal and whether it aligns with or contradicts the analytical consensus. When Red strongly disagrees with the analytical majority, flag it explicitly — the gut is sometimes the first to notice what the mind takes longer to articulate.

### Step 5: Present Integrated Analysis

Use this template for the final synthesis:

---

## Epistemic Analysis: [Topic]

### Convergent Concerns
*Issues flagged by 4+ perspectives - address these regardless of approach*

- [Concern 1]: Raised by [agents]
- [Concern 2]: Raised by [agents]

### Intuitive Read
*Red's gut reaction — reported without requiring justification*

[1-2 sentence summary of Red's emotional signal and whether it aligns with or contradicts the analytical consensus]

### Information Foundation
*White's fact check — what we actually know vs. assume*

- **Verified:** [Key facts with evidence]
- **Assumed:** [Claims treated as fact without evidence]
- **Unknown:** [Critical gaps that would change the analysis]

### Productive Tensions
*Genuine tradeoffs revealed through disagreement*

| Tension | Agents | Tradeoff | Cross-Exam Result | Implication |
|---------|--------|----------|-------------------|-------------|
| [Description] | [A] vs [B] | [What's being traded off] | [Held / Shifted / Sharpened] | [What decision-maker must weigh] |

### Cross-Examination Highlights
*Second-order insights from agents engaging each other's positions*

- **[Tension 1]:** [Agent A] conceded [X] but held firm on [Y]. [Agent B] sharpened their argument to [Z].
- **[Tension 2]:** ...
- **[Tension 3]:** ...

### Disagreement Register
*Explicit record of where minority arguments beat the majority — and where consensus may mask weak reasoning*

| Disagreement | Minority Position | Majority Position | Verdict | Rationale |
|-------------|-------------------|-------------------|---------|-----------|
| [Topic] | [Agent(s)]: [Position] | [Agent(s)]: [Position] | Minority wins / Majority holds / Unresolved | [Why the reasoning quality, not vote count, determined the verdict] |

*A well-argued minority beats a hand-waving majority. If a single agent provides stronger evidence or identifies a flaw the majority overlooked, record it here.*

### Critical Questions
*Questions that would change multiple assessments*

1. [Question] — Would affect [which agents' views]
2. [Question] — Would affect [which agents' views]

### Reframes to Consider
*Alternative problem definitions from Violet and others*

- [Alternative framing 1]
- [Alternative framing 2]

### Synthesis
*What the diversity of perspectives reveals*

[2-3 paragraph synthesis of what the analysis reveals about the decision/proposal, including what would need to be true for each major concern to be addressed. Note where the intuitive read and analytical consensus align or diverge.]

---

## Example Usage

**User:** "Run epistemic analysis on this proposal for reorganizing our team structure."

**Claude:**
1. Invokes all 7 agents in parallel with the proposal
2. Collects assessments — notes Green and Gold flag unclear decision rights, Red reports unease, White identifies missing org performance data
3. Identifies top 3 tensions: (a) Orange vs. Gold on speed-to-pilot, (b) Red vs. Green on gut-feel vs. logic, (c) White vs. Violet on data gaps vs. reframing
4. Re-invokes the 6 agents involved in those tensions with each other's positions
5. Notes that Orange concedes Gold's timeline concern after seeing the implementation detail, but Gold acknowledges Orange's pilot approach could work in one division
6. Presents integrated analysis with cross-examination shifts made explicit

## Integration with Working Memory

When epistemic analysis surfaces significant findings:

1. **Capture in Working Memory** (if session continues):
   - Key unresolved tensions
   - Questions requiring investigation
   - Tradeoffs requiring explicit decision
   - Red's gut signal when it contradicts consensus

2. **Flag for follow-up** if analysis reveals:
   - Stakeholder perspectives not yet gathered
   - Data needed to resolve information gaps (White's unknowns)
   - Fundamental reframes worth exploring

## Quality Criteria

A good epistemic analysis:
- Each agent surfaces 2+ unique concerns
- At least 4 pairs of agents have opposing views representing real tradeoffs
- Red's intuitive signal is reported without being rationalized away
- White's fact check reveals at least 1 assumption treated as fact
- Cross-examination produces at least 1 position shift or sharpened argument
- Disagreements map to genuine tradeoffs, not arbitrary variation
- Synthesis identifies what decision-maker must weigh
- Reframes challenge the problem definition, not just solutions

## When NOT to Use

Skip epistemic analysis for:
- Simple, unambiguous decisions
- Tasks with clear right answers
- Situations where speed is critical and stakes are low
- When the user just needs execution, not analysis

**Use without cross-examination** (Steps 1-2, skip Step 3, proceed to Step 4) when:
- Time pressure is moderate and stakes are medium
- Initial assessments show strong convergence
- User requests "quick epistemic" or "fast pass"

## Related Skills

- Background research (gather context before analysis)
- Persona simulator (model specific stakeholders, not abstract lenses)
- Decision journaling (document decisions and rationale)
