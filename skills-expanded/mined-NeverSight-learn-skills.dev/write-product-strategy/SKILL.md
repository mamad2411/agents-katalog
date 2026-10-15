---
name: write-product-strategy
description: "Generate comprehensive product strategy documents aligned with business goals. Use this when defining or updating your product's strategic direction, aligning teams on where to play and how to win, or creating a STRATEGY.md that bridges vision and execution. Triggers include: clarifying product strategy, articulating competitive positioning, defining strategic pillars, creating alignment documents, or answering 'what are we betting on as a company?' This skill scans existing project docs (roadmaps, market research, competitive analyses) to inform strategy, then either creates a new STRATEGY.md or updates an existing one."
compatibility: "Requires filesystem access to project directory. Works best with markdown and project context documents."
version: 1.0.0
argument-hint: "[product name or context]"
allowed-tools: [Read, Write, Bash]
---

# Product Strategy Generator

This skill helps you build a rigorous, comprehensive product strategy document (STRATEGY.md) that serves as the connective tissue between vision and execution. Rather than dictating strategy, this skill helps you think through the critical strategic questions and structures your answers into a compelling narrative — complete with research evidence and transparent strategic reasoning.

## How It Works

> **Before starting:** If you haven't done a structured brainstorm yet, `/superpowers:brainstorming` can map the problem space before we commit to strategic direction.

### Step 1: Context Gathering (Automatic)

Silently scan the project directory using Read and Bash:

```bash
# Gambit-generated artefacts
cat STRATEGY.md 2>/dev/null
find . -maxdepth 2 -name "OKRs-*.md" 2>/dev/null | sort | xargs cat 2>/dev/null
cat ROADMAP.md 2>/dev/null
find . -maxdepth 3 \( -name "COMPETITIVE-ANALYSIS.md" -o -name "competitive-analysis.md" \) 2>/dev/null | head -3 | xargs cat 2>/dev/null
# Research synthesis output from synthesize-user-research skill
find . -maxdepth 3 -name "research-synthesis-*.md" 2>/dev/null | sort | xargs cat 2>/dev/null
# Broader project context — product briefs, market research, vision docs, user research notes
find . -maxdepth 3 \( -name "VISION.md" -o -name "vision.md" -o -name "BRIEF.md" -o -name "brief.md" \) 2>/dev/null | head -5 | xargs cat 2>/dev/null
find . -maxdepth 4 -type f -name "*.md" \( -path "*/research/*" -o -path "*/market/*" -o -path "*/discovery/*" \) 2>/dev/null | head -10 | xargs cat 2>/dev/null
```

Based on what you find:
- **If STRATEGY.md exists**: present its current contents and ask what needs to change. Update only modified sections, preserve the rest.
- **If OKR or roadmap docs exist**: treat them as constraints on the new strategy — do not contradict committed OKRs without explicitly flagging the conflict.
- **If research-synthesis-*.md files exist**: extract themes, pain points, and jobs-to-be-done to ground the strategy's problem statements in evidence.
- **If product briefs, vision docs, or research notes exist**: use them to inform target audience, market context, and competitive position.
- **If nothing is found**: ask clarifying questions about target audience, core problems, and strategic bets before writing.

Do not mention the scan to the user.

### Step 2: Input & Validation (Prompt-Responsive)

If you provide market/user/competitive context upfront, I'll use it directly. If your input is sparse or vague, I'll guide you through key questions section-by-section.

**What I MUST have to build the strategy:**
- Target audience (who are we building for?)
- Core problem(s) we're solving
- At least one strategic pillar or bet (what are we optimizing for?)
- A rough sense of business context (market size, competitive position, etc.)

If you can't answer these yet, that's OK — we'll work through them together. But a strategy without these is incomplete.

### Step 3: Generate STRATEGY.md with Research Citations

I'll structure your input into the standard 7-section format, making transparent **how research findings drove each strategic choice**. This means:
- Research evidence is explicitly connected to strategic pillars
- Assumptions are clearly labeled as "validated via research" or "speculative"
- The strategy explains *why* each choice was made, not just *what* it is

## STRATEGY.md Format

The output will follow this structure:

```markdown
# Product Strategy: [Product Name]

## Executive Summary

**Vision**: [One-sentence aspirational statement about the future state]

**The Big Bet**: [The primary strategic shift or focus for the upcoming period. What are we willing to bet our roadmap on?]

---

## Market & User Context

**Target Audience**: [Primary and secondary user personas. Who are we building for?]

**Problem Statement**: [Specific, underserved pain points we're solving. What makes this moment ripe?]

**Competitive Landscape**: [Direct and indirect competitors. What is the status quo we're disrupting?]

**Market Trends**: [Regulatory, technological, economic factors influencing our trajectory]

---

## How We Got Here: Strategic Reasoning

Before diving into pillars, briefly summarize the key research findings and decisions that shaped this strategy:

**Key Research Findings**:
- [Finding 1]: [How you discovered it (interviews, surveys, data)]
- [Finding 2]: [How you discovered it]

**Why These Pillars**: [Explain how findings led to specific strategic bets]
- We observed [Problem/Insight] in [% of users/market segment], which led us to prioritize [Pillar]
- [Competitor analysis] showed that [Opportunity], so we're betting on [Pillar]

---

## Strategic Pillars

### Pillar 1: [Theme]
**Objective**: [What does success look like for this pillar?]

**Rationale & Research Evidence**: [Explain why this matters NOW, grounded in specific research or market context]
- **Research backing**: [How do you know this? Cite interviews, data, customer feedback, market trends]
- **Competitive positioning**: [How does this differentiate you?]
- **Success criteria**: [What would prove this pillar is working?]

### Pillar 2: [Theme]
**Objective**: [...]

**Rationale & Research Evidence**: [...]
- **Research backing**: [...]
- **Competitive positioning**: [...]
- **Success criteria**: [...]

### Pillar 3: [Theme]
**Objective**: [...]

**Rationale & Research Evidence**: [...]
- **Research backing**: [...]
- **Competitive positioning**: [...]
- **Success criteria**: [...]

---

## Governance & Risk

**Compliance & Regulatory Risks**: [How do new laws or standards affect viability?]

**Technical Constraints**: [Legacy debt, infrastructure limitations that might slow execution]

**Mitigation Strategy**: [High-level plans to address risks before they become blockers]

---

## Strategic Roadmap (Themes, Not Features)

### Horizon 1 (Now): [Theme]
Strengthen core and address immediate gaps. Expected outcomes: [...]

### Horizon 2 (Next): [Theme]
Expand capabilities and enter adjacent markets. Expected outcomes: [...]

### Horizon 3 (Future): [Theme]
Long-term innovation and "moonshot" ideas. Expected outcomes: [...]

---

## Success Metrics (KPIs)

**Primary Metric (North Star)**: [The one metric that best captures core value delivered]

**Supporting Metrics**:
- [Metric 1]: [What it measures and why it matters]
- [Metric 2]: [...]
- [Metric 3]: [...]

---

## Resource & Alignment Requirements

**Cross-functional Dependencies**: [What Engineering, Marketing, Sales, Legal need to deliver]

**Budgetary Needs**: [Significant capex or partnerships required]

---

## Appendix: Key Assumptions

List critical assumptions your strategy depends on, and mark whether they're validated or speculative:

| Assumption | Validated? | How Validated | Risk if Wrong |
|-----------|-----------|---|---|
| [Assumption 1] | ✅ Yes / ❓ Unknown | Interview data, surveys, pilot | [Risk impact] |
| [Assumption 2] | ❓ Unknown | Needs validation | [Risk impact] |

---
```

## Key Principles

1. **Opinionated on Essentials**: You MUST articulate:
   - Who you're building for (target audience)
   - What problem you're solving (grounded in research)
   - How you're different from competitors
   - At least 3 strategic pillars (each tied to research)
   - A primary metric that defines success
   
   Missing these means the strategy is incomplete.

2. **Transparent About Reasoning**: Rather than just stating pillars, explain:
   - How you discovered the insight (interviews? data? market analysis?)
   - Why you believe this matters (80% of users mentioned this pain, competitive gap, market trend)
   - What would prove you right (success metrics tied to each pillar)

3. **Flexible on Details**: You DON'T need to lock in:
   - Exact feature roadmaps (that's a separate Roadmap.md)
   - Detailed financial projections (unless critical to strategy)
   - Lengthy competitive matrices (focus on what matters)

4. **Grounded in Data, Not Guessing**: Every assertion should connect to:
   - Customer research or market evidence
   - Competitive positioning
   - Business context (market size, growth stage, etc.)
   
   If you say "this is a pain point," I'll ask: *How do you know?* (interviews, support tickets, user feedback, etc.)

5. **Concise but Complete**: A strategy should be ~2,000–3,500 words — long enough to be rigorous, short enough to be readable.

## Workflow

### If You Have Context Ready:
Provide your input in one go:
```
Market: [describe your target market]
Users: [describe primary/secondary personas]
Problem: [what pain are they in? cite research if you have it]
Research: [20 customer interviews showed X, surveys showed Y, etc.]
Competitors: [who else is playing in this space?]
Your Differentiation: [why will customers choose you?]
Strategic Bets: [what are the 2-3 big bets you want to make?]
```

I'll structure this into a STRATEGY.md with research citations and save it to your project.

### If You're Thinking Through It:
Just tell me what you know and what you're uncertain about. I'll ask focused questions to fill the gaps, then build the strategy iteratively. **The final output will show how your answers shaped each strategic pillar.**

### If You're Updating Existing Strategy:
I'll present your current STRATEGY.md and ask:
- Which sections still feel true?
- What's changed in your market, users, or competitive position?
- Any pillars or bets you want to shift?
- New research findings?

Then I'll update only what needs to change, adding research evidence where applicable.

## What You'll Get

- **STRATEGY.md**: Saved directly to your project directory
- **A coherent narrative**: Each section builds on the last so the strategy "hangs together"
- **Research transparency**: Clear connection between evidence and strategic choices
- **Specificity**: Concrete enough to guide engineering/marketing decisions
- **Assumption tracking**: Explicit list of what you're betting on and what still needs validation

## Example: Output with Research Evidence

A completed STRATEGY.md for a consumer finance app might include:

```markdown
# Product Strategy: SaveFlow

## Executive Summary

**Vision**: Make saving feel as natural and rewarding as spending.

**The Big Bet**: Gen Z and early millennials want to save but lack behavioral support. We're betting on social + gamified saving vs. traditional spreadsheet tools.

---

## How We Got Here: Strategic Reasoning

We interviewed 20+ target users and found a clear pattern:

**Key Research Findings**:
- 78% of users who try budgeting apps abandon within 3 months
- #1 reason for abandonment: "Felt like a chore, too depressing to track failures"
- Users follow personal finance creators on TikTok/Instagram but have no app to share savings wins
- YNAB/Mint are feature-rich but feel cold and punitive (focus on mistakes)

**Why These Pillars**: 
- Finding #1 led us to Pillar 1 (Behavioral Design) — users want *enjoyment*, not guilt
- Finding #2 led us to Pillar 2 (Social Proof) — peer support drives habit formation
- Finding #3 led us to Pillar 3 (Goal-Centric) — frame around dreams, not failures

---

## Strategic Pillars

### Pillar 1: Behavioral Design Over Feature Completeness
**Objective**: Every interaction should celebrate progress and build streaks.

**Rationale & Research Evidence**:
- **Research backing**: 20 user interviews with ages 25-35; 78% cited "feels like a chore" as abandonment reason
- **Competitive positioning**: YNAB wins with pedagogy, loses with joy. Mint lost trust. We win on delight + results
- **Success criteria**: 30+ day average streaks, 30% monthly retention (vs current 20%)

### Pillar 2: Social Proof & Peer Accountability
**Objective**: Users feel supported by community, can share wins with friends.

**Rationale & Research Evidence**:
- **Research backing**: Behavioral economics shows peer accountability >personal accountability. TikTok finance community exists but has no native app
- **Competitive positioning**: Neobanks (Chime, Revolut) gamify spending but don't support saving. We do both
- **Success criteria**: 40% of users invite friends within 3 months; friend groups have 20% higher retention

### Pillar 3: Goal-Centric, Not Spending-Centric
**Objective**: Start with "what do you want to save for?" not "how much do you spend?"

**Rationale & Research Evidence**:
- **Research backing**: Users framed their relationship with money around *aspirations* (vacation, home, emergency fund), not guilt
- **Competitive positioning**: YNAB leads with rules (painful). We lead with dreams (exciting)
- **Success criteria**: 50% goal adoption rate; average goal completion time < 12 months

---

## Appendix: Key Assumptions

| Assumption | Validated? | How Validated | Risk if Wrong |
|-----------|-----------|---|---|
| Gen Z/millennials will engage with gamified saving | ❓ Pending | Beta cohort test in Q2 | If false, pivot to simplicity positioning |
| 10% of users will pay for group goals | ❓ Pending | WTP survey in beta | If false, explore ads or B2B partnerships |
| Streaks > feature completeness | ✅ Yes | 20 interviews, 78% cited engagement issue | Low; validated in research |
| Neobank partnerships are feasible | ❓ Pending | Outreach in Q2 | If false, build integrations ourselves |
```

---

## Frequently Asked Questions

**Q: What if we don't have market research or customer interviews yet?**
A: That's OK. I'll ask you to articulate what you *do* know about your customers and why you believe the problem matters. If you can't answer that, strategy is premature — focus on customer discovery first.

**Q: Can we have more than 3 strategic pillars?**
A: Prefer 3. With 4+, you're trying to do everything, which means you're doing nothing. If you have more than 3 ideas, consolidate or deprioritize. Strategy is about choices.

**Q: Should this include a feature roadmap?**
A: No. Roadmaps (features, timelines, owners) are *derived* from strategy, not part of it. This skill generates strategic themes. You'll build a separate Roadmap.md that operationalizes strategy into features.

**Q: How long does this take?**
A: Depends on how much thinking is already done. If you can answer the core questions, ~30 minutes. If we're thinking it through together, 1–2 hours.

**Q: Can you update an existing STRATEGY.md?**
A: Yes. Share the current version, tell me what's changed, and I'll update only what needs to change.

**Q: What's the difference between "Strategic Pillars" and "Roadmap Horizons"?**
A: Strategic Pillars are *timeless themes* (e.g., "Enterprise-Grade Security"). Roadmap Horizons are *time-based execution phases* (e.g., "Q1: Build MVP"). Pillars guide decisions across all horizons; horizons operationalize pillars into milestones.
