---
name: syncfusion-angular-tab
description: |
  Implement the responsive tabbed navigation in Angular using Syncfusion Tab. Supports tab selection, 
  dynamic loading, drag-and-drop reordering, localization, multiple orientations, state persistence, 
  data binding, remote data, animations, and advanced patterns like wizards, nested tabs, and collapsible tabs.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Navigation Components"
---

# Implementing Syncfusion Angular Tabs

The Syncfusion Angular Tab component provides a flexible, responsive way to organize and display content in a tabbed interface. Tabs allow users to switch between multiple content panels, making it ideal for multi-step workflows, settings panels, navigation structures, and organized data displays.

## When to Use This Skill

- **Building tabbed navigation:** Organize related content into separate tabs with easy switching
- **Multi-step workflows:** Create wizard-like experiences or step-by-step processes
- **Responsive layouts:** Adapt tab display for mobile, tablet, and desktop screens (different orientations)
- **Dynamic content management:** Add, remove, reorder, or drag-drop tabs at runtime
- **Complex applications:** Integrate Grids, Charts, Calendars, Forms within tabs
- **State preservation:** Save and restore user selections across browser sessions
- **Localized applications:** Support multiple languages with localized UI text
- **Multiple orientations:** Vertical or horizontal tab headers based on layout needs
- **Large data sets:** Load tabs from remote APIs or databases
- **Customized UI:** Style headers, icons, animations, overflow modes, and content areas
- **User preferences:** Remember last selected tab with state persistence

## Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Package installation and setup
- Angular CLI configuration (standalone vs module)
- CSS imports and theme setup
- Three rendering methods: JSON items, ng-template, HTML elements
- Basic usage examples and minimal setup

### Content Rendering Modes
📄 **Read:** [references/rendering-modes.md](references/rendering-modes.md)
- **On Demand (default):** Load active tab content, preserve state
- **Dynamic:** Memory-optimized, single content in DOM
- **Init:** All content upfront, access between tabs
- Performance tradeoffs and use case selection
- Code examples for each mode

### Content Management & Data
📄 **Read:** [references/content-management.md](references/content-management.md)
- DataSource binding and data-driven tabs
- Dynamic tab addition/removal (.addTab(), .removeTab())
- AJAX and server-side content loading
- Show/hide tabs dynamically
- Reactive forms within tabs (FormGroup, FormControl)
- Content reuse with TemplateRef

### Tab Selection & Navigation
📄 **Read:** [references/selection-navigation.md](references/selection-navigation.md)
- Tab selection events (selecting, selected)
- Programmatic tab selection (.select() method)
- Determining user vs programmatic selection (isInteracted)
- Keyboard navigation (Tab key, arrow keys, Enter/Space)
- Click handlers and selection callbacks

### Customization & Styling
📄 **Read:** [references/customization-styling.md](references/customization-styling.md)
- Header styles and CSS classes (fill, background, accent)
- Icon positioning and icon CSS customization
- Content height management and auto-sizing
- Scroll step configuration
- Animation control and custom animations
- CSS customization guide for advanced styling
- Responsive header display

### Drag and Drop Reordering
📄 **Read:** [references/drag-and-drop-reordering.md](references/drag-and-drop-reordering.md)
- Enable drag and drop with `allowDragAndDrop` property
- Configure drag area with `dragArea` property
- Handle `onDragStart`, `dragging`, `dragged` events
- Prevent dragging/dropping specific tabs
- Reorder active tab in popup overflow mode
- Drag items between multiple Tab components
- Drag Tab items to external components (TreeView, etc.)

### Localization and Orientation
📄 **Read:** [references/localization-and-orientation.md](references/localization-and-orientation.md)
- Localize UI text using `locale` property and L10n class
- Header placement options (Top, Bottom, Left, Right)
- Overflow modes (Scrollable vs Popup)
- `scrollStep` configuration for scroll speed
- Responsive orientation changes based on screen size
- Multi-language support with custom translations

### State Persistence and Data Binding
📄 **Read:** [references/state-persistence-and-data-binding.md](references/state-persistence-and-data-binding.md)
- Enable persistence with `enablePersistence` property
- Automatic state saving to browser localStorage
- Binding tabs to data sources (arrays, APIs, DataManager)
- Loading tab data from remote servers (OData, HTTP)
- Load tab content through POST requests
- Combined persistence with dynamic data binding

### Advanced Scenarios
📄 **Read:** [references/advanced-scenarios.md](references/advanced-scenarios.md)
- Nested tabs (multiple levels of tabbed content)
- Collapsible tabs with accordion-like behavior
- Wizard pattern implementation (step validation)
- State persistence with LocalStorage/SessionStorage
- Component initialization from events
- Edge cases and best practices

### Responsive & Adaptive Behavior
📄 **Read:** [references/responsive-adaptive.md](references/responsive-adaptive.md)
- Adaptive rendering for constrained spaces
- Overflow modes: Scrollable and Popup
- Responsive tab display on mobile/desktop
- Orientation changes (horizontal/vertical)
- Prevent swipe selection on touch devices
- Width and height constraints

### Troubleshooting & Best Practices
📄 **Read:** [references/troubleshooting.md](references/troubleshooting.md)
- Common implementation issues and solutions
- Performance optimization techniques
- Content rendering gotchas
- State management pitfalls
- Accessibility and keyboard support
- Animation performance
- Migration from EJ1 to EJ2

## Quick Start Example

Basic Tab with multiple content panels:

```typescript
import { Component } from '@angular/core';
import { TabModule } from '@syncfusion/ej2-angular-navigations';

@Component({
  imports: [TabModule],
  standalone: true,
  selector: 'app-root',
  template: `
    <ejs-tab id="element">
      <e-tabitems>
        <e-tabitem [header]="headerText[0]" [content]="content0"></e-tabitem>
        <e-tabitem [header]="headerText[1]" [content]="content1"></e-tabitem>
        <e-tabitem [header]="headerText[2]" [content]="content2"></e-tabitem>
      </e-tabitems>
    </ejs-tab>
  `
})
export class AppComponent {
  public headerText: object[] = [
    { text: 'Home' },
    { text: 'Settings' },
    { text: 'Profile' }
  ];

  public content0 = 'Welcome to the home tab with your dashboard content.';
  public content1 = 'Configure application settings and preferences here.';
  public content2 = 'View and edit your user profile information.';
}
```

## Common Patterns

### Pattern 1: Dynamic Tab Creation
```typescript
// Add new tab at specific index
const newTab = { 
  header: { text: 'New Tab' }, 
  content: 'New content here' 
};
this.tabObj.addTab([newTab], 2);
```

### Pattern 2: Selection with Event Handling
```typescript
// Handle tab selection changes
onTabSelected(args: SelectEventArgs) {
  console.log('Selected tab index:', args.selectedIndex);
  // Refresh data for selected tab
  this.loadDataForTab(args.selectedIndex);
}
```

### Pattern 3: Responsive Tab Header with Icons
```typescript
public headerText: object[] = [
  { text: 'Dashboard', iconCss: 'e-icons e-home' },
  { text: 'Products', iconCss: 'e-icons e-shopping-cart' },
  { text: 'Orders', iconCss: 'e-icons e-receipt' }
];
```

### Pattern 4: Content Rendering Mode Selection
```typescript
// Use Dynamic mode for memory optimization
<ejs-tab 
  loadOn="Dynamic"  // Only active content in DOM
  heightAdjustMode="Auto">
</ejs-tab>
```

### Pattern 5: Keyboard Navigation
```typescript
// Tab component has built-in keyboard support
// Tab key - focus next header
// Arrow keys - navigate between tabs
// Enter/Space - activate tab
// Users can switch tabs without mouse
```

## Key Properties & Methods

**Common Properties:**
- `items` - Tab item collection
- `selectedIndex` - Currently active tab index
- `heightAdjustMode` - How content height is managed
- `loadOn` - Content rendering mode (Default, Dynamic, Init)
- `overflowMode` - Handling overflow (Scrollable, Popup)
- `animation` - Animation configuration
- `allowDragAndDrop` - Enable/disable drag-drop (boolean)
- `dragArea` - CSS selector for drag boundary
- `reorderActiveTab` - Reorder active from popup (boolean)
- `headerPlacement` - Header position (Top, Bottom, Left, Right)
- `enablePersistence` - Save/restore state (boolean)
- `locale` - Language/culture code (e.g., 'en-US', 'fr-FR')
- `scrollStep` - Pixels to scroll per click

**Key Methods:**
- `.select(index)` - Programmatically select tab
- `.addTab(items, index)` - Add new tabs
- `.removeTab(index)` - Remove tab
- `.hideTab(index, hide)` - Hide/show tab (hide=true to hide, false to show)
- `.refresh()` - Refresh tab layout
- `.dataBind()` - Update data binding

**Important Events:**
- `selecting` - Before tab selection
- `selected` - After tab selection
- `onDragStart` - Before drag begins (cancellable)
- `dragging` - During drag operation
- `dragged` - After drop completes (cancellable)
- `created` - Tab component initialized
- `destroyed` - Tab component destroyed

## Related Skills

- [Implementing Buttons](../buttons/implementing-buttons/) - For button styling in tab headers
- [Implementing Forms](../forms/implementing-forms/) - For reactive forms within tabs
- [Implementing Grids](../grids/implementing-grids/) - For data display in tabs

---

**Next Step:** Based on your needs, read the appropriate reference file from the navigation guide above.
