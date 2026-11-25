---
name: module-structure
description: Module-structure entrypoint (invoke manually). Use when deciding whether to split/merge modules or where logic should live, or when reviewing messy structure — shallow layers, error leakage, over-abstraction. Routes between cohesion-locality (boundary/ownership decisions) and modularity-review (structure review & design).
disable-model-invocation: true
metadata:
  targets: [claude, cursor, codex, agents]
---

# Module Structure

An optional entrypoint for selecting and combining two independently usable first-party skills. Each skill owns its analysis and can complete its work without reading this entrypoint. Composition means one main agent applies the capabilities the task needs, without a fixed two-skill pipeline. Review work may use subagents under the selected skill's review guidance; design does not require them. Install both companion skills for the full workflow; if one is unavailable, identify the missing capability and complete supported work without claiming to have used it. Matt's `codebase-design` / `improve-codebase-architecture` are optional external tools when explicitly requested and available; ordinary design exploration can stay within this workflow.

## Pick

For a manual invocation, establish the requested task before routing. Reuse clear intent and scope from the conversation; if design versus review is unclear, ask rather than assuming a diff review. For an underspecified review, the main asks whether to inspect uncommitted changes, the latest commit or a specified range/PR, or a named project/module, then resolves any missing repository, path, or revision details and waits for the answer before review or delegation. These are examples, not a closed list. Pass the resolved scope to the selected skills and reviewers so they do not ask again.

Use these as starting points. Inspect the actual question and code when wording is ambiguous; keywords are clues rather than hard dispatch rules. Language is not a clue at all: the same request routes the same way in Chinese, English, or any other language, and the reply uses the user's language.

Before selecting or delegating work, the main reads root and applicable local `AGENTS.md`, relevant architecture/ADR guidance, and applicable project-local `SKILL.md` files. Carry their actual constraints into the task. Required domain reviews get one dedicated fresh-context reviewer per domain and scope under the same main; reuse an existing assignment, and have the reviewer read its own source rules without further delegation.

| The user is asking | Use |
| --- | --- |
| Design module/class/function responsibilities, place new feature code, or assign rules/state/lifecycle ownership before implementation? | `cohesion-locality` |
| Decide whether units stay together or split, where existing logic should live, or whether to extract a helper? Change axis, over-split, shrinking files, one-class-per-file, catch-all utils/helpers/common, Manager/Helper | `cohesion-locality` |
| Messy, over-abstraction, scattered error mapping, hard-to-test handlers/components, same change in many files, PR structure, cross-module refactor, shallow, leakage, cosplay | `modularity-review` |
| Adopt Clean / hexagonal / DDD layering? Add ports, interfaces, DI? | `modularity-review` (compare the benefit and cost; distinguish exploration from an adoption recommendation) |
| Open-ended structure exploration / architecture survey | Relevant boundary or surface analysis; use external tools when explicitly requested and available. HTML alone is a format choice. |
| Deepen a chosen candidate / design its public surface | `modularity-review` Mode C |

The verb in the request settles most ambiguity. A request to *review or clean up* structure — "review this PR (for boundaries/coupling)", "this handler is a mess, help me clean it up", "理下结构", "审查" — starts at `modularity-review`, even when it names boundaries; `cohesion-locality` enters only for a stay-together/split question the review uncovers. A request to *decide* — "should this be one module or three", "where should X live", "要不要拆" — starts at `cohesion-locality`. Executing a decision the user has already made ("extract this block into a helper", "把这个抽成组件", "move X to Y") is ordinary implementation work: no row matches, so briefly say structural analysis is unnecessary and complete the task. If no other row matches (bug fix, formatting, rename), do the same.

## Combine when needed

Choose one starting point based on the unanswered question:

- **Boundary only:** use `cohesion-locality` to decide ownership and split, join, move, or keep; finish when that answers the request.
- **Surface only:** use `modularity-review` for review, design, or implementation. It handles any boundary uncertainty that affects its recommendations.
- **Boundary and surface:** obtain the boundary conclusion first, then use it in `modularity-review` for the remaining requested work. Keeping a unit together can still leave its public surface worth simplifying.

Keep the user's scope, boundary conclusion and evidence, unresolved questions, behavior/public contracts, project constraints, and remaining deliverable available as task context. The same agent can reuse this directly; a separate handoff form or return to this entrypoint is unnecessary.

For a combined review, keep one main coordinator and one review scope across skills. Assign relevant capabilities within that review; consulting a companion adds analysis, not another dispatch tree. Reviewers may read neighboring code to understand shared contracts. The main owns cross-area relationships and the final synthesis; each skill retains its own review instructions.

Selection preserves the user's review, design, or implementation scope and existing authorization. Continue until the requested deliverable is complete; using another skill neither authorizes edits during a review nor requires renewed permission for implementation already requested. `modularity-review` owns selection of its working mode.

## Maintenance

Both skills are first-party (`modularity-review` is a full fork — provenance in its README; no upstream tracking). Keep selection and combination examples here; maintain boundary reasoning in `cohesion-locality` and surface analysis and modes in `modularity-review`. The routing regression set lives in `evals/routing-queries.json`. Run and score it using [evals/README.md](evals/README.md) whenever selection or combination guidance changes. Each case names one initial route; contextual cases also check continuation, scope, and boundary outcomes.
