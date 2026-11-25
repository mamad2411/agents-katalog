---
name: martix-sharepoint-server
description: >-
  SharePoint Server classic on-prem guidance for farm solutions, WSPs,
  Feature Framework, feature receivers, event receivers, site definitions,
  delegate controls, application pages, master pages, page layouts, Design
  Manager, and classic provisioning targeting SharePoint 2019 and
  Subscription Edition, with SharePoint 2010 and 2013 legacy context. Use
  this skill when the task mentions WSPs, farm solutions, feature XML or
  receivers, site or list definitions, delegate controls, application pages,
  master pages, page layouts, composed looks, or classic on-prem
  modernization; route SPFx web parts or extensions to
  `martix-sharepoint-spfx` and PnP automation or provisioning tooling to
  `martix-sharepoint-pnp`.
license: Complete terms in LICENSE.txt
---

## MartiX SharePoint server router

- Standalone-first skill package focused on classic and on-prem SharePoint
  server-side work.
- Keep platform target, WSP packaging, feature wiring, extensibility,
  branding, and provisioning aligned instead of treating them as unrelated
  cleanup passes.
- Use [AGENTS.md](./AGENTS.md) when the scenario crosses multiple workstreams
  or needs the longer review routes, package inventory, or maintainer cues.

## When to use this skill

- Author or review farm solutions, WSP packages, feature XML, feature
  receivers, or feature-based deployments.
- Design event receivers, list event receivers, remote event receivers,
  supporting timer jobs, or related classic extensibility points.
- Work with site definitions, list definitions, modules, delegate controls,
  application pages, or classic provisioning artifacts.
- Maintain or modernize master pages, page layouts, Design Manager assets,
  themes, or composed looks.
- Target SharePoint 2019 or Subscription Edition while using SharePoint 2010
  and 2013 guidance as legacy context.

## Route these requests to companion skills

- Use [`martix-sharepoint-spfx`](../martix-sharepoint-spfx/SKILL.md) for SPFx,
  React, TypeScript, web parts, extensions, Form Customizers, or SharePoint
  Online client-side customization.
- Use [`martix-sharepoint-pnp`](../martix-sharepoint-pnp/SKILL.md) for PnP
  PowerShell, CLI for Microsoft 365, PnPjs, tenant automation, site scripts,
  or provisioning tooling decisions that are not anchored in classic
  server-side artifacts.

## Quick default choices

| Concern | Default | Escalate when |
| --- | --- | --- |
| Platform target | SharePoint 2019 or Subscription Edition first | The task is explicitly a SharePoint 2010 or 2013 migration or compatibility review |
| Packaging | WSP with explicit feature ownership and activation order | The requirement is actually cloud-first or belongs in SPFx or PnP guidance |
| Extensibility | Choose the lightest receiver, remote receiver, or job model that matches the hosting boundary | Operations, retries, diagnostics, or future modernization risk are still unclear |
| Branding | Keep master pages, page layouts, themes, and Design Manager tied to classic publishing needs | The requested experience does not truly depend on classic publishing-era surfaces |
| Modernization | Preserve current on-prem delivery needs first, then name future migration seams | The user is asking for an actual redesign or cross-surface migration plan |

## Start with the closest workstream

1. Pick the closest workstream below.
2. Read only the linked rules needed for the current change.
3. Pull in reference maps after the core workstream is chosen.
4. Open [AGENTS.md](./AGENTS.md) when the scenario spans packaging,
   branding, extensibility, and modernization together.

## Rule library by workstream

### Foundation and boundaries

- Use for version targeting, deciding whether a task still belongs in classic
  server-side guidance, and separating on-prem artifacts from SPFx or
  PnP-first solutions.
- Rule:
  [SharePoint server foundation — platform boundaries and version targets](./rules/foundation-platform-and-boundaries.md)
- Map:
  [Platform and boundaries map](./references/platform-and-boundaries-map.md)

### Packaging and feature framework

- Use for WSP composition, feature layout, activation strategy, and packaging
  choices for classic artifacts.
- Rule:
  [SharePoint server packaging — WSPs, features, and upgrade shape](./rules/packaging-features-and-wsp.md)
- Map:
  [Packaging and extensibility map](./references/packaging-and-extensibility-map.md)

### Extensibility

- Use for event receivers, remote event receivers, timer jobs, and related
  classic extension points.
- Rule:
  [SharePoint server extensibility — event receivers, remote receivers, and jobs](./rules/extensibility-event-receivers-and-jobs.md)
- Map:
  [Packaging and extensibility map](./references/packaging-and-extensibility-map.md)

### Site artifacts and information architecture

- Use for site definitions, list definitions, modules, managed metadata,
  navigation, and publishing-era site composition.
- Rule:
  [SharePoint server site artifacts — definitions, modules, metadata, and navigation](./rules/site-artifacts-and-information-architecture.md)
- Map:
  [Site and branding map](./references/site-and-branding-map.md)

### Branding

- Use for master pages, page layouts, Design Manager assets, themes, and
  composed-look-era branding decisions.
- Rule:
  [SharePoint server branding — master pages, Design Manager, and themes](./rules/branding-master-pages-design-manager-and-themes.md)
- Map: [Site and branding map](./references/site-and-branding-map.md)

### Provisioning and modernization

- Use for classic site provisioning, publishing rollouts, and the
  modernization boundary when classic assets still exist.
- Rule:
  [SharePoint server provisioning — classic rollout, publishing, and modernization boundaries](./rules/provisioning-publishing-and-modernization.md)
- Map:
  [Provisioning and modernization map](./references/provisioning-modernization-map.md)

## Quick reference surfaces

- [Source index and guardrails](./references/doc-source-index.md)
- [Platform and boundaries map](./references/platform-and-boundaries-map.md)
- [Packaging and extensibility map](./references/packaging-and-extensibility-map.md)
- [Site and branding map](./references/site-and-branding-map.md)
- [Provisioning and modernization map](./references/provisioning-modernization-map.md)
- [Anti-patterns quick reference](./references/anti-patterns-quick-reference.md)
