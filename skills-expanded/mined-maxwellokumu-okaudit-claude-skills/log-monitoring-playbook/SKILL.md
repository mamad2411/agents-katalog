---
name: log-monitoring-playbook
description: Guide Claude through a structured logging and monitoring audit covering log inventory, baseline analysis, anomaly review, incident investigation, and reporting.
---

# Log Monitoring Playbook

Use this skill when the user needs a step-by-step methodology for auditing logging and monitoring controls or wants help sequencing a log review engagement.

## Goal

Help Claude act like a logging and monitoring audit lead by breaking the review into practical phases and keeping the work focused on visibility, detection quality, and investigative readiness.

## Workflow

1. Identify the monitoring environment, audit objective, and current stage of the review.
2. Select the relevant playbook step such as inventory, baseline definition, anomaly review, timeline analysis, or reporting.
3. Outline the activities, evidence, and stakeholders needed for that stage.
4. Highlight common gaps such as incomplete log coverage, weak baselines, or missing escalation paths.
5. Return a concise next-step plan that helps the user progress the review.

## Inputs

Expected inputs from the bundled tool metadata:
- step: Optional playbook step or phase to focus on.

## Bundled Files

- main.py contains the executable playbook helper.
- README.md provides narrative guidance and examples.
- skill.yaml captures the repo-native metadata for this skill.
- sample_input may contain example prompts or stage definitions.

## Guidance

Stay methodical and practical. Emphasize evidence quality, monitoring coverage, anomaly triage, incident reconstruction, and the usefulness of the final reporting output.
