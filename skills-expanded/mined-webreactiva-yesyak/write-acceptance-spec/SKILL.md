---
name: write-acceptance-spec
description: Writes or refines a feature spec in docs/SLUG-spec.md with a plain-language TL;DR, architecture, business rules, accepted risks, numbered Given/When/Then acceptance criteria, a testing map and an out-of-scope section. Use it whenever the user asks for a spec, a PRD, requirements, acceptance criteria, Given/When/Then, or to turn interview decisions into a document; also use it to apply review findings to an existing spec, to resolve ambiguities, or to add a TL;DR and diagrams to it.
---

# Write acceptance spec

## Inputs

- The decisions from `on-the-spot` (`.scratchpad/<slug>/interview-decisions.md`) or from the conversation.
- The terms from `domain-language` (`.scratchpad/<slug>/domain-language.md`), if it ran. Use only those terms.
- The current code, so the spec names real files, routes and tables.
- The existing decision records of the code the feature touches. A new rule must not contradict an accepted ADR without a new one that supersedes it.
- The feature slug from the branch (`git-commit-organizer`).

## Output

`docs/<slug>-spec.md`, in the document language of `simplified-technical-language`. Commit it with `git-commit-organizer`.

## Template

```markdown
# <Feature> Spec

## TL;DR                      plain-language summary (plain-visual-docs)

| | |
| --- | --- |
| Status | Draft / Approved / Implemented |
| Branch | `<branch>` |
| Date | YYYY-MM-DD |
| Revision | n - what changed |

## Summary
## Goals
## Domain language         (term table and state diagram from domain-language)
## Architecture
### Code layout            (ASCII tree with + and ~)
### Stack additions
### Scripts
### Environment variables  (name, default, notes)
### Interface              (routes, commands or public API; table and ASCII tree)
## Data model              (SQL or schema, erDiagram)
## Business rules          (one subsection per area, with diagrams)
## Accepted risks          (known risks that the user accepted, with the reason)
## Acceptance criteria
## Testing                 (layer → criteria table)
## Documentation           (docs to update)
## Out of scope
```

Leave out the sections that do not apply.

## Acceptance criteria

- Number them `AC-01`, `AC-02`… and group them by area with `###` headings.
- Use this exact shape:

  ```markdown
  **AC-15 Order cancelled before shipping**
  - **Given** an order `1042` in state `paid`
  - **When** its customer cancels it
  - **Then** the answer is `200`, the order is in state `cancelled`, and a refund for the full amount is created
  ```
- One observable behavior per criterion. Include status codes, messages and data changes that a test can check.
- Cover the unhappy paths: invalid input, missing or expired credentials when the feature has them, missing permission, limits, unknown ids.
- Every criterion must map to a test layer in the Testing section, or be marked as manual with a reason.
- When a rule defines how a value is computed, add one criterion that every place that shows the value or something taken from it uses the same rule: for example the order total in the list, in the detail, in a badge color and in the export.
- If the feature reads data, every odd case seen in it (empty, duplicated, out of range, mixed units) becomes a business rule or a line in Out of scope.

## Accepted risks

For every operation the feature touches that deletes or overwrites data, say what it now removes and whether the person who runs it is warned. Check every accepted risk with a command before you accept it (for example, build and start the app when the risk is about the build output). Write the command and its result next to the risk. A risk that nobody ran is an assumption, not an accepted risk.

## Out of scope

List everything that was discussed and left out, plus close neighbors a reader might expect. It protects the plan from scope creep.

## Modes

### Create
Write the full spec from the decisions. List every detail you decided alone at the end of your chat message, so the user can confirm them.

### Refine
Apply review findings (for example from `red-team-review` with a devil's advocate mission) or answers to ambiguities:

- Change the rules, criteria, risks and out-of-scope list together.
- If criteria are added or removed, renumber them in order and update every reference (Testing table, plan, diagrams).
- Increase the Revision number and say what changed.

### Visualize
Add the TL;DR and diagrams with `plain-visual-docs`. This mode can go to a subagent. Tell it to change only the TL;DR and diagrams, to report every ambiguity it finds while drawing, and to validate each Mermaid block. Review its diff before you commit.

## Finish

Before you report, count the lines of the spec and estimate the lines of code and tests the change needs. If the spec is longer, keep only what a reviewer needs to check the change: the TL;DR, the interface, the acceptance criteria and what is out of scope. Remove the other sections, and every line that repeats the decisions, the code or another document (`no-slop-code`). Count again. If the spec is still longer, say in one line which part must stay and why.

Report in the chat: the path, both line counts, the number of criteria, the main sections, and the defaults that need confirmation. Ask before moving to the plan.
