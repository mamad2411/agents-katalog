---
name: syncfusion-angular-popups
description: Comprehensive guide for implementing Syncfusion Angular popup components including Dialog, Predefined Dialogs and Tooltip. Use this when building modal/modeless dialogs, confirmation popups, forms in dialogs, draggable windows, popovers, tooltips, and overlaid content with custom positioning, animations, WCAG 2.2 accessibility, forms integration, and event handling in Angular applications.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Layout"
---

# Implementing Syncfusion Angular Popups

## Dialog

The Dialog component is a window that displays information to the user and is used to get user input. It supports both **modal dialogs** (blocking parent interaction) and **modeless dialogs** (allowing parent interaction).

### Component Overview

#### Key Features

- **Modal & Modeless modes** - Block or allow parent interaction
- **Templates** - Customizable headers, content, and footers
- **Positioning** - 9 built-in positions or custom placement
- **Animations** - Smooth open/close effects (Fade, Zoom, Slide)
- **Draggable & Resizable** - Allow users to move and resize dialogs
- **Forms Integration** - Reactive and template-driven forms
- **Accessibility** - Full WCAG 2.2 Level AA support with ARIA
- **Keyboard Navigation** - Tab, Escape, Enter, and arrow keys
- **Responsive** - Full-screen mode on mobile devices

### Documentation and Navigation Guide

When you need to implement Dialog features, follow these references:

#### Getting Started
📄 **Read:** [references/dialog-getting-started.md](references/dialog-getting-started.md)
- Installation and setup in Angular 21+
- Basic dialog implementation
- CSS imports and themes
- Opening and closing dialogs
- Built-in button support

#### Dialog Modes & Types
📄 **Read:** [references/dialog-modal-vs-modeless.md](references/dialog-modal-vs-modeless.md)
- Modal dialog behavior (blocks parent interaction)
- Modeless dialog behavior (allows parent interaction)
- Use cases and when to use each mode
- Toggling between modes
- Overlay customization and styling

#### Content & Templates
📄 **Read:** [references/dialog-templates-and-content.md](references/dialog-templates-and-content.md)
- Header templates and customization
- Content as strings, HTML, or ng-template
- Footer templates with buttons
- Using ng-content for dynamic content
- Button binding and click events
- Dynamic button arrays

#### Positioning & Sizing
📄 **Read:** [references/dialog-positioning-and-sizing.md](references/dialog-positioning-and-sizing.md)
- Built-in positions (9 locations: Top, Center, Bottom, etc.)
- Custom positioning with X, Y coordinates
- Width and height configuration
- Min/max height constraints
- Responsive sizing on different screen sizes
- Full-screen mode on mobile devices

#### Styling & Customization
📄 **Read:** [references/dialog-styling-and-customization.md](references/dialog-styling-and-customization.md)
- CSS class customization (header, content, footer, overlay)
- Theme integration (Material, Bootstrap, Tailwind, Fluent)
- Dark mode support
- Animation effects (Fade, Zoom, SlideLeft, SlideRight, etc.)
- Icon customization (close button, resize handles)
- RTL (Right-to-Left) language support

#### Accessibility & Forms
📄 **Read:** [references/dialog-accessibility-and-forms.md](references/dialog-accessibility-and-forms.md)
- WCAG 2.2 Level AA compliance standards
- ARIA attributes (aria-labelledby, aria-describedby, aria-modal, aria-grabbed)
- Keyboard navigation patterns (Tab, Shift+Tab, Escape, Enter)
- Screen reader support and best practices
- Form validation with FormValidator
- Reactive forms patterns
- Template-driven forms patterns
- Custom validation rules and error handling

#### Interaction & Events
📄 **Read:** [references/dialog-interaction-and-events.md](references/dialog-interaction-and-events.md)
- Dialog open/close events
- Draggable dialogs (allow users to move dialogs)
- Resizable dialogs (allow users to resize)
- Button click events and handling
- Content interaction patterns
- Preventing dialog closure
- Focus management
- Dialog lifecycle events

#### Advanced Patterns
📄 **Read:** [references/dialog-advanced-patterns.md](references/dialog-advanced-patterns.md)
- Nested dialogs (dialog within dialog)
- Ajax-loaded content dynamically
- Utility functions for programmatic creation
- Complex layouts (Rich Text Editor, multi-step forms)
- Scroll handling and auto-centering
- Custom event emitters
- Routing integration patterns

#### API Reference (Complete)
📄 **Read:** [references/dialog-api-reference.md](references/dialog-api-reference.md)
- Complete Dialog API documentation
- All valid properties with types and examples
- All methods (show, hide, refresh, destroy)
- All events (beforeOpen, beforeClose, drag, resize, etc.)
- Interfaces and models (AnimationSettingsModel, ButtonPropsModel, etc.)
- Valid enumerations (DialogEffect, ResizeDirections)
- Official Syncfusion documentation links

### Quick Start Example

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

### Common Patterns

#### Pattern 1: Modal Confirmation Dialog

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

#### Pattern 2: Dialog with Form (Reactive Forms)

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

#### Pattern 3: Positioned Dialog

```typescript
// Dialog positioned at a specific location
<ejs-dialog 
  [position]="{ X: 100, Y: 50 }"
  width="400px"
  content="Positioned Dialog"
>
</ejs-dialog>
```

### Key Props Quick Reference

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

### Common Use Cases

1. **Confirmation before delete** - Modal dialog asking user to confirm deletion
2. **Form submission** - Dialog with form for user to submit data
3. **Alerts and notifications** - Display important information to users
4. **Multi-step processes** - Use nested dialogs for workflows
5. **Settings panels** - Modeless dialog for settings that don't block interaction
6. **Help and guidance** - Display help content in a draggable dialog
7. **Loading states** - Show progress in a dialog while processing
8. **Error handling** - Display error messages in a modal

---

### Related Skills

- [Dialog Animation](references/dialog-styling-and-customization.md) - Customize open/close animations
- [Form Validation](references/dialog-accessibility-and-forms.md) - Validate user input in dialogs
- [Routing Integration](references/dialog-advanced-patterns.md) - Use dialogs with Angular routing

## Predefined Dialogs

This skill covers building alert, confirm, and prompt dialogs using Syncfusion's `DialogUtility` — a zero-template, utility-first approach to displaying modal feedback and user-input dialogs in Angular applications.

### Which Dialog Type?

| Need | Dialog Type | API |
|------|------------|-----|
| Warn/inform user, single OK | Alert | `DialogUtility.alert(...)` |
| Ask for confirmation (OK + Cancel) | Confirm | `DialogUtility.confirm(...)` |
| Collect user input (HTML content + OK + Cancel) | Prompt | `DialogUtility.confirm(...)` with input in `content` |

> **Key insight:** Angular's predefined dialogs have no separate "prompt" method — use `DialogUtility.confirm()` with custom HTML in the `content` property to build a prompt pattern.

### Quick Start

```bash
ng add @syncfusion/ej2-angular-popups
```

```typescript
// src/app/app.ts
import { Component } from '@angular/core';
import { DialogModule } from '@syncfusion/ej2-angular-popups';
import { ButtonModule } from '@syncfusion/ej2-angular-buttons';
import { DialogUtility } from '@syncfusion/ej2-popups';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [DialogModule, ButtonModule],
  template: `
    <button ejs-button cssClass="e-danger" (click)="showAlert()">Alert</button>
    <button ejs-button cssClass="e-success" (click)="showConfirm()" style="margin-left:8px">Confirm</button>
    <button ejs-button [isPrimary]="true" (click)="showPrompt()" style="margin-left:8px">Prompt</button>
  `
})
export class App {
  showAlert(): void {
    DialogUtility.alert({
      title: 'Warning',
      content: 'Disk space is running low.',
      width: '280px'
    });
  }

  showConfirm(): void {
    const dlg = DialogUtility.confirm({
      title: 'Delete Item',
      content: 'Are you sure you want to delete this item?',
      width: '300px',
      okButton: { text: 'Yes', click: () => { dlg.hide(); /* handle confirm */ } },
      cancelButton: { text: 'No', click: () => { dlg.hide(); } }
    });
  }

  showPrompt(): void {
    const dlg = DialogUtility.confirm({
      title: 'Enter Name',
      content: '<p>Your name:</p><input id="nameInput" class="e-input" type="text" placeholder="Type here..." />',
      width: '300px',
      okButton: {
        text: 'Submit',
        click: () => {
          const value = (document.getElementById('nameInput') as HTMLInputElement).value;
          dlg.hide();
          // use value
        }
      },
      cancelButton: { text: 'Cancel', click: () => dlg.hide() }
    });
  }
}
```

```css
/* styles.css */
@import '../node_modules/@syncfusion/ej2-base/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-icons/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-buttons/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-angular-popups/styles/material3.css';
```

### Common Patterns

**Pattern 1 — Delete confirmation with icons:**
```typescript
DialogUtility.confirm({
  title: 'Delete Files',
  content: 'Permanently delete selected files?',
  width: '300px',
  okButton: { text: 'Yes', icon: 'e-icons e-check' },
  cancelButton: { text: 'No', icon: 'e-icons e-close' }
});
```

**Pattern 2 — Alert with close button + ESC support:**
```typescript
DialogUtility.alert({
  title: 'Session Expired',
  content: 'Your session has expired. Please log in again.',
  width: '300px',
  showCloseIcon: true,
  closeOnEscape: true
});
```

**Pattern 3 — Positioned modal confirm:**
```typescript
DialogUtility.confirm({
  title: 'Confirm Action',
  content: 'Submit the form?',
  isModal: true,
  position: { X: 'center', Y: 'center' },
  animationSettings: { effect: 'Zoom' },
  isDraggable: true,
  width: '280px'
});
```

### Key Properties at a Glance

| Property | Purpose | Default |
|----------|---------|---------|
| `title` | Dialog header text | — |
| `content` | Body text or HTML string | — |
| `width` | Dialog width (px or %) | `'100%'` |
| `isModal` | Overlay + modal behavior | `false` |
| `isDraggable` | Allow header drag to reposition | `false` |
| `showCloseIcon` | Show × close button | `false` |
| `closeOnEscape` | Close on ESC key | `false` |
| `position` | `{ X, Y }` — predefined or offset | `center/center` |
| `animationSettings` | `{ effect, duration, delay }` | `Fade, 400ms` |
| `okButton` | OK button config `{ text, icon, click }` | — |
| `cancelButton` | Cancel button config `{ text, icon, click }` | — |
| `cssClass` | Custom CSS class on dialog root | `''` |
| `zIndex` | Stacking order | `1000` |
| `open` | Callback after dialog opens | — |
| `close` | Callback after dialog closes | — |

### Documentation

#### Getting Started
📄 **Read:** [references/getting-started.md](references/predefineddialog-getting-started.md)
- Installation and package setup
- CSS imports and theme options
- Basic alert, confirm, and prompt examples
- All `DialogUtility` option properties

#### Customization
📄 **Read:** [references/customization.md](references/predefineddialog-customization.md)
- Button text and icon customization
- Show/hide close icon and ESC behavior
- Custom HTML content in dialogs
- Programmatic dialog close with `hide()`

#### Position and Dimension
📄 **Read:** [references/position-and-dimension.md](references/predefineddialog-position-and-dimension.md)
- Position X/Y values and offset usage
- Width and height properties
- Max-width/max-height via `cssClass`
- Min-width/min-height via `cssClass`

#### Animation and Draggable
📄 **Read:** [references/animation-and-draggable.md](references/predefineddialog-animation-and-draggable.md)
- `animationSettings` effect options (Zoom, Fade, FadeZoom, etc.)
- Duration and delay configuration
- `isDraggable` for all dialog types

#### Events and Patterns
📄 **Read:** [references/events-and-patterns.md](references/predefineddialog-events-and-patterns.md)
- `open` and `close` event callbacks
- `isModal`, `zIndex`, `cssClass` advanced usage
- Common real-world patterns (delete confirm, form prompt, info alert)
- Managing multiple dialog instances

#### API Reference
📄 **Read:** [references/api.md](references/predefineddialog-api.md)
- Complete `DialogUtility.alert()` and `DialogUtility.confirm()` options
- `okButton` / `cancelButton` ButtonArgs properties
- `AnimationSettingsModel` properties
- `PositionDataModel` properties
- `DialogComponent` properties, methods, and events

## Tooltip

The Syncfusion Angular Tooltip (`ejs-tooltip`) displays a pop-up with information or a message when you hover, click, focus, or touch a target element. It supports 12 positions, animations, HTML/template/AJAX content, sticky mode, mouse trailing, and full accessibility compliance.

### Navigation Guide

#### Getting Started
📄 **Read:** [references/getting-started.md](references/tooltip-getting-started.md)
- Installation and package setup (`ng add @syncfusion/ej2-angular-popups`)
- CSS theme imports
- Basic single-target tooltip
- Multi-target tooltip with `target` property
- Standalone (Angular 19+) and module-based setup

#### Content
📄 **Read:** [references/content.md](references/tooltip-content.md)
- Static text and HTML string content
- Template content using `ng-template`
- Dynamic content via AJAX/Fetch in `beforeRender` event
- Loading HTML elements (iframes, videos) in tooltip
- `enableHtmlParse` and `enableHtmlSanitizer` options

#### Position & Dimensions
📄 **Read:** [references/position-and-dimension.md](references/tooltip-position-and-dimension.md)
- All 12 position values (`TopCenter`, `BottomLeft`, etc.)
- Tip pointer show/hide and position
- Mouse trailing
- Offset values (`offsetX`, `offsetY`)
- Width, height, and scroll mode
- Window collision handling

#### Open Modes
📄 **Read:** [references/open-mode.md](references/tooltip-open-mode.md)
- `opensOn`: Auto, Hover, Click, Focus, Custom
- Combining multiple open modes
- Custom mode with programmatic `open()`/`close()`
- Sticky mode (`isSticky`)
- Open/close delay

#### Animation
📄 **Read:** [references/animation.md](references/tooltip-animation.md)
- `animation` property with open/close settings
- All supported animation effects
- Applying animations via `open()`/`close()` methods
- Custom transition effects

#### Customization & Style
📄 **Read:** [references/customization-and-style.md](references/tooltip-customization-and-style.md)
- `cssClass` for custom styles
- CSS class reference for tooltip structure
- Tip pointer customization
- Fancy tips (curved, bubble)
- SVG and canvas tooltips
- Tooltips on disabled elements
- Container, RTL, htmlAttributes

#### Accessibility
📄 **Read:** [references/accessibility.md](references/tooltip-accessibility.md)
- WCAG 2.2, Section 508 compliance
- WAI-ARIA attributes
- Keyboard navigation
- Screen reader support

#### API Reference
📄 **Read:** [references/api.md](references/tooltip-api.md)
- All properties, methods, and events
- Type definitions and defaults
- `TooltipEventArgs`, `AnimationModel`, `TooltipAnimationSettings`
- `Position`, `TipPointerPosition`, and `Effect` enumerations

### Quick Start

```bash
ng add @syncfusion/ej2-angular-popups
```

```typescript
// src/app/app.ts (Angular 19+ standalone)
import { Component, ViewEncapsulation } from '@angular/core';
import { TooltipModule } from '@syncfusion/ej2-angular-popups';

@Component({
  standalone: true,
  imports: [TooltipModule],
  selector: 'app-root',
  encapsulation: ViewEncapsulation.None,
  template: `
    <ejs-tooltip content="Hello, I am a Tooltip!" position="BottomCenter">
      <button>Hover me</button>
    </ejs-tooltip>
  `
})
export class App {}
```

```css
/* styles.css */
@import "@syncfusion/ej2-base/styles/material3.css";
@import "@syncfusion/ej2-angular-buttons/styles/material3.css";
@import "@syncfusion/ej2-angular-popups/styles/material3.css";
```

### Common Patterns

#### Multi-target tooltip (single instance)
```html
<!-- Wraps a container; target selector picks which children get tooltips -->
<ejs-tooltip target=".has-tip">
  <div id="container">
    <button class="has-tip" title="Save your work">Save</button>
    <button class="has-tip" title="Delete selected item">Delete</button>
    <button>No tooltip here</button>
  </div>
</ejs-tooltip>
```

#### Tooltip that opens on click
```html
<ejs-tooltip content="Clicked!" opensOn="Click" position="RightCenter">
  <button>Click me</button>
</ejs-tooltip>
```

#### Sticky tooltip with close button
```html
<ejs-tooltip content="I stay until you close me." [isSticky]="true">
  <span>Hover and pin me</span>
</ejs-tooltip>
```

#### HTML content tooltip
```typescript
public htmlContent: string = '<b>Bold</b> and <i>italic</i> text with a <a href="#">link</a>.';
```
```html
<ejs-tooltip [content]="htmlContent">
  <button>Rich content</button>
</ejs-tooltip>
```

#### Programmatic open/close (custom mode)
```typescript
@ViewChild('tooltip') tooltip!: TooltipComponent;

openTip(): void {
  this.tooltip.open(this.tooltip.element);
}
closeTip(): void {
  this.tooltip.close();
}
```
```html
<ejs-tooltip #tooltip content="Custom trigger" opensOn="Custom">
  <span>Target</span>
</ejs-tooltip>
<button (click)="openTip()">Show</button>
<button (click)="closeTip()">Hide</button>
```

### Key Properties at a Glance

| Property | Type | Default | Purpose |
|---|---|---|---|
| `content` | `string \| HTMLElement` | — | Tooltip content |
| `position` | `Position` | `'TopCenter'` | Where tooltip appears |
| `opensOn` | `string` | `'Auto'` | Trigger: Auto/Hover/Click/Focus/Custom |
| `isSticky` | `boolean` | `false` | Keep open until manually closed |
| `mouseTrail` | `boolean` | `false` | Follow mouse pointer |
| `openDelay` | `number` | `0` | Delay (ms) before opening |
| `closeDelay` | `number` | `0` | Delay (ms) before closing |
| `animation` | `AnimationModel` | FadeIn/FadeOut 150ms | Open/close animation |
| `target` | `string` | — | Selector for multi-target |
| `cssClass` | `string` | `null` | Custom CSS class |
| `showTipPointer` | `boolean` | `true` | Show/hide arrow tip |
| `width` / `height` | `string \| number` | `'auto'` | Dimensions |

> For full property, method, and event reference, read [references/api.md](references/tooltip-api.md).
