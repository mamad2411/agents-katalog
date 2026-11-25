---
name: syncfusion-javascript-popups
description: Comprehensive guide for implementing Syncfusion TypeScript Dialog (popup) components. Use this when building modal or modeless dialogs, alert/confirm windows, or DialogUtility-based prompts in TypeScript/EJ2 projects. Covers animations, drag, resize, nested dialogs, templates, and WAI-ARIA accessibility.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Popups"
---

# Implementing Syncfusion TypeScript Popups

## Dialog

A comprehensive skill for implementing the Syncfusion Dialog component in TypeScript. The Dialog displays content in an overlay window above the main page, supporting modal/modeless modes, custom templates, action buttons, animations, drag, resize, and built-in utility dialogs (alert/confirm).

### Documentation and Navigation Guide

#### Getting Started
📄 **Read:** [references/dialog-getting-started.md](references/dialog-getting-started.md)
- Package installation and dependencies
- CSS imports and theme setup
- Basic dialog initialization and rendering
- Modal dialog usage
- Enabling header and close icon
- Configuring action buttons in footer
- Draggable dialog setup
- Dialog positioning with `position` property
- Showing and hiding dialogs (`show()`, `hide()`)

#### Templates
📄 **Read:** [references/dialog-templates.md](references/dialog-templates.md)
- Header template with HTML content
- Content template using DOM elements
- Footer template vs buttons property
- Dynamic content loading patterns
- Template with Rich Text Editor (RTE) in modal dialog

#### Features and Configuration
📄 **Read:** [references/dialog-features.md](references/dialog-features.md)
- Animation settings (`animationSettings`: effect, duration, delay)
- Resize feature (`enableResize`, `resizeHandles`)
- Localization (`locale` property and `L10n.load`)
- Z-index control (`zIndex`)
- Persistence (`enablePersistence`)
- RTL support (`enableRtl`)
- CSS customization (`cssClass`)
- Fullscreen dialog via `show(true)`
- Setting max height via `beforeOpen` event
- Scroll position centering with `cssClass: 'e-fixed'`
- Setting `minHeight` on Dialog's parent element to ensure minimum visible space
- Nested dialogs

#### Events and Control Flow
📄 **Read:** [references/dialog-events.md](references/dialog-events.md)
- `beforeOpen` — prevent opening, set maxHeight
- `beforeClose` — prevent closing, prevent focus return
- `open` — post-open actions, prevent focus on first element
- `close` — post-close actions
- `overlayClick` — close dialog on overlay click
- Drag events: `drag`, `dragStart`, `dragStop`
- Resize events: `resizeStart`, `resizing`, `resizeStop`
- `created`, `destroyed` events

#### How-To Scenarios
📄 **Read:** [references/dialog-how-to.md](references/dialog-how-to.md)
- Add minimize/maximize buttons to dialog header
- Add icons to dialog footer buttons
- Close dialog when clicking outside (non-modal)
- Create nested dialogs
- Customize dialog appearance with DOM element content
- Display dialog at custom X/Y position
- Load dialog content using AJAX
- Prevent focus on first element when dialog opens
- Prevent focus returning to previous element on close
- Read form values from dialog on button click
- Render dialog without header
- Show dialog in fullscreen mode

#### Dialog Utility Functions
📄 **Read:** [references/dialog-dialog-utility.md](references/dialog-dialog-utility.md)
- `DialogUtility.alert()` — simple and with options
- `DialogUtility.confirm()` — simple and with options
- Closing utility dialogs programmatically
- Available utility options: title, content, okButton, cancelButton, isModal, position, showCloseIcon, closeOnEscape, animationSettings, cssClass, zIndex, open, close, isDraggable

#### Accessibility
📄 **Read:** [references/dialog-accessibility.md](references/dialog-accessibility.md)
- WAI-ARIA roles and attributes
- Keyboard navigation shortcuts
- WCAG 2.2 and Section 508 compliance
- Screen reader support
- RTL support

#### API Reference
📄 **Read:** [references/dialog-api.md](references/dialog-api.md)
- All properties with types and defaults
- All methods with signatures
- All events with argument types
- `AnimationSettingsModel` sub-properties
- `ButtonPropsModel` sub-properties

### Quick Start

```typescript
import { Dialog } from '@syncfusion/ej2-popups';
import { enableRipple } from '@syncfusion/ej2-base';

enableRipple(true);

// HTML: <div id="dialog"></div>
// HTML: <button id="openBtn">Open Dialog</button>

let dialog: Dialog = new Dialog({
    header: 'Welcome',
    content: 'This is a simple dialog.',
    showCloseIcon: true,
    width: '350px',
    target: document.body,
    buttons: [
        {
            buttonModel: { content: 'OK', isPrimary: true },
            click: () => { dialog.hide(); }
        }
    ]
});
dialog.appendTo('#dialog');

document.getElementById('openBtn').onclick = () => { dialog.show(); };
```

### Common Patterns

#### Modal Dialog (with overlay)
```typescript
import { Dialog } from '@syncfusion/ej2-popups';

let dialog: Dialog = new Dialog({
    header: 'Confirm Action',
    content: 'Are you sure you want to proceed?',
    isModal: true,
    showCloseIcon: true,
    width: '400px',
    target: document.body,
    overlayClick: () => { dialog.hide(); },
    buttons: [
        { buttonModel: { content: 'Yes', isPrimary: true }, click: () => { /* action */ dialog.hide(); } },
        { buttonModel: { content: 'No', cssClass: 'e-flat' }, click: () => { dialog.hide(); } }
    ]
});
dialog.appendTo('#dialog');
```

#### Alert and Confirm via DialogUtility
```typescript
import { DialogUtility } from '@syncfusion/ej2-popups';

// Simple alert
DialogUtility.alert('Operation completed successfully!');

// Confirm with custom actions
DialogUtility.confirm({
    title: 'Delete Item',
    content: 'This action cannot be undone. Continue?',
    okButton: { text: 'Delete', click: () => { /* delete logic */ } },
    cancelButton: { text: 'Cancel' },
    showCloseIcon: true,
    closeOnEscape: true
});
```

#### Set minHeight on Dialog Parent Element
```typescript
import { Dialog } from '@syncfusion/ej2-popups';

// Set minHeight on the parent/target element so the Dialog always
// has enough vertical space to render correctly inside its container.
const container = document.getElementById('container') as HTMLElement;
container.style.minHeight = '400px';

let dialog: Dialog = new Dialog({
    header: 'Notice',
    content: 'Dialog rendered inside a container with minHeight.',
    showCloseIcon: true,
    width: '350px',
    target: container,       // Dialog is scoped to this container
    buttons: [
        {
            buttonModel: { content: 'OK', isPrimary: true },
            click: () => { dialog.hide(); }
        }
    ]
});
dialog.appendTo('#dialog');

(document.getElementById('targetButton') as HTMLElement).onclick = () => {
    dialog.show();
};
```

#### Prevent Dialog from Closing (Validation)
```typescript
import { Dialog } from '@syncfusion/ej2-popups';

let dialog: Dialog = new Dialog({
    header: 'Login',
    content: document.getElementById('loginForm'),
    isModal: true,
    width: '350px',
    target: document.body,
    beforeClose: (args) => {
        const username = (document.getElementById('username') as HTMLInputElement).value;
        if (!username) {
            args.cancel = true;  // prevent close
            alert('Please enter a username');
        }
    },
    buttons: [
        { buttonModel: { content: 'Login', isPrimary: true }, click: () => { dialog.hide(); } }
    ]
});
dialog.appendTo('#dialog');
```

### Key Properties

| Property | Type | Default | Purpose |
|---|---|---|---|
| `header` | string \| HTMLElement | `''` | Dialog title text or HTML |
| `content` | string \| HTMLElement | `''` | Dialog body content |
| `isModal` | boolean | `false` | Show as modal with overlay |
| `showCloseIcon` | boolean | `false` | Show × button in header |
| `visible` | boolean | `true` | Initial visibility |
| `width` | string \| number | `'100%'` | Dialog width |
| `height` | string \| number | `'auto'` | Dialog height |
| `position` | PositionDataModel | `{X:'center',Y:'center'}` | Position in target |
| `target` | HTMLElement \| string | `null` (body) | Container element |
| `buttons` | ButtonPropsModel[] | `[{}]` | Footer action buttons |
| `footerTemplate` | string \| HTMLElement | `''` | Custom footer HTML |
| `allowDragging` | boolean | `false` | Enable header drag |
| `enableResize` | boolean | `false` | Enable resize handles |
| `resizeHandles` | ResizeDirections[] | `['South-East']` | Resize directions |
| `animationSettings` | AnimationSettingsModel | `{effect:'Fade',duration:400,delay:0}` | Open/close animation |
| `cssClass` | string | `''` | Custom CSS classes |
| `closeOnEscape` | boolean | `true` | Close on Esc key |
| `zIndex` | number | `1000` | Stack order |
| `locale` | string | `''` | Culture for localization |
| `enableRtl` | boolean | `false` | Right-to-left mode |

### Common Use Cases

- **Confirmation prompts** — Use `isModal: true` with OK/Cancel buttons and `beforeClose` validation
- **Form dialogs** — Load DOM element as `content`, read values in button click handler
- **Alert messages** — Use `DialogUtility.alert()` for minimal code
- **Lightbox / image viewer** — Fullscreen via `dialog.show(true)`
- **Nested workflows** — Use `target` pointing to outer dialog element for nested dialogs
- **Repositionable dialogs** — `allowDragging: true` requires `header` to be set
- **Container sizing** — Set `minHeight: '400px'` on the Dialog's parent element when using a scoped `target` to guarantee the Dialog has sufficient vertical space to render without clipping
