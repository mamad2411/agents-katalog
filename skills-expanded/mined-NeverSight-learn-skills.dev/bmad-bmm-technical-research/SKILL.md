---
name: bmad-bmm-technical-research
description: >-
  Use this skill to conduct comprehensive, web-verified technical research on
  technologies, frameworks, APIs, or architectural patterns and produce a
  structured report with cited sources. Invoke when the user says "create a
  technical research report on [topic]", "research the technology for [area]",
  or when a project needs technology comparison or architectural guidance before
  implementation decisions. The skill facilitates scope definition, then
  systematically researches the tech stack, integration patterns, APIs,
  architectural patterns, and implementation approaches — verifying all claims
  against current public sources. Output is a strategic research document with
  recommendations saved to the planning artifacts folder. Requires web search;
  aborts if unavailable. Unlike bmad-bmm-domain-research (industry structure and
  regulations) and bmad-bmm-market-research (customers and competition), this
  skill focuses on technical choices. Best for framework comparisons,
  architecture decisions, and API evaluations.
argument-hint: "Provide the technology, tool, or technical area to research (e.g., 'React vs Vue', 'GraphQL vs REST', 'serverless deployment options')."
metadata:
  bmad:
    module: bmm
    type: workflow
---

# Technical Research

Conduct comprehensive technical research on technologies and architecture using web data and verified sources.

## Outcome

A comprehensive technical research document with verified citations covering technology stack analysis, integration patterns, architectural patterns, implementation approaches, and strategic technical recommendations.

## Your Role

Technical research facilitator working with an expert partner. You bring research methodology and web search capabilities, while your partner brings domain knowledge and research direction. Continue to operate with your given name, identity, and communication_style, merged with this role.

## Prerequisite

**Web search required.** If unavailable, abort and tell the user.

## Core Rules

- All claims must be verified against current public sources via web search.
- Multi-source validation for critical technical claims.
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

"Welcome {{user_name}}! Let's get started with your **technical research**.

**What technology, tool, or technical area do you want to research?**

For example:
- 'React vs Vue for large-scale applications'
- 'GraphQL vs REST API architectures'
- 'Serverless deployment options for Node.js'
- 'Or any other technical topic you have in mind...'"

3. Based on the user's topic, briefly clarify:
   - **Core Technology**: "What specific aspect of [technology] are you most interested in?"
   - **Research Goals**: "What do you hope to achieve with this research?"
   - **Scope**: "Should we focus broadly or dive deep into specific aspects?"

4. Set `research_type = "technical"`, `research_topic`, and `research_goals` from the discussion.

5. Create the starter output file: `{planning_artifacts}/research/technical-{{research_topic}}-research-{{date}}.md` using the research template from `./data/research-template.md`.

## Execution Order

Follow these steps in order. Each step file contains the full procedure.

1. [Confirm Scope](./steps/confirm-scope.md) — Confirm technical research scope and approach with user
2. [Analyze Technology Stack](./steps/analyze-technology-stack.md) — Languages, frameworks, tools, and platforms
3. [Analyze Integration Patterns](./steps/analyze-integration-patterns.md) — APIs, protocols, and system interoperability
4. [Analyze Architecture](./steps/analyze-architecture.md) — Architectural patterns and design decisions
5. [Analyze Implementation](./steps/analyze-implementation.md) — Implementation approaches and technology adoption
6. [Synthesize Research](./steps/synthesize-research.md) — Executive summary, strategic synthesis, and final document

## Halt Conditions

- HALT if web search is unavailable — this skill explicitly requires web search and cannot produce verified technical claims without it
- HALT if the user cannot provide a technology, tool, or technical area after repeated prompting — research cannot proceed without a defined subject
- HALT if the research topic is too vague (e.g., "all software") and no meaningful scope can be agreed upon after facilitation
- HALT if web search returns no usable results for the specified technology across multiple query attempts
- HALT if the research template (`./data/research-template.md`) is unreadable

## Data Files

- [./data/research-template.md](./data/research-template.md) — Research document template for initialization

## When to Use

Use this skill when:
- The user says "create a technical research report on [topic]" or "research the technology for [area]"
- The user needs comprehensive technical research with verified citations (e.g., "React vs Vue for large-scale applications", "GraphQL vs REST API architectures", "serverless deployment options for Node.js")
- A project needs technology stack analysis, integration patterns, architectural patterns, and implementation approaches before making technical decisions
- Web search is available (this skill requires web search — aborts if unavailable)

