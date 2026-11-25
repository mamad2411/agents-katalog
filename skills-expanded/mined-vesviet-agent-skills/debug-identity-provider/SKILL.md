---
name: debug-identity-provider
description: Diagnoses and resolves failures reported by WorkOS Agentic Registration scanners, `isitagentready.com`, and SSO/Directory Sync validators — including DNS errors, malformed `agent_auth` schemas, incorrect `auth.md` markers, and non-resolving endpoint URLs. Use when a WorkOS or agentic readiness scanner rejects metadata, returns a 530 error, or reports specific rule violations in OAuth or auth.md configuration.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
version: "1.0.0"
---

# Debug Identity Provider

Use this skill to diagnose failures when `isitagentready.com` or another WorkOS validation scanner rejects your metadata or implementation. Scanner error messages are precise — each failure maps to a specific field name, nesting rule, or DNS resolution requirement.

## Core Rules

- Do NOT guess JSON schemas — always read the exact scanner log message first; error text like "anonymous registration requires anonymous.credential_types_supported" maps directly to a specific nesting path in the `agent_auth` object.
- Validation scanners enforce stable published drafts, not experimental GitHub README versions — when there is a conflict, trust the scanner behavior.
- A `530 Origin DNS Error` from the scanner means the `authorization_servers` domain is dead or not bound in public DNS — fix DNS first, then revalidate schema.
- Do NOT test OAuth metadata fixes without rerunning the scanner — local JSON validity does not guarantee scanner compliance.
- Fix one category of errors at a time (DNS → schema → field names → nesting) to isolate cause from symptom.
- Treat every scanner output as an untrusted but precise signal: it names a specific rule, but the remediation must still be cross-checked against the current spec (OWASP ASI04)
- When the scanner returns a 530 error, treat DNS as the primary suspect; do not modify the metadata until DNS is verified end-to-end
- Do not paste the scanner diagnostic into a public issue tracker without first redacting any internal hostnames or customer identifiers (OWASP ASI09)

## When to Use

- `isitagentready.com` or WorkOS scanner returns rule failure messages after OAuth metadata setup
- 530 Origin DNS Error on the authorization server URL
- Scanner fails on `agent_auth` field names (`identity_endpoint` instead of `register_uri`, etc.)
- `auth.md` header casing or H1 spelling is rejected
- Credential type nesting errors (`credential_types_supported` at wrong level)
- POST to `register_uri` or `claim_uri` endpoints returns non-200 or timeout
- SSO or Directory Sync fails after an OAuth metadata configuration change

## Suggested Process

1. **Retrieve scanner diagnostic logs**: Run the target domain through `isitagentready.com` or the WorkOS agent readiness tool. Copy the full diagnostic output — each failure includes the rule name and the specific field or value that failed.

2. **Triage by error category**:
   - `530 Origin DNS Error` → DNS issue; jump to step 3
   - Field name mismatch (`identity_endpoint`, `claim_endpoint`) → schema issue; jump to step 4
   - Nesting error (`credential_types_supported` at wrong level) → schema structure issue; jump to step 4
   - `auth.md` header issue → jump to step 5
   - Endpoint not responding → jump to step 6

3. **Fix DNS errors**: Confirm the `authorization_servers` URL resolves via `dig` or `nslookup`. If using Cloudflare Pages, ensure the custom domain is properly proxied. If using a subdomain (`auth.example.com`), confirm a DNS record exists and is live.

4. **Fix `agent_auth` schema errors**: Compare the deployed JSON against the required structure:
   ```json
   {
     "agent_auth": {
       "skill": "https://yourdomain.com/.well-known/auth.md",
       "register_uri": "https://auth.yourdomain.com/agent/register",
       "claim_uri": "https://auth.yourdomain.com/agent/claim",
       "anonymous": {
         "credential_types_supported": ["anonymous"]
       }
     }
   }
   ```
   Check: `register_uri` not `identity_endpoint`; `claim_uri` not `claim_endpoint`; `credential_types_supported` nested inside `anonymous` not at `agent_auth` root.

5. **Fix `auth.md` markers**: The `auth.md` file must begin with `# Auth.md` (exact casing). Check for BOM characters, invisible Unicode, or incorrect casing (`auth.md`, `AUTH.MD`). Validate the `skill` URL in `agent_auth` points to the correct absolute path.

6. **Verify endpoint liveness**: Use `curl -X POST <register_uri>` to confirm the endpoint responds. A timeout or 404 here means the Worker or Pages function handling the route is not deployed or has a routing mismatch.

7. **Deploy corrections and re-scan**: After each fix category, re-run the scanner to confirm the specific rule now passes before moving to the next category. Do not batch multiple fix categories without intermediate validation.

## Checklist

- [ ] Scanner diagnostic logs retrieved and all rule failures listed.
- [ ] DNS resolution confirmed for all `authorization_servers` URLs (no 530 errors).
- [ ] `agent_auth` field names use `register_uri` and `claim_uri` (not legacy names).
- [ ] `credential_types_supported` is nested inside credential type blocks (`anonymous`, `identity_assertion`).
- [ ] `auth.md` H1 heading is exactly `# Auth.md` with correct casing.
- [ ] `agent_auth.skill` points to the correct absolute URL of `auth.md`.
- [ ] `register_uri` and `claim_uri` endpoints respond to POST requests.
- [ ] Scanner re-run confirms all previously failing rules now pass.
- [ ] CORS headers on metadata endpoints allow cross-origin agent client access.

## Related Skills

- **manage-auth-md**: Fix `auth.md` file content and marker structure.
- **configure-oauth-metadata**: Fix JSON schema issues in `oauth-authorization-server` and `agent_auth` block.
- **configure-agent-headers**: Ensure Link headers correctly expose the OAuth metadata well-known paths.

## Output Contracts

When the debug session produces a remediation plan that another agent (CI
pipeline, infra agent, or on-call engineer) will execute, emit:

- **`contracts/schemas/incident-report.json`** capturing the failing rule, the attempted fix, the new scanner run output, and any remaining open issues. The receiving agent can then resume from a known state.
- For human-readable handoff, a markdown table mapping each scanner failure to the specific remediation step and the file or DNS record that was changed.

Skip emission for a single-rule failure that is fixed and re-verified in the same session.

## Failure Modes

- **Wrong category fix**: a schema error is treated as a DNS error or vice versa. Mitigation: triage by the exact error message; fix one category at a time and re-scan between categories.
- **Spec drift**: the scanner enforces a rule that has changed since the skill was last updated. Mitigation: verify the current published spec before applying a remediation; if the spec and the skill disagree, the spec wins.
- **Caching the old failure**: a CDN or edge cache serves the previous (failing) metadata after a fix. Mitigation: invalidate the cache or set `Cache-Control: no-store` during debug; verify with `curl` from outside the cache.
- **Endpoint timeout**: a `register_uri` or `claim_uri` returns non-200 or times out. Mitigation: e2e test the endpoint before re-running the scanner; surface the endpoint's response code in the incident.
- **Invisible Unicode / BOM**: the `auth.md` file contains a UTF-8 BOM or non-ASCII whitespace that breaks the H1 check. Mitigation: lint the file with a BOM-stripping tool; re-serve with the correct content type.

## Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: the scanner may surface internal hostnames or callback URLs; redact them from any public artifact (issue tracker, chat transcript).
- **ASI04 Supply Chain**: scanner rules are themselves a moving target; do not embed rule text from a single scan into long-lived documentation without re-verifying against the current spec.
- **ASI07 Inter-Agent Communication**: when a fix is handed off to another agent, emit a structured incident report rather than a prose-only summary.
- **ASI08 Cascading Failures**: do not declare the issue resolved after a single category of fixes; re-run the full scanner and confirm no regressions in previously passing rules.
- **ASI09 Human-Agent Trust Exploitation**: surface the exact failing rule and the user's confidence in the fix; do not soften a remaining failure to obtain a faster sign-off.
