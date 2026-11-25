---
name: manage-auth-md
description: Use when creating, updating, or auditing the /auth.md file at the repository or domain root to ensure agentic registration discovery compliance with WorkOS and isitagentready.com standards.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
version: "1.0.0"
---

# Manage Auth.md

Use this skill when adding or updating the Agentic Registration Discovery file (`/auth.md`) to comply with WorkOS and `isitagentready.com` standards. The `auth.md` file is a human and machine-readable document that declares an application's agent registration endpoints, OAuth authorization metadata locations, and agentic compliance posture.

## Core Rules

- The file MUST begin exactly with the H1 heading `# Auth.md` on the first line of the document body. Do not use variations like `# Authentication`, `# auth`, or `## Auth.md`.
- The file MUST document the registration endpoints explicitly (e.g., `POST /agent/identity`).
- The phrase "agentic registration" MUST appear in the document body.
- The file MUST be served publicly at `/auth.md` from the domain root (e.g., `https://example.com/auth.md`).
- Link to the OAuth authorization metadata endpoints using exact URLs — do not use relative paths.
- Do not embed credentials, secrets, or tokens in `auth.md`. Only reference public endpoint paths.
- Treat `auth.md` as a public, signed contract: do not include internal-only registration endpoints or unreleased callback URLs
- Validate the file against the current scanner rule set before every deploy; reject schema-drifted files (OWASP ASI04)
- Every registration endpoint URL must be on the operator's own domain; reject third-party URLs at code review
- Run a `curl` check from outside the cache to confirm the deployed content matches the source after each change

## When to Use

- Setting up a new service for WorkOS agentic authentication integration
- Repairing a failing `isitagentready.com` scanner check for the Auth.md requirement
- Updating registration endpoint documentation after OAuth or agent identity changes
- Auditing an existing `auth.md` for spec compliance before submitting to a scanner or registrar

## Suggested Process

1. **Create the file**: Create `auth.md` in the root workspace directory (`public/auth.md` for static sites, root for Workers). Ensure it will be served publicly at `/auth.md`.

2. **Write the required header**: The first non-empty line MUST be exactly:
   ```
   # Auth.md
   ```
   Follow with a brief one-paragraph description of the service and its agentic registration support.

3. **Add the required phrase**: Include "agentic registration" in the first or second paragraph — for example: "This service supports agentic registration for AI agent clients."

4. **Document registration endpoints**: List each registration endpoint with its HTTP method, path, and description:
   ```
   ## Registration
   
   - `POST /agent/identity` — Register a new agent identity
   - `POST /agent/identity/callback` — Handle OAuth callback for agent sessions
   ```

5. **Link to OAuth metadata**: Add explicit links to the OAuth discovery endpoints:
   ```
   ## OAuth Metadata
   
   - Protected Resource: `/.well-known/oauth-protected-resource`
   - Authorization Server: `/.well-known/oauth-authorization-server`
   ```

6. **Deploy and verify**: Confirm the file is publicly accessible at `/auth.md` via `curl https://yourdomain.com/auth.md`. Check HTTP status `200 OK` and correct `Content-Type: text/markdown` or `text/plain`.

7. **Run scanner check**: Submit the domain to `isitagentready.com` and confirm the Auth.md check passes. Remediate any field failures reported by the scanner.

## Output Format

- `/auth.md` (or `public/auth.md`) — Markdown text file served publicly at `/auth.md`

## Checklist

- [ ] File is named `auth.md` (lowercase) and committed to the correct location.
- [ ] First line of the document body is exactly `# Auth.md`.
- [ ] Document contains the phrase "agentic registration".
- [ ] HTTP registration markers (`POST /agent/identity` etc.) are clearly documented.
- [ ] Points to `/.well-known/oauth-protected-resource` with explicit URL.
- [ ] Points to `/.well-known/oauth-authorization-server` with explicit URL.
- [ ] File is publicly accessible at `/auth.md` (verified via `curl`).
- [ ] Response status is `200 OK` with text content type.
- [ ] `isitagentready.com` Auth.md scanner check passes.

## Related Skills

- **configure-oauth-metadata**: Set up the `/.well-known/oauth-protected-resource` and `/.well-known/oauth-authorization-server` endpoints that `auth.md` references.
- **debug-identity-provider**: Troubleshoot WorkOS agent registration and scanner failures.
- **configure-agent-headers**: Expose `auth.md` presence via HTTP Link headers for passive discovery.
- **configure-mcp**: Reference MCP servers from the `## MCP Servers` section with a `transport` field.
- **manage-agent-identity**: Cross-link the registration endpoints declared in `auth.md` with the NHI lifecycle.

## Output Contracts

When the `auth.md` change is consumed by an infra agent, a CI pipeline, or an
on-call engineer, emit:

- **`contracts/schemas/edge-deployment-spec.json`** listing the served path (`/auth.md`), the content type, and the list of registration endpoints declared.
- **`contracts/schemas/api-contract-spec.json`** describing each registration endpoint (HTTP method, path, expected payload) so the deployment agent can validate before serving.
- For human-readable reports, a markdown diff of the file with the previous version is sufficient.

Skip emission for trivial typo fixes that do not cross a role boundary.

## Failure Modes

- **Wrong H1 casing**: the file starts with `# Authentication` or `# auth` instead of `# Auth.md`. Mitigation: lint the first non-empty line; reject any deviation.
- **Missing phrase**: the document body omits "agentic registration". Mitigation: lint the body for the required phrase; reject if absent.
- **Wrong URLs**: a registration endpoint URL points to a non-operator domain. Mitigation: enforce an allowlist at code review; reject third-party URLs.
- **BOM or invisible Unicode**: the file contains a UTF-8 BOM or non-ASCII whitespace that breaks the H1 check. Mitigation: strip the BOM in the deploy pipeline; re-serve with `Content-Type: text/markdown`.
- **Stale cache**: a CDN or edge serves an older version after a fix. Mitigation: invalidate the cache or set `Cache-Control: no-store` during debug; verify with `curl` from outside the cache.
- **MCP server missing transport**: the `## MCP Servers` section lists an MCP server without a `transport` field. Mitigation: enforce `transport: streamable-http | sse`; the scanner rejects SSE-only entries.

## Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: a malicious or compromised `auth.md` could redirect agents to attacker-controlled endpoints. Validate every URL against the operator's own domain allowlist.
- **ASI03 Identity & Privilege Abuse**: do not include client secrets, signing keys, or unreleased callback URLs in the served file.
- **ASI04 Supply Chain**: the file must be validated against the current scanner rule set before every deploy; reject schema-drifted files.
- **ASI07 Inter-Agent Communication**: the file is consumed by external agents and scanners; treat it as a public contract and review all changes before deploy.
- **ASI09 Human-Agent Trust Exploitation**: do not present `auth.md` as "scanner-compliant" without a successful scanner run; surface the scanner output in the deploy record.

### 2026: Auth.md Enhancements

- **auth.md spec evolution (mid-2026):** The `## MCP Servers` section now requires a `transport` field (`streamable-http` or `sse`). The isitagentready.com scanner rejects auth.md files that reference SSE-only MCP servers without a `streamable-http` transport declaration.
- **Validation before publish:** Run `curl -s "https://isitagentready.com/check?url=YOUR_DOMAIN"` after every auth.md change to catch scanner errors before they affect agent registration flows. Do not rely on manual inspection alone.
