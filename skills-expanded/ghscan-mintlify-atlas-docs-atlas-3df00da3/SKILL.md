---
title: bool skill
description: Install the Bool CLI skill for AI agents
---

The `bool skill` command installs the Bool CLI agent skill into your project, enabling AI agents to understand and use Bool CLI commands.

## Usage

```bash
bool skill [directory] [--output <path>]
```

<ParamField path="directory" type="string" default=".">
  Target directory for skill installation
</ParamField>

<ParamField path="--output" type="string">
  Custom output path for the skill folder (overrides default location)
</ParamField>

## What it does

This command copies the Bool CLI skill files into your project's `.agents/skills/using-bool-cli/` directory. The skill contains:

- Instructions for AI agents on how to use Bool CLI
- Command reference and examples
- Best practices and workflows
- Integration patterns

## Examples

### Install to current directory

```bash
$ bool skill
✔ Skill installed to .agents/skills/using-bool-cli
ℹ Agents can now discover the bool-cli skill in your project.
```

The skill is installed to:
```
.
└── .agents/
    └── skills/
        └── using-bool-cli/
            ├── SKILL.md
            └── ...
```

### Install to specific directory

```bash
$ bool skill ~/my-project
✔ Skill installed to /home/user/my-project/.agents/skills/using-bool-cli
ℹ Agents can now discover the bool-cli skill in your project.
```

### Use custom output path

```bash
$ bool skill --output ~/custom/location
✔ Skill installed to /home/user/custom/location/.agents/skills/using-bool-cli
ℹ Agents can now discover the bool-cli skill in your project.
```

## How agents use skills

AI agents that support the `.agents/skills/` convention can automatically discover and load the Bool CLI skill. This enables them to:

- Execute Bool CLI commands correctly
- Understand command options and flags
- Follow Bool CLI best practices
- Integrate Bool deployment into workflows

<Note>
  The skill is a local reference for agents. It doesn't require internet access or external dependencies.
</Note>

## Supported agents

The skill format is compatible with agents that follow the `.agents/skills/` specification, including:

- OpenCode
- Claude Code (with skill support)
- Other MCP-compatible agents

<Tip>
  After installing the skill, you can ask your AI agent: "Deploy this project to Bool" or "Show me my Bools" and it will understand how to use the CLI.
</Tip>

## Updating the skill

To update the skill to the latest version, run `bool skill` again in the same directory. It will overwrite the existing skill files.

```bash
$ bool skill
✔ Skill installed to .agents/skills/using-bool-cli
ℹ Agents can now discover the bool-cli skill in your project.
```