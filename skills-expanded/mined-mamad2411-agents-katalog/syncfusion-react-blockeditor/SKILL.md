---
name: syncfusion-react-blockeditor
description: Implement the Syncfusion React BlockEditor component for block-based content editing. Use this skill for block-based rich content editing, document creation, CMS interfaces, markdown alternatives, editor setup, block configuration, toolbar or menu customization, drag-and-drop behavior, formatting options, APIs, accessibility, real-time collaborative editing with Yjs integration, user presence and remote cursors, document version history and snapshot management in React.
metadata:
  author: "Syncfusion Inc"
  version: "34.1.29"
---

# Syncfusion React Block Editor in React

## Component Overview

The Syncfusion React BlockEditorComponent is a powerful block-based rich text editor that allows users to create, edit, and format content using a modern block architecture. Each piece of content (paragraphs, headings, lists, tables, code snippets) is a discrete, manageable block.

### Key Capabilities

The BlockEditorComponent provides:
- **Block-based architecture** - Content structured as discrete, reorderable blocks
- **Built-in block types** - Paragraphs, headings, lists, tables, code, callouts, quotes, collapsible sections
- **Intuitive menus** - Slash commands, context menus, inline toolbars
- **Drag-and-drop** - Reorder blocks easily with visual handles
- **Content export** - Export as JSON, HTML, or plain text
- **Accessibility** - WCAG 2.1 compliant with keyboard navigation and screen reader support
- **Customization** - Custom styling, themes, RTL support, globalization
- **Collaborative Editing** - Real-time multi-user editing powered by Yjs, with user presence and remote cursors, document version history and snapshot management

## Documentation Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and npm package setup
- Basic component implementation
- CSS imports and theme configuration
- Creating your first block editor
- Setting initial content with blocks

### Built-in Block Types
📄 **Read:** [references/built-in-blocks.md](references/built-in-blocks.md)
- Block type reference (Paragraph, Heading, List, Table, Code, Quote, Callout)
- Nested block types (CollapsibleHeading, CollapsibleParagraph)
- Block indentation and CSS class styling
- Content configuration and properties

### Menus and Commands
📄 **Read:** [references/block-editor-menus.md](references/block-editor-menus.md)
- Slash command menu customization
- Context menu configuration with Table and Link options
- Inline toolbar setup with Transform, code, link, and color support
- Block action menu customization and tooltips
- Menu events and filtering

### Drag-Drop and Content Management
📄 **Read:** [references/drag-drop-and-content.md](references/drag-drop-and-content.md)
- Drag-and-drop block reordering (`enableDragAndDrop`)
- Content insertion and nesting
- Drag events (`blockDragStart`, `blockDragging`, `blockDropped`)
- Programmatic block movement

### Mentions and Labels
📄 **Read:** [references/mentions-and-labels.md](references/mentions-and-labels.md)
- `users` prop and `UserModel` interface for `@mention` feature
- `labelSettings` prop and `LabelItemModel` interface for label feature
- `ContentType.Mention` / `ContentType.Label` inline content
- `IMentionContentSettings` / `ILabelContentSettings`

### Methods and API
📄 **Read:** [references/methods-and-api.md](references/methods-and-api.md)
- Block management methods (add, remove, update, move)
- Selection and cursor control
- Data export/import (JSON, HTML)
- Content formatting and rendering

### Styling and Appearance
📄 **Read:** [references/styling-and-appearance.md](references/styling-and-appearance.md)
- CSS theming and imports
- Block styling with custom CSS classes
- Typography and formatting options
- Dark mode and responsive design

### Advanced Features
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- Paste cleanup and content sanitization
- Undo/redo functionality
- Keyboard shortcut customization
- Read-only mode configuration
- XSS protection and HTML sanitization
- RTL support and internationalization

### Collaborative Editing
📄 **Read:** [references/collaborative-editing.md](references/collaborative-editing.md)
- Real-time collaborative editing powered by Yjs (CRDT-based sync and conflict resolution)
- Injecting the `Collaboration` and `VersionHistory` modules
- `collaborationSettings` property (provider, adapter, enableAwareness, versionHistory)
- Choosing a Yjs provider (y-websocket, y-webrtc, y-indexeddb, Hocuspocus, Liveblocks, PartyKit)
- Setting up a Yjs document, `YjsAdapter`, and provider
- User presence, remote cursors, and text selection overlays (enableAwareness)
- Configuring the current user via `users` and `currentUserId`
- Version history: creating, listing, renaming, restoring, comparing, exporting, and importing snapshots
- Custom snapshot storage via the `IVersionStorage` interface
- Version history events: `snapshotCreated`, `snapshotRestored`

### Accessibility
📄 **Read:** [references/accessibility.md](references/accessibility.md)
- WCAG 2.1 compliance
- Keyboard navigation patterns
- Screen reader support and ARIA attributes
- Focus management
- Color contrast and visual indicators

## Quick Start Example

```tsx
import { BlockEditorComponent } from '@syncfusion/ej2-react-blockeditor';
import { BlockModel, ContentType } from '@syncfusion/ej2-react-blockeditor';
import '@syncfusion/ej2-react-blockeditor/styles/material.css';

function App() {
  // Define initial blocks
  const blocksData: BlockModel[] = [
    {
      id: 'block-1',
      blockType: 'Heading',
      properties: { level: 1 },
      content: [
        {
          contentType: ContentType.Text,
          content: 'Welcome to Block Editor'
        }
      ]
    },
    {
      id: 'block-2',
      blockType: 'Paragraph',
      content: [
        {
          contentType: ContentType.Text,
          content: 'This is your first paragraph. Click the "+" button to add more blocks.'
        }
      ]
    }
  ];

  return (
    <BlockEditorComponent
      id="block-editor"
      blocks={blocksData}
    />
  );
}

export default App;
```

## Common Patterns

### 1. Add a Block Programmatically

```tsx
const editorRef = React.useRef<BlockEditorComponent>(null);

const addNewBlock = () => {
  const newBlock: BlockModel = {
    blockType: 'Paragraph',
    content: [
      {
        contentType: ContentType.Text,
        content: 'New paragraph block'
      }
    ]
  };
  
  editorRef.current?.addBlock(newBlock);
};
```

### 2. Handle Menu Item Selection

```tsx
const commandMenuSettings = {
  itemSelect: (args) => {
    console.log('Selected command:', args.command.label, args.command.id);
    // Handle custom actions based on selected command
  }
};
```

### 3. Export Content as JSON

```tsx
const exportContent = () => {
  const jsonContent = editorRef.current?.getDataAsJson();
  console.log('Exported content:', jsonContent);
};
```

### 4. Enable Read-Only Mode

```tsx
<BlockEditorComponent
  id="block-editor"
  blocks={blocksData}
  readOnly={true}
/>
```

## Key Props

> ⚠️ Props `toolbarSettings`, `containerCssClass`, and `showBlockHandle` do **not** exist in the BlockEditor API and must not be used.

| Prop | Type | Description |
|------|------|-------------|
| `id` | `string` | Unique identifier for the component |
| `blocks` | `BlockModel[]` | Array of block objects defining content |
| `readOnly` | `boolean` | Enable read-only mode (default: `false`) |
| `width` | `string \| number` | Width of the editor container (default: `'100%'`) |
| `height` | `string \| number` | Height of the editor container |
| `commandMenuSettings` | `CommandMenuSettingsModel` | Customize slash command (/) menu |
| `contextMenuSettings` | `ContextMenuSettingsModel` | Configure right-click context menu |
| `inlineToolbarSettings` | `InlineToolbarSettingsModel` | Configure inline text selection toolbar |
| `blockActionMenuSettings` | `BlockActionMenuSettingsModel` | Configure block action (⋮) menu |
| `transformSettings` | `TransformSettingsModel` | Configure block type transform menu |
| `imageBlockSettings` | `ImageBlockSettingsModel` | Configure image upload and rendering |
| `codeBlockSettings` | `CodeBlockSettingsModel` | Configure code block languages |
| `pasteCleanupSettings` | `PasteCleanupSettingsModel` | Control paste sanitization behavior |
| `users` | `UserModel[]` | User list for `@mention` feature and collaboration presence with avatar colors |
| `labelSettings` | `LabelSettingsModel` | Label items and trigger char for label feature |
| `enableDragAndDrop` | `boolean` | Enable/disable drag-and-drop reordering (default: `true`) |
| `undoRedoStack` | `number` | Max number of undo/redo history steps |
| `keyConfig` | `{ [key: string]: string }` | Custom keyboard shortcut mappings |
| `locale` | `string` | Localization language code (default: `'en-US'`) |
| `blockChanged` | `EmitType<BlockChangedEventArgs>` | Fires when block content changes |
| `collaborationSettings` | `CollaborationSettingsModel` | Configure real-time collaboration with Yjs provider, awareness, and version history |
| `currentUserId` | `string` | Unique identifier of the current user for collaboration and cursor identification |

## Common Use Cases

**Content Management System** - Build a CMS with block-based editing, custom block types, and content export

**Document Editor** - Create a collaborative document editor with formatting, templates, and version control

**Note-Taking App** - Implement a personal notes app with nesting, tagging, and search capabilities

**Blog Editor** - Enable blog authors to write with rich formatting, media embeds, and preview

**Knowledge Base** - Build internal documentation with organized blocks, search, and linked references

**Survey/Form Builder** - Create dynamic surveys with conditional blocks and response capture

---