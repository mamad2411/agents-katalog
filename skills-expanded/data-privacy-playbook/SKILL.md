---
name: data-privacy-playbook
description: Guide Claude through a structured data privacy audit covering discovery, notice review, rights verification, impact assessment, and reporting.
---

# Data Privacy Playbook

Use this skill when the user needs a step-by-step privacy audit methodology, wants help sequencing privacy review activities, or needs a practical structure for assessing data protection controls.

## Goal

Help Claude act like a privacy audit lead by breaking the review into manageable phases and keeping the work focused on data visibility, lawful processing, privacy rights, risk assessment, and reporting.

## Workflow

1. Identify the privacy framework, environment, and current stage of the review.
2. Select the relevant playbook step such as data discovery, notice review, rights validation, PIA work, or reporting.
3. Outline the activities, evidence, and stakeholders needed for that stage.
4. Highlight common blind spots such as incomplete inventories, unclear legal bases, or weak retention controls.
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

Stay practical and privacy-focused. Connect technical or process issues back to notice quality, lawful handling, rights enablement, and evidence readiness.
