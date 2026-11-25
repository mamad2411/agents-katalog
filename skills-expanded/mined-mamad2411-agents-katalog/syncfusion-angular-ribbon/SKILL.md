---
name: syncfusion-angular-ribbon
description: Implement the Syncfusion Angular Ribbon component. Use this skill when you need to create Microsoft Office-style ribbon interfaces, organize application commands in tabs and groups, implement file menus or backstage views, or create sophisticated command interfaces. Includes setup, configuration, event handling, layouts, and customization. Use this skill for all Ribbon component implementation needs.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Syncfusion Angular Ribbon Component

## Component Overview

The **Syncfusion Angular Ribbon** is a professional command interface component that organizes application commands in a tabbed ribbon format, similar to Microsoft Office. It features:

- **Hierarchical Command Organization:** Tabs → Groups → Collections → Items for logical command structure
- **7 Built-in Item Types:** Button, CheckBox, DropDown, SplitButton, ComboBox, ColorPicker, GroupButton, and Gallery
- **Dual Layout Modes:** Classic (multi-row) and Simplified (collapsible) layouts with automatic resizing
- **File Menu & Backstage Views:** Traditional file menus or modern backstage interfaces for document operations
- **Contextual Tabs:** Dynamic tabs that appear based on user selection or context
- **Responsive Resizing:** Automatic item size adjustment (Large, Medium, Small) based on available width
- **Keyboard Navigation:** Full keytips support for keyboard-first workflows
- **Accessibility Features:** WCAG compliance with ARIA attributes and screen reader support
- **RTL Support:** Right-to-left layout for Arabic, Hebrew, Persian, and Urdu languages
- **Gallery Items:** Visual selection panels for themes, styles, and color schemes
- **Help Pane:** Customizable help pane with template support
- **Advanced Event System:** Comprehensive events for tab selection, collapse/expand, launcher clicks, and item interactions
- **Highly Configurable:** Extensive API with 20+ ribbon properties, 30+ item properties, and 10+ events

## Key Concepts & Hierarchy

**Important concepts:**
- **Tabs:** Organize major feature categories (Home, Insert, View)
- **Groups:** Group related commands within a tab (Clipboard, Font, Alignment)
- **Collections:** Visual groupings within a group for better organization
- **Items:** Individual commands with 7 types (Button, DropDown, ColorPicker, etc.)
- **Layouts:** Classic (multi-row) or Simplified (collapse-capable) with automatic switching
- **File Menu/Backstage:** Application-level operations (New, Open, Save, Print)

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and package setup (Ivy vs ngcc)
- CSS theme imports and dependencies
- Creating your first Ribbon
- Adding tabs and groups
- Basic items and running the application

### Tabs, Groups, and Items Structure
📄 **Read:** [references/tabs-groups-items.md](references/tabs-groups-items.md)
- Tab hierarchy and properties
- Adding groups to tabs
- Ribbon collections and items
- Item size configuration (Large, Medium, Small)
- Orientation settings (Row/Column)
- Multiple tabs and groups examples

### Item Types and Configuration
📄 **Read:** [references/item-types.md](references/item-types.md)
- All 7 built-in item types
- Button items (toggle, disabled states)
- CheckBox, DropDown, SplitButton items
- ComboBox, ColorPicker, GroupButton items
- Complete code examples for each type
- Item settings models and properties

### Ribbon Layouts and Resizing
📄 **Read:** [references/layouts.md](references/layouts.md)
- Classic layout (default multi-row format)
- Simplified layout (with collapse support)
- Switching between layouts
- Item size allowances and configuration
- Responsive resizing behavior
- Layout examples and best practices

### File Menu and Backstage Views
📄 **Read:** [references/file-menu-and-backstage.md](references/file-menu-and-backstage.md)
- File Menu configuration and visibility
- Adding menu items with icons and actions
- Backstage view as file menu replacement
- Backstage items and content
- Footer items and separators
- Back button customization
- Target element positioning
- Complete file menu and backstage examples

### Advanced Features
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- Contextual tabs (dynamic tab creation)
- Keytips for keyboard navigation
- Gallery items for visual selection
- Help pane templates
- Tooltip configuration
- Resizing behavior and responsive design
- RTL support for right-to-left languages
- Accessibility features and WCAG compliance

### Events and Interactivity
📄 **Read:** [references/events.md](references/events.md)
- Tab selection events (tabSelected, tabSelecting)
- Ribbon collapse/expand events
- Backstage item click events
- Event arguments and cancellation
- Event handling patterns
- Complete event examples

### Customization and Styling
📄 **Read:** [references/customization-and-styling.md](references/customization-and-styling.md)
- CSS class customization
- Theme integration and switching
- CSS variables for styling
- Custom styling examples
- Group icon customization
- Item customization and appearance
- Launcher icon usage

## Quick Start Example

Here's a minimal Ribbon with Home and Insert tabs:

```typescript
import { Component } from "@angular/core";
import { RibbonModule } from '@syncfusion/ej2-angular-ribbon';
import { RibbonButtonSettingsModel, RibbonSplitButtonSettingsModel } from '@syncfusion/ej2-angular-ribbon';

@Component({
  imports: [ RibbonModule ],
  standalone: true,
  selector: "app-root",
  template: `
    <ejs-ribbon id="ribbon">
      <e-ribbon-tabs>
        <e-ribbon-tab header="Home">
          <e-ribbon-groups>
            <e-ribbon-group header="Clipboard" orientation="Row">
              <e-ribbon-collections>
                <e-ribbon-collection>
                  <e-ribbon-items>
                    <e-ribbon-item type="SplitButton" [splitButtonSettings]="pasteSettings"></e-ribbon-item>
                  </e-ribbon-items>
                </e-ribbon-collection>
                <e-ribbon-collection>
                  <e-ribbon-items>
                    <e-ribbon-item type="Button" [buttonSettings]="cutButton"></e-ribbon-item>
                    <e-ribbon-item type="Button" [buttonSettings]="copyButton"></e-ribbon-item>
                  </e-ribbon-items>
                </e-ribbon-collection>
              </e-ribbon-collections>
            </e-ribbon-group>
          </e-ribbon-groups>
        </e-ribbon-tab>
        <e-ribbon-tab header="Insert">
          <e-ribbon-groups>
            <e-ribbon-group header="Illustrations" orientation="Row">
              <e-ribbon-collections>
                <e-ribbon-collection>
                  <e-ribbon-items>
                    <e-ribbon-item type="Button" [buttonSettings]="chartButton"></e-ribbon-item>
                  </e-ribbon-items>
                </e-ribbon-collection>
              </e-ribbon-collections>
            </e-ribbon-group>
          </e-ribbon-groups>
        </e-ribbon-tab>
      </e-ribbon-tabs>
    </ejs-ribbon>
  `,
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  public pasteSettings = { 
    iconCss: "e-icons e-paste", 
    items: [{ text: "Keep Source Format" }, { text: "Merge format" }], 
    content: "Paste" 
  };
  public cutButton: RibbonButtonSettingsModel = { iconCss: "e-icons e-cut", content: "Cut" };
  public copyButton: RibbonButtonSettingsModel = { iconCss: "e-icons e-copy", content: "Copy" };
  public chartButton: RibbonButtonSettingsModel = { iconCss: "e-icons e-chart", content: "Chart" };
}
```

---

## Common Patterns

### Pattern 1: Multi-Tab Command Interface
1. Define multiple tabs for major features (Home, Insert, View, Format)
2. Add groups within each tab for related commands
3. Configure collections to organize items visually
4. Use appropriate item types (Button, DropDown, ColorPicker)
5. Set `activeLayout` to Classic or Simplified
6. Handle `tabSelected` event for tab-specific actions

### Pattern 2: File Menu Integration with Backstage
1. Configure `fileMenu` or `backStageMenu` for document operations
2. Add menu items for New, Open, Save, Print, Export
3. Set icons with `iconCss` and content areas for backstage
4. Handle menu item clicks with event handlers
5. Use footer items for settings or account options
6. Configure back button for backstage navigation

### Pattern 3: Responsive Resizing with Size Priorities
1. Set `allowedSizes` array on items (Large, Medium, Small)
2. Configure `activeSize` for initial display size
3. Ribbon automatically adjusts item sizes based on width
4. Use `Large` for primary commands, `Small` for secondary
5. Handle `ribbonCollapsing` event for custom resize logic
6. Test responsive behavior at different viewport widths

### Pattern 4: Contextual Tabs for Dynamic Commands
1. Define `contextualTabs` array with tab configurations
2. Set `visible` property based on user selection or context
3. Use `isSelected` to activate contextual tab programmatically
4. Add tab-specific groups and items for contextual commands
5. Handle `tabSelected` to detect contextual tab activation
6. Toggle visibility dynamically in response to user actions

### Pattern 5: Keyboard Navigation with Keytips
1. Enable `enableKeyTips` on ribbon component
2. Assign `keyTip` property to tabs (Alt+H for Home)
3. Add keytips to groups and individual items
4. Configure `layoutSwitcherKeyTip` for layout toggle
5. Set keytips on file menu and backstage items
6. Follow consistent keytip patterns (Alt+ letter combinations)

### Pattern 6: Gallery Items for Visual Selection
1. Configure items with `type="Gallery"` for visual panels
2. Define `gallerySettings` with groups and items
3. Set `itemCount`, `popupWidth`, `popupHeight` for display
4. Use templates for custom gallery item rendering
5. Handle selection events for gallery item clicks
6. Common use cases: themes, styles, colors, table designs

---

## Key Properties & Events

### Core Ribbon Configuration
| Property | Type | Default | When to Use |
|----------|------|---------|------------|
| `tabs` | RibbonTabModel[] | `[]` | Define ribbon tabs with groups and items |
| `activeLayout` | LayoutType | `'Classic'` | Set layout mode (Classic or Simplified) |
| `selectedTab` | number | `0` | Set or get the currently active tab index |
| `isMinimized` | boolean | `false` | Control ribbon minimized state |

### Layout & Appearance
| Property | Type | Default | When to Use |
|----------|------|---------|------------|
| `width` | string \| number | `'100%'` | Set ribbon container width |
| `cssClass` | string | `''` | Apply custom CSS classes for styling and themes |
| `hideLayoutSwitcher` | boolean | `false` | Hide the Classic/Simplified layout toggle button |
| `tabAnimation` | object | `null` | Configure tab switching animation settings |

### Keyboard & Accessibility
| Property | Type | Default | When to Use |
|----------|------|---------|------------|
| `enableKeyTips` | boolean | `false` | Enable keytips for keyboard navigation (Alt+ shortcuts) |
| `layoutSwitcherKeyTip` | string | `''` | Set keytip for layout switcher button |
| `launcherIconCss` | string | `''` | Default CSS class for launcher icons across all groups |

### File Menu & Backstage
| Property | Type | Default | When to Use |
|----------|------|---------|------------|
| `fileMenu` | FileMenuSettingsModel | `null` | Configure traditional file menu (New, Open, Save, Print) |
| `backStageMenu` | BackStageMenuModel | `null` | Configure modern backstage view (replaces file menu) |

### Advanced Features
| Property | Type | Default | When to Use |
|----------|------|---------|------------|
| `contextualTabs` | RibbonContextualTabModel[] | `[]` | Define tabs that appear based on context or selection |
| `helpPaneTemplate` | string | `''` | Custom template for help pane content |

### Globalization
| Property | Type | Default | When to Use |
|----------|------|---------|------------|
| `locale` | string | `'en-US'` | Set language/culture for localization |
| `enableRtl` | boolean | `false` | Enable right-to-left layout (Arabic, Hebrew, Persian, Urdu) |
| `enablePersistence` | boolean | `false` | Save ribbon state between page reloads |

### Tab Configuration
| Property | Type | Default | When to Use |
|----------|------|---------|------------|
| `header` | string | `''` | Tab display text (Home, Insert, View) |
| `groups` | RibbonGroupModel[] | `[]` | Array of groups within the tab |
| `id` | string | `''` | Unique identifier for the tab |
| `keyTip` | string | `''` | Keyboard shortcut keytip (H for Home) |

### Group Configuration
| Property | Type | Default | When to Use |
|----------|------|---------|------------|
| `header` | string | `''` | Group display text (Clipboard, Font, Alignment) |
| `orientation` | ItemOrientation | `'Column'` | Layout direction (Row or Column) |
| `enableGroupOverflow` | boolean | `false` | Show overflow dropdown when group doesn't fit |
| `isCollapsible` | boolean | `true` | Allow group to collapse in simplified layout |
| `showLauncherIcon` | boolean | `false` | Show launcher icon for dialog/pane launch |
| `groupIconCss` | string | `''` | CSS class for group icon in overflow/launcher |

### Item Configuration
| Property | Type | Default | When to Use |
|----------|------|---------|------------|
| `type` | RibbonItemType | `'Button'` | Item type: Button, CheckBox, DropDown, SplitButton, ComboBox, ColorPicker, GroupButton, Gallery |
| `id` | string | `''` | Unique identifier for the item |
| `allowedSizes` | RibbonItemSize[] | `['Large', 'Medium', 'Small']` | Sizes item can resize to (responsive behavior) |
| `activeSize` | RibbonItemSize | `'Medium'` | Current display size of item |
| `disabled` | boolean | `false` | Disable item to prevent user interaction |
| `displayOptions` | DisplayMode | `'Auto'` | Control display (Auto, Classic, Simplified, Overflow) |
| `cssClass` | string | `''` | Custom CSS class for item styling |
| `keyTip` | string | `''` | Keyboard shortcut keytip for item |
| `ribbonTooltipSettings` | TooltipSettingsModel | `null` | Tooltip configuration (id, title, content, iconCss, cssClass) |
| `itemTemplate` | string | `''` | Custom template for item rendering |
| `buttonSettings` | RibbonButtonSettingsModel | `null` | Button-specific settings (iconCss, content, clicked) |
| `dropDownSettings` | RibbonDropDownSettingsModel | `null` | DropDown-specific settings (iconCss, content, items) |
| `splitButtonSettings` | RibbonSplitButtonSettingsModel | `null` | SplitButton-specific settings (iconCss, items, clicked) |
| `checkBoxSettings` | RibbonCheckBoxSettingsModel | `null` | CheckBox-specific settings (label, checked, change) |
| `colorPickerSettings` | RibbonColorPickerSettingsModel | `null` | ColorPicker-specific settings (value, change) |
| `comboBoxSettings` | RibbonComboBoxSettingsModel | `null` | ComboBox-specific settings (dataSource, value, fields) |
| `groupButtonSettings` | RibbonGroupButtonSettingsModel | `null` | GroupButton-specific settings (items, selected) |
| `gallerySettings` | RibbonGallerySettingsModel | `null` | Gallery configuration (groups, items, itemCount, popupWidth, popupHeight, template) |

### File Menu Configuration
| Property | Type | Default | When to Use |
|----------|------|---------|------------|
| `visible` | boolean | `false` | Show/hide file menu button |
| `text` | string | `'File'` | File menu button text |
| `menuItems` | FileMenuItemModel[] | `[]` | Array of menu items (New, Open, Save, Print) |
| `itemTemplate` | string | `''` | Custom template for menu items |
| `popupTemplate` | string | `''` | Custom template for entire popup |
| `keyTip` | string | `''` | Keytip for file menu (F for File) |
| `ribbonTooltipSettings` | TooltipSettingsModel | `null` | Tooltip settings for file menu button |

### Backstage Configuration
| Property | Type | Default | When to Use |
|----------|------|---------|------------|
| `visible` | boolean | `false` | Show/hide backstage view |
| `text` | string | `'File'` | Backstage button text |
| `items` | BackStageItemModel[] | `[]` | Backstage items (id, text, iconCss, content, separator, isFooter) |
| `backButton` | BackButtonModel | `null` | Back button configuration (text, iconCss, visible) |
| `width` | string | `'auto'` | Backstage width dimension |
| `height` | string | `'auto'` | Backstage height dimension |
| `target` | HTMLElement | `null` | Element for positioning backstage |
| `template` | string | `''` | Custom template for backstage content |
| `keyTip` | string | `''` | Keytip for backstage button |
| `ribbonTooltipSettings` | TooltipSettingsModel | `null` | Tooltip settings for backstage button |

### Contextual Tab Configuration
| Property | Type | Default | When to Use |
|----------|------|---------|------------|
| `visible` | boolean | `false` | Show/hide contextual tab group |
| `isSelected` | boolean | `false` | Whether contextual tab is active |
| `tabs` | RibbonTabModel[] | `[]` | Array of tabs in contextual group |

### Key Events
| Event | Arguments | When to Use |
|-------|-----------|------------|
| `(tabSelected)` | TabSelectedEventArgs | After a tab is selected (get tab index and data) |
| `(tabSelecting)` | TabSelectingEventArgs | Before tab selection (cancelable, validate selection) |
| `(ribbonCollapsing)` | RibbonCollapsingEventArgs | Before ribbon collapses (cancelable) |
| `(ribbonExpanded)` | RibbonExpandedEventArgs | After ribbon expands |
| `(launcherClick)` | LauncherClickEventArgs | When launcher icon is clicked (open dialog/pane) |
| `(overflowPopupOpen)` | OverflowPopupEventArgs | Before overflow popup opens (cancelable) |
| `(overflowPopupClose)` | OverflowPopupEventArgs | Before overflow popup closes (cancelable) |
| `(layoutSwitched)` | LayoutSwitchedEventArgs | When layout switches between Classic/Simplified |
| `(backStageItemClick)` | BackStageItemClickEventArgs | When backstage item is clicked |

### File Menu Events
| Event | Arguments | When to Use |
|-------|-----------|------------|
| `beforeOpen` | BeforeOpenCloseMenuEventArgs | Before file menu opens (cancelable) |
| `open` | OpenCloseMenuEventArgs | After file menu opens |
| `beforeClose` | BeforeOpenCloseMenuEventArgs | Before file menu closes (cancelable) |
| `close` | OpenCloseMenuEventArgs | After file menu closes |
| `beforeItemRender` | MenuEventArgs | Before menu item renders (customize rendering) |
| `select` | MenuEventArgs | When menu item is selected |

---
