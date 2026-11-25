---
name: resync-map
description: Resync Ork's interaction map (docs/interaction-map) with the code — review what changed since the last sync, flip statuses that are now built, update facts, doc links, new components and journeys, record the synced commit, validate, and look at it. Use when asked to resync, update or refresh the interaction map, or after a milestone lands.
---

# Resync the interaction map

You are bringing every map in `docs/interaction-map/public/js/data/` up to date
with the code in this repository. Read `docs/interaction-map/sync.md` and
`docs/interaction-map/content-style.md` first; follow `sync.md` step by step.

Arguments (optional): a map id to limit the sync to (`architecture`,
`lifecycle`, `context`, `messaging`, `feedback`).

## Procedure

1. **Baseline.** Run `pnpm map:check` and keep its output: the commits since
   the sync, the uncommitted changes, and "Review these statuses" are your
   worklist. If nothing changed, say so and stop.

2. **Triage.** Group the changes by the map they touch, using the table in
   `sync.md` §2. Skip dependency bumps and tooling chores that change nothing a
   map shows.

3. **Review each change against the code**, not the commit message: read the
   diff, the code and its tests. `built` means on `main` with tests; a field the
   schema accepts but nothing reads is `partial`; a design section alone is
   `specified`.

4. **Update the data** (`nodes.js`, `edges.js`, `journeys.js`): statuses on
   nodes, their edges and journey steps; summaries and facts; doc links to the
   code and tests; `src` paths; new nodes on the zone grid with their edges and
   steps; `see` links both ways. Keep cards on the grid described in
   `design-language.md#layout`, and subtitles within ~30 characters. Never put
   secrets in the data.

5. **Record the sync** in `public/js/data/sources.js`: `synced` = the short
   hash you reviewed; `SYNCED_ON` = today (YYYY-MM-DD).

6. **Validate.** `pnpm map:check` must end with `✓ Data and links are
   consistent.` Then `pnpm map` and, if a browser tool is available, open each
   touched map: fit (`0`), select a few changed cards, play a changed journey,
   toggle dark (`T`), and check the console has no errors. Fix overlaps,
   edges that cross cards, and cut-off subtitles.

7. **Update docs** if the procedure, the maps or the data model changed
   (`maps.md`, `README.md`, `AGENTS.md`).

8. **Commit** only if the user asked for one:
   `Sync the interaction map to <sha>`, with a body listing per map what
   changed.

## Report

End with a short summary: the commit range reviewed, per map what changed
(status flips, new components and journeys), anything ambiguous you decided,
and anything you could not verify.
