---
name: genai-interaction-type-selection
description: Selects the optimal GenAI coding interaction type (in-code suggestions, chat, or combined) for a given task to maximize efficiency and minimize cognitive load. Use when designing AI coding assistant workflows, creating interaction guidance for developers, or optimizing AI tool adoption patterns. NOT for general productivity measurement or model selection decisions.
---

# GenAI Interaction Type Selection

## Core Principle

GenAI coding assistants offer multiple interaction types (in-code suggestions, chat, in-line chat), but combining them within a single task diminishes benefits. The interaction type must be matched to task characteristics upfront, not switched mid-task.

## The Evidence

Based on the SAP mixed-methods field study (Brandebusemeyer, Zunic, Zimmermann, Schimmer & Arnrich, arXiv:2607.02337, July 2026). 22 professional developers observed over four days with controlled and uncontrolled study phases. GitHub Copilot used in controlled sessions; free choice in uncontrolled periods.

### Key Findings

1. **Using one interaction type improves efficiency and reduces workload** — Either in-code suggestions OR chat alone significantly reduced task duration and perceived workload (NASA-TLX) compared to no Copilot use.

2. **Combining interaction types eliminates benefits** — Using both in-code suggestions and chat within a single task produced task durations and workload levels comparable to no Copilot use at all. Switching between interaction modes introduces cognitive overhead.

3. **Chat boosts task completion** — Only chat-based interaction significantly increased task completion likelihood. In-code suggestions alone or combined usage showed no significant effect on accuracy.

4. **In-code suggestions preferred for coding** — 14 of 20 participants used in-code suggestions more than 50% of the time. Rated higher in satisfaction and perceived productivity for simple code changes.

5. **Chat preferred for debugging and non-coding tasks** — Better for tasks requiring broader codebase context, explanations, and higher-level reasoning.

6. **AI increases cognitive load in development tasks** — In uncontrolled work periods, AI-assisted development-heavy tasks showed significantly higher cognitive load (EMM 4.72 vs 4.14, d=0.34) but comparable productivity. Cognitive load comes from AI interaction itself (switching, verifying, steering), not from the task.

7. **Helpful AI boosts productivity without adding load** — When AI was perceived as helpful, productivity was significantly higher (EMM 4.00 vs 3.27, d=0.83) with no significant change in cognitive load.

## The Rule-of-Thumb Framework

### Decision Questions

Ask before starting a task:
- Is the task primarily coding or non-coding related?
- How much codebase context does the model need?
- Are explanations of the output required?

### Interaction Type Selection Matrix

| Task Characteristic | Recommended Interaction | Rationale |
|---|---|---|
| Simple code changes, boilerplate, documentation, testing | In-code suggestions | Low context needed, rapid iteration, supports flow |
| Debugging, brainstorming, summaries, codebase exploration | Chat | Broader context, explanations needed, higher-level reasoning |
| Complex multi-file changes requiring both | Plan first, then pick one | Switching mid-task eliminates efficiency gains |
| Unfamiliar framework/language | Chat | Explanations accelerate learning and onboarding |

### The Anti-Pattern: Interaction Switching

Switching between in-code suggestions and chat during a single task is the primary failure mode. Each switch forces:
- Context reload (what was the model doing?)
- Mode adjustment (how do I phrase this now?)
- Verification restart (is this output consistent with the previous mode?)

The result: task duration and workload return to no-Copilot baselines.

## Measurement Framework

### Efficiency Metrics
- Task duration (time from start to completion)
- Interaction count (number of AI invocations per task)
- Interaction type switches per task (target: 0)

### Quality Metrics
- Task completion rate
- Output accuracy (does it meet requirements?)

### Experience Metrics
- NASA-TLX perceived workload score
- Perceived helpfulness (helpful / not helpful binary per task)
- Cognitive load rating per task category

## A-Tech Applications

### A-Coder
- **Interaction type indicator**: Show the recommended interaction type for the current task category in the UI
- **Switch warning**: Alert when a developer switches interaction types mid-task ("Switching modes may reduce efficiency — consider finishing the current approach first")
- **Cognitive load dashboard**: Track AI-assisted task cognitive load vs non-AI task cognitive load
- **Helpfulness feedback loop**: Quick "was this helpful?" toggle to correlate with productivity metrics

### Be Practical
- **Interaction type curriculum**: Teach the rule-of-thumb as a core GenAI workflow skill
- **Task-type matching exercise**: Practice matching task types to interaction types
- **Anti-pattern demonstration**: Show the efficiency loss from interaction switching

### Builder's Club
- **Community interaction patterns**: Share effective interaction patterns for specific frameworks
- **Open-source interaction guide**: Publish the rule-of-thumb as a community resource
- **Interaction type A/B testing**: Community experiments comparing interaction types for specific task categories

## Cross-References

- `prompt-wait-evaluate-flow-collapse` — The flow collapse mechanism; this skill provides the interaction-type dimension
- `ai-skill-formation-interaction-patterns` — The six interaction patterns; this skill adds the task-matching layer
- `calm-technology-ai-coding` — Calm technology principles; this skill provides the interaction-type selection mechanism
- `ai-productivity-output-volume-paradox` — Output volume mechanism; this skill explains the interaction-type variable
- `devex-verification-bottleneck-framework` — Verification bottleneck; this skill shows how interaction type affects verification load
- `ai-experience-design-2026` — AX design; this skill provides the interaction-level design pattern
- `unified-devex-measurement-stack-2026` — Measurement stack; this skill adds the interaction-type metric layer

## Anti-Patterns

1. **Default to chat for everything** — Chat is slower for simple code changes and reduces satisfaction
2. **Default to in-code for everything** — In-code suggestions lack the context for debugging and complex reasoning
3. **Let the developer figure it out** — Without guidance, developers switch modes reactively, eliminating efficiency gains
4. **Measure only productivity** — Cognitive load from AI interaction is invisible without workload measurement
5. **Assume more AI = more productivity** — AI increases cognitive load in development tasks; helpfulness, not usage, drives productivity gains

## Limitations

- Study used GitHub Copilot specifically; other tools (Cursor, Claude Code) may have different interaction type dynamics
- Controlled sessions used Java; interaction preferences may vary by language
- 22 developers at SAP; generalizability across organizations untested
- Task categories were predefined; real-world task boundaries are fuzzier
- Physiological data (wristband) collected but not analyzed in this paper