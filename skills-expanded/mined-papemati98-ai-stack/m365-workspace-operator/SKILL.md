---
name: m365-workspace-operator
description: "Inspect or manage Microsoft 365 workspaces: Teams, SharePoint sites/lists, Planner, Microsoft Graph and Entra applications/consent. Use for M365 integration diagnostics, resource discovery, permission planning and explicitly authorized operations, including a configured managed MCP connector. Reuse cloud-org-operator for tenant/account selection. Do not activate for unrelated web coding or ordinary email reading."
---

# Microsoft 365 workspace operator

Find the existing resource and its owner before proposing a replacement. A Teams
tab, a SharePoint list, an Entra application and a Graph permission are different
objects; availability in a tenant does not make them accessible through this MCP.

## Short path

1. Identify the requested company, project, operation and source of truth from
   the current task and its existing context. Reuse known IDs and the parent's
   verified context. Do not rescan a tenant or ask for already confirmed values.
2. For actual cloud access, use `cloud-org-operator` once for the selected
   execution channel and intent. Bind tenant, principal, connector and, when
   relevant, SharePoint host/site. A current login or connector label alone is
   insufficient. Offline planning needs no login or new registry.
3. Check the currently exposed tool and its schema. Choose a targeted read and
   expand only when necessary. Apply the relevant reference below; do not load
   every reference or enumerate every service.
4. Return the useful result or prepare the exact change: target IDs, endpoint,
   required permission, desired diff, verification and narrow recovery. Execute
   only within existing authorization and connector boundaries. Missing tools
   do not authorize switching to a wider Graph client or expanding consent.

## Read only the needed branch

| Task | Reference |
| --- | --- |
| MCP discovery, denied tool, client authentication, managed read-only connector | [Managed MCP capabilities](references/mcp-and-initech.md) |
| Team/channel/site/list mapping, Graph errors, Planner, synchronization | [Graph and data](references/graph-and-data.md) |
| App registrations, service principals, scopes, consent, access errors | [Entra and permissions](references/entra-and-permissions.md) |

For a Teams tab, bot, Adaptive Card or app package use `teams-app-engineering`
for that development slice. Keep M365 operations here; do not start two plans.

Use existing task evidence for IDs and mappings; do not invent a new central
register. Report partial discovery and access denial as such, not as absence.
Keep resource contents, employee data and credentials out of Office and shared
knowledge. A redacted count, result and opaque local evidence reference suffice.

For mutations, verify the live target immediately before execution under the
existing organization gate. No new IAM grants, deletion, app publication, real
notifications or production configuration changes without the required owner's
authorization. This skill does not expand that authorization.
