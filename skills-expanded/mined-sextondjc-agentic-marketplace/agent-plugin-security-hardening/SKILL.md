---
name: agent-plugin-security-hardening
description: Apply security controls to agents including sandbox configuration, SSRF prevention, secret management, input validation, and permission hardening.
---

# Agent Security Hardening

## Specialization

Harden agent security posture through explicit controls on external access (SSRF prevention), secret management, tool permissions, sandbox configuration, and input validation. This skill is a peer to implementation and must be applied before release.

## Supporting Activities

- Audit tool permissions and remove unnecessary access.
- Prevent Server-Side Request Forgery (SSRF) via URL validation.
- Implement secret management (environment variables, vault integration).
- Configure sandbox constraints on MCP servers and shell execution.
- Validate user input at agent boundaries.
- Document security assumptions and incident response.
- Perform threat modeling and security checklist validation.

## Workflow

1. **Audit tool permissions** (deny-by-default):
   - Review agent's tool whitelist from design and implementation.
   - For each tool, confirm justification: Is it essential for the agent's purpose?
   - Remove any tool not strictly necessary.
   - Example: Code reviewer should NOT have `edit` or `execute` tools.
   - Document: `tools/authorization-matrix.md` with tool → agent → justification.

2. **Prevent SSRF vulnerabilities**:
   - Identify all `web/fetch` or `http` tool usage in agent instructions.
   - Add URL validation rules:
     ```
     Approved domains: api.github.com, docs.microsoft.com
     Blocked patterns: localhost, 127.0.0.1, 192.168.*, 10.0.0.0/8, file://, gopher://, ftp://
     Blocked protocols: file, gopher, ftp (allow only https)
     ```
   - Document in agent instructions: "Never fetch from internal networks or local machine."
   - If custom tool handles web requests, add URL validation code (check before fetch):
     ```
     1. Parse URL.
     2. Check hostname against blocklist and allowlist.
     3. Block if matches private IP range (RFC 1918) or local host.
     4. Block non-HTTP(S) protocols.
     5. Allow fetch only if all checks pass.
     ```

3. **Manage secrets**:
   - Audit: Are any secrets hardcoded in agent instructions, plugin.json, or `.mcp.json`?
   - Refactor: Move all secrets to environment variables or vault service.
   - Plugin secret access:
     ```json
     {
       "mcpServers": {
         "api-client": {
           "command": "node",
           "args": ["server.js"],
           "env": {
             "API_KEY": "${env:MY_API_KEY}"  // Loaded from environment
           }
         }
       }
     }
     ```
   - TypeScript agent secret access:
     ```typescript
     const apiKey = process.env.MY_API_KEY;
     if (!apiKey) {
       throw new Error('MY_API_KEY environment variable not set');
     }
     ```
   - Document: `.env.example` with placeholder variable names (NO actual values).
   - CI/CD integration: Store secrets in GitHub Secrets, pass to job via environment.

4. **Configure sandbox constraints** (MCP servers; macOS/Linux only):
   ```json
   {
     "mcpServers": {
       "sandboxed-server": {
         "command": "node",
         "args": ["server.js"],
         "sandboxEnabled": true,
         "sandbox": {
           "filesystem": {
             "allowRead": ["${workspaceFolder}"],
             "allowWrite": ["${workspaceFolder}/build"],
             "denyRead": ["/etc/passwd", "/root"],
             "denyWrite": ["/usr/bin", "/etc"]
           },
           "network": {
             "allowedDomains": ["api.github.com", "api.example.com"],
             "deniedDomains": ["internal-proxy.corp"]
           }
         }
       }
     }
   }
   ```
   - Principle: Allow ONLY what is needed; deny everything else.
   - File access: whitelist specific directories (workspace, temp, config only).
   - Network access: whitelist specific domains (deny internal networks).

5. **Input validation at boundaries**:
   - In agent instructions, add explicit validation guidance:
     ```
     Before processing user input:
     1. Check length: Reject input > 10KB (prevent resource exhaustion).
     2. Check encoding: Accept UTF-8 only.
     3. Check format: If expecting file path, validate against path traversal (no ../ or absolute paths outside workspace).
     4. Check type: If expecting JSON, validate schema before parsing.
     5. If validation fails, reject input and ask user to retry with valid data.
     ```
   - TypeScript agents: Use Syrx guards or equivalent validation library (zod, yup, joi).

6. **Restrict terminal execution**:
   - If agent uses `execute` tool, limit to safe commands:
     ```jsonc
     {
       "chat.tools.terminal.autoApprove": {
         "git status": true,
         "git show": true,
         "find": true,
         "/^npm (list|view)$/": true,  // Read-only npm commands
         "rm": false,
         "sudo": false,
         "curl": false
       }
     }
     ```
   - Deny by default: auto-approve only commands that don't modify system state.
   - Document: TERMINAL.md with safe commands and rationale for each.

7. **Audit logging and telemetry**:
   - Ensure agent does NOT log secrets, PII, or sensitive file contents.
   - If agent generates logs, sanitize them:
     ```
     BAD:  "User provided API key: sk-1234567890"
     GOOD: "Authentication configured (via environment variable)"
     ```
   - Telemetry events should include: agent action, tool used, outcome (success/failure), not raw user input.
   - Example safe telemetry:
     ```
     {
       "eventType": "tool_invocation",
       "agentName": "code-reviewer",
       "toolName": "read",
       "success": true,
       "durationMs": 234
     }
     ```

8. **Security checklist** (before release):
   - [ ] Tool whitelist is minimal (deny-by-default).
   - [ ] No hardcoded secrets in any file (plugin.json, .agent.md, code).
   - [ ] SSRF prevention rules documented and tested.
   - [ ] Sandbox constraints configured for MCP servers.
   - [ ] URL allowlist/blocklist is explicit and tested.
   - [ ] Terminal auto-approval rules disable destructive commands.
   - [ ] Input validation is in place (length, encoding, type, format).
   - [ ] Logs and telemetry do not include secrets or PII.
   - [ ] Threat model is documented (what could go wrong? → mitigation).
   - [ ] Security review completed by peer or security team.

## Inputs

- Agent design with tool whitelist (from agent-plugin-design skill).
- Implementation code (TypeScript or .agent.md).
- Plugin configuration (plugin.json, .mcp.json).
- Threat model or security concerns (from org security policy).
- Secret management approach (environment variables, vault, CI/CD secrets).

## Required Outputs

- Audit report: tool permissions, SSRF rules, secret locations, sandbox config.
- Security hardening checklist (all items pass or documented exceptions).
- `.env.example` file (if using environment variables).
- TERMINAL.md or SECURITY.md documentation (safe commands, threat model, incident response).
- Validation evidence: SSRF test (malicious URL rejected), input validation test (oversized input rejected), secrets test (no secrets in logs).

## Done Criteria

- Tool whitelist is minimal and justified (no unnecessary access).
- No secrets are hardcoded (all moved to environment or vault).
- SSRF prevention is explicit (URL validation rules documented and tested).
- Sandbox constraints are applied to MCP servers (if present).
- Terminal auto-approval denies destructive commands (rm, sudo, del, etc.).
- Input validation is in place at agent boundaries.
- Logs and telemetry are sanitized (no secrets or PII).
- Security checklist is complete (all items pass or exceptions documented).
- Security review has been completed (peer or security team sign-off).

## Validation Checklist

- [ ] Agent tool whitelist has no tools beyond what is required.
- [ ] `grep -r "password\|secret\|api.key\|token" plugin.json .agent.md .mcp.json` returns no hardcoded values.
- [ ] SSRF rules explicitly list approved domains and blocked patterns.
- [ ] SSRF rules tested: malicious URLs (localhost, private IPs, file://) are rejected.
- [ ] Sandbox constraints are present for MCP servers and whitelist only necessary access.
- [ ] Terminal auto-approval rules deny `rm`, `sudo`, `del`, format, and equivalent destructive commands.
- [ ] Input validation rejects oversized input (>10KB), invalid encoding, path traversal attempts.
- [ ] Logs do not print secrets (search for $API_KEY, $PASSWORD, etc. in log statements).
- [ ] Telemetry events include only safe fields (no raw user input, secrets, or file contents).
- [ ] Security review completed and documented (name, date, findings, resolution).

## References

- [OWASP: Server-Side Request Forgery (SSRF)](https://owasp.org/www-community/attacks/Server-Side_Request_Forgery)
- [VS Code Security Documentation](https://code.visualstudio.com/docs/copilot/security)
- [MCP Sandbox Configuration](https://code.visualstudio.com/docs/copilot/security#_sandbox)
- [Secret Management Best Practices](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
- [OWASP Top 10: A03:2021 Injection](https://owasp.org/Top10/A03_2021-Injection/)

## Trigger Conditions

Invoke this skill when any of the following is true:

- An agent is ready for security review before release.
- Tool permissions need to be audited and restricted.
- SSRF or input validation vulnerabilities are suspected.
- Sandbox configuration for MCP servers is required.
- Secret management approach must be designed and validated.
- Agent handles sensitive data (code, user input, API credentials).

