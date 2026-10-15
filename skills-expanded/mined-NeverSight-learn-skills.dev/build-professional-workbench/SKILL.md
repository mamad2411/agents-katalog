---
name: build-professional-workbench
description: Build, redesign, extend, or audit a complete role-based professional workbench, operations cockpit, case portal, expert workstation, or data-rich internal tool for any occupation. Use for 工作台、业务驾驶舱、职业后台、运营中心、role dashboard、admin portal、CRM-like workspace or reusable multi-page web apps, especially when every module needs realistic records, distinct dashboards, profession-specific information architecture, Quiet Luxury A visual design, complex interactions, automatic local persistence, offline pure-Web compatibility and verifiable workflows.
---

# 超快速的多职业工作台构建 Skill

Build a role-centered operational product, not a renamed dashboard shell. Preserve an existing architecture when present. For a new pure-Web build, start from `assets/reference-workbench-template/`, then replace its education reference domain completely.

## Start

1. Classify the request as new build, extension, redesign or audit.
2. Infer the profession, organization, role, users, work objects, lifecycle, decisions, risks, approvals, privacy boundary and deployment mode. Ask only when a missing choice materially changes the product.
3. Read only the needed references:
   - Always read [deployment-modes.md](references/deployment-modes.md) for a new build.
   - Read [workbench-architecture.md](references/workbench-architecture.md) for shell, module and page contracts.
   - Read [profession-profiles.md](references/profession-profiles.md) to select or combine domain patterns.
   - Read [dashboard-catalog.md](references/dashboard-catalog.md) for KPIs, charts and analytical pages.
   - Read [design-interaction.md](references/design-interaction.md) for visual, motion, canvas, navigation or responsive work.
   - Read [local-persistence.md](references/local-persistence.md) whenever users can create, edit, delete, arrange, annotate, import or attach data.
   - Read [data-and-validation.md](references/data-and-validation.md) before record generation and final acceptance.
4. For a new offline project, run:

```bash
python3 scripts/scaffold_professional_workbench.py <target> --profile <profile> --profession "..." --organization-name "..." --role-name "..." --user-name "..." --deployment-mode local-offline
```

5. Treat scaffolding as a starting point. Do not deliver until every route, record, workflow, chart, control, persistence path and domain-remnant check passes.

## Model the profession

- Define the role's primary nouns: cases, clients, patients, projects, candidates, accounts, content, assets, experiments, orders, incidents or equivalent objects.
- Define lifecycle states, owners, handoffs, deadlines, decisions, exception conditions, evidence and approvals.
- Separate personal work, team operations, shared resources, analytics and administration/compliance.
- Keep organization, role, period, territory, team or portfolio context visible.
- Use explicit Chinese text labels in navigation; icons only reinforce meaning.
- Select one profile from [profession-profiles.md](references/profession-profiles.md), or combine profiles for hybrid roles. Retain only responsibilities supported by the real role.

## Build complete pages

- Give every navigation item a complete page with title, context, actions, dense records, statuses and one distinct analytical dashboard.
- Avoid placeholders, three-row tables, repeated renamed cards, decorative charts and unsupported buttons.
- Use deterministic, coherent demonstration records and label them as simulated data.
- Include appropriate normal, empty, loading, warning, error, disabled, overdue, conflict, approval and confirmation states.
- Make record-heavy pages searchable, filterable, sortable and bounded by pagination or controlled scrolling.
- Make primary records directly editable. Create, update and delete must feed the same source used by table, details, export and dashboards.
- Make date, range, filter and segment controls operate on real records. Visual-only controls are defects.
- Export current filtered records with stable headers. Validate imports for format, row shape, limits and merge/replace intent; preview first and keep current data unchanged on failure.
- Trace the main work object across list, detail, workflow and dashboard pages.

## Assign distinct dashboards

- Give every page a different business question, KPI set, chart combination, diagnostic, interaction and color variant.
- Use trends for time, bars for categories, heatmaps for density, Sankey for flow, networks for relationships, radar or parallel coordinates for profiles, Gantt for schedules and histograms or boxplots for distributions.
- Compose each dashboard from one dominant chart, 3–4 KPIs, a secondary diagnostic, a ranked or segmented view, range controls, tooltips and a concise interpretation.
- Bind charts to the same visible records and provide accessible text summaries.
- Treat financial, medical, legal, safety and compliance output as decision support, never autonomous professional judgment.

## Apply Quiet Luxury A

- Use the bundled `css/premium-minimal.css` as the final cascade layer unless the user selects another visual direction.
- Keep a warm ivory field, ink-green typography, desaturated sage accents, serif display titles, system sans-serif controls, fine rules and generous whitespace.
- Prefer editorial hierarchy and alignment over nested rounded cards and heavy shadows.
- Keep the shell calm and text-labeled. Use light analytical dashboards; reserve dark graphite for the spatial hero or infinite canvas.
- Keep heatmaps dense but quiet, with five square-cell levels.
- Use hover inspection, focus, selection, drill-down, detail drawers, modals, pan/zoom and progressive disclosure where they clarify state.
- Keep motion short, interruptible and disabled under `prefers-reduced-motion`.
- Preserve keyboard access, visible focus, semantic controls, touch layouts and print/report views.
- Adapt `--workbench-folio`, context selectors and hero language to the new organization and profession.
- The reference hero image is embedded as text in `js/hero-media.js` so the Skill remains Red Skill compatible and the generated site remains fully offline.

## Require local-first persistence

- Save create, edit, delete, reorder, annotation, draft, preference and layout changes automatically to the current computer after validation.
- Restore saved state before the first meaningful render. A save toast without a successful write is a defect.
- Use bundled `js/local-persistence.js` for small JSON records and drafts. Use IndexedDB for attachments, large collections and offline queues.
- Namespace each workbench, version stored records and add migrations when schemas change.
- Show saving, saved, failure and quota states. Never silently discard a failed write.
- Provide versioned JSON export, validated atomic import with merge/replace semantics, attachment management and confirmed clearing. Roll back any partially applied import.
- Keep demo seeds separate from personal records. Do not store secrets or claim browser storage is encrypted.
- For `local-offline`, disclose single-device and single-browser limits. For `team-server` or `enterprise`, use authenticated APIs and a server database as the system of record; see [deployment-modes.md](references/deployment-modes.md).

## Use the bundled implementation

The reference template provides pure HTML/CSS/JavaScript with no CDN, multi-area text navigation, 56 module entries, dense records, Quiet Luxury A, a spatial hero, infinite canvas, activity heatmap, custom cursor, route motion, 22 chart families, editable tables, namespaced localStorage, autosave, versioned backup/import, dialogs, forms, responsive behavior and print styles.

Replace all reference-domain names, navigation, records, workflows, KPIs, simulated identities and hero wording. Never ship a non-education workbench by changing only its title.

## Validate

1. Run `python3 scripts/validate_redskill_package.py .` when preparing this Skill for Red Skill upload.
2. Run `python3 scripts/validate_professional_workbench.py <project-path>` for the generated workbench.
3. Run native syntax or build checks.
4. Verify every navigation entry resolves to a complete page and receives a distinct dashboard.
5. Verify record density, cross-page coherence, operational filters, forms, details, workflow states and keyboard access.
6. Verify local assets and `file://` behavior for offline delivery.
7. Verify add → reload, edit → reload, delete → reload, export → clear → import, malformed import rejection and storage-failure reporting.
8. Run `node scripts/test_local_persistence.js <project-path>` when Node.js is available.
9. For non-education profiles, require zero education-domain remnants.
10. Perform visual and interaction QA when a browser surface is available; never equate file existence or syntax success with visual acceptance.
11. Report path, deployment mode, profession, role, module and dashboard coverage, CRUD/filter/import/export results, persistence results, validation and remaining boundaries.

## Guardrails

- Do not infer authority for external writes, approvals, messages, transactions or publication.
- Do not present simulated records as real data or expose sensitive identifiers.
- Do not automate high-stakes decisions without professional review.
- Do not use external CDNs for offline deliverables.
- Keep `production_ready` false until the selected deployment mode's architecture, security and acceptance gates pass.
- Do not publish or deploy unless the user requests it or active site-building instructions require hosting.
