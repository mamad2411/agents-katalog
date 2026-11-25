---
name: syncfusion-javascript-dropdowntree
description: "Implement Syncfusion Dropdown Tree control to display hierarchical data in dropdown format. Use this skill when implementing single or multiple value selection from hierarchical data, enabling checkboxes with dependent parent-child states, lazy-loading large datasets, customizing tree items with templates, and configuring multi-language support. Comprehensive coverage of properties, methods, events, data binding modes, checkbox selection, templates, and accessibility features."
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Dropdown Components"
---

# Implementing Syncfusion Dropdown Tree

---

## When to Use This Skill

Use the Dropdown Tree control when you need to:

- **Display hierarchical data** in a compact dropdown format with tree-like structure
- **Enable multiple selections** from tree items with checkbox support
- **Load large datasets on-demand** (lazy loading) to optimize performance
- **Customize tree appearance** with item templates, headers, and footers
- **Handle parent-child dependencies** with automatic checkbox propagation
- **Support multiple languages** with localization features
- **Provide keyboard navigation** and accessibility for users with assistive technologies

The Dropdown Tree is ideal for scenarios like organizational hierarchies, category selections, location/region pickers, and permission/role management interfaces.

---

## Component Overview

The **Syncfusion Dropdown Tree** control allows you to select single or multiple values from hierarchical data displayed in a tree structure. Key features include:

- **Data Binding**: Local (hierarchical/self-referential) and remote (OData, Web API, DataManager)
- **Checkboxes**: Multi-select with optional parent-child auto-check behavior
- **Select All**: Built-in checkbox in header to select/deselect all items
- **Templates**: Customize items, values, headers, footers, and no-records content
- **Lazy Loading**: Load child data on-demand to reduce initial bandwidth
- **Sorting**: Display items in ascending/descending order
- **Filtering**: Search and filter tree items dynamically
- **Localization**: Multi-language support with text customization
- **Accessibility**: Keyboard navigation and screen reader support
- **Multi-Selection Modes**: Box, Delimiter, Default, or Custom display modes

---

## Documentation Navigation

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and package dependencies
- Development environment setup
- CSS imports and theme configuration
- Basic HTML initialization
- Creating your first Dropdown Tree with TypeScript and ES5 examples

### Data Binding and Tree Structure
📄 **Read:** [references/data-binding.md](references/data-binding.md)
- Local data binding with hierarchical structure
- Self-referential data binding patterns
- Remote data binding (OData, Web API, DataManager)
- Load on demand (lazy loading) configuration
- Field mapping and data structure requirements
- Practical examples with different data sources

### Checkbox Features and Selection
📄 **Read:** [references/checkbox-features.md](references/checkbox-features.md)
- Enable checkboxes with showCheckBox property
- Single item selection
- Auto-check propagation for parent-child items
- Select All functionality in the popup header
- Customizing Select All text and behavior
- Managing selected items programmatically

### Templates and Customization
📄 **Read:** [references/templates-and-customization.md](references/templates-and-customization.md)
- Item template for custom list rendering
- Value template for selected value display
- Header template for popup header customization
- Footer template for popup footer content
- No Records template for empty state handling
- Action Failure template for error scenarios
- Template expression syntax and best practices

### Localization and Accessibility
📄 **Read:** [references/localization-and-accessibility.md](references/localization-and-accessibility.md)
- Localization library setup and usage
- Multi-language text customization
- Default and custom locale configurations
- Keyboard navigation support
- Screen reader compatibility
- WCAG accessibility features

---

## Quick Start Example

### Basic Setup (TypeScript)

```typescript
import { DropDownTree } from '@syncfusion/ej2-dropdowns';

// Define hierarchical data
let continents = [
    {
        code: 'AF', 
        name: 'Africa', 
        countries: [
            { code: 'NGA', name: 'Nigeria' },
            { code: 'EGY', name: 'Egypt' }
        ]
    },
    {
        code: 'AS', 
        name: 'Asia',
        expanded: true,
        countries: [
            { code: 'IND', name: 'India', selected: true },
            { code: 'JPN', name: 'Japan' }
        ]
    }
];

// Initialize Dropdown Tree
let ddtree = new DropDownTree({
    fields: { 
        dataSource: continents, 
        value: 'code', 
        text: 'name', 
        child: 'countries' 
    }
});

ddtree.appendTo('#ddtElement');
```

### HTML Element

```html
<input type="text" id="ddtElement" />
```

---

## Core Concepts

### 1. Hierarchical Data Structure

Hierarchical data uses nested arrays to represent parent-child relationships:

```typescript
let hierarchicalData = [
    {
        id: 1,
        name: 'Parent Item',
        children: [
            { id: 2, name: 'Child 1' },
            { id: 3, name: 'Child 2' }
        ]
    }
];
```

### 2. Self-Referential Data Structure

Self-referential data uses parent ID references:

```typescript
let selfRefData = [
    { id: 1, name: 'Parent', parentId: null },
    { id: 2, name: 'Child 1', parentId: 1 },
    { id: 3, name: 'Child 2', parentId: 1 }
];
```

### 3. Single vs. Multiple Selection

- **Single Selection**: Users can select one item (default behavior)
- **Multiple Selection**: Enable with `allowMultiSelection: true` or `showCheckBox: true`

### 4. Parent-Child Checkbox Dependency

When `autoCheck: true` in `treeSettings`:
- Checking a parent auto-checks all children
- Unchecking a parent auto-unchecks all children
- Mixed states (intermediate) occur when only some children are checked

---

## FieldsModel Configuration

The `fields` property uses `FieldsModel` to map data source fields to Dropdown Tree properties.

### FieldsModel Properties

| Property | Type | Description | Example |
|----------|------|-------------|---------|
| `dataSource` | DataManager \| Object[] | Array of data or DataManager instance | `[{...}, {...}]` |
| `value` | string | Field name for item value/ID | `'id'` or `'code'` |
| `text` | string | Field name for display text | `'name'` or `'title'` |
| `child` | string \| FieldsModel | Field name for child collection (hierarchical) | `'children'` or `'items'` |
| `parentValue` | string | Field name for parent reference (self-referential) | `'parentId'` or `'pid'` |
| `hasChildren` | string | Field name indicating if item has children | `'hasChild'` or `'hasItems'` |
| `expanded` | string | Field name for expanded state | `'expanded'` or `'isExpanded'` |
| `selected` | string | Field name for selected state | `'selected'` or `'isSelected'` |
| `iconCss` | string | Field name for icon CSS class | `'iconClass'` |
| `imageUrl` | string | Field name for image URL | `'imageUrl'` or `'icon'` |
| `htmlAttributes` | string | Field name for HTML attributes | `'htmlAttrs'` |
| `tooltip` | string | Field name for tooltip text | `'title'` or `'tooltip'` |
| `selectable` | string | Field name for item selectability | `'canSelect'` |
| `query` | Query | External query for DataManager | Custom Query object |
| `tableName` | string | Table name for server-side data | `'EmployeeTable'` |

### FieldsModel Examples

#### Hierarchical Data with Custom Fields
```typescript
let ddtree = new DropDownTree({
    fields: {
        dataSource: hierarchicalData,
        value: 'id',
        text: 'name',
        child: 'subitems',
        expanded: 'isExpanded',
        iconCss: 'iconClass'
    }
});
ddtree.appendTo('#ddtElement');
```

#### Self-Referential Data
```typescript
let ddtree = new DropDownTree({
    fields: {
        dataSource: selfRefData,
        value: 'id',
        text: 'name',
        parentValue: 'parentId',
        hasChildren: 'hasChild'
    }
});
ddtree.appendTo('#ddtElement');
```

#### Remote Data with OData
```typescript
import { DataManager, ODataV4Adaptor } from '@syncfusion/ej2-data';

let ddtree = new DropDownTree({
    fields: {
        dataSource: new DataManager({
            url: 'https://services.odata.org/V4/Northwind/Northwind.svc/Employees',
            adaptor: new ODataV4Adaptor()
        }),
        value: 'EmployeeID',
        text: 'FirstName',
        hasChildren: 'EmployeeID'
    }
});
ddtree.appendTo('#ddtElement');
```

---

## TreeSettingsModel Configuration

The `treeSettings` property uses `TreeSettingsModel` to configure tree-specific behavior.

### TreeSettingsModel Properties

| Property | Type | Description | Default |
|----------|------|-------------|---------|
| `loadOnDemand` | boolean | Enable lazy loading of child items | `false` |
| `autoCheck` | boolean | Enable parent-child checkbox dependency | `false` |
| `checkDisabledChildren` | boolean | Include disabled children in parent check | `false` |
| `expandOn` | ExpandOn | Trigger for expand/collapse action | `ExpandOn.Auto` |

### ExpandOn Enum Values

| Value | Description |
|-------|-------------|
| `Auto` | Double-click on desktop, single-tap on mobile |
| `Click` | Single-click/tap on both desktop and mobile |
| `DblClick` | Double-click/tap on both desktop and mobile |
| `None` | Expand/collapse disabled |

### TreeSettingsModel Examples

#### Lazy Loading Configuration
```typescript
let ddtree = new DropDownTree({
    fields: { dataSource: data, value: 'id', text: 'name', parentValue: 'pid' },
    treeSettings: {
        loadOnDemand: true  // Children load when parent expands
    }
});
ddtree.appendTo('#ddtElement');
```

#### Auto-Check with Disabled Children Support
```typescript
let ddtree = new DropDownTree({
    fields: { dataSource: data, value: 'id', text: 'name', parentValue: 'pid' },
    showCheckBox: true,
    treeSettings: {
        autoCheck: true,
        checkDisabledChildren: true  // Disabled items get checked too
    }
});
ddtree.appendTo('#ddtElement');
```

#### Custom Expand Trigger
```typescript
let ddtree = new DropDownTree({
    fields: { dataSource: data, value: 'id', text: 'name', parentValue: 'pid' },
    treeSettings: {
        expandOn: 'Click'  // Single-click to expand/collapse
    }
});
ddtree.appendTo('#ddtElement');
```

---

## 📋 API Properties Reference

> 📄 Complete API properties documentation with examples and type specifications

### 🔗 [**Open api-properties.md**](references/api-properties.md)

**What's Inside:**
- ✅ **55+ Properties** - Every property documented with type, default value, and description
- ✅ **10 Categories** - Essential, Selection, Templates, Popup, Filtering, Sorting, Styling, State, HTML Security, Localization
- ✅ **100+ Examples** - Real-world code samples for each property
- ✅ **Type Specifications** - Complete type info and default values
- ✅ **Best Practices** - Usage patterns and recommendations

---

## 🔧 API Methods Reference

> 📄 Complete API methods documentation with parameter details and examples

### 🔗 [**Open api-methods.md**](references/api-methods.md)

**What's Inside:**
- ✅ **16 Methods** - All component methods fully documented
- ✅ **6 Categories** - Lifecycle, Data & Value, Popup, DOM, Event Management, Module Injection
- ✅ **Parameter Specs** - Complete parameter types, descriptions, and return types
- ✅ **Working Examples** - Production-ready code for each method
- ✅ **Use Cases** - When and how to use each method

---

## 🎯 API Events Reference

> 📄 Complete API events documentation with event argument properties and examples

### 🔗 [**Open api-events.md**](references/api-events.md)

**What's Inside:**
- ✅ **13 Events** - All component events fully documented
- ✅ **7 Categories** - Selection, Data, Filtering, Popup, Focus, Keyboard, Lifecycle
- ✅ **8 Event Argument Types** - Complete property mappings (30+ properties)
- ✅ **Event Details** - When each event triggers and what data it provides
- ✅ **Real Examples** - Practical event handling implementations

---

## Common Patterns

### Pattern 1: Multiple Selection with Checkboxes

```typescript
let ddtree = new DropDownTree({
    fields: { dataSource: data, value: 'id', text: 'name', parentValue: 'pid' },
    showCheckBox: true,
    showSelectAll: true,
    treeSettings: { autoCheck: true },
    change: (args) => {
        console.log('Selected items:', args.value);
    }
});
ddtree.appendTo('#ddtElement');
```

**Use when**: User needs to select multiple items with parent-child dependency.

### Pattern 2: Load Large Datasets On-Demand

```typescript
let ddtree = new DropDownTree({
    fields: { 
        dataSource: dataManager, 
        value: 'id', 
        text: 'name',
        parentValue: 'parentId'
    },
    treeSettings: { loadOnDemand: true }
});
ddtree.appendTo('#ddtElement');
```

**Use when**: Working with large hierarchies (1000+ items).

### Pattern 3: Custom Item Display with Templates

```typescript
let ddtree = new DropDownTree({
    fields: { dataSource: data, text: 'name', value: 'id' },
    itemTemplate: '<div class="item-row"><span>${name}</span> <small>${department}</small></div>',
    valueTemplate: '<span class="selected-badge">${name}</span>'
});
ddtree.appendTo('#ddtElement');
```

**Use when**: Need to display additional data fields.

### Pattern 4: Remote Data with Filtering

```typescript
import { DataManager, ODataV4Adaptor } from '@syncfusion/ej2-data';

let ddtree = new DropDownTree({
    fields: {
        dataSource: new DataManager({
            url: 'https://api.example.com/items',
            adaptor: new ODataV4Adaptor()
        }),
        value: 'id',
        text: 'name'
    },
    allowFiltering: true,
    filterBarPlaceholder: 'Search items...',
    filterType: 'Contains'
});
ddtree.appendTo('#ddtElement');
```

**Use when**: Fetching data from remote service with search capability.

### Pattern 5: Customized Select All with Delimiter Mode

```typescript
let ddtree = new DropDownTree({
    fields: { dataSource: data, value: 'id', text: 'name', parentValue: 'pid' },
    showCheckBox: true,
    showSelectAll: true,
    selectAllText: 'Select All Items',
    unSelectAllText: 'Clear All',
    mode: 'Delimiter',
    delimiterChar: '; ',
    allowMultiSelection: true
});
ddtree.appendTo('#ddtElement');
```

**Use when**: Want friendly checkbox text and delimited display.

### Pattern 6: Dynamic Data Update

```typescript
let ddtree = new DropDownTree({
    fields: { dataSource: [], value: 'id', text: 'name', child: 'items' }
});
ddtree.appendTo('#ddtElement');

// Later, update data
let newData = [{ id: 1, name: 'Item 1', items: [] }];
ddtree.fields.dataSource = newData;
ddtree.refresh();  // Re-render
```

**Use when**: Data changes dynamically after initialization.

### Pattern 7: Programmatic Value Setting with Validation

```typescript
let ddtree = new DropDownTree({
    fields: { dataSource: data, value: 'id', text: 'name', child: 'items' },
    showCheckBox: true,
    change: (args) => {
        if (args.value.length > 5) {
            console.warn('Maximum 5 items can be selected');
            // Reset to previous value
            ddtree.value = args.oldValue;
        }
    }
});
ddtree.appendTo('#ddtElement');
```

**Use when**: Need to enforce selection constraints.

---

## Use Cases & Implementation Guide

### Organizational Hierarchy Navigation

**Scenario**: Department/Employee selection with multi-select and role assignment

```typescript
let employees = [
    { id: 1, name: 'IT Department', hasChild: true },
    { id: 2, pid: 1, name: 'John Doe', department: 'IT' },
    { id: 3, pid: 1, name: 'Jane Smith', department: 'IT' },
    { id: 4, name: 'HR Department', hasChild: true },
    { id: 5, pid: 4, name: 'Mike Johnson', department: 'HR' }
];

let ddtree = new DropDownTree({
    fields: { 
        dataSource: employees, 
        value: 'id', 
        text: 'name', 
        parentValue: 'pid',
        hasChildren: 'hasChild'
    },
    showCheckBox: true,
    treeSettings: { autoCheck: true },
    itemTemplate: '<div>${name} <span class="text-muted">${department}</span></div>',
    change: (args) => {
        assignRolesToSelectedEmployees(args.value);
    }
});
ddtree.appendTo('#employeeSelection');
```

### Geographic Location/Region Selection

**Scenario**: Country → State → City selection with lazy loading

```typescript
import { DataManager, WebApiAdaptor } from '@syncfusion/ej2-data';

let ddtree = new DropDownTree({
    fields: {
        dataSource: new DataManager({
            url: 'api/locations',
            adaptor: new WebApiAdaptor()
        }),
        value: 'id',
        text: 'name',
        parentValue: 'parentId',
        hasChildren: 'hasChildren'
    },
    treeSettings: { 
        loadOnDemand: true  // Load children on demand
    },
    allowFiltering: true,
    filterBarPlaceholder: 'Search locations...',
    change: (args) => {
        updateMapWithSelectedLocation(args.value);
    }
});
ddtree.appendTo('#locationPicker');
```

### Category-Based Product Filtering

**Scenario**: Display product categories with item counts and icons

```typescript
let categories = [
    { 
        id: 'cat1', 
        name: 'Electronics', 
        count: 125,
        icon: 'e-icons e-mobile',
        products: [
            { id: 'prod1', name: 'Mobile Phones', count: 45, icon: 'e-icons e-phone' },
            { id: 'prod2', name: 'Laptops', count: 30, icon: 'e-icons e-laptop' }
        ]
    }
];

let ddtree = new DropDownTree({
    fields: { 
        dataSource: categories, 
        value: 'id', 
        text: 'name', 
        child: 'products',
        iconCss: 'icon'
    },
    itemTemplate: `
        <div class="category-item">
            <i class="\${icon}"></i>
            <span>\${name}</span>
            <span class="badge">\${count}</span>
        </div>
    `,
    change: (args) => {
        filterProductsByCategories(args.value);
    }
});
ddtree.appendTo('#categorySelector');
```

### Permission/Role Management

**Scenario**: Multi-level permission hierarchy with selective enabling

```typescript
let permissions = [
    { id: 'admin', name: 'Admin', hasChild: true },
    { id: 'admin-users', pid: 'admin', name: 'Manage Users' },
    { id: 'admin-system', pid: 'admin', name: 'System Settings' },
    { id: 'user', name: 'User', hasChild: true, disabled: true },
    { id: 'user-profile', pid: 'user', name: 'Edit Profile' }
];

let ddtree = new DropDownTree({
    fields: { 
        dataSource: permissions, 
        value: 'id', 
        text: 'name', 
        parentValue: 'pid',
        hasChildren: 'hasChild'
    },
    showCheckBox: true,
    showSelectAll: true,
    selectAllText: 'Grant All Permissions',
    unSelectAllText: 'Revoke All Permissions',
    treeSettings: { autoCheck: true },
    change: (args) => {
        savePermissionsToRole(args.value);
    }
});
ddtree.appendTo('#permissionSelector');
```

---

## Next Steps

1. **Start with [references/getting-started.md](references/getting-started.md)** to install dependencies and create your first control
2. **Choose your data source** and follow the appropriate pattern in [references/data-binding.md](references/data-binding.md)
3. **Enable checkboxes** if multi-selection is needed ([references/checkbox-features.md](references/checkbox-features.md))
4. **Customize appearance** with templates as required ([references/templates-and-customization.md](references/templates-and-customization.md))
5. **Reference this API documentation** as needed during implementation

For implementation assistance with specific features or advanced scenarios, reference the appropriate guide above.

