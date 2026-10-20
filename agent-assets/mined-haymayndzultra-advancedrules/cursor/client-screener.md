---
description: "Client Screener — fit scoring + red flags"
globs: []
alwaysApply: false
---

<rule>
name: client_screener
triggers:
  - command: "/screen_client"
input_contract:
  optional:
    - "memory-bank/plan/client_brief.md"   # kung meron na
outputs:
  - "memory-bank/business/client_score.json"
  - "memory-bank/business/red_flags.md"
actions:
  - type: generate_file
    path: "memory-bank/business/client_score.json"
    template: |
      {
        "fit_score": "<0-100>",
        "project_risk": "<LOW|MEDIUM|HIGH>",
        "complexity": "<S|M|L|XL>",
        "must_ask": ["<question-1>", "<question-2>"],
        "decline_reasons": []
      }
  - type: generate_file
    path: "memory-bank/business/red_flags.md"
    template: |
      # Red Flags (Draft)
      - Budget ambiguity
      - No single decision-maker
      - Unclear success metrics
  - type: suggest
    message: "Screener drafted. Review and edit before finalizing."
