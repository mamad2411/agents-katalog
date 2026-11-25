---
name: webviewer-build
description: Generate a complete web application inside a FileMaker Web Viewer — self-contained HTML/CSS/JS styled with the FM theme, plus companion FM bridge scripts for bidirectional data flow. Use when the developer says "web viewer", "webviewer app", "HTML in FileMaker", "build web viewer", or when the layout-design skill delegates to the web-first output path. Recommended for modern, responsive UI, complex interactions (drag-and-drop, charts, rich text), or solutions considering future migration off FileMaker.
---

# WebViewer Build

Generate a complete web application that runs inside a FileMaker Web Viewer object, along with the companion FM scripts that connect it to FileMaker data. The output is a self-contained HTML file plus fmxmlsnippet scripts — together they form a bidirectional data bridge between the web UI and the FM solution.

---

## Step 1: Determine the automation tier

Read `agent/config/automation.json` and check `project_tier` (preferred) or `default_tier`:

- **Tier 1** — FM scripts go to clipboard with paste instructions
- **Tier 2/3** — agent can deploy FM scripts via companion server automation

Also read `companion_url` from `automation.json` for preview pushes.

---

## Step 2: Gather context

1. Read `agent/CONTEXT.json` for:
   - `current_layout` — the layout where the Web Viewer will be placed
   - `tables` — the data schema (fields, types, TOs) that the web app will display and edit
   - `relationships` — related data the web app needs to access
   - `scripts` — existing scripts the web app may need to call
   - `value_lists` — for dropdowns, filters, and validation
   - `custom_functions` — for any calculations the FM scripts need

2. If CONTEXT.json is absent or scoped to the wrong layout, ask the developer to run **Push Context** on the target layout.

3. Read the theme data from `agent/context/{solution}/`:
   ```bash
   cat agent/context/*/theme.css 2>/dev/null
   cat agent/context/*/theme-manifest.json 2>/dev/null
   ```

   - `theme.css` — inline this into the HTML for visual consistency with the FM solution
   - `theme-manifest.json` — color palette for matching FM's visual language

4. If no theme data exists, note this and suggest running `python3 agent/scripts/extract_theme.py`. Proceed with a clean, neutral stylesheet if the developer wants to continue.

---

## Step 3: Design conversation

Understand what the web app needs to do. Key questions:

1. **What data does it display?** — Which tables, fields, and relationships? List view, detail view, or both?
2. **What interactions does it support?** — Read-only display, inline editing, record creation, deletion, drag-and-drop, filtering, sorting?
3. **Does it need charts or visualizations?** — Bar charts, line graphs, KPIs, gauges?
4. **What actions trigger FM scripts?** — Save, delete, navigate, print, run a process?
5. **Does FM need to push data updates to the web viewer?** — Real-time refresh when the user navigates records in FM?

If the developer provided a spec from `layout-spec` or a design brief, extract the answers from that.

---

## Step 4: Generate the HTML application

Build a single, self-contained HTML file. All CSS and JavaScript are inline — no external dependencies. The file must work when loaded via `Set Web Viewer` with a `data:text/html` URL or from a file path.

### HTML structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{App Title}</title>
  <style>
    /* FM theme CSS for visual consistency */
    {theme_css_content}

    /* Application styles */
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    /* ... app-specific styles ... */
  </style>
</head>
<body>
  <!-- Application markup -->
  <div id="app">
    <!-- Loading state shown until FM pushes data -->
    <div id="loading">Loading...</div>
    <!-- Main content hidden until data arrives -->
    <div id="content" style="display: none;">
      <!-- ... -->
    </div>
  </div>

  <script>
    // === FM Bridge ===

    /**
     * Called by FM via Perform JavaScript in Web Viewer.
     * Receives JSON data from the FM data-loading script.
     * @param {string} json — JSON string from FM
     */
    function fmCallback(json) {
      try {
        const data = JSON.parse(json);
        renderApp(data);
      } catch (e) {
        console.error("fmCallback parse error:", e);
      }
    }

    /**
     * Call an FM script with a JSON parameter.
     * Uses the FileMaker.PerformScript() JS-to-FM bridge.
     * @param {string} scriptName — the FM script to call
     * @param {object} param — parameter object (will be JSON-stringified)
     */
    function callFM(scriptName, param) {
      if (typeof FileMaker !== "undefined") {
        FileMaker.PerformScript(scriptName, JSON.stringify(param));
      } else {
        console.log("FM bridge not available. Would call:", scriptName, param);
      }
    }

    // === Application Logic ===

    function renderApp(data) {
      document.getElementById("loading").style.display = "none";
      document.getElementById("content").style.display = "block";
      // ... render data into the DOM ...
    }

    // ... event handlers, UI logic ...
  </script>
</body>
</html>
```

### Design principles for FM Web Viewers

- **Self-contained**: No external CDN links, no fetch() calls to third-party APIs. Everything is inline. FM Web Viewers run in a sandboxed context and external resources may be blocked.
- **Theme-consistent**: Use the FM theme CSS so the web app looks like it belongs in the solution. Match colors, fonts, and spacing from the theme manifest.
- **Responsive within the viewer**: Unlike native FM layouts, web content can use flexbox and responsive CSS. Design for the Web Viewer's container size but allow graceful resizing.
- **Loading state**: Always show a loading indicator until FM pushes data via `fmCallback()`. The web viewer loads before FM can call JavaScript.
- **Error resilience**: Handle missing data gracefully. If `fmCallback` receives incomplete JSON, render what is available and show placeholders for the rest.
- **No FileMaker dependency for testing**: When `FileMaker.PerformScript()` is not available (opened in a browser outside FM), log calls to the console instead of crashing. This allows browser-based development and testing.

---

## Step 5: Generate companion FM scripts

The web viewer needs two FM scripts to function:

### Script 1: Data Loader

This script gathers data from the FM solution and pushes it to the web viewer via `Perform JavaScript in Web Viewer`. It is called when:
- The layout loads (via an OnLayoutEnter trigger)
- The user navigates to a different record
- Data changes and the web viewer needs a refresh

**HR format outline:**

```
# Push data to web viewer
Set Error Capture [ On ]
Allow User Abort [ Off ]
#
# Gather data as JSON
Set Variable [ $json ; Value:
  JSONSetElement ( "{}" ;
    ["records" ; <related records or found set as JSON array> ; JSONArray] ;
    ["meta" ; <metadata object> ; JSONObject]
  )
]
#
# Push to web viewer
Perform JavaScript in Web Viewer [ Object Name: "{webviewer_object_name}" ;
  Function Name: "fmCallback" ;
  Parameters: $json ]
```

Generate this as fmxmlsnippet XML using the step catalog. The data-gathering logic depends on what the web app needs — typically a combination of:
- Current record field values via `GetFieldName` / field references
- Related records via `ExecuteSQL` or looping through a portal relationship
- Value list values via `ValueListItems`

### Script 2: Event Handler

This script receives calls from the web viewer's `FileMaker.PerformScript()`. It parses the JSON parameter and dispatches to the appropriate action.

**HR format outline:**

```
# Handle web viewer event
Set Error Capture [ On ]
Allow User Abort [ Off ]
#
Set Variable [ $param ; Value: Get ( ScriptParameter ) ]
Set Variable [ $action ; Value: JSONGetElement ( $param ; "action" ) ]
#
If [ $action = "save" ]
  # Parse fields from $param and set them
  Set Field [ {TO}::{Field} ; JSONGetElement ( $param ; "fields.{fieldName}" ) ]
  Commit Records/Requests [ With dialog: Off ]
  # Refresh the web viewer with updated data
  Perform Script [ "Data Loader Script" ; Parameter: "" ]
Else If [ $action = "delete" ]
  Delete Record/Request [ With dialog: Off ]
Else If [ $action = "navigate" ]
  Set Variable [ $layout ; Value: JSONGetElement ( $param ; "layout" ) ]
  Go to Layout [ $layout ]
End If
```

Generate this as fmxmlsnippet XML. The action cases depend on the web app's interaction design from Step 3.

### Script generation rules

Follow all standard script creation rules from CLAUDE.md:
1. Grep the step catalog for each step type
2. Resolve field/layout/script IDs from CONTEXT.json
3. Follow coding conventions from `agent/docs/CODING_CONVENTIONS.md`
4. Write to `agent/sandbox/`
5. Validate with `python3 agent/scripts/validate_snippet.py`

---

## Step 6: Preview

Push the HTML to the webviewer for the developer to preview:

```bash
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"type": "layout-preview", "content": "<html content>"}' \
  {companion_url}/webviewer/push
```

If the companion server is not reachable, write the HTML to `agent/sandbox/{app-name}.html` and instruct the developer to open it in a browser.

> The web viewer app has been pushed to the webviewer for preview. Note that FM bridge calls (`FileMaker.PerformScript`) will log to the browser console since there is no FM context — the UI and layout are what to review here.

Iterate on feedback. Each revision generates an updated HTML file and a new push.

---

## Step 7: Output and deployment

Write all output files to `agent/sandbox/`:

| File | Contents |
|------|----------|
| `{app-name}.html` | The self-contained web viewer HTML application |
| `{app-name}-data-loader.xml` | fmxmlsnippet for the data-loading FM script |
| `{app-name}-event-handler.xml` | fmxmlsnippet for the event-handling FM script |

### Deploy FM scripts

Deploy the companion FM scripts per the current tier:

**Tier 1:**

```bash
python3 agent/scripts/clipboard.py write agent/sandbox/{app-name}-data-loader.xml
```

> The data loader script is on your clipboard. To install it:
>
> 1. Create a new script named **{Data Loader Script Name}** in Script Workspace
> 2. **⌘V** — paste

Repeat for the event handler script.

**Tier 2/3:** Deploy via `agent/scripts/deploy.py`.

### Install the Web Viewer

Provide instructions for setting up the Web Viewer object:

> To install the web viewer:
>
> 1. Open **{Layout Name}** in Layout Mode
> 2. Add a **Web Viewer** object — size it to fill the desired area
> 3. Set the Web Viewer's **Object Name** to **"{webviewer_object_name}"** (Inspector > Position > Name)
> 4. Set the Web Viewer's **URL** to one of:
>    - **File path**: `"file:" & Get ( DocumentsPath ) & "{app-name}.html"` (place the HTML file in the Documents folder)
>    - **Data URL**: `"data:text/html," & {a global field or variable containing the HTML}` (for self-contained deployment)
> 5. Set the **OnLayoutEnter** script trigger to run **{Data Loader Script Name}**
> 6. Switch to Browse Mode and test

---

## When to recommend the Web Viewer path

The web viewer approach is stronger than native FM layout objects when:

- **Responsive layout** is needed — FM layouts are fixed-position; web content reflows
- **Complex interactions** — drag-and-drop, sortable lists, rich text editing, inline search/filter
- **Data visualizations** — charts, graphs, KPI dashboards, Gantt charts, calendars
- **Modern UI patterns** — cards, accordions, modals, toast notifications, infinite scroll
- **Future migration** — the HTML/CSS/JS is portable to any web platform if the solution moves off FM
- **Rapid iteration** — CSS changes are instant; FM layout styling requires Layout Mode round-trips

The native FM path is stronger when:

- **Printing** — FM's print engine handles layout parts, sub-summaries, and page breaks natively
- **Simple forms** — a standard detail or list view with fields and portals is faster to build natively
- **Privilege-based field access** — FM's built-in security controls field-level access automatically; a web viewer must implement its own access checks
- **Accessibility** — FM's native objects have built-in accessibility support; web content requires manual ARIA markup

---

## Constraints

- The HTML must be **fully self-contained** — no external scripts, stylesheets, or API calls. FM Web Viewers run in a sandboxed WebKit/Chromium instance.
- The `FileMaker.PerformScript()` bridge is only available when the HTML is loaded inside a FileMaker Web Viewer — the code must handle its absence gracefully for browser testing.
- `Perform JavaScript in Web Viewer` requires the Web Viewer object to have a **named Object Name** set in the Inspector — always specify what this name should be.
- The data loader script must handle the case where the Web Viewer has not finished loading — consider a brief pause or a polling loop if needed.
- All FM script output follows standard fmxmlsnippet conventions — steps only, no `<Script>` wrapper, validated before deployment.
- Field IDs and script IDs must come from CONTEXT.json — never invent references.
- Follow coding conventions from `agent/docs/CODING_CONVENTIONS.md` for all FM script calculations.
