---
name: syncfusion-angular-toolbar
description: Creates dynamic, responsive Angular toolbars with Syncfusion. Configure button items, separators, input components, templates, styling, tooltips, links, and responsive scrolling. Supports customization, accessibility, keyboard navigation, RTL mode, and component embedding for building professional toolbar interfaces in Angular applications.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Navigation Components"
---

# Implementing Syncfusion Angular Toolbar

Displays a group of command buttons arranged horizontally with responsive overflow handling and rich customization options.

## When to Use This Skill

Use this skill when you need to:
- Create action buttons in a horizontal toolbar layout
- Add separators between button groups
- Embed input components (NumericTextBox, DropDownList, CheckBox)
- Customize styling with CSS and Font Awesome icons
- Handle click events and command interactions
- Render custom templates and components in toolbar items
- Set tooltips for toolbar commands
- Add routing links as toolbar items
- Create toggle buttons with state management
- Implement responsive scrolling or popup overflow modes
- Build accessible toolbars with keyboard navigation

## Toolbar Overview

The Syncfusion Angular Toolbar is a container component that displays a collection of command buttons arranged horizontally. It supports multiple item types (buttons, separators, inputs), custom templates, styling, responsive behavior, and accessibility features.

**Key Features:**
- **Button Items:** Default item type with text, icons, and styling
- **Separators:** Vertical divisions between command groups
- **Input Components:** Embed NumericTextBox, DropDownList, CheckBox, RadioButton
- **Template Support:** Render Angular components and custom HTML
- **Responsive Modes:** Scrollable (default) and Popup overflow handling
- **Custom Styling:** CSS customization, Font Awesome integration, themes
- **Tooltips:** Hint text on mouse hover for all commands
- **Links:** Embed routing links and anchor elements
- **Toggle Buttons:** Stateful buttons with play/pause, show/hide functionality
- **Keyboard Navigation:** Tab key support, arrow key navigation
- **RTL Support:** Right-to-left text and layout direction
- **Accessibility:** WCAG compliance with ARIA attributes

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Install @syncfusion/ej2-angular-navigations package
- Setup Angular environment and dependencies
- Import ToolbarModule in component
- Add CSS imports for themes
- Create basic toolbar with button items
- Run and test the application

### Item Configuration
📄 **Read:** [references/item-configuration.md](references/item-configuration.md)
- Configure button item properties (text, id, prefixIcon, suffixIcon, width, align)
- Add separator items to group commands
- Setup Input type items (NumericTextBox, DropDownList, CheckBox, RadioButton)
- Enable tab key navigation with tabIndex property
- Dynamic item management and updates

### Styling & Customization
📄 **Read:** [references/styling-customization.md](references/styling-customization.md)
- Customize toolbar container styling with CSS
- Style toolbar items and buttons
- Customize icons and icon colors
- Apply hover and focus state styles
- Integrate Font Awesome third-party icons
- CSS class customization (e-toolbar, e-toolbar-item, e-tbar-btn)
- Icon positioning with e-icons class

### Command Events & Customization
📄 **Read:** [references/command-events.md](references/command-events.md)
- Implement click event handlers for toolbar items
- Use htmlAttributes property for custom HTML attributes
- Apply multiple CSS classes with cssClass property
- Command customization with id, class, style, role attributes
- Event-driven patterns for toolbar interactions
- Handle item-specific actions and responses

### Item Templates & Components
📄 **Read:** [references/item-templates.md](references/item-templates.md)
- Use template property for custom item rendering
- Render Angular components with ng-template directive
- Checkbox and input templates as string literals
- Template references with query selectors
- Menu component integration in toolbar
- Render multiple components (NumericTextBox, DatePicker, Button)
- Custom HTML template structures

### Tooltips & Links
📄 **Read:** [references/tooltips-links.md](references/tooltips-links.md)
- Set tooltipText property for hint text on hover
- Import and initialize Tooltip module with target selector
- Add anchor elements with ng-template
- Create routing links in toolbar items
- Toggle button implementation with state changes
- Play/pause, show/hide, and filter toggle patterns
- Accessibility for links and button states

### Responsive & Scrolling
📄 **Read:** [references/responsive-scrolling.md](references/responsive-scrolling.md)
- Scrollable overflow mode (default) with navigation arrows
- Touch swipe gestures for scrolling on devices
- Popup overflow mode for mobile-optimized display
- Customize scrollStep property for scroll distance
- Handle overflow when items exceed container width
- Navigation icon disabled states and behavior
- Continuous scrolling with long press navigation

### Advanced Features
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- Grouping related toolbar buttons together
- Nested items and hierarchical structures
- Keyboard navigation with arrow keys and Tab support
- WCAG accessibility compliance and ARIA attributes
- RTL (right-to-left) language support
- Performance optimization for large toolbars
- Built-in compliance with WAI-ARIA specifications

### Complete API Reference
📄 **Read:** [references/api-reference.md](references/api-reference.md)
- **Toolbar Component Properties** (12 properties)
  - allowKeyboard, cssClass, enableCollision, enableHtmlSanitizer, enablePersistence
  - enableRtl, height, items, locale, overflowMode, scrollStep, width
- **Toolbar Events** (5 events)
  - beforeCreate (BeforeCreateArgs), clicked (ClickEventArgs), created, keyDown (KeyDownEventArgs), destroyed
- **Toolbar Methods** (7 methods)
  - addItems, destroy, disable, enableItems, hideItem, refreshOverflow, removeItems
- **Item Configuration Properties** (19+ properties)
  - align, cssClass, disabled, htmlAttributes, id, overflow, prefixIcon, suffixIcon
  - showAlwaysInPopup, showTextOn, tabIndex, template, text, tooltipText, type, visible, width
- **Types & Enums** (5 enums)
  - ItemType, ItemAlign, OverflowMode, OverflowOption, DisplayMode
- **Complete API Examples**
  - Advanced toolbar with all features
  - Responsive toolbar with dynamic configuration

## Quick Start Example

```typescript
import { ToolbarModule } from '@syncfusion/ej2-angular-navigations';
import { Component } from '@angular/core';

@Component({
  imports: [ToolbarModule],
  standalone: true,
  selector: 'app-root',
  template: `
    <ejs-toolbar>
      <e-items>
        <e-item text='Cut'></e-item>
        <e-item text='Copy'></e-item>
        <e-item type='Separator'></e-item>
        <e-item text='Paste'></e-item>
        <e-item type='Separator'></e-item>
        <e-item text='Bold'></e-item>
        <e-item text='Italic'></e-item>
        <e-item text='Underline'></e-item>
      </e-items>
    </ejs-toolbar>
  `
})
export class AppComponent { }
```

**Add CSS imports in styles.css:**

```css
@import '../node_modules/@syncfusion/ej2-base/styles/material3.css';  
@import '../node_modules/@syncfusion/ej2-buttons/styles/material3.css';  
@import '../node_modules/@syncfusion/ej2-popups/styles/material3.css';  
@import '../node_modules/@syncfusion/ej2-navigations/styles/material3.css';
```

## Common Patterns

### Pattern 1: Simple Text Buttons

```typescript
<e-item text='Cut'></e-item>
<e-item text='Copy'></e-item>
<e-item text='Paste'></e-item>
```

**Use when:** You need basic action buttons with text labels.

---

### Pattern 2: Icon Buttons with Text

```typescript
<e-item text='Bold' prefixIcon='e-icons e-bold'></e-item>
<e-item text='Italic' prefixIcon='e-icons e-italic'></e-item>
<e-item text='Undo' suffixIcon='e-icons e-undo'></e-item>
```

**Use when:** You want visual icons before or after text labels.

---

### Pattern 3: Grouped Commands with Separators

```typescript
<e-item text='Cut'></e-item>
<e-item text='Copy'></e-item>
<e-item type='Separator'></e-item>
<e-item text='Paste'></e-item>
<e-item type='Separator'></e-item>
<e-item text='Bold'></e-item>
<e-item text='Italic'></e-item>
```

**Use when:** You need to visually group related commands.

---

### Pattern 4: Toolbar with Input Components

```typescript
<e-item type='Input'>
  <ng-template #template>
    <ejs-numerictextbox value="10" width="150"></ejs-numerictextbox>
  </ng-template>
</e-item>
<e-item type='Input'>
  <ng-template #template>
    <ejs-dropdownlist [dataSource]='data' width="120"></ejs-dropdownlist>
  </ng-template>
</e-item>
```

**Use when:** You need input fields, dropdowns, or other controls within the toolbar.

---

### Pattern 5: Custom Templates with Checkboxes

```typescript
<e-item>
  <ng-template #template>
    <input type='checkbox' id='check1' checked=''>
    <label for='check1'>Enable Feature</label>
  </ng-template>
</e-item>
```

**Use when:** You need custom HTML elements like checkboxes or custom controls.

---

### Pattern 6: Links in Toolbar

```typescript
<e-item>
  <ng-template #template>
    <a href="url" target="_blank">Documentation</a>
  </ng-template>
</e-item>
```

**Use when:** You need to add clickable links as toolbar items.

---

### Pattern 7: Tooltips with Hover Help

```typescript
<ejs-tooltip target='#Toolbar [title]'>
  <ejs-toolbar id='Toolbar'>
    <e-items>
      <e-item text='Cut' tooltipText='Cut selected content'></e-item>
      <e-item text='Paste' tooltipText='Paste copied content'></e-item>
    </e-items>
  </ejs-toolbar>
</ejs-tooltip>
```

**Use when:** You want to show hint text on mouse hover.

---

### Pattern 8: Responsive Scrollable Toolbar

```typescript
<ejs-toolbar width="300px">
  <e-items>
    <e-item text='Cut'></e-item>
    <e-item text='Copy'></e-item>
    <!-- Multiple items trigger horizontal scroll -->
  </e-items>
</ejs-toolbar>
```

**Use when:** Container is narrower than total content width, triggering scrollable mode.

---

### Pattern 9: Toggle Buttons with State

```typescript
<ng-template #template>
  <button ejs-button class="e-btn" iconCss="e-play-icon" 
    isToggle="true" (click)="onPlayClick()"></button>
</ng-template>
```

**Use when:** You need buttons that toggle states (play/pause, show/hide).

---

### Pattern 10: Font Awesome Icons

```typescript
<link rel="stylesheet" href="url" />

<e-item prefixIcon="fa fa-twitter"></e-item>
<e-item prefixIcon="fa fa-facebook"></e-item>
```

**Use when:** You need third-party icons like Font Awesome.

---

## Key Properties

| Property | Type | Purpose | Example |
|----------|------|---------|---------|
| `text` | string | Button display text | `text='Cut'` |
| `type` | string | Item type (Button, Separator, Input) | `type='Separator'` |
| `prefixIcon` | string | CSS class for icon before text | `prefixIcon='e-icons e-cut'` |
| `suffixIcon` | string | CSS class for icon after text | `suffixIcon='e-icons e-undo'` |
| `id` | string | Unique item identifier | `id='item1'` |
| `width` | string | Button width | `width='100px'` |
| `align` | string | Item alignment (Left, Center, Right) | `align='Right'` |
| `tooltipText` | string | Hover tooltip hint text | `tooltipText='Cut'` |
| `cssClass` | string | CSS classes to apply | `cssClass='custom-btn'` |
| `htmlAttributes` | object | Custom HTML attributes | `[htmlAttributes]='{class: "custom"}'` |
| `template` | string\|object | Custom template content | `[template]='templateVar'` |
| `tabIndex` | number | Tab key navigation order | `tabIndex=1` |
| `scrollStep` | number | Scroll distance in pixels | `scrollStep='50'` |

## Common Use Cases

1. **Text Editor Toolbar** - Bold, Italic, Underline buttons with separators
2. **File Operations** - Cut, Copy, Paste, Undo, Redo buttons
3. **Search Bar in Toolbar** - Input field for search within container width
4. **Formatting Options** - Font size, color picker, alignment buttons
5. **Navigation Toolbar** - Links to different sections or pages
6. **Mobile App Header** - Icons with tooltips in compact, scrollable layout
7. **Document Viewer** - Zoom in/out, print, download toggles
8. **Rich Text Editor** - Full formatting toolbar with templates and inputs
9. **Dashboard Controls** - Date picker, filters, sorting options
10. **Social Media Sharing** - Font Awesome social icons in toolbar

