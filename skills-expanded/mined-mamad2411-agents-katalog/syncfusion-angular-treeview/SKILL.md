---
name: syncfusion-angular-treeview
description: |
  Implement hierarchical tree structures with Syncfusion Angular TreeView component. Use this when building tree-based UIs with features like checkboxes, drag-and-drop, node editing, filtering, and templating. This skill covers dynamic data binding, nested hierarchies, folder structures, and interactive tree-based interfaces.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Navigation Components"
---

# Implementing TreeView in Angular

The **TreeView** component displays hierarchical data in a tree-like structure with built-in support for interactive features including checkboxes, drag-and-drop, in-place editing, multi-selection, filtering, sorting, templating, and keyboard navigation. It's ideal for displaying file systems, organizational charts, category hierarchies, navigation menus, and any nested data structure.

## When to Use This Skill

- **Building hierarchical UIs**: Displaying parent-child data relationships
- **File/folder browsers**: Showing directory structures with expand/collapse
- **Navigation structures**: Creating menu systems or site hierarchies  
- **Data organization**: Displaying categorized or nested data
- **Interactive selection**: Implementing multi-selection or checkbox-based selection
- **Drag-and-drop interfaces**: Reorganizing tree data by dragging nodes
- **Search/filter functionality**: Finding nodes in large tree structures
- **Customized appearances**: Styling nodes per level or with templates

## Navigation Guide

Choose your task below to navigate to the relevant reference documentation:

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)

When to read: Setting up TreeView for the first time, installing packages, importing modules, basic component initialization, CSS imports, theme selection, creating your first tree.

### Data Binding & Hierarchies
📄 **Read:** [references/data-binding.md](references/data-binding.md)

When to read: Connecting data sources to TreeView, binding hierarchical or self-referential data, using DataManager, loading data from remote APIs, implementing lazy loading (load on demand), dynamically updating tree data.

### Node Selection & Checkboxes
📄 **Read:** [references/node-selection.md](references/node-selection.md)

When to read: Enabling checkboxes, managing checkbox states (checked/unchecked/tri-state), implementing multi-selection vs single-selection, using selection events, getting selected node IDs, disabling checkboxes, removing parent checkboxes.

### Node Editing & Manipulation
📄 **Read:** [references/node-editing.md](references/node-editing.md)

When to read: Enabling in-place editing, adding/removing/updating nodes programmatically, validating edited text, moving nodes, using node manipulation methods (addNodes, removeNodes, updateNode, moveNodes).

### Drag and Drop
📄 **Read:** [references/drag-and-drop.md](references/drag-and-drop.md)

When to read: Enabling drag-and-drop functionality, restricting drops on specific nodes, handling drag events, customizing drop indicators, preventing invalid operations.

### Templating & Styling Nodes
📄 **Read:** [references/templating.md](references/templating.md)

When to read: Creating custom node templates, using dynamic icons, styling nodes based on level, customizing expand/collapse icons, showing tooltips, handling multi-line nodes, CSS customization.

### Filtering & Sorting
📄 **Read:** [references/filtering-sorting.md](references/filtering-sorting.md)

When to read: Filtering nodes by text, implementing search functionality, sorting nodes globally or per level, organizing tree display order.

### Context Menu Integration
📄 **Read:** [references/context-menu.md](references/context-menu.md)

When to read: Adding context menu for node operations, handling right-click actions, implementing add/edit/delete via menu, creating custom menu items.

### Accessibility, Advanced Features & API Migration
📄 **Read:** [references/accessibility-advanced.md](references/accessibility-advanced.md)

When to read: Keyboard navigation (arrow keys, Enter, Space), ARIA attributes and accessibility compliance, RTL (right-to-left) support, getting child nodes, accordion behavior, advanced methods, migrating from EJ1 to EJ2, performance optimization.

## Quick Start Example

Here's a minimal TreeView implementation with static hierarchical data:

```typescript
import { Component } from '@angular/core';
import { TreeViewModule } from '@syncfusion/ej2-angular-navigations';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-tree-view',
  standalone: true,
  imports: [FormsModule, TreeViewModule],
  template: `
    <ejs-treeview 
      id="treeView"
      [fields]="treeFields"
      [allowMultiSelection]="true">
    </ejs-treeview>
  `
})
export class TreeViewComponent {
  // Hierarchical data structure
  treeData = [
    {
      id: '01',
      name: 'Documents',
      hasChild: true,
      expanded: true,
      subChild: [
        { id: '01-01', name: 'Work Files' },
        { id: '01-02', name: 'Personal' }
      ]
    },
    {
      id: '02',
      name: 'Downloads',
      hasChild: true,
      subChild: [
        { id: '02-01', name: 'Images' },
        { id: '02-02', name: 'Videos' }
      ]
    }
  ];

  // Field mapping configuration
  treeFields = {
    dataSource: this.treeData,
    id: 'id',
    text: 'name',
    child: 'subChild',
    hasChildren: 'hasChild',
    expanded: 'expanded'
  };
}
```

## Key TreeView Methods

| Method | Purpose |
|--------|---------|
| `addNodes(nodes, target?, index?, preventTargetExpand?)` | Add collection of nodes at target position |
| `removeNodes(nodeIds)` | Remove nodes by ID |
| `updateNode(target, newText)` | Replace node text (requires allowEditing enabled) |
| `moveNodes(sourceNodes, target, index?, preventTargetExpand?)` | Move nodes to new parent and index position |
| `getTreeData(nodeId?)` | Get all tree data or specific node data |
| `getAllCheckedNodes()` | Get all checked node IDs including child nodes whether loaded or not |
| `checkAll(nodes?)` | Check all or specific nodes |
| `uncheckAll(nodes?)` | Uncheck all or specific nodes |
| `beginEdit(nodeId)` | Start editing a node |
| `expandAll(nodes?, level?, excludeHiddenNodes?, preventAnimation?)` | Expand all or specific nodes, optionally by level |
| `collapseAll(nodes?, level?, excludeHiddenNodes?)` | Collapse all or specific nodes, optionally by level |
| `ensureVisible(nodeId)` | Scroll to make node visible |
| `disableNodes(nodeIds)` | Disable specific nodes |
| `enableNodes(nodeIds)` | Enable specific nodes |
| `getNode(nodeId)` | Get HTML element of node |
| `destroy()` | Destroy TreeView component |

## Key TreeView Events

| Event | Triggered When |
|-------|-----------------|
| `created` | TreeView component is created |
| `dataBound` | Data source binding is complete |
| `dataSourceChanged` | Tree data is modified (add/remove/update) |
| `nodeClicked` | User clicks on a node |
| `nodeSelected` | Node is selected |
| `nodeSelecting` | Before node selection (can prevent) |
| `nodeChecked` | Checkbox state changes |
| `nodeChecking` | Before checkbox changes (can prevent) |
| `nodeExpanding` | Before node expansion |
| `nodeExpanded` | Node is expanded |
| `nodeCollapsing` | Before node collapse |
| `nodeCollapsed` | Node is collapsed |
| `nodeEditing` | Before node text editing |
| `nodeEdited` | After node text is edited |
| `nodeDragStart` | Drag operation begins |
| `nodeDragging` | Node is being dragged |
| `nodeDragStop` | Drag ends before drop |
| `nodeDropped` | Node is dropped successfully |
| `drawNode` | Before rendering each node (customize appearance) |
| `keyPress` | User presses keyboard key |
| `destroyed` | TreeView component is destroyed |

## Common Patterns

### Pattern 1: Checkbox-Based Selection
Enable checkboxes for multi-selection with hierarchical checkbox states:

```typescript
treeFields = {
  dataSource: this.treeData,
  id: 'id',
  text: 'name',
  child: 'subChild',
  hasChildren: 'hasChild'
};

showCheckBox = true;  // Enable checkboxes
autoCheck = true;     // Parent/child auto-check
```

### Pattern 2: File Browser with Drag-and-Drop
Create an interactive file browser with node reorganization:

```typescript
<ejs-treeview 
  [fields]="treeFields"
  [allowDragAndDrop]="true"
  [allowMultiSelection]="true"
  (nodeDragging)="onNodeDragging($event)"
  (nodeDropped)="onNodeDropped($event)">
</ejs-treeview>
```

### Pattern 3: Search and Filter
Implement real-time filtering of tree nodes:

```typescript
<input 
  type="text" 
  (keyup)="filterTree($event.target.value)" 
  placeholder="Search nodes...">

<ejs-treeview 
  #treeView
  [fields]="filteredFields">
</ejs-treeview>
```

### Pattern 4: Editable Tree
Enable in-place node editing with validation:

```typescript
<ejs-treeview 
  [fields]="treeFields"
  [allowEditing]="true"
  (nodeEditing)="onNodeEditing($event)"
  (nodeEdited)="onNodeEdited($event)">
</ejs-treeview>
```

## Key TreeView Properties

| Property | Type | Purpose |
|----------|------|---------|
| `fields` | Object | Configures data source mapping (id, text, child, parentID, hasChildren, expanded, isChecked, etc.) |
| `dataSource` | Array | Hierarchical or flat data array |
| `allowMultiSelection` | Boolean | Enable multiple node selection |
| `showCheckBox` | Boolean | Display checkboxes before nodes |
| `autoCheck` | Boolean | Auto-check children when parent is checked (default: true) |
| `allowDragAndDrop` | Boolean | Enable drag-and-drop functionality |
| `allowEditing` | Boolean | Enable in-place node editing |
| `loadOnDemand` | Boolean | Load child nodes only when parent expands (default: true) |
| `sortOrder` | String | Sort order: 'Ascending', 'Descending', or 'None' |
| `cssClass` | String | Apply custom CSS class for styling |
| `enableRtl` | Boolean | Enable right-to-left layout support |
| `enablePersistence` | Boolean | Save and restore TreeView state (expanded nodes, selections) |
| `checkedNodes` | Array | Array of node IDs that should be checked |
| `selectedNodes` | Array | Array of node IDs that should be selected |
| `nodeTemplate` | Template | Custom template for rendering nodes |
| `animation` | Object | Configure expand/collapse animations |
| `allowKeyboardNavigation` | Boolean | Enable keyboard navigation (default: true) |

## Common Use Cases

**Organizational Chart**: Display employee hierarchy with parent-child relationships and custom templates showing roles.

**File/Folder Browser**: Show directory structure with drag-and-drop to move files between folders.

**Category Navigation**: Multi-level product categories with checkboxes for filtering and multi-selection.

**Settings Menu**: Hierarchical preferences or configuration options organized by topic.

**Knowledge Base**: Nested documentation topics with search and expand/collapse navigation.

## Reference Files

- `getting-started.md` - Installation, setup, basic initialization
- `data-binding.md` - Data sources, hierarchies, remote data, lazy loading
- `node-selection.md` - Checkboxes, multi-select, selection events
- `node-editing.md` - Editing, adding, removing, updating nodes
- `drag-and-drop.md` - Drag-and-drop configuration and restrictions
- `templating.md` - Custom templates, icons, styling, tooltips
- `filtering-sorting.md` - Filter, search, and sort functionality
- `context-menu.md` - Context menu integration and node operations
- `accessibility-advanced.md` - Keyboard navigation, ARIA, RTL, advanced methods

---

**Next Steps:**
1. Choose your use case from the navigation guide above
2. Read the relevant reference file
3. Adapt code examples to your data structure
4. Test with your data source
