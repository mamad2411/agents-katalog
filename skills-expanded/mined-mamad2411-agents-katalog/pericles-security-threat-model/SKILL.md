---
name: pericles-security-threat-model
version: 2026.05.0
description: >
  The Pericles threat model in build terms — what an attacker (or a poisoned data feed,
  or a malicious Custom Skill) could try, and the controls that stop it. Use this
  WHENEVER you handle untrusted content, add egress, build Custom Skill support, or
  review a security-sensitive change. Encodes the five tenant-isolation guarantees,
  prompt-injection defenses, the egress allowlist (MCP-only), PII/exfiltration
  prevention, the Custom Skill sandbox, and the P0 response.
doctrine_refs: [Security Spec (all); §5, §8, §9]
depends_on: [pericles-tenant-isolation, pericles-prompts, pericles-mcp-layer, pericles-execution-node]
last_reconciled: 2026-05-28
---

# Pericles Security Threat Model (build skill)

Pericles ingests adversarial inputs (customer documents, external feeds), runs LLMs that
can be manipulated, serves mutually distrustful tenants, and (in Standard/Enterprise)
runs customer-authored Custom Skills. This skill is the consolidated threat model and
the controls — most live in other skills; here they're assembled so a reviewer can reason
about the whole.

## When to use this skill

Handling untrusted content; adding network egress; building/reviewing Custom Skill
support; any security-sensitive change; threat-modeling a new feature.

## Threats → controls

| Threat | Control | Skill |
|---|---|---|
| Cross-tenant data access | `organization_id` on every query/tool/log; auth-layer binding via `UserOrganization`; the five guarantees | `pericles-tenant-isolation` |
| Prompt injection via customer docs / feeds | treat as untrusted DATA; `<untrusted_content>` boundary marking; strict output-schema validation | `pericles-prompts` |
| Cross-Skill contagion | only schema-validated structured data crosses Skill boundaries | `pericles-prompts` |
| Data exfiltration / egress | Custom Skills egress ONLY to registered MCP servers; MCP enforces tenant scoping; non-allowlisted egress = P0 | `pericles-mcp-layer` |
| Unauthorized consequential action | supervisors propose, deterministic Execution Nodes commit + independent rule validation + approval gate | `pericles-execution-node` |
| Malicious Custom Skill | sandbox: no DB access (data via MCP), no filesystem/env/secrets outside declared `knowledge_sources`, allow-listed libraries, can't invoke Execution Nodes directly, namespace-bound | `pericles-tenant-isolation`, `pericles-custom-skill` |
| Capability over-reach | capability minimization: declare only needed deps/sources | `pericles-prompts`, `pericles-skill-authoring` |
| Version tampering | registry pinning + lifecycle gates; post-promotion tamper = P0 | `pericles-skill-registry` |
| PII / facial data harvesting | never collect/compile PII across sources; never scrape facial images | this skill |

## Custom Skill sandbox (the highest-risk surface)

A Custom Skill (Standard/Enterprise) runs **untrusted customer code**. It must: resolve
only within `tenant/<active>` + platform; reach data **only via MCP** (no direct DB);
have no filesystem/env/secret access beyond declared `knowledge_sources`; import only
allow-listed libraries; never invoke an Execution Node directly; and pass the four-stage
review before activation (`pericles-custom-skill`, post-MVP). A sandbox escape is P0.

## Untrusted-content rules (always on)

Customer documents and external API/MCP responses are untrusted: boundary-mark them,
validate against schemas, never let them become instructions, and screen at ingestion
(`pericles-org-memory`, `pericles-external-feeds`).

## P0 response

Confirmed cross-tenant leak, Custom Skill sandbox escape, non-allowlisted egress, or
post-promotion version tamper → pause the capability platform-wide; investigate; notify
affected customers within 4h; postmortem within 5 business days; prevention plan within
30 days. P1 = strong anomaly without confirmation (24h).

## What this forbids

Trusting untrusted content as instructions; egress outside registered MCP servers;
Custom Skills with DB/filesystem/secret access or non-allowlisted imports; committing
actions outside an Execution Node; collecting PII across sources or scraping facial
images; shipping a security-sensitive change without threat-model review.

## Verification

Untrusted content is boundary-marked + schema-validated; egress is allowlisted and
tenant-scoped; Custom Skills run only in the sandbox; consequential actions go through
Execution Nodes; tests cover injection, cross-tenant access, and egress attempts; P0
runbook is wired.

## Existing standards (read alongside)

Skills Security Spec (Notion); `.cursor/rules/100-security/{101-security-coding,102-password-security}-*`;
`.claude/rules/11-security.md`; `pericles-tenant-isolation`, `pericles-prompts`,
`pericles-mcp-layer`.

## Open questions

- The library allow-list and sandbox runtime for Custom Skills — define before Custom
  Skills ship (`pericles-custom-skill`).
- Automated injection/egress red-team tests in CI — build a suite.

## Changelog

- 2026.05.0 — Initial draft; consolidated threat→control table from the Security Spec and
  the related skills.
