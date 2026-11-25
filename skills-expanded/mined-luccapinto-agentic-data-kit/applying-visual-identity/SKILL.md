---
name: applying-visual-identity
description: Use when the user wants output to follow a company's brand / visual identity, or asks to set one up — "use our brand", "make it on-brand", "here's our identity", "create a DESIGN.md". Reads and applies a DESIGN.md (Google Labs open spec): brand tokens for colors, typography, spacing, radius, shadows, and components, so decks, sites, and docs come out consistently on-brand. Scaffolds a DESIGN.md when none exists.
---

# Skill: applying-visual-identity

A company's visual identity lives in a **`DESIGN.md`** at the project root — the open
spec from Google Labs (Apache-2.0, 2026). It pairs machine-readable **design tokens** (YAML
frontmatter) with human-readable rationale (prose), so any AI tool renders the brand the same
way across sessions. This skill reads that file and applies it; if none exists, it scaffolds one.

## Workflow
1. **Locate.** Look for `DESIGN.md` in the project root. If found, parse the frontmatter tokens
   — they are the *normative* values; the prose is guidance.
2. **Apply.** Map tokens to the target medium:
   - **HTML/reveal.js/Marp** → CSS custom properties on `:root` (`--brand-primary`, `--font-heading`, …).
   - **Markdown/docs** → headings, callouts, accent usage per the Do's/Don'ts.
   - Resolve token references like `{colors.primary}` before output.
3. **Stay in-spec.** Use only defined tokens; don't introduce off-palette colors or fonts. If a
   needed token is missing, ask or pick the closest defined one and note it.
4. **Scaffold when absent.** If there's no `DESIGN.md`, offer to create one from
   `templates/DESIGN.md` — ask for (or extract from a provided logo/site) the primary color,
   font, and tone. Never silently invent a brand; fall back to a neutral theme until confirmed.

## The DESIGN.md format (Google Labs spec)
YAML frontmatter holds the tokens; the body documents intent in fixed sections.

**Frontmatter token groups:** `colors`, `typography` (objects: `fontFamily`, `fontSize`,
`fontWeight`, `lineHeight`, `letterSpacing`), `spacing`, `rounded`, `shadows`, `components`
(per-component token refs). Colors accept hex / rgb / hsl / `oklch()`. Dimensions carry units
(`px`, `rem`). References use braces: `{colors.primary}`, `{typography.h1}`.

**Body sections (in order):** Overview · Colors · Typography · Layout & Spacing ·
Elevation & Depth · Shapes · Components · Do's and Don'ts.

See `templates/DESIGN.md` for a complete, fillable example.

## Rules
- Tokens are normative — match them exactly; the prose only explains *why*.
- Keep `DESIGN.md` in the **project root** so every tool and agent finds it.
- One source of truth: when the brand changes, edit `DESIGN.md`, not individual decks.
- This skill defines the *look*; `building-html-presentations` defines the *structure*.
