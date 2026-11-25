---
name: syncfusion-javascript-pdf-viewer
description: Implements the Syncfusion Javascript (ES6) is case-sensitive PDF Viewer (PdfViewer) for embedding, configuring, and loading PDF documents. Use this when rendering PDFs in a TypeScript application using the EJ2 class-based approach, embedding viewer controls, or generating TypeScript and HTML code for PDF display and interaction.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Syncfusion TypeScript PdfViewer – UI Sample Generator

## Generate Code for the User's Project *(default)*

**Trigger keywords:** "how to", "add pdfviewer", "code sample", "show me", "example", "snippet", "integrate", "component", "create sample", "typescript sample".

**Purpose:** Generate minimal, copy-pasteable TypeScript (`.ts`) and HTML code that the user can integrate directly into their TypeScript EJ2 project.

**Workflow:**
**⚠️ CRITICAL — Feature Support Policy (STRICT MODE):**
 
**FUNDAMENTAL RULE:** Only generate code using APIs and properties that are EXPLICITLY listed in the reference files. ANY deviation is a VIOLATION.
 
- **MANDATORY CHECKS BEFORE GENERATING ANY CODE:**
  1. Search the reference files for the exact API/property name
  2. Verify it appears in the Method Reference, Properties, or Events tables
  3. If NOT found in ANY reference file, STOP immediately
  4. Do NOT generate or suggest undocumented APIs under any circumstances
 
- **STRICT ENFORCEMENT - ZERO TOLERANCE:**
  - **NO custom properties** - Only use properties from reference file tables
  - **NO invented methods** - Only use methods from reference file tables
  - **NO workarounds with undefined APIs** - Forbidden
  - **NO assumptions** about undocumented behavior - Forbidden
  - **NO alternative implementations** using guess-work - Forbidden
  - **NO pretending support exists** - Forbidden
 
- **MANDATORY RESPONSE FOR UNSUPPORTED FEATURES:**
  - **If a requested scenario/feature/API is NOT listed in any reference file, you MUST respond with:**
    ```
    "This feature is not supported in the current Syncfusion TypeScript PDF Viewer implementation."
    ```
  - **Then list what IS supported** from the appropriate reference file
  - **Never suggest alternatives** unless explicitly documented in reference files
 
- **REFERENCE FILE HIERARCHY:**
  - Each reference file contains complete, authoritative documentation for its domain
  - The tables (Method Reference, Properties, Events) are the SOURCE OF TRUTH
  - Content outside these tables in reference files is explanatory only
  - Do NOT extend beyond what appears in the reference file tables
 
- **AUDIT YOUR GENERATION:**
  - Before providing any code, verify EVERY API used appears in a reference file table
  - Document which reference file each API comes from
  - If you cannot cite a reference file table entry, DELETE that code
 
- **This is a CRITICAL REQUIREMENT.** Violations compromise the skill's integrity and reliability.
 
#### Step 1 — Detect the Application Type *(REQUIRED - DO NOT SKIP)*
- **Use file_search and read_file tools to inspect workspace project files:**
  - `package.json` (check for `@syncfusion/ej2-pdfviewer` or `@syncfusion/ej2` dependency)
  - `tsconfig.json` (TypeScript configuration)
  - `webpack.config.js` (EJ2 quickstart uses webpack)
  - `src/index.ts` or `src/app.ts` (main TypeScript entry point)
  - `src/index.html` (HTML container file)
- **Output:** Confirm the detected application type is a **TypeScript EJ2 webpack project** (NOT a React/Vue/Angular project) before proceeding.
- **CRITICAL:** This skill generates **vanilla TypeScript** code using the EJ2 `PdfViewer` class. Do NOT generate React, Angular, or Vue component code.
 
#### Step 2 — Generate Code from Reference Files Only *(REQUIRED)*
- **Before generating:** Confirm that Step 1 is complete
- Read the relevant `references/*.md` file(s) for the requested feature
- Cross-reference EVERY API, property, and method against these tables
- **CLASS-BASED APPROACH (MANDATORY - TypeScript EJ2 PATTERNS ONLY):**
  - Import `PdfViewer` and required module classes from `@syncfusion/ej2-pdfviewer`
  - Use `PdfViewer.Inject(...)` to inject required feature modules
  - Instantiate with `new PdfViewer({ ... })` or `new PdfViewer()` and set properties
  - Mount to DOM using `viewer.appendTo('#ElementId')`
  - **NEVER use JSX, TSX, React hooks, or component-based syntax**
  - **NEVER use `<PdfViewerComponent>`, `<Inject services={...}>`, `useState`, `useRef`, or `useEffect`**
- **MANDATORY:** Before generating ANY code, verify that reference files exist and are accessible
- **Read the appropriate reference file(s)** for the requested feature:
  - Use `read_file` tool on relevant `references/*.md` files
  - Confirm file contains Methods/Properties/Events tables
  - Verify tables are complete and readable
- **If reference file is missing or cannot be read:**
  - STOP code generation
  - Respond: "Reference file for this feature is not available. Please ensure all reference files are present in the `references/` directory."
  - List the missing reference file name
- **This is a BLOCKER step:** Cannot proceed without reference file validation
- If an API/property does NOT appear in the reference file table, DO NOT USE IT
- Do NOT invent, guess, or suggest any API, method, property, class, or namespace not explicitly present in the reference files
 
---

## 🔄 DOCUMENT LIFECYCLE REQUIREMENTS (CRITICAL)

### When to Use `documentLoad` Event

Certain operations MUST be performed inside the `documentLoad` event callback, not immediately after instantiation:

**Operations that REQUIRE `documentLoad`:**
- ✅ Adding form fields programmatically (`formDesigner.addFormField()`)
- ✅ Adding annotations (`annotation.addAnnotation()`)
- ✅ Accessing form field collections (`formFieldCollections`)
- ✅ Accessing document metadata
- ✅ Modifying document-dependent properties

**Operations safe at instantiation time:**
- ✅ Setting `enableToolbar`, `enableAnnotation`, etc.
- ✅ Setting viewer properties like `width`, `height`
- ✅ Configuring settings objects

### Example: Correct Timing for Form Fields

**❌ WRONG - Causes "formFieldCollections.findIndex is not a function":**
```typescript
let pdfviewer = new PdfViewer({
  documentPath: 'https://...',
  resourceUrl: 'https://...'
});
pdfviewer.appendTo('#PdfViewer');

// ERROR! formFieldCollections not yet initialized
pdfviewer.formDesigner.addFormField('Textbox', { ... });
```

**✅ CORRECT - Inside documentLoad callback:**
```typescript
let pdfviewer = new PdfViewer({
  documentPath: 'https://...',
  resourceUrl: 'https://...',
  documentLoad: () => {
    // SAFE - Document fully loaded, formFieldCollections initialized
    pdfviewer.formDesigner.addFormField('Textbox', { ... });
  }
});
pdfviewer.appendTo('#PdfViewer');
```

---

## ⚙️ SETTINGS CONFIGURATION BEST PRACTICES

**When generating code with settings (toolbarSettings, annotationSettings, annotationSelectorSettings, arrowSettings, rectangleSettings, etc.), follow these guidelines:**

### Rule 1: Simple Settings → Pass directly to the PdfViewer constructor

**Use this approach when:**
- Configuring only 1-3 properties
- Settings are straightforward without complex enums or custom types

**Example (DO THIS):**
```typescript
import { PdfViewer, Toolbar, Annotation } from '@syncfusion/ej2-pdfviewer';

PdfViewer.Inject(Toolbar, Annotation);

let pdfviewer: PdfViewer = new PdfViewer({
  documentPath: 'https://cdn.syncfusion.com/content/pdf/pdf-succinctly.pdf',
  resourceUrl: 'https://cdn.syncfusion.com/ej2/31.1.23/dist/ej2-pdfviewer-lib',
  annotationSelectorSettings: {
    selectionBorderColor: '#0000ff',
    resizerBorderColor: '#ff0000',
    resizerSize: 8
  }
});
pdfviewer.appendTo('#PdfViewer');
```

**Benefits:**
- ✅ No extra imports needed
- ✅ Simple and readable
- ✅ Less code clutter
- ✅ Type checking still works

---

### Rule 2: Complex Settings → Define as Typed Constant (OUTSIDE instantiation)

**Use this approach when:**
- Configuring 4+ properties OR multiple related settings
- Using enums or complex configurations
- Need to reuse the same configuration in multiple places
- Settings are complex enough to warrant separate definition

**Example (DO THIS ONLY FOR COMPLEX CASES):**

```typescript
import { PdfViewer, Toolbar, Annotation, AnnotationResizerLocation, CursorType } from '@syncfusion/ej2-pdfviewer';
import { AnnotationSelectorSettingsModel } from '@syncfusion/ej2-pdfviewer';

PdfViewer.Inject(Toolbar, Annotation);

// Define constant OUTSIDE instantiation with proper types and enums
const annotationSelectorConfig: AnnotationSelectorSettingsModel = {
  selectionBorderColor: '#0000ff',
  selectionBorderThickness: 2,
  resizerBorderColor: '#ff0000',
  resizerFillColor: '#4070ff',
  resizerSize: 8,
  resizerShape: 'Square',
  selectorLineDashArray: [5, 6],
  resizerLocation: AnnotationResizerLocation.Corners | AnnotationResizerLocation.Edges,
  resizerCursorType: CursorType.grab
};

let pdfviewer: PdfViewer = new PdfViewer({
  documentPath: 'https://cdn.syncfusion.com/content/pdf/pdf-succinctly.pdf',
  resourceUrl: 'https://cdn.syncfusion.com/ej2/31.1.23/dist/ej2-pdfviewer-lib',
  annotationSelectorSettings: annotationSelectorConfig
});
pdfviewer.appendTo('#PdfViewer');
```

**When to import types and enums:**
- [ ] Import model types (e.g., `AnnotationSelectorSettingsModel`) for TypeScript type checking
- [ ] Import any enums used in the settings (e.g., `AnnotationResizerLocation`, `CursorType`)
- [ ] Keep imports minimal - import ONLY what is used

**Benefits:**
- ✅ Type-safe configuration
- ✅ Proper enum usage
- ✅ Reusable across multiple viewer instances
- ✅ Clean instantiation code

---

### Rule 3: NEVER Over-Engineer Simple Cases

**❌ DO NOT DO THIS (Over-engineered):**
```typescript
import { PdfViewer, Toolbar } from '@syncfusion/ej2-pdfviewer';
import { ToolbarSettingsModel } from '@syncfusion/ej2-pdfviewer';

PdfViewer.Inject(Toolbar);

// Unnecessary constant for 2 simple properties
const toolbarSettings: ToolbarSettingsModel = {
  showTooltip: true
};

let pdfviewer: PdfViewer = new PdfViewer({
  toolbarSettings: toolbarSettings
});
pdfviewer.appendTo('#PdfViewer');
```

**✅ DO THIS INSTEAD (Simple & Clean):**
```typescript
import { PdfViewer, Toolbar } from '@syncfusion/ej2-pdfviewer';

PdfViewer.Inject(Toolbar);

let pdfviewer: PdfViewer = new PdfViewer({
  documentPath: 'https://cdn.syncfusion.com/content/pdf/pdf-succinctly.pdf',
  resourceUrl: 'https://cdn.syncfusion.com/ej2/31.1.23/dist/ej2-pdfviewer-lib',
  toolbarSettings: { showTooltip: true }
});
pdfviewer.appendTo('#PdfViewer');
```

---

### Checklist Before Generating Code

- [ ] **Count the settings properties:** 1-3? → Pass inline in constructor | 4+? → Extract to typed constant
- [ ] **Are enums involved?** Yes → Must use typed constant with enum imports | No → Can pass inline
- [ ] **Is it reused elsewhere?** Yes → Use constant | No → Prefer inline
- [ ] **Do I need type safety?** Yes → Import the model type | No → Skip model type import
- [ ] **Do I need enums?** Yes → Import required enums from `@syncfusion/ej2-pdfviewer` | No → Skip enum imports
- [ ] **Package name correct?** Always import from `@syncfusion/ej2-pdfviewer` — NEVER from `@syncfusion/ej2-typescript-pdfviewer`

---

### Code References

All templates and operation snippets live in `references/*.md`. Each file is a focused snippet or template the agent will combine when generating samples.

**Flow:** Always start with `references/basic-sample.md`, then merge matched features into its anchors. If no keyword matches, return only the basic sample.

---

## Reference File Routing Guide

### 🎯 Core Setup & Configuration

| File | Purpose | **Route When User Asks About** |
|---|---|---|
| **basic-sample.md** | Minimal PdfViewer setup: clone quickstart, install packages, import CSS, create `PdfViewer` instance with `documentPath` and `resourceUrl`, and `appendTo` HTML container. | "basic setup", "minimal example", "getting started", "how to load PDF" |
| **general-properties.md** | Configure core viewer properties (width, height, document path, locale, resourceUrl, serviceUrl, AJAX settings, scroll settings, commandManager). | "configuration", "server settings", "locale", "document path setup", "width height" |
| **enable-properties.md** | Enable/disable specific features (toolbar, annotations, forms, navigation, text selection, download, print). | "disable toolbar", "hide features", "enable/disable", "read-only mode", "restrict features" |

### 📐 Navigation & Page Management

| File | Purpose | **Route When User Asks About** |
|---|---|---|
| **page-navigation.md** | Navigate between pages (first, last, next, previous page), go to specific page numbers. | "page navigation", "go to page", "next page", "previous page", "jump to page" |
| **bookmark-navigation.md** | Navigate using PDF bookmarks/table of contents in the bookmark panel. **CRITICAL: Bookmark API methods are accessed on the `pdfviewer` instance directly (e.g., `pdfviewer.bookmark.openBookmarkPane()`). Requires `BookmarkView` to be injected and `enableBookmark: true`.** | "bookmarks", "bookmark", "table of contents", "TOC navigation", "outline panel", "get bookmarks", "retrieve bookmarks", "fetch bookmarks", "bookmarks programmatically", "getBookmarks", "goToBookmark", "bookmark API", "list bookmarks", "open bookmark", "close bookmark" |
| **hyperlink-navigation.md** | Configure hyperlink navigation behavior and external link handling in PDFs. | "hyperlinks", "external links", "URL navigation", "clickable links", "url", "link" |
| **thumbnail-navigation.md** | Display and navigate using page thumbnails in the thumbnail panel. | "thumbnails", "preview pages", "thumbnail panel", "thumbnail", "page previews" |

### � Comments & Panels

| File | Purpose | **Route When User Asks About** |
|---|---|---|
| **general-properties.md** | Configure core viewer properties including `isCommandPanelOpen` to show/hide the comments panel programmatically. See "Controlling Command Panel (Comments Panel)" section. **REQUIREMENT:** Set `enableAnnotation: true` for the command panel to be functional. **PROPERTY:** `isCommandPanelOpen` is read/write boolean (not read-only). | "show comments panel", "hide comments panel", "toggle comments", "command panel", "show/hide comments", "isCommandPanelOpen", "comments panel", "annotation comments" |

### �🔍 Viewing & Interaction

| File | Purpose | **Route When User Asks About** |
|---|---|---|
| **magnification.md** | Configure zoom levels, zoom modes, and magnification controls (fit-to-page, fit-to-width). | "zoom", "magnification", "fit to page", "zoom levels", "scale document" |
| **interaction-mode.md** | Switch between Selection mode (text selection) and Panning mode (touch scrolling). | "text selection", "panning", "scroll mode", "interaction mode", "touch navigation" |
| **text-selection.md** | Enable text selection, copying text, and text selection events. | "select text", "copy text", "highlight text to copy", "text selection mode" |
| **text-search.md** | Implement text search functionality with search options and navigation. | "search text", "find in PDF", "search functionality", "highlight search results" |

### 🛠️ Toolbar & Context Menu

#### Toolbar Configuration

| File | Purpose | **Route When User Asks About** |
|---|---|---|
| **toolbar-settings.md** | Configure toolbar visibility, tooltip behavior, and customize/remove toolbar items using `toolbarSettings`. | "customize toolbar", "hide toolbar items", "remove toolbar buttons", "toolbar configuration" |
| **toolbar-methods.md** | Programmatically show/hide toolbars and enable/disable toolbar items at runtime using methods like `showToolbar()`. | "show/hide toolbar dynamically", "toggle toolbar", "enable/disable toolbar items programmatically" |

##### ⚠️ STRICT VALIDATION FOR TOOLBAR ITEM NAMES

**When generating toolbar configurations, you MUST follow these rules to prevent incorrect toolbar item names:**

1. **ALWAYS reference exact item names from `toolbar-settings.md`**
   - Do NOT invent, guess, or assume toolbar item names
   - Do NOT apply naming pattern logic to derive names
   - Use ONLY names listed in the "Available Primary Toolbar Items", "Available Annotation Toolbar Items", and "Available Form Designer Items" sections in `toolbar-settings.md`

2. **VALIDATE item names character-by-character**
   - Case sensitivity matters: `HighlightTool` ≠ `HighlightOption`
   - Exact names only: `AnnotationEditTool` ≠ `AnotatetionEditTool`
   - No abbreviations or shortcuts

3. **Before generating toolbar configuration code:**
   - [ ] Open `toolbar-settings.md` reference file
   - [ ] Locate: "Available Primary Toolbar Items" section
   - [ ] Locate: "Available Annotation Toolbar Items" section
   - [ ] Locate: "Available Form Designer Items" section
   - [ ] Copy exact names from THESE SECTIONS ONLY
   - [ ] Cross-check every single item name character-by-character
   - [ ] If ANY item name is not in the reference sections, DO NOT USE IT
   - [ ] Consult the "❌ COMMON MISTAKES TO AVOID" table in `toolbar-settings.md` if unsure

4. **Common errors to prevent:**
   - ❌ `AnotatetionEditTool` → ✅ `AnnotationEditTool` (typo)
   - ❌ `CalibrationOption` → ✅ `CalibrateTool` (wrong suffix)
   - ❌ `ShapeAnnotationOption` → ✅ `ShapeTool` (annotation toolbar version)
   - ❌ `InkAnnotationOption` → ✅ `InkAnnotationTool` (annotation toolbar version)
   - For complete list of mistakes to avoid, see `toolbar-settings.md` "❌ COMMON MISTAKES TO AVOID" table

#### Context Menu Customization

| File | Purpose | **Route When User Asks About** |
|---|---|---|
| **context-menu.md** | Customize context menu items and handle context menu events. | "right-click menu", "context menu", "custom context menu", "disable context menu items" |

### 📝 Annotations

| File | Purpose | **Route When User Asks About** |
|---|---|---|
| **annotation-settings.md** | Configure annotation appearance (colors, opacity, styles) and behavior for all annotation types. | "annotation colors", "annotation styles", "customize annotation appearance", "annotation defaults" |
| **annotation-events.md** | Handle annotation lifecycle events (add, delete, move, resize, select, property change). | "annotation events", "when annotation is added", "annotation change detection", "annotation callbacks" |
| **shape-label-settings.md** | Customize shape and measure annotation labels (position, color, font, visibility). | "annotation labels", "shape labels", "measurement labels", "label customization" |
| **redaction-annotation.md** | Create, configure, and apply redaction annotations to permanently remove sensitive content. | "redaction", "redact content", "remove sensitive data", "black out text", "permanent removal" |

### 📄 Forms

| File | Purpose | **Route When User Asks About** |
|---|---|---|
| **form-field-settings.md** | Configure default properties for form fields (text, checkbox, radio, dropdown, signature). Use `TextFieldSettings`, `CheckBoxFieldSettings`, `RadioButtonFieldSettings`, etc. for proper type casting. **CRITICAL:** Form field bounds use capitalized properties (X, Y, Width, Height), NOT lowercase. **TIMING CRITICAL:** Always add form fields inside the `documentLoad` event callback - calling before document loads causes "formFieldCollections is not a function" error. | "form field defaults", "form field styles", "configure form fields", "form field properties", "add text field", "add form field", "add textbox", "add checkbox", "programmatically add field", "addFormField", "TextFieldSettings" |
| **form-field-events.md** | Handle form field interaction events (focus, blur, value change, validation). | "form field events", "when field changes", "form validation events", "field interaction callbacks" |

### 📋 Document Actions

| File | Purpose | **Route When User Asks About** |
|---|---|---|
| **download.md** | Enable/configure PDF download functionality with custom filenames. | "download PDF", "save PDF", "export document", "download button" |
| **print.md** | Configure and trigger PDF printing functionality. | "print PDF", "print document", "printing options", "print button" |
| **organize-pages.md** | Reorder, rotate, insert, remove, copy, import, and extract PDF pages. | "reorder pages", "rotate pages", "add blank pages", "remove pages", "rearrange pages", "merge PDFs" |

### ⚙️ Advanced Features

| File | Purpose | **Route When User Asks About** |
|---|---|---|
| **api-methods.md** | Programmatic control: load documents, manage forms, annotations, extract text, undo/redo, navigation APIs. | "load PDF programmatically", "API methods", "export form data", "extract text", "undo/redo", "programmatic control" |
| **events.md** | Complete list of all PdfViewer events (document load, download, annotations, forms, search, navigation). | "event list", "all events", "available events", "event reference", "event handlers" |

---

## Common Pitfalls and Corrections

- Extract Pages API location: `extractPages()` is a method of `PdfViewer`, not of `pageOrganizer`. Call `pdfviewer.extractPages('1-3')`, not `pdfviewer.pageOrganizer.extractPages('1-3')`. The `PageOrganizer` service enables the UI and capabilities, but programmatic extraction uses the viewer instance.

- Loading extracted/serialized PDFs: `pdfviewer.load(document, password?)` accepts two parameters. When loading output returned by `extractPages(...)`, provide the password parameter as an empty string if the document is not protected, for example: `pdfviewer.load(extractedPdf, '')`. Supply the actual password only for password-protected PDFs.

- Event timing for document-dependent operations: Perform annotation and form field operations inside `documentLoad` to avoid initialization errors (e.g., `formFieldCollections` availability).

---