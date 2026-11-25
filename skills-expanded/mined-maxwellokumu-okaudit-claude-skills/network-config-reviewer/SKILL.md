---
name: network-config-reviewer
description: Review firewall and network rule sets for overly permissive access, risky exposure, and other configuration weaknesses so Claude can explain the highest-priority findings clearly.
---

# Network Config Reviewer

Use this skill when the user wants to audit firewall rules, security groups, ACLs, or other network access controls for risky patterns and excessive exposure.

## Goal

Help Claude identify insecure network rules, explain why they are risky, and present practical remediation priorities for infrastructure or audit teams.

## Workflow

1. Confirm whether the user is reviewing local rule files or a live environment and note any use of sample data.
2. Inspect the rule set for broad exposure, sensitive ports, overly permissive sources, or suspicious descriptions.
3. Separate clear misconfigurations from items that may depend on environment context.
4. Summarize the most important findings and explain their likely impact on network security posture.
5. Present prioritized recommendations for tightening the rule set.

## Inputs

Expected inputs from the bundled tool metadata:
- rules: Optional path to a CSV file of network rules.
- mode: Optional execution mode such as local or aws.
- dry_run: Optional flag to use bundled sample data.

## Bundled Files

- main.py contains the executable network review logic.
- README.md provides examples and usage notes.
- skill.yaml captures the repo-native metadata for this skill.
- sample_input may contain representative firewall or rule data.

## Guidance

Prioritize material exposure issues such as open access to sensitive ports or any-to-any style rules. Be explicit about assumptions when environment context is limited.
