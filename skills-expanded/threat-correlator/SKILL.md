---
name: threat-correlator
description: Match network log activity against indicators of compromise so Claude can surface likely hits, explain their significance, and prioritize follow-up.
---

# Threat Correlator

Use this skill when the user has network logs and IOC data that need to be cross-referenced to identify possible malicious infrastructure, domains, or related indicators.

## Goal

Help Claude correlate observable network activity with threat intelligence indicators and present the most important matches in a clear, actionable format.

## Workflow

1. Confirm the network log source and the IOC list the user wants to compare.
2. Review the available indicators and normalize them across supported types such as IPs, CIDRs, domains, or hashes.
3. Identify matches between the logs and the IOC set.
4. Distinguish strong correlation results from weaker matches that may need validation.
5. Summarize the most important hits, their likely significance, and recommended next steps.

## Inputs

Expected inputs from the bundled tool metadata:
- logs: Path to the network log file.
- iocs: Path to the IOC file.
- output: Optional output format.

## Bundled Files

- main.py contains the executable correlation logic.
- README.md provides usage guidance and examples.
- skill.yaml captures the repo-native metadata for this skill.
- sample_input may contain representative logs and IOC lists.

## Guidance

Be precise about what matched and how strong the signal is. Avoid overstating certainty, and separate confirmed hits from items that need additional context or validation.
