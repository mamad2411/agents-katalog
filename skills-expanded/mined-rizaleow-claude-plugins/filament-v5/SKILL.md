---
description: Filament v5 (Laravel admin panel) overview — core concepts (Resources, Schemas, Tables, Actions, Panels, Widgets), naming conventions, when to extract Schema/Table classes. Use whenever the user works in `app/Filament/`, mentions Filament, or builds admin UI in Laravel.
---

# Filament v5 — orientation

Filament v5 unifies forms + infolists + layouts under a single **Schemas API** and moves actions into the top-level `Filament\Actions` namespace. Everything below assumes v5; do not import any `Filament\Forms\Form`, `Filament\Tables\Actions\*`, or `Filament\Infolists\*` style symbols.

## Preflight

1. Confirm version via `mcp__boost__filament_get_version` (or `composer show filament/filament`). Refuse to scaffold v3/v4 patterns.
2. Run `mcp__boost__filament_list_panels` to see registered `PanelProvider` classes — there is at least one (`AdminPanelProvider`).
3. For an audit pass, run `mcp__boost__filament_lint` on the target directory.

## Core concepts

| Concept | Namespace | Typical file |
| --- | --- | --- |
| Resource | `App\Filament\Resources\<Models>\<Model>Resource` | `app/Filament/Resources/Customers/CustomerResource.php` |
| Schema (form/infolist) | `Filament\Schemas\Schema` | `Schemas/CustomerForm.php`, `Schemas/CustomerInfolist.php` |
| Table | `Filament\Tables\Table` | `Tables/CustomersTable.php` |
| Action | `Filament\Actions\Action` (+ subclasses) | inline or `Actions/SendInvoiceAction.php` |
| Panel | `Filament\Panel` via `PanelProvider` | `app/Providers/Filament/AdminPanelProvider.php` |
| Widget | `Filament\Widgets\*` | `app/Filament/Widgets/StatsOverview.php` |

## Decision tree

- Editing a CRUD over an existing Eloquent model → **filament-resources**.
- Designing fields / sections / wizard / repeater / infolist → **filament-schemas**.
- Columns, filters, grouping, row actions → **filament-tables**.
- Header / row / bulk / modal actions → **filament-actions**.
- Dashboard cards, charts → **filament-widgets**.
- Auth, tenancy, multi-panel, branding → **filament-panels**.
- Reusable field/column/entry/plugin → **filament-custom-components**.
- Pest tests for any of the above → **filament-testing**.
- Touching v3/v4 code or upgrading → **filament-v5-migration**.

## MCP tool reference (from `rizaleow/filament-boost`)

| Tool | Purpose |
| --- | --- |
| `mcp__boost__filament_get_version` | Detect installed Filament version. |
| `mcp__boost__filament_list_panels` | All registered panels + IDs. |
| `mcp__boost__filament_list_resources` | All resources in a panel. |
| `mcp__boost__filament_inspect_resource` | Schema, table, pages, policies of one resource. |
| `mcp__boost__filament_list_widgets` | Registered widgets per panel. |
| `mcp__boost__filament_list_custom_components` | User-defined fields/columns/entries. |
| `mcp__boost__filament_list_installed_plugins` | Filament plugin packages. |
| `mcp__boost__filament_scaffold_resource` | Generate Resource + Schema + Table diff. |
| `mcp__boost__filament_scaffold_widget` | Generate Stats/Chart/Table widget diff. |
| `mcp__boost__filament_scaffold_action` | Generate standalone Action class diff. |
| `mcp__boost__filament_scaffold_custom_field` | Generate a custom Field + view diff. |
| `mcp__boost__filament_docs_search` | Search the bundled v5 docs corpus. |
| `mcp__boost__filament_lint` | Detect v3/v4 holdovers and convention drift. |
| `mcp__boost__filament_upgrade_suggest` | Propose v4→v5 rewrites. |

## Conventions Filament v5 expects

- Plural model directory: `app/Filament/Resources/Customers/CustomerResource.php`.
- Extract schemas/tables once they exceed ~30 lines or are reused.
- Static methods on resources: `static form(Schema $schema): Schema`, `static table(Table $table): Table`, `static getPages(): array`.
- Actions imported from `Filament\Actions\*`, **never** `Filament\Tables\Actions\*`.
- Tables use `->recordActions([...])`, `->toolbarActions([...])` — not `->actions([...])` or `->bulkActions([...])`.

See also: filament-resources, filament-schemas, filament-tables, filament-actions, filament-v5-migration.
