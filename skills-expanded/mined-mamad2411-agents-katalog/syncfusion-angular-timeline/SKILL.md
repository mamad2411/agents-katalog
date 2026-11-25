---
name: syncfusion-angular-timeline
description: Syncfusion Angular Timeline component for displaying sequential events and milestones. Use this to create vertical or horizontal timelines with configurable alignments (Before, After, Alternate, AlternateReverse), custom content, opposite-side content, event handlers, and advanced customization including dot styling, connector appearance, and item templates. Essential for implementing product roadmaps, project timelines, activity feeds, career progression timelines, and any sequential event visualization.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Timelines"
---

# Implementing Syncfusion Angular Timeline

The Timeline component displays a sequence of events or milestones in chronological order, supporting both vertical and horizontal layouts with rich customization options.

## When to Use This Skill

- **Product Roadmaps:** Display product evolution and release milestones
- **Project Timelines:** Show project phases and deliverables  
- **Activity Feeds:** Display recent activities in reverse chronological order
- **Career/Education:** Show career progression or educational achievements
- **Business Events:** Visualize company history, important milestones, or processes
- **Trip Itineraries:** Display scheduled activities and events
- **News Timelines:** Show chronological news items or announcements

## Component Overview

The Timeline component provides:
- Flexible orientation (vertical/horizontal)
- Multiple content alignments (Before, After, Alternate, AlternateReverse)
- Dual-sided content with `oppositeContent`
- Event handlers for lifecycle and rendering
- Extensive dot and connector customization
- Template support for complete layout control
- Item-level customization (disabled, styling, content)

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and package setup
- Creating a basic Timeline
- Angular 21 standalone architecture setup
- Importing TimelineModule and TimelineAllModule
- First working example with items

### Items and Content
📄 **Read:** [references/items-and-content.md](references/items-and-content.md)
- String content and opposite content configuration
- Template-based content rendering
- CSS classes for item styling
- Disabled state and dot-item property
- Data binding from arrays
- Content property usage

### Alignment
📄 **Read:** [references/alignment.md](references/alignment.md)
- Content positioning with align property
- Before alignment (horizontal & vertical behavior)
- After alignment
- Alternate alignment (zigzag pattern)
- AlternateReverse alignment
- Combining alignment with orientation

### Orientations and Reverse
📄 **Read:** [references/orientations-and-reverse.md](references/orientations-and-reverse.md)
- Vertical orientation (default, top-to-bottom)
- Horizontal orientation (left-to-right)
- Reverse property for reversed sequence
- Recent-first timelines
- Reverse with different alignments
- Use cases for activity feeds and news

### Customization
📄 **Read:** [references/customization.md](references/customization.md)
- Connector styling (common and individual item connectors)
- Dot appearance: size, color, outline, shadow, variant
- Dot icons with dotCss property (Material Icons, FontAwesome)
- Item spacing and borders
- CSS class-based customization
- Per-item vs global connector styling
- Advanced visual styling examples

### Events
📄 **Read:** [references/events.md](references/events.md)
- Created event (component initialization)
- BeforeItemRender event (pre-render customization)
- Event handler setup and binding
- Dynamic item modification via events
- Conditional styling during render
- Event arguments and properties

### Templates
📄 **Read:** [references/templates.md](references/templates.md)
- Template property for complete customization
- Template context (item, itemIndex)
- Custom dot indicator design
- Content area layout restructuring
- Custom connectors via templates
- Advanced layout examples

### API Reference
📄 **Read:** [references/api-reference.md](references/api-reference.md)
- Complete property documentation with examples
- All component properties explained (including advanced: enablePersistence, enableRtl, locale)
- All item properties documented
- Event binding and handling
- Enumeration values (TimelineAlign, TimelineOrientation)
- Working code examples for every property and event

## Quick Start Example

```ts
import { Component } from '@angular/core';
import { TimelineItemModel, TimelineModule, TimelineAllModule } from "@syncfusion/ej2-angular-layouts";
import { CommonModule } from '@angular/common';

@Component({
  imports: [CommonModule, TimelineModule, TimelineAllModule],
  standalone: true,
  selector: 'app-root',
  template: `
    <div class="container">
      <ejs-timeline orientation="Vertical" align="Before">
        <e-items>
          <e-item *ngFor="let item of milestones" [content]="item.content" [oppositeContent]="item.oppositeContent"></e-item>
        </e-items>
      </ejs-timeline>
    </div>
  `,
  styles: [`.container { padding: 20px; }`]
})
export class AppComponent {
  public milestones: TimelineItemModel[] = [
    { content: 'Q1 2024', oppositeContent: 'Planning phase' },
    { content: 'Q2 2024', oppositeContent: 'Development' },
    { content: 'Q3 2024', oppositeContent: 'Testing' },
    { content: 'Q4 2024', oppositeContent: 'Launch' }
  ];
}
```

## Common Patterns

### Pattern 1: Activity Feed (Reverse Chronological)
```ts
<ejs-timeline [reverse]="true" align="Before">
  <e-items>
    <e-item *ngFor="let activity of recentActivities" [content]="activity.time" [oppositeContent]="activity.description"></e-item>
  </e-items>
</ejs-timeline>
```
**When to use:** Display latest activities first, news feeds, log entries.

### Pattern 2: Alternate Timeline (Balanced Layout)
```ts
<ejs-timeline align="Alternate" orientation="Horizontal">
  <e-items>
    <e-item *ngFor="let event of events" [content]="event.title" [oppositeContent]="event.description"></e-item>
  </e-items>
</ejs-timeline>
```
**When to use:** Visual balance, alternating left/right content, company history.

### Pattern 3: Custom Styled Timeline
```ts
<ejs-timeline align="Before" [cssClass]="'custom-timeline'">
  <e-items>
    <e-item *ngFor="let item of items" [content]="item.content" [cssClass]="item.cssClass" [disabled]="item.disabled"></e-item>
  </e-items>
</ejs-timeline>
```
**When to use:** Branded styling, visual differentiation of item states, custom themes.

## Key Properties

| Property | Type | Default | Purpose |
|---|---|---|---|
| **Layout & Display** | | | |
| `orientation` | `Vertical` \| `Horizontal` | `Vertical` | Timeline layout direction |
| `align` | `Before` \| `After` \| `Alternate` \| `AlternateReverse` | `After` | Content alignment |
| `reverse` | boolean | `false` | Reverse item order (newest first) |
| `items` | `TimelineItemModel[]` | `[]` | Timeline items array |
| **Item Content** | | | |
| `content` | string \| object | - | Main item text/content |
| `oppositeContent` | string \| object | - | Opposite-side content |
| `dotCss` | string | - | CSS class for dot icons |
| `cssClass` | string | - | CSS class for item styling |
| `disabled` | boolean | `false` | Disable individual item |
| **Customization** | | | |
| `template` | string \| object | - | Custom item template |
| `cssClass` (component) | string | - | Component CSS class |
| **Advanced** | | | |
| `enablePersistence` | boolean | `false` | Persist state to localStorage |
| `enableRtl` | boolean | `false` | Right-to-left layout support |
| `locale` | string | `en-US` | Localization settings |
| **Events** | | | |
| `created` | Event | - | Triggered after component renders |
| `beforeItemRender` | Event | - | Triggered before item renders |

**See [references/api-reference.md](references/api-reference.md) for complete details, examples, and advanced configurations.**

## Common Use Cases

1. **Product Roadmap:** Horizontal timeline with milestones and features
2. **Project Status:** Alternate timeline showing phases and progress
3. **Career Timeline:** Vertical timeline with job positions and dates
4. **Company History:** Reverse timeline showing company evolution
5. **Trip Itinerary:** Vertical timeline with location and activity information
6. **User Activity Log:** Reverse timeline with timestamps and actions
7. **News Feed:** Horizontal reverse timeline with headlines
8. **Educational Path:** Vertical alternate timeline showing degrees and courses
