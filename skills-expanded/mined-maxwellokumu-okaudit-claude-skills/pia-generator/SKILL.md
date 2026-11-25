---
name: pia-generator
description: Generate structured privacy impact assessments so Claude can organize project privacy risks, controls, and decision points into a review-ready report.
---

# PIA Generator

Use this skill when the user needs a Privacy Impact Assessment or DPIA-style document for a project, system, or processing activity.

## Goal

Help Claude turn project details into a structured privacy assessment that captures processing context, risks, mitigation considerations, and governance details.

## Workflow

1. Confirm the project name, processed data types, purposes, recipients, retention, and any optional governance details.
2. Review the inputs for privacy risk indicators such as sensitive data, broad sharing, or unclear necessity.
3. Organize the assessment into a coherent privacy narrative with practical risk observations.
4. Highlight areas that may require stronger controls, legal review, or additional safeguards.
5. Present a clear PIA or DPIA-style output that is ready for stakeholder review.

## Inputs

Expected inputs from the bundled tool metadata:
- project: Name of the project or system.
- data-types: Comma-separated list of processed data types.
- purposes: Comma-separated list of processing purposes.
- recipients: Comma-separated list of data recipients.
- retention: Data retention period.
- controller: Optional data controller name.
- dpo: Optional DPO name or email.
- framework: Optional framework such as gdpr or iso27701.

## Bundled Files

- main.py contains the executable PIA generation logic.
- README.md provides examples and usage notes.
- skill.yaml captures the repo-native metadata for this skill.
- sample_input may contain example project inputs.

## Guidance

Keep the assessment structured and professional. Be explicit about risk factors, data sensitivity, and where additional review or safeguards may be needed.
