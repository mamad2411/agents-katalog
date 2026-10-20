---
applyTo: "**"
description: Security requirements that apply to every file in this repository.
---

# Security Instructions

## Secrets

- Never write a literal secret, token, key, password, certificate, or connection string into any file.
- Resolve secrets at runtime from Azure Key Vault or the platform secret store using Managed Identity.
- Local development uses a git-ignored `.env` or user secrets. `.env` is never committed.
- If a secret is discovered in source or history, stop and report it as a rotation incident before continuing.

## Identity and access

- Prefer Managed Identity, then workload identity federation, then short-lived credentials. Static keys require an ADR.
- Grant least privilege at the narrowest scope that satisfies the requirement.
- Do not use owner or contributor role assignments for application identities.

## Input handling

- Treat every value crossing a trust boundary as hostile: HTTP input, files, queue messages, environment, and model output.
- Validate against an allow-list, then encode for the destination context.
- Use parameterized queries. Never concatenate user input into SQL, shell, path, or template strings.
- Constrain and canonicalize file paths before use; reject traversal outside the intended root.

## Output and logging

- Never log secrets, tokens, credentials, personal data, or full request bodies.
- Return generic errors to callers; keep diagnostic detail in server-side logs.

## Dependencies

- Add a dependency only when it is necessary, maintained, and license-compatible.
- Pin GitHub Actions to a full commit SHA. Pin package versions and commit the lock file.

## Prohibited without explicit approval

- Disabling TLS validation, authentication, authorization, or CSRF protection.
- Dynamic code execution such as `eval` or constructing functions from strings.
- Enabling shell interpretation when spawning processes.
- Wildcard CORS or wildcard network rules in any shared environment.
