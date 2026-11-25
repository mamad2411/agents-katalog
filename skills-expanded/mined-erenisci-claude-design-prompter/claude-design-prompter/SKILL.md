---
name: claude-design-prompter
description: DEPRECATED — use Acta (acta-design-prompt) at https://github.com/erenisci/acta. Using brand decisions established by /claude-design-brand, generate paste-ready Claude Design prompts (and persist files) for Logo, All-Pages (every detected app page in one doc), or Landing — and resolve Claude Design follow-up questions consistently. Trigger on /claude-design-prompter, "generate logo prompt", "generate all pages", "generate landing", "answer Claude Design question".
---

# Claude Design Prompter

The **second step** of the design pipeline. Reads the brand foundation produced by `/claude-design-brand` and turns it into focused, paste-ready prompts for specific surfaces — plus answers Claude Design's follow-ups consistently with stored decisions.

Four modes: **Logo**, **All-Pages**, **Landing**, **Answer**.

---

## Pre-condition

Before any mode runs, check for `docs/design/BRAND.md` AND a `## Brand` section in `.claude/design-system.md`. If missing or empty:

```
"Brand foundation hasn't been set up yet. Run /claude-design-brand first — it scans
the repo, detects what kind of project this is, and produces the brand decisions
that every other artifact (logo, pages, landing) will inherit. Want me to suggest
running it now?"
```

Don't proceed with any mode until brand exists. The whole point of this skill is consistency — no foundation, no consistent output.

---

## Localization

Translate user-facing strings to the user's current conversation language. Internal keys (file names, frontmatter, template placeholders) stay English.

---

## Agent Usage — dispatcher

On invocation without explicit mode, the FIRST action is a single `AskUserQuestion` (after the BRAND pre-condition check). No preamble. Translate strings to user language. Canonical English:

```
question: "Claude Design Prompter — which mode?"
header:   "Mode"
multiSelect: false
options:
  1. label: "Logo — generate logo prompt + LOGO.md"
     description: "Reads BRAND.md, asks ≤4 logo-specific questions (construction, feel, color treatment, variants) with brand-aware recommendations, prints a Claude Design prompt block, writes docs/design/LOGO.md."
  2. label: "All-Pages — every app page (landing excluded)"
     description: "Detects pages from app/, pages/, src/routes/, README. For each page asks ≤4 questions (content type, density, primary action, states) with brand-aware recommendations. Prints one Claude Design prompt block per page, writes docs/design/ALL-PAGES.md (one document, sectioned by page)."
  3. label: "Landing — composite landing page"
     description: "Reads BRAND.md, asks ≤4 questions about goal / hero treatment / sections / interactivity. Prints one composite Claude Design prompt block (navbar + hero + sections + cta + footer in one), writes docs/design/LANDING.md."
  4. label: "Answer — resolve a Claude Design follow-up"
     description: "Paste the question Claude Design asked you (text or screenshot — Win+Shift+S works). The skill checks BRAND.md + existing prompter outputs and proposes a consistent answer; new answers can be recorded back."
```

On direct invocation with explicit mode arg (`logo`, `all-pages`, `landing`, `answer`): skip the dispatcher, go straight in (still run the BRAND pre-condition check).

---

## Mode 1: Logo

Loads `targets/logo.md`. Brand-aware: pulls primary color, mood, voice from BRAND.md. Recommendations in questions reflect brand character (e.g. brand mood "industrial" → recommendation favors mark-only or monogram, sharp construction; brand mood "editorial" → wordmark recommendation).

Output: `docs/design/LOGO.md` + `## Logo` section in `.claude/design-system.md` + paste-ready prompt block.

---

## Mode 2: All-Pages

**Page discovery** (this is where the system stops being static):

1. Enumerate routes from filesystem:
   - `app/`, `pages/`, `src/app/`, `src/pages/`, `src/routes/`, `routes/`, `app/routes/`
   - Each top-level route directory or file is a candidate page key (kebab-case)
   - Nested routes become `parent/child` keys (e.g. `admin/users`)
2. Add pages mentioned in README "Pages" / "Screens" / "Features" / "Routes" sections.
3. Add pages implied by the backend API surface (e.g. `/api/billing` → `billing` page candidate).
4. Build `pages_detected[]`. Show the user the list and ask:
   - "Generate prompts for all <N> pages with brand-aware defaults? [Yes / Customize the list]"
5. If Customize: show the list as a multi-select pre-checked, with an "Add another" free-text option.

For each chosen page, load `targets/all-pages.md` for the question flow + per-page prompt block format.

Output: a single `docs/design/ALL-PAGES.md` with one section per page. Each section contains:

- One-line goal
- Per-page Claude Design prompt block (fenced)

Also append `## Pages.<key>` summaries to `.claude/design-system.md`.

---

## Mode 3: Landing

Loads `targets/landing.md`. Composite: navbar + hero + sections + cta + footer in ONE landing prompt — not split, because Claude Design produces a coherent landing better when given the whole thing.

Brand-aware: recommendations reflect detected project type (e.g. SaaS landing recommends "social proof early"; portfolio landing recommends "big type hero, low-volume CTA").

Output: `docs/design/LANDING.md` + `## Landing` section in `.claude/design-system.md` + paste-ready prompt block.

---

## Mode 4: Answer

Loads `targets/answer.md` for the full flow including multi-question screenshot batching and brand-aware option generation. Summary:

1. User pastes input — text or screenshot (Win+Shift+S since Claude Design buttons aren't selectable). If invoked without input, ask for it before anything else.
2. Match the question against `claude-design-questions.md`.
3. Read `.claude/design-system.md` (brand + per-mode sections). If a decision exists, propose it directly with one-line justification: `BRAND.md sets motion=subtle (industrial mood, terminal feel — fits this project type)`.
4. If no decision exists, present 2–3 brand-aware options via `AskUserQuestion`. After the user picks, ask whether to record it. If yes, edit the relevant doc (`BRAND.md` or per-mode doc) AND `.claude/design-system.md`.
5. If the question doesn't match any catalog pattern, append a new entry to `claude-design-questions.md`.

---

## Persistence rules (every mode that writes a file MUST do these)

After Logo / All-Pages / Landing modes write their `docs/design/<NAME>.md`:

1. **Update `docs/design/README.md`** — render `templates/docs-readme.md.tmpl` from scratch using the current set of files in `docs/design/`. The `{{OPTIONAL_FILES}}` placeholder lists every file present in the folder right now (excluding `README.md` itself), with a one-line description per file. This is regenerated, not appended — keeps the index in lock-step with reality.

2. **Update `CLAUDE.md` design-system block** — read the block between `<!-- design-system:start -->` and `<!-- design-system:end -->`. Replace it with a freshly rendered `templates/claude-md-section.md.tmpl`. If the file or block doesn't exist, create it (block at end of file; create file with a top-level heading if missing). Idempotent: same content always produces the same block.

3. **Update `.claude/design-system.md`** — append or replace the section for this mode (`## Logo` / `## Pages.<key>` / `## Landing`). Other sections are left untouched.

Never duplicate any of these blocks. Never delete content owned by other sections.

## (auto) propagation

When reading `BRAND.md`, scan for any value followed by `(auto)` — these were defaulted in Quick mode without user confirmation. When generating downstream prompts (Logo / All-Pages / Landing) the agent MUST:

- Surface `(auto)` markers in the printed prompt block's `Assumptions` or footer section so the user knows which inherited brand decisions are unconfirmed.
- Flag in the per-mode doc's "Notes" section: `> Inherited from BRAND.md with (auto) defaults: <list>. Run /claude-design-prompter → Answer or re-run /claude-design-brand to lock these.`
- Never _propagate_ `(auto)` further as a fact in other docs — it stays a flagged assumption until the user confirms.

## Safety

- Never run any mode if BRAND.md is missing — point user at `/claude-design-brand`.
- Never overwrite existing per-mode docs without confirmation (merge / overwrite / skip).
- Never invent decisions outside what's recorded or what the user just confirmed.
