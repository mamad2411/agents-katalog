---
name: biome-enforcement
description: Use this skill when a task touches code, tests, Biome config, or generated artifacts and Biome must remain the final remediation and enforcement pass using the required JSON changed-files command.
license: Apache-2.0
metadata:
  author: Mike Willbanks
  repository: https://github.com/mwillbanks/agent-skills
  homepage: https://github.com/mwillbanks/agent-skills
  bugs: https://github.com/mwillbanks/agent-skills/issues
---

# Biome Enforcement

This skill governs how agents should work with **Biome as a repository enforcement tool**.

It still preserves the core rule from the prior skill:

- Biome is primarily a **final remediation and enforcement pass**
- the required final command remains fixed
- the remediation loop remains mandatory
- post-Biome build and test re-validation still occurs only when Biome changed files

This skill is broader than a single final step. Agents should also use it when they need to:

- reason about whether a task is Biome-relevant
- interpret Biome JSON diagnostics
- decide whether generated output belongs in ignore rules
- update Biome configuration safely
- distinguish source issues from tool-noise issues before the final pass

Operational details for how Biome works are defined in:

```
references/biome.md
```

Agents must consult that reference when executing this skill.

---

## Concern Ownership

This skill owns **Biome-specific execution policy**.

It takes precedence whenever the task involves:

- Biome command selection
- Biome diagnostic interpretation
- Biome remediation sequencing
- Biome ignore-path decisions
- post-Biome validation rules

Repository-wide standards skills may still govern adjacent concerns, but they should defer to this skill for Biome behavior.

---

## When This Skill Must Be Used

Activate this skill whenever a task:

- modifies source code
- modifies tests
- adds or removes files in Biome-managed areas
- changes `biome.json`, related workspace config, or scripts that affect Biome usage
- creates new directories or generated output that may need ignore handling
- requires interpretation of Biome diagnostics or JSON reporter output
- completes an implementation that must be validated before handoff

In practice, this means **most coding tasks that touch Biome-managed files** should consult this skill, even if Biome itself is only executed at the end.

---

## Execution Timing

Biome must run as the **final enforcement routine after implementation and normal validation are already complete**.

Agents may consult this skill earlier for planning, config awareness, or ignore-path triage, but they should not turn Biome into a continuous edit-loop tool.

Correct order:

1. Complete implementation
2. Run repository-native validation before Biome such as build, typecheck, and tests
3. Run the Biome remediation loop
4. If Biome modified files:
   - re-run the same build and test validation that was already used
5. Declare the task complete

---

## Required Final Command

Always run Biome using the following command:

```bash
biome check --write --unsafe --changed --no-errors-on-unmatched --files-ignore-unknown=true --reporter=json
```

Requirements:

- JSON reporter **must always be used**
- the command must run against **changed files**
- autofix must be enabled
- this exact invocation remains the required final enforcement command

Do not substitute alternative reporters or command structures.

---

## Broader Biome Responsibilities

This skill is not limited to "run one command at the end."

Agents should also apply it when working with:

- Biome config updates
- Biome ignore rules
- parser or config failures surfaced by Biome
- lint-rule remediation strategy
- repository changes that expand or shrink the set of files Biome should own

These activities support the final enforcement pass. They do not replace it.

---

## Remediation Loop

If Biome reports errors:

1. Parse the JSON output
2. Convert diagnostics into a remediation task list
3. Resolve the issues
4. Run the Biome command again

Repeat until **Biome reports zero errors**.

Full remediation workflow details are defined in:

```
references/biome.md
```

---

## Ignore Path Responsibilities

If the task introduces **generated artifacts or machine-produced output**, the agent must determine whether those paths should be ignored by Biome.

Examples may include:

- test artifacts
- playwright output
- coverage reports
- generated snapshots
- build output
- tool-generated directories

Guidance for determining when ignore paths are appropriate is defined in:

```
references/biome.md
```

Agents must **not add ignore rules for real source code issues**.

---

## Final Validation Requirement

Work is **not complete** until all of the following are true:

- Biome reports zero errors from the required command
- if Biome made changes, the repository-native build and test commands used earlier succeed again
- no new Biome noise remains in the changed scope
- any newly introduced generated output is either ignored appropriately or intentionally Biome-managed

---

## Agent Responsibility

Agents must treat Biome as a **mandatory repository enforcement mechanism**.

For any coding task:

- consult this skill when Biome-related decisions are required
- run the required Biome command before completion
- use the JSON reporter
- follow the remediation loop
- re-run build and test validation **only if Biome modifies files**

Agents should consult the reference document for operational details when executing this skill.
