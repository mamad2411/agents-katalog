---
name: docs-update
description: Used to update project documentation after completing work items. Ensures documentation stays in sync with code changes.
---

## Documentation structure

### Core files (keep lean)

| File | Purpose | Keep it |
|------|---------|---------|
| `CLAUDE.md` | Coding rules and "How to Add X" checklists. Read first when coding. | Prescriptive, minimal. Checklist format. |
| `AGENTS.md` | Quick reference for AI agents. Module table, key patterns, common mistakes. | High-density, no fluff. Max 100 lines. |

### Detailed docs (can grow)

| File | Purpose | Detail level |
|------|---------|--------------|
| `docs/architecture.md` | System design, data flow, component specs, design decisions. | Comprehensive. Diagrams welcome. |
| `docs/configuration.md` | Full `config.yaml` field reference with examples. | Exhaustive. User-facing. |
| `README.md` | Project intro, quick start, installation. | Marketing + getting started. |

### Internal/historical (do not reference in public docs)

- `desired_architecture.md` — planning scratchpad, not authoritative
- `CONTRIBUTING.md` — PR process, branch conventions

## Decision tree: What to update?

### You changed a trait or added a new component type

**Update:**
- `docs/architecture.md` — component description, trait signature, extension point section
- `CLAUDE.md` — "How to Add X" checklist if pattern changed

**Keep lean:** If the trait is already documented, just update the signature. Don't duplicate examples.

### You refactored internal construction (like the `resolve_users` fix)

**Update:**
- `CLAUDE.md` — "How to Add X" checklist (steps changed)
- `docs/architecture.md` — extension point description, remove outdated patterns (e.g., "two-phase construction")

**Do NOT update:** `AGENTS.md` unless the refactor changes a key pattern that appears in the "Common mistakes" or "Key patterns" section.

### You added a new config field

**Update:**
- `docs/configuration.md` — add to field reference table with type, default, description
- `examples/config.yaml` — add example usage if not obvious

**Do NOT update:** `CLAUDE.md` or `AGENTS.md` unless it's a new top-level section.

### You added a new module

**Update:**
- `AGENTS.md` — add one line to the module table
- `docs/architecture.md` — add component description if it's a major subsystem

**Keep lean:** Module table entries are `| file | one sentence |`. No implementation details.

### You changed how messages flow or added a pipeline stage

**Update:**
- `docs/architecture.md` — data flow section, system overview diagram

**Do NOT update:** `AGENTS.md` (references architecture.md for this).

### You fixed a bug with no architectural impact

**Update:** Nothing, unless the bug revealed incorrect documentation.

## How to update

### Read first

Before editing, read the relevant doc file(s) to understand:
- Current structure and tone
- What's already there (avoid duplication)
- What's explicitly deferred to another file

### Editing CLAUDE.md

- **Checklists only.** "How to Add X" sections are numbered steps, imperative mood.
- **No examples.** Code samples belong in `docs/architecture.md`.
- **No rationale.** Just the steps. If context is needed, link to `docs/architecture.md`.

### Editing AGENTS.md

- **High-density.** Every line earns its place. Target: stay under 100 lines total.
- **Tables over prose.** Module table, file guide, etc.
- **No duplication.** If it's in `docs/architecture.md`, reference it instead of repeating.

### Editing docs/architecture.md

- **Comprehensive is fine.** This is where detail lives. 
- **Diagrams welcome.** Mermaid, ASCII art, whatever clarifies the design.
- **Explain *why*.** Design decisions should include rationale.

### Editing docs/configuration.md

- **User-facing.** Assume reader has never seen the code.
- **Exhaustive.** Every field, every default, every validation rule.
- **Examples.** Show real YAML snippets, not abstract descriptions.

## Migration principle

If you find detailed implementation guidance in `CLAUDE.md` or `AGENTS.md`:
1. Move it to `docs/architecture.md`
2. Replace with a one-line reference: "See `docs/architecture.md` for X"

If you find a "How to" checklist growing beyond 12 steps, split it:
- Keep the checklist skeleton in `CLAUDE.md`
- Move substep details and code examples to `docs/architecture.md`

## Verification

After updating docs:

1. **Cross-reference check:** Did you introduce a forward reference to something not yet documented?
2. **Duplication check:** Is the same information now in two places?, make sure duplication is cleaned-up.
3. **Sync check:** Run `cargo test` — if tests changed, did docs?
4. **Brevity check:** If you edited `CLAUDE.md` or `AGENTS.md`, is there a shorter way to say it?

## Example workflow

**Scenario:** You refactored channel provider construction to use free functions instead of instance methods.

**Steps:**
1. **Read** `CLAUDE.md` "How to Add a New Channel Provider" section → outdated, mentions "build a temporary provider"
2. **Read** `docs/architecture.md` extension point section → also outdated, shows trait with removed method
3. **Update CLAUDE.md:** Change step 2 to "Add a module-level `resolve_users` function", step 3 to "call `resolve_users` directly, build gate, construct provider once"
4. **Update docs/architecture.md:** Remove `resolve_users` from trait signature, add free-function examples for each provider
5. **Update docs/architecture.md design decisions table:** Change "two-phase SecurityGate construction" to "user resolution via free functions"
6. **Check AGENTS.md:** No mention of resolve_users → no change needed
7. **Verification:** `cargo test` still passes, no broken references, no duplication

Done. Documentation is now accurate and lean.