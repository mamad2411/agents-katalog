---
name: vendor-assessor
description: Evaluate third-party security posture from assessment responses so Claude can explain vendor risk scores, category weaknesses, and follow-up priorities clearly.
---

# Vendor Assessor

Use this skill when the user wants to score a vendor security assessment, understand category-level weaknesses, or summarize third-party risk from questionnaire responses.

## Goal

Help Claude turn vendor assessment answers into a practical view of security posture, key weaknesses, and the most important follow-up actions.

## Workflow

1. Confirm the vendor assessment answer file and whether custom weighting is being used.
2. Review the responses across the major risk categories.
3. Identify weak areas, partial controls, or response patterns that materially increase vendor risk.
4. Summarize the overall posture and the issues that deserve the highest follow-up priority.
5. Present the result in a concise format suitable for procurement, security, or audit review.

## Inputs

Expected inputs from the bundled tool metadata:
- answers: Path to the vendor assessment answers file.
- weights: Optional path to custom category weights.
- output: Optional output format such as markdown or json.

## Bundled Files

- main.py contains the executable vendor scoring logic.
- README.md provides guidance and examples.
- skill.yaml captures the repo-native metadata for this skill.
- sample_input may contain representative questionnaire responses.

## Guidance

Focus on material vendor risk, not just the numeric score. Explain which control areas are weakest and what follow-up evidence or remediation is most important.
