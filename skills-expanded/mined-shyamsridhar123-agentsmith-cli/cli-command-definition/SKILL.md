---
name: cli-command-definition
description: Define CLI commands, arguments, and options using commander with styled banners and versioning.
---

# Cli Command Definition

Define CLI commands, arguments, and options using commander with styled banners and versioning.

## When to Use

Use this skill when:

- Working with code in `src\main.ts/`
- User mentions "cli"
- User mentions "command"
- User mentions "commander"
- User mentions "agentsmith"
- User mentions "main"

## Patterns

- commander program setup with .command().argument().option().action()
- chalk-based banner and colored output
- semantic versioning via .version() and help text via .addHelpText()

## Examples

```
program.command("assimilate").argument("<target>").option("-n, --dry-run").action(assimilateCommand);
```

## Category

**architecture** - Structural patterns and system design
