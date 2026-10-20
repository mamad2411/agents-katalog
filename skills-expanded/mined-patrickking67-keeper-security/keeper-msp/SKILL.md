---
name: keeper-msp
description: Manage a Keeper MSP tenant using Keeper Commander CLI (keeper) - managed companies, licenses and add-ons, MSP billing reports, and running commands inside a managed company via switch-to-mc / switch-to-msp. Use when the user mentions Keeper MSP, managed company, MC, msp-info, MSP billing, license allocation, plan or add-on changes for a managed company, converting a node to a managed company, distributor accounts, or administering many Keeper tenants from one console. For single-tenant enterprise administration use the keeper-admin skill; for runtime secret retrieval use keeper-secrets.
---

# Keeper MSP Management (keeper)

Keeper MSP lets a Managed Service Provider administer many customer tenants
(Managed Companies, "MCs") from one console. Commander exposes the full MSP
surface: license pools, MC lifecycle, billing reports, and the ability to run
any Commander command *inside* a managed company.

## Official documentation

- [MSP Management Commands](https://docs.keeper.io/keeperpam/commander-cli/command-reference/msp-management-commands) - full command reference
- [Keeper MSP](https://docs.keeper.io/enterprise-guide/keeper-msp) - MSP platform guide
- The **keeper-docs** MCP server bundled with this plugin can search these docs live (`searchDocumentation`, `getPage`).

## When to Use MSP Commands

| Need | Command family |
| --- | --- |
| See license pools and managed companies | `msp-info` |
| Create / remove a managed company | `msp-add`, `msp-remove` |
| Change an MC's plan, seats, storage, add-ons | `msp-update` |
| Monthly billing / consumption reports | `msp-billing-report`, `msp-legacy-report` |
| Run admin commands inside one MC | `switch-to-mc` ... `switch-to-msp` |
| Convert an enterprise node into an MC | `msp-convert-node` |
| Copy role enforcements MSP -> MCs | `msp-copy-role` |
| Distributor (multi-MSP) management | `distributor info`, `distributor license` |

Everything else (users, teams, roles, reports inside a tenant) is the
**keeper-admin** skill - run it inside the right context.

## Prerequisites

1. Python 3.10+ and `pip install keepercommander` (see keeper-setup skill)
2. An MSP-type Keeper account with MSP Admin privileges
3. Logged-in Commander session (`keeper shell`, persistent login recommended)

Check: `keeper version`, then `msp-info` in the shell.

Follow the tmux-session pattern from the **keeper-admin** skill for all
interactive Commander work - MSP commands run in the same `keeper shell`.

## Managed Companies and Licensing

```bash
My Vault> msp-info                 # license pools + managed companies (IDs!)
My Vault> msp-down                 # refresh local MSP data from server

My Vault> msp-add --plan=enterprise --seats=10 "Acme Corp"
# Plans: business, businessPlus, enterprise, enterprisePlus
# The new MC id is stored in the last_mc_id environment variable

My Vault> msp-update "Acme Corp" --seats 25 --file-plan 1tb
My Vault> msp-update "Acme Corp" --add-addon secrets_manager
My Vault> msp-update "Acme Corp" --remove-addon chat
# Add-ons include: compliance_report, enterprise_audit_and_reporting,
# secrets_manager, enterprise_breach_watch, connection_manager,
# password_rotation, remote_browser_isolation, privileged_access_manager,
# keeper_endpoint_privilege_manager

My Vault> msp-remove "Acme Corp"   # DESTRUCTIVE - confirm with the user first
```

## Context Switching (switch-to-mc)

`switch-to-mc` changes the whole session context: every subsequent command runs
as an administrator of that managed company until `switch-to-msp`.

```bash
My Vault> msp-info                 # find the MC ID first
My Vault> switch-to-mc 3987
Acme Corp> enterprise-info         # now operating inside the MC
Acme Corp> enterprise-user --invite user@acme.com
Acme Corp> switch-to-msp           # ALWAYS return to MSP context when done
```

Rules:

1. Always resolve the MC ID with `msp-info` first - never guess an ID.
2. Treat `switch-to-mc <id> -> commands -> switch-to-msp` as one self-contained
   block. Never leave a session parked in MC context.
3. State clearly in your output which tenant a command ran against.

## Billing and Reporting

```bash
My Vault> msp-billing-report --month 2026-06 --show-company --format csv --output billing.csv
My Vault> msp-billing-report --month 2026-06 --show-date
My Vault> msp-legacy-report        # legacy license usage
```

## Node Conversion and Role Copy

```bash
My Vault> msp-convert-node "Branch Node"   # convert node -> managed company
# WARNING: remove SSO provisioning from the node BEFORE converting

My Vault> msp-copy-role "Acme Corp" --role "Desktop Users"
```

## Distributor Accounts

Distributor accounts manage multiple MSPs:

```bash
My Vault> distributor info --mc-details
My Vault> distributor msp-info <MSP>
My Vault> distributor license <MSP>    # view/edit an MSP's license options
```

## References

- Use `references/msp-commands.md` for the full switch/flag reference of every
  MSP and distributor command.

## Guardrails

- `msp-remove` and `msp-convert-node` are destructive or hard to reverse -
  always confirm with the user and restate the target MC/node before running.
- License changes (`msp-update`) affect customer billing - restate plan, seats,
  and add-ons and get confirmation before executing.
- Never leave the session in a managed-company context; end every MC block
  with `switch-to-msp`.
- Never expose vault secret values while in an MC context - the keeper-admin
  guardrails apply inside every tenant.
- If a command's syntax is uncertain, run `help <command>` or check the
  official MSP docs (via the keeper-docs MCP server) instead of guessing.
