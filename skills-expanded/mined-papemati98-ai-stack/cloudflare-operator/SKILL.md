---
name: cloudflare-operator
description: Operate Cloudflare DNS, proxy and TLS, Tunnel and Access, Workers and Pages, WAF, rate limits, cache and redirects. Use for scoped Cloudflare administration, deployment troubleshooting, access checks and usage diagnosis; distinguish account/zone/environment and preserve rollback before changes.
metadata:
  version: "0.1.0"
---

# Cloudflare Operator

## Resolve before acting

Read the project brief through `llm-wiki` and reconcile it with live state.
Identify project, customer, account ID, zone ID, hostname, environment and owner
of the configuration (Terraform, Wrangler, Git deployment or dashboard). A domain
name or currently selected browser account alone is not sufficient identity.
Do not infer a client account from a similarly named zone or inherited CLI login.

Read only the applicable procedure:
- [Identity and operations](references/identity-operations.md): tokens, API/MCP,
  inventory, usage, error diagnosis and receipt.
- [DNS and TLS](references/dns-tls.md): domains, records, proxy, certificates.
- [Tunnel and Access](references/tunnel-access.md): connector lifecycle and
  interactive/machine access to local or remote applications.
- [Workers and Pages](references/workers-pages.md): builds, environments,
  bindings, deployments, logs and rollback.
- [Edge protection](references/edge-protection.md): WAF, limits, cache, redirects.

## Keep the change bounded

Read-only discovery can proceed within the user's resource/data scope. Before a
write, record exact IDs, expected result, current state, rollback and approval.
Public DNS/tunnel/domain changes, production deployment, IAM/secret changes,
destructive operations and paid resource activation require explicit owner scope.
Skill installation is not such approval. Once authorized, execute the bounded
operation without asking again at every command.

Prefer the project's existing IaC owner, installed CLI or supported API. Use an
available authorized Cloudflare connector if appropriate; this skill does not
install a plugin, grant permissions or guarantee a connector exists. Dashboard
automation is a fallback, not permission to switch accounts or expose tokens.
Recheck official API schemas, installed `--help`, plan features and prices before
use; do not copy obsolete commands or assume a successful login authorizes a write.

Large changes use existing planning, `agent-graph`, `agent-loop` and
`accept-system`; this skill supplies Cloudflare-specific operations and oracles.
Fleet remains the contractor/model router. `ngrok-operator` is a separate provider,
not an automatic fallback. Use `data-governance` for storage/migration/retention and
`remote-computer-use` for relevant user-journey verification on the test VM.

## Honest verification

HTTP 200 alone is not PASS: check API `success`/errors, live resource state and
the consumer's actual behavior. Include an authorized and unauthorized access
case where protection changes. Use synthetic DEV/TEST identities and technically
block real email/payment/webhook effects before testing.

Restore only changed, owned resources; re-read live state before rollback to
avoid overwriting concurrent work. Never treat DNS propagation, cache purge or
external side effects as instantly reversible. Report gaps, not invented PASS.

End with changed IDs, expected/actual checks, usage if measured and rollback
readiness. Record material integration/deploy/auth changes with a redacted Hub
handoff. Skill installed, credentials configured, native discovery and live
operation verified are separate states, especially across machines.
