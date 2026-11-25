---
name: agent-md-writer
description: Guidelines and best practices for writing high-performance agent persona files (*.agent.md, CLAUDE.md). Use this when you need to create or refine a specialized agent persona.
license: MIT
---

# Agent MD Writer

<!-- markdownlint-disable MD013 MD023 MD031 MD032 -->

This skill provides a structured process and set of principles for creating effective agent personas that reduce hallucination and increase task success rates.

## WHEN TO USE

- **Specialized Persona Creation**: Designing high-performance agent personas (`*.agent.md`, `CLAUDE.md`) with a narrow, domain-specific mandate.
- **Cognitive Architecture Design**: Defining internal reasoning protocols like Socratic Depth, Adversarial Red-Teaming, and Design-by-Contract.
- **Strict Boundary Enforcement**: Establishing explicit `Always`, `Ask first`, and `Never` operational guardrails to ensure safety and alignment.
- **Workflow Standardization**: Authoring consistent boot sequences, task boards, and verification gates for autonomous agents.
- **Pruning & Optimization**: Refining existing personas to remove fluff, reduce token usage, and eliminate activation drift.

## WHEN NOT TO USE

- **Platform Syntax Reference**: Learning the technical syntax or frontmatter schema of Agent MD files — use the `agent-md` skill instead.
- **Mechanical Playbook Authoring**: Writing command-level execution steps for specific tools — use `SKILL.md` (via `agent-skill-md-writer`) instead.
- **Global Rule Definition**: Setting workspace-wide coding standards or formatting rules — use `*.instructions.md` instead.

## Common Pitfalls

- **Role Dilution**: Creating "general helper" personas that lack the specific invariants and cognitive depth needed for complex tasks.
- **Imperative Bloat**: Describing actions in abstract prose instead of providing contract-style imperatives and concrete code examples.
- **Missing Termination Logic**: Failing to define a clear "Definition of Done" and empirical verification steps for the agent to follow.

## Core Process

1. **Identify the Persona**: Determine the exact, narrow role the agent will perform (e.g., `docs-agent`, `test-agent`). Avoid "general helper" personas.
2. **Structure the Content**: Follow the `agent-md` syntax and include high-performance sections: Persona, Initialization, Cognitive Framework, Directives, Invariants, Tooling, Workflow, and Verification Gates.
3. **Prune Fluff**: Use real code snippets and contract-style imperatives instead of abstract descriptions.
4. **Preserve Quality**: When updating, always choose the better, clearer sections. If previous changes are better, leave them intact. Always pick the best format.
5. **Output**: Output the complete markdown file without conversational wrappers.

## Core Principles

- **Specialization Over Generality**: Each agent must be a specialist (e.g., technical writer, QA engineer, security analyst).
- **Scope & Constraints**: Explicitly define what is *out* of scope. Agents perform better when they know their limits.
- **Commands Early & Exact**: List executable commands with flags early in the document. Do not just list tool names.
- **Code Examples Over Explanations**: Provide concrete code snippets showing the expected style. One example is worth ten paragraphs.
- **Tech Stack Specificity**: Explicitly name technologies and versions (e.g., "React 18 with TypeScript").
- **Strict 3-Tier Boundaries**: Clearly categorize actions into "Always do", "Ask first", and "Never do". "Never commit secrets" is mandatory.

## High-Performance Persona Sections

When writing a top-tier agent persona, always include and refine these key sections:

- **Role Persona**: Defines the agent's identity, core mandate, and philosophical approach (e.g., "Elite autonomous engineering kernel").
- **Core Responsibilities**: Enumerates the primary functional domains and high-level deliverables the agent is accountable for.
- **Initialization Sequence**: Mandatory boot sequence instructions (e.g., "Execute Core_Initialization_Sequence defined in AGENTS.mmd").
- **Cognitive Framework**: Detailed internal reasoning protocols (e.g., Adversarial Self-Inquiry, Design-by-Contract Enforcement, Division of Labor).
- **Secondary Directives**: Architectural vision and long-horizon design investments (e.g., "Deep Module Architect", "Conceptual Integrity Guardian").
- **Task Invariants**: Non-negotiable operational rules (e.g., "Broken-Window Annihilation", "Two-Hats Discipline").
- **Tooling & Resource Management**: Strict rules for tool usage, context economy, and resource pruning.
- **Workflow Contract**: Phase-by-phase execution roadmap (Intent -> Execution -> Verification -> Termination).
- **Quality & Security Gates**: Non-negotiable standards for code quality, security envelopes, and testing.
- **Hardened NEVER / MUST NOT Constraints**: Absolute prohibited actions to prevent system corruption or security leaks.
- **Important Limitations**: Explicit definitions of negative scope (what the agent should not touch).
- **File Types**: Explicit whitelist of files the agent is authorized to modify.
- **Termination Invariants**: Definition of "done" (e.g., "100% of tracked #todos must be empirically verified").
- **Communication & Output Constraints**: Strict formatting for user interaction (e.g., "Zero-Scaffolding Tone", "Commit-Message Resolution Summary").
- **Checklists**:
  - **Pre-Flight Discovery**: Steps to take before acting (Assumptions validated, Blast-radius assessed).
  - **Post-Execution Assurance**: Steps to take after completion (Living docs synced, Leakage scan passed).
  - **Verification**: Final objective truth checks (Entropy eradicated, Fidelity delta validation).

## What to Avoid

- **Vague Roles**: Avoid generic personas like "helpful assistant".
- **Abstract Style Guides**: Do not describe code style; show it.
- **Missing Boundaries**: Never omit the "Never do" section.
- **Bloated Personas**: Keep the total file size under 500 KiB to avoid truncation by GitHub.
- **Manual Step Suggestions**: For agents operating in automated environments, avoid suggesting manual steps that they should perform themselves.

## Related Skills

- **agent-md**:
  Load this skill for the technical syntax reference and schema of Agent MD files.
- **agent-skill-md-writer**:
  Load this skill when writing `SKILL.md` files for Copilot skills.
- **agents-md-writer**:
  Load this skill for general `AGENTS.md` project context files.
