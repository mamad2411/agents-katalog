---
name: asset-validator
description: Reconcile authorized inventory against discovered devices so Claude can explain rogue assets, ghost assets, and inventory coverage gaps clearly.
---

# Asset Validator

Use this skill when the user wants to compare asset inventory records against discovered devices and identify unauthorized, missing, or poorly tracked hardware.

## Goal

Help Claude evaluate asset inventory quality, highlight rogue and ghost assets, and summarize the most important reconciliation issues for audit follow-up.

## Workflow

1. Confirm the authorized inventory file and the discovered asset file.
2. Review both sources for enough identifying information to compare devices reliably.
3. Identify rogue assets that appear in discovery but not inventory and ghost assets that appear in inventory but not discovery.
4. Summarize coverage gaps, unusual patterns, and areas where asset records may be stale or incomplete.
5. Present a practical reconciliation summary with priorities for remediation.

## Inputs

Expected inputs from the bundled tool metadata:
- inventory: Path to the authorized asset inventory CSV.
- discovered: Path to the discovered asset CSV.
- output: Optional output format such as markdown, json, or csv.

## Bundled Files

- main.py contains the executable asset reconciliation logic.
- README.md provides guidance and examples.
- skill.yaml captures the repo-native metadata for this skill.
- sample_input may contain representative inventory data.

## Guidance

Be clear about the difference between rogue, ghost, and unknown assets. Focus on inventory integrity and the operational risk created by poor asset visibility.
