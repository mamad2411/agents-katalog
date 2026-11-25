---
name: syncfusion-angular-dialog
description: Implement Syncfusion Angular Dialog component with complete API coverage. Build modal/modeless dialogs, confirmation popups, forms in dialogs, draggable windows, and overlaid content. Use this skill when users need dialog implementation, positioning, animations, WCAG 2.2 accessibility, forms integration, and event handling.
metadata:
  author: "Syncfusion Inc"
  category: "Layout"
  version: "33.1.44"
---

# Implementing Dialog

The Dialog component is a window that displays information to the user and is used to get user input. It supports both **modal dialogs** (blocking parent interaction) and **modeless dialogs** (allowing parent interaction).

## Component Overview

### Key Features

- **Modal & Modeless modes** - Block or allow parent interaction
- **Templates** - Customizable headers, content, and footers
- **Positioning** - 9 built-in positions or custom placement
- **Animations** - Smooth open/close effects (Fade, Zoom, Slide)
- **Draggable & Resizable** - Allow users to move and resize dialogs
- **Forms Integration** - Reactive and template-driven forms
- **Accessibility** - Full WCAG 2.2 Level AA support with ARIA
- **Keyboard Navigation** - Tab, Escape, Enter, and arrow keys
- **Responsive** - Full-screen mode on mobile devices

## Documentation and Navigation Guide

When you need to implement Dialog features, follow these references:

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and setup in Angular 21+
- Basic dialog implementation
- CSS imports and themes
- Opening and closing dialogs
- Built-in button support

### Dialog Modes & Types
📄 **Read:** [references/modal-vs-modeless.md](references/modal-vs-modeless.md)
- Modal dialog behavior (blocks parent interaction)
- Modeless dialog behavior (allows parent interaction)
- Use cases and when to use each mode
- Toggling between modes
- Overlay customization and styling

### Content & Templates
📄 **Read:** [references/templates-and-content.md](references/templates-and-content.md)
- Header templates and customization
- Content as strings, HTML, or ng-template
- Footer templates with buttons
- Using ng-content for dynamic content
- Button binding and click events
- Dynamic button arrays

### Positioning & Sizing
📄 **Read:** [references/positioning-and-sizing.md](references/positioning-and-sizing.md)
- Built-in positions (9 locations: Top, Center, Bottom, etc.)
- Custom positioning with X, Y coordinates
- Width and height configuration
- Min/max height constraints
- Responsive sizing on different screen sizes
- Full-screen mode on mobile devices

### Styling & Customization
📄 **Read:** [references/styling-and-customization.md](references/styling-and-customization.md)
- CSS class customization (header, content, footer, overlay)
- Theme integration (Material, Bootstrap, Tailwind, Fluent)
- Dark mode support
- Animation effects (Fade, Zoom, SlideLeft, SlideRight, etc.)
- Icon customization (close button, resize handles)
- RTL (Right-to-Left) language support

### Accessibility & Forms
📄 **Read:** [references/accessibility-and-forms.md](references/accessibility-and-forms.md)
- WCAG 2.2 Level AA compliance standards
- ARIA attributes (aria-labelledby, aria-describedby, aria-modal, aria-grabbed)
- Keyboard navigation patterns (Tab, Shift+Tab, Escape, Enter)
- Screen reader support and best practices
- Form validation with FormValidator
- Reactive forms patterns
- Template-driven forms patterns
- Custom validation rules and error handling

### Interaction & Events
📄 **Read:** [references/interaction-and-events.md](references/interaction-and-events.md)
- Dialog open/close events
- Draggable dialogs (allow users to move dialogs)
- Resizable dialogs (allow users to resize)
- Button click events and handling
- Content interaction patterns
- Preventing dialog closure
- Focus management
- Dialog lifecycle events

### Advanced Patterns
📄 **Read:** [references/advanced-patterns.md](references/advanced-patterns.md)
- Nested dialogs (dialog within dialog)
- Ajax-loaded content dynamically
- Utility functions for programmatic creation
- Complex layouts (Rich Text Editor, multi-step forms)
- Scroll handling and auto-centering
- Custom event emitters
- Routing integration patterns

### API Reference (Complete)
📄 **Read:** [api-reference.md](api-reference.md)
- Complete Dialog API documentation
- All valid properties with types and examples
- All methods (show, hide, refresh, destroy)
- All events (beforeOpen, beforeClose, drag, resize, etc.)
- Interfaces and models (AnimationSettingsModel, ButtonPropsModel, etc.)
- Valid enumerations (DialogEffect, ResizeDirections)
- Official Syncfusion documentation links

## Quick Start Example

Here's a minimal example to open a basic modal dialog:

```typescript
import { Component, ViewChild } from '@angular/core';
import { DialogModule, DialogComponent } from '@syncfusion/ej2-angular-popups';

@Component({
  selector: 'app-root',
  imports: [DialogModule],
  template: `
    <div id="dialog-container" style="height: 500px;">
      <button class="e-control e-btn" (click)="onOpenDialog()">
        Open Dialog
      </button>
      
      <ejs-dialog 
        #ejDialog
        target="#dialog-container"
        [showCloseIcon]="true"
        width="400px"
        content="This is a Dialog content"
      >
        <ng-template #header>
          <div class="e-dlg-header-content">
            <span>Dialog Title</span>
          </div>
        </ng-template>
      </ejs-dialog>
    </div>
  `
})
export class AppComponent {
  @ViewChild('ejDialog') ejDialog!: DialogComponent;

  onOpenDialog(): void {
    this.ejDialog.show();
  }
}
```

**CSS:**
```css
#dialog-container {
  height: 500px;
}
```

## Common Patterns

### Pattern 1: Modal Confirmation Dialog

```typescript
// Create a modal dialog for confirmation
<ejs-dialog 
  [isModal]="true"
  [showCloseIcon]="true"
  width="350px"
  content="Are you sure you want to delete this item?"
>
  <ng-template #footer>
    <button class="e-control e-btn e-primary" (click)="onConfirm()">
      Yes, Delete
    </button>
    <button class="e-control e-btn" (click)="onCancel()">
      Cancel
    </button>
  </ng-template>
</ejs-dialog>
```

### Pattern 2: Dialog with Form (Reactive Forms)

```typescript
// Dialog containing a reactive form
<ejs-dialog [showCloseIcon]="true" width="450px">
  <form [formGroup]="form">
    <div class="e-dlg-content">
      <input formControlName="name" placeholder="Enter name" />
      <input formControlName="email" placeholder="Enter email" />
    </div>
  </form>
  
  <ng-template #footer>
    <button class="e-control e-btn e-primary" (click)="onSubmit()">
      Submit
    </button>
  </ng-template>
</ejs-dialog>
```

### Pattern 3: Positioned Dialog

```typescript
// Dialog positioned at a specific location
<ejs-dialog 
  [position]="{ X: 100, Y: 50 }"
  width="400px"
  content="Positioned Dialog"
>
</ejs-dialog>
```

## Key Props Quick Reference

| Property | Type | Purpose | Example |
|----------|------|---------|---------|
| `isModal` | boolean | Block parent interaction | `[isModal]="true"` |
| `showCloseIcon` | boolean | Show close button in header | `[showCloseIcon]="true"` |
| `width` | string \| number | Set dialog width | `width="400px"` |
| `height` | string \| number | Set dialog height | `height="300px"` |
| `minHeight` | string \| number | Minimum height constraint | `[minHeight]="200"` |
| `position` | PositionDataModel | Set position (X, Y) or preset | `[position]="{ X: 'center', Y: 'center' }"` |
| `target` | HTMLElement \| string | Set container element | `target="#container"` |
| `content` | string \| HTMLElement | Set content text or HTML | `content="Hello"` |
| `header` | string \| HTMLElement | Set header text or element | `header="Title"` |
| `buttons` | ButtonPropsModel[] | Add footer buttons | `[buttons]="buttonArray"` |
| `closeOnEscape` | boolean | Close on Escape key | `[closeOnEscape]="true"` |
| `allowDragging` | boolean | Enable header dragging | `[allowDragging]="true"` |
| `enableResize` | boolean | Enable resizing | `[enableResize]="true"` |
| `resizeHandles` | ResizeDirections[] | Specify resize directions | `[resizeHandles]="['All']"` |
| `cssClass` | string | Custom CSS class(es) | `cssClass="custom-dialog"` |
| `animationSettings` | AnimationSettingsModel | Configure animations | `[animationSettings]="{ effect: 'FadeZoom' }"` |
| `enablePersistence` | boolean | Save state between reloads | `[enablePersistence]="true"` |
| `zIndex` | number | Z-order for layering | `[zIndex]="1000"` |

## Common Use Cases

1. **Confirmation before delete** - Modal dialog asking user to confirm deletion
2. **Form submission** - Dialog with form for user to submit data
3. **Alerts and notifications** - Display important information to users
4. **Multi-step processes** - Use nested dialogs for workflows
5. **Settings panels** - Modeless dialog for settings that don't block interaction
6. **Help and guidance** - Display help content in a draggable dialog
7. **Loading states** - Show progress in a dialog while processing
8. **Error handling** - Display error messages in a modal

---

## Related Skills

- [Dialog Animation](references/styling-and-customization.md) - Customize open/close animations
- [Form Validation](references/accessibility-and-forms.md) - Validate user input in dialogs
- [Routing Integration](references/advanced-patterns.md) - Use dialogs with Angular routing
