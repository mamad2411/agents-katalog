# service-secrets

Secrets is the only agent-facing boundary for OpenBao-backed secret material,
scoped secret tokens, lease lifecycle, rotation, and secret access audit.

## Agent Rules

1. Do not ask Core, Gateway, runtime, or another service to reveal raw secret
   values. Use Secrets only when an approved workflow needs a secret value or
   scoped token.
2. Prefer secret references and scoped leases over raw values. Request
   `includeValue=true` only for the smallest approved operation.
3. Treat every returned token, secret value, accessor, and lease ID as
   sensitive. Do not quote it in user-facing answers, prompts, logs, or
   artifacts.
4. Use lease renewal only while the work is still active. Revoke leases when
   work is cancelled or no longer needs the secret.
5. Use rotation only after explicit approval and include a reason.
6. Record an audit event for unusual or manually approved secret access.

## Service Functions

- `ResolveRef(ResolveRefRequest) -> ResolveRefResponse`
  - Generated service function: `secrets_ResolveRef`
  - NATS subject: `svc.secrets.v1.resolve_ref`
  - Resolves an OpenBao KV reference.

- `IssueScopedSecret(IssueScopedSecretRequest) -> IssueScopedSecretResponse`
  - Generated service function: `secrets_IssueScopedSecret`
  - NATS subject: `svc.secrets.v1.issue_scoped_secret`
  - Issues a scoped token through OpenBao.

- `RenewLease(RenewLeaseRequest) -> RenewLeaseResponse`
  - Generated service function: `secrets_RenewLease`
  - NATS subject: `svc.secrets.v1.renew_lease`
  - Renews a lease.

- `RevokeLease(RevokeLeaseRequest) -> RevokeLeaseResponse`
  - Generated service function: `secrets_RevokeLease`
  - NATS subject: `svc.secrets.v1.revoke_lease`
  - Revokes a lease.

- `RotateSecret(RotateSecretRequest) -> RotateSecretResponse`
  - Generated service function: `secrets_RotateSecret`
  - NATS subject: `svc.secrets.v1.rotate_secret`
  - Rotates a KV v2 secret value.

- `AuditAccess(AuditAccessRequest) -> AuditAccessResponse`
  - Generated service function: `secrets_AuditAccess`
  - NATS subject: `svc.secrets.v1.audit_access`
  - Records a redacted secret access event.

## Boundaries

- Secrets owns OpenBao API calls, lease renewal/revocation, scoped token
  creation, rotation, and redacted access audit.
- Gateway and other services receive secret references or scoped credentials;
  they do not embed OpenBao clients.
- OpenBao audit devices remain OpenBao configuration. This service records
  Quark-side redacted audit IDs for service-function calls.
