---
name: iam-audit-playbook
description: Step-by-step IAM audit methodology covering user inventory, policy review, MFA verification, privileged account monitoring, SOD analysis, and reporting. Use this skill for procedural IAM audit guidance.
---

# Playbook

Use this skill when the user asks for IAM playbooks, IAM audit steps, access management audit guidance, or identity audit methodology.

## Goal
Provide a step-by-step IAM audit methodology covering planning, identity review, privilege analysis, SOD analysis, and reporting.

## Workflow
1. Use this playbook when the user needs process guidance rather than a single point-in-time check.
2. Focus on a specific step if the user narrows the scope.
3. Review README.md if you need the full methodology wording or usage examples.
4. Run main.py when the user wants the playbook rendered directly.
5. Convert the playbook into practical next actions for the current IAM audit.

## Inputs
- step (string, optional): Step number 1 through 6, or full for the whole playbook.

## Bundled Files
- main.py: executable logic for the skill.
- README.md: detailed methodology notes and usage examples.
- skill.yaml: existing repo manifest retained for this project's original packaging.

## Guidance
- Use this skill for sequencing and structure, not as a replacement for the analysis skills.
- Keep the response procedural and easy to act on.
- Route users into access-review, privileged-account-monitor, or sod-analyzer when they need concrete findings.
