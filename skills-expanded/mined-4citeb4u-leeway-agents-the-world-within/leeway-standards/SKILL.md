---
name: "leeway-standards"
description: "Apply Leeway Standards governance to code and skill changes: preserve or add Leeway headers, keep REGION and TAG metadata valid, avoid hardcoded secrets, respect file placement and naming rules, and run the available verification tooling when working in Leeway-governed repositories. Use whenever Codex edits code, scripts, SKILL.md files, or project configuration in a Leeway repository."
---

# Leeway Standards

Use this skill whenever you modify code or skills in a Leeway-governed repository.

## Quick start

- Read `references/compliance.md` for the policy summary and operational expectations.
- Read `references/sdk-readme.md` when you need the header format, tag model, agent roster, or directory conventions.
- Preserve existing Leeway headers and add compatible headers to new tracked files when the repo policy requires them.
- Never hardcode secrets; move credentials to environment variables, config, or a secure secret store.
- Run the local Leeway verification tooling after meaningful changes when it is available.

## Verification

- Prefer `node scripts/verify-leeway-setup.js` for repo-level verification.
- Use `node scripts/leeway-agents/header-injector.js` to repair or add missing headers when appropriate.
- Use `node scripts/leeway-agents/compliance-monitor.js` when you need a broader compliance audit.

## Reference map

- `references/compliance.md` -> repo-facing compliance rules and policy summary
- `references/sdk-readme.md` -> canonical LEEWAY header and structure guidance
