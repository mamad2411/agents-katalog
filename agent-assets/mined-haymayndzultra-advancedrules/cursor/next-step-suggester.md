---
description: >
  Post-run suggester na strict: goal-first, one-step-only, at evidence-gated.
globs: ["**/*"]
alwaysApply: true
---

<rule>
name: suggest_next_step_strict
description: Deterministic, single next step, locked to active goal.
actions:
  - type: suggest
    message: |
      {{#eligible_command_found}}
      ### Suggested Next Step
      **Do:** {{command.ui.label}} ({{command.trigger}})
      **Why:** {{command.ui.reason}}

      **Run:**
      ```bash
      {{command.run.shell | join:" "}}
      ```

      **Evidence to Provide After Running:**
      - {{command.emits.add_completed_step}}
      - State becomes: {{command.emits.sets_state}}
      {{/eligible_command_found}}

      {{^eligible_command_found}}
      No eligible next step from your registry.
      {{/eligible_command_found}}
</rule>
