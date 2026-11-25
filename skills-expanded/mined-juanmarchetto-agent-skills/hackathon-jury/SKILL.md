---
name: hackathon-jury
description: "Simulate a real hackathon jury evaluating your project. Researches actual jury members via web search, builds personalized juror personas, dispatches parallel evaluations, and synthesizes a deliberation with scores, feedback, and pitch coaching. Use when: hackathon, jury, evaluate my project, hackathon submission, judge my project, prepare for hackathon, hackathon feedback, hackathon prep."
license: MIT
metadata:
  version: 1.0.0
  category: evaluation
  tags: [hackathon, jury, evaluation, competition, pitch, multi-agent]
---

# Hackathon Jury Simulator

Simulate a complete hackathon jury evaluation. Given a project and a hackathon event name, this skill researches the real jury members, builds personalized juror personas, and evaluates the project from each juror's perspective.

## How It Works

1. **Project Discovery** — analyze the project's architecture, code quality, README, and git history
2. **Hackathon Research** — use WebSearch to find real jury members, judging criteria, past winners, and sponsor priorities (see `agents/researcher.md`)
3. **Jury Construction** — build 3-7 juror personas based on real people or representative archetypes
4. **Parallel Evaluation** — dispatch each juror as a parallel agent using `agents/juror.md`, each evaluating from their unique perspective
5. **Deliberation Synthesis** — simulate jury deliberation using `agents/synthesizer.md`, resolving disagreements and estimating placement

## Usage

```
"Evaluate my project for the Colosseum Eternals hackathon"
"How would the ETHGlobal Bangkok judges score this repo?"
"Prep me for the Solana Breakpoint hackathon — judge my submission at ./my-project"
```

## Output

The evaluation produces:

1. **Verdict Overview** — overall score, placement estimate, one-sentence consensus
2. **Jury Scorecard** — per-criterion scores from each juror with weighted averages
3. **Individual Juror Feedback** — what impressed them, what concerned them, questions they'd ask
4. **Deliberation Simulation** — points of agreement, debate, and what would swing the decision
5. **Competitive Position** — strength vs typical submissions, what would beat this project
6. **Improvement Roadmap** — max 7 prioritized actions (quick wins + strategic moves)
7. **Pitch Coaching** — optimal demo flow, buzzwords, what to emphasize vs downplay

## Agent Files

| Agent | Purpose |
|-------|---------|
| `agents/researcher.md` | Researches hackathon event, jury members, criteria, past winners, sponsors |
| `agents/juror.md` | Role-plays as a specific juror, evaluates from their perspective |
| `agents/synthesizer.md` | Simulates deliberation, produces unified verdict and recommendations |

## References

| File | Content |
|------|---------|
| `references/default-criteria.md` | Default judging criteria when hackathon-specific ones aren't found (universal + ecosystem-specific) |

## Important Notes

- **WebSearch is critical** — the value is in researching REAL jury members and criteria, not fabricating them
- If jury member info is scarce, construct archetypes based on organizers, sponsors, and ecosystem
- Always include at least one technical judge, one business/impact judge, and one ecosystem judge
- Be brutally honest — sugarcoating defeats the purpose
- Score relative to hackathon caliber (local event vs major global competition)
- Demo quality matters as much as technical quality at hackathons

## Example Output

A condensed version of the jury scorecard produced by this skill:

```
| Criterion      | Weight | Juror 1 (VC) | Juror 2 (Tech) | Juror 3 (Ecosystem) | Avg  |
|----------------|--------|-------------|---------------|-------------------|------|
| Innovation     | 25%    | 8           | 7             | 9                 | 8.0  |
| Technical      | 25%    | 6           | 9             | 7                 | 7.3  |
| UX/Design      | 15%    | 7           | 5             | 6                 | 6.0  |
| Impact         | 20%    | 8           | 6             | 8                 | 7.3  |
| Presentation   | 15%    | 7           | 7             | 8                 | 7.3  |
| **Overall**    |        | **7.2**     | **7.0**       | **7.8**           | **7.3** |

Placement: Top 15% — Strong finalist, needs one champion juror to win
```

This is followed by individual juror feedback (what impressed them, concerns, questions they would ask), a deliberation simulation, competitive positioning, an improvement roadmap (max 7 prioritized actions), and pitch coaching.

## Without WebSearch

If WebSearch is not available, the skill uses default criteria from `references/default-criteria.md` and constructs archetype jurors instead of researching real people:

- **Technical Judge** — evaluates architecture, code quality, scalability, and technical innovation
- **Business Judge** — evaluates market fit, revenue model, user acquisition, and growth potential
- **Ecosystem Judge** — evaluates community impact, ecosystem alignment, composability, and adoption potential

The evaluation is still valuable but loses the personalization that comes from researching real jury members, their backgrounds, and their known preferences. When WebSearch is available, always prefer it for more accurate and targeted feedback
