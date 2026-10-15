---
name: syncfusion-react-pdf-viewer
description: Implements the Syncfusion React PDF Viewer (PdfViewerComponent) for embedding, configuring, and loading PDF documents. Use this when rendering PDFs in a React application, embedding viewer controls, or generating TSX/HTML code for PDF display and interaction.
compatibility: React supported version >= 15.5.4+, Node version >= 14.0.0+ (NPM Package Manager)
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Syncfusion React Pdfviewer – UI Sample Generator

## Generate Code for the User's Project *(default)*

**Trigger keywords:** "how to", "add pdfviewer", "code sample", "show me", "example", "snippet", "integrate", "component", "create sample", "react sample".

**Purpose:** Generate minimal, copy-pasteable TS and HTML code that the user can integrate directly into their React project.

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
    "This feature is not supported in the current Syncfusion React PDF Viewer implementation."
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
  - `package.json` (project configuration and dependencies)
  - `tsconfig.json` (TypeScript configuration)
  - `App.tsx` or `App.jsx` (root component)
  - `vite.config.ts` or `webpack.config.js` (build configuration)
  - Any existing `.tsx` or `.jsx` files in src/ folder
- **Output:** Confirm the detected application type is a React TypeScript or JavaScript project before proceeding.
 
#### Step 2 — Generate Code from Reference Files Only *(REQUIRED)*
- **Before generating:** Confirm that Steps 1 are complete
- Read the relevant `references/*.md` file(s) for the requested feature
- Cross-reference EVERY API, property, and method against these tables
- **COMPONENT-BASED APPROACH (MANDATORY - REACT PATTERNS ONLY):**
  - Use JSX/TSX syntax for React component composition
  - Configure all PDF Viewer properties directly as component props
  - Use React hooks (useState, useRef, useEffect) when programmatic access is needed
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

## ⚙️ SETTINGS CONFIGURATION BEST PRACTICES

**When generating code with settings (toolbarSettings, annotationSettings, annotationSelectorSettings, arrowSettings, rectangleSettings, etc.), follow these guidelines to prevent unnecessary imports and over-engineering:**

### Rule 1: Simple Settings → Define INLINE in Component Props

**Use this approach when:**
- Configuring only 1-3 properties
- Settings are straightforward without complex enums or custom types
- No need for TypeScript typed constants

**Example (DO THIS):**
```tsx
<PdfViewerComponent
  id="container"
  documentPath="https://cdn.syncfusion.com/content/pdf/pdf-succinctly.pdf"
  annotationSelectorSettings={{
    selectionBorderColor: '#0000ff',
    selectionBorderThickness: 2,
    resizerBorderColor: '#ff0000',
    resizerFillColor: '#4070ff',
    resizerSize: 8,
  }}
  style={{ height: '640px' }}
>
  <Inject services={[Annotation]} />
</PdfViewerComponent>
```

**Benefits:**
- ✅ No extra imports needed
- ✅ Simple and readable
- ✅ Less code clutter
- ✅ Type checking still works

---

### Rule 2: Complex Settings → Define as Typed Constant (OUTSIDE component)

**Use this approach when:**
- Configuring 4+ properties OR multiple related settings
- Using enums or complex configurations
- Need to reuse the same configuration across multiple components
- Settings are complex enough to warrant separate definition

**Example (DO THIS ONLY FOR COMPLEX CASES):**

```tsx
import { PdfViewerComponent, Inject, Annotation } from '@syncfusion/ej2-react-pdfviewer';
import type { AnnotationSelectorSettingsModel } from '@syncfusion/ej2-react-pdfviewer';
import { AnnotationResizerLocation, CursorType } from '@syncfusion/ej2-react-pdfviewer';

// Define constant OUTSIDE component with proper types and enums
const annotationSelectorConfig: AnnotationSelectorSettingsModel = {
  selectionBorderColor: '#0000ff',
  selectionBorderThickness: 2,
  resizerBorderColor: '#ff0000',
  resizerFillColor: '#4070ff',
  resizerSize: 8,
  resizerShape: 'Square',
  selectorLineDashArray: [5, 6],
  resizerLocation: AnnotationResizerLocation.Corners | AnnotationResizerLocation.Edges,
  resizerCursorType: CursorType.grab,
};

export function App() {
  return (
    <PdfViewerComponent
      id="container"
      documentPath="https://cdn.syncfusion.com/content/pdf/pdf-succinctly.pdf"
      annotationSelectorSettings={annotationSelectorConfig}
      style={{ height: '640px' }}
    >
      <Inject services={[Annotation]} />
    </PdfViewerComponent>
  );
}
```

**When to import types and enums:**
- [ ] Import `type { SettingsNameModel }` for TypeScript type checking
- [ ] Import any enums that are used in the settings (e.g., `AnnotationResizerLocation`, `CursorType`)
- [ ] Keep imports minimal - import ONLY what is used in the settings

**Benefits:**
- ✅ Type-safe configuration
- ✅ Proper enum usage
- ✅ Reusable across multiple components
- ✅ Clean component code

---

### Rule 3: NEVER Over-Engineer Simple Cases

**❌ DO NOT DO THIS (Over-engineered):**
```tsx
import { PdfViewerComponent, Inject, Annotation } from '@syncfusion/ej2-react-pdfviewer';
import type { ToolbarSettingsModel } from '@syncfusion/ej2-react-pdfviewer';

// Unnecessary constant for 2 simple properties
const toolbarSettings: ToolbarSettingsModel = {
  showTooltip: true,
};

export function App() {
  return (
    <PdfViewerComponent
      toolbarSettings={toolbarSettings}
      // ... rest of props
    />
  );
}
```

**✅ DO THIS INSTEAD (Simple & Clean):**
```tsx
<PdfViewerComponent
  toolbarSettings={{ showTooltip: true }}
  // ... rest of props
/>
```

---

### Checklist Before Generating Code

- [ ] **Count the settings properties:** 1-3? → Use inline | 4+? → Use constant
- [ ] **Are enums involved?** Yes → Must use typed constant with imports | No → Can use inline
- [ ] **Is it reused elsewhere?** Yes → Use constant | No → Prefer inline
- [ ] **Do I need type safety?** Yes → Import `type { SettingsModel }` | No → Skip type import
- [ ] **Do I need enums?** Yes → Import required enums | No → Skip enum imports
- [ ] **Is the component prop simple enough?** Yes → Keep inline | No → Extract to constant

---

### Code References

All templates and operation snippets live in `references/*.md`. Each file is a focused snippet or template the agent will combine when generating samples.

**Flow:** Always start with `references/basic-sample.md`, then merge matched features into its anchors (PROPS, EVENTS, UI_BUTTONS, HANDLERS). If no keyword matches, return only the basic sample.

---

## Reference File Routing Guide

### 🎯 Core Setup & Configuration

| File | Purpose | **Route When User Asks About** |
|---|---|---|
| **basic-sample.md** | Minimal PDFViewer with documentPath, height, and width. Base template for all samples. | "basic setup", "minimal example", "getting started", "how to load PDF" |
| **general-properties.md** | Configure core viewer properties (server URL, document path, locale, resource base path). | "configuration", "server settings", "locale", "document path setup" |
| **enable-properties.md** | Enable/disable specific features (toolbar, annotations, forms, navigation, text selection, download, print). | "disable toolbar", "hide features", "enable/disable", "read-only mode", "restrict features" |

### 📐 Navigation() & Page Management

| File | Purpose | **Route When User Asks About** |
|---|---|---|
| **page-navigation.md** | Navigate between pages (first, last, next, previous page), go to specific page numbers. | "page navigation", "go to page", "next page", "previous page", "jump to page" |
| **bookmark-navigation.md** | Navigate using PDF bookmarks/table of contents in the bookmark panel. **CRITICAL: All bookmark methods MUST be accessed via `viewerRef.current.bookmark.*` (e.g., `viewerRef.current.bookmark.openBookmarkPane()`), NOT directly on `viewerRef.current`** | "bookmarks", "bookmark", "table of contents", "TOC navigation", "outline panel", "get bookmarks", "retrieve bookmarks", "fetch bookmarks", "bookmarks programmatically", "getBookmarks", "goToBookmark", "bookmark API", "list bookmarks", "open bookmark", "close bookmark" |
| **hyperlink-navigation.md** | Configure hyperlink navigation behavior and external link handling in PDFs. | "hyperlinks", "external links", "URL navigation", "clickable links", "url", "link" |
| **thumbnail-navigation.md** | Display and navigate using page thumbnails in the thumbnail panel. | "thumbnails", "preview pages", "thumbnail panel", "thumbnail","page previews" |

### 🔍 Viewing & Interaction

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
| **toolbar-settings.md** | Configure toolbar visibility, tooltip behavior, and customize/remove toolbar items. | "customize toolbar", "hide toolbar items", "remove toolbar buttons", "toolbar configuration" |
| **toolbar-methods.md** | Programmatically show/hide toolbars and enable/disable toolbar items at runtime. | "show/hide toolbar dynamically", "toggle toolbar", "enable/disable toolbar items programmatically" |

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
| **contextmenu.md** | Customize context menu items and handle context menu events. | "right-click menu", "context menu", "custom context menu", "disable context menu items" |

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
| **form-field-settings.md** | Configure default properties for form fields (text, checkbox, radio, dropdown, signature). | "form field defaults", "form field styles", "configure form fields", "form field properties" |
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
| **events.md** | Complete list of all PDFViewer events (document load, download, annotations, forms, search, navigation). | "event list", "all events", "available events", "event reference", "event handlers" |

---
