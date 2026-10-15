---
name: syncfusion-angular-buttons
description: Comprehensive guide for implementing Syncfusion Angular button components including Button, ButtonGroup, DropDownButton, Floating Action Button (FAB), ProgressButton, RadioButton, Switch, Speed Dial, SplitButtons. Use this when implementing and styling these components - covering visual styles (primary, outline, toggle, icon, round, block), grouping, dropdowns with popup items and animations, FAB positioning/scoping, Speed Dial linear/radial action items, progress-enabled buttons, and toggle/radio controls.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Buttons"
---

# Implementing Syncfusion Angular Buttons

## Button

The Syncfusion Angular Button is a graphical user interface element rendered via the `ejs-button` directive. It triggers an action on click and supports text, icons, or both — with extensive styling, accessibility, and behavioral options.

### Navigation Guide

#### Getting Started
📄 **Read:** [references/button-getting-started.md](references/button-getting-started.md)
- Prerequisites and package dependencies
- Setting up a new Angular application (standalone architecture)
- Installing `@syncfusion/ej2-angular-buttons` via `ng add`
- CSS/theme imports for Material and other themes
- Rendering the first `ejs-button` directive
- Changing button type using `cssClass`

#### Types and Styles
📄 **Read:** [references/button-types-and-styles.md](references/button-types-and-styles.md)
- Predefined color styles (`e-primary`, `e-success`, `e-info`, `e-warning`, `e-danger`, `e-link`)
- Basic HTML types: submit and reset buttons
- Flat, outline, round, and toggle button types
- Toggle button active state via `e-active` class
- Icon buttons using `iconCss` and `iconPosition`
- SVG icon support
- Button sizes: small (`e-small`) vs normal

#### How-To Patterns
📄 **Read:** [references/button-how-to.md](references/button-how-to.md)
- Create a block (full-width) button using `e-block`
- Create a rounded-corner button with custom CSS
- Add a navigation link inside a button
- Customize button appearance with a custom CSS class
- Style native `<input>` and `<a>` elements as buttons
- Set disabled state with `[disabled]="true"`
- Enable right-to-left (RTL) support with `[enableRtl]="true"`
- Add a tooltip on hover using the `created` event
- Implement a repeat button using mouse and touch events

#### Accessibility
📄 **Read:** [references/button-accessibility.md](references/button-accessibility.md)
- WCAG 2.2 and Section 508 compliance details
- WAI-ARIA attributes (`aria-label` for icon-only buttons)
- Keyboard interaction: Space key behavior
- Screen reader support and automated testing tools

#### EJ1 Migration
📄 **Read:** [references/button-ej1-migration.md](references/button-ej1-migration.md)
- Property mapping from EJ1 to EJ2 (e.g., `text` → `content`, `prefixIcon` → `iconCss`)
- Method and event equivalents
- Properties not available in EJ2

#### API Reference
📄 **Read:** [references/button-api.md](references/button-api.md)
- All properties with types, defaults, and code samples
- Methods: `click()`, `focusIn()`, `destroy()`
- Events: `created`

---

### Quick Start

```bash
ng add @syncfusion/ej2-angular-buttons
```

```typescript
// src/app/app.ts (Angular 20+) or src/app/app.component.ts (Angular 19 and below)
import { ButtonModule } from '@syncfusion/ej2-angular-buttons';
import { Component } from '@angular/core';

@Component({
  imports: [ButtonModule],
  standalone: true,
  selector: 'app-root',
  template: `
    <div class="e-section-control">
      <button ejs-button>Default</button>
      <button ejs-button cssClass="e-primary">Primary</button>
      <button ejs-button cssClass="e-success">Success</button>
    </div>
  `
})
export class AppComponent { }
```

> **Angular 20+ note:** The CLI generates `src/app/app.ts`, `app.html`, and `app.css` (no `.component.` suffix). In Angular 19 and below, the file is `app.component.ts`.

---

### Common Patterns

#### Color-Styled Buttons
```html
<button ejs-button cssClass="e-primary">Primary</button>
<button ejs-button cssClass="e-success">Success</button>
<button ejs-button cssClass="e-warning">Warning</button>
<button ejs-button cssClass="e-danger">Danger</button>
```

#### Icon Button
```html
<button ejs-button iconCss="e-icons e-save">Save</button>
<button ejs-button iconCss="e-icons e-delete" iconPosition="Right">Delete</button>
```

#### Toggle Button
```typescript
// In component class
@ViewChild('togglebtn') togglebtn: ButtonComponent | any;
@HostListener('click', ['togglebtn'])
btnClick() {
  if (this.togglebtn.element.classList.contains('e-active')) {
    this.togglebtn.content = 'Pause';
  } else {
    this.togglebtn.content = 'Play';
  }
}
```
```html
<button #togglebtn ejs-button cssClass="e-flat" [isToggle]="true" content="Play"></button>
```

#### Disabled Button
```html
<button ejs-button [disabled]="true">Disabled</button>
```

#### Block (Full-Width) Button
```html
<button ejs-button cssClass="e-block e-primary">Full Width</button>
```

---

## ButtonGroup

The Syncfusion Angular ButtonGroup is a **CSS-only component** that groups multiple buttons together into a single cohesive UI element. It supports horizontal and vertical layouts, radio/checkbox selection behaviors, outline and color styles, icon buttons, nested split/dropdown buttons, RTL, form integration, and full accessibility compliance.

**Package:** `@syncfusion/ej2-angular-buttons`
**Container class:** `.e-btn-group`
**Button directive:** `ejs-button` (from `ButtonModule`)

---

### Navigation Guide

#### Getting Started
📄 **Read:** [references/buttongroup-getting-started.md](references/buttongroup-getting-started.md)
- Installing `@syncfusion/ej2-angular-buttons` via `ng add`
- `ButtonModule` import in standalone component's `imports[]`
- CSS theme imports for material theme
- Basic horizontal ButtonGroup with `ejs-button`
- Vertical orientation using `e-vertical` class

#### Types and Styles
📄 **Read:** [references/buttongroup-types-and-styles.md](references/buttongroup-types-and-styles.md)
- Outline ButtonGroup (`e-outline` on container + each button)
- Color styles: `e-primary`, `e-success`, `e-info`, `e-warning`, `e-danger` via `cssClass`
- Rounded corners with `e-round-corner`
- Icon buttons using `iconCss` property

#### Selection (Radio & Checkbox)
📄 **Read:** [references/buttongroup-selection.md](references/buttongroup-selection.md)
- Single selection (radio type) with `<input type="radio">` + `<label class="e-btn">`
- Multiple selection (checkbox type) with `<input type="checkbox">` + `<label class="e-btn">`
- Show pre-selected state on initial render using `checked` attribute
- Nesting DropDownButton or SplitButton inside a group

#### How-To Recipes
📄 **Read:** [references/buttongroup-how-to.md](references/buttongroup-how-to.md)
- Disable individual button or entire group
- Enable ripple effect
- RTL (right-to-left) layout
- Form submission with radio/checkbox button groups
- Programmatic initialization using `createButtonGroup` utility

#### Accessibility
📄 **Read:** [references/buttongroup-accessibility.md](references/buttongroup-accessibility.md)
- WCAG 2.2 / Section 508 compliance
- Keyboard navigation shortcuts (normal, checkbox, radio behaviors)
- Screen reader guidance

---

### Quick Start

**1. Install the package:**
```bash
ng add @syncfusion/ej2-angular-buttons
```

**2. Add CSS to `styles.css`:**
```css
@import 'node_modules/@syncfusion/ej2-base/styles/material.css';
@import 'node_modules/@syncfusion/ej2-buttons/styles/material.css';
@import 'node_modules/@syncfusion/ej2-splitbuttons/styles/material.css';
```

**3. Create a basic ButtonGroup:**
```typescript
import { Component } from '@angular/core';
import { ButtonModule } from '@syncfusion/ej2-angular-buttons';

@Component({
  imports: [ButtonModule],
  standalone: true,
  selector: 'app-root',
  template: `
    <div class='e-btn-group'>
      <button ejs-button>HTML</button>
      <button ejs-button>CSS</button>
      <button ejs-button>JavaScript</button>
    </div>`
})
export class AppComponent { }
```

---

### Common Patterns

#### Vertical ButtonGroup
Add `e-vertical` to the container — buttons stack top-to-bottom:
```html
<div class='e-btn-group e-vertical'>
  <button ejs-button>HTML</button>
  <button ejs-button>CSS</button>
  <button ejs-button>JavaScript</button>
</div>
```
> `e-vertical` does **not** support nesting SplitButton.

#### Outline Style
Add `e-outline` to container and `cssClass='e-outline'` to each button:
```html
<div class='e-btn-group e-outline'>
  <button ejs-button cssClass='e-outline'>HTML</button>
  <button ejs-button cssClass='e-outline'>CSS</button>
  <button ejs-button cssClass='e-outline'>JavaScript</button>
</div>
```

#### Radio Selection (Single Select)
```html
<div class='e-btn-group'>
  <input type="radio" id="radioleft" name="align" value="left"/>
  <label class="e-btn" for="radioleft">Left</label>
  <input type="radio" id="radiomiddle" name="align" value="middle"/>
  <label class="e-btn" for="radiomiddle">Center</label>
  <input type="radio" id="radioright" name="align" value="right"/>
  <label class="e-btn" for="radioright">Right</label>
</div>
```

#### Checkbox Selection (Multi Select)
```html
<div class='e-btn-group'>
  <input type="checkbox" id="check_bold" name="font" value="bold"/>
  <label class="e-btn" for="check_bold">Bold</label>
  <input type="checkbox" id="check_italic" name="font" value="italic"/>
  <label class="e-btn" for="check_italic">Italic</label>
  <input type="checkbox" id="check_underline" name="font" value="underline"/>
  <label class="e-btn" for="check_underline">Underline</label>
</div>
```

---

### Key Decision Guide

| User Need | Approach |
|---|---|
| Group action buttons visually | Basic `e-btn-group` with `ejs-button` |
| Only one option selectable at a time | Radio type (input[radio] + label.e-btn) |
| Multiple options selectable | Checkbox type (input[checkbox] + label.e-btn) |
| Stack buttons vertically | Add `e-vertical` to container |
| Buttons with icons | `iconCss` property on each `ejs-button` |
| Rounded edges on group | `e-round-corner` on container |
| RTL layout | `e-rtl` on container |
| Programmatic initialization | `createButtonGroup` from `@syncfusion/ej2-splitbuttons` |
| Extend group with dropdown/popup | Nest `ejs-dropdownbutton` or `ejs-splitbutton` |

---

## DropDownButton

The Syncfusion Angular DropDownButton is a graphical UI element rendered via the `ejs-dropdownbutton` directive. It displays a button that opens a popup menu of action items when clicked. It supports icons, custom templates, animations, navigation links, accessibility, RTL, and dynamic item management.

---

### Navigation Guide

#### Getting Started
📄 **Read:** [references/dropdownbutton-getting-started.md](references/dropdownbutton-getting-started.md)
- Prerequisites and package dependencies
- Setting up a new Angular application (standalone architecture)
- Installing `@syncfusion/ej2-angular-splitbuttons` via `ng add`
- CSS/theme imports for Material and other themes
- Rendering the first `ejs-dropdownbutton` directive
- Defining `ItemModel[]` action items

#### Icons and Appearance
📄 **Read:** [references/dropdownbutton-icons-and-appearance.md](references/dropdownbutton-icons-and-appearance.md)
- Button icon with `iconCss` and `iconPosition` (Left, Top)
- Vertical button layout using `e-vertical` cssClass
- Icon-only button with `e-caret-hide` cssClass
- Sprite image as button icon
- Hiding the dropdown arrow
- Rounded corner styling
- Customizing icon size and button width
- Changing the caret/dropdown arrow icon dynamically

#### Popup Items and Templating
📄 **Read:** [references/dropdownbutton-popup-items.md](references/dropdownbutton-popup-items.md)
- Icons on popup action items via `iconCss`
- Navigation links via `url` property on items
- Separator items using `separator: true`
- Item-level templating with `beforeItemRender` event
- Full popup templating using `target` property
- `itemTemplate` property for custom item rendering
- Grouping items with ListView as popup target
- Underlining a character in item text

#### Events and Interactivity
📄 **Read:** [references/dropdownbutton-events.md](references/dropdownbutton-events.md)
- `select` — handle item selection
- `open` / `close` — popup open/close callbacks
- `beforeOpen` / `beforeClose` — cancel or customize before open/close
- `beforeItemRender` — customize each item during render
- `created` — component initialized callback
- Opening a dialog on popup item click
- Changing popup open position via `open` event

#### Animation
📄 **Read:** [references/dropdownbutton-animation.md](references/dropdownbutton-animation.md)
- `animationSettings` property overview
- Supported effects: None, SlideDown, ZoomIn, FadeIn
- Configuring `duration` and `easing`

#### Configuration and Behavior
📄 **Read:** [references/dropdownbutton-configuration.md](references/dropdownbutton-configuration.md)
- Disabling the DropDownButton via `disabled`
- RTL support via `enableRtl`
- `popupWidth` for consistent popup sizing
- `createPopupOnClick` for deferred popup creation
- `enableHtmlSanitizer` for safe HTML rendering
- `closeActionEvents` to customize popup close trigger
- `enablePersistence` for state persistence
- Dynamic item management: `addItems`, `removeItems`, `toggle`

#### API Reference
📄 **Read:** [references/dropdownbutton-api.md](references/dropdownbutton-api.md)
- All properties with types, defaults, and descriptions
- All events with argument types
- All methods with parameters and return types
- `ItemModel` interface fields
- Supporting interfaces: `BeforeOpenCloseMenuEventArgs`, `MenuEventArgs`, `OpenCloseMenuEventArgs`

#### Accessibility
📄 **Read:** [references/dropdownbutton-accessibility.md](references/dropdownbutton-accessibility.md)
- WCAG 2.2 / Section 508 compliance
- WAI-ARIA attributes and roles
- Keyboard navigation shortcuts
- Screen reader support
- RTL support

---

### Quick Start

```typescript
import { Component } from '@angular/core';
import { DropDownButtonModule, ItemModel } from '@syncfusion/ej2-angular-splitbuttons';

@Component({
  standalone: true,
  imports: [DropDownButtonModule],
  selector: 'app-root',
  template: `
    <button ejs-dropdownbutton [items]="items" content="Clipboard" iconCss="e-icons e-copy" (select)="onSelect($event)"></button>
  `
})
export class AppComponent {
  public items: ItemModel[] = [
    { text: 'Cut',   iconCss: 'e-icons e-cut' },
    { text: 'Copy',  iconCss: 'e-icons e-copy' },
    { text: 'Paste', iconCss: 'e-icons e-paste' }
  ];

  onSelect(args: any) {
    console.log('Selected:', args.item.text);
  }
}
```

---

### Common Patterns

#### Popup with separator groups
```typescript
public items: ItemModel[] = [
  { text: 'Cut' },
  { text: 'Copy' },
  { text: 'Paste' },
  { separator: true },
  { text: 'Font' },
  { text: 'Paragraph' }
];
```

#### Icon-only button (no text, no caret)
```html
<button ejs-dropdownbutton [items]="items" iconCss="e-icons e-menu" cssClass="e-caret-hide"></button>
```

#### Vertical layout with top icon
```html
<button ejs-dropdownbutton [items]="items" content="Paste" iconCss="e-icons e-paste" iconPosition="Top" cssClass="e-vertical"></button>
```

#### RTL layout
```html
<button ejs-dropdownbutton [items]="items" content="Message" enableRtl="true"></button>
```

#### Custom popup width
```html
<button ejs-dropdownbutton [items]="items" [popupWidth]="'250px'" content="Options"></button>
```

#### Navigation items
```typescript
public items: ItemModel[] = [
  { text: 'Home',   url: '/home' },
  { text: 'About',  url: '/about' }
];
```

---

## Floating Action Button

The Syncfusion Angular Floating Action Button (`ejs-fab`) is a circular button that floats above the UI and represents the primary action in an application. It supports flexible **positioning**, **icon + text content**, **predefined styles**, **events**, full **accessibility compliance**, and CSS customization.

**Package:** `@syncfusion/ej2-angular-buttons`
**Module:** `FabModule`
**Selector:** `ejs-fab`

---

### Navigation Guide

#### Getting Started
📄 **Read:** [references/floating-action-button-getting-started.md](references/floating-action-button-getting-started.md)
- Installing `@syncfusion/ej2-angular-buttons` via `ng add`
- CSS theme imports for Material theme
- `FabModule` import in standalone component
- Minimal `ejs-fab` setup
- Using `target` to scope FAB to a container
- Handling the `(click)` event

#### Icons and Content
📄 **Read:** [references/floating-action-button-icons.md](references/floating-action-button-icons.md)
- `iconCss` property for icon-only FAB
- `content` property for text label
- `iconPosition` for Left vs Right icon placement
- Combined icon + text FAB examples

#### Positions
📄 **Read:** [references/floating-action-button-positions.md](references/floating-action-button-positions.md)
- `position` property with all nine predefined values (`TopLeft` → `BottomRight`)
- `target` property to scope FAB to a container element
- Custom CSS position using `cssClass`
- Calling `refreshPosition()` after target resize

#### Styles and Appearance
📄 **Read:** [references/floating-action-button-styles.md](references/floating-action-button-styles.md)
- Predefined `cssClass` values: `e-primary`, `e-outline`, `e-info`, `e-success`, `e-warning`, `e-danger`
- CSS class override reference table (`.e-fab.e-btn`, hover, focus, active, icon)
- Show text on hover with CSS transition
- Outline color customization

#### Events
📄 **Read:** [references/floating-action-button-events.md](references/floating-action-button-events.md)
- `(created)` event for post-render initialization
- `(click)` event for click handling

#### Accessibility
📄 **Read:** [references/floating-action-button-accessibility.md](references/floating-action-button-accessibility.md)
- WCAG 2.2 / Section 508 compliance summary
- WAI-ARIA attributes (`aria-label`)
- Keyboard interaction (Space key)
- RTL support via `enableRtl`
- Screen reader guidance

#### API Reference
📄 **Read:** [references/floating-action-button-api.md](references/floating-action-button-api.md)
- All properties: `content`, `cssClass`, `disabled`, `enableHtmlSanitizer`, `enablePersistence`, `enableRtl`, `iconCss`, `iconPosition`, `isPrimary`, `isToggle`, `position`, `target`, `visible`
- Methods: `click()`, `destroy()`, `focusIn()`, `getPersistData()`, `refreshPosition()`
- Events: `created`, `click`

---

### Quick Start

```bash
ng add @syncfusion/ej2-angular-buttons
```

```css
/* styles.css – added automatically by ng add */
@import '../node_modules/@syncfusion/ej2-base/styles/material.css';
@import '../node_modules/@syncfusion/ej2-buttons/styles/material.css';
@import '../node_modules/@syncfusion/ej2-icons/styles/material.css';
```

```typescript
import { FabModule } from '@syncfusion/ej2-angular-buttons';
import { Component } from '@angular/core';

@Component({
  imports: [FabModule],
  standalone: true,
  selector: 'app-root',
  template: `
    <div id="targetElement" style="position:relative;min-height:350px;border:1px solid;"></div>
    <button ejs-fab id="fab" content="Add" target="#targetElement"></button>
  `
})
export class AppComponent { }
```

---

### Common Patterns

#### Icon-Only FAB (most common)
```typescript
import { FabModule } from '@syncfusion/ej2-angular-buttons';
import { Component } from '@angular/core';

@Component({
  imports: [FabModule],
  standalone: true,
  selector: 'app-root',
  template: `
    <div id="target" style="position:relative;min-height:350px;border:1px solid;"></div>
    <button ejs-fab id="fab" iconCss="e-icons e-edit" target="#target"></button>
  `
})
export class AppComponent { }
```

#### FAB with Click Handler
```typescript
import { FabModule } from '@syncfusion/ej2-angular-buttons';
import { Component } from '@angular/core';

@Component({
  imports: [FabModule],
  standalone: true,
  selector: 'app-root',
  template: `
    <div id="target" style="position:relative;min-height:350px;border:1px solid;"></div>
    <button ejs-fab id="fab" iconCss="e-icons e-edit" content="Edit"
      (click)="onFabClick()" target="#target"></button>
  `
})
export class AppComponent {
  onFabClick(): void {
    alert('FAB clicked!');
  }
}
```

#### FAB with Custom Style
```typescript
import { FabModule } from '@syncfusion/ej2-angular-buttons';
import { Component } from '@angular/core';

@Component({
  imports: [FabModule],
  standalone: true,
  selector: 'app-root',
  template: `
    <div id="target" style="position:relative;min-height:350px;border:1px solid;"></div>
    <button ejs-fab id="fab" iconCss="e-icons e-delete" cssClass="e-danger" target="#target"></button>
  `
})
export class AppComponent { }
```

---

### Key Props at a Glance

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `iconCss` | `string` | `''` | CSS class for the FAB icon |
| `content` | `string` | `''` | Text label displayed on/beside the FAB |
| `iconPosition` | `'Left' \| 'Right'` | `'Left'` | Icon placement relative to text |
| `position` | `FabPosition` | `'BottomRight'` | Predefined position within target/viewport |
| `target` | `string \| HTMLElement` | `''` | Container element selector for FAB scoping |
| `cssClass` | `string` | `''` | Custom CSS class(es) for styling |
| `disabled` | `boolean` | `false` | Disables the FAB |
| `visible` | `boolean` | `true` | Shows or hides the FAB |
| `isPrimary` | `boolean` | `true` | Applies primary styling |
| `enableRtl` | `boolean` | `false` | Right-to-left rendering |
| `enableHtmlSanitizer` | `boolean` | `true` | Sanitizes HTML in `content` |

---

## Speed Dial

The Syncfusion Angular Speed Dial component renders a floating action button that expands to reveal a set of action items. It is based on the `ejs-speeddial` directive and supports linear and radial display modes, flexible positioning, animations, modal overlay, custom templates, and full accessibility compliance.

---

### Navigation Guide

#### Getting Started
📄 **Read:** [references/speeddial-getting-started.md](references/speeddial-getting-started.md)
- Prerequisites and package dependencies
- Installing `@syncfusion/ej2-angular-buttons` via `ng add`
- CSS/theme imports
- Rendering the first `ejs-speeddial` directive with `items`
- Standalone vs NgModule architecture

#### Items and Animation
📄 **Read:** [references/speeddial-items-and-animation.md](references/speeddial-items-and-animation.md)
- Configuring action items (`SpeedDialItemModel`: `text`, `iconCss`, `id`, `title`, `disabled`)
- Icon-only, text-only, and icon-with-text item variants
- Disabling individual items
- Configuring open/close animation (`animation`, `SpeedDialAnimationSettingsModel`)
- Supported animation effects (Fade, Zoom, etc.)

#### Display Modes
📄 **Read:** [references/speeddial-display-modes.md](references/speeddial-display-modes.md)
- Linear mode: list-like display with `direction` (Up, Down, Left, Right, Auto)
- Radial mode: circular pattern using `mode='Radial'`
- Configuring radial settings (`radialSettings`: `direction`, `startAngle`, `endAngle`, `offset`)
- Choosing mode based on use case

#### Position and Visibility
📄 **Read:** [references/speeddial-position-and-visibility.md](references/speeddial-position-and-visibility.md)
- All nine `position` values (TopLeft → BottomRight)
- Using `target` to anchor Speed Dial within a container
- Opening items on hover via `opensOnHover`
- Programmatic show/hide using `show()` and `hide()` methods
- Refreshing button position using `refreshPosition()`
- Controlling visibility with `visible` property

#### Styles and Appearance
📄 **Read:** [references/styles-and-appearance.md](references/styles-and-appearance.md)
- Button icon customization: `openIconCss`, `closeIconCss`, `content`
- Predefined CSS styles via `cssClass` (`e-primary`, `e-success`, `e-warning`, etc.)
- Enabling/disabling the component with `disabled`
- Controlling visibility with `visible`
- Hover open behavior with `opensOnHover`
- Item tooltip via `title` field
- Custom CSS class usage

#### Templates
📄 **Read:** [references/speeddial-templates.md](references/speeddial-templates.md)
- Item template using `itemTemplate` and `<ng-template #itemTemplate>`
- Popup template using `popupTemplate` and `<ng-template #popupTemplate>`
- Template context and binding

#### Events
📄 **Read:** [references/speeddial-events.md](references/speeddial-events.md)
- `clicked` — action item clicked (`SpeedDialItemEventArgs`)
- `created` — component rendered
- `beforeOpen` / `onOpen` — popup opening lifecycle
- `beforeClose` / `onClose` — popup closing lifecycle
- `beforeItemRender` — each item rendered

#### Accessibility
📄 **Read:** [references/speeddial-accessibility.md](references/speeddial-accessibility.md)
- WCAG 2.2 and Section 508 compliance
- WAI-ARIA attributes (`role`, `aria-label`, `aria-expanded`, etc.)
- Keyboard shortcuts (Enter, Arrow keys, Esc, Home, End)
- Screen reader and RTL support

#### API Reference
📄 **Read:** [references/speeddial-api.md](references/speeddial-api.md)
- All component properties with types and defaults
- All methods: `show()`, `hide()`, `refreshPosition()`
- All events with their argument types
- `SpeedDialItemModel` fields
- `SpeedDialAnimationSettingsModel` fields
- `RadialSettingsModel` fields

---

### Quick Start

```typescript
import { Component } from '@angular/core';
import { SpeedDialModule, SpeedDialItemModel } from '@syncfusion/ej2-angular-buttons';

@Component({
  imports: [SpeedDialModule],
  standalone: true,
  selector: 'app-root',
  template: `
    <div id="target" style="position:relative; min-height:350px; border:1px solid;"></div>
    <button ejs-speeddial
      id="speeddial"
      content="Edit"
      openIconCss="e-icons e-edit"
      closeIconCss="e-icons e-close"
      target="#target"
      [items]="items"
      (clicked)="onItemClicked($event)">
    </button>
  `
})
export class AppComponent {
  public items: SpeedDialItemModel[] = [
    { text: 'Cut',   iconCss: 'e-icons e-cut' },
    { text: 'Copy',  iconCss: 'e-icons e-copy' },
    { text: 'Paste', iconCss: 'e-icons e-paste' }
  ];

  public onItemClicked(args: any) {
    console.log(args.item.text + ' clicked');
  }
}
```

---

### Common Patterns

#### Icon-only items with tooltips
```typescript
public items: SpeedDialItemModel[] = [
  { iconCss: 'e-icons e-cut',   title: 'Cut' },
  { iconCss: 'e-icons e-copy',  title: 'Copy' },
  { iconCss: 'e-icons e-paste', title: 'Paste' }
];
```

#### Radial menu
```html
<button ejs-speeddial id="speeddial"
  openIconCss="e-icons e-edit"
  closeIconCss="e-icons e-close"
  mode="Radial"
  position="MiddleCenter"
  target="#target"
  [items]="items"
  [radialSettings]="radialSettings">
</button>
```
```typescript
public radialSettings: RadialSettingsModel = {
  direction: 'AntiClockwise',
  startAngle: 180,
  endAngle: 360,
  offset: '80px'
};
```

#### Modal overlay
```html
<button ejs-speeddial id="speeddial"
  openIconCss="e-icons e-edit"
  [modal]="true"
  target="#target"
  [items]="items">
</button>
```

#### Programmatic show/hide
```typescript
@ViewChild('speeddial') speeddialObj: SpeedDialComponent;

show() { this.speeddialObj.show(); }
hide() { this.speeddialObj.hide(); }
```

## ProgressButton

The Syncfusion Angular **ProgressButton** (`ejs-progressbutton`) extends a standard button with built-in progress indication — a spinner and/or background filler UI — ideal for async operations, form submissions, or any action with a perceivable wait time.

### Navigation Guide

| Task | Reference File |
|---|---|
| Installation & basic setup | 📄 [references/getting-started.md](references/progressbutton-getting-started.md) |
| Spinner config & progress animation | 📄 [references/spinner-and-progress.md](references/progressbutton-spinner-and-progress.md) |
| How-to recipes (hide spinner, cssClass, events, text/style changes) | 📄 [references/how-to.md](references/progressbutton-how-to.md) |
| Accessibility & keyboard interaction | 📄 [references/accessibility.md](references/progressbutton-accessibility.md) |
| Full API — properties, methods, events, interfaces | 📄 [references/api.md](references/progressbutton-api.md) |

### Quick Start

```bash
# Install the package
ng add @syncfusion/ej2-angular-splitbuttons
```

```typescript
// src/app/app.ts (Angular 20+) or app.component.ts (Angular 19 and below)
import { Component } from '@angular/core';
import { ProgressButtonModule } from '@syncfusion/ej2-angular-splitbuttons';

@Component({
  standalone: true,
  imports: [ProgressButtonModule],
  selector: 'app-root',
  template: `
    <button ejs-progressbutton content="Upload" [enableProgress]="true"
            [duration]="3000">
    </button>
  `
})
export class AppComponent {}
```

```css
/* styles.css — or import individually */
@import '@syncfusion/ej2-base/styles/material.css';
@import '@syncfusion/ej2-buttons/styles/material.css';
@import '@syncfusion/ej2-popups/styles/material.css';
@import '@syncfusion/ej2-splitbuttons/styles/material.css';
```

### Common Patterns

#### Spinner on the right

```typescript
template: `
  <button ejs-progressbutton content="Submit"
          [spinSettings]="{ position: 'Right' }">
  </button>
`
```

#### Background filler + animation

```typescript
template: `
  <button ejs-progressbutton content="Download" [enableProgress]="true"
          [animationSettings]="{ effect: 'SlideLeft' }">
  </button>
`
```

#### Handle lifecycle events

```typescript
template: `
  <button ejs-progressbutton content="Send"
          (begin)="onBegin($event)"
          (progress)="onProgress($event)"
          (end)="onEnd($event)"
          (fail)="onFail($event)">
  </button>
`
// Component class
onBegin(args: any)    { console.log('Started:', args.percent); }
onProgress(args: any) { console.log('Progress:', args.percent); }
onEnd(args: any)      { console.log('Completed'); }
onFail(args: any)     { console.log('Failed'); }
```

#### Programmatic control

```typescript
@ViewChild('progressBtn') progressBtn!: ProgressButtonComponent;

startProgress()    { this.progressBtn.start(0); }
stopProgress()     { this.progressBtn.stop(); }
completeProgress() { this.progressBtn.progressComplete(); }
```

## Switch

A lightweight toggle component (`ejs-switch`) for on/off binary input. Supports checked state, labels, disabled, sizing, two-way binding, form integration, custom styling, events, and full WCAG 2.2 accessibility.

### Navigation Guide

#### Getting Started
📄 **Read:** [references/getting-started.md](references/switch-getting-started.md)
- Installation with `ng add @syncfusion/ej2-angular-buttons`
- Standalone component and NgModule setup
- Basic Switch with `checked` state
- CSS / SCSS theme imports
- Setting `onLabel` and `offLabel` text

#### Switch Features
📄 **Read:** [references/switch-features.md](references/switch-features.md)
- Disabled state (`disabled` property)
- Size variants — default and small (`cssClass: 'e-small'`)
- RTL support (`enableRtl`)
- Two-way data binding with `ngModel`
- Toggle programmatically with `toggle()` method
- State persistence across page reloads (`enablePersistence`)

#### Events & State Control
📄 **Read:** [references/events-and-state.md](references/switch-events-and-state.md)
- `change` event — react to user-driven state flips
- `beforeChange` event — intercept and cancel state change
- `created` event — run logic after component renders
- `click()` and `focusIn()` native methods

#### Form Integration
📄 **Read:** [references/form-integration.md](references/switch-form-integration.md)
- `name` and `value` attributes for form POST
- Rules: disabled / unchecked values are NOT submitted
- Template-driven two-way binding with `ngModel`
- Grouping switches by `name` in a form

#### Customization
📄 **Read:** [references/customization.md](references/switch-customization.md)
- `cssClass` for custom styles
- Reshape bar/handle (square corners via CSS)
- Custom bar colors for on/off states
- Enable ripple effect on Switch labels
- Extra HTML attributes via `htmlAttributes`

#### Accessibility
📄 **Read:** [references/accessibility.md](references/switch-accessibility.md)
- WCAG 2.2 / Section 508 / ADA compliance
- WAI-ARIA: `role="switch"`, `aria-disabled`
- Keyboard navigation (Space key to toggle)
- Screen reader support and RTL accessibility

#### API Reference
📄 **Read:** [references/api.md](references/switch-api.md)
- All properties, methods, and events with types and defaults
- `BeforeChangeEventArgs` and `ChangeEventArgs` interfaces

---

### Quick Start

```bash
ng add @syncfusion/ej2-angular-buttons
```

```typescript
// src/app/app.ts (Angular 19+ standalone)
import { Component } from '@angular/core';
import { SwitchModule } from '@syncfusion/ej2-angular-buttons';

@Component({
  standalone: true,
  imports: [SwitchModule],
  selector: 'app-root',
  template: `
    <ejs-switch [checked]="isOn" (change)="onToggle($event)"></ejs-switch>
  `
})
export class AppComponent {
  isOn = false;

  onToggle(args: any): void {
    console.log('Switch is now:', args.checked);
  }
}
```

```css
/* styles.css */
@import '../node_modules/@syncfusion/ej2-base/styles/material.css';
@import '../node_modules/@syncfusion/ej2-buttons/styles/material.css';
```

---

### Common Patterns

#### Checked by default
```html
<ejs-switch [checked]="true"></ejs-switch>
```

#### With ON / OFF labels
```html
<ejs-switch [checked]="true" onLabel="ON" offLabel="OFF"></ejs-switch>
```
> Labels are not displayed in Material themes. Avoid long custom text.

#### Small size
```html
<ejs-switch cssClass="e-small"></ejs-switch>
```

#### Disabled
```html
<ejs-switch [disabled]="true"></ejs-switch>
```

#### Two-way binding
```html
<ejs-switch [(ngModel)]="isEnabled"></ejs-switch>
<p>State: {{ isEnabled }}</p>
```

#### Prevent state change conditionally
```html
<ejs-switch (beforeChange)="onBeforeChange($event)"></ejs-switch>
```
```typescript
onBeforeChange(args: BeforeChangeEventArgs): void {
  // Cancel if condition not met
  if (!this.canToggle) {
    args.cancel = true;
  }
}
```

#### Programmatic toggle
```typescript
@ViewChild('switch') switchObj!: SwitchComponent;

toggle(): void {
  this.switchObj.toggle();
}
```

## RadioButton

The Syncfusion Angular RadioButton (`ejs-radiobutton`) is a form input component that lets users select exactly one option from a group. It supports labels, size variants, two-way binding, form integration, accessibility, and extensive customization.

### Navigation Guide

#### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Angular 19+/21 standalone setup
- Package installation via `ng add`
- CSS/SCSS theme imports
- Minimal RadioButton example
- Running the application

#### Labels, Sizes & States
📄 **Read:** [references/label-size-states.md](references/radio-button-label-size-states.md)
- `label` and `labelPosition` (Before/After)
- Size variants: default and small (`e-small`)
- `checked` and unchecked states
- `disabled` state
- `enablePersistence`

#### Forms & Data Binding
📄 **Read:** [references/forms-and-binding.md](references/radio-button-forms-and-binding.md)
- `name` attribute for grouping radio buttons
- `value` attribute for form submission
- Which values are sent on form submit
- Two-way binding with `[(ngModel)]`
- Binding a RadioButton group to a DropDownList

#### Customization & Advanced Features
📄 **Read:** [references/customization-and-advanced.md](references/radio-button-customization-and-advanced.md)
- Custom CSS classes and appearance styles
- Right-to-left (`enableRtl`)
- `htmlAttributes` for ARIA and data attributes
- `enableHtmlSanitizer` and `locale`
- Methods: `getSelectedValue()`, `click()`, `focusIn()`, `destroy()`

#### Accessibility
📄 **Read:** [references/accessibility.md](references/radio-button-accessibility.md)
- WCAG 2.2, Section 508, ADA compliance
- WAI-ARIA attributes
- Keyboard navigation shortcuts
- Screen reader support

#### API Reference
📄 **Read:** [references/api.md](references/radio-button-api.md)
- All properties with types, defaults, and usage examples
- All methods with signatures
- Events and `ChangeArgs` interface

---

### Quick Start

```typescript
import { Component } from '@angular/core';
import { RadioButtonModule } from '@syncfusion/ej2-angular-buttons';

@Component({
  standalone: true,
  imports: [RadioButtonModule],
  selector: 'app-root',
  template: `
    <ejs-radiobutton label="Option A" name="choice" value="a" [checked]="true"></ejs-radiobutton>
    <ejs-radiobutton label="Option B" name="choice" value="b"></ejs-radiobutton>
    <ejs-radiobutton label="Option C" name="choice" value="c"></ejs-radiobutton>
  `
})
export class AppComponent {}
```

> Always set a shared `name` attribute on buttons that belong to the same group — this enforces mutual exclusivity.

---

### Common Patterns

#### Detect Selection Change
```typescript
template: `
  <ejs-radiobutton label="Credit Card" name="payment" value="credit"
    (change)="onPaymentChange($event)">
  </ejs-radiobutton>
  <ejs-radiobutton label="Debit Card" name="payment" value="debit"
    (change)="onPaymentChange($event)">
  </ejs-radiobutton>
`

onPaymentChange(args: ChangeArgs): void {
  console.log('Selected value:', args.value);  // 'credit' or 'debit'
}
```

#### Two-Way Binding with ngModel
```typescript
// All buttons share [(ngModel)]="selectedValue"
template: `
  <ejs-radiobutton label="Monthly" name="plan" value="monthly"
    [(ngModel)]="selectedPlan">
  </ejs-radiobutton>
  <ejs-radiobutton label="Annual" name="plan" value="annual"
    [(ngModel)]="selectedPlan">
  </ejs-radiobutton>
  <p>Selected: {{ selectedPlan }}</p>
`
```

#### Small Size Variant
```typescript
<ejs-radiobutton label="Small Option" name="size" cssClass="e-small"></ejs-radiobutton>
```

#### Disabled RadioButton
```typescript
<ejs-radiobutton label="Unavailable" name="plan" [disabled]="true"></ejs-radiobutton>
```

---

### Key Properties at a Glance

| Property | Type | Default | Purpose |
|---|---|---|---|
| `label` | string | `''` | Caption text next to the button |
| `name` | string | `''` | Groups mutually exclusive buttons |
| `value` | string | `''` | Form submission value |
| `checked` | boolean | `false` | Pre-select the button |
| `disabled` | boolean | `false` | Disable interaction |
| `cssClass` | string | `''` | Custom CSS; use `'e-small'` for small size |
| `labelPosition` | RadioLabelPosition | `'After'` | `'Before'` or `'After'` |
| `enableRtl` | boolean | `false` | Right-to-left layout |

For the full API, read [`references/api.md`](references/radio-button-api.md).

## SplitButton

A comprehensive guide for implementing the Syncfusion Essential JS 2 SplitButton component in Angular applications. Learn to create split buttons with dropdown menus, manage items, handle events, customize styling, and integrate with forms.

## SplitButton Overview

The Syncfusion Angular SplitButton component is a versatile UI control that combines a primary button with a dropdown menu:

- **Dual-action design:** Primary action button + dropdown menu with multiple options
- **Item management:** Configure items with text, icons, separators, URLs, and disable states
- **Event system:** click (primary), select (item), open, close, beforeOpen events
- **Popup control:** Placement options, collision detection, offset adjustment, auto-positioning
- **Icon support:** Material Design icons, Font Awesome, Bootstrap icons, custom fonts
- **Customization:** CSS classes, themes (Material, Bootstrap, Fabric, Tailwind), dark mode
- **Template support:** Item templates with HTML content, image icons, custom rendering
- **Accessibility:** Full WCAG 2.2 compliance, keyboard navigation, ARIA attributes, RTL support
- **Forms integration:** Reactive Forms and template-driven forms support
- **Dynamic updates:** Add/remove items, update properties at runtime, state management

**Package:** `@syncfusion/ej2-angular-splitbuttons`

## Documentation Navigation

Read the following references based on your specific needs:

### Getting Started
📄 **Read:** [references/getting-started.md](references/split-button-getting-started.md)
- Package installation and module setup
- CSS theme imports and dependencies
- Basic SplitButton implementation
- Component initialization with items
- Event handler setup
- Running and testing setup

### Button Items Configuration
📄 **Read:** [references/button-items-configuration.md](references/split-button-items-configuration.md)
- ItemModel interface and properties
- Text and icon configuration
- URL navigation and external links
- Separators between items
- Item disable/enable states
- Dynamic item management
- Item click event handling

### Events & Methods
📄 **Read:** [references/events-and-methods.md](references/split-button-events-and-methods.md)
- click event (primary button action)
- select event (item selection from dropdown)
- open event (dropdown opens)
- close event (dropdown closes)
- beforeOpen event (before dropdown opens)
- Methods: `toggle()`, `addItems()`, `removeItems()`, `focusIn()`
- ViewChild access patterns
- Event argument types and handling

### Styling & Customization
📄 **Read:** [references/styling-and-customization.md](references/split-button-styling-and-customization.md)
- CSS class customization (.e-split-button, .e-dropdown-popup)
- Icon configuration (iconCss, prefix, suffix properties)
- Icon positioning (left, right, top, bottom)
- Theme selection (Material, Bootstrap, Fabric, Tailwind)
- Dark mode implementation
- RTL (Right-to-Left) support
- Custom CSS overrides and sizing

### Templates & Icons
📄 **Read:** [references/templates-and-icons.md](references/split-button-templates-and-icons.md)
- Icon font libraries (Material Design, Bootstrap, Font Awesome)
- Icon positioning and sizing
- Item templates with HTML content
- Image icons and custom graphics
- Content templates for rich styling
- Multiple icon combinations
- Icon alignment and spacing

### Popup Behavior & Target Customization
📄 **Read:** [references/popup-positioning.md](references/split-button-popup-positioning.md)
- Default popup behavior (auto opens below button)
- `popupWidth` property — fixed popup width
- `target` property — custom popup content (color picker, ListView, etc.)
- `createPopupOnClick` — deferred popup creation
- `closeActionEvents` — custom dismiss trigger
- Grouped items with ListView as target
- Edge cases: fixed toolbar, modal dialogs, scrollable containers

### Accessibility & Globalization
📄 **Read:** [references/accessibility-and-globalization.md](references/split-button-accessibility-and-globalization.md)
- WCAG 2.2 and Section 508 compliance
- ARIA roles and attributes (role="button", aria-haspopup, aria-expanded)
- Keyboard navigation (Tab, Enter, Escape, Arrow Keys)
- Screen reader compatibility and announcements
- RTL (Right-to-Left) layout support
- Localization and locale property usage
- Language-specific formatting and translations

### Reactive Forms Integration
📄 **Read:** [references/reactive-forms-integration.md](references/split-button-reactive-forms-integration.md)
- FormControl integration with SplitButton
- FormGroup and form binding
- Validation rules and error states
- Form state changes and subscriptions
- Programmatic control and updates
- Reset and submit patterns
- Disabled state management

### API Reference
📄 **Read:** [references/api-reference.md](references/split-button-api-reference.md)
- All 16 official properties: `content`, `items`, `iconCss`, `iconPosition`, `cssClass`, `disabled`, `enableRtl`, `target`, `popupWidth`, `animationSettings`, `closeActionEvents`, `createPopupOnClick`, `enableHtmlSanitizer`, `enablePersistence`, `locale`
- Official methods: `toggle()`, `addItems()`, `removeItems()`, `focusIn()`, `getPersistData()`, `onPropertyChanged()`
- All 8 official events with correct event arg interfaces
- `ItemModel` interface: `text`, `id`, `iconCss`, `url`, `separator`, `disabled`
- `SplitButtonIconPosition` enum: `"Left"` | `"Top"`
- Event arg interfaces: `BeforeOpenCloseMenuEventArgs`, `OpenCloseMenuEventArgs`, `MenuEventArgs`, `ClickEventArgs`

## Quick Start Example

```typescript
// app.component.ts
import { Component } from '@angular/core';
import { ItemModel } from '@syncfusion/ej2-angular-splitbuttons';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  // Dropdown items
  public dropdownItems: ItemModel[] = [
    { text: 'Cut' },
    { text: 'Copy' },
    { text: 'Paste' }
  ];
  
  // Primary button action handler
  onPrimaryClick(): void {
    console.log('Primary action clicked');
  }
  
  // Item selection handler
  onItemSelect(args: any): void {
    console.log('Selected item:', args.item.text);
  }
}
```

```html
<!-- app.component.html -->
<div style="padding: 20px; font-family: Arial, sans-serif;">
  <h2>Basic SplitButton</h2>
  <ejs-splitbutton 
    content="Paste"
    [items]="dropdownItems"
    (click)="onPrimaryClick()"
    (select)="onItemSelect($event)">
  </ejs-splitbutton>
</div>
```

```css
/* app.component.css */
@import '../node_modules/@syncfusion/ej2-base/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-buttons/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-popups/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-splitbuttons/styles/material3.css';

:host ::ng-deep .e-split-button {
  margin: 10px;
}
```

## Common Patterns

### Pattern 1: Action Menu with Icons

When you need a split button with icon-rich dropdown menu:

```typescript
export class AppComponent {
  public fileActions: ItemModel[] = [
    { text: 'Save', iconCss: 'e-icons e-save' },
    { text: 'Save As', iconCss: 'e-icons e-save-as' },
    { separator: true },
    { text: 'Export', iconCss: 'e-icons e-export' },
    { text: 'Print', iconCss: 'e-icons e-print' }
  ];
  
  onFileAction(args: any): void {
    const action = args.item.text;
    console.log(`File action: ${action}`);
    // Execute based on selected action
  }
}
```

### Pattern 2: Conditional Item Enable/Disable

When you need to enable/disable menu items based on application state:

```typescript
export class AppComponent {
  @ViewChild('splitBtn') splitButtonRef!: SplitButtonComponent;
  
  isEditMode: boolean = false;
  
  public items: ItemModel[] = [
    { text: 'Edit', disabled: true },
    { text: 'Delete', disabled: true },
    { text: 'Duplicate' }
  ];
  
  toggleEditMode(): void {
    this.isEditMode = !this.isEditMode;
    // Update item disabled states
    this.items[0].disabled = !this.isEditMode;
    this.items[1].disabled = !this.isEditMode;
  }
  
  onItemSelect(args: any): void {
    if (!args.item.disabled) {
      console.log('Executing:', args.item.text);
    }
  }
}
```

### Pattern 3: Dynamic Item Management

When you need to add/remove items at runtime:

```typescript
export class AppComponent {
  @ViewChild('splitBtn') splitButtonRef!: SplitButtonComponent;
  
  public items: ItemModel[] = [];
  
  ngOnInit(): void {
    // Load initial items
    this.loadItems();
  }
  
  loadItems(): void {
    this.items = [
      { text: 'Item 1' },
      { text: 'Item 2' },
      { text: 'Item 3' }
    ];
  }
  
  addItem(text: string): void {
    this.items.push({ text: text });
  }
  
  removeItem(index: number): void {
    this.items.splice(index, 1);
  }
  
  clearAllItems(): void {
    this.items = [];
  }
}
```

### Pattern 4: Item Navigation with URLs

When you need menu items to navigate to different URLs. Note: `ItemModel` only supports `url`; the open-target (`_blank`, `_self`) must be handled in `(select)`:

```typescript
export class AppComponent {
  public navigationItems: ItemModel[] = [
    { id: 'home',    text: 'Home',          url: '/' },
    { id: 'docs',    text: 'Documentation', url: '/docs' },
    { separator: true },
    { id: 'github',  text: 'GitHub',        url: 'https://github.com' },
    { id: 'support', text: 'Support',       url: 'https://support.syncfusion.com' }
  ];
  
  onNavigate(args: any): void {
    const itemUrl: string = args.item.url;
    if (!itemUrl) return;
    // Open external URLs in new tab, internal in same tab
    const isExternal = itemUrl.startsWith('http');
    window.open(itemUrl, isExternal ? '_blank' : '_self');
  }
}
```

### Pattern 5: Custom Popup Width and Target

When you need a fixed popup width or a completely custom popup element:

```typescript
import { Component } from '@angular/core';
import { ItemModel, SplitButtonModule } from '@syncfusion/ej2-angular-splitbuttons';

@Component({
  standalone: true,
  imports: [SplitButtonModule],
  selector: 'app-root',
  template: `
    <!-- Fixed-width popup -->
    <ejs-splitbutton
      content="Actions"
      [items]="items"
      popupWidth="250px"
      (beforeOpen)="onBeforeOpen($event)"
      (open)="onOpen()"
      (close)="onClose()">
    </ejs-splitbutton>
  `
})
export class AppComponent {
  public items: ItemModel[] = [
    { text: 'Save',   iconCss: 'e-icons e-save' },
    { text: 'Export', iconCss: 'e-icons e-export' },
    { text: 'Print',  iconCss: 'e-icons e-print' }
  ];

  onBeforeOpen(args: any): void {
    console.log('Popup about to open');
  }

  onOpen(): void {
    console.log('Popup opened');
  }

  onClose(): void {
    console.log('Popup closed');
  }
}
```

## Key Props Reference

| Prop | Type | Description | Example |
|------|------|-------------|---------|
| `content` | `string` | Text for primary button | `content="Save"` |
| `items` | `ItemModel[]` | Dropdown menu items | `[items]="items"` |
| `iconCss` | `string` | Primary button icon CSS class | `iconCss="e-icons e-save"` |
| `iconPosition` | `SplitButtonIconPosition` | Icon position (`"Left"` or `"Top"`) | `iconPosition="Top"` |
| `disabled` | `boolean` | Enable/disable component | `[disabled]="false"` |
| `cssClass` | `string` | Custom CSS classes on component | `cssClass="custom-split-btn"` |
| `enableRtl` | `boolean` | Enable RTL layout | `[enableRtl]="true"` |
| `target` | `string \| Element` | Custom element as popup content | `target="#colorPicker"` |
| `popupWidth` | `string \| number` | Popup width (`"auto"` default) | `popupWidth="250px"` |
| `createPopupOnClick` | `boolean` | Defer popup DOM creation | `[createPopupOnClick]="true"` |
| `closeActionEvents` | `string` | DOM event to dismiss popup | `closeActionEvents="mouseleave"` |
| `animationSettings` | `AnimationModel` | Open/close animation | `[animationSettings]="animation"` |
| `locale` | `string` | Culture/language code | `locale="ar-SA"` |
| `(beforeOpen)` | `EventEmitter` | Before dropdown opens | `(beforeOpen)="onBeforeOpen($event)"` |
| `(click)` | `EventEmitter` | Primary button clicked | `(click)="onPrimaryClick($event)"` |
| `(select)` | `EventEmitter` | Item selected from dropdown | `(select)="onItemSelect($event)"` |
| `(open)` | `EventEmitter` | Dropdown opened | `(open)="onOpen($event)"` |
| `(close)` | `EventEmitter` | Dropdown closed | `(close)="onClose($event)"` |
| `(beforeClose)` | `EventEmitter` | Before dropdown closes | `(beforeClose)="onBeforeClose($event)"` |
| `(beforeItemRender)` | `EventEmitter` | Before each item renders | `(beforeItemRender)="onRender($event)"` |
| `(created)` | `EventEmitter` | Component created | `(created)="onCreated()"` |

> **⚠️ Note:** `position`, `title` and `open()`/`close()` methods do **not** exist in the official API. Use `toggle()` for programmatic open/close. See [`references/api-reference.md`](references/api-reference.md) for the full authoritative API.

## Common Use Cases

**Use Case 1: Document Toolbar**
- Primary action (Save), dropdown with Save As, Export, Print
- Icons for visual clarity
- Disable Save when no changes
- Solution: Combine iconCss with dynamic disable states
- Reference: [Button Items Configuration](references/split-button-items-configuration.md) + [Styling & Customization](references/split-button-styling-and-customization.md)

**Use Case 2: Form Actions Menu**
- Primary button (Submit), dropdown with Save Draft, Schedule, Delete
- Disable options based on form state
- Handle each action differently
- Solution: Use select event with item tracking
- Reference: [Events & Methods](references/split-button-events-and-methods.md) + [Reactive Forms Integration](references/split-button-reactive-forms-integration.md)

**Use Case 3: Navigation Menu**
- Primary action (Dashboard), dropdown with other pages
- External links to documentation or support
- RTL support for international apps
- Solution: Use url property and target attribute
- Reference: [Button Items Configuration](references/split-button-items-configuration.md) + [Accessibility & Globalization](references/split-button-accessibility-and-globalization.md)

**Use Case 4: Settings Panel**
- Accessible split button with keyboard navigation
- Screen reader compatible
- WCAG 2.2 compliant
- Solution: Use proper ARIA attributes and keyboard handlers
- Reference: [Accessibility & Globalization](references/split-button-accessibility-and-globalization.md)

**Use Case 5: Responsive Toolbar**
- Split button with adaptive positioning
- Responsive popup on small screens
- Touch-friendly spacing
- Solution: Use dynamic positioning and responsive CSS
- Reference: [Popup Positioning](references/split-button-popup-positioning.md) + [Styling & Customization](references/split-button-styling-and-customization.md)