---
description: "Demo Playbook — 5–10 min demo flow (goal-level)"
globs: []
alwaysApply: false
---

<rule>
name: demo_playbook_init
description: "Gumawa ng standardized demo script + checklist (no solutioning)."
triggers:
  - command: "/demo"
outputs:
  - "memory-bank/demo/demo_playbook.md"
  - "memory-bank/demo/demo_checklist.md"
  - "memory-bank/demo/demo_metrics.md"
actions:
  - type: generate_file
    path: "memory-bank/demo/demo_playbook.md"
    template: |
      # Demo Playbook (Goal-Level)
      Duration: 5–10 minutes
      Objective: Ipakita ang outcome, hindi implementation details.

      ## Flow
      1) Context (30s): Ano ang problema at desired outcome
      2) Inputs (30s): Sample data / prompt / endpoint
      3) Run (3–5m): Live run ng minimal path
      4) Result (1m): Outcome, metrics, acceptance criteria
      5) Next Steps (30s): Ano ang susunod kung go-signal

      ## Success Criteria
      - Deterministic steps (repeatable)
      - Walang manual patching sa git
      - Clear pass/fail signals

      ## Notes
      - Avoid tech deep-dives; focus sa outcomes.

  - type: generate_file
    path: "memory-bank/demo/demo_checklist.md"
    template: |
      # Demo Checklist
      - [ ] Environment ready (versions, .env.example)
      - [ ] Sample inputs prepared
      - [ ] Clear pass/fail
      - [ ] Rollback plan kung mag-fail

  - type: generate_file
    path: "memory-bank/demo/demo_metrics.md"
    template: |
      # Demo Metrics (Draft)
      - Time to result (sec):
      - Success rate over N runs:
      - Noted risks:

  - type: suggest
    message: "Drafted demo playbook + checklist + metrics. Review then run."
</rule>
