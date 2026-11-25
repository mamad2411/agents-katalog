---
name: recording-studio-output
description: Finish the whole Recording Studio deliverable instead of truncating. Use when a screen, critique, or theme change must be complete. Execution is Flatpack ViewComponents, tokens, and named themes.
---

# Recording Studio output

Taste and branding are direction. Implementation is always Flatpack ViewComponents, tokens, and named themes. The dummy default is `html data-theme="rounded"` plus core `UsesDefaultLayout`. Hosts get a named theme (for example `featured-in`), not forked CSS. Never Tailwind, shadcn, GSAP, custom CSS kits, or third-party UI libraries on gem, dummy, or Admin screens. If a look is missing, add a Flatpack token or component first.

Adapted from [leonxlnx/taste-skill](https://github.com/leonxlnx/taste-skill) `skills/output-skill` (MIT, Leonxlnx). See `docs/taste-skill-attribution.md`.

Taste critique: `recording-studio-taste`. Audit path: `recording-studio-redesign`. Page shape: `recording-studio-ui`. Components: `recording-studio-flatpack`. Image then code: `recording-studio-image-to-code`. Direction packs: `recording-studio-soft`, `recording-studio-minimalist`, `recording-studio-brutalist`. Brand: `recording-studio-brandkit`.

## When to use

- A screen, helper, or named theme must actually ship
- A Taste review must include the full four-part critique, not a summary
- A previous turn truncated files, left TODOs, or said "the rest is similar"

A partial output is a broken output. Completeness does not license Tailwind skeletons, GSAP samples, or "use any CSS framework" leftovers.

## Banned patterns

Hard failures:

**In code:** `// ...`, `// rest of code`, `// implement here`, `// TODO` standing in for work, `/* ... */`, `// similar to above`, `// continue pattern`, bare `...` for omitted markup.

**In prose:** "let me know if you want me to continue", "for brevity", "the rest follows the same pattern", "similarly for the remaining", "I'll leave that as an exercise."

**Structural shortcuts:** A skeleton when a full implementation was asked. First and last section with the middle skipped. One example plus a description of repeats. Describing Flatpack instead of rendering it.

**Taste shortcuts:** Checklist-only reviews. "Looks fine" with no "this would look better if…" notes.

## Process

1. **Scope** - Count deliverables: files, screens, critique parts, theme tokens. Lock the number.
2. **Build** - Finish every deliverable in Flatpack. No "you can extend this later."
3. **Cross-check** - Re-read the request. If a file, state, or critique part is missing, add it before responding.

When a response hits a token limit, stop on a clean breakpoint (end of a component, end of a file, end of a critique part). End with:

```
[PAUSED - X of Y complete. Send "continue" to resume from: next section name]
```

On continue, pick up exactly there. No recap.

## Recording Studio completeness

A finished screen includes:

- Flatpack components, not hand-rolled buttons or forms
- Default layout (or the host named theme) wired, not described
- Loading, empty, and error when those states exist in the job
- Copy that follows `recording-studio-text`
- The four-part Taste critique when the task was a review

A finished host look includes the named theme hook (`data-theme="…"`), not a forked stylesheet.

## Quick check

- No banned truncation patterns
- Every requested item is present and finished
- Code is runnable Flatpack, not a sketch of another stack
- Critique is four parts, not a checklist
- Dummy / gem / Admin still rounded plus `UsesDefaultLayout` unless opted in
