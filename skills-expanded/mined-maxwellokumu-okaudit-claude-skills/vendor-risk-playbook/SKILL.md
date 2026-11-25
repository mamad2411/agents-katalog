---
name: vendor-risk-playbook
description: Guide Claude through a structured third-party risk audit covering vendor inventory, tiering, assessment, contract review, ongoing monitoring, and reporting.
---

# Vendor Risk Playbook

Use this skill when the user needs a step-by-step vendor risk audit methodology or wants help sequencing third-party review activities.

## Goal

Help Claude act like a third-party risk lead by breaking the review into manageable phases and keeping the work focused on inventory quality, risk tiering, assessment depth, contractual coverage, and monitoring.

## Workflow

1. Identify the vendor population, audit objective, and current stage of the review.
2. Select the relevant playbook step such as inventory, tiering, assessment, contract review, monitoring, or reporting.
3. Outline the activities, evidence, and stakeholders needed for that stage.
4. Highlight common blind spots such as weak inventories, inconsistent tiering, shallow assessments, or missing contract protections.
5. Return a concise next-step plan the user can apply immediately.

## Inputs

Expected inputs from the bundled tool metadata:
- step: Optional playbook step or phase to focus on.

## Bundled Files

- main.py contains the executable playbook helper.
- README.md provides narrative guidance and examples.
- skill.yaml captures the repo-native metadata for this skill.
- sample_input may contain example prompts or stage definitions.

## Guidance

Stay practical and risk-based. Connect vendor findings back to business dependency, contractual protection, ongoing assurance, and audit evidence needs.
