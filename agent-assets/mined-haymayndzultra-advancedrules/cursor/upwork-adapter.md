---
description: "Upwork Adapter — cover letter + milestones/hourly scope"
globs: ["memory-bank/**", "templates/**"]
alwaysApply: false
---

# Convert goal-level proposal → Upwork-ready artifacts
<rule>
name: upwork_cover_and_scope
triggers:
  - command: "/upwork_cover"
inputs_optional:
  - "memory-bank/plan/proposal.md"
  - "memory-bank/business/estimate.matrix.yaml"
outputs:
  - "memory-bank/upwork/cover_letter.md"
  - "memory-bank/upwork/milestones.yaml"
  - "memory-bank/upwork/hourly_scope.md"
actions:
  - type: generate_file
    path: "memory-bank/upwork/cover_letter.md"
    template: |
      # Cover Letter (Goal-Level, 200–300 words)
      - Problem statement (1–2 lines)
      - Desired outcomes (bullet form)
      - Relevant experience (brief)
      - Next step (clarifications + start condition)

  - type: generate_file
    path: "memory-bank/upwork/milestones.yaml"
    template: |
      # Fill only if FIXED-PRICE
      milestones:
        - name: "Milestone 1 - Discovery"
          deliverable: "<artifact>"
          amount: 0
          due: "YYYY-MM-DD"
        - name: "Milestone 2 - Build"
          deliverable: "<artifact>"
          amount: 0
          due: "YYYY-MM-DD"

  - type: generate_file
    path: "memory-bank/upwork/hourly_scope.md"
    template: |
      # Use only if HOURLY
      Weekly cap: <hours>
      Work Diary: required
      In-scope (weekly):
      - <deliverable>
      Notes:
      - Add task memos each session

  - type: suggest
    message: "Drafted Upwork cover + milestones/hourly scope. Edit amounts/caps before submit."
</rule>
