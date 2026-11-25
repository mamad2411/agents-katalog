---
name: hardware-physical-playbook
description: Guide Claude through a structured hardware and physical security audit covering inventory, access control, firmware posture, environmental controls, and reporting.
---

# Hardware and Physical Playbook

Use this skill when the user needs a step-by-step hardware and physical security audit approach or wants help sequencing fieldwork across inventory, access, device posture, and reporting.

## Goal

Help Claude act like a hardware and physical security audit lead by breaking the review into practical phases and keeping the work focused on asset visibility, access control, device condition, and evidence quality.

## Workflow

1. Identify the environment, audit objective, and current stage of the review.
2. Select the relevant playbook step such as inventory, physical access, firmware review, environmental control review, or reporting.
3. Outline the activities, evidence, and stakeholders needed for that stage.
4. Highlight common blind spots such as stale inventories, weak badge governance, outdated firmware, or missing physical safeguards.
5. Return a concise next-step plan the user can use immediately.

## Inputs

Expected inputs from the bundled tool metadata:
- step: Optional playbook step or phase to focus on.

## Bundled Files

- main.py contains the executable playbook helper.
- README.md provides narrative guidance and examples.
- skill.yaml captures the repo-native metadata for this skill.
- sample_input may contain example prompts or stage definitions.

## Guidance

Stay practical and evidence-oriented. Connect asset, access, and device findings back to operational risk and audit conclusions.
