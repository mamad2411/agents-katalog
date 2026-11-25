---
name: design-refactor
description: >
  Improve an EXISTING UI: normalise components, migrate to shadcn/ui + Radix, replace native select/date/dialog controls, polish a screen without breaking behaviour. For polish and design-debt cleanup.
---

# Design refactor

The improve-what-exists half of the design pipeline. `design-pipeline` governs
new surfaces; this one takes a surface that already works and makes it good,
without changing routes, data flow or markup semantics — except to fix
accessibility.

## The rule that overrides taste here

**Native interactive elements are never acceptable.** No native date picker, no
raw `<select>`, no browser `<dialog>`, no `confirm()`. Always a custom
shadcn/Radix component. `reference/native-to-shadcn.md` gives the replacement
for each one, the `Select`-vs-`Combobox` decision, the react-hook-form
`Controller` pitfall, and the behaviour a swap must not lose.

```bash
aval design gate native src/
```

Exits non-zero on any hit. `components/ui/**` is exempt — that is where the
Radix wrappers legitimately live.

## Order of work

Audit, then apply in order: tokens, typography and spacing, component states,
motion. Never the reverse: restyling components before the tokens are
consolidated just re-hardcodes the same drift in new places.

## Consistency is the whole job

> Consolidate to ONE shared token theme and make every page consume it. A
> redesign that leaves different pages on different palettes has failed.

Verify it, do not assert it:

Run the gates and report their output:

```bash
aval design gate hardcodes src/                       # literal colours/sizes that should be tokens
aval design gate theme-refs --theme theme.css src/    # var(--x) pointing at nothing
aval design gate pairs tokens/colors.json             # every fg/bg pair, light and dark
```

## Micro-interactions

Motion is added last and only with a stated reason. Defaults that survive
review: 100ms for a state echo, 200ms for an entrance, ease-out on enter and
ease-in on exit, `transform` and `opacity` only — never `width`, `height` or
`top`. Every animation needs a `prefers-reduced-motion` branch;
check it in the render; no gate covers it.

## Verification is not optional

Run the gates against a states harness, then render it with
`~/.claude/skills/design-pipeline/scripts/shot.mjs` and look at the screenshots.
That is the step that catches what no gate does: mismatched stroke weights, a
control that reads too heavy, a transition artefact mid-animation.

Report real output as `[design-audit]`. A gate you did not run is reported as
not run, never as a pass.
