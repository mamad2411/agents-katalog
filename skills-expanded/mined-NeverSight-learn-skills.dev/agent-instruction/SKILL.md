---
name: agent-instruction
description: Manage AI instruction files in monorepos during development sessions. Use when the user says "add rule", "update CLAUDE.md", "update AGENTS.md", "list instruction rules", "build instruction files", or "show available rules".
author: Kyle Davis
version: 1.0.0
---

# agent-instruction

Manage AI instruction files in monorepos during development sessions. This skill bridges the gap between discovering best practices during development and codifying them as durable instructions.

Use the `agent-instruction` CLI to add rules, build instruction files, and list existing rules.

**Requires:** `agent-instruction` CLI installed and in PATH (`go install github.com/validkeys/agent-instruction@latest`)

## Commands

### add_rule

Add a new instruction rule to a rule file.

```bash
agent-instruction add "[rule content]" --title "[title]" --rule="[rule-file]"
```

- `content` (required): The instruction rule text
- `--title` (optional): Heading for the rule section
- `--rule` (optional): Target rule file name (prompts interactively if omitted)

Examples:
```bash
agent-instruction add "Always use table-driven tests in Go" --title="Testing Standards" --rule="testing"
agent-instruction add "Never use global variables" --title="Code Standards"
agent-instruction add "Validate all user input before database queries" --rule="security"
```

### build

Generate or update instruction files (CLAUDE.md, AGENTS.md) from all rule configurations.

```bash
agent-instruction build
```

### list

Display all available rule files and their contents.

```bash
agent-instruction list [--verbose]
```

- `--verbose` (optional): Show full rule content with formatting

## Best Practices

- **Check before adding:** Run `agent-instruction list --verbose` before adding a rule to avoid duplicates.
- **Build after changes:** After adding multiple rules, run `agent-instruction build` to propagate changes to CLAUDE.md and AGENTS.md.
- **Use descriptive titles:** Clear, specific titles make rules easy to find later.
- **Group related rules:** Use category-named rule files — e.g., `testing.json`, `security.json`, `golang.json`, `global.json`.
- **When to add rules:** When the user says "remember this for next time", when a recurring mistake is found, or when a new standard is established.

## Notes

This skill requires the `agent-instruction` CLI to be installed and available in PATH. The CLI manages rule files in the `.agent-instruction/` directory and builds instruction files at the repository root.
