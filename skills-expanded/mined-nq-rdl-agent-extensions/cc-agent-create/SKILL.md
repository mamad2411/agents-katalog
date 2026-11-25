---
name: cc-agent-create
license: CC-BY-4.0
description: >-
  Create or import a delegatable workflow into this agent-extensions catalog.
  Use when adding or adapting an agent procedure: author a task-focused skill,
  place the optional subagent outline in references/subagent.rst, and complete
  registry, generated plugin, changelog, and validation wiring.
argument-hint: "Workflow name and purpose, or upstream agent URL to adapt"
user-invocable: true
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# Create a delegatable catalog workflow

The `agent-create` invocation is retained for contributors importing agent
procedures. Its output is a skill with an optional delegation reference; this
catalog does not publish named agent definitions.

1. Identify the task, home subject, and action leaf in an existing bundle. Check
   for an existing skill that already owns the procedure before adding another.
2. Read [references/frontmatter-contract.rst](references/frontmatter-contract.rst)
   for the skill and reference layout. For an import, also read
   [references/normalization.rst](references/normalization.rst) and preserve its
   upstream attribution and license.
3. Author `skills/<name>/SKILL.md` with the direct workflow and a conditional link
   to `references/subagent.rst`. Put the worker outline in that reference: the
   main agent may read it when delegation helps or a user requests a subagent.
   Start from [assets/skill.md.template](assets/skill.md.template) if useful.
4. Follow [references/pipeline.rst](references/pipeline.rst) to register, sync,
   generate, add a changie fragment, and validate the complete plugin package.
5. Report the changed paths and validation results. Commit or push only when
   requested. This authoring workflow does not install session hooks.
