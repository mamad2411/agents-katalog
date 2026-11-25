---
name: syncfusion-angular-kanban
description: Create and manage interactive Kanban boards with Syncfusion Angular component. Use this skill when you need to build workflow visualization tools with drag-and-drop cards, swimlanes, columns, and real-time data binding. Covers setup, configuration, events, properties, methods, and best practices for implementing task management and project tracking interfaces.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Data Visualization"
---

# Implementing Syncfusion Angular Kanban

## When to Use This Skill

The Syncfusion Angular Kanban component is essential when you need to:

- **Visualize workflows** - Display task stages (To Do → In Progress → Testing → Done)
- **Enable task management** - Allow users to organize and track work across multiple columns
- **Implement drag-and-drop** - Let users move cards between columns to change task status
- **Group tasks** - Use swimlanes to organize cards by owner, priority, or category
- **Set constraints** - Enforce WIP (Work In Progress) limits with min/max card counts
- **Customize appearance** - Apply templates, themes, and custom styling to cards and columns
- **Handle events** - Listen to card clicks, drag operations, and state changes
- **Persist state** - Save board configuration and card positions

## Component Overview

The Kanban board is a visual workflow management tool built with:

- **Cards** - Represent individual tasks (mapped to dataSource via `cardSettings`)
- **Columns** - Define workflow stages (mapped using `keyField` and column configuration)
- **Swimlanes** - Group cards by category (employee, priority, etc.)
- **Drag-and-drop** - Enabled by default (`allowDragAndDrop: true`)
- **Data Binding** - Supports local arrays and remote DataManager
- **Templates** - Customize card, column header, swimlane header, and tooltip rendering
- **Responsive** - Adapts layout to desktop and mobile devices
- **Themes** - Five built-in themes: Material, Bootstrap 3, Bootstrap 4, Fabric, High Contrast

## Key Features

✓ **Multi-column workflow** with customizable headers  
✓ **Smooth drag-and-drop** between columns and within columns  
✓ **Swimlane grouping** by any data field  
✓ **WIP validation** (min/max card counts per column/swimlane)  
✓ **Templates** for cards, columns, swimlanes, dialogs, and tooltips  
✓ **Local & remote data binding** with DataManager integration  
✓ **Keyboard navigation** and full accessibility support  
✓ **Events** for user interactions (click, drag, selection, dialog open/close)  
✓ **Methods** for programmatic control (add/delete cards, show/hide columns)  
✓ **Multiple selection modes** (single or multiple card selection)  
✓ **Stacked headers** for grouping related columns  
✓ **Built-in themes** with CSS customization support  

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and npm package setup
- Angular module imports and configuration
- CSS imports and theme registration
- Basic Kanban initialization with minimal example
- First running board with sample data

### Core Structure: Columns and Swimlanes
📄 **Read:** [references/columns-and-swimlanes.md](references/columns-and-swimlanes.md)
- Column configuration with keyField mapping
- Single-key vs. multi-key column mapping
- Column headers and stacked headers
- Swimlane grouping by field
- Dynamic column add/remove/show/hide

### Cards and Data Binding
📄 **Read:** [references/cards-and-data-binding.md](references/cards-and-data-binding.md)
- Card structure: header field, content field, grabber field
- Card templates and custom rendering
- Local array data binding
- Remote data binding with DataManager
- OData v4 support
- Card selection modes (single/multiple)

### Drag-and-Drop and Interaction
📄 **Read:** [references/drag-and-drop.md](references/drag-and-drop.md)
- Drag-and-drop functionality (enabled by default)
- Card movement between columns
- Reordering within columns
- transitionColumns to control valid transitions
- Drag events (beforeDragStart, dragStart, dragStop)
- WIP limits: enforcing min/max card counts
- Keyboard navigation support

### Features and Customization
📄 **Read:** [references/features-and-customization.md](references/features-and-customization.md)
- Sorting, filtering, and searching cards
- Validation rules and dialogs
- Responsive mode for mobile
- Custom dialog templates
- Tooltip templates and configuration
- Priority indicators and color grabbers
- Column toggling and collapsing

### Properties Reference
📄 **Read:** [references/properties.md](references/properties.md)
- Core properties: allowDragAndDrop, allowKeyboard, allowSelection
- Card configuration: cardSettings (headerField, contentField, template, etc.)
- Column setup: columns array with ColumnsModel
- Swimlane configuration: swimlaneSettings
- Dialog and tooltip templates
- WIP limits: minCount, maxCount per column
- Responsive breakpoints and heights

### Methods Reference
📄 **Read:** [references/methods.md](references/methods.md)
- Card operations: addCard(), deleteCard(), updateCard(), getSelectedCards()
- Column operations: addColumn(), removeColumn(), hideColumn(), showColumn()
- Board operations: refresh(), getCardCount()
- Swimlane operations: getSwimlaneData()
- Dialog control: openDialog(), closeDialog()
- Search/Filter: search(), filter(), sortBy()

### Events Reference
📄 **Read:** [references/events.md](references/events.md)
- Action events: actionBegin, actionComplete, actionFailure
- Card events: cardClick, cardDoubleClick, cardSelection
- Drag events: dragStart, dragStop, beforeDragStart
- Dialog events: dialogOpen, dialogClose
- Column/swimlane events: columnClick, swimlaneClick
- Event argument types and data structures

### Data Persistence and State
📄 **Read:** [references/data-persistence.md](references/data-persistence.md)
- Local storage persistence for board state
- Saving card positions and column state
- ObservableCollection integration
- State restoration after page reload
- Manual state save/restore patterns

### Styling, Themes, and Appearance
📄 **Read:** [references/styling-and-theming.md](references/styling-and-theming.md)
- Built-in themes (Material, Bootstrap 3/4, Fabric, High Contrast)
- CSS variable customization
- Card and column custom styling
- Dark mode support
- RTL (right-to-left) language support
- Theme Studio integration

### Accessibility and Internationalization
📄 **Read:** [references/accessibility-and-localization.md](references/accessibility-and-localization.md)
- WCAG compliance and keyboard navigation
- ARIA attributes for screen readers
- Focus management and keyboard shortcuts
- Internationalization (i18n) setup
- Multi-language support
- Locale data configuration

### Migration and Best Practices
📄 **Read:** [references/migration-and-best-practices.md](references/migration-and-best-practices.md)
- EJ1 to EJ2 migration guide
- Performance optimization strategies
- Virtual scrolling for large datasets
- Common patterns and code examples
- Troubleshooting common issues
- FAQ and gotchas

## Quick Start Example

### 1. Install Package
```bash
npm install @syncfusion/ej2-angular-kanban
```

### 2. Import and Setup Component
```typescript
import { Component } from '@angular/core';
import { KanbanModule } from '@syncfusion/ej2-angular-kanban';
import { CardSettingsModel } from '@syncfusion/ej2-angular-kanban';

@Component({
  selector: 'app-kanban-board',
  standalone: true,
  imports: [KanbanModule],
  template: `
    <ejs-kanban 
      keyField="Status" 
      [dataSource]="data"
      [cardSettings]="cardSettings">
      <e-columns>
        <e-column headerText="To Do" keyField="Open"></e-column>
        <e-column headerText="In Progress" keyField="InProgress"></e-column>
        <e-column headerText="Testing" keyField="Testing"></e-column>
        <e-column headerText="Done" keyField="Close"></e-column>
      </e-columns>
    </ejs-kanban>
  `
})
export class KanbanBoardComponent {
  data = [
    { Id: 1, Status: 'Open', Summary: 'Analyze the new requirements gathered from the customer.', Type: 'Epic' },
    { Id: 2, Status: 'InProgress', Summary: 'Improve application performance', Type: 'Epic' },
    { Id: 3, Status: 'Testing', Summary: 'Fix the issues reported in the IE browser', Type: 'Bug' },
    { Id: 4, Status: 'Close', Summary: 'Fix the issue reported by the customer.', Type: 'Bug' }
  ];

  cardSettings: CardSettingsModel = {
    headerField: 'Id',
    contentField: 'Summary'
  };
}
```

### 3. Add Styles
```css
@import '../node_modules/@syncfusion/ej2-base/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-kanban/styles/material3.css';
```

## Common Patterns

### Pattern 1: Enable Swimlanes by Owner
Group cards by assigned team member:
```typescript
swimlaneSettings: { keyField: 'Assignee' }
```

### Pattern 2: Enforce WIP Limits
Set min/max cards per column:
```typescript
columns: [
  { headerText: 'To Do', keyField: 'Open', minCount: 1, maxCount: 5 },
  { headerText: 'In Progress', keyField: 'InProgress', minCount: 0, maxCount: 3 }
]
```

### Pattern 3: Handle Card Click Events
Listen to card interactions:
```typescript
onCardClick(args: CardClickEventArgs): void {
  console.log('Card clicked:', args.data);
}
```

### Pattern 4: Programmatically Add Cards
Use the method API:
```typescript
@ViewChild('kanban') kanban: KanbanComponent;

addNewCard(): void {
  this.kanban.addCard({
    Id: 5,
    Status: 'Open',
    Summary: 'New task'
  });
}
```

## Key Props Reference

| Prop | Type | Purpose |
|------|------|---------|
| `keyField` | string | Maps cards to columns based on field value |
| `dataSource` | Object[] \| DataManager | Array or DataManager instance with card data |
| `cardSettings` | CardSettingsModel | Header, content, and template field mappings |
| `columns` | ColumnsModel[] | Column definitions with headers and key fields |
| `swimlaneSettings` | SwimlaneSettingsModel | Swimlane grouping by field |
| `allowDragAndDrop` | boolean | Enable card drag-and-drop (default: true) |
| `allowKeyboard` | boolean | Enable keyboard navigation (default: true) |
| `allowSelection` | boolean | Allow card selection |
| `selectionType` | 'Single' \| 'Multiple' | Selection mode |
| `height` | string | Board height |
| `width` | string | Board width |

## Common Use Cases

1. **Project Management** - Track tasks from backlog to completion
2. **Bug Tracking** - Organize issues by status (Open, In Progress, Testing, Closed)
3. **Customer Support** - Manage tickets through resolution pipeline
4. **Agile Sprint Board** - Display user stories across sprint stages
5. **Sales Pipeline** - Track leads from prospect to customer
6. **Content Workflow** - Manage articles from draft to published
7. **Recruitment** - Organize candidates through hiring stages
8. **DevOps Pipeline** - Track deployments across environments

---

**Next Steps:** Choose a reference file from the navigation guide above based on your immediate need, or start with **Getting Started** to set up your first Kanban board.
