---
name: self-configure
description: |
  Configures Claude Code for the current project by executing the claude-code-setup-guide
  procedure: fetches the guide from GitHub, inspects the project, reads the chapters whose
  triggers match, and applies CLAUDE.md, permissions, hooks, and skills. Use at the start
  of work on a new or unconfigured project, or when asked to "set up Claude Code",
  "configure this project", or "self-configure".
allowed-tools: Read, Grep, Glob, Bash(curl -s https://raw.githubusercontent.com/AlexandrG539/claude-code-setup-guide/*), WebFetch(domain:raw.githubusercontent.com)
---

# Self-Configure This Project

Execute the configuration guide against the current project. The guide's README is the authoritative procedure — follow it exactly, including its boundaries table (always / ask first / never).

1. Fetch the machine-readable index:
   `curl -s https://raw.githubusercontent.com/AlexandrG539/claude-code-setup-guide/main/llms.txt`
   Then fetch the README it lists and follow "For Agents: Self-Configuration Procedure".
2. Shape of the procedure (the fetched README governs where they differ): inspect the project → read core chapters 1, 2, 4, 7 → read conditional chapters whose `read_when` matches → apply CLAUDE.md → permissions → plugins/MCP → hooks → skills/subagents, omitting template sections that don't apply to the project type → verify immediately-checkable state, and ask the user to confirm `/context` (Memory files section), `/permissions`, `/hooks` in a fresh session.
3. If any chapter's frontmatter `claude_code_version` is older than the installed `claude --version`, re-verify the affected claims against https://code.claude.com/docs before applying them.
4. Ask before overwriting any existing CLAUDE.md, settings file, or hook. Never delete existing configuration, and never write secrets into committed files.
5. Finish with a report: what was configured, which chapters were used, which conditional chapters were skipped and why, and what awaits fresh-session verification.
