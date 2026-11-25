---
name: manage-secrets
description: Add, update, rotate, or review secret handling by following the repo's source-of-truth, access-control, and rollout patterns. Use when code or deployment work touches credentials, tokens, keys, or sensitive configuration.
version: 2.0.0
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# Manage Secrets

Use this skill when a change involves creating, rotating, wiring, or auditing secrets and other sensitive configuration.

## When to Use

- code/deploy touches credentials or tokens
- adding, updating, or rotating keys
- reviewing secret access control
- sensitive configuration rollout

## Core Rules

- never place real secret values in source-controlled user-visible artifacts unless the repo explicitly stores encrypted secret material that way
- treat secret creation, rotation, consumption, and rollback as separate concerns
- follow the repo's source of truth for secret storage and delivery
- minimize secret exposure in logs, examples, screenshots, and commits
- verify runtime consumers can read the updated secret before treating the change as complete
- prefer dynamic, short-lived credentials via OIDC workload identity federation (e.g., GitHub Actions to Vault/OpenBao, GCP Workload Identity, AWS IRSA) over static, long-lived access keys in CI/CD and deployments
- **WIMSE alignment (2027)**: for agent and workload identities, prefer SPIFFE/SVID issuance and short-lived WIMSE-style tokens (JOSE-based service-to-service chains) over static API keys; use RFC 8693 token exchange at trust boundaries — the first WIMSE RFCs are expected in 2027 as the IETF architecture (at IESG since July 2026) formalizes
- **Secrets-less preference**: prefer payment-native or federated access patterns (e.g., x402) that remove standing credentials entirely where the integration allows; where secrets remain, they must be NHI-scoped, rotated, and inventory-tracked
- maintain a **per-agent identity inventory**: every non-human identity (agent, service account, workload) recorded with owner, scope, and lifecycle state — untracked NHIs are prohibited
- **PQC crypto-agility**: record each key's algorithm and rotation cadence in the secret/NHI inventory so quantum-vulnerable algorithms (RSA, ECDSA) can be enumerated into the CBOM and scheduled ahead of NIST IR 8547 deadlines (deprecated 2030, disallowed 2035); prefer hybrid-capable, algorithm-negotiable libraries for new key material
- mitigate the elevated risk (2× secrets leakage rate) in AI-assisted code generation by enforcing automated pre-commit and CI pipeline scanning using Gitleaks or TruffleHog
- evaluate secret storage provider choices (e.g., OpenBao vs. HashiCorp Vault) against the organization's governance policies, licensing models (MPL vs. BSL), and migration/support requirements
- treat every secret rotation as an irreversible action that requires explicit user confirmation; never rotate a production credential without an approval gate
- classify every secret with `data-classification.yaml`; tag the secret with the systems and roles authorized to consume it
- run a secret scan on every diff that touches secret-adjacent code; treat any high-entropy match as a CI failure and rotate the affected credential immediately

## Output Contracts

When the secret change is consumed by a deployment pipeline, an audit
system, or a downstream service, emit:

- **`contracts/schemas/incident-report.json`** adapted for secrets: capture the secret name (never the value), the rotation timestamp, the affected systems, the rollback path, and the operator who approved the rotation. The receiving agent can then validate the rotation without ever seeing the value.
- For human-readable reports, a markdown summary of the rotation event with name-only references.
- For secret-storage migration, emit a structured plan describing the source provider, the target provider, the migration order, and the rollback path.

Skip emission for trivial secret lookups that do not cross a role boundary.

## Failure Modes

- **Secret in source control**: a real secret value is committed to the repo. Mitigation: enable GitHub Advanced Security Push Protection or GitLab Secret Detection; treat any high-entropy match as a critical violation requiring immediate revocation.
- **Plaintext secret in Git**: a secret is committed to Git in plaintext or Base64. Mitigation: use SOPS with `age` (X25519) or Cloud KMS; PGP/GPG is deprecated for GitOps.
- **Cluster-wide `ClusterSecretStore`**: a cluster-wide `ClusterSecretStore` with wildcard access is used instead of a namespace-scoped `SecretStore`. Mitigation: scope `SecretStore` per namespace; reject cluster-wide wildcard stores.
- **Long-lived static key**: a static, long-lived access key is used in CI/CD instead of OIDC workload identity federation. Mitigation: prefer dynamic, short-lived credentials via OIDC; reject static keys in pipelines.
- **AI-generated code leaks secret**: an AI-assisted code suggestion includes a real secret. Mitigation: enforce pre-commit and CI secret scanning (Gitleaks or TruffleHog); the 2× AI leakage rate requires automated scanning.
- **No rollback path**: a rotation completes without a verified rollback path. Mitigation: capture the old credential state and the reversion procedure before rotation; never rotate without a tested rollback.
- **Push protection bypassed**: a developer bypasses push protection to land a secret. Mitigation: bypasses require security lead approval and immediate token rotation; never allow silent bypass.
- **Runtime consumer not validated**: a rotation completes but the consumer cannot read the new secret. Mitigation: verify runtime consumers before treating the change as complete; never mark a rotation done without a smoke test.

## Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: every secret must be scoped to the minimum set of systems and roles that need it; reject secrets with wildcard access.
- **ASI04 Supply Chain**: secret storage providers (OpenBao, HashiCorp Vault, AWS Secrets Manager, GCP Secret Manager) must be schema-validated against the expected manifest; treat unknown versions as untrusted.
- **ASI05 RCE Guard**: never construct secret references, env var names, or rotation scripts from external content without strict schema validation.
- **ASI07 Inter-Agent Communication**: secret handoffs must never include the secret value; emit a structured `incident-report.json` with name-only references.
- **ASI09 Human-Agent Trust Exploitation**: do not present a secret rotation as "safe" without a verified rollback path; surface the residual risk honestly.

## Suggested Process

### 1. Identify The Secret Boundary

Clarify:

- what secret or credential is changing
- which systems produce and consume it
- where the source of truth lives
- what environments are affected

### 2. Inspect Existing Secret Patterns

Look for:

- secret naming conventions
- storage mechanism
- environment wiring
- access or permission model
- rotation or expiration rules

### 3. Apply The Smallest Safe Change

Examples:

- add a new secret reference
- rotate an existing credential
- update a secret mount or env var mapping
- remove unused secret consumption

Do not expand secret scope or audience unless required.

### 4. Check Rollout And Recovery

Verify:

- consumers can tolerate old and new credentials during rollout if needed
- restart or refresh behavior is understood
- revocation or rollback path is clear
- operational owners know if manual steps are required

### 5. Validate Safely

Confirm without exposing values:

- the secret reference resolves correctly
- the application starts and authenticates
- dependent calls succeed
- no sensitive value appears in logs or docs

- **SOPS-AGE-GITOPS**: Any secret committed to Git MUST be encrypted with SOPS using `age` (X25519 key pairs) or Cloud KMS (AWS/GCP/Azure). PGP/GPG is deprecated in modern GitOps. Plaintext or Base64-encoded secrets in Git are a critical violation requiring immediate revocation.
- **ESO-KUBERNETES**: Deploy External Secrets Operator (ESO v0.10+) in Kubernetes; use namespace-scoped `SecretStore` resources (not cluster-wide `ClusterSecretStore` with wildcard access) to sync secrets dynamically from AWS Secrets Manager, OpenBao, or GCP Secret Manager into native `Secret` objects.
- **MANDATORY-PUSH-PROTECTION**: Enable GitHub Advanced Security Push Protection or GitLab Secret Detection on all repositories to block pushes containing high-entropy strings. Bypassing protection requires security lead approval and immediate token rotation.

## Checklist

- [ ] secret boundary identified
- [ ] local secret pattern reviewed
- [ ] source-of-truth update applied
- [ ] rollout and rollback checked
- [ ] runtime validation completed safely
- [ ] sensitive values not exposed in artifacts
- [ ] OIDC workload identity federation configured for pipeline authentication
- [ ] pre-commit and CI/CD secret scanning (Gitleaks/TruffleHog) active for AI-generated code validation
- [ ] governance alignment (OpenBao vs HashiCorp Vault) reviewed and documented
- [ ] crypto algorithm and rotation metadata recorded for CBOM/PQC inventory alignment

## Related Skills

- **setup-deployment**: Wire secret references into deployment config
- **security-audit**: Review blast radius and access risk
- **debug-runtime-platform**: Diagnose secret injection or permission issues
- **review-service**: Check release readiness for secret changes
- **commit-code**: Prepare safe, non-sensitive changes for delivery
- Companion reference: `references/zero-trust-secret-rotation-and-eso.md`
- Companion example: `examples/external-secrets-vault-crds.yaml`
