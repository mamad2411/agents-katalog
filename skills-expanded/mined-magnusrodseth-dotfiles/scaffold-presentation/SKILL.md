---
name: scaffold-presentation
description: Scaffold a new slide deck in the user's central presentations repo (~/dev/personal/presentations), sourcing content from the current code repo, the current conversation, or material in the Obsidian vault, and matching or creating a brand theme. Works from any directory. Use when the user says "make a presentation about X", "scaffold a deck", "turn this into slides", "lag en presentasjon om X", "create a talk from this repo/conversation", or wants to present something they have been working on.
---

# Scaffold Presentation

Create a new presentation in the central presentations repo. All decks live in **one** repo:

```
PRES="$HOME/dev/personal/presentations"
```

This skill is a thin orchestrator. The repo's `AGENTS.md` and project skills own narrative, layout, components, themes, and deployment. Gather the source material, then follow them.

## Workflow

### 1. Read the repo's instructions first

Read `$PRES/AGENTS.md` before anything else. It defines the route scaffold, the `presentations.ts` manifest, available themes, slide variants, and key rules (bun not npm, lucide-react not emojis, "Magnus Rødseth" with ø, Norwegian content by default, no scrolling within slides).

Then read `$PRES/.agents/skills/presentation-craft/SKILL.md` before outlining or coding. Follow its brief, evidence, composition, and revision workflow, including for requests to go straight to a first draft. Read it explicitly when invoked from another repo; do not rely on automatic skill discovery.

Other project skills live under `$PRES/.agents/skills/`:
- `presentation-theming`: full workflow for adding a new token-driven theme
- `brand-designer`: deriving a brand identity from scratch
- `<company>-brand-guidelines` (capra, reitan, multiconsult, eden-stack, wispr-flow, ...): existing brand systems
- `deploy-presentation`: shipping to Vercel

### 2. Gather content (pick the source the user implies)

**From the current code repo** (e.g. "make a deck about this project"):
- Read README, docs/, architecture notes, CONTEXT.md if present
- Skim recent git history for the narrative arc (what was built, in what order, what was hard)
- Note the project's brand signals: design tokens, Tailwind config, logo assets, existing brand guideline files

**From the current conversation** (e.g. "turn this into slides"):
- Distill the conversation into its load-bearing points: the problem, the journey, the insights, the punchlines
- Confirm the intended audience and duration with the user if not obvious

**From the vault** (e.g. "a talk about agentic coding from my notes"):
- Use the `read-up-on` skill's discovery approach against `$HOME/dev/personal/vault`: filename find + full-text grep (Norwegian and English variants), rank, read top notes
- Learnings, brags, and project notes are the richest slide material

Use `presentation-craft` to turn the material into an outline with a job, evidence, and transition for each slide. Let the story and speaking time determine the length. Show consequential gaps before coding; follow existing authorization to proceed.

### 3. Pick or create the brand theme

1. Check the themes table in `$PRES/AGENTS.md` and `$PRES/src/styles/themes/tokens/`. If the audience or company matches an existing theme (capra, gjensidige, reitan, anthropic, ...), reuse it.
2. If the deck needs a new brand (e.g. derived from the code repo's design system or a client's visual identity), follow the repo's `presentation-theming` skill: add the `Theme` union member, create the token file (single source of truth; OG palette, background palette, and contract CSS are derived), register it, add bespoke CSS and fonts only if needed.
3. When deriving a brand from a code repo: pull primary/accent colors, font choices, and logo from the repo's actual design tokens, not from memory.

### 4. Scaffold the deck

Follow the "Creating a New Presentation" section of `AGENTS.md` exactly:
1. `src/routes/presentations/<name>.tsx` with `ssr: false`, `head()` via `generateHead`, and a `slides` array passed to `<Deck>`
2. Register in `src/data/presentations.ts` (title, description, date, lang, theme)
3. Static assets to `public/presentations/<name>/assets/`
4. Content in Norwegian unless the audience is international

### 5. Verify

- `cd $PRES && bunx tsc --noEmit` must exit 0
- `bun run build` must exit 0
- Follow the repo's dev-server instructions; locate the running server's actual port
- Complete the visual and narrative review in `presentation-craft`. Report blocked checks and unresolved material gaps; distinguish a reviewable draft from a deck ready for delivery.

## Heuristics

- Don't duplicate `AGENTS.md` knowledge from memory; it changes, this skill doesn't. Always re-read it.
- Keep presentation preferences in the repo's `presentation-craft` skill; do not duplicate them here.
- Deployment is a separate, explicit step (`deploy-presentation` skill). Never deploy unless asked.
