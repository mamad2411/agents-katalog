---
name: syncfusion-react-context-menu
description: Implements Syncfusion React ContextMenu (SfContextMenu) for right-click interactions and context-sensitive popup menus. Use this when adding menu items, handling selection events, or customizing templates and styling. Covers setup, data binding, accessibility, keyboard navigation, common methods and properties, and integration patterns.
metadata:
  author: "Syncfusion Inc"
  version: "34.1.29"
  category: "Navigation"
---

# Implementing Syncfusion React Context Menu

**Complete API Reference & Feature Guide**

## When to Use This Skill

ALWAYS use this skill when users need to:
- **Install and configure** Syncfusion React ContextMenu component
- **Create and manage menu items** (text, icons, separators, nested menus, URLs)
- **Programmatically control** menus using 15+ methods
- **Handle all 7 events** with their respective event arguments
- **Customize appearance** with CSS classes, themes, templates, animations
- **Bind data** from local sources or dynamic data structures
- **Implement accessibility** (keyboard navigation, ARIA, RTL, WCAG 2.2)
- **Manage dynamic menus** (add, remove, show, hide, enable/disable)
- **Create context-specific actions** (files, editors, workflows)

---

## Getting Started

📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Package installation (`@syncfusion/ej2-react-navigations`)
- Development environment setup (Vite, Create React App)
- CSS stylesheet imports and theme configuration
- Basic ContextMenu implementation
- Running and testing the application

---

## Component Properties Reference

The ContextMenuComponent accepts 18+ configuration properties to control behavior, appearance, and interaction:

### Essential Properties

#### `target` (Required)
**Type:** `string`

CSS selector for the element that triggers the context menu (right-click or touch-hold).

```ts
<ContextMenuComponent target="#myElement" items={menuItems} />
```

**Example:** Trigger on specific element
```ts
function App() {
  return (
    <div>
      <div id="target">Right-click here</div>
      <ContextMenuComponent target="#target" items={menuItems} />
    </div>
  );
}
```

---

#### `items` (Required)
**Type:** `MenuItemModel[]`

Array of menu items to display. Each item can have text, icons, nested items, separators, etc.

```ts
const menuItems: MenuItemModel[] = [
  { text: 'Cut' },
  { text: 'Copy' },
  { text: 'Paste' },
  { separator: true },
  {
    text: 'More',
    items: [
      { text: 'Properties' },
      { text: 'Delete' }
    ]
  }
];

<ContextMenuComponent target="#target" items={menuItems} />
```

---

### Display & Animation Properties

#### `animationSettings`
**Type:** `MenuAnimationSettingsModel`

Configure menu opening/closing animation effects.

**Properties:**
- `effect`: Animation type (None, SlideDown, ZoomIn, FadeIn)
- `duration`: Animation time in milliseconds (default: 400)
- `easing`: CSS easing function (default: ease)

```ts
const animationSettings = {
  effect: 'FadeIn',
  duration: 300,
  easing: 'ease-out'
};

<ContextMenuComponent
  target="#target"
  items={menuItems}
  animationSettings={animationSettings}
/>
```

**Available Effects:**
| Effect | Description |
|--------|-------------|
| `None` | No animation |
| `SlideDown` | Slide down from top |
| `ZoomIn` | Zoom in effect |
| `FadeIn` | Fade in opacity |

---

#### `cssClass`
**Type:** `string`

Add custom CSS classes to the ContextMenu wrapper for custom styling.

```ts
<ContextMenuComponent
  target="#target"
  items={menuItems}
  cssClass="custom-menu dark-theme"
/>
```

---

#### `enableScrolling`
**Type:** `boolean` (default: false)

Enable scrolling when menu height exceeds available space.

```ts
<ContextMenuComponent
  target="#target"
  items={largeMenuList}
  enableScrolling={true}
/>
```

---

### Interaction Properties

#### `filter`
**Type:** `string`

CSS selector for specific elements inside the target that should trigger the context menu. Use to limit context menu to certain child elements.

```ts
// Context menu only appears on table rows, not the entire table
<ContextMenuComponent
  target="#table"
  filter="tr"
  items={menuItems}
/>
```

---

#### `hoverDelay`
**Type:** `number` (default: 400)

Milliseconds to wait before displaying submenu on hover.

```ts
<ContextMenuComponent
  target="#target"
  items={menuItems}
  hoverDelay={500}  // 500ms before submenu appears
/>
```

---

#### `showItemOnClick`
**Type:** `boolean` (default: false)

Force submenus to open only on click (not on hover). When `true`, arrow key navigation is required to open submenus.

```ts
<ContextMenuComponent
  target="#target"
  items={menuItems}
  showItemOnClick={true}  // Submenus open on click only
/>
```

---

### Data & Content Properties

#### `itemTemplate`
**Type:** `string | Function`

Custom HTML template for menu items. Use template string with property placeholders (`${propertyName}`).

```ts
const template = `
  <div class="menu-item">
    <span class="${iconCss}"></span>
    <span>${text}</span>
    <span class="shortcut">${shortcut}</span>
  </div>
`;

<ContextMenuComponent
  target="#target"
  items={menuItems}
  itemTemplate={template}
/>
```

---

#### `locale`
**Type:** `string` (default: 'en-US')

Set localization language for component. Overrides global culture setting.

```ts
<ContextMenuComponent
  target="#target"
  items={menuItems}
  locale="es-ES"  // Spanish localization
/>
```

---

### Security & State Properties

#### `enableHtmlSanitizer`
**Type:** `boolean` (default: true)

Enable HTML sanitization to prevent XSS attacks. Sanitizes untrusted HTML in menu items.

```ts
<ContextMenuComponent
  target="#target"
  items={menuItems}
  enableHtmlSanitizer={true}  // Sanitize HTML content
/>
```

---

#### `enablePersistence`
**Type:** `boolean` (default: false)

Persist component state (expanded/collapsed state) across page reloads using browser storage.

```ts
<ContextMenuComponent
  target="#target"
  items={menuItems}
  enablePersistence={true}
/>
```

---

#### `enableRtl`
**Type:** `boolean` (default: false)

Enable right-to-left (RTL) layout for Arabic, Hebrew, and other RTL languages.

```ts
<ContextMenuComponent
  target="#target"
  items={menuItems}
  enableRtl={true}
/>
```

---

## Menu Item Model Properties

Each menu item is configured using `MenuItemModel` interface with the following properties:

### Text & Display

#### `text`
**Type:** `string`

Display text for the menu item.

```ts
{ text: 'Cut' }
{ text: 'Copy' }
```

---

#### `id`
**Type:** `string`

Unique identifier for the menu item. Use for identifying items in event handlers or programmatic operations.

```ts
{ id: 'cut-item', text: 'Cut' }
{ id: 'copy-item', text: 'Copy' }
```

---

#### `iconCss`
**Type:** `string`

CSS class for icon display. Supports Syncfusion icons or custom icon classes.

```ts
{ text: 'Cut', iconCss: 'e-icons e-cut' }
{ text: 'Copy', iconCss: 'e-icons e-copy' }
{ text: 'Delete', iconCss: 'e-icons e-delete' }
```

---

### Item Structure

#### `items`
**Type:** `MenuItemModel[]`

Nested submenu items. Creates hierarchical menu structure.

```ts
{
  text: 'File',
  items: [
    { text: 'New' },
    { text: 'Open' },
    { text: 'Save' }
  ]
}
```

---

#### `separator`
**Type:** `boolean` (default: false)

Render as a visual separator line instead of a clickable item.

```ts
const menuItems: MenuItemModel[] = [
  { text: 'Cut' },
  { text: 'Copy' },
  { separator: true },  // Visual divider
  { text: 'Delete' }
];
```

---

### Navigation

#### `url`
**Type:** `string`

Navigation URL. Creates an anchor link that navigates when clicked.

```ts
{ text: 'Visit Site', url: 'https://example.com' }
{ text: 'Documentation', url: '/docs' }
```

---

### Custom Attributes

#### `htmlAttributes`
**Type:** `Record<string, string>`

Add custom HTML attributes to menu item element.

```ts
{
  text: 'Download',
  htmlAttributes: {
    'data-action': 'download',
    'aria-label': 'Download file',
    'title': 'Download the file'
  }
}
```

---

## Menu Methods – Programmatic Control

The ContextMenu exposes 15+ methods for runtime control and manipulation:

### Menu State Control

#### `open(top: number, left: number, target?: HTMLElement): void`

Programmatically open the context menu at specified coordinates.

**Parameters:**
- `top`: Vertical position (Y-coordinate in pixels)
- `left`: Horizontal position (X-coordinate in pixels)
- `target`: Optional HTML element for z-index calculation

```ts
function App() {
  const menuRef = React.useRef<ContextMenuComponent>(null);

  const openMenuAtClick = (event: React.MouseEvent) => {
    menuRef.current?.open(event.clientY, event.clientX);
  };

  return (
    <div>
      <button onClick={openMenuAtClick}>Open Menu</button>
      <ContextMenuComponent ref={menuRef} target="#target" items={menuItems} />
    </div>
  );
}
```

---

#### `close(): void`

Programmatically close the context menu.

```ts
function App() {
  const menuRef = React.useRef<ContextMenuComponent>(null);

  const closeMenu = () => {
    menuRef.current?.close();
  };

  const handleItemSelect = (args: MenuEventArgs) => {
    console.log('Selected:', args.item?.text);
    closeMenu();  // Close menu after selection
  };

  return (
    <ContextMenuComponent
      ref={menuRef}
      target="#target"
      items={menuItems}
      select={handleItemSelect}
    />
  );
}
```

---

### Item Visibility Control

#### `showItems(items: string[], isUniqueId?: boolean): void`

Show menu items that were previously hidden.

**Parameters:**
- `items`: Array of item text or IDs to show
- `isUniqueId`: If true, treat items as unique IDs; if false, treat as text (default: false)

```ts
function App() {
  const menuRef = React.useRef<ContextMenuComponent>(null);

  const showDeleteOption = () => {
    menuRef.current?.showItems(['Delete', 'Rename']);
  };

  return (
    <div>
      <button onClick={showDeleteOption}>Show Options</button>
      <ContextMenuComponent ref={menuRef} target="#target" items={menuItems} />
    </div>
  );
}
```

---

#### `hideItems(items: string[], isUniqueId?: boolean): void`

Hide specific menu items from display while keeping them in the menu structure.

**Parameters:**
- `items`: Array of item text or IDs to hide
- `isUniqueId`: If true, treat items as unique IDs

```ts
function App() {
  const menuRef = React.useRef<ContextMenuComponent>(null);

  React.useEffect(() => {
    // Hide delete option for read-only mode
    if (isReadOnly) {
      menuRef.current?.hideItems(['Delete', 'Modify']);
    }
  }, [isReadOnly]);

  return (
    <ContextMenuComponent ref={menuRef} target="#target" items={menuItems} />
  );
}
```

---

### Item State Management

#### `enableItems(items: string[], enable: boolean, isUniqueId?: boolean): void`

Enable or disable menu items to control interactivity.

**Parameters:**
- `items`: Array of item text or IDs to modify
- `enable`: true to enable, false to disable
- `isUniqueId`: If true, treat items as unique IDs

```ts
function App() {
  const menuRef = React.useRef<ContextMenuComponent>(null);

  const disablePasteIfNoClipboard = async () => {
    const canPaste = await navigator.permissions.query({ name: 'clipboard-read' });
    if (canPaste.state === 'denied') {
      menuRef.current?.enableItems(['Paste'], false);
    }
  };

  React.useEffect(() => {
    disablePasteIfNoClipboard();
  }, []);

  return (
    <ContextMenuComponent
      ref={menuRef}
      target="#target"
      items={menuItems}
      beforeOpen={disablePasteIfNoClipboard}
    />
  );
}
```

---

### Item Manipulation

#### `insertAfter(items: MenuItemModel[], text: string, isUniqueId?: boolean): void`

Insert new menu items after a specified target item.

**Parameters:**
- `items`: Array of new MenuItemModel items to insert
- `text`: Text or ID of target item to insert after
- `isUniqueId`: If true, treat text as unique ID

```ts
function App() {
  const menuRef = React.useRef<ContextMenuComponent>(null);

  const addSortByOption = () => {
    const newItems: MenuItemModel[] = [
      { text: 'Sort By Name' },
      { text: 'Sort By Date' }
    ];
    menuRef.current?.insertAfter(newItems, 'View');
  };

  return (
    <div>
      <button onClick={addSortByOption}>Add Sort Options</button>
      <ContextMenuComponent ref={menuRef} target="#target" items={menuItems} />
    </div>
  );
}
```

---

#### `insertBefore(items: MenuItemModel[], text: string, isUniqueId?: boolean): void`

Insert new menu items before a specified target item.

```ts
function App() {
  const menuRef = React.useRef<ContextMenuComponent>(null);

  const addPremiumOptions = () => {
    const premiumItems: MenuItemModel[] = [
      { text: 'Premium Feature 1' },
      { text: 'Premium Feature 2', iconCss: 'e-icons e-star' }
    ];
    // Insert before 'Delete' option
    menuRef.current?.insertBefore(premiumItems, 'Delete');
  };

  React.useEffect(() => {
    if (user.isPremium) {
      addPremiumOptions();
    }
  }, [user.isPremium]);

  return (
    <ContextMenuComponent ref={menuRef} target="#target" items={menuItems} />
  );
}
```

---

#### `removeItems(items: string[], isUniqueId?: boolean): void`

Remove menu items from the menu.

**Parameters:**
- `items`: Array of item text or IDs to remove
- `isUniqueId`: If true, treat items as unique IDs

```ts
function App() {
  const menuRef = React.useRef<ContextMenuComponent>(null);

  const removeRestrictedActions = () => {
    menuRef.current?.removeItems(['Delete', 'Export', 'Archive']);
  };

  React.useEffect(() => {
    if (userRole === 'viewer') {
      removeRestrictedActions();
    }
  }, [userRole]);

  return (
    <ContextMenuComponent
      ref={menuRef}
      target="#target"
      items={menuItems}
      created={removeRestrictedActions}
    />
  );
}
```

---

### Item Queries

#### `getItemIndex(item: MenuItem | string, isUniqueId?: boolean): number[]`

Get the index/indices of a menu item. Returns array because item can exist at multiple levels (for nested items).

**Parameters:**
- `item`: MenuItem object or text/ID string to find
- `isUniqueId`: If true, treat item as unique ID

**Returns:** `number[]` - Array of index numbers representing item position

```ts
function App() {
  const menuRef = React.useRef<ContextMenuComponent>(null);

  const findItemPosition = () => {
    const indices = menuRef.current?.getItemIndex('Copy');
    console.log('Copy is at index:', indices);  // Output: [1] or [0, 1] for nested
    
    const nestedIndices = menuRef.current?.getItemIndex('Open', false);
    console.log('Open is at indices:', nestedIndices);  // Output: [0, 1] for nested
  };

  return (
    <div>
      <button onClick={findItemPosition}>Find Item</button>
      <ContextMenuComponent ref={menuRef} target="#target" items={menuItems} />
    </div>
  );
}
```

---

#### `setItem(item: MenuItem, id?: string, isUniqueId?: boolean): void`

Update an existing menu item's properties.

**Parameters:**
- `item`: MenuItem object with updated properties
- `id`: Text or ID of item to update
- `isUniqueId`: If true, treat id as unique ID

```ts
function App() {
  const menuRef = React.useRef<ContextMenuComponent>(null);

  const updateDeleteItemStyle = () => {
    const updatedItem: MenuItemModel = {
      text: 'Delete',
      iconCss: 'e-icons e-delete',
      htmlAttributes: {
        'class': 'dangerous-action'
      }
    };
    menuRef.current?.setItem(updatedItem, 'Delete');
  };

  return (
    <div>
      <button onClick={updateDeleteItemStyle}>Update Delete Item</button>
      <ContextMenuComponent ref={menuRef} target="#target" items={menuItems} />
    </div>
  );
}
```

---

### Component Lifecycle

#### `destroy(): void`

Destroy the ContextMenu component and free resources.

```ts
function App() {
  const menuRef = React.useRef<ContextMenuComponent>(null);

  React.useEffect(() => {
    return () => {
      // Cleanup on component unmount
      menuRef.current?.destroy();
    };
  }, []);

  return (
    <ContextMenuComponent ref={menuRef} target="#target" items={menuItems} />
  );
}
```

---

## Events & Event Arguments

The ContextMenu component provides 7 events for monitoring and controlling user interactions:

### Menu Lifecycle Events

#### `beforeOpen`
**Type:** `EmitType<BeforeOpenCloseMenuEventArgs>`

Fires **before** the menu opens. Use to prevent opening, modify items, or prepare data.

**Event Arguments:**

```ts
interface BeforeOpenCloseMenuEventArgs {
  element: HTMLElement;           // Menu element
  event: Event;                    // Browser event object
  items: MenuItemModel[];          // Current menu items
  cancel: boolean;                 // Set to true to prevent action
  parentItem?: MenuItemModel;      // Parent item if submenu
}
```

**Example: Prevent opening in certain conditions**

```ts
function App() {
  const handleBeforeOpen = (args: BeforeOpenCloseMenuEventArgs) => {
    // Prevent opening on read-only elements
    const target = args.event?.target as HTMLElement;
    if (target?.classList.contains('read-only')) {
      args.cancel = true;  // Prevent menu from opening
      return;
    }

    // Modify items before opening
    const selectedText = window.getSelection()?.toString();
    if (!selectedText) {
      // Disable text-related operations if no text selected
      args.items = args.items?.map(item => ({
        ...item,
        disabled: ['Copy', 'Cut'].includes(item.text as string)
      }));
    }
  };

  return (
    <ContextMenuComponent
      target="#target"
      items={menuItems}
      beforeOpen={handleBeforeOpen}
    />
  );
}
```

---

#### `onOpen`
**Type:** `EmitType<OpenCloseMenuEventArgs>`

Fires **after** the menu opens. Use to initialize UI or perform post-open actions.

**Event Arguments:**

```ts
interface OpenCloseMenuEventArgs {
  element: HTMLElement;           // Menu element
  event: Event;                    // Browser event that triggered opening
  items: MenuItemModel[];          // Current menu items
}
```

**Example: Initialize after opening**

```ts
function App() {
  const handleOnOpen = (args: OpenCloseMenuEventArgs) => {
    console.log('Menu opened at:', new Date());
    console.log('Number of items:', args.items?.length);
    
    // Set focus to first menu item for accessibility
    setTimeout(() => {
      const firstItem = args.element?.querySelector('.e-menu-item');
      (firstItem as HTMLElement)?.focus();
    }, 0);
  };

  return (
    <ContextMenuComponent
      target="#target"
      items={menuItems}
      onOpen={handleOnOpen}
    />
  );
}
```

---

#### `beforeClose`
**Type:** `EmitType<BeforeOpenCloseMenuEventArgs>`

Fires **before** the menu closes. Use to prevent closing or save state.

**Example: Prevent closing on unsaved changes**

```ts
function App() {
  const [hasUnsavedChanges, setHasUnsavedChanges] = React.useState(false);

  const handleBeforeClose = (args: BeforeOpenCloseMenuEventArgs) => {
    if (hasUnsavedChanges) {
      const confirmed = window.confirm('Unsaved changes. Close anyway?');
      if (!confirmed) {
        args.cancel = true;  // Prevent menu from closing
      }
    }
  };

  return (
    <ContextMenuComponent
      target="#target"
      items={menuItems}
      beforeClose={handleBeforeClose}
    />
  );
}
```

---

#### `onClose`
**Type:** `EmitType<OpenCloseMenuEventArgs>`

Fires **after** the menu closes. Use for cleanup or state management.

**Example: Clean up after menu closes**

```ts
function App() {
  const handleOnClose = (args: OpenCloseMenuEventArgs) => {
    console.log('Menu closed');
    
    // Clear temporary selections or states
    document.querySelectorAll('.temp-highlight').forEach(el => {
      el.classList.remove('temp-highlight');
    });
  };

  return (
    <ContextMenuComponent
      target="#target"
      items={menuItems}
      onClose={handleOnClose}
    />
  );
}
```

---

### Item Interaction Events

#### `select`
**Type:** `EmitType<MenuEventArgs>`

Fires when a menu item is clicked/selected. Use to execute actions based on selection.

**Event Arguments:**

```ts
interface MenuEventArgs {
  element: HTMLElement;           // Menu item element
  event: Event;                    // Click/keyboard event
  item?: MenuItemModel;            // Selected menu item
  items?: MenuItemModel[];         // All menu items
}
```

**Example: Execute actions on item selection**

```ts
function App() {
  const handleSelect = (args: MenuEventArgs) => {
    const itemText = args.item?.text;

    switch (itemText) {
      case 'Cut':
        document.execCommand('cut');
        console.log('Cut executed');
        break;
      case 'Copy':
        document.execCommand('copy');
        console.log('Copy executed');
        break;
      case 'Paste':
        document.execCommand('paste');
        console.log('Paste executed');
        break;
      case 'Delete':
        if (confirm('Confirm delete?')) {
          console.log('Delete executed');
        }
        break;
    }
  };

  return (
    <ContextMenuComponent
      target="#target"
      items={menuItems}
      select={handleSelect}
    />
  );
}
```

---

#### `beforeItemRender`
**Type:** `EmitType<MenuEventArgs>`

Fires **before** each menu item renders. Use to customize item appearance or add custom logic.

**Example: Conditionally disable items**

```ts
function App() {
  const handleBeforeItemRender = (args: MenuEventArgs) => {
    const itemText = args.item?.text;

    // Disable delete if user doesn't have permission
    if (itemText === 'Delete' && !userPermissions.canDelete) {
      args.element?.classList.add('e-disabled');
    }

    // Highlight recent items
    if (itemText?.startsWith('Recent:')) {
      args.element?.classList.add('recent-item-highlight');
    }

    // Add keyboard shortcut indicator
    const shortcuts: Record<string, string> = {
      'Cut': 'Ctrl+X',
      'Copy': 'Ctrl+C',
      'Paste': 'Ctrl+V'
    };

    if (shortcuts[itemText as string]) {
      const shortcutEl = document.createElement('span');
      shortcutEl.className = 'shortcut-hint';
      shortcutEl.textContent = shortcuts[itemText as string];
      args.element?.appendChild(shortcutEl);
    }
  };

  return (
    <ContextMenuComponent
      target="#target"
      items={menuItems}
      beforeItemRender={handleBeforeItemRender}
    />
  );
}
```

---

### Component Lifecycle

#### `created`
**Type:** `EmitType<Event>`

Fires after the component is fully created and rendered. Use for initialization.

**Example: Initialize after creation**

```ts
function App() {
  const menuRef = React.useRef<ContextMenuComponent>(null);

  const handleCreated = () => {
    console.log('ContextMenu created and ready');
    
    // Perform initial setup
    menuRef.current?.enableItems(['Advanced Options'], userRole === 'admin');
    
    // Add custom data to items
    const items = menuRef.current?.items;
    if (items) {
      items.forEach((item, index) => {
        item.id = `item-${index}`;
      });
    }
  };

  return (
    <ContextMenuComponent
      ref={menuRef}
      target="#target"
      items={menuItems}
      created={handleCreated}
    />
  );
}
```

---

## Menu Items and Data Binding

📄 **Read:** [references/menu-items-and-data-binding.md](references/menu-items-and-data-binding.md)
- Creating menu items with MenuItemModel
- Using the items property
- Data binding with local data sources
- Dynamic menu item generation from arrays
- Nested submenu configuration

---

## Templates and Customization

📄 **Read:** [references/templates-and-customization.md](references/templates-and-customization.md)
- Custom item templates (itemTemplate)
- Rendering rich content in menu items
- beforeItemRender event for item customization
- Adding icons and metadata to items
- Conditional rendering

---

## Styling and Appearance

📄 **Read:** [references/styling-and-appearance.md](references/styling-and-appearance.md)
- CSS class customization
- Theme Studio integration
- Custom CSS overrides for menu elements
- Icon styling and positioning
- Visual states (hover, selected, disabled)

---

## Accessibility and Keyboard Navigation

📄 **Read:** [references/accessibility-and-keyboard-navigation.md](references/accessibility-and-keyboard-navigation.md)
- WCAG 2.2 and Section 508 compliance
- Screen reader support and ARIA attributes
- Keyboard shortcuts (Esc, Enter, arrow keys)
- Right-to-left (RTL) support
- Focus management

---

## Advanced Features

📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- Scrollable context menus
- Animation settings and effects
- Menu open types and positioning
- Overflow handling and dynamic layouts
- Configuration for complex scenarios

---

## Use Cases and Patterns

📄 **Read:** [references/use-cases-and-patterns.md](references/use-cases-and-patterns.md)
- Common context menu patterns
- Adding/removing/enabling/disabling items dynamically
- Rendering separators between items
- Multi-level nesting examples
- Real-world integration scenarios

---

## Quick Reference

### Essential Code Template

```ts
import { ContextMenuComponent, MenuItemModel } from '@syncfusion/ej2-react-navigations';
import * as React from 'react';

function App() {
  const menuRef = React.useRef<ContextMenuComponent>(null);

  const menuItems: MenuItemModel[] = [
    { text: 'Cut', iconCss: 'e-icons e-cut', id: 'cut' },
    { text: 'Copy', iconCss: 'e-icons e-copy', id: 'copy' },
    { text: 'Paste', iconCss: 'e-icons e-paste', id: 'paste' },
    { separator: true },
    {
      text: 'More',
      items: [
        { text: 'Delete' },
        { text: 'Properties' }
      ]
    }
  ];

  const handleSelect = (args: any) => {
    console.log('Selected:', args.item?.text);
  };

  const handleBeforeOpen = (args: any) => {
    // Customize menu before opening
  };

  return (
    <div>
      <div id="target">Right-click me</div>
      <ContextMenuComponent
        ref={menuRef}
        target="#target"
        items={menuItems}
        select={handleSelect}
        beforeOpen={handleBeforeOpen}
        animationSettings={{ effect: 'FadeIn', duration: 300 }}
        enableScrolling={true}
      />
    </div>
  );
}

export default App;
```

### Common Methods Reference

```ts
// Open menu at coordinates
menuRef.current?.open(100, 150);

// Close menu
menuRef.current?.close();

// Enable/disable items
menuRef.current?.enableItems(['Delete', 'Archive'], false);

// Show/hide items
menuRef.current?.showItems(['Delete']);
menuRef.current?.hideItems(['Export']);

// Add items
menuRef.current?.insertAfter(
  [{ text: 'New Option' }],
  'Existing Item'
);

// Remove items
menuRef.current?.removeItems(['Outdated Item']);

// Get item index
const indices = menuRef.current?.getItemIndex('Copy');
```

---

**Next Steps:** Choose reference based on your need. Start with [getting-started.md](references/getting-started.md), or explore specific features in other references.
