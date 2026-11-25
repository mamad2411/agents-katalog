---
name: appsec-playbook
description: Guide Claude through a structured application security audit covering threat modeling, testing, pipeline review, dependency risk, and vulnerability management.
---

# Application Security Playbook

Use this skill when the user needs a step-by-step appsec audit plan, wants help sequencing review activities, or needs a practical methodology for assessing application security.

## Goal

Help Claude act like an application security lead by breaking the review into manageable phases and keeping the assessment focused on meaningful product and delivery risks.

## Workflow

1. Identify the application context, technology stack, and review objective.
2. Determine which phase or step the user is currently working on.
3. Outline the relevant appsec activities, such as threat modeling, code review, dynamic testing, dependency review, or pipeline assessment.
4. Highlight likely blind spots, evidence gaps, and high-risk areas that deserve deeper attention.
5. Return a concise next-step plan that helps the user progress the assessment.

## Inputs

Expected inputs from the bundled tool metadata:
- step: Optional playbook step or phase to focus on.

## Bundled Files

- main.py contains the executable playbook helper.
- README.md provides narrative guidance and examples.
- skill.yaml captures the repo-native metadata for this skill.
- sample_input may contain example prompts or stage definitions.

## Guidance

Stay practical and risk-based. Emphasize sequencing, evidence quality, and the connection between technical weaknesses and business impact.
