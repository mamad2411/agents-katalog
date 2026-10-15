---
name: syncfusion-javascript-block-editor
description: "Implement the Syncfusion JavaScript BlockEditor control - a modern block-based text editor with drag-and-drop, slash commands, and extensive formatting capabilities. Use this skill IMMEDIATELY for: BlockEditor implementation, block-based editors, content editing with blocks, document editors with block structure, text editing with modern UI, slash command menus, drag-and-drop content reordering, inline toolbars, collaborative editing features, structured content creation, @mentions and labels, code blocks with syntax highlighting, tables and lists, collapsible sections, or any Syncfusion EJ2 BlockEditor control usage in JavaScript applications."
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Syncfusion JavaScript BlockEditor

## Overview

The Syncfusion JavaScript BlockEditor is a modern, block-based text editor that enables users to create, format, and organize content using various block types. It provides an intuitive editing experience with features like drag-and-drop reordering, slash commands, inline toolbars, and extensive customization options. The BlockEditor control is built on a block-based architecture where content is organized into discrete blocks. Each block has a specific type (paragraph, heading, list, image, etc.) and can contain formatted content. Key characteristics:

- **Block Types**: 14 built-in block types including typography, lists, tables, images, code, and collapsible sections
- **Content Model**: Structured content with BlockModel and ContentModel for programmatic manipulation
- **Intuitive UX**: Slash commands (/), drag handles, inline toolbars, and context menus
- **Extensibility**: Custom blocks, commands, menu items, and templates
- **Data Formats**: Import/export as HTML or JSON for flexible storage and interchange
- **Accessibility**: Keyboard navigation, ARIA attributes, and screen reader support

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and package setup (`@syncfusion/ej2-blockeditor`)
- CSS imports and theme configuration (Tailwind3, Material, Bootstrap, etc.)
- Basic BlockEditor initialization and first render
- Webpack configuration for development environment
- Minimal working example with sample blocks

### Blocks and Content Models
📄 **Read:** [references/blocks-and-content-models.md](references/blocks-and-content-models.md)
- Complete BlockModel interface (id, blockType, content, properties, cssClass, indent, parentId, template)
- BlockType enum (Paragraph, Heading, BulletList, NumberedList, Checklist, Table, Image, Code, Quote, Callout, Divider, CollapsibleParagraph, CollapsibleHeading, Template)
- ContentModel interface (id, contentType, content, properties)
- ContentType enum (Text, Link, Mention, Label)
- Block-specific properties (HeadingProps, ImageProps, CodeProps, ChecklistProps, CollapsibleProps, etc.)
- Content-specific properties (LinkContentProps, MentionContentProps, StyleModel)
- UserModel for mentions and collaboration
- BlockFactory class with helper methods for creating blocks

### Built-in Block Types
📄 **Read:** [references/built-in-block-types.md](references/built-in-block-types.md)
- Typography blocks: Paragraph, Heading (1-4), Quote, Callout
- Text formatting: bold, italic, underline, strikethrough, uppercase, lowercase, subscript, superscript, inline code
- Font color and background color (text highlighting)
- List blocks: BulletList, NumberedList, Checklist (with isChecked)
- Table blocks with configuration
- Media blocks: Image with upload, resize, and constraints (imageBlockSettings)
- Code blocks with syntax highlighting and language selection (codeBlockSettings)
- Advanced blocks: CollapsibleParagraph, CollapsibleHeading, Divider, Template
- Nested block structures with parent-child relationships

### Editor Menus and Toolbars
📄 **Read:** [references/editor-menus-and-toolbars.md](references/editor-menus-and-toolbars.md)
- Slash Command Menu (/) - commandMenuSettings with CommandItemModel
- Block Action Menu (⋮ handle) - blockActionMenuSettings with BlockActionItemModel
- Context Menu (right-click) - contextMenuSettings with ContextMenuItemModel
- Inline Formatting Toolbar - inlineToolbarSettings with ToolbarItemModel and BuiltInToolbar enum
- Transform Menu - transformSettings for block type conversion
- Custom commands and menu items
- Menu events: filtering, itemSelect, beforeOpen, beforeClose
- Complete customization examples

### Methods Reference
📄 **Read:** [references/methods-reference.md](references/methods-reference.md)
- Block management: addBlock, removeBlock, moveBlock, updateBlock
- Block queries: getBlock, getBlockCount, getSelectedBlocks
- Selection: selectBlock, selectAllBlocks, selectRange, setSelection, getRange, setCursorPosition
- Data operations: getDataAsHtml, getDataAsJson, parseHtmlToBlocks, renderBlocksFromJson
- Toolbar control: enableToolbarItems, disableToolbarItems, executeToolbarAction
- Focus management: focusIn, focusOut
- Utility: print, refresh, dataBind
- Lifecycle: appendTo, destroy, addEventListener, removeEventListener

### Events Reference
📄 **Read:** [references/events-reference.md](references/events-reference.md)
- Lifecycle: created
- Content: blockChanged (with BlockChangedEventArgs), selectionChanged
- Focus: focus (FocusEventArgs), blur (BlurEventArgs)
- Drag-drop: blockDragStart, blockDragging, blockDropped (with BlockDragEventArgs, BlockDropEventArgs)
- Paste: beforePasteCleanup, afterPasteCleanup (with PasteCleanupEventArgs)
- File upload: beforeFileUpload, fileUploading, fileUploadSuccess, fileUploadFailed
- Complete event arguments interfaces
- ActionType enum for undo/redo tracking

### Drag-Drop and Selection
📄 **Read:** [references/drag-drop-and-selection.md](references/drag-drop-and-selection.md)
- Drag-and-drop configuration (enableDragAndDrop property)
- Single and multiple block dragging
- Drag events and visual indicators
- Selection management methods
- Programmatic selection control
- NodeSelection class
- Cursor positioning

### Paste, Undo/Redo, and Keyboard
📄 **Read:** [references/paste-undo-redo-keyboard.md](references/paste-undo-redo-keyboard.md)
- Paste cleanup configuration (pasteCleanupSettings with keepFormat, plainText, allowedStyles, deniedTags)
- Paste events for interception and modification
- Undo/redo stack configuration (undoRedoStack property)
- Keyboard shortcuts (keyConfig property for custom shortcuts)
- Default keyboard commands
- Mentions (@user) with users property and UserModel
- Labels/tags ($label) with labelSettings property and LabelItemModel

### Customization and Appearance
📄 **Read:** [references/customization-and-appearance.md](references/customization-and-appearance.md)
- Dimensions: width, height properties
- Custom styling: cssClass property
- Font color customization: fontColorSettings (FontColorSettingsModel with palette/picker modes)
- Background color customization: backgroundColorSettings (BackgroundColorSettingsModel)
- ColorModeType enum (Palette, Picker)
- Read-only mode: readOnly property
- RTL support: enableRtl property
- Localization: locale property
- Custom block templates
- Theme integration

### Security and Sanitization
📄 **Read:** [references/security-and-sanitization.md](references/security-and-sanitization.md)
- HTML sanitization
- HTML encoding (enableHtmlEncode property)
- XSS prevention strategies
- Read-only mode for view-only content
- Paste security with deniedTags
- Safe content handling best practices
- Compliance considerations

## Quick Start Example

```typescript
import { BlockEditor, BlockType, ContentType } from '@syncfusion/ej2-blockeditor';

// Initialize BlockEditor with sample content
const editor = new BlockEditor({
    width: '100%',
    height: '600px',
    blocks: [
        {
            id: 'heading-1',
            blockType: BlockType.Heading,
            properties: { level: 1 },
            content: [
                {
                    id: 'h1-content',
                    contentType: ContentType.Text,
                    content: 'Welcome to BlockEditor'
                }
            ]
        },
        {
            id: 'intro-para',
            blockType: BlockType.Paragraph,
            content: [
                {
                    id: 'intro-text',
                    contentType: ContentType.Text,
                    content: 'Start typing or press "/" to open the command menu.'
                }
            ]
        },
        {
            id: 'bullet-list',
            blockType: BlockType.BulletList,
            content: [
                {
                    id: 'list-item-1',
                    contentType: ContentType.Text,
                    content: 'Drag blocks to reorder'
                }
            ]
        }
    ],
    enableDragAndDrop: true,
    enableHtmlSanitizer: true
});

// Render the editor
editor.appendTo('#blockeditor');
```

```html
<!DOCTYPE html>
<html>
<head>
    <link href="https://cdn.syncfusion.com/ej2/32.1.19/tailwind.css" rel="stylesheet" />
</head>
<body>
    <div id="blockeditor"></div>
</body>
</html>
```

## Common Patterns

### Adding Blocks Programmatically

```typescript
// Add a new paragraph block after a target block
const newBlock = {
    id: 'new-para',
    blockType: BlockType.Paragraph,
    content: [
        {
            id: 'new-content',
            contentType: ContentType.Text,
            content: 'This is a new paragraph.'
        }
    ]
};

editor.addBlock(newBlock, 'target-block-id', true); // true = after
```

### Getting Content as HTML/JSON

```typescript
// Get all content as HTML
const htmlContent = editor.getDataAsHtml();

// Get all content as JSON
const jsonContent = editor.getDataAsJson();

// Get specific block content
const blockHtml = editor.getDataAsHtml('block-id');
const blockJson = editor.getDataAsJson('block-id');
```

### Handling Block Changes

```typescript
const editor = new BlockEditor({
    blockChanged: (args) => {
        console.log('Blocks changed:', args.changes);
        // Auto-save functionality
        saveContent(editor.getDataAsJson());
    }
});
```

### Custom Slash Commands

```typescript
const editor = new BlockEditor({
    commandMenuSettings: {
        popupWidth: '350px',
        commands: [
            {
                id: 'custom-quote',
                type: BlockType.Quote,
                label: 'Quote Block',
                iconCss: 'e-icons e-quote',
                groupBy: 'Basic'
            },
            {
                id: 'timestamp',
                label: 'Insert Timestamp',
                iconCss: 'e-icons e-schedule',
                groupBy: 'Actions'
            }
        ],
        itemSelect: (args) => {
            if (args.command.id === 'timestamp') {
                // Custom action: insert current timestamp
                const timestamp = new Date().toLocaleString();
                // Insert logic here
            }
        }
    }
});
```

### Image Upload Configuration

```typescript
const editor = new BlockEditor({
    imageBlockSettings: {
        saveUrl: 'https://your-server.com/api/upload',
        path: '/images/',
        allowedTypes: ['.jpg', '.jpeg', '.png', '.gif'],
        maxFileSize: 5000000, // 5MB
        maxWidth: 1200,
        maxHeight: 800,
        enableResize: true,
        saveFormat: 'Base64' // or 'Blob'
    },
    fileUploadSuccess: (args) => {
        console.log('File uploaded:', args.fileUrl);
    }
});
```

## Key Configuration Options

### Essential Properties

- **blocks**: `BlockModel[]` - Initial content blocks
- **width**: `string | number` - Editor width (default: '100%')
- **height**: `string | number` - Editor height (default: 'auto')
- **readOnly**: `boolean` - Read-only mode (default: false)
- **enableDragAndDrop**: `boolean` - Drag-drop blocks (default: true)
- **enableHtmlSanitizer**: `boolean` - Sanitize HTML (default: true)
- **undoRedoStack**: `number` - Max undo/redo operations (default: 30)
- **cssClass**: `string` - Custom CSS class for styling

### Menu and Toolbar Settings

- **commandMenuSettings**: `CommandMenuSettingsModel` - Slash command menu (/)
- **blockActionMenuSettings**: `BlockActionMenuSettingsModel` - Block action menu (⋮)
- **contextMenuSettings**: `ContextMenuSettingsModel` - Right-click context menu
- **inlineToolbarSettings**: `InlineToolbarSettingsModel` - Text formatting toolbar
- **transformSettings**: `TransformSettingsModel` - Block transformation menu

### Feature Settings

- **imageBlockSettings**: `ImageBlockSettingsModel` - Image upload and configuration
- **codeBlockSettings**: `CodeBlockSettingsModel` - Code syntax highlighting
- **pasteCleanupSettings**: `PasteCleanupSettingsModel` - Paste formatting control
- **labelSettings**: `LabelSettingsModel` - Labels/tags configuration ($label)
- **users**: `UserModel[]` - Users for mentions (@user)
- **keyConfig**: `{ [key: string]: string }` - Custom keyboard shortcuts

### Color Settings

- **fontColorSettings**: `FontColorSettingsModel` - Text color palette
- **backgroundColorSettings**: `BackgroundColorSettingsModel` - Background/highlight color palette

### Localization and RTL

- **locale**: `string` - Localization code (default: 'en-US')
- **enableRtl**: `boolean` - Right-to-left support (default: false)
- **enablePersistence**: `boolean` - Persist state across reloads (default: false)
