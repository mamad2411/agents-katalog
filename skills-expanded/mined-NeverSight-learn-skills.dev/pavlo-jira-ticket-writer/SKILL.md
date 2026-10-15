---
name: pavlo-jira-ticket-writer
description: >
  Write structured engineering tickets for Jira, output as .md files
  ready to paste into a Jira ticket description.
  Use when creating a new ticket for a feature, task, or bug.
  Also produces a stripped-down *_forJira copy that removes implementation
  detail and internal references before pasting into Jira.
metadata:
  author: Pavlo Glushko
  version: "1.5.2"
  applies_to:
    - "docs/ticket_*.md"
    - "docs/*_forJira.md"
  triggers:
    - write ticket
    - create ticket
    - jira ticket
    - write jira
    - create jira
    - new ticket
    - new story
    - new task
    - prepare for jira
    - jira copy
    - forjira
    - paste to jira
    - strip ticket
  capabilities:
    - create new Jira ticket .md files
    - produce structured tickets with Objective, Background, Scope, Requirements, and Acceptance Criteria sections
    - include JSON metadata block with Jira field values
    - reference real codebase files and symbols in Current State sections
    - produce a stripped *_forJira.md copy ready to paste directly into Jira
---

# Skill: Jira Ticket Writer

Write engineering tickets for Jira. Output a single `.md` file the user can paste directly into a Jira ticket description.

## Output File

- Location: `docs/` directory of the repository.
- Naming convention: `<EPIC_OR_MILESTONE>_<IDENTIFIER>_ticket.md` (e.g., `M3_PR1_ticket.md`, `PROJ-42_ticket.md`).
- Ask for the file name if the user did not specify one.

---

## Ticket Structure

Every ticket **must** follow this exact structure and section order.

### 1. Agent Context Comment

An HTML comment block at the very top listing the source documents the ticket is based on:

```markdown
<!-- 
  Notes for AI agent:
  This ticket is based on the following documents:
  - docs/epic_<ID>.md — <brief description>
  - docs/<other_doc>.md — <brief description>
-->
```

Include only documents that actually exist and are relevant.

### 2. JSON Metadata Block

Immediately after the comment, a fenced JSON code block containing Jira field values:

```json
{
  "ticket": "<TICKET-KEY or TBD>",
  "epic": "<EPIC-KEY> — <Epic title>",
  "type": "Story",
  "priority": "Medium",
  "labels": ["<label1>", "<label2>"],
  "components": ["<component>"],
  "story_points": null,
  "sprint": null
}
```

- `ticket`: leave as `"TBD"` if not yet assigned; otherwise use the Jira key (e.g., `"PROJ-1201"`).
- `type`: typically `"Story"` for feature work, `"Task"` for technical debt / refactors, `"Bug"` for defects.
- `priority`: one of `"Highest"`, `"High"`, `"Medium"`, `"Low"`.
- `story_points` and `sprint`: `null` unless the user provides values.

### 3. Title

```markdown
# <PR/Task Label>: <Concise Imperative Title>
```

The title should be imperative and specific — not a noun phrase. Example: `# PR 3: Implement User Authentication & Session Management`.

```markdown
**Epic:** <EPIC-KEY> — <Epic title>
```

### 4. Objective

```markdown
## Objective
```

One short paragraph. State *what* this ticket delivers and *why* it matters in the context of the larger epic. Avoid repeating the title — add context.

### 5. Background & Motivation

```markdown
## Background & Motivation
```

Explain the current limitations this ticket resolves. Use a **markdown table** when comparing multiple modules:

| Module | Current State | Limitation |
|--------|--------------|------------|
| `ModuleName` | ⚠️ Oversimplified / ❌ Missing / ✅ Done | Specific gap |

Use icons: `✅` complete, `⚠️` oversimplified/placeholder, `❌` missing entirely.

After the table, add a short prose paragraph providing any additional context (design decisions, links to relevant docs sections, deferred items).

### 6. Scope

```markdown
## Scope

### In Scope

1. **Component Name** — one-sentence description of what is being built/changed.
...

### Out of Scope

- Explicit statement of what is *not* in this ticket and where it is deferred (e.g., "Historical calibration — M6").
```

`In Scope` uses a **numbered list** (items build on each other and the numbering correlates with Requirement IDs).
`Out of Scope` uses a **bullet list**.

End the Scope section with a horizontal rule (`---`).

### 7. Current State (Code References)

```markdown
## Current State (Code References)
```

One subsection per component that will be changed. Each subsection contains:
- **File:** `path/to/file.py`
- A bullet list describing the current behaviour, limitations, and any relevant details.
- Reference only *real* files and *real* behaviour observed in the codebase.

End with a horizontal rule (`---`).

### 8. Requirements

```markdown
## Requirements

### R<N> — <Requirement Name>

**Current:** <one-sentence summary of the status quo>

**Target:** <one-sentence summary of the desired outcome>

**Details:**
- Bullet list of implementation specifics.
- Code snippets, entity fields, method signatures, validation rules — include anything needed to implement without ambiguity.
- Notes in blockquotes for non-obvious design decisions: `> **Note:** ...`
```

Requirements must correspond 1-to-1 with the In Scope items (R1 = scope item 1, R2 = scope item 2, etc.).

End with a horizontal rule (`---`).

### 9. Acceptance Criteria

```markdown
## Acceptance Criteria

- [ ] Specific, verifiable statement.
```

Each criterion is a checkbox. Criteria must be verifiable by a reviewer — avoid vague statements like "works correctly". Include one criterion per meaningful behaviour, entity field, configuration parameter, test coverage expectation, and documentation update.

### 10. Open Questions (optional)

```markdown
## Open Questions

- **<Short label>:** <Clear statement of the unresolved question,
  including the options considered and their trade-offs.>
```

This section collects **ambiguities the agent cannot resolve on its own**
and presents them to the user for decision.

#### Workflow

1. While writing the ticket,
   the agent must **never embed ambiguity into the ticket body**.
   No hedging phrases like "either A or B",
   "should default to a value that preserves current behaviour
   (e.g., from X)", or "could be configured via X or Y".
   Requirements, Details, and Acceptance Criteria
   must contain **only definitive statements**.
2. When the agent encounters a design choice it cannot resolve,
   it adds an entry to the Open Questions section
   with a clear description of the options and trade-offs.
3. After the first draft is complete,
   the agent presents the Open Questions to the user
   and asks for decisions.
4. Once the user resolves a question,
   the agent updates the ticket body
   with the definitive answer
   and removes the question from the Open Questions section.
5. The final ticket must have **no Open Questions section** —
   all ambiguities must be resolved before the ticket is considered done.
   The only exception is when the user explicitly asks
   to keep a question open
   (e.g., "leave this for implementation time", "decide later").

---

## Step 2: Prepare for Jira Paste

**Trigger:** The user explicitly asks to prepare the ticket for Jira
(e.g., "prepare for Jira", "make the Jira copy", "forJira", "strip the ticket").
This step is never run automatically — it requires an explicit user request.

### Output File

Create a copy of the source ticket file in the same `docs/` directory.
Append `_forJira` to the base name before the `.md` extension:

```
docs/M2_PR4_ticket.md  →  docs/M2_PR4_ticket_forJira.md
```

### Transformations

Apply all of the following transformations to the copy.
The source file is **not modified**.

#### 1. Remove the agent context comment

Delete the entire `<!-- Notes for AI agent: ... -->` HTML comment block at the top of the file.

#### 2. Remove the PR title and Epic line

Delete the top-level `#` heading (e.g., `# PR 4: Implement …`)
and the `**Epic:** …` line directly beneath it.
The ticket body then starts at `## Objective`.

#### 3. Remove the Current State section

Delete the entire `## Current State (Code References)` section,
including its heading, all subsections, and the trailing `---` separator.

#### 4. Strip Details from every Requirement

In each `### R<N>` section, delete the `**Details:**` block
(the line `**Details:**` and every line that follows it
up to, but not including, the next `### R`, `---`, or end of section).
Keep the `**Current:**` and `**Target:**` lines — they provide enough
context for Jira without exposing internal code references.
Keep any `> **Note:**` blockquotes that follow `**Target:**`
and appear before `**Details:**`;
delete any blockquotes that appear inside or after the `**Details:**` block.

#### 5. Rewrite Acceptance Criteria

Rewrite the Acceptance Criteria section so that each criterion:

- Describes **what** is required, not **how** it is implemented.
- Remains specific enough for a product owner or QA engineer
  to verify the outcome.

**Code references — keep the key ones, remove the noise.**
A criterion may keep the one or two most important identifiers
(the central entity, field, or concept being introduced)
when dropping them would make the criterion too vague to verify.

Remove:
- File paths and module locations (e.g., `adapters/outbound/geo/`)
- Internal helper names, method signatures, and return-type annotations
- Implementation details that describe *how*, not *what*
  (e.g., "uses numpy internally", "returns `list[list[float]]`")
- Any reference to more than two code identifiers per criterion;
  if a criterion lists many, keep only the central one and paraphrase the rest.

Keep:
- The name of the primary concept, entity, field, or config parameter
  being introduced or changed (e.g., `` `assignment_interval` ``,
  `` `HaversineDistanceCalculator` ``)
- A single qualifier that makes the criterion unambiguous
  (e.g., `` `gt=0` `` for a validated field)

Where multiple detailed criteria covered the same high-level outcome,
merge them into one criterion.
Preserve the checkbox format (`- [ ]`).

Example transformation:

```markdown
Before (too much internal detail):
- [ ] `HaversineGeoDistanceCalculator` exists in `adapters/outbound/geo/`
  implementing `GeoDistanceCalculator`; `distance_matrix_km` and
  `travel_matrix_min` use numpy internally and return `list[list[float]]`;
  numpy is not imported anywhere in `domain/` or `application/`.

After (key reference kept, noise removed):
- [ ] `HaversineGeoDistanceCalculator` is implemented and wired
  as the default geo-distance provider.
```

#### 6. Remove the Implementation Notes section (if present)

If the ticket contains a `## Implementation Notes` section,
delete it entirely — it is an internal working document,
not Jira content.

### What to Keep

- The JSON metadata block (`\`\`\`json { ... }\`\`\``).
- The `## Objective` section, unchanged.
- The `## Background & Motivation` section, unchanged.
- The `## Scope` section, unchanged.
- The `### R<N>` headings, `**Current:**`, and `**Target:**` lines.
- Any `> **Note:**` blockquotes that appear before `**Details:**`
  in each requirement.
- The `## Acceptance Criteria` section (rewritten per rule 5 above).
- The `## Open Questions` section, if present and unresolved.

---

## Real-World Example

See `examples/E1_PR2_ticket.md` for a reference ticket.
Read it before generating a new ticket to match the style, detail level, and structure.

---

## Writing Guidelines

- **Tone:** Technical, precise, and direct. Write for a senior engineer who will implement the ticket without further clarification.
- **Specificity:** Always reference exact file paths, class names, method signatures, and entity field names. Never write "update the service" — write "update `UserService.authenticate()` in `src/services/user_service.py`".
- **Current State first:** Every requirement must describe the current state before describing the target. This prevents misunderstandings about what actually needs to change.
- **Scope boundaries:** Be explicit about what is deferred and to which milestone/PR. This prevents scope creep.
- **Backward compatibility:** Explicitly state whether changes must preserve backward compatibility for CLI / dashboard / pipeline entry points.
- **Defaults:** Every new configuration parameter must have a default value that preserves existing behaviour.
- **No local file links:** Never use Markdown links to local files (e.g., `[see § 3](design_doc.md#section)`).
  They break when the ticket is pasted into Jira.
  Reference local documents as plain text or inline code instead:
  `docs/design_doc.md § 3` or simply `design_doc.md`.
- **Privacy:** Do not expose personal workflow rules (from `copilot-instructions.md` or `AGENTS.md`) in the ticket output.
