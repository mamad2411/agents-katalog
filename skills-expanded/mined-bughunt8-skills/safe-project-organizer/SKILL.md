---
name: safe-project-organizer
description: Analyze a repository and propose conservative structural cleanup. Use for requests to organize a project, clean its root directory, remove empty directories, or prepare a codebase handoff.
---

# Safe Project Organizer

Inspect a project and make organization changes only after the user has reviewed a complete preview and explicitly approved execution.

## Safety rules

1. Start with a read-only scan. Do not modify files during analysis.
2. Never touch protected paths: version-control metadata, dependency directories, virtual environments, build outputs, caches, secrets, environment files, or lock files.
3. Treat source-code moves as out of scope. They can invalidate imports, build configuration, and tooling assumptions.
4. Show every proposed path and action before requesting approval.
5. Use a dry run before real execution.
6. Require the user to type `yes` for real execution.
7. Run the project's relevant validation commands after any approved changes.

## Workflow

Run commands from the repository root, replacing `<project>` with the project to inspect.

### 1. Scan

```bash
python3 skills/engineering/safe-project-organizer/scripts/project_organizer.py <project> --scan
```

This is read-only. It reports files, directories, protected items, empty directories, and root-level documentation candidates.

### 2. Analyze and preview

```bash
python3 skills/engineering/safe-project-organizer/scripts/project_organizer.py <project> --preview
```

The preview proposes only conservative actions:

- move eligible root documentation into `docs/`;
- remove truly empty, unprotected directories;
- create `docs/` when documentation moves need it.

`README.md`, license files, changelogs, root configuration, and all protected paths stay in place. Review the complete output, including risk labels and paths, with the user.

### 3. Simulate execution

```bash
python3 skills/engineering/safe-project-organizer/scripts/project_organizer.py <project> --execute
```

This repeats the preview and validates the planned operations without changing the filesystem.

### 4. Execute only with explicit approval

After the user has reviewed the preview and dry run, run:

```bash
python3 skills/engineering/safe-project-organizer/scripts/project_organizer.py <project> --execute-real
```

The script asks for `yes` before applying the plan. It records the result in `.project_organizer.log` at the inspected project's root. Moves and created directories include rollback instructions in that log; deleted empty directories are recorded so they can be recreated.

## How to assess suggestions

- **Low risk:** creating a missing `docs/` directory or removing a verified empty directory.
- **Medium risk:** moving a documentation file, because links or automation may reference its old path.
- **High risk:** not generated automatically. Discuss a project-specific plan instead.

Do not execute suggestions that conflict with repository conventions, published documentation paths, deployment tooling, or user intent. If the requested reorganization needs source-code moves, dependency changes, or broad renames, prepare a separate, repository-aware plan and validate it incrementally.

## Protected paths

The organizer protects:

- `.git`, `.svn`, `.hg`;
- `node_modules`, `vendor`, `venv`, `.venv`, and `__pycache__`;
- `dist`, `build`, `.next`, `.nuxt`, and `out`;
- `.env*`, `secrets.*`, `credentials.*`;
- common lock files and all `*.lock` files.

The script also rejects any operation whose resolved source or destination would escape the requested project root.

## Attribution

This skill is adapted from the MIT-licensed [Safe Project Organizer](https://github.com/endlessblink/claude-dev-infrastructure/tree/138ec5abb7918236e7fc12e4b84ee7288edc59f2/skills/safe-project-organizer) by endlessblink. See [ATTRIBUTION.md](ATTRIBUTION.md) and [LICENSE](LICENSE).
