---
name: quick-spec
description: Create implementation-ready technical specifications through conversational discovery, code investigation, and structured documentation. USE WHEN user needs to plan a feature, create tech-spec, or prepare implementation-ready documentation. Triggers on "buat spec", "create tech spec", "plan feature", "specification", or when user describes a feature to build without clear implementation plan.
category: planning
---

# Quick Spec

## Overview

Create implementation-ready technical specifications through a 4-step conversational workflow. This skill guides you from vague requirements to a complete tech-spec with tasks, acceptance criteria, and technical context that any developer can use to implement the feature.

**The output meets the "Ready for Development" standard:**
- **Actionable**: Every task has a clear file path and specific action
- **Logical**: Tasks are ordered by dependency (lowest level first)
- **Testable**: All ACs follow Given/When/Then and cover happy path and edge cases
- **Complete**: All investigation results are inlined; no placeholders or "TBD"
- **Self-Contained**: A fresh agent can implement the feature without reading the workflow history

---

## Workflow Decision Tree

```
User wants to build a feature
        |
        v
+----------------------------------+
| Have tech-spec?                  |
+----------------------------------+
    |              |
   YES             NO
    |              |
    v              v
+---------+  +---------------------+
| Use     |  | Start quick-spec    |
| spec    |  | workflow            |
+---------+  +---------------------+
```

---

## Core Principles

### Step-File Architecture

This workflow uses **micro-file design** for disciplined execution:

- **Just-In-Time Loading**: Only the current step file is in memory - never load future step files until directed
- **Sequential Enforcement**: Sequence within step files must be completed in order, no skipping or optimization
- **State Tracking**: Progress is documented in output file frontmatter using `stepsCompleted` array
- **Append-Only Building**: Build the tech-spec by updating content as directed

### Step Processing Rules

1. **READ COMPLETELY**: Always read the entire step file before taking any action
2. **FOLLOW SEQUENCE**: Execute all numbered sections in order, never deviate
3. **WAIT FOR INPUT**: If a menu is presented, halt and wait for user selection
4. **CHECK CONTINUATION**: Only proceed to next step when user selects [c] (Continue)
5. **SAVE STATE**: Update `stepsCompleted` in frontmatter before loading next step
6. **LOAD NEXT**: When directed, load and read entire next step file, then execute

### Critical Rules (NO EXCEPTIONS)

- **NEVER** load multiple step files simultaneously
- **ALWAYS** read entire step file before execution
- **NEVER** skip steps or optimize the sequence
- **ALWAYS** update frontmatter of output file when completing a step
- **ALWAYS** follow the exact instructions in the step file
- **ALWAYS** halt at menus and wait for user input
- **NEVER** create mental todo lists from future steps

---

## The 4-Step Workflow

### Step 1: Analyze Requirement Delta

**Goal**: Define the technical requirement delta and scope through informed questioning.

**Process**:
1. **Check for Work in Progress** - Look for existing tech-spec-wip.md
2. **Greet and Ask for Initial Request** - Get user's feature description
3. **Quick Orient Scan** - Rapid codebase scan to understand landscape
4. **Ask Informed Questions** - Ask specific questions based on code findings
5. **Capture Core Understanding** - Extract title, problem, solution, scope
6. **Initialize WIP File** - Create tech-spec-wip.md with template
7. **Present Checkpoint Menu** - [a] Advanced Elicitation, [c] Continue, [p] Party Mode

**Output**: WIP file with Overview section filled

---

### Step 2: Map Technical Constraints

**Goal**: Map the problem statement to specific anchor points in the codebase.

**Process**:
1. **Load Current State** - Read WIP file from Step 1
2. **Execute Investigation Path**:
   - Build on Step 1's quick scan
   - Read and analyze relevant code files
   - Document technical context (stack, patterns, files)
   - Look for project-context.md
3. **Update WIP File** - Add technical context to frontmatter and Context for Development section
4. **Present Checkpoint Menu** - [a] Advanced Elicitation, [c] Continue, [p] Party Mode

**Output**: WIP file with technical context documented

---

### Step 3: Generate Implementation Plan

**Goal**: Create the implementation sequence that addresses the requirement delta.

**Process**:
1. **Load Current State** - Read WIP file with Overview and Context
2. **Generate Implementation Plan**:
   - Task breakdown (discrete, ordered, specific files)
   - Task format: `- [ ] Task N: Description` with File, Action, Notes
3. **Generate Acceptance Criteria**:
   - Given/When/Then format
   - Cover happy path, error handling, edge cases
4. **Complete Additional Context**:
   - Dependencies
   - Testing strategy
   - Notes (risks, limitations, future considerations)
5. **Write Complete Spec** - Update WIP file, set status to 'review'
6. **Auto-continue to Step 4**

**Output**: Complete tech-spec ready for review

---

### Step 4: Review and Finalize

**Goal**: Review the complete spec and finalize it for development.

**Process**:
1. **Load and Present Complete Spec** - Show the full tech-spec to user
2. **Handle Review Feedback**:
   - Make requested changes
   - Ensure "Ready for Development" standard is met
   - Answer questions
3. **Finalize the Spec**:
   - Update status to 'ready-for-dev'
   - Rename WIP file to tech-spec-SLUG.md
4. **Present Final Menu**:
   - [a] Advanced Elicitation
   - [r] Adversarial Review (recommended)
   - [b] Begin Development
   - [d] Done - exit workflow
   - [p] Party Mode

**Output**: Finalized tech-spec file ready for implementation

---

## Tech-Spec Template Structure

The output tech-spec follows this structure:

```markdown
---
title: 'Feature Name'
slug: 'feature-name'
created: '2026-01-15'
status: 'ready-for-dev'
stepsCompleted: [1, 2, 3, 4]
tech_stack: []
files_to_modify: []
code_patterns: []
test_patterns: []
---

# Tech-Spec: Feature Name

## Overview
### Problem Statement
### Solution
### Scope (In/Out)

## Context for Development
### Codebase Patterns
### Files to Reference
### Technical Decisions

## Implementation Plan
### Tasks
### Acceptance Criteria

## Additional Context
### Dependencies
### Testing Strategy
### Notes
```

---

## Checkpoint Menus

### Step 1-2 Menu
```
[a] Advanced Elicitation - dig deeper into requirements
[c] Continue - proceed to next step
[p] Party Mode - bring in other experts
```

### Step 4 Final Menu
```
[a] Advanced Elicitation - refine further
[r] Adversarial Review - critique of the spec (highly recommended)
[b] Begin Development - start implementing now (not recommended)
[d] Done - exit workflow
[p] Party Mode - get expert feedback before dev
```

---

## Usage Examples

### Example 1: New Feature
**User**: "I want to add user authentication to my app"

**Agent**: Uses quick-spec workflow to:
1. Ask about auth methods, user flows, existing user model
2. Investigate current codebase for auth patterns
3. Generate tasks: create AuthService, add middleware, update routes, etc.
4. Create acceptance criteria for login/logout/error cases

### Example 2: API Endpoint
**User**: "Need an endpoint to export user data as CSV"

**Agent**: Uses quick-spec workflow to:
1. Ask about data fields, filtering, permissions
2. Investigate existing API patterns, CSV libraries in use
3. Generate tasks: create endpoint, add service method, write tests
4. Create acceptance criteria for export functionality

---

## Integration with Other Workflows

The quick-spec workflow can invoke:

- **Advanced Elicitation** - For deeper requirement discovery
- **Party Mode** - For bringing in expert perspectives
- **Quick Dev** - For implementation after spec is finalized
- **Adversarial Review** - For critical review of the spec

---

## Best Practices

1. **Don't rush Step 1** - Good questions lead to better specs
2. **Investigate thoroughly in Step 2** - Understanding existing code prevents rework
3. **Be specific in Step 3** - Vague tasks create implementation confusion
4. **Get adversarial review** - Step 4's [r] option catches blind spots
5. **Use fresh context for dev** - After finalizing, start implementation in new context

---

## Output Location

Tech-specs are saved to: IMPLEMENTATION_ARTIFACTS/tech-spec-SLUG.md

Default: project-root/.ai/tech-spec-SLUG.md

---

## Resources

### references/
- `references/step-01-understand.md` - Step 1 instruction file
- `references/step-02-investigate.md` - Step 2 instruction file
- `references/step-03-generate.md` - Step 3 instruction file
- `references/step-04-review.md` - Step 4 instruction file

### assets/
- `assets/tech-spec-template.md` - Template for output tech-spec files
