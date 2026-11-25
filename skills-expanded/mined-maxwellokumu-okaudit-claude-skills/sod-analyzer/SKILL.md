---
name: sod-analyzer
description: Detect segregation of duties conflicts in user role assignments. Use this skill for role conflict analysis, four-eyes control review, and SOD violation detection.
---

# Sod Analyzer

Use this skill when the user asks about segregation of duties, SOD analysis, role conflicts, duties separation, or four-eyes controls.

## Goal
Detect user role combinations that violate segregation-of-duties expectations and report the conflicts with risk context.

## Workflow
1. Confirm the user role dataset and whether built-in or custom conflict rules should be used.
2. Gather the user-role input and any custom conflict definitions.
3. Review README.md if you need examples of supported input shapes or output style.
4. Run main.py with the selected inputs and rule settings.
5. Summarize the conflicts, affected users, and the highest-risk combinations first.

## Inputs
- users (string, required): Path to JSON file mapping usernames to roles.
- conflicts (string, optional): Path to JSON file with custom conflict pairs.
- builtin_conflicts (boolean, optional): Include the built-in conflict library.

## Bundled Files
- main.py: executable logic for the skill.
- README.md: detailed usage, supported inputs, and sample outputs.
- sample_input: bundled example user-role and conflict data.
- skill.yaml: existing repo manifest retained for this project's original packaging.

## Guidance
- Prefer built-in conflicts for standard reviews and add custom rules when the environment has specialized duties.
- Keep the explanation tied to independence of control and risk, not just role names.
- If the role dataset is incomplete, flag that the analysis may underreport conflicts.
