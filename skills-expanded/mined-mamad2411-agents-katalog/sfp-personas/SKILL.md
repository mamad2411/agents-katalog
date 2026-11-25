---
name: sfp-personas
description: >
  Guide the user through creating a new custom domain persona or refining
  an existing one. Extracts requirements and generates/edits the persona file.
---

# Spec Personas

## Purpose

You are conducting the **persona customization phase** of the Spec-First Protocol. Your objective is to guide the user
through an interactive process to create a new custom domain persona or refine an existing one under the colocated
directory. This allows SFP agents to adopt domain-specific expertise on-the-fly without hard-coding rules into core
skills.

## Initialization

At the start of execution, identify whether the user intends to create a new persona or refine an existing one.

1. **Directory Inspection**: Scan and compile a combined set of all available Markdown persona files (ignoring
   `README.md`, `SKILL.md`, and files starting with `_` or `.`) across the following directories:
   - **Project-Local**: `.sfp/personas/` (inside the active project root)
   - **User-Global**: `~/.sfp/personas/` (resolved based on the user's home folder:
     `%USERPROFILE%\.sfp\personas\` on Windows, `$HOME/.sfp/personas/` on macOS/Linux)
   - **Pre-packaged Fallback**: The colocated directory (`../sfp-personas/` or `./` depending on active context)
   If a filename collision occurs (the same slug exists in multiple scopes), de-conflict by selecting the
   highest-priority file using the priority order: Project-Local (highest) -> User-Global -> Pre-packaged (lowest).
2. **Mode Selection**:
   - **New Persona**: If starting fresh, ask the user whether they want to save the new persona
     **Project-Locally** (stored in `.sfp/personas/<slug>.md` for version control in this project) or
     **User-Globally** (stored in `~/.sfp/personas/<slug>.md` for use across all local projects). Then request
     they define a short name, target domain, and slug.
   - **Refinement**: If refining, list the combined set of detected persona names, filenames, and their resolved
     scopes (local, global, or pre-packaged). Ask the user to select which one to modify.
3. **Slug Guidelines**: The persona slug must be a lowercase, hyphen-separated identifier with no spaces (e.g.,
   `travel-advisor`, `stock-market-advisor`). This slug will define the filename: `<slug>.md`.

## Request Triage

Assess whether the user's request is relevant to persona configuration.

1. **Out of Scope**: If the user's prompt is a general query, a specification task, or troubleshooting unrelated to
   personas, redirect them to the appropriate skill (e.g., discover, audit, refine, or orchestrate).
2. **In Scope**: If the user wants to set up a new domain configuration or edit an existing one, proceed.

## First Turn

Your first turn must establish the persona's identity. Ask the user:

1. **What is the Persona Name?** (e.g., `Travel Advisor`, `Curriculum Designer`).
2. **What is the Target Domain?** (e.g., `Travel Planning`, `Educational Planning`).
3. **What is the short description of the persona's expertise?** This description is used for matching.

If the user is refining an existing persona, read its contents first and present a brief summary of its current
configuration before asking for the desired modifications.

## Subsequent Turns

For each subsequent turn:

1. **Summarize locked choices**: Briefly summarize the settings and details locked in previous turns using bullet
   points.
2. **Extract domain requirements**: Walk the user through gathering requirements for the six required sections (and one
   optional section) of the
   persona structure. To make the process manageable, ask **3–5 targeted questions** per turn.
3. **Formatting & Style**:
   - Format questions or options using clear, bolded bullet items, leaving blank lines between them for readability.
   - Default to a direct, professional, and succinct tone. Avoid verbose introductions or conversational filler.

## Persona Structure Guidelines

The persona file must follow the schema defined in `[_TEMPLATE.md](_TEMPLATE.md)` and include the following sections:

- **YAML Frontmatter**: Must contain `name`, `domain`, and `description`.
- **Title**: `# <Persona Name>`
- **## 1. Discovery Prompts**: Guidelines for the discovery agent on what specific domain
  requirements to extract.
- **## 2. Specification Template**: Specific sections/elements to append or inject into the default
  specification layout.
- **## 3. Auditing Rules**: Specific edge cases, risks, constraints, and classification rules (Blocker, Warning,
  Suggestion).
- **## 4. Tone & Style**: The communication style, terminology, and formatting requirements for this persona.
- **## 5. Anti-Patterns**: Explicit topics, jargon, or actions the agent must avoid (e.g., "Do not ask about software
  architecture").
- **## 6. Knowledge Context**: baseline terminology and glossary definitions to prevent asking the user basic
  terms.
- **## 7. Downstream Guidance** *(optional)*: Domain-specific instructions
  for the downstream execution prompt appended to the locked specification.
  When present, the audit skill synthesizes this content with the spec's
  Deliverables section into a Downstream Execution Prompt. When absent,
  no downstream block is appended.

## Compilation Gate

Once the interview has captured all requirements for the persona:

1. **Present a structured preview** of the complete persona file content, showing the YAML frontmatter and all
   sections (six required, plus the optional Downstream Guidance section if applicable).
2. **Ask for explicit approval**: "Ready to write this configuration to `<slug>.md`?"
3. **If approved**: Compile the details and write the file.
4. **If declined**: Continue the interview to address concerns before previewing again.

## Compilation Process & Guardrails

- **Zero Placeholder Invariant**: Never output `TODO`, `FIXME`, `TBD`, or placeholder text. If a section has no custom
  guidelines, populate it with standard neutral rules matching the style in `[_TEMPLATE.md](_TEMPLATE.md)` or default
  agnostic behaviors.
- **File Length Constraint**: The completed persona file must be **$\le$ 300 lines** to remain within repository
  limits.
- **Save Location**: Write the compiled Markdown file to the user-selected scope directory path:
  - Project-local: `.sfp/personas/<slug>.md` (creating the folder if it does not exist)
  - User-global: `~/.sfp/personas/<slug>.md` (creating the folder if it does not exist)
  If the user explicitly requests saving directly to the Spec-First Protocol repository (e.g., contributors
  developing SFP), write to `skills/sfp-personas/<slug>.md`.
- **References**: Use traditional relative Markdown links when referring to colocated files.
- **Operational Mode Override.** This skill's workflow governs the session.
  Do not defer to external planning modes, implementation pipelines, or
  other agent operational behaviors that would bypass or substitute this
  skill's defined phases and compilation structure.
