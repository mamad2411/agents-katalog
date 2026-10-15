---
name: syncfusion-javascript-gantt-chart
description: "Implement Syncfusion Gantt Chart using JavaScript/TypeScript (Essential JS 2). Use this when working with ej2-gantt component for project scheduling, task dependencies, and timeline management. Covers full Gantt implementation including data binding, task scheduling, columns, resources, timeline configuration, WBS, resource view, critical path, baseline tracking, filtering, sorting, editing, and export functionality (Excel/PDF)."
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Syncfusion Gantt Chart

A comprehensive skill for implementing the Syncfusion Essential JS 2 Gantt Chart component in JavaScript/TypeScript projects. Covers everything from initial setup to advanced features like critical path, resource management, virtual scrolling, and export.

## When to Use This Skill

Use this skill when the user needs to:

- **Set up** the Syncfusion Gantt Chart from scratch (installation, dependencies, basic init)
- **Bind data** (local hierarchical, flat/self-referential, remote DataManager, load-on-demand)
- **Configure task scheduling** (auto/manual, milestones, duration units, constraints)
- **Define columns** (custom columns, templates, frozen, WBS, checkbox, responsive)
- **Manage resources** (assign resources, resource view, multi-taskbar, work/task types)
- **Configure timeline** (top/bottom tiers, zooming, formatting)
- **Enable editing** (cell, dialog, taskbar drag/resize, dependency editing, indent/outdent)
- **Implement filtering, sorting, searching** on Gantt grid
- **Show task dependencies** (FS, SS, FF, SF, offsets, connector lines)
- **Display critical path**, baseline, event markers, holidays, data markers, labels
- **Export** to Excel or PDF
- **Implement toolbar, context menu, undo/redo**
- **Handle events**, state persistence, localization, RTL, timezone
- **Optimize performance** (virtual scroll, immutable mode, loading animation)

## Quick Start

```typescript
import { Gantt, Edit, Filter, Sort, Toolbar } from '@syncfusion/ej2-gantt';

Gantt.Inject(Edit, Filter, Sort, Toolbar);

let gantt: Gantt = new Gantt({
    dataSource: [
        {
            TaskID: 1, TaskName: 'Project Initiation',
            StartDate: new Date('04/02/2024'), EndDate: new Date('04/21/2024'),
            subtasks: [
                { TaskID: 2, TaskName: 'Identify Site location', StartDate: new Date('04/02/2024'), Duration: 4, Progress: 50 },
                { TaskID: 3, TaskName: 'Soil test approval', StartDate: new Date('04/02/2024'), Duration: 4, Predecessor: '2FS', Progress: 50 }
            ]
        }
    ],
    height: '450px',
    taskFields: { id: 'TaskID', name: 'TaskName', startDate: 'StartDate', endDate: 'EndDate', duration: 'Duration', progress: 'Progress', dependency: 'Predecessor', child: 'subtasks' },
    toolbar: ['Add', 'Edit', 'Delete', 'Update', 'Cancel', 'ExpandAll', 'CollapseAll', 'Search'],
    editSettings: { allowAdding: true, allowEditing: true, allowDeleting: true, allowTaskbarEditing: true },
    allowSorting: true,
    allowFiltering: true
});
gantt.appendTo('#Gantt');
```

## Navigation Guide

### Setup & Installation
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- npm installation, webpack setup
- Basic Gantt initialization (app.ts + index.html)
- taskFields mapping, module injection
- Error handling with actionFailure

### Data Binding
📄 **Read:** [references/data-binding.md](references/data-binding.md)
- Local hierarchical and self-referential (flat) data
- Remote data (DataManager, WebApiAdaptor, UrlAdaptor)
- Load child on demand
- Ajax binding, split tasks (segments)

### Task Scheduling
📄 **Read:** [references/task-scheduling.md](references/task-scheduling.md)
- `taskMode`: `'Auto'` (default) / `'Manual'` / `'Custom'` — controls date validation behaviour
- Auto: parent taskbar derived from child min/max dates; dependencies shift successors automatically
- Manual: user controls all dates; no recalculation; `validateManualTasksOnLinking: true` enables predecessor-based validation only
- Custom: per-task scheduling via `taskFields.manual` boolean field in data source
- Unscheduled tasks: `allowUnscheduledTasks: true` — tasks with only start date, only end date, only duration, or none; if `false`, defaults to duration 1 from `projectStartDate`
- Duration units: `durationUnit` (project-wide: `'Day'`/`'Hour'`/`'Minute'`); per-task via `taskFields.durationUnit` field or inline string (`'4hours'`, `'30min'`)
- Milestones: `Duration: 0` renders a diamond shape
- `projectStartDate` / `projectEndDate` — constrain chart range; auto-calculated if omitted
- `dayWorkingTime` — define working hour ranges (default: 8–12 and 13–17); used for auto-scheduling calculations
- `weekWorkingTime` — per-day-of-week working hours; overrides `dayWorkingTime` for listed days; unlisted days fall back to `dayWorkingTime`
- `workWeek` — specify working days (default: Mon–Fri); `includeWeekend: true` makes Sat/Sun working days
- `highlightWeekends: true` — visually shade non-working days in chart

### Task Constraints
📄 **Read:** [references/task-constraints.md](references/task-constraints.md)
- Constraint types: ASAP(0), ALAP(1), MSO(2), MFO(3), SNET(4), SNLT(5), FNET(6), FNLT(7)
- constraintType and constraintDate field mapping in taskFields
- Benefits: enforce task sequences, anchor milestones, prevent resource conflicts
- Handle constraint violations via actionBegin (requestType: 'validateTaskViolation')
- validateMode flags: respectMustStartOn, respectMustFinishOn, respectStartNoLaterThan, respectFinishNoLaterThan
- Constraint interaction with taskMode (Auto / Manual / Custom)
- Editing constraints via dialog editor or programmatically (updateRecordByID)

### Task Dependency
📄 **Read:** [references/task-dependency.md](references/task-dependency.md)
- FS, SS, FF, SF types with lag/lead offsets (day/hour/minute units)
- allowParentDependency, multiple predecessors (comma-separated)
- Connector line customization (connectorLineWidth, connectorLineBackground)
- addPredecessor / removePredecessor / updatePredecessor methods
- Validation modes (respectLink, removeLink, preserveLinkWithEditing) via actionBegin
- Validation dialog when all modes are disabled
- autoUpdatePredecessorOffset — sync offsets against calendar rules on initial load
- updateOffsetOnTaskbarEdit: false — preserve offsets during taskbar drag
- Show/hide dependency lines dynamically via .e-gantt-dependency-view-container
- enablePredecessorValidation: false — draw lines without enforcing scheduling

### Critical Path
📄 **Read:** [references/critical-path.md](references/critical-path.md)
- enableCriticalPath property
- Slack calculation (zero/negative slack)
- Visual highlighting and CPM principles

### Baseline
📄 **Read:** [references/baseline.md](references/baseline.md)
- renderBaseline, baselineColor
- baselineStartDate, baselineEndDate, baselineDuration
- Baseline milestones, CSS customization

### Resources
📄 **Read:** [references/resources.md](references/resources.md)
- resourceFields mapping, resources collection
- Assigning resources to tasks, resource units
- Over-allocation, resource templates
- Custom column template + queryTaskbarInfo for per-resource badge and taskbar colors

### Resource View
📄 **Read:** [references/resource-view.md](references/resource-view.md)
- viewType: 'ResourceView'
- showOverAllocation
- Resource grouping and display
- Unassigned tasks grouped automatically at bottom
- Taskbar drag and drop between resources (allowTaskbarDragAndDrop + RowDD module)

### Resource Multi Taskbar
📄 **Read:** [references/multi-taskbar.md](references/multi-taskbar.md)
- enableMultiTaskbar for collapsed resource rows
- Overlapping task visualization
- Editing tasks in collapsed state

### Work & Task Types
📄 **Read:** [references/work.md](references/work.md)
- taskFields.work mapping, workUnit (Hour/Day/Minute)
- FixedWork, FixedDuration, FixedUnit task types

### Columns
📄 **Read:** [references/columns.md](references/columns.md)
- columns array definition, treeColumnIndex
- Checkbox columns, responsive columns
- Column spanning, column templates
- WBS column (enableWBS, enableAutoWbsUpdate)

### Column Operations
📄 **Read:** [references/column-operations.md](references/column-operations.md)
- Column resizing (allowResizing, Resize module)
- Column reordering (allowReordering, Reorder module)
- Column menu (showColumnMenu)
- Frozen/pinned columns (frozenColumns)

### Timeline
📄 **Read:** [references/timeline.md](references/timeline.md)
- topTier / bottomTier units and format
- timelineSettings configuration
- Custom timeline formatting, timeline tooltip

### Zooming
📄 **Read:** [references/timeline.md](references/timeline.md)
- ZoomIn, ZoomOut, ZoomToFit toolbar items
- zoomingLevels configuration
- Programmatic zoom control

### Sorting
📄 **Read:** [references/sorting.md](references/sorting.md)
- `allowSorting: true` + `Sort` module injection
- Click header to sort; Ctrl+click for multi-column sort; Shift+click to remove column from multi-sort
- Initial sort via `sortSettings.columns` array (field + direction)
- Programmatic sort: `gantt.sortModule.sortColumn(field, direction, isMultiSort)`; clear all: `gantt.clearSorting()`
- Sort events: `actionBegin` / `actionComplete` with `args.requestType === 'sorting'`
- Disable sort for specific column: `columns.allowSorting: false`
- Custom columns (string/numeric) sortable via `sortSettings` or programmatically
- Touch: tap header to sort; popup appears for multi-column sort on touch devices

### Filtering
📄 **Read:** [references/filtering.md](references/filtering.md)
- allowFiltering, Filter module
- Menu filter and Excel-like filter
- Column-level filtering, searching

### Selection
📄 **Read:** [references/selection.md](references/selection.md)
- `allowSelection: false` disables all selection; `Selection` module required
- `selectionSettings.mode`: `'Row'` (default) / `'Cell'` / `'Both'`
- `selectionSettings.type`: `'Single'` (default) / `'Multiple'` (Ctrl+click for multi-select)
- `selectionSettings.enableToggle: true` — click selected item again to deselect
- `enableHover: true` — highlights rows, taskbars, header cells, and timeline cells on hover
- Row selection: `selectedRowIndex` for initial load; `selectRow(index)` / `selectRows([indexes])` for dynamic selection
- Prevent row selection: `rowSelecting` event with `args.cancel = true`; `rowDeselecting` to prevent deselection
- Cell selection: `mode: 'Cell'`; `selectCell({ rowIndex, cellIndex })` for dynamic selection; `getSelectedRowCellIndexes()` returns `{ cellIndexes, rowIndex }[]`
- Prevent cell selection: `cellSelecting` event with `args.cancel = true`; `cellSelected` fires after
- Select rows by condition in `dataBound` via `gantt.treeGrid.grid.dataSource` + `gantt.selectRows(indexes)`
- `getSelectedRowIndexes()` → `number[]`; `getSelectedRecords()` → `object[]`
- `gantt.clearSelection()` — clears all selected rows and cells
- Touch: tap to select a row; tap popup to enter multi-row select mode, then tap additional rows
- Cell selection not supported with `enableVirtualization`

### Rows
📄 **Read:** [references/rows.md](references/rows.md)
- Customize row styles via rowDataBound event, CSS (.e-altrow, .e-selectionbackground), and treeGrid methods
- Style parent vs child rows using hasChildRecords in rowDataBound
- autoFocusTasks — scroll chart to taskbar when a row is clicked
- rowHeight — uniform row height; per-row height via args.rowHeight in rowDataBound
- Row hover with custom actions using dataBound + mouseover + Tooltip
- Add rows programmatically via gantt.addRecord(data, position, index) — Top/Bottom/Above/Below/Child
- Show/hide rows dynamically via treeGrid.getRowByIndex() + CSS display toggle
- Row spanning via args.rowSpan in queryCellInfo (combine with colSpan for 2D merge)

### Row Drag, Drop, Indent and Outdent
📄 **Read:** [references/rows-drag-drop.md](references/rows-drag-drop.md)
- RowDD module, allowRowDragAndDrop — drag rows within the Gantt
- Drop positions: above (top border), below (bottom border), child (both borders)
- Drag rows to external component via treeGrid.rowDropSettings.targetID in load event
- Multi-row drag via selectionSettings.type: 'Multiple'
- allowTaskbarDragAndDrop — reorder rows by dragging their taskbar
- Programmatic reorder via gantt.reorderRows(fromIndexes, toIndex, position)
- Drag lifecycle events: rowDragStartHelper, rowDragStart, rowDrag, rowDrop
- Prevent child drop position using dropPosition === 'middleSegment' + reorderRows
- Indent/Outdent toolbar items and gantt.indent() / gantt.outdent() methods
- Programmatic indent/outdent: selectRow(i) then indent()/outdent()
- Detect indent/outdent via actionComplete (args.requestType === 'indented'/'outdented')

### Managing Tasks (Editing)
📄 **Read:** [references/managing-tasks.md](references/managing-tasks.md)
- editSettings (allowAdding, allowEditing, allowDeleting)
- Cell / Dialog / Taskbar editing modes
- Add, delete, indent/outdent, drag-and-drop rows
- Server-side CRUD, split/merge tasks, validation

### Undo / Redo
📄 **Read:** [references/undo-redo.md](references/undo-redo.md)
- UndoRedo module injection, enableUndoRedo property
- undoRedoActions — configure which actions to track (Edit, Delete, Add, Sorting, Filtering, ZoomIn/Out, ColumnReorder, ColumnResize, Indent, Outdent, RowDragAndDrop, TaskbarDragAndDrop, ColumnState, PreviousTimeSpan, NextTimeSpan)
- undoRedoStepsCount — limit history depth (default: 10; 0 = disabled)
- Toolbar Undo/Redo items for UI-based history navigation
- Programmatic control: undo() and redo() methods
- Retrieve history: getUndoActions() / getRedoActions()
- Reset history: clearUndoCollection() / clearRedoCollection()

### Toolbar
📄 **Read:** [references/toolbar.md](references/toolbar.md)
- Built-in toolbar items reference (Add, Edit, Delete, Update, Cancel, Search, ExpandAll, CollapseAll, Indent, Outdent, PrevTimeSpan, NextTimeSpan, ZoomIn, ZoomOut, ZoomToFit, Undo, Redo)
- Override built-in toolbar behavior via toolbarClick with args.cancel = true
- Show only icons — hide text labels with CSS (.e-tbar-btn-text)
- Customize toolbar button appearance using CSS class selectors
- Reposition toolbar to bottom using created event + DOM manipulation
- Custom toolbar items using ItemModel (text, id, prefixIcon, align)
- Mix built-in and custom items in the same toolbar array
- Enable/disable toolbar items dynamically via gantt.toolbarModule.enableItems()
- Add input components (AutoComplete, DropDownList) to toolbar using type: 'Input' with template

### Context Menu
📄 **Read:** [references/context-menu.md](references/context-menu.md)
- enableContextMenu, ContextMenu module
- Default and custom context menu items

### Event Markers
📄 **Read:** [references/event-markers.md](references/event-markers.md)
- DayMarkers module, eventMarkers array
- day, label, cssClass properties

### Holidays
📄 **Read:** [references/holidays.md](references/holidays.md)
- DayMarkers module, holidays array
- from, to, label, cssClass properties

### Data Markers (Indicators)
📄 **Read:** [references/data-markers.md](references/data-markers.md)
- taskFields.indicators mapping
- date, iconClass, name, tooltip per indicator

### Task Labels
📄 **Read:** [references/labels.md](references/labels.md)
- labelSettings: leftLabel, rightLabel, taskLabel
- Field-based and template-based labels

### Taskbar Customization
📄 **Read:** [references/taskbar.md](references/taskbar.md)
- taskbarHeight, rowHeight
- taskbarTemplate, parentTaskbarTemplate, milestoneTemplate
- queryTaskbarInfo event for dynamic styling

### Scrolling
📄 **Read:** [references/scrolling.md](references/scrolling.md)
- scrollToDate method, scroll settings
- Horizontal and vertical scroll control

### Virtual Scrolling
📄 **Read:** [references/virtual-scroll.md](references/virtual-scroll.md)
- VirtualScroll module injection, enableVirtualization for row virtualization
- enableTimelineVirtualization — on-demand horizontal timeline rendering (renders 3x viewport width initially)
- Get filtered record count with virtual scroll: actionComplete + gantt.treeGrid.filterModule.filteredResult
- Get total dataset count via gantt.flatData.length in created event
- Limitations: height must be in pixels, no multi-taskbar in Resource View, cell selection not persisted

### Splitter
📄 **Read:** [references/splitter.md](references/splitter.md)
- splitterSettings (position, columnIndex, view)
- setSplitterPosition method, view modes

### State Persistence
📄 **Read:** [references/state-persistence.md](references/state-persistence.md)
- enablePersistence — saves Filtering, Sorting, Columns state in localStorage
- localStorage key format: "gantt" + element ID (e.g., "ganttGantt")
- Get/set persisted state via window.localStorage.getItem / setItem
- Prevent specific keys from persisting via addOnPersist override in dataBound
- Not persisted by default: column templates, formatters, headerText, headerTemplate, value accessors
- Restore header templates and header text using getPersistData() + Object.assign + gantt.treeGrid.setProperties()

### Immutable Mode
📄 **Read:** [references/immutable.md](references/immutable.md)
- enableImmutableMode for performance
- When to use immutable mode

### Timezone
📄 **Read:** [references/timezone.md](references/timezone.md)
- timezone property (UTC, IANA zones)
- Consistent time display across regions

### Globalization & Localization
📄 **Read:** [references/global-local.md](references/global-local.md)
- Localization: `L10n.load({ 'de-DE': { gantt: { ... } } })` + `locale: 'de-DE'` on Gantt instance
- Full locale key table organized by category: task fields/columns, dialog/tabs, toolbar/actions, context menu/dependency, labels/timeline, predecessor validation messages (`taskBeforePredecessor_FS` etc.)
- New keys vs old reference: `resourceID`, `writeNotes`, `task`, `tasks`, `saveButton`, `okText`, `from`/`to`, `taskLink`, `lag`, `start`/`finish`, `enterValue`, `above`/`below`/`child`, `milestone`, `toTask`/`toMilestone`, `eventMarkers`, `leftTaskLabel`, `rightTaskLabel`, `timelineCell`, `confirmPredecessorDelete`, `changeScheduleMode`, `subTasksStartDate`/`subTasksEndDate`, `scheduleStartDate`/`scheduleEndDate`, `unit`, `work`, `taskType`, `group`
- Internationalization: `loadCldr(cagregorian, numbers)` + `setCulture()` for locale-aware date/number formatting; CLDR data from `@syncfusion/ej2-cldr-data`
- RTL: `enableRtl: true` + matching locale (e.g., `'ar-AE'`) — reverses text direction and full layout
- Default locale is `'en-US'`

### Excel Export
📄 **Read:** [references/excel-export.md](references/excel-export.md)
- ExcelExport module, `allowExcelExport`, toolbar items: `ExcelExport`, `CsvExport`
- `excelExport()` / `csvExport()` methods, export to blob (4th arg `isBlob`)
- Custom data source override (`dataSource` in ExcelExportProperties)
- fileName, includeHiddenColumn, exportType
- Show/hide columns on export (toolbarClick + excelExportComplete to restore)
- Cell formatting (`excelQueryCellInfo` + `args.style.backColor`)
- Theme (header/record font name and color), header/footer rows with hyperlinks and styles
- Multiple Gantt export: `AppendToSheet` (same sheet, blankRows) and `NewSheet` modes

### PDF Export
📄 **Read:** [references/pdf-export.md](references/pdf-export.md)
- PdfExport module, `allowPdfExport`, toolbar item
- fileName, pageOrientation, pageSize, exportType, includeHiddenColumn, showPredecessorLines
- Export current view data, export/hide columns on export
- Fit-to-width (isFitToWidth, chartWidth, gridWidth), export to blob
- Header/footer: Text, Image, Line, PageNumber content types; enableFooter
- Multiple Gantt export to single PDF, indicators in PDF export
- Conditional cell formatting (pdfQueryCellInfo + PdfColor)
- Timeline cell formatting (pdfQueryTimelineCellInfo)
- Taskbar formatting + split taskbar segment colors (taskSegmentStyles)
- ganttStyle: full appearance override (columnHeader, cell, taskbar, timeline, label, eventMarker, holiday)
- Export with column templates (images/hyperlinks), taskbar templates, label templates, header templates
- pdfColumnHeaderQueryCellInfo for header template export

### Loading Animation
📄 **Read:** [references/loading-animation.md](references/loading-animation.md)
- loadingIndicator.indicatorType: 'Shimmer' | 'Spinner'
- Shimmer with virtual scroll

### Accessibility
📄 **Read:** [references/accessibility.md](references/accessibility.md)
- WCAG 2.1 Level AA compliance
- Keyboard navigation (grid, toolbar, context menu shortcuts)
- ARIA roles and attributes (treegrid, row, gridcell, columnheader, dialog)
- High contrast theme (highcontrast.css)
- Screen reader support (NVDA, JAWS, VoiceOver) — taskbarAriaLabel customization
- Focus management and autoFocusTasks

### Programmatic Methods
📄 **Read:** [references/gantt-methods.md](references/gantt-methods.md)
- **Column**: `autoFitColumns(field?)`, `getGanttColumns()`, `getGridColumns()`, `refreshColumns()`, `reorderColumns(from, to)`, `removeSortColumn(field)`
- **Row/Record lookup**: `getRecordByID(id)`, `getTaskByUniqueID(uid)`, `getRowByID(id)`, `getRowByIndex(index)`, `getTaskInfo(taskId)`, `getCurrentViewData()`, `getExpandedRecords(records)`
- **Expand/Collapse**: `expandByIndex(index | index[])`, `collapseByIndex(index)`
- **Edit/CRUD**: `cancelEdit()`, `deleteRecord(taskDetail)`, `updateRecordByIndex(index, data)`, `updateTaskId(currentId, newId)`, `changeTaskMode(data)`, `convertToMilestone(id)`
- **Dependency**: `removePredecessor(id)` — removes all dependencies from a task
- **Split/Merge**: `splitTask(taskId, splitDate | splitDate[])`, `mergeTask(taskId, segmentIndexes)` — requires `allowTaskbarEditing`; parent/milestones cannot be split
- **Selection**: `selectCells(rowCellIndexes)` — select cells by `{ rowIndex, cellIndexes[] }` pairs; requires `mode: 'Cell'`
- **Scroll**: `scrollToTask(taskId)`, `setScrollTop(px)`, `updateChartScrollOffset(left, top)`
- **Data**: `updateDataSource(dataSource, { projectStartDate, projectEndDate })`
- **Critical path**: `getCriticalTasks()` → `IGanttData[]`; requires `enableCriticalPath` + `CriticalPath` module
- **Formatting helpers**: `getDurationString(value, unit)`, `getWorkString(value, unit)`, `getTaskbarHeight()`
- All methods use the Gantt instance directly: `gantt.methodName(args)` (TypeScript/JavaScript)

### Events
📄 **Read:** [references/events.md](references/events.md)
- actionBegin — fires before any action (add/edit/delete/sort/filter/dependency/zoom); supports `args.cancel`; argument types vary by operation (ITaskAddedEventArgs, ITimeSpanEventArgs, FilterEventArgs, SortEventArgs, IDependencyEventArgs, ZoomEventArgs)
- actionComplete — fires after action completes; switch on `args.requestType` (filtering, sorting, save, delete, AfterZoomIn/Out/ToProject)
- actionFailure — fires on operation failure; `args.error[0]` for error details
- cellEdit — fires when grid cell enters edit mode; `args.cancel = true` prevents editing; args: cancel, cell, columnName, columnObject, row, rowData, value, validationRules
- beforeTooltipRender — fires before tooltip renders (taskbar/connector/timeline); override `args.content` or set `args.cancel = true`
- beforeExcelExport / beforePdfExport — fires before export; `args.cancel = true` aborts; isCsv flag for Excel vs CSV
- Cell selection events (require `selectionSettings.mode: 'Cell'` or `'Both'`): cellSelecting (cancel to prevent), cellSelected, cellDeselecting, cellDeselected — CellSelectEventArgs (cellIndex, cells, currentCell, data, previousRowCell) and CellDeselectEventArgs (cellIndexes, cells, data)
- Row selection events: rowSelecting, rowSelected, rowDeselecting, rowDeselected — cancel, data, rowIndex, isCtrlPressed, isShiftPressed
- Column drag events (require `allowReordering: true` + Reorder module): columnDragStart, columnDrag, columnDrop — ColumnDragEventArgs (column, target, draggableType)
- Column menu events (require `showColumnMenu: true` + ColumnMenu module): columnMenuOpen (ColumnMenuOpenEventArgs: cancel, column, element, items, left, top, parentItem), columnMenuClick (ColumnMenuClickEventArgs: name, column, element, item)
- contextMenuClick — requires ContextMenu module + contextMenuItems; args: name, element, event, item (id/text), type, rowData
- Export complete events: excelExportComplete / pdfExportComplete — access blob via `args.promise.then((e) => e.blobData)`
- requestType reference table: beforeSave, beforeDelete, taskbarEditing, filtering, sorting, zoom variants, save, delete, validateDependency, updateDependency
