---
name: syncfusion-angular-treegrid
description: Implements Syncfusion Angular TreeGrid for hierarchical data with sorting, filtering, editing, exporting, paging, virtual scrolling, and advanced features. Supports configuration, CRUD, aggregates, templates, state persistence, and performance optimization in Angular applications.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Grid Components"
---

# Syncfusion Angular TreeGrid

Complete guide to implementing and customizing the Syncfusion Angular TreeGrid component for hierarchical data visualization.

## Table of Contents
- [When to Use This Skill](#when-to-use-this-skill)
- [Data Structure Rules](#data-structure-rules)
- [Documentation Navigation Guide](#documentation-navigation-guide)
- [Quick Start Example](#quick-start-example)
- [Common Patterns](#common-patterns)
- [Best Practices](#best-practices)
- [Key Props Summary](#key-props-summary)
- [Module Injection](#module-injection)

## When to Use This Skill

Use this skill when you need to:
- Display hierarchical or tree-structured data in a grid format
- Implement advanced data manipulation (sorting, filtering, searching, editing)
- Configure pagination, virtual scrolling for large datasets
- Add export functionality (PDF, Excel)
- Customize appearance with themes and CSS
- Handle selection, aggregates, and state management
- Support mobile/responsive design
- Implement row/column freezing

## Mandatory Rules

### Rule 1: childMapping is MANDATORY for Hierarchical Data
**Severity**: 🔴 CRITICAL - Grid will not expand/collapse without this

**Requirement**:
```typescript
// ✅ REQUIRED - Must match data property name exactly
<ejs-treegrid 
  [dataSource]='data'
  childMapping='subtasks'>  // Property name is case-sensitive
</ejs-treegrid>

// ❌ WRONG - Will not work
<ejs-treegrid 
  [dataSource]='data'>
  <!-- No expansion possible without childMapping -->
</ejs-treegrid>
```

**Data Format**:
```typescript
// ✅ CORRECT - childMapping matches 'subtasks' property
public data = [
  {
    TaskID: 1,
    TaskName: 'Parent',
    subtasks: [  // Must match childMapping value
      { TaskID: 2, TaskName: 'Child' }
    ]
  }
];
```

**Exception**: Use `idMapping` + `parentIdMapping` for flat parent-child structure:
```typescript
// Alternative: Flat structure with parent IDs
<ejs-treegrid 
  [dataSource]='flatData'
  idMapping='TaskID'
  parentIdMapping='ParentID'
  hasChildMapping='isParent'>
</ejs-treegrid>
```
---

### Rule 2: Data Type Matching is MANDATORY
**Severity**: 🟠 IMPORTANT - Type mismatches cause rendering/sorting issues

**Requirement**:
```typescript
// ✅ CORRECT - Type matches column definition
public data = [
  {
    TaskID: 1,              // number type
    TaskName: 'Planning',   // string type
    StartDate: new Date(),  // Date object for date columns
  }
];

// Column definition must match data types
<e-columns>
  <e-column field='TaskID' headerText='ID' type='number'></e-column>
  <e-column field='TaskName' headerText='Task' type='text'></e-column>
  <e-column field='StartDate' headerText='Date' type='date' format='yMd'></e-column>
</e-columns>

// ❌ WRONG - Type mismatch
public data = [
  {
    TaskID: '1',            // String instead of number
    StartDate: '02/03/2024' // String instead of Date object
  }
];
```

### Inbuilt properties, events and Methods
📄 **Read:** [references/api-reference.md](references/api-reference.md)
- Complete property reference
- Methods and events documentation
- Column and editing interfaces
- Common data structures

---
 
## Documentation Navigation Guide

### Getting Started & Setup
📄 **Read:** [references/getting-started-guide.md](references/getting-started-guide.md)
- Complete installation and setup
- Module configuration
- Project initialization
- First TreeGrid component

### Data Management
**Data Binding & Adapters**
📄 **Read:** [references/data-binding.md](references/data-binding.md)
- Local and remote data binding
- ORM and custom adaptor implementation
- Loading data from various sources

**Observables Data**
📄 **Read:** [references/observables.md](references/observables.md)
- RxJS observables integration
- Async data binding patterns
- Observable-based event handling
- Async operators and pipelines

**CRUD Operations & Validation**
📄 **Read:** [references/persisting-data-in-server.md](references/persisting-data-in-server.md)
- Server-side data persistence
- CRUD operation management
- Batch operations and transactions
- Offline sync patterns

### Column Configuration

📄 **Read:** [references/column.md](references/column.md)
- Column definition and width management
- Custom column templates and rendering
- Column reordering and freezing

### Column Spanning
📄 **Read:** [references/column-spanning.md](references/column-spanning.md)
- Multi-column spanning configuration
- Cell spanning across columns
- Dynamic span calculation

### Command Columns
📄 **Read:** [references/command-column.md](references/command-column.md)
- Command column with action buttons
- Edit, Delete, and Cancel buttons
- Custom command implementations

### Column Menu
📄 **Read:** [references/column-menu.md](references/column-menu.md)
- Column header context menu
- Sort, group, and filter menu items
- Custom column menu options

### Column Chooser
📄 **Read:** [references/column-chooser.md](references/column-chooser.md)
- Column visibility toggle UI
- Show/hide columns dynamically
- Column chooser dialog configuration

### Row Configuration

📄 **Read:** [references/row.md](references/row.md)
- Row templates and detail rows
- Row drag-drop functionality
- Row spanning and customization

### Cell-Level Features

📄 **Read:** [references/cell.md](references/cell.md)
- Cell styling and formatting
- Cell templates and tooltips
- Custom CSS and HTML content

### Module System & Architecture

📄 **Read:** [references/modules.md](references/modules.md)
- Module imports and dependencies
- Required service providers
- Angular version compatibility
- Library setup and initialization

### Editing

📄 **Read:** [references/editing.md](references/editing.md)
- Cell, inline, dialog, row, and batch editing
- Data validation and error handling
- Custom editors and validation rules

### Sorting

📄 **Read:** [references/sorting.md](references/sorting.md)
- Single and multi-column sorting
- Custom sort comparers
- Sort order and keyboard navigation

### Filtering

📄 **Read:** [references/filtering.md](references/filtering.md)
- Filter bar and menu modes
- Excel-like filtering
- Custom filters and predicates

### Searching

📄 **Read:** [references/searching.md](references/searching.md)
- Global and column-level search
- Case-sensitive searching
- Text highlighting

### Selection

📄 **Read:** [references/selection.md](references/selection.md)
- Row, cell, and checkbox selection modes
- Selection events and APIs
- Programmatic selection

### Paging

📄 **Read:** [references/paging.md](references/paging.md)
- Pagination configuration
- Server-side paging
- Page navigation APIs

### Scrolling

📄 **Read:** [references/scrolling.md](references/scrolling.md)
- Virtual scrolling for large datasets
- Infinite scroll and lazy loading
- Height/width management and scroll positioning

### Frozen Columns

📄 **Read:** [references/frozen-columns.md](references/frozen-columns.md)
- Freeze rows and columns
- Fixed visibility configuration
- Performance optimization

### Aggregations

📄 **Read:** [references/aggregates.md](references/aggregates.md)
- Summary calculations (Sum, Avg, Min, Max, Count)
- Footer templates and child aggregates
- Aggregate events

### Export & Print

📄 **Read:** [references/print.md](references/print.md)
- Print functionality and modes
- Page setup and column visibility
- Custom print templates

📄 **Read:** [references/pdf-export.md](references/pdf-export.md)
- PDF export with styling
- Headers, footers, and watermarks
- Server-side export

📄 **Read:** [references/excel-export.md](references/excel-export.md)
- Excel export configuration
- Cell styling and formatting
- Merged cells and custom data

📄 **Read:** [references/csv-export.md](references/csv-export.md)
- CSV export configuration
- Custom data formatting for export
- Dynamic file naming
- Export events and callbacks
- Selected records export

### User Interface & Interaction

📄 **Read:** [references/toolbar.md](references/toolbar.md)
- Built-in toolbar items
- Custom toolbar items and alignment
- Toolbar event handling

📄 **Read:** [references/clipboard.md](references/clipboard.md)
- Copy/paste operations
- Custom clipboard formats
- Clipboard event handling

📄 **Read:** [references/context-menu.md](references/context-menu.md)
- Context menu configuration
- Built-in and custom menu items
- Menu event handling

### Appearance & Responsiveness

📄 **Read:** [references/adaptive.md](references/adaptive.md)
- Responsive and adaptive design
- Mobile optimization
- Breakpoints and device detection

📄 **Read:** [references/styling.md](references/styling.md)
- Built-in themes (Material, Bootstrap, Fabric, Tailwind)
- CSS customization and overrides
- Row/cell conditional styling

### Performance

📄 **Read:** [references/performance-optimization.md](references/performance-optimization.md)
- Virtual scrolling and lazy loading
- Pagination for large datasets
- Column virtualization and rendering optimization
- Query optimization strategies

### State Management

📄 **Read:** [references/state-persistence.md](references/state-persistence.md)
- Save and restore grid state
- LocalStorage integration
- Custom state management

### Foreign-key
📄 **Read:** [references/foreign-keys.md](references/foreign-keys.md)
- Foreign key column configuration
- Display text mapping for FK values
- Dropdown editors for FK fields
- Cascading foreign key relationships
- Remote data binding for FK data

### Row Drag and Drop

📄 **Read:** [references/row-drag-drop.md](references/row-drag-drop.md)
- Hierarchical drag-and-drop operations
- Parent-child relationship updates
- Circular hierarchy prevention
- Drop event validation and constraints
- Visual feedback during drag operations

### Custom Editors

📄 **Read:** [references/custom-editors.md](references/custom-editors.md)
- Custom editor component creation
- Editor lifecycle management
- Validation in custom editors
- Custom editor templates
- Complex data input patterns

### Validation

📄 **Read:** [references/validation.md](references/validation.md)
- Built-in and custom validation rules
- Async validation against server
- Cross-field validation patterns
- Server-side validation strategies
- Error display and highlighting
- Conditional validation rules

### Globalization

📄 **Read:** [references/globalization.md](references/globalization.md)
- Localization and language support
- RTL (Right-to-Left) support
- Cultural formatting and date/number formats

### Loading Animation

📄 **Read:** [references/loading-animation.md](references/loading-animation.md)
- Loading spinner configuration
- Custom loading templates
- Loading animation customization

### Accessibility & Compliance
📄 **Read:** [references/accessibility.md](references/accessibility.md)
- WCAG 2.1 Level AA conformance
- ARIA labels and attributes
- Keyboard navigation and screen reader support
- Focus management and visual indicators
- Accessibility testing guidance

## Quick Start Example

```typescript
import { Component, ViewChild } from '@angular/core';
import { TreeGridComponent } from '@syncfusion/ej2-angular-treegrid';
import { PageService, SortService, FilterService, EditService } from '@syncfusion/ej2-angular-treegrid';

@Component({
  selector: 'app-treegrid',
  template: `
    <ejs-treegrid 
      #treegrid
      [dataSource]='data'
      [childMapping]='childMapping'
      [allowPaging]='true'
      [allowSorting]='true'
      [allowFiltering]='true'
      <e-columns>
        <e-column field='TaskID' headerText='Task ID' width='90' isPrimaryKey='true'></e-column>
        <e-column field='TaskName' headerText='Task Name' width='200'></e-column>
      </e-columns>
    </ejs-treegrid>
  `,
  providers: [PageService, SortService, FilterService, EditService]
})
export class AppComponent {
  @ViewChild('treegrid') treegrid!: TreeGridComponent;

  public data: Object[] = [
    {
      TaskID: 1,
      TaskName: 'Planning',
      subtasks: [
        { TaskID: 2, TaskName: 'Scope', Duration: 4, Progress: 100 },
        { TaskID: 3, TaskName: 'Budget', Duration: 4, Progress: 100 }
      ]
    }
  ];
  
  public childMapping: string = 'subtasks';
  
  public editSettings = { mode: 'Cell', allowEditing: true, allowDeleting: true, allowAdding: true };
}
```

## Best Practices

1. **Performance Optimization**
   - Use virtual scrolling for large datasets (10,000+ records)
   - Implement server-side operations (sorting, filtering, paging)
   - Use frozen columns sparingly to avoid layout shifts

2. **Data Management**
   - Always provide a primary key (isPrimaryKey='true')
   - Use ChildMapping for hierarchical data
   - Implement proper error handling for API calls

3. **User Experience**
   - Provide loading indicators during data fetch
   - Implement search and filter for data discovery
   - Show validation messages for editing errors
   - Support keyboard navigation and accessibility

4. **Customization**
   - Use themes for consistent styling
   - Create reusable cell templates for common patterns
   - Style conditional rows for user guidance
   - Implement responsive design for mobile devices

5. **State Management**
   - Enable state persistence for user preferences
   - Save sort, filter, and column settings

## Key Props Summary

| Prop | Type | Default | Use Case |
|------|------|---------|----------|
| `dataSource` | DataManager\|Object[] | null | Set grid data source |
| `childMapping` | string | null | Property for child records (must be explicitly set) |
| `allowPaging` | boolean | false | Enable pagination |
| `allowSorting` | boolean | false | Enable sorting |
| `allowFiltering` | boolean | false | Enable filtering |
| `editSettings` | EditSettings | {} | Configure edit mode |
| `enableVirtualization` | boolean | false | Enable virtual scrolling |

## Module Injection

Must inject required services:

```typescript
import { PageService, SortService, FilterService, EditService, ExcelExportService, PdfExportService,
  PrintService, AggregateService, ToolbarService } from '@syncfusion/ej2-angular-treegrid';

@Component({
  providers: [
    PageService, 
    SortService, 
    FilterService, 
    EditService,
    ExcelExportService,
    PdfExportService,
    PrintService,
    AggregateService,
    ToolbarService
  ]
})
```
