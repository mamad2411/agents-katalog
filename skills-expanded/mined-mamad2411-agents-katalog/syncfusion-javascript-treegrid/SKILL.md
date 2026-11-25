---
name: syncfusion-javascript-treegrid
description: Implements Syncfusion Javascript TreeGrid for hierarchical data with sorting, filtering, editing, exporting, paging, virtual scrolling, and advanced features. Supports configuration, CRUD, aggregates, templates, state persistence, and performance optimization in Javascript applications.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Grids"
---

# Syncfusion TypeScript TreeGrid

A comprehensive skill for implementing and customizing Syncfusion's Javascript TreeGrid component. TreeGrid visualizes self-referential hierarchical data in a tabular layout with expand/collapse functionality, enterprise features like virtual scrolling, and comprehensive export options.

	## ⚠️ Security & Trust Boundary
 
- The TreeGrid skill does not perform any remote data access.
- All external API interaction is handled by a separate DataManager skill outside this skill’s trust boundary.

## When to Use This Skill

Use this skill when you need to:
  - Display hierarchical or tree-structured data (organizational charts, file systems, bill of materials)
  - Configure columns with proper data binding and formatting
  - Implement data editing (cell, row, dialog, batch, template modes)
  - Add sorting, filtering, and searching capabilities
  - Handle row and cell operations (selection, templates, spanning)
  - Optimize performance with virtual scrolling or infinite scrolling
  - Configure paging and scrolling strategies
  - Export data to PDF, Excel, or CSV formats
  - Implement state persistence and aggregation
  - Customize appearance with themes and styling
  - Support accessibility and internationalization (RTL, localization)

**DO NOT use this skill for:**
- Simple flat table display (use DataGrid instead)
- Tree view components (use TreeView control)
- File upload/download handling (separate concern)

## Table of Contents
  - [TreeGrid Overview](#treegrid-overview)
  - [Data Structure Rules](#data-structure-rules)
  - [API Reference](#api-reference)
  - [Feature Overview & Navigation Guide](#feature-overview--navigation-guide)
  - [Quick Start Example](#quick-start-example)

## TreeGrid Overview

The TreeGrid is optimized for displaying self-referential hierarchical data with:
  - **Auto-expand/collapse** functionality for collapsible rows
  - **Enterprise features**: virtual scrolling, aggregates, state persistence
  - **Adaptive UI** for mobile and small screens
  - **Comprehensive export**: PDF, Excel, CSV formats
  - **Full accessibility**: WCAG compliance, keyboard navigation, ARIA support
  - **Internationalization**: RTL support, locale customization

## Data Structure Rules

### Rule 1: childMapping is MANDATORY for Hierarchical Data
**Severity**: 🔴 CRITICAL - Grid will not expand/collapse without this

**Requirement**:
```typescript
import { TreeGrid } from '@syncfusion/ej2-treegrid';

// ✅ REQUIRED - childMapping matches data property name exactly
let treeGridObj: TreeGrid = new TreeGrid({
    dataSource: hierarchicalData,
    childMapping: 'subtasks',  // Must match property in data
    treeColumnIndex: 0,
    columns: [
        { field: 'taskID', headerText: 'Task ID', width: 90 },
        { field: 'taskName', headerText: 'Task Name', width: 200 }
    ]
});

// ❌ WRONG - No childMapping = No expansion possible
let treeGridObj2: TreeGrid = new TreeGrid({
    dataSource: hierarchicalData,
    // Missing childMapping - Won't work!
    columns: [...]
});
```

**Data Format**:
```typescript
// ✅ CORRECT - childMapping matches 'subtasks' property
const hierarchicalData = [
  {
    taskID: 1,
    taskName: 'Planning',
    subtasks: [  // Must match childMapping value exactly
      { taskID: 2, taskName: 'Identify Site' },
      { taskID: 3, taskName: 'Perform Test' }
    ]
  }
];

// Alternative: Flat structure with parent IDs
const flatData = [
    { taskID: 1, taskName: 'Planning', parentID: null, isParent: true },
    { taskID: 2, taskName: 'Identify Site', parentID: 1, isParent: false }
];

let treeGridObj3: TreeGrid = new TreeGrid({
    dataSource: flatData,
    idMapping: 'taskID',
    parentIdMapping: 'parentID',
    hasChildMapping: 'isParent'
});
```

### Rule 2: Data Type Matching is MANDATORY
**Severity**: 🟠 IMPORTANT - Type mismatches cause rendering/sorting issues

**Requirement**:
```typescript
// ✅ CORRECT - Type matches column definition
const data = [
  {
    taskID: 1,              // number type
    taskName: 'Planning',   // string type
    startDate: new Date(),  // Date object for date columns
  }
];

// Column definition must match data types
let treeGridObj: TreeGrid = new TreeGrid({
    dataSource: data,
    columns: [
        { field: 'taskID', headerText: 'ID', type: 'number', width: 90 },
        { field: 'taskName', headerText: 'Task', type: 'string', width: 200 },
        { field: 'startDate', headerText: 'Date', type: 'date', format: 'yMd', width: 120 }
    ]
});

// ❌ WRONG - Type mismatch
const badData = [
  {
    taskID: '1',            // String instead of number
    startDate: '02/03/2024' // String instead of Date object
  }
];
```

---

## API Reference

### Properties & Methods
📄 **Read:** [references/api-properties-methods.md](references/api-properties-methods.md)
- Complete property reference (83 properties)
- Organized by category: Data & Configuration, Behavior & Display, Selection, Editing, Export, Advanced
- All methods (108 total)
- Method signatures and return types
- When to use? Setting up configuration, CRUD operations, DOM manipulation, row/cell management

### Events & Modules
📄 **Read:** [references/api-events-modules.md](references/api-events-modules.md)
- Complete event reference (66 events)
- Events organized by lifecycle: Lifecycle Events, Data, Edit, Selection, Expand/Collapse, Export, UI Interaction, Drag/Drop
- Feature modules (15 total)
- Module injection patterns and usage
- When to use? Responding to grid state changes, handling user interactions, optimizing feature loading

---

## Feature Overview & Navigation Guide

The TreeGrid component provides comprehensive features for managing, displaying, and interacting with hierarchical data. Below is the complete navigation guide organized by feature area.

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and package setup
- TypeScript configuration
- Basic TreeGrid initialization
- Minimal data binding example
- First tree structure setup

### Data Handling & Binding
📄 **Read:** [references/data-handling.md](references/data-handling.md)
- Local data binding (hierarchical and self-referential structures)
- Hierarchical data with childMapping (nested arrays)
- Self-referential data with idMapping/parentIdMapping (flat data)
- Remote data binding with DataManager and adaptors
- Load on demand for lazy loading child records
- Offline mode for client-side processing
- Custom adaptors for extended functionality
- AJAX binding with Fetch API
- Immutable mode for performance optimization
- Error handling and CRUD operations via DataManager

### Column Configuration & Features
📄 **Read:** [references/columns.md](references/columns.md)
- Column basics (field binding, types, primary keys, per-column operation control)
- Column types (string, number, date, datetime, boolean) and formatting
- Header customization (text, templates, custom HTML)
- Column templates and value accessors (custom formatting, computed columns)
- Complex data binding with dot notation (nested objects, hierarchical data)
- Column resizing with min/max width constraints
- Column reordering via drag-drop or programmatic API
- Column visibility control (show/hide per column)
- Column menu with sort, filter, and autofit actions
- Column chooser for end-user visibility management
- Column spanning to merge cells horizontally
- Responsive columns that hide/show based on media queries
- Auto-fit columns to content width
- Frozen columns: Lock specific columns with isFrozen to keep visible while scrolling
- Freeze direction: Freeze columns at left or right side (freeze: 'Left'|'Right')
- Frozen with 4-zone layout: Combine frozenRows + frozenColumns for master-detail grids

### Row Features & Templates
📄 **Read:** [references/row-features.md](references/row-features.md)
- Row selection modes (single, multiple)
- Checkbox selection
- Row detail/template expansion
- Row drag and drop
- Row indentation and spanning
- Row height configuration
- Frozen rows: Keep top N rows visible while scrolling vertically (frozenRows)
- Frozen rows + columns: Create 4-zone layout for master-detail grids
- Frozen rows with hierarchy: Expand/collapse works in frozen parent rows
- Frozen with detail templates: Combine frozen rows with master-detail patterns

### Editing Operations
📄 **Read:** [references/editing.md](references/editing.md)
- CRUD operations setup (Create, Read, Update, Delete)
- Edit modes (Cell, Row, Dialog, Batch) with use cases
- Edit types and components (text, number, dropdown, date, checkbox)
- Custom edit templates with create/write/read patterns
- Field validation (required, type, custom rules)
- Toolbar actions and delete confirmation dialogs
- Command column with built-in and custom buttons
- Default values and disabling column editing
- Server persistence with URL Adaptor and Remote Save Adaptor
- Server-side CRUD operation handlers (Insert, Update, Delete, Batch)

### Sorting Features
📄 **Read:** [references/sorting.md](references/sorting.md)
- Sorting basics: Click column header to toggle ascending/descending
- Initial sort: Set default sort columns at load time via sortSettings
- Multi-column sort: Use CTRL+Click to sort by multiple columns
- Sort configuration: Disable sorting for specific columns, set default direction
- Sort methods: Programmatically sort or clear sorts (sortByColumn, clearSorting)
- Sort events: Respond to sort start/complete (actionBegin, actionComplete)
- Sort UI: Column header icons indicating sort direction
- Touch interaction: Multi-sort popup on touch devices
- Common patterns: Sort + Filter combinations, hierarchical sort behavior

### Searching & Quick Find
📄 **Read:** [references/searching.md](references/searching.md)
- Searching basics: Enable toolbar search box for text-based filtering
- Initial search: Set default search value and configuration at load time
- Search operators: Contains, startswith, endswith, equal, notequal matching
- Search configuration: Configure searchable columns and ignoreCase behavior
- Search external button: Trigger search programmatically from custom UI
- Search specific columns: Limit search scope to specific column fields only
- Search methods: Use search() method for programmatic searching
- Common patterns: Search + Sort, Search + Filter combinations

### Filtering Options
📄 **Read:** [references/filtering.md](references/filtering.md)
- Filtering basics and configuration
- Filter hierarchy modes (Parent, Child, Both, None)
- Initial filters via filterSettings.columns
- Filter operators and expressions
- Filter bar with custom templates
- Filter menu with custom components
- Excel-like filter interface
- Diacritics and special character handling
- Programmatic filtering methods

### Aggregation & Summaries
📄 **Read:** [references/aggregation.md](references/aggregation.md)
- Aggregate types (sum, average, count, min, max, custom)
- Footer aggregates display
- Group-level aggregation
- Custom aggregate templates

### Excel Export
📄 **Read:** [references/excel-export.md](references/excel-export.md)
- Basic Excel export with hierarchy preservation
- Export options: persist collapsed state, include hidden columns, show/hide columns during export
- File name customization and custom data source
- Cell styling: conditional formatting (excelQueryCellInfo event), theme application
- Headers and footers with styling, hyperlinks, and alignment
- Server-side export: ASP.NET MVC configuration, serverExcelExport method
- CSV export (server-side): serverCsvExport method
- Custom aggregates export using excelAggregateQueryCellInfo event

### PDF Export
📄 **Read:** [references/pdf-export.md](references/pdf-export.md)
- Basic PDF export with hierarchical layout
- Export options: include hidden columns, show/hide columns, page orientation, page size
- File name customization and font customization (standard + custom fonts)
- Cell styling: conditional formatting (pdfQueryCellInfo event), theme application
- Headers and footers: text, lines, page numbers, images with positioning
- Server-side export: ASP.NET MVC configuration, serverPdfExport method
- Header rotation using BeginCellLayout event (server-side only)

### Performance Optimization
📄 **Read:** [references/performance.md](references/performance.md)
- Performance best practices
- Change detection strategies
- Lazy loading data patterns
- Memory management
- Monitoring and optimization techniques

### Styling & Appearance
📄 **Read:** [references/styling-and-appearance.md](references/styling-and-appearance.md)
- Theme configuration: Material, Bootstrap, Fabric, HighContrast, Tailwind
- CSS customization: Override default styles with custom CSS classes
- Adaptive UI: enableAdaptiveUI for mobile-friendly interface with responsive dialogs
- CSS classes reference: Complete list of TreeGrid CSS classes (root, header, body, pager, summary)
- CSS class customization: Override specific sections with targeted CSS

### Selection & Interaction
📄 **Read:** [references/selection-and-interaction.md](references/selection-and-interaction.md)
- Cell and row selection modes
- Checkbox selection
- Mouse and keyboard interactions
- Context menu integration
- Clipboard operations (copy, cut, paste)
- Selection types: Single vs Multiple row/cell selection
- Selection modes: Row selection, Cell selection, Both modes
- Row selection: Initial, conditional, get selected rows programmatically
- Cell selection: Flow vs Box selection modes
- Checkbox selection with header select-all option
- Programmatic selection control (selectRow, selectRows, getSelectedRecords)
- Toggle selection: Click selected row again to deselect
- Touch interactions: Multi-select popup on touch devices
- Selection events and event handlers (rowSelected, cellSelected)
- Bulk actions on selected rows (delete, archive, etc.)

### Context Menu
📄 **Read:** [references/context-menu.md](references/context-menu.md)
- Context menu basics: Enable with ContextMenu module injection
- Default menu items: AutoFit, Edit, Delete, Export, Sort, Page, Indent, Outdent
- Custom menu items: Define custom items with text, target, and id properties
- Custom item actions: Handle in contextMenuClick event handler
- Dynamic enable/disable: Use contextMenuOpen event to toggle item availability
- Target-specific menus: Show menus for header, row, or content areas using target property
- Common scenarios: Expand/Collapse rows, Edit/Delete records, Export actions

### Paging Configuration
📄 **Read:** [references/paging.md](references/paging.md)
- Paging setup with Page module injection and allowPaging property
- Page size modes: All (total count) vs Root (parent count only)
- Page size dropdown: Let users change rows per page dynamically
- Custom pager templates with page navigation controls
- Pager positioning: Move pager from bottom to top
- Programmatic page navigation (goToPage, goToNextPage, goToPreviousPage)
- Page change events (actionComplete with requestType: 'paging')
- Responsive page size based on screen width
- Tracking page changes for data loading or UI updates

### Scrolling & Performance
📄 **Read:** [references/scrolling.md](references/scrolling.md)
- Basic scrolling: Fixed height/width containers with auto scrollbars
- Responsive scrolling: 100% height/width in parent containers
- Sticky headers: Keep column headers visible while scrolling with enableStickyHeader
- Scroll to row: Jump to specific row or scroll selected row into view
- Row virtualization: Render only visible rows for 10,000+ row datasets (enableVirtualization)
- Column virtualization: Render only visible columns for 100+ column grids (enableColumnVirtualization)
- Infinite scrolling: Load buffer pages as user scrolls down (enableInfiniteScrolling)
- Infinite scroll cache mode: Cache loaded pages to avoid re-fetching
- Performance comparison: When to use paging vs virtual vs infinite scrolling
- Virtual vs Infinite: Virtual for client-side data, Infinite for server-side data
- Limitations: Virtual/Infinite don't support batch edit, detail templates, row templates

### Advanced Features & Operations

📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- Print: Toolbar print button, print modes (All/CurrentPage), show/hide columns while printing
- Toolbar: Built-in items, custom toolbar buttons, enable/disable toolbar items
- Clipboard: Copy/paste shortcuts, hierarchy modes, AutoFill in batch edit
- State Persistence: Enable persistence, get/set localStorage, persisted properties

### Loading Animation

📄 **Read:** [references/loading-animation.md](references/loading-animation.md)
- Spinner and Shimmer loading indicator types
- Automatic display during data operations
- Remote data source loading

### Global Locale & Accessibility

📄 **Read:** [references/global-local-accessibility.md](references/global-local-accessibility.md)
- Localization: L10n.load() for culture-specific translations, locale property setup
- Localization of dependent components: DatePicker, Form Validator, Grid
- Internationalization: loadCldr, setCulture, setCurrencyCode for number/date formatting
- Right-to-Left (RTL): enableRtl property for Arabic, Farsi, Urdu languages
- Accessibility compliance: WCAG 2.2, Section 508, screen reader support standards
- WAI-ARIA attributes: role=treegrid, aria-selected, aria-expanded, aria-sort, aria-busy, aria-label
- Keyboard navigation: Complete keyboard shortcuts and accessibility-checker validation

### Testing & Test Helpers

📄 **Read:** [references/testing-and-helpers.md](references/testing-and-helpers.md)
- Helper API reference: 20+ helper methods for DOM element access and property manipulation
- Setting up Cypress: Project initialization, Syncfusion package installation, Cypress configuration
- TreeGridHelper initialization: Import and instantiate helper with element ID
- Using setModel/getModel: Set and retrieve TreeGrid properties dynamically
- Using invoke function: Call TreeGrid methods programmatically (collapseAll, expandAll, print, export)
- Testing element access: Get header, footer, pager, dialog, filter, and content elements
- Writing test cases: Complete examples for property access, method invocation, and UI interaction
- Running Cypress: Interactive mode, headless mode, browser selection, spec file targeting
- Best practices: Use helpers instead of CSS selectors, meaningful delays, data setup, cleanup

---

## Quick Start Example

Here's a minimal TypeScript TreeGrid setup with vanilla Inject pattern:

```typescript
import { TreeGrid, Page, Edit } from '@syncfusion/ej2-treegrid';

// Data interface for type safety
interface TreeGridData {
  taskID: number;
  taskName: string;
  startDate: Date;
  endDate: Date;
  duration: number;
  progress: number;
  subtasks?: TreeGridData[];
}

// Sample hierarchical data
const data: TreeGridData[] = [
  {
    taskID: 1,
    taskName: 'Planning',
    startDate: new Date('02/03/2017'),
    endDate: new Date('02/07/2017'),
    duration: 5,
    progress: 100,
    subtasks: [
      {
        taskID: 2,
        taskName: 'Identify Site location',
        startDate: new Date('02/03/2017'),
        endDate: new Date('02/04/2017'),
        duration: 2,
        progress: 100
      },
      {
        taskID: 3,
        taskName: 'Perform soil test',
        startDate: new Date('02/04/2017'),
        endDate: new Date('02/05/2017'),
        duration: 1,
        progress: 100
      }
    ]
  }
];

// Inject required modules
TreeGrid.Inject(Page, Edit);

// Initialize TreeGrid
let treeGridObj: TreeGrid = new TreeGrid({
    dataSource: data,
    childMapping: 'subtasks',
    allowPaging: true,
    pageSettings: { pageSize: 10 },
    editSettings: { allowEditing: true, allowAdding: true, allowDeleting: true, mode: 'Row' },
    treeColumnIndex: 1,
    columns: [
        { field: 'taskID', headerText: 'Task ID', isPrimaryKey: true, width: 90, textAlign: 'Right' },
        { field: 'taskName', headerText: 'Task Name', width: 180, textAlign: 'Left' },
        { field: 'startDate', headerText: 'Start Date', width: 90, textAlign: 'Right', type: 'date', format: 'yMd' },
        { field: 'duration', headerText: 'Duration', width: 80, textAlign: 'Right' },
        { field: 'progress', headerText: 'Progress (%)', width: 80, textAlign: 'Right' }
    ]
});

treeGridObj.appendTo('#TreeGrid');
```

