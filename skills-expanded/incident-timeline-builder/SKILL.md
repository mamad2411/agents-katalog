---
name: incident-timeline-builder
description: Reconstruct incidents from log data into a clear chronological timeline so Claude can explain what happened, when it happened, and which actors or indicators matter most.
---

# Incident Timeline Builder

Use this skill when the user needs to reconstruct an incident sequence from logs, focus on a time window, or build a timeline for investigation or reporting.

## Goal

Help Claude turn raw event data into an understandable timeline that highlights important actions, indicators, and actor activity.

## Workflow

1. Confirm the log source, relevant time range, and whether the user wants actor-specific filtering.
2. Review the events and normalize them into a consistent chronological view.
3. Highlight notable indicators, suspicious actions, or clusters of activity that matter to the investigation.
4. Group or summarize events in a way that preserves sequence without overwhelming the user with noise.
5. Present a timeline that is useful for incident review, audit documentation, or stakeholder reporting.

## Inputs

Expected inputs from the bundled tool metadata:
- logs: Path to a JSON-lines or CSV log file.
- start: Optional ISO timestamp filter start.
- end: Optional ISO timestamp filter end.
- actor: Optional actor or source filter.
- output: Optional output format.

## Bundled Files

- main.py contains the executable timeline-building logic.
- README.md provides usage guidance and examples.
- skill.yaml captures the repo-native metadata for this skill.
- sample_input may contain representative incident logs.

## Guidance

Preserve chronology and be careful not to imply causation where the data only shows sequence. Call out notable IOC-related events and any gaps in visibility.
