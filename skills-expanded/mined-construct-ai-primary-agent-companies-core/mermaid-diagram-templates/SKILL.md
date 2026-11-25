---
name: mermaid-diagram-templates
description: >
  Shared skill for parameterized mermaid diagram templates used across all disciplines.
  Provides a template registry, renderer CLI, and versioned diagram patterns that serve
  as the source of truth for both documentation and code generation.
company: paperclipforge-ai
---

# Mermaid Diagram Templates

## Overview

This shared skill provides a library of **parameterized mermaid diagram templates** that serve as the single source of truth for workflow visualization across all disciplines. Instead of hardcoding diagrams in each UI/UX spec, agents use these templates with discipline-specific parameters to generate consistent, versioned diagrams.

The templates also drive **code generation** — the same template that produces a mermaid diagram can produce the corresponding React component structure (state routers, modal wiring, button configurations).

## Template Registry

All templates are stored in `docs-paperclip/templates/mermaid/` with a central registry at `docs-paperclip/templates/mermaid/registry.yaml`.

### Available Templates

| Template | Description | Parameters |
|----------|-------------|------------|
| `procurement-lifecycle` | Full procurement lifecycle from need to payment | discipline, complexity, showHITL, showPayment |
| `three-state-navigation` | Agents/Upserts/Workspace navigation with modal integration | discipline, states, buttons |
| `order-creation-flow` | Order creation with template variation selection | discipline, complexity |
| `sow-generation` | SOW generation and appendix routing | discipline, appendices |
| `hitl-review` | Human-in-the-Loop review workflow | discipline, confidenceThreshold |
| `approval-matrix` | Progressive approval routing by value thresholds | discipline, thresholds |
| `spec-template-registry` | Configurable appendix content schemas | discipline, appendixLetter |
| `appendix-b-hitl` | Template-driven HITL flow for appendix content | discipline, templateId |
| `template-complexity-tree` | Complexity level decision tree | discipline |
| `page-state-flow` | Page state flow with modal integration | discipline, states, modals |

## Routing Criteria

Route to this skill when:

- **Creating or updating a UI/UX specification** for any discipline — renders parameterized diagrams with discipline-specific codes, labels, and complexity levels
- **Generating React components from diagrams** — maps diagram patterns to component structure (state routers, modals, buttons, HITL queues)
- **Validating code against specifications** — compares generated component structure against actual implementation
- **Refining a diagram pattern** — updates a template, bumps its version, and re-renders all consuming specs
- **Cross-referencing diagram usage** — queries the registry to find which specs use which templates

## Capabilities

### Template Rendering

```bash
# Render a diagram for a specific discipline
node docs-paperclip/scripts/render-mermaid.js \
  --template procurement-lifecycle \
  --discipline 00860 \
  --complexity complex \
  --showHITL true \
  --output docs-paperclip/disciplines/00860-electrical-engineering/diagrams/procurement-lifecycle.md

# Render all diagrams for a discipline
node docs-paperclip/scripts/render-mermaid.js \
  --discipline 01900 \
  --output-dir docs-paperclip/disciplines/01900-procurement/diagrams/
```

### Template Versioning

Each template has a version history in `registry.yaml`. When a template is refined:

1. Update the template YAML with the new pattern
2. Bump the version in `registry.yaml`
3. Add a changelog entry
4. Re-render all consuming specs

### Code Generation

The same templates can generate React component structure:

```javascript
const component = generateFromTemplate("three-state-navigation", {
  discipline: "01900",
  states: ["Agents", "Upserts", "Workspace"],
  buttons: [
    { label: "View Details", modal: "AgentDetails", gate: "always" },
    { label: "Create New", modal: "CreateRecord", gate: "editor" },
    { label: "Approve", modal: "Approval", gate: "reviewer" }
  ]
});
// Output: React component with state router, button config, modal wiring
```

## Agent Usage Matrix

| Agent | Company | Uses Templates For |
|-------|---------|-------------------|
| `interface-devforge` | DevForge AI | Generate React state routers, modal wiring, button configs from diagrams |
| `codesmith-devforge` | DevForge AI | Generate component code that matches diagram flows |
| `construction-domainforge` | DomainForge AI | Create discipline-specific UI/UX specs with parameterized diagrams |
| `commercial-domainforge` | DomainForge AI | Create commercial discipline specs with procurement flows |
| `guardian-qualityforge` | QualityForge AI | Validate code matches diagram specs |
| `knowledge-curator-domainforge` | KnowledgeForge AI | Index template registry, cross-reference diagram usage |

## Related Skills

- `diagram-driven-code-generation` (DevForge AI) — Generates React components from diagram templates
- `discipline-ui-ux-spec-generation` (DomainForge AI) — Creates UI/UX specs using diagram templates
- `diagram-code-conformance` (QualityForge AI) — Validates code against diagram specs
- `user-experience-engineering` — UI/UX design patterns
- `engineering-ui-design` — Engineering discipline UI design

## Template Format

Each template is a YAML file with:

```yaml
name: string              # Unique template identifier
version: string           # Semantic version
description: string       # Human-readable description
parameters:               # Parameter definitions
  - name: string
    type: string           # string, enum, boolean, number
    default: any           # Default value
    values: []             # For enum types
template: string          # Mermaid diagram template with {{ param }} substitution
                          # and {% if param %} conditional blocks
```

## Success Metrics

- **Template Coverage**: ≥90% of diagrams in UI/UX specs use parameterized templates
- **Version Compliance**: All consuming specs reference the current template version
- **Render Accuracy**: 100% of rendered diagrams parse without Mermaid syntax errors
- **Code Conformance**: Generated components match diagram specifications

---

*This shared skill provides the mermaid diagram template system used across all Paperclip companies for consistent, versioned, code-generatable workflow visualization.*