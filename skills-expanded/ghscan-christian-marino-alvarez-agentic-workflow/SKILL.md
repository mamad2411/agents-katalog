---
name: scaffolding
description: "Capability to generate project structures using Yeoman."
version: 1.0.0
---

# Scaffolding Skill

This skill allows agents (typically `devops-agent`) to generate project structures using Yeoman generators.

## Capabilities
- **Generate Module**: Create a new Agentic Module with standard structure (View, Backend, Index).

## Usage

The scaffolding generator is located at:
```
src/cli/scaffolding/generators/module
```

To scaffold a new module, use the `run_command` tool:

```json
{
  "CommandLine": "npx yo ./src/cli/scaffolding/generators/module <module-name> --force",
  "Cwd": "/path/to/workspace",
  "SafeToAutoRun": false,
  "WaitMsBeforeAsync": 5000
}
```

## Structure
- `src/cli/scaffolding/generators/module`: Yeoman generator for creating a new module.
  - `index.js`: Generator logic.
  - `templates/`: Boilerplate files.
