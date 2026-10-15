---
name: syncfusion-angular-rich-text-editor
description: "Implements the Syncfusion Angular Rich Text Editor (ejs-richtexteditor) from @syncfusion/ej2-angular-richtexteditor using RichTextEditorModule, HtmlEditorService, and MarkdownEditorService.Use this skill for toolbar configuration, image/video/audio insertion, paste cleanup, AI assistant integration, emoji picker, slash menu, mentions, import/export Word/PDF, form validation, and source code view in Angular applications."
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "File Viewers & Editors"
---

# Implementing Syncfusion Angular Rich Text Editor

The Syncfusion Angular Rich Text Editor is a full-featured WYSIWYG editor that enables users to create, edit, and format rich text content. It supports HTML and Markdown editing modes, multimedia insertion, AI assistance, smart editing features, and deep customization.

## When to Use This Skill

Use this skill when you need to:
- **Content Editing UI**: Add a rich text / WYSIWYG editor to an Angular application
- **HTML or Markdown Output**: Capture formatted content as HTML or Markdown
- **Media-Rich Editors**: Allow image, audio, video, and file insertion
- **AI-Assisted Writing**: Integrate AI content generation into the editor
- **Smart Editing Features**: Add mentions, emoji picker, slash commands, or mail merge
- **Custom Toolbar**: Configure, extend, or restrict toolbar items and tools
- **Form Integration**: Use RTE with Angular Reactive or Template-driven forms
- **Document Import/Export**: Import from Word or export to PDF/Word

## Component Overview

The `<ejs-richtexteditor>` component from `@syncfusion/ej2-angular-richtexteditor` provides:
- HTML and Markdown editing modes
- Configurable toolbar (expand, multirow, scrollable, popup)
- Image, video, audio, and file insertion with upload support
- Inline, IFrame, and resizable editor variants
- Smart editing: Mentions, Emoji Picker, Slash Menu, Mail Merge
- AI assistant integration
- Import/Export (Word, PDF)
- Full accessibility (WCAG 2.1), keyboard navigation, RTL support
- Multiple themes: Tailwind 3, Material 3, Bootstrap 5, Fluent 2

## Quick Start

```typescript
import { Component } from '@angular/core';
import { RichTextEditorModule } from '@syncfusion/ej2-angular-richtexteditor';
import {
  ToolbarService, LinkService, ImageService,
  HtmlEditorService, QuickToolbarService
} from '@syncfusion/ej2-angular-richtexteditor';

@Component({
  imports: [RichTextEditorModule],
  standalone: true,
  selector: 'app-root',
  template: `<ejs-richtexteditor [(value)]="content"></ejs-richtexteditor>`,
  providers: [ToolbarService, LinkService, ImageService, HtmlEditorService, QuickToolbarService]
})
export class AppComponent {
  public content: string = '<p>Start editing here...</p>';
}
```

**CSS (styles.css):**
```css
@import '../node_modules/@syncfusion/ej2-base/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-buttons/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-inputs/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-lists/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-navigations/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-popups/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-splitbuttons/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-richtexteditor/styles/material3.css';
```

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)

**When to read:** First-time setup, installation, basic implementation, module injection

**Topics covered:**
- Installing `@syncfusion/ej2-angular-richtexteditor`
- Module imports: `RichTextEditorModule` vs `RichTextEditorAllModule`
- Service injection: all available services and what they unlock
- CSS theme imports (Material3, Tailwind3, Bootstrap5, Fluent2)
- Standalone component vs NgModule setup
- Basic `<ejs-richtexteditor>` with value binding

---

### Editor Types
📄 **Read:** [references/editor-types.md](references/editor-types.md)

**When to read:** Choosing the right editor rendering mode

**Topics covered:**
- Default (DIV-based) editor — standard use case
- IFrame editor — isolated styling, CSS encapsulation
- Inline editing — edit content directly in-page
- Resizable editor — user-resizable editor area
- Switching between HTML mode and Markdown mode
- When to choose each type

---

### Toolbar Configuration
📄 **Read:** [references/toolbar.md](references/toolbar.md)

**When to read:** Customizing toolbar layout, position, or items

**Topics covered:**
- Toolbar types: Expand, MultiRow, Scrollable, Popup (floating)
- Toolbar position: top or bottom
- Quick toolbar (image, link, table context toolbars)
- Configuring `toolbarSettings.items` array
- Disabling or enabling toolbar items dynamically
- Toolbar with separators (`|`) and line breaks

---

### Built-in and Custom Tools
📄 **Read:** [references/tools.md](references/tools.md)

**When to read:** Working with text formatting, custom toolbar items, or fullscreen

**Topics covered:**
- Built-in tools overview (all available tool names)
- Text formatting tools: Bold, Italic, FontName, FontSize, Color, Alignment
- Styling tools: Lists, Indent, Formats
- Fullscreen tool
- Creating custom toolbar tools with commands
- Styling custom tool buttons

---

### Inserting Images, Video, Audio & Files
📄 **Read:** [references/insert-image-media.md](references/insert-image-media.md)

**When to read:** Handling media insertion, uploads, or the file browser

**Topics covered:**
- Image insertion (URL, file upload, base64)
- Server-side upload handler configuration
- Image resize, alignment, and alt text
- Video insertion and embedding
- Audio insertion
- File browser integration (`FileManagerService`)
- Renaming images on server after upload
- Checking image size before insert

---

### Tables and Links
📄 **Read:** [references/table-and-links.md](references/table-and-links.md)

**When to read:** Working with tables or hyperlinks inside the editor

**Topics covered:**
- Inserting and configuring tables
- Table resize, merge, split cells, add/remove rows and columns
- Table styles and borders
- Link insertion and editing
- `insertLink` dialog configuration
- Opening links in new tab, link validation

---

### Editor Value, Selection & Commands
📄 **Read:** [references/editor-value-and-selection.md](references/editor-value-and-selection.md)

**When to read:** Programmatically reading/writing content or controlling the editor

**Topics covered:**
- Getting and setting the HTML value
- Getting and setting Markdown value
- `executeCommand` API (bold, italic, insertHTML, etc.)
- Selection range APIs: `getRange`, `setRange`
- Positioning cursor at specific location
- Capturing keyboard shortcuts to update value
- Undo/redo programmatic control

---

### Properties
📄 **Read:** [references/properties.md](references/properties.md)

**When to read:** Configuring editor behavior, appearance, or feature settings

**Topics covered:**
- AI Assistant configuration (`aiAssistantSettings`)
- Auto-save settings (`autoSaveOnIdle`)
- Color palette configuration (`backgroundColor`, `fontColor`)
- Code block and format lists
- Editor mode settings (`editorMode`, `enterKey`)
- Emoji picker configuration
- Feature flags (enableAutoUrl, enableResize, enableXhtml, etc.)
- Import/Export settings (PDF, Word)
- IFrame and inline mode configuration
- Media insertion settings (image, audio, video)
- Styling properties (cssClass, height, htmlAttributes)
- Toolbar and format configuration
- File manager integration

---

### Methods
📄 **Read:** [references/methods.md](references/methods.md)

**When to read:** Calling programmatic APIs to control the editor

**Topics covered:**
- AI Assistant methods (`addAIPromptResponse`, `clearAIPromptHistory`, `executeAIPrompt`, `getAIPromptHistory`)
- Content retrieval methods (`getHtml`, `getText`, `getXhtml`, `getContent`, `getCharCount`)
- Content manipulation (`executeCommand`, `clearUndoRedo`, `sanitizeHtml`)
- Dialog management (`showDialog`, `closeDialog`)
- Focus management (`focusIn`, `focusOut`)
- Selection methods (`getRange`, `selectRange`, `selectAll`, `getSelection`, `getSelectedHtml`)
- Toolbar management (`enableToolbarItem`, `disableToolbarItem`, `removeToolbarItem`)
- Popup and UI control (`showEmojiPicker`, `showFullScreen`, `showSourceCode`, `showInlineToolbar`, `hideInlineToolbar`, `refreshUI`)
- Component lifecycle (`destroy`)

---

### Events — Core
📄 **Read:** [references/events-core.md](references/events-core.md)

**When to read:** Handling lifecycle, action, content change, selection, dialog, popup, quick toolbar, or resize events

**Topics covered:**
- Lifecycle events (`created`, `destroyed`, `focus`, `blur`)
- Action events (`actionBegin`, `actionComplete`)
- Content change events (`change`)
- Selection events (`selectionChanged`)
- Dialog events (`beforeDialogOpen`, `dialogOpen`, `beforeDialogClose`, `dialogClose`)
- Popup events (`beforePopupOpen`, `beforePopupClose`)
- Quick toolbar events (`beforeQuickToolbarOpen`, `quickToolbarOpen`, `quickToolbarClose`)
- Resize events (`resizeStart`, `resizing`, `resizeStop`)

---

### Events — Media, Upload & Toolbar
📄 **Read:** [references/events-media-upload.md](references/events-media-upload.md)

**When to read:** Handling AI assistant, media, paste/clipboard, toolbar, upload, or import/export events

**Topics covered:**
- AI Assistant events (`aiAssistantPromptRequest`, `aiAssistantStopRespondingClick`, `aiAssistantToolbarClick`)
- Media events (`afterImageDelete`, `afterMediaDelete`, `beforeImageDrop`, `beforeMediaDrop`)
- Paste and clipboard events (`beforePasteCleanup`, `afterPasteCleanup`, `beforeClipboardWrite`)
- Toolbar events (`toolbarClick`, `updatedToolbarStatus`, `slashMenuItemSelect`)
- Upload events — image lifecycle (`beforeImageUpload`, `imageUploading`, `imageUploadSuccess`, `imageUploadFailed`, `imageSelected`, `imageRemoving`)
- Upload events — media lifecycle (`beforeFileUpload`, `fileUploading`, `fileUploadSuccess`, `fileUploadFailed`, `fileSelected`, `fileRemoving`)
- Document import/export events (`documentExporting`, `wordImporting`)

---

### Smart Editing Features
📄 **Read:** [references/smart-editing.md](references/smart-editing.md)

**When to read:** Adding mentions, emoji, slash commands, or mail merge

**Topics covered:**
- Mentions (`@user`) — configuration and data source
- Emoji picker — enabling and customizing
- Slash command menu — enabling `/` trigger commands
- Mail merge — inserting merge fields into content
- Combining multiple smart editing features

---

### AI Assistant Integration
📄 **Read:** [references/ai-assistant.md](references/ai-assistant.md)

**When to read:** Integrating AI content generation into the editor

**Topics covered:**
- AI AssistView integration overview
- `AIAssistantService` injection
- Configuring AI properties (endpoint, model, prompts)
- Custom AI prompt handling in Angular
- Toolbar AI button setup
- AI content generation and insertion workflow

---

### Clipboard and Paste Cleanup
📄 **Read:** [references/clipboard-and-paste.md](references/clipboard-and-paste.md)

**When to read:** Controlling what happens when content is pasted into the editor

**Topics covered:**
- `PasteCleanupService` — enabling paste cleanup
- Allowing/denying specific HTML tags and attributes
- Cleaning up Word and Excel paste formatting
- `ClipboardCleanupService` for copy/cut cleanup
- `afterPasteCleanup` event handling
- Configuring paste as plain text

---

### Styling and Accessibility
📄 **Read:** [references/style-and-accessibility.md](references/style-and-accessibility.md)

**When to read:** Customizing editor appearance or ensuring accessibility compliance

**Topics covered:**
- CSS class customization and theming
- Style encapsulation in IFrame mode
- Custom placeholder styling
- WCAG 2.1 compliance overview
- Keyboard navigation and shortcuts
- ARIA attributes and screen reader support
- Focus management

---

### Globalization and Localization
📄 **Read:** [references/globalization-and-i18n.md](references/globalization-and-i18n.md)

**When to read:** Supporting multiple languages, RTL, or locale-specific formatting

**Topics covered:**
- Localization setup with `L10n`
- RTL (Right-to-Left) support
- Custom locale string overrides
- Date and number formatting within the editor

---

### Import, Export & Spell Check
📄 **Read:** [references/import-export-spellcheck.md](references/import-export-spellcheck.md)

**When to read:** Importing Word documents or exporting editor content, or adding spell/grammar check

**Topics covered:**
- `ImportExportService` injection
- Importing from Word documents
- Exporting to PDF, HTML, or Word
- Spell check integration
- Grammar check integration
- Web Spell Checker plugin setup

---

### Validation and Security
📄 **Read:** [references/validation-and-security.md](references/validation-and-security.md)

**When to read:** Using the editor in forms or enforcing content security

**Topics covered:**
- Form validation with Angular Reactive forms
- Form validation with Template-driven forms
- XHTML validation
- Read-only mode
- Content sanitization
- XSS prevention strategies

---

### Integrations and How-To
📄 **Read:** [references/integrations-and-how-to.md](references/integrations-and-how-to.md)

**When to read:** Integrating third-party libraries or solving common configuration scenarios

**Topics covered:**
- CodeMirror source-code editor integration
- HighlightJS syntax highlighting for code blocks
- Embedly rich media preview integration
- Tailwind CSS preflight conflict fix
- Adding Google Fonts to font picker
- File attachments support
- RTE inside Angular Dialog component
- RTE inside Angular Tab component
- Changing default font family
- Formatting code blocks

## Common Patterns

### Two-Way Value Binding
```typescript
// Template
<ejs-richtexteditor [(value)]="htmlContent"></ejs-richtexteditor>

// Component
public htmlContent: string = '<p>Initial content</p>';
```

### One-Way Binding + Change Event
```typescript
<ejs-richtexteditor [value]="htmlContent" (change)="onChange($event)">
</ejs-richtexteditor>

onChange(args: ChangeEventArgs): void {
  this.htmlContent = args.value;
}
```

### Using with Reactive Forms
```typescript
import { FormControl, ReactiveFormsModule } from '@angular/forms';

// Template
<ejs-richtexteditor formControlName="content"></ejs-richtexteditor>

// Component
this.form = new FormGroup({
  content: new FormControl('<p></p>', Validators.required)
});
```

### Key Services Reference

| Service | What it enables |
|---|---|
| `ToolbarService` | Toolbar rendering and item management |
| `HtmlEditorService` | HTML editing mode |
| `MarkdownEditorService` | Markdown editing mode |
| `LinkService` | Hyperlink insertion and editing |
| `ImageService` | Image insertion and management |
| `TableService` | Table insertion and editing |
| `QuickToolbarService` | Floating context toolbars |
| `FileManagerService` | File browser dialog |
| `PasteCleanupService` | Paste content sanitization |
| `ResizeService` | Editor resizing handle |
| `ImportExportService` | Word/PDF import and export |
| `AIAssistantService` | AI assistant integration |
| `EmojiPickerService` | Emoji picker dialog |
| `SlashMenuService` | `/` slash command menu |
| `CodeBlockService` | Inline code block formatting |
| `AudioService` | Audio insertion |
| `VideoService` | Video insertion |
| `FormatPainterService` | Format painting (copy/apply styles) |
| `ClipboardCleanupService` | Copy/cut clipboard cleanup |
| `AutoFormatService` | Auto Markdown-to-HTML conversion |

## Related Skills
- [Syncfusion Angular Components](../../SKILL.md) — Parent library skill
