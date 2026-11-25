---
name: readd-git-submodule
description: Industrial protocol for removing and re-adding Git submodules to standardize paths or repair configurations.
category: Git & Repository Management
---

# Re-add Git Submodule Skill (v1)

This skill provides a standardized, high-fidelity protocol for the atomic removal and re-addition of Git submodules. It
ensures a "pure removal" (cleaning up all internal Git metadata) before re-adding at a new or standardized path.

***

## 1. Environment & Dependencies

Before execution, the agent MUST verify:

- **git**: Core tool for submodule operations.
    - Check: `which git`
    - Version: `git --version`
- **Submodule Protocol Compliance**: Refer to `ai-agent-rules/git-submodule-rules.md` for the core principles of branch
tracking.

***

## 2. Extraction & Plan Mapping

1. **Identify Repository URL**: Extract the URL from `.gitmodules` for the target path.
2. **Determine New Path**: Apply the project's naming convention (e.g., `git_submodule_addition` skill's mapping) to
derive the target directory.
3. **Atomic Plan**: Present a step-by-step plan for the specific submodule migration.

***

## 3. Execution Workflow (Atomic & Sequential)

The agent MUST perform the following steps **atomically for each submodule** to ensure zero error propagation:

### 3.1 Pure Removal (Delegation)

The agent MUST explicitly invoke and follow the protocol defined in the **Git Submodule Removal Skill**
(`../git_submodule_removal/SKILL.md`).

- **Reference Target**: `<OLD_PATH>`
- **Action**: Completely purge the old path from the index, `.gitmodules`, `.git/config`, and `.git/modules/<OLD_PATH>`.
- **Commit**: Execute the atomic git commit for the removal per the skill's instructions.

### 3.2 Standardized Re-addition (Delegation)

The agent MUST explicitly invoke and follow the protocol defined in the **Git Submodule Addition Skill**
(`../../.agents/skills/git-submodule-addition/SKILL.md`).

- **Reference Target**: `<NEW_PATH>` (derived per the addition skill's rules) and `<URL>`.
- **Action**: Add, initialize, and enforce branch tracking at the newly standardized path.
- **Commit**: Execute the atomic git commit for the addition per the skill's instructions.

***

## 4. Verification

1. **Verify Lineage**: Ensure the two atomic commits (`refactor(submodules): remove...` and `feat(submodule): add...`)
cohesively document the standardization of the submodule.

***

## 5. Traceability & Related Protocols

- **Skill Factory**: Generated via the Skill Factory protocol.
- **Related Skills**: `git_submodule_addition`, `git_submodule_removal` (Delegated SSOTs).
- **Parent Rules**: `ai-agent-rules/git-submodule-rules.md`.
- **Reference**: [StackOverflow: How do I remove a submodule?](https://stackoverflow.com/a/1260982/3333438)
