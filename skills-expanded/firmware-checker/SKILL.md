---
name: firmware-checker
description: Review device firmware versions against vulnerability data so Claude can explain which devices appear exposed and which updates deserve priority.
---

# Firmware Checker

Use this skill when the user wants to assess firmware versions for known vulnerability exposure or identify unpatched hardware that may require remediation.

## Goal

Help Claude compare device firmware information against vulnerability references and summarize which devices are most likely to need attention.

## Workflow

1. Confirm the device inventory file and whether a custom CVE database is being used.
2. Review the listed firmware versions and compare them against the available vulnerability reference data.
3. Identify devices with likely vulnerable or outdated firmware.
4. Highlight the devices and versions that present the strongest remediation priority.
5. Present a concise summary that supports patch planning or audit reporting.

## Inputs

Expected inputs from the bundled tool metadata:
- devices: Path to the device firmware CSV.
- cve-db: Optional path to a custom CVE database CSV.

## Bundled Files

- main.py contains the executable firmware review logic.
- README.md provides examples and usage notes.
- skill.yaml captures the repo-native metadata for this skill.
- sample_input may contain representative device and CVE data.

## Guidance

Be precise about which version relationships are confirmed by the input data and which conclusions depend on simplified matching logic. Prioritize clarity over alarmism.
