---
name: adding-roadmap-item
description: >-
  Use when the user wants to add a roadmap item, submit a roadmap request,
  propose a product roadmap candidate, or log RO-team roadmap intake in Linear.
  Not for generic Linear issue creation, bug reports, or implementation tickets.
version: 3.2.0
disable-model-invocation: true
---

# Adding Roadmap Items

## Overview

Add a product roadmap item to Linear's Roadmap team (`RO`) with no Linear project. This skill is a Linear workflow, not a form-template generator: resolve live Roadmap metadata, attach the correct canonical User Flow child label, preview the issue, and create it only after user confirmation.

## When to Use

- User wants to add a roadmap item, roadmap request, or product roadmap candidate.
- The request belongs in the Roadmap team (`RO`) and should feed the product roadmap.
- Do not use for implementation tickets, PR work, bug reports, closing work, or generic Linear issue creation.
- Do not use when "create Linear issue" is the phrasing — use `creating-linear-issue` for that.

## Workflow

| Step | Requirement |
|---|---|
| 1 | Parse the user request into title, problem, desired outcome, priority, estimate, and obvious product area |
| 2 | Query live Linear metadata for the Roadmap team: labels, statuses, and candidate User Flow child labels |
| 3 | Resolve one canonical User Flow child label using the same matching rules as `creating-linear-issue` |
| 4 | Stop and ask the user to choose when no User Flow label clearly fits |
| 5 | Resolve priority, estimate, status, and useful labels from live Linear metadata |
| 6 | Show a concise Linear issue preview |
| 7 | Create the Linear issue only after user confirmation |

## User Flow Tag

Every roadmap item created by this skill needs one User Flow child label.
Always try to resolve the User Flow label from live workspace labels; leaving the Linear project blank never makes the User Flow label optional.

Use the same lookup mechanics as `creating-linear-issue/references/linear-operations.md`:

- query labels at workspace scope
- keep labels whose parent label name is `User Flow`
- match candidate names and descriptions against the request title, product area, and user outcome
- propose exactly one label when one clear match exists
- list close alternatives when several are plausible
- ask the user to pick from current child labels when no clear match exists
- never hard-code User Flow label names

Do not create the roadmap item until the User Flow label is confirmed.

## Linear Fields

Use live Linear metadata instead of hard-coded adapter-specific tool names or YAML payloads.

| Field | Rule |
|---|---|
| Team | Always Roadmap (`RO`) |
| Title | Action-oriented, under 80 characters when practical |
| Priority | Use user-provided priority when present; otherwise default to Normal |
| Estimate | Use user-provided size/effort when present; otherwise default to S |
| Project | Always leave blank. Do not set a project, even when a matching Roadmap project exists |
| Status | Use the team's triage or backlog-like state from live statuses |
| Labels | Include `feature`, the confirmed User Flow child label, and any matching scope/persona labels from live metadata |

If required Linear metadata cannot be loaded, stop before creation and report the missing metadata. Do not fall back to stale hard-coded label or status names for roadmap item creation.

## Preview and Confirmation

Before creating the issue, show a concise preview:

- title
- Roadmap team
- project: blank
- priority and estimate
- status
- labels, including User Flow
- description sections that will be sent to Linear

Ask the user to confirm or adjust. Apply natural-language adjustments and show the updated preview again.

## Description

Keep the Linear description product-level. Include:

```md
## Description
...

## User Outcome
...

## Business Rationale
...
```

## Creation

After confirmation, create the issue with the available Linear issue-creation tool. Confirm success with the Linear issue identifier and URL.

## Stop Conditions

- The request is too vague to draft a title and user outcome.
- Live Linear metadata for Roadmap cannot be loaded.
- No User Flow child label is confirmed.
- The user has not confirmed the preview.
- The Linear create operation fails after one retry.
