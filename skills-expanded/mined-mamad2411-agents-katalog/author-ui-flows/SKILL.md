---
name: author-ui-flows
description: Analyzes site personas or roles together with business-domain.md to determine the pages, routes, and navigation required to meet the business objectives of the site. Use when documentTypes and search criteria have been established and the remaining task is defining the UI pages that make up the site.
intent: >-
  Author UI flow plans after domain modeling is complete. This workflow turns personas, roles, and the business-domain.md into implementation-ready page inventories, route flows, and menu/navigation structures that can be encoded in site-endpoint-config.json.
type: workflow
best_for:
  - "Defining UI pages after documentTypes and search criteria are already established"
  - "Translating business-domain.md into role-based page flows"
  - "Designing site-endpoint-config.json pages and menu structures"
  - "Determining required routes, navigation transitions, and role-specific entry points"
  - "Creating ui-flows.md planning artifacts before site configuration work"
scenarios:
  - "The business objects are done and we need to define the pages"
  - "Determine the customer and picker flows from the business domain"
  - "What pages and nav items are required for each role to fulfill the product goals?"
  - "Draft the UI flow plan before implementing site-endpoint-config.json"
---

# Author UI Flows

Translate a finished business-domain model into role-based page flows and navigation before UI configuration starts.

## What This Skill Does

1. Reads the business domain and identifies the site personas or roles.
2. Determines the critical business objectives each role must accomplish.
3. Derives the pages, routes, and transitions required to achieve those objectives.
4. Maps pages to repo-aligned render types and route patterns.
5. Produces a navigation model suitable for `site-endpoint-config.json` and a planning artifact such as `ui-flows.md`.

## Preconditions

Use this skill only after:
- documentTypes are established
- search criteria and search projections are established
- core business-domain planning is available

This skill is not for initial domain modeling. It assumes the underlying business objects already exist.

## Required Inputs

- personas or roles of the site
- `business-domain.md`
- any existing site constraints already decided for the repo

Optional supporting context:
- existing `site-endpoint-config.json`
- current menu structure
- existing page inventory
- role-specific value proposition notes

## Repo-Specific Rules

### Page Type Rule

Prefer existing repo page render types rather than inventing new UI abstractions.

Typical page mappings:
- `dynamicListing` for queues, history, catalogs, and worklists
- `dynamicView` for detail pages and read-only drill-down pages
- `dynamicForm` for creation, claim, edit, checkout, confirmation, and remediation actions
- `dynamicSearch` for explicit search entry pages
- `staticContent` for dashboards, landing pages, and low-state informational pages

### Role Flow Rule

Each role must have a coherent task path from entry point to business outcome.

For every role, identify:
- entry page
- primary task pages
- secondary or exception paths
- success state or terminal page

Do not create pages that do not correspond to a real business objective, state transition, or navigation need.

### Navigation Rule

Top-level menu items should reflect stable role objectives, not every individual screen.

Prefer menus for:
- dashboards
- work queues
- search entry points
- active workload lists
- history or reporting views
- operational admin areas

Avoid exposing implementation-only pages directly in the menu if they are only reachable through workflow transitions. Avoid creating alternative navigation or activity usage patterns such as a list of 'action' buttons on a page except where it is needed for a specific business reason. Use role-specific menu entries where the primary user of a page or flow is limited to a specific role, but avoid creating separate menu entries for pages that are shared across roles unless it is needed for clarity or access control.

### Search Rule

If a role needs a navbar or entry-point search experience, tie it to an explicit `dynamicSearch` resource and corresponding menu/navigation definition.

Do not treat free-form search UI as separate from the search projection already defined in domain modeling.

### Endpoint Config Rule

When translating UI flows into config, define:
- `resource`
- `renderType`
- `renderOptions`
- `methods.GET.route`
- `methods.POST.route` where applicable
- `nav.prev`, `nav.next`, `nav.success`, or similar transitions
- menu entries aligned to role access

Note: When authoring `site-endpoint-config.json` fragments for services, place service endpoint fragments as `endpoint-config.json` directly inside the service folder: `sites/<site>/config/<service>/endpoint-config.json`. The launcher expects the fragment at the service folder level and will not find fragments nested under an additional `endpoint-config/` subdirectory.

## Page UX Rule
Design pages to support the business task with the appropriate render type, but do not over-index on UX details such as wireframes, mockups, or specific UI elements. Ensure 100% coverage of the business objectives defined in `business-domain.md` with at least one complete UI flow to create, one UI flow to update, and one UI flow to delete. Do not attempt to determine critical versus non-critical flows or to reduce the effort required to implement as they have been defined in the business domain, but do ensure that every objective has a clear path to completion through the UI. Ensure each UI flow has an equivalent playwright smoke test that can be implemented in the same repo commit as the site-endpoint-config.json changes.

## Workflow

### Step 1: Identify Roles and Objectives

From the business domain, list each site persona or role and the business outcomes they must achieve.

Examples:
- discover catalog inventory
- register or sign in
- create or manage subscriptions
- search and claim work
- fulfill shipments
- review or remediate exceptions

### Step 2: Break Objectives into Flow Steps

For each role, convert each objective into a sequence of user-visible steps until completion. Ensure 100% coverage of the business objectives with at least one create flow, one update flow, and one delete flow. Steps should be granular enough to determine page boundaries but do not need to include every minor interaction or UI element.

Capture:
- required entry point
- intermediate pages
- branching decisions
- completion page or next state

Treat each step as a candidate page only if the step needs a dedicated screen, route, or form.

### Step 3: Determine Page Inventory

Create the minimal page set needed to support the flows.

For each page, define:
- role owner
- business purpose
- render type
- likely resource name
- route shape
- upstream and downstream navigation

### Step 4: Determine Navigation Surfaces

Define which pages belong in:
- top navigation (should be stable, role-aligned entry points that cover 95% of the role's objectives)
- dropdown groups
- contextual next/prev transitions
- workflow success redirects

Separate always-available navigation from workflow-only transitions.

### Step 5: Validate Coverage Against Business Objectives

Check that every critical business objective from `business-domain.md` is reachable through at least one complete UI path.

Look for gaps such as:
- no entry point for a required task
- no detail page for an operational listing
- no form page for a required state change
- no success route after a required business action

### Step 6: Produce Artifacts

Produce one or more of:
- `ui-flows.md`
- role-by-role page inventory
- route list
- menu definition outline by unauthenticated versus authenticated, and by role
- `site-endpoint-config.json` page and menu draft

## Output Template

### A) Roles and business objectives
- role:
- primary objectives:
- supporting objectives:

### B) Flow inventory
- flow name:
- actor:
- start page:
- steps:
- end state:

### C) Page inventory
- resource:
- renderType:
- purpose:
- route:
- acl:

### D) Navigation model
- top-level menu groups:
- dropdown items:
- workflow transitions:
- role-specific search entry points:

### E) Config implementation notes
- pages to add:
- menu items to add:
- routes to reserve:
- pages that should stay workflow-only:

## Anti-Patterns

- Designing pages before the domain model exists.
- Creating one menu item per page instead of per durable role objective.
- Treating modal steps or inline actions as standalone pages without need.
- Adding dashboards that do not support a real business task.
- Creating search pages without tying them to an established search projection.
- Mixing admin exception flows into primary user navigation without clear reason.
- Exposing implementation-only edit or remediation pages directly in the menu.

## References

- `sites/*/domain/business-domain.md`
- `sites/*/domain/ui-flows.md`
- `shared-lib/schema/site-config-schema.json`
- `shared-lib/schema/page-schema.json`
- existing `site-endpoint-config.json` files in the repo