---
name: syncfusion-aspnetcore-splitter
description: Implement Syncfusion ASP.NET Core Splitter component for building responsive multi-pane layouts. Use this when implementing splitter layouts, configuring panes, enabling resize functionality, or creating complex nested layouts with multiple split sections.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Layout Components"
---

# Implementing Syncfusion ASP.NET Core Splitter

## When to Use This Skill

Use this skill when you need to:
- Create responsive multi-pane layouts with the Splitter component
- Configure horizontal and vertical split panes
- Set up pane sizing (pixels, percentages, auto)
- Enable or disable pane resizing with min/max constraints
- Add HTML, plain text, or Syncfusion controls as pane content
- Implement expand/collapse functionality for panes
- Build nested splitters for complex layouts
- Customize splitter styling and appearance
- Enable RTL (right-to-left) support for globalization

## Component Overview

The Syncfusion ASP.NET Core Splitter is a layout/container control that allows you to create complex multi-pane applications. It supports:
- **Multiple panes** with horizontal and vertical orientations
- **Flexible sizing** using pixels, percentages, or automatic sizing
- **Resizable panes** with drag handles and min/max constraints
- **Collapsible panes** with expand/collapse buttons
- **Rich content** including HTML, text, and other Syncfusion controls
- **Nested splitters** for hierarchical layout architectures
- **Customizable styling** and RTL support

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- NuGet package installation
- Tag helper registration
- Stylesheet and script setup
- Creating your first splitter
- Basic two-pane configuration
- Orientation setup

### Split Pane Layouts
📄 **Read:** [references/split-pane-layouts.md](references/split-pane-layouts.md)
- Horizontal vs vertical layouts
- Multiple pane configurations
- Separator customization
- Nested splitter implementation
- Layout patterns for complex designs

### Pane Content
📄 **Read:** [references/pane-content.md](references/pane-content.md)
- HTML markup as pane content
- Syncfusion controls within panes
- Plain text content
- Content templates
- Selector-based content loading
- JavaScript initialization approach (Accordion + ListView)

### Pane Sizing and Resizing
📄 **Read:** [references/pane-sizing-and-resizing.md](references/pane-sizing-and-resizing.md)
- Pixel-based pane sizing
- Percentage-based sizing
- Auto-sizing panes
- Min/max size constraints
- Enabling/disabling resize
- Resize events and gripper customization

### Expand and Collapse
📄 **Read:** [references/expand-collapse.md](references/expand-collapse.md)
- Collapsible pane configuration
- Programmatic expand/collapse methods
- Initial collapsed state
- Expand/collapse events

### Styling and Globalization
📄 **Read:** [references/styling-and-globalization.md](references/styling-and-globalization.md)
- CSS customization for split bars
- Resize handle styling
- Custom themes
- RTL (right-to-left) support
- Accessibility features

### API Reference
📄 **Read:** [references/api-reference.md](references/api-reference.md)
- Complete Splitter properties documentation
- Pane properties with examples
- Methods (expand, collapse, addPane, removePane)
- All events with event handlers
- Event argument objects and properties
- Complete working examples

## Quick Start Example

```csharp
<!-- _Layout.cshtml -->
<head>
    <link rel="stylesheet" href="url" />
    <script src="url"></script>
</head>

<body>
    @RenderBody()
    <ejs-scripts></ejs-scripts>
</body>
```

```csharp
<!-- Index.cshtml -->
@addTagHelper *, Syncfusion.EJ2

<ejs-splitter id="splitter" height="400px">
    <e-splitter-panes>
        <e-splitter-pane size="50%">
            <div class="content">
                <h3>Pane 1</h3>
                <p>Left pane content</p>
            </div>
        </e-splitter-pane>
        <e-splitter-pane size="50%">
            <div class="content">
                <h3>Pane 2</h3>
                <p>Right pane content</p>
            </div>
        </e-splitter-pane>
    </e-splitter-panes>
</ejs-splitter>
```

## Common Patterns

### Two-Pane Layout (Left Navigation + Content)
```csharp
<ejs-splitter id="splitter" height="600px">
    <e-splitter-panes>
        <e-splitter-pane size="25%" min="20%"></e-splitter-pane>
        <e-splitter-pane size="75%" min="40%"></e-splitter-pane>
    </e-splitter-panes>
</ejs-splitter>
```

### Three-Pane Layout (Master, Detail, Preview)
```csharp
<ejs-splitter id="splitter" height="600px">
    <e-splitter-panes>
        <e-splitter-pane size="30%" min="20%"></e-splitter-pane>
        <e-splitter-pane size="40%" min="25%"></e-splitter-pane>
        <e-splitter-pane size="30%" min="20%"></e-splitter-pane>
    </e-splitter-panes>
</ejs-splitter>
```

### Vertical Stack (Header, Main, Footer)
```csharp
<ejs-splitter id="splitter" height="600px" orientation="Vertical">
    <e-splitter-panes>
        <e-splitter-pane size="15%" min="50px"></e-splitter-pane>
        <e-splitter-pane size="70%" min="100px"></e-splitter-pane>
        <e-splitter-pane size="15%" min="50px"></e-splitter-pane>
    </e-splitter-panes>
</ejs-splitter>
```

## Key Pane Configuration Properties

| Property | Type | Purpose |
|----------|------|---------|
| `size` | string | Pane size in pixels (`"200px"`) or percentage (`"50%"`) |
| `min` | string | Minimum size to prevent over-resizing |
| `max` | string | Maximum size to limit expansion |
| `resizable` | bool | Enable/disable resize for this pane (default: true) |
| `collapsible` | bool | Enable/disable collapse button (default: false) |
| `collapsed` | bool | Initial collapsed state (default: false) |
| `content` | string | HTML or text content for pane |

## Common Use Cases

1. **Code Editor Layout** - Split code editor with preview/output pane
2. **Dashboard** - Multiple sections with resizable panels
3. **Email Client** - Folder list, message list, message detail
4. **IDE Interface** - Project explorer, editor, properties panel
5. **Document Editor** - Ribbon, canvas, properties, preview
6. **File Manager** - Tree view, file list, preview
7. **Chat Application** - Conversation list, chat area, user info

## Next Steps

- Review the **Getting Started** guide for installation and basic setup
- Choose your layout pattern from **Split Pane Layouts**
- Configure pane sizing in **Pane Sizing and Resizing**
- Add rich content using **Pane Content** options
- Implement advanced features like **Expand and Collapse**
- Apply custom styling from **Styling and Globalization**
