---
name: six-layer-product-research
description: "Execute Teresa Torres' 6-Layer Problem Definition Framework for rigorous product research — from customer voice to scoped problem statement"
license: MIT
user-invokable: true
argument-hint: "[product/domain] [--quick|--full]"
metadata:
  author: smith-horn
  version: 1.0.0
  category: productivity
  tags:
    - product-research
    - discovery
    - teresa-torres
    - problem-definition
    - behavioral-science
    - claude-skill
---

# 6-Layer Product Research

Execute Teresa Torres' 6-Layer Problem Definition Framework to produce a rigorous, multi-perspective problem definition before considering solutions.

## Behavioral Classification

**Type**: Advanced
**Behavior**: Guided

This skill guides you through six structured research layers, asking for input at each stage. It produces research documents, per-layer syntheses, and a cross-layer problem statement grounded in 435+ source patterns.

## When to Use

- Starting a new product or significant feature area
- Repositioning an existing product after stagnation
- A market or competitive shift requires re-grounding in customer reality
- You have a hypothesis and want to stress-test it before committing resources
- "Run product research", "6-layer analysis", "Teresa Torres framework", "problem definition research"

## Trigger Phrases

- "run product research"
- "6-layer research"
- "six-layer product research"
- "teresa torres framework"
- "problem definition framework"
- "product discovery research"
- "run the 6-layer framework"

## The Six Layers

| Layer | Core Question |
|-------|--------------|
| 1 — Customer Mental Models | What problem does the customer say they have, in their own words? |
| 2 — Ecosystem View | How do other actors interpret or feel the impact of this problem? |
| 3 — Behavioral Dynamics | What frictions, incentives, norms, habits, or power dynamics block or reinforce current behaviors? |
| 4 — Status Quo Attempts | What have people already tried, and why did it fail? |
| 5 — Technology Enablers | Where does product or technology create new possibilities? |
| 6 — Feasible Influence | What can we realistically change, given our constraints? |

## Execution Flow

### Step 1: Setup

Ask the user for:
1. **Product/problem domain** — what are we researching?
2. **Depth mode** — Quick (5-10 sources/layer, ~1-2 days each) or Full (25-40+ sources/layer, ~3-5 days each)
3. **Output directory** — default: `docs/research/` in the current project

### Step 2: Execute Layer by Layer

For each layer (1 through 6), in order:

1. Read the layer guide from `layers/layer-{N}-{name}.md`
2. Conduct research using the sources and questions defined in the guide
3. Use WebSearch and WebFetch to gather evidence from the specified source types
4. Collect verbatim quotes, data points, and source URLs
5. Produce two documents per layer:
   - **Raw research document(s)** — verbatim findings, sources, links
   - **Layer synthesis** — use `templates/layer-synthesis-template.md`
6. Present key findings to the user before proceeding to the next layer

Each layer builds on previous layers. Do not skip layers or run them out of order.

### Step 3: Cross-Layer Synthesis

After all six layers are complete:

1. Use `templates/cross-layer-synthesis-template.md` to produce the final document
2. Identify convergences across layers — patterns that appear in 3+ layers
3. Write the unified problem statement (grounded in all six layers)
4. Write the solution direction (not a spec — a direction)
5. List open questions for follow-up research

### Step 4: Review

Present the complete problem statement and solution direction to the user. Ask:
- Does this match your intuition? Where does it diverge?
- Which findings were most surprising?
- Are there scope boundaries you'd adjust?

## Framework Reference

Read `resources/framework.md` for the full framework overview including:
- Why six layers (each catches blind spots the others miss)
- Depth modes (Quick vs Full)
- Output artifacts
- How this connects to Opportunity Solution Trees
- Vocabulary definitions

## Behavioral Science Frameworks (Layer 3)

Read `resources/references.md` for annotated references including:
- BJ Fogg — Behavior Model (B=MAP)
- Fred Davis — Technology Acceptance Model (TAM)
- Everett Rogers — Diffusion of Innovations
- Cognitive Load Theory
- Context Switching Research

## Output Artifacts

For each layer:
- Raw research document(s) with verbatim quotes and source URLs
- Layer synthesis using the structured template

After all layers:
- Cross-layer synthesis with convergence analysis
- Unified problem statement (one paragraph, all six lenses)
- Solution direction (what the research points toward)
- Source index (all sources cited, organized by layer)

## Common Mistakes to Avoid

1. **Interpreting too early** (Layer 1) — listen before synthesizing
2. **Stopping at direct users** (Layer 2) — ecosystem extends beyond your customer
3. **Treating behavioral blockers as communication problems** (Layer 3) — "better docs" is rarely the answer
4. **Skipping the graveyard** (Layer 4) — prior failures are data, not embarrassments
5. **Technology-first framing** (Layer 5) — filter tech through human needs, not the reverse
6. **Scope set by ambition** (Layer 6) — be honest about what you can't change

## Dependencies

- WebSearch and WebFetch tools for research gathering
- No external packages required

## License

MIT License
