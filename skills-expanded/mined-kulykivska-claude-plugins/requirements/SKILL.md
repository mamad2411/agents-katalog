---
name: requirements
description: >-
  Turn a raw (often dictated) idea into concrete requirements before coding.
  Trigger on "let us build...", "I want a feature...", "add a feature", or any
  substantial new-feature request where scope is fuzzy. Produces user-visible
  behavior, edge cases, acceptance criteria, and a consistency check against
  the existing app.
---

# Requirements

Turn an idea into something implementable without back-and-forth later.

## Steps

1. **Restate the goal** in one sentence: who gets what value.
2. **Concretize behavior**: for each user-visible surface (web, iOS, API,
   voice), what exactly does the user see/do? Free vs paid tier treatment
   (default policy: free = teaser, paid = everything).
3. **Edge cases**: empty data, first-time user, offline/failed upstream,
   locale (en/uk/es where the app is localized), mobile layout.
4. **Consistency check**: grep the codebase for adjacent features; flag
   anything the new behavior would contradict (naming, gating, i18n,
   existing endpoints). List conflicts explicitly.
5. **Acceptance criteria**: a short checklist that QA (the `qa` skill) can
   execute verbatim.
6. Keep it tight: one screen of output. If a decision is genuinely the
   owner's (pricing, tier gating changes, external services), ask; otherwise
   pick the sensible default and note it.
