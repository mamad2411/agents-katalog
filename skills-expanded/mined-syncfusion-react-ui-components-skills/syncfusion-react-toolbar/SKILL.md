---
name: syncfusion-react-toolbar
description: "Implement the Syncfusion React Toolbar component to create responsive command bars and action toolbars. This skill covers organizing buttons, separators, and input components with various overflow handling modes. Use this when building rich text editors, document editors, or command-driven interfaces in React applications."
metadata:
  author: "Syncfusion Inc"
  version: "34.1.29"
  category: "Navigation"
---

# Implementing Syncfusion React Toolbar

## Component Overview

The Syncfusion React Toolbar component provides a flexible command bar for organizing and executing commands. It supports multiple item types (buttons, separators, inputs), responsive overflow modes, and comprehensive accessibility features.

**Key Capabilities:**
- Multiple item types: Button, Separator, Input
- Responsive overflow modes: Scrollable, Popup, MultiRow, Extended
- Built-in keyboard navigation and ARIA support
- Component rendering within toolbar items
- Customizable appearance and behavior
- Tab key navigation support
- Dynamic item management (add/remove/enable/disable)
- Rich event system (beforeCreate, clicked, keyDown, created, destroyed)
- Full RTL and locale support
- Stateless template rendering

---

## Complete Table of Contents

### 1. Getting Started
**File:** [references/getting-started.md](references/getting-started.md)
- Dependencies setup
- Project initialization (Vite/CRA)
- Package installation
- CSS theme imports (Tailwind, Bootstrap, Fluent, Material)
- Basic implementation examples
- Global configuration:
  - Locale support for internationalization
  - RTL (Right-to-Left) layout
  - Persistence settings
  - Collision detection
  - HTML sanitizer
- Development server setup

### 2. Item Configuration
**File:** [references/item-configuration.md](references/item-configuration.md)
- **ItemModel API Reference:**
  - Complete interface structure
  - All 16 properties with types
  - Property reference with descriptions
  - Items array configuration patterns
  - Configuration examples (simple, grouped, conditional, accessible)
- Button item type with properties:
  - `text` - Display text
  - `id` - Unique identifier
  - `prefixIcon` / `suffixIcon` - Icons positioning
  - `width` - Custom width
  - `align` - Alignment (Left/Center/Right)
  - `disabled` - Disabled state
  - `visible` - Visibility control
  - `cssClass` - Custom CSS classes
  - `htmlAttributes` - HTML attributes
  - `overflow` - Priority display (Show/Hide/None)
  - `showAlwaysInPopup` - Force popup display
  - `showTextOn` - Text display mode (Both/Overflow/Toolbar)
- Separator item type
- Input item type for components
- Tab navigation with `tabIndex`
- Complete working examples

### 3. Responsive Modes
**File:** [references/responsive-modes.md](references/responsive-modes.md)
- **Scrollable Mode** (default)
  - Horizontal scrolling with navigation arrows
  - Touch swipe support
  - Keyboard arrow navigation
  - Use cases: many items, large screens
- **Popup Mode**
  - Dropdown overflow container
  - Command priority control
  - Compact appearance
  - Use cases: limited space, mobile
- **MultiRow Mode**
  - Item wrapping to multiple rows
  - No scrolling needed
  - All items visible
  - Use cases: responsive width containers
- **Extended Mode**
  - Multi-row with horizontal scrolling
  - Row-level navigation
  - Use cases: many items in limited width
- Command priority (Show/Hide/None)
- Text display options (Both/Overflow/Toolbar)
- Mode comparison table
- Practical examples for each mode

### 4. Accessibility & Keyboard Support
**File:** [references/accessibility.md](references/accessibility.md)
- Compliance standards:
  - WCAG 2.2 Level AA
  - Section 508 compliance
  - Screen reader support (NVDA, JAWS, VoiceOver)
- ARIA attributes:
  - `role="toolbar"`
  - `aria-label`, `aria-orientation`
  - `aria-expanded`, `aria-haspopup`
- Keyboard navigation:
  - **allowKeyboard** property control
  - Arrow keys (Left/Right) navigation
  - Home/End keys
  - Tab/Shift+Tab for focus
  - Enter/Space for activation
  - Escape to close popups
- **keyDown Event** handling:
  - Event parameters (currentItem, nextItem, originalEvent)
  - Custom keyboard shortcuts
  - Preventing default navigation
  - Key-specific actions
- Screen reader support and testing
- Color contrast WCAG compliance
- Mobile/touch accessibility
- RTL support
- ARIA best practices
- Testing checklist and tools

### 5. Item Configuration (Continued)
**File:** [references/item-configuration.md](references/item-configuration.md)
- Button properties reference
- Separator styling
- Input components (NumericTextBox, DropDownList, CheckBox, RadioButton)
- Tab navigation control
- Complete toolbar examples

### 6. Styling & Customization
**File:** [references/styling-customization.md](references/styling-customization.md)
- CSS class structure:
  - `.e-toolbar` - Container
  - `.e-toolbar-item` - Item wrapper
  - `.e-tbar-btn` - Button
  - `.e-icons` - Icon element
  - `.e-separator` - Separator
  - `.e-toolbar-pop` - Popup
- Toolbar container styling
- Item & button styling
- Icon styling and customization
- State styling (hover, focus, active, disabled)
- Theme integration (Tailwind, Bootstrap, Fluent, Material)
- **Popup customization CSS classes:**
  - `.e-toolbar-pop` - Popup container
  - `.e-overflow-button` - Dropdown toggle
  - `.e-overflow-show` - Show priority items
  - `.e-overflow-hide` - Hide priority items
  - `.e-popup-text` - Popup text styling
  - `.e-toolbar-text` - Toolbar text styling
- Custom styling examples
- Performance optimization
- Complete styled examples

### 7. Advanced Features & Templates
**File:** [references/advanced-features.md](references/advanced-features.md)
- **Template Configuration:**
  - Template basics (functions/JSX)
  - Template properties
  - When to use templates
- **Item-Wise Custom Templates:**
  - Single item templates
  - Multiple different templates
  - State within templates
  - Template styling
- **Stateless Templates:**
  - Performance optimization
  - CSS class customization
  - Popup customization equivalents
- **Toggle Buttons:**
  - Single toggle state
  - Toggle groups (radio-like)
  - CSS styling
- **Link Items:**
  - Navigation links
  - External links
  - Breadcrumb patterns
- **Tooltips:**
  - HTML title attribute
  - Custom tooltip components
  - Styling and positioning
- **Rendering Other Components:**
  - Syncfusion components (DropDownList, NumericTextBox, ColorPicker)
  - React components
  - Custom components
- **Command Customization:**
  - Click handlers
  - Context menus
  - Custom actions
- **Dynamic Item Management:**
  - `addItems()` - Add items at runtime
  - `removeItems()` - Remove by index or ID
  - `enableItems()` - Enable/disable items
  - `hideItem()` - Show/hide items
  - `disable()` - Disable entire toolbar
  - `destroy()` - Cleanup
  - `refreshOverflow()` - Recalculate layout
- **Event Handling:**
  - `beforeCreate` - Pre-initialization customization
  - `created` - Post-initialization callback
  - `clicked` - Item click events with ClickEventArgs
  - `keyDown` - Keyboard events with KeyDownEventArgs
  - `destroyed` - Cleanup event
- **Scroll Step Customization:**
  - Control scroll distance
  - Dynamic scroll step
  - Touch swipe behavior
- Complete advanced example

---

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Package installation and dependencies
- Setup with Vite and React
- CSS imports and theme configuration
- Basic toolbar with ItemsDirective
- HTML element initialization
- Running the development server

### Item Configuration & Types
📄 **Read:** [references/item-configuration.md](references/item-configuration.md)
- Button item type with properties (text, icons, width, align)
- Separator item type
- Input item type for components
- Tab key navigation with tabIndex
- Complete working examples

### Responsive Modes
📄 **Read:** [references/responsive-modes.md](references/responsive-modes.md)
- Scrollable mode (default behavior)
- Popup overflow mode
- Command priority (show, hide, none)
- Text display options
- Navigation and interaction patterns

### Accessibility & Keyboard Support
📄 **Read:** [references/accessibility.md](references/accessibility.md)
- WCAG 2.2 and Section 508 compliance
- ARIA attributes and roles
- Keyboard navigation keys
- Screen reader support
- Mobile device accessibility

### Styling & Customization
📄 **Read:** [references/styling-customization.md](references/styling-customization.md)
- CSS customization patterns
- Toolbar and item styling
- Icon and button customization
- Hover and focus states
- Theme integration

### Advanced Features & Templates
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- Template configuration and patterns
- Item-wise custom templates
- Toggle buttons
- Link items
- Tooltips
- Rendering other Syncfusion components
- Command and scroll customization

---

## Quick Start Example

```jsx
import { ItemDirective, ItemsDirective, ToolbarComponent } from '@syncfusion/ej2-react-navigations';
import './App.css';

const App = () => {
  return (
    <ToolbarComponent id='toolbar'>
      <ItemsDirective>
        <ItemDirective text="Cut" prefixIcon="e-cut-icon" />
        <ItemDirective text="Copy" prefixIcon="e-copy-icon" />
        <ItemDirective text="Paste" prefixIcon="e-paste-icon" />
        <ItemDirective type="Separator" />
        <ItemDirective text="Bold" prefixIcon="e-bold-icon" />
        <ItemDirective text="Italic" prefixIcon="e-italic-icon" />
        <ItemDirective text="Underline" prefixIcon="e-underline-icon" />
      </ItemsDirective>
    </ToolbarComponent>
  );
};

export default App;
```

**Required CSS imports in App.css:**
```css
@import '../node_modules/@syncfusion/ej2-base/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-buttons/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-popups/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-react-navigations/styles/tailwind3.css';
```

---

## Common Patterns

### Basic Toolbar with Buttons and Separators
Create a simple toolbar with button commands and visual separators between groups:

```jsx
<ToolbarComponent>
  <ItemsDirective>
    {/* Edit commands */}
    <ItemDirective text="Cut" />
    <ItemDirective text="Copy" />
    <ItemDirective type="Separator" />
    {/* Format commands */}
    <ItemDirective text="Bold" />
    <ItemDirective text="Italic" />
  </ItemsDirective>
</ToolbarComponent>
```

### Toolbar with Icons
Use prefixIcon to add icons to buttons for better visual representation:

```jsx
<ItemDirective text="Save" prefixIcon="e-save-icon" />
<ItemDirective text="Print" prefixIcon="e-print-icon" />
```

### Responsive Overflow Handling
Choose between Scrollable (default) for continuous display or Popup for compact overflow:

```jsx
{/* Scrollable mode with navigation arrows */}
<ToolbarComponent overflowMode="Scrollable">
  {/* items */}
</ToolbarComponent>

{/* Popup mode with dropdown */}
<ToolbarComponent overflowMode="Popup">
  {/* items */}
</ToolbarComponent>
```

### Toolbar with Input Components
Include interactive components like dropdowns within toolbar items:

```jsx
<ItemDirective type="Input" template={<DropDownComponent {...props} />} />
```

---

## Key Props

| Property | Type | Description |
|----------|------|-------------|
| `id` | string | Unique identifier for the toolbar |
| `overflowMode` | "Scrollable" \| "Popup" | How to handle overflow items |
| `width` | string | Width of the toolbar container |
| `items` | ItemModel[] | Array of toolbar items |
| `text` | string | Display text for button items |
| `prefixIcon` | string | Icon class for prefix position |
| `suffixIcon` | string | Icon class for suffix position |
| `type` | "Button" \| "Separator" \| "Input" | Item type |
| `align` | "Left" \| "Center" \| "Right" | Item alignment |
| `overflow` | "Show" \| "Hide" \| "None" | Priority for popup mode |
| `tabIndex` | number | Tab navigation order |
| `template` | function | Custom template for items |

---

## Common Use Cases

1. **Text Editor Toolbar**
   - Format buttons (Bold, Italic, Underline)
   - Alignment options
   - Color and font pickers
   - See: responsive-modes.md, advanced-features.md

2. **File Operations Toolbar**
   - New, Open, Save, Save As buttons
   - Print functionality
   - Undo/Redo commands
   - See: item-configuration.md, advanced-features.md

3. **Responsive Mobile Toolbar**
   - Popup overflow mode for compact display
   - Scrollable mode for continuous access
   - See: responsive-modes.md

4. **Accessible Command Bar**
   - Keyboard navigation support
   - ARIA attributes
   - Screen reader friendly
   - See: accessibility.md

5. **Customized Branded Toolbar**
   - Custom CSS styling
   - Theme integration
   - Company-specific icons
   - See: styling-customization.md

---

## Summary

The Toolbar component provides a comprehensive solution for command organization and execution in React applications. Start with getting-started.md for basic setup, then explore specific features based on your needs. Use advanced-features.md for template customization and complex scenarios.

**Navigation Path:**
1. Getting Started → Basic toolbar setup
2. Item Configuration → Add different item types
3. Responsive Modes → Handle overflow
4. Accessibility → Ensure keyboard support
5. Styling → Customize appearance
6. Advanced Features → Templates and custom components
