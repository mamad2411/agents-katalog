---
name: design-structure
description: Build the initial design structure from a vague or partially formed idea. Use when the task lacks a clear design tree, scope boundaries, core objects, key flows, or explicit decision points. Trigger when the user has an idea, feature request, or system goal that needs to be turned into a structured design skeleton before deeper refinement. Do not use when the design tree already exists and the main need is to deepen or validate it.
---

# Design Structure

## Overview

This skill turns a vague idea into an initial design tree through a two-phase workflow:

1. **Interactive confirmation** — progressively confirm problem, scope, and assumptions with the user
2. **Design tree generation** — produce the design tree based on confirmed inputs

All output is written to a file. The conversation stays concise: questions during confirmation, tree diagram and action items during generation.

## When to Use

Use this skill when:

- the user has an idea but not a design
- the task lacks scope, boundaries, core objects, or key flows
- there is no clear design tree yet
- the current design conversation is still at the "what are we even designing?" stage

Do not use this skill when:

- a workable design tree already exists
- the main need is deeper decomposition of existing branches
- the main need is to compare options for one explicit decision node
- the main need is to decide whether the design is ready for planning

## Language Strategy

Match the design file language to the user's instruction language.

Use this priority order:
1. An explicit output-language request from the user
2. The dominant natural language of the user's current instruction
3. The dominant natural language of the most recent user instructions in the same task
4. English if the signal is weak or ambiguous

Rules:
- Keep the chat response, interactive Q&A, and the design file in the same language
- Translate section headings into the chosen language
- Keep file paths, code identifiers, template placeholders (e.g., `{{...}}`), and literal config keys unchanged
- Do not mix languages unless the user explicitly asks for bilingual output
- Interactive Q&A in Phase 1 must also match the chosen language

Default heading examples:

If the output language is English:
- `Problem`
- `Scope`
- `Included` / `Excluded`
- `Assumptions`
- `Design Tree`
- `Open Branches`
- `Decision Nodes`
- `Decisions`
- `External Dependencies`

## Workflow

### Phase 1: Interactive Confirmation

Confirm the foundation before generating the design tree. Proceed in order:

1. **Problem** — confirm the core problem and success metrics
2. **Scope** — confirm what is included and excluded
3. **Assumptions** — confirm implicit assumptions being made

After each confirmation, immediately write the confirmed section to the design file. Do not repeat confirmed content in subsequent conversation.

Skip a section only if the user explicitly provides it upfront (e.g., "the problem is X and the scope is Y" — confirm both in one round).

### Phase 2: Design Tree Generation

Based on confirmed inputs, generate the design tree covering (when relevant):

1. Problem definition
2. Scope and boundaries
3. Core objects
4. Core flows
5. Interfaces and data
6. Decision points
7. Non-functional requirements
8. Validation and delivery

If a branch is not relevant, say so explicitly instead of silently omitting it.

Write the complete design tree to the file. In conversation, show only:
- the tree diagram
- decision nodes that need user action
- open branch names (point user to file for details)
- next step recommendation

## Interactive Q&A

### Intent-Driven Strategy

Use whatever interactive question tool is available in the current environment. Do not hardcode tool names — describe the interaction intent and constraints; the model selects the right tool based on its environment.

**Constraints (cross-CLI compatible):**
- 1–3 questions per prompt
- ≤ 4 options per question
- Structured text (question + optional choices)

**Fallback:** If no dedicated question tool is available, use natural language prompts (see format templates below).

### Question Types and Formats

#### Confirmation — state understanding, ask to verify

```
## Problem

Core problem: Build an internal API gateway for unified routing, authentication, and rate limiting.
Success metrics: P99 latency < 50ms, availability > 99.9%

↑ Is this correct? Anything to amend?
```

#### Scope — checklist with include/exclude markers

```
## Scope

My assessment:

Included ✓
- Request routing
- Authentication and authorization
- Rate limiting
- Request logging

Excluded ✗
- Service discovery
- Load balancing

↑ Any adjustments?
```

#### Decision — table with star ratings, best option first, max 4 options

```
## Pending Decision: Auth Mode

| Option | Rating | Pros | Cons |
|--------|--------|------|------|
| JWT (stateless) | ★★★ | Scales horizontally, no server state | Revocation is complex, token size |
| Session (stateful) | ★★ | Instant revocation, mature pattern | Requires shared storage, limited scaling |
| API Key | ★ | Simple to implement | Low security, not suitable for user-level auth |

↑ Which one? Or a different idea?
```

#### Supplement — direct question with relaxed prompt

```
## Supplementary Info

Expected daily request volume?

↑ Please fill in (a rough range is fine if uncertain)
```

**Rules for all types:**
- One question type per message
- End every question with `↑` marker to signal "your turn"
- After user confirms, do not repeat the confirmed content (it is already in the file)

## File Output

### Path

Write the design file to `docs/design-tree/<feature-name>.md`.

Derive `<feature-name>` from the user's request (e.g., "payment service" → `payment-service`). Create the directory if it does not exist.

### Template

```markdown
# <Feature Name> Design Tree

## Problem
[confirmed content]

## Scope
### Included
- ...
### Excluded
- ...

## Assumptions
- ...

## Design Tree
[tree diagram]

## Open Branches
- ...

## Decision Nodes
- ...

## Decisions
[filled later by decision-evaluation]
```

### Incremental Write

Write each section to the file as soon as it is confirmed or generated. Do not wait until the end. This prevents data loss if the process is interrupted.

## Design Tree Requirement

Create an initial design tree that covers, at minimum, these branches when relevant:

1. Problem definition
2. Scope and boundaries
3. Core objects
4. Core flows
5. Interfaces and data
6. Decision points
7. Non-functional requirements
8. Validation and delivery

If a branch is not relevant, say so explicitly instead of silently omitting it.

## Core Responsibilities

Your responsibilities are:

1. Clarify the real goal of the design through interactive confirmation.
2. Capture scope, non-goals, and constraints.
3. Build an initial design tree with first-level and, where useful, second-level branches.
4. Identify open branches that still need refinement.
5. Identify explicit decision nodes that should later go to `decision-evaluation`.
6. Record assumptions instead of silently relying on them.
7. Write all output to the design file incrementally.
8. Flag nodes that depend on unverified external tools, APIs, libraries, or services. Perform a lightweight feasibility check (web search or doc lookup) at the time of flagging. If the dependency is clearly infeasible, mark `✗` immediately; if confirmed feasible with open questions, mark `[RESEARCH]` with initial findings; if fully confirmed, mark `✓`.

## Expected Outputs

### File Output (complete)

The design file at `docs/design-tree/<name>.md` must contain:
- Problem — confirmed
- Scope — confirmed, with explicit non-goals
- Assumptions — confirmed
- Design Tree — tree diagram
- Open Branches — list
- Decision Nodes — list
- External Dependencies — list, each entry contains: node, dependency, validation_needed, status (unverified | verified | blocked)

### Conversation Output (concise)

- Phase 1: one question at a time (see Question Types)
- Phase 2: tree diagram + decision node summaries + open branch names + next step

You are not expected to fully close every branch.

## Diagram Conventions

Render the design tree as a character tree diagram inside a code block (no language tag).

**Format:**

```
design_tree
├── 1. Problem definition
│   ├── 1.1 Core problem
│   └── 1.2 Success metrics ✓
├── 2. Core flows [OPEN]
│   ├── 2.1 Happy path
│   └── 2.2 Error path
├── 3. Interfaces and data
│   └── 3.1 API contract [DRAFT]
├── 4. External integrations
│   └── 4.1 Payment SDK [RESEARCH]
└── 5. Decision points
    └── 5.1 Storage choice [DECISION]
```

**Character rules:**

- Branches: `├──` (middle), `└──` (last)
- Continuation: `│   ` (non-last parent), `    ` (last parent, 4 spaces)
- Numbering: `1.`, `1.1` — required at first two levels
- Max width: 78 characters

**Status markers:**

| Marker | Meaning |
|--------|---------|
| `[OPEN]` | Unresolved, needs refinement or decision |
| `[DECISION]` | Decision node with multiple real options |
| `[DRAFT]` | Tentative, may change |
| `[RESEARCH]` | Depends on an external tool, API, library, or service that has passed initial feasibility check but needs deeper validation |
| `✓` | Complete / verified |
| `✗` | Rejected / out of scope |

**When to render:** Always include a tree diagram when the design tree has 3+ branches. Omit only if the design is trivially small (1-2 branches).

## Entry and Exit Criteria

Enter when:

- there is no meaningful design tree yet
- the request is still mostly unstructured

Exit when:

- the design tree exists with enough structure for follow-on work
- the main remaining work is branch refinement or explicit decision analysis

## Handoff Rules

- Hand off to `design-refinement` when the tree exists but branches are still too shallow.
- Hand off to `decision-evaluation` when there is a concrete decision node with real options.
- Hand back to `design-orchestrator` if the design state changed enough that routing should be re-evaluated.
- Do not force the conversation into option comparison before the design tree is formed.
