---
name: syncfusion-angular-listview
description: Guide for implementing Syncfusion Angular ListView component. Use this skill when building interactive lists with data binding, grouping, templates, selection, events, drag-and-drop, or virtualization features. This skill covers getting started, data binding, customization, selection, advanced features, specialized use cases, styling, and accessibility for building production-ready list interfaces.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "List Components"
---

# Implementing Syncfusion Angular ListView

The Syncfusion Angular ListView component is a feature-rich, interactive component for displaying data in list format. It provides built-in support for data binding, grouping, nested lists, custom templates, selection modes, drag-and-drop, virtualization for large datasets, and comprehensive accessibility features. The component is production-ready and suitable for creating modern, data-driven user interfaces.

## When to Use This Skill

Use this skill when:
- Building interactive list-based interfaces with Angular
- Displaying data from local or remote sources
- Creating grouped or nested list structures
- Customizing list item appearance with templates
- Handling item selection and user interactions
- Implementing specialized patterns (chat windows, checklists, dual-lists)
- Optimizing performance with virtualization for large datasets
- Building accessible list interfaces

## Component Overview

**Package:** `@syncfusion/ej2-angular-lists`

**Key Capabilities:**
- ✅ Local and remote data binding (arrays, DataManager, OData, REST APIs)
- ✅ Grouping and nested list hierarchies
- ✅ Flexible item, header, and group templates
- ✅ Single/multiple selection modes with checkboxes
- ✅ Full event system (select, click, delete, add, remove)
- ✅ Drag-and-drop for item reordering
- ✅ Virtualization for large datasets (1000+ items)
- ✅ AJAX content loading and dynamic templates
- ✅ Integrated paging support
- ✅ Comprehensive theming and styling options
- ✅ WCAG accessibility compliance

---

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Angular CLI setup and project configuration
- Installing @syncfusion/ej2-angular-lists package
- Adding CSS themes and styles
- Creating your first ListView component
- Basic data binding with minimal examples
- Running the application (ng serve)

### Data Binding
📄 **Read:** [references/data-binding.md](references/data-binding.md)
- Binding local data arrays (strings, objects)
- Field configuration and data mapping
- Remote data binding with DataManager
- OData and REST API integration
- Dynamic data updates and refresh strategies
- Field properties: id, text, isChecked, enabled, tooltip, groupBy

### Customization and Templates
📄 **Read:** [references/customization-and-templates.md](references/customization-and-templates.md)
- Header template customization with buttons and search bars
- Item templates with avatars, badges, multi-line layouts
- Group header templates with dynamic content
- Dynamic templates based on device or screen size
- Built-in CSS classes (e-list-template, e-list-wrapper, e-list-avatar, etc.)
- Advanced template patterns with data binding

### Grouping and Nested Lists
📄 **Read:** [references/grouping-and-nested-lists.md](references/grouping-and-nested-lists.md)
- Grouping items by category with groupBy field
- Customizing group headers and templates
- Creating nested list structures for hierarchical data
- Child data binding and expandable groups
- Group header customization with item counts

### Selection and Item Management
📄 **Read:** [references/selection-and-items.md](references/selection-and-items.md)
- Selection modes (single, multiple, checkbox)
- Getting selected items with getSelectedItems() method
- Adding items dynamically with addItem()
- Removing items with removeItem()
- Event handling (select, actionComplete)
- Programmatic selection and deselection

### Advanced Features
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- Virtualization for high-performance large datasets
- Scrolling and scroll position management
- Drag-and-drop for item reordering
- Filtering and searching list items
- Integrating pager component with ListView
- Loading states and spinners during data fetch
- AJAX content loading into list items

### Specialized Use Cases
📄 **Read:** [references/specialized-use-cases.md](references/specialized-use-cases.md)
- Building chat window layouts
- Creating checklist interfaces with checkboxes
- Building dual-list (transfer list) components
- Creating grid-based layouts with ListView
- Rendering hyperlinked navigation lists
- Customizing with dynamic tags and badges
- Mobile contact layout patterns

### Styling and Themes
📄 **Read:** [references/styling-and-themes.md](references/styling-and-themes.md)
- Theme imports (Material3, Bootstrap, Fabric, Tailwind)
- CSS class customization and overrides
- Custom styling for list items and groups
- Responsive design and mobile optimization
- Animation settings and transitions
- RTL (right-to-left) support
- Dark mode theming

### Item Count and Group Headers
📄 **Read:** [references/item-count-and-grouping.md](references/item-count-and-grouping.md)
- Displaying item count in group headers
- Dynamic count calculation and updates
- Group statistics and aggregations
- Advanced group header templates
- Conditional item count display

### Accessibility
📄 **Read:** [references/accessibility.md](references/accessibility.md)
- WCAG 2.1 compliance and keyboard navigation
- ARIA attributes and screen reader support
- Focus management and indicators
- Keyboard shortcuts and navigation patterns
- Color contrast and accessible theming
- Testing accessibility with assistive technologies

### Complete API Reference
📄 **Read:** [references/api-reference.md](references/api-reference.md)
- Properties: animation, enablePersistence, enableRtl, locale, query, and more
- Methods: back(), checkAllItems(), selectMultipleItems(), and complete method suite
- Events: select, scroll, actionBegin, actionComplete, actionFailure with argument details
- Complete working examples for each API
- Quick reference tables for properties, methods, and events

---

## Quick Start Example

```typescript
import { ListViewModule } from '@syncfusion/ej2-angular-lists';
import { Component } from '@angular/core';

@Component({
  imports: [ListViewModule],
  standalone: true,
  selector: 'app-root',
  template: `
    <ejs-listview 
      id='sample-list' 
      [dataSource]='data'>
    </ejs-listview>
  `
})
export class AppComponent {
  // Simple string data
  public data: string[] = [
    'Artwork', 'Abstract', 'Modern Painting', 
    'Ceramics', 'Animation Art', 'Oil Painting'
  ];
}
```

**CSS Import (in styles.css):**
```css
@import "../node_modules/@syncfusion/ej2-base/styles/material3.css";
@import "../node_modules/@syncfusion/ej2-angular-lists/styles/material3.css";
```

**Run:**
```bash
npm install @syncfusion/ej2-angular-lists --save
ng serve --open
```

---

## Common Patterns

### Pattern 1: Data-Driven List with Field Mapping
Use when displaying complex objects with multiple properties:
```typescript
public data = [
  { name: 'John', email: 'john@example.com', id: '1' },
  { name: 'Jane', email: 'jane@example.com', id: '2' }
];
public fields = { text: 'name', id: 'id' };
```

### Pattern 2: Grouped List
Use when organizing items by category:
```typescript
public fields = { text: 'name', groupBy: 'department' };
```

### Pattern 3: Templated List
Use when you need custom layouts:
```html
<ejs-listview [dataSource]='data' cssClass='e-list-template'>
  <ng-template #template let-data="">
    <div class="e-list-wrapper">
      <span>{{ data.name }}</span>
    </div>
  </ng-template>
</ejs-listview>
```

### Pattern 4: Selection with Checkboxes
Use when users need to select multiple items:
```html
<ejs-listview [dataSource]='data' [showCheckBox]='true'></ejs-listview>
```

### Pattern 5: Dynamic Add/Remove
Use for interactive list management:
```typescript
addItem() {
  this.listview.addItem([{ text: 'New Item', id: 'new' }]);
}
removeItem(element: HTMLElement) {
  this.listview.removeItem(element);
}
```

---

## Key Props and Configuration

| Property | Type | Description |
|---|---|---|
| `dataSource` | array/DataManager | The data to display in the list |
| `fields` | object | Field mappings (text, id, groupBy, etc.) |
| `template` | string/function | Custom template for list items |
| `headerTemplate` | string/function | Custom header template |
| `groupTemplate` | string/function | Custom group header template |
| `showCheckBox` | boolean | Show checkboxes for selection (default: false) |
| `showHeader` | boolean | Display ListView header (default: false) |
| `headerTitle` | string | Title for the header |
| `enableVirtualization` | boolean | Enable virtual scrolling for large datasets |
| `enableHtmlSanitizer` | boolean | Sanitize HTML content (default: true) |
| `allowDragAndDrop` | boolean | Enable drag-and-drop reordering |
| `select` | event | Triggered when item is selected |
| `actionComplete` | event | Triggered after add/remove operations |

---

## Common Use Cases

1. **Task Manager** - Dynamic add/remove with checkboxes and drag-drop
2. **Contact Directory** - Multi-line templates with grouping by department
3. **Chat Interface** - Custom templates with avatars and timestamps
4. **Product Catalog** - Virtualization for thousands of products
5. **Navigation Menu** - Nested lists with icons and routing
6. **Checklist** - Checkbox selection with count in headers
7. **Dual-List Transfer** - Two ListViews with move operations
8. **Mobile Navigation** - Touch-friendly, responsive list layout

---

## Next Steps

- **Start here:** [Getting Started](references/getting-started.md)
- **Bind data:** [Data Binding](references/data-binding.md)
- **Build interactive:** [Selection and Items](references/selection-and-items.md)
- **Optimize performance:** [Advanced Features](references/advanced-features.md)
- **Advanced patterns:** [Specialized Use Cases](references/specialized-use-cases.md)

For API reference and detailed documentation, see the [Syncfusion Angular ListView API](https://ej2.syncfusion.com/angular/documentation/api/list-view/).
