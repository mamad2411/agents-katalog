---
name: council
description: "Life advisory council with 8 parallel specialist advisors and synthesis. Dispatches domain-specific advisors (life coach, finance, health, career, learning, systems, relationships, creative) in parallel, synthesizes their outputs into a unified action plan with prioritized next steps. Use when: life planning, goal setting, periodic review, career decision, financial planning, health optimization, relationship advice, productivity systems, creative projects, life direction, organize my life, what should I focus on, I need advice about, quarterly review."
license: MIT
metadata:
  version: 1.0.0
  category: life-planning
  tags: [life-advisory, multi-agent, coaching, goal-setting, reviews, finance, health, career, productivity]
---

## Important: This skill provides structured thinking frameworks, not professional advice. For medical, legal, or financial decisions, always consult qualified professionals.

# Council — Life Advisory Council

Coordinate 8 specialist advisors to analyze any life topic from multiple angles simultaneously. Each advisor brings domain expertise, then a synthesizer resolves conflicts and produces a unified, prioritized action plan.

## How It Works

1. **Topic Analysis** — determines which advisors (3-8) are relevant
2. **Advisor Selection** — picks from the full roster:
   - **Life Coach**: always included (holistic perspective, values alignment)
   - **Finance**: budget, investments, debt strategy
   - **Health**: physical, mental, nutrition, sleep
   - **Career**: development, networking, positioning
   - **Learning**: skill acquisition, courses, deliberate practice
   - **Systems**: time management, workflows, automation
   - **Relationships**: communication, social dynamics, community
   - **Creative**: innovation, projects, aesthetics
3. **Parallel Dispatch** — launches advisors simultaneously using agent files in `agents/`
4. **Synthesis** — `agents/advisor-synthesizer.md` resolves conflicts, finds synergies, produces unified output

## Output

- **Council Summary** — holistic overview
- **Key Synergies** — actions serving multiple domains
- **Prioritized Action Plan** — max 7 focused actions
- **Watch List** — monitor but don't act yet
- **Recommended Follow-ups** — which advisors to consult individually

## Example Output

```
## Prioritized Action Plan
1. **Career**: Start networking in target industry (Career Advisor: 8/10 urgency)
2. **Finance**: Build 6-month runway before transition (Finance Advisor: 9/10 urgency)
3. **Health**: Establish stress management routine (Health Advisor: 7/10 urgency)
4. **Relationships**: Communicate plans with partner (Relationships Advisor: 8/10 urgency)

Advisor Consensus: 6/8 advisors support the transition with conditions.
Key Conflict: Finance says "wait 6 months", Career says "move now" — Synthesizer recommends staged approach.
```

## Usage

```
"I'm considering a career change — convene the council"
"Help me plan my finances for the next quarter"
"I need to optimize my daily routines and productivity"
"Review my progress across all life domains"
"organize my life"
"what should I focus on"
"I need advice about..."
"quarterly review"
```

## Individual Advisors

Use standalone advisor commands for focused sessions:
- `commands/council-life-coach.md` — values, direction, life balance
- `commands/council-finance.md` — budgeting, investing, debt
- `commands/council-health.md` — fitness, nutrition, sleep, mental health
- `commands/council-career.md` — career strategy, networking, positioning
- `commands/council-learning.md` — learning plans, skill development
- `commands/council-systems.md` — workflows, automation, productivity
- `commands/council-relationships.md` — communication, social dynamics
- `commands/council-creative.md` — creative projects, innovation
- `commands/council-review.md` — quarterly/annual structured reviews

## Structure

```
council/
├── SKILL.md                              # This file
├── commands/
│   ├── council.md                        # Main orchestrator (full council)
│   ├── council-life-coach.md             # Life Coach standalone
│   ├── council-finance.md                # Financial Advisor standalone
│   ├── council-health.md                 # Health Director standalone
│   ├── council-career.md                 # Career Strategist standalone
│   ├── council-learning.md               # Learning Architect standalone
│   ├── council-systems.md                # Systems Engineer standalone
│   ├── council-relationships.md          # Relationships Advisor standalone
│   ├── council-creative.md               # Creative Director standalone
│   └── council-review.md                 # Periodic Review Coordinator
├── agents/
│   ├── advisor-life-coach.md
│   ├── advisor-finance.md
│   ├── advisor-health.md
│   ├── advisor-career.md
│   ├── advisor-learning.md
│   ├── advisor-systems.md
│   ├── advisor-relationships.md
│   ├── advisor-creative.md
│   └── advisor-synthesizer.md
├── references/
│   ├── frameworks.md                     # Analysis frameworks per domain
│   ├── assessment-rubrics.md             # 1-10 scoring criteria for reviews
│   └── review-templates.md              # Quarterly/annual review templates
└── data/
    ├── profile.md                        # Your personal context (fill this in)
    ├── goals/
    │   ├── active.md                     # Current goals
    │   └── archive.md                    # Completed/abandoned goals
    ├── tracking/                         # Domain tracking data (auto-populated)
    │   ├── finance.md
    │   ├── health.md
    │   ├── career.md
    │   ├── learning.md
    │   ├── systems.md
    │   ├── relationships.md
    │   └── creative.md
    ├── reviews/                          # Periodic review documents
    └── journal/                          # Session logs (auto-populated)
```

## Setup

After installing, fill in `data/profile.md` with your:
- Core values and life vision
- Current situation (career, finances, health, relationships)
- Priorities (ranked)
- Constraints and considerations
- Communication preferences

This personalizes all advisory sessions to your context.

## Language

All advisors respond in the same language the user writes in. Detected automatically — no configuration needed.
