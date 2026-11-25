---
name: improve-codebase-architecture
description: >
  Scan a codebase for deepening opportunities, present them as a visual HTML
  report, then grill through whichever one you pick. Use when the user says
  architecture review, codebase health, deepening, refactor suggestions, or
  complains about architectural friction.
---

# Improve Codebase Architecture

Surface architectural friction and propose **deepening opportunities** — refactors that turn shallow modules into deep ones. The aim is testability and AI-navigability.

This command is _informed_ by the project's domain model and [design-vocabulary.md](../architect-design/design-vocabulary.md) — use those terms exactly in every suggestion.

The domain language in `CONTEXT.md` gives names to good seams; ADRs in `docs/adr/` record decisions this command should not re-litigate.

## Process

### 1. Graph check (optional)

`architecture_health` flows run a **`graph_build` phase** first (`phases.py`). If you arrive here without a graph, check for `graphify-out/graph.json`:

- If `graphify-out/graph.json` exists, tell the user: "代码图谱已就绪（N 个模块），将基于图谱做增强分析。" Then query `/code-graph query god-nodes` and `/code-graph query communities` to get the global view. Query specific modules as needed via `/code-graph query`.
- If no graph exists, tell the user: "未检测到代码图谱，使用有机探索模式。如需更精确的分析，可先运行 `/code-graph build`（需要先安装 graphify）。" Then fall back to organic exploration.

### 2. Multi-modal sweep

Run 6 perspective agents in parallel using the Agent tool. Each agent queries the code graph from a different angle. See [sweep-patterns.md](sweep-patterns.md) for agent prompt templates.

**Structure agent** — Identify shallow modules (god-nodes where interface ≈ implementation)

**Data-flow agent** — Trace cross-module data flow and seam leakage

**Change agent** — Identify friction from hotspots: high-coupling + high-churn modules

**Test agent** — Map untested critical seams (high in-degree, zero test coverage)

**Security agent** — Identify trust boundary violations and auth/business logic mixing

**Performance agent** — Structural performance risks: broad-state queries, missing cache seams, deep sync chains

### 3. Cross-validate

Spawn a synthesis agent that receives all 6 perspectives:
- De-duplicate findings (same module flagged by multiple agents = higher confidence)
- Rank by convergence: findings confirmed by 2+ agents rank highest
- Apply the **deletion test** to the top findings
- Produce a final candidate list (5-10 items)

### 4. Present candidates as an HTML report

Write a self-contained HTML file to the OS temp directory so nothing lands in the repo. Resolve the temp dir from `$TMPDIR`, falling back to `/tmp` (or `%TEMP%` on Windows), and write to `<tmpdir>/architecture-review-<timestamp>.html` so each run gets a fresh file. Open it for the user — `xdg-open <path>` on Linux, `open <path>` on macOS, `start <path>` on Windows — and tell them the absolute path.

The report uses **Tailwind via CDN** for layout and styling, and **Mermaid via CDN** for diagrams where a graph/flow/sequence reliably communicates the structure. Mix Mermaid with hand-crafted CSS/SVG visuals — use Mermaid when relationships are graph-shaped (call graphs, dependencies, sequences), and hand-built divs/SVG when you want something more editorial (mass diagrams, cross-sections, collapse animations). Each candidate gets a **before/after visualisation**. Be visual.

For each candidate, render a card with:

- **Files** — which files/modules are involved
- **Problem** — why the current architecture is causing friction
- **Solution** — plain English description of what would change
- **Benefits** — explained in terms of locality and leverage, and how tests would improve
- **Before / After diagram** — side-by-side, custom-drawn, illustrating the shallowness and the deepening
- **Recommendation strength** — one of `Strong`, `Worth exploring`, `Speculative`, rendered as a badge
- **Sweep evidence** — which perspective agents flagged this (badge per agent)

End the report with a **Top recommendation** section: which candidate you'd tackle first and why.

**Use CONTEXT.md vocabulary for the domain, and [design-vocabulary.md](../architect-design/design-vocabulary.md) for structure.** If `CONTEXT.md` defines "Order," talk about "the Order intake module" — not "the FooBarHandler," and not "the Order service."

**ADR conflicts**: if a candidate contradicts an existing ADR, only surface it when the friction is real enough to warrant revisiting the ADR. Mark it clearly in the card (e.g. a warning callout: _"contradicts ADR-0007 — but worth reopening because…"_). Don't list every theoretical refactor an ADR forbids.

See [HTML-REPORT.md](HTML-REPORT.md) for the full HTML scaffold, diagram patterns, and styling guidance.

Do NOT propose interfaces yet. After the file is written, ask the user: "Which of these would you like to explore?"

### 5. Grilling loop

Once the user picks a candidate, run the `/grilling` skill to walk the design tree with them — constraints, dependencies, the shape of the deepened module, what sits behind the seam, what tests survive.

Side effects happen inline as decisions crystallise — run the `/domain-modeling` skill to keep the domain model current as you go:

- **Naming a deepened module after a concept not in `CONTEXT.md`?** Add the term to `CONTEXT.md`. Create the file lazily if it doesn't exist.
- **Sharpening a fuzzy term during the conversation?** Update `CONTEXT.md` right there.
- **User rejects the candidate with a load-bearing reason?** Offer an ADR, framed as: _"Want me to record this as an ADR so future architecture reviews don't re-suggest it?"_ Only offer when the reason would actually be needed by a future explorer to avoid re-suggesting the same thing — skip ephemeral reasons ("not worth it right now") and self-evident ones.

## Legacy mode (no code graph)

If the user declines `/code-graph build`, fall back to a single Explore agent for organic exploration — the original behavior. The HTML report should note that findings are based on exploration only, not structured graph data, and may be less comprehensive.
