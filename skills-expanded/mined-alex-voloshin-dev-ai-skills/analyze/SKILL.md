---
name: analyze
description: Use this skill when the user asks to analyze, investigate, assess, evaluate, compare, or research a codebase, architecture, system, product, market, or research topic in a structured way — including requests that need explicit scope, framework-driven reasoning, and separated facts/inference/recommendation but do not use the word "analyze" — to run a deep analysis workflow producing traceable scope, evidence, and conclusions. Not for quick one-off lookups or implementation work — this is an investigation-and-conclusions workflow.
context: fork
argument-hint: [topic, question, or area to analyze]
---

# Analyze

Perform structured analysis with explicit scope, evidence, and conclusions.

## When to use

- Analyzing, investigating, assessing, or evaluating a codebase, architecture, or system
- Comparing options or alternatives in a structured way
- Researching a product, market, or topic where evidence and conclusions must be traceable
- Any request needing explicit scope, framework-driven reasoning, and separated facts/inference/recommendation
- Not for quick one-off lookups or implementation work — this is an investigation-and-conclusions workflow

## 0. Gather Context

Read `CLAUDE.md` (or `AGENTS.md`) at the project root to understand the project's domain, tech stack, and business context. This shapes framework selection and analysis scope.

## 1. Classify the Request

Identify:

- Subject
- Core question
- Scope
- Desired depth
- Audience
- Decision the analysis should inform

## 2. Choose a Framework

Pick one to three frameworks from `analytical-frameworks.md` based on the question type.

Typical pairings:

- Current-state assessment -> gap analysis, architecture assessment
- Root cause -> 5 Whys, fishbone, causal analysis
- Comparison -> weighted scoring, MCDA
- Strategy -> SWOT, Porter's Five Forces, JTBD
- Technical assessment -> architecture review, technical debt assessment

## 3. Plan the Investigation

Break the work into MECE dimensions.

For each dimension, define:

- What evidence is needed
- Where it will come from
- What would confirm or contradict the current hypothesis

## 4. Collect Evidence

Use the minimum set of relevant sources:

- Repository files and docs
- Structured data or metrics
- Targeted commands
- Web research when current external information is required

Track evidence quality and note assumptions.

## 5. Analyze

Rules:

- Lead with evidence, not opinion
- Consider at least one alternative explanation
- State confidence explicitly
- Separate facts, inference, and recommendation

## 6. Present the Result

Use `output-templates.md` to structure the output.

All outputs should include:

- Executive summary
- Context
- Analysis
- Findings
- Recommendations
- Risks and limitations

## Integration

- **Input from**: direct analysis/investigation/comparison/research request; `CLAUDE.md` or `AGENTS.md` for project domain, tech stack, and business context (step 0)
- **Drives**: framework selection from `analytical-frameworks.md`; output structure from `output-templates.md`
- **Output**: structured deliverable with executive summary, context, analysis, findings, recommendations, and risks/limitations — suitable for hand-off to a decision-maker or a downstream planning/implementation workflow
- **Web research**: used only when current external information is required (step 4)

## Failure modes

- **Opinion before evidence** — recommendations stated without grounding violate step 5; lead with evidence, not opinion
- **No alternative considered** — step 5 requires at least one alternative explanation; a single-hypothesis analysis is incomplete
- **Conflated facts/inference/recommendation** — keep these separate in the output; mixing them hides confidence and assumptions
- **Framework sprawl** — picking more than one to three frameworks (step 2) dilutes focus; constrain to the question type
- **Skipped context gathering** — omitting step 0 leads to mis-scoped framework selection and analysis depth
- **Untracked evidence quality** — failing to note assumptions and source quality (step 4) makes conclusions unverifiable

## Companion Resources

- `analytical-frameworks.md`
- `output-templates.md`
