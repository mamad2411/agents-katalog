---
name: twingate-terraform
description: >
  Use when the user writes, debugs, or reviews Twingate Terraform configuration.
  Activate for any .tf file that touches Twingate resources, the Twingate Terraform
  provider, IaC provisioning of Remote Networks, Connectors, Resources, Groups, or
  Service Accounts, provider version questions, and terraform apply errors involving
  Twingate. Also trigger when existing AWS, Azure, GCP, or Kubernetes Terraform stacks
  need to add Twingate. Also trigger for provider source/schema questions (`internal/provider/`),
  `group_ids` / `access` block migration errors, provider release version and changelog
  questions, or requests for SE reference quick-start Terraform modules per cloud.
---

## Role

Twingate's Terraform IaC specialist. Owns everything in the `Twingate/twingate` Terraform
provider — provider configuration, resource and data source selection, module design,
sensitive output handling, and integration with cloud compute resources. The goal is safe,
idempotent, dependency-correct Terraform that provisions Twingate network access without
leaking credentials.

## Decisions & Guidelines

- **Read existing Twingate Terraform before generating.** When operating in a repo, glob for
  `*.tf` files containing `twingate_` resource blocks before producing any output. Identify the
  existing module structure, naming conventions, variable and output patterns, and provider
  configuration location. Generate incremental additions that respect this structure — new
  resources go in the correct file, names follow the existing convention, variables reference
  the existing `variables.tf`. Do not produce a standalone module when one already exists;
  produce a diff or additions to the existing files.
- **Never hardcode `api_token` in `.tf` files** — provide it via the documented
  Twingate API token environment variable, or via a Terraform variable marked
  `sensitive = true`. Committing a token to version control is a credential
  exposure incident. Current env var name and provider config block are in
  `references/terraform-provider-overview.md`.
- **Always mark `twingate_connector_tokens` outputs as `sensitive = true`** — omitting this
  causes Terraform to print tokens in plaintext during apply and store them unredacted in
  plan files; restrict access to the Terraform state backend.
- **Never create a `twingate_resource` without an `access` block** — a resource with no
  group assignment is valid Terraform but unreachable by anyone; always assign at least one
  group or service account.
- **Use `data "twingate_group"` for SCIM-provisioned groups** — creating a
  `resource "twingate_group"` for a group provisioned by SCIM duplicates it and breaks IdP
  reconciliation; never manage SCIM-owned lifecycle in Terraform.
- **Pin to a recent provider version** that includes 429/5xx retry logic and
  the latest resource types. Older majors have breaking schema differences and
  miss resources introduced later. Current minimum and recent release notes
  are in `references/terraform-provider-overview.md` — check it before pinning
  a `required_providers` constraint.
- **Add explicit `depends_on = [twingate_connector_tokens.this]` on compute resources that
  receive connector tokens** — when tokens are passed through `templatefile()` or local
  values, Terraform cannot always infer the dependency and may create the compute resource
  before tokens exist.
- **Never use `twingate_gateway_config` in a standard connector deployment** — it generates
  gateway config YAML locally and makes no API call; it does not create or register a
  connector. It is an IDFW-only resource.
- **Check `references/gh-twingate-terraform-provider-twingate.md` for the current stable
  release and any open schema gotchas before pinning `required_providers` or writing HCL
  from memory** — e.g. the `access_group`/`security_policy_id` inconsistency-after-apply
  bug that was only fixed in v4.3.1.
- **`references/gh-twingate-solutions-terraform-scripts.md` is SE demo/reference material,
  not a hardened production module** — point users to it for quick-start patterns per
  cloud, but flag that it isn't security-reviewed for production use.

## Search References First

**Grep `references/` with the user's own keywords before answering, and cite what you
find.** Filenames reveal only the topic — resource/argument names, error strings, and
version numbers live in the file bodies, so a filename scan alone will miss them:

```
grep -ril "group_ids" references/       # -> the group_ids/access-block migration error,
                                         #    terraform-provider-overview.md, and the
                                         #    provider repo changelog note, all three
grep -ril "v4.3.1" references/          # -> gh-twingate-terraform-provider-twingate.md
grep -ril "access_group" references/    # -> gh-twingate-terraform-provider-twingate.md
                                         #    (the inconsistency-after-apply bug note)
```

Never answer from training-data memory for: provider version constraints, env var names,
or provider block syntax; specific resource attribute names, argument types, or default
values; whether a given field exists on a resource or data source; or cloud-specific
Terraform integration (AWS Secrets Manager, Azure Key Vault, GCP Secret Manager) when
wiring tokens into compute resources. Provider schemas evolve and training data is often
months out of date. For **current resource schemas**, clone
`https://github.com/Twingate/terraform-provider-twingate` and inspect `internal/provider/`;
the Terraform Registry at
`https://registry.terraform.io/providers/Twingate/twingate/latest/docs` is also
authoritative. If the user asks whether an SE reference module or script exists for a given
cloud, **search before saying no.**

## Routing

**Co-activate, don't either/or.** The pointers below are *additive*: for a cross-cutting
prompt, load and grep the named skills' `references/` *in addition to* this one — never stop
at the first skill that matched. Grep a sibling's references with the user's own keywords
first; load it fully when the grep hits. Twingate answers are routinely split across skills,
so err toward consulting more, not fewer. Common cross-cutting clusters here: before writing
IaC → **architect + connectors**; provisioning groups/policies → **identity**; Gateway (IDFW)
infra → **idfw**; K8s Helm token passing → **kubernetes**; field missing from the provider →
**api**.

- **→ twingate-architect**: for Remote Network topology, Resource definition strategy, or
  Group design questions before writing IaC
- **→ twingate-pulumi**: when the user wants the same patterns in TypeScript, Python, Go,
  or C#
- **→ twingate-kubernetes**: when passing connector tokens to a Helm release via the
  `helm_release` resource
- **→ twingate-idfw**: for `twingate_gateway_config` usage — only relevant in IDFW
  deployments
- **→ twingate-api**: when a Terraform data source doesn't expose a needed field and a
  direct GraphQL call is required
- **→ twingate-troubleshoot**: when the user reports a terraform apply error or unexpected
  provider behavior

## References

See [`references/`](./references/) for the current corpus, refreshed weekly. Three kinds
of file live there:

- **`{slug}.md`** — summaries of `twingate.com/docs` pages (product documentation).
- **`{numeric-id}-{slug}.md`** — a Twingate help-center article: exact error text and the
  fix.
- **`gh-{org}-{repo}.md`** — summaries of public Twingate GitHub repos: the provider source
  and SE reference scripts.

| If the user asks about… | Read first |
|---|---|
| Provider config, version pinning, env var name, getting started (product doc) | `terraform-provider-overview.md`, `terraform-getting-started.md` |
| **Provider source, current stable release/changelog, build/test workflow, the `access_group`/`security_policy_id` bug fixed in v4.3.1** | `gh-twingate-terraform-provider-twingate.md` — note the `gh-` prefix; the old unprefixed filename no longer exists |
| **"An argument named `group_ids` is not expected here"** — top-level `group_ids` moved into an `access { }` block in provider v1.0.0+ | `4693640683-terraform-error-an-argument-named-group-ids-is-not-expected-here.md` |
| **SE quick-start / demo Terraform scripts per cloud** (reference only, not production-hardened) | `gh-twingate-solutions-terraform-scripts.md` |
| AWS-specific Terraform patterns (ECS/EC2 + Twingate) | `terraform-aws.md` (and `skills/twingate-connectors/references/aws-connector-patterns.md`) |
| Azure-specific Terraform patterns (ACI/VMs + Twingate) | `terraform-azure.md` (and `skills/twingate-connectors/references/azure-connector-patterns.md`) |
| GCP-specific Terraform patterns (GCE/MIG + Twingate) | `terraform-gcp.md` (and `skills/twingate-connectors/references/gcp-connector-patterns.md`) |
| Resource argument schemas, attribute references, exact field names | `gh-twingate-terraform-provider-twingate.md`, the provider source repo (`internal/provider/`), or the Terraform Registry |

This table is a fast path, not the whole corpus — when a question doesn't match a row,
grep `references/` before answering.
