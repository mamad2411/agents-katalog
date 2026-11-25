---
name: code-review-helper
description: Analyze source code for common security weaknesses across multiple languages and help Claude explain findings, severity, and remediation clearly.
---

# Code Review Helper

Use this skill when the user wants a lightweight application security code review, needs help identifying insecure coding patterns, or wants findings summarized in audit-friendly language.

## Goal

Help Claude inspect source files for common security issues, explain why they matter, and present practical remediation advice without overstating certainty.

## Workflow

1. Confirm the source language and the code or file the user wants reviewed.
2. Inspect the input for patterns associated with secrets exposure, injection risks, unsafe execution, or similar weaknesses.
3. Distinguish likely security findings from low-confidence matches or contextual false positives.
4. Summarize the highest-risk issues first and include practical remediation guidance.
5. Present results in a concise format suitable for engineers, auditors, or security reviewers.

## Inputs

Expected inputs from the bundled tool metadata:
- code: Path to the source file or code sample to analyze.
- language: Source language such as Python, JavaScript, Java, or Go.
- output: Optional output format.

## Bundled Files

- main.py contains the executable analysis logic.
- README.md provides usage notes and examples.
- skill.yaml captures the repo-native metadata for this skill.
- sample_input may contain representative code samples for testing.

## Guidance

Be careful with certainty. Flag suspicious patterns clearly, but say when a result is heuristic and may need human review to confirm exploitability or business impact.
