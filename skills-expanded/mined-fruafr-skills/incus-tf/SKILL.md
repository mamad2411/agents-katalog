---
name: incus-tf
description: Ground AI responses, Terraform project generation, and infrastructure-as-code questions in offline authoritative terraform-incus provider documentation. Must be loaded before generating Terraform configurations for Incus, writing HCL that references incus_* resources/data sources, or answering questions about managing Incus with Terraform. Reduces hallucinations by routing all claims through verified reference files.
license: Apache-2.0
compatibility: Requires incus-tf/references/docs/index.md (doc index), incus-tf/references/docs/provider-index.md (provider overview), incus-tf/references/docs/resources/ (per-resource docs), and incus-tf/references/docs/data-sources/ (per-data-source docs) in the skill folder.
allowed-tools: read glob grep bash
metadata:
  status: active
  version: 1.0.0
  updated: 2026-07-25
  author: David HEURTEVENT
  source: https://github.com/fruafr/skills/tree/main/skills/incus-tf
  owner: David HEURTEVENT
  tags: incus, terraform, infrastructure-as-code, container, virtual-machine, virtualization, iac, hcl, terraform-provider
---

# Skill: incus-tf

- **Purpose:** Ground every terraform-incus provider answer, Terraform configuration, and HCL snippet in authoritative offline documentation to eliminate hallucinations.
- **Use when:** The user asks to generate Terraform configurations for Incus, asks about `incus_*` resources or data sources, wants to manage Incus with Terraform, or asks questions about the lxc/incus Terraform provider.
- **Don't use when:** The question is purely about Incus CLI commands (use incus-doc skill), general Terraform concepts unrelated to the Incus provider, or non-Incus Terraform providers.
- **Success looks like:** Every `incus_*` resource/data source name, argument, attribute, and configuration option is verified against the skill's reference files before being emitted; no fabricated resource types, arguments, or behaviors.

## Inputs

This skill does not require explicit inputs — it activates on context (mentions of terraform-incus, incus_* resources, managing Incus with Terraform). The skill's own reference files serve as the input.

**Assumptions:**
- The `references/` directory within the skill folder (`incus-tf/references/`) exists and is up to date.
- `incus-tf/references/docs/index.md` contains the authoritative documentation tree with links to all markdown files in `incus-tf/references/docs/`.
- `incus-tf/references/docs/provider-index.md` contains the provider overview including authentication, remote configuration, and environment variables.
- Resource documentation files are in `incus-tf/references/docs/resources/`.
- Data source documentation files are in `incus-tf/references/docs/data-sources/`.

## Output

**Format:** Grounded answer / Terraform HCL configuration / corrected resource block

Every `incus_*` resource or data source name, argument, attribute, or configuration option **must** be traceable to a reference file. If the reference does not contain the claim, the claim must not be emitted.

## Reasoning

1. **Understand** — Parse the user request; identify all `incus_*` resources, data sources, arguments, and provider configuration blocks.
2. **Plan** — Determine which reference files to consult:
   - Provider configuration (authentication, remotes, environment variables) → `incus-tf/references/docs/provider-index.md`
   - Resource arguments and attributes → `incus-tf/references/docs/resources/<resource>.md`
   - Data source arguments and attributes → `incus-tf/references/docs/data-sources/<datasource>.md`
   - Full documentation tree navigation → `incus-tf/references/docs/index.md`
3. **Generate** — Produce answer with every `incus_*` element verified.
4. **Verify** — Re-read relevant reference lines to confirm every resource type, argument, and attribute exists.

**When uncertain:** Consult reference files. If not covered, state "Not found in the terraform-incus provider reference documentation."

## Decision Rules

| If | Then |
|----|------|
| User asks about provider setup/auth | Open `incus-tf/references/docs/provider-index.md`, answer from it |
| User asks about an `incus_*` resource | Open `incus-tf/references/docs/index.md`, find resource, open linked `incus-tf/references/docs/resources/<resource>.md`, answer from it |
| User asks about an `incus_*` data source | Open `incus-tf/references/docs/index.md`, find data source, open linked `incus-tf/references/docs/data-sources/<datasource>.md`, answer from it |
| User asks to generate Terraform config | Verify every resource/data source type and its arguments against its reference file |
| User asks about provider-supported features | Consult relevant resource/data source doc and provider-index.md |
| Not in references | "This is not covered in the bundled terraform-incus provider reference documentation." |

## Documentation Pages

### Provider

| Page | Summary |
|------|---------|
| [provider-index](references/docs/provider-index.md) | Provider configuration, authentication, remotes, environment variables |

### Resources

| Page | Summary |
|------|---------|
| [certificate](references/docs/resources/certificate.md) | Manage Incus client certificates |
| [cluster_group](references/docs/resources/cluster_group.md) | Manage Incus cluster groups |
| [image](references/docs/resources/image.md) | Manage locally-stored Incus images |
| [instance](references/docs/resources/instance.md) | Manage Incus instances (containers and VMs) |
| [instance_snapshot](references/docs/resources/instance_snapshot.md) | Manage Incus instance snapshots |
| [network](references/docs/resources/network.md) | Manage Incus networks |
| [network_acl](references/docs/resources/network_acl.md) | Manage Incus network ACLs |
| [network_address_set](references/docs/resources/network_address_set.md) | Manage Incus network address sets |
| [network_forward](references/docs/resources/network_forward.md) | Manage Incus network forwards |
| [network_integration](references/docs/resources/network_integration.md) | Manage Incus network integrations |
| [network_load_balancer](references/docs/resources/network_load_balancer.md) | Manage Incus network load balancers |
| [network_peer](references/docs/resources/network_peer.md) | Manage Incus network peers |
| [network_zone](references/docs/resources/network_zone.md) | Manage Incus network zones |
| [network_zone_record](references/docs/resources/network_zone_record.md) | Manage Incus network zone records |
| [profile](references/docs/resources/profile.md) | Manage Incus profiles |
| [project](references/docs/resources/project.md) | Manage Incus projects |
| [server](references/docs/resources/server.md) | Manage Incus server configuration |
| [storage_bucket](references/docs/resources/storage_bucket.md) | Manage Incus storage buckets |
| [storage_bucket_key](references/docs/resources/storage_bucket_key.md) | Manage Incus storage bucket keys |
| [storage_pool](references/docs/resources/storage_pool.md) | Manage Incus storage pools |
| [storage_volume](references/docs/resources/storage_volume.md) | Manage Incus storage volumes |

### Data Sources

| Page | Summary |
|------|---------|
| [cluster](references/docs/data-sources/cluster.md) | Query Incus cluster information |
| [image](references/docs/data-sources/image.md) | Query locally-stored Incus images |
| [instance](references/docs/data-sources/instance.md) | Query Incus instances |
| [network](references/docs/data-sources/network.md) | Query Incus networks |
| [network_acl](references/docs/data-sources/network_acl.md) | Query Incus network ACLs |
| [network_address_set](references/docs/data-sources/network_address_set.md) | Query Incus network address sets |
| [network_forward](references/docs/data-sources/network_forward.md) | Query Incus network forwards |
| [network_integration](references/docs/data-sources/network_integration.md) | Query Incus network integrations |
| [network_load_balancer](references/docs/data-sources/network_load_balancer.md) | Query Incus network load balancers |
| [network_peer](references/docs/data-sources/network_peer.md) | Query Incus network peers |
| [network_zone](references/docs/data-sources/network_zone.md) | Query Incus network zones |
| [profile](references/docs/data-sources/profile.md) | Query Incus profiles |
| [project](references/docs/data-sources/project.md) | Query Incus projects |
| [storage_bucket](references/docs/data-sources/storage_bucket.md) | Query Incus storage buckets |
| [storage_pool](references/docs/data-sources/storage_pool.md) | Query Incus storage pools |
| [storage_volume](references/docs/data-sources/storage_volume.md) | Query Incus storage volumes |

## Guardrails

**Must:** Consult references before every `incus_*` claim · cite reference file path · verify every resource type, argument, and attribute exists before using · open specific doc file for exact resource/data source.

**Must not:** Invent resource types, arguments, or configuration options · guess HCL syntax for incus resources · output unverified `incus_*` blocks · reference non-existent documentation paths.

**Priority:** [1] Exact resource/data source doc text > [2] Provider overview > [3] No answer

## Edge Cases

| Situation | Response |
|-----------|----------|
| Missing reference files | Refuse: "terraform-incus provider reference files not found." |
| Resource exists but argument not in doc | Don't use the argument |
| Feature not in docs | "Not covered in bundled terraform-incus provider reference documentation." |
| User asks about incus CLI (not Terraform) | "This skill covers the Terraform Incus provider, not the incus CLI. Use the incus-doc skill for CLI questions." |
| User asks about non-Incus Terraform provider | "This skill only covers the lxc/incus Terraform provider." |
| Complex config with many resources | Verify each resource type and its arguments independently |

## Self-Check (run before returning)

- [ ] Correctness — every `incus_*` resource/data source/argument verified against a reference file
- [ ] Format — output contains reference file paths for traceability
- [ ] Safety — no fabricated Terraform resources or arguments
- [ ] Completeness — all incus Terraform-related parts addressed

**If a check fails after 2 attempts:** Refuse with "Unable to ground the answer in the terraform-incus provider reference documentation."

## Examples

**Good:** User asks "How do I create an incus container with Terraform?" → Agent opens `incus-tf/references/docs/index.md`, finds `instance` resource → `incus-tf/references/docs/resources/instance.md`, reads arguments (`name`, `image`, `type`), answers with verified HCL.

**Bad:** User asks "Use `incus_init` resource" → Agent guesses `incus_init` is valid, but it doesn't exist in the reference files. Correct: use `incus_instance`.

## Change log

- v1.0.0 — initial: Ground all terraform-incus provider AI output in bundled offline documentation to eliminate hallucinations.
