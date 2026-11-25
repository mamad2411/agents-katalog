---
name: consent-checker
description: Review privacy policy or notice text against common privacy frameworks so Claude can explain coverage gaps, strengths, and compliance priorities.
---

# Consent Checker

Use this skill when the user wants to assess a privacy notice or policy against GDPR, CCPA, or PDPA-style expectations and identify missing elements.

## Goal

Help Claude evaluate privacy notice content, highlight missing or weak disclosures, and summarize likely compliance gaps in a practical way.

## Workflow

1. Confirm the policy file and the privacy framework the user wants assessed.
2. Review the text for required notice elements, rights information, legal basis cues, and disclosure quality.
3. Identify where the notice is strong, incomplete, or silent on key privacy obligations.
4. Summarize the likely compliance posture and the most important gaps to address.
5. Present results in a concise format that supports legal, privacy, or audit follow-up.

## Inputs

Expected inputs from the bundled tool metadata:
- policy: Path to the privacy policy text file.
- framework: Optional framework such as gdpr, ccpa, or pdpa.

## Bundled Files

- main.py contains the executable notice review logic.
- README.md provides usage guidance and examples.
- skill.yaml captures the repo-native metadata for this skill.
- sample_input may contain example policy text.

## Guidance

Stay careful and specific. Explain what the text covers, what appears missing, and where a legal or privacy specialist should validate the interpretation.
