---
name: skill-creator
description: Create or update a Tomcat skill with focused instructions and only the scripts, references, or assets its workflow needs.
license: Apache-2.0; see LICENSE.txt
---

# Skill Creator

Create skills that give an agent useful, non-obvious guidance without constraining unrelated work.

## Core principles

**Assume the agent can do ordinary work.** Include information only when it changes a decision, improves a result, or records a real constraint. Remove generic advice, repeated rules, speculative edge cases, and examples that do not make the work clearer.

**Preserve the user's scope.** A skill supports the requested task. It must not silently broaden the assignment, modify unrelated configuration, or treat approval for one action as permission for another. A retrying or externally changing workflow needs a stopping condition that matches its risk.

**Match detail to risk.** Use deterministic steps or scripts when safety, correctness, permissions, or a fragile workflow needs them. For ordinary work, state the outcome and decision criteria instead of forcing one rigid process.

**Keep discovery precise.** The name and description are seen before the body. Describe what the skill does and when it applies. Do not turn one skill into a catch-all list of capabilities.

**Reveal detail progressively.** Put purpose, essential constraints, and routing in `SKILL.md`. Put large examples, schemas, or mode-specific procedures in `references/`, and load only the file relevant to the current task.

## Anatomy of a skill

Every skill is a folder containing a required `SKILL.md` and only the optional resources its real workflow needs:

```text
skill-name/
|-- SKILL.md                 required instructions
|   |-- YAML frontmatter     name and description
|   `-- Markdown body        instructions loaded on use
|-- scripts/                 optional deterministic helpers
|-- references/              optional material loaded on demand
`-- assets/                  optional files copied into an output
```

Choose the smallest useful structure. Do not create empty folders, examples, changelogs, or extra documentation without a concrete use.

### SKILL.md

The YAML frontmatter identifies a skill and determines when it can be considered. A portable Tomcat skill requires a lowercase hyphen-case string `name` and a one-line string `description`.

The body supplies the purpose, actual workflow, non-obvious constraints, and links to supporting files. Keep conditional procedures in references instead of placing every detail in the entrypoint.

Skill information is available in three stages:

1. **Name and description** — used to decide whether the skill applies.
2. **Body** — loaded when the skill is used.
3. **Supporting resources** — read or executed only when the current task needs them.

A large limit is not a target. Move conditional material to a reference when it makes the main instructions easier to use.

### Scripts

Use `scripts/` when a repeated transformation would otherwise be re-created, or when a deterministic helper materially improves reliability.

Good uses include repeated file conversions, data transformations, and safe validation. Run a changed script to verify observable behavior. Scripts must take explicit paths; do not rely on the process working directory or executable permissions.

### References

Use `references/` for maintained, task-specific information needed only in particular situations. Link each reference from this file and say when to load it. Keep one source of truth; do not copy a manual or tutorial simply because it is available elsewhere.

For a large reference, add useful search words or a short contents list when that makes the needed section easier to find.

### Assets

Use `assets/` for files intended for generated output, such as templates, images, fonts, or starter projects. Assets are not instructions and should not be loaded into context unless inspection is needed for the task.

## Create or update a skill

Adapt the work to the request. A small edit may only require reading the existing header and body. A complex new skill may need realistic use cases, support files, initialization, writing, and validation.

Ask a question only when a missing fact matters and cannot be safely inferred. Preserve the user's chosen location; otherwise create the skill in a separate source directory that the user controls.

### Naming

- Use lowercase letters, digits, and hyphens.
- Keep names below 64 characters.
- Prefer short, action-oriented names.
- Name the folder after the skill.

### Initialize a new skill

Use the bundled initializer when it prevents avoidable format drift:

```bash
python3 "<skill directory>/scripts/init_skill.py" my-skill --path "<source directory>"
python3 "<skill directory>/scripts/init_skill.py" my-skill --path "<source directory>" --resources scripts,references
```

The initializer creates a source skill only. It never installs the skill, overwrites an existing folder, or changes workspace permissions. Request resource folders only when they will be used. If examples are created, replace or remove them before shipping.

### Write the instructions

Write a concise description that says what the skill does and when it applies. Put the desired outcome, non-obvious context, genuine constraints, and useful references in the body. Do not prescribe an arbitrary number of steps or a fixed structure unless variation would create a concrete problem.

For multi-stage work, read [workflows.md](references/workflows.md). For an output another program must consume, read [output-patterns.md](references/output-patterns.md).

### Validate and iterate

Validate the completed source skill with:

```bash
python3 "<skill directory>/scripts/quick_validate.py" "<source skill directory>"
```

The validator checks the portable format and unfinished placeholders. It does not prove that the instructions make good decisions. Also check that the description is specific, the references are discoverable, and every added script actually works.

Improve the skill using a demonstrated failure or real usage. Prefer a narrow correction to collecting universal rules for every past incident.

## Tomcat-specific routes

- For portable frontmatter, byte limits, and validation rules, read [portable-skills.md](references/portable-skills.md).
- For packaging and the three installation scopes, read [tomcat-packages.md](references/tomcat-packages.md).
- A standalone skill does not become a plugin merely because it has a `plugins/` folder. Follow the package manifest rules when plugin code is intended.

Use `load_skill(name="skill-creator", file="references/<file>.md")` to load a reference when needed.

Installing is separate from creating. With an explicit session project root, `scope` installs into that project; without one, report that scope is unavailable. `agent` and `global` installations require their own user confirmation and audit trail. Never bypass installation by copying into a managed directory, changing a registry, or using a shell command as a substitute for the authorized installer.

An explorer is read-only. It can inspect a source skill and report validation evidence, but cannot claim it changed or installed anything.
