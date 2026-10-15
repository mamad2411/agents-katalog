---
name: syncfusion-angular-context-menu
description: "Implement Syncfusion Angular ContextMenu component for right-click and touch-hold menus. Use this skill when user needs to create context menus, add/remove/enable menu items, handle menu clicks, customize animations, apply templates, handle data binding, trigger dialogs from menu items, show/hide items dynamically, add icons, create scrollable menus, or customize menu appearance."
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Navigation Components"
---

# Implementing Syncfusion Angular ContextMenu

The **ContextMenu** is a graphical user interface that appears when users right-click or perform touch-hold actions. It provides a context-aware menu with support for nested items, dynamic updates, animations, custom templates, and comprehensive event handling. This skill guides you through implementing, configuring, and customizing context menus for Angular applications.

## When to Use This Skill

**Use this skill when:**
- You need to create a right-click or touch-hold context menu
- Managing menu items dynamically (add, remove, enable, disable)
- Handling menu item click events and actions
- Opening dialogs or navigating from menu selections
- Customizing menu appearance with animations, icons, or themes
- Showing/hiding items based on context or user permissions
- Binding menu items from data sources
- Creating complex menu templates or nested structures
- Implementing responsive menus with scrolling
- Adding keyboard shortcuts or accessibility features

## Component Overview

The ContextMenu component enables intuitive right-click interfaces with:
- ✅ Dynamic item management (add/remove/enable/disable)
- ✅ Multi-level nested menus
- ✅ Data binding from arrays or objects
- ✅ Customizable animations (FadeIn, SlideDown, ZoomIn, None)
- ✅ Template support for rich content (icons, HTML, tables)
- ✅ Event handling (click, open, close)
- ✅ Icon and URL navigation
- ✅ Scrollable menus for large item lists
- ✅ Accessibility with keyboard support

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Package installation and dependencies
- Angular environment setup (standalone architecture)
- Creating your first ContextMenu
- Configuring target elements
- Basic menu item structure

### Menu Items Management
📄 **Read:** [references/menu-items-management.md](references/menu-items-management.md)
- Adding menu items dynamically (insertBefore, insertAfter)
- Removing menu items (removeItems method)
- Enabling and disabling items (enableItems)
- Showing and hiding items (showItems, hideItems)
- Dynamic context-aware menus
- Multi-level nested menus

### Data Binding
📄 **Read:** [references/data-binding.md](references/data-binding.md)
- Populating items from data sources
- MenuItemModel structure and properties
- Parent-child item relationships
- beforeItemRender event for item formatting
- Dynamic data updates

### Interaction & Events
📄 **Read:** [references/interaction-and-events.md](references/interaction-and-events.md)
- Menu item click handlers (select event)
- Click-to-open submenus (showItemOnClick)
- Programmatic open and close methods
- Menu positioning with coordinates
- Opening dialogs on item selection
- MenuEventArgs and event properties

### Styling & Customization
📄 **Read:** [references/styling-and-customization.md](references/styling-and-customization.md)
- Animation settings and effects (FadeIn, SlideDown, ZoomIn, None)
- CSS customization and class targeting
- Icon styling with iconCss property
- URL navigation and external links
- Scrollable menus (enableScrolling)
- Responsive design and Theme Studio

### Templates & Advanced Features
📄 **Read:** [references/templates-and-advanced.md](references/templates-and-advanced.md)
- Custom item templates (itemTemplate)
- Rich content with HTML and tables
- Character underlining and formatting
- Separator items and grouping
- Accessibility and keyboard navigation
- Advanced template patterns

## Quick Start Example

```typescript
import { Component } from '@angular/core';
import { ContextMenuModule } from '@syncfusion/ej2-angular-navigations';
import { MenuItemModel } from '@syncfusion/ej2-navigations';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [ContextMenuModule],
  template: `
    <div class="e-section-control">
      <!-- Target element for context menu -->
      <div id="target">Right click / Touch hold to open the ContextMenu</div>
      
      <!-- ContextMenu component -->
      <ejs-contextmenu 
        id='contextmenu' 
        target='#target' 
        [items]='menuItems'>
      </ejs-contextmenu>
    </div>
  `
})
export class AppComponent {
  public menuItems: MenuItemModel[] = [
    { text: 'Cut', iconCss: 'e-cm-icons e-cut' },
    { text: 'Copy', iconCss: 'e-cm-icons e-copy' },
    { text: 'Paste', iconCss: 'e-cm-icons e-paste' },
    { separator: true },
    {
      text: 'View',
      items: [
        { text: 'Large icons' },
        { text: 'Small icons' }
      ]
    }
  ];
}
```

## Common Patterns

### Pattern 1: Dynamic Item Management
```typescript
// Add items after 'Refresh'
this.contextmenu.insertAfter([{ text: 'Sort By' }], 'Refresh');

// Remove 'Paste' item
this.contextmenu.removeItems(['Paste']);

// Disable 'Edit' item
this.contextmenu.enableItems(['Edit'], false);
```

### Pattern 2: Context-Aware Menus
```typescript
beforeOpen(args: BeforeOpenCloseMenuEventArgs) {
  if ((args.event.target as HTMLElement).id === 'editor') {
    this.contextmenu.showItems(['Add', 'Edit', 'Delete']);
    this.contextmenu.hideItems(['Cut', 'Copy', 'Paste']);
  }
}
```

### Pattern 3: Menu Item Click Handler
```typescript
itemSelect(args: MenuEventArgs): void {
  if (args.item.text === 'Save As...') {
    this.dialogComponent.show();
  }
}
```

### Pattern 4: Animation Configuration
```typescript
public animationSettings = {
  effect: 'FadeIn',
  duration: 400,
  easing: 'ease'
};
```

## Complete API Reference

### Component Properties

#### Core Configuration Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `target` | `string` | `''` | **Required.** Specifies target element selector in which the ContextMenu should be opened. |
| `items` | `MenuItemModel[]` | `[]` | Specifies menu items with its properties which will be rendered as ContextMenu. |
| `showItemOnClick` | `boolean` | `false` | Specifies whether to show the sub menu or not on click. When `true`, the sub menu will open only on mouse click. |
| `filter` | `string` | `''` | Specifies the filter selector for elements inside the target in that the context menu will be opened. |
| `hoverDelay` | `number` | `0` | If `hoverDelay` is set by particular number, the menu will open after that period (in milliseconds). |

#### Styling & Appearance Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `animationSettings` | `MenuAnimationSettingsModel` | `{ duration: 400, easing: 'ease', effect: 'SlideDown' }` | Specifies the animation settings for the sub menu open/close. See [Animation Settings](#animation-settings) section. |
| `cssClass` | `string` | `''` | Defines class/multiple classes separated by a space in the Menu wrapper. Use for custom styling. |
| `enableRtl` | `boolean` | `false` | Enable or disable rendering component in right to left direction. |

#### Data & Behavior Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `itemTemplate` | `string \| Function` | `null` | This property allows you to define custom templates for items in the ContextMenu. Can be string selector or template function. |
| `locale` | `string` | `''` | Overrides the global culture and localization value for this component. Default global culture is `'en-US'`. |
| `enableScrolling` | `boolean` | `false` | Specifies whether to enable/disable the scrollable option in ContextMenu. |

#### Security & Persistence Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `enableHtmlSanitizer` | `boolean` | `true` | Specifies whether to enable the rendering of untrusted HTML values. If `true`, the component will sanitize any suspected untrusted strings and scripts before rendering them. Set to `false` only when you trust the HTML source completely. |
| `enablePersistence` | `boolean` | `false` | Enable or disable persisting component's state between page reloads. When enabled, menu state is saved in localStorage. |

#### Property Example - Basic Configuration

**Brief Example:**
```typescript
@Component({
  selector: 'app-context-menu',
  template: `
    <div id="target">Right click here</div>
    <ejs-contextmenu 
      target='#target' 
      [items]='items'
      [animationSettings]='animSettings'
      cssClass='custom-menu'>
    </ejs-contextmenu>
  `
})
export class ContextMenuComponent {
  items: MenuItemModel[] = [
    { text: 'Edit' },
    { text: 'Delete' }
  ];
  
  animSettings = {
    duration: 300,
    effect: 'FadeIn',
    easing: 'ease-out'
  };
}
```

**Full Working Example:**
```typescript
import { Component, ViewChild } from '@angular/core';
import { ContextMenuComponent } from '@syncfusion/ej2-angular-navigations';
import { MenuItemModel } from '@syncfusion/ej2-navigations';

@Component({
  selector: 'app-context-menu-config',
  standalone: true,
  imports: [ContextMenuModule],
  template: `
    <div class="container">
      <h3>Advanced Configuration Example</h3>
      
      <!-- Target element for context menu -->
      <div id="configTarget" class="target-box">
        Right click or touch hold to open menu
      </div>
      
      <!-- ContextMenu with complete configuration -->
      <ejs-contextmenu 
        #contextMenu
        id='contextMenu'
        target='#configTarget'
        [items]='menuItems'
        [animationSettings]='animationSettings'
        cssClass='modern-menu'
        [showItemOnClick]='true'
        [enableScrolling]='true'
        [hoverDelay]='300'
        [enableHtmlSanitizer]='true'
        [enablePersistence]='true'
        locale='en-US'>
      </ejs-contextmenu>
    </div>
  `,
  styles: [`
    .target-box {
      width: 300px;
      height: 200px;
      border: 2px dashed #ccc;
      display: flex;
      align-items: center;
      justify-content: center;
      background: #f5f5f5;
      cursor: context-menu;
    }
  `]
})
export class AdvancedContextMenuComponent {
  @ViewChild('contextMenu') contextMenu!: ContextMenuComponent;
  
  menuItems: MenuItemModel[] = [
    { text: 'Edit', iconCss: 'e-cm-icons e-edit', id: 'edit' },
    { text: 'Delete', iconCss: 'e-cm-icons e-delete', id: 'delete' },
    { separator: true },
    { text: 'More', id: 'more' }
  ];
  
  animationSettings = {
    effect: 'FadeIn' as any,
    duration: 400,
    easing: 'ease-in-out'
  };
}
```

### Menu Item Properties (MenuItemModel)

MenuItemModel defines the structure for each menu item. Each item in the `items` array follows this model:

| Property | Type | Optional | Description |
|----------|------|----------|-------------|
| `text` | `string` | No | **Required.** Specifies text for menu item. This is the display label shown to users. |
| `id` | `string` | Yes | Specifies the id for menu item. Use this for identifying items in methods like `enableItems()`, `removeItems()`, etc. |
| `items` | `MenuItemModel[]` | Yes | Specifies the sub menu items that is the array of MenuItem model. Creates nested/hierarchical menus. |
| `separator` | `boolean` | Yes | Specifies separator between the menu items. Separators are either horizontal or vertical lines used to group menu items. Set to `true` to create a visual divider. |
| `iconCss` | `string` | Yes | Defines class/multiple classes separated by a space for the menu Item that is used to include an icon. Menu Item can include font icon and sprite image. Example: `iconCss: 'e-icons e-edit'`. |
| `url` | `string` | Yes | Specifies url for menu item that creates the anchor link to navigate to the url provided. When clicked, navigates to this URL. |
| `htmlAttributes` | `Record<string, any>` | Yes | Specifies the htmlAttributes property to support adding custom attributes to the menu items. Example: `{ 'data-info': 'value', 'title': 'My Tooltip' }`. |

#### MenuItem Example - Basic Usage

**Brief Example:**
```typescript
items: MenuItemModel[] = [
  { text: 'Cut', id: 'cut', iconCss: 'e-icons e-cut' },
  { text: 'Copy', id: 'copy', iconCss: 'e-icons e-copy' },
  { text: 'Paste', id: 'paste', iconCss: 'e-icons e-paste' },
  { separator: true },
  { text: 'Delete', id: 'delete', iconCss: 'e-icons e-delete' }
];
```

**Full Working Example - Complex MenuItemModel:**
```typescript
@Component({
  selector: 'app-menu-items-config',
  standalone: true,
  imports: [ContextMenuModule],
  template: `
    <div id="target">Right click for advanced menu</div>
    <ejs-contextmenu target='#target' [items]='menuItems'></ejs-contextmenu>
  `
})
export class MenuItemsComponent {
  menuItems: MenuItemModel[] = [
    // Item with icon
    {
      text: 'Edit',
      id: 'edit-item',
      iconCss: 'e-icons e-edit',
      htmlAttributes: {
        'data-action': 'edit',
        'title': 'Edit selected item'
      }
    },
    // Item with submenu
    {
      text: 'Format',
      id: 'format',
      iconCss: 'e-icons e-palette',
      items: [
        { text: 'Bold', id: 'bold' },
        { text: 'Italic', id: 'italic' },
        { text: 'Underline', id: 'underline' }
      ]
    },
    // Navigation item with URL
    {
      text: 'Visit Website',
      id: 'website',
      iconCss: 'e-icons e-export',
      url: 'https://example.com',
      htmlAttributes: { 'target': '_blank' }
    },
    // Separator
    { separator: true },
    // Item with nested submenu
    {
      text: 'Advanced',
      id: 'advanced',
      items: [
        {
          text: 'Settings',
          id: 'settings',
          items: [
            { text: 'General', id: 'general' },
            { text: 'Advanced', id: 'adv' }
          ]
        },
        { text: 'Help', id: 'help', url: 'https://help.example.com' }
      ]
    }
  ];
}
```

### Component Methods

#### Method: enableItems

**Signature:**
```typescript
enableItems(items: string[], enable?: boolean, isUniqueId?: boolean): void
```

| Parameter | Type | Optional | Description |
|-----------|------|----------|-------------|
| `items` | `string[]` | No | Array of item text or ids that needs to be enabled/disabled. |
| `enable` | `boolean` | Yes, default: `true` | Set `true` to enable items; set `false` to disable items. |
| `isUniqueId` | `boolean` | Yes, default: `false` | Set `true` if items array contains unique ids instead of text. |

**Return:** `void`

**Brief Example:**
```typescript
// Disable 'Delete' item by text
this.contextMenu.enableItems(['Delete'], false);

// Enable items by id
this.contextMenu.enableItems(['edit-item', 'copy-item'], true, true);
```

**Full Working Example:**
```typescript
@Component({
  selector: 'app-enable-items',
  template: `
    <button (click)="disableDelete()">Disable Delete</button>
    <button (click)="enableAll()">Enable All</button>
    <div id="target">Right click here</div>
    <ejs-contextmenu #cm target='#target' [items]='items'></ejs-contextmenu>
  `
})
export class EnableItemsComponent {
  @ViewChild('cm') contextMenu!: ContextMenuComponent;
  items: MenuItemModel[] = [
    { text: 'Edit', id: 'edit' },
    { text: 'Delete', id: 'delete' },
    { text: 'Copy', id: 'copy' }
  ];
  
  disableDelete() {
    this.contextMenu.enableItems(['Delete'], false);
  }
  
  enableAll() {
    this.contextMenu.enableItems(['Edit', 'Delete', 'Copy'], true);
  }
}
```

#### Method: insertAfter

**Signature:**
```typescript
insertAfter(items: MenuItemModel[], text: string, isUniqueId?: boolean): void
```

| Parameter | Type | Optional | Description |
|-----------|------|----------|-------------|
| `items` | `MenuItemModel[]` | No | Array of MenuItemModel that needs to be inserted. |
| `text` | `string` | No | Text item after which the element to be inserted. If `isUniqueId` is true, this is the unique id. |
| `isUniqueId` | `boolean` | Yes, default: `false` | Set `true` if text is a unique id instead of display text. |

**Return:** `void`

**Brief Example:**
```typescript
// Insert item after 'Edit'
this.contextMenu.insertAfter([{ text: 'Save' }], 'Edit');

// Insert after item with specific id
this.contextMenu.insertAfter([{ text: 'New', id: 'new-item' }], 'edit-item', true);
```

**Full Working Example:**
```typescript
@Component({
  selector: 'app-insert-after',
  template: `
    <button (click)="addAfterEdit()">Add Item After Edit</button>
    <div id="target">Right click here</div>
    <ejs-contextmenu #cm target='#target' [items]='items'></ejs-contextmenu>
  `
})
export class InsertAfterComponent {
  @ViewChild('cm') contextMenu!: ContextMenuComponent;
  items: MenuItemModel[] = [
    { text: 'Edit', id: 'edit' },
    { text: 'Delete', id: 'delete' }
  ];
  
  addAfterEdit() {
    this.contextMenu.insertAfter(
      [
        { text: 'Copy', id: 'copy' },
        { text: 'Paste', id: 'paste' }
      ],
      'Edit'
    );
  }
}
```

#### Method: insertBefore

**Signature:**
```typescript
insertBefore(items: MenuItemModel[], text: string, isUniqueId?: boolean): void
```

| Parameter | Type | Optional | Description |
|-----------|------|----------|-------------|
| `items` | `MenuItemModel[]` | No | Array of MenuItemModel that needs to be inserted. |
| `text` | `string` | No | Text item before which the element to be inserted. If `isUniqueId` is true, this is the unique id. |
| `isUniqueId` | `boolean` | Yes, default: `false` | Set `true` if text is a unique id instead of display text. |

**Return:** `void`

**Brief Example:**
```typescript
this.contextMenu.insertBefore([{ text: 'Undo' }], 'Edit');
```

#### Method: removeItems

**Signature:**
```typescript
removeItems(items: string[], isUniqueId?: boolean): void
```

| Parameter | Type | Optional | Description |
|-----------|------|----------|-------------|
| `items` | `string[]` | No | Array of item text or ids that needs to be removed. |
| `isUniqueId` | `boolean` | Yes, default: `false` | Set `true` if items array contains unique ids instead of text. |

**Return:** `void`

**Brief Example:**
```typescript
this.contextMenu.removeItems(['Delete', 'Copy']);
```

#### Method: hideItems

**Signature:**
```typescript
hideItems(items: string[], isUniqueId?: boolean): void
```

| Parameter | Type | Optional | Description |
|-----------|------|----------|-------------|
| `items` | `string[]` | No | Array of item text or ids that needs to be hidden. |
| `isUniqueId` | `boolean` | Yes, default: `false` | Set `true` if items array contains unique ids instead of text. |

**Return:** `void`

**Brief Example:**
```typescript
this.contextMenu.hideItems(['AdminOnly'], true);
```

#### Method: showItems

**Signature:**
```typescript
showItems(items: string[], isUniqueId?: boolean): void
```

| Parameter | Type | Optional | Description |
|-----------|------|----------|-------------|
| `items` | `string[]` | No | Array of item text or ids that needs to be shown. |
| `isUniqueId` | `boolean` | Yes, default: `false` | Set `true` if items array contains unique ids instead of text. |

**Return:** `void`

**Brief Example:**
```typescript
this.contextMenu.showItems(['AdminOnly'], true);
```

#### Method: getItemIndex

**Signature:**
```typescript
getItemIndex(item: MenuItem | string, isUniqueId?: boolean): number[]
```

| Parameter | Type | Optional | Description |
|-----------|------|----------|-------------|
| `item` | `MenuItem \| string` | No | MenuItem object or id/text to get the index for. |
| `isUniqueId` | `boolean` | Yes, default: `false` | Set `true` if item is a unique id instead of text. |

**Return:** `number[]` - Array of indices representing the position of the item in the menu hierarchy.

**Brief Example:**
```typescript
// Get index by text
const index = this.contextMenu.getItemIndex('Edit'); // [0] for first item

// Get index by id
const index = this.contextMenu.getItemIndex('edit-item', true); // [0]

// For nested items
const index = this.contextMenu.getItemIndex('Bold', true); // [1, 0] for Format > Bold
```

**Full Working Example:**
```typescript
@Component({
  selector: 'app-get-index',
  template: `
    <button (click)="findItem()">Find Item Index</button>
    <div>Index: {{ itemIndex }}</div>
    <div id="target">Right click here</div>
    <ejs-contextmenu #cm target='#target' [items]='items'></ejs-contextmenu>
  `
})
export class GetIndexComponent {
  @ViewChild('cm') contextMenu!: ContextMenuComponent;
  itemIndex: any = null;
  
  items: MenuItemModel[] = [
    { text: 'Edit', id: 'edit' },
    {
      text: 'Format',
      id: 'format',
      items: [
        { text: 'Bold', id: 'bold' },
        { text: 'Italic', id: 'italic' }
      ]
    }
  ];
  
  findItem() {
    this.itemIndex = this.contextMenu.getItemIndex('Bold', true);
    console.log('Item index:', this.itemIndex); // [1, 0]
  }
}
```

#### Method: setItem

**Signature:**
```typescript
setItem(item: MenuItem, id?: string, isUniqueId?: boolean): void
```

| Parameter | Type | Optional | Description |
|-----------|------|----------|-------------|
| `item` | `MenuItem` | No | MenuItem object containing updated properties. |
| `id` | `string` | Yes | id or text of the item to be updated. If not provided, updates the item passed as first parameter. |
| `isUniqueId` | `boolean` | Yes, default: `false` | Set `true` if id is a unique id instead of text. |

**Return:** `void`

**Brief Example:**
```typescript
// Update item by text
this.contextMenu.setItem({ text: 'Edit Document' }, 'Edit');

// Update item by id
this.contextMenu.setItem(
  { text: 'Remove', iconCss: 'e-icons e-delete' },
  'delete-item',
  true
);
```

#### Method: open

**Signature:**
```typescript
open(top: number, left: number, target?: HTMLElement): void
```

| Parameter | Type | Optional | Description |
|-----------|------|----------|-------------|
| `top` | `number` | No | To specify ContextMenu vertical positioning (Y coordinate in pixels). |
| `left` | `number` | No | To specify ContextMenu horizontal positioning (X coordinate in pixels). |
| `target` | `HTMLElement` | Yes | To calculate z-index for ContextMenu based upon the specified target element. |

**Return:** `void`

**Brief Example:**
```typescript
// Open at mouse position
this.contextMenu.open(event.clientY, event.clientX);

// Open at specific coordinates
this.contextMenu.open(200, 300);

// Open relative to target element
this.contextMenu.open(100, 150, document.getElementById('target'));
```

#### Method: close

**Signature:**
```typescript
close(): void
```

| Parameter | - | - | - |
|-----------|---|---|---|

**Return:** `void`

**Brief Example:**
```typescript
// Close the open ContextMenu
this.contextMenu.close();
```

#### Method: destroy

**Signature:**
```typescript
destroy(): void
```

| Parameter | - | - | - |
|-----------|---|---|---|

**Return:** `void`

**Brief Example:**
```typescript
// Completely destroy the component and cleanup resources
this.contextMenu.destroy();
```

**Full Working Example - Destroy on Component Destroy:**
```typescript
import { Component, ViewChild, OnDestroy } from '@angular/core';
import { ContextMenuComponent } from '@syncfusion/ej2-angular-navigations';

@Component({
  selector: 'app-destroy-example',
  template: `
    <button (click)="destroyMenu()">Destroy Menu</button>
    <div id="target">Right click here</div>
    <ejs-contextmenu #cm target='#target' [items]='items'></ejs-contextmenu>
  `
})
export class DestroyExampleComponent implements OnDestroy {
  @ViewChild('cm') contextMenu!: ContextMenuComponent;
  items: MenuItemModel[] = [{ text: 'Item 1' }];
  
  destroyMenu() {
    if (this.contextMenu) {
      this.contextMenu.destroy();
      console.log('Menu destroyed');
    }
  }
  
  ngOnDestroy() {
    // Cleanup when component is destroyed
    if (this.contextMenu) {
      this.contextMenu.destroy();
    }
  }
}
```

### Animation Settings (MenuAnimationSettingsModel)

Configure how menu items animate when opening/closing:

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `duration` | `number` | `400` | Specifies the time duration (in milliseconds) to transform/animate the menu. Example: `300` for 300ms animation. |
| `easing` | `string` | `'ease'` | Specifies the easing effect applied while transform. Examples: `'ease'`, `'ease-in'`, `'ease-out'`, `'ease-in-out'`, `'linear'`, `'cubic-bezier(0.25, 0.1, 0.25, 1)'`. |
| `effect` | `MenuEffect` | `'SlideDown'` | Specifies the effect that shown in the sub menu transform. Options: `'None' \| 'SlideDown' \| 'ZoomIn' \| 'FadeIn'`. |

**Effect Options:**
- **None**: Specifies the sub menu transform with no animation effect.
- **SlideDown**: Specifies the sub menu transform with slide down effect (default).
- **ZoomIn**: Specifies the sub menu transform with zoom in effect.
- **FadeIn**: Specifies the sub menu transform with fade in effect.

**Brief Example:**
```typescript
animationSettings = {
  duration: 300,
  effect: 'FadeIn' as any,
  easing: 'ease-out'
};
```

**Full Working Example:**
```typescript
@Component({
  selector: 'app-animation-config',
  template: `
    <div id="target">Right click here</div>
    <ejs-contextmenu 
      target='#target' 
      [items]='items'
      [animationSettings]='animSettings'>
    </ejs-contextmenu>
  `
})
export class AnimationConfigComponent {
  items: MenuItemModel[] = [
    { text: 'Option 1' },
    { text: 'Option 2' }
  ];
  
  animSettings = {
    effect: 'ZoomIn' as any,
    duration: 200,
    easing: 'ease-in-out'
  };
}
```

### Component Events

#### Event: beforeOpen

**Signature:** `(beforeOpen): EmitType<BeforeOpenCloseMenuEventArgs>`

Triggers before opening the menu item. Use this to prevent menu opening, show/hide items based on context, or customize menu before display.

**Event Arguments - BeforeOpenCloseMenuEventArgs:**

| Property | Type | Description |
|----------|------|-------------|
| `name` | `string` | Specifies name of the event (value: `'beforeOpen'`). |

**Brief Example:**
```typescript
onBeforeOpen(args: BeforeOpenCloseMenuEventArgs) {
  console.log('Menu about to open');
}
```

**Full Working Example:**
```typescript
@Component({
  selector: 'app-before-open',
  template: `
    <div id="target">Right click to open</div>
    <ejs-contextmenu 
      target='#target' 
      [items]='items'
      (beforeOpen)='onBeforeOpen($event)'>
    </ejs-contextmenu>
  `
})
export class BeforeOpenComponent {
  items: MenuItemModel[] = [{ text: 'Item 1' }];
  
  onBeforeOpen(args: BeforeOpenCloseMenuEventArgs) {
    console.log('Event:', args.name); // 'beforeOpen'
  }
}
```

#### Event: beforeClose

**Signature:** `(beforeClose): EmitType<BeforeOpenCloseMenuEventArgs>`

Triggers before closing the menu. Use this to perform cleanup or prevent menu from closing.

**Event Arguments - BeforeOpenCloseMenuEventArgs:**

| Property | Type | Description |
|----------|------|-------------|
| `name` | `string` | Specifies name of the event (value: `'beforeClose'`). |

**Brief Example:**
```typescript
onBeforeClose(args: BeforeOpenCloseMenuEventArgs) {
  console.log('Menu about to close');
}
```

#### Event: onOpen

**Signature:** `(onOpen): EmitType<OpenCloseMenuEventArgs>`

Triggers while opening the menu item. This event fires after the menu has been opened and is visible.

**Event Arguments - OpenCloseMenuEventArgs:**

| Property | Type | Description |
|----------|------|-------------|
| `name` | `string` | Specifies name of the event (value: `'onOpen'`). |

**Brief Example:**
```typescript
onOpen(args: OpenCloseMenuEventArgs) {
  console.log('Menu opened:', args.name);
}
```

**Full Working Example:**
```typescript
@Component({
  selector: 'app-open-event',
  template: `
    <div id="target">Right click here</div>
    <ejs-contextmenu 
      target='#target' 
      [items]='items'
      (onOpen)='onOpen($event)'
      (onClose)='onClose($event)'>
    </ejs-contextmenu>
    <p>Status: {{ menuStatus }}</p>
  `
})
export class OpenEventComponent {
  items: MenuItemModel[] = [{ text: 'Item 1' }];
  menuStatus = 'Closed';
  
  onOpen(args: OpenCloseMenuEventArgs) {
    this.menuStatus = 'Menu Opened - ' + args.name;
  }
  
  onClose(args: OpenCloseMenuEventArgs) {
    this.menuStatus = 'Menu Closed - ' + args.name;
  }
}
```

#### Event: onClose

**Signature:** `(onClose): EmitType<OpenCloseMenuEventArgs>`

Triggers while closing the menu. This event fires after the menu has been closed and is no longer visible.

**Event Arguments - OpenCloseMenuEventArgs:**

| Property | Type | Description |
|----------|------|-------------|
| `name` | `string` | Specifies name of the event (value: `'onClose'`). |

**Brief Example:**
```typescript
onClose(args: OpenCloseMenuEventArgs) {
  console.log('Menu closed:', args.name);
}
```

#### Event: select

**Signature:** `(select): EmitType<MenuEventArgs>`

Triggers while selecting menu item. Use this to handle menu item clicks and perform actions.

**Event Arguments - MenuEventArgs:**

| Property | Type | Description |
|----------|------|-------------|
| `name` | `string` | Specifies name of the event (value: `'select'`). |

**Brief Example:**
```typescript
onSelect(args: MenuEventArgs) {
  console.log('Item selected:', args.name);
}
```

**Full Working Example:**
```typescript
@Component({
  selector: 'app-select-event',
  template: `
    <div id="target">Right click here</div>
    <ejs-contextmenu 
      target='#target' 
      [items]='items'
      (select)='onSelect($event)'>
    </ejs-contextmenu>
    <p>Selected: {{ selectedItem }}</p>
  `
})
export class SelectEventComponent {
  items: MenuItemModel[] = [
    { text: 'Edit', id: 'edit' },
    { text: 'Delete', id: 'delete' },
    { text: 'Copy', id: 'copy' }
  ];
  
  selectedItem = 'None';
  
  onSelect(args: MenuEventArgs) {
    this.selectedItem = args.name;
    console.log('Selected item event:', args.name);
  }
}
```

#### Event: beforeItemRender

**Signature:** `(beforeItemRender): EmitType<MenuEventArgs>`

Triggers while rendering each menu item. Use this to customize each item's appearance or behavior before rendering.

**Event Arguments - MenuEventArgs:**

| Property | Type | Description |
|----------|------|-------------|
| `name` | `string` | Specifies name of the event (value: `'beforeItemRender'`). |

**Brief Example:**
```typescript
onBeforeItemRender(args: MenuEventArgs) {
  console.log('Rendering item:', args.name);
}
```

**Full Working Example:**
```typescript
@Component({
  selector: 'app-before-item-render',
  template: `
    <div id="target">Right click here</div>
    <ejs-contextmenu 
      target='#target' 
      [items]='items'
      (beforeItemRender)='onBeforeItemRender($event)'>
    </ejs-contextmenu>
  `
})
export class BeforeItemRenderComponent {
  items: MenuItemModel[] = [
    { text: 'Edit', id: 'edit' },
    { text: 'Delete', id: 'delete' }
  ];
  
  onBeforeItemRender(args: MenuEventArgs) {
    console.log('Rendering:', args.name);
    // Customize items before rendering
  }
}
```

#### Event: created

**Signature:** `(created): EmitType<Event>`

Triggers once the component rendering is completed. Use this for post-initialization setup.

**Event Arguments:**

| Property | Type | Description |
|----------|------|-------------|
| - | `Event` | Standard JavaScript Event object. |

**Brief Example:**
```typescript
onCreated(event: Event) {
  console.log('ContextMenu component created and ready');
}
```

---

## Key Properties & Events Quick Reference

| Property/Event | Purpose | Example |
|---|---|---|
| `items` | Define menu structure | `items: MenuItemModel[]` |
| `target` | Element triggering menu | `target='#target'` |
| `select` | Menu item click | `(select)="onSelect($event)"` |
| `beforeOpen` | Before menu opens | `(beforeOpen)="onBeforeOpen($event)"` |
| `enableItems()` | Toggle item availability | `enableItems(['Edit'], false)` |
| `insertAfter()` | Add items after target | `insertAfter([...], 'Refresh')` |
| `hideItems()` | Hide specific items | `hideItems(['Cut', 'Copy'])` |
| `animationSettings` | Control appearance effects | `animationSettings: {...}` |

## Common Use Cases

1. **File Operations Menu** - Cut, Copy, Paste, Delete options
2. **Content Editor Menu** - Format, Insert, Link, Media options
3. **Data Grid Context** - Edit, Delete, Export, Filter actions
4. **Navigation Menu** - Links to pages or external URLs
5. **Permission-Based Menu** - Show/hide items based on user role
6. **Multi-Language Menu** - Dynamic item text from translations
7. **Confirmation Dialogs** - Open dialog before executing action
8. **Table Operations** - Row/column management in data tables

## Next Steps

1. **Select a reference file** based on your task (Getting Started, Menu Management, Data Binding, Events, Styling, or Templates)
2. **Review the code examples** for your specific use case
3. **Copy relevant code patterns** to your project
4. **Customize menu items** for your application context
5. **Test interactions** with different target elements

---

**Need help with a specific task?** Reference the appropriate guide above and let me know which menu feature you're implementing.
