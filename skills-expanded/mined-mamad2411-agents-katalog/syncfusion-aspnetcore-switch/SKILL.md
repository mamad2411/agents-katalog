---
name: syncfusion-aspnetcore-switch
description: Guide for implementing Syncfusion ASP.NET Core Switch component. Use this skill when creating a toggle button/switch for form inputs or state management. Covers installation, basic implementation, property configuration, event handling, and styling customization. Provides guidance on getting started, properties, events, and styling documentation.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Syncfusion ASP.NET Core Switch Component

## When to Use This Skill

Use this skill when your users need to:
- **Create toggle buttons/switches** for boolean input (on/off, enabled/disabled, yes/no)
- **Add Switch controls** to forms for user state selection
- **Configure Switch appearance** (labels, size, colors)
- **Handle Switch state changes** with event handlers
- **Style and customize** the Switch component
- **Integrate Switch** with ASP.NET Core models and backend logic
- **Implement validation** and form submission with Switch values

## About the Switch Component

The Syncfusion Switch (Toggle Button) is a lightweight, accessible input control for toggling between two states. Built on TypeScript/JavaScript, it integrates seamlessly with ASP.NET Core Razor markup and C# backend code.

**Key Features:**
- Binary state toggle (checked/unchecked)
- Custom on/off labels
- Keyboard navigation support
- Event-driven change detection
- CSS-based customization
- WCAG accessibility compliance
- Lightweight and responsive

## Documentation and Navigation Guide

### Getting Started with Switch
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- TagHelper registration and setup
- NuGet package installation and verification
- Creating your first Switch control
- Setting on/off labels
- Basic initialization and rendering

### Switch Properties and Configuration
📄 **Read:** [references/switch-properties.md](references/switch-properties.md)
- Understanding Switch properties (checked, disabled, name, value)
- Property binding with ASP.NET Core models
- Data model integration for forms
- Binding Switch state to C# properties
- Default values and initial state

### Switch Events and State Management
📄 **Read:** [references/switch-events.md](references/switch-events.md)
- Change event handler implementation
- Detecting state transitions
- Form submission with Switch values
- Server-side validation
- Tracking user interactions

### Styling and Customization
📄 **Read:** [references/styling-customization.md](references/styling-customization.md)
- CSS classes for customization (wrapper, handle, inner)
- Theme application (Material, Fabric, Bootstrap)
- Custom appearance with CSS
- Theme Studio integration
- Advanced styling techniques

### Advanced How-To Patterns
📄 **Read:** [references/advanced-how-to.md](references/advanced-how-to.md)
- Change Switch size (default vs small)
- Enable right-to-left (RTL) support
- Prevent or intercept state changes
- Set disabled state based on conditions
- Submit Switch values through forms

## Quick Start Example

### Basic Switch Implementation
```cshtml
<!-- In ~/Pages/Shared/_ViewImports.cshtml (if not already added) -->
@addTagHelper *, Syncfusion.EJ2

<!-- In ~/Pages/Index.cshtml -->
<div class="switch-container">
    <label>Enable Notifications</label>
    <ejs-switch id="switchId"></ejs-switch>
</div>
```

### Switch with Labels
```cshtml
<ejs-switch id="switchWithLabels" 
            onLabel="ON" 
            offLabel="OFF">
</ejs-switch>
```

### Switch with Event Handling
```cshtml
<ejs-switch id="switchWithEvent" 
            change="onChange">
</ejs-switch>

<script>
    function onChange(args) {
        console.log('Switch state changed:', args.checked);
        // Update UI or call server
    }
</script>
```

## Common Patterns

**Pattern 1: Bind Switch to Form Model**
```cshtml
<!-- Page Model: public bool NotificationEnabled { get; set; } -->
<ejs-switch id="notificationSwitch" 
            checked="@Model.NotificationEnabled"
            change="onNotificationChange">
</ejs-switch>

<script>
    function onNotificationChange(args) {
        // Update form data for submission
        document.getElementById('notificationValue').value = args.checked;
    }
</script>
```

**Pattern 2: Disabled State with Conditional Logic**
```cshtml
<!-- Disable Switch based on condition -->
<ejs-switch id="premiumSwitch" 
            disabled="@(!Model.IsPremiumUser)">
</ejs-switch>
```

**Pattern 3: Group Multiple Switches**
```cshtml
<div class="preferences">
    <div class="preference-item">
        <label>Email Notifications</label>
        <ejs-switch id="emailSwitch"></ejs-switch>
    </div>
    <div class="preference-item">
        <label>SMS Notifications</label>
        <ejs-switch id="smsSwitch"></ejs-switch>
    </div>
</div>
```

## Key Properties

| Property | Type | Description | When to Use |
|----------|------|-------------|-------------|
| `checked` | boolean | Initial state (true = on, false = off) | Set default switch position on page load |
| `disabled` | boolean | Disable interaction (true/false) | Show but prevent changes (permissions, loading) |
| `name` | string | HTML form name attribute | Form submission and server-side binding |
| `value` | string | HTML form value | Custom value sent to server |
| `onLabel` | string | Text shown in "on" state | Clarify the enabled option |
| `offLabel` | string | Text shown in "off" state | Clarify the disabled option |
| `change` | function | Event handler for state changes | React to user interaction |
| `cssClass` | string | Custom CSS class for styling | Apply theme or custom appearance |

## Common Use Cases

1. **User Preferences** - Enable/disable notifications, emails, analytics tracking
2. **Feature Toggles** - Toggle experimental features, beta versions, maintenance mode
3. **Form Options** - Accept/agree to terms, agree to share data, consent forms
4. **Admin Controls** - Enable/disable users, features, or system settings
5. **Subscription States** - Activate/deactivate subscriptions, trial versions, licenses

## Next Steps

1. **Start Here:** Review [Getting Started](references/getting-started.md) for initial setup
2. **Configure:** Explore [Switch Properties](references/switch-properties.md) for your use case
3. **Handle Events:** Learn [Event Handling](references/switch-events.md) for interactivity
4. **Customize:** Check [Styling](references/styling-customization.md) for appearance

For complete reference, visit the [Syncfusion ASP.NET Core Switch Documentation](https://ej2.syncfusion.com/aspnetcore/documentation/switch/getting-started/).
