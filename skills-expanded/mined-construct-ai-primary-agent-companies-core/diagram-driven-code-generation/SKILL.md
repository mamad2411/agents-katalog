---
name: diagram-driven-code-generation
description: >
  Routes React component generation from mermaid diagram templates to DevForge AI agents.
  Loads the shared mermaid-diagram-templates skill, then maps each diagram pattern
  to its corresponding React component structure (state routers, modals, buttons, HITL queues).
company: devforge-ai
---

# Diagram-Driven Code Generation

## Overview

This skill enables DevForge AI agents to generate React components directly from parameterized mermaid diagram templates. The templates serve as the single source of truth — when a diagram is refined, the generated code updates automatically.

## Routing Criteria

Route to this skill when:

- **Generating React components from UI/UX specifications** — maps diagram patterns to component structure
- **Creating state routers** — generates three-state navigation (Agents/Upserts/Workspace) from `three-state-navigation` template
- **Wiring modals to buttons** — generates button click handlers and modal open/close logic from `page-state-flow` template
- **Building HITL review queues** — generates review queue components from `hitl-review` template
- **Implementing approval matrices** — generates approval routing components from `approval-matrix` template
- **Regenerating code after diagram refinement** — re-renders components when template version bumps

## Capabilities

### Component Generation Patterns

| Template | Generated Component | Key Outputs |
|----------|-------------------|-------------|
| `three-state-navigation` | State router + nav bar | State buttons, active state tracking, transition handlers |
| `page-state-flow` | Page layout with modal wiring | Modal open/close handlers, state-aware rendering |
| `hitl-review` | HITL review queue | Review cards, approve/reject/assign buttons, audit trail |
| `approval-matrix` | Approval routing UI | Approval chain display, threshold-based routing |
| `procurement-lifecycle` | Procurement workflow UI | Step indicators, status tracking, action buttons |
| `order-creation-flow` | Order creation form | Template selector, discipline picker, form validation |
| `sow-generation` | SOW generation interface | Appendix list, AI generation trigger, content preview |
| `spec-template-registry` | Template selector UI | Template list, version display, schema preview |
| `appendix-b-hitl` | Appendix review interface | Dynamic section rendering, confidence indicators, chatbot |
| `template-complexity-tree` | Complexity selector | Radio button group, complexity descriptions, workflow preview |

### Code Generation Workflow

```javascript
// 1. Load the diagram template
const template = loadTemplate('three-state-navigation');

// 2. Generate React component structure
const component = generateComponent(template, {
  discipline: '01900',
  states: ['Agents', 'Upserts', 'Workspace'],
  buttons: [
    { label: 'View Details', modal: 'AgentDetails', gate: 'always' },
    { label: 'Create New', modal: 'CreateRecord', gate: 'editor' },
    { label: 'Approve', modal: 'Approval', gate: 'reviewer' }
  ]
});

// 3. Output: React component with:
//    - State router (useState for active state)
//    - Button config array (label, modal, visibility gate)
//    - Modal wiring (open/close handlers per button)
//    - Nav bar component with active state highlighting
```

### Template Version Awareness

When a template version bumps, the skill:

1. Detects the version change from `registry.yaml`
2. Compares old vs new diagram structure
3. Identifies changed nodes, edges, or parameters
4. Regenerates only the affected components
5. Creates a PR with the updated code

## Related Skills

- `mermaid-diagram-templates` (PaperclipForge AI) — Shared template library (prerequisite)
- `interface-devforge-api-integration` — API integration patterns
- `forge-devforge-system-architecture` — System architecture design
- `devcore-devforge-core-development` — Core development patterns

## Success Metrics

- **Code-Diagram Conformance**: 100% of generated components match their source diagram
- **Template Coverage**: ≥90% of UI components generated from diagram templates
- **Regeneration Speed**: <1 second per component regeneration
- **Version Drift**: Zero drift between diagram version and generated code version

---

*This skill routes to DevForge AI agents for generating React components from mermaid diagram templates.*