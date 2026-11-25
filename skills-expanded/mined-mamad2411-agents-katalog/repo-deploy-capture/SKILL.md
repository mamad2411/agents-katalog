---
description: 'Capture a verified deployment workflow into project documentation or
  memory after a successful deploy. Use when a user asks to record deployment steps,
  save deploy lessons, document server update procedures, preserve health checks,
  or make future deployments repeatable. The skill is generic: reusable skill text
  must not include private project names, hostnames, domains, secrets, or user-specific
  infrastructure. Follows agent-native CI/CD with eval-gated promotion, canary rollouts,
  and compensating rollback actions.'
metadata:
  evolved: true
  evolved_at: '2026-07-20T14:07:06.279401+00:00'
name: repo-deploy-capture
tags:
- documentation
- infrastructure
- security
- deploy
version: 2
---

# Repo Deploy Capture

Record the concrete deployment path that just worked so the next agent can redeploy the same project without rediscovering commands, directories, checks, and pitfalls.

## Principles

1. Capture only verified facts from the current project or deployment run.
2. Keep reusable instructions generic; put project-specific details only in that project's docs or memory.
3. Never record secrets, API keys, tokens, private keys, passwords, cookies, or full sensitive environment values.
4. Prefer one authoritative deployment document over scattered notes.
5. Preserve exact commands only when they are safe to rerun or clearly labeled as examples requiring local confirmation.

## Workflow

### 1. Confirm Scope

Identify what should be captured:

- Project root and repository status.
- Deployment target type: local server, remote host, container platform, static hosting, PaaS, mobile/app release, or other.
- The deployment that actually succeeded.
- The user's preferred destination for notes: existing docs, new deploy doc, project memory, or both.

If no destination is specified, prefer an existing deployment document. If none exists, create the smallest suitable project-local doc such as `docs/deploy.md` or `docs/DEPLOY.md`, matching existing naming style.

### 2. Extract Verified Deployment Facts

Read only the current project context and recent commands/logs needed to capture:

- Source branch or release artifact used.
- Build/test commands that gate deployment.
- Deploy commands and working directories.
- Required runtime services and process manager.
- Configuration files that matter.
- Public or internal health checks.
- Browser or API smoke checks.
- Rollback or restart command, if known.
- Pitfalls encountered and the verified fix.

Do not invent missing steps. Mark unknowns as `TBD` only if the user explicitly wants a draft; otherwise leave them out.

### 3. Scrub Sensitive Details

Before writing, classify each detail:

- Keep: command shapes, relative paths, service roles, health-check endpoints without secrets, expected success signals.
- Generalize: private project names, private domains, host aliases, usernames, absolute home paths, internal repository names.
- Remove: credentials, tokens, API keys, private IPs when not necessary, full `.env` contents, customer/user data.

Use placeholders when a detail is necessary:

```text
<remote-host>
<deploy-dir>
<service-name>
<domain>
<health-url>
<env-file>
```

### 4. Write the Capture

Use a compact structure:

````markdown
# Deployment

## When To Use

Use this procedure to deploy this project after code changes have passed local verification.

## Prerequisites

- Access to `<remote-host>`.
- Required environment is already configured in `<env-file>`.

## Verification Before Deploy

```bash
<test-command>
<build-command>
```

## Deploy

```bash
<deploy-command>
```

## Verify

```bash
<health-check-command>
<smoke-check-command>
```

Expected success:

- `<service-name>` is running.
- `<health-url>` returns success.
- Main page or API smoke check works.

## Rollback / Recovery

```bash
<rollback-or-restart-command>
```

## Known Pitfalls

- Symptom: ...
  Cause: ...
  Fix: ...
````

Keep the document operational. Avoid generic deployment theory.

### 5. Update Memory Only When Appropriate

If the environment has a memory system and the user explicitly asks to update memory, write a concise memory note according to that system's rules. The memory entry should summarize reusable lessons and point to the project doc. Do not put secrets or private infrastructure details into a general-purpose skill.

### 6. Verify The Capture

After writing:

1. Re-read the doc.
2. Confirm no secrets leaked.
3. Confirm commands are copied accurately from verified evidence.
4. Confirm there is one clear deploy path, not conflicting alternatives.
5. Run repository formatting or markdown checks if the project has them.

## Output

Report:

- File updated.
- What deploy path was captured.
- Any unknowns intentionally omitted.
- Verification performed.

## Error Handling

- Always check the exit code or response status of commands before proceeding
- On failure, log the error details and attempt recovery if a retry strategy exists
- If recovery fails, report the error with context: what was attempted, what went wrong, and suggested next steps
- Never silently ignore errors — treat unexpected output as potential failure


## Verification

- After each step, verify the expected outcome before continuing
- Use idempotent checks: running the same action twice produces the same result
- If verification fails, roll back the last change and report the issue
- Log verification results for audit trail


## Rollback

- Every action should have a defined undo procedure
- If a step fails after partial completion, reverse all changes made in this session
- Verify the system is in a known good state after rollback
- Document what was rolled back and why


## Security

- Never hardcode secrets, tokens, or credentials in skill files or scripts
- Use environment variables or secret management tools for sensitive values
- Validate all user inputs before processing
- Follow least-privilege principle: request only the permissions you need
- Log all security-relevant actions for audit
