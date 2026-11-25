---
name: contract-checker
description: Review third-party contract text for required clauses so Claude can explain what protections are present, what is missing, and where legal review should focus.
---

# Contract Checker

Use this skill when the user wants to review vendor, SaaS, or data-processing contract language for required clauses or identify contractual protection gaps.

## Goal

Help Claude analyze contract text for expected clauses, summarize what appears present or missing, and present the result in a way that supports commercial, legal, or audit review.

## Workflow

1. Confirm the contract file and the clause library or contract type to apply.
2. Review the text for required clauses, keywords, and likely synonym matches.
3. Identify which expected protections appear present, incomplete, or absent.
4. Highlight the most significant contractual gaps and the likely risk they create.
5. Present a concise clause summary with clear follow-up priorities.

## Inputs

Expected inputs from the bundled tool metadata:
- contract: Path to the contract text file.
- standard: Optional built-in clause set such as vendor, saas, or data-processor.
- requirements: Optional path to custom clause requirements.

## Bundled Files

- main.py contains the executable contract review logic.
- README.md provides examples and usage notes.
- skill.yaml captures the repo-native metadata for this skill.
- sample_input may contain representative contract text.

## Guidance

Be careful not to overstate legal certainty. Explain what language appears present, what seems missing, and where a formal legal review is still needed.
