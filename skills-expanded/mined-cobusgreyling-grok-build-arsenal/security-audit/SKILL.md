---
name: security-audit
description: |
  Perform focused security reviews on code, diffs, hooks, and MCP servers.
  Look for auth issues, injection, secret leakage, unsafe tool/MCP usage, and hook risks.
  Use for any change involving external input, credentials, or agent capabilities.
  Triggers: "security review", "audit this diff", "check for vulnerabilities".
version: 1.0.0
author: Cobus Greyling
---

# Security Audit

Treat every hook, MCP, and agent capability as high-risk.

## Checklist (always cover these)

- Hard-coded secrets or credentials
- Unsafe command execution or shell injection
- Path traversal or arbitrary file access
- Insufficient input validation / sanitization
- Overly broad permissions in MCP servers or hooks
- Trust model for project-provided hooks/skills
- Data exfiltration risks (especially in research or browser MCPs)
- Logging of sensitive information

## Process

1. Identify the trust boundary for the change.
2. Trace data from untrusted sources (user input, files from disk, network, session logs).
3. Flag anything that can lead to code execution or secret access.
4. Propose the smallest hardening changes.
5. Recommend tests or verification steps (e.g. "try to escape the sandbox").

## When Working on Meta-Tooling

Extra scrutiny for anything that will run inside other people's agent sessions (skills, MCPs, hooks in this arsenal itself).

Always pair with `plan-mode-orchestrator` for security-related work.
