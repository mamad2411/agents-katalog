---
name: pr-map
description: Use when reviewing a GitHub pull request and you want to see how its files connect (imports, references, and why) as an interactive mind map with per-file review insights (risks, suspected bugs, tests to check, impact), and to review it — inline/general comments plus a verdict — from the browser. Triggers on review PR, map this PR, visualize a pull request, how do these files connect.
---

# /pr-map

Turn a GitHub Pull Request into an interactive mind map with review insights, then review it
from the browser. The static graph (nodes + import edges + one-hop neighbors) is built by a
bundled deterministic script; you (the agent) dispatch `pr-file-analyst` subagents in parallel
to add summaries, the "why" of each connection, and review insights; a bundled merge script
folds them in; then a local dashboard opens for the review.

All bundled scripts run with plain `node` from the installed plugin via `${CLAUDE_PLUGIN_ROOT}`
— no `npm install`, no `tsx`.

## Prerequisites (check first; stop with a clear message if unmet)

1. `gh auth status` succeeds (PR data and review actions use the authenticated `gh`).
2. The current directory is a checkout of the PR's repository (`gh` resolves `{owner}/{repo}`
   from the git remote; incoming-edge detection runs `git grep`).

## Steps

1. **Resolve the PR ref** from the user's argument (number or URL). If none, default to the
   current branch's PR (`gh pr view --json number,url`). Confirm it exists.

2. **Check out the PR** so its files (including added ones) are on disk: `gh pr checkout <number>`.

3. **Build the static graph:**
   ```
   node "${CLAUDE_PLUGIN_ROOT}/dist/cli.js" <ref> "$(pwd)"
   ```
   It prints `{ dataDir, graphPath, prNumber, title, nodeCount, edgeCount }`. Capture `dataDir`.

4. **Analyze files with subagents (in parallel).** Read `graphPath`. Take the PR-file nodes
   (`inPr: true`). Decide batching: **≤ 10 changed files → one `pr-file-analyst` per file;
   > 10 → batches of ~5 files per subagent** (so a 40-file PR uses ~8 subagents). For each
   subagent, dispatch the `pr-file-analyst` agent with: the file path(s); each file's diff
   (the node's `patch`, or `gh pr diff <ref>`); its content if useful; the PR title/body; and
   the edges touching the node (id, other endpoint, kind, direction, origin) plus a one-line
   note per neighbor. Run the subagents concurrently. Write each subagent's returned JSON to
   `<dataDir>/enrichment/<index>.json` (create the `enrichment` directory). A subagent that
   fails or returns invalid JSON is fine to skip — note which files were not enriched.

5. **Merge the enrichment** into the graph:
   ```
   node "${CLAUDE_PLUGIN_ROOT}/dist/merge.js" "<dataDir>"
   ```
   It applies summaries, edge "why"s, insights, and `origin: "llm"` semantic edges, never
   altering `origin: "static"` edges.

6. **Open the dashboard:**
   ```
   node "${CLAUDE_PLUGIN_ROOT}/dist/server.js" "<dataDir>"
   ```
   It serves the graph and opens the browser. The user explores the graph (changed files +
   indirectly-affected neighbors), reads each file's diff and review insights, writes inline
   (click a diff line) and general comments, replies to threads, and submits a verdict
   (Approve / Request changes / Comment). Review actions post to GitHub via `gh`. Submitting is
   an explicit user action in the UI — do not submit on the user's behalf.

## `pr-file-analyst` output (EnrichmentResult)

Each subagent returns ONLY a JSON object (or `{ "files": [ ... ] }` for a batch):
- `path` — the file's repo-relative path (a node id).
- `summary` — what the file does and its role in this PR.
- `edgeWhys` — `{ "<edgeId>": "<why these files are connected>" }` for the edges you gave it.
- `insights` — `{ risks: string[], suspectedBugs: string[], testsToCheck: string[], impact: string }`.
- `semanticEdges` — optional `[ { target, confidence (0..1), why } ]` for related files the
  static scan missed; added as `origin: "llm"` edges. Omit when none.

## graph.json contract (mirror of the bundled `types`)

- `meta`: `{ owner, repo, number, title, description, author, baseRef, headRef }`
- `nodes[]`: `{ id, path, language, inPr, status?, additions?, deletions?, patch?, summary?, insights? }`
  (`inPr: false` = one-hop neighbor not changed in this PR).
- `edges[]`: `{ id, source, target, kind, direction, origin, confidence, why? }`
  (`origin` is `static` | `llm`; never modify `static` edges except adding a `why`).

## Notes

- Static edges cover JavaScript/TypeScript, Python, Go, Java/Kotlin, Ruby, and Rust imports. For
  other languages the graph may show isolated nodes; lean on `pr-file-analyst` `semanticEdges`
  (flagged `origin: "llm"`) to connect them.
- `graph.json`, `raw.json`, `enrichment/`, and `pending-review.json` live under
  `<repo>/.pr-map/<owner>-<repo>-<number>/` — gitignore `.pr-map/` in the target repo.
- The dashboard server is stopped automatically by the plugin's `SessionEnd` cleanup hook.
