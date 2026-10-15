---
name: project-summary
description: Update the PROJECT-SUMMARY.md with current features, learnings, and Claude tools used. Triggers on "/project-summary" or requests to "update the project summary".
---

# Project Summary Generator

Update the project summary documentation to reflect the current state of the GDS-MCP project. This skill explores the codebase and generates a comprehensive summary for sharing with the wider team.

## Usage

```
/project-summary
```

## Step-by-Step Workflow

When invoked, follow these steps exactly:

### Step 1: Read the Template

Read the template at `.claude/skills/resources/project-summary-template.md` to understand the required structure.

### Step 2: Explore Current State

Gather information about:

1. **Project Structure** - Run `find` or `ls` to understand the current file structure
2. **Documentation Coverage** - Count files in `docs/`
3. **Recent Changes** - Read `CHANGELOG.md` for latest updates
4. **Package Info** - Read `package.json` for available scripts and dependencies
5. **MCP Configuration** - Read `mcp-config.json` and `mcp.json` for tool configuration
6. **Skills** - List skills in `.claude/skills/`
7. **Core Modules** - List files in `core/` and `mcp-server/`

### Step 3: Calculate Metrics

Count and calculate:
- Total documentation files per folder
- Total lines of documentation (approximate)
- Number of skills available
- Number of MCP tools configured
- Number of core modules

### Step 4: Identify Key Features

List all major features by examining:
- `core/*.js` - What generators/transformers exist
- `mcp-server/tools/*.js` - What MCP tools are available
- `.claude/skills/*/SKILL.md` - What skills are defined
- `scripts/*.js` - What CLI commands are available

### Step 5: Document Claude Tools Used

Identify all Claude/MCP integrations:
- Figma MCP (`mcp.figma.com`)
- GitMCP (`gitmcp.io`)
- Custom MCP servers
- Claude Code skills
- Any other integrations

### Step 6: Capture Learnings

Extract key learnings from:
- `CLAUDE.md` - Project constraints and patterns
- Code comments in `core/` files
- README documentation
- Architecture decisions evident in code structure

### Step 7: Generate Summary

Create/update `PROJECT-SUMMARY.md` at the repository root following the template structure:

1. **What It Is** - One-paragraph overview
2. **Key Features Built** - Table of features with descriptions
3. **Current Coverage** - Metrics on documentation generated
4. **Key Claude Tools Used** - Table of tools and their purpose
5. **Key Learnings** - Numbered list of insights
6. **Architecture Diagram** - ASCII diagram of system flow
7. **Quick Start** - Commands for team members to get started
8. **Recent Updates** - Last 3-5 changelog entries

### Step 8: Update Changelog

Add an entry to `CHANGELOG.md`:

```markdown
| Updated PROJECT-SUMMARY.md with current project state | 🟡 Updated | NA | NA | NA |
```

### Step 9: Report

Summarize what was updated:
- New features documented
- Updated metrics
- Any significant changes noted

## Output

**Single file updated:** `PROJECT-SUMMARY.md`

The summary should be:
- Concise but comprehensive
- Suitable for sharing in team channels (Slack, email)
- Updated with accurate metrics
- Reflecting the current state of the project

## Template Reference

Always follow the structure defined in `.claude/skills/resources/project-summary-template.md`
