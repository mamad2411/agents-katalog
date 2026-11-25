---
name: cli-banners-and-versioning
description: Define a polished CLI with Commander, chalk-styled banners, versioning, and subcommands.
---

# Cli Banners And Versioning

Define a polished CLI with Commander, chalk-styled banners, versioning, and subcommands.

## When to Use

Use this skill when:

- Working with code in `src/main.ts/`
- User mentions "cli"
- User mentions "commander"
- User mentions "banner"
- User mentions "help"
- User mentions "version"

## Patterns

- Commander program initialization
- chalk banner and help text injection
- subcommand registration with options
- semantic version setting

## Examples

```
program.name('agentsmith').version('0.3.0').addHelpText('beforeAll', banner);
```

## Category

**patterns** - Common code patterns and conventions
