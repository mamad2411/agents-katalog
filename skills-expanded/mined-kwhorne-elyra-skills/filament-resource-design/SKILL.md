---
name: filament-resource-design
description: Build Filament admin panels that stay fast and maintainable - resource vs custom page decisions, table and form design, actions, authorization via policies, and query performance in tables. Use when creating or reviewing Filament resources, deciding how to structure an admin panel, adding actions or widgets, or when a Filament table is slow or an admin panel has grown chaotic.
license: MIT
compatibility: elyra >=0.1, claude-code
allowed-tools: read, bash, grep, edit, write
metadata:
  author: elyra-skills
  version: 1.0.0
  tags: [filament, laravel, admin, crud, panels]
---

# Filament Resource Design

Filament gives you a CRUD admin in minutes — and an unmaintainable one just as fast. The craft is in **what you don't put in the resource** and in keeping table queries honest.

## When to use

- Creating or reviewing Filament resources, pages, actions, widgets
- "Resource, relation manager, or custom page?" decisions
- Slow admin tables, N+1s in columns, memory-hungry exports
- Authorization and multi-user safety in a panel

## Principles

- **A resource mirrors a model; a process gets a page.** CRUD on `Order` = resource. "Monthly reconciliation flow" = custom page with steps — forcing processes into resource edit forms is how admin panels rot.
- **Policies are the law, visibility is courtesy.** Filament respects model policies — write them first. Hiding a button is UX; the policy is security.
- **The table query is a query.** Every column, badge, and count runs SQL per row unless you eager load and aggregate deliberately.
- **Schema code is code.** Long `form()`/`table()` definitions get extracted, shared field groups reused — same review standards as any class.

## Process

### 1. Choose the structure

| Need | Build |
|---|---|
| CRUD on a model | Resource |
| Child records edited in parent context | Relation manager (or repeater for simple owned rows) |
| Multi-step process, dashboard-like flows | Custom page (optionally with embedded widgets/tables) |
| Cross-model overview, KPIs | Dashboard + widgets |
| Different audiences (admin vs vendor) | Separate panels, not one panel with role-spaghetti |

### 2. Authorization first

- Write the model policy (`viewAny`, `view`, `create`, `update`, `delete`, plus custom abilities) before decorating the UI
- Per-action checks: bulk actions and custom actions need explicit `authorize`/policy calls — they don't inherit the row's edit check magically
- Tenancy/scoping: scope the resource's base query (`getEloquentQuery()`) — a global search or direct URL must not reach other tenants' records

### 3. Design the table for the operator

- Columns: the few the operator scans for, not every DB column; `searchable()`/`sortable()` only where indexed (each adds query cost)
- **Performance checklist per table:**
  - relations rendered? → eager load via query modification (`->with(...)`)
  - counts/sums shown? → `withCount`/`withSum`, not per-row closures
  - heavy columns (images, JSON) excluded from select where possible
- Filters: a handful of high-value ones (status, date range, owner); default filter for the 90% case (e.g. "active")
- Bulk actions: confirmation + chunked processing; exports queued, never built in-request for big tables

### 4. Design forms that guide

- Group with sections/tabs by how the *operator* thinks, not by column order
- Reactive fields (`live()`) only where a field genuinely drives another — every one is a server round-trip
- Extract repeated field groups (address, money, SEO block) into shared schema classes/methods
- Validation mirrors the domain rules — the admin panel is not a validation-free backdoor

### 5. Actions for domain operations

- Domain operations (refund, approve, resend invoice) = explicit actions calling your domain layer/action classes — **not** "edit the status field and hope side effects fire"
- Destructive/irreversible: `requiresConfirmation()`, danger color, and an audit trail (who did what when — log it)

### 6. Review pass

```bash
grep -rn "getStateUsing\|formatStateUsing" app/Filament | head   # per-row closures: N+1 suspects
grep -rn "live()" app/Filament | wc -l                            # round-trip count
ls app/Policies                                                   # do policies exist at all?
```

Plus: resources > ~300 lines (extract schema classes), missing `getEloquentQuery()` scoping in multi-tenant apps, status changed via edit form instead of actions.

## Output format

```markdown
## Filament review: <panel/resource>

### Structure
| Need | Built as | Should be |
|------|----------|-----------|

### Authorization
Policies: ✅/❌ per model — scoped base query: ✅/❌ — bulk/custom actions authorized: ✅/❌

### Table performance
| Table | eager loads | aggregates | per-row closures | indexed search |
|-------|-------------|------------|------------------|----------------|

### Findings (ranked)
1. <file:line> — <issue> → <fix>
```

## Anti-patterns

- ❌ Building the panel first, policies "later" — later never comes
- ❌ Per-row closures hitting relations: an N+1 per column per row
- ❌ A 700-line resource with the whole domain modeled in one form
- ❌ Domain state changed by editing a status dropdown instead of an explicit action
- ❌ `live()` on half the form because one field once needed it
- ❌ One panel serving admins, vendors, and customers via visibility conditions
- ❌ Synchronous export of 100k rows from a table action
- ❌ Multi-tenant app without a scoped `getEloquentQuery()` — global search leaks records
