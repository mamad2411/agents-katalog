# spec-expert-role-skill: Expert role skill and implementation expert bodies

**Master:** [Specifications](README.md)
**Covers:** req-roles-follow-model
**Context:** context-factory

## Description

The `expert-role` skill tells an agent how to set up an implementation expert for one component.
Its files are in `services/factory/composition/artifact-driven/_assets/agent/skill/by-role/solution-expert/expert-role/`.
The reference `references/role-template.md` gives the body template of an expert and one filled
example. The template tells the expert to read the tasks of a feature from a root `tasks/` folder.
That folder does not exist in the layout of spec-artifact-layout.

The template, the skill rules, and the two implementation expert bodies of this repository change
so that an expert reads the tasks of a change and the current version of the feature. The two
bodies `utils/agent/role/factory-expert/ROLE.md` and `utils/agent/role/nix-lib-expert/ROLE.md`
are not factory assets. They are the bodies of this repository. They follow the template, so they
get the same change.

## Contract

### The role body template

In `references/role-template.md`, the Read first bullet of the template changes. Old lines 23
and 24:

```markdown
- `docs/artifact/feat-<name>/tasks/`, the tasks of the feature. Read the specifications and the
  requirements that each task covers.
```

New lines:

```markdown
- `docs/artifact/feat-<name>/changes/change-<name>/tasks/`, the tasks of the change. Read the
  specifications and the requirements that each task covers. A file that is not in the change is
  in `versions/<current>/` of the feature.
```

The Read first line of the example changes. Old line 77:

```markdown
- `docs/artifact/feat-<name>/tasks/`, `AGENTS.md`, and `docs/domain/context-orders/README.md`.
```

New line:

```markdown
- `docs/artifact/feat-<name>/changes/change-<name>/tasks/`, `AGENTS.md`, and `docs/domain/context-orders/README.md`.
```

The example line stays on one line. The example keeps 40 lines or fewer from its title line to
the end of the file, as spec-role-template of `feat-expert-role-skill` requires.

After the change, the file does not contain the string `feat-<name>/tasks/`. The rest of the
file is unchanged: the seven headings, their order, and the text before the template.

### The skill file

In `SKILL.md`, the frontmatter is unchanged. The `name` is `expert-role`. In `## Rules`, the line
about phases 2 and 3 stays:

```markdown
- The expert gives `spec-<name>.md` and `task-<name>.md` to the solution expert in phases 2
  and 3. The expert does not write `specifications/README.md` or `tasks/README.md`.
```

One rule is added after it:

```markdown
- The expert reads the tasks of a change and the current version of the feature. The expert
  does not write in `versions/`.
```

The rest of `SKILL.md` is unchanged.

### The implementation expert bodies of this repository

The files `utils/agent/role/factory-expert/ROLE.md` and `utils/agent/role/nix-lib-expert/ROLE.md`
get the same Read first bullet replacement as the template. In each file, old lines 12 and 13:

```markdown
- `docs/artifact/feat-<name>/tasks/`, the tasks of the feature. Read the specifications and the
  requirements that each task covers.
```

New lines:

```markdown
- `docs/artifact/feat-<name>/changes/change-<name>/tasks/`, the tasks of the change. Read the
  specifications and the requirements that each task covers. A file that is not in the change is
  in `versions/<current>/` of the feature.
```

The rest of each body is unchanged. `devenv.local.nix` reads each body with `builtins.readFile`.
The shell renders the role file of each harness in use when it starts. The rendered files under
`.claude/agents/` are not sources.

### Names

The template, the skill, and the bodies use the terms of spec-artifact-layout: change,
`changes/change-<name>/tasks/`, current version, `versions/<current>/`.

## Errors

- `references/role-template.md` contains the string `feat-<name>/tasks/`. The template tells the
  expert to read a folder that spec-artifact-layout does not have. Correct the template. The
  check of this string in `tests/eval.nix` is in spec-eval-checks.
- A body in `utils/agent/role/` names a root `tasks/` folder of a feature, for example
  `docs/artifact/feat-<name>/tasks/`. The body does not follow the template. Correct the body.
- `SKILL.md` does not have the frontmatter `name: expert-role`. The check `skillFrontmatter` in
  `tests/eval.nix` fails.
- `references/role-template.md` names `services/factory`, `libs/nix`, or `nix-instantiate`. The
  check `skillIsGeneric` in `tests/eval.nix` fails.
