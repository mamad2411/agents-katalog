---
name: azure-hsm-incident-response-review
description: Helps agents create and review incident response plans for Azure Key Vault Managed HSM incidents, including suspected key exposure, unsafe export attempts, suspicious cryptographic use, compromised identity, lockout, failed restore, key deletion, purge risk, and security-domain handling. Use when the user mentions key exposure, compromise, leak, incident, IR, forensic review, recovery, or emergency rotation.
license: MIT
compatibility: Requires current Azure and organizational incident-response documentation for production procedures.
---

# Azure HSM Incident Response Review Skill

Use this skill when planning or reviewing Managed HSM incident response.

## Approach

1. Classify the incident: suspected exposure, access compromise, cryptographic misuse, key deletion, purge risk, lockout, security-domain issue, backup/restore issue, or service outage.
2. Preserve evidence before destructive changes where possible.
3. Freeze unsafe access and high-risk identities.
4. Determine affected keys, key versions, roles, scopes, consuming services, and data protected by the key.
5. Plan emergency rotation or cutover without prematurely purging old key versions needed for recovery.
6. Review logs, audit events, role assignments, service errors, and deployment changes.
7. Coordinate explicit approval for restore, purge, security-domain, or role-removal operations.

## Workflow

Use `workflows/incident-response-review-workflow.md` to build or review an incident response plan.

## Resource

Use `resources/incident-response-runbook-template.md` for runbook drafting.

## Example

Use `examples/key-exposure-triage-notes.md` for triage guidance.
