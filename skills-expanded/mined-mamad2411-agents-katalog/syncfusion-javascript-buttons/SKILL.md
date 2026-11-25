---
name: syncfusion-javascript-buttons
description: Implement and configure the Syncfusion EJ2 JavaScript Buttons components (ProgressButton, RadioButton, and SplitButton). Use this when adding interactive button controls, progress indicators, radio selections, or dual-action menus in a JavaScript or ES5 application. This skill covers component configuration, states, events, templates, accessibility, and common UI patterns.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Buttons"
---

# Syncfusion JavaScript Buttons

## ProgressButton

The Syncfusion EJ2 JavaScript **ProgressButton** visualizes the progression of an operation, indicating to the user that a background process is running. It supports a background filler UI, spinner customization, content animation, progress events, and programmatic start/stop control.

---

### Navigation Guide

#### Getting Started
📄 **Read:** [references/getting-started.md](references/progressbutton-getting-started.md)
- Install `@syncfusion/ej2-splitbuttons` and set up dependencies
- Initialize ProgressButton with `new ProgressButton({...})`
- TypeScript setup via webpack quickstart
- Add CSS/theme references (local and CDN)
- Enable the background filler with `enableProgress: true`
- Minimal working ES5 and TypeScript examples

#### Spinner and Progress
📄 **Read:** [references/spinner-and-progress.md](references/progressbutton-spinner-and-progress.md)
- Change spinner position (`spinSettings.position`: Left/Right/Top/Bottom/Center)
- Change spinner size (`spinSettings.width`)
- Use a custom spinner template (`spinSettings.template`)
- Animate button content during progress (`animationSettings.effect`, `duration`, `easing`)
- Control progress step intervals via `ProgressEventArgs.step` in the `begin` event
- Dynamically change progress percentage via `ProgressEventArgs.percent`
- Start and stop progress programmatically with `start()` and `stop()` methods

#### Events
📄 **Read:** [references/events.md](references/progressbutton-events.md)
- `begin` — fires when progress starts, use to set initial state
- `progress` — fires at each step interval, use to update UI
- `end` — fires when progress completes, use to reset or show success
- `fail` — fires when progress is incomplete
- `created` — fires after the component renders
- Tracing all events and logging pattern

#### How-To Patterns
📄 **Read:** [references/how-to.md](references/progressbutton-how-to.md)
- Hide the spinner using `e-hide-spinner` CSS class
- Change text content and styles of the button during progress
- Customize progress direction: vertical (`e-vertical`), top (`e-progress-top`), reverse
- Use `dataBind()` to apply property changes immediately

#### Accessibility
📄 **Read:** [references/accessibility.md](references/progressbutton-accessibility.md)
- WCAG 2.2 and Section 508 compliance
- WAI-ARIA attributes (`aria-label`, `aria-disabled`)
- Keyboard navigation (`Enter` / `Space` to start progress)
- Screen reader, RTL, and mobile device support

#### API Reference
📄 **Read:** [references/api.md](references/progressbutton-api.md)
- All properties with types and defaults
- `SpinSettingsModel` interface (position, template, width)
- `AnimationSettingsModel` interface (effect, duration, easing)
- `ProgressEventArgs` interface (percent, step, currentDuration, name)
- All methods: `start()`, `stop()`, `dataBind()`, `progressComplete()`, `destroy()`
- All events: `begin`, `progress`, `end`, `fail`, `created`

---

### Quick Start

#### TypeScript

**index.html**
```html
<!DOCTYPE html>
<html>
<head>
  <link href="https://cdn.syncfusion.com/ej2/ej2-base/styles/material.css" rel="stylesheet" />
  <link href="https://cdn.syncfusion.com/ej2/ej2-buttons/styles/material.css" rel="stylesheet" />
  <link href="https://cdn.syncfusion.com/ej2/ej2-popups/styles/material.css" rel="stylesheet" />
  <link href="https://cdn.syncfusion.com/ej2/ej2-splitbuttons/styles/material.css" rel="stylesheet" />
</head>
<body>
  <button id="progressbtn"></button>
  <script src="bundle.js"></script>
</body>
</html>
```

```typescript
import { ProgressButton } from '@syncfusion/ej2-splitbuttons';

const progressBtn: ProgressButton = new ProgressButton({
  content: 'Spin Left',
  enableProgress: true
});
progressBtn.appendTo('#progressbtn');
```

---

### Common Patterns

#### Download button with pause/resume
```typescript
import { ProgressButton } from '@syncfusion/ej2-splitbuttons';

const progressBtn: ProgressButton = new ProgressButton({
  content: 'Download',
  enableProgress: true,
  duration: 4000,
  iconCss: 'e-btn-sb-icon e-download',
  cssClass: 'e-hide-spinner',
  end: (): void => {
    progressBtn.content = 'Download';
    progressBtn.iconCss = 'e-btn-sb-icon e-download';
    progressBtn.dataBind();
  }
});
progressBtn.appendTo('#progressbtn');

progressBtn.element.addEventListener('click', (): void => {
  if (progressBtn.content === 'Download') {
    progressBtn.content = 'Pause';
    progressBtn.iconCss = 'e-btn-sb-icon e-pause';
    progressBtn.dataBind();
  } else if (progressBtn.content === 'Pause') {
    progressBtn.content = 'Resume';
    progressBtn.iconCss = 'e-btn-sb-icon e-play';
    progressBtn.dataBind();
    progressBtn.stop();
  } else if (progressBtn.content === 'Resume') {
    progressBtn.content = 'Pause';
    progressBtn.iconCss = 'e-btn-sb-icon e-pause';
    progressBtn.dataBind();
    progressBtn.start();
  }
});
```

#### Upload button with text state changes
```typescript
import { ProgressButton } from '@syncfusion/ej2-splitbuttons';

const uploadBtn: ProgressButton = new ProgressButton({
  content: 'Upload',
  cssClass: 'e-hide-spinner',
  enableProgress: true,
  duration: 4000,
  begin: (): void => {
    uploadBtn.content = 'Uploading...';
    uploadBtn.cssClass = 'e-hide-spinner e-info';
    uploadBtn.dataBind();
  },
  end: (): void => {
    uploadBtn.content = 'Success';
    uploadBtn.cssClass = 'e-hide-spinner e-success';
    uploadBtn.dataBind();
    setTimeout((): void => {
      uploadBtn.content = 'Upload';
      uploadBtn.cssClass = 'e-hide-spinner';
      uploadBtn.dataBind();
    }, 500);
  }
});
uploadBtn.appendTo('#progressbtn');
```

#### Spinner on the right with custom size
```typescript
import { ProgressButton } from '@syncfusion/ej2-splitbuttons';

const progressBtn: ProgressButton = new ProgressButton({
  content: 'Submit',
  spinSettings: { position: 'Right', width: 20 }
});
progressBtn.appendTo('#progressbtn');
```
## RadioButton

The Syncfusion EJ2 JavaScript RadioButton is a graphical UI element that lets a user select exactly one option from a group. It supports checked/unchecked states, label positioning, small size, disabled state, RTL layout, form integration via `name`/`value`, custom CSS appearance, full keyboard navigation, and WCAG 2.2 accessibility — all from the `@syncfusion/ej2-buttons` package.

### Navigation Guide

#### Getting Started (TypeScript)
📄 **Read:** [references/getting-started.md](references/radiobutton-getting-started.md)
- Package dependencies (`ej2-buttons`, `ej2-base`)
- Webpack quickstart project setup
- CSS theme imports
- Basic TypeScript rendering example
- Checked and unchecked states

#### Label and Size
📄 **Read:** [references/label-and-size.md](references/radiobutton-label-and-size.md)
- Setting label text with the `label` property
- Positioning the label before or after the button (`labelPosition: 'Before'` / `'After'`)
- Small size RadioButton using `cssClass: 'e-small'`
- Default size RadioButton

#### How-To Scenarios
📄 **Read:** [references/how-to.md](references/radiobutton-how-to.md)
- Set the disabled state using `disabled: true`
- Display selected label via `change` event
- Enable RTL layout using `enableRtl: true`
- Use `name` and `value` for HTML form submission
- Customize appearance with semantic CSS classes (`e-primary`, `e-success`, `e-info`, `e-warning`, `e-danger`)

#### Accessibility
📄 **Read:** [references/accessibility.md](references/radiobutton-accessibility.md)
- WCAG 2.2, Section 508, and ADA compliance
- WAI-ARIA attributes (`aria-disabled`)
- Keyboard interaction (Up/Left arrow, Down/Right arrow)
- Screen reader support and color contrast

#### API Reference
📄 **Read:** [references/api.md](references/radiobutton-api.md)
- All properties: `checked`, `cssClass`, `disabled`, `enableHtmlSanitizer`, `enablePersistence`, `enableRtl`, `htmlAttributes`, `label`, `labelPosition`, `locale`, `name`, `value`
- All methods: `appendTo`, `click`, `dataBind`, `destroy`, `focusIn`, `getRootElement`, `getSelectedValue`, `refresh`, `addEventListener`, `removeEventListener`
- All events: `change` (`ChangeArgs`), `created`

### Quick Start

#### TypeScript

```typescript
import { RadioButton } from '@syncfusion/ej2-buttons';
import { enableRipple } from '@syncfusion/ej2-base';

enableRipple(true);

// Initialize RadioButton component
let radiobutton: RadioButton = new RadioButton({ label: 'Option 1', name: 'default' });
radiobutton.appendTo('#element1');

radiobutton = new RadioButton({ label: 'Option 2', name: 'default', checked: true });
radiobutton.appendTo('#element2');
```

```html
<!-- index.html -->
<input id="element1" type="radio" />
<input id="element2" type="radio" />
```

#### TypeScript (module setup)

**index.html**
```html
<!DOCTYPE html>
<html>
<head>
  <link href="https://cdn.syncfusion.com/ej2/ej2-base/styles/material.css" rel="stylesheet" />
  <link href="https://cdn.syncfusion.com/ej2/ej2-buttons/styles/material.css" rel="stylesheet" />
</head>
<body>
  <input id="radio1" type="radio" />
  <input id="radio2" type="radio" />
  <script src="bundle.js"></script>
</body>
</html>
```

```typescript
import { RadioButton } from '@syncfusion/ej2-buttons';
import { enableRipple } from '@syncfusion/ej2-base';

enableRipple(true);

const rb1: RadioButton = new RadioButton({ label: 'Option 1', name: 'default' });
rb1.appendTo('#radio1');

const rb2: RadioButton = new RadioButton({ label: 'Option 2', name: 'default', checked: true });
rb2.appendTo('#radio2');
```

### Common Patterns

#### RadioButton group with change event
```typescript
import { RadioButton, ChangeEventArgs } from '@syncfusion/ej2-buttons';

let rb1: RadioButton = new RadioButton({
  label: 'Option 1',
  name: 'group',
  checked: true,
  change: (args: ChangeEventArgs) => {
    console.log('Selected: ' + (args.event.target as HTMLInputElement).value);
  }
});
rb1.appendTo('#element1');
```

#### Small-size RadioButton
```typescript
import { RadioButton } from '@syncfusion/ej2-buttons';

let rb: RadioButton = new RadioButton({ label: 'Small', name: 'size', cssClass: 'e-small' });
rb.appendTo('#element');
```

#### Disabled RadioButton
```typescript
import { RadioButton } from '@syncfusion/ej2-buttons';

let rb: RadioButton = new RadioButton({ label: 'Disabled Option', name: 'group', disabled: true });
rb.appendTo('#element');
```
## SplitButton

The Syncfusion EJ2 JavaScript SplitButton renders a dual-action button: the primary button triggers a default action, and the secondary arrow button opens a contextual popup menu with additional action items. It supports icons, separators, item/popup templating, RTL, disabled state, keyboard navigation, and full accessibility — all from the `ej2-splitbuttons` package.

### Navigation Guide

#### Getting Started
📄 **Read:** [references/getting-started.md](references/splitbutton-getting-started.md)
- Package dependencies (`ej2-splitbuttons`, `ej2-base`, `ej2-buttons`, `ej2-popups`)
- Local script/style setup
- CDN-based setup
- Minimal working example (ES5 global namespace)
- Rendering via `appendTo()`, `items` configuration

#### Icons and Separator
📄 **Read:** [references/icons-and-separator.md](references/splitbutton-icons-and-separator.md)
- Adding icons via `iconCss` property
- Positioning icons: `Left` (default) and `Top`
- Vertical SplitButton using `e-vertical` CSS class and `cssClass`
- Adding horizontal separators between popup items via `separator: true`

#### Popup Items
📄 **Read:** [references/popup-items.md](references/splitbutton-popup-items.md)
- Adding icons to popup action items via `iconCss` on `ItemModel`
- Item templating with `beforeItemRender` event
- Popup templating using the `target` property with a custom HTML element
- `addItems()` and `removeItems()` methods for dynamic item management

#### How-To Scenarios
📄 **Read:** [references/how-to.md](references/splitbutton-how-to.md)
- Enable RTL (right-to-left) layout
- Set disabled state
- Group popup items using ListView
- Open a Dialog on popup item click via `select` event
- Underline a character in popup item text using `beforeItemRender`

#### Accessibility
📄 **Read:** [references/accessibility.md](references/splitbutton-accessibility.md)
- WCAG 2.2, Section 508, ADA compliance
- WAI-ARIA attributes: `role`, `aria-haspopup`, `aria-expanded`, `aria-owns`, `aria-disabled`
- Keyboard shortcuts (Esc, Enter, Space, Arrow keys, Alt+Arrow)
- Screen reader support, RTL, color contrast

#### API Reference
📄 **Read:** [references/api.md](references/splitbutton-api.md)
- All properties: `content`, `items`, `iconCss`, `iconPosition`, `cssClass`, `disabled`, `enableRtl`, `target`, `itemTemplate`, `animationSettings`, `closeActionEvents`, `createPopupOnClick`, `popupWidth`, `enableHtmlSanitizer`, `enablePersistence`, `locale`
- All methods: `appendTo`, `toggle`, `addItems`, `removeItems`, `dataBind`, `refresh`, `destroy`, `focusIn`, `getRootElement`
- All events: `click`, `select`, `beforeOpen`, `open`, `beforeClose`, `close`, `beforeItemRender`, `created`

### Quick Start

#### TypeScript

**index.html**
```html
<!DOCTYPE html>
<html>
<head>
  <link href="https://cdn.syncfusion.com/ej2/ej2-base/styles/material.css" rel="stylesheet" />
  <link href="https://cdn.syncfusion.com/ej2/ej2-buttons/styles/material.css" rel="stylesheet" />
  <link href="https://cdn.syncfusion.com/ej2/ej2-popups/styles/material.css" rel="stylesheet" />
  <link href="https://cdn.syncfusion.com/ej2/ej2-splitbuttons/styles/material.css" rel="stylesheet" />
</head>
<body>
  <button id="element">Paste</button>
  <script src="bundle.js"></script>
</body>
</html>
```

```typescript
import { SplitButton, ItemModel } from '@syncfusion/ej2-splitbuttons';
import { enableRipple } from '@syncfusion/ej2-base';

enableRipple(true);

const items: ItemModel[] = [
  { text: 'Cut' },
  { text: 'Copy' },
  { text: 'Paste' }
];

const splitBtn: SplitButton = new SplitButton({ items: items });
splitBtn.appendTo('#element');
```

### Common Patterns

#### SplitButton with icon (left position, default)
```typescript
import { SplitButton, ItemModel } from '@syncfusion/ej2-splitbuttons';

const items: ItemModel[] = [{ text: 'Cut' }, { text: 'Copy' }, { text: 'Paste' }];

const splitBtn: SplitButton = new SplitButton({
  content: 'Paste',
  iconCss: 'e-icons e-paste',
  items: items
});
splitBtn.appendTo('#element');
```

#### SplitButton with click and select event handlers
```typescript
import { SplitButton, ItemModel, ClickEventArgs, MenuEventArgs } from '@syncfusion/ej2-splitbuttons';

const items: ItemModel[] = [{ text: 'Cut' }, { text: 'Copy' }, { text: 'Paste' }];

const splitBtn: SplitButton = new SplitButton({
  content: 'Paste',
  items: items,
  click: (args: ClickEventArgs): void => {
    console.log('Primary button clicked');
  },
  select: (args: MenuEventArgs): void => {
    console.log('Selected item: ' + args.item.text);
  }
});
splitBtn.appendTo('#element');
```

#### Disabled SplitButton
```typescript
import { SplitButton, ItemModel } from '@syncfusion/ej2-splitbuttons';

const items: ItemModel[] = [{ text: 'Cut' }, { text: 'Copy' }, { text: 'Paste' }];

const splitBtn: SplitButton = new SplitButton({
  content: 'Paste',
  items: items,
  disabled: true
});
splitBtn.appendTo('#element');
```
