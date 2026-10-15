---
name: syncfusion-aspnetcore-buttons
description: Provides complete guidance for implementing the Syncfusion ASP.NET Core Switch (Toggle Switch Button), SplitButton component using Tag Helper. Use this when adding a toggle switch, on/off control, or binary state input to an ASP.NET Core application. This skill covers checked/disabled state, label customization (onLabel/offLabel), RTL support, form integration, BeforeChange event handling, and custom appearance.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Buttons"
---

# Syncfusion ASP.NET Core Switch

The Syncfusion ASP.NET Core Switch is a graphical UI element that allows toggling between checked (ON) and unchecked (OFF) states. It supports labels, small size, RTL, disabled state, form integration, event handling, and full CSS customization.

## Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- NuGet package installation (`Syncfusion.EJ2.AspNet.Core`)
- Tag Helper registration in `_ViewImports.cshtml`
- CDN stylesheet and script references
- Script manager setup (`<ejs-scripts>`)
- Basic Switch rendering (Tag Helper and MVC HTML Helper)
- Setting ON/OFF label text with `onLabel` / `offLabel`
- Setting initial checked state with `checked`

### Switch Features & Configuration
📄 **Read:** [references/switch-features.md](references/switch-features.md)
- Setting disabled state with `disabled`
- Changing switch size to small with `cssClass="e-small"`
- Enabling RTL layout with `enableRtl`
- Form integration: `name`, `value`, `checked` attributes
- Submitting switch values in an HTML form
- Enabling state persistence with `enablePersistence`
- Locale/culture override with `locale`

### Events & State Management
📄 **Read:** [references/events.md](references/events.md)
- `BeforeChange` event – intercept and cancel state changes
- `Change` event – respond after state changes
- `Created` event – execute logic after component renders
- Preventing switch state change conditionally

### Customization & Appearance
📄 **Read:** [references/customization.md](references/customization.md)
- CSS class list for Switch bar and handle
- Customizing bar shape (square vs round) with `cssClass`
- Customizing switch bar and handle colors
- iOS-style switch example
- Style and Appearance reference table
- Theme Studio integration

### Accessibility
📄 **Read:** [references/accessibility.md](references/accessibility.md)
- WCAG 2.2 AA compliance
- WAI-ARIA attributes (`role`, `aria-disabled`)
- Keyboard interaction (Space key)
- Screen reader support
- RTL and color contrast support
- Ripple effect for switch labels

### API Reference
📄 **Read:** [references/api.md](references/api.md)
- All properties: `checked`, `cssClass`, `disabled`, `enablePersistence`, `enableRtl`, `htmlAttributes`, `locale`, `name`, `offLabel`, `onLabel`, `value`
- All events: `beforeChange`, `change`, `created`
- Tag Helper attribute names and MVC HTML Helper equivalents
- Default values for each property

## Quick Start

**ASP.NET Core Tag Helper:**
```cshtml
@* _ViewImports.cshtml must have: @addTagHelper *, Syncfusion.EJ2 *@

<ejs-switch id="default"></ejs-switch>
```

**Switch with ON/OFF labels (checked by default):**
```cshtml
<ejs-switch id="switch1" onLabel="ON" offLabel="OFF" checked="true"></ejs-switch>
```

## Common Patterns

### Disabled Switch
```cshtml
<ejs-switch id="switch1" disabled="true"></ejs-switch>
```

### Small Size Switch
```cshtml
<ejs-switch id="switch1" cssClass="e-small"></ejs-switch>
```

### RTL Switch
```cshtml
<ejs-switch id="switch1" enableRtl="true"></ejs-switch>
```

### Prevent State Change (BeforeChange event)
```cshtml
<ejs-switch id="switch1" BeforeChange="onBeforeChange"></ejs-switch>
<script>
    function onBeforeChange(args) {
        args.cancel = true; // Prevents toggle
    }
</script>
```

### Form Submission
```cshtml
<form>
    <ejs-switch id="switch1" name="wifi" value="on" checked="true"></ejs-switch>
    <ejs-button id="submit" content="Submit"></ejs-button>
</form>
```

# Syncfusion ASP.NET Core SplitButton

The SplitButton component combines a primary action button with a dropdown arrow that reveals a popup list of secondary action items. Clicking the primary button triggers the default action; clicking the dropdown arrow opens the popup.

## Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- NuGet package installation and tag helper registration
- Stylesheet and script CDN setup
- Basic SplitButton with popup items (`content`, `items`)
- Running the application for the first time
- Controller action to populate `ViewBag.items`

### Icons and Appearance
📄 **Read:** [references/icons-and-appearance.md](references/icons-and-appearance.md)
- Adding icons via `iconCss` property
- Changing icon position (`iconPosition`: Left / Top)
- Vertical button layout using `cssClass="e-vertical"`
- Icons on popup action items
- Separator lines between popup items (`separator: true`)
- Style and appearance CSS class reference (`.e-dropdown-btn`, `.e-split-btn`, etc.)
- Theme Studio customization

### Popup Items and Templating
📄 **Read:** [references/popup-items.md](references/popup-items.md)
- Defining popup items with `text`, `iconCss`, `separator`, `id`, `url`, `disabled`
- Item templating via `beforeItemRender` event
- Popup templating using the `target` property
- Grouping items using ListView as `target`

### How-To Scenarios
📄 **Read:** [references/how-to.md](references/how-to.md)
- Set disabled state via `disabled` property
- Enable right-to-left layout with `enableRtl`
- Open a Dialog on popup item click using `select` event
- Underline a character in item text using `beforeItemRender`
- Group items in popup with ListView

### Events and Interactivity
📄 **Read:** [references/events.md](references/events.md)
- `click` — primary button clicked
- `select` — popup action item selected
- `beforeOpen` / `open` / `close` / `beforeClose` — popup lifecycle
- `beforeItemRender` — customize each popup item at render time
- `created` — component initialization complete
- Practical event handler examples

### Accessibility
📄 **Read:** [references/accessibility.md](references/accessibility.md)
- WCAG 2.2 AA compliance
- WAI-ARIA attributes (`role`, `aria-haspopup`, `aria-expanded`, `aria-owns`, `aria-disabled`)
- Keyboard navigation shortcuts
- Screen reader support
- Accessibility checker validation

### API Reference
📄 **Read:** [references/api.md](references/api.md)
- Complete property list with types and defaults
- Event signatures
- Method reference (`toggle`, `destroy`)
- EJ1 to EJ2 migration mapping

## Quick Start

**Controller (HomeController.cs):**
```csharp
public ActionResult Index()
{
    List<object> items = new List<object>();
    items.Add(new { text = "Cut" });
    items.Add(new { text = "Copy" });
    items.Add(new { text = "Paste" });
    ViewBag.items = items;
    return View();
}
```

**View (Index.cshtml):**
```cshtml
<ejs-splitbutton id="element" content="Paste" items="ViewBag.items"></ejs-splitbutton>
```

## Common Patterns

### SplitButton with Icon
```cshtml
<ejs-splitbutton id="element" content="Paste" items="ViewBag.items"
    iconCss="e-icons e-paste"></ejs-splitbutton>
```

### SplitButton with Icon on Top (Vertical style)
```cshtml
<ejs-splitbutton id="element" content="Paste" items="ViewBag.items"
    iconCss="e-icons e-paste" iconPosition="Top"
    cssClass="e-vertical"></ejs-splitbutton>
```

### Disabled SplitButton
```cshtml
<ejs-splitbutton id="element" content="Paste" items="ViewBag.items"
    disabled="true"></ejs-splitbutton>
```

### RTL SplitButton
```cshtml
<ejs-splitbutton id="rtl" content="Message" items="ViewBag.items"
    enableRtl="true"></ejs-splitbutton>
```

### Handle Primary Click and Item Select
```cshtml
<ejs-splitbutton id="element" content="Paste" items="ViewBag.items"
    click="onPrimaryClick" select="onItemSelect"></ejs-splitbutton>

<script>
    function onPrimaryClick(args) {
        // Primary button clicked
    }
    function onItemSelect(args) {
        // args.item contains the selected popup item
        console.log(args.item.text);
    }
</script>
```
