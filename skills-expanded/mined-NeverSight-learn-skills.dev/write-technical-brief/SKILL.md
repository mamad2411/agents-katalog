---
name: write-technical-brief
description: |
  Write an engineering handoff document from a verified Feature Request. Covers scope boundaries,
  technical constraints, edge cases with recommended handling, open questions engineering needs
  answered, and integration points. Bridges PM spec and engineering without designing the solution.

  Trigger on: "write a technical brief", "help me hand this off to engineering", "what does eng
  need to know to build this", "create a technical handoff doc", "make this FR ready for the
  engineering team", or at the end of a feature request authoring session.
compatibility: "Requires filesystem access to project directory. Works best with Feature Request markdown docs."
version: 1.0.0
argument-hint: "[paste FR or path to FR file]"
allowed-tools: [Read, Write, Bash]
---

# Technical Brief Writer

## When to Use

Use this skill when a feature has been specced and needs to be handed to engineering in a form they can act on. It adds the most value when:

- **After an FR is written and ACs are verified** — the feature request describes the problem and the expected outcomes; the technical brief translates that into what engineering needs to start work without ambiguity
- **Before handing to engineering** — prevents the classic "this spec has gaps" discovery mid-sprint by surfacing open questions while there is still time to resolve them with the PM
- **When starting a sprint and realising the spec has gaps** — if engineering finds unanswered questions during sprint planning, use this skill to structure those gaps and route them back to the PM quickly
- **After a feature request authoring session** — run this skill at the end of a `write-feature-request` session to produce both the FR and the engineering handoff in a single workflow
- **When an existing spec needs a structured review** — use this skill to audit a spec written without a template and surface what is missing before engineering reads it

## Input Format

The skill works best with a Feature Request markdown document produced by the `write-feature-request` skill, but accepts any structured or unstructured spec. Provide one of the following:

**A Feature Request markdown file (preferred):**
```
Path: ./feature-requests/FR-0042-export-filters.md
```

**A pasted FR description:**
```
Feature: Saved Export Filters
Users need to save their filter configurations so they don't have to re-apply them
every time they export data. Filters include: date range, team, project, status.
ACs:
  - Users can name and save a filter configuration
  - Saved filters appear in a dropdown on the export screen
  - Users can delete saved filters
  - Filters are user-scoped (not shared across the team)
```

**Optionally, existing technical notes or architecture context:**
```
Current export system: server-side rendered, filters applied as query params.
No persistent filter storage exists today. Auth is session-based.
User settings currently stored in users table (PostgreSQL).
```

If architecture context is provided, it is used to make the constraints and integration points sections more concrete. If none is provided, constraints are derived from the FR alone and flagged for validation.

## How It Works

The skill follows five steps to transform a Feature Request into an engineering handoff document.

### Step 0 — Scan Project for Architecture Context (silent)

Before reading the FR, silently scan the project for context that will enrich the constraints and integration points sections:

```bash
# Architecture docs
find . -maxdepth 3 \( -name "ARCHITECTURE.md" -o -name "architecture.md" -o -name "TECH-STACK.md" \) 2>/dev/null | head -5 | xargs cat 2>/dev/null
find . -maxdepth 3 -type d \( -name "adr" -o -name "architecture" \) 2>/dev/null | head -3
# Tech stack
cat README.md 2>/dev/null | head -80
cat package.json 2>/dev/null || cat Cargo.toml 2>/dev/null || cat go.mod 2>/dev/null
```

Use any found artefacts to:
- Populate **technical constraints** with confirmed platform and framework details
- Populate **integration points** with known existing systems
- Mark constraints derived from scanned files as **Confirmed** (not Assumed)

If nothing is found, continue from Step 1 as normal. Do not mention the scan to the user.

### Step 1 — Read the FR and Identify All Requirements and ACs

The skill reads the full FR and extracts:
- The problem statement (what user need is being addressed)
- Every functional requirement (what the feature must do)
- Every Acceptance Criterion (the testable conditions for done)
- Any non-functional requirements mentioned (performance, security, accessibility)

This inventory becomes the foundation for every subsequent step. If the FR is missing a problem statement or ACs, the skill notes the gap and proceeds with what is available.

### Step 2 — Derive Scope (In and Out of This Implementation)

From the requirements inventory, the skill draws explicit scope boundaries:

- **In scope** — everything the FR and ACs commit to, stated as discrete deliverables
- **Out of scope** — related things a reader might assume are included but are not. This is the most important part of the scope section. "Out of scope" items are not a wish list for the future; they are guardrails against scope creep. Every "out of scope" item should be something a reasonable engineer might ask about.

Example: If the FR is for saved export filters, out of scope would explicitly state: *"Shared/team-level filters, filter templates, scheduled exports using saved filters, mobile export UI."*

### Step 3 — Identify Constraints

Constraints are conditions the implementation must respect, regardless of how engineering chooses to build the solution. The skill identifies constraints in four categories:

- **Technical constraints** — platform, language, framework, or infrastructure limitations (e.g. "must work within the existing server-side rendered export pipeline")
- **Compliance constraints** — legal, regulatory, or security requirements (e.g. "filter configurations must not store PII beyond what is already in the user record")
- **Dependency constraints** — external systems, services, or internal APIs that this feature depends on (e.g. "depends on the user settings service being available at write time")
- **Performance constraints** — latency, throughput, or load requirements (e.g. "filter save must complete in under 300ms at P99 to not disrupt the export flow")

Constraints derived from architecture context are marked as Confirmed. Constraints inferred from the FR alone are marked as Assumed and flagged for validation by engineering.

### Step 4 — Enumerate Edge Cases and Recommend Handling

Edge cases are scenarios the ACs do not explicitly cover but that engineering will encounter during implementation. The skill works through the requirements systematically and asks: *"What happens when...?"*

For each edge case identified, the skill provides:
- A plain-language description of the scenario
- A recommended handling approach (from a PM perspective — not a technical design)
- Whether the recommended handling is a decision the PM can make now, or an open question that needs further input

Edge cases are presented as a table (see Output Format). If the recommended handling requires a PM decision, the row is marked with Open? = Yes and the question is surfaced in the Open Questions section.

### Step 5 — Surface Open Questions

Open questions are decisions engineering needs the PM to make before they can start building. They fall into two categories:

- **Decision questions** — the PM must choose between two or more valid approaches, and the choice has product implications (not just technical ones). Example: *"Should saved filters be user-scoped or team-scoped? The FR says user-scoped, but three enterprise customers in support tickets have asked for team-level sharing."*
- **Validation questions** — something in the FR is ambiguous or missing, and engineering needs clarification before they can design a solution. Example: *"The FR says 'users can name a filter' — is there a character limit, reserved names, or uniqueness requirement?"*

Each open question is numbered, written as a direct question, and accompanied by the context that makes it important.

## Output Format

The skill saves the technical brief as `technical-brief-[feature-slug].md` in the current project directory, where `[feature-slug]` is derived from the FR title in kebab-case (e.g. `technical-brief-saved-export-filters.md`). The output follows this structure:

```markdown
# Technical Brief: [Feature Name]

**Source FR:** [filename or "Pasted input"]  
**Date:** [date]  
**Status:** Draft — pending PM sign-off on open questions

---

## Scope

### In Scope
- [Discrete deliverable 1 — one line each]
- [Discrete deliverable 2]
- [...]

### Out of Scope
- [Thing a reader might assume is included, explicitly excluded]
- [...]

---

## Constraints

| Type | Constraint | Confirmed / Assumed |
|---|---|---|
| Technical | [constraint] | Confirmed |
| Compliance | [constraint] | Assumed — validate with [team/person] |
| Dependency | [constraint] | Confirmed |
| Performance | [constraint] | Assumed — validate with [team/person] |

---

## Edge Cases

| Scenario | Recommended Handling | Open? |
|---|---|---|
| [What happens when X] | [Recommended approach from PM perspective] | No |
| [What happens when Y] | [Recommended approach — see Open Question #2] | Yes |

---

## Open Questions for PM

1. **[Short label]:** [Direct question]. Context: [Why this matters and what the impact of each option is.]
2. **[Short label]:** [Direct question]. Context: [...]

---

## Integration Points

- **[System / Service name]:** [How this feature touches it — read, write, or depends on. One sentence each.]
- [...]

---

## Out of Scope (Explicit List)

The following are explicitly excluded from this implementation. Do not design for these unless the scope is formally revised:

- [Item]
- [Item]
```

## After Producing the Brief

Once the brief is saved, surface this to the user:

> "To route this to engineering for review, `/superpowers:requesting-code-review` walks through the handoff."

## Key Rule

This document describes the problem space, not the solution. Every question of *"how should this work technically?"* becomes an open question for engineering to answer — not a decision in this document. The technical brief should never include:

- Proposed data models, schemas, or table structures
- Suggested algorithms or implementation approaches
- Technology or library recommendations
- Architecture diagrams

If a constraint implies a technical direction, state the constraint, not the direction. For example: *"Filters must persist across sessions"* is a constraint. *"Store filters in the user_preferences table"* is a solution design decision that belongs to engineering.

## Length Target

A well-scoped technical brief is 1–2 pages. If the document runs longer, one of two things is true:

1. **Scope is too broad** — the feature should be broken into smaller, independently deliverable units
2. **Too many unresolved open questions** — the FR needs more PM work before engineering handoff is appropriate

If the output exceeds 2 pages, the skill will flag this and recommend either scoping down or scheduling a PM review session to resolve the open questions before handoff.

## How to Trigger

Ask your assistant to write a technical brief by saying things like:

- "Write a technical brief for this feature request"
- "Help me hand this off to engineering"
- "What does eng need to know to build this?"
- "Create a technical handoff doc from this FR"
- "Make this feature request ready for the engineering team"
- "I've finished writing the FR — now write the technical brief"

This skill will automatically, run the five-step process, and save the result as a `technical-brief-[slug].md` file in your project directory.
