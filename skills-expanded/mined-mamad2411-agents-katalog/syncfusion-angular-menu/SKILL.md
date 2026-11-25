---
name: syncfusion-angular-menu
description: Guide for implementing Syncfusion Angular Menu component. Use this skill when the user needs to create navigation menus, hierarchical menu structures, submenu items, menu events, animation, orientation changes, RTL support, or customize menu appearance. Covers installation, data binding, templates, events, styling, accessibility, and real-world implementations like sidebar menus and toolbars.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Navigation Component"
---

# Implementing Syncfusion Angular Menu Component

The Menu component is a graphical user interface that serves as a navigation header for your application or site. It supports multi-level nested menu items, rich customization, data binding, templates, animations, comprehensive event handling, internationalization, state persistence, and mobile-friendly hamburger mode.

## When to Use This Skill

Use this skill when you need to:
- **Create navigation menus** with hierarchical structures
- **Bind data** from arrays or remote sources
- **Customize menu items** dynamically (add, remove, enable, disable)
- **Handle menu events** (click, open, close, select)
- **Apply animations** and control orientation
- **Add icons, images, and navigation URLs** to menu items
- **Implement accessibility** features
- **Style and theme** the menu
- **Build real-world patterns** (sidebar menus, toolbar menus, context menus)

## Component Overview

**Key Features:**
- ✅ Hierarchical and self-referential data binding
- ✅ HTML templates and custom item rendering
- ✅ Multi-level submenu support with nesting
- ✅ Multiple animation effects (FadeIn, SlideDown, ZoomIn)
- ✅ Horizontal and vertical orientation
- ✅ Icon and image support
- ✅ Enable/disable, show/hide menu items dynamically
- ✅ Event-driven customization
- ✅ RTL (Right-to-Left) support
- ✅ Accessibility features (keyboard navigation, ARIA)
- ✅ CSS customization and theming

## Documentation and Navigation Guide

### 📖 Core Documentation (Start Here)

#### 1️⃣ Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md) **(Start here for new users)**
- ✅ Installation and package setup
- ✅ Basic menu implementation
- ✅ CSS imports and theme configuration
- ✅ Essential properties (enablePersistence, enableRtl, cssClass, hoverDelay, enableScrolling, locale)
- ✅ Standalone architecture setup
- ✅ First application example

#### 2️⃣ Data Source Binding and Templates
📄 **Read:** [references/data-source-binding.md](references/data-source-binding.md)
- ✅ Hierarchical data binding with field mappings
- ✅ Self-referential data structures
- ✅ Remote data binding with DataManager
- ✅ HTML templates and custom item rendering
- ✅ Dynamic data population
- ✅ FieldSettingsModel configuration

#### 3️⃣ Menu Items Customization & Dynamic Management
📄 **Read:** [references/menu-items.md](references/menu-items.md) **(Now includes methods!)**
- ✅ Menu item properties (text, id, iconCss, url, separator)
- ✅ Icons and images in menu items
- ✅ Navigation URLs
- ✅ Custom attributes (htmlAttributes)
- ✅ **NEW:** Dynamic Methods Reference:
  - `insertBefore()` - Add items before a target
  - `insertAfter()` - Add items after a target
  - `removeItems()` - Delete menu items
  - `enableItems()` - Enable/disable items
  - `showItems()` - Display hidden items
  - `hideItems()` - Hide menu items
- ✅ Enable/disable menu items
- ✅ Show/hide menu items
- ✅ Add, remove, insert menu items dynamically
- ✅ Separators for grouping items
- ✅ Complete dynamic menu management example

#### 4️⃣ Animation and Orientation
📄 **Read:** [references/animation-and-orientation.md](references/animation-and-orientation.md)
- ✅ Animation settings (effect, duration, easing)
- ✅ Animation effects (FadeIn, SlideDown, ZoomIn, None)
- ✅ Horizontal and vertical orientation
- ✅ Sub-menu positioning and behavior
- ✅ Menu open-on-click vs hover behavior

#### 5️⃣ Events and Interactions
📄 **Read:** [references/events-and-interactions.md](references/events-and-interactions.md) **(Enhanced with event arguments)**
- ✅ Event overview (7 events documented)
- ✅ **NEW:** Complete Event Arguments Documentation:
  - `BeforeOpenCloseMenuEventArgs` - beforeOpen/beforeClose events
  - `OpenCloseMenuEventArgs` - onOpen/onClose events
  - `MenuEventArgs` - select/beforeItemRender events
- ✅ beforeOpen and beforeClose events (cancelable)
- ✅ onOpen and onClose events
- ✅ Select event handling
- ✅ beforeItemRender event (for tooltips and custom rendering)
- ✅ Created event for initialization
- ✅ Dynamic menu modification through events

### 🎯 Advanced Features & Patterns

#### 6️⃣ Complete API Reference
📄 **Read:** [references/api-reference.md](references/api-reference.md) **(Comprehensive API documentation!)**
- ✅ All MenuModel properties with examples (16 properties)
- ✅ All MenuItem properties with examples (7 properties)
- ✅ Animation settings configuration
- ✅ Field settings for data binding
- ✅ **All Menu Methods** with signatures and examples:
  - insertBefore(), insertAfter(), removeItems()
  - enableItems(), showItems(), hideItems()
- ✅ **All Menu Events** with arguments
- ✅ Event arguments interfaces
- ✅ Enumerations (Orientation, MenuEffect, MenuOpenType)
- ✅ Quick reference summary

#### 7️⃣ Hamburger Mode and Responsive Design
📄 **Read:** [references/hamburger-and-responsive.md](references/hamburger-and-responsive.md) **(Mobile-first design)**
- ✅ Hamburger mode overview
- ✅ hamburgerMode property configuration
- ✅ target and title properties
- ✅ Basic hamburger implementation
- ✅ Responsive toggle (Desktop/Mobile)
- ✅ Hamburger with animations
- ✅ Complete mobile menu solution
- ✅ State persistence with hamburger
- ✅ Accessibility best practices
- ✅ Touch-friendly interactions

#### 8️⃣ Internationalization and State Management
📄 **Read:** [references/internationalization-and-persistence.md](references/internationalization-and-persistence.md) **(i18n + Storage)**
- ✅ Localization (i18n) with 15+ locales
- ✅ RTL language support (Arabic, Hebrew, Persian)
- ✅ State persistence (enablePersistence)
- ✅ HTML sanitization (enableHtmlSanitizer)
- ✅ Hover delay control (hoverDelay)
- ✅ Custom CSS classes (cssClass)
- ✅ Advanced configuration patterns
- ✅ Complete setup example

#### 9️⃣ Styling and Appearance
📄 **Read:** [references/styling-and-appearance.md](references/styling-and-appearance.md)
- ✅ CSS styling and custom classes
- ✅ Rounded corner styling
- ✅ Title and icon positioning
- ✅ Theme customization
- ✅ Material3 and other theme integration
- ✅ CSS variable customization

#### 🔟 Advanced Features and Scrolling
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- ✅ Right-to-Left (RTL) language support
- ✅ Horizontal and vertical scrolling
- ✅ Large menu handling
- ✅ Menu item grouping with separators
- ✅ Accessibility features (keyboard navigation, ARIA)
- ✅ Nested submenu patterns

#### 1️⃣1️⃣ Use Cases and Real-World Patterns
📄 **Read:** [references/use-cases-and-scenarios.md](references/use-cases-and-scenarios.md)
- ✅ Sidebar menu implementations
- ✅ Toolbar menu patterns
- ✅ Context menu scenarios
- ✅ ListView and other component integrations
- ✅ Multi-level menu structures
- ✅ Mobile navigation
- ✅ Admin dashboard patterns
- ✅ Best practices and common patterns

### 🔍 Quick Access by Task

**I need to...**
- ▶️ **Install and get started** → [getting-started.md](references/getting-started.md)
- ▶️ **Add dynamic menu items** → [menu-items.md](references/menu-items.md)
- ▶️ **Bind data from array/API** → [data-source-binding.md](references/data-source-binding.md)
- ▶️ **Handle menu clicks and events** → [events-and-interactions.md](references/events-and-interactions.md)
- ▶️ **Add animations** → [animation-and-orientation.md](references/animation-and-orientation.md)
- ▶️ **Make mobile-friendly menu** → [hamburger-and-responsive.md](references/hamburger-and-responsive.md)
- ▶️ **Support multiple languages** → [internationalization-and-persistence.md](references/internationalization-and-persistence.md)
- ▶️ **Find all properties/methods/events** → [api-reference.md](references/api-reference.md)
- ▶️ **Style and customize appearance** → [styling-and-appearance.md](references/styling-and-appearance.md)
- ▶️ **Build production pattern** → [use-cases-and-scenarios.md](references/use-cases-and-scenarios.md)

## Quick Start Example

```typescript
import { Component } from '@angular/core';
import { MenuModule } from '@syncfusion/ej2-angular-navigations';
import { MenuItemModel } from '@syncfusion/ej2-angular-navigations';
import { enableRipple } from '@syncfusion/ej2-base';

enableRipple(true);

@Component({
  imports: [MenuModule],
  standalone: true,
  selector: 'app-root',
  template: `<ejs-menu [items]="menuItems"></ejs-menu>`
})
export class AppComponent {
  public menuItems: MenuItemModel[] = [
    {
      text: 'File',
      items: [
        { text: 'Open' },
        { text: 'Save' },
        { separator: true },
        { text: 'Exit' }
      ]
    },
    {
      text: 'Edit',
      items: [
        { text: 'Cut' },
        { text: 'Copy' },
        { text: 'Paste' }
      ]
    },
    { text: 'Help' }
  ];
}
```

**CSS Setup:**
```css
@import '../node_modules/@syncfusion/ej2-base/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-navigations/styles/material3.css';
```

## Common Patterns

### 1. Menu with Icons
```typescript
public menuItems: MenuItemModel[] = [
  {
    text: 'File',
    iconCss: 'e-icons e-file',
    items: [
      { text: 'Open', iconCss: 'e-icons e-open' },
      { text: 'Save', iconCss: 'e-icons e-save' }
    ]
  }
];
```

### 2. Menu with Animation
```typescript
public animationSettings: MenuAnimationSettingsModel = {
  effect: 'FadeIn',
  duration: 800
};
```
Use in template: `<ejs-menu [animationSettings]="animationSettings"></ejs-menu>`

### 3. Menu with Events
```typescript
public onItemSelect(args: MenuEventArgs): void {
  console.log('Selected item:', args.item.text);
}
```
Use in template: `<ejs-menu (select)="onItemSelect($event)"></ejs-menu>`

### 4. Dynamic Menu Modification
```typescript
@ViewChild('menu')
public menuObj?: MenuComponent;

public addItem(): void {
  const newItem: MenuItemModel[] = [
    { text: 'New Menu Item' }
  ];
  this.menuObj?.insertAfter(newItem, 'File', false);
}
```

## Complete API Reference

The Menu component includes **16 component properties**, **7 menu item properties**, **7 events**, **3 animation properties**, **6 field settings properties**, and **10+ methods**.

**See [references/api-reference.md](references/api-reference.md) for complete documentation of:**
- ✅ All MenuModel properties with examples
- ✅ All MenuItem properties with examples
- ✅ All methods (insertBefore, insertAfter, removeItems, enableItems, showItems, hideItems)
- ✅ All events with event arguments
- ✅ Enumerations and quick reference

## Key Properties

### Essential Properties (Most Used)

| Property | Type | Purpose | Default |
|----------|------|---------|---------|
| `items` | `MenuItemModel[]` | Array of menu items to render | `[]` |
| `fields` | `FieldSettingsModel` | Maps data source fields to menu structure | - |
| `template` | `string` | Custom template for menu items | - |
| `animationSettings` | `MenuAnimationSettingsModel` | Controls menu animation behavior | - |
| `orientation` | `Orientation` | 'Horizontal' or 'Vertical' | `'Horizontal'` |
| `showItemOnClick` | `boolean` | Open submenu on click (true) or hover (false) | `false` |
| `cssClass` | `string` | Custom CSS class for styling | - |
| `enableRtl` | `boolean` | Enable right-to-left layout | `false` |

### Advanced Properties (For Special Cases)

| Property | Type | Purpose | Default |
|----------|------|---------|---------|
| `hamburgerMode` | `boolean` | Enable mobile hamburger menu | `false` |
| `target` | `string` | Hamburger toggle button selector | - |
| `title` | `string` | Title for hamburger drawer | - |
| `enablePersistence` | `boolean` | Save menu state to localStorage | `false` |
| `enableScrolling` | `boolean` | Enable scrollbar for large menus | `false` |
| `enableHtmlSanitizer` | `boolean` | Sanitize HTML content (security) | `true` |
| `hoverDelay` | `number` | Delay before submenu opens (ms) | `0` |
| `locale` | `string` | Localization culture code | `'en-US'` |

## Common Use Cases

1. **Application Menu Bar** - File, Edit, View, Tools menus with submenus
2. **Navigation Sidebar** - Vertical menu for page navigation
3. **Toolbar Menu** - Horizontal menu with icons and commands
4. **Context Menu** - Right-click menu with dynamic items
5. **Mobile Navigation** - Collapsible menu for responsive design
6. **Admin Dashboard** - Multi-level navigation for admin panels

---

## Feature Summary

✅ **Data Binding**
- Hierarchical menus (parent-child structure)
- Self-referential data (id/parentId relationships)
- Remote data binding via DataManager/HTTP
- Custom templates for items

✅ **Customization**
- Dynamic add/remove/insert menu items
- Enable/disable items (grayed out)
- Show/hide items programmatically
- Custom HTML attributes and content
- Icon and image support
- Navigation URLs

✅ **Interactivity**
- 7 events (beforeOpen, beforeClose, onOpen, onClose, select, beforeItemRender, created)
- Cancelable events for control flow
- Keyboard shortcuts support
- Mnemonic UI

✅ **Styling & Theming**
- 6+ built-in themes (Material3, Bootstrap5, Fluent2, etc.)
- Custom CSS classes
- Rounded corners support
- Icon/title customization
- Dark mode support

✅ **Responsive & Mobile**
- Hamburger mode for mobile
- RTL language support (15+ locales)
- Horizontal and vertical layouts
- Touch-friendly interactions
- Hamburger animations

✅ **Performance & State**
- State persistence to localStorage
- Hover delay control
- HTML sanitization for security
- Efficient rendering of large menus

**Next Steps:** 
1. Start with [getting-started.md](references/getting-started.md) for installation
2. Choose a reference based on your task (see "Quick Access by Task" above)
3. Refer to [api-reference.md](references/api-reference.md) for complete API details
