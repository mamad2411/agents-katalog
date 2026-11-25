---
name: kg-build
description: Build a knowledge graph of a codebase, a docs folder, notes or a website as glassbrain JSON, saving a snapshot after each step so the build can be replayed and diffed. Use when asked to map, graph or explain the structure of a project, docs or site.
---

# kg-build

Write `kg/1-skeleton/graph.json`, `kg/2-filled/graph.json`, `kg/3-linked/graph.json`:

```json
{ "nodes": [{ "id": "src/auth", "label": "auth", "kind": "folder", "parent": "src", "description": "…" }],
  "edges": [{ "source": "src/auth/login.ts", "target": "src/db", "kind": "uses" }] }
```

Rules:
- **Structure is `parent`** (what sits inside what). Edges are only for relations across the tree.
- **Ids are stable paths** (`src/auth/login.ts`, `docs/billing#refunds`), never counters: the same thing keeps its id in every snapshot.
- `kind` says what a node is (`folder`, `file`, `page`, `function`). Give the leaf kinds a color in `kg/_profile.json`: `{ "nodePalette": { "file": "#6366f1" } }`.
- `description` is markdown, from the source, 1–3 sentences, in the user's language. Link with `[text](node:<id>)`.
- Edges only between nodes in the graph.

Steps (each one a new folder: copy the previous one, then edit the copy; never edit an earlier snapshot):
1. **skeleton**: one node per area / folder / file / page, nested by `parent`, down to the depth the
   user asked for (for code: every public class, function and method that matters to a reader, read
   from the source, not from memory). Be complete at that depth; no descriptions yet, and every node
   `"flags": ["stub"]`. In the profile, `"placeholderFlags": ["stub"]` draws them as plain default nodes
   until filled, and `"detail": { "flagNotes": { "stub": "Not filled in yet." } }` says so when one is opened.
2. **filled**: add `description` (and fields like `owner`, `status`) and drop the `stub` flag. No new structure.
3. **linked**: edges a reader would agree with (`imports`, `calls`, `extends`, `requires`, `references`).
   In code, read them from the source: every import and every call between mapped nodes is certain,
   so add them all. In prose, few and certain beats many and guessed.

For a website, read it with whatever browser tool you have (for example `playwright-cli open <url>` then `playwright-cli snapshot`); pages are nodes, the nav menu gives `parent`.

After each step run `npx glassbrain validate kg --strict` and fix everything it reports (dangling edges and missing parents are warnings, `--strict` makes them count). From step 2 on, `npx glassbrain diff kg/<previous> kg/<current>` should show only that step's job: step 2 only `~ changed` (no `+`, `−` or moved), step 3 only `edges added`. Finish with `npx glassbrain view kg` and give the user the path it prints.
