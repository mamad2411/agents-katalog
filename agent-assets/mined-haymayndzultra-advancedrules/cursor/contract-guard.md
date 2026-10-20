---
description: "Upwork Contract Guard — escrow/work diary checks"
globs: ["memory-bank/**", "templates/**"]
alwaysApply: false
---

# Offer status template (kung wala pa)
<rule>
name: upwork_offer_template
triggers:
  - command: "/upwork_checks"
outputs:
  - "memory-bank/upwork/offer_status.json"
actions:
  - type: generate_file
    if_missing: true
    path: "memory-bank/upwork/offer_status.json"
    template: |
      {
        "contract_type": "<fixed|hourly>",
        "escrow_funded": false,
        "work_diary_ready": false,
        "weekly_cap_hours": 0,
        "notes": "Paste key details from Upwork offer here."
      }
  - type: suggest
    message: "Fill offer_status.json from the actual Upwork offer before /preflight."
</rule>

# Guard logic (goal-level; enforced by readiness gate)
<rule>
name: upwork_guard_signal
triggers:
  - command: "/upwork_checks"
actions:
  - type: suggest
    message: |
      If fixed-price: require escrow_funded=true for Milestone 1.
      If hourly: require work_diary_ready=true and weekly_cap_hours>0.
</rule>
