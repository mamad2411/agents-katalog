---
name: enterprise-admin
description: Administer a Keeper enterprise via Commander - users, teams, roles, nodes, device approvals, KSM Applications, and the compliance reports that show who can access which records, all over decrypted metadata only. Use when asked to review or manage enterprise users/teams/roles/nodes, approve devices, audit access, or run a compliance report.
---

# Keeper Enterprise Administration

Commander's enterprise surface manages the people and access structure of a
Keeper tenant and produces the audit evidence security teams need. Everything
here works over **metadata**, never secret values. Drive Commander through the
tmux shell pattern in the **keeper-admin** skill.

## Structure

- **Nodes** - the org hierarchy; users, teams, and roles live under nodes.
- **Users** - accounts; can be invited, locked, unlocked, moved between nodes,
  added to roles/teams. SCIM-provisioned users may be queued pending key creation.
- **Teams** - group users for sharing; carry restrictions (edit, share, view).
  SCIM-created teams can be queued until approved.
- **Roles** - enforcement policies (MFA, rotation rights, PAM capabilities like
  "can launch connections", "can rotate credentials").

```bash
My Vault> enterprise-info                # tree overview (alias: ei)
My Vault> enterprise-info --users --teams --roles --nodes
My Vault> enterprise-user --invite user@company.com    # alias: eu
My Vault> enterprise-user --lock user@company.com
My Vault> enterprise-team --add "Engineering"          # alias: et
My Vault> enterprise-role --add-user user@company.com --role "Admin Role"
My Vault> device-approve                 # pending device approvals
```

## Compliance reports (the audit surface)

Because Keeper is **zero-knowledge**, compliance reports decrypt only record
*metadata* - title, type, URL - using the enterprise private key, restricted
to admins with Compliance Reporting permission. Report types:

```bash
My Vault> compliance-report --username user@co.com     # owned records + sharing
My Vault> compliance record-access-report --user user@co.com   # historical access
My Vault> compliance team-report -tu                   # teams -> shared folders (+ members)
My Vault> compliance shared-folder-report              # entities per shared folder
```

Reports use a cache built on first run (slow for large tenants); scope by user
to speed it up. Separate **currently accessible** (vault view) from
**historically accessed** (record-access) - they answer different audit
questions.

## KSM Applications

Enterprise admins also manage the KSM Applications and Client Devices behind
Secrets Manager (`secrets-manager app list`, `secrets-manager client add`).
Reviewing an Application's scope is a least-privilege check: a device should
bind to only the records its workload needs. Runtime secret retrieval belongs
to the keeper-secrets plugin.

## Safe handling

Compliance reports are metadata-only and require admin permission. Never
retrieve or display a secret value during an access review. Propose
user/team/role/sharing changes; never execute a lock, delete, revoke, or share
change without explicit confirmation. Treat report generation as an audited
action.
