---
name: workspace-manager
description: Automatically organizes repository structure, routes incoming files, and enforces Git hygiene.
---

# Workspace Manager Skill

This skill allows the agent to maintain, structure, and route files within the workspace directory.

## Core Operations

1. File Routing:
   - Move software projects to `workspace/projects/`
   - Move homelab & lab documentation to `workspace/docs/`
   - Move CTF & malware reports to `workspace/writeups/`
   - Move reference snippets and cheatsheets to `workspace/notes/`

2. Formatting Standard:
   - Strictly plain ASCII formatting.
   - Avoid unicode characters or non-standard symbols.
