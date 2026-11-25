---
name: discipline-ui-ux-spec-generation
description: >
  Routes UI/UX specification creation and updates for any discipline to DomainForge AI agents.
  Loads the shared mermaid-diagram-templates skill, then renders parameterized diagrams
  with discipline-specific codes, labels, and complexity levels.
company: domainforge-ai
---

# Discipline UI/UX Spec Generation

## Overview

This skill enables DomainForge AI agents to create and update UI/UX specifications for any engineering discipline using parameterized mermaid diagram templates. Instead of hardcoding diagrams in each spec, agents render templates with discipline-specific parameters, ensuring consistency across all specs and enabling automatic updates when templates are refined.

## Routing Criteria

Route to this skill when:

- **Creating a new UI/UX specification** for any discipline — generates the full spec with parameterized diagrams
- **Updating an existing UI/UX specification** — re-renders diagrams with current template versions
- **Adding a new workflow diagram** to a spec — selects the appropriate template and renders with discipline parameters
- **Cross-referencing diagram usage** — queries the registry to find which templates a spec uses
- **Validating spec consistency** — ensures all diagrams use parameterized templates (not hardcoded)

## Capabilities

### Spec Generation Workflow

```bash
# 1. Create a new UI/UX spec for a discipline
node docs-paperclip/scripts/render-mermaid.js \
  --discipline 00860 \
  --output-dir docs-paperclip/disciplines/00860-electrical-engineering/diagrams/

# 2. The spec document references rendered diagrams via include directives:
#    ![Procurement Lifecycle](diagrams/procurement-lifecycle.md)
#    ![Three-State Navigation](diagrams/three-state-navigation.md)
```

### Discipline-Specific Parameters

| Parameter | 01900 Procurement | 00860 Electrical | 02400 Safety |
|-----------|------------------|-----------------|--------------|
| discipline | 01900 | 00860 | 02400 |
| complexity | standard | complex | compliance |
| showHITL | true | true | true |
| showPayment | true | false | false |
| appendices | A, B, C, E | A, C, D, F | A, B, C, F |

### Template Selection by Discipline

| Discipline | Required Templates |
|------------|-------------------|
| 01900 Procurement | procurement-lifecycle, three-state-navigation, order-creation-flow, sow-generation, hitl-review, approval-matrix, spec-template-registry, appendix-b-hitl, template-complexity-tree, page-state-flow |
| 00860 Electrical | procurement-lifecycle, three-state-navigation, hitl-review, approval-matrix, page-state-flow |
| 02400 Safety | procurement-lifecycle, three-state-navigation, hitl-review, approval-matrix, spec-template-registry, appendix-b-hitl, page-state-flow |
| 00872 Structural | procurement-lifecycle, three-state-navigation, hitl-review, approval-matrix, page-state-flow |
| 01300 Governance | three-state-navigation, approval-matrix, page-state-flow |

### Template Version Awareness

When a template version bumps, the skill:

1. Detects the version change from `registry.yaml`
2. Identifies all specs that use the updated template
3. Re-renders the affected diagrams with current parameters
4. Updates the spec document's version history
5. Creates a PR with the updated spec

## Related Skills

- `mermaid-diagram-templates` (PaperclipForge AI) — Shared template library (prerequisite)
- `construction-domainforge-construction-engineering` — Construction engineering domain knowledge
- `commercial-domainforge-commercial` — Commercial domain knowledge
- `user-experience-engineering` — UI/UX design patterns

## Success Metrics

- **Template Coverage**: ≥90% of diagrams in UI/UX specs use parameterized templates
- **Version Compliance**: All specs reference the current template version
- **Render Accuracy**: 100% of rendered diagrams parse without Mermaid syntax errors
- **Spec Creation Speed**: <30 minutes to generate a complete UI/UX spec for any discipline

---

*This skill routes to DomainForge AI agents for creating and updating discipline-specific UI/UX specifications using parameterized mermaid diagram templates.*