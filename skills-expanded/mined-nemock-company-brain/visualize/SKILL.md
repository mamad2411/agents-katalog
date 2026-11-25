---
name: visualize
description: Generate a D3-based interactive HTML viewer for a company-brain vault. Single self-contained file the user opens in any browser — no server. Three view modes: graph (default, full force-directed graph, color by node type), ifu-chain (indication-for-use nodes connected via preceded_by/followed_by, medical-device only), predicate-tree (regulatory-clearance nodes connected via preceded_by, medical-device only). Branding palette and template overrides supported.
---

# visualize

This skill turns the typed graph into an interactive HTML page. Force-directed D3 layout, color by node type, hover for tooltip, click for details. Single file, single command. No server, no database.

You do not visualize the controlled-document space. You do not invent edges. The viewer reflects what is in the vault.

## Before any render

1. **Confirm the vault path.** Default: current working directory. Refuse if `_system/PROFILE.md` is missing.
2. **Run `cb validate --path <vault>` first.** Broken edges show as missing nodes in the viewer — clean validate first so the layout reflects the real graph.
3. **Confirm the active profile.** The `ifu-chain` and `predicate-tree` view modes require the medical-device profile.

## Capabilities

### `cb viewer` (default mode: graph)

```bash
cb viewer --path <vault>                          # → <vault>/vault-graph.html
cb viewer --path <vault> --out ~/some-graph.html  # custom output path
```

The default mode renders every node and every link in the vault. Nodes are colored by type with an inline legend. Edges follow the typed edge set (`derived_from`, `supports`, `preceded_by`, `related_to`, etc.). Hover any node for title + summary; click for full detail in the side panel; drag to reposition; scroll to zoom.

### IFU history chain (medical-device)

```bash
cb viewer --path <vault> --mode ifu-chain --out exports/ifu-chain.html
```

Only `indication-for-use` nodes appear, connected via `preceded_by` / `followed_by` edges. Use this for IFU evolution questions: "how did CardioTrace's IFU shift between their two 510(k)s?" The answer is the chain walk.

### 510(k) predicate tree (medical-device)

```bash
cb viewer --path <vault> --mode predicate-tree --out exports/predicate-tree.html
```

Only `regulatory-clearance` nodes, connected via `preceded_by` (the predicate citation). Use this for substantial-equivalence questions: "which competitor clearances do our planned filings cite as predicates, and how deep does that chain go?"

## Branding

The viewer reads `<vault>/_branding/colors.yaml` and uses the palette in the CSS variables of the rendered page. Override the entire HTML chrome by placing `_branding/templates/viewer.html.j2` in the vault (same convention as the doc HTML wrapper).

## Output

- One self-contained HTML file (~30–80 KB depending on vault size, mostly the embedded JSON node list).
- D3 v7 loaded from CDN. The file works offline once D3 has loaded once; for a fully offline-able file, override the template and inline the D3 bundle yourself.
- `vault-graph.html` is gitignored at the vault level by default — it's regenerated on demand, not part of the committed history. If you want to commit a snapshot for sharing, name the output something else (e.g. `exports/landscape-2026-q2.html`).

## What this skill does NOT do

- Does not modify vault nodes.
- Does not visualize node bodies — only frontmatter (id, type, title, summary, confidence, verified_at, source_kind) is in the JSON island. Click-to-detail shows that subset; for body text, point the user at `cb get-node <id>` or to opening the markdown file directly.
- Does not implement community detection (PRD §15 mentions it; deferred to a later milestone).
- Does not embed a search box (deferred — for now, the legend filter and node labels are the navigation).
- Does not visualize edges that point at unresolved targets. Run `cb validate` to find broken edges.

## What to do when something goes wrong

- **The viewer opens but no nodes appear.** Likely a zero-node vault or all edges to missing targets. Check `cb maintain audit`.
- **`cb viewer --mode ifu-chain` errors with profile mismatch.** The vault isn't medical-device. Use `--mode graph` instead.
- **Layout looks chaotic on a large vault.** D3's force-directed layout settles over a few seconds; let it run. For dense subgraphs, click a node — neighbors stay highlighted and the rest dim, which makes the local structure readable.
- **A node is missing from the graph but exists in the vault.** It probably has no id, or it's in `_system` / `_attachments` / `_branding` (those folders are skipped). Run `cb validate` to surface parsing issues.

## After rendering

- Report the output path, node count, and link count to the user.
- Offer to open it in the browser (the user can `open <vault>/vault-graph.html` themselves on macOS, or use whatever browser-launch helper their OS provides).
- For a presentation, suggest the IFU chain or predicate-tree views — they're tighter than the full graph and tell a specific story.
