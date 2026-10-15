---
name: taruvi-app-developer
description: >
  Use this skill when the user wants to build, add features to, debug, or
  deploy a web application that uses Taruvi as its backend — including CRUD
  pages, dashboards, file uploads, serverless functions, auth, or access
  control. Activate on any app-building request when the project contains
  @taruvi/sdk, @taruvi/refine-providers, TARUVI_API_KEY, sdk_client, or
  taruvi.cloud in its files. Also activate when the user mentions Taruvi,
  Refine providers, dataProvider, storageDataProvider, appDataProvider,
  userDataProvider, or sdk_client. Always read this skill first before
  loading any other Taruvi skill.
metadata:
  author: taruvi-ai
  version: "1.0.0"
---

## Overview

Entry-point orchestrator for all Taruvi app development. This skill detects the project context, decides whether a serverless function is needed, and routes to the right module skill before any code is written.

Default delivery standard: **always build a production-ready, production-scale app.** Not a demo, not an MVP, not a prototype. Every feature must be wired to real backend data, use proper error handling, and be built to handle real-world usage. The user must explicitly ask for a reduced scope if they want anything less.

## ⚠️ Skill Compliance — Non-Negotiable

**These skills are the single source of truth for all Taruvi implementation decisions.** They override existing project code, template patterns, training data, and personal shortcuts.

Rules:

1. **If a skill prescribes a specific way to implement something, use that way. No exceptions, no shortcuts, no "simpler" alternatives.**
2. **Do not copy patterns from existing project code if they contradict the skills.** Existing code may be outdated, a prototype, or pre-skill. The skills define the correct pattern.
3. **Do not skip steps to save time.** Every step in the skill instructions exists because skipping it causes real bugs or drift.
4. **If you cannot implement a skill requirement** (missing credentials, missing MCP tool, unclear API), **stop and ask the user** instead of silently falling back to an easier approach.
5. **After implementation, verify against the skill's checklist.** If any checklist item fails, fix it before presenting the work as done.

Common violations to avoid:
- Using `useList` with `aggregate`/`groupBy` for dashboard elements that need data from 2+ tables (use analytics queries instead)
- Omitting search bar and filter controls on list pages
- Using static `Select` instead of debounced `Autocomplete` for backend-loaded options
- Skipping `accessControlProvider` wiring without asking the user
- Hardcoding demo data instead of wiring real backend queries

## When to Use This Skill

- Starting a new Taruvi-powered app from scratch
- Adding a feature to an existing Taruvi app
- Refactoring or enhancing provider/hook/function code
- Debugging a broken query, upload flow, or function
- Deploying a frontend worker
- Any task that involves `@taruvi/sdk`, `@taruvi/refine-providers`, or `sdk_client`

## Step-by-Step Instructions

### Step 1 — Detect Project Mode

Identify which mode applies before doing anything:

| Mode | Signals |
|---|---|
| **Greenfield** | No existing Taruvi code, scaffolding from scratch |
| **Existing app** | Project has `@taruvi/sdk`, `.env` with `TARUVI_*` keys, or existing provider/function code |

For existing apps — read the relevant existing files first. Understand what is already built before proposing changes.

### Step 2 — Read Foundation Reference

Open and read `references/runtime-and-packages.md` before writing any code.

For deploy tasks, ask the user for their deploy target and workflow details.

### Step 2.5 — Identify the Current Package API

Before writing code against Taruvi packages, identify the current non-deprecated API surface in the installed package for this repo.

- Never introduce new usage of deprecated package APIs.
- If old examples, README snippets, or existing code use deprecated providers or hooks, do not copy them into new work.
- If the canonical path is unclear, resolve that before building the feature.
- If the only apparent working path is deprecated, treat that as a provider/docs issue to fix before finalizing the app code.

### Step 2.6 — Set Production-Ready Acceptance Baseline

Unless explicitly scoped down by the user, treat app tasks as production-ready deliverables:

- no hardcoded demo-only arrays for core workflows
- real backend wiring for CRUD/list/detail flows
- backend-driven pagination/sort/filter for list pages
- list-page UX includes visible search and relevant filter controls
- dashboards show live data from real backend queries, automatically calculated from the system's data and kept up to date — never hardcoded or demo values
- error and success paths are surfaced through the app notification provider
- required empty/loading/error states are present for key screens

### Step 3 — Decide: Function or Provider?

Answer this question before routing:

**Does this task touch more than one resource?**
(resources = database tables, storage buckets, users, secrets, analytics)

- **Yes** → a serverless function is required
- **No** → use provider hooks directly

Functions are required when the task involves:
- 2+ resources (multi-resource create/update/delete/mix)
- Backend logic beyond simple CRUD
- Reacting to data or user lifecycle events
- Scheduled / cron background jobs
- Calling external APIs using stored secrets
- Long-running tasks (>30s)
- Public unauthenticated endpoints
- Authorization-gated operations
- Function-to-function pipelines

For everything else — use provider hooks directly, no function needed.

### Step 4 — Route to the Right Module

**You MUST open and read the `SKILL.md` for every relevant module before writing any code.** Do not proceed to implementation until all applicable skills are loaded. Use your file search tool to locate each one.

| If the task involves… | You MUST load |
|---|---|
| Any frontend page, hook, or provider code | `taruvi-refine-providers` |
| List pages, detail views, filtered tables | `taruvi-database` |
| Dashboards, KPI cards, charts, summaries | `taruvi-database` |
| File upload, download, storage, attachments | `taruvi-storage` |
| Multi-resource operations, backend logic, events, cron | `taruvi-functions` |

**Most app-building tasks require 2+ skills.** For example:
- "Build an employee list page" → `taruvi-refine-providers` + `taruvi-database`
- "Add file upload to onboarding" → `taruvi-refine-providers` + `taruvi-storage` + `taruvi-functions` (multi-resource)
- "Build a dashboard" → `taruvi-refine-providers` + `taruvi-database`
- "Build a full CRUD feature" → `taruvi-refine-providers` + `taruvi-database` (+ `taruvi-storage` if files, + `taruvi-functions` if multi-resource)

Find and read the `SKILL.md` for each required skill. Do not hardcode a path — use your file search tool to locate it.

### Step 5 — Choose Dashboard Query Strategy

If the task includes a dashboard, KPI cards, charts, or summary metrics:

- **Single-table aggregates** → use datatable provider with `useList` + `meta.aggregate`/`groupBy`. This is the default for most dashboards.
- **Multi-table visualizations** → use saved analytics queries via `appDataProvider` + `useCustom` with `meta.kind: "analytics"`. This is required when a dashboard element (card, chart, metric, or any visual) needs to combine data from 2+ tables to render.
- **Row query + derive in React** is never allowed for summary metrics. Always push aggregation to the server.

**Before writing any dashboard query, check:** does this metric/chart need data from more than one table? For example, "revenue by department" needs orders + departments — that's 2 tables, so use analytics. "Orders by status" only needs the orders table — use datatable aggregate.

### Step 6 — Default List Views to Backend-Driven Queries

For any backend-backed list or table page, the default implementation must be backend-driven:

- backend pagination is required by default
- default list `pageSize` is `10`; recommend exposing `10`, `20`, `50`, and `100` as user-selectable options
- search, filters, and sorting must be server-side by default
- provide visible list controls for search and common filters by default (for example: status, department, date range, active/inactive)
- when the list is rendered with MUI `DataGrid`, default to Refine `useDataGrid`
- client-side filtering or search is only allowed if the user explicitly asks for it or the list is intentionally local-only
- do not fetch one page of backend rows and then apply the primary list filtering logic in React
- if a backend-backed MUI `DataGrid` list is not using `useDataGrid`, document the reason explicitly
- if the current schema or query path cannot support the needed server-side list behavior, fix the backend/query path before calling the feature done
- if search/filter controls are omitted, document the explicit user instruction or concrete reason

### Step 7 — Default Network-Backed Dropdowns to Autocomplete

For any dropdown whose options come from network calls:

- use `Autocomplete` (or equivalent typeahead), not a static `Select`
- query options from the backend with pagination (default option `pageSize` `10`)
- debounce input before sending search requests
- send the current search term as server-side filters, not client-side filtering over previously fetched options
- if the field cannot support server-side search + pagination, treat that as a query/schema gap and fix it before calling the feature done

### Step 8 — Enforce Access-Control Contract

For permission checks in app code:

- use only the published non-deprecated SDK/provider contract with prefixed ACL resource strings
- `useCan`/`CanAccess` resources must be in prefixed form (for example `datatable:employees`, `function:employee-terminate`, `query:hrms-dashboard-summary`)
- do not rely on `params.entityType` for access-control checks
- verify runtime payloads in browser network logs: each `check/resources` `resource.kind` must exactly match the requested `resource` string
- when SDK/provider ACL contract changes, app code must be updated in the same release cycle and versioned accordingly

### Step 9 — Default Bulk Actions to Backend Bulk Operations

For bulk update/delete/status-change flows:

- execute bulk changes through backend bulk operations by default (`updateMany`, `deleteMany`, or a batch serverless function)
- define and show selection scope clearly (selected rows vs filtered result set)
- return and display partial-failure details per record when applicable
- invalidate/refetch affected list and related summary queries after completion

### Step 10 — Use Refine Notification Provider

For user-facing success/error feedback:

- use the app's existing Refine notification integration (`notificationProvider`) by default
- do not introduce custom toast/snackbar systems when Refine notification provider is available

## Examples

**Greenfield:** User says "build me an employee directory". Read references, wire `dataProvider` and `userDataProvider`, scaffold list/detail pages with Refine hooks. No function needed (single-resource CRUD).

**Existing app refactor:** User says "the cascade delete is broken". Read existing delete handler first, detect multi-resource pattern (tasks + attachments + activities), route to `taruvi-functions/SKILL.md` and rewrite as a serverless function.

**Deploy task:** User says "deploy the frontend". Ask for their deploy target and follow their project's build and deploy workflow.

**List + feedback baseline:** For backend-backed list pages, use `useDataGrid` (`pageSize: 10`) and surface success/error via Refine `notificationProvider` (`useNotification`) rather than custom toasts.
Include visible search and filter controls unless the user explicitly asks for a minimal list.

## Rules (always apply)

- **Dashboards** — single-table metrics use datatable `aggregate`/`groupBy`. When a dashboard element needs data from 2+ tables, use saved analytics queries. Never fetch full row sets into React to derive summary metrics.
- **Functions** — use a serverless function whenever there is any cross-resource side effect, even if it seems minor.
- **Lists** — backend pagination, server-side search/filter/sort, visible search + filter controls, `useDataGrid` for MUI DataGrid. No exceptions unless the user explicitly asks.
- **Dropdowns** — debounced server-side `Autocomplete` with pagination. No static `Select` with one-shot loads.
- **Deprecated providers** — flag `functionsDataProvider`/`analyticsDataProvider` as deprecated; migrate to `appDataProvider + useCustom`.
- **Package API** — use the installed package's current non-deprecated API surface. Do not copy deprecated patterns from existing code.
- **Multi-module tasks** — load all relevant SKILL.md files before starting; don't guess from memory.
- **Unclear project mode** — ask the user: "Is this a new app or does it already have Taruvi providers set up?"

## References

- `references/runtime-and-packages.md` — mandatory runtime split, package list, query strategy
