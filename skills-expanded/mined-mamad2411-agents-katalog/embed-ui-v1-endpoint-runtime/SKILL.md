---
name: embed-ui-v1-endpoint-runtime
description: Use when building, editing, or reviewing RetailCRM JS module endpoint wiring with @retailcrm/embed-ui-v1-endpoint. Covers pages, widgets, runners, targets, menu hierarchy, page publishing payloads, and public Host API boundaries.
---

# Embed UI v1 Endpoint Runtime

Use this skill before changing JS module endpoint wiring, page registration, widget targets, or Host API navigation.

## Reading order

1. Read project `AGENTS.md` if it exists.
2. Read `./node_modules/@retailcrm/embed-ui-v1-endpoint/README.md`.
3. Read `./node_modules/@retailcrm/embed-ui-v1-endpoint/docs/README.md`.
4. Read the relevant endpoint docs:
   - `docs/define-runner.md`
   - `docs/define-page-runner.md`
   - `docs/define-widget-runner.md`
   - `docs/page-routes.md`
   - `docs/menu-placements.md`
   - `docs/targets.md`
5. If MCP resources are available, read `embed-ui-v1-endpoint://targets` and then the target profile for the target being changed.
6. If MCP is not available, use `./node_modules/@retailcrm/embed-ui-v1-endpoint/docs/targets/*.yml` as fallback.

## Workflow

1. Identify whether the task is a page, widget, or shared endpoint runner change.
2. For pages, keep the runtime runner map and extension config page descriptors aligned by page `code`.
3. For widgets, choose the exact target from endpoint docs or MCP resources before writing UI.
4. Use documented public entrypoints such as `@retailcrm/embed-ui-v1-endpoint/remote`; do not import from `dist/*`, source files, or repository-only paths.
5. Keep widget inline UI compact; use component package widget composition guidance for UI mounted into CRM targets.
6. After the first page vertical slice, verify it in the CRM host: menu item, `/modules/<moduleCode>/<pageCode>` route, entrypoint URL, stylesheet URL, and actual frontend mount.
7. Keep page switch/root components thin; move shared locale synchronization and context plumbing into composables or plugins when several embed pages need them.
8. Prefer domain-specific frontend API helpers over one generic page-level `callAdminApi`; preserve status, field errors, and error codes in structured error objects.
9. If a runtime error appears only in a minified bundle, switch to a dev bundle or sourcemaps before guessing.

## Page and menu checks

- Published page descriptors must be objects, not string page codes.
- Page descriptors need `code`, `menu`, and usually `menuItemTitle`.
- Before choosing RetailCRM system `menu` or `parentMenuItemCode`, read `https://docs.retailcrm.ru/api/ru/RetailCRM/jsApiMethods/navigation`; do not guess menu codes from section names or stale examples.
- Use `parentMenuItemCode` and `menuItemOrdering` to model the intended CRM page/menu hierarchy.
- Breadcrumb-like navigation is derived by CRM from the page/menu hierarchy passed in the extension config; do not hand-roll breadcrumbs in the page unless the product task explicitly asks for local in-page navigation.
- For updating an already installed module, use the existing integration module edit/update flow and put pages under `integrationModule.integrations.embedJs.pages`.
- Build/lint success does not prove page rendering; check the installed module in the CRM host when page routing or menu placement changed.

## Host API checks

- Use public Host API for location, query state, and navigation.
- Do not depend on internal endpoint runtime stores or private channel state.
- Keep route names, page codes, and extension descriptor values documented in the project.

## Shared page setup checks

- If i18n is used by several embed pages, synchronize remote locale once through a shared composable or plugin.
- Do not duplicate the same locale watch/load code in every page component.
- Domain helpers such as `loadSettings`, `saveSettings`, `loadSpecialties`, `saveSpecialist`, and `deleteSpecialist` should express page contracts better than generic transport calls.
- If the API returns machine-readable error codes, translate them in the frontend UI layer; backend messages may be fallbacks or explicit product requirements, not the only structured contract.
