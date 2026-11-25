---
name: syncfusion-aspnetcore-tree-view
description: Implement the Syncfusion ASP.NET Core TreeView component for hierarchical data visualization. Use this when working with tree structures, node selection, checkboxes, or drag-and-drop operations. This skill covers data binding, node editing, and advanced tree configurations.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Navigation Components"
---

# Implementing Syncfusion Core TreeView

## When to Use This Skill

Use this skill when you need to:

- **Display hierarchical data structures** - Render organizational charts, file systems, category trees, or any nested data in a tree format
- **Enable user selection** - Implement single or multi-select functionality with keyboard and mouse interactions
- **Build interactive trees** - Add drag-and-drop, node editing, checkboxes, and dynamic node manipulation
- **Customize appearance** - Apply templates, icons, animations, and styling to match your application design
- **Handle tree events** - Respond to node interactions with expand/collapse, selection, and editing events
- **Implement load-on-demand** - Optimize performance for large datasets by loading child nodes only when parent nodes expand
- **Create accessibility-compliant interfaces** - Ensure keyboard navigation and screen reader support for users with accessibility needs

## Component Overview

The **Syncfusion TreeView** is an enterprise-grade component that displays hierarchical data in a tree structure with powerful interactive features. It supports local and remote data binding, multiple selection modes, drag-and-drop operations, node editing, checkboxes, and comprehensive event handling.

### Key Capabilities

- **Data Binding**: Support for hierarchical data, self-referential data, local arrays, and remote data services (OData, Web API, DataManager)
- **Node Interactions**: Single selection, multi-selection (Ctrl/Shift keys), keyboard navigation (arrow keys, F2, Delete)
- **Selection Types**: Full row selection, node text selection, checkbox selection, independent node states
- **Dynamic Operations**: Add, remove, update, refresh, and move nodes programmatically
- **Editing**: In-place editing with double-click or F2 key, with validation support
- **Drag-and-Drop**: Full drag-and-drop support with visual indicators and multi-node dragging
- **Checkboxes**: Parent-child dependency, auto-check propagation, independent states
- **Customization**: Node templates, custom icons, CSS styling, animation effects
- **Performance**: Load-on-demand rendering for large datasets, lazy loading of child nodes
- **Accessibility**: Full keyboard support, ARIA attributes, screen reader compatibility

## Documentation and Navigation Guide

Use this guide to navigate to the specific TreeView feature you need to implement:

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)

When you need to:
- Set up TreeView in your application for the first time
- Understand basic component initialization and configuration
- Learn prerequisite setup and installation steps
- See your first working TreeView example

### Data Binding and Field Configuration
📄 **Read:** [references/data-binding-and-fields.md](references/data-binding-and-fields.md)

When you need to:
- Bind data from local arrays or remote services
- Configure hierarchical or self-referential data structures
- Map data source fields to TreeView properties
- Implement remote data binding with DataManager
- Handle load-on-demand scenarios

### Node Selection (Single and Multi-Select)
📄 **Read:** [references/node-selection.md](references/node-selection.md)

When you need to:
- Enable single node selection
- Implement multi-selection with Ctrl and Shift keys
- Track selected nodes programmatically
- Respond to selection events
- Prevent selection for specific nodes

### Node Expansion and Collapsing
📄 **Read:** [references/node-expansion.md](references/node-expansion.md)

When you need to:
- Control node expand/collapse behavior
- Configure expand-on-click or double-click
- Handle expand/collapse events
- Manage expanded nodes state
- Implement load-on-demand expansion

### Checkboxes and Checked Nodes
📄 **Read:** [references/checkboxes-and-checked-nodes.md](references/checkboxes-and-checked-nodes.md)

When you need to:
- Enable checkboxes in TreeView nodes
- Track checked nodes and their states
- Implement auto-check for parent-child relationships
- Configure independent node check states
- Handle checkbox change events

### Drag and Drop Operations
📄 **Read:** [references/drag-and-drop.md](references/drag-and-drop.md)

When you need to:
- Enable drag-and-drop functionality
- Handle single and multi-node dragging
- Control drop zones and restrictions
- Respond to drag-drop lifecycle events
- Prevent dragging for specific nodes

### Node Editing and Validation
📄 **Read:** [references/node-editing.md](references/node-editing.md)

When you need to:
- Enable in-place node text editing
- Implement edit mode with double-click or F2
- Validate node text during editing
- Prevent editing for specific nodes
- Save or cancel edit operations

### Templates and Styling
📄 **Read:** [references/templates-and-styling.md](references/templates-and-styling.md)

When you need to:
- Customize node appearance with templates
- Apply custom icons and images
- Configure animations and transitions
- Implement full-row selection styling
- Use CSS classes for TreeView customization

### Node Manipulation and Dynamic Operations
📄 **Read:** [references/node-manipulation.md](references/node-manipulation.md)

When you need to:
- Add new nodes programmatically
- Remove existing nodes
- Update node text or properties
- Refresh node content
- Move nodes to different positions
- Get tree data programmatically

### Events and Keyboard Navigation
📄 **Read:** [references/events-and-keyboard-navigation.md](references/events-and-keyboard-navigation.md)

When you need to:
- Handle all TreeView events (expand, select, check, drag, edit)
- Implement keyboard navigation support
- Respond to user interactions
- Prevent default behavior for specific actions
- Track component lifecycle events

### Complete API Reference
📄 **Read:** [references/api-reference.md](references/api-reference.md)

When you need to:
- Look up specific property definitions and default values
- Find method signatures with parameter descriptions
- Understand event handler parameters and structure
- Reference FieldsSettings configuration options
- Check AnimationSettings for expand/collapse effects
- Get complete API documentation with code examples for all properties, methods, and events

## Quick Start Example

Here's a minimal example to get TreeView running immediately:

```html
<ejs-treeview id="treeAdvanced" showCheckBox="true" 
    allowMultiSelection="true" allowDragAndDrop="true" allowEditing="true">
    <e-treeview-fields dataSource="ViewBag.dataSource" id="id" parentId="pid" text="name" hasChildren="hasChild"></e-treeview-fields>
</ejs-treeview>
```

## Common Patterns

### Pattern 1: Single Selection with Event Handling

```html
<ejs-treeview id="treeAdvanced" allowMultiSelection="false">
    <e-treeview-fields dataSource="ViewBag.dataSource" id="id" parentId="pid" text="name" hasChildren="hasChild"></e-treeview-fields>
</ejs-treeview>
```

### Pattern 2: Multi-Select with Checkboxes

```html
<ejs-treeview id="treeAdvanced" showCheckBox="true" 
    allowMultiSelection="true">
    <e-treeview-fields dataSource="ViewBag.dataSource" id="id" parentId="pid" text="name" hasChildren="hasChild"></e-treeview-fields>
</ejs-treeview>
```

### Pattern 3: Lazy Loading with Load-on-Demand

```html
<ejs-treeview id="treeAdvanced" loadOnDemand="true">
    <e-treeview-fields dataSource="ViewBag.dataSource" id="id" parentId="pid" text="name" hasChildren="hasChild"></e-treeview-fields>
</ejs-treeview>
```

### Pattern 4: Editable Tree with Validation

```html
<ejs-treeview id="treeRestricted" allowEditing="true" nodeEditing="nodeEditing" nodeEdited="nodeEdited">
    <e-treeview-fields dataSource="ViewBag.dataSource" id="id" text="name"></e-treeview-fields>
</ejs-treeview>

<script>
    function nodeEditing(args) {
        if (args.newText.length < 3) {
          args.cancel = true;
        }
    }
    function nodeEdited(args) {
      console.log('Node text updated to:', args.newText);
    }
</script>
```

### Pattern 5: Drag-Drop with Restrictions

```html
<ejs-treeview id="treeNodeDrag" allowDragAndDrop="true" 
    nodeDragStart="onDragStart" 
    nodeDropped="nodeDropped">
    <e-treeview-fields dataSource="ViewBag.dataSource" id="id" text="name"></e-treeview-fields>
</ejs-treeview>

<script>
    function onDragStart(args) {
      if (!args.nodeData.pid) {
          args.cancel = true;
      }
    }
    
    function nodeDropped(args) {
        console.log('Node dropped successfully');
    }
</script>
```

## Key Props Reference

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `fields` | FieldsSettings | - | Configure data source and field mappings |
| `dataSource` | array \| DataManager | [] | Data source for TreeView nodes |
| `showCheckBox` | boolean | false | Show checkboxes for node selection |
| `allowMultiSelection` | boolean | false | Enable multi-node selection |
| `allowDragAndDrop` | boolean | false | Enable drag-and-drop operations |
| `allowEditing` | boolean | false | Enable in-place node editing |
| `allowTextWrap` | boolean | false | Wrap node text for overflow |
| `loadOnDemand` | boolean | true | Load child nodes on parent expand |
| `fullRowSelect` | boolean | false | Select entire row instead of text |
| `fullRowNavigable` | boolean | false | Navigate entire row with keyboard |
| `expandOn` | string | 'Click' | Action to expand/collapse (Click, DblClick, None) |
| `sortOrder` | string | 'None' | Sort nodes (None, Ascending, Descending) |
| `selectedNodes` | string[] | [] | Selected node IDs |
| `checkedNodes` | string[] | [] | Checked node IDs |
| `expandedNodes` | string[] | [] | Expanded node IDs |
| `cssClass` | string | '' | Custom CSS classes |
| `disabled` | boolean | false | Disable TreeView interaction |
| `enablePersistence` | boolean | false | Persist state between page reloads |
| `enableRtl` | boolean | false | Right-to-left rendering |

## Common Use Cases

### Use Case 1: File Manager Tree
Display a hierarchical file system with folders and files, enabling users to browse, select, and manage files.

**Key Features**: Hierarchical data, icons for file/folder types, multi-select, drag-drop for moving files, context menu for operations.

**Related References**: data-binding-and-fields.md, templates-and-styling.md, drag-and-drop.md

### Use Case 2: Organizational Chart
Show company hierarchy with employees organized by departments and teams.

**Key Features**: Hierarchical data, node templates for employee details, search/filter, single selection, expand/collapse.

**Related References**: data-binding-and-fields.md, templates-and-styling.md, node-selection.md

### Use Case 3: Permission/Role Management
Display hierarchical permissions or roles where users select multiple permissions for roles.

**Key Features**: Checkboxes, multi-select, parent-child dependency, auto-check propagation, checkbox events.

**Related References**: checkboxes-and-checked-nodes.md, node-selection.md

### Use Case 4: Product Category Browser
Browse product categories with filtering and search capability.

**Key Features**: Large dataset with load-on-demand, single selection, keyboard navigation, expand-on-click.

**Related References**: data-binding-and-fields.md, node-expansion.md, events-and-keyboard-navigation.md

### Use Case 5: Menu Structure Editor
Allow administrators to create and edit hierarchical menu structures.

**Key Features**: Node editing, add/remove/move nodes, templates, drag-drop, in-place editing with validation.

**Related References**: node-manipulation.md, node-editing.md, templates-and-styling.md

## Summary

The Syncfusion TreeView component provides a complete solution for displaying and interacting with hierarchical data. It combines powerful data binding capabilities with rich interactive features like multi-selection, drag-and-drop, editing, and checkboxes. With extensive customization options through templates and styling, you can create sophisticated tree-based interfaces that meet any business requirement.

Start with the **Getting Started** reference to set up your first TreeView, then explore specific features using the documentation guide above based on your requirements.

---

**Next Steps**: Choose your first task from the **Documentation and Navigation Guide** section and follow the reference guide to implement your TreeView feature.
