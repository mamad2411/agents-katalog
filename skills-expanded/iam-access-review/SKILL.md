---
name: iam-access-review
description: Analyse IAM policies for excessive permissions, wildcards, admin-equivalent actions, missing conditions, and inline policies. Use this skill for access review and least-privilege analysis.
---

# Access Review

Use this skill when the user asks for IAM review, access review, policy review, excessive permissions analysis, wildcard permission review, or least-privilege checks.

## Goal
Analyse IAM policy data to identify dangerous permissions, wildcards, admin-equivalent actions, and missing security conditions.

## Workflow
1. Confirm whether the user is supplying local policy data or wants a cloud-backed mode.
2. Gather the policy input and any mode selection.
3. Review README.md if you need exact input formats, supported modes, or sample outputs.
4. Run main.py with the relevant input, mode, and optional dry-run settings.
5. Summarize the most dangerous findings first and include remediation guidance.

## Inputs
- input (string, optional): Path to IAM policy JSON or raw JSON string for local mode.
- mode (string, optional): Execution mode: local, aws, or azure.
- dry_run (boolean, optional): Use bundled sample data instead of live API calls.

## Bundled Files
- main.py: executable logic for the skill.
- README.md: detailed usage, input expectations, and sample outputs.
- sample_input: bundled example IAM policy inputs.
- skill.yaml: existing repo manifest retained for this project's original packaging.

## Guidance
- Prefer local or dry-run analysis before live cloud access when possible.
- Prioritize wildcard actions, broad resource scope, and missing MFA or condition constraints.
- Clearly separate observed permissions from inferred risk.
