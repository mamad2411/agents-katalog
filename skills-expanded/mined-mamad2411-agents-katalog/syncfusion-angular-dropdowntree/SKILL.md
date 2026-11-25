---
name: syncfusion-angular-dropdowntree
description: |
  Implement Syncfusion Angular Dropdown Tree component for hierarchical data selection with single or multiple values. Use this when selecting items from tree-structured hierarchies, enabling checkboxes for multi-selection, binding hierarchical data, customizing tree items with templates, or implementing parent-child dependent selection. Works with self-referential structures and remote OData/REST endpoints for category selectors and organizational interfaces.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Dropdowns"
---

# Implementing Syncfusion Angular Dropdown Tree

The Dropdown Tree component allows you to select single or multiple values from hierarchical data in a tree-like structure. It provides essential features like data binding, checkboxes, templates, and accessibility, making it ideal for displaying categorized selections, organizational hierarchies, and nested data structures.

## When to Use This Skill

Use the Dropdown Tree component when you need to:

- **Hierarchical Selection** - Allow users to select from nested, tree-structured data (categories, file hierarchies, organizational trees)
- **Multi-Selection** - Enable checkbox-based selection of multiple items with optional auto-check (parent-child sync)
- **Dynamic Data** - Bind local arrays, self-referential structures, or remote OData/REST endpoints
- **Customized Display** - Use item templates, value templates, headers, and footers for rich UI customization
- **Large Datasets** - Support remote data with lazy loading to optimize performance
- **Localization** - Adapt component text and messages for different cultures and languages

## Component Overview

The Dropdown Tree provides a compact dropdown input that expands to show a full tree structure with powerful filtering, selection, and templating capabilities. Unlike flat dropdowns, it maintains hierarchical relationships, enabling intuitive navigation through multi-level data.

**Key Characteristics:**
- Single or multiple item selection
- Checkbox-based multi-selection with optional auto-check
- Local hierarchical and self-referential data binding
- Remote data binding with DataManager (OData, ODataV4, WebAPI)
- Rich templating: items, values, headers, footers, no-records, action-failure
- Built-in accessibility with keyboard navigation and ARIA attributes
- Full localization support

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Dependencies and package setup
- Angular CLI configuration
- Module registration (@syncfusion/ej2-angular-dropdowns)
- CSS imports and theme configuration
- Basic component integration
- First working example with local data

### Data Binding
📄 **Read:** [references/data-binding.md](references/data-binding.md)
- Hierarchical data structure (nested arrays)
- Self-referential data binding (flat arrays with parentValue)
- Remote data with DataManager
- OData and ODataV4 adaptors
- WebAPI adaptor configuration
- Query-based filtering

### Checkbox Features
📄 **Read:** [references/checkbox-features.md](references/checkbox-features.md)
- Enable checkboxes with showCheckBox property
- Multi-selection without UI disruption
- Auto-check hierarchical behavior (parent-child sync)
- Select All feature (showSelectAll with custom labels)
- Checkbox state synchronization
- Intermediate states (partially checked)

### Templates and Customization
📄 **Read:** [references/templates.md](references/templates.md)
- Item template for custom tree item rendering
- Value template for selected item display
- Header and footer templates
- No records and action failure templates
- Custom display template for multi-selection (Custom mode)
- Template expressions and interpolation

### Localization
📄 **Read:** [references/localization.md](references/localization.md)
- Supported localization keys and default messages
- Setting locale and culture
- Customizing locale-specific strings
- Key messages: noRecordsTemplate, actionFailureTemplate, overflowCountTemplate, totalCountTemplate
- Multi-language configuration

### API Reference
📄 **Read:** [references/api-reference.md](references/api-reference.md)
- Core properties and field mappings
- TreeSettings configuration options
- Common events and callbacks
- Best practices for property configuration
- Performance optimization tips

### Methods and Events
📄 **Read:** [references/methods-and-events.md](references/methods-and-events.md)
- Component methods: showPopup(), hidePopup(), refresh(), clearSelection(), expandAll(), collapseAll()
- Selection events: change, select
- Popup events: open, close, beforeOpen
- Data events: dataBound, actionFailure, filtering
- Lifecycle events: created, destroyed
- User interaction events: focus, blur, keyPress
- Event arguments and signatures
- Complete working examples

## Quick Start Example

Here's a minimal working example with hierarchical data:

```typescript
import { Component } from '@angular/core';
import { DropDownTreeModule } from '@syncfusion/ej2-angular-dropdowns';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

@Component({
  selector: 'app-dropdown-tree',
  template: `<ejs-dropdowntree id='dropdowntree' 
                [fields]='fields' 
                placeholder='Select a category'></ejs-dropdowntree>`,
  standalone: true,
  imports: [DropDownTreeModule, FormsModule, ReactiveFormsModule]
})
export class AppComponent {
  // Hierarchical data structure with nested arrays
  public data = [
    {
      nodeId: '01', nodeText: 'Music',
      nodeChild: [
        { nodeId: '01-01', nodeText: 'Gouttes.mp3' }
      ]
    },
    {
      nodeId: '02', nodeText: 'Videos', expanded: true,
      nodeChild: [
        { nodeId: '02-01', nodeText: 'Naturals.mp4' },
        { nodeId: '02-02', nodeText: 'Wild.mpeg' }
      ]
    }
  ];

  // Field mapping: value=nodeId, text=nodeText, child=nodeChild
  public fields = { 
    dataSource: this.data, 
    value: 'nodeId', 
    text: 'nodeText', 
    child: 'nodeChild' 
  };
}
```

## Common Patterns

### Pattern 1: Multi-Selection with Checkboxes

```typescript
@Component({
  template: `<ejs-dropdowntree id='dropdowntree' 
                [fields]='fields' 
                [showCheckBox]='true' 
                [showSelectAll]='true'
                selectAllText='Check All' 
                unSelectAllText='Uncheck All'></ejs-dropdowntree>`,
  standalone: true,
  imports: [DropDownTreeModule, FormsModule, ReactiveFormsModule]
})
export class CheckboxExample {
  public data = [
    { id: 1, name: 'Music', hasChild: true, expanded: true },
    { id: 2, pid: 1, name: 'Hot Singles' },
    { id: 3, pid: 1, name: 'Rising Artists' }
  ];
  public fields = { 
    dataSource: this.data, 
    value: 'id', 
    text: 'name', 
    parentValue: 'pid', 
    hasChildren: 'hasChild' 
  };
}
```

**When to use:** Allow users to select multiple items in a single interaction, with convenient "Select All" option. Use `selectAllText` for unchecked label and `unSelectAllText` for checked label.

### Pattern 2: Auto-Check (Parent-Child Sync)

```typescript
@Component({
  template: `<ejs-dropdowntree [fields]='fields' 
                [showCheckBox]='true' 
                [treeSettings]='{ autoCheck: true }'></ejs-dropdowntree>`
})
export class AutoCheckExample {
  public fields = { dataSource: this.data, /* ... */ };
}
```

**When to use:** Enforce hierarchical consistency—checking a parent automatically checks all children, and unchecking the last child unchecks the parent (intermediate state for partial selection).

### Pattern 3: Remote Data with OData

```typescript
import { DataManager, ODataV4Adaptor, Query } from '@syncfusion/ej2-data';

@Component({
  template: `<ejs-dropdowntree [fields]='fields'></ejs-dropdowntree>`
})
export class RemoteDataExample {
  public data = new DataManager({
    url: 'https://services.odata.org/V4/Northwind/Northwind.svc',
    adaptor: new ODataV4Adaptor,
    crossDomain: true
  });
  
  public fields = {
    dataSource: this.data,
    query: new Query().from('Employees').select('EmployeeID,FirstName').take(5),
    value: 'EmployeeID',
    text: 'FirstName',
    hasChildren: 'EmployeeID'
  };
}
```

**When to use:** Fetch hierarchical data from a remote server, reducing initial load and supporting large datasets.

### Pattern 4: Custom Item Display

```typescript
@Component({
  template: `<ejs-dropdowntree [fields]='fields' 
                [itemTemplate]='itemTemplate'></ejs-dropdowntree>`
})
export class TemplateExample {
  public itemTemplate = '<div><strong>${name}</strong> - ${type}</div>';
  public fields = { dataSource: this.data, /* ... */ };
}
```

**When to use:** Display rich, formatted content for each tree item (names, icons, metadata).

## Key Features

| Feature | Use Case |
|---------|----------|
| **Hierarchical Data** | Organize items in parent-child relationships (categories, departments, file trees) |
| **Checkboxes** | Enable multi-selection without affecting dropdown UI |
| **Auto-Check** | Synchronize parent-child selection states automatically |
| **Remote Binding** | Fetch data from OData, REST APIs, or custom endpoints |
| **Templates** | Customize item display, headers, footers, and selected value format |
| **Accessibility** | Full keyboard navigation, ARIA attributes, screen reader support |
| **Localization** | Support for multiple languages and regional formats |
| **Select All** | Quickly select or deselect all items with a single click |

