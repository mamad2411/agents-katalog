---
name: syncfusion-aspnetcore-popups
title: Implementing Syncfusion Popups (ASP.NET Core)
platform: aspnetcore
description: Comprehensive guide for implementing Syncfusion ASP.NET Core Popup components including Dialog. Covers modal dialogs, positioning, animations, templates, accessibility, and event handling.
metadata:
  author: "Syncfusion Inc"
  category: "Popups"
  version: "33.1.44"
---

# Implementing Dialog — ASP.NET Core

This skill documents how to implement, configure, and customize the Syncfusion Dialog in ASP.NET Core applications using the `<ejs-dialog>` Tag Helper API. It covers setup, modality, positioning, animations, templates, events, accessibility, and styling.

## Quick Links
- [API Reference](references/dialog-api.md)
- [Getting Started](references/dialog-getting-started.md)
- [Basic Features](references/dialog-basic-features.md)
- [Positioning & Sizing](references/dialog-positioning-and-sizing.md)
- [Animations & Transitions](references/dialog-animations-and-transitions.md)
- [Templates](references/dialog-templates.md)
- [Accessibility & Localization](references/dialog-accessibility-and-localization.md)
- [Events & Interactions](references/dialog-events-and-interactions.md)
- [Styling & Themes](references/dialog-styling-and-themes.md)

## Quick Start (Tag Helper)

In your Razor view:

```csharp
@using Syncfusion.EJ2

<ejs-dialog id="dialog" header="Welcome" isModal="true" width="500px">
    <e-content-template>
        <p>This is a basic dialog with default settings.</p>
    </e-content-template>
</ejs-dialog>

<script>
    window.onload = function () {
        document.getElementById('openBtn').onclick = function () {
            document.getElementById('dialog').ej2_instances[0].show();
        };
    };
</script>
```

Ensure you include the script manager and styles in your layout (`_Layout.cshtml`):

```csharp
<!-- In <head> -->
<link rel="stylesheet" href="https://cdn.syncfusion.com/ej2/{{ site.ej2version }}/fluent.css" />

<!-- At end of <body> -->
<script src="https://cdn.syncfusion.com/ej2/{{ site.ej2version }}/dist/ej2.min.js"></script>
<ejs-scripts></ejs-scripts>
```

## Common Patterns

### Modal Confirmation Dialog
```csharp
<ejs-dialog id="confirmDialog" header="Confirm Action" isModal="true" width="400px">
    <e-dialog-buttons>
        <e-dialog-dialogbutton content="Yes" isPrimary="true" click="confirmAction"></e-dialog-dialogbutton>
        <e-dialog-dialogbutton content="No" click="closeDialog"></e-dialog-dialogbutton>
    </e-dialog-buttons>
    <e-content-template>
        <p>Are you sure you want to proceed?</p>
    </e-content-template>
</ejs-dialog>
```

### Draggable Dialog with Header
```csharp
<ejs-dialog id="draggableDialog" 
    header="Drag Me" 
    allowDragging="true" 
    width="500px" 
    showCloseIcon="true">
    <e-content-template>
        <p>Grab the header to drag this dialog.</p>
    </e-content-template>
</ejs-dialog>
```

### Centered Dialog
```csharp
<ejs-dialog id="centeredDialog" 
    header="Centered Position" 
    width="500px">
    <e-dialog-position x="center" y="center"></e-dialog-position>
    <e-content-template>
        <p>This dialog is centered on the page.</p>
    </e-content-template>
</ejs-dialog>
```

## Key Properties

| Tag Helper Attribute | Type | Purpose | Example |
|----------------------|------|---------|---------|
| `header` | string | Dialog title bar text | `header="Confirm Delete"` |
| `isModal` | bool | Shows overlay behind dialog | `isModal="true"` |
| `width` | string | Dialog width (px, %) | `width="500px"` |
| `height` | string | Dialog height (px, %) | `height="300px"` |
| `minHeight` | string | Minimum dialog height | `minHeight="150px"` |
| `allowDragging` | bool | Enable drag to reposition | `allowDragging="true"` |
| `enableResize` | bool | Enable end-user resizing | `enableResize="true"` |
| `showCloseIcon` | bool | Display close (X) button | `showCloseIcon="true"` |
| `closeOnEscape` | bool | Close on Escape key | `closeOnEscape="true"` |
| `visible` | bool | Initial visibility | `visible="false"` |
| `target` | string | Target container selector | `target="#container"` |
| `cssClass` | string | Custom CSS class(es) | `cssClass="my-dialog"` |
| `enableRtl` | bool | Right-to-left rendering | `enableRtl="true"` |
| `enablePersistence` | bool | Persist state on reload | `enablePersistence="true"` |
| `zIndex` | double | Z-order stacking level | `zIndex="2000"` |
| `<e-dialog-position>` | DialogPositionData | X/Y positioning | `x="center" y="center"` |
| `<e-dialog-animationsettings>` | DialogAnimationSettings | Open/close animation | `effect="Zoom" duration="400"` |
| `footerTemplate` | string | Custom footer HTML string | `footerTemplate="<span>...</span>"` |

> **Removed invalid APIs:** `is-hidden` (use `visible="false"`), `position-x`/`position-y` flat attributes (use `<e-dialog-position>`), `allow-resizing` (use `enable-resize`), `max-height`, `max-width`, `min-width` (not supported).

## Next Steps
Read `getting-started.md` for full installation steps, NuGet package setup, and configuration details.

