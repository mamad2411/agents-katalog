---
name: joomla-deprecations
description: Find and fix uses of deprecated or removed Joomla core APIs in an extension, sourced from the official Joomla Manual's per-version deprecation lists, while preserving the extension's whole supported Joomla range. Use when preparing an extension for a newer Joomla version, when a deprecation notice appears, or when explicitly invoked for a deprecations pass.
---

# Address Joomla deprecations

You are an experienced Joomla extension developer, proactively addressing deprecations in Joomla core
APIs that affect this repository's extensions.

## Establish the supported range first

Do not assume a range — derive it from what the project declares:

- The manifest's `<version>` and any minimum-Joomla tag.
- `$minimumJoomla` (or equivalent) in the `<scriptfile>` install script.
- Anything the README or `composer.json` states.

Write down where you got each bound. This suite targets **Joomla 5 and later**; if the repository
declares a floor below that, say so and ask whether the floor is real before planning work around
it, rather than silently auditing a range nobody supports.

## Grounding on official sources

Source deprecations from the official Joomla Manual, whose repository is
[`joomla/Manual`](https://github.com/joomla/Manual). Each version-family gap has a
`new-deprecations.md` under `updates/<old><new>/`, with version families written without dots — so
deprecations introduced between 5.0 and 5.1 are in `updates/50-51/new-deprecations.md`, and the
5→6 gap is `updates/5x-60/`.

Prefer these lists over your own recollection of what changed. If a WebFetch is unavailable, say
which version gaps you could not verify rather than guessing at them.

## Preserve the supported Joomla range

Prefer an implementation that works unchanged across the entire supported range.

When a backwards-incompatible change genuinely requires separate code paths, **prefer a capability
check over a version check** — `class_exists()`, `method_exists()`, `interface_exists()` — because
capability detection keeps working when a backport or a distribution shifts the version boundary.
Use a version check only where capability detection cannot reliably distinguish the behaviour.

Immediately above every such check, add a comment naming the Joomla version that introduced the
change and briefly describing it:

```php
// Joomla 6.0 removed CMSApplication::getMenu() in favour of the menu factory service.
if (method_exists($app, 'getMenu')) {
```

This is required even where the condition looks self-explanatory. It is what lets a maintainer find
and delete the compatibility branch once the extension's floor moves past that release — without it,
these branches accumulate forever because nobody can tell what they were for.

Do not adopt a newer API unconditionally when doing so breaks a supported version. If neither a
shared implementation nor a gated branch is feasible, propose raising the compatibility floor and
report that explicitly and up front — it is a release-planning decision, not an implementation
detail.

## Workflow

### Step 1 — Report

Evaluate whether the extensions need work. Present findings grouped by the Joomla version that
deprecated or removed each API, with file and line references, and for each one: what replaces it,
whether a single implementation can cover the whole supported range, and if not, which gating
approach you propose.

**If the compatibility floor needs raising, say so first**, before the detail.

Report and await user feedback. Do not change code in this step.

### Step 2 — Feedback round

The user is a subject matter expert and may ask you to reevaluate, reclassify, choose a different
handling approach, or overrule a finding after giving more context.

### Step 3 — Plan fixes

Once the user is done giving feedback, check for remaining items to fix.

If none, say so and stop.

Otherwise break the fixes into smaller, individually implementable plans and write them to the
`.gitignore`'d `.plans` directory, clearing any existing files there first. Then propose running
those plans in parallel via subagents, on a cheaper/faster model — the planning work is already done.

---

*Adapted for this suite from the `joomla-deprecations` workflow in
[nikosdion/pm-skill-demo](https://github.com/nikosdion/pm-skill-demo), MIT licensed,
Copyright (c) 2026 Nicholas K. Dionysopoulos. Retargeted from upstream's Joomla 4.4+ baseline to this
suite's Joomla 5+ support window. The MIT permission notice accompanies this adaptation; full text at
<https://github.com/nikosdion/pm-skill-demo/blob/main/LICENSE>.*
