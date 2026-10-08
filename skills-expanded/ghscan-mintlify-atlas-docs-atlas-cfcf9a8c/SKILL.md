---
title: 'desloppify update-skill'
description: 'Install or update the Desloppify skill document for AI coding tools'
---

## Overview

The `update-skill` command downloads and installs the Desloppify skill document, which provides AI coding assistants (like Claude, Cursor, Windsurf) with instructions for working with Desloppify projects. This enables AI tools to understand Desloppify commands, workflows, and output formats.

## Usage

```bash
desloppify update-skill [interface]
```

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `interface` | No | Target AI tool interface: `cursor`, `windsurf`, `cline`, `roo-cline`, or `opencode` |

## Behavior

**Without interface argument:**
- Detects existing skill document installation
- Updates in place using the same interface
- If no installation found, lists available interfaces

**With interface argument:**
- Installs or updates skill for the specified interface
- Creates target file if it doesn't exist
- Preserves existing content in shared files

## Supported interfaces

<AccordionGroup>
  <Accordion title="cursor">
    **Target file:** `.cursorrules`
    
    Shared file that may contain other project rules. Desloppify section is inserted between `<!-- desloppify-begin -->` and `<!-- desloppify-end -->` markers.
  </Accordion>

  <Accordion title="windsurf">
    **Target file:** `.windsurfrules`
    
    Shared file with marker-based section insertion.
  </Accordion>

  <Accordion title="cline">
    **Target file:** `.clinerules`
    
    Shared file with marker-based section insertion.
  </Accordion>

  <Accordion title="roo-cline">
    **Target file:** `.roo-cline`
    
    Shared file with marker-based section insertion.
  </Accordion>

  <Accordion title="opencode">
    **Target file:** `.opencode/DESLOPPIFY.md`
    
    Dedicated file containing only Desloppify instructions.
  </Accordion>
</AccordionGroup>

## Examples

### First-time installation

```bash
# List available interfaces
desloppify update-skill

# Install for Cursor
desloppify update-skill cursor

# Install for OpenCode
desloppify update-skill opencode
```

### Updating existing installation

```bash
# Auto-detect and update
desloppify update-skill

# Output:
# Downloading skill document (cursor)...
# Updated .cursorrules (v2.1, tool expects v2.1)
```

### Switching interfaces

```bash
# Install for different interface
desloppify update-skill windsurf

# Old installation in .cursorrules remains
# New installation created in .windsurfrules
```

## What's included

The skill document contains:

- **Command reference** - All Desloppify CLI commands and options
- **Workflow patterns** - Common task sequences (scan → fix → test)
- **Output format guide** - How to parse JSON reports and console output
- **Error handling** - Common errors and troubleshooting steps
- **Language-specific notes** - Detector capabilities per language

## Version management

<Info>
The skill document is versioned independently from the Desloppify CLI. The command shows both versions after updating:

```
Updated .cursorrules (v2.3, tool expects v2.1)
```

- **Downloaded version (v2.3)** - Latest from GitHub
- **Expected version (v2.1)** - Version your CLI was built against

Minor version mismatches are usually fine. Major version differences may indicate outdated CLI.
</Info>

## Update source

Skill documents are downloaded from:
```
https://raw.githubusercontent.com/peteromallet/desloppify/main/docs/
```

Files:
- `SKILL.md` - Core skill content
- `SKILL-OVERLAY-{interface}.md` - Interface-specific additions (if any)

## Shared file handling

For shared configuration files (`.cursorrules`, `.windsurfrules`, etc.):

1. **First install** - Desloppify section is appended to existing content
2. **Updates** - Content between markers is replaced, surrounding text preserved
3. **Markers** - Section boundaries:
   ```markdown
   <!-- desloppify-begin -->
   ... Desloppify instructions ...
   <!-- desloppify-end -->
   ```

**Example `.cursorrules` with mixed content:**
```markdown
# Project-specific rules

Use TypeScript strict mode.

<!-- desloppify-begin -->
<!-- desloppify-skill-version: 2.1 -->

# Desloppify Integration
...
<!-- desloppify-end -->

# More project rules
Prefer functional components.
```

## Troubleshooting

<AccordionGroup>
  <Accordion title="Download failed: URLError">
    **Cause:** Network connectivity issue or GitHub unavailable.
    
    **Solution:**
    1. Check internet connection
    2. Try again in a few minutes
    3. Verify access to `github.com`
  </Accordion>

  <Accordion title="Downloaded content doesn't look like a skill document">
    **Cause:** GitHub returned unexpected content (404, redirect, etc.).
    
    **Solution:**
    1. Verify Desloppify repository exists at specified URL
    2. Check for renamed or moved files
    3. Report issue if persistent
  </Accordion>

  <Accordion title="Unknown interface 'xyz'">
    **Cause:** Interface name not recognized.
    
    **Solution:** Use one of the supported interfaces: `cursor`, `windsurf`, `cline`, `roo-cline`, or `opencode`.
  </Accordion>

  <Accordion title="No installed skill document found">
    **Cause:** Running `update-skill` without arguments when no installation exists.
    
    **Solution:** Specify an interface:
    ```bash
    desloppify update-skill cursor
    ```
  </Accordion>
</AccordionGroup>

## When to use

<Steps>
  <Step title="Initial setup">
    After installing Desloppify in a project, install the skill for your AI tool:
    ```bash
    desloppify update-skill cursor
    ```
  </Step>

  <Step title="Regular updates">
    Periodically update to get latest command reference and workflows:
    ```bash
    desloppify update-skill
    ```
  </Step>

  <Step title="CLI upgrades">
    After upgrading Desloppify CLI, update the skill to match:
    ```bash
    pip install --upgrade desloppify
    desloppify update-skill
    ```
  </Step>
</Steps>

## Related commands

- [`desloppify config`](/commands/config) - Configure Desloppify behavior
- [`desloppify scan`](/commands/scan) - Run analysis (what AI tools will invoke)
