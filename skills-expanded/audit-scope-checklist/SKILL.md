---
name: audit-scope-checklist
description: Generate a scoped IT audit program with controls mapped to roles and compliance frameworks. Use this skill for audit planning, control checklist generation, and audit_program.json creation.
---

# Audit Scope Checklist

Use this skill when the user asks for audit scope, audit program, audit checklist, control checklist, or audit planning.

## Goal
Generate a scoped IT audit program with controls mapped to roles and compliance frameworks. Use it to produce a markdown audit plan and an audit_program.json file for downstream analysis.

## Workflow
1. Clarify the system or environment being audited.
2. Collect the relevant role filters and framework filters if the user has them.
3. Review README.md if you need the supported role IDs or sample output structure.
4. Run main.py with the selected inputs.
5. Return the generated scope and call out any missing role or framework assumptions.

## Inputs
- system (string, required): Description of the system or environment being audited.
- roles (string, optional): Comma-separated list of role IDs to include.
- frameworks (string, optional): Comma-separated list of compliance frameworks to annotate.
- mode (string, optional): Execution mode: local, aws, or azure.
- output_dir (string, optional): Directory to write audit_program.json.

## Bundled Files
- main.py: executable logic for the skill.
- README.md: detailed usage, examples, role IDs, and output expectations.
- skill.yaml: existing repo manifest retained for this project's original packaging.

## Guidance
- Prefer the repo's documented role IDs from README.md instead of guessing role names.
- Use the generated audit_program.json as the source of truth for downstream evidence and reporting skills.
- If the user does not specify roles or frameworks, state the assumptions you use.
