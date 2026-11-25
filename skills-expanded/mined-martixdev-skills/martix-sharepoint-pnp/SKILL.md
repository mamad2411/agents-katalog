---
name: martix-sharepoint-pnp
description: >-
  Standalone-first SharePoint PnP guidance for tool selection, provisioning,
  automation, authentication, and cross-tool delivery using PnP PowerShell, CLI
  for Microsoft 365, and PnPjs. Use this skill whenever the user mentions PnP
  PowerShell cmdlets (for example Connect-PnPOnline), CLI for Microsoft 365
  SharePoint commands (for example m365 spo), PnPjs, provisioning templates,
  site scripts or site designs, tenant automation, SharePoint scripting, or
  choosing among these tooling paths for SharePoint delivery. Keep scope on
  tooling, automation, provisioning, auth, and operational safety. Do not use
  for classic farm-solution packaging or pure SPFx component implementation.
license: Complete terms in LICENSE.txt
---

## MartiX SharePoint PnP router

- Standalone-first skill package focused on SharePoint PnP guidance for provisioning, automation, auth, PnP PowerShell, CLI for Microsoft 365, PnPjs, and cross-tool delivery practices.
- Keep decisions grounded in the bundled rule files and reference maps.
- Use [AGENTS.md](./AGENTS.md) when the task crosses multiple workstreams or needs the long-form review routes, package inventory, or maintainer guidance.

## When to use this skill

- Choose between PnP PowerShell, CLI for Microsoft 365, and PnPjs for SharePoint automation or provisioning.
- Set up authentication, app registration, or connection strategy for SharePoint automation tooling.
- Author or review provisioning-oriented automation, tenant scripts, or idempotent operational routines.
- Troubleshoot or design command-level workflows using PnP cmdlets, `m365 spo` commands, or PnPjs calls.
- Combine PnP tooling with SPFx or native SharePoint APIs while keeping the automation-versus-runtime boundary clear.

## Not for this skill

- Classic WSP, Feature Framework, event receiver, or master-page work (handoff to `martix-sharepoint-server`).
- Pure SPFx component implementation where provisioning and automation are not the focus (handoff to `martix-sharepoint-spfx`).
- Generic PowerShell or JavaScript advice that is not tied to SharePoint PnP tooling decisions.

## Start with the closest workstream

1. Pick the closest workstream below.
2. Read only the linked rules needed for the current change.
3. Pull reference maps in only after the core workstream is chosen.
4. Open [AGENTS.md](./AGENTS.md) for cross-workstream review routes, package inventory, and maintainer guidance.

## Rule library by workstream

### Tool selection and boundaries

- Use for first-pass routing between PnP PowerShell, CLI for Microsoft 365, PnPjs, and the adjacent SPFx or server-side packages.
- Rules:
  - [SharePoint PnP foundation — tool selection and package boundaries](./rules/tool-selection-and-boundaries.md)
- Map: [Tool selection map](./references/tool-selection-map.md)

### Authentication and connections

- Use for app registration, permissions, connection flow, and environment-specific auth decisions.
- Rules:
  - [SharePoint PnP auth — app registration, permissions, and connection flow](./rules/auth-app-registration-and-connections.md)
- Map: [Authentication and connection map](./references/auth-connection-map.md)

### Automation patterns

- Use for PowerShell and CLI automation shapes, repeatable operational routines, and scripting safety.
- Rules:
  - [SharePoint PnP automation — PnP PowerShell patterns and safety](./rules/pnppowershell-automation-patterns.md)
  - [SharePoint PnP automation — CLI for Microsoft 365 and tenant operations](./rules/cli-m365-and-tenant-automation.md)
- Map: [Automation recipes](./references/automation-recipes.md)

### Provisioning and composition

- Use for provisioning engines, site scripts, site designs, and PnPjs composition inside broader SharePoint delivery flows.
- Rules:
  - [SharePoint PnP composition — PnPjs, site scripts, and provisioning workflows](./rules/pnpjs-and-provisioning-composition.md)
- Map: [Provisioning composition map](./references/provisioning-composition-map.md)

### Operations and integration

- Use for idempotency, governance, rollback awareness, and SPFx handoff boundaries in PnP-heavy workflows.
- Rules:
  - [SharePoint PnP operations — idempotency, governance, and SPFx integration boundaries](./rules/governance-idempotency-and-spfx-integration.md)
- Maps:
  - [Provisioning composition map](./references/provisioning-composition-map.md)
  - [Anti-patterns quick reference](./references/anti-patterns-quick-reference.md)

## Package conventions

- Every rule follows the shared section contract in [rules/_sections.md](./rules/_sections.md): `Purpose`, `Default guidance`, `Avoid`, `Review checklist`, `Related files`, and `Source anchors`.
- Use [the rule template](./templates/rule-template.md) for new rules, [the research pack template](./templates/research-pack-template.md) for scoped source inventories, and [the comparison matrix template](./templates/comparison-matrix-template.md) for external comparisons.
- Use [metadata.json](./metadata.json) as the registration-ready inventory for entrypoints, workstream coverage, and distribution notes.
- The taxonomy and preferred ordering live in [assets/taxonomy.json](./assets/taxonomy.json) and [assets/section-order.json](./assets/section-order.json).

## Standalone-first note

- This skill is authored as a standalone package under `skills`.
- If you document or install the package directly, use `npx skills add <source>` rather than `npx skill add`.
- Keep this package focused on its named SharePoint lane. Cross-link to sibling SharePoint packages instead of diluting the boundaries.
