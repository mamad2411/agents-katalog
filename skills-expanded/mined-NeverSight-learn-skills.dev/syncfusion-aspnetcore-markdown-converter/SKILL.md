---
name: syncfusion-aspnetcore-markdown-converter
description: Guides implementation of the Syncfusion ASP.NET Core Markdown Converter (Syncfusion.EJ2 NuGet). Use this skill when the user needs to convert Markdown text to HTML, use the MarkdownConverter toHtml method, configure MarkdownConverterOptions (async, gfm, lineBreak, silence), or integrate the Markdown Converter with the Syncfusion Rich Text Editor tag helper for live preview or side-by-side editing in ASP.NET Core MVC or Razor Pages projects. Trigger when user mentions markdown to HTML conversion, MarkdownConverter, toHtml, ej2-markdown-converter, markdown preview, or RTE markdown mode.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "File Viewers & Editors"
---

# Syncfusion ASP.NET Core Markdown Converter

The Syncfusion ASP.NET Core Markdown Converter is a lightweight client-side utility (loaded via CDN or npm) that transforms Markdown text into clean, semantic HTML. It supports all common Markdown elements — headings, lists, tables, links, images, and inline styles — and integrates seamlessly with the Syncfusion Rich Text Editor tag helper (`<ejs-richtexteditor>`) for live editing and preview workflows in ASP.NET Core MVC or Razor Pages applications.

---

## Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- NuGet installation and tag helper registration
- CDN stylesheet and script references
- Running a basic Markdown-to-HTML conversion in a Razor view
- Required CSS and theme setup

### toHtml API
📄 **Read:** [references/tohtml-api.md](references/tohtml-api.md)
- `toHtml` method signature and parameters (JavaScript usage from Razor views)
- Supported Markdown elements (headings, lists, tables, links, images, inline styles)
- Return value and usage patterns
- Simple conversion code examples

### Configurable Options
📄 **Read:** [references/configurable-options.md](references/configurable-options.md)
- `MarkdownConverterOptions` object
- `async` — asynchronous conversion for large content
- `gfm` — GitHub Flavored Markdown support
- `lineBreak` — single line breaks as `<br>` elements
- `silence` — suppress errors on invalid Markdown
- When and why to use each option

### Rich Text Editor Integration
📄 **Read:** [references/richtexteditor-integration.md](references/richtexteditor-integration.md)
- Combining `<ejs-richtexteditor>` (editorMode="Markdown") with MarkdownConverter
- Live preview on keyup using `toHtml`
- Full preview toggle pattern
- Side-by-side Splitter layout
- Toolbar configuration for Markdown mode

---

## Quick Start

Register the tag helper and add CDN references, then run a minimal conversion:

```razor
{{! _ViewImports.cshtml }}
@addTagHelper *, Syncfusion.EJ2
```

```html
{{! _Layout.cshtml <head> }}
<link rel="stylesheet" href="https://cdn.syncfusion.com/ej2/{{ site.ej2version }}/fluent.css" />
<script src="https://cdn.syncfusion.com/ej2/{{ site.ej2version }}/dist/ej2.min.js"></script>

{{! _Layout.cshtml before </body> }}
<ejs-scripts></ejs-scripts>
```

```javascript
// Inline script in Razor view or a linked .js file
var markdownContent = '# Hello World\nThis is **Markdown** text.';
var htmlOutput = ej.markdownconverter.MarkdownConverter.toHtml(markdownContent);
console.log(htmlOutput);
// Output: <h1>Hello World</h1><p>This is <strong>Markdown</strong> text.</p>
```

---

## Common Patterns

### Convert with all options enabled

```javascript
var html = ej.markdownconverter.MarkdownConverter.toHtml(markdownContent, {
  async: true,      // Non-blocking for large content
  gfm: true,        // GitHub Flavored Markdown
  lineBreak: true,  // Treat single newlines as <br>
  silence: true     // Suppress parse errors
});
```

### Live preview on user input

```javascript
document.getElementById('textarea').addEventListener('keyup', function () {
  document.getElementById('preview').innerHTML =
    ej.markdownconverter.MarkdownConverter.toHtml(this.value);
});
```

### Integrate with Syncfusion RTE tag helper in Markdown mode

```razor
<ejs-richtexteditor id="markdown-editor" editorMode="Markdown" value="@ViewBag.value">
    <e-richtexteditor-toolbarsettings items="@ViewBag.tools"></e-richtexteditor-toolbarsettings>
</ejs-richtexteditor>
```

```csharp
// HomeController.cs
public ActionResult Index()
{
    ViewBag.value = "# Hello\nType **Markdown** here.";
    ViewBag.tools = new[] {
        "Bold", "Italic", "StrikeThrough", "|",
        "Formats", "Blockquote", "OrderedList", "UnorderedList", "|",
        "CreateLink", "Image", "CreateTable", "|", "Undo", "Redo"
    };
    return View();
}
```

---

## Key Props

| Option | Type | Default | Purpose |
|--------|------|---------|---------|
| `async` | `boolean` | `false` | Async conversion for large payloads |
| `gfm` | `boolean` | `true` | GitHub Flavored Markdown support |
| `lineBreak` | `boolean` | `false` | Single newlines → `<br>` |
| `silence` | `boolean` | `false` | Skip invalid Markdown instead of throwing |

---

## Common Use Cases

- **Static content rendering** — Convert user-authored Markdown from a textarea or controller action into HTML for display in a Razor view
- **Live editor preview** — Pair with the Syncfusion RTE tag helper in Markdown mode for real-time HTML preview
- **Side-by-side editing** — Use the Syncfusion Splitter tag helper to show editor and rendered HTML simultaneously
- **CMS / documentation tools** — Process Markdown stored in a database or files before rendering inside a Razor partial view
