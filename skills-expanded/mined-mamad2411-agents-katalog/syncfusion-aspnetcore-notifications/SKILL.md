---
name: syncfusion-aspnetcore-notifications
description: Implement Syncfusion ASP.NET Core Toast notification component for displaying brief messages, alerts, and notifications. Use this skill when building toast notifications, alert messages, success/error/warning/info banners, progress notifications, notification pop-ups, timed dismissal messages, or any on-screen notification UI in ASP.NET Core (EJ2 Tag Helper / Razor). Trigger for keywords like toast, notification, alert popup, snackbar, brief message, dismiss message, progress toast, action buttons toast.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Notifications"
---

# Syncfusion ASP.NET Core Toast

The Toast component displays brief, auto-dismissing notification messages on screen. It supports positioning, animations, action buttons, progress bars, templates, timeout control, and accessibility—covering simple alerts to rich notification UIs.

**Do NOT skip this skill if users mention:** notifications, alerts, snackbar, brief messages, dismiss popup, toast utility, progress notification, action button popup.

---

## Component Overview

### Key Capabilities

| Feature | Description |
|---------|-------------|
| **Types / cssClass** | Predefined styles: `e-toast-success`, `e-toast-info`, `e-toast-warning`, `e-toast-danger` |
| **Position** | X: Left/Center/Right, Y: Top/Bottom or custom pixel/percent values |
| **Timeout** | Auto-dismiss via `timeOut`; `extendedTimeout` for hover delay; `0` for static toast |
| **Progress Bar** | Visual countdown bar with `showProgressBar`; direction via `progressDirection` |
| **Action Buttons** | Add button models with click handlers via `buttons` / `e-toast-buttonmodelprops` |
| **Templates** | Full custom HTML via `template` property or `<e-content-template>` tag |
| **Animation** | Custom show/hide animation effects via `animation` settings |
| **Close Button** | Manual close via `showCloseButton` |
| **Multiple Toasts** | Separate toast instances per position; `newestOnTop` ordering |
| **Toast Utility** | `ToastUtility.show()` for zero-markup quick toasts |
| **Accessibility** | WAI-ARIA `role="alert"`, WCAG 2.2 AA, Section 508, RTL support |

### NuGet Package

```
Install-Package Syncfusion.EJ2.AspNet.Core
```

### Setup (one-time)

**`~/Pages/_ViewImports.cshtml`**
```cshtml
@addTagHelper *, Syncfusion.EJ2
```

**`~/Pages/Shared/_Layout.cshtml`** — inside `<head>`:
```cshtml
<link rel="stylesheet" href="https://cdn.syncfusion.com/ej2/{{ site.ej2version }}/fluent.css" />
<script src="https://cdn.syncfusion.com/ej2/{{ site.ej2version }}/dist/ej2.min.js"></script>
```
And before `</body>`:
```cshtml
<ejs-scripts></ejs-scripts>
```

---

## Documentation & Navigation Guide

### 📖 Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and NuGet setup
- Tag helper registration
- Basic toast with title and content
- Triggering toast via JavaScript `show()` method
- First working example

### 📖 Configuration & Options
📄 **Read:** [references/configuration.md](references/configuration.md)
- Title and content setup
- Custom target container
- Close button (`showCloseButton`)
- Progress bar (`showProgressBar`, `progressDirection`)
- Newest-on-top ordering (`newestOnTop`)
- Width and height customization
- HTML sanitizer (`enableHtmlSanitizer`)

### 📖 Position & Layout
📄 **Read:** [references/position.md](references/position.md)
- Predefined X/Y positions (Left, Center, Right / Top, Bottom)
- Custom pixel or percentage positions
- Multiple toasts in different positions
- Full-width toast with `width="100%"`

### 📖 Timeout & Lifecycle
📄 **Read:** [references/timeout.md](references/timeout.md)
- Auto-dismiss with `timeOut` (milliseconds)
- Extended hover timeout (`extendedTimeout`)
- Static (persistent) toast with `timeOut="0"`
- Closing toast on click/tap
- Restricting maximum visible toasts
- Preventing duplicate toasts

### 📖 Action Buttons
📄 **Read:** [references/action-buttons.md](references/action-buttons.md)
- Adding buttons with `e-toast-buttonmodelprops`
- Button click handlers
- Dismissing toast from a button click

### 📖 Templates & Animation
📄 **Read:** [references/templates-animation.md](references/templates-animation.md)
- Static HTML template via `template` property
- Dynamic content template with `<e-content-template>`
- Changing templates dynamically on `show()`
- Custom show/hide animation effects
- Playing audio before toast opens

### 📖 Toast Types & Styling
📄 **Read:** [references/types-and-styling.md](references/types-and-styling.md)
- Predefined types using `cssClass` (success, info, warning, danger)
- CSS customization for title, content, icon, background
- `ToastUtility.show()` with predefined types
- `ToastUtility.show()` with full ToastModel
- Mobile swipe-close prevention

### 📖 Accessibility
📄 **Read:** [references/accessibility.md](references/accessibility.md)
- WAI-ARIA role="alert"
- WCAG 2.2 AA compliance
- Section 508 support
- RTL rendering (`enableRtl`)
- Screen reader compatibility

### 📖 API Reference
📄 **Read:** [references/api.md](references/api.md)
- All properties with types and defaults
- All events (BeforeOpen, Open, Close, BeforeClose, Click, Created, Destroyed, BeforeSanitizeHtml)
- Sub-component types (ToastPosition, ToastAnimationSettings, ToastButtonModelProp)

---

## Quick Start Example

```cshtml
@* ~/Pages/Index.cshtml *@
<ejs-toast id="toast_default"
           title="Friend Request"
           content="Matt sent you a friend request."
           showCloseButton="true"
           showProgressBar="true"
           timeOut="5000">
    <e-toast-position X="Right" Y="Bottom"></e-toast-position>
</ejs-toast>

<ejs-button id="showBtn" content="Show Toast" cssClass="e-btn"></ejs-button>

<script>
    setTimeout(function () {
        var toast = document.getElementById('toast_default').ej2_instances[0];
        toast.target = document.body;
        toast.show();
    }, 500);

    document.getElementById('showBtn').addEventListener('click', function () {
        var toast = document.getElementById('toast_default').ej2_instances[0];
        toast.show();
    });
</script>
```

---

## Common Patterns

### Pattern 1: Show Typed Notification (Success / Error / Warning / Info)
```cshtml
<ejs-toast id="typed_toast">
    <e-toast-position X="Right" Y="Top"></e-toast-position>
</ejs-toast>

<script>
    var toasts = [
        { title: 'Success !', content: 'Record saved successfully.', cssClass: 'e-toast-success' },
        { title: 'Error !',   content: 'Failed to save record.',    cssClass: 'e-toast-danger'  },
        { title: 'Warning !', content: 'Unsaved changes present.',  cssClass: 'e-toast-warning' },
        { title: 'Info !',    content: 'Session expires in 5 min.', cssClass: 'e-toast-info'    }
    ];
    function showToast(index) {
        var toast = document.getElementById('typed_toast').ej2_instances[0];
        toast.target = document.body;
        toast.show(toasts[index]);
    }
</script>
```

### Pattern 2: Toast Utility (Zero Markup)
```javascript
// Predefined type — no container element needed
ejs.notifications.ToastUtility.show('Record saved successfully', 'Success', 5000);

// With full model
ejs.notifications.ToastUtility.show({
    title: 'Upload Complete',
    content: 'Your file has been uploaded.',
    timeOut: 5000,
    position: { X: 'Right', Y: 'Bottom' },
    showCloseButton: true
});
```

### Pattern 3: Action Buttons with Close Handler
```cshtml
<ejs-toast id="action_toast" title="New Message" timeOut="0">
    <e-toast-position X="Right" Y="Bottom"></e-toast-position>
    <e-toast-buttonmodelprops>
        <e-toast-buttonmodelprop model="ViewBag.AcceptBtn" click="onAccept"></e-toast-buttonmodelprop>
        <e-toast-buttonmodelprop model="ViewBag.DismissBtn"></e-toast-buttonmodelprop>
    </e-toast-buttonmodelprops>
</ejs-toast>

<script>
    function onAccept(e) {
        var toastEle = ej.base.closest(e.target, '.e-toast');
        document.getElementById('action_toast').ej2_instances[0].hide(toastEle);
    }
</script>
```
```csharp
// Controller
ViewBag.AcceptBtn  = new { content = "Accept" };
ViewBag.DismissBtn = new { content = "Dismiss" };
```

### Pattern 4: Prevent Duplicate Toast
```cshtml
<ejs-toast id="dup_toast" beforeOpen="onBeforeOpen" close="onClose"
           title="Alert" content="Network issue detected.">
    <e-toast-position X="Center" Y="Top"></e-toast-position>
</ejs-toast>

<script>
    var isOpen = false;
    function onBeforeOpen(e) {
        if (isOpen) { e.cancel = true; }
        else { isOpen = true; }
    }
    function onClose() { isOpen = false; }
</script>
```

### Pattern 5: Restrict Maximum Toasts
```cshtml
<ejs-toast id="max_toast" beforeOpen="onBeforeOpen"
           title="Notification" content="New item added.">
    <e-toast-position X="Center" Y="Top"></e-toast-position>
</ejs-toast>

<script>
    var maxCount = 3;
    function onBeforeOpen(e) {
        var toast = document.getElementById('max_toast').ej2_instances[0];
        if (toast.element.childElementCount >= maxCount) {
            e.cancel = true;
        }
    }
</script>
```
