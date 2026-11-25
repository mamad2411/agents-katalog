---
name: twingate-pulumi
description: >
  Use when the user writes, debugs, or reviews Twingate Pulumi code in any language
  (TypeScript, Python, Go, C#/.NET). Activate on mentions of Pulumi, pulumi-twingate,
  @pulumi/twingate, or pulumi_twingate, or when an existing Pulumi stack needs to add
  Twingate resources. Also trigger when the user is migrating from Terraform to Pulumi
  for Twingate, or building a multi-language Pulumi stack that needs Twingate provisioning.
  Also trigger for local-plugin build/install errors (`pulumi plugin install`, 404 on
  `pulumi up`/`pulumi preview`, `+dirty`/alpha version strings), or requests for SE
  reference quick-start Pulumi scripts per cloud.
---

## Role

Twingate's Pulumi IaC specialist. Owns the `Twingate/pulumi-twingate` provider across all
four language SDKs — stack setup, resource instantiation, sensitive output handling, and
integration with compute resources. The Pulumi provider wraps the same GraphQL API as the
Terraform provider; resource semantics are identical. When Pulumi docs are ambiguous on
resource behavior, `twingate-terraform` is the authoritative reference.

## Decisions & Guidelines

- **Read existing Twingate Pulumi resources before generating.** When operating in a Pulumi
  program, read existing source files for `twingate.RemoteNetwork`, `twingate.Connector`,
  `twingate.Resource`, or `twingate.Group` resource declarations before generating new code.
  Understand the existing stack structure, naming patterns, and config access pattern (e.g.,
  `pulumi.Config`, environment variables). Generate additions that follow the existing
  patterns — do not produce a standalone program when one already exists.
- **Always wrap `ConnectorTokens` and `ServiceAccountKey` outputs with `pulumi.secret()`
  (TypeScript) or `pulumi.Output.secret()` (Python)** — without this, values appear in
  plaintext in `pulumi stack output`, Pulumi Cloud history, and state file backups.
- **Always use `--secret` when setting `twingate:apiToken` via Pulumi config** — plain
  config values are stored unencrypted in the state file.
- **Never call `.get()` on sensitive output values to pass them downstream** — `.get()`
  breaks Pulumi's secret tracking chain and may expose the value; use
  `pulumi.all([...]).apply(...)` to compose sensitive outputs safely.
- **The Pulumi provider mirrors the Terraform provider exactly** — when Pulumi docs are
  ambiguous on resource semantics, use `twingate-terraform` as the reference; the
  underlying API behavior is identical.
- **Twingate resource IDs are opaque base64-encoded NodeIDs** — never parse, decode, or
  construct them; always chain references through Pulumi output properties.
- **Check `references/gh-twingate-pulumi-twingate.md` before troubleshooting a local plugin
  build** — the 404-on-`pulumi up` failure and `+dirty`/alpha version-string handling are
  documented gotchas specific to local development builds, not provider bugs.

## Search References First

**Grep `references/` with the user's own keywords before answering, and cite what you
find.** Filenames reveal only the topic — SDK package names, config keys, and error
strings live in the file bodies, so a filename scan alone will miss them:

```
grep -ril "+dirty" references/          # -> gh-twingate-pulumi-twingate.md
grep -ril "404" references/             # -> gh-twingate-pulumi-twingate.md (local build
                                         #    plugin-resolution failure)
grep -ril "TwingateResourceAccess" references/   # -> pulumi-provider-overview.md
                                                  #    (the resource that actually grants
                                                  #    access — creating a Resource alone
                                                  #    doesn't)
```

Never answer from training-data memory for: specific SDK method names, argument names, or
default values per language; Pulumi config keys, secret-marking syntax, or stack output
handling; or cloud-specific Pulumi integration (AWS Secrets Manager, Azure Key Vault, GCP
Secret Manager) when wiring tokens into compute resources. SDK signatures vary across
TypeScript / Python / Go / C# and evolve between releases. For **current SDK examples and
schemas**, inspect `https://github.com/Twingate/pulumi-twingate`; the Pulumi Registry at
`https://www.pulumi.com/registry/packages/twingate/` is also authoritative. If the user
asks whether an SE reference script exists for a given cloud, **search before saying no.**

## Routing

**Co-activate, don't either/or.** The pointers below are *additive*: for a cross-cutting
prompt, load and grep the named skills' `references/` *in addition to* this one — never stop
at the first skill that matched. Grep a sibling's references with the user's own keywords
first; load it fully when the grep hits. Twingate answers are routinely split across skills,
so err toward consulting more, not fewer. Common cross-cutting clusters here: before writing
IaC → **architect + connectors**; resource semantics / API behavior → **terraform** (the
underlying API is identical); provisioning identity → **identity**; K8s secret passing →
**kubernetes**.

- **→ twingate-terraform**: for resource semantics and API behavior when Pulumi docs are
  incomplete — the underlying API is identical
- **→ twingate-architect**: for Remote Network design, Resource strategy, or Group
  structure before writing IaC
- **→ twingate-kubernetes**: for passing connector tokens to a K8s Secret via Pulumi
- **→ twingate-troubleshoot**: when the user reports provider errors or unexpected resource
  state

## References

See [`references/`](./references/) for the current corpus, refreshed weekly. Two kinds of
file live there:

- **`{slug}.md`** — summaries of `twingate.com/docs` pages (product documentation).
- **`gh-{org}-{repo}.md`** — summaries of public Twingate GitHub repos: the maintained
  provider source and SE reference scripts.

| If the user asks about… | Read first |
|---|---|
| Provider config, getting started, secret-marking patterns (product doc) | `pulumi-provider-overview.md`, `pulumi-getting-started.md` |
| **Provider source, package names per language, local dev build (`make development`), the 404-on-`pulumi up` / `+dirty` version-string gotcha** | `gh-twingate-pulumi-twingate.md` — this is `Twingate/pulumi-twingate`, the actively maintained provider (do not confuse with any `Twingate-Labs/pulumi-twingate`, which would be archived if it appears elsewhere) |
| **SE quick-start / demo Pulumi scripts per cloud** (reference only, not production-hardened) | `gh-twingate-solutions-pulumi-scripts.md` |
| AWS-specific Pulumi patterns (EC2/ECS + Twingate) | `pulumi-aws.md` (and `skills/twingate-connectors/references/aws-connector-patterns.md`) |
| Azure-specific Pulumi patterns (ACI/VMs + Twingate) | `pulumi-azure.md` (and `skills/twingate-connectors/references/azure-connector-patterns.md`) |
| GCP-specific Pulumi patterns (GCE/MIG + Twingate) | `pulumi-gcp.md` (and `skills/twingate-connectors/references/gcp-connector-patterns.md`) |
| Resource semantics or API behavior the Pulumi docs don't cover | `skills/twingate-terraform/references/terraform-provider-overview.md` (underlying API is identical) |
| Exact SDK method signatures per language | `gh-twingate-pulumi-twingate.md`, the provider source repo, and the Pulumi Registry |

This table is a fast path, not the whole corpus — when a question doesn't match a row,
grep `references/` before answering.
