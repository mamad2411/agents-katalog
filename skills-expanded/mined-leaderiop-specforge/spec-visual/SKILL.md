---
name: spec-visual
description: "Sub-orchestrator for the visual/ directory in a spec. Manages the Flux Pattern view specification structure including pages, components, elements, stores, events, actions, and workflows. Handles triad authoring (YAML + markdown wireframe + Gherkin feature)."
---

# Spec Visual (Sub-Orchestrator)

Sub-orchestrator for the `visual/` directory in a spec. Manages the directory structure, entity index, Flux Pattern overview, and individual entity triad authoring.

## When to Use

- Creating a `visual/` directory for a package with UI specifications
- Adding new pages, components, elements, stores, events, or actions to the visual spec
- Auditing visual spec completeness (missing triads, broken Flux cycle references)
- Managing the entity index across all visual entities

## Delegation

| Task | Delegate To |
|------|-------------|
| Authoring entity triads (.yaml + .md + .feature) | _(handled by this skill)_ |
| Flux Pattern cycle, entity types, YAML schema | _(handled by this skill)_ |

**This skill owns:** directory structure, entity index, Flux Pattern overview, and cross-reference conventions.

## Directory Structure

```
visual/
  index.yaml                    # Manifest of all visual entities
  index.md                      # Navigation index + Flux Pattern overview
  pages/                        # PG-* route-bound screens
    PG-001-<name>/
      spec.yaml
      wireframe.md
      tests.feature
  components/                   # CMP-* reusable UI blocks
    CMP-001-<name>/
      spec.yaml
      wireframe.md
      tests.feature
  elements/                     # ELM-* atomic interactive units
    ELM-001-<name>/
      spec.yaml
      wireframe.md
      tests.feature
  stores/                       # STR-* state containers
    STR-001-<name>/
      spec.yaml
  events/                       # EVT-* state mutation signals
    EVT-001-<name>/
      spec.yaml
  actions/                      # ACT-* user intent triggers
    ACT-001-<name>/
      spec.yaml
  workflows/                    # End-to-end Flux cycle walkthroughs
    WF-001-<name>.md
```

### index.yaml Schema

```yaml
kind: visual
package: "@myproject/<name>"
entries:
  - id: PG-001
    file: pages/PG-001-dashboard/spec.yaml
    title: Dashboard Page
    status: active              # active | draft | deprecated
    entity_type: page           # page | component | element | store | event | action | workflow
  - id: CMP-001
    file: components/CMP-001-sidebar/spec.yaml
    title: Sidebar Component
    status: active
    entity_type: component
  - id: STR-001
    file: stores/STR-001-auth/spec.yaml
    title: Auth Store
    status: active
    entity_type: store
```

**Rules:**
- Every entity directory/file in `visual/` MUST have a corresponding entry
- Every entry MUST have a corresponding entity on disk
- No duplicate `id` values across entries
- Triad completeness: pages, components, and elements MUST have all three files (.yaml + .md + .feature)

## Flux Pattern Overview

The `visual/index.md` opens with a summary of the Flux Pattern cycle used throughout the visual spec:

```
Element (ELM) ──triggers──► Action (ACT) ──dispatches──► Event (EVT)
    ▲                                                         │
    │                                                         ▼
    └──────────renders──── Store (STR) ◄──────reduces─────────┘
```

Every visual entity participates in this cycle. Cross-references between entities MUST follow the Flux direction.

## Content Rules

1. **Frontmatter exemption** — Visual `.md` files (wireframes) are EXCLUDED from the YAML frontmatter requirement. Visual entities use `spec.yaml` triads for their metadata.

## Cross-References

```markdown
# From visual to behaviors:
See [BEH-XX-020-ui-state.md](../behaviors/BEH-XX-020-ui-state.md)

# From visual to types:
See [types/ui.md](../types/ui.md)

# From pages to components:
components: [CMP-001, CMP-002]

# From actions to events:
dispatches: [EVT-001]

# From events to stores:
target_stores: [STR-001]
```
