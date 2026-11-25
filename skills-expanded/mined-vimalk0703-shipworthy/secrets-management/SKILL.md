---
name: secrets-management
description: Use when handling API keys, database credentials, tokens, certificates, or any sensitive configuration values.
invoke_when: Use when creating, storing, rotating, or accessing API keys, database credentials, tokens, certificates, or any sensitive configuration.
---

# Secrets Management

## Core Rule

**A secret that touches source code, logs, or version history is a compromised secret.** Treat it as such immediately.

## Never Hardcode Secrets

This is absolute. No exceptions. Not in source code, not in config files checked into git, not in Dockerfiles, not in CI scripts, not in comments, not in documentation with "example" values that are actually real.

```
# ALL OF THESE ARE WRONG
DATABASE_URL = "postgres://admin:password123@prod-db:5432/app"
api_key = "sk-live-abc123..."
ENV SECRET_KEY=mysecretkey  # in Dockerfile
echo $API_TOKEN  # in CI script logs
```

If you find a hardcoded secret during code review, treat it as an incident: rotate the secret immediately, then fix the code.

## Environment Variables with Startup Validation

Environment variables are the standard mechanism for injecting secrets at runtime. But they must be validated:

```typescript
// Validate ALL required secrets at startup, fail fast if missing
const required = ['DATABASE_URL', 'JWT_SECRET', 'STRIPE_KEY'] as const;
for (const key of required) {
  if (!process.env[key]) {
    throw new Error(`Missing required environment variable: ${key}`);
  }
}
```

**Why validate at startup?** A missing secret discovered mid-request causes a confusing 500 error and a debugging session. A missing secret discovered at startup causes a clear error message and a 10-second fix.

## .env Files in .gitignore

Every project with a `.env` file must have it in `.gitignore`. No exceptions.

```gitignore
# .gitignore — secrets
.env
.env.*
!.env.example
```

Provide a `.env.example` file with placeholder values (not real secrets) so developers know which variables to configure. The `.env.example` file is committed; the `.env` file is not.

## Secret Rotation Strategies

Secrets are not permanent. They leak, employees leave, and compliance frameworks require rotation.

- **API keys:** Rotate every 90 days minimum. Support dual active keys during rotation (old key works for 24 hours after new key is generated).
- **Database passwords:** Rotate quarterly. Use connection poolers that can reload credentials without downtime.
- **JWT signing keys:** Rotate annually. Support multiple active verification keys (the `kid` header in JWT selects the correct key).
- **TLS certificates:** Automate renewal with Let's Encrypt or ACME. Set monitoring alerts for certificates expiring within 30 days.
- **Service account tokens:** Prefer short-lived tokens (1 hour) with automatic refresh over long-lived tokens.

## Different Secrets Per Environment

Development, staging, and production must use completely different secrets. Sharing secrets across environments means a dev environment breach compromises production.

- Development: local-only secrets, can be less complex
- Staging: unique secrets, similar rotation policy to production
- Production: strongest secrets, strictest rotation, access audited

Never copy production secrets into a development environment for debugging. Reproduce the issue with staging or synthetic data.

## Production Secret Stores

For production deployments, use a dedicated secret management service:

- **HashiCorp Vault:** Self-hosted, supports dynamic secrets, lease-based rotation, and audit logging.
- **AWS Secrets Manager:** Managed, integrates with IAM, supports automatic rotation for RDS, Redshift, and DocumentDB.
- **GCP Secret Manager:** Managed, integrates with IAM, versioned secrets.
- **Azure Key Vault:** Managed, supports HSM-backed keys, certificate management.

**Never read secrets from environment variables in production if a secret store is available.** Secret stores provide audit logging, access control, automatic rotation, and encryption at rest. Environment variables provide none of these.

## Git History Remediation

If a secret was committed to git -- even briefly, even on a branch that was deleted -- it is compromised. Git history is permanent and cloneable.

1. **Rotate the secret immediately.** This is step one, before anything else. The secret is compromised.
2. **Remove from history** using `git filter-repo` (preferred) or `BFG Repo Cleaner`. Do not use `git filter-branch` -- it is slow and error-prone.
3. **Force push** the cleaned history. All collaborators must re-clone or rebase.
4. **Invalidate caches:** GitHub caches repository data. Contact support if the secret appeared in a public repository.
5. **Post-mortem:** Determine how the secret was committed and add a pre-commit hook to prevent recurrence.

## Pre-Commit Hooks for Secret Detection

Install a secret detection hook that scans every commit before it is created:

- **gitleaks:** Fast, configurable, supports custom patterns. Add a `.gitleaks.toml` config.
- **detect-secrets (Yelp):** Generates a baseline of known secrets and alerts on new ones.
- **trufflehog:** Scans for high-entropy strings and known secret patterns.

Configure in `.pre-commit-config.yaml` or as a git hook. The hook must block the commit if secrets are detected, not just warn.

## Certificate Management

- **Automate renewal:** Use Let's Encrypt with ACME clients (certbot, acme.sh) for TLS certificates. Manual renewal processes lead to expiration outages.
- **Monitor expiration:** Set alerts at 30, 14, and 7 days before expiration.
- **Store private keys securely:** Private keys must be readable only by the service that uses them. File permissions: `0600`. Never commit private keys to git.
- **Use separate certificates** per service and environment. A shared wildcard certificate means one compromised service exposes all services.

## API Key Scoping (Least Privilege)

When creating API keys for third-party services:

- **Request the minimum permissions needed.** If you only need read access, do not request write access.
- **Use separate keys per service.** The key your backend uses to call Stripe should be different from the key your batch processor uses.
- **Use separate keys per environment.** Development, staging, and production each get their own key.
- **Set IP restrictions** where supported. Restrict API keys to known server IP ranges.
- **Set expiration dates** where supported. A key that never expires is a key that will eventually leak.
