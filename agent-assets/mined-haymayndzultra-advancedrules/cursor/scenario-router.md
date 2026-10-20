---
kind: orchestrator
id: scenario_router
description: "Suggest valid triggers when domain+contexts are satisfied"
globs:
  - "memory-bank/plan/**"
alwaysApply: false
version: 1
---

# Scenario Router — Valid Trigger Suggestions

<rule>
name: allow_product_owner_when_ready
description: "Expose run_product_owner when client_brief.md exists"
actions:
  - type: reject
    when: not(exists("memory-bank/plan/client_brief.md"))
    message: "⛔ Missing memory-bank/plan/client_brief.md"
  - type: suggest
    message: "✅ You may trigger: run_product_owner"
</rule>

<rule>
name: allow_planning_when_ready
description: "Expose run_planning only if domain+inputs ready"
actions:
  - type: reject
    when: or([
      and([
        not(attached("domain_python")),
        not(attached("domain_node"))
      ]),
      not(exists("memory-bank/plan/product_backlog.yaml")),
      not(exists("memory-bank/plan/acceptance_criteria.json")),
      not(exists("memory-bank/upwork/offer_status.json"))
    ])
    message: "⛔ Planning blocked: missing domain or required inputs."
  - type: suggest
    message: "✅ You may trigger: run_planning"
</rule>

<rule>
name: allow_audit_when_ready
description: "Expose run_auditor when Action_Plan.md exists"
actions:
  - type: reject
    when: not(exists("memory-bank/plan/Action_Plan.md"))
    message: "⛔ Missing memory-bank/plan/Action_Plan.md"
  - type: suggest
    message: "✅ You may trigger: run_auditor"
</rule>

<rule>
name: allow_peer_review_when_ready
description: "Expose run_principal_engineer_peer_review when Summary_Report.md exists"
actions:
  - type: reject
    when: not(exists("memory-bank/plan/Summary_Report.md"))
    message: "⛔ Missing memory-bank/plan/Summary_Report.md"
  - type: suggest
    message: "✅ You may trigger: run_principal_engineer_peer_review"
</rule>

<rule>
name: allow_synthesis_when_ready
description: "Expose run_principal_engineer_synthesis when Summary+Validation exist"
actions:
  - type: reject
    when: or([
      not(exists("memory-bank/plan/Summary_Report.md")),
      not(exists("memory-bank/plan/Validation_Report.md"))
    ])
    message: "⛔ Missing peer review artifacts."
  - type: suggest
    message: "✅ You may trigger: run_principal_engineer_synthesis"
</rule>

