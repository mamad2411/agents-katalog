---
description: "Pricing Policy — ratecard & terms"
globs: []
alwaysApply: false
---

<rule>
name: pricing_policy
triggers:
  - command: "/pricing"
outputs:
  - "memory-bank/business/pricing.ratecard.yaml"
  - "memory-bank/business/terms.md"
actions:
  - type: generate_file
    path: "memory-bank/business/pricing.ratecard.yaml"
    template: |
      base_hourly: 0
      rush_multiplier: 1.5
      weekend_multiplier: 2.0
      tiers:
        - name: discovery
          hourly: 0
        - name: build
          hourly: 0
        - name: advisory
          hourly: 0
  - type: generate_file
    path: "memory-bank/business/terms.md"
    template: |
      - 50% upfront for fixed-scope packages
      - Change requests via signed CR
      - Invoicing weekly net 7
