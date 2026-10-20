---
description: Review one recurring job the OS runs for you and propose changes to it. Say "review the follow-up watcher" or run /founder-os:employee-review <id>. Reads its row, its verdicts, and what it filed, then proposes a shown diff. Never applies its own diff.
argument-hint: "<employee id>"
allowed-tools: ["Read", "Grep", "Glob", "Bash"]
---

# Founder OS employee review

Run the employee-review skill at `skills/employee-review/SKILL.md` end to end.

## Procedure

1. If `$ARGUMENTS` is empty, run `python scripts/employee_verdict.py render` and show which jobs have a review due, then ask which one. Stop there.
2. If `roles/employees.yaml` does not exist, reply: `No org chart yet. Copy templates/roles/employees.yaml to roles/employees.yaml and add your first row - see rules/digital-employees.md.` and stop.
3. Read `skills/employee-review/SKILL.md` and run it against the named id.
4. Refuse with one line if there are no verdicts and nothing filed. Never invent a performance narrative.

## Rules

- Propose only. No diff lands without an explicit yes per diff.
- One employee per run.
- Never widen a tool grant inside a review.
- No pay, no commercial terms, no personal data in the registry.
- No em dashes or en dashes. No banned words.
