---
name: syncfusion-angular-gantt-chart
description: Implement and configure the Syncfusion Angular Gantt Chart component (ejs-gantt, GanttModule). Use this when building Angular applications with Gantt chart functionality, task scheduling, dependencies, or resource management. Covers component setup, task dependencies, taskbar editing, critical path analysis, resource allocation, timeline configuration, filtering, sorting, export, undo/redo, state persistence, and localization.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Syncfusion Angular Gantt Chart

A comprehensive skill for implementing and configuring the Syncfusion Angular Gantt Chart component (`ejs-gantt`). This covers everything from initial setup through advanced features like critical path, virtual scrolling, resource views, undo/redo, state persistence, localization, and export.

## When to Use This Skill

Use this skill when you need to:
- Install and set up the Angular Gantt Chart component
- Bind local or remote data to the Gantt chart
- Configure task scheduling modes (Auto/Manual/Custom)
- Define task dependencies and predecessor relationships
- Add, edit, or delete tasks (cell, dialog, taskbar editing)
- Assign and manage resources
- Configure timelines, zooming, and tier formats
- Customize taskbars, labels, and data markers
- Filter, sort, search, or select rows/cells
- Enable toolbar, context menu, or undo/redo
- Export to Excel or PDF
- Implement virtual scrolling or state persistence
- Apply localization, RTL layout, or timezone configuration
- Work with holidays, event markers, critical path, or baseline

---

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation via `ng add @syncfusion/ej2-angular-gantt`
- CSS imports for all themes (material3, bootstrap5, fluent2, tailwind3)
- Setting up Angular standalone component with `imports` and `providers`
- Binding data with `dataSource` and `taskFields` — self-referential vs hierarchical
- Injecting feature services (EditService, FilterService, ToolbarService, etc.)
- Configuring timeline, toolbar, editing, filtering, sorting
- `gridLines` values: `'Both'` | `'Horizontal'` | `'Vertical'` | `'None'`
- `actionFailure` error handling for common configuration mistakes

### Data Binding
📄 **Read:** [references/data-binding.md](references/data-binding.md)
- **Default pattern:** Self-referential flat array with `id` + `parentID` (idMapping + parentIdMapping) — use this unless user explicitly asks for nested data
- Hierarchical local data with `child` array — only when user explicitly requests nested/tree structure
- Decision table: when to use self-referential vs hierarchical
- Remote data binding with `DataManager` and adaptors (ODataV4, WebApiAdaptor, UrlAdaptor)
- Load-on-demand (virtual loading) with `loadChildOnDemand` and `hasChildMapping`
- Observable / RxJS data binding with `async` pipe
- Remote CRUD with `crudUrl`, `insertUrl`, `updateUrl`, `removeUrl`, `batchUrl`
- Common gotchas table (missing `isPrimaryKey`, wrong adaptor, parent date issues)

### Task Scheduling
📄 **Read:** [references/task-scheduling.md](references/task-scheduling.md)
- `taskMode`: `'Auto'` (default), `'Manual'`, `'Custom'` (per-task via boolean field)
- Auto mode: dates calculated from dependencies, working time, and holidays
- Manual mode: all dates fixed as-is in data source; use `validateManualTasksOnLinking` to still adjust on link
- Custom mode: per-task scheduling via mapped boolean field in data source
- Unscheduled tasks (`allowUnscheduledTasks`) — partial dates, floating bars
- `durationUnit`: `'Day'` | `'Hour'` | `'Minute'`
- **Working days:** `workWeek` array (default Mon–Fri); `includeWeekend: true` makes all 7 days working
- **Working hours:** `dayWorkingTime` — array of `{ from, to }` ranges (default 8–17); affects hour-based durations
- Baseline dates (`renderBaseline`, `baselineStartDate`, `baselineEndDate`, `baselineColor`)
- Work scheduling (effort-driven) with `work` field and `workUnit`

### Task Dependencies
📄 **Read:** [references/task-dependencies.md](references/task-dependencies.md)
- Dependency types: `FS` (Finish-to-Start), `SS`, `FF`, `SF` — format: `'2FS'`, `'3SS+1d'`
- Comma-separated multiple predecessors: `'2FS,3SS'`
- Predecessor lag/lead offsets with `d`/`h`/`m` units
- `autoUpdatePredecessorOffset` — sync offset values with actual positions on load
- `allowParentDependency` — enable parent-child and cross-hierarchy dependencies
- Editing via connector line drag when `editSettings.allowTaskbarEditing: true`
- `actionBegin` `requestType: 'validateLinkedTask'` — handle dependency conflicts
- Programmatic: `addPredecessor()`, `removePredecessor()`, `updateRecordById()`
- `connectorLineWidth` and `connectorLineBackground` for connector styling

### Task Constraints
📄 **Read:** [references/task-constraints.md](references/task-constraints.md)
- 8 constraint types: ASAP (0), ALAP (1), MSO (2), MFO (3), SNET (4), SNLT (5), FNET (6), FNLT (7)
- Map via `taskFields.constraintType` (numeric) and `taskFields.constraintDate` (Date)
- Constraints enforced only in Auto mode; stored-but-passive in Manual mode
- Conflicts with dependencies surface in `actionBegin` event

### Managing Tasks
📄 **Read:** [references/managing-tasks.md](references/managing-tasks.md)
- `editSettings`: `allowEditing`, `allowAdding`, `allowDeleting`, `allowTaskbarEditing`, `mode` (`'Auto'` | `'Dialog'`)
- Cell editing with `editType` per column: `'numericedit'`, `'defaultedit'`, `'dropdownedit'`, `'booleanedit'`, `'datepickeredit'`
- Dialog editing with custom tab configuration (`addDialogFields`, `editDialogFields`)
- Programmatic: `addRecord()`, `updateRecordById()`, `deleteRecord()`, `openAddDialog()`, `openEditDialog(id)`
- Expand/collapse: `expandAll()`, `collapseAll()`, `expandByID(id)`, `collapseByID(id)`; events: `expanding`, `expanded`, `collapsing`, `collapsed`
- Validation via `actionBegin` event (`args.cancel = true` to block)
- Server CRUD via `actionComplete` + `requestType` inspection
- Indent / outdent hierarchy changes via toolbar or `indent()` / `outdent()` methods

### Splitting and Merging Tasks
📄 **Read:** [references/splitting-and-merging.md](references/splitting-and-merging.md)
- `taskFields.segments` for hierarchical data; `taskFields.segmentId` for self-referential data
- Split at load time or dynamically via dialog Segments tab or context menu `SplitTask`
- Merge via context menu `MergeTask` or by dragging segments together
- `onTaskbarClick` with `segmentIndex` to detect which segment was clicked
- Limitations: no splits on parent/milestone tasks; incompatible with multi-taskbar resource view

### Resources
📄 **Read:** [references/resources.md](references/resources.md)
- `resources` (data) + `resourceFields` (field mapping: `id`, `name`, `unit`, `group`)
- `taskFields.resourceInfo` to link resources to tasks
- Resource view mode (`viewType: 'ResourceView'`) with row-per-resource display
- `showOverAllocationAsMultiTaskbar` — stacked taskbars for over-allocated resources
- Work-based scheduling: `work` field, `taskType` (`'FixedWork'`, `'FixedDuration'`, `'FixedUnit'`)
- Work unit: `workUnit: 'Hour'` | `'Day'` | `'Minute'`

### Columns
📄 **Read:** [references/columns.md](references/columns.md)
- Column `field`, `headerText`, `width`, `format`, `type`, `template`, `headerTemplate`
- Column reordering (`allowReordering`), resizing (`allowResizing`)
- Frozen columns (`freeze: 'Left'` | `'Right'`) — requires `FreezeService`
- Column spanning via `queryCellInfo`
- `treeColumnIndex` for tree expand/collapse column
- WBS (Work Breakdown Structure) column with `columnType: 'WBS'`
- Column menu (`showColumnMenu`) — sort, filter, auto-fit, column chooser
- `isPrimaryKey` requirement for CRUD operations

### Timeline
📄 **Read:** [references/timeline.md](references/timeline.md)
- `timelineSettings` configuration
- Top tier and bottom tier customization
- Timeline view modes (day/week/month/year)
- Formatter function with `(date, format, tier, mode)` parameters
- Timeline cell width (`timelineUnitSize`)
- Custom date formats
- `projectStartDate` and `projectEndDate`
- Timeline view window (`viewStartDate` / `viewEndDate`)
- Week start day (`weekStartDay`)
- Automatic timescale update (`updateTimescaleView`)
- Weekend highlighting (`timelineSettings.showWeekend`)
- Timeline cells tooltip (`showTooltip`)
- Navigate timeline (`previousTimeSpan()` / `nextTimeSpan()`)
- Zooming in and out

### Taskbar
📄 **Read:** [references/taskbar.md](references/taskbar.md)
- `taskbarTemplate`, `parentTaskbarTemplate`, `milestoneTemplate` — full custom templates
- `labelSettings`: `leftLabel`, `rightLabel`, `taskLabel` (field names or templates)
- `queryTaskbarInfo` — dynamic styling: `taskbarBgColor`, `progressBarBgColor`, `taskbarBorderColor`
- `indicators` / data markers on individual tasks: `date`, `iconClass`, `label`, `tooltip`
- Tooltip customization via `tooltipSettings.taskbar` template
- `taskbarHeight`, `taskbarCornerRadius`, `allowTaskbarDragAndDrop`

### Filtering and Searching
📄 **Read:** [references/filtering-and-searching.md](references/filtering-and-searching.md)
- `allowFiltering: true` + `FilterService` — menu and Excel filter types
- `filterSettings.type`: `'Menu'` (default) | `'Excel'`
- `filterSettings.hierarchyMode`: `'Parent'` | `'Child'` | `'Both'` | `'None'`
- Initial filter on load via `filterSettings.columns` array
- Searching: `allowSearching: true` + `'Search'` in toolbar
- `searchSettings`: `fields`, `operator`, `ignoreCase`
- Programmatic: `filterByColumn()`, `clearFiltering()`, `search()`

### Sorting
📄 **Read:** [references/sorting.md](references/sorting.md)
- `allowSorting: true` + `SortService` — click column headers to sort
- Disable per column: `{ field: 'TaskID', allowSorting: false }`
- Multi-column sort: Ctrl+click additional headers; Shift+click to remove
- Initial sort on load via `sortSettings.columns` array
- Programmatic: `sortColumn()`, `removeSortColumn()`, `clearSorting()`

### Rows
📄 **Read:** [references/rows.md](references/rows.md)
- `rowDataBound` / `queryCellInfo` — dynamic row/cell styling
- `rowHeight` — uniform row height in pixels (must exceed `taskbarHeight`)
- `enableAltRow` — alternate row background (default `true`)
- `rowTemplate` — fully custom row layout in TreeGrid pane
- `queryRowInfo` with `rowSpan` — vertical cell spanning
- `allowRowDragAndDrop` — drag rows to reorder/reparent; `rowDragStartHelper` / `rowDrop` events

### Selection
📄 **Read:** [references/selection.md](references/selection.md)
- `allowSelection: true` + `SelectionService` — required for any selection feature
- `selectionSettings.mode`: `'Row'` (default) | `'Cell'` | `'Both'`
- `selectionSettings.type`: `'Single'` (default) | `'Multiple'` (Ctrl+click for multi-select)
- `selectionSettings.enableToggle` — click to deselect already-selected row
- Cell selection modes: `'Flow'` | `'Box'` | `'BoxWithBorder'`
- Programmatic: `selectRow()`, `selectRows()`, `selectCell()`, `clearSelection()`, `getSelectedRecords()`

### Scrolling
📄 **Read:** [references/scrolling.md](references/scrolling.md)
- `enableVirtualization: true` + `VirtualScrollService` — DOM virtualization for large datasets
- `enableTimelineVirtualization` — virtualize timeline columns independently
- Splitter: `splitterSettings.position` (percentage string or pixel value), `columnIndex`, `view` (`'Default'` | `'Grid'` | `'Chart'`)
- Programmatic: `scrollToDate('04/02/2024')`, `scrollToTaskbar(taskId)`
- Virtual scroll limitations: row/column templates, grouping, and some aggregate features not supported

### Toolbar
📄 **Read:** [references/toolbar.md](references/toolbar.md)
- `ToolbarService` required; set `toolbar` as string array or mixed `ItemModel` array
- Built-in items: `'Add'`, `'Edit'`, `'Delete'`, `'Update'`, `'Cancel'`, `'ExpandAll'`, `'CollapseAll'`, `'Search'`, `'Indent'`, `'Outdent'`, `'ZoomIn'`, `'ZoomOut'`, `'ZoomToFit'`, `'ExcelExport'`, `'CsvExport'`, `'PdfExport'`, `'CriticalPath'`, `'Undo'`, `'Redo'`, `'SplitTask'`, `'MergeTask'`, `'ColumnChooser'`
- Custom items via `ItemModel`: `text`, `id`, `prefixIcon`, `align`, `tooltipText`
- `{ type: 'Separator' }` for visual dividers
- `toolbarClick` event — use `args.item.id` to identify clicked item (format: `'{ganttId}_{itemId}'`)
- Enable/disable programmatically: `enableToolbarItems()` / `disableToolbarItems()`

### Programmatic Methods
📄 **Read:** [references/gantt-methods.md](references/gantt-methods.md)
- Column utilities: `autoFitColumns()`
- Edit control: `cancelEdit()`, `openAddDialog()`, `openEditDialog()`
- Task management: `deleteRecord()`, `convertToMilestone()`, `changeTaskMode()`, `updateRecordByID()`, `updateRecordByIndex()`, `updateTaskId()`, `updateDataSource()`, `updateProjectDates()`
- Toolbar control: `enableItems()`
- Expand/Collapse: `expandByIndex()`, `collapseByIndex()`
- Undo/Redo stacks: `clearUndoCollection()`, `clearRedoCollection()`, `getUndoActions()`, `getRedoActions()`
- Data retrieval: `getCurrentViewData()`, `getRecordByID()`, `getTaskByUniqueID()`, `getTaskInfo()`, `getTaskbarHeight()`, `getExpandedRecords()`, `getGanttColumns()`, `getGridColumns()`
- Formatting helpers: `getDurationString()`, `getWorkString()`
- DOM access: `getRowByID()`, `getRowByIndex()`
- Sorting: `removeSortColumn()`
- Selection: `selectCells()`
- Row reorder: `reorderRows()`
- Scrolling: `scrollToTask()`, `updateChartScrollOffset()`

### Events
📄 **Read:** [references/events.md](references/events.md)
- Lifecycle: `load`, `created`, `dataBound`, `destroyed`
- Edit lifecycle: `actionBegin` (cancel with `args.cancel = true`), `actionComplete`, `actionFailure`
- Taskbar: `taskbarEditing`, `taskbarEdited`, `onTaskbarClick`, `queryTaskbarInfo`
- Row/cell: `rowDataBound`, `queryCellInfo`, `queryRowInfo`, `rowSelected`, `rowDeselected`, `cellSelected`
- Expand/collapse: `expanding`, `expanded`, `collapsing`, `collapsed`
- Export: `beforeExcelExport`, `excelExportComplete`, `beforePdfExport`, `pdfExportComplete`, `pdfQueryTaskbarInfo`
- `recordDoubleClick` — open custom edit on double click

### Context Menu
📄 **Read:** [references/context-menu.md](references/context-menu.md)
- `enableContextMenu: true` + `ContextMenuService` — right-click on rows or header
- Default items include: `'AutoFitAll'`, `'AutoFit'`, `'SortAscending'`, `'SortDescending'`, `'Add'`, `'Edit'`, `'Delete'`, `'Save'`, `'Cancel'`, `'Indent'`, `'Outdent'`, `'TaskInformation'`, `'SplitTask'`, `'MergeTask'`
- Custom items via `ContextMenuItemModel`: `text`, `id`, `iconCss`, `target` (row/header)
- `contextMenuOpen` — dynamically hide/show items per row
- `contextMenuClick` — handle item selection

### Holidays and Event Markers
📄 **Read:** [references/holidays-and-markers.md](references/holidays-and-markers.md)
- `DayMarkersService` required for both holidays and event markers
- `holidays`: array of `{ from, to?, label, cssClass }` — non-working days that extend task durations
- `eventMarkers`: array of `{ day, label, cssClass, top? }` — full-height vertical lines at specific dates
- Custom styling per type via `cssClass` + CSS targeting `.e-gantt-event-marker` / `.e-span-label`
- `top` property staggers overlapping markers at the same date

### Critical Path
📄 **Read:** [references/critical-path.md](references/critical-path.md)
- `enableCriticalPath: true` + `CriticalPathService` — highlights zero/negative-slack tasks in red
- `'CriticalPath'` toolbar item — user toggle button
- `getCriticalTasks()` — returns array of `IGanttData` objects with `slack` value
- `queryTaskbarInfo` + `ganttProperties.isCritical` — conditional per-task coloring
- CSS overrides: `.e-critical-path-container`, `.e-critical-connector-line`
- Rules: completed tasks (100%) excluded; parent/child criticality independent; auto-recalculates on any change

### Export (Excel and PDF)
📄 **Read:** [references/export.md](references/export.md)
- Excel: `allowExcelExport: true` + `ExcelExportService`; call `excelExport()` / `csvExport()`
- PDF: `allowPdfExport: true` + `PdfExportService`; call `pdfExport()`
- `ExcelExportProperties`: `fileName`, `dataSource`, `includeHiddenColumn`, `header`, `footer`
- `PdfExportProperties`: `fileName`, `pageOrientation`, `pageSize`, `fitToWidthSettings`, `ganttStyle`, `theme`
- PDF header/footer content types: `Text`, `Line`, `PageNumber`, `Image`
- Single-page export: `fitToWidthSettings.isFitToWidth: true`
- Blob export: `pdfExport({}, true)` → blob available in `pdfExportComplete` event
- Multi-Gantt export to one PDF via chained `pdfExport()` with `multipleExport`
- `pdfQueryTaskbarInfo` — per-taskbar colors in PDF output

### Undo / Redo
📄 **Read:** [references/undo-redo.md](references/undo-redo.md)
- `enableUndoRedo: true` + `UndoRedoService` — up to 10 steps by default
- `undoRedoActions` array — choose which action types are tracked (18 supported actions)
- `undoRedoStepsCount` — configure history depth
- Keyboard: `Ctrl+Z` / `Ctrl+Y`; programmatic: `undo()` / `redo()`
- `'Undo'` / `'Redo'` toolbar items auto-disable when history is exhausted

### State Persistence
📄 **Read:** [references/state-persistence.md](references/state-persistence.md)
- `enablePersistence: true` — saves filter/sort/column state to `localStorage` under key `'{id}gantt'`
- Requires unique `id` on `<ejs-gantt>` element
- Reset methods: `clearStorage()`, remove localStorage key manually, or set new `id`
- Immutable mode (`enableImmutableMode`) — only re-renders changed rows for large-dataset performance
- Loading animation: `loadingIndicator.indicatorType` — `'Spinner'` (default) | `'Shimmer'`
- Manual spinner: `showSpinner()` / `hideSpinner()`

### Localization, RTL and Formatting
📄 **Read:** [references/localization-rtl.md](references/localization-rtl.md)
- `locale` property + `setCulture()` + `L10n.load()` — translate all Gantt UI strings
- Full locale key reference for the `'gantt'` namespace
- RTL: `[enableRtl]="true"` + `locale="ar"` — reverses layout direction
- `timezone` — IANA timezone string (e.g. `'America/New_York'`, `'UTC'`) for consistent cross-region dates
- Column date formatting: `format` string or `{ type: 'date', skeleton: 'yMd' }`
- Column number formatting: `'N2'`, `'C2'`, `'P1'` etc.

---

## Quick Start Example

```typescript
import { Component } from '@angular/core';
import { GanttModule, EditService, SortService, FilterService, ToolbarService, SelectionService } from '@syncfusion/ej2-angular-gantt';

@Component({
  imports: [GanttModule],
  standalone: true,
  providers: [EditService, SortService, FilterService, ToolbarService, SelectionService],
  selector: 'app-root',
  template: `
    <ejs-gantt
      [dataSource]="data"
      [taskFields]="taskFields"
      [height]="'450px'"
      [toolbar]="toolbar"
      [allowFiltering]="true"
      [allowSorting]="true"
      [editSettings]="editSettings">
    </ejs-gantt>
  `
})
export class AppComponent {
  // Default: self-referential data (flat array with id + parentID)
  // Use hierarchical (child array) only if user explicitly requests it
  public data: object[] = [
    { TaskID: 1, TaskName: 'Project Initiation',    StartDate: new Date('04/02/2024'), Duration: 5,  Progress: 0,  ParentID: null },
    { TaskID: 2, TaskName: 'Identify Site location', StartDate: new Date('04/02/2024'), Duration: 4, Progress: 50, ParentID: 1 },
    { TaskID: 3, TaskName: 'Perform Soil test',      StartDate: new Date('04/02/2024'), Duration: 4, Progress: 50, ParentID: 1 },
    { TaskID: 4, TaskName: 'Soil test approval',     StartDate: new Date('04/02/2024'), Duration: 4, Progress: 50, ParentID: 1, Predecessor: '3FS' }
  ];
  public taskFields: object = {
    id: 'TaskID',         // idMapping
    name: 'TaskName',
    startDate: 'StartDate',
    duration: 'Duration',
    progress: 'Progress',
    dependency: 'Predecessor',
    parentID: 'ParentID'  // parentIdMapping — null = root task
  };
  public toolbar: string[] = ['Add', 'Edit', 'Delete', 'ExpandAll', 'CollapseAll', 'Search'];
  public editSettings: object = { allowEditing: true, allowAdding: true, allowDeleting: true, allowTaskbarEditing: true };
}
```

---

## Common Patterns

### When user needs task editing
→ Set `editSettings.allowEditing: true`, inject `EditService`
→ Use `mode: 'Auto'` for cell editing, `mode: 'Dialog'` for dialog

### When user needs large dataset performance
→ Read `references/scrolling.md` — enable `enableVirtualization: true` + `VirtualScrollService`

### When user needs to export data
→ Read `references/export.md` — inject `ExcelExportService` or `PdfExportService`

### When user needs resource management
→ Read `references/resources.md` — configure `resources` + `resourceFields`

### When user needs undo/redo
→ Read `references/undo-redo.md` — inject `UndoRedoService`, set `enableUndoRedo: true`

### When user needs localization or RTL
→ Read `references/localization-rtl.md` — call `L10n.load()` before bootstrap, set `locale` and `enableRtl`

### When user needs state persistence
→ Read `references/state-persistence.md` — set `enablePersistence: true` and unique `id`

### When user needs split/segment tasks
→ Read `references/splitting-and-merging.md` — map `taskFields.segments`, inject `EditService`

---

## Key Module Injections

| Feature | Service to Inject |
|---------|------------------|
| Editing (add/edit/delete/taskbar drag) | `EditService` |
| Filtering | `FilterService` |
| Sorting | `SortService` |
| Toolbar | `ToolbarService` |
| Selection | `SelectionService` |
| Day Markers / Holidays / Event Markers | `DayMarkersService` |
| Critical Path | `CriticalPathService` |
| Excel / CSV Export | `ExcelExportService` |
| PDF Export | `PdfExportService` |
| Undo / Redo | `UndoRedoService` |
| Column Menu | `ColumnMenuService` |
| Context Menu | `ContextMenuService` |
| Virtual Scrolling | `VirtualScrollService` |
| Row Drag and Drop | `RowDDService` |
| Column Reordering | `ReorderService` |
| Frozen Columns | `FreezeService` |
| Column Resizing | `ResizeService` |

---

## Key Props Reference

| Property | Type | Default | Description |
|---|---|---|---|
| `dataSource` | `object[]` \| `DataManager` | `[]` | Task data — self-referential (flat) or hierarchical |
| `taskFields` | `TaskFieldsModel` | — | Maps data fields to Gantt task properties |
| `height` | `string` \| `number` | `'auto'` | Component height (e.g. `'450px'`) |
| `taskMode` | `string` | `'Auto'` | Scheduling mode: `'Auto'` \| `'Manual'` \| `'Custom'` |
| `editSettings` | `EditSettingsModel` | — | Enable add/edit/delete/taskbar editing and edit mode |
| `toolbar` | `string[]` \| `ItemModel[]` | — | Toolbar buttons — requires `ToolbarService` |
| `allowFiltering` | `boolean` | `false` | Enable column filter menus — requires `FilterService` |
| `filterSettings` | `FilterSettingsModel` | — | `type`, `hierarchyMode`, `columns` (initial filters) |
| `allowSorting` | `boolean` | `false` | Enable column sorting — requires `SortService` |
| `sortSettings` | `SortSettingsModel` | — | `columns` array for initial sort on load |
| `allowSelection` | `boolean` | `true` | Enable row/cell selection — requires `SelectionService` |
| `selectionSettings` | `SelectionSettingsModel` | — | `mode`, `type`, `enableToggle`, `cellSelectionMode` |
| `enableCriticalPath` | `boolean` | `false` | Highlight critical path — requires `CriticalPathService` |
| `enableUndoRedo` | `boolean` | `false` | Enable undo/redo — requires `UndoRedoService` |
| `undoRedoActions` | `string[]` | (all actions) | Which action types to track in history |
| `undoRedoStepsCount` | `number` | `10` | Maximum undo/redo history depth |
| `enablePersistence` | `boolean` | `false` | Persist filter/sort/column state to `localStorage` |
| `enableImmutableMode` | `boolean` | `false` | Re-render only changed rows on data refresh |
| `allowExcelExport` | `boolean` | `false` | Enable Excel export — requires `ExcelExportService` |
| `allowPdfExport` | `boolean` | `false` | Enable PDF export — requires `PdfExportService` |
| `enableContextMenu` | `boolean` | `false` | Enable right-click context menu — requires `ContextMenuService` |
| `contextMenuItems` | `string[]` \| `ContextMenuItemModel[]` | (defaults) | Context menu items |
| `enableVirtualization` | `boolean` | `false` | DOM virtualization for large datasets — requires `VirtualScrollService` |
| `enableTimelineVirtualization` | `boolean` | `false` | Virtualize timeline columns |
| `renderBaseline` | `boolean` | `false` | Show baseline bars alongside current taskbars |
| `baselineColor` | `string` | `'red'` | Baseline bar color |
| `allowUnscheduledTasks` | `boolean` | `false` | Allow tasks missing start/end/duration |
| `validateManualTasksOnLinking` | `boolean` | `false` | Adjust manual task dates when dependency links change |
| `allowParentDependency` | `boolean` | `true` | Allow dependencies between parent/child tasks |
| `autoUpdatePredecessorOffset` | `boolean` | `false` | Sync predecessor offsets with actual positions on load |
| `highlightWeekends` | `boolean` | `false` | Shade weekend columns in timeline |
| `gridLines` | `string` | `'Both'` | Grid lines: `'Both'` \| `'Horizontal'` \| `'Vertical'` \| `'None'` |
| `rowHeight` | `number` | `36` | Height of each row in pixels |
| `enableAltRow` | `boolean` | `true` | Alternate row background color |
| `allowRowDragAndDrop` | `boolean` | `false` | Drag rows to reorder or reparent |
| `showColumnMenu` | `boolean` | `false` | Column header context menu — requires `ColumnMenuService` |
| `timelineSettings` | `TimelineSettingsModel` | — | `topTier`, `bottomTier`, `timelineUnitSize`, `weekStartDay` |
| `timelineViewMode` | `string` | — | Shortcut: `'Hour'` \| `'Day'` \| `'Week'` \| `'Month'` \| `'Year'` |
| `projectStartDate` | `Date` \| `string` | (from data) | Fix timeline start bound |
| `projectEndDate` | `Date` \| `string` | (from data) | Fix timeline end bound |
| `holidays` | `HolidayModel[]` | `[]` | Non-working days with labels — requires `DayMarkersService` |
| `eventMarkers` | `EventMarkerModel[]` | `[]` | Vertical marker lines — requires `DayMarkersService` |
| `resources` | `object[]` | — | Resource data array |
| `resourceFields` | `ResourceFieldsModel` | — | Maps resource `id`, `name`, `unit`, `group` fields |
| `locale` | `string` | `'en-US'` | Culture code for localization (e.g. `'fr'`, `'ar'`) |
| `enableRtl` | `boolean` | `false` | Right-to-left layout |
| `timezone` | `string` | (browser) | IANA timezone (e.g. `'UTC'`, `'America/New_York'`) |
| `durationUnit` | `string` | `'Day'` | Default duration unit: `'Day'` \| `'Hour'` \| `'Minute'` |
| `workUnit` | `string` | `'Hour'` | Work scheduling unit: `'Hour'` \| `'Day'` \| `'Minute'` |
| `workWeek` | `string[]` | Mon–Fri | Working days: `['Monday','Tuesday','Wednesday','Thursday','Friday']` |
| `includeWeekend` | `boolean` | `false` | Treat all 7 days as working days |
| `dayWorkingTime` | `object[]` | `[{from:8,to:17}]` | Working hour ranges per day: `[{ from: 8, to: 12 }, { from: 13, to: 17 }]` |
| `dateFormat` | `string` | `'MM/dd/yyyy'` | Global date display format for all date columns |
| `splitterSettings` | `SplitterSettingsModel` | — | `position`, `columnIndex`, `view` for TreeGrid/chart split |
| `loadingIndicator` | `LoadingIndicatorModel` | — | `indicatorType`: `'Spinner'` \| `'Shimmer'` |
