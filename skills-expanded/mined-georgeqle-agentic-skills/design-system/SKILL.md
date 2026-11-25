---
name: design-system
description: Extract or scan design tokens from a consolidated UI spec or existing codebase and produce a DESIGN.md file following the Google Labs Stitch format — machine-readable YAML frontmatter with prose rationale sections
type: planning
version: v0.3
required_conventions: [alignment-page]
argument-hint: "[spec path | --scan | --update]"
visual_tier: prototype
---

# Design System

Invoke as `$design-system`.

Use this skill after `$consolidate-prototypes` to lock design decisions into machine-readable tokens before implementation begins. It bridges the gap between prose UI specs and code — without it, agents interpret "dark surface with primary accent" differently each session, causing UI consistency drift.

Also use this skill retroactively on an existing codebase (`--scan`) to generate a DESIGN.md from tokens already in use.

## Modes

- **Default**: reads `specs/ui-final-*.md` or `prototypes/*/consolidated/` (or a user-provided spec path) and extracts tokens.
- **`--scan`**: scans the codebase for CSS custom properties, Tailwind config, theme files, and component patterns to reverse-engineer a DESIGN.md.
- **`--update`**: reads an existing `DESIGN.md` alongside new spec changes and produces an updated version.

## Process

1. **Resolve context**
   - Read `.agents/project.json`, `README.md`, `AGENTS.md`, `CLAUDE.md` when present.
   - Locate the input source:
     - Default: find `specs/ui-final-*.md` or accept a path argument.
     - `--scan`: find `tailwind.config.*`, `globals.css`, CSS custom property files, theme files, component directories, and any existing design token files.
     - `--update`: read the existing `DESIGN.md` and the changed spec or codebase files.
   - If no input can be found, ask the user to point to the source.

2. **Extract raw tokens**
   - From spec: pull every concrete visual decision — colors (hex, HSL, OKLCH), font families, font sizes, weights, line heights, spacing values, border radii, shadows, elevation layers, and component-level styling.
   - From codebase (`--scan`): parse Tailwind config extends, CSS custom properties, repeated Tailwind classes, theme provider values, and component prop defaults. Deduplicate and group by semantic role.
   - Normalize all colors to hex. Record OKLCH or HSL originals as comments when present.
   - Identify semantic roles: primary, secondary, accent, surface, background, on-primary, on-surface, error, warning, success, info, border, muted.

3. **Interview to confirm tokens**
   - Present the extracted token inventory grouped by category (Colors, Typography, Spacing, Shapes, Elevation, Components).
   - For each category, ask one primary confirmation or adjustment question per turn. If the session is already in Plan mode and there are 2-3 concrete options for the current token decision, prefer `request_user_input`; otherwise ask one concise plain-text question.
     - Are these the correct values? Flag any that look like defaults vs intentional choices.
     - Are there missing semantic roles? (e.g., no error color found, no hover state defined)
     - For typography: confirm the scale — is this intentional or inherited from a framework default?
     - For spacing: confirm the scale — 4px base? 8px base? Irregular?
   - Do not batch unrelated token categories into the same question. Continue one category or decision at a time so the user can have a deeper discussion before moving on.
   - Record user confirmations and adjustments.

4. **Validate accessibility**
   - Check WCAG 2.1 AA contrast ratios for all foreground/background color pairings:
     - Normal text: minimum 4.5:1
     - Large text (≥18px bold or ≥24px): minimum 3:1
     - UI components and graphical objects: minimum 3:1
   - Report failures with the specific pairing, current ratio, and minimum required.
   - Resolve failures one at a time: adjust the color, accept the risk, or mark as decorative-only. If already in Plan mode, `request_user_input` may present those options for the current failure; otherwise ask one concise plain-text question.

5. **Draft DESIGN.md**
   - Follow the Google Labs Stitch format. The file has two parts:

   **Part 1 — YAML frontmatter** with machine-readable tokens:
   ```yaml
   ---
   version: "1.0"
   name: "Project Design System"
   colors:
     primary: "#1A1C1E"
     on-primary: "#FFFFFF"
     secondary: "#4A6741"
     surface: "#FAFAFA"
     background: "#FFFFFF"
     error: "#BA1A1A"
     border: "#E0E0E0"
   typography:
     h1:
       fontFamily: "Inter"
       fontSize: "2.25rem"
       fontWeight: 700
       lineHeight: 1.2
     body:
       fontFamily: "Inter"
       fontSize: "1rem"
       fontWeight: 400
       lineHeight: 1.5
   spacing:
     xs: "4px"
     sm: "8px"
     md: "16px"
     lg: "24px"
     xl: "32px"
   rounded:
     sm: "4px"
     md: "8px"
     lg: "16px"
     full: "9999px"
   elevation:
     sm: "0 1px 2px rgba(0,0,0,0.05)"
     md: "0 4px 6px rgba(0,0,0,0.1)"
     lg: "0 10px 15px rgba(0,0,0,0.1)"
   components:
     button:
       backgroundColor: "{colors.primary}"
       textColor: "{colors.on-primary}"
       rounded: "{rounded.md}"
       paddingX: "{spacing.lg}"
       paddingY: "{spacing.sm}"
     card:
       backgroundColor: "{colors.surface}"
       border: "1px solid {colors.border}"
       rounded: "{rounded.lg}"
       padding: "{spacing.lg}"
       shadow: "{elevation.sm}"
   ---
   ```

   **Part 2 — Prose sections** (all optional, must appear in this order if present):

   Each prose section must be written as a Markdown heading, not a bold paragraph label. Use `## Overview`, `## Colors`, `## Typography`, and the other section names below exactly when present.

   1. `## Overview` — brand identity, visual tone, and design philosophy.
   2. `## Colors` — palette rationale, dark mode strategy, semantic color usage.
   3. `## Typography` — type scale rationale, heading hierarchy, body text rules.
   4. `## Layout & Spacing` — grid strategy, spacing scale rationale, container max-widths, content density.
   5. `## Elevation & Depth` — shadow usage, layering rules, z-index strategy.
   6. `## Shapes` — corner radius philosophy, form language.
   7. `## Components` — styling guidance for UI atoms including state variants (hover, active, disabled, focus). Reference tokens using `{token.path}` syntax.
   8. `## Do's and Don'ts` — concrete guardrails. Include at least: colors to never use, spacing anti-patterns, component misuse patterns observed in prior implementations.

   - Use `{colors.primary}` cross-reference syntax in component definitions and prose.
   - Present the draft to the user and ask one concise approval or adjustment question before writing.

6. **Write deliverables**
   - Write `DESIGN.md` to the project root.
   - If `--update`: archive the previous version to `docs/history/archive/YYYY-MM-DD/HHMMSS/DESIGN.md` first.

## Deliverables

- `DESIGN.md` in the project root — the single source of truth for visual identity, consumed by both Claude Code and Codex.
- Interview log written to `design-system-interview.md` in the project root.

## Constraints

- Do not invent token values. Every value must come from the spec, codebase scan, or explicit user confirmation.
- Do not skip the accessibility check. Report all contrast failures even if the user is likely to accept them.
- Do not include tokens for features that don't exist yet — scope to the current spec or codebase.
- Keep the YAML frontmatter machine-readable. No comments in YAML. Put rationale in prose sections.
- Token cross-references use curly braces: `{colors.primary}`, `{spacing.md}`, `{rounded.lg}`.
- When recommending a skill from another pack, verify the pack is installed via `.agents/project.json` `enabled_packs`. If not installed, recommend `npx skillpacks install <pack-name>` from the project shell, before the target skill.
- When updating an existing DESIGN.md, preserve token names and values that haven't changed. Only modify tokens that the new spec explicitly changes.

## Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page following `ALIGNMENT-PAGE.md` in this skill's directory. Output: `alignment/design-system-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
