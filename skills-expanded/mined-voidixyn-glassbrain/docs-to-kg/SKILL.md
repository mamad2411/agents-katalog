---
name: docs-to-kg
description: "Turn a product's docs (and the product itself, when you can read it) into a graph of its features written as user stories, in four snapshots: enumerated → merged → stories → linked. Use when someone wants to see what a product does, check docs against the product, or plan tests from them."
---

# docs-to-kg

Write four snapshots of plain glassbrain JSON (`{ "nodes": [...], "edges": [...] }`, structure by `parent`):

```
kg/1-enumerated/graph.json   every feature each source mentions, names only
kg/2-merged/graph.json       duplicates merged, renamed, grouped into areas
kg/3-stories/graph.json      each feature written as a user story
kg/4-linked/graph.json       what each feature needs and acts on
kg/_profile.json             colors and layers (template at the end)
```

Each step starts from a copy of the previous snapshot; never edit an earlier one. After each step run
`npx glassbrain validate kg --strict` and fix what it reports, then
`npx glassbrain diff kg/<previous> kg/<current>` and check the step did only its job (below).

## What a feature is

One thing a user can do and see the result of: "Share a board", "Filter cards by label". Not a
screen, not a setting's name, not a paragraph. Label: a short verb phrase in the user's words.
Ids: `f:<area>/<slug>` once areas exist, stable from then on.

## 1. Enumerate: two passes that do not see each other

Be exhaustive: every action a user can take, small ones too (sort, collapse, toggle). Merging is
the next step's job.

- **Docs pass.** Read every page. One node per feature, `kind: "feature"`,
  `source: "<file>#<heading>"`, `found_in: ["docs"]`, no description, `"flags": ["stub"]`.
- **Product pass.** Read the product itself: the running app, or its UI code (routes, screens,
  dialogs, buttons, menu items, translation strings). Same node shape, `source` = the route or file,
  `found_in: ["app"]`.

Run the passes in separate sub-agents if you can; if not, finish and save the docs pass before
opening the product. A pass that has seen the other one stops finding what the other one missed,
and those gaps are the point of doing two. Put the two lists under two top nodes `from-docs` and
`from-app` (`kind: "source"`), ids `d:<slug>` and `a:<slug>`.

## 2. Merge

- **Areas.** 5–9 product areas by what the user is doing, not by doc page (`kind: "area"`, id
  `area:<slug>`). Every feature moves under one; a feature that only exists inside another
  (editing a card's due date inside the card) may go under that feature instead.
- **Duplicates.** Same user action from both passes → one node. Keep one of the two ids, drop the
  other, and set `found_in: ["docs", "app"]` and both sources.
- **Rename.** Labels become one consistent style; keep ids.
- Keep single-source features. Docs-only may be stale; app-only is undocumented. Both are findings.
- `from-docs` and `from-app` go away.

Diff check: added = the areas only; removed = the dropped duplicates and the two source nodes;
moved = features into areas (a renamed feature shows as moved too). No new features.

## 3. Stories

For each feature, remove the `stub` flag and add:

| Field | |
|---|---|
| `role` | who does it (`member`, `project manager`, `admin`…) |
| `description` | markdown: **As a** role, **I want** goal, **so that** benefit. Then `Steps` (numbered, real UI words: menus, buttons), `Expected` (what the user sees), `Preconditions` if any |

Write from the source, in its terms. If the docs and the app disagree, say so in one line and
keep both. No new structure. Diff check: only `~ changed`.

## 4. Link

- **Concepts.** The nouns features act on (board, card, label, member…) as a tree under one node
  `concepts` (`kind: "concept"` for each). Only nouns the product manipulates.
- **Edges.**
  - `requires`: feature → feature, when it cannot be done before the other has been done (a card needs a list, which needs a board).
  - `acts-on`: feature → concept.
  - `conflicts`: feature ↔ feature, only when doing one undoes or blocks the other.

  Only edges a reader would agree with; few and certain beats many and guessed.

Diff check: concept nodes added, edges added, nothing else.

## `kg/_profile.json`

```json
{ "layers": [{ "id": "feature", "label": "Features", "structural": true }, { "id": "concept", "label": "Concepts", "structural": true }],
  "nodePalette": { "feature": "#e63b7a", "concept": "#0891b2" },
  "edgePalette": { "requires": "#e63b7a", "acts-on": "#53d5fd", "conflicts": "#ff6a00" },
  "placeholderFlags": ["stub"],
  "detail": { "line": [{ "key": "role", "label": "ROLE" }, { "key": "found_in", "label": "FOUND IN" }, { "key": "source", "label": "SOURCE" }] } }
```

Give concept nodes `"layer": "concept"` (the rest default to the first layer).
Finish with `npx glassbrain view kg` and give the user the path it prints.
