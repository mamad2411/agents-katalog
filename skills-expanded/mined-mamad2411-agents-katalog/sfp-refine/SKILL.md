---
name: sfp-refine
description: >
  Walk through audit findings one at a time with the project owner, resolve
  each issue incrementally, then recompile the specification from updated
  notes after owner approval.
---

# Spec Refine

## Purpose

You are operating as the **refinement capability** of the Spec-First
Protocol. Your objective is to take a set of audit findings and walk the
project owner through them **one at a time**, driving each to resolution
through focused dialogue. Once all critical findings are resolved, you
compile the updated Discovery Notes into a revised specification with the
owner's approval.

You are not exploring from scratch. The discovery phase has already
established the scope. You are resolving known issues surgically.

## Inputs

- **Audit Report**: The structured findings from the audit skill, located at
  `.sfp/YYYY-MM-DD_<SLUG>/audit_report.md`, classified by severity.
- **Specification file**: A draft specification inside the spec-specific subdirectory, named
  using the `.sfp/YYYY-MM-DD_<SLUG>/YYYY-MM-DD_<SLUG>_SPEC_DRAFT.md` convention
  (explicitly ignore the `.sfp/_archive/` directory). If multiple draft
  specifications exist, ask the project owner which one to refine.
- **Discovery Notes**: The existing validated requirements from prior
  discovery or refinement cycles, located at
  `.sfp/YYYY-MM-DD_<SLUG>/discovery_notes.md`.
- **Persona Context**: Read `.sfp/YYYY-MM-DD_<SLUG>/status.md`. If the `persona` field is present, load the
  corresponding Persona file (`<slug>.md`) by checking the following directories and resolving conflicts by
  loading the first match in priority order:
  1. **Project-Local**: `.sfp/personas/<slug>.md`
  2. **User-Global**: `~/.sfp/personas/<slug>.md` (resolving using the home folder path:
     `%USERPROFILE%\.sfp\personas\<slug>.md` on Windows, `$HOME/.sfp/personas/<slug>.md` on macOS/Linux)
  3. **Pre-packaged Fallback**: The colocated `../sfp-personas/<slug>.md` directory
  If the file is missing across all directories or malformed, halt execution and report the error to the user
  immediately.

## Incremental Review Loop

If the Audit Report contains no findings, inform the project owner that no
refinement is needed and suggest proceeding to finalization via the audit
skill.

Otherwise, walk through findings individually rather than presenting them all
at once:

### Step 1: Prioritize Findings

Load the Audit Report and sort findings by severity:

1. **Blockers** first (contradictions, critical gaps, constraint violations)
2. **Warnings** second (edge cases, incomplete sections, ambiguities)
3. **Suggestions** last (improvements, best practices)

### Step 2: Present One Finding at a Time

Findings may be **batched together** if they reference the **same specification
section** or arise from the **same underlying requirement** in the Discovery
Notes. Thematic batching is not permitted. Present related findings as a group,
explain the shared context once, and ask the owner to resolve each finding in
the batch. Unrelated findings must be presented separately.

#### Interactive Triage for Suggestions

After all **Blockers** and **Warnings** have been resolved through the
standard interactive review (individually or in same-section batches),
present the remaining **Suggestions** as a numbered summary list. For each
Suggestion, the owner provides a simple **accept** or **decline** decision.

Suggestions are eligible for this streamlined review because they are
non-blocking improvements that do not require the owner to choose between
resolution options or provide additional detail. If a Suggestion does require
a design choice (e.g., choosing between two structural approaches), it must
be presented individually using the standard interactive format below.

Blockers and Warnings are never eligible for streamlined review. They always
require the full interactive process with resolution options.

For each finding (or batch):

1. **State the finding** clearly and concisely, referencing its ID (e.g., "Blocker B-1", "Warning W-2") and severity.
2. **Reference the relevant spec section** in brackets (e.g., `[Section 3. Workflows]`) so the owner has context.
3. **Explain why it matters**: in a single, direct sentence, describe what breaks, what is ambiguous, or what risk it
   introduces.
4. **Propose resolution options**: Propose logical and realistic resolution options using a clean, bulleted list.
   Each option must start on a new line, prefixed with a bold option identifier (e.g., `- **Option A**: description`).
   Options should be concrete, actionable, and separated by a blank line for readability. When the finding is too
   ambiguous to propose options, present the issue and ask a single, direct question.
5. **Ask the owner for a resolution decision.** Keep this prompt to a single concise sentence.

Wait for the owner's response before moving to the next finding or batch. Do
not batch multiple unrelated findings into a single turn.

### Step 3: Record Decisions

After each resolution, immediately update
`.sfp/YYYY-MM-DD_<SLUG>/discovery_notes.md` with the new decision. Tag each
new or revised entry with its refinement cycle and the finding ID it resolves,
using the format `[Refined in cycle <N>, resolves <FINDING-ID>]` (e.g.,
`[Refined in cycle 2, resolves W-3]`). Read the current `iteration` value
from `status.md` to determine the cycle number. This tag enables future
audits and refinements to distinguish historical decisions from current ones.

When updating an existing requirement, preserve its original `REQ-<NN>`
identifier. Do not reassign or remove identifiers. If a requirement is
split into multiple sub-requirements, assign new `REQ-<NN>` identifiers
to each sub-requirement and note the parent in the tag (e.g.,
`[Refined in cycle 2, resolves W-3, split from REQ-05]`).

### Step 4: Repeat

Continue through all blockers, then warnings. For suggestions, present them
for the owner's consideration but do not block on them. Record whether the
owner accepts, rejects, or defers each suggestion.

When suggestions are resolved via the streamlined batch review, record
each accepted suggestion individually in the Discovery Notes with its own
refinement tag. Do not combine multiple accepted suggestions into a single
entry.

## Scope Expansion

After all findings have been addressed, ask the project owner whether they
want to add any new requirements or expand the specification's scope.

- **If the owner has additions**:
  1. **Record each addition** in the Discovery Notes, clearly marked as new
     scope from this refinement cycle.
  2. **Ask targeted clarifying questions** as needed to fully specify each
     addition, following the same style as the discovery skill's interview.
  3. **Do not re-open resolved findings.** Scope expansion is additive; it does
     not revisit prior decisions.
  4. Once additions are clarified, proceed to the Compilation Gate.
- **If the owner has no additions and indicates readiness to proceed/compile**:
  Proceed directly to compilation. Present the summary of all decisions and
  recompile the specification in the same turn without asking for confirmation
  a second time.

## Compilation Gate

When all findings are resolved, scope expansion is complete (if any), and
warnings have been addressed (resolved or explicitly accepted as-is by the
project owner):

1. **Present a summary of all decisions** made during this refinement cycle,
   organized by finding.
2. **Determine if confirmation is needed**:
   - If the project owner already gave clear consent to compile/proceed
     (e.g., by stating they have no scope additions and want to proceed, or
     by confirming after scope additions are finalized), proceed directly to
     recompilation.
   - Otherwise, ask: "Ready to recompile the specification with these changes?"
3. **If proceeding (or approved)**: recompile the specification from the
   updated Discovery Notes following the process described below.
4. **If declined**: allow the owner to revisit specific decisions before
   presenting the summary again.

## Compilation Process

After the owner approves recompilation:

1. Load the specification schema from the
   [specification schema](#specification-schema-template) below as your
   starting scaffold.
2. Read the updated Discovery Notes from
   `.sfp/YYYY-MM-DD_<SLUG>/discovery_notes.md` and the conversation context.
3. Extract resolved constraints, entities, workflows, rules, and open
   questions.
4. Map each extracted element to the appropriate section of the schema.
5. Adapt the schema to the domain:
   - If a Persona was loaded, integrate any custom sections and schema structural
     modifications specified in the Persona file.
   - Add sections that the domain requires.
   - Omit sections that do not apply.
   - Rename section headings to use the project owner's terminology where it
     improves clarity.
6. Output the complete, updated specification file to the spec-specific
   subdirectory `.sfp/YYYY-MM-DD_<SLUG>/`, updating the existing
   `YYYY-MM-DD_<SLUG>_SPEC_DRAFT.md` file rather than creating a new one.

### Compilation Guardrails

- **No hallucinations.** You must not invent requirements, technologies,
  constraints, or features that were not explicitly stated or approved in the
  Discovery Notes or conversation. If the inputs are silent on a topic, omit
  the corresponding section entirely.
- **Zero Placeholder Invariant.** Never use `TODO`, `FIXME`, `TBD`, or
  language like "to be determined." If a section cannot be populated from the
  inputs, it must be omitted instead of stubbed.
- **Context Preservation.** Do not alter sections of the specification that
  are already locked unless the incoming inputs explicitly note an override
  or revision of that requirement.
- **Structural Invariance.** Always output the full, updated document. The
  spec must be self-contained and readable without reference to the
  conversation history.

## Resolution Guardrails

- **No solutions.** You must not design fixes, write specification sections,
  or propose implementations. You clarify the project owner's intent and
  record their decisions. Compilation happens only after the owner approves.
- **Stay focused.** Do not re-explore settled scope beyond the explicit
  scope expansion step. If the project owner raises something that requires
  deep exploration, flag it and suggest starting a new **discover** session
  for a separate specification.
- **Contradiction Blocker.** If a resolution contradicts a previously
  locked requirement, flag the conflict immediately and demand explicit
  resolution before proceeding.
- **Audit traceability.** Reference specific audit findings (e.g., "Blocker
  B-1", "Warning W-2") when discussing issues so that the conversation
  remains traceable to the Audit Report.
- **Progress Acknowledgment.** After the owner resolves a finding, briefly acknowledge
  the decision before presenting the next finding or batch. Keep acknowledgments to a
  single concise sentence. Do not restate the owner's full response.
- **Elaboration Prompting.** If the owner provides a resolution that is too brief or
  vague to update the Discovery Notes with a clear decision, ask for elaboration.
  Frame the follow-up around what is needed for a concrete update. Accept the owner's
  response if they decline to elaborate further.
- **Tone & Style**: Adopt the tone and style defined in the Persona. If no Persona is loaded,
  default to a neutral, professional, and highly succinct tone. Focus on brevity: avoid conversational
  pleasantries, verbose introductions, or repetitive summaries. Keep paragraphs as brief as needed to convey
  the information.
- **Output Succinctness & UX**: Minimize conversational filler. Proceed directly to the brief acknowledgment,
  followed by the next finding and its resolution options. Ensure all options or choices are formatted as separate
  bullet points with bold prefixes (e.g., `- **Option A**: description`), leaving blank lines between items for
  a clean visual presentation.
- **Anti-Patterns**: Strictly adhere to any anti-patterns or exclusions defined in the Persona.
- **Knowledge Context**: Use the provided glossary or context to understand domain terminology
  without asking the user for basic definitions.
- **Operational Mode Override.** This skill's workflow governs the session.
  Do not defer to external planning modes, implementation pipelines, or
  other agent operational behaviors that would bypass or substitute this
  skill's defined phases and resolution structure.

## Output

Your outputs are:

1. **Updated Discovery Notes** at
   `.sfp/YYYY-MM-DD_<SLUG>/discovery_notes.md`, including all new decisions
   and scope additions made during refinement, organized by topic and clearly
   marked as new or revised.
2. **Updated Specification File** in the spec-specific subdirectory `.sfp/YYYY-MM-DD_<SLUG>/`
   (retaining the `_SPEC_DRAFT.md` suffix), recompiled from the updated Discovery
   Notes after owner approval.
3. **Updated Status File** at `.sfp/YYYY-MM-DD_<SLUG>/status.md`: set `phase`
   to `refine` and update `last_updated` to the current ISO-8601 timestamp.
   If `status.md` does not exist, create it with `iteration: 1` and
   `max_iterations: 5`.

## Suggested Next Skill

After recompiling the specification, suggest:

> **Next step -> Spec Audit**: Re-audit the updated specification to verify
> that all findings have been resolved and no new issues were introduced.
>
> Consider clearing your current context and starting a fresh session for the
> audit skill, providing the specification file and
> `.sfp/YYYY-MM-DD_<SLUG>/discovery_notes.md` as input.

## Specification Schema Template

```markdown
# Project Name Specification

> This schema is a starting scaffold. Adapt it to the domain: add sections
> that apply, omit sections that do not, and rename headings to match the
> project owner's terminology. Every section that appears must be fully
> populated from validated Discovery Notes without placeholders or stubs.

## 1. Overview

The purpose of this specification, its intended audience, primary
stakeholders, and high-level scope.

## 2. Constraints and Rules

Business rules, invariants, guardrails, validation logic, and
non-negotiable requirements. Define what must always be true.

## 3. Domain Model

Core entities, their attributes, relationships, and lifecycle states.
Define the vocabulary of the domain, including the nouns and their connections.

## 4. Workflows and Processes

Sequences, state machines, decision logic, and procedural steps. Define
how entities move through the system or process (the verbs).

## 5. Interfaces and Contracts

Integration points, handoff protocols, input/output schemas, or API
contracts. Define how components or parties interact with each other.

> Omit this section if the specification does not involve integrations or
> programmatic interfaces.

## 6. Non-Functional Requirements

Performance targets, scalability constraints, compliance requirements,
availability expectations, and observability needs.

> Omit this section if non-functional requirements are not applicable or
> have not been discussed.

## 7. Failure Modes and Edge Cases

Known failure scenarios, expected behavior for each, fallback mechanisms,
and recovery strategies. Define what happens when things go wrong.

## 8. Deliverables

What the downstream process will produce from this specification. A single
artifact or multiple outputs; enumerate each with its purpose and format.

## 9. Open Questions

Items surfaced during discovery that remain unresolved. Each entry should
include the question, its origin, and its blocking impact.
```
