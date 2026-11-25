---
name: syncfusion-aspnetcore-blockeditor
description: Implement Syncfusion Block Editor control in ASP.NET Core applications using Razor Tag Helpers. Use this skill when working with Syncfusion Block Editor, EJ2 BlockEditor, ASP.NET Core block-based content editing, or <ejs-blockeditor> syntax. Covers block management, nested content structures, drag-and-drop functionality, content sanitization, installation, tag helper setup, block types, content manipulation, events, menus, and advanced features for creating rich block-based document editors.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Syncfusion ASP.NET Core Block Editor Control

## Overview

A comprehensive skill for implementing Syncfusion EJ2 Block Editor in ASP.NET Core applications using Razor Tag Helpers. This skill covers setup, block configuration, content manipulation, events, and best practices for creating block-based document editors.

The Syncfusion Block Editor is a versatile, block-based content editor that allows users to create and edit structured documents using discrete content blocks. Key capabilities include:

- **Multiple Block Types**: Paragraph, Headings (1-4), Lists (Bullet, Numbered, Checklist), Code, Tables, Images, Quotes, Callouts, and more
- **Nested Structures**: Support for collapsible headings, quotes, and callouts with child blocks
- **Rich Editor Menus**: Slash commands, context menus, inline toolbars, and block action menus
- **Drag-and-Drop**: Reorder blocks seamlessly with visual feedback
- **Content Sanitization**: Built-in paste cleanup with configurable allowed styles and denied tags
- **Keyboard Shortcuts**: Comprehensive shortcuts for formatting, block creation, and management
- **Undo/Redo**: Configurable undo/redo stack (default 30 actions)
- **Globalization**: Multi-language support and RTL layout support
- **Events**: Rich event system for monitoring user interactions and content changes
- **Responsive Design**: Adaptive UI that works on desktop and mobile devices

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and package setup
- Basic BlockEditor implementation
- CSS imports and theme selection
- Creating the first Block Editor instance
- Setting initial block content

### Built-in Blocks
📄 **Read:** [references/built-in-blocks.md](references/built-in-blocks.md)
- Block types overview (Paragraph, Heading, Lists, Code, Table, Embed, etc.)
- Block properties (id, blockType, content, indent)
- Nested block types (CollapsibleHeading, CollapsibleParagraph, Quote, Callout)
- Parent-child relationships and hierarchy
- Expanded state control and placeholders
- CSS class customization and templates

### Block Editor Menus
📄 **Read:** [references/blockeditor-menus.md](references/blockeditor-menus.md)
- Inline toolbar configuration and events
- Block actions menu customization
- Slash commands (/) for quick block insertion
- Context menu configuration
- Toolbar buttons and formatting actions

### Drag-Drop and Content
📄 **Read:** [references/drag-drop-and-content.md](references/drag-drop-and-content.md)
- Enable drag-and-drop functionality
- Reordering blocks by dragging
- Multiple block selection and movement
- Visual feedback during drag operations
- Content insertion and block positioning

### Methods and API
📄 **Read:** [references/methods-and-api.md](references/methods-and-api.md)
- Block Management: addBlock, removeBlock, moveBlock, updateBlock, getBlock, getBlockCount
- Selection & Cursor: setSelection, setCursorPosition, getSelectedBlocks, getRange, selectRange, selectBlock, selectAllBlocks
- Focus Management: focusIn, focusOut
- Formatting: executeToolbarAction, enableToolbarItems, disableToolbarItems
- Data Export: getDataAsJson, getDataAsHtml, renderBlocksFromJson, parseHtmlToBlocks, print
- Practical examples for each method category

### Styling and Appearance
📄 **Read:** [references/styling-and-appearance.md](references/styling-and-appearance.md)
- CSS theming options (Material, Bootstrap, Fluent, Tailwind, Fabric themes)
- Block-level styling and cssClass property
- Typography options (bold, italic, underline, strikethrough)
- Indentation and nested block styling
- Placeholder text customization
- Dark mode support and custom themes

### Advanced Features
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- Paste cleanup and content sanitization (allowed styles, denied tags)
- Keep format and plain text modes
- Undo/Redo functionality and stack configuration
- Keyboard shortcuts and customization
- Read-only mode for view-only editors
- XSS protection and HTML sanitizer
- RTL (Right-to-Left) support
- Globalization and multi-language localization

## Quick Start Example

### Basic Block Editor Setup

**Step 1: Install NuGet Package**
```powershell
Install-Package Syncfusion.EJ2.AspNet.Core
```

**Step 2: Register in _ViewImports.cshtml**
```razor
@addTagHelper *, Syncfusion.EJ2
```

**Step 3: Add CSS and Scripts in _Layout.cshtml**
```razor
<head>
    <link rel="stylesheet" href="https://cdn.syncfusion.com/ej2/dist/ej2.min.css" />
</head>
<body>
    @RenderBody()
    
    <script src="https://cdn.syncfusion.com/ej2/dist/ej2.min.js"></script>
    <ejs-scripts></ejs-scripts>
    
    @RenderSection("Scripts", required: false)
</body>
```

**Step 4: Create Block Editor in View**
```razor
@using Syncfusion.EJ2.BlockEditor

<div id='blockeditor-container'>
    <ejs-blockeditor id="block-editor" blocks="@ViewBag.BlocksData"></ejs-blockeditor>
</div>

<style>
    #blockeditor-container {
        margin: 20px auto;
    }
</style>
```

**Step 5: Configure Blocks in Controller**
```csharp
using Syncfusion.EJ2.BlockEditor;

public class BlockModel
{
    public string id { get; set; }
    public string blockType { get; set; }
    public object properties { get; set; }
    public List<object> content { get; set; }
}

public IActionResult Index()
{
    var blocks = new List<BlockModel>
    {
        new BlockModel
        {
            id = "heading-1",
            blockType = "Heading",
            properties = new { level = 1 },
            content = new List<object>
            {
                new { contentType = "Text", content = "Welcome to Block Editor" }
            }
        },
        new BlockModel
        {
            id = "paragraph-1",
            blockType = "Paragraph",
            content = new List<object>
            {
                new { contentType = "Text", content = "Start creating your content with blocks!" }
            }
        }
    };
    
    ViewBag.BlocksData = blocks;
    return View();
}
```

## Common Patterns

### Pattern 1: Add New Block Dynamically

```javascript
var blockEditorObj = ej.base.getInstance(document.getElementById('block-editor'), ejs.blockeditor.BlockEditor);

const newBlock = {
    id: 'new-paragraph',
    blockType: 'Paragraph',
    content: [
        {
            contentType: "Text",
            content: 'This is a newly added block'
        }
    ]
};

// Add after a specific block
blockEditorObj.addBlock(newBlock, 'existing-block-id', true);
```

### Pattern 2: Nested Collapsible Structure

```csharp
new BlockModel
{
    blockType = "CollapsibleHeading",
    content = new List<object>
    {
        new { contentType = "Text", content = "Section Title" }
    },
    properties = new
    {
        level = 1,
        isExpanded = true,
        children = new List<BlockModel>
        {
            new BlockModel
            {
                blockType = "Paragraph",
                content = new List<object>
                {
                    new { contentType = "Text", content = "Hidden content goes here" }
                }
            }
        }
    }
}
```

### Pattern 3: Configure Paste Cleanup

```razor
<ejs-blockeditor id="block-editor">
    <e-blockeditor-pastesettings 
        allowedStyles="@(new string[] { "font-weight", "font-style", "text-decoration" })"
        deniedTags="@(new string[] { "script", "iframe", "form" })"
        keepFormat="true">
    </e-blockeditor-pastesettings>
</ejs-blockeditor>
```

### Pattern 4: Custom Slash Commands

```csharp
var commandMenuItems = new List<object>
{
    new 
    {
        id = "timestamp",
        groupHeader = "Actions",
        label = "Insert Timestamp",
        iconCss = "e-icons e-schedule"
    },
    new 
    {
        id = "separator",
        type = "Divider",
        groupHeader = "Utility",
        label = "Insert Divider",
        iconCss = "e-icons e-divider"
    }
};

ViewBag.CommandMenuItems = commandMenuItems;
```

### Pattern 5: Readonly Editor for Display

```razor
<ejs-blockeditor id="block-editor" 
                 readOnly="true" 
                 blocks="@ViewBag.BlocksData">
</ejs-blockeditor>
```

## Key Properties

| Property | Type | Description | Default |
|----------|------|-------------|---------|
| `id` | string | Unique identifier for the Block Editor instance | - |
| `blocks` | List<BlockModel> | Initial block content | [] |
| `height` | string | Height of the editor (px, vh, %) | auto |
| `width` | string | Width of the editor (px, %) | 100% |
| `readOnly` | bool | Enable read-only mode | false |
| `cssClass` | string | Custom CSS class for styling | - |
| `enableDragAndDrop` | bool | Enable block drag-and-drop | true |
| `enableRtl` | bool | Enable right-to-left layout | false |
| `locale` | string | Localization culture (e.g., "de", "es") | "en" |
| `undoRedoStack` | int | Number of undo/redo steps | 30 |
| `keyConfig` | object | Keyboard shortcuts configuration | default shortcuts |

## Common Use Cases

1. **Blog Post Editor** - Create a structured blog editor with headings, paragraphs, lists, code snippets, and images
2. **Knowledge Base** - Build hierarchical documentation with collapsible sections and nested content
3. **Newsletter Template Builder** - Design email templates with predefined blocks
4. **Content Management System** - Manage modular content with drag-and-drop block reordering
5. **Documentation Platform** - Create technical documentation with code blocks, tables, and callouts
6. **Form Builder** - Create dynamic forms with conditional block visibility
7. **Collaborative Editing** - Implement shared document editing with block-level permissions

## Workflow Pattern

When implementing a Syncfusion Block Editor in ASP.NET Core:

1. **Install and Setup** - Follow Getting Started guide for package installation and registration
2. **Define Block Structure** - Choose block types and configure them in references/built-in-blocks.md
3. **Initialize Editor** - Create Block Editor instance with initial blocks
4. **Configure Features** - Enable menus, drag-drop, paste cleanup as needed
5. **Handle Events** - Bind to events for content validation, logging, or integration
6. **Customize Appearance** - Apply CSS themes, custom classes, and styling
7. **Implement Methods** - Use API methods for programmatic content manipulation
8. **Test and Optimize** - Verify functionality and performance
