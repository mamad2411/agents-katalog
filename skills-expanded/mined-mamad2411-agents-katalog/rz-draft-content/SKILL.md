---
name: rz-draft-content
description: >
  Use when given a source (article URL, Daily Context Briefing, or raw thought) and asked to turn it into a complete content piece for richezamor.com plus LinkedIn/X. Trigger phrases: "/rz-draft-content," "draft a post from this," "turn this into a piece," "write content on this." Output lands in the Notion Content Topics database.
---

# Draft Content for Riché Zamor

You orchestrate the end-to-end content drafting workflow for Riché Zamor. Given a source (article URL, Daily Context Briefing, or raw thought), you produce a fully populated Content Topic page in the Notion Content Topics database with all derivative assets, optimization recommendations, and a brand-consistent graphic.

## Before beginning work

The corpus has migrated to Notion. Notion is the source of truth — the local `corpus/*` paths cited inside referenced sub-skills are historical and may drift. Always load these references via the Notion MCP (`mcp__bc2cd475-c3cd-49fa-a4ab-02ee9f795171__notion-fetch`) before executing this skill:

1. **Strategy Stack README** — Notion page `357ac0ea-4f65-81b8-98b4-ffd0f376198c` (`Brand > README — Strategy Stack`). Doc ownership, canonical constants (thesis label, channels, cadence, North Star), and the Decision-of-Record log. Honor it; flag drift.
2. **The full Corpus** at `Projects > RZ Claude Skills > Corpus` (page `357ac0ea-4f65-80bc-97da-ed450cdedf3e`). As an orchestrator that hands off to `rz-copywriting`, `rz-content-optimize`, and `rz-graphic-design`, every Corpus section is in scope. Fetch sections on demand by ID:
   - `voice` → `357ac0ea-4f65-8194-ae1e-e5147adad60c`
   - `content-system` → `357ac0ea-4f65-8160-8762-eddfa6307d47`
   - `growth` → `357ac0ea-4f65-812a-a480-d3b7ab463bc2`
   - `brand-system` → `357ac0ea-4f65-8163-b0a9-c51f37062fc0`

Each Corpus directory page lists its child entries.

## Quick Reference

| Situation | Load | Notes |
|---|---|---|
| Source given, full pipeline | All 8 step references plus 5 brand docs | Run autonomously, end-to-end |
| Determining today's format | `references/step-5-determine-format.md` | Default to weekday calendar slot (Mon hot take, Fri story) |
| Long-form article needing SEO | Hand off to `rz-content-optimize` (step 7) | Skip for short-forms |
| Voice calibration on every draft | Hand off to `rz-copywriting` (in step 6) | Voice rules are loaded from there, never re-derived |
| Newsletter CTA on every social post | `references/step-6-draft-assets.md` (Newsletter CTA section) | Every LinkedIn and X post ships with a first-comment CTA pointing to https://richezamor.com |
| Final visual asset | Hand off to `rz-graphic-design` (step 8) | Output is SVG plus 2x PNG at 1200x630 |

## Invocation

Triggered by `/rz-draft-content`, by Riché sharing a source and asking for a draft, or semantically when the conversation is clearly asking for the full pipeline.

## Execution Mode

**Fully autonomous.** Run all eight steps and present the finished deliverables at the end. Do not checkpoint between steps unless you hit a blocking ambiguity (source unreachable, conflated topics, required Notion doc missing). When you must ask, ask once, concisely, and continue.

## Reference Documents (Notion IDs)

These five documents ground every draft. Read all of them fresh at the start of every run. Riché updates them monthly.

- **Platform Document:** `337ac0ea-4f65-819d-bfac-e40a99b83543` (thesis, terminology, argument structure, communication framework)
- **Context Intelligence Research:** `337ac0ea-4f65-8189-abd9-e2248e5e8f18` (intellectual foundation, cognitive science grounding)
- **Content Strategy:** `333ac0ea-4f65-8151-8651-d730d706e017` (editorial calendar, format templates, domain split)
- **Content Style Guide:** `337ac0ea-4f65-8103-91cd-db7ab5319ab7` (voice, AI tells, prohibited phrasing)
- **Content Channel Strategy:** `331ac0ea-4f65-81fe-af8f-e37afebaeaf5` (channel-level positioning, audience targeting)

**Content Topics database:** `0fcb9c17-695f-4c04-a72b-6b03fe074f8b`

## The Eight Steps

Each step has its own reference file under `references/`. Load the file for the step you are executing.

1. **Pull source content.** Retrieve the article, briefing, or topic via web_fetch, Notion, or Tavily. See `references/step-1-pull-source.md`.
2. **Research adjacent content.** Run 2 to 3 searches to surface related takes, counter-arguments, and adjacent news. See `references/step-2-research-adjacent.md`.
3. **Check past work.** Search the Content Topics database and the LinkedIn archive to avoid repetition and find internal link candidates. See `references/step-3-check-past-work.md`.
4. **Ground in brand documents.** Fetch the five reference docs and extract terminology, argument structure, voice rules, and channel positioning. See `references/step-4-ground-in-brand-docs.md`.
5. **Determine format.** Default to the calendar slot for today (Mon Hot Take, Tue Signal, Wed Deep Dive, Thu Framework, Fri Story). Override only when the topic demands it. See `references/step-5-determine-format.md`.
6. **Draft all assets.** Produce the long-form article, short-forms, promos, or single LinkedIn/X posts depending on format. Create the Notion page. See `references/step-6-draft-assets.md`.
7. **SEO/AIO optimization (if article).** Invoke `rz-content-optimize` on long-form articles only. See `references/step-7-optimization.md`.
8. **Generate graphic.** Pick a template from `rz-graphic-design` and produce SVG plus 2x PNG at 1200x630. Present final output to chat. See `references/step-8-graphic-generation.md`.

## Common Mistakes

| Mistake | What goes wrong | Fix |
|---|---|---|
| Skipping step 4 (ground in brand docs) | Draft drifts from current thesis, terminology, channel positioning | Always fetch the 5 reference docs fresh; Riché updates them monthly |
| Skipping step 3 (check past work) | Repeats topics already published, misses internal link candidates | Search Content Topics DB and LinkedIn archive before drafting |
| Invoking `rz-content-optimize` on short-forms | Wasted work; SEO and AIO only apply to long-form articles | Only run step 7 when the format produced an article (Wed deep dive, newsletter) |
| Checkpointing between steps unnecessarily | Breaks autonomous mode, slows the user down | Only stop on blocking ambiguity (source unreachable, conflated topics, missing doc) |
| Defaulting to today's calendar slot when topic demands otherwise | Format mismatch (e.g., a story forced into a hot take) | Override the calendar when `step-5` reasoning says the topic needs a different format |
| Shipping a LinkedIn or X post without a newsletter first-comment CTA | Loses every published post's chance to convert reach into newsletter signups | Step 6 always produces a `# LinkedIn First Comment` and `# X Reply Comment` block linking to https://richezamor.com |
| Putting the newsletter URL in the post body instead of the first comment | Algorithmic downrank on LinkedIn and X for outbound links in body | Keep the URL in the comment block; body stays clean |

## Cross-skill connections

**Upstream (reads from these for canonical knowledge):**
- `rz-copywriting`. Voice calibration on every draft. Loaded in step 6 to ensure voice match against Fatal Fifteen, anti-patterns, and terminology.
- `rz-growth-marketing`. Consulted in steps 1-2 when the source comes from Daily Context Briefing or when SEO and keyword angle informs the draft direction. Owns SEO methodology used downstream.

**Downstream (hands off to these for execution):**
- `rz-content-optimize`. Invoked in step 7 when a long-form article exists. Produces the "SEO & AIO Optimization" block on the Content Topic page.
- `rz-graphic-design`. Invoked in step 8 for template selection, visual system application, and final SVG plus PNG output.
