---
name: syncfusion-aspnetcore-ribbon
description: Implement the Syncfusion ASP.NET Core Ribbon control using Razor Tag Helpers. Use this skill when the user mentions Syncfusion ASP.NET Core Ribbon, `<ejs-ribbon>`, `<e-ribbon-tab>`, `<e-ribbon-group>`, Razor Tag Helpers, ribbon implementation, tabs, groups, items, file menu, backstage, layouts, events, or ASP.NET Core ribbon setup. Covers installation, tag helper registration, component structure, items, events, theming, accessibility, and advanced patterns.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Syncfusion ASP.NET Core Ribbon Control

## Overview

A comprehensive skill for implementing the Syncfusion EJ2 Ribbon component in ASP.NET Core applications using Razor Tag Helpers. This skill covers installation, setup, component structure, all item types, events, theming, and advanced features. The Ribbon component is a feature-rich navigation control that:

- **Organizes commands in tabs and groups** - Tabbed interface with logical grouping
- **Supports 7 item types** - Button, CheckBox, DropDown, SplitButton, ComboBox, ColorPicker, GroupButton
- **Provides file menu & backstage** - Traditional file menu or modern backstage view
- **Contextual tabs on demand** - Tabs appear when needed (e.g., on image/table selection)
- **Gallery items** - Visual selection of styles, templates, or options
- **Responsive layouts** - Classic (multi-row) and Simplified (compact) modes
- **Keyboard navigation** - KeyTips for Alt+key shortcuts
- **WCAG 2.1 compliant** - Full accessibility support with ARIA
- **Built-in themes** - Material, Bootstrap, Fluent, Tailwind, Fabric

## Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- NuGet package installation
- Tag Helper registration in _ViewImports.cshtml
- CSS and script setup in _Layout.cshtml
- First working example with complete setup
- Available themes (Material, Bootstrap, Fluent, Tailwind, Fabric)
- Advanced feature registration (no separate module injection needed in ASP.NET Core)
- Localization with `locale` property
- State persistence with `enablePersistence`

### Ribbon Structure
📄 **Read:** [references/ribbon-structure.md](references/ribbon-structure.md)
- Component hierarchy (Ribbon → Tab → Group → Collection → Item)
- Adding tabs with `<e-ribbon-tab>`
- Adding groups with `<e-ribbon-group>`
- Adding collections and items
- Organizing ribbon content
- Best practices for structure

### Items & Groups Configuration
📄 **Read:** [references/items-and-groups.md](references/items-and-groups.md)
- All 7 item types (Button, CheckBox, DropDown, SplitButton, ComboBox, ColorPicker, GroupButton, Template)
- Exact `RibbonXxxSettings` configuration for each type
- Group properties (header, collapsibility, priority, overflow)
- Item sizing (Large, Medium, Small)
- Display options (Auto, Classic, Simplified, Overflow)
- Disabled states

### Tabs & Groups Management
📄 **Read:** [references/tabs-and-groups.md](references/tabs-and-groups.md)
- Tab management patterns
- Multi-tab setup examples
- Group organization
- Collapsibility control (`isCollapsible`)
- Priority handling (higher = collapses first)
- Launcher icons
- Group overflow behavior

### Layouts & Display Modes
📄 **Read:** [references/layouts-display-modes.md](references/layouts-display-modes.md)
- Classic layout (default, multi-row)
- Simplified layout (compact, single-row)
- Layout switching
- Responsive resizing behavior
- Item sizing progression (Large → Medium → Small)
- Minimized state
- Hide layout switcher option

### File Menu & Backstage
📄 **Read:** [references/file-menu-backstage.md](references/file-menu-backstage.md)
- File menu basics (`<e-ribbon-filemenusettings>`)
- Menu item configuration with `MenuItem` list
- Backstage view (`<e-ribbon-backstagemenusettings>`)
- Backstage items with content
- Footer items and separators
- Back button customization

### Contextual Tabs & Gallery
📄 **Read:** [references/contextual-tabs-gallery.md](references/contextual-tabs-gallery.md)
- Contextual tabs on demand
- Visibility control with conditions
- Gallery items (`type=Gallery`)
- Gallery groups with headers
- Gallery item properties (content, iconCss, disabled)
- Visual selection patterns

### Events & Accessibility
📄 **Read:** [references/events-accessibility.md](references/events-accessibility.md)
- Ribbon events (tabSelected, tabSelecting, itemClick, etc.)
- KeyTips configuration (`enableKeyTips`, `keyTip` property)
- Keyboard navigation
- WCAG 2.1 compliance
- ARIA attributes support
- RTL support (`enableRtl`)

### Customization & Theming
📄 **Read:** [references/customization-theming.md](references/customization-theming.md)
- Built-in themes table (5 themes)
- Theme CSS import paths
- Theme switching implementation
- CSS customization classes
- Dark mode support
- Custom icons and styling

### Tooltips & Help
📄 **Read:** [references/tooltips-help-pane.md](references/tooltips-help-pane.md)
- Item tooltips with `RibbonTooltipSettings`
- Title and content properties
- Custom tooltip HTML
- Help pane component patterns
- Contextual help implementation

### Methods & Properties
📄 **Read:** [references/methods-and-properties.md](references/methods-and-properties.md)
- Ribbon methods (getComponent, destroy)
- Key events and callbacks
- Property access patterns
- Programmatic control
- State management

### Troubleshooting
📄 **Read:** [references/troubleshooting.md](references/troubleshooting.md)
- Common issues and solutions
- Tag helper registration problems
- Data binding issues
- Event handling troubleshooting
- Performance optimization
- Styling problems
- ASP.NET Core-specific gotchas

## Key Properties & Events

**Essential Properties:**
- `id` - Unique identifier for the ribbon
- `activeLayout` - Set to `Classic` or `Simplified`
- `isMinimized` - Collapse/expand the ribbon (true/false)
- `enableKeyTips` - Enable keyboard shortcuts (true/false)
- `enableRtl` - Right-to-left support (true/false)
- `hideLayoutSwitcher` - Hide layout switcher button (true/false)
- `layoutSwitcherKeyTip` - KeyTip character for the layout switcher button
- `helpPaneTemplate` - CSS selector or HTML string for the right-side help pane
- `enablePersistence` - Persist ribbon state across page reloads (true/false)
- `locale` - Locale string for built-in UI text (e.g., `"en-us"`, `"fr-FR"`)

**Key Events:**
- `created` - Triggered after component creation
- `tabSelected` - Triggered after tab selection (`args.selectedIndex`, `args.previousIndex`, `args.isContextual`)
- `tabSelecting` - Triggered before tab selection (`args.cancel` to prevent, `args.isInteracted`)
- `ribbonCollapsing` - Triggered before ribbon collapses (`args.cancel` to prevent)
- `ribbonExpanding` - Triggered before ribbon expands (`args.cancel` to prevent)
- `ribbonLayoutSwitched` - Triggered after layout switch (`args.activeLayout`)
- `launcherIconClick` - Triggered when a group launcher icon is clicked (`args.groupId`)
- `overflowPopupOpen` - Triggered when overflow popup opens (`args.element`, `args.cancel`)
- `overflowPopupClose` - Triggered when overflow popup closes (`args.element`, `args.cancel`)

## Quick Start

### Basic Ribbon with Tabs & Groups

```razor
@using Syncfusion.EJ2
@using Syncfusion.EJ2.Ribbon
@using Syncfusion.EJ2.Navigations

<ejs-ribbon id="ribbon">
    <e-ribbon-tabs>
        <e-ribbon-tab header="Home">
            <e-ribbon-groups>
                <e-ribbon-group header="Clipboard">
                    <e-ribbon-collections>
                        <e-ribbon-collection>
                            <e-ribbon-items>
                                <e-ribbon-item type=Button>
                                    <e-ribbon-buttonsettings iconCss="e-icons e-paste" content="Paste"></e-ribbon-buttonsettings>
                                </e-ribbon-item>
                            </e-ribbon-items>
                        </e-ribbon-collection>
                    </e-ribbon-collections>
                </e-ribbon-group>
            </e-ribbon-groups>
        </e-ribbon-tab>
        <e-ribbon-tab header="Insert">
            <e-ribbon-groups>
                <e-ribbon-group header="Tables">
                    <e-ribbon-collections>
                        <e-ribbon-collection>
                            <e-ribbon-items>
                                <e-ribbon-item type=Button>
                                    <e-ribbon-buttonsettings iconCss="e-icons e-table" content="Table"></e-ribbon-buttonsettings>
                                </e-ribbon-item>
                            </e-ribbon-items>
                        </e-ribbon-collection>
                    </e-ribbon-collections>
                </e-ribbon-group>
            </e-ribbon-groups>
        </e-ribbon-tab>
    </e-ribbon-tabs>
</ejs-ribbon>
```

### With File Menu

```razor
@{
    List<MenuItem> fileOptions = new List<MenuItem>() {
        new MenuItem { Text = "New", IconCss = "e-icons e-file-new" },
        new MenuItem { Text = "Open", IconCss = "e-icons e-folder-open" },
        new MenuItem { Text = "Save", IconCss = "e-icons e-save" }
    };
}

<ejs-ribbon id="ribbon">
    <e-ribbon-filemenusettings visible="true" menuItems=fileOptions></e-ribbon-filemenusettings>
    <e-ribbon-tabs>
        <!-- tabs -->
    </e-ribbon-tabs>
</ejs-ribbon>
```

## Common Patterns

### Pattern: Multi-Tab Ribbon with Multiple Groups

```razor
<ejs-ribbon id="ribbon">
    <e-ribbon-tabs>
        <e-ribbon-tab header="Home">
            <e-ribbon-groups>
                <e-ribbon-group header="Clipboard" orientation=Row>
                    <!-- Items -->
                </e-ribbon-group>
                <e-ribbon-group header="Font" orientation=Row enableGroupOverflow=true>
                    <!-- Items -->
                </e-ribbon-group>
            </e-ribbon-groups>
        </e-ribbon-tab>
        <e-ribbon-tab header="View">
            <e-ribbon-groups>
                <e-ribbon-group header="Views" orientation=Row>
                    <!-- Items -->
                </e-ribbon-group>
            </e-ribbon-groups>
        </e-ribbon-tab>
    </e-ribbon-tabs>
</ejs-ribbon>
```

### Pattern: Multiple Item Types in Groups

```razor
@{
    List<string> fontOptions = new List<string>() { "Arial", "Calibri", "Cambria", "Georgia" };
}

<e-ribbon-group header="Formatting">
    <e-ribbon-collections>
        <e-ribbon-collection>
            <e-ribbon-items>
                <!-- ComboBox -->
                <e-ribbon-item type=ComboBox>
                    <e-ribbon-comboboxsettings dataSource=fontOptions index=0 width="120px"></e-ribbon-comboboxsettings>
                </e-ribbon-item>
                <!-- ColorPicker -->
                <e-ribbon-item type=ColorPicker allowedSizes=Small>
                    <e-ribbon-colorpickersettings value="#123456"></e-ribbon-colorpickersettings>
                </e-ribbon-item>
                <!-- Toggle Button -->
                <e-ribbon-item type=Button allowedSizes=Small>
                    <e-ribbon-buttonsettings iconCss="e-icons e-bold" isToggle=true></e-ribbon-buttonsettings>
                </e-ribbon-item>
            </e-ribbon-items>
        </e-ribbon-collection>
    </e-ribbon-collections>
</e-ribbon-group>
```

### Pattern: Event Handling

```razor
<ejs-ribbon id="ribbon"
    tabSelected="onTabSelected"
    tabSelecting="onTabSelecting"
    ribbonLayoutSwitched="onLayoutSwitched"
    launcherIconClick="onLauncherClick">
    <!-- ribbon content -->
</ejs-ribbon>

<script>
    function onTabSelected(args) {
        console.log('Tab selected:', args.selectedIndex);
        console.log('Previous tab:', args.previousIndex);
        console.log('Is contextual:', args.isContextual);
    }

    function onTabSelecting(args) {
        console.log('Tab selecting:', args.selectedIndex);
        // args.cancel = true; // Prevent selection if needed
    }

    function onLayoutSwitched(args) {
        console.log('Layout changed to:', args.activeLayout); // 'Classic' or 'Simplified'
    }

    function onLauncherClick(args) {
        console.log('Launcher clicked for group:', args.groupId);
    }
</script>
```

## Workflow Pattern

When a user needs Ribbon functionality:

1. **Identify scope**: Tab organization, item types, file menu, events needed
2. **Start with Getting Started**: Installation and basic setup
3. **Choose references** based on features:
   - Items configuration → items-and-groups.md
   - Layout/responsive → layouts-display-modes.md
   - File menu → file-menu-backstage.md
   - Keyboard/accessibility → events-accessibility.md
   - Look & feel → customization-theming.md
4. **Implement patterns** following copy-paste examples
5. **Debug issues** → troubleshooting.md

---
