---
name: diagram-code-conformance
description: >
  Routes code-to-diagram conformance validation to QualityForge AI agents.
  Loads the shared mermaid-diagram-templates skill, then compares generated component
  structure against the actual implementation to detect drift.
company: qualityforge-ai
---

# Diagram-Code Conformance

## Overview

This skill enables QualityForge AI agents to validate that implemented React components match their source mermaid diagram templates. By comparing the generated component structure against the actual implementation, agents detect drift, missing features, and structural inconsistencies.

## Routing Criteria

Route to this skill when:

- **Validating code against UI/UX specifications** — compares implemented components against diagram templates
- **Detecting diagram-code drift** — identifies when code has diverged from the source diagram
- **Auditing template version compliance** — ensures all components use the current template version
- **Pre-deployment conformance checks** — validates code before release
- **Regression testing after template updates** — ensures re-rendered diagrams still match code

## Capabilities

### Conformance Validation Checks

| Check | What It Validates | Pass/Fail Criteria |
|-------|------------------|-------------------|
| **State Router Conformance** | Three-state navigation matches `three-state-navigation` template | All states present, transitions match diagram edges |
| **Button Configuration** | Button labels, modals, and visibility gates match `page-state-flow` template | Every button in diagram has corresponding implementation |
| **Modal Wiring** | Modal open/close handlers match diagram modal nodes | All modal connections present |
| **HITL Queue Structure** | Review queue matches `hitl-review` template | Approve/reject/assign paths match |
| **Approval Chain** | Approval routing matches `approval-matrix` template | Thresholds and chain levels match |
| **Template Version** | Component references current template version from `registry.yaml` | No version drift |

### Validation Workflow

```bash
# 1. Load the diagram template and the implemented component
const template = loadTemplate('three-state-navigation');
const component = loadComponent('src/pages/01900-procurement/01900-procurement-page.js');

# 2. Run conformance checks
const results = validateConformance(template, component, {
  discipline: '01900',
  states: ['Agents', 'Upserts', 'Workspace'],
  buttons: [
    { label: 'View Details', modal: 'AgentDetails', gate: 'always' },
    { label: 'Create New', modal: 'CreateRecord', gate: 'editor' },
    { label: 'Approve', modal: 'Approval', gate: 'reviewer' }
  ]
});

# 3. Output conformance report
console.log(results);
# {
#   conformance: 0.92,          # 92% match
#   passed: 6,                  # 6 checks passed
#   failed: 1,                  # 1 check failed
#   failures: [
#     {
#       check: 'Button Configuration',
#       expected: { label: 'Generate PO', modal: 'GeneratePO', gate: 'editor' },
#       actual: { label: 'Generate PO', modal: 'GeneratePO', gate: 'admin' },
#       severity: 'warning'
#     }
#   ],
#   versionDrift: {
#     template: 'three-state-navigation',
#     expected: '1.2',
#     actual: '1.0',
#     action: 'Re-render diagram with current template version'
#   }
# }
```

### Version Drift Detection

When a template version bumps, the skill:

1. Compares the template version used by the component against `registry.yaml`
2. Identifies structural changes between old and new template versions
3. Flags components that need regeneration
4. Generates a conformance report with remediation steps

### Conformance Report Format

```yaml
conformance:
  overall: 0.92                    # 0.0 - 1.0 score
  timestamp: "2026-04-29T10:00:00Z"
  discipline: "01900"
  template: "three-state-navigation"
  templateVersion: "1.2"
  checks:
    - name: "State Router Conformance"
      status: "pass"
      score: 1.0
    - name: "Button Configuration"
      status: "fail"
      score: 0.67
      failures:
        - expected: { label: "Generate PO", modal: "GeneratePO", gate: "editor" }
          actual: { label: "Generate PO", modal: "GeneratePO", gate: "admin" }
          severity: "warning"
    - name: "Modal Wiring"
      status: "pass"
      score: 1.0
  versionDrift:
    - template: "three-state-navigation"
      expectedVersion: "1.2"
      actualVersion: "1.0"
      action: "Re-render diagram with --template three-state-navigation --discipline 01900"
```

## Related Skills

- `mermaid-diagram-templates` (PaperclipForge AI) — Shared template library (prerequisite)
- `guardian-qualityforge-quality-guardian` — Quality guardian for overall quality oversight
- `validator-qualityforge-validator` — Validation specialist
- `e2e-qualityforge-end-to-end-testing` — End-to-end testing
- `hitl-qualityforge-human-in-the-loop-testing` — HITL testing

## Success Metrics

- **Conformance Score**: ≥95% conformance between diagrams and implemented code
- **Version Compliance**: 100% of components reference current template versions
- **Drift Detection Latency**: <1 hour from template version bump to drift detection
- **False Positive Rate**: <5% false positives in conformance checks

---

*This skill routes to QualityForge AI agents for validating code-to-diagram conformance using the shared mermaid diagram template system.*