---
name: ai-skill-auditor
description: A universal, dependency-free Node.js tool to statically audit AI Skills and local agents for malicious patterns. 
---

# `ai-skill-auditor`

This skill provides the AI Assistant the capability to automatically audit and review local code directories (such as other downloaded AI Skills) looking for standard malicious patterns (eval, destructive child_process, hidden HTTP requests) before running them. 

## Instructions for the AI Assistant:
When the user asks you to "audit a skill", "check a folder for security", or "verify the integrity of this downloaded repo":

1. Use the `run_command` tool to execute the central audit script.
2. The argument is the path the user wants to audit.
   - Example 1: `node {workspaceRoot}/smartbrain-skill-auditor/bin/audit.js "C:/path/to/target/skill"`
   - Example 2 (If auditing the current folder): `node {workspaceRoot}/smartbrain-skill-auditor/bin/audit.js .`

3. Wait for the terminal output. 
4. If it returns 0 vulnerabilities, tell the user the audit passed and provide them with the SMARTbrain Security Badge returned by the console.
5. If it returns vulnerabilities, explicitly list the files and the malicious patterns found so the user can review them manually. DO NOT run any script in that folder without user consent.
