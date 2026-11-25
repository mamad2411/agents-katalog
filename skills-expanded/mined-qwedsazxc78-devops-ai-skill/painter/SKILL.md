---
name: painter
description: >
  Draw clear, easy-to-understand architecture diagrams, flow charts, and feature
  explainer graphics from code, system architecture, or DevOps pipelines. Output is
  an HTML artifact (inline CSS and SVG) styled with a blue-white tech palette, flat
  vector icons, a card-based multi-step layout, flow arrows, and dark code blocks.
  Supports two output levels: `basic` (single-page overview) and `detailed`
  (overview plus clickable drill-down per-component pages), and can use multi-agent
  parallel scanning to speed up analysis of large architectures. Triggered when the
  user asks to "draw an architecture diagram / flow chart" or invokes `*diagram` /
  `devops:painter`. Output renders directly in a browser for review and screenshots,
  suitable for technical documentation and presentation material.
version: "1.1.0"
---

# Painter (Architecture & Flow Diagram Expert)

Use this Skill when the user asks to "draw an architecture diagram", "draw a flow
chart", "visualize the relationships between system components", or triggers it via
`devops:painter` / Zeus `*diagram`. Your job is to analyze the user's code,
architecture, or concept and turn it into a visually polished, easy-to-understand
diagram.

## Purpose

Turn an abstract system architecture, DevOps pipeline, or program logic into a
high-information-density yet uncluttered visual. Because these diagrams require
precise layout and design (cards, shadows, code blocks), prefer to **produce an HTML
artifact (e.g. `diagram.html`)** as the output, using HTML and CSS (inline `<style>`)
together with SVG arrows and icons to achieve a perfect result that the user can view
and screenshot directly in a browser.

## Invocation Parameters

Parameters at invocation time control the output scale. If the user does not specify
a level, **first ask in one sentence whether they want `basic` or `detailed`**; if
there is no response, default to `basic`.

| Parameter | Values | Default | Description |
|-----------|--------|---------|-------------|
| `--level` | `basic` \| `detailed` | `basic` | `basic` = single-page overview (the original behavior); `detailed` = overview page plus clickable drill-down detail pages per component |
| `--output` | path | current directory | Output directory; `detailed` creates a `diagrams/` subdirectory underneath it |
| `--parallel` | `auto` \| `off` \| number | `auto` | Whether to enable multi-agent parallel scanning; `auto` = enabled automatically when component count ≥ 5 |

Example: `devops:painter --level detailed --output sre/app/nununi-infra`

Decision guidance: when there are **many top-level components** (e.g. ≥ 5 Helm charts /
modules / services) or the user explicitly asks for "more detail", use `detailed`.
Use `basic` for presentations or a quick overview.

## Visual Style Rules (strictly enforced)

1. **Colors & background**:
   - **Blue-white tech palette**: use tech blue as the primary color (e.g. `#0052CC`,
     `#0D6EFD`, `#2563EB`), with light blue or cyan as secondary accents. Use a clean
     pure white (`#FFFFFF`) or very light gray (`#F8F9FA`, `#F3F4F6`) background.
   - **High resolution, clean background**: avoid fancy backgrounds; keep the canvas
     clean and crisp.

2. **Icons & fonts**:
   - **Flat vector icons**: use simple SVG icons inside cards to represent each
     component (e.g. server, database, API, gear).
   - **Professional typography**: use clean sans-serif fonts (e.g. `system-ui`,
     `-apple-system`, `Segoe UI`, `Inter`), with neatly aligned text suitable for
     technical documents and presentation material.

3. **Layout structure (similar to Kubernetes / official DevOps architecture diagrams / migration guides)**:
   - **Top main title**: a clear main title and subtitle.
   - **Main body layout**: a **card-based layout** in three columns or multiple steps,
     arranged horizontally or vertically according to the flow order.
   - **Flow connections**: each stage or card must be **clearly connected with flow
     arrows** (SVG arrows in tech blue or gray).
   - **Card design (Card UI)**: each step uses a **standalone info box**. It must have
     a "step number" and a "title", and use **shadows (box-shadow)** and **rounded
     corners (border-radius: 8px~12px)** to add depth.
   - **Card content**: a card may contain text descriptions, concise **code blocks
     (with a dark background and syntax colors)**, or **configuration examples**.
   - **Bottom section**: at the bottom of the flow, design a "completion checklist" or
     "result summary" section.

4. **Language & content**:
   - Use **clear, professional English** for the explanations (match the user's
     requested language if they ask for another one).
   - **High information density without clutter**: use whitespace (padding, margin)
     well and clearly separate titles, body text, and code.

## Multi-Level Drill-Down Diagrams (`--level detailed`)

When the architecture is large, a single diagram cannot carry all the detail. The
`detailed` mode produces **one overview page plus one detail page per major
component**. The user can **click a card on the overview page to jump straight** to
that component's detail explanation, and return with one click.

### Output file structure

```
<output>/
├── diagram.html              # Overview page (index): components as clickable cards
└── diagrams/
    ├── prometheus.html       # Detail page for a single component
    ├── keda.html
    └── argo-rollouts.html    # File name uses the component slug (lowercase, spaces → -)
```

### Linking & navigation rules

1. **Cards are links**: wrap each component card on the overview page in
   `<a class="card" href="diagrams/<slug>.html">` (or `onclick="location.href=..."`),
   and add hover feedback (deeper shadow, border turning tech blue, `cursor: pointer`)
   plus a "View details →" hint in the bottom-right so it is obvious the card is
   clickable.
2. **Detail page content**: keep the same visual style, focused on a single component.
   Recommended content: purpose description, key configuration (`values.yaml` /
   Terraform variable snippets in dark code blocks), dependencies, version info, and
   caveats.
3. **Back navigation**: each detail page must have a **"← Back to overview" link in the
   top-left** (`href="../diagram.html"`), and may include a breadcrumb
   (Overview / Component name).
4. **Relative paths**: always use relative paths so the whole folder can be packaged,
   moved, or opened offline directly.
5. **Recursive**: if a component is itself large, its detail page's sub-items can link
   to a further level `diagrams/<slug>/...`, forming a multi-level drill-down; each
   level keeps a link back to the level above.

`basic` mode keeps a single `diagram.html` with all information on one page and does
not create a `diagrams/` subdirectory.

## Multi-Agent Parallel Scanning (`--parallel`)

For large repos (many Helm charts / Kustomize modules / services), analyzing each one
sequentially is slow. When there are many top-level components (`auto`: ≥ 5) or the
user asks to speed it up, use fan-out parallel scanning:

1. **Quick inventory (sequential)**: first do one shallow scan to list the top-level
   components (e.g. subdirectories under `helm/`, Terraform module blocks,
   `kustomization.yaml` resources) to get a work list.
2. **Fan-out (parallel)**: dispatch **one scan agent per component**, each
   independently analyzing that component's configuration, dependencies, and purpose,
   returning **structured results** (recommended JSON: `{name, slug, purpose,
   config_snippets, dependencies, version, notes}`), without blocking each other.
3. **Aggregate (sequential)**: the main flow collects all agent results, deduplicates,
   sorts, and then generates the overview page and each detail page.

### Per-platform mapping

| Platform | Fan-out mechanism |
|----------|-------------------|
| Claude Code | Call `Agent` (subagent, optionally `run_in_background`) per component, or use `Workflow` with `pipeline()` / `parallel()` to dispatch in parallel; pair with `schema` for structured output |
| Gemini CLI | Run parallel subagents / multiple `run_shell_command` scan tasks separately, then aggregate |
| Codex CLI | Split into parallelizable subtasks, run in batches, then aggregate |

Notes:
- **Keep a sequential fallback**: with `--parallel off` or when the tool does not
  support parallelism, degrade to sequential scanning; the output is unchanged.
- **Limit concurrency**: with very many components, run in batches (e.g. 8–16 at a
  time) to avoid resource exhaustion.
- **Draw only after aggregation**: start generating HTML only after all scans complete
  and results are aggregated, to ensure cross-component consistency.

## Execution Steps

1. **Confirm parameters**: parse `--level` / `--output` / `--parallel`. If the user did
   not specify a level, briefly ask whether they want `basic` or `detailed` (or decide
   automatically based on component count), then continue.
2. **Inventory & analyze code**: carefully read the code or architecture to present and
   extract the main modules, API call order, or logic flow. When there are many
   components, follow "Multi-Agent Parallel Scanning" to fan out and speed up, then
   aggregate into a structured list.
3. **Plan the layout**:
   - Decide how many steps (cards) to use.
   - Prepare each step's title, brief description, and the key code snippets to show in
     the card.
   - Decide the bottom checklist items or expected results.
   - `detailed` mode: additionally plan each component detail page's content and
     drill-down link structure.
4. **Write & produce the artifact**:
   - Use tools to create the HTML file(s) as the artifact.
   - `basic`: a single `diagram.html`.
   - `detailed`: an overview `diagram.html` (cards are clickable links) plus
     `diagrams/<slug>.html` detail pages (each with "← Back to overview"), all using
     relative paths.
   - Write polished CSS so the visual requirements are perfectly met: "blue-white tech
     style", "shadows and rounded corners", "arrow connections", "dark code blocks",
     and hover feedback on clickable cards.
5. **Present the result**: report to the user that the artifact has been created (list
   the overview and each detail page path), briefly explain the design highlights and
   how to drill down, and ask the user to click preview or open `diagram.html` to view.
