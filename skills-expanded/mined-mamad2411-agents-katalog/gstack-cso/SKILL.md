---
name: gstack-cso
description: Security audit workflow for OPC code, providers, plugins, Electron surfaces, local HTTP bridges, filesystem access, and command execution.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# gstack-cso

Use this skill for a security review with OWASP and STRIDE lenses.

## Scope

Prioritize OPC-specific attack surfaces:

- Electron main/preload/renderer IPC
- Local provider bridges and localhost auth
- API key and token storage
- Plugin, hook, skill, and MCP loading
- Shell command construction and tool permissions
- File reads/writes, path traversal, symlinks, and workspace boundaries
- Prompt injection from web, files, tool output, or plugin content

## Workflow

1. Map the trust boundaries and data flows.
2. Identify assets: secrets, filesystem access, provider credentials, session state, command execution, and user prompts.
3. Review entrypoints that cross boundaries.
4. Test high-confidence concerns with direct code evidence.
5. Ignore speculative issues unless there is a concrete exploit path.

## Output

For each finding include:

- Severity
- Affected file or component
- Exploit scenario
- Evidence
- Recommended remediation

Also include a short "Not Findings" section for checked risks that are already mitigated.
