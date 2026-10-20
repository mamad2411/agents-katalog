---
description: "Risk Catalog — reusable list of common risks/mitigations"
globs: []
alwaysApply: false
---

<rule>
name: risk_catalog_init
description: "Gumawa ng standard risks + tags na pwedeng i-import sa proposal."
triggers:
  - command: "/risks"
outputs:
  - "memory-bank/risk_catalog.md"
  - "memory-bank/risk_tags.yaml"
actions:
  - type: generate_file
    path: "memory-bank/risk_catalog.md"
    template: |
      # Risk Catalog (Draft)
      ## Planning
      - Requirements drift — Mitigation: freeze + CR policy
      - Unclear success metrics — Mitigation: define measurable KPIs

      ## Technical
      - Integration unknowns — Mitigation: spike + mock interfaces
      - Performance risk — Mitigation: perf budget + load test plan

      ## Data
      - Data quality variance — Mitigation: schema checks + sample set
      - PII exposure — Mitigation: masking + access policy

      ## Security
      - Secrets leakage — Mitigation: .env + vault + scanning
      - Dependency vulns — Mitigation: lockfiles + regular audit

      ## Delivery
      - Overcommit — Mitigation: capacity guard + staged milestones
      - Scope creep — Mitigation: CR template + explicit out-of-scope

  - type: generate_file
    path: "memory-bank/risk_tags.yaml"
    template: |
      tags:
        planning: ["requirements", "kpi", "timeline"]
        technical: ["integration", "performance", "infra"]
        data: ["quality", "privacy", "schema"]
        security: ["secrets", "dependency", "scan"]
        delivery: ["capacity", "scope", "handoff"]

  - type: suggest
    message: "Risk catalog drafted. Import relevant items into proposal.md."
</rule>
