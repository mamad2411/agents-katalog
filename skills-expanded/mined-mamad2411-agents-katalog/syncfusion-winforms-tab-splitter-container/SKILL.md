---
name: syncfusion-winforms-tab-splitter-container
description: Implement Syncfusion TabSplitterContainer control for creating split-view layouts with tabbed panels in Windows Forms. Use when building Visual Studio-style split views, document editors with design/preview modes, or multi-pane applications. Covers primary/secondary page collections, swap button functionality, collapse/expand panes, horizontal/vertical orientation, adjustable splitter position, and Office2016 themes for professional multi-view interfaces.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Syncfusion WinForms TabSplitterContainer

The **TabSplitterContainer** control provides a Visual Studio 2008-style tabbed split view of tab groups, enabling users to easily render different views of the same document. This control is ideal for creating code editors with preview panes, design/code split views, or any multi-view document interface.

## When to Use This Skill

Use this skill when the user needs to:

- **Split View Editors:** Code editor with XAML/Design split view (like Visual Studio)
- **Document Multi-View:** Display same document in different modes (edit vs preview)
- **Tabbed Splitter Layouts:** Multiple tab groups that can be swapped or repositioned
- **Collapsible Panes:** Split view with collapsible secondary pane
- **VS-Style Interfaces:** Visual Studio 2008-style multi-pane editors
- **Adjustable Split Position:** User can drag splitter bar to resize panes
- **Multi-Pane Applications:** Applications requiring primary and secondary tab groups
- **Horizontal/Vertical Splits:** Support both horizontal and vertical layout orientations

## Component Overview

**TabSplitterContainer** (`Syncfusion.Windows.Forms.Tools.TabSplitterContainer`) is a versatile split-view layout control supporting:

- **Primary and Secondary Pages:** Two collections of tabbed pages (PrimaryPages, SecondaryPages)
- **Swap Functionality:** Built-in swap button to exchange primary/secondary tab groups
- **Collapse/Expand:** Built-in collapse button to hide/show secondary pane
- **Dual Orientation:** Horizontal (side-by-side) or Vertical (top-bottom) layouts
- **Adjustable Splitter:** Draggable splitter bar with SplitterPosition property
- **Office2016 Themes:** Colorful, White, DarkGray, Black theme support
- **TabSplitterPage:** Customizable pages with images, tooltips, border styles
- **Splitter Components:** Swap button, collapse/expand buttons, orientation toggles
- **Design-Time Support:** Visual designer integration with smart tags

**Key Namespace:** `Syncfusion.Windows.Forms.Tools`

**Assembly:** `Syncfusion.Tools.Windows.dll` (and dependencies)

---

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)

**When to read:** User needs to install, configure, or create their first TabSplitterContainer.

**Topics covered:**
- Assembly deployment and NuGet package installation
- Adding TabSplitterContainer via designer (toolbox + smart tags)
- Adding TabSplitterContainer via code
- Creating and adding TabSplitterPage instances
- PrimaryPages and SecondaryPages collections
- Basic tab page setup and configuration
- Adding controls to tab pages

### Splitter Components and Pages
📄 **Read:** [references/splitter-components.md](references/splitter-components.md)

**When to read:** User wants to understand swap button, collapse/expand functionality, or customize TabSplitterPage properties.

**Topics covered:**
- Splitter component overview (swap, collapse/expand buttons)
- Primary page collection (PrimaryPages property)
- Secondary page collection (SecondaryPages property)
- Swap button functionality (Swapped property)
- Collapse/Expand functionality (Collapsed property)
- TabSplitterPage customization (Text, Image, Tooltip)
- Page properties (BorderStyle, BackgroundImage, Visible)
- Runtime page manipulation and visibility

### Orientation and Splitter Position
📄 **Read:** [references/orientation-and-position.md](references/orientation-and-position.md)

**When to read:** User needs horizontal/vertical layout or wants to adjust splitter position.

**Topics covered:**
- Horizontal orientation (default, side-by-side layout)
- Vertical orientation (top-bottom layout)
- Orientation property configuration
- SplitterPosition property for programmatic control
- Design-time splitter adjustment
- Runtime splitter position changes
- Layout considerations for different orientations

### Styling and Appearance
📄 **Read:** [references/styling-and-appearance.md](references/styling-and-appearance.md)

**When to read:** User wants Office2016 themes or custom splitter appearance.

**Topics covered:**
- Visual styles overview (Default, Office2016 variants)
- Office2016Colorful, Office2016White, Office2016DarkGray, Office2016Black
- Style property usage
- Customizable splitter back color (SplitterBackColor)
- Theme consistency with application
- Visual appearance customization

### Advanced Features
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)

**When to read:** User needs events, localization, or runtime page management.

**Topics covered:**
- TabSplitterContainer events
- Localization support and CultureInfo
- Runtime manipulation (swap, collapse, expand programmatically)
- Page visibility control
- Dynamic page management (add/remove at runtime)
- Best practices and troubleshooting
- Performance considerations

---

## Quick Start Example

### Basic XAML/Design Split View

```csharp
using Syncfusion.Windows.Forms.Tools;

// Create TabSplitterContainer
TabSplitterContainer splitterContainer = new TabSplitterContainer();
splitterContainer.Dock = DockStyle.Fill;

// Create primary page (XAML view)
TabSplitterPage xamlPage = new TabSplitterPage();
xamlPage.Text = "XAML";
xamlPage.BackColor = Color.White;

// Create secondary page (Design view)
TabSplitterPage designPage = new TabSplitterPage();
designPage.Text = "Design";
designPage.BackColor = Color.White;

// Add pages to collections
splitterContainer.PrimaryPages.Add(xamlPage);
splitterContainer.SecondaryPages.Add(designPage);

// Add to form
this.Controls.Add(splitterContainer);
```

### Vertical Split with Office2016 Theme

```csharp
// Configure vertical orientation
splitterContainer.Orientation = Orientation.Vertical;

// Apply Office2016 Colorful theme
splitterContainer.Style = TabSplitterContainerStyle.Office2016Colorful;

// Set initial splitter position (50% split)
splitterContainer.SplitterPosition = splitterContainer.Height / 2;
```

---

## Common Patterns

### Code Editor with Preview Pane

```csharp
// Primary: Code editor
TabSplitterPage codePage = new TabSplitterPage();
codePage.Text = "Code";
TextBox codeEditor = new TextBox { Dock = DockStyle.Fill, Multiline = true };
codePage.Controls.Add(codeEditor);

// Secondary: Preview pane
TabSplitterPage previewPage = new TabSplitterPage();
previewPage.Text = "Preview";
WebBrowser previewBrowser = new WebBrowser { Dock = DockStyle.Fill };
previewPage.Controls.Add(previewBrowser);

// Add to splitter
tabSplitterContainer1.PrimaryPages.Add(codePage);
tabSplitterContainer1.SecondaryPages.Add(previewPage);
```

**When to use:** Markdown editors, HTML editors, any code with live preview.

### Multi-Tab Groups (VS-Style)

```csharp
// Primary group: Multiple document tabs
TabSplitterPage doc1 = new TabSplitterPage { Text = "Document1.cs" };
TabSplitterPage doc2 = new TabSplitterPage { Text = "Document2.cs" };
tabSplitterContainer1.PrimaryPages.AddRange(new[] { doc1, doc2 });

// Secondary group: Properties/Output tabs
TabSplitterPage propPage = new TabSplitterPage { Text = "Properties" };
TabSplitterPage outputPage = new TabSplitterPage { Text = "Output" };
tabSplitterContainer1.SecondaryPages.AddRange(new[] { propPage, outputPage });
```

**When to use:** IDE-style interfaces, multi-document editors.

### Collapsible Secondary Pane

```csharp
// Start with secondary pane collapsed
tabSplitterContainer1.Collapsed = true;

// Toggle collapse on button click
btnToggle.Click += (s, e) => {
    tabSplitterContainer1.Collapsed = !tabSplitterContainer1.Collapsed;
};
```

**When to use:** Optional preview panes, collapsible sidebars.

### Swap Tab Groups Programmatically

```csharp
// Swap primary and secondary tab groups
tabSplitterContainer1.Swapped = true;

// Toggle swap on button click
btnSwap.Click += (s, e) => {
    tabSplitterContainer1.Swapped = !tabSplitterContainer1.Swapped;
};
```

**When to use:** User preference for tab group positioning.

---

## Key Properties

### Core Properties

| Property | Type | Description | When to Use |
|----------|------|-------------|-------------|
| **PrimaryPages** | `TabSplitterPageCollection` | Collection of primary tab pages | Add/manage primary pane tabs |
| **SecondaryPages** | `TabSplitterPageCollection` | Collection of secondary tab pages | Add/manage secondary pane tabs |
| **Orientation** | `Orientation` | Horizontal or Vertical split | Change layout direction |
| **SplitterPosition** | `int` | Position of splitter bar (pixels) | Set initial or runtime split position |
| **Collapsed** | `bool` | Collapse/expand secondary pane | Show/hide secondary pane |
| **Swapped** | `bool` | Swap primary/secondary tab groups | Exchange tab group positions |

### Styling Properties

| Property | Type | Description | When to Use |
|----------|------|-------------|-------------|
| **Style** | `TabSplitterContainerStyle` | Visual style (Default, Office2016*) | Apply Office2016 themes |
| **SplitterBackColor** | `Color` | Splitter bar background color | Custom splitter appearance |

### TabSplitterPage Properties

| Property | Type | Description | When to Use |
|----------|------|-------------|-------------|
| **Text** | `string` | Tab page text/caption | Set tab label |
| **Image** | `Image` | Tab page icon | Add icon to tab |
| **ToolTip** | `string` | Tab tooltip text | Provide hover information |
| **BorderStyle** | `BorderStyle` | Page border style | Add/remove page borders |
| **BackgroundImage** | `Image` | Page background image | Custom page background |
| **Visible** | `bool` | Page visibility | Show/hide specific pages |

---

## Common Use Cases

### 1. Code Editor with Split View
**Scenario:** Markdown editor with edit/preview split view.
- Create primary page with TextBox for editing
- Create secondary page with WebBrowser for preview
- Use Orientation.Horizontal for side-by-side
- Enable Collapsed to allow hiding preview
- Read: [getting-started.md](references/getting-started.md), [orientation-and-position.md](references/orientation-and-position.md)

### 2. Visual Studio-Style Document Editor
**Scenario:** Multi-document IDE with tab groups.
- Add multiple TabSplitterPages to PrimaryPages (document tabs)
- Add tool/output pages to SecondaryPages
- Use Office2016 theme for professional appearance
- Enable swap button for user preference
- Read: [splitter-components.md](references/splitter-components.md), [styling-and-appearance.md](references/styling-and-appearance.md)

### 3. Document Viewer with Thumbnails
**Scenario:** PDF viewer with thumbnail sidebar.
- Primary page: Main document viewer
- Secondary page: Thumbnail panel
- Use Orientation.Vertical for top-bottom layout
- Set SplitterPosition to allocate more space to main view
- Allow collapse for full-screen document view
- Read: [orientation-and-position.md](references/orientation-and-position.md), [splitter-components.md](references/splitter-components.md)

### 4. Data Entry Form with Help Pane
**Scenario:** Form with contextual help in secondary pane.
- Primary page: Data entry form
- Secondary page: Help/documentation panel
- Start with Collapsed = true (hide by default)
- Add toggle button to show/hide help
- Read: [splitter-components.md](references/splitter-components.md)

### 5. Multi-Language Editor
**Scenario:** Localized application with language-specific views.
- Multiple TabSplitterPages for different languages
- Swap functionality for language switching
- Use localization support for tab labels
- Read: [advanced-features.md](references/advanced-features.md)

### 6. Report Designer
**Scenario:** Report design with code/preview split.
- Primary: Report definition editor (XML/JSON)
- Secondary: Report preview rendering
- Vertical orientation for stacked layout
- Adjustable splitter for resizing panes
- Read: [orientation-and-position.md](references/orientation-and-position.md)

---

## Events

**Common events for TabSplitterContainer:**
- Component-specific events for state changes
- See [advanced-features.md](references/advanced-features.md) for detailed event documentation

---

## Best Practices

1. **Theme Consistency:** Match TabSplitterContainer Style to application theme
2. **Splitter Position:** Set initial SplitterPosition based on content importance
3. **Page Management:** Use PrimaryPages for main content, SecondaryPages for supporting views
4. **Collapse State:** Provide UI controls for users to toggle Collapsed state
5. **Orientation Choice:** Use Horizontal for side-by-side, Vertical for stacked layouts
6. **Swap Functionality:** Enable Swapped property for user preference customization
7. **Page Naming:** Use descriptive Text property for clear tab labels
8. **Performance:** Lazy-load page content to improve initial load time

---

## See Also

- [Syncfusion TabSplitterContainer Documentation](https://help.syncfusion.com/windowsforms/tabsplittercontainer/overview)
- [TabSplitterContainer API Reference](https://help.syncfusion.com/cr/windowsforms/Syncfusion.Windows.Forms.Tools.TabSplitterContainer.html)
- [TabSplitterPage API Reference](https://help.syncfusion.com/cr/windowsforms/Syncfusion.Windows.Forms.Tools.TabSplitterPage.html)
