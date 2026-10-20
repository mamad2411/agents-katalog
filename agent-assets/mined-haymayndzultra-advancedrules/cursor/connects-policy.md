---
description: "Upwork Connects Policy — boost or not"
globs: ["memory-bank/**", "templates/**"]
alwaysApply: false
---

<rule>
name: connects_decision
triggers:
  - command: "/connects_policy"
inputs_optional:
  - "memory-bank/business/client_score.json"
outputs:
  - "memory-bank/upwork/connects_decision.md"
actions:
  - type: generate_file
    path: "memory-bank/upwork/connects_decision.md"
    template: |
      # Connects Decision
      fit_score: <0-100>
      competition_level: <low|med|high>
      decision: <no_boost|boost_low|boost_mid|boost_high>
      rationale: "<why>"
  - type: suggest
    message: "Set fit_score & competition_level to finalize Connects strategy."
</rule>
