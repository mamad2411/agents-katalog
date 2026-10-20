---
name: wp-playground-environment
description: Selects, starts, and reviews WordPress Playground browser or CLI environments, mounts, persistence, version targets, snapshots, and fallback decisions.
---

# WordPress Playground environment

Use this skill when the agent must start or review a Playground environment, choose between browser/CLI modes, mount a project, preserve/reset state, or decide that Playground is unsuitable.

## Required inputs

- Project root and likely project type.
- Desired WordPress and PHP targets.
- Local development, CI, demo, snapshot, or reproduction purpose.
- Persistence requirements.
- Build requirements and whether generated artifacts exist.
- Port and browser constraints.
- Whether native services or extensions are required.

## Procedure

1. Run the project inspector with `--help`, then inspect the repository.
2. Classify the project as plugin, theme, `wp-content`, full WordPress, monorepo, or unknown.
3. Read `resources/environment-decision-matrix.md`.
4. Choose:
   - browser Playground for a public one-click demo;
   - `start` for simple persistent local work;
   - `server` for custom mounts, CI, or multiple components;
   - `run-blueprint` for setup/validation without serving;
   - `build-snapshot` for portable reproduction;
   - `php` for PHP entry points or PHPUnit;
   - a non-Playground stack when runtime fidelity is required.
5. Confirm Node.js and inspect current CLI help.
6. Pin WordPress/PHP and CLI versions when the result will be committed or shared.
7. Use Windows-safe mount flags when colon-based host/VFS syntax is ambiguous.
8. Start the environment and verify the mounted component is active.
9. Record persistence location and cleanup/reset behavior.
10. Preserve command, versions, Blueprint, and diagnostics.

## Workflow

Use `workflows/start-playground-environment-workflow.md` for the complete sequence.

## Resources and examples

- `resources/environment-decision-matrix.md`
- `examples/powershell-cli-examples.md`

## Script

Run:

```powershell
python .\.agents\plugins\wp-playground\skills\wp-playground-environment\scripts\inspect-playground-project.py --help
```

The script is read-only. It reports evidence and recommendations; it does not run npm, modify files, or prove the project works.
