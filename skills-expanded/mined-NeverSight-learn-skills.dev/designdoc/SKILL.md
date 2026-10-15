---
name: designdoc
description: Write a design document following Google's design doc practices. Guides through structured sections interactively to produce a comprehensive design doc.
argument-hint: "[system or feature name] [--lang=en|ja]"
allowed-tools: Read, Glob, Grep, Write, Edit, Bash(ls *), Bash(cat *), WebSearch, AskUserQuestion
---

# designdoc

Write a design document by guiding the user through structured sections, following practices described in [Design Docs at Google](https://www.industrialempathy.com/posts/design-docs-at-google/).

## When to use

- When the user wants to write a design document for a new system, feature, or significant change
- When the user wants to document architectural decisions and trade-offs
- When the user runs `/designdoc`

## Instructions

Guide the user through writing a design document section by section. At each section, ask relevant questions, wait for answers, then draft that section before moving to the next.

### Language Selection

- If `--lang=en` or `--lang=ja` is specified, use that language throughout.
- If not specified, detect the user's language from their input and use it.
- The design doc itself should be written in the selected language.

### Determine Scope

First, determine the scope of the design doc:

- **Full design doc** (10-20 pages): For new systems, major features, or significant architectural changes
- **Mini design doc** (1-3 pages): For incremental improvements, small features, or focused subtask decisions

Ask the user which scope is appropriate, or infer from context.

---

### Section 1: Title and Metadata

Generate the metadata block:

- **Title**: Descriptive name of the design
- **Authors**: Ask the user
- **Status**: Draft / In Review / Approved / Implemented / Deprecated
- **Created**: Today's date
- **Last Updated**: Today's date
- **Reviewers**: Ask the user (optional at draft stage)

---

### Section 2: Context and Scope

Ask the user:

- What is the system or feature you are designing?
- What is the current state? (existing system, greenfield, etc.)
- What is the broader context this design fits into?
- Are there related systems or prior designs the reader should know about?

Draft an objective overview of the landscape. Keep it concise — assume the reader has general domain knowledge. Focus on facts, not opinions.

---

### Section 3: Goals and Non-Goals

Ask the user:

- What are the primary goals of this design? What problems does it solve?
- What are explicit non-goals? (things that could reasonably be goals but are intentionally excluded)

**Important**: Non-goals are NOT negated goals (e.g., "not be slow" is a bad non-goal). They should be things that a reasonable reader might expect to be in scope but are explicitly excluded (e.g., "Supporting multi-region deployment" when designing a single-region service).

---

### Section 4: The Actual Design

This is the core section. Guide the user through:

#### 4.1 Overview

- Ask for a high-level summary of the proposed solution
- What is the key insight or approach?

#### 4.2 System-Context Diagram

- Help create a diagram (Mermaid format) showing how the new system fits into the broader technical environment
- Show key interactions with external systems, users, and data flows

#### 4.3 APIs

- What APIs will the system expose or consume?
- Sketch key API shapes — avoid overly formal definitions
- Focus on design trade-offs in API decisions

#### 4.4 Data Storage

- What data needs to be stored?
- What storage technology and format will be used?
- What are the trade-offs in the storage design?

#### 4.5 Code and Pseudo-Code (if applicable)

- Only include if there are novel algorithms or non-obvious logic
- Link to prototypes if they exist

#### 4.6 Degree of Constraint

- How constrained is this design? Are there hard requirements that shaped it?
- What flexibility exists for future changes?

For **mini design docs**, sections 4.3-4.6 can be abbreviated or omitted as appropriate.

---

### Section 5: Alternatives Considered

Ask the user:

- What other approaches were considered?
- Why were they rejected?
- What trade-offs led to choosing the proposed design over alternatives?

This section is critical — it shows that the design space was explored and helps reviewers understand the rationale.

---

### Section 6: Cross-Cutting Concerns

Address each of the following, asking the user about relevance:

- **Security**: Authentication, authorization, data protection, threat model
- **Privacy**: PII handling, data retention, compliance (GDPR, etc.)
- **Observability**: Logging, monitoring, alerting, tracing
- **Reliability**: Failure modes, recovery, SLOs/SLAs
- **Scalability**: Expected load, growth projections, bottlenecks
- **Accessibility**: If applicable (UI/UX designs)
- **Internationalization**: If applicable

Skip concerns that are clearly not relevant to the design.

---

### Section 7: Open Questions (optional)

- Are there unresolved decisions?
- What needs further investigation or input from specific people?

---

## Output

After completing all sections, produce a final design document as a Markdown file containing:

1. Title and Metadata
2. Context and Scope
3. Goals and Non-Goals
4. The Actual Design (with subsections)
5. Alternatives Considered
6. Cross-Cutting Concerns
7. Open Questions (if any)

Suggest the filename as `design-doc-<short-name>.md` and ask the user for confirmation before writing.

## Important notes

- Always wait for user responses at each section before proceeding — do NOT skip ahead or assume answers.
- Focus on **trade-offs and rationale** throughout. A design doc is not a specification — it explains *why* decisions were made.
- If source code exists in the working directory that is relevant to the design, read it proactively to inform the discussion.
- Keep the document concise and scannable. Use bullet points, diagrams, and tables over prose when possible.
- Emphasize that a design doc is a living document — it should be updated as the design evolves during implementation.
