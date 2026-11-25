---
name: "ux-researcher-designer"
description: UX research and design toolkit for Senior UX Designer/Researcher including data-driven persona generation, journey mapping, usability testing frameworks, and research synthesis. Use for user research, persona creation, journey mapping, and design validation.
---

# UX Researcher & Designer

Generate user personas from research data, create journey maps, plan usability
tests, and synthesize research findings into actionable design recommendations.

## When to apply

Use this skill when the operator wants to:

- Create a research-backed user persona.
- Build a customer or product journey map.
- Plan or analyze a usability test.
- Synthesize interviews, surveys, or observational research.
- Define user archetypes, empathy maps, or pain points.
- Calculate sample sizes or pick the right research method.

Trigger phrases include: "create user persona", "generate persona from data",
"build customer journey map", "plan usability test", "synthesize interview
findings", "calculate research sample size", "create empathy map".

Do not use this skill for: pure visual design, marketing personas based on
purchase intent only, or product analytics without a research component.

## Required input contract

Before producing any artifact, identify:

- **Decision the artifact supports** — what gets decided with this output.
- **Audience** — designer, PM, executive, customer-facing team.
- **Source data available** — interviews, surveys, analytics, support tickets,
  session recordings. Note volume and recency.
- **Sample size and recency** — drives confidence level and method choice.
- **Privacy posture** — consent recorded, retention window, redaction status.

If the operator requests a persona or journey map without ≥ 2 data sources,
ask one sharp question to surface what data exists before drafting.

## Method selection

| Question Type | Best Method | Sample Size |
|---------------|-------------|-------------|
| "What do users do?" | Analytics, observation | 100+ events |
| "Why do they do it?" | Interviews | 8-15 users |
| "How well can they do it?" | Usability test | 5-8 users |
| "What do they prefer?" | Survey, A/B test | 50+ users |
| "What do they feel?" | Diary study, interviews | 10-15 users |

Extended table (longitudinal, segmented): `references/research-workflow.md`.

## Core workflows

### 1. Generate User Persona

1. Prepare user data (JSON: demographics, usage, features, pain points).
2. Run `python scripts/persona_generator.py` (or `json` for machine output).
3. Review archetype, demographics, goals, frustrations with frequency counts, design implications.
4. Validate with 3-5 real users + cross-check support tickets + analytics.

### 2. Create Journey Map

1. Define scope: persona, goal, start, end, timeframe.
2. Gather data from interviews, recordings, analytics, support.
3. Map stages (e.g., Awareness → Evaluation → Onboarding → Adoption → Advocacy).
4. Fill layers per stage: Actions, Touchpoints, Emotions (1-5), Pain, Opportunities.
5. Score opportunities: `Frequency × Severity × Solvability`.

### 3. Plan Usability Test

1. Convert vague goals into testable questions.
2. Pick method (moderated 5-8 / unmoderated 10-20 / guerrilla 3-5).
3. Design tasks as scenario + goal + success criterion (not instructions).
4. Define success metrics (completion > 80%, time < 2×, error < 15%, satisfaction > 4/5).
5. Prepare moderator guide with think-aloud + non-leading prompts.

### 4. Synthesize Research

1. Code data: `[GOAL]`, `[PAIN]`, `[BEHAVIOR]`, `[CONTEXT]`, `[QUOTE]`.
2. Cluster patterns (≥ 3 participants = pattern; below that = hypothesis).
3. Calculate segment sizes and viability.
4. Extract findings: statement + evidence + frequency + business impact + recommendation.
5. Prioritize opportunities by Frequency × Severity × Solvability (or FBS-S 4-axis).

Full step-by-step procedures: `references/research-workflow.md`.
Templates (interview guide, survey, moderator script, empathy map, journey layers):
`references/methods-and-templates.md`.
Coding, finding statements, reporting templates: `references/synthesis-and-artifacts.md`.

## Safety, privacy, and consent

- Treat all research data as PII by default.
- Obtain explicit recorded consent before any session; state purpose, recording, retention, anonymization, right to withdraw.
- Mask sensitive on-screen data before recording.
- Use participant IDs (P01, P02) in artifacts, not names.
- Apply retention window from consent (default 90 days raw / 12 months redacted).
- Never paste raw participant data into shared chat tools or third-party LLMs without an explicit data-handling check.
- Never re-identify pseudonymized participants, attribute quotes by name when consent was anonymous, or publish demographics that single out an individual in a small segment.
- Escalate findings that touch accessibility/age-gating compliance, retention or collection changes, or contradict recently shipped major decisions.

Full privacy detail: `references/privacy-validation-and-troubleshooting.md`.

## Validation gates

Every artifact must pass its gate before being delivered.

| Artifact | Gate |
|----------|------|
| Persona | 20+ users, ≥ 2 data sources, goals + frustrations (with frequency) + design implications + confidence stated |
| Journey map | Scope defined; based on real data; all 5 layers filled; opportunities prioritized |
| Usability test | Testable questions; tasks are scenarios not instructions; 5+ participants/design; success metrics defined; severity ratings on findings |
| Synthesis | Consistent coding; patterns ≥ 3 data points; findings carry evidence + frequency + business impact; recommendations actionable + prioritized |

Full checklists: `references/privacy-validation-and-troubleshooting.md`.

## Confidence and severity scales

| Sample Size | Confidence | Use Case |
|-------------|------------|----------|
| 5-10 users | Low | Exploratory |
| 11-30 users | Medium | Directional |
| 31+ users | High | Production |

| Severity | Definition | Action |
|----------|------------|--------|
| 4 - Critical | Prevents task completion | Fix immediately |
| 3 - Major | Significant difficulty | Fix before release |
| 2 - Minor | Causes hesitation | Fix when possible |
| 1 - Cosmetic | Noticed but not problematic | Low priority |

## Output expectations

| Request | You produce |
|---------|-------------|
| "Create a persona" | Persona one-pager with goals, frustrations (with frequency), design implications, sample size, confidence |
| "Map the journey" | Journey one-pager with stages × layers + top 3 prioritized opportunities |
| "Plan a usability test" | Test plan: questions, method, tasks, success metrics, moderator guide |
| "Synthesize this research" | Readout: question, method/sample, top 3 findings with evidence, recommendations table, confidence + limitations |

Worked examples for each: `references/examples.md`.

## Tool reference

`scripts/persona_generator.py`

| Argument | Values | Default | Description |
|----------|--------|---------|-------------|
| format | (none), json | (none) | Output format |

Archetypes: power_user, casual_user, business_user, mobile_first. Persona
components, archetype signals, and sample output: `references/methods-and-templates.md`, `references/examples.md`.

## Reference map

| Need | Read |
|------|------|
| Full step-by-step for all 4 workflows + extended method selection | `references/research-workflow.md` |
| Interview / survey / moderator templates, archetypes, persona components, empathy map, journey layers | `references/methods-and-templates.md` |
| Coding scheme, clustering, finding statement, prioritization, reporting templates | `references/synthesis-and-artifacts.md` |
| Consent and privacy rules, validation checklists, anti-patterns, troubleshooting, escalation | `references/privacy-validation-and-troubleshooting.md` |
| Worked outputs: persona, journey, usability findings, readout | `references/examples.md` |

## Related skills

- `product-team/ui-design-system/` — research findings inform design system decisions.
- `product-team/product-manager-toolkit/` — customer interview analysis complements persona research.
