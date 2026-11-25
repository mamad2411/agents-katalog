---
name: bmad-bmm-market-research
description: >-
  Use this skill to conduct comprehensive, web-verified market research focused
  on customers, competition, and buying behavior, producing a structured report
  with cited sources. Invoke when the user says "create a market research report
  about [topic]", "research the market for [idea]", or when a project needs
  customer insights before product planning begins. The skill facilitates scope
  definition, then systematically researches customer behavior patterns and
  demographics, pain points and unmet needs, decision-making processes and
  journey mapping, and competitive landscape and market positioning. Output is a
  market research document with strategic recommendations saved to the planning
  artifacts folder. Requires web search; aborts if unavailable. Unlike bmad-bmm-
  domain-research (which focuses on industry structure and regulations), this
  skill is customer and competition focused. Unlike bmad-bmm-technical-research,
  this skill does not cover technology choices or architecture patterns.
argument-hint: "Provide the market topic, problem, or area to research (e.g., 'electric vehicle market in Europe', 'plant-based food alternatives')."
metadata:
  bmad:
    module: bmm
    type: workflow
---

# Market Research

Conduct comprehensive market research on competition and customers using web data and verified sources.

## Outcome

A comprehensive market research document with verified citations covering customer behavior, pain points, decision processes, competitive landscape, strategic recommendations, and implementation guidance.

## Your Role

Market research facilitator working with an expert partner. You bring research methodology and web search capabilities, while your partner brings domain knowledge and research direction. Continue to operate with your given name, identity, and communication_style, merged with this role.

## Prerequisite

**Web search required.** If unavailable, abort and tell the user.

## Core Rules

- All claims must be verified against current public sources via web search.
- Multi-source validation for critical market claims.
- Apply confidence levels for uncertain information.
- Write research content to the document immediately after each analysis step.
- Execute steps in strict sequential order. Do not skip or reorder.
- At every step menu, halt and wait for user input before proceeding.
- Track progress via `stepsCompleted` array in the output document's frontmatter.
- Always speak in your agent communication style using the configured `{communication_language}`.

## Initialization

Before starting Step 1, load and resolve configuration:

1. `Invoke skill: bmad-core-config` — loads core config and auto-delegates to `bmad-bmm-config` for module-specific values (`project_name`, `planning_artifacts`, `output_folder`, `user_name`, `communication_language`, `document_output_language`, `user_skill_level`, etc.).

2. Conduct quick topic discovery:

"Welcome {{user_name}}! Let's get started with your **market research**.

**What topic, problem, or area do you want to research?**

For example:
- 'The electric vehicle market in Europe'
- 'Plant-based food alternatives market'
- 'Mobile payment solutions in Southeast Asia'
- 'Or anything else you have in mind...'"

3. Based on the user's topic, briefly clarify:
   - **Core Topic**: "What exactly about [topic] are you most interested in?"
   - **Research Goals**: "What do you hope to achieve with this research?"
   - **Scope**: "Should we focus broadly or dive deep into specific aspects?"

4. Set `research_type = "market"`, `research_topic`, and `research_goals` from the discussion.

5. Create the starter output file: `{planning_artifacts}/research/market-{{research_topic}}-research-{{date}}.md` using the research template from `./data/research-template.md`.

## Execution Order

Follow these steps in order. Each step file contains the full procedure.

1. [Initialize](./steps/initialize.md) — Confirm understanding and establish research scope
2. [Analyze Customer Behavior](./steps/analyze-customer-behavior.md) — Customer behavior patterns, demographics, and psychographics
3. [Analyze Pain Points](./steps/analyze-pain-points.md) — Customer challenges, unmet needs, and barriers
4. [Analyze Decisions](./steps/analyze-decisions.md) — Customer decision processes and journey mapping
5. [Analyze Competition](./steps/analyze-competition.md) — Competitive landscape and market positioning
6. [Synthesize Research](./steps/synthesize-research.md) — Strategic synthesis, executive summary, and final document

## Halt Conditions

- HALT if web search is unavailable — this skill explicitly requires web search and cannot produce verified market data without it
- HALT if the user cannot provide a market topic, problem, or area after repeated prompting — research cannot proceed without a defined subject
- HALT if the market topic is too vague (e.g., "the whole economy") and no meaningful scope can be agreed upon after facilitation
- HALT if web search returns no usable results for the specified market across multiple query attempts
- HALT if the research template (`./data/research-template.md`) is unreadable

## Data Files

- [./data/research-template.md](./data/research-template.md) — Research document template for initialization

## When to Use

Use this skill when:
- The user says "create a market research report about [topic]" or "research the market for [idea]"
- The user needs comprehensive market research on competition and customers with verified citations (e.g., "electric vehicle market in Europe", "plant-based food alternatives")
- A project needs customer behavior, pain points, decision processes, and competitive landscape analysis before planning begins
- Web search is available (this skill requires web search — aborts if unavailable)

