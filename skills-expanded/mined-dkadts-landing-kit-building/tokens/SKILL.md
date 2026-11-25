---
name: tokens
description: Generates site/css/tokens.css from DESIGN-LOCK.md and brief/animation.md. Refuses to work until DESIGN-LOCK is frozen. Sole writer of tokens.css in the project.
---

# /tokens

Turns the frozen `DESIGN-LOCK.md` constitution and the `brief/animation.md` motion spec into CSS variables in `site/css/tokens.css`.

## When to use

- Immediately after `/design-lock` (DESIGN-LOCK.md has LOCKED status on all sections).
- After `/animation` (motion tokens are added).
- When DESIGN-LOCK is changed via override (regenerate tokens).

## Requirements — HARD BLOCKING

**Refuse to work** if any DESIGN-LOCK field is `TBD` or any section is not `LOCKED`:

```
❌ Cannot generate tokens.
DESIGN-LOCK.md → §3 Color: STATUS = TBD.
Run /design-lock to complete.
```

Also refuse if `brief/animation.md` is missing (needed for motion tokens).

## Process

**Step 1. Read DESIGN-LOCK.md**
Ensure all 9 sections are `STATUS: LOCKED` and no value is `TBD`.

**Step 2. Read brief/animation.md**
Load motion decisions (intensity multiplier, stagger, computed durations).

**Step 3. Read site/css/tokens.css**
Existing template — do not rewrite everything, update values.

**Step 4. Map DESIGN-LOCK → tokens.css**

Explicit mapping:

| DESIGN-LOCK | tokens.css |
|---|---|
| §1 Spacing → base unit | `--space-base` |
| §1 Spacing → rhythm N× | `--space-1`, `--space-2`, ..., `--space-13` |
| §1 Section padding top/bottom | `--section-pad-top`, `--section-pad-bottom` |
| §1 Content max-width | `--content-max-w` |
| §1 Page margin left/right | `--page-padding-x` |
| §2 Type → font families | `--font-heading`, `--font-body`, `--font-mono` |
| §2 Type → sizes | `--fs-body`, `--fs-h1`, `--fs-h2`, `--fs-h3`, `--fs-caption` |
| §2 Type → line-height | `--lh-body`, `--lh-heading` |
| §2 Type → weights | `--fw-body`, `--fw-heading` |
| §3 Color | `--c-bg`, `--c-fg`, `--c-fg-muted`, `--c-accent`, `--c-border`, `--c-overlay` |
| §3 Color → semantic | `--c-success`, `--c-error`, `--c-warning` |
| §4 Radius | `--radius` (ONE value!) |
| §5 Motion → ease | `--ease`, `--ease-in`, `--ease-out` |
| §5 Motion → duration | `--dur-fast`, `--dur-base`, `--dur-slow` |
| §5 Motion → scroll-behavior (from /animation) | `--scroll-reveal` |
| §5 Motion → stagger-base-ms (from /animation) | `--stagger-base-ms` |
| §5 Motion → motion-multiplier (from /animation) | `--motion-multiplier` |

**Step 5. Post-generation checks**

- **Only 2 font weights** used in tokens (DESIGN-LOCK rule).
- **Only 1 radius** used.
- **Only 1 accent color**.
- **Only 1 ease-primary**.
- All variables named per convention (`--<category>-<name>`).

If anything is violated — do not save, return an error.

**Step 6. @font-face**

If self-hosted fonts exist in brand/fonts/ (`.woff2`):
- Add @font-face declarations at the top of tokens.css.
- Reference `/fonts/*.woff2`.
- `font-display: swap`.
- Log: user may need to add preload to `index.html`.

**Step 7. Update DESIGN.md**

In the "Design tokens" section — brief summary of what was generated (for reference, no value duplication).

## Rules

- **One writer.** Only `/tokens` writes `site/css/tokens.css`. `/build` only reads.
- **No hardcode.** Every value comes from DESIGN-LOCK.
- **Do not invent variables.** If DESIGN-LOCK didn't decide — go back to `/design-lock` (do not invent).
- **Comments in CSS.** Each variable block is annotated "§N of DESIGN-LOCK.md".

## What NOT to do

- Do not edit tokens.css by hand after generation (next run overwrites).
- Do not create "intermediate" variables not in DESIGN-LOCK.
- Do not merge project-specific additions with the base set — everything via DESIGN-LOCK override.

## Next

- `/media` — media conversion.
- `/icons` — icon set.
- `/build` — section assembly with tokens ready.
