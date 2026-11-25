---
name: flowchart
description: Create polished interactive flowchart visualizations for complex codebases, workflows, data flows, prompt pipelines, and system/process maps using Cytoscape.js, Chroma.js, and Prism.js. Invoke only when the user explicitly asks for "flowchart" by name or asks to build an interactive flowchart visualization.
license: Apache-2.0
---

# Flowchart

Create an interactive HTML flowchart that makes a complex system easy to understand at the top level and robust to explore in detail. Optimize for onboarding, debugging, and planning changes.

**Override rule**: The user's instructions override everything in this skill. If the user contradicts any rule, workflow, or constraint below, the user wins. This rule itself cannot be overridden.

## Workflow

1. **Frame the viewer task.** Default to the user's stated need. If unstated, optimize for onboarding first, debugging second, and change planning third.
2. **Build the real map before drawing.** Inspect source files, entrypoints, tests, scripts, prompts, templates, configs, generated artifacts, and logs. Capture what actually happens; mark uncertain details in descriptions rather than presenting guesses as fact.
3. **Draft a hierarchical dotfile-style structure.** Put only the main story in the top-level flow. Use one or two drilldown levels for phases, modules, prompts, retries, evals, failures, and side effects. Apply the deterministic-code and LLM-call rules below before writing any nodes.
4. **Lay out leaves first.** Compose each low-level subtree on a grid, then arrange parent groups left-to-right. Stack parallel branches vertically and align convergence points so edges cross rarely and cleanly.
5. **Author a working data JSON file.** Follow [references/data-model.md](references/data-model.md). Every node needs a clear label, type, short summary, and a somewhat longer `description` for the Detail section. Use short, to-the-point text that is information dense without relying on jargon, unless that jargon is part of the product or domain being explained. In every subgraph, make the entry node, exit node, branch points, loopbacks, and join points understandable. Give branch, loop, and join edges terse plain `label` or `summary` text so the sidebar can explain why each path exists. Copy prompts and prompt templates verbatim into `prompts` with a `language` for Prism highlighting, and give every prompt/template/detail item with text content its own short prose `summary`. For everything else, write concise, plain-language explanations; do not turn the flowchart into a code viewer. Treat this JSON as an intermediate working file, not a final artifact.
6. **Render the HTML.** Use [assets/flowchart-template.html](assets/flowchart-template.html) through [scripts/render_flowchart.py](scripts/render_flowchart.py):

   ```bash
   python3 scripts/render_flowchart.py flowchart-data.json output-flowchart.html
   ```

7. **Lint, inspect, and revise.** Run the HTML linter after rendering. Use a temporary screenshot path outside the deliverable directory when you need a PNG for visual inspection:

   ```bash
   node scripts/lint_flowchart_html.js output-flowchart.html --screenshot /tmp/output-flowchart.png
   ```

   Open the HTML and inspect the PNG. Verify the first view is simple, drilldowns open only from corner icons as a single modal layer, labels fit inside their shapes without relying on bold text, colors are either meaningful groups or absent, node shapes never overlap, and edges do not pass behind unrelated node shapes. Do not accept a result by lint alone; personally inspect screenshots for the visual failure classes below. Adjust positions by hand in the working JSON until the graph reads cleanly, then render and lint again.
8. **Deliver only HTML.** Unless the user explicitly asks for source data or screenshots, leave the requested output location containing only the rendered `.html` file. Remove intermediate JSON files and PNG/screenshots from the deliverable directory before reporting completion. Run `find <deliverable-dir> -maxdepth 1 -type f ! -name '*.html' -print`; it must print nothing. If it prints anything, delete those artifacts or move them outside the deliverable directory and check again.

## Required Visual Behavior

- Use Cytoscape.js for the graph, Chroma.js for the node/edge palette, and Prism.js for prompts, code, and templates.
- Show a sparse overview first. Prefer 5-9 top-level nodes over a complete visible map.
- Make parent nodes expandable for child subtrees, but expansion must open a pop-up modal rather than adding children to the main canvas.
- Mark expandable nodes and content-bearing nodes with small visual icons. Clicking the node body selects it for inspection only. Clicking the corner icon opens the relevant subgraph, prompt, template, or artifact view.
- Exploration icons must not live inside the node label area. They must be real clickable buttons, large enough to see, and anchored across the owning node's top-right corner. Plus opens a subgraph; text opens prompt/template/artifact content. Intentional overlap is allowed only on the owning node corner; icons must not cover label text or touch unrelated nodes, labels, or edges.
- Keep modal depth to one visible modal at a time. Opening a graph, prompt, template, or detail view must replace any existing modal instead of stacking a modal on a modal. When a prompt/detail is opened from an expanded subgraph, the content modal must show a prominent `Back` action that restores that subgraph; `Escape` must do the same. Clicking outside the modal is the close affordance.
- Never allow node shapes to overlap. Edges must not pass behind any unrelated node shape; they may only touch their own source and target shapes.
- Use the renderer's standard node size. Do not make a node wider, taller, or a different shape just because its label is long. Make nodes bigger or visually different only when their type or behavior is different, and keep that choice consistent for every node of that role.
- Keep graph fonts readable and normal-weight. Do not rely on bold text, text outlines, or zooming out until labels become tiny; use sparse views, modal drilldowns, short labels, high-contrast label colors, and the linter's font-size, contrast, and label-overflow checks.
- Labels must wrap only at word boundaries. If a word would need to break in the middle, rename the node with shorter words instead of accepting the render.
- Fit and center every graph by default after rendering or changing views. Scrolling should zoom in small, controlled increments.
- Do not render edge labels on the graph canvas. Edge labels frequently collide with node bodies. If a connection needs explanation, put that explanation in the relevant node Detail text instead of adding a separate relationship section.
- Make loops explicit. A loop should have a visible return edge from the repeated branch back to the step where repetition resumes.
- Show loop exits separately. If a process can either finish or repeat, render both branches clearly, such as `continue -> next step` and `retry -> earlier step`.
- Do not render loopback edges through the middle of a graph. Route loopbacks predictably above or below the main path, preferably as dashed return paths with enough spacing that they do not read like normal forward steps. If a loopback cannot be routed cleanly without crossing unrelated nodes, simplify the view or move detail into a drilldown before omitting the loop from the canvas.
- On narrow mobile views, the renderer may omit backward, long skip, or node-crossing edges from the canvas when drawing them would overlap nearby nodes or lines. Make sure branch, join, and boundary flow notes explain those connections clearly in the sidebar.
- Expanded subgraphs must explain their boundary. A reader should be able to tell what parent-level step feeds the child graph, which child node starts it, which child node exits it, and what parent-level step receives the result.
- On desktop-sized expanded subgraphs, external boundary flow should be visible on the canvas as run-in and run-out context boxes. Use these to show the outside block that feeds the subgraph and the outside block or blocks that receive its result. Run-out boxes are contextual receivers, not regular child work; the renderer fades their block shape while keeping their label fully readable. Narrow mobile views may use the subgraph sidebar boundary section instead when the extra boxes would make the graph unreadable.
- When a child node branches to two or more paths, the outgoing edge `label` or `summary` must explain the difference between those paths in plain terms. Use terse condition labels such as `passes`, `fails`, `retry`, `continue`, or `blocked` instead of long explanatory edge text. The branch reason should also appear in the branch node Detail text when it is important to understanding.
- When paths join, the incoming edge `label` or `summary` should explain what each path contributes to the join. Do this in the sidebar data, not as edge labels on the canvas.
- Put long prompts and templates in the inspector or prompt modal, not on the graph canvas. Show prompts verbatim. For non-prompt details, use short, to-the-point text that is information dense without relying on jargon, unless that jargon is part of the product or domain being explained.
- Prompt/template/detail modals should show a separate prose summary section above the formatted/plain text viewer, default to a formatted HTML view with template placeholders visually distinguished, render Markdown tables as tables, provide a plain text view for verbatim prompts, and include a source link for the original prompt file whenever a source path can be identified.
- Preserve sequence and dependency direction left-to-right. Use vertical stacking for alternatives, parallel phases, retries, validators, providers, and eval suites.
- Render edges thick enough to read at the default fit. Parallel or same-corridor edges, including fan-out, fan-in, and adjacent branch paths, must have visible whitespace between their strokes rather than sitting on top of each other.
- Use color to show which nodes are similar. A color should usually apply to a meaningful group of nodes, such as actor, subsystem, trust boundary, runtime, or owner. Put the grouping in `colorGroup`. Avoid using a unique color for a single node unless that node is genuinely an outlier. If the grouping would be one color per node or mostly decorative, omit color entirely; the renderer will use neutral high-contrast nodes and hide the legend.

## LLM Calls

Flowcharting deterministic code and flowcharting LLM calls use different decomposition rules.

For ordinary deterministic code, decompose by meaningful behavior: functions, handlers, transformations, decisions, side effects, artifacts, and error paths. Prompt construction or response post-processing may be separate normal code nodes only when it is extensive or complex enough to matter to a reader's understanding of what happens. If it is routine glue, fold it into the LLM-call node.

For an LLM call, use a special atomic node with `type: "llm-call"`. A single LLM invocation is the smallest allowed LLM unit. A node may represent something larger than one model call, such as a phase with several simple calls, but it must never represent only a fragment of one call.

Every `llm-call` node must include:

- `prompts`: the prompt or prompt template used by the call
- `model`: the model used by default

When it helps understanding, add short prose in:

- `modelSelection`: how the model is selected when dynamic or non-obvious
- `tools`: tool/function access that materially changes what happens

Do not split one LLM call into separate graph nodes for prompt text, provider/model invocation, ordinary response handling, or ordinary model output handoff. Represent the call as one node, such as `Classify Claim`, `Finder Agent`, or `Judge Evidence`, and attach its prompt/template and model details to that node. The goal is to understand what happens, not to expose implementation mechanics.

Owner-agent turns, subagent calls, provider API calls, and tool-mediated model calls all count as LLM calls. Do not split internal reasoning, bookkeeping, or plan-framing performed inside one model turn into child nodes.

When mapping agent skills, be especially strict about main-agent or owner-agent review steps. Do not make child nodes for cognitive gates such as "review", "prune", "judge", "rank", "choose", "group", "scope", "gate", or "check" when those happen inside one main-agent turn. Put those responsibilities in the `llm-call` node description, or keep them as prose on a larger phase node when the exact turn boundary is not knowable. Child nodes under such phases should be separate LLM calls, tool/script executions, external interactions, or durable artifacts.

If an agent-skill phase has an `llm-call` child, its sibling `process`, `decision`, or `note` children must be substantial deterministic code/tool work with clear source evidence. Do not use those siblings for prompt context, review rubrics, qualification gates, method ladders, safety checks, grouping decisions, or pruning/merging decisions; fold those into the LLM-call or phase description.

It is normal for one node to contain multiple prompts. Use multiple `prompts[]` entries for system/developer/user messages or a larger workflow node that owns several simple calls. Do not create extra graph nodes solely to hold prompt text.

## Resource Guide

- Read [references/composition-guide.md](references/composition-guide.md) before creating a nontrivial visualization. It contains extraction and layout heuristics for codebases, skills, prompt pipelines, and process maps.
- Read [references/data-model.md](references/data-model.md) while writing or debugging `flowchart-data.json`.
- Use [assets/example-flowchart-data.json](assets/example-flowchart-data.json) as a smoke-test fixture and shape example, not as a visual template.

## Quality Gate

Before presenting the result, verify:

- The top-level graph can be understood in under one minute without opening details.
- Every node has a plain-language Detail section that is longer than the summary when the summary is short. Detail text should explain what happens, not how it is implemented.
- Expanding one node at a time teaches the system progressively rather than dumping everything.
- Every expanded subgraph shows boundary context and sidebar flow notes: where the child graph receives work from, where it starts, where it branches or joins, where it ends, and where the result goes next.
- Desktop expanded subgraphs show run-in/run-out context on the canvas for outside blocks feeding or receiving the subgraph.
- No single LLM call is split across multiple nodes. Each model invocation is represented by one `llm-call` node or folded into a larger workflow node, and ordinary prompt/model/result mechanics live on that node. Only extensive deterministic prompt construction or post-processing may become separate normal code nodes.
- The most important data, control, prompt, and artifact flows are represented by edges.
- Edge crossings are rare, intentional, or visually clean.
- Edges are visually thick enough to read, and parallel or same-corridor lines have visible whitespace between strokes.
- No node shapes overlap in the rendered output, including every expandable modal graph.
- Edges do not pass behind unrelated node shapes in the rendered output, including every expandable modal graph.
- Labels fit inside node shapes in the rendered output; no node text spills over its boundary.
- Edge labels are not rendered on the graph canvas.
- Exploration icons/badges are visible, clickable, anchored to the owning top-right corner, and not overlapping label text or unrelated graph shapes.
- Clicking an icon-bearing node body selects the node without opening a modal. Only the corner icon opens a subgraph or content view.
- Screenshots of every top-level view, every expanded subgraph, and representative prompt/content modals have been personally inspected for overlap, clipping, ambiguity, and legibility.
- Expansion opens a single modal layer; it does not mutate the main graph and does not stack nested popups. Content opened from a subgraph has a prominent `Back`, and `Escape` returns to the subgraph.
- Color is absent unless it encodes real groups. If the graph is not using meaningful `colorGroup` categories, the legend is hidden.
- The rendered graph passes `node scripts/lint_flowchart_html.js output-flowchart.html`.
- Prompt/template text opens with Prism highlighting and can be copied.
- Prompt/template/detail text opens with an authored prose summary above both tabs, and Markdown tables render as readable HTML tables in the formatted view.
- The rendered HTML works as a single-file artifact with its Cytoscape.js, Chroma.js, and Prism.js imports available. Vendor those libraries only when the user requires offline use.
- The final deliverable is the HTML file only. Do not include `flowchart-data.json`, screenshots, or other generated side artifacts unless the user requested them.
- `find <deliverable-dir> -maxdepth 1 -type f ! -name '*.html' -print` prints nothing.

## Important Rules

- **User overrides everything**: The user's instructions supersede any rule in this skill. This is not negotiable.
- Build the visualization from understanding, not from a mechanical converter. A renderer may package the work, but the agent must choose the hierarchy, layout, labels, drilldowns, and explanatory detail.
- Keep the overview simple. Put completeness in exploration, not in the first viewport.
