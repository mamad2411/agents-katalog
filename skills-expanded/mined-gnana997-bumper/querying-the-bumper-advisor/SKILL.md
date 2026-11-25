---
name: querying-the-bumper-advisor
description: Looks up authoritative security knowledge from the bumper Advisor — CVEs and other vulnerability advisories, malicious-package reputation, and Infrastructure-as-Code misconfiguration rules (Terraform, Kubernetes, Dockerfile, CloudFormation). Use when you need ground-truth detail on a vulnerability, whether a package is safe to install, or what a security finding means, instead of guessing.
---

# Querying the bumper Advisor

The bumper Advisor is a hosted knowledge base of CVEs, malicious packages, and IaC
misconfiguration rules. Reach for it instead of guessing about a vulnerability, a
package's safety, or a security finding. Only package names, versions, and queries
leave the machine — never your code. Needs the `bumper` CLI and/or the
`bumper-advisor` MCP wired by `bumper init` (https://github.com/gnana997/bumper).

## How to reach it

Preferred — the `bumper-advisor` MCP server. Use fully-qualified tool names:

- `bumper-advisor:lookup_cve` — CVEs affecting a package at a version (ecosystem, package, version)
- `bumper-advisor:get_vuln` — full detail for one advisory id (CVE/GHSA); set `include_insight` for an AI-enriched explanation
- `bumper-advisor:check_malware` — is a package known-malicious? (ecosystem, package)
- `bumper-advisor:search_cve` — search CVEs by keyword / ecosystem / severity
- `bumper-advisor:search_rules` — find IaC rules by keyword / provider / severity
- `bumper-advisor:get_rule` — full detail for one IaC rule (source, source_id)

Fallback — the CLI (no MCP):
- `bumper search <query>` — search the bundled IaC ruleset
- `bumper explain <RULE_ID>` — one IaC rule in detail
- `bumper deps --json <lock>` — vuln/malware data for a lockfile

## When to use which

- "Is X safe to install?" → `bumper-advisor:check_malware`, then `lookup_cve`.
- "What does CVE-2023-… mean / how do I fix it?" → `bumper-advisor:get_vuln`.
- "What's wrong with this Terraform/K8s/Dockerfile?" → `bumper-advisor:search_rules`
  then `get_rule` (or `bumper plan.json` for a full plan scan).

## Example

User: "is the `event-stream` npm package safe?"
→ `bumper-advisor:check_malware ecosystem=npm package=event-stream`
→ flagged malicious (historic backdoor). Advise against it; suggest a maintained
  alternative.

## Full, version-matched reference

For the complete tool reference for this installed bumper version:
```
bumper skills get advisor
```
