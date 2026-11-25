---
name: openai-security-threat-model
description: Generates a repository-grounded threat model, identifying trust boundaries, assets, and abuse paths. Useful for AppSec analysis and vulnerability assessment.
allowed-tools:
- Read
- Grep
- Glob
- Write
- Edit
metadata:
  version: 0.2.0
  category: security
---
# Threat Model Source Code Repo

## Quick Start
```bash
# Generate a repository summary to use as input
# (Follow instructions in references/prompt-template.md)
```

## Workflow
1. **Analyze**: Collect repo root path, intended usage, and deployment model.
2. **Model**: Identify components, data stores, trust boundaries, and entry points.
3. **Assess**: Enumerate threats as abuse paths tied to assets and boundaries.
4. **Prioritize**: Use qualitative likelihood and impact reasoning to rank risks.
5. **Mitigate**: Recommend specific, location-based controls (authZ, validation, etc.).
6. **Finalize**: Generate `<repo-basename>-threat-model.md` after quality checks.

## Rules & Constraints
- **RULE-1**: Never claim components, flows, or controls without evidence from the repo.
- **RULE-2**: Separate runtime behavior from CI/build/dev tooling and tests/examples.
- **RULE-3**: Explicitly state all assumptions that influence threat ranking or scope.

## When to Use
- Explicit requests to threat model a codebase or path.
- Enumerating abuse paths or performing AppSec threat modeling.

## When NOT to Use
- General architecture summaries or non-security design work.
- Standard code reviews without a threat modeling focus.

## References
- [Skill Manual](references/openai-security-threat-model-manual.md)
- [Prompt Template](references/prompt-template.md)
- [Security Controls and Assets](references/security-controls-and-assets.md)
