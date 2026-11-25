---
name: ai-review-fatigue-mitigation
description: Mitigate review fatigue in AI-assisted development — the convergence of vigilance decrement, automation complacency, and context-switching costs that degrades code review quality when reviewing AI-generated output. Covers the three-mechanism stack, the amplifier loop, the verification gap, structural countermeasures from aviation/radiology/cybersecurity, and review-fatigue signal metrics. Use when designing code review practices for AI-assisted teams, building review-quality dashboards, setting WIP limits for AI-generated PRs, or diagnosing why review quality is declining despite stable test coverage. NOT for the decision-density crisis (use coding-agent-decision-fatigue-mitigation) or general AI fatigue measurement (use ai-fatigue-scale-design).
---

# AI Review Fatigue Mitigation

## Overview
AI-assisted development has redirected — not reduced — cognitive load, shifting it toward a kind of reviewing humans aren't built for: evaluating output you didn't conceive, in patterns you didn't choose, at a pace you don't control. Three well-studied phenomena (vigilance decrement, automation complacency, context switching) converge and stack, degrading review quality silently. The solution is structural, not individual.

## When to Use
- Designing code review practices for teams using AI coding assistants or agents
- Building review-quality dashboards and metrics
- Setting WIP limits for AI-generated pull requests
- Diagnosing why review quality is declining despite stable or increasing test coverage
- Establishing team norms for reviewing AI-generated code
- NOT for the decision-density crisis in agentic coding (use `coding-agent-decision-fatigue-mitigation`)
- NOT for general AI fatigue measurement across products (use `ai-fatigue-scale-design`)
- NOT for managing too many concurrent agents (use `ai-brain-fry-defense`)

## Core Process / Workflow

### 1. Understand the three-mechanism stack

| Mechanism | What happens | Key research |
|---|---|---|
| **Vigilance decrement** | Sustained monitoring depletes attention resources; detection performance declines after ~30 minutes | Warm, Parasuraman & Matthews (2008); Klein & Feltmate (2025) — 75-year review |
| **Automation complacency** | When automation is mostly correct, humans over-trust it and detect only ~30% of errors (vs. ~75% when failures are visible) | Parasuraman et al. (1993); McBride, Rogers & Fisk (2014); Bainbridge (1983) — irony of automation |
| **Context switching** | Each switch leaves "attention residue" (Leroy 2009); glutamate accumulates in the lateral prefrontal cortex (Wiehler et al. 2022), making cognitive control literally more expensive over time | Leroy (2009); Wiehler et al. (2022, Current Biology) |

**The key insight:** These don't take turns — they stack. Your attention depletes, your trust inflates, and every context switch makes both worse, simultaneously.

### 2. Recognize the amplifier loop

```
AI increases output volume
    → increases review volume
    → increases vigilance demand + context switches
    → degrades review quality
    → bugs slip through
    → but throughput metrics still go up (erosion is invisible)
```

The system looks productive while judgment degrades. This is the silent quality erosion pattern.

### 3. Name the experience: review fatigue

The point where sustained code review quietly shifts from deep evaluation to surface scanning — not because you stopped caring, but because vigilance decrement, automation complacency, and context-switching costs are all operating on you at once.

**Personal tells:**
- Everything starts looking correct
- The urge to approve grows
- Edge cases stop triggering alarm bells
- You stop asking second-order questions ("what if this input is null?")
- You scan at higher and higher levels instead of understanding
- You start approving faster

### 4. Account for the verification gap

AI makes it easy to generate code in domains you haven't mastered yet. Complacency hits harder when you lack the expertise to spot what's wrong.

- Perry et al. (2023): developers with AI access wrote **less secure code** yet believed they had written **more secure code**
- Goddard, Roudsari & Wyatt (2012): erroneous automated advice was followed at a **26% higher rate** among inexperienced users
- The less you know a domain, the more you trust the machine

### 5. Apply structural countermeasures (from other industries)

The solution is structural, not individual. You cannot train, motivate, or discipline your way past biological limits.

| Countermeasure | Origin industry | Application to AI code review |
|---|---|---|
| **Treat review as high-focus work** | Aviation (cockpit procedures) | Schedule review in protected, uninterrupted windows — not as background noise |
| **Protect uninterrupted review windows** | Air traffic control (mandatory rest between positions) | No meetings, no Slack during review sessions |
| **Normalize stepping away** | NIOSH (breaks every 2 hours); ATC (mandatory rest) | 25-30 min deep review → deliberate break. Stepping away is quality assurance, not lost time |
| **Pair on reviews** | Aviation (two-pilot cockpit) | Two sets of eyes, shared cognitive load, real-time calibration through dialogue. Especially for large AI diffs, unfamiliar domains, late-in-day reviews |
| **Small PRs, small review units** | Software engineering best practice | Break 500-line AI diffs into focused units; don't review large blocks in one pass |
| **Seek out failure (red-green-refactor discipline)** | TU Berlin (Bahner et al. 2008) — exposing operators to automation failures during training decreases complacency | Before accepting AI output, articulate what "incorrect" would look like. If you can't describe the failure mode, you're rubber-stamping |
| **Limit WIP** | Kanban / lean | Every open review thread is an open loop consuming working memory (~4 slots). Finish one before opening the next |
| **Strengthen automated layers** | Type systems, linters, static analysis, CI | If human review is more fallible than assumed, automated layers become more critical — but when tests are also AI-generated, question whether they encode the same flawed assumptions |
| **Document intent** | Architecture Decision Records | Restore the context that makes review meaningful — "does this do what we intended?" not just "does this work?" |
| **Retro on review quality** | Agile retrospectives | "Did we catch ourselves rubber-stamping this sprint? Where did AI code slip through?" |

### 6. Watch the signals (hypotheses to instrument)

| Signal | What it indicates |
|---|---|
| Review approval speed trending faster without PR complexity decrease | Rubber-stamping |
| Review comment density declining; fewer questions per review | Surface scanning |
| Bug escape rate increasing despite stable/increasing test coverage | Quality erosion |
| Late-in-day approvals correlating with higher defect rates | Vigilance depletion by time-of-day |
| PRs approved per day rising without corresponding review time increase | Throughput masking degradation |
| Engineers following AI rather than directing it | Passive acceptance |

### 7. Address the deeper cost

Review isn't just quality assurance — it's how you learn the system you're building. If you skip or rush review, you don't just risk defects — you lose comprehension of the system itself. The cost of review fatigue isn't just escaped bugs; it's eroding the understanding that makes you capable of leading the next round of work.

### 8. Handle the recursive automation problem

Teams are already using AI to review AI-generated code — a pragmatic adaptation. But automating the review of automated output doesn't eliminate the human factors problem; it nests it. Now you're monitoring the monitor, and the same complacency dynamics apply one level up. Bainbridge's irony of automation (1983) is recursive.

**The gates that can't be automated away:** deliberate checkpoints where humans have ownership and accountability — where a person must actively choose to accept rather than passively allowing code to flow through.

## A-Tech Applications

| Product | Application |
|---|---|
| **A-Coder** | Build review-fatigue signals into the IDE dashboard (approval speed trend, comment density, time-of-day defect correlation); implement cooldown prompts when fatigue signals trigger; default to small PR units for AI-generated code |
| **Be Practical** | Module on "Reviewing AI Code Well" — teach the three-mechanism stack, the personal tells, and the structural countermeasures; frame review discipline as a core AI-era engineering skill |
| **Builder's Club** | Community practice guide for AI-assisted review; open-source a review-fatigue metrics MCP tool; publish the structural countermeasure checklist as a team adoption resource |

## References
- See [references/review-fatigue-evidence.md](references/review-fatigue-evidence.md) for the full research base, industry case studies, and cross-references.