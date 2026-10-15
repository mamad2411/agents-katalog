---
name: syncfusion-angular-accordion
description: Guide for implementing Angular Accordion components for collapsible content panels, expandable sections, FAQs, multi-step wizards, step-by-step forms, navigation menus, or tabbed navigation. Use this skill when users mention expanding/collapsing content, accordion layouts, step-by-step workflows, or hierarchical content organization. This skill covers initialization, expand modes, data binding, dynamic loading, animations, nested accordions, and real-world patterns.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Navigation Components"
---

# Implementing Syncfusion Angular Accordion Component

## When to Use This Skill

Use this skill when you need to:
- **Create collapsible content panels** - Organize related content into expandable sections that collapse to save space
- **Build step-by-step wizards** - Create multi-step forms or workflows where users progress through accordion items
- **Implement FAQ sections** - Display frequently asked questions with expandable answers
- **Create navigation menus** - Build hierarchical menus or navigation structures with nested expandable items
- **Load content dynamically** - Fetch and display content on-demand as users expand accordion items
- **Add custom animations** - Enhance user experience with smooth expand/collapse transitions
- **Organize complex data** - Display structured data with expandable categories and subcategories

## Component Overview

The Syncfusion Angular Accordion component displays a vertically collapsible content panel where users can expand one or more sections at a time. Key capabilities include:

- **Single/Multiple expand modes** - Control whether one or multiple items can be open simultaneously
- **Data binding** - Bind accordion items from arrays or OData services
- **Dynamic item management** - Add, remove, or update items at runtime
- **Event handling** - Respond to expand, collapse, and click events
- **Custom animations** - Configure smooth transitions with custom effects and duration
- **Nested accordions** - Create hierarchical accordion structures for complex navigation
- **TreeView integration** - Embed other components like TreeView for advanced navigation
- **Content projection** - Use Angular's `ng-content` for reusable content components

## Master Table of Contents

**Quick Navigation to Documentation:**
1. [Getting Started](references/getting-started.md) - Installation, setup, and basic initialization
2. [Expand Modes](references/expand-modes.md) - Single vs. Multiple expand modes, configuration
3. [Data Binding](references/data-binding.md) - Data sources, OData, REST APIs, refresh strategies
4. [Dynamic Loading and Interactions](references/dynamic-loading-and-interactions.md) - Events, methods, dynamic item management
5. [Advanced Features](references/advanced-features.md) - Animations, nested accordions, styling, RTL
6. [Use Cases and Patterns](references/use-cases-patterns.md) - Real-world implementations and patterns

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)

When to use:
- Setting up your first Accordion component
- Installing required packages and dependencies
- Understanding CSS imports and theme configuration
- Learning basic initialization methods (template-based, items array, HTML elements)
- Creating your first working example

### Expand Modes
📄 **Read:** [references/expand-modes.md](references/expand-modes.md)

When to use:
- Deciding whether users should expand one or multiple items
- Configuring single mode (only one item open at a time)
- Using multiple mode for simultaneously open items
- Selecting the right mode for your use case
- Handling performance with large datasets

### Data Binding
📄 **Read:** [references/data-binding.md](references/data-binding.md)

When to use:
- Binding accordion data from external sources
- Using DataManager to fetch from OData services
- Mapping data properties to headers and content
- Working with structured data arrays
- Refreshing accordion content after data updates

### Dynamic Loading and Interactions
📄 **Read:** [references/dynamic-loading-and-interactions.md](references/dynamic-loading-and-interactions.md)

When to use:
- Adding items dynamically at runtime
- Handling expand/collapse/click events
- Loading content via AJAX or remote requests
- Implementing checkbox-controlled expansion
- Preventing item collapse or forcing items to stay open
- Using `ng-content` for reusable content components
- Creating always-open accordion items

### Advanced Features
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)

When to use:
- Customizing expand/collapse animations with effects and easing
- Creating nested accordions for hierarchical structures
- Integrating TreeView components within accordion items
- Applying custom CSS styling and theming
- Enabling RTL (right-to-left) support
- Styling headers, items, and expand/collapse icons

### Use Cases and Patterns
📄 **Read:** [references/use-cases-patterns.md](references/use-cases-patterns.md)

When to use:
- Building FAQ sections with best practices
- Creating multi-step wizard forms with validation
- Designing settings panels with categories
- Building navigation menus and organizational hierarchies
- Displaying help and documentation sections
- Learning real-world patterns and code organization strategies

## Quick Start Example

**Basic template-based accordion with three items:**

```typescript
import { Component } from '@angular/core';
import { AccordionModule } from '@syncfusion/ej2-angular-navigations';

@Component({
  standalone: true,
  selector: 'app-root',
  imports: [AccordionModule],
  template: `
    <ejs-accordion>
      <e-accordionitems>
        <e-accordionitem expanded="true">
          <ng-template #header>
            <div>ASP.NET</div>
          </ng-template>
          <ng-template #content>
            <div>Microsoft ASP.NET is a set of technologies in the Microsoft .NET Framework for building Web applications and XML Web services.</div>
          </ng-template>
        </e-accordionitem>
        
        <e-accordionitem>
          <ng-template #header>
            <div>ASP.NET MVC</div>
          </ng-template>
          <ng-template #content>
            <div>The Model-View-Controller (MVC) architectural pattern separates an application into three main components: the model, the view, and the controller.</div>
          </ng-template>
        </e-accordionitem>
        
        <e-accordionitem>
          <ng-template #header>
            <div>JavaScript</div>
          </ng-template>
          <ng-template #content>
            <div>JavaScript (JS) is an interpreted computer programming language used for creating interactive web pages and applications.</div>
          </ng-template>
        </e-accordionitem>
      </e-accordionitems>
    </ejs-accordion>
  `
})
export class AppComponent {}
```

**Using items array approach:**

```typescript
import { Component } from '@angular/core';
import { AccordionModule } from '@syncfusion/ej2-angular-navigations';

@Component({
  standalone: true,
  selector: 'app-root',
  imports: [AccordionModule],
  template: `<ejs-accordion [items]="accordionItems"></ejs-accordion>`
})
export class AppComponent {
  public accordionItems = [
    {
      header: 'ASP.NET',
      content: 'Microsoft ASP.NET is a set of technologies in the Microsoft .NET Framework for building Web applications.',
      expanded: true
    },
    {
      header: 'ASP.NET MVC',
      content: 'The Model-View-Controller (MVC) architectural pattern separates an application into three main components.'
    },
    {
      header: 'JavaScript',
      content: 'JavaScript (JS) is an interpreted computer programming language used for creating interactive web pages.'
    }
  ];
}
```

## Common Patterns

### Pattern 1: Single Expand Mode (One Item Open)
Use when you want only one accordion item open at a time, common for navigation menus and settings panels.

```typescript
<ejs-accordion expandMode="Single">
  <!-- items here -->
</ejs-accordion>
```

### Pattern 2: Dynamic Item Addition
Add items programmatically in response to user actions or data loading.

```typescript
@ViewChild('accordion') accordionObj?: AccordionComponent;

addNewItem() {
  this.accordionObj?.addItem({
    header: 'New Item',
    content: 'New content here'
  });
}
```

### Pattern 3: Event-Driven Workflows
Respond to accordion events for custom logic like validation or data loading.

```typescript
<ejs-accordion (expanding)="onExpanding($event)" (expanded)="onExpanded($event)">
  <!-- items here -->
</ejs-accordion>

onExpanding(event: ExpandEventArgs) {
  // Prevent collapse of currently open item
  event.cancel = true;
}
```

### Pattern 4: Animated Expand/Collapse
Add smooth animations for better visual feedback.

```typescript
<ejs-accordion [animation]="animationSettings">
  <!-- items here -->
</ejs-accordion>

animationSettings = {
  expand: { effect: 'SlideDown', duration: 400, easing: 'ease' },
  collapse: { effect: 'SlideUp', duration: 400, easing: 'ease' }
};
```

## Complete API Reference

For detailed documentation on each API element with working code examples, refer to the reference files. Below is a comprehensive summary.

### Accordion Component Properties (13 Total)

| Property | Type | Default | Purpose | Learn More |
|---|---|---|---|---|
| `items` | `AccordionItemModel[]` | `[]` | Collection of accordion items | [Data Binding](references/data-binding.md) |
| `dataSource` | `DataManager \| Object[]` | `null` | Data source for binding items | [Data Binding](references/data-binding.md) |
| `expandMode` | `'Single' \| 'Multiple'` | `'Multiple'` | Controls single or multiple item expansion | [Expand Modes](references/expand-modes.md) |
| `expandedIndices` | `number[]` | `[]` | Indices of initially expanded items | [Expand Modes](references/expand-modes.md) |
| `animation` | `AccordionAnimationSettingsModel` | `{ expand: { effect: 'SlideDown', duration: 400, easing: 'linear' }, collapse: { effect: 'SlideUp', duration: 400, easing: 'linear' } }` | Expand/collapse animation settings | [Advanced Features](references/advanced-features.md) |
| `headerTemplate` | `string \| Function` | `null` | Template for item headers | [Getting Started](references/getting-started.md) |
| `itemTemplate` | `string \| Function` | `null` | Template for item content | [Getting Started](references/getting-started.md) |
| `height` | `string \| number` | `auto` | Component height | [Getting Started](references/getting-started.md) |
| `width` | `string \| number` | `100%` | Component width | [Getting Started](references/getting-started.md) |
| `enableRtl` | `boolean` | `false` | Enable right-to-left layout | [Advanced Features](references/advanced-features.md) |
| `enablePersistence` | `boolean` | `false` | Save expanded state in localStorage | [Getting Started](references/getting-started.md) |
| `enableHtmlSanitizer` | `boolean` | `true` | Sanitize HTML in content | [Data Binding](references/data-binding.md) |
| `locale` | `string` | `'en-US'` | Localization culture | [Advanced Features](references/advanced-features.md) |

### AccordionItem Properties (8 Total)

| Property | Type | Default | Purpose | Learn More |
|---|---|---|---|---|
| `header` | `string \| HTMLElement` | `''` | Item header text or element | [Getting Started](references/getting-started.md) |
| `content` | `string \| HTMLElement \| Function` | `''` | Item content text, HTML, or function | [Getting Started](references/getting-started.md) |
| `expanded` | `boolean` | `false` | Initial expanded state | [Expand Modes](references/expand-modes.md) |
| `disabled` | `boolean` | `false` | Disable item interaction | [Dynamic Loading](references/dynamic-loading-and-interactions.md) |
| `visible` | `boolean` | `true` | Item visibility | [Dynamic Loading](references/dynamic-loading-and-interactions.md) |
| `cssClass` | `string` | `''` | Custom CSS class for item | [Advanced Features](references/advanced-features.md) |
| `iconCss` | `string` | `''` | Font Awesome/Bootstrap icon class | [Getting Started](references/getting-started.md) |
| `id` | `string` | `''` | Unique item identifier | [Getting Started](references/getting-started.md) |

### Methods (7 Total)

| Method | Signature | Purpose | Learn More |
|---|---|---|---|
| `addItem()` | `addItem(item: AccordionItemModel \| Object[], index?: number): void` | Add items at specific index or end | [Dynamic Loading](references/dynamic-loading-and-interactions.md) |
| `removeItem()` | `removeItem(index: number): void` | Remove item at index | [Dynamic Loading](references/dynamic-loading-and-interactions.md) |
| `expandItem()` | `expandItem(isExpand: boolean, index?: number): void` | Expand/collapse specific or all items | [Dynamic Loading](references/dynamic-loading-and-interactions.md), [Expand Modes](references/expand-modes.md) |
| `enableItem()` | `enableItem(index: number, isEnable: boolean): void` | Enable/disable item interaction | [Dynamic Loading](references/dynamic-loading-and-interactions.md) |
| `hideItem()` | `hideItem(index: number, isHidden?: boolean): void` | Show/hide item without removal | [Dynamic Loading](references/dynamic-loading-and-interactions.md) |
| `select()` | `select(index: number): void` | Set focus to item header | [Dynamic Loading](references/dynamic-loading-and-interactions.md) |
| `destroy()` | `destroy(): void` | Clean up component resources | [Dynamic Loading](references/dynamic-loading-and-interactions.md) |

### Events (5 Total)

| Event | Event Args | Triggered When | Learn More |
|---|---|---|---|
| `created` | `Event` | Component rendering completes | [Dynamic Loading](references/dynamic-loading-and-interactions.md) |
| `expanding` | `ExpandEventArgs` | Item begins to expand (cancellable) | [Dynamic Loading](references/dynamic-loading-and-interactions.md) |
| `expanded` | `ExpandEventArgs` | Item finishes expanding | [Dynamic Loading](references/dynamic-loading-and-interactions.md) |
| `clicked` | `AccordionClickArgs` | Header or content clicked | [Dynamic Loading](references/dynamic-loading-and-interactions.md) |
| `destroyed` | `Event` | Component destroyed | [Dynamic Loading](references/dynamic-loading-and-interactions.md) |

### Animation Effects (6 Types)

| Effect | Expand Behavior | Collapse Behavior | Best For |
|---|---|---|---|
| `SlideDown` | Content slides down | N/A (use with SlideUp) | Default, smooth animations |
| `SlideUp` | N/A (use with SlideDown) | Content slides up | Default collapse effect |
| `FadeDown` | Content fades in while sliding | N/A (use with FadeUp) | Professional appearance |
| `FadeUp` | N/A (use with FadeDown) | Content fades out while sliding | Professional appearance |
| `Zoom` | Content zooms in | Content zooms out | Attention-grabbing effects |
| `None` | Instant | Instant | Best performance |

### Easing Functions (5 Types)

| Easing | Curve | Best For | Typical Use |
|---|---|---|---|
| `linear` | Constant speed | Simple animations | Straightforward expand/collapse |
| `ease` | Slow start/end, fast middle | Default behavior | Balanced feel |
| `ease-in` | Accelerating | Collapse action | Speeds up as it closes |
| `ease-out` | Decelerating | Expand action | Slows down as it opens |
| `ease-in-out` | Slow start and end | Symmetric animations | Equal timing both directions |

## Common Use Cases

1. **FAQ Section** - Expandable question/answer pairs with single expand mode
2. **Multi-Step Wizard** - Sequential items with validation and conditional enabling
3. **Settings Panel** - Grouped settings organized in expandable sections
4. **Navigation Menu** - Hierarchical navigation with nested accordions
5. **Data Explorer** - Expandable data categories with dynamic loading
6. **Help Documentation** - Collapsible help sections organized by topic

## Troubleshooting Quick Reference

**Item won't expand?**
- Check if item is disabled with `enableItem(false, index)`
- Verify `expandMode` setting matches your requirement

**Content not loading?**
- Ensure `header` and `content` properties are set
- Check CSS imports are included in styles

**Animation not smooth?**
- Verify CSS is properly imported
- Check browser console for errors
- Consider reducing animation duration for slower devices

**Multiple items closing unexpectedly?**
- Verify `expandMode` is set to 'Multiple' if multiple should be open
- Check event handlers aren't calling `e.cancel = true`

---

For detailed information on any aspect, refer to the documentation and navigation guide above. Start with **getting-started.md** if you're new to the component.
