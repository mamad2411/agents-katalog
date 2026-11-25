---
name: cloud-org-operator
description: "Dobiera właściwą organizację i konto dla Azure, Microsoft Graph, Microsoft 365/SharePoint, GCP oraz Google Workspace, a następnie tworzy fail-closed plan preflight dla CLI i MCP bez logowania i mutacji. Użyj przed każdą pracą chmurową, zwłaszcza gdy wiele firm ma osobne tenanty, witryny, konektory, subskrypcje, projekty lub konfiguracje."
---

# cloud-org-operator

Fail-closed organization targeting for Azure, Microsoft Graph, Microsoft 365 and
SharePoint, GCP and Google Workspace. The deterministic helper resolves an
organization from a local JSON registry and returns a non-executing preflight
plan. The helper itself never logs in, invokes a cloud CLI or MCP connector,
creates provider configuration or performs a mutation.

After a successful preflight, the agent may execute the user's requested cloud
work as a separate phase, using the isolated environment and exact target from
the receipt. Global production, secret and destructive-operation rules still
apply.

## Operating modes

1. `resolve`: identify exactly one organization and provider. If the request
   does not identify the company and local evidence cannot do so unambiguously,
   ask Mateusz instead of choosing the currently logged-in account.
2. `preflight`: validate the registry and build exact identity-inspection steps.
   For `m365`, name `--execution-channel` and `--intent`; tenant, SharePoint host,
   optional site path, authentication mode and principal are one composite target.
3. `inspect`: read-only Azure, Graph, M365/SharePoint, GCP or Workspace queries
   are allowed after context verification. An unregistered MCP connector remains
   `UNVERIFIED`; it may be used only for an explicitly warned read, never mutation.
4. `act`: perform the explicitly requested mutation only after the ordinary
   permission and production gates are satisfied. Re-run context verification
   immediately before the mutation and record a redacted receipt plus rollback.

## Commands

```text
python scripts/cloud_org.py validate-registry [--registry PATH]
python scripts/cloud_org.py resolve --provider PROVIDER (--organization-id ID | --alias ALIAS) [--registry PATH]
python scripts/cloud_org.py plan-preflight --provider PROVIDER (--organization-id ID | --alias ALIAS) [--registry PATH]
python scripts/cloud_org.py verify-context --provider PROVIDER (--organization-id ID | --alias ALIAS) --observed-file PATH [--registry PATH]
```

For provider `m365`, both context commands additionally require
`--execution-channel graph-powershell|m365-cli|mcp` and
`--intent read|mutate`. Channel `mcp` also requires `--connector-id ID`.

The default registry is `~/.agents/cloud-organizations.json`. `--organization-id`
and `--alias` are mutually exclusive. A missing registry, ambiguous alias,
unknown organization, provider mismatch, invalid schema, or secret-looking field
is a denial. Exit code `0` means allow/pass; exit code `2` means an expected
fail-closed denial; exit code `1` means malformed CLI or unexpected error.

`resolve` and `plan-preflight` return `REGISTRY_ALLOW` with
`live_context_status: UNVERIFIED` and `execution_allowed: false`. Only
`verify-context` can return `ALLOW`, after exact comparison with a separately
captured, non-secret context snapshot.

The helper plan contains explicit organization and provider targets plus isolated,
provider-specific configuration roots: `AZURE_CONFIG_DIR` with
tenant/subscription/account, Graph context plus account,
`CLOUDSDK_CONFIG` with configuration/project/account, and
`GOOGLE_WORKSPACE_CLI_CONFIG_DIR` with domain/configuration/account. Schema v2
keeps credential-bearing provider state outside project trees through an explicit
`config_root`; these are descriptions only and the helper never authenticates.

Provider `m365` is additive: legacy `graph` remains unchanged, while SharePoint
work requires schema v2 and a complete `tenant_id` + canonical lowercase
`sharepoint_host` + optional canonical `site_path`. `auth_mode` is mandatory:
`delegated` binds an `account`; `app-only` binds an `application_id`. App-only
verification uses a sanitized organization/site response, never `Get-MgContext`
and never a raw token. Named CLI for Microsoft 365 connections and MCP connector
IDs are registry-bound; a current login or connector label is not evidence by itself.
M365 CLI steps are emitted as argument arrays, never executable shell strings.
Connector IDs are resolved globally before use: an ID registered to another
organization is denied for both read and mutation, while a genuinely unknown
connector may receive only an explicitly unverified read-only inspection plan.

Use `references/registry-example.json` only as a structural template. Populate
the real registry from confirmed tenant, subscription, project, domain and
account identities; never infer a company-to-account mapping from the active
login. New registries use schema v2. Schema v1 remains readable only for
backward compatibility and does not provide account-level verification.
Use `references/trigger-cases.json` for activation and sensitive-operation
boundaries.

## Safety contract

- Registry data is local and untrusted; validate it before resolution.
- Secret-looking keys are rejected recursively, including nested objects and
  list elements. No credential value is accepted or echoed.
- Output is canonical JSON with sorted keys and no timestamps or host identity.
- The skill is stdlib-only and has no network, subprocess, filesystem mutation,
  provider SDK, or provider CLI behavior. This invariant applies to the helper;
  provider execution is an explicit agent phase after `ALLOW`.
- Never fall back to an active global Azure, Graph, gcloud or Workspace context.
- Never infer a SharePoint host from a company name or email domain. Confirm the
  tenant through Microsoft OIDC metadata, then record the separately verified
  SharePoint host and site in the owner's local registry.
- Before any mutating MCP call, verify the registered connector identity and the
  exact tenant/host/site target. Unknown connectors are fail-closed for mutation.
- Treat every emitted `argv` item as one literal process argument; do not join the
  array into a shell command. Canonical site paths reject shell metacharacters,
  nested percent encoding and dot segments as defence in depth.
- If isolated authentication is absent, stop with the exact account/tenant that
  must be authenticated. Do not copy tokens between organization profiles.
- Prefer the existing Teams connector for messaging workflows and Graph for
  organization administration; both still require the same organization gate.
