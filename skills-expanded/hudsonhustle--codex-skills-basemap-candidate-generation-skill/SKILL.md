---
name: basemap-candidate-generation
description: Use when creating or revising Hudson Hustle city basemap candidates from map config, protected zones, city recipes, AI reference art, or future NYC/Berlin backdrop workflows.
---

# Basemap Candidate Generation

Use this when the work is about repeatable backdrop generation, not one-off visual tuning.

## Goal
Generate a quiet vector basemap candidate that sits between the board surface and gameplay routes/stations/labels.
Routes, stations, and labels are protected; the basemap supports place memory without becoming playable information.

## Inputs
- Config map folder or id: `map.json` supplies board size, active stations, route geometry, labels, and waypoints.
- Protected zones: pass a JSON file when available, otherwise derive them from the config map.
- City recipe: reusable local knowledge for land/water shapes, region labels, landmarks, theme traces, and AI-reference intent.

## Command
```bash
pnpm config:basemap-candidate \
  --config v0.4-flushing-newark-airport \
  --recipe configs/hudson-hustle/basemap-recipes/nyc-harbor-memory-v1.json \
  --out /tmp/nyc-basemap-candidate.json
```

Optional:
```bash
pnpm config:basemap-candidate --config <id-or-folder> --recipe <recipe.json> --protected-zones <zones.json> --out <candidate.json>
```

## Recipe Rules
- Use `coordinates: "normalized"` for reusable city recipes; use `coordinates: "board"` only for final hand-tuned output.
- Keep recipe geometry 神似, not GIS-exact.
- Put broad land/water memory in `landAreas`, `waterAreas`, and `shorelines`.
- Put local flavor in `landmarks` and `themeLines`.
- Default landmarks and theme lines must avoid protected zones; set `avoidProtectedZones: false` only when the feature is intentionally under gameplay and visually quiet.
- Use low opacities. The route graph must still read if the candidate is shown at real play size.

## Workflow
1. Verify the config id or folder with `pnpm config:preview <config-id>`.
2. Draft or update a city recipe under `configs/hudson-hustle/basemap-recipes/`.
3. Generate to `/tmp` first.
4. Review the candidate JSON against protected-zone omissions in `generatedBy.notes`.
5. Paste or merge the candidate into `visuals.json` only after visual approval.
6. Run `pnpm --filter @hudson-hustle/game-core test -- game.test.ts`, `pnpm config:preview <config-id>`, and `pnpm build`.

## Acceptance
- Candidate output is vector-only: land areas, water areas, shorelines, region labels, landmarks, and theme lines.
- It does not require changing `current.json`.
- It keeps gameplay on top and avoids route/label confusion.
- City-specific recipes can be reused for Berlin and future maps without changing the generator.
