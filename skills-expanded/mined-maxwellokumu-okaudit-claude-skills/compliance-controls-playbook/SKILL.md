---
name: compliance-controls-playbook
description: Guide Claude through a structured compliance audit workflow covering framework selection, evidence planning, control testing, exception handling, and reporting.
---

# Compliance Controls Playbook

Use this skill when the user needs a step-by-step compliance audit approach, help planning evidence collection, or support navigating control testing and reporting.

## Goal

Help Claude act like a methodical compliance lead by breaking the audit into practical phases and keeping attention on evidence quality, exceptions, and reporting outcomes.

## Workflow

1. Identify the framework, environment, and audit objective the user is working toward.
2. Select the current stage of the compliance effort, from planning through reporting.
3. Outline the expected activities, stakeholders, and evidence needed for that stage.
4. Highlight common failure points such as weak evidence, incomplete testing, or unresolved exceptions.
5. Return a concise next-step plan the user can use to progress the audit.

## Inputs

Expected inputs from the bundled tool metadata:
- step: Optional playbook step or phase to focus on.

## Bundled Files

- main.py contains the executable playbook helper.
- README.md provides narrative guidance and examples.
- skill.yaml captures the repo-native metadata for this skill.
- sample_input may contain example prompts or stage definitions.

## Guidance

Stay process-oriented and practical. Emphasize sequencing, evidence readiness, exception handling, and the quality of the final audit narrative.
