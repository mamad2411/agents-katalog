---
name: snap-agents-md
description: >
  Create, regenerate, or refine AGENTS.md repo instruction scopes. Use for
  project agent instructions, monorepo instruction layouts, stale AGENTS.md
  rewrites, instruction aliases, or bootstrap agent context. Trigger on
  "/snap-agents-md", "snap agents md", "write AGENTS.md", "fix AGENTS.md",
  "project AI instructions", or equivalent phrasing.
---

`AGENTS.md` is canonical: root = repo defaults, nested = subtree deltas; parent applies unless local overrides, nearest wins, user wins. Add scopes for behavior splits, not folder taxonomy; `CLAUDE.md` is inventory context/optional alias.

## Process

1. Inventory
   - Find all `AGENTS.md`/`CLAUDE.md` with available search tools (`fd`, `find`, `rg`, glob); include symlinks/hidden paths when relevant.
   - For each path: record link target and resolved realpath.
   - Same realpath = aliases; read once. Distinct real files = read both as context.

2. Explore
   - Read manifests, workspace config, lockfiles, scripts, docs, tests, deploy seams, generated paths, domain seams.

3. Decide files
   - Classify: single-root, multi-scope, domain-scoped, divergent monorepo.
   - Show before drafting: `path | purpose | template | action`.
   - Ask only for missing intent, conflicts, or risky overwrite.

4. Draft AGENTS.md
   - `references/single-root-template.md` — one repo-wide scope.
   - `references/multi-scope-root-template.md` — root defaults plus nested scopes.
   - `references/scoped-template.md` — subtree deltas.

5. Apply
   - Show draft first; diff before overwrite; write AGENTS.md only.
   - After writes, show final AGENTS.md paths.
   - Ask: “Do you want cleanup: create CLAUDE.md symlinks beside these AGENTS.md files and remove old AGENTS.md/CLAUDE.md files?”
   - Before removing or replacing any real file, show the exact path and require explicit yes.
