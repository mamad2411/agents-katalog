---
name: syncfusion-angular-pivot-table
description: Use this skill when users ask how to build or customize Syncfusion PivotView pivot tables in Angular. Trigger for Angular pivot grid/OLAP, aggregation, data binding (JSON/remote), drill-down/drill-through, grouping, filtering, conditional formatting, exports (Excel/PDF/CSV), or pivot charts. Angular-only, not React/Vue/Blazor.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Grids"
---

# Implementing Angular Pivot Grid

The Syncfusion Angular Pivot Grid is a powerful data visualization and analysis component for creating interactive pivot tables, aggregating multidimensional data, and performing advanced analytics operations.

**Important:** Always verify API class names, properties, and method signatures by consulting the **reference files in this skill** (`references/*.md`). These are maintained with verified, working examples. Do not assume API details from other sources.

## When to Use This Skill

Use this skill when users need to:
- Create and configure pivot tables from multidimensional data
- Bind data from OLAP or relational data sources
- Aggregate data with multiple aggregation functions (Sum, Avg, Count, etc.)
- Group data by number ranges, dates, or custom categories
- Create and manage calculated fields with formulas
- Enable drill-down and drill-through operations
- Visualize data with integrated pivot charts
- Apply custom formatting and conditional styling
- Optimize large dataset performance
- Export pivot grid data to Excel or PDF
- Persist and restore pivot grid state
- Customize UI with field lists, grouping bars, and toolbars

## Documentation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and package setup
- Basic Angular Pivot Grid implementation
- CSS imports and theme configuration
- RTL (Right-to-Left) support
- Component initialization

### Aggregation
📄 **Read:** [references/aggregation.md](references/aggregation.md)
- Aggregation functions: Sum, Avg, Count, Min, Max, Product, Median, DistinctCount
- Advanced aggregations: DifferenceFrom, PercentageOfDifferenceFrom, PercentageOfParentTotal
- Base field configuration with baseField and baseItem properties
- Multiple aggregations on same field
- Customizing aggregation dropdown and UI
- Runtime aggregation type changes
- Events: aggregateCellInfo, actionBegin, actionComplete

### Grouping
📄 **Read:** [references/grouping.md](references/grouping.md)
- Enable grouping with `allowGrouping: true` and inject `GroupingService`
- Number grouping: Configure ranges with rangeInterval, startingAt, endingAt
- Date grouping: Organize by Years, Quarters, Months, Days, Hours, Minutes, Seconds
- Custom grouping: Group data by business-defined categories
- UI-based grouping through context menu
- Ungrouping and programmatic ungrouping
- Common grouping patterns and troubleshooting

### Calculated Fields
📄 **Read:** [references/calculated-field.md](references/calculated-field.md)
- Creating calculated fields interactively and programmatically
- Enabling with `allowCalculatedField: true`, injecting `CalculatedFieldService`
- Defining with `calculatedFieldSettings` (name, formula)
- Adding to values array with `type: 'CalculatedField'`
- Editing/renaming fields through UI (Field List, Grouping Bar)
- Formula syntax: Operators (+, -, *, /, ^, <, >, ==, !=, &, |, ?), Functions (abs, min, max, isNaN, Math.*)
- Aggregation functions in formulas: Sum, Count, Avg, Min, Max
- Formatting with separate `formatSettings` array: Currency (C), Number (N), Percentage (P)
- Events: calculatedFieldCreate (validation), actionBegin/actionComplete (control operations)

### Pivot Chart Integration
📄 **Read:** [references/pivot-chart-integration.md](references/pivot-chart-integration.md)
- Chart types: 21+ types including Line, Column, Area, Bar, Pie, Doughnut, Funnel, Pyramid
- Display options: Configure with `displayOption` to show Grid, Chart, or Both
- Series customization: Customize charts via `chartSeries` with marker, dataLabel, etc.
- Drill operations: Enable drill-down/drill-up on accumulation charts
- Multiple axes: Configure `enableMultipleAxis` for multi-value visualization
- Chart events: Series creation, axis customization, legend customization

### Filtering & Sorting
📄 **Read:** [references/filtering-and-sorting.md](references/filtering-and-sorting.md)
- Label filtering: Filter by field names and member values
- Value filtering: Filter rows/columns by aggregated values
- Member filtering: UI-based filtering through Field List
- Member search: Quick search in filter dialogs
- Sort settings: Configure ascending/descending sort by field
- Advanced sorting: Sort by aggregated values or custom order

### Data Formatting & Conditional Formatting
📄 **Read:** [references/data-formatting.md](references/data-formatting.md)
- Number formats: Currency (C), Percentage (P), Number (N), Scientific (E)
- Custom formats: Define format strings with placeholders
- Conditional formatting: Apply colors/styles based on cell values
- Icon sets: Display icons based on thresholds
- Data bars: Show bar visualization within cells
- Format settings configuration

### Export & Printing
📄 **Read:** [references/export-and-print.md](references/export-and-print.md)
- Excel export: `excelExport()` with custom properties, themes
- PDF export: `pdfExport()` with headers, footers, page orientation
- CSV export: `csvExport()` for large datasets (1M+ rows)
- Print functionality: `print()` method for table and chart
- Multi-table export: Combine multiple pivot tables in single file
- Export customization: Cell styling, color themes, branding

### UI Customization
📄 **Read:** [references/ui-customization.md](references/ui-customization.md)
- Toolbar configuration: Show/hide built-in toolbar items
- Report management: New, Save, Load, Delete reports
- View switching: Toggle between Grid and Chart modes
- Export options: Quick export buttons
- Grand totals/Subtotals: Show/hide and customize positioning
- Custom templates: Build custom toolbar or field list

### Grouping Bar UI Operations
📄 **Read:** [references/grouping-bar-ui-operations.md](references/grouping-bar-ui-operations.md)
- Grouping bar setup and configuration
- Drag-and-drop field reorganization between axes
- Filter, sort, and remove operations
- Fields panel management and visibility control
- Icon controls: filter, sort, remove buttons
- Field-specific vs global icon configuration
- Responsive grouping bar for different screen sizes

### Tooltips Customization
📄 **Read:** [references/tooltips-customization.md](references/tooltips-customization.md)
- Enable/disable tooltips with `showTooltip` property
- Custom tooltip templates with dynamic placeholders
- Available placeholders: `${rowHeaders}`, `${columnHeaders}`, `${value}`, etc.
- Pivot chart tooltip customization
- CSS styling for tooltip appearance
- Dynamic tooltip content based on cell values
- Troubleshooting tooltip rendering issues

### Editing & Drill Operations
📄 **Read:** [references/editing-drill-operations.md](references/editing-drill-operations.md)
- Enable cell editing with `allowEditing: true` (relational data only)
- Edit settings: `allowAdding`, `allowDeleting`, `allowCommandColumns`
- Four editing modes: Normal, Dialog, Batch, Command Column
- Inline editing for quick updates
- Edit events: `editCompleted`, `actionBegin`, `actionComplete`, `actionFailure`
- Custom validation and confirmation dialogs
- Editing via pivot chart data points
- CRUD operations and data persistence
- Drill through and drill down operations
- Cell drill-down events and customization

### OLAP Data Sources
📄 **Read:** [references/olap-data-sources.md](references/olap-data-sources.md)
- OLAP vs relational data source differences
- Connection configuration: `url`, `catalog`, `cube`, `providerType`
- OLAP cube elements: Measures, Dimensions, Hierarchies, Named Sets
- Authentication and role-based access control
- Working with hierarchies and attribute hierarchies
- Calculated fields (Calculated Measures and Dimensions) for OLAP
- Advanced features: Virtual scrolling, drill-down, filter axis
- MDX formula support and expression syntax

### Paging Configuration
📄 **Read:** [references/paging-configuration.md](references/paging-configuration.md)
- Enable paging with `enablePaging: true` and inject `PagerService`
- Page settings: `rowPageSize`, `columnPageSize`, `currentRowPage`, `currentColumnPage`
- Pager UI configuration and positioning (Top/Bottom)
- Row vs column paging
- Compact view and inverse pager layout
- Custom page size options in dropdown
- Paging with virtual scrolling for optimization
- Server-side paging for huge datasets
- Mobile-optimized paging

### Virtual Scrolling
📄 **Read:** [references/virtual-scrolling.md](references/virtual-scrolling.md)
- Enable virtual scrolling with `enableVirtualization: true` for large datasets
- Single page mode: Use `allowSinglePage: true` to render only current view page
- Limitations: pixel-based columnWidth, avoid runtime sizing changes
- Static FieldList synchronization using `enginePopulated` events and `update`/`updateView` methods
- Performance optimization for 100K+ rows on client-side

### Drill-Down & Drill-Through Operations
📄 **Read:** [references/drill-down.md](references/drill-down.md)
- Drill-down: Navigate hierarchical data by clicking cells
- Drill-up: Navigate back to higher levels
- Drill-through: View raw underlying data for aggregated values
- Events: `cellClick`, `fieldDrop`, `fieldsUpdated` for drill interactions
- Context menu: Built-in drill operations

### Database Connections
📄 **Read:** [references/database-connections.md](references/database-connections.md)
- Relational databases: SQL Server, MySQL, PostgreSQL, Oracle
- NoSQL databases: MongoDB support
- Big data: Elasticsearch integration
- Connection strings: Configure data source connections
- Query optimization: Pre-aggregation and filtering

### Server-Side Pivot Engine
📄 **Read:** [references/server-side-pivot-engine.md](references/server-side-pivot-engine.md)
- Server-side processing: Delegate aggregation to backend server
- ASP.NET Core setup: Download and configure PivotController application
- Angular client configuration: Set mode: 'Server' with server endpoint URL
- Data sources: Collection, JSON, CSV, DataTable, Dynamic objects
- Virtual scrolling: Handle 100K+ rows efficiently
- Excel/CSV export: Export processed data to files
- Security: Add authentication headers with beforeServiceInvoke event

### Performance Optimization
📄 **Read:** [references/performance-optimization.md](references/performance-optimization.md)
- Virtual scrolling: Enable with `enableVirtualization: true` for 100K+ rows
- Single page mode: Use `allowSinglePage: true` for better performance
- Paging: Configure with `pageSettings` for row/column pagination
- Data compression: Enable `allowDataCompression: true` for duplicate record summarization
- Deferred updates: Use `allowDeferLayoutUpdate: true` to batch field operations
- Large dataset handling: Server-side processing with `mode: 'Server'`
- Best practices: Pre-filtering, optimized sorting, member filtering limits, avoiding built-in grouping

### State Persistence & Hyperlinks
📄 **Read:** [references/state-persistence-hyperlinks.md](references/state-persistence-hyperlinks.md)
- State persistence: Save and restore pivot configuration
- Local storage: Store report state in browser
- Report export/import: JSON format serialization
- Hyperlinks: Enable clickable hyperlinks in cells
- Hyperlink events: Respond to hyperlink clicks
- Hyperlink customization: Set targets and formatting

---

## Quick Start Example

```typescript
import { PivotViewAllModule, PivotChartService } from '@syncfusion/ej2-angular-pivotview';
import { Component, OnInit, ViewChild } from '@angular/core';
import { PivotViewComponent, IDataSet } from '@syncfusion/ej2-angular-pivotview';

@Component({
  imports: [PivotViewAllModule],
  providers: [PivotChartService],
  standalone: true,
  selector: 'app-pivot-grid',
  template: `
    <ejs-pivotview #pivotview id='PivotView' 
      [dataSourceSettings]=dataSourceSettings
      [height]="'500px'"
      [width]="'100%'"
      [allowCalculatedField]="true" 
      [allowGrouping]="true"
      [allowConditionalFormatting]="true"
      [displayOption]="displayOption"
      [toolbar]="toolbarItems">
    </ejs-pivotview>
  `
})
export class AppComponent implements OnInit {
    @ViewChild('pivotview') pivotViewComponent!: PivotViewComponent;
    
    public pivotData!: IDataSet[];
    public dataSourceSettings: any;
    public displayOption: any;
    public toolbarItems: string[] = ['New', 'Save', 'SaveAs', 'Rename', 'Remove', 'Load',
                                      'Grid', 'Chart', 'Export', 'SubTotal', 'GrandTotal'];

    ngOnInit(): void {
        this.pivotData = [
            { 'Sold': 31, 'Amount': 52824, 'Country': 'France', 'Products': 'Mountain Bikes', 'Year': 'FY 2015', 'Quarter': 'Q1' },
            { 'Sold': 51, 'Amount': 86904, 'Country': 'France', 'Products': 'Mountain Bikes', 'Year': 'FY 2015', 'Quarter': 'Q2' },
            { 'Sold': 90, 'Amount': 153360, 'Country': 'France', 'Products': 'Mountain Bikes', 'Year': 'FY 2015', 'Quarter': 'Q3' },
            { 'Sold': 25, 'Amount': 42500, 'Country': 'France', 'Products': 'Road Bikes', 'Year': 'FY 2015', 'Quarter': 'Q1' },
            { 'Sold': 40, 'Amount': 68000, 'Country': 'Germany', 'Products': 'Mountain Bikes', 'Year': 'FY 2015', 'Quarter': 'Q2' }
        ];

        // Display both grid and chart with grid as primary view
        this.displayOption = { view: 'Both', primary: 'Table' };

        this.dataSourceSettings = {
            dataSource: this.pivotData,
            expandAll: false,
            rows: [{ name: 'Country' }, { name: 'Products' }],
            columns: [{ name: 'Year' }, { name: 'Quarter' }],
            values: [
                { name: 'AvgAmount', type: 'CalculatedField' },
                { name: 'Sold', type: 'Count' }
            ],
            calculatedFieldSettings: [
                {
                    name: 'AvgAmount',
                    formula: '"Sum(Amount)"/"Count(Sold)"'  // Calculated field: Average
                }
            ],
            formatSettings: [
                { name: 'Amount', format: 'C2' },             // Currency format
                { name: 'AvgAmount', format: 'C2' }           // Format calculated field
            ],
            conditionalFormatSettings: [
                {
                    measure: 'Amount',
                    value1: 50000,
                    value2: 100000,
                    condition: 'Between',
                    style: { backgroundColor: '#FFE5CC', color: 'black' }
                }
            ]
        };
    }
}
```

---

## Common Patterns

### Pattern 1: Multiple Fields with Different Aggregation Types
Each field supports only ONE aggregation type. To analyze different aspects, use different fields with their respective aggregation functions:
```typescript
values: [
    { name: 'Amount', type: 'Sum' },      // Total sales amount
    { name: 'Quantity', type: 'Avg' },    // Average quantity sold
    { name: 'Sold', type: 'Count' },      // Number of transactions
    { name: 'Price', type: 'Min' },       // Minimum price
]
```
**Note:** Each field in the values array can only have ONE type. To get multiple aggregation types for analysis, use different fields or create calculated fields combining aggregations.

### Pattern 2: Hierarchical Grouping
Organize data with multi-level grouping:
```typescript
rows: [
    { name: 'Country' },    // Primary level
    { name: 'Region' },     // Secondary level
    { name: 'City' }        // Tertiary level
],
columns: [
    { name: 'Year' },       // Year level
    { name: 'Quarter' }     // Quarter level
]
```

### Pattern 4: Number Range Grouping
Group numeric fields into ranges:
```typescript
groupSettings: [
    {
        name: 'ProductID',
        type: 'Number',
        rangeInterval: 5,
        startingAt: 1000,
        endingAt: 1010
    }
]
```

### Pattern 5: Date Hierarchy Grouping
Organize dates with time-based hierarchies:
```typescript
groupSettings: [
    {
        name: 'OrderDate',
        type: 'Date',
        groupInterval: ['Years', 'Months'],  // Year then month hierarchy
        startingAt: new Date(2020, 0, 1),
        endingAt: new Date(2023, 11, 31)
    }
]
```

---

## Key Configuration Properties

| Property | Type | Purpose |
|----------|------|---------|
| `values` | Array | Fields to aggregate with type (Sum, Avg, Count, CalculatedField, etc.) |
| `type` | String | Aggregation type for value field (Sum, Avg, Count, Min, Max, etc.) or 'CalculatedField' for calculated fields |
| `baseField` | String | Field reference for DifferenceFrom/Percentage comparisons |
| `baseItem` | String | Specific member for base field comparisons |
| `allowCalculatedField` | Boolean | Enable calculated field feature |
| `calculatedFieldSettings` | Array | Define calculated field name and formula |
| `formula` | String | Mathematical expression for calculated field using aggregation functions |
| `formatSettings` | Array | SEPARATE array for number formatting (N, C, P) of values and calculated fields |
| `allowGrouping` | Boolean | Enable grouping feature |
| `groupSettings` | Array | Configure number, date, or custom grouping |
| `groupInterval` | Array | Grouping hierarchy (Years, Months, Days, etc.) |
| `aggregateTypes` | Array | Show specific aggregation types in UI dropdown |
| `showAggregationOnValueField` | Boolean | Display aggregation type in button text |

**Important**: When adding calculated fields to values, use `type: 'CalculatedField'` to distinguish them from regular aggregations.

---

## Next Steps

**Foundation (Start here):**
1. Read **Getting Started** for setup and initialization
2. Read **Aggregation** to implement aggregation functions and base field aggregations
3. Read **Grouping** to configure number, date, and custom grouping

**Data Manipulation:**
4. Read **Calculated Fields** for complex calculations and custom field formulas
5. Read **Filtering & Sorting** for label/value filtering and custom sorting
6. Read **Data Formatting** for number formats and conditional formatting

**Visualization & Interaction:**
7. Read **Pivot Chart Integration** for charting and drill operations
8. Read **UI Customization** for toolbars and custom interfaces
9. Read **Drill-Down & Drill-Through** for hierarchical data exploration

**Advanced Features:**
10. Read **Export & Printing** for multi-format export (Excel, PDF, CSV)
11. Read **State Persistence** for saving and restoring configurations
12. Read **Database Connections** for SQL/NoSQL/big data integration
13. Read **Server-Side Pivot Engine** for processing 100K+ rows on backend
14. Read **Performance Optimization** for large datasets, deferred updates, and virtual scrolling

---

## Foundational References

These files provide foundational knowledge and may be referenced by feature guides:

📄 **[references/core-concepts.md](references/core-concepts.md)** - Data binding types (JSON, CSV, OLAP), client-side vs server-side comparison, choosing appropriate data sources

📄 **[references/layout-and-columns.md](references/layout-and-columns.md)** - Classic layout, row/column sizing, column features, cell selection and customization

📄 **[references/field-list.md](references/field-list.md)** - Field list UI (popup/fixed modes), field organization, deferred updates patterns
