---
description: "PRE-START Acceptance Gate for solo freelancer workflow"
globs:
  - "memory-bank/business/**"
  - "memory-bank/upwork/offer_status.json"
  - "memory-bank/plan/proposal.md"
alwaysApply: false
---

# PRE-START Acceptance Gate
<rule>
name: prestart_gate
description: |
  Hindi papayagang mag-PLAN kung kulang ang pre-start artifacts.
  Target outputs na dapat meron bago tumuloy:
  - memory-bank/business/client_score.json
  - memory-bank/business/capacity_report.md
  - memory-bank/business/pricing.ratecard.yaml
  - memory-bank/business/estimate_brief.md
  - memory-bank/plan/proposal.md
triggers:
  - command: "/preflight"
actions:
  - type: attach_rules
    rules:
      - "kits/prestart/client_screener.mdc"
      - "kits/prestart/capacity_planner.mdc"
      - "kits/prestart/pricing_policy.mdc"
      - "kits/prestart/estimate_sizer.mdc"
      - "kits/prestart/proposal_builder.mdc"
  - type: suggest
    message: |
      ▶ PRE-START initiated. Tumatakbo ang screener, capacity, pricing, estimate, at proposal.
      Kapag kumpleto na ang artifacts, tatak ang gate as PASS.
  - type: set_state
    key: "phase"
    value: "PRE_START"
</rule>

# Block planning kung kulang
<rule>
name: block_planning_if_incomplete
description: "Block PLAN kapag kulang PRE-START artifacts at Upwork offer readiness"
filters:
  - type: equals
    key: "phase"
    value: "PRE_START"
actions:
  # Required business artifacts
  - type: reject
    when: missing_all([
      "memory-bank/business/client_score.json",
      "memory-bank/business/capacity_report.md",
      "memory-bank/business/pricing.ratecard.yaml",
      "memory-bank/business/estimate_brief.md",
      "memory-bank/plan/proposal.md"
    ])
    message: |
      ⛔ PRE-START incomplete. Run `/preflight` at ayusin ang kulang.

  # Upwork contract readiness (choose path)
  - type: reject
    when: or([
      and([
        equals("fixed", json("memory-bank/upwork/offer_status.json.contract_type")),
        not(json("memory-bank/upwork/offer_status.json.escrow_funded"))
      ]),
      and([
        equals("hourly", json("memory-bank/upwork/offer_status.json.contract_type")),
        or([
          not(json("memory-bank/upwork/offer_status.json.work_diary_ready")),
          lte(json("memory-bank/upwork/offer_status.json.weekly_cap_hours"), 0)
        ])
      ])
    ])
    message: |
      ⛔ Upwork guard: fund escrow (fixed) or enable Work Diary + weekly cap (hourly).

  # Pass → move to PLAN
  - type: set_state
    when: and([
      exists_all([
        "memory-bank/business/client_score.json",
        "memory-bank/business/capacity_report.md",
        "memory-bank/business/pricing.ratecard.yaml",
        "memory-bank/business/estimate_brief.md",
        "memory-bank/plan/proposal.md"
      ]),
      or([
        and([
          equals("fixed", json("memory-bank/upwork/offer_status.json.contract_type")),
          json("memory-bank/upwork/offer_status.json.escrow_funded")
        ]),
        and([
          equals("hourly", json("memory-bank/upwork/offer_status.json.contract_type")),
          json("memory-bank/upwork/offer_status.json.work_diary_ready"),
          gt(json("memory-bank/upwork/offer_status.json.weekly_cap_hours"), 0)
        ])
      ])
    ])
    key: "phase"
    value: "PLAN"

  - type: suggest
    when: equals("PLAN", state("phase"))
    message: "✅ PRE-START PASS (Upwork conditions met). You may run `/plan`."
</rule>
