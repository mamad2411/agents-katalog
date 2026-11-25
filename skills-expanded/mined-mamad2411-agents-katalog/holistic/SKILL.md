---
name: holistic
description: Zoom out to see how code, features, or plans fit into the bigger picture. Maps bounded contexts, traces cross-cutting concerns, surfaces hidden dependencies, and identifies systemic risks. Use when you're lost in details, unfamiliar with an area, or need to understand the full impact of a change.
user-invocable: true
argument-hint: "[area, feature, or file to contextualize]"
---

# Holistic View

Provide a comprehensive, multi-layered view of how a piece of code, feature, or plan fits into the broader system. This skill operates at the system level, not the implementation level.

## Process

### 1. Discover project context

Read existing domain documentation to ground the analysis:

1. `docs/CONTEXT_MAP.md` — bounded contexts and relationships
2. `docs/UBIQUITOUS_LANGUAGE.md` — canonical terminology
3. `docs/contexts/*/CONTEXT.md` — per-context ownership and contracts
4. `CLAUDE.md` — project-level context

If these don't exist, explore the codebase organically to build the picture.

### 2. Identify the focal point

Determine what the user wants to understand. This could be:
- A specific file, module, or package
- A feature or capability
- A planned change or new feature
- A bug or unexpected behavior
- A concept or term they're uncertain about

### 3. Map the context

For the focal point, produce a **multi-layer map**:

#### Layer 1: Domain Position
- Which bounded context does this belong to?
- What domain concepts does it implement?
- What is its role within that context? (core logic, infrastructure, surface/UI, contract/boundary)

#### Layer 2: Data Flow
- What data flows INTO this component? (upstream dependencies)
- What data flows OUT? (downstream consumers)
- What shared kernels or contracts does it participate in?
- Trace the full request/data path from origin to destination

#### Layer 3: Cross-Context Impact
- Which other bounded contexts does this touch?
- What are the coupling points? (shared tables, events, APIs, window globals)
- If this breaks, what else breaks? (blast radius)
- If this changes, what else needs to change? (change propagation)

#### Layer 4: Temporal View
- How does this relate to recent changes? (check git log)
- Are there planned changes that will affect this? (check specs, open issues)
- Is this area stable or actively evolving?
- Are there known technical debt or open questions? (check CONTEXT.md open questions)

### 4. Surface insights

After mapping, highlight:

- **Hidden dependencies** — coupling that isn't obvious from imports alone (e.g., shared ClickHouse tables, window globals, convention-based contracts)
- **Systemic risks** — single points of failure, untested boundaries, stale assumptions
- **Opportunities** — places where the current structure creates unnecessary friction or where a small change would have outsized positive impact
- **Missing documentation** — if this exploration revealed gaps in CONTEXT.md, UBIQUITOUS_LANGUAGE.md, or CONTEXT_MAP.md, note what should be added

### 5. Present the map

Structure the output as:

```
## [Focal Point Name]

### Domain Position
[Which context, what role, what concepts]

### Data Flow
[Upstream → This → Downstream, with specific contracts]

### Cross-Context Impact
[What it touches beyond its own context, blast radius]

### Key Insights
[Hidden dependencies, risks, opportunities]

### Recommended Reading
[Specific files or docs to read for deeper understanding]
```

Keep it concise. The goal is orientation, not exhaustive documentation.

## When to use this skill

- "I don't know this area of code well" → map the modules and callers
- "What would break if I change X?" → trace the blast radius
- "How does feature Y actually work end-to-end?" → trace the data flow
- "Where does this concept live in the codebase?" → map to bounded context + ownership
- "I'm about to start a big change — what should I be aware of?" → full holistic view

## Related skills

- `/domain` — stress-test a plan against the domain model (deeper, interactive)
- `/architect` — surface friction and design better interfaces (prescriptive)
- `/spec` — after understanding the picture, formalize a plan
