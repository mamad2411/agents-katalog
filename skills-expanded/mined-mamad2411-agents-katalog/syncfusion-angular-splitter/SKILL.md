---
name: syncfusion-angular-splitter
description: Create resizable, multi-pane layouts with Syncfusion Angular Splitter. Use this skill whenever the user wants to build split-pane interfaces, create dashboard layouts, implement sidebar+content patterns, or manage dynamic pane structures. Include scenarios involving horizontal/vertical splitting, collapsible panes, pane resizing, dynamic pane addition/removal, or complex nested layouts. Perfect for creating flexible UI layouts that adapt to user interaction.

metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Layout Components"
---

# Implementing Syncfusion Angular Splitter

The Splitter component divides a container into resizable panes separated by draggable separator bars. This enables flexible, user-controllable multi-pane layouts for dashboards, editors, and complex UI structures.

## When to Use This Skill

- **Dashboard layouts**: Create multi-column dashboards with resizable panels
- **Editor interfaces**: Build text editors, code editors, or IDEs with side panels
- **Navigation + content**: Implement sidebar navigation with main content area
- **Data exploration**: Design interfaces with filters, previews, and detailed views
- **Nested layouts**: Create complex hierarchical pane structures
- **Dynamic interfaces**: Add/remove panes programmatically based on user actions
- **Responsive splitting**: Support both horizontal and vertical orientations
- **Constrained resizing**: Enforce min/max pane sizes for layout stability

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Package installation and setup
- Standalone component vs NgModule imports
- Basic Splitter component setup
- CSS theme imports
- First working example

### API Reference (Complete)
📄 **Read:** [references/api-reference.md](references/api-reference.md)
- All component properties (orientation, height, width, etc.)
- All pane properties (size, min, max, collapsible, etc.)
- All public methods (addPane, removePane, expand, collapse)
- All 8 events with argument details
- Complete working examples

### Pane Orientation & Layout
📄 **Read:** [references/split-panes.md](references/split-panes.md)
- Horizontal layout (default, side-by-side panes)
- Vertical layout (stacked panes with horizontal separator)
- Multiple panes (3+ panes in single splitter)
- Nested splitters (splitter within pane content)
- Template-based pane content

### Pane Sizing & Configuration
📄 **Read:** [references/pane-sizing.md](references/pane-sizing.md)
- Fixed pixel sizing (200px, 300px)
- Responsive percentage sizing (30%, 50%)
- Auto-sizing (flex layout, automatic distribution)
- Mixed sizing strategies in single splitter
- Dynamic pane size adjustments

### Expand & Collapse Functionality
📄 **Read:** [references/expand-collapse.md](references/expand-collapse.md)
- Collapsible panes (user-clickable expand/collapse icons)
- Collapsed state on initialization
- Programmatic `expand()` method
- Programmatic `collapse()` method
- Dynamic pane visibility control

### Resizing & Interaction
📄 **Read:** [references/resizing.md](references/resizing.md)
- Resize behavior and dragging separator
- Fixed panes (non-resizable, static size)
- Resizable pane configuration
- Min/max size constraints (pane validation)
- Preventing invalid resize operations

### Layout Patterns & Recipes
📄 **Read:** [references/layout-patterns.md](references/layout-patterns.md)
- Two-pane sidebar layouts
- Three-pane editor layouts (left sidebar, main content, right panel)
- Nested splitters and complex hierarchies
- Common UI patterns with complete code examples
- Layout composition strategies

### Styling & Customization
📄 **Read:** [references/styling-customization.md](references/styling-customization.md)
- Theme application (Material3, Bootstrap, etc.)
- CSS class customization
- Separator styling and sizing
- Pane content styling

### Globalization & Localization
📄 **Read:** [references/globalization.md](references/globalization.md)
- Right-to-left (RTL) language support (Arabic, Hebrew)
- Locale and culture configuration
- Text direction attributes
- Multi-language content
- Locale-aware formatting

### Content Loading
📄 **Read:** [references/content-loading.md](references/content-loading.md)
- HTML element content
- String content via `content` property
- ng-template content (template-based)
- DOM selector content (external HTML)
- Dynamic content updates

### Dynamic Pane Manipulation
📄 **Read:** [references/dynamic-manipulation.md](references/dynamic-manipulation.md)
- Adding panes with `addPane()` method
- Removing panes with `removePane()` method
- Pane configuration and properties
- Dynamic pane state management
- Methods and events reference
- Constraints during manipulation

### Security Best Practices
📄 **Read:** [references/security-best-practices.md](references/security-best-practices.md)
- HTML sanitization and XSS prevention
- `enableHtmlSanitizer` property usage
- Content validation patterns
- Safe content sources and ranking
- Common vulnerabilities to avoid
- Secure code examples

---

## Quick Start

### Basic Two-Pane Layout

```typescript
import { Component } from '@angular/core';
import { SplitterModule } from '@syncfusion/ej2-angular-layouts';

@Component({
  selector: 'app-splitter',
  standalone: true,
  imports: [SplitterModule],
  template: `
    <ejs-splitter height="400px" width="100%">
      <e-panes>
        <e-pane size="300px">
          <ng-template #content>
            <div>Left Pane</div>
          </ng-template>
        </e-pane>
        <e-pane size="300px">
          <ng-template #content>
            <div>Right Pane</div>
          </ng-template>
        </e-pane>
      </e-panes>
    </ejs-splitter>
  `
})
export class SplitterComponent {}
```

### Vertical Layout with Collapsible Panes

```typescript
import { Component } from '@angular/core';
import { SplitterModule } from '@syncfusion/ej2-angular-layouts';

@Component({
  selector: 'app-vertical-splitter',
  standalone: true,
  imports: [SplitterModule],
  template: `
    <ejs-splitter orientation="Vertical" height="400px" width="100%">
      <e-panes>
        <e-pane size="150px" [collapsible]="true">
          <ng-template #content>
            <div>Header Panel</div>
          </ng-template>
        </e-pane>
        <e-pane [collapsible]="true">
          <ng-template #content>
            <div>Content Area</div>
          </ng-template>
        </e-pane>
      </e-panes>
    </ejs-splitter>
  `
})
export class VerticalSplitterComponent {}
```

## Common Patterns

### Sidebar + Content Layout

The classic two-pane layout with a fixed sidebar and flexible content area:

```typescript
<ejs-splitter height="500px" width="100%">
  <e-panes>
    <!-- Fixed sidebar -->
    <e-pane size="250px">
      <ng-template #content>
        <div class="sidebar">
          <ul>
            <li>Navigation Item 1</li>
            <li>Navigation Item 2</li>
          </ul>
        </div>
      </ng-template>
    </e-pane>
    <!-- Flexible content -->
    <e-pane>
      <ng-template #content>
        <div class="content">Main Content Area</div>
      </ng-template>
    </e-pane>
  </e-panes>
</ejs-splitter>
```

### Responsive Percentage-Based Layout

Panes that resize based on container size:

```typescript
<ejs-splitter height="400px" width="100%">
  <e-panes>
    <e-pane size="25%">
      <ng-template #content>25% Panel</ng-template>
    </e-pane>
    <e-pane size="50%">
      <ng-template #content>50% Panel</ng-template>
    </e-pane>
    <e-pane size="25%">
      <ng-template #content>25% Panel</ng-template>
    </e-pane>
  </e-panes>
</ejs-splitter>
```

### Collapsible Dashboard Panels

Panes with expand/collapse icons for compact UI:

```typescript
<ejs-splitter height="500px" width="100%">
  <e-panes>
    <e-pane size="200px" [collapsible]="true">
      <ng-template #content>
        <div>Filters Panel (Collapsible)</div>
      </ng-template>
    </e-pane>
    <e-pane [collapsible]="true">
      <ng-template #content>
        <div>Main Dashboard</div>
      </ng-template>
    </e-pane>
    <e-pane size="300px" [collapsible]="true">
      <ng-template #content>
        <div>Details Panel (Collapsible)</div>
      </ng-template>
    </e-pane>
  </e-panes>
</ejs-splitter>
```

## Key Features

| Feature | Purpose | When to Use |
|---------|---------|-----------|
| **Orientation** | Horizontal or vertical pane layout | Choose based on UI design needs |
| **Pane Sizing** | Fixed pixels, percentages, or auto | Mix sizing strategies for responsive layouts |
| **Collapsible** | User-controlled expand/collapse | Save space in dashboards and editors |
| **Fixed Panes** | Non-resizable panes with static size | Create stable reference areas (sidebars) |
| **Min/Max Constraints** | Enforce pane size limits | Prevent layout breaking during resize |
| **Nested Splitters** | Splitter within splitter panes | Create complex hierarchical layouts |
| **Dynamic Manipulation** | Add/remove panes programmatically | Adapt UI to user actions or data changes |
| **Content Flexibility** | HTML, strings, templates, selectors | Load any type of content into panes |
| **Themes & Styling** | Multiple built-in themes | Apply consistent design across app |

## Related Skills

- **Data Grids** - Display tabular data within splitter panes
- **Charts & Visualization** - Embed dashboards and analytics in split layouts
- **Navigation Components** - Build sidebars and navigation structures with splitter

---

**Next Steps:** Choose a reference file based on your specific use case, then refer to the code snippets and examples provided.
