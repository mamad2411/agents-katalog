---
name: syncfusion-aspnetcore-rich-text-editor
description: "Implements the Syncfusion ASP.NET Core Rich Text Editor (ejs-richtexteditor tag helper) supporting HTML (WYSIWYG) and Markdown editing modes. Set editorMode='Markdown' for Markdown; default is HTML. Use this skill for toolbar configuration, image upload, table editing, inline or iframe mode, AI assistant integration, mentions, and form validation with rich text in ASP.NET Core projects."
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "File Viewers & Editors"
---

# Implementing the Syncfusion ASP.NET Core Rich Text Editor

The Syncfusion ASP.NET Core Rich Text Editor (`<ejs-richtexteditor>`) is a single component that supports two editing modes:

- **HTML mode** (default) — WYSIWYG editor producing valid HTML markup
- **Markdown mode** (`editorMode="Markdown"`) — plain-text markdown editor with optional HTML preview

Both modes share the same tag helper, toolbar system, events, and most features. Choose the mode based on what your output format needs to be.

## Editor Mode Decision

```
User wants to edit formatted content → output is HTML?
  └─ Use default HTML mode (no editorMode needed)

User wants to write/edit Markdown text?
  └─ Set editorMode="Markdown"
     └─ Add Marked.js for live preview (see references/markdown-features.md)
```

## When to Use This Skill

- Adding a rich text / WYSIWYG editor to an ASP.NET Core Razor page or MVC view
- Implementing a Markdown editor in ASP.NET Core
- Configuring toolbars, toolbar types, or custom toolbar tools
- Handling image, video, or audio uploads within the editor
- Inserting and managing tables
- Enabling inline editing, iframe mode, or resizable editor
- Integrating AI assistant, mentions, emoji picker, slash menu, or mail merge
- Getting, setting, or saving editor values; auto-save; character count
- Form validation with rich text content
- Read-only or disabled editor states
- XSS prevention and security
- Accessibility, keyboard support, globalization, RTL
- Handling editor events (lifecycle, focus, toolbar, upload, dialog, AI)
- Looking up available properties, types, and defaults
- Calling editor methods programmatically from JavaScript

## Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- NuGet installation and tag helper registration
- CDN stylesheet and script references
- Basic HTML editor (default mode)
- Basic Markdown editor (`editorMode="Markdown"`)
- Initial value binding via `ViewBag`
- Toolbar configuration basics

### Editor Modes & Display Options
📄 **Read:** [references/editor-modes.md](references/editor-modes.md)
- HTML mode vs Markdown mode (`editorMode` property)
- IFrame mode for isolated editing (`iframeSettings`)
- Inline editing mode (`inlineMode`)
- Resizable editor (`enableResize`)
- Setting editor height and width

### Toolbar Configuration
📄 **Read:** [references/toolbar.md](references/toolbar.md)
- Toolbar types: Expand, MultiRow, Scrollable, Popup
- Sticky / floating toolbar (`enableFloating`, `floatingToolbarOffset`)
- Toolbar position (top / bottom)
- Quick toolbar for images, links, text, and tables
- HTML mode toolbar items reference
- Markdown mode toolbar items reference

### Text Formatting
📄 **Read:** [references/text-formatting.md](references/text-formatting.md)
- Basic text styles: Bold, Italic, Underline, StrikeThrough, InlineCode
- Font name, size, color, background color
- Headings and paragraph formats
- Text alignments and indent/outdent
- Lists (ordered/unordered), blockquote, quotation formatting

### Markdown Features
📄 **Read:** [references/markdown-features.md](references/markdown-features.md)
- Full supported markdown syntax reference
- Custom markdown format configuration
- Live Markdown-to-HTML preview with Marked.js
- Table and image insertion in Markdown mode
- Mention support in Markdown mode

### Media & Links
📄 **Read:** [references/media-and-links.md](references/media-and-links.md)
- Image insertion, upload to server, drag-and-drop
- Image quick toolbar (caption, alt text, dimensions, alignment)
- Video and audio insertion
- Link insertion and quick toolbar
- File browser integration

### Tables
📄 **Read:** [references/table.md](references/table.md)
- Inserting tables and configuring the CreateTable tool
- Table quick toolbar (rows, columns, merge, split, styles)
- Cell properties, background color, alignment
- Nesting tables
- Table selection and copy/paste

### Smart Editing Features
📄 **Read:** [references/smart-editing.md](references/smart-editing.md)
- Emoji picker
- Slash menu
- Mentions integration with the Mention component
- Mail merge
- Format painter
- Code block formatting

### AI Assistant
📄 **Read:** [references/ai-assistant.md](references/ai-assistant.md)
- Enabling AICommands and AIQuery toolbar items
- Streaming and non-streaming AI response handling
- `AiAssistantPromptRequest` event
- `addAIPromptResponse` method

### Editor Value & Content Management
📄 **Read:** [references/editor-value.md](references/editor-value.md)
- Getting and setting HTML/Markdown values
- `getHtml()`, `getText()`, `getCharCount()` methods
- Auto-save with `saveInterval`
- Placeholder text
- Character count (`showCharCount`, `maxLength`)
- HTML-encoded value (`enableHtmlEncode`)
- Source code / code view editing
- Paste and clipboard cleanup
- Import and export (Word/PDF)
- Undo/redo management

### Validation & Security
📄 **Read:** [references/validation-security.md](references/validation-security.md)
- Form validation integration (`FormValidator`)
- Read-only mode (`readonly`)
- Disable editor (`enabled`)
- XSS prevention (`enableHtmlSanitizer`, `beforeSanitizeHtml`)
- XHTML validation
- Style encapsulation

### Customization
📄 **Read:** [references/customization.md](references/customization.md)
- Custom toolbar tools (template-based buttons)
- Built-in toolbar items reference
- CSS styling and theme customization
- Enter key / Shift+Enter key behavior (`enterKey`, `shiftEnterKey`)
- `execCommand` API for programmatic formatting
- Third-party integrations (CodeMirror)
- `enableToolbarItem` / `disableToolbarItem` methods

### Accessibility & Globalization
📄 **Read:** [references/accessibility-globalization.md](references/accessibility-globalization.md)
- WCAG 2.2 AA compliance
- ARIA roles and attributes
- Keyboard shortcuts (HTML and Markdown modes)
- Localization and globalization (`locale`, `enableRtl`)

### Events
📄 **Read:** [references/events.md](references/events.md)
- Lifecycle events: `Created`, `Destroyed`
- Focus/blur events: `Focus`, `Blur`, `Change`
- Toolbar/command events: `ActionBegin`, `ActionComplete`
- Paste/clipboard events: `BeforePasteCleanup`, `AfterPasteCleanup`, `BeforeClipboardWrite`
- Dialog events: `BeforeDialogOpen`, `DialogOpen`, `BeforeDialogClose`, `DialogClose`
- Popup events: `BeforePopupOpen`, `BeforePopupClose`, `BeforeQuickToolbarOpen`
- Image upload events: `ImageSelected`, `BeforeImageUpload`, `ImageUploading`, `ImageUploadSuccess`, `ImageUploadFailed`, `ImageRemoving`, `AfterImageDelete`, `BeforeImageDrop`
- Media upload events: `FileSelected`, `BeforeFileUpload`, `FileUploading`, `FileUploadSuccess`, `FileUploadFailed`, `FileRemoving`, `AfterMediaDelete`, `BeforeMediaDrop`
- Security events: `BeforeSanitizeHtml`
- Export events: `DocumentExporting`
- AI Assistant events: `AiAssistantPromptRequest`, `AiAssistantStopRespondingClick`, `AiAssistantToolbarClick`

### Properties
📄 **Read:** [references/properties.md](references/properties.md)
- Complete property reference with types, defaults, and descriptions
- Core properties: `Value`, `EditorMode`, `Placeholder`, `CssClass`, `Locale`
- State flags: `Enabled`, `Readonly`, `EnableResize`, `EnablePersistence`, `EnableRtl`, `EnableTabKey`
- Content & encoding: `EnableHtmlEncode`, `EnableHtmlSanitizer`, `EnableXhtml`, `EnableAutoUrl`, `EnableClipboardCleanup`
- Character count & auto-save: `ShowCharCount`, `MaxLength`, `SaveInterval`, `AutoSaveOnIdle`
- Key behavior: `EnterKey`, `ShiftEnterKey`, `FloatingToolbarOffset`
- Undo/redo: `UndoRedoSteps`, `UndoRedoTimer`
- Complex settings objects: `ToolbarSettings`, `QuickToolbarSettings`, `IframeSettings`, `InlineMode`, `InsertImageSettings`, `InsertVideoSettings`, `InsertAudioSettings`, `PasteCleanupSettings`, `TableSettings`, `FontFamily`, `FontColor`, `BackgroundColor`, `Format`, `SlashMenuSettings`, `EmojiPickerSettings`, `FormatPainterSettings`, `CodeBlockSettings`, `AiAssistantSettings`, `ImportWordSettings`, `ExportWordSettings`, `ExportPdfSettings`, `FileManagerSettings`

### Methods
📄 **Read:** [references/methods.md](references/methods.md)
- Content methods: `getHtml()`, `getText()`, `getContent()`, `getSelectedHtml()`, `getXhtml()`, `getCharCount()`, `selectAll()`, `selectRange()`, `print()`
- Command execution: `executeCommand()` with full `CommandName` enum reference
- Toolbar methods: `enableToolbarItem()`, `disableToolbarItem()`, `removeToolbarItem()`
- Focus methods: `focusIn()`, `focusOut()`
- Inline toolbar: `showInlineToolbar()`, `hideInlineToolbar()`
- Dialog methods: `showDialog()`, `closeDialog()`
- Undo/redo: `clearUndoRedo()`
- Source code: `showSourceCode()`
- Full screen: `showFullScreen()`
- Emoji picker: `showEmojiPicker()`
- AI Assistant: `addAIPromptResponse()`, `executeAIPrompt()`, `getAIPromptHistory()`, `clearAIPromptHistory()`, `showAIAssistantPopup()`, `hideAIAssistantPopup()`
- Lifecycle: `refresh()`, `refreshUI()`, `dataBind()`, `destroy()`
- Security: `sanitizeHtml()`

---

## Quick Start

### HTML Editor (default)

```razor
<!-- _ViewImports.cshtml -->
@addTagHelper *, Syncfusion.EJ2

<!-- _Layout.cshtml <head> -->
<link rel="stylesheet" href="https://cdn.syncfusion.com/ej2/{{ site.ej2version }}/fluent.css" />
<script src="https://cdn.syncfusion.com/ej2/{{ site.ej2version }}/dist/ej2.min.js"></script>

<!-- _Layout.cshtml <body> end -->
<ejs-scripts></ejs-scripts>

<!-- Index.cshtml -->
<ejs-richtexteditor id="editor" value="@ViewBag.value">
    <e-richtexteditor-toolbarsettings items="@ViewBag.tools"></e-richtexteditor-toolbarsettings>
</ejs-richtexteditor>
```

```csharp
// HomeController.cs
public ActionResult Index()
{
    ViewBag.value = "<p>Start editing here...</p>";
    ViewBag.tools = new[] {
        "Bold", "Italic", "Underline", "|",
        "Formats", "Alignments", "OrderedList", "UnorderedList", "|",
        "CreateLink", "Image", "CreateTable", "|",
        "SourceCode", "|", "Undo", "Redo"
    };
    return View();
}
```

### Markdown Editor

```razor
<ejs-richtexteditor id="markdown-editor" editorMode="Markdown" value="@ViewBag.value">
    <e-richtexteditor-toolbarsettings items="@ViewBag.tools"></e-richtexteditor-toolbarsettings>
</ejs-richtexteditor>
```

```csharp
public ActionResult Index()
{
    ViewBag.value = "**Hello World** — start writing *markdown* here.";
    ViewBag.tools = new[] {
        "Bold", "Italic", "StrikeThrough", "InlineCode", "|",
        "Formats", "Blockquote", "OrderedList", "UnorderedList", "|",
        "CreateLink", "Image", "CreateTable", "|", "Undo", "Redo"
    };
    return View();
}
```

---

## Common Patterns

### Read editor value on form submit

```razor
<form id="form-element">
    <ejs-richtexteditor id="rte" name="rteContent" value="@ViewBag.value"></ejs-richtexteditor>
    <button type="submit">Submit</button>
</form>
<script>
    document.querySelector('form').onsubmit = function () {
        var rte = document.getElementById('rte').ej2_instances[0];
        console.log(rte.getHtml());
    };
</script>
```

### Image upload to server

```razor
<ejs-richtexteditor id="editor">
    <e-richtexteditor-insertimagesettings
        saveUrl="/Home/SaveImage"
        removeUrl="/Home/RemoveImage"
        path="./Uploads/">
    </e-richtexteditor-insertimagesettings>
</ejs-richtexteditor>
```

### Inline editing

```razor
<ejs-richtexteditor id="inline" value="@ViewBag.value">
    <e-richtexteditor-inlinemode enable="true" onSelection="true"></e-richtexteditor-inlinemode>
</ejs-richtexteditor>
```

### Character count with limit

```razor
<ejs-richtexteditor id="editor" showCharCount="true" maxLength="500" value="@ViewBag.value">
</ejs-richtexteditor>
```
