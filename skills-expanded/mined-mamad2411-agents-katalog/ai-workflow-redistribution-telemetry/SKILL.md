---
name: ai-workflow-redistribution-telemetry
description: Detects and measures how AI coding assistants redistribute developer workflows across productivity, code quality, editing, reuse, and context-switching dimensions using longitudinal telemetry. Use when measuring AI's real impact on developer behavior over time, designing AI-era DevEx dashboards, or investigating perception-behavior gaps in AI tool adoption. NOT for short-term productivity studies or single-task evaluations.
---

# AI Workflow Redistribution Telemetry

## Core Principle

AI coding assistants do not simply accelerate existing workflows — they redistribute effort across five workflow dimensions in ways that often elude developers' own perception. Longitudinal telemetry reveals behavioral shifts that surveys and self-report miss.

## The Evidence

Based on the JetBrains HAX team's mixed-methods study (Fraser & Sergeyuk, ICSE 2026, April 2026). Two years of telemetry from 800 developers (400 AI users, 400 non-users) across IntelliJ IDEA, PyCharm, PhpStorm, and WebStorm, combined with surveys (62 respondents) and interviews.

### The Five Workflow Dimensions

## 1. Productivity (Typed Characters)

**Behavior**: AI users increased typed characters by ~600/month vs ~75/month for non-users — a sustained, growing gap over two years.

**Perception**: 80%+ reported increased productivity; half reported decreased coding time.

**Alignment**: Behavior and perception ALIGNED. Developers produce more code and perceive productivity gains.

## 2. Code Quality (Debugging Session Starts)

**Behavior**: No significant change in debugging frequency for AI users. Slight decrease for non-users.

**Perception**: ~50% reported increased code quality; ~43% reported increased readability; only ~10% reported decreased quality.

**Alignment**: Behavior and perception DIVERGE. Developers perceive quality improvements but debugging behavior is unchanged.

## 3. Code Editing (Delete and Undo Actions)

**Behavior**: AI users increased deletions by ~100/month vs ~7/month for non-users — a stark rise in rework.

**Perception**: Half reported no perceived change in editing behavior; ~40% reported slight/significant increase.

**Alignment**: Behavior and perception DIVERGE INVERTED. Telemetry shows large increase in editing/rework that developers don't perceive.

## 4. Code Reuse (External Pastes Without In-IDE Copy)

**Behavior**: AI users show higher external paste rates but no significant change over time for either group.

**Perception**: ~33% reported increased reuse; ~20% reported decreased; ~44% no change.

**Alignment**: No clear divergence — both behavior and perception show modest patterns.

## 5. Context Switching (IDE Window Activations)

**Behavior**: AI users show ~6 more IDE activations/month; non-users show ~7 fewer — AI users switch context at least as much, if not more.

**Perception**: ~25% reported increase, ~20% decrease, ~50% no change.

**Alignment**: Behavior and perception DIVERGE. Telemetry shows increased context switching that developers don't report.

## The Perception-Behavior Gap Matrix

| Dimension | Behavior Change | Perception Change | Gap Type |
|---|---|---|---|
| Productivity | Large increase | Increase reported | Aligned |
| Code quality | No change | Increase reported | Perception overestimates |
| Code editing | Large increase | Little change reported | Perception underestimates |
| Code reuse | Small/no change | Mixed reports | No clear gap |
| Context switching | Slight increase | Mixed reports | Perception underestimates |

## Key Insight

AI tools redistribute developer workflows in ways that are **subtle enough that developers don't always see them clearly in their own habits**. The largest behavioral shift (increased code editing/rework) is the least perceived. This is the core finding: **AI reshapes what developers do, not just how fast they do it.**

## The Telemetry Methodology

### Data Collection
- Anonymized IDE usage logs (characters typed, not content)
- Monthly aggregation per device
- Two-year window (October 2022 — October 2024)
- 151,904,543 total logged events

### Group Definition
- AI users: interacted with JetBrains AI Assistant ≥1x/month from April-October 2024
- Non-users: never used AI Assistant during study period
- Both groups active in both October 2022 and October 2024

### Metrics
- Productivity: typed characters per month
- Code quality: debugging session starts per month
- Code editing: delete and undo actions per month
- Code reuse: external paste events (paste without prior in-IDE copy) per month
- Context switching: IDE window activations per month

## Measurement Framework for A-Tech

### The Redistribution Dashboard

Track all five dimensions simultaneously:
1. **Productivity**: Code output volume (tokens, lines, characters)
2. **Code quality**: Debugging frequency, error rates, test pass rates
3. **Code editing**: Deletion/undo frequency, modification rate of AI-generated code
4. **Code reuse**: External snippet integration, AI suggestion acceptance rate
5. **Context switching**: IDE/tool switches per hour, focus duration

### The Perception-Behavior Audit

Quarterly comparison:
- Self-reported workflow changes (survey)
- Telemetry-measured workflow changes (logs)
- Gap analysis (where perception diverges from behavior)
- Intervention design (where gaps indicate problems)

## A-Tech Applications

### A-Coder
- **Five-dimension dashboard**: Real-time telemetry across all five workflow dimensions
- **Perception-behavior gap alert**: Flag when developer perception significantly diverges from telemetry (e.g., "You report no change in editing, but your undo rate has increased 3x")
- **Context switching reducer**: Identify high-frequency context switchers and suggest focus-mode interventions
- **Rework tracker**: Monitor deletion/undo rates as a leading indicator of AI output quality issues

### Be Practical
- **Workflow redistribution curriculum**: Teach the five dimensions and the perception-behavior gap
- **Self-audit tool**: Help developers compare their self-perception to their telemetry
- **Anti-pattern guide**: Common redistribution patterns and their implications

### Builder's Club
- **Open-source telemetry toolkit**: Five-dimension measurement framework as an MCP tool
- **Community benchmark**: Aggregate redistribution patterns across open-source projects
- **Perception gap dataset**: Community-contributed perception vs. behavior data for research

## Cross-References

- `unified-devex-measurement-stack-2026` — The measurement framework; this skill adds the redistribution dimension
- `ai-productivity-output-volume-paradox` — Output volume mechanism; this skill shows the broader redistribution pattern
- `prompt-wait-evaluate-flow-collapse` — Flow collapse; this skill provides the telemetry evidence
- `devex-verification-bottleneck-framework` — Verification bottleneck; this skill shows the editing/rework dimension
- `genai-interaction-type-selection` — Interaction type selection; this skill shows the behavioral impact of different interaction patterns
- `ai-era-devex-measurement-at-scale` — DevEx at scale; this skill adds the longitudinal telemetry method
- `botsitting-botshitting-cycle` — Hidden human labor; this skill provides the measurement infrastructure

## Anti-Patterns

1. **Measure only productivity** — Misses the redistribution to editing, context switching, and quality dimensions
2. **Trust self-report alone** — The largest behavioral shift (editing) is the least perceived
3. **Short measurement windows** — Redistribution patterns emerge over months, not days
4. **Single-metric optimization** — Optimizing productivity without monitoring editing/rework creates hidden technical debt
5. **Assume AI reduces context switching** — Telemetry shows AI users switch context at least as much

## Limitations

- JetBrains IDEs only; VS Code, Cursor, other tools may show different patterns
- "AI user" defined as monthly JetBrains AI Assistant use; lighter users may differ
- Telemetry proxies are imperfect (e.g., debugging starts ≠ code quality)
- 2022-2024 window; agentic tools (Claude Code, Codex) may create different redistribution patterns
- No causal claims; observational study identifies patterns, not causes