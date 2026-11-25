---
name: container-supervision-s6
description: "Modify, debug, or extend the s6-overlay supervision tree inside the agent runtime Agent Docker image — adding new services, debugging profile gateways, understanding the Architecture B main-program pattern."
---

# container-supervision-s6

## Purpose

Modify, debug, or extend the s6-overlay supervision tree inside the agent runtime Agent Docker image — adding new services, debugging profile gateways, understanding the Architecture B main-program pattern.

## Use When

- The user request matches `container-supervision-s6`, `container supervision s6`, `devops` or the skill description.
- Modify, debug, or extend the s6-overlay supervision tree inside the agent runtime Agent Docker image — adding new services, debugging profile gateways, understanding the Architecture B main-program pattern.
- The task benefits from domain-specific workflow, checks, output structure, or safe fallback behavior.

## Workflow

1. Identify environment, repo, service, config, credentials, and desired state.
2. Prefer read-only status and dry-run commands before writes.
3. Require explicit confirmation for deploy, publish, delete, credential, production, or external writes.
4. Provide rollback, verification, and audit steps.

## Codex Runtime Rules

- Use only tools, plugins, MCP servers, files, commands, and credentials that are actually available in the current Codex session.
- If an external write, install, publish, deploy, paid action, credential use, account operation, physical-device action, or production action is needed, ask for explicit confirmation first.
- If the required tool is unavailable, return a portable fallback such as Markdown, CSV, prompt pack, implementation plan, config sketch, or verification checklist.
- Do not claim files, media, issues, API calls, payments, deployments, transactions, messages, or integrations were created unless there is concrete local or tool evidence.
- Treat source repository runtime details as historical source context, not active Codex capabilities.

## Avoid

- Do not mutate production, cloud resources, CI secrets, webhooks, or deployments without confirmation.
- Do not hide operational risk.

## Output

Return the useful artifact first, then evidence and verification status.

For non-trivial work, include:

```markdown
Result: ...
Evidence: ...
Verification: PASS/FAIL/NOT RUN
Risks / Next Steps: ...
```
