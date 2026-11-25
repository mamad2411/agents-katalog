---
name: nk-documentation-best-practices
description: >-
  Use this skill whenever creating or updating documentation across any Naykel
  project. Do not wait for an explicit request — if documentation is being
  created or updated, this skill applies.
---

# NK Documentation Best Practices

Shared documentation rules across all Naykel projects. Project-specific skills
extend this one — apply both, with the project skill taking precedence where
they conflict.

## Review Workflow

- Mark every new heading with `(review)` until its content is confirmed.
- When you update a section carrying `(review)`, ask: "[Section name] has been
  updated. Is this section complete?"
- On confirmation: remove the `(review)` tag.
- Leave `(review)` on any headings that are still unresolved.
- When all `(review)` tags are gone from a doc, it is considered complete.
- When closing documentation work, call out which headings or docs still carry
  `(review)` tags.

## Common Rules

- **One doc, one job.** If a page explains the mental model AND lists all
  properties AND shows a quickstart, split it.
- **Code-first.** Add prose only when behaviour is non-obvious or context is
  needed.
- **No `## Introduction` heading.** The lead is the introduction.
- Do not include process notes, review commentary, or TODOs in published docs.
- **No horizontal rules (`---`).** Use headings and spacing instead.

## Lead Quality

Every doc starts with a title and a one-line lead. The lead names what the page
covers and the outcome for the reader.

Watch out for leads that open with `Configure`, `Manage`, `Handle` — they
usually mean the sentence hasn't landed on a concrete object or outcome yet.

**Bad:** Set the disk your uploads use, and make sure the same disk is used when
the app generates file URLs.

**Good:** Gotime stores uploaded files on a Laravel filesystem disk. This page
covers how to configure that disk for local storage or S3, including URL
generation for each environment.

## Nav Management

- Only add docs to nav after the doc or section has been reviewed and agreed.
- When starting work on a doc not yet in the nav, add it in its real category
  with `(wip)` suffixed to the name so it is accessible during development.
- Keep nav labels and sections minimal. Add structure back only as docs are
  reviewed and agreed.

## Completion Follow-Through

- When a doc is confirmed complete, remove `(wip)` from its nav label.

## Doc Types

Choose based on what is being documented.

| Type | Use for |
|------|---------|
| **Component** | Named component, trait, guide, or reference within a package |
| **Reference** | Operational and technical docs — commands, tools, workflows |

### Component

Show minimum working usage first.

```markdown
1. ## Basic Usage
2. ## Properties     ← reference table
3. Additional sections as needed
```

Rules:

- Properties table immediately after basic usage.
- Add sections only for behaviour that needs explanation beyond the table.
- For traits, add a short "When to Use" paragraph before Basic Usage.
- For guides, use numbered steps not bullet points. One goal per guide.
- For reference docs, omit Basic Usage — go straight to the reference tables.

### Reference

For operational and technical documentation — commands, tools, workflows,
cheatsheets.

```markdown
1. Prerequisites or assumptions (if needed)
2. ## Section per operation or topic
       ### Syntax
       ### Example
       ### In a Script (if applicable)
```

Rules:

- Group by operation, not by implementation detail.
- Syntax + Example is the default pattern per operation.
- For cheatsheets, keep it dense and scannable.
- List assumptions at the top.
