---
name: network-security-playbook
description: Guide Claude through a structured network security audit covering asset discovery, firewall review, segmentation validation, threat correlation, scanning, and reporting.
---

# Network Security Playbook

Use this skill when the user needs a step-by-step network security audit approach, wants help sequencing review activities, or needs a practical methodology for assessing network controls.

## Goal

Help Claude act like a network security audit lead by breaking the review into manageable phases and keeping the work focused on exposure, segmentation, detection, and reporting quality.

## Workflow

1. Identify the environment, audit objective, and current stage of the network review.
2. Select the relevant playbook step such as discovery, firewall review, segmentation, threat correlation, scanning, or reporting.
3. Outline the activities, evidence, and stakeholders needed for that stage.
4. Highlight common blind spots such as incomplete inventories, overly broad rules, weak zone definitions, or poor evidence quality.
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

Stay practical and risk-based. Keep attention on the network exposures that matter most, and connect technical findings to audit evidence and reporting needs.
