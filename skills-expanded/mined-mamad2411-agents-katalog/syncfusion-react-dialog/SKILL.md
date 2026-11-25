---
name: syncfusion-react-dialog
description: Create interactive dialogs and modal windows in React with Syncfusion DialogComponent. Implement modal/modeless dialogs with custom positioning, dragging, resizing, animations, templating, and keyboard navigation. Use this skill whenever the user needs to display dialog boxes, modal windows, confirmation prompts, forms in popups, floating panels, or complex windowed interactions.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Layout"
---

# Implementing React Dialog

The DialogComponent displays content in a floating window with support for modal and modeless modes, custom positioning, dragging, resizing, animations, templating, and comprehensive accessibility features.

## Component Overview

**DialogComponent Features:**
- **Modal/Modeless modes**: Control parent interaction blocking
- **9 preset positions + custom X/Y**: Flexible placement
- **Dragging**: Header-based drag and drop (allowDragging)
- **Resizing**: Diagonal resize grip (enableResize)
- **Templating**: Custom header, content, footer
- **Animations**: 16 effects (Fade, Zoom, Flip, Slide, FadeZoom, etc.)
- **Buttons**: Built-in action buttons with click handlers
- **Events**: open, close, beforeOpen, beforeClose, drag, dragStart, dragStop, resize events
- **Keyboard Navigation**: Tab, Escape (closeOnEscape), Enter
- **WCAG 2.2 Accessibility**: ARIA roles, focus management
- **Localization**: 20+ locales via locale property
- **RTL Support**: Right-to-left rendering

## Documentation & Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation (`@syncfusion/ej2-react-popups`)
- CSS/theme imports (material, bootstrap, tailwind)
- Basic DialogComponent JSX structure
- show()/hide() methods and refs
- Functional component patterns with hooks
- Initial visibility with visible prop

### Modal vs Modeless
📄 **Read:** [references/modal-vs-modeless.md](references/modal-vs-modeless.md)
- isModal boolean property (true/false)
- Modal overlay behavior and parent blocking
- Modeless floating behavior
- Focus management differences
- When to choose each mode
- Side-by-side comparisons

### Positioning and Dragging
📄 **Read:** [references/positioning-and-dragging.md](references/positioning-and-dragging.md)
- position object (X: 'center'|'left'|'right'|number, Y: 'top'|'center'|'bottom'|number)
- 9 preset position combinations
- Custom pixel-based positioning
- allowDragging boolean property
- enableResize and resizeHandles configuration
- Target element constraints with target prop

### Templates and Content
📄 **Read:** [references/templates-and-content.md](references/templates-and-content.md)
- content property (string, HTML, JSX function)
- header property (text or template)
- footerTemplate (custom footer JSX)
- Dynamic content updates
- HTML sanitization (enableHtmlSanitizer)
- Styling content and edge cases

### Buttons and Actions
📄 **Read:** [references/buttons-and-actions.md](references/buttons-and-actions.md)
- buttons array with ButtonPropsModel[]
- ButtonPropsModel structure (buttonModel, click, isFlat, type)
- buttonModel properties (content, isPrimary, cssClass)
- Click event handlers
- Styling buttons with cssClass
- Button types (Button, Submit, Reset)

### Animation Effects
📄 **Read:** [references/animation-effects.md](references/animation-effects.md)
- AnimationSettingsModel (effect, duration, delay)
- 16 animation effects (Fade, FadeZoom, FlipLeftDown, FlipLeftUp, etc.)
- Duration in milliseconds
- Delay before animation starts
- Disable animations (effect: 'None')
- Performance considerations

### Localization and Accessibility
📄 **Read:** [references/localization-and-accessibility.md](references/localization-and-accessibility.md)
- locale property for culture/language
- WCAG 2.2 compliance
- Keyboard navigation (Tab, Enter, Escape)
- closeOnEscape behavior control
- ARIA roles and attributes
- Screen reader support
- RTL support with enableRtl
- Focus management patterns

### Advanced Patterns
📄 **Read:** [references/advanced-patterns.md](references/advanced-patterns.md)
- Events: open, close, beforeOpen, beforeClose, drag, dragStart, dragStop, resizeStart, resizeStop, resizing
- Nested and stacked dialogs
- Forms with validation
- AJAX content loading
- Prevent close logic (beforeClose event)
- Full-screen dialogs
- HTML sanitization and security
- CSS classes and z-index management
- Enable persistence (enablePersistence)
- Common edge cases and troubleshooting

### API Reference (Complete)
📄 **Read:** [references/api-reference.md](references/api-reference.md)
- All 24 DialogModel properties with types and defaults
- All 11 events with event arguments
- Methods: show(), hide(), refresh(), destroy()
- ButtonPropsModel structure (buttonModel, click, isFlat, type)
- AnimationSettingsModel with all 16 effects
- Types and enumerations
- Quick reference patterns

## Quick Start Example

**Basic Modal Dialog:**

```jsx
import React, { useRef, useState } from 'react';
import { DialogComponent } from '@syncfusion/ej2-react-popups';
import '@syncfusion/ej2-base/styles/material.css';
import '@syncfusion/ej2-buttons/styles/material.css';
import '@syncfusion/ej2-popups/styles/material.css';

export default function App() {
  const dialogRef = useRef(null);
  const [isOpen, setIsOpen] = useState(false);

  const handleOpen = () => {
    dialogRef.current?.show();
    setIsOpen(true);
  };

  const handleClose = () => {
    dialogRef.current?.hide();
    setIsOpen(false);
  };

  const buttons = [
    {
      buttonModel: {
        content: 'OK',
        cssClass: 'e-flat',
        isPrimary: true,
      },
      click: handleClose,
    },
    {
      buttonModel: {
        content: 'Cancel',
        cssClass: 'e-flat',
      },
      click: handleClose,
    },
  ];

  return (
    <div id="dialog-target" style={{ position: 'relative', width: '100%', minHeight: '400px' }}>
      <button onClick={handleOpen} className="e-control e-btn e-primary">
        Open Dialog
      </button>

      <DialogComponent
        ref={dialogRef}
        header="Confirm Action"
        buttons={buttons}
        showCloseIcon={true}
        target="#dialog-target"
        width="400px"
        isModal={true}
        visible={false}
      >
        <p>Are you sure you want to proceed with this action?</p>
      </DialogComponent>
    </div>
  );
}
```

## Common Patterns

### Pattern 1: Confirmation Dialog
Delete action with confirmation buttons:
```jsx
const buttons = [
  {
    buttonModel: { content: 'Delete', cssClass: 'e-flat e-danger', isPrimary: true },
    click: () => { performDelete(); dialogRef.current?.hide(); }
  },
  {
    buttonModel: { content: 'Cancel', cssClass: 'e-flat' },
    click: () => dialogRef.current?.hide()
  }
];
```

### Pattern 2: Form Dialog
Dialog with form inputs and validation:
```jsx
<DialogComponent header="Edit Profile" buttons={buttons} isModal={true} width="500px">
  <div style={{ padding: '16px' }}>
    <input type="text" placeholder="Name" className="form-control" />
    <input type="email" placeholder="Email" className="form-control" />
    <textarea placeholder="Bio" className="form-control"></textarea>
  </div>
</DialogComponent>
```

### Pattern 3: Centered Dialog
Position dialog in center of screen:
```jsx
<DialogComponent
  header="Alert"
  position={{ X: 'center', Y: 'center' }}
  isModal={true}
  showCloseIcon={true}
  width="350px"
>
  This dialog is centered on the screen.
</DialogComponent>
```

### Pattern 4: Draggable Floating Panel
Non-modal, draggable properties panel:
```jsx
<DialogComponent
  header="Properties"
  isModal={false}
  allowDragging={true}
  position={{ X: 200, Y: 150 }}
  width="300px"
  enableResize={true}
  resizeHandles={['All']}
  showCloseIcon={true}
>
  Drag me around! I don't block the page.
</DialogComponent>
```

### Pattern 5: Animated Dialog
Dialog with Zoom animation:
```jsx
<DialogComponent
  header="Welcome"
  animationSettings={{ effect: 'Zoom', duration: 400, delay: 0 }}
  isModal={true}
  position={{ X: 'center', Y: 'center' }}
  width="400px"
>
  This dialog zooms in smoothly!
</DialogComponent>
```

### Pattern 6: Custom Footer Template
Custom footer instead of buttons:
```jsx
<DialogComponent
  header="Custom Footer"
  isModal={true}
  footerTemplate={
    <div style={{ padding: '12px', textAlign: 'right' }}>
      <button className="e-control e-btn e-primary" style={{ marginRight: '8px' }}>
        Save
      </button>
      <button className="e-control e-btn">Cancel</button>
    </div>
  }
>
  Dialog content with custom footer.
</DialogComponent>
```

### Pattern 7: Nested Dialogs
Parent dialog containing child dialog:
```jsx
const childDialogRef = useRef(null);

<DialogComponent header="Parent" isModal={true} width="400px">
  <button onClick={() => childDialogRef.current?.show()} className="e-control e-btn">
    Open Child Dialog
  </button>
  
  <DialogComponent
    ref={childDialogRef}
    header="Child"
    isModal={true}
    width="300px"
    visible={false}
  >
    Nested dialog content
  </DialogComponent>
</DialogComponent>
```

## Key Props (DialogModel)

| Prop | Type | Description | Default | When to Use |
|------|------|-------------|---------|------------|
| `isModal` | boolean | Enable modal mode (blocks parent interaction) | false | Confirmations, alerts, critical actions |
| `visible` | boolean | Initial visibility state | false | Control initial dialog display |
| `header` | string \| JSX | Dialog header/title | - | Every dialog needs a title |
| `content` | string \| HTML \| JSX | Dialog body content | - | Main dialog information |
| `buttons` | ButtonPropsModel[] | Action buttons in footer | - | For OK/Cancel, action confirmations |
| `footerTemplate` | JSX | Custom footer content | - | When buttons prop doesn't fit |
| `showCloseIcon` | boolean | Show close button in header | false | Allow users to dismiss |
| `position` | PositionData | X/Y positioning (center, top, etc.) | { X: 'center', Y: 'center' } | Custom placement |
| `allowDragging` | boolean | Enable drag functionality | false | Movable dialogs, floating panels |
| `enableResize` | boolean | Enable resize with grip | false | Resizable dialogs |
| `resizeHandles` | ResizeDirections[] | Which edges/corners resize | ['All'] | Control resize behavior |
| `width` | string \| number | Dialog width | '330px' | Control dialog size |
| `height` | string \| number | Dialog height | 'auto' | Control dialog size |
| `minHeight` | string \| number | Minimum height | - | Prevent too-small resize |
| `animationSettings` | AnimationSettingsModel | Animation effect/duration/delay | - | Smooth open/close transitions |
| `closeOnEscape` | boolean | Close on Escape key press | true | Keyboard navigation |
| `target` | string (selector) | Container element | document.body | Modal positioning |
| `enableHtmlSanitizer` | boolean | Sanitize HTML content | true | Security (prevent XSS) |
| `cssClass` | string | Custom CSS classes | - | Styling and theming |
| `enableRtl` | boolean | Right-to-left rendering | false | RTL languages |
| `locale` | string | Culture/language code | 'en-US' | Localization |
| `zIndex` | number | Stack order | - | Manage overlapping dialogs |
| `enablePersistence` | boolean | Persist state on reload | false | Remember size/position |

## Common Use Cases

1. **Confirmation Dialogs** - Confirm delete, submit, or critical actions before proceeding
2. **Alert/Info Popups** - Display system messages, warnings, or notifications
3. **Form Dialogs** - Edit profiles, settings, or create new records in modal forms
4. **Input Prompts** - Collect user input for specific actions (e.g., "Enter file name")
5. **Properties Panels** - Draggable, non-modal panels for settings or properties
6. **Multi-Step Workflows** - Nested dialogs for step-by-step processes
7. **Loading/Processing** - Show progress indicators or loading states
8. **Help/Documentation** - Contextual help, tips, or tutorial overlays
9. **Image Galleries** - Lightbox dialogs for images or media previews
10. **Settings/Preferences** - Organize application settings in tabbed dialogs

---

**Next:** Choose a reference based on what you need to implement. All references include working code examples, best practices, and troubleshooting guidance.
