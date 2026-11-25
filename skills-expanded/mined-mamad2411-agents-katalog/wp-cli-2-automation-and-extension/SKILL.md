---
name: wp-cli-2-automation-and-extension
description: Designs WP-CLI 2 configuration, aliases, remote automation, and custom commands. Use when reviewing wp-cli.yml files, scripting machine-readable WP-CLI output, running across remote targets, or implementing and testing a reusable custom WP-CLI command.
license: MIT
compatibility: Requires WP-CLI 2.x; guidance is validated against WP-CLI 2.12.0. The optional audit script requires Python 3.10 or newer.
---

# WP-CLI 2 Automation and Extension

Use this skill for repeatable automation and custom command implementation after command and target safety are understood.

## Configuration Review

1. Resolve command-line, local, project, and global config precedence.
2. Review aliases for transport, host, path, URL, user, environment, and fan-out.
3. Treat `require` and `exec` as code-execution boundaries.
4. Keep secrets out of YAML and command lines.
5. Keep `wp-cli.local.yml` untracked when it contains machine-local values.

Run the static scanner before changing configuration:

```powershell
python .agents/plugins/wp-cli-2/skills/wp-cli-2-automation-and-extension/scripts/wp-cli-config-audit.py --help
python .agents/plugins/wp-cli-2/skills/wp-cli-2-automation-and-extension/scripts/wp-cli-config-audit.py . --strict
```

## Automation Design

- Prefer JSON, CSV, count, or IDs output over parsing tables.
- Verify exit codes and distinguish no-op from failure.
- Use explicit targets and bounded lists; avoid accidental `@all` fan-out.
- Make retries safe and idempotent.
- Avoid shell interpolation of untrusted values.
- Record target and outcome without credentials or personal data.

## Custom Command Design

- Register through documented WP-CLI APIs.
- Keep selection, validation, mutation, and output separate.
- Provide documented synopsis and examples.
- Require explicit confirmation for destructive behavior.
- Use batches and progress carefully for large datasets.
- Add Behat-oriented functional tests and machine-readable output.

## Workflows

- [Remote automation workflow](workflows/remote-automation-workflow.md)
- [Custom command development workflow](workflows/custom-command-development-workflow.md)

## Resource

- [Configuration and custom command reference](resources/config-and-custom-command-reference.md)
