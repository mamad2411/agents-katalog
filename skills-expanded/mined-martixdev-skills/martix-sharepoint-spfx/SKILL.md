---
name: martix-sharepoint-spfx
description: 'SharePoint Framework guidance for SharePoint Online client-side architecture, tooling, hosts, and modernization. Use when the task mentions SPFx, SharePoint Framework, SharePoint Online customizations, web parts, extensions, Form Customizer, library components, supportedHosts, Teams tabs, Viva Connections, ACE, Adaptive Card Extensions, MSGraphClientV3, AadHttpClient, PnPjs, Heft, gulp toolchain, skipFeatureDeployment, or modernizing Script Editor, JSLink, UserCustomAction, or ECB customizations. Do not use it for classic farm solutions, WSPs, Feature Framework, master pages, server-side object model code, or provisioning-only work.'
license: Complete terms in LICENSE.txt
---

## MartiX SharePoint Framework router

- Standalone-first skill package focused on SharePoint Online-first SPFx
  decisions for modern client-side customization.
- Keep host surface, SPFx version, toolchain, component choice, API clients,
  deployment, and migration guidance aligned instead of treating them as
  unrelated cleanup passes.
- Use [AGENTS.md](./AGENTS.md) when the scenario crosses multiple workstreams or
  needs the longer review routes, package inventory, or maintainer cues.

## When to use this skill

- Author, review, set up, or verify SPFx web parts, extensions, Form
  Customizers, library components, toolchains, scaffolds, or compatibility
  postures for SharePoint Online.
- Design property panes, `propertiesMetadata`, React structure, theme-aware UI,
  packaging, asset hosting, or rollout strategy.
- Integrate SPFx code with SharePoint REST, PnPjs, `MSGraphClientV3`, or
  `AadHttpClient`; expose web parts in Teams or wire Viva Connections and ACE.
- Translate Script Editor, Content Editor, JSLink, UserCustomAction, or ECB-era
  customizations into supported modern client-side surfaces.
- Review SharePoint 2019 or Subscription Edition compatibility notes.

## Not for this skill

- Classic farm solutions, WSP packages, Feature Framework receivers, master
  pages, page layouts, or other server-side SharePoint Server work better
  handled by `martix-sharepoint-server`.
- Pure provisioning, tenant automation, or operator-run workflows better
  handled by `martix-sharepoint-pnp`.
- Generic React or TypeScript advice that is not materially shaped by SPFx
  constraints.
- Broad SharePoint governance, compliance, or tenant administration questions
  with no client-side implementation angle.

## Quick default choices

| Concern | Default | Escalate when |
| --- | --- | --- |
| Page content or configurable page experience | SPFx web part | The request is really page chrome, list commands, or list form replacement |
| Page chrome, placeholders, command bars, or list cells | SPFx extension | The request is really page content or a form experience |
| List or library new, edit, or display forms | SPFx Form Customizer | The requirement spans more than list or library form lifecycle |
| Reuse across multiple SPFx solutions | Local package or shared workspace code first | A separately deployed library component is truly needed across solutions |
| Runtime SharePoint data access | `SPHttpClient` or carefully scoped PnPjs | The task is actually provisioning-only or requires Graph or external API auth |
| Graph or Entra-secured API access | `MSGraphClientV3` or `AadHttpClient` with explicit permissions | The task depends on server-side processing or non-SPFx auth flows |
| SharePoint Server 2019 or SE target | Treat 2019-era constraints as the conservative baseline | Local validation and current docs prove a narrower or broader support envelope |

## Start with the closest route

1. Pick the closest workstream below.
2. Add the paired reference map before widening the answer.
3. Pull in [assets/host-support-matrix.json](./assets/host-support-matrix.json)
   whenever host or version support is part of the decision.
4. Open [AGENTS.md](./AGENTS.md) when the scenario spans setup, component
   selection, deployment, and migration together.

## Rule library by workstream

### Foundation and support boundaries

Scope checks, host identity, classic exclusions, 2019 or Subscription Edition constraints.
Rule: [foundation-scope-and-support-boundaries](./rules/foundation-scope-and-support-boundaries.md)

### Versioning, compatibility, and scaffolding

Node, React, TypeScript, Heft vs. gulp, generator, serve, and debug setup.
Rules: [tooling-versioning-and-compatibility](./rules/tooling-versioning-and-compatibility.md) ·
[projects-toolchain-and-scaffolding](./rules/projects-toolchain-and-scaffolding.md)

### Web parts and property panes

Web parts, property pane shape, `propertiesMetadata`, page-hosted experiences.
Rule: [webparts-property-panes-and-properties](./rules/webparts-property-panes-and-properties.md)

### Extensions, forms, and reusable components

Application Customizers, Command Sets, Field Customizers, Form Customizers, library components.
Rules: [extensions-application-command-field](./rules/extensions-application-command-field.md) ·
[components-form-customizers-and-library-components](./rules/components-form-customizers-and-library-components.md)

### Data and API clients

`SPHttpClient`, PnPjs, Graph, `MSGraphClientV3`, `AadHttpClient`, permissions.
Rule: [data-sharepoint-graph-and-aad-clients](./rules/data-sharepoint-graph-and-aad-clients.md)

### Packaging, deployment, and tenant rollout

`package-solution.json`, app catalog, `skipFeatureDeployment`, asset hosting.
Rule: [deployment-packaging-and-tenant-rollout](./rules/deployment-packaging-and-tenant-rollout.md)

### Teams and Viva host integration

`supportedHosts`, Teams tabs, ACE, Viva Connections, messaging-extension boundaries.
Rule: [hosts-teams-and-viva-integration](./rules/hosts-teams-and-viva-integration.md)

### React, TypeScript, and theming

Fluent UI, theme tokens, CSS isolation, theme-variant support.
Rule: [ui-react-typescript-and-theming](./rules/ui-react-typescript-and-theming.md)

### Migration and modernization

Script Editor, Content Editor, JSLink, UserCustomAction, ECB modernization.
Rule: [migration-classic-to-modern-spfx](./rules/migration-classic-to-modern-spfx.md)

## Quick reference surfaces

- [Source index and guardrails](./references/doc-source-index.md)
- [Foundation and support map](./references/foundation-scope-support-map.md)
- [Version support map](./references/version-support-map.md)
- [Component selection map](./references/component-selection-map.md)
- [Data and integration map](./references/data-integration-map.md)
- [Teams and Viva map](./references/teams-viva-map.md)
- [Migration map](./references/migration-map.md)
- [Cookbook index](./references/cookbook-index.md)
