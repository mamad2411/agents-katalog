---
name: formal-work-package
description: Compile structural truth, behavioral truth, human-readable behavior, and verification requirements into a bounded implementation package.
---

# Skill: Formal Work Package

Use after Joern and Alloy artifacts are current.

## Goal

Compile structural truth, behavioral truth, human-readable behavior, and verification requirements into a bounded implementation package.

## Output Format

The canonical output format is JSON conforming to `.kilo/schemas/work-package.schema.json`. A Markdown companion file is optional. When generating, produce the JSON as the primary artifact and the Markdown as the human-readable companion in the same run folder.

## JSON Output

```json
{
  "artifact_id": "FWP-<feature>-<###>",
  "run_id": "RUN-YYYY-MM-DD-NNN-<slug>",
  "artifact_type": "fwp",
  "parent_artifact_id": "<grounding report id>",
  "commit_hash": "<sha>",
  "workflow_state": "READY_FOR_IMPLEMENTATION",
  "change_class": "CLASS_3",
  "created_at": "<ISO-8601>",
  "tool_versions": { "alloy": "...", "joern": "..." },
  "feature": "...",
  "risk_level": "HIGH",
  "autonomy_level": "LEVEL_3",
  "allowed_files": [...],
  "forbidden_files": [...],
  "structural_truth": { ... },
  "behavioral_truth": { ... },
  "human_readable_summary": "Markdown or plain-text summary",
  "required_tests": [...],
  "success_criteria": [...],
  "stop_conditions": [...]
}
```

## Markdown Output (Optional Companion)

# Formal Work Package

## Artifact Metadata
- Artifact ID:
- Parent Artifact:
- Commit Hash:
- Graph Snapshot:
- Alloy Validation:
- Timestamp:

## Feature

## Allowed Files

## Forbidden Files

## Structural Truth

## Behavioral Truth

## Human-Readable Implementation Summary

## Required Tests

## Required Fixtures

## Success Criteria

## Stop Conditions
