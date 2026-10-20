---
name: powershell-script-library
description: Use when maintaining or adding reusable PowerShell scripts across automation, governance, and orchestration with strict deduplication and catalog-first reuse.
---

# PowerShell Script Library

## Specialization

Prevent script duplication and keep script assets discoverable through catalog-first reuse.

## Trigger Conditions

Use this skill when:

- A reusable PowerShell script is requested.
- Existing script overlap or duplication risk is detected.
- A skill needs script-local assets under references/scripts.
- Shared automation should be promoted into .github/scripts/powershell.

## Required Inputs

- Automation goal and target consumers.
- Candidate script name and expected reuse scope.
- Current catalog at [README.md](./../../scripts/powershell/README.md).

## Required Outputs

- Reuse decision: Reuse Existing, Extend Existing, or Create New.
- Script update in the correct location for its scope.
- Catalog update for shared scripts.
- Change-log update when scripts are materially changed.

## Placement Rule

- Skill-local use: place script in references/scripts for that skill.
- Cross-skill shared use: place script in .github/scripts/powershell and catalog it.
- Niche, skill-specific procedures should be documented and stored under [references/scripts/README.md](./references/scripts/README.md).

## Workflow

1. Check shared catalog and nearby skill references/scripts before creating anything new.
2. Decide reuse path and justify it briefly.
3. Implement or extend script with approved PowerShell patterns.
4. For niche local scripts, place under `references/scripts` and add usage notes.
5. Register shared scripts in catalog and record change tracking.

## Non-Interactive Automation Rule

Prefer one non-interactive script invocation with explicit parameters over manual prompt-based command chains.

## References

- [README.md](./../../scripts/powershell/README.md)
- [README.md](./references/README.md)
- [script-authoring-standards.md](./references/script-authoring-standards.md)
- [reuse-and-promotion-matrix.md](./references/reuse-and-promotion-matrix.md)
- [references/scripts/README.md](./references/scripts/README.md)

## Done Criteria

- Script placement matches expected reuse scope.
- Duplicate inline logic is removed or avoided.
- Shared script is cataloged with usage and output format.
- Safety and consistency checks are completed.
