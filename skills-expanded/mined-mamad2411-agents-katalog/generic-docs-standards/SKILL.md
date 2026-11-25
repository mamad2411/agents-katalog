---
name: generic-docs-standards
description: Apply when writing or editing files under docs/{requirements,bdd,design,research}. Defines placement heuristic, writing order, status labels, and metadata conventions.
metadata:
  stack: [generic]
---

# Documentation standards

Project documentation is split into four intent-scoped directories. Each has its own audience and writing style.

| Directory | Intent | Writing style | Audience |
|---|---|---|---|
| `docs/requirements/` | WHAT and WHY | Plain-language rule list with stable FR-/NFR- IDs | Product, delivery, auditors, non-developer IT |
| `docs/bdd/` | HOW users experience it | Representative Gherkin scenarios — not exhaustive | QA, delivery, stakeholders |
| `docs/design/` | HOW the system is shaped (current state) | High-level architectural decisions, requirement-mirrored where business-driven. No code mirroring, no changelog. | Engineering, reviewers |
| `docs/research/` | Evidence feeding the other three | Raw exploration, vendor comparisons | Any |

## Placement heuristic

When a sentence could plausibly live in more than one place:

- Explains **what the system must do or satisfy** → requirements.
- Explains **how the system is shaped** or **why this shape** → design, under the requirement it serves.
- Describes **what a user observes** → BDD.

## Writing order

Requirements first. Then BDD. Then design. Edge cases that affect observable behaviour land in BDD if they're worth a scenario, otherwise in the design doc under the requirement they refine. Every BDD scenario and every `§Response per requirement` design entry is tagged with its governing requirement ID (e.g. `[FR-IDV-013]`). Tech-driven design sections (Context, Architecture, State machines, Sequence diagrams) need not carry an ID — see `generic-spec-authoring` Rule 4.

## Status labels

Use these words, not emoji: `Done`, `In Progress`, `TBD`, `Pending`, `Blocked`.

## File conventions

- H1 = title.
- No `Last Updated:` footers, no "owner/date/status" header blocks, no per-file changelogs. Git history and PR descriptions are the audit trail; the doc is the current-state snapshot. Status labels (above) belong inline on the requirement, scenario, or section they qualify, not as page-level metadata.
- Code blocks tagged with language.
- Be specific where it helps the reader — file paths and line numbers in research and vendor docs, FR/NFR IDs in requirements and BDD. Design docs avoid file paths and class/method names; see `generic-spec-authoring` Rule 3.

## Anti-patterns

- Putting design narrative ("we chose X because Y") in code comments — that belongs in design docs.
- Duplicating BDD scenarios in requirements (or vice versa). Tag scenarios to requirement IDs instead.
- Writing exhaustive BDDs — pick representative scenarios. Edge cases go to design.
- Leaving `TBC` headers in requirements and treating them as authoritative — `TBC` sections are ignored by gates.
- Putting changelog or "resolved on X date" entries in design docs. Design = current state; the audit trail is git history and PR descriptions.
- Mirroring code in design docs — class names, method signatures, configuration keys, column-mapping tables. If renaming a class forces a design-doc edit, the doc was wrong.
