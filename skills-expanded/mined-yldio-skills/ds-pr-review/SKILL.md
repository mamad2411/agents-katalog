---
name: ds-pr-review
description: Reviews a UI pull request against design system rules and writes one comment grouped by severity. Use when a PR touches UI in a design system component library or an app that consumes it, before a person starts the design review.
---

# Design System PR Review

## When to use

A pull request touches UI in a design system component library or an app that
consumes it. Run it before a person starts the design review, not instead of it.

## You need

- The PR diff, with enough surrounding code to show how components are composed
- The repo type: component library or consuming app
- The design system: components, tokens (Tailwind config or CSS variables) and
  Storybook docs
- The rules file for that profile, with severities
- Linked Figma frames, if the change implements a specific design (pulled through
  the Figma MCP)

## Steps

1. State what the input covers and what it doesn't.
2. Load the rule profile for the repo type.
3. Pick out the files in the diff that touch UI.
4. Consuming app: check DS components are used, not local copies; props and
   variants match the docs; no internal styles are overridden.
5. Consuming app: check tokens are used, not hardcoded colours, spacing, radii,
   type or shadows, and no arbitrary Tailwind values.
6. Library: check referenced tokens exist, flag public prop or variant changes as
   breaking, and confirm stories, docs and Code Connect mappings are updated.
7. Check layout: spacing scale, grid, breakpoints, responsive behaviour.
8. Check accessibility: semantic elements, labels, alt text, focus states,
   keyboard access, contrast, ARIA use.
9. Check polish: loading, empty, error and disabled states; hover and focus
   styles; long content and truncation.
10. If a Figma frame is linked, compare the implementation and flag drift.
11. Write one PR comment grouped by severity.
12. List anything you were unsure about.

## Decisions and defaults

- Which rule profile applies. Default: ask before proceeding.
- What blocks merge, what is a warning, what is a nit. Default: ask before
  proceeding.
- Custom component: justified, or a DS candidate. Default: ask before proceeding.
- How strict to be on tokens, and which values are exempt. Default: ask before
  proceeding.
- Figma mismatch: code wrong or design out of date. Default: ask before
  proceeding.
- Every instance, or once per pattern with a count. Default: ask before
  proceeding.
- Suggest fixes only, or also push commits. Default: ask before proceeding.

## Output

One PR comment, in this order: rule profile used and a pass or fail line; findings
under Blocking, Should fix and Nit, each with file and line, rule broken, why it
matters and a suggested fix; breaking changes (library profile only); what
couldn't be checked, such as runtime contrast or animation; uncertainties.

## Never do this

- Do not apply a rule profile without confirming the repo type.
- Do not flag legitimate exceptions as violations.
- Do not treat a Figma file as the source of truth. Report drift for a designer.
- Do not report runtime-only accessibility issues as fact. Flag them for a manual
  check.
- Do not let minor findings bury blocking ones on a large PR.
- Do not suggest components, props or tokens that don't exist.
- Never approve or merge a PR, or edit the design system.
- Do not invent numbers, names, quotes or trends. If the input doesn't support it,
  say so and leave a placeholder.

## Before it goes out

- A reviewer opens two or three of the blocking findings in the diff and confirms
  the file, line and rule are right, and that each suggested fix uses a component,
  prop or token that exists in Storybook.
- The profile line at the top matches the repo.
- A designer checks Figma mismatches and decides which side is right.
- Custom-component exceptions are approved before they become precedent.
- The library maintainer signs off any flagged breaking change.
- False positives are logged so the rules files can be tuned.

This output is a draft. A person signs it.
