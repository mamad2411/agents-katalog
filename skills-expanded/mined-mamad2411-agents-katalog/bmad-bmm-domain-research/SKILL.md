---
name: bmad-bmm-domain-research
description: >-
  Use this skill to conduct comprehensive, web-verified domain or industry
  research and produce a structured research report with citations. Invoke when
  the user says "research a domain", "create a domain research report about
  [industry]", or when a project needs industry analysis before planning begins.
  The skill facilitates discovery of research scope, then systematically
  researches industry size and growth, competitive landscape, regulatory
  requirements and compliance frameworks, and technical trends — verifying all
  claims against current public sources via multi-source web search. Output is
  a comprehensive research document saved to the planning artifacts folder.
  Requires web search to be available; aborts immediately if unavailable.
  Unlike bmad-bmm-market-research (which focuses on customers, pain points, and
  buying behavior), this skill focuses on industry structure, regulations, and
  technology trends. Do not invoke without a specific domain or industry topic.
argument-hint: "Provide the domain, industry, or sector to research (e.g., 'healthcare technology', 'sustainable packaging')."
metadata:
  bmad:
    module: bmm
    type: workflow
---

# Domain Research

Conduct comprehensive domain/industry research using web data and verified sources.

## Outcome

A comprehensive domain/industry research document with verified citations covering industry analysis, competitive landscape, regulatory requirements, technical trends, and strategic synthesis.

## Your Role

Domain research facilitator working with an expert partner. You bring research methodology and web search capabilities, while your partner brings domain knowledge and research direction. Continue to operate with your given name, identity, and communication_style, merged with this role.

## Prerequisite

**Web search required.** If unavailable, abort and tell the user.

## Core Rules

- All claims must be verified against current public sources via web search.
- Multi-source validation for critical domain claims.
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

"Welcome {{user_name}}! Let's get started with your **domain/industry research**.

**What domain, industry, or sector do you want to research?**

For example:
- 'The healthcare technology industry'
- 'Sustainable packaging regulations in Europe'
- 'Construction and building materials sector'
- 'Or any other domain you have in mind...'"

3. Based on the user's topic, briefly clarify:
   - **Core Domain**: "What specific aspect of [domain] are you most interested in?"
   - **Research Goals**: "What do you hope to achieve with this research?"
   - **Scope**: "Should we focus broadly or dive deep into specific aspects?"

4. Set `research_type = "domain"`, `research_topic`, and `research_goals` from the discussion.

5. Create the starter output file: `{planning_artifacts}/research/domain-{{research_topic}}-research-{{date}}.md` using the research template from `./data/research-template.md`.

## Execution Order

Follow these steps in order. Each step file contains the full procedure.

1. [Confirm Scope](./steps/confirm-scope.md) — Confirm domain research scope and approach with user
2. [Analyze Industry](./steps/analyze-industry.md) — Market size, growth dynamics, and industry structure
3. [Analyze Competition](./steps/analyze-competition.md) — Key players, market share, and competitive dynamics
4. [Analyze Regulations](./steps/analyze-regulations.md) — Regulatory requirements and compliance frameworks
5. [Analyze Technology](./steps/analyze-technology.md) — Technical trends, emerging technologies, and innovation
6. [Synthesize Research](./steps/synthesize-research.md) — Executive summary, strategic synthesis, and final document

## Halt Conditions

- HALT if web search is unavailable — this skill explicitly requires web search and cannot produce verified research without it
- HALT if the user cannot provide a domain or industry topic after repeated prompting — research cannot proceed without a defined subject
- HALT if the research topic is so broad (e.g., "all industries") that no meaningful scoping can be agreed upon after facilitation
- HALT if web search returns no usable results for the specified domain across multiple query attempts
- HALT if the research template (`./data/research-template.md`) is unreadable

## Data Files

- [./data/research-template.md](./data/research-template.md) — Research document template for initialization

## When to Use

Use this skill when:
- The user says "research a domain" or "create a domain research report about [industry]"
- The user needs comprehensive domain/industry research with verified citations (e.g., "the healthcare technology industry", "sustainable packaging regulations in Europe")
- A project needs industry analysis, competitive landscape, regulatory requirements, and technical trends research before planning begins
- Web search is available (this skill requires web search — aborts if unavailable)

