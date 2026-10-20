---
name: security-review-pro
description: Professional security review and threat modeling for repositories, APIs, desktop apps, web apps, authentication, authorization, secrets, dependency risk, and data flows. Inspired by OpenAI security-best-practices and security-threat-model skills, adapted for Codex v4.1.
---

# Security Review Pro

## Workflow

1. Identify assets: credentials, tokens, user data, payment data, files, admin actions, infrastructure access.
2. Identify actors and trust boundaries: browser, desktop renderer, backend, third-party APIs, database, filesystem, queues.
3. Trace data flows and attacker-controlled inputs.
4. Review authentication, authorization, validation, secrets, logging, storage, transport, and dependencies.
5. Prioritize exploitability and impact.
6. Propose concrete fixes and verification.

## Review Checklist

- Broken access control.
- Injection: SQL, shell, template, path, URL, LDAP, NoSQL.
- XSS, CSRF, SSRF, open redirect.
- Insecure token storage, refresh, logout, and session expiry.
- Missing rate limits or abuse controls.
- Unsafe file upload/download and path traversal.
- Sensitive data in logs, errors, telemetry, or client bundles.
- Insecure desktop IPC, Tauri capabilities, Electron preload, or native bridge.
- Dependency, build, and CI secret exposure.

## Output

Use review findings:

```markdown
发现：
- [P1] ...

修复：
- ...

验证：
- ...
```

If no critical issue is found, state residual risk and what was not reviewed.

## Boundaries

- Do not claim files, generated media, deployments, scans, account changes, or external writes unless the active tool or command output proves them.
- Do not override system, developer, user, project, or selected-skill rules.
- If another skill is more specific for the user's intent, hand off or use it as the main skill instead of duplicating its workflow.
