---
name: redis-7-security-review
description: Reviews Redis 7 ACLs, network exposure, credentials, TLS, dangerous commands, sensitive data boundaries, MCP access, and agent command safety. Use when auditing Redis security, secrets, or privacy-sensitive Redis data.
license: MIT
compatibility: Requires Redis Open Source 7.x context. Hook script requires Python 3.
---

# Redis 7 Security Review

Use this skill when reviewing Redis 7 security posture, ACLs, command exposure, secrets, sensitive data, or agent access.

## Workflows

- `workflows/security-review-workflow.md`: Use for a structured Redis 7 security review.
- `workflows/sensitive-data-review-workflow.md`: Use when Redis data may contain secrets, regulated data, high-trust identifiers, or linkable values.

## Resources

- `resources/acl-template.md`: Starter ACL template with placeholders only.
- `resources/sensitive-data-checklist.md`: Checklist for Redis data sensitivity and leakage review.

## Script

- `scripts/redis-7-command-guard.py`: Hook helper for risky Redis shell commands.

Run the script with `--help` before manually using it.

## Review Priorities

1. Network exposure.
2. Authentication and ACLs.
3. Secret handling.
4. TLS or private encrypted path.
5. Dangerous command restrictions.
6. Sensitive data in keys, values, logs, dumps, backups, slowlog, and MCP responses.
7. Persistence and backup security.
8. MCP and agent access scope.
9. Production runbook approvals.

## Redis MCP Safety

The Redis MCP server can give agents direct Redis access. Keep it disabled until the endpoint, credentials, command scope, and environment are explicitly approved. Prefer development or staging instances for MCP access. Treat production MCP access as privileged operational access.

## Agent Safety

- Require approval before destructive commands.
- Do not paste secrets into prompts.
- Do not inspect large production keyspaces with blocking commands.
- Do not write test data to production Redis unless a runbook explicitly allows it.
- Prefer read-only diagnostics first.
