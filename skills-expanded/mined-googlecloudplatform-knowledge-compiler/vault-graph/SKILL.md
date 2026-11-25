---
name: vault-graph
description: >-
  Launches or exports the hardware-accelerated 2D/3D WebGL Knowledge Graph Visualizer and Search Hub for the local OKF v0.2 knowledge vault. Use when the user invokes /vault-graph or /graph, asks to visualize the vault graph, open the graph view, export a standalone WebGL graph HTML, or open the Knowledge Graph sidecar pane. Don't use for editing markdown notes or running schema lint repairs without visualization (use vault-lint).
---

# WebGL Knowledge Graph Visualizer (`/vault-graph`)

You are the **Graph Engineering & Visualization Engine** for the **Knowledge Compiler**.
When the user invokes `/vault-graph` or asks to visualize the Obsidian Vault knowledge graph in a browser or side pane, execute this workflow.

---

## ⚡ Why WebGL Over Desktop Graph Views on Remote VMs

On remote Linux workstations and VMs accessed over remote desktop protocols, desktop Electron apps often fall back to CPU software rasterization or suffer from full-screen pixel-streaming lag.
`scripts/vault_graph.py` solves this by serving a **zero-CDN, hardware-accelerated WebGL2 / WebGL1 (2D Obsidian + 3D Orbit) single-page application** that executes directly on the **client browser's local GPU** at 60–120 FPS, with an automatic high-DPI batched Canvas2D fallback when hardware WebGL is unavailable.

---

## 🛠 Core Execution Modes

### 1. Export Standalone Self-Contained HTML Artifact (`--export`)
To generate a portable, zero-dependency HTML file (for sharing or offline viewing):

```bash
python3 <plugin_dir>/scripts/vault_graph.py \
  "${OBSIDIAN_VAULT_PATH:-$HOME/ObsidianVault}" \
  --export /tmp/vault_graph.html
```

### 2. Launch Live Local Web Server (`--serve`)
To start an interactive loopback HTTP server (`http://127.0.0.1:8765`) that dynamically recompiles the vault topology on refresh:

```bash
python3 <plugin_dir>/scripts/vault_graph.py \
  "${OBSIDIAN_VAULT_PATH:-$HOME/ObsidianVault}" \
  --serve --port 8765
```

### 3. Native Antigravity UI Plugin Sidecar (`--sidecar`)
When packaged inside the plugin at `<plugin_dir>/sidecars/vault_graph/sidecar.json`, the host `SidecarManager` launches `vault_graph.py --sidecar` on `127.0.0.1:$ANTIGRAVITY_SIDECAR_WEB_PORT` with constant-time `X-Sidecar-Token` authentication and embeds the WebGL visualizer directly inside the **Auxiliary Pane** (`[Vault WebGL Graph](sidecar://knowledge-compiler/vault_graph/)`).

---

## 🎨 Interactive Capabilities

- **Dual 2D Obsidian & 3D WebGL Orbit Modes**: Instant toggle between orthographic 2D pan/zoom and perspective 3D trackball orbit with 3D sphere lighting.
- **1-Hop & 2-Hop Neighborhood Spotlight**: Hovering or clicking any node performs a live BFS traversal, illuminating connected nodes and edges while dimming unrelated subgraphs.
- **Local Subgraph Mode**: Isolate a selected note's 1-hop or 2-hop ego-network.
- **Live Filtering**: Filter by OKF category (`entity`, `concept`, `pattern`, `synthesis`, `source`, `anchor`, `raw`), frontmatter tags, orphan status, and instant fuzzy search (`/`).
- **Real-Time Physics & Display Sliders**: Adjust repulsion charge, link spring distance, center gravity, node sizing (`Total Degree`, `Inbound Backlinks`, `PageRank`, `Uniform`), edge opacity, and LOD label density.
- **Slide-Out Markdown Reader & Inspector**: Inspect OKF v0.2 frontmatter badges, topology metrics, clickable inbound/outbound connection chips, and full rendered Markdown with interactive `[[wikilinks]]`.
