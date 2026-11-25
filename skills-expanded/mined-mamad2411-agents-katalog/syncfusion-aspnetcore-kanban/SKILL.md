---
name: syncfusion-aspnetcore-kanban
description: Guide for implementing the Syncfusion ASP.NET Core Kanban component using Tag Helper syntax. Use this skill when building task boards, configuring columns and swimlanes, or enabling drag-and-drop. Covers card settings, dialogs, and binding remote data for ASP.NET Core MVC and Razor Pages.
metadata:
    author: "Syncfusion Inc"
    version: "33.1.44"
    category: "Data Visualization"
---

# Implementing Syncfusion ASP.NET Core Kanban

## Table of Contents
- [Quick Start](#quick-start)
- [When to Use This Skill](#when-to-use-this-skill)
- [Documentation and Navigation Guide](#documentation-and-navigation-guide)
  - [Setup and First Board](#setup-and-first-board)
  - [Data Binding](#data-binding)
  - [Cards](#cards)
  - [Columns](#columns)
  - [Swimlanes](#swimlanes)
  - [Drag and Drop](#drag-and-drop)
  - [Card Edit Dialog](#card-edit-dialog)
  - [Sorting, Priority, and Validation](#sorting-priority-and-validation)
  - [Tooltip, Style, and Dimensions](#tooltip-style-and-dimensions)
  - [Persistence, Localization, and Responsive](#persistence-localization-and-responsive)
  - [Virtual Scrolling and Accessibility](#virtual-scrolling-and-accessibility)
  - [Events](#events)
  - [Methods](#methods)
  - [All Properties Reference](#all-properties-reference)
  - [How-To Recipes](#how-to-recipes)
- [Common Patterns](#common-patterns)
- [Key Properties Reference](#key-properties-reference)
- [Data Model](#data-model)

## Quick Start

```csharp
// HomeController.cs
public IActionResult Index()
{
    ViewBag.data = new KanbanDataModels().KanbanTasks();
    return View();
}
```

```html
<!-- Index.cshtml -->
<ejs-kanban id="Kanban" keyField="Status" dataSource="@ViewBag.data">
    <e-kanban-columns>
        <e-kanban-column headerText="To Do" keyField="Open"></e-kanban-column>
        <e-kanban-column headerText="In Progress" keyField="InProgress"></e-kanban-column>
        <e-kanban-column headerText="Testing" keyField="Testing"></e-kanban-column>
        <e-kanban-column headerText="Done" keyField="Close"></e-kanban-column>
    </e-kanban-columns>
    <e-kanban-cardsettings headerField="Title" contentField="Summary"></e-kanban-cardsettings>
</ejs-kanban>
```

**Prerequisites:**
- NuGet: `Install-Package Syncfusion.EJ2.AspNet.Core`
- `_ViewImports.cshtml`: `@addTagHelper *, Syncfusion.EJ2`
- `_Layout.cshtml`: Fluent CSS + `ej2.min.js` CDN links + `<ejs-scripts></ejs-scripts>`

→ For full setup details, see [references/getting-started.md](references/getting-started.md)

## When to Use This Skill

Use this skill when you need to:
- **Build a Kanban board** — multi-column workflow visualization
- **Configure columns** — single/multi-key columns, stacked headers, toggle, drag
- **Add swimlanes** — group cards by team, user, or category with frozen rows
- **Enable drag-and-drop** — between columns, swimlanes, or external components
- **Implement card dialogs** — edit dialog with custom fields, templates, CRUD persistence
- **Bind remote data** — OData, WebAPI, UrlAdaptor with CRUD operations
- **Apply sorting** — by index, data source order, or custom field
- **Set card priorities** — exact-position drop ordering via numeric rank field
- **Add column constraints** — min/max card count validation per column
- **Show tooltips** — default or template-based hover tooltips
- **Enable virtual scrolling** — handle large datasets (100k+ cards) efficiently
- **Configure accessibility** — WCAG 2.2 AA, keyboard navigation, screen reader support
- **Localize or RTL** — multi-language support and right-to-left layout
- **Filter or search cards** — using the `query` property
- **Change columns dynamically** — update column configuration at runtime
- **Handle events** — react to card clicks, drags, dialog open/close, data binding, and more
- **Call methods programmatically** — add/update/delete cards, open dialogs, show/hide columns, refresh the board
- **Reference all properties** — full list of component and sub-model properties with types and defaults

## Documentation and Navigation Guide

### Setup and First Board
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- NuGet installation and package setup
- Tag Helper registration in `_ViewImports.cshtml`
- CDN configuration (CSS + JS) in `_Layout.cshtml`
- Minimal Kanban board with 4 columns
- Basic swimlane quickstart
- License key registration

### Data Binding
📄 **Read:** [references/data-binding.md](references/data-binding.md)
- Local data binding via `@ViewBag.data`
- Remote data: OData, ODataV4, WebAPI, UrlAdaptor
- `<e-data-manager>` configuration
- CRUD operations with `insertUrl`, `updateUrl`, `removeUrl`, `crudUrl`
- Custom adaptor pattern
- `actionFailure` event handling
- Ajax loading indicator behavior

### Cards
📄 **Read:** [references/cards.md](references/cards.md)
- `headerField` (mandatory unique card ID)
- `showHeader` — show/hide card header
- `contentField` — card body text field
- Card template with jsrender syntax
- `selectionType` — None, Single, Multiple
- Card color customization via `colorField`

### Columns
📄 **Read:** [references/columns.md](references/columns.md)
- Single-key and multi-key `keyField` mapping
- `headerText` — column display name
- Column header template
- `allowToggle` — collapsible columns
- `isExpanded` — initial expand/collapse state
- Stacked headers (`<e-kanban-stackedheaders>`)
- Column-level drag (`allowColumnDragAndDrop`)
- `showItemCount` — display card count in header

### Swimlanes
📄 **Read:** [references/swimlane.md](references/swimlane.md)
- `keyField` — data field to group by
- `textField` — display label field
- Swimlane header template
- `sortBy` — sort swimlane rows
- `allowDragAndDrop` — enable cross-swimlane card drag
- `showEmptyRow` — display empty swimlane rows
- `showItemCount` — card count per swimlane
- `enableFrozenRows` — sticky swimlane headers on scroll

### Drag and Drop
📄 **Read:** [references/drag-and-drop.md](references/drag-and-drop.md)
- Internal column drag (default enabled)
- `allowDragAndDrop="false"` — disable all drag
- Per-column `allowDrag`/`allowDrop` flags
- `transitionColumns` — restrict allowed column transitions
- Cross-swimlane drag via `swimlaneSettings.allowDragAndDrop`
- External drag: `externalDropId` property
- Kanban-to-Kanban drag (`dragStop` event + `deleteCard`/`addCard`)
- Kanban-to-Treeview and Kanban-to-Schedule integration

### Card Edit Dialog
📄 **Read:** [references/dialog.md](references/dialog.md)
- Default dialog (double-click card)
- Custom dialog fields via `<e-kanban-dialogsettings fields="...">`
- Field types: String, Numeric, TextArea, DropDown, TextBox, Input
- Custom dialog template with EJ2 component initialization
- Preventing dialog open with `dialogOpen` event + `args.cancel = true`
- Programmatic add: `kanbanObj.openDialog('Add', data)`
- CRUD persistence via UrlAdaptor with server-side `EditParams` class

### Sorting, Priority, and Validation
📄 **Read:** [references/sorting-priority-validation.md](references/sorting-priority-validation.md)
- `<e-kanban-sortsettings>` with `sortBy`, `field`, `direction`
- `sortBy` values: Index, DataSourceOrder, Custom
- Priority field: `<e-kanban-cardsettings priority="RankId">` for exact-position drops
- Column min/max card count: `minCount`, `maxCount` on `<e-kanban-column>`
- Constraint type: Column (default) or Swimlane
- Visual color indication on constraint violation

### Tooltip, Style, and Dimensions
📄 **Read:** [references/tooltip-style-dimensions.md](references/tooltip-style-dimensions.md)
- `enableTooltip="true"` — hover tooltip on cards
- `tooltipTemplate` — custom HTML tooltip template
- CSS class reference for all Kanban elements
- Sticky header pattern
- `width` and `height` — auto, pixel, percentage values

### Persistence, Localization, and Responsive
📄 **Read:** [references/persistence-localization-responsive.md](references/persistence-localization-responsive.md)
- `enablePersistence="true"` — localStorage state saving
- `locale` property + `ej.base.L10n.load()` script
- All locale key names for Kanban strings
- `enableRtl="true"` — right-to-left layout
- Mobile responsive behavior (swipe, tap-hold, swimlane menu)

### Virtual Scrolling and Accessibility
📄 **Read:** [references/virtual-scrolling-accessibility.md](references/virtual-scrolling-accessibility.md)
- `enableVirtualization="true"` — on-demand card rendering
- `cardHeight` — fixed height required for virtualization
- Server-side `KanbanVirtualization` parameter handling
- WCAG 2.2 AA compliance table
- WAI-ARIA attributes (`aria-label`, `aria-expanded`, `aria-selected`, etc.)
- Keyboard shortcuts reference
- `AllowKeyboard="false"` — disable keyboard interaction

### Events
📄 **Read:** [references/events.md](references/events.md)
- `ActionBegin` / `ActionComplete` / `ActionFailure` — lifecycle and error handling
- `CardClick` / `CardDoubleClick` / `CardRendered` — card interaction hooks
- `ColumnDrag` / `ColumnDragStart` / `ColumnDrop` — column reorder events
- `Created` / `DataBinding` / `DataBound` / `DataSourceChanged` — initialization and data events
- `DialogOpen` / `DialogClose` — intercept or cancel dialog (use `args.cancel = true`)
- `Drag` / `DragStart` / `DragStop` — card drag lifecycle (cross-Kanban scenarios use `DragStop`)
- `QueryCellInfo` — customize column cell elements before render

### Methods
📄 **Read:** [references/methods.md](references/methods.md)
- `AddCard` / `UpdateCard` / `DeleteCard` — CRUD card operations
- `AddColumn` / `DeleteColumn` — dynamic column management
- `OpenDialog` / `CloseDialog` — programmatic dialog control
- `ShowColumn` / `HideColumn` — toggle column visibility
- `GetCardDetails` / `GetColumnData` / `GetSelectedCards` / `GetSwimlaneData` — data retrieval
- `ShowSpinner` / `HideSpinner` — loading indicator control
- `Refresh` / `RefreshHeader` / `RefreshUI` — board re-render helpers
- `DataBind` / `Destroy` / `AppendTo` / `Inject` — component lifecycle utilities

### All Properties Reference
📄 **Read:** [references/properties.md](references/properties.md)
- Complete list of all `<ejs-kanban>` root properties with types, defaults, and examples
- Sub-model properties: `CardSettings`, `Columns`, `SwimlaneSettings`, `SortSettings`, `DialogSettings`, `StackedHeaders`
- Enum values: `ConstraintType`, `SelectionType`, `SortOrderBy`, `SortDirection`

### How-To Recipes
📄 **Read:** [references/how-to.md](references/how-to.md)
- Dynamically change columns at runtime
- Filter cards using the `query` property with dropdown
- Search cards by field values with text input
- Add header double-click event handler

## Common Patterns

### Swimlane Board with Remote Data

> **Use when:** You need to group cards by user/team and load data from an API endpoint (OData, WebAPI, etc.) instead of a local collection.

```html
<ejs-kanban id="Kanban" keyField="Status">
    <e-data-manager url="/api/tasks" adaptor="ODataV4Adaptor"></e-data-manager>
    <e-kanban-columns>
        <e-kanban-column headerText="To Do" keyField="Open"></e-kanban-column>
        <e-kanban-column headerText="In Progress" keyField="InProgress"></e-kanban-column>
        <e-kanban-column headerText="Done" keyField="Close"></e-kanban-column>
    </e-kanban-columns>
    <e-kanban-cardsettings headerField="Title" contentField="Summary"></e-kanban-cardsettings>
    <e-kanban-swimlanesettings keyField="Assignee" textField="Assignee"></e-kanban-swimlanesettings>
</ejs-kanban>
```

### Board with Column Constraints

> **Use when:** You need to enforce WIP (Work-In-Progress) limits — preventing too few or too many cards from stacking in a column.

```html
<ejs-kanban id="Kanban" keyField="Status" dataSource="@ViewBag.data">
    <e-kanban-columns>
        <e-kanban-column headerText="To Do" keyField="Open"></e-kanban-column>
        <e-kanban-column headerText="In Progress" keyField="InProgress"
            minCount="3" maxCount="5" showItemCount="true"></e-kanban-column>
        <e-kanban-column headerText="Done" keyField="Close"></e-kanban-column>
    </e-kanban-columns>
    <e-kanban-cardsettings headerField="Title" contentField="Summary"></e-kanban-cardsettings>
</ejs-kanban>
```

### Board with Card Edit Dialog + CRUD

> **Use when:** Users need to create, edit, or delete cards through a dialog form, with changes persisted to the server via `UrlAdaptor`.

```html
<ejs-kanban id="Kanban" keyField="Status">
    <e-data-manager url="/Home/UpdateData" adaptor="UrlAdaptor"
        crudUrl="/Home/UpdateData"></e-data-manager>
    <e-kanban-columns>
        <e-kanban-column headerText="To Do" keyField="Open"></e-kanban-column>
        <e-kanban-column headerText="Done" keyField="Close"></e-kanban-column>
    </e-kanban-columns>
    <e-kanban-cardsettings headerField="Title" contentField="Summary"></e-kanban-cardsettings>
    <e-kanban-dialogsettings fields="@ViewBag.dialogFields"></e-kanban-dialogsettings>
</ejs-kanban>
```

### Virtual Scrolling Board

> **Use when:** The dataset is large (hundreds to thousands of cards) and rendering all cards at once would cause performance issues.

```html
<ejs-kanban id="Kanban" keyField="Status" dataSource="@ViewBag.data"
    enableVirtualization="true">
    <e-kanban-columns>
        <e-kanban-column headerText="To Do" keyField="Open"></e-kanban-column>
        <e-kanban-column headerText="In Progress" keyField="InProgress"></e-kanban-column>
        <e-kanban-column headerText="Done" keyField="Close"></e-kanban-column>
    </e-kanban-columns>
    <e-kanban-cardsettings headerField="Title" contentField="Summary"
        selectionType="Multiple"></e-kanban-cardsettings>
</ejs-kanban>
```

## Key Properties Reference

| Property | Tag | Values | Purpose |
|---|---|---|---|
| `keyField` | `<ejs-kanban>` | Field name string | Maps cards to columns by status value |
| `dataSource` | `<ejs-kanban>` | `@ViewBag.data` | Local data collection |
| `enableVirtualization` | `<ejs-kanban>` | true/false | Virtual scrolling for large data |
| `enableTooltip` | `<ejs-kanban>` | true/false | Hover tooltip on cards |
| `tooltipTemplate` | `<ejs-kanban>` | Template ID string | Custom tooltip HTML template |
| `allowDragAndDrop` | `<ejs-kanban>` | true/false | Global drag-and-drop toggle |
| `externalDropId` | `<ejs-kanban>` | Element ID array | Target IDs for external drop |
| `enablePersistence` | `<ejs-kanban>` | true/false | Save state to localStorage |
| `locale` | `<ejs-kanban>` | Locale string (e.g. `"de"`) | UI string localization |
| `enableRtl` | `<ejs-kanban>` | true/false | Right-to-left layout |
| `width` | `<ejs-kanban>` | auto/px/% | Board width |
| `height` | `<ejs-kanban>` | auto/px/% | Board height |
| `AllowKeyboard` | `<ejs-kanban>` | true/false | Keyboard navigation toggle |
| `headerField` | `<e-kanban-cardsettings>` | Field name string | Unique card ID field (mandatory) |
| `contentField` | `<e-kanban-cardsettings>` | Field name string | Card body text field |
| `template` | `<e-kanban-cardsettings>` | Template ID string | Custom card HTML template |
| `selectionType` | `<e-kanban-cardsettings>` | None/Single/Multiple | Card selection mode |
| `priority` | `<e-kanban-cardsettings>` | Field name string | Numeric rank field for ordering |
| `showHeader` | `<e-kanban-cardsettings>` | true/false | Show/hide card header |
| `keyField` | `<e-kanban-column>` | Status value(s) | Column card filter (single or comma-separated) |
| `headerText` | `<e-kanban-column>` | Display string | Column title |
| `allowToggle` | `<e-kanban-column>` | true/false | Collapsible column |
| `isExpanded` | `<e-kanban-column>` | true/false | Initial expand state |
| `minCount` | `<e-kanban-column>` | Integer | Minimum cards constraint |
| `maxCount` | `<e-kanban-column>` | Integer | Maximum cards constraint |
| `showItemCount` | `<e-kanban-column>` | true/false | Show card count badge |
| `allowDrag` | `<e-kanban-column>` | true/false | Allow cards to be dragged from column |
| `allowDrop` | `<e-kanban-column>` | true/false | Allow cards to be dropped into column |
| `keyField` | `<e-kanban-swimlanesettings>` | Field name string | Swimlane grouping field |
| `textField` | `<e-kanban-swimlanesettings>` | Field name string | Swimlane display label field |
| `sortBy` | `<e-kanban-sortsettings>` | Index/DataSourceOrder/Custom | Card sort strategy |
| `field` | `<e-kanban-sortsettings>` | Field name string | Field to sort by |
| `direction` | `<e-kanban-sortsettings>` | Ascending/Descending | Sort direction |

## Data Model

The standard `KanbanDataModels` class for all examples:

```csharp
public class KanbanDataModels
{
    public string Id { get; set; }
    public string Title { get; set; }
    public string Status { get; set; }      // Maps to keyField
    public string Summary { get; set; }     // Card body content
    public string Type { get; set; }
    public string Priority { get; set; }
    public string Tags { get; set; }
    public double Estimate { get; set; }
    public string Assignee { get; set; }    // Used for swimlane grouping
    public int RankId { get; set; }         // Numeric rank for priority ordering
    public string Color { get; set; }       // Optional card color field
}
```
