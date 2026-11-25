---
name: claude-design-brand
description: DEPRECATED — use Acta (acta-design) at https://github.com/erenisci/acta. Detect the project's character from its repo (project type, audience, voice) and produce a complete brand foundation — palette, typography, mood, motion, voice, accessibility — with type-specific recommendations the user can accept or override. Writes docs/design/BRAND.md + .claude/design-system.md + a CLAUDE.md block. Run this FIRST. Trigger on /claude-design-brand or "set up brand", "init brand", "design foundation".
---

# Claude Design Brand

The **first step** of the design pipeline. Reads the project, infers what kind of thing it is, and produces a brand foundation with opinionated recommendations. Output is the input to `claude-design-prompter` — every later artifact (logo, pages, landing) inherits these decisions.

---

## Localization

User-facing strings (questions, options, summaries) MUST be in the language the user is conversing with you in **right now**. Detection: current conversation language → README/CLAUDE.md dominant language → English. Translate canonical English strings on the fly. Internal artifacts (file names, frontmatter keys, template keys) stay in English.

---

## Flow

1. **Deep scan (read-only)** to understand the project's character:
   - `README.md`, `CLAUDE.md`, `AGENTS.md`, `docs/`, `docs/architecture.md`, `docs/PRD.md`, `docs/adr/`
   - `package.json` (name, description, deps — auth lib, UI lib, ORM, etc.)
   - `requirements.txt` / `pyproject.toml` for backend hints
   - Existing palette/font hints in `tailwind.config.*`, `theme.*`, `tokens.json`
   - `.claude/design-system.md` if exists — those decisions are LOCKED

2. **Detect project type** using `project-types.md` (the static catalog of types + their signals + their recommendations). Common types:
   - hacker / cybersec / dev-tool, SaaS app, e-commerce, portfolio, marketing site, dashboard / data, docs, content/blog, fintech, social/community
   - Pick the single best match. If ambiguous, list the top two and let the user confirm.
   - Show what was detected and on what evidence: `Detected: <type> — signals: <2–4 short bullets>`. The user can correct via the first question.

3. **Build a recommendation set from the type**: for each brand decision (mood, palette, typography, motion, voice, …), pull the type-specific recommended value from `project-types.md`. These appear as `(recommended)` in the AskUserQuestion options with a one-line WHY.

4. **Ask only what's missing** (LOCKED items skipped, ≤4 questions per `AskUserQuestion` call, recommended option always first and labeled). Round 1 is the most blocking 4; Round 2 is run only if essentials remain unresolved. Translate all strings to user language.

   Round 1 (max 4):
   - Project type (only if ambiguous; pre-checked recommendation visible)
   - Mood / character — recommendation comes from type
   - Default theme — recommendation from type (e.g. hacker → Dark; e-commerce → Light)
   - Primary palette direction — recommendation from type (e.g. hacker → terminal green mono; SaaS → indigo cool)

   Round 2 (only if still ambiguous):
   - Typography family direction — recommendation from type (mono for hacker, sans-serif geometric for SaaS, serif editorial for portfolio)
   - Motion intensity — recommendation from type
   - Voice / tone — recommendation from type
   - Special-effect call (e.g. matrix-rain for hacker, parallax for marketing) — recommendation; mark "off" by default unless type strongly implies it

   For anything unresolved beyond the asked rounds, apply the type's recommendation and mark `(auto)` in the output so the user can audit.

5. **Print a Claude Design prompt block** (fenced, copy-able) describing the brand. This is what the user pastes into Claude Design to generate brand visuals (mood board, type sample, palette swatches). Structure:

   ```markdown
   # <Project> — Brand Foundation

   ## Project & character

   - Type: <detected-type>
   - Audience: <from-readme>
   - Voice: <chosen voice>
   - Mood: <chosen mood>

   ## Palette

   - Primary: <hex>
   - Accent: <hex or "derive from primary">
   - Neutrals: <warm/cool slate scale>
   - Semantic: success / warning / danger / info (desaturated to fit mood)

   ## Typography

   - Heading: <font>
   - Body: <font>
   - Mono: <font>
   - Scale: 12 / 14 / 16 / 18 / 20 / 24 / 30 / 36

   ## Shape & motion

   - Radius character: <character>
   - Elevation: <flat/layered>
   - Motion intensity: <intensity>; durations 150 / 250 ms; ease-out entrance

   ## Special character

   <type-specific notes — e.g. "monospace-feel even in body, occasional terminal-style cursor blink on hero", "editorial pull-quotes with serif", "data-dense surfaces with chart-friendly palette">

   ## Accessibility

   WCAG AA, reduced-motion respected.
   ```

6. **Persist**:
   - `docs/design/BRAND.md` from `templates/BRAND.md.tmpl` (human-readable, prose).
   - `.claude/design-system.md` — create or update; this skill owns the `## Brand` section. Other sections (Logo, Pages, Landing) are owned by the prompter skill.
   - `CLAUDE.md` — inject (or update, marker-delimited, never duplicate) a "Design system" block pointing at `docs/design/` and `.claude/design-system.md`. If `CLAUDE.md` doesn't exist, create it with a header + the design block.
   - `docs/design/README.md` — index file; create or update entries.

7. **End with**:
   - Brand prompt block (above) for the user to paste into Claude Design.
   - One-line summary: "Brand done. Next: `/claude-design-prompter` to generate Logo / All-Pages / Landing — all will inherit these brand decisions."
   - If any `(auto)` defaults remain in BRAND.md (Quick mode was used or rounds were skipped), call them out explicitly: `> N decisions were filled from project-type defaults and marked (auto). Run /claude-design-prompter → Answer to confirm or override individual ones, or re-run /claude-design-brand to revisit.`

## Persistence rules

- `BRAND.md` is rendered from `templates/BRAND.md.tmpl`. Every value gets a real string; if the user didn't confirm and no recommendation applies, write `TBD` (never fabricate).
- `(auto)` suffix marks values defaulted from `project-types.md` without explicit confirmation. The downstream prompter modes propagate this flag (see prompter SKILL.md `(auto) propagation`).
- `.claude/design-system.md` — own ONLY the `## Brand` section. Do not touch `## Logo`, `## Pages.*`, `## Landing` (those are owned by prompter).
- `docs/design/README.md` — render from `templates/docs-readme.md.tmpl`. List every file currently in `docs/design/` (initially just `BRAND.md`).
- `CLAUDE.md` — render `templates/claude-md-section.md.tmpl` between the markers; create the file if missing. Idempotent.

---

## Safety

- Never overwrite `BRAND.md` without confirmation (offer merge / overwrite / skip).
- Never invent brand assets the user hasn't approved. Unknown values → `TBD`, never fabricate hex codes or font choices outside the recommendation set.
- Recommendations are opinions from `project-types.md` — always show WHY, never present as absolutes.
- Translate user-facing strings; keep internal keys English.

---

## Agent Usage

On invocation, the FIRST action is the deep scan + type detection (no AskUserQuestion yet — gather evidence first). Then present the detection in 2–4 lines and immediately move to Round 1 questions. No preamble like "let me scan the repo" — just do it and report findings together with the first question.

If `.claude/design-system.md` already has a `## Brand` section: ask once whether to "View existing / Update specific decisions / Re-run from scratch". Default to View.
