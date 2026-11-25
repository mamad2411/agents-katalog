---
name: syncfusion-angular-blockeditor
description: Implement the Syncfusion Angular Block Editor component. Use this skill for block-based editing with advanced formatting, custom menus, event handling, content management, security features, globalization support, and extensive customization options for Angular applications.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Syncfusion Angular Block Editor Component

## Component Overview

The Syncfusion Angular Block Editor is a powerful block-based editor component for Angular applications. It provides a document-centric editing experience similar to modern content management systems, with extensive support for formatting, customization, and advanced features.

**Key Capabilities:**
- **Block Management** - Compose documents with various block types (paragraphs, headings, lists, tables, code, images)
- **Text Formatting** - Bold, italic, underline, strikethrough, colors, highlights, and inline styles
- **Advanced Menus** - Slash commands, context menus, inline toolbars, and block action menus
- **Events & Interactions** - Comprehensive event handling for content changes, selection, drag-drop, paste operations
- **Content Management** - Import/export as JSON, HTML, or Markdown with full serialization control
- **Methods** - Programmatically add, remove, move, and update blocks with full API access
- **Security Features** - Built-in HTML sanitization and XSS prevention for safe content
- **Toolbar Configuration** - Customizable slash commands and block action menus with grouping
- **Templates** - Custom templates for blocks, placeholders, and empty states
- **Globalization** - Multi-language support, RTL languages, and locale-based keyboard shortcuts
- **Customizable UI** - Themes, CSS variables, responsive sizing, read-only mode, and placeholder text

## Quick Navigation Guide

### Getting Started
Start here if you're new to Block Editor or need setup instructions.

**Read When**: 
- Setting up a new project with Block Editor
- Installing and importing dependencies
- Configuring CSS and basic properties
- Creating your first editor instance

👉 **[Getting Started](./references/getting-started.md)**

---

### Core Concepts
Learn the fundamental architecture and data structures.

**Read When**:
- Understanding block types and their purposes
- Learning about BlockModel and ContentModel
- Grasping how blocks are organized and related
- Understanding different content types within blocks

👉 **[Core Concepts](./references/core-concepts.md)**

---

### Block Management Methods
Programmatically manipulate editor content and structure.

**Read When**:
- Adding, removing, or moving blocks
- Updating block properties
- Querying block count and data
- Building dynamic document structures

👉 **[Block Management Methods](./references/block-management-methods.md)**

---

### Selection and Cursor Methods
Control user selection and cursor positioning.

**Read When**:
- Setting cursor position programmatically
- Selecting text or blocks
- Implementing text selection features
- Managing ranges and selections
- Execute toolbar actions programmatically (executeToolbarAction)

👉 **[Selection and Cursor Methods](./references/selection-and-cursor-methods.md)**

---

### Utility Methods
Control editor focus, toolbar state, and printing functionality.

**Read When**:
- Focusing or blurring the editor programmatically
- Enabling or disabling toolbar items dynamically
- Implementing conditional toolbar access
- Printing editor content
- Managing editor state based on user actions

👉 **[Utility Methods](./references/utility-methods.md)**

---

### Configuration Properties
Configure editor styling, security settings, users and labels.

**Read When**:
- Applying custom CSS classes for theming
- Implementing dark mode or custom themes
- Configuring HTML encoding for security
- Setting up XSS prevention
- Integrating with CSS frameworks (Bootstrap, Tailwind, Material)
- Configuring users for multi-user editing
- Adding user avatars and identification
- Implementing @mentions functionality
- Creating label/tag systems (#tags)
- Setting up project management labels
- Tracking content by user or category

👉 **[Configuration Properties](./references/configuration-properties.md)**

---

### Editor Menus
Configure slash commands, context menus, and toolbars.

**Read When**:
- Customizing the slash command menu (/)
- Adding context menu items
- Configuring block action menus
- Creating inline toolbars
- Adding custom menu items

👉 **[Editor Menus](./references/editor-menus.md)**

---

### Events and Callbacks
Handle user interactions and content changes.

**Read When**:
- Implementing auto-save functionality
- Validating content changes
- Tracking user interactions
- Responding to selection changes
- Handling paste operations

👉 **[Events and Callbacks](./references/events-and-callbacks.md)**

---

### Formatting and Styles
Apply text formatting and styling.

**Read When**:
- Making text bold, italic, underlined
- Applying colors and backgrounds
- Using advanced text styles (superscript, code, etc.)
- Formatting block types (headings, quotes, etc.)
- Creating styled content

👉 **[Formatting and Styles](./references/formatting-and-styles.md)**

---

### Data Structures and Lists
Work with list blocks and table structures.

**Read When**:
- Creating bullet or numbered lists
- Adding checklists with checkboxes
- Building tables with rows and columns
- Creating nested indented content
- Working with toggle/collapsible blocks

👉 **[Data Structures and Lists](./references/data-structures-and-lists.md)**

---

### Advanced Features
Explore undo/redo, drag-drop, code blocks, and templates.

**Read When**:
- Configuring undo/redo stack size
- Customizing drag and drop behavior
- Adding code blocks with syntax highlighting
- Creating custom template blocks
- Building complex document layouts

👉 **[Advanced Features](./references/advanced-features.md)**

---

### Data Export and Import
Convert between formats and persist content.

**Read When**:
- Exporting editor content as JSON
- Converting to HTML or Markdown
- Importing from JSON or HTML files
- Parsing external HTML content
- Printing documents
- Synchronizing with servers

👉 **[Data Export and Import](./references/data-export-and-import.md)**

---

### Keyboard Shortcuts and Globalization
Configure shortcuts and multi-language support.

**Read When**:
- Customizing keyboard shortcuts
- Setting up platform-specific shortcuts
- Implementing internationalization
- Supporting RTL languages
- Configuring language-specific settings

👉 **[Keyboard Shortcuts and Globalization](./references/keyboard-shortcuts-and-globalization.md)**

---

### Security and Paste Handling
Secure the editor and manage content pasting.

**Read When**:
- Enabling HTML sanitization
- Preventing XSS attacks
- Configuring paste cleanup rules
- Managing allowed styles and tags
- Implementing read-only mode
- Validating user input

👉 **[Security and Paste Handling](./references/security-and-paste-handling.md)**

---

### Appearance and Customization
Style and customize the editor appearance.

**Read When**:
- Setting custom width/height
- Applying themes (light, dark, high-contrast)
- Using CSS variables for styling
- Customizing fonts and typography
- Creating responsive editors
- Styling with custom CSS classes

👉 **[Appearance and Customization](./references/appearance-and-customization.md)**

---

## Quick Start Example

### 1. Install Dependencies

```bash
npm install @syncfusion/ej2-angular-blockeditor
npm install @syncfusion/ej2-angular-buttons
npm install @syncfusion/ej2-base
```

### 2. Create Component

```typescript
import { Component } from '@angular/core';
import { BlockEditorModule } from '@syncfusion/ej2-angular-blockeditor';

@Component({
  selector: 'app-editor',
  template: `<ejs-blockeditor [height]="'500px'" />`,
  standalone: true,
  imports: [BlockEditorModule]
})
export class EditorComponent {}
```

### 3. Import CSS

```css

@import '../node_modules/@syncfusion/ej2-base/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-inputs/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-popups/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-buttons/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-splitbuttons/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-navigations/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-dropdowns/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-angular-blockeditor/styles/material3.css';

```

### 4. Add to Module/Bootstrap

```typescript
// app.config.ts
import { importProvidersFrom } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

export const appConfig = {
  providers: [
    importProvidersFrom(BrowserModule)
  ]
};

// OR in app.module.ts
@NgModule({
  imports: [BlockEditorModule]
})
export class AppModule {}
```

---

## Common Patterns

### Pattern 1: Document Auto-Save

```typescript
@Component({
  selector: 'app-autosave-editor',
  template: `
    <div>
      <span>Status: {{ saveStatus }}</span>
      <ejs-blockeditor #editor (blockChanged)="onContentChange()"></ejs-blockeditor>
    </div>
  `,
  standalone: true,
  imports: [BlockEditorModule]
})
export class AutosaveEditorComponent {
  @ViewChild('editor') editor!: BlockEditorComponent;
  public saveStatus = 'Saved';
  private saveTimeout: any;

  public onContentChange(): void {
    this.saveStatus = 'Unsaved';
    clearTimeout(this.saveTimeout);
    
    this.saveTimeout = setTimeout(() => {
      const content = this.editor.getDataAsJson();
      this.saveToServer(content);
    }, 1000);
  }

  private saveToServer(content: any): void {
    // Save to backend
    this.saveStatus = 'Saved';
  }
}
```

### Pattern 2: Formatted Document Export

```typescript
@Component({
  selector: 'app-document-exporter',
  template: `
    <div>
      <button (click)="exportJson()">Export JSON</button>
      <button (click)="exportHtml()">Export HTML</button>
      <button (click)="exportMarkdown()">Export Markdown</button>
      <ejs-blockeditor #editor></ejs-blockeditor>
    </div>
  `,
  standalone: true,
  imports: [BlockEditorModule]
})
export class DocumentExporterComponent {
  @ViewChild('editor') editor!: BlockEditorComponent;

  public exportJson(): void {
    const data = this.editor.getDataAsJson();
    this.downloadFile(JSON.stringify(data, null, 2), 'document.json', 'application/json');
  }

  public exportHtml(): void {
    const html = this.editor.getDataAsHtml();
    this.downloadFile(html, 'document.html', 'text/html');
  }

  public exportMarkdown(): void {
    // Convert to markdown format
    const data = this.editor.getDataAsJson();
    const markdown = this.convertToMarkdown(data);
    this.downloadFile(markdown, 'document.md', 'text/markdown');
  }

  private downloadFile(content: string, filename: string, type: string): void {
    const blob = new Blob([content], { type });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.click();
  }

  private convertToMarkdown(blocks: any[]): string {
    // Implementation details in Data Export and Import reference
    return '';
  }
}
```

---

## Troubleshooting Guide

### Issue: Editor not displaying

**Solution**: Ensure CSS is imported in main.ts or global styles
```css

@import '../node_modules/@syncfusion/ej2-base/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-inputs/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-popups/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-buttons/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-splitbuttons/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-navigations/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-dropdowns/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-angular-blockeditor/styles/material3.css';

```

### Issue: Content not saving

**Solution**: Use `getDataAsJson()` method to retrieve content
```typescript
const content = this.blockEditor.getDataAsJson();
```

### Issue: Events not firing

**Solution**: Ensure component is standalone and imports are correct
```typescript
@Component({
  standalone: true,
  imports: [BlockEditorModule]
})
```

---
