---
name: ui-rules
version: 4
description: >-
  Define project-wide UI direction before any code is written — triggers like "set UI rules", "write anti-slop guardrails", "plan UI direction". Reads an existing `<cwd>/.plans/DESIGN.md`, runs a focused discovery interview, and writes `<cwd>/.plans/UI-RULES.md` — a project-wide rulebook for downstream implement skills. Pick this for a project-wide rulebook rather than a per-feature design brief, and when the goal is a planning document, not working UI code. Never writes UI code.
---

# UI Rules

Project-wide UI rulebook generator. Pairs with `<cwd>/.plans/DESIGN.md` to guide every later UI build.

## Inputs and outputs

- **Required input**: `<cwd>/.plans/DESIGN.md` — must contain design tokens and prose covering palette, fonts, density, shape, and mood. Validate the file's contents; do not assume a specific upstream schema.
- **Required input**: discovery interview with the user — see [DISCOVERY.md](DISCOVERY.md).
- **Output**: `<cwd>/.plans/UI-RULES.md` — frontmatter plus 7 content sections (see Workflow §3).

## Core rules

1. **DESIGN.md must exist first.** If `<cwd>/.plans/DESIGN.md` is missing, stop and tell the user a `DESIGN.md` must exist at `<cwd>/.plans/DESIGN.md` first. Do not invent design tokens.
2. **Never overwrite silently.** If `<cwd>/.plans/UI-RULES.md` already exists, read it, summarise its contents, and ask the user: update in place, version-bump, or abort.
3. **Anti-slop is non-negotiable.** Apply every rule in [ANTI-SLOP.md](ANTI-SLOP.md). The bans are absolute; the reflex-font list is absolute. No exceptions for "this case is different".
4. **Tailor, don't templatise.** Project rules must reference DESIGN.md's actual tokens (colours, fonts, density). Generic "use OKLCH" advice is useless without naming the project's specific palette decisions.
5. **No code in UI-RULES.md output.** The artefact is prose rules — not CSS, not components. Implementation is a separate skill's job. (Companion files in this skill may use CSS as illustration; the output file must not.)
6. **No fabricated references.** Don't cite fonts, packages, or APIs you can't verify exist.

## Workflow

### 1. Read DESIGN.md and check resume state

- Read `<cwd>/.plans/DESIGN.md` end-to-end. Note the chosen palette, fonts, density, shape, and stated mood. If any of those are absent, surface the gap to the user before continuing.
- If the file is missing, abort and tell the user a `DESIGN.md` must exist at `<cwd>/.plans/DESIGN.md` first.
- Glob `<cwd>/.plans/UI-RULES.md`. If present, read it and ask the user: update in place, version-bump, or abort.
  - **Version-bump path**: glob `<cwd>/.plans/UI-RULES.v*.md`, find the highest existing `N`, rename the current `UI-RULES.md` to `UI-RULES.v{N+1}.md` (start at `v1` if none exist), then proceed to write the new `UI-RULES.md`.

### 2. Discovery interview

Run the interview in [DISCOVERY.md](DISCOVERY.md). Skip any question DESIGN.md already answers. Bundle 2–4 questions per turn — do not drip-feed.

The interview surfaces what DESIGN.md doesn't capture: anti-goals, interaction priorities, motion appetite, accessibility floor, project-specific anti-slop boundaries, anti-references.

### 3. Synthesise UI-RULES.md

While drafting, consult [AESTHETICS.md](AESTHETICS.md) for the principle rationale behind each recommendation, and [EXAMPLES.md](EXAMPLES.md) to verify each section meets the slop / distinctive bar.

Write `<cwd>/.plans/UI-RULES.md` with this exact order — frontmatter plus 7 content sections:

1. **Frontmatter** — `name`, `version`, `derivedFrom: .plans/DESIGN.md`, `updatedAt` (date).
2. **Aesthetic Direction** — 3 brand words, one sentence on the chosen extreme (brutalist, editorial, refined-minimal, maximalist, etc.), one sentence on what makes this UNFORGETTABLE.
3. **Typography Decisions** — the actual fonts chosen (must not appear in [ANTI-SLOP.md](ANTI-SLOP.md) reflex-font list), pairing rationale, scale ratio, line-length cap.
4. **Colour & Theme Decisions** — light/dark choice with the specific user-context justification, tinted-neutral hue, accent-usage rule, contrast floor.
5. **Spatial & Motion Decisions** — spacing scale, grid strategy, motion appetite (none / restrained / expressive), easing family.
6. **Project-Specific Bans** — the subset of [ANTI-SLOP.md](ANTI-SLOP.md) bans that matter most given the brief, plus any user-named anti-references.
7. **AI Slop Test** — the 3 questions a reviewer should ask of any UI built under these rules (pulled verbatim from [ANTI-SLOP.md](ANTI-SLOP.md)).
8. **Open Questions** — anything the implementer must resolve at build time.

Each content section: 4–10 lines. Reference DESIGN.md tokens by name (e.g. "use `--md-sys-color-primary` from DESIGN.md") rather than re-stating values.

### 4. Confirm and finish

Show the user the full `UI-RULES.md` body. Get explicit confirmation. If they push back on a section, revisit the relevant discovery question and rewrite that section only — do not redo the whole brief.

Once confirmed, the artefact is done. Any downstream implement skill can now consume it alongside DESIGN.md.

## Companion files

Each companion covers a distinct domain — splitting is by domain, not by line count.

- [ANTI-SLOP.md](ANTI-SLOP.md) — absolute bans, reflex-font list, AI-tell patterns, the 3-question AI Slop Test.
- [AESTHETICS.md](AESTHETICS.md) — typography, colour/OKLCH, spatial, motion, interaction principles. The "why" behind the rules.
- [DISCOVERY.md](DISCOVERY.md) — interview questions and section-mapping table.
- [EXAMPLES.md](EXAMPLES.md) — before/after pairs showing slop vs distinctive UI direction.
