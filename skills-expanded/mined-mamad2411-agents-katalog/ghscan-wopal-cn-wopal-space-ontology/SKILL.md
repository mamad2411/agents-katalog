---
description: Evaluate skill and generate report
---

# Evaluate Skill

Perform a comprehensive evaluation of a specified skill and generate a standardized report.

## Target Skill

Target path: `$ARGUMENTS`

> **Note**: if no argument provided, ask the user.

---

## Execution Method

This command uses the `skill-master` skill's evaluation capabilities.

**Detailed evaluation spec**: `references/evaluate-skill.md`

## Quick Evaluation Steps

1. **Information gathering**: directory structure, file count, SKILL.md line count
2. **Functionality analysis**: name, description, core features, trigger scenarios
3. **Standards compliance**: directory / naming / metadata compliance check
4. **Quality assessment**: 5-dimension scoring
5. **Relationship analysis**: overlap / complement with existing skills

## Evaluation Output

Select report format based on skill status:
- **Installed skill**: deep analysis (mechanism, scenario, principles)
- **INBOX skill**: intake assessment (value quantification, keep/discard decision)

## Next Steps

After evaluation, ask the user:
1. Install recommended skills
2. Fix compliance issues then install
3. Remove low-value skills
4. Export evaluation report