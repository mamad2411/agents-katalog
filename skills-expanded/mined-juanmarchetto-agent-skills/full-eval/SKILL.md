---
name: full-eval
description: "Complete strategic and personal evaluation of any idea, project, or life decision. Runs architect (6 business evaluators) and council (8 life advisors) in parallel, cross-references their outputs, and generates a PDF report. Use when: full evaluation, complete assessment, should I do this, evaluate everything, life decision, career move, startup decision."
license: MIT
metadata:
  version: 1.0.0
  category: evaluation
  tags: [evaluation, multi-agent, decision-making, strategic, personal, comprehensive]
---

# Full Evaluation: Strategic + Personal Assessment

Evaluate any idea, project, or life decision from **every angle** -- 6 business evaluators and 8 life advisors running in parallel, cross-referenced into a unified verdict, delivered as a professional PDF report.

One command. Complete assessment.

## When to Use This

| Situation | Example |
|-----------|---------|
| Career move | "Should I quit my job to build this startup?" |
| New project | "Is this SaaS idea worth pursuing?" |
| Life decision | "Should I relocate to another country for this opportunity?" |
| Investment | "Should I invest 6 months into learning this technology?" |
| Pivot decision | "My project is stalling -- should I pivot or persevere?" |

Use this when the decision spans both **strategic viability** (will it work?) and **personal fit** (should *I* do it, *now*?). For purely business analysis, use architect alone. For purely personal planning, use council alone.

## Dependencies

This skill composes three existing systems:

| System | Role | Agents |
|--------|------|--------|
| **Architect** | Strategic evaluation | 6 evaluators (Risk, Technical, Market, Impact, Resources, Innovation) + synthesizer |
| **Council** | Personal evaluation | 8 advisors (Life Coach, Finance, Health, Career, Learning, Systems, Relationships, Creative) + synthesizer |
| **PDF Presentation** | Report generation | Formats the combined output as a professional PDF |

## The Flow

```
                         +-----------+
                         |   INPUT   |
                         | idea/path |
                         +-----+-----+
                               |
                    +----------+----------+
                    |                     |
              +-----v-----+        +-----v-----+
              |  ARCHITECT |        |  COUNCIL  |
              |  (parallel)|        | (parallel)|
              +-----+-----+        +-----+-----+
              |           |        |             |
        +-----+-----+    |  +-----+-----+      |
        | 6 business |    |  | 8 life    |      |
        | evaluators |    |  | advisors  |      |
        +-----+-----+    |  +-----+-----+      |
              |           |        |             |
        +-----v-----+    |  +-----v-----+      |
        | Architect  |    |  | Council   |      |
        | Synthesizer|    |  | Synthesizer|     |
        +-----+-----+    |  +-----+-----+      |
              |           |        |             |
              +-----+-----+-------+             |
                    |                            |
              +-----v-----------+               |
              | META-SYNTHESIZER |              |
              | Cross-reference  |              |
              | both outputs     |              |
              +---------+-------+              |
                        |                      |
                  +-----v-----+               |
                  |    PDF    |               |
                  |  REPORT   |               |
                  +-----------+               |
```

### Step 1: Parse Input

Detect whether the input is:
- **New idea**: A description, concept, or question (e.g., "AI-powered meal planning app")
- **Existing project**: A path to a codebase (e.g., `/home/user/my-saas-project`)
- **Life decision**: A personal question with strategic dimensions (e.g., "Should I quit my job to build this?")

### Step 2: Dispatch Architect (Strategic Evaluation)

Run the Architect system with all 6 evaluators in parallel:

1. **Risk Assessor** -- Always included. Identifies critical, significant, and monitoring-level risks.
2. **Technical Architect** -- Auto-included for software ideas. Evaluates feasibility, architecture, stack choices.
3. **Market Analyst** -- Auto-included for revenue-generating ideas. TAM/SAM/SOM, competitive landscape, monetization.
4. **Impact Evaluator** -- Social, educational, and community impact assessment.
5. **Resource Strategist** -- Cost-benefit analysis, timeline, team requirements, bootstrapping viability.
6. **Innovation Scout** -- Technology readiness, first-mover advantage, adjacent possible opportunities.

The Architect Synthesizer combines these into:
- **Value Matrix**: Commercial / Educational / Social scores (each 1-10)
- **Opportunity Score**: Overall 1-10 with 6 sub-scores
- **Risk Assessment**: GO / CONDITIONAL GO / NO-GO
- **Architecture Proposal**: For software ideas
- **Prioritized Next Steps**: Maximum 7 actions

### Step 3: Dispatch Council (Personal Evaluation)

Run the Council system with all 8 advisors in parallel:

1. **Life Coach** -- Values alignment, life balance, holistic direction
2. **Finance Advisor** -- Budget impact, runway, cash flow, investment risk
3. **Health Advisor** -- Physical/mental health implications, burnout risk, sustainability
4. **Career Advisor** -- Career trajectory, skill development, positioning, network effects
5. **Learning Advisor** -- Skill gaps, learning curve, educational investment required
6. **Systems Advisor** -- Time management, workflow impact, automation opportunities
7. **Relationships Advisor** -- Social impact, family considerations, collaboration dynamics
8. **Creative Advisor** -- Creative fulfillment, innovation alignment, aesthetic satisfaction

The Council Synthesizer combines these into:
- **Life Impact Assessment**: How this decision affects all life domains
- **Key Synergies**: Actions that serve multiple personal domains
- **Conflicts Resolved**: Where advisors disagreed
- **Prioritized Action Plan**: Maximum 7 actions
- **Watch List**: Items to monitor

### Step 4: Meta-Synthesis

The **Meta-Synthesizer** (see `agents/meta-synthesizer.md`) receives both outputs and:

1. **Identifies alignment** -- Where strategic opportunity and personal readiness both say "go" (strong signal)
2. **Identifies conflicts** -- Where the opportunity is great but personal circumstances say "wait" (or vice versa)
3. **Produces conditions** -- Specific requirements that must be met before proceeding
4. **Generates a narrative** -- Connects the strategic and personal dimensions into a coherent story
5. **Issues a combined verdict** -- GO / CONDITIONAL GO / NOT NOW / NO-GO with clear reasoning

### Step 5: Generate PDF Report

Use the pdf-presentation skill to format the combined output as a professional document:

- Title page with the idea/project name and date
- Executive Summary (meta-synthesis verdict)
- Strategic Assessment section (Architect output: Value Matrix, Opportunity Score, Risk Assessment)
- Personal Assessment section (Council output: Life Impact, Action Plan)
- Cross-Reference Analysis (Meta-Synthesizer: alignments, conflicts, conditions)
- Combined Next Steps (merged and deduplicated from both systems)

## Example Output

Given the input: **"Should I quit my job to build an AI-powered meal planning app?"**

### Meta-Synthesis Verdict

```
VERDICT: CONDITIONAL GO

The opportunity scores 7.5/10 strategically -- strong market demand, feasible
technology, and good resource efficiency. However, the personal assessment
reveals critical constraints that require a phased approach.

CONFLICTS IDENTIFIED:
- Market Analyst says "move fast, the window is 12-18 months" but Finance
  Advisor flags only 3 months of personal runway
- Innovation Scout says "first-mover advantage is real" but Health Advisor
  flags existing burnout indicators from current role
- Career Advisor notes this aligns with long-term trajectory but Relationships
  Advisor flags the strain of a startup on family commitments

CONDITIONS FOR GO:
1. Validate the idea for 3 months while still employed (evenings/weekends MVP)
2. Secure 9 months of runway before transitioning (current savings + 6 months)
3. Hit 50 beta users and $500 MRR before giving notice
4. Establish a hard stop date: if conditions not met in 6 months, reassess

COMBINED SCORE: 6.8/10 (strategic 7.5 adjusted down by personal constraints)

NARRATIVE: The idea has genuine merit -- the meal planning space is growing,
AI personalization is a defensible differentiator, and your technical skills
are a strong fit. But your current personal situation (limited runway, burnout
risk, family commitments) means an immediate leap would be reckless. The smart
play is a structured transition: validate while employed, build runway, then
make the jump with evidence and a safety net.
```

### Value Matrix (from Architect)

```
| Dimension              | Score | Key Driver                                    |
|------------------------|-------|-----------------------------------------------|
| Commercial             | 7/10  | $4B meal kit market, AI personalization moat   |
| Educational            | 6/10  | ML/nutrition knowledge transfer                |
| Social                 | 7/10  | Addresses food waste and dietary health        |
| Technical Feasibility  | 8/10  | Proven tech stack, APIs available               |
| Risk Level             | 6/10  | Competitive market, regulatory (nutrition)      |
| Resource Efficiency    | 8/10  | Solo MVP viable, low infrastructure cost        |
```

### Life Impact Assessment (from Council)

```
| Domain         | Impact | Key Concern                                     |
|----------------|--------|-------------------------------------------------|
| Finance        | HIGH   | 3 months runway insufficient for startup         |
| Health         | HIGH   | Burnout risk -- current role already draining     |
| Career         | POSITIVE | Aligns with ML/product trajectory               |
| Relationships  | MODERATE | Startup hours strain family time                |
| Learning       | POSITIVE | Deep ML and nutrition domain knowledge           |
| Creative       | HIGH   | Strong creative fulfillment potential             |
```

## Error Handling

The system is designed to be resilient when individual components encounter issues:

### If Architect Fails Partially
- If 1-2 evaluators fail, the Architect Synthesizer proceeds with available evaluators and notes gaps in its output
- The Meta-Synthesizer marks affected dimensions as "insufficient data" and lowers confidence
- The PDF report includes a notice about which evaluators were unavailable

### If Council Fails Partially
- If 1-2 advisors fail, the Council Synthesizer proceeds with available advisors and notes gaps
- The Meta-Synthesizer adjusts confidence and flags uncovered personal domains
- Critical failures (Life Coach or Finance) trigger a warning in the final verdict

### If Architect Fails Completely
- The Meta-Synthesizer produces a personal-only assessment with a clear disclaimer
- The verdict is marked "INCOMPLETE -- strategic assessment unavailable"
- The PDF report omits the Strategic Assessment section

### If Council Fails Completely
- The Meta-Synthesizer produces a strategic-only assessment with a clear disclaimer
- The verdict is marked "INCOMPLETE -- personal assessment unavailable"
- The PDF report omits the Personal Assessment section

### If PDF Generation Fails
- The full evaluation results are displayed in the terminal as formatted text
- A markdown file is saved as a fallback

## Language

All evaluators, advisors, synthesizers, and the meta-synthesizer respond in the same language the user writes in. The entire evaluation — including the PDF report — is produced in the user's language. Matched automatically without asking.

## Structure

```
full-eval-skill/
├── SKILL.md                        # This file
├── agents/
│   └── meta-synthesizer.md         # Cross-references architect + council outputs
├── .claude-plugin/plugin.json      # Plugin metadata
├── README.md                       # Installation and usage guide
├── LICENSE                         # MIT License
└── .gitignore
```
