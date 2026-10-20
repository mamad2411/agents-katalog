---
description: "Estimate Sizer — goal-level, risk-adjusted"
globs: []
alwaysApply: false
---

<rule>
name: estimate_sizer
triggers:
  - command: "/estimate"
inputs_optional:
  - "memory-bank/plan/client_brief.md"
  - "memory-bank/business/client_score.json"
outputs:
  - "memory-bank/business/estimate_brief.md"
  - "memory-bank/business/estimate.matrix.yaml"
actions:
  - type: generate_file
    path: "memory-bank/business/estimate_brief.md"
    template: |
      # Estimate (Draft)
      Size: <S|M|L|XL>
      Range: <min>-<max> days
      Risk buffer: <10-40%>
      Key uncertainties: [...]
  - type: generate_file
    path: "memory-bank/business/estimate.matrix.yaml"
    template: |
      tasks:
        - name: discovery
          effort_days: 0
        - name: build
          effort_days: 0
        - name: qa
          effort_days: 0
