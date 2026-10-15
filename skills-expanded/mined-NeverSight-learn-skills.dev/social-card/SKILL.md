---
name: social-card
description: Use when generating fixed-size editorial social cards (Rednote/Xiaohongshu-style 1080×1440 portrait) from a source article, brief, or topic. Owns intake, story planning, visual stance, layout selection, image strategy, and review. Renders, edits, comments, and exports happen in OpenPress — do not reimplement those.
---

# Social Card Skill

A fixed-layout social-card generation workflow that targets OpenPress as the application layer.
This skill brings **creative decisions**; OpenPress brings the **substrate**.

## Two-layer split

| This skill owns | OpenPress owns |
| --- | --- |
| Intake, target-platform choice, source-material handling | Fixed page geometry, Press Tree runtime |
| Story plan, layout selection, visual stance (Editorial / Swiss) | Dev server, workbench, inline edit, comment markers |
| Image / source strategy, provenance | Source-backed MDX/TSX workspace, search, replace |
| Per-domain validation rules (overflow / density / readability) | PDF / web export, validation primitives |
| Taste calls | Agent-facing commands (`apply-comment`, `create-document`, `create-theme`, …) |

**Never reimplement OpenPress substrate from this skill.** If the workbench, dev server, or marker
pipeline does not cover something, report it back (see `NOTES.md`) — do not patch the framework
from a skill.

## What this skill doesn't do

The skill does not implement rendering, preview serving, PNG export, or validation runtime.

Use OpenPress commands for:

- workspace init
- dev preview
- build / render
- validation
- PNG / PDF / image export

If the installed OpenPress version does not provide the needed command, **stop and report the
missing OpenPress substrate capability**. Do not create a skill-local renderer or Playwright
export script. That stance is non-negotiable — it's the only way the two-layer split stays real.

## First-slice scope (v1)

- **Target:** editorial portrait cards at **1080×1440 (3:4)**, matching the original
  guizang/Rednote visual baseline.
- **Recipes:** 11 OpenPress-native magazine layouts — `EditorialCover`, `FieldNotePhoto`,
  `EditorialNoteRows`, `EditorialEssaySplit`, `PullQuote`, `EvidenceWall`, `ClosingLedger`,
  `TallLedger`, `EvidenceFeature`, `MarginaliaEssay`, `SectionDivider`. Plus `SwissStatement`
  as the alternate Swiss-mode primitive. See `references/layout-recipes.md`.
- **Page chrome:** `PageChrome` fixes issue-strip headers / footers outside the recipe content
  flow. Use it around cards that need stable top / bottom metadata; don't let individual recipes
  push the footer down.
- **Themes:** 6 Editorial palettes (Ink Classic default, Indigo Porcelain, Forest Ink, Kraft
  Paper, Dune, Midnight Ink) + 2 Swiss palettes (IKB Blue, Cinnabar). See
  `references/theme-presets.md`.
- **Visual identity:** structured rules in `references/validator-rules.md` ready to register
  with `openpress validate` when the hook ships. Until then, the rules are agent-readable QA
  guidance (see `references/qa-checklist.md`).
- **Export, validation, preview:** owned by OpenPress (current or expected). The skill does not
  ship its own runtime for any of these.
- **Deferred to v2:** square 1080×1080, 4:5 feed 1080×1350, Facebook link-preview 1200×630, per-frame
  geometry for mixed-ratio carousels. Three upstream guizang recipes (M05 / M09 / M13) are
  absorbed by existing components rather than deferred — see `references/visual-grammar.md`
  § Absorbed by existing recipes.

## Workflow

A typical flow looks like this. **Intake comes first** because skill quality depends on
understanding the user — that one is load-bearing. Everything after can be re-sequenced when the
context calls for it.

### 1. Intake

Ask once, in one message:

1. **Target platform(s)** — v1 defaults to 1080×1440 editorial portrait. Square, 4:5 feed,
   and FB link-preview variants are deferred to v2.
2. **Source material** — paste text, link, or attached file. If only a topic is given, ask whether
   to research first or to brainstorm a draft together.
3. **Image availability** — does the user have photos / screenshots / brand assets, or should the
   skill source images?
4. **Visual stance preference** — Editorial (calm, paper-like, serif-leaning) or Swiss (graphic,
   chunky type, geometric). If the user has no preference, recommend based on content tone.
5. **Constraints** — language, brand colors, hard text the user wants kept verbatim.

Do not generate anything before all five are answered.

### 2. Evidence gate

If a page needs visual evidence and the user supplied no images, ask **once**:

> "I need images for the evidence pages. Want me to:
> (a) use media you'll attach,
> (b) source images from the web (I'll record provenance), or
> (c) generate images (raw visuals only, no embedded text)?"

Apply the user's choice for the whole project. Do not mix without asking again.

For web-sourced images, always record source URL + license status in
`press/media/SOURCES.md` before using them.

### 3. Story plan

Produce a page-by-page plan **before** touching the workspace. Match each page to one recipe
from `references/layout-recipes.md`. Keep it short:

```
Page 1  cover       EditorialCover     title + subtitle + image + issue strip
Page 2  field note  FieldNotePhoto     documentary image + takeaway + caption
Page 3  notes       EditorialNoteRows   title + 3 horizontal observations
Page 4  ledger      TallLedger         4-6 detailed rows
Page 5  closing     ClosingLedger      summary ledger + closing quote
```

Show the plan to the user. Iterate the plan, not the rendered cards.

### 4. Style choice

After the plan is approved, lock **one visual stance + one theme** for the whole carousel.

- **Stance**: Editorial (default) or Swiss. Don't mix per page.
- **Theme**: pick one of the 6 Editorial palettes (Ink Classic / Indigo Porcelain / Forest Ink
  / Kraft Paper / Dune / Midnight Ink) or one of the 2 Swiss palettes (IKB Blue / Cinnabar).
  See `references/theme-presets.md` for which palette fits which content tone.

Apply via `data-theme="..."` on the `<Workspace>` or a parent wrapper. Tokens live in
`press/theme/tokens.css`; for a brand-specific palette, override the seven palette tokens there
rather than pasting inline styles into cards.

### 5. Workspace operation

This skill **does not** ask the agent to hand-write standalone HTML. It also **does not** rely on
OpenPress to fetch the starter — this skill owns its starter and is responsible for getting it
into the workspace. OpenPress only initializes a blank runtime workspace; populating it is the
skill's job.

Bootstrap flow:

```bash
# 1. Init a blank OpenPress workspace. No --pack. OpenPress only sets up the runtime.
npx @open-press/cli@next init my-cards
cd my-cards

# 2. Resolve this skill's installed location. Path differs by harness
#    and by whether `skills add` installed into the current workspace.
for candidate in \
  "$PWD/.agents/skills/social-card" \
  "$HOME/.agents/skills/social-card" \
  "${CODEX_HOME:-$HOME/.codex}/skills/social-card" \
  "$HOME/.claude/skills/social-card"
do
  if [ -d "$candidate/starter/press" ]; then
    SOCIAL_CARD_SKILL_DIR="$candidate"
    break
  fi
done

if [ -z "${SOCIAL_CARD_SKILL_DIR:-}" ]; then
  echo "social-card skill starter not found" >&2
  exit 1
fi

# 3. Replace the default press/ with this skill's starter.
rm -rf press
cp -R "$SOCIAL_CARD_SKILL_DIR/starter/press" press

# 4. Boot the workbench.
npm run dev
```

Notes for the agent at this step:

- `openpress init --pack …` is not how this works. OpenPress doesn't fetch external skill starters.
- The installed skill directory (`$SOCIAL_CARD_SKILL_DIR`) is the source of truth for
  `starter/` and `references/`.
- After the starter is copied in, the workspace belongs to the user — edit it like any other code.

**If the starter doesn't run on the current OpenPress version**, that's expected — frameworks
evolve. The starter is a worked example calibrated for the OpenPress version this skill was last
validated against (see the `Compatibility` note in `README.md` if present, otherwise treat the
starter as illustrative). When the starter and the installed `@open-press/core` disagree:

1. Read https://open-press.dev/docs and the installed `@open-press/core` type definitions.
2. Make the smallest migration that preserves the skill's intent — 1080×1440 editorial
   portrait cards, MDX-driven, Editorial / Swiss visual systems, source-backed and editable.
3. Then continue with the workflow.

Don't wait for a `MIGRATIONS.md` recipe — there isn't one. The starter is a starting point, not
a contract.

Typical edit targets, roughly in order of impact:

- `press/cards/<page>/content/<page>.mdx` — copy text. Each card is one MDX file. Layout
  components are referenced by name; OpenPress auto-discovers them from `press/components/`, so
  MDX files don't need imports.
- `press/theme/tokens.css` — brand colors, type, padding.
- `press/components/*.tsx` — flat directory of auto-discovered components. Add a new one when
  an existing layout doesn't express the page.
- `press/media/` — drop images here; web-sourced images go through `SOURCES.md` first.

### 6. Review

Show the user the workbench (`npm run dev`) or rendered PNGs first. Never describe the cards in
words and call it done — render and screenshot.

Comments use OpenPress's `@openpress-comment` markers. The user marks; the agent applies via the
OpenPress `apply-comment` skill. Do not invent a separate comment flow.

### 7. Validation

Use OpenPress's own validation when the user asks for auto-check (e.g. `openpress validate` /
`openpress inspect` once those ship, or `npm run build` for the basic compile / overflow check
that's available today). Visual review remains essential regardless.

**If the installed OpenPress version doesn't have a validate command yet**, stop and report it
as a missing substrate capability — don't build a skill-local validator to fill the gap.
This is the same principle as PNG export: skills don't shadow-implement substrate. False-green
validators are worse than no validator.

### 8. Iteration

Iterate by editing the **MDX source / theme tokens / layout components** and re-exporting.
Never patch the rendered PNG by hand.

## Hard rules

These are the lines that define the skill. Violating one means the skill failed, not that the
agent made a tradeoff.

- **Don't fake current facts, metrics, prices, or release details.** If a number could be wrong,
  browse and cite before using it.
- **Don't use web images without recording provenance.** `press/media/SOURCES.md` is the
  ledger — entries before references.
- **Don't deliver a standalone HTML file.** The deliverable lives inside an OpenPress workspace
  with source-backed cards. Bypassing the workspace is bypassing the whole skill.
- **Don't skip intake.** Without intake the skill collapses into a generic prompt.

## Strong defaults

Production-quality guidelines. Break them only when the user explicitly asks.

- Don't crop faces, key UI text, or product details — increase image area instead.
- Don't solve overflow by shrinking text below the floors in `references/qa-checklist.md`.
- Don't mix Editorial and Swiss in one carousel.
- Don't embed visible "instructions to the agent" inside the image — the card is the deliverable,
  not a how-to.

## References (load on demand)

- `references/background-systems.md` — the layered atmosphere model (paper grain + paper wash +
  optional ink-wash), per-theme overrides, RGB-triplet token contract, why WebGL was excluded.
- `references/visual-grammar.md` — the magazine vocabulary the skill ports, what was deliberately
  not ported (WebGL, PNG runtime, validator runtime), and the M-series semantic name map.
- `references/platform-specs.md` — per-platform pixel sizes, safe areas, density expectations.
- `references/style-system.md` — Editorial vs Swiss: tokens, type pairings, identity tests,
  anti-patterns. Quick-reference for mode selection.
- `references/theme-presets.md` — 6 Editorial + 2 Swiss palettes with full token values.
- `references/layout-recipes.md` — the 6 v1 recipes and what content shape each one expects.
- `references/validator-rules.md` — structured rule specs (identity, density, type floors,
  provenance) ready to register with `openpress validate` when the hook ships.
- `references/qa-checklist.md` — visual / typography / image / provenance / identity-test
  checklist for delivery review.

## OpenPress commands the skill relies on

All runtime — init, preview, build, validation, export — is owned by OpenPress. The skill
itself does not ship any of these. If a needed command isn't present in the installed OpenPress
version, **stop and report a substrate gap**; don't ship a skill-local replacement.

| Command | Status | Purpose |
| --- | --- | --- |
| `npx @open-press/cli@next init` | available | Create a blank runtime workspace. No `--pack`. |
| `npm run dev` (= `openpress preview`) | available | Workbench preview |
| `npm run build` (= `openpress build`) | available | Render to `dist-react/` |
| `npm run openpress:pdf` | available | PDF output |
| `openpress export png --out output/png` | **expected, not yet shipped** | PNG export per `.reader-page` at real pixel dimensions |
| `openpress validate` / `openpress inspect` | **expected, not yet shipped** | Overflow / small-type / density / provenance checks |
| `apply-comment` skill | available | Apply user's `@openpress-comment` markers |

When the agent finds an "expected" command isn't actually available, the correct response is to
**stop, tell the user what's missing, and treat it as a substrate gap to report back via
`NOTES.md`**. Building a skill-local Playwright renderer or validator is explicitly the wrong
answer.
