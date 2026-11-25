---
name: design-token-generation
description: Use when turning typographic decisions into tokens, variables, or theme config — naming a type scale, structuring font/size/weight/line-height tokens, exporting to CSS/Tailwind/Style Dictionary/iOS/Android, or fixing a token set that has drifted into arbitrary values. Also use when design and code disagree about what the type scale actually is.
---

# Typographic design token generation

Tokens are how a type scale survives contact with a codebase. A scale that isn't
enforced is a suggestion.

## 1. When to invoke

- Turning a type scale into tokens, CSS variables, or theme config.
- Naming typographic tokens.
- Exporting type across platforms (web, iOS, Android).
- A token set has accumulated arbitrary values, or design and code disagree.

**Do not** invoke to design the scale (`hierarchy-and-scale`) or choose the face
(`typeface-selection`). Tokenize decisions already made.

## 2. Required context

- The **finalised scale** and its rationale.
- **Target platforms** and their unit conventions.
- Whether tokens must support **theming** (density modes, brand variants).
- Whether the pipeline is **generated** (Style Dictionary, Figma variables) or
  hand-maintained.
- Whether **fluid/responsive** values are in scope.

## 3. Invariant principles

- **Three tiers: primitive → semantic → component.**
  - *Primitive* — raw values, no meaning: `font-size-300: 1.125rem`.
  - *Semantic* — role-based, referencing primitives: `text-body-size`.
  - *Component* — component-scoped, referencing semantics: `button-label-size`.
  Components consume semantics. Semantics consume primitives. **Never let a
  component reference a primitive directly** — that's how a scale erodes.
- **Name by role, never by appearance.** `text-body`, not `text-16` or `text-grey`.
  Appearance names become lies the first time the value changes. This is
  Kholmatova's naming argument applied to type: a presentationally-named token
  "can only be pink" — confined to the value it was named after — while a
  role-based name survives the value changing under it.
- **Never name by size number alone.** `text-14` blocks you from ever changing 14.
- **Line-height tokens must be unitless.**
- **A token set is a constraint.** If arbitrary values remain possible, tokens are
  documentation, not enforcement. Lint for off-token values.
- **Typography tokens are composite in practice.** Size, line-height, weight,
  tracking, and family travel together; a size alone is rarely a usable token.

## 4. Context-dependent heuristics

**Numeric primitive scales** (`100`, `200`, `300`…) leave room to insert values.
T-shirt sizes (`sm`, `md`, `lg`) run out fast and force renames. Prefer numeric
for primitives, semantic names above that.

**Composite type tokens.** The W3C Design Tokens format has a `typography` type
bundling the properties that must move together:

```json
{
  "text": {
    "body": {
      "$type": "typography",
      "$value": {
        "fontFamily": "{font.family.sans}",
        "fontSize": "{font.size.300}",
        "fontWeight": "{font.weight.regular}",
        "lineHeight": "1.5",
        "letterSpacing": "0"
      }
    }
  }
}
```

Composite tokens prevent the common bug where someone updates a size and leaves
the line-height behind.

**Fluid values in tokens.** A `clamp()` expression can be a token value, but it's
opaque to non-CSS platforms. Two options: store min/max/preferred as separate
primitives and compose per platform, or keep a stepped token set as the source of
truth and derive fluid CSS from it. Choose based on whether iOS/Android consume the
same tokens.

**Platform units.** Web `rem`; iOS points with Dynamic Type text styles; Android
`sp` (never `dp` for text — `sp` respects the user's font-size setting). A
generator must emit the right unit per platform, not a shared `px`.

**Density themes.** A compact mode is a *different semantic layer over the same
primitives*, not a second primitive scale.

**Don't tokenize everything.** One-off display sizes used once are not tokens.
Rule of three: tokenize on the third use.

## 5. Failure patterns

| Pattern | Cause | Fix |
|---|---|---|
| `text-16` now renders 18px | Named by value | Rename by role |
| Size changed, line-height didn't | Separate tokens, no composite | Composite typography token |
| Component references a primitive directly | Tier skipped | Route through a semantic |
| Arbitrary `font-size: 15px` in the codebase | No enforcement | Lint off-token values |
| Android text ignores user font-size setting | `dp` instead of `sp` | Use `sp` |
| Token set has 40 sizes | Every one-off tokenized | Tokenize on third use |
| Figma and code disagree | Two hand-maintained sources | One source, generated both ways |
| Dark theme needed a new size scale | Weight/colour conflated with size | Theme the semantic layer only |
| `lineHeight: "24px"` | Fixed unit | Unitless |

## 6. Evaluation procedure

1. Confirm three tiers exist and each references only the tier below.
2. Grep component tokens for direct primitive references. Should be zero.
3. Grep the codebase for raw font-size/line-height values. Should be zero outside
   token definitions.
4. Confirm every name is role-based, not value- or appearance-based.
5. Confirm all line-heights are unitless.
6. Build for every target platform; verify units (`rem` / points / `sp`).
7. Change one primitive and rebuild — confirm the change propagates everywhere it
   should and nowhere it shouldn't.
8. Verify the generated output against the rendered result, not just the build log.

## 7. Output format

```
Tiers: primitive <n> · semantic <n> · component <n>
Naming: role-based <yes/no> — violations: <list>
Composite typography tokens: <yes/no>
Line-heights unitless: <yes/no>
Platforms: web <unit> · ios <unit> · android <unit>
Off-token values in codebase: <n> — <locations>
Propagation test: changed <token> → <n> surfaces updated, <expected?>
Fluid strategy: <clamp-in-token | derived | n/a>
```

## 8. Examples

**Scale from `hierarchy-and-scale` (1.2 ratio, body 14, four levels) into tokens.**

> Primitives carry the raw ramp: `font-size-100: 0.875rem` … `font-size-400:
> 1.5rem`, numeric so a value can be inserted later without renaming. Semantics
> name roles: `text-body`, `text-card-title`, `text-section`, `text-page-title` —
> each a composite token bundling family, size, weight, line-height, and tracking,
> so a size change can't leave line-height behind. Components reference only
> semantics. Android emits `sp`, iOS maps to Dynamic Type text styles, web emits
> `rem`. Added a lint rule failing the build on any raw `font-size` outside the
> token file — without that, the scale is advisory.

## 9. Counterexamples

- ❌ `--text-16: 16px` — names the value; guarantees a lie on first change.
- ❌ `--heading-blue-large` — appearance naming, three ways.
- ❌ Component token pointing straight at a primitive. — Skips the semantic layer,
  so rebranding requires touching components.
- ❌ `lineHeight: "1.5rem"` — fixed unit; breaks at other sizes.
- ❌ Android text in `dp`. — Ignores the user's font-size preference.
- ❌ "We have tokens" with 200 raw values in the codebase. — Documentation, not
  enforcement.
- ❌ Maintaining the scale by hand in both Figma and CSS. — They will diverge.

## 10. Source citations

- Kholmatova, *Design Systems* (ch. 5, "Shared Language") — naming brings an
  object into existence; a presentational name confines an object's future to
  its current style. The general token-tier and naming argument this skill
  applies to typography; see the `design-tokens` skill for the full treatment.
- Stocks, *Universal Principles of Typography* — a typographic scale is already a
  design system; a full system documents how typographic elements interact with
  other elements and offers a limited set of options via constraints.
- Brown, *Flexible Typesetting* — the modular scale as a shared system of
  measurement referenced throughout a composition.
- Santa Maria, *On Web Typography* — devising a sizing and spacing system;
  standardising method reproducibly and enabling consistency across a team.
- Latin, *Better Web Typography* — modular scale and meaningful typography.
- [W3C Design Tokens Community Group format](https://tr.designtokens.org/format/) —
  composite `typography` token type.
- MDN — [custom properties](https://developer.mozilla.org/en-US/docs/Web/CSS/--*).
