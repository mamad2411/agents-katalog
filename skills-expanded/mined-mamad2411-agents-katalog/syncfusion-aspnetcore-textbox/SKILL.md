---
name: syncfusion-aspnetcore-textbox
description: Complete guide to implementing the Syncfusion TextBox component in ASP.NET Core applications with tag helpers, validation, floating labels, and adornments for building accessible input forms.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Input Controls"
  platform: "ASP.NET Core"
  framework: "Syncfusion.EJ2.AspNet.Core"
---

# Implementing TextBox in ASP.NET Core

The TextBox is a fundamental input component that enables users to enter text data with advanced features like floating labels, validation states, adornments (icons/buttons), and accessibility support. This skill guides you through implementing TextBox in ASP.NET Core applications using Syncfusion's tag helper syntax.

## When to Use This Skill

Use this skill when you need to:
- Create text input fields with floating labels and placeholder support
- Add validation visual states (success, error, warning)
- Display icons or buttons within text inputs (prepend/append templates)
- Build multiline textarea fields with auto-grow behavior
- Implement password fields with visibility toggles
- Create accessible forms following WCAG 2.2 Level AA standards
- Integrate TextBox with ASP.NET Core models and data binding

## Key Features

| Feature | Use Case |
|---------|----------|
| **Floating Labels** | Professional form UI that floats labels above input on focus |
| **Validation States** | Visual feedback with error, warning, and success classes |
| **Adornments** | Add icons, buttons, or text before/after the input |
| **Multiline Mode** | Create textarea fields with optional auto-grow |
| **Icon Groups** | Combine icons with floating labels for better UX |
| **WCAG Compliance** | Built-in accessibility support for screen readers and keyboard navigation |
| **Data Binding** | Two-way binding with ASP.NET Core models |
| **Event Handling** | Respond to Created, Change, Input, Focus, and Blur events |

## Documentation Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Prerequisites and system requirements
- Installing Syncfusion.EJ2.AspNet.Core NuGet package
- Configuring TagHelper in _ViewImports.cshtml
- Adding stylesheets and script resources via CDN
- Registering the script manager
- Creating your first TextBox
- Running and testing the application

### Tag Helper Syntax
📄 **Read:** [references/tag-helper-syntax.md](references/tag-helper-syntax.md)
- TextBox tag helper structure and properties
- Common properties (Placeholder, Value, Readonly, Disabled)
- Data binding with ASP.NET Core models
- Event binding in tag helpers
- Tag helper vs programmatic approaches
- Best practices and performance tips

### Validation States
📄 **Read:** [references/validation-states.md](references/validation-states.md)
- Implementing error, warning, and success validation states
- CSS class-based validation styling
- Server-side validation integration
- Client-side validation patterns
- Real-world form validation examples
- Accessibility for validation messages

### Adornments and Icons
📄 **Read:** [references/adornments-and-icons.md](references/adornments-and-icons.md)
- Adding prepend and append templates
- Icon integration (FontAwesome, Material Icons, Bootstrap Icons)
- Password visibility toggle implementation
- Clear button functionality
- Unit indicators (currency, measurements)
- Complex adornment patterns

### Floating Labels
📄 **Read:** [references/floating-labels.md](references/floating-labels.md)
- FloatLabelType property (Auto, Always, Never)
- Styling and animating floating labels
- Accessibility with floating labels
- Dynamic label positioning patterns
- Edge cases and troubleshooting

### Multiline TextBox
📄 **Read:** [references/multiline-textarea.md](references/multiline-textarea.md)
- Converting TextBox to textarea
- Multiline property configuration
- Character counting implementation
- Auto-grow and resize behavior
- Placeholder in multiline mode
- Validation in multiline TextBox
- Accessibility for textarea fields

### Advanced Patterns
📄 **Read:** [references/advanced-patterns.md](references/advanced-patterns.md)
- Data binding with HTML helpers
- Programmatic TextBox creation with C# and JavaScript
- Event handling patterns (Created, Change, Input, Focus, Blur)
- Template-based rendering
- Integration with ASP.NET Core Forms and Validation
- Model binding examples
- Security: XSS prevention and input sanitization

## Quick Start Example

### Basic TextBox with Floating Label (Tag Helper)

```cshtml
@* Pages/Index.cshtml *@
<div class="form-group">
    <ejs-textbox id="email" 
                  placeholder="Enter email" 
                  floatLabelType="Auto"
                  type="email">
    </ejs-textbox>
</div>
```

### In _ViewImports.cshtml (one-time setup)

```cshtml
@addTagHelper *, Syncfusion.EJ2
```

### In _Layout.cshtml (one-time setup)

```html
<head>
    <link rel="stylesheet" href="https://cdn.syncfusion.com/ej2/{{ site.ej2version }}/fluent.css" />
</head>
<body>
    @RenderBody()
    
    <script src="https://cdn.syncfusion.com/ej2/{{ site.ej2version }}/dist/ej2.min.js"></script>
    <ejs-scripts></ejs-scripts>
</body>
```

### Result

User sees:
1. Input field with placeholder "Enter email"
2. When focused or filled, label "email" floats above the input
3. Email validation applied automatically

## Common Patterns

### Pattern 1: Contact Form with Validation States

```cshtml
<form asp-action="Submit">
    <div class="form-group">
        <ejs-textbox id="name" 
                      placeholder="Full Name" 
                      floatLabelType="Auto"
                      cssClass="e-success">
        </ejs-textbox>
        <small class="d-block mt-2">Name is valid</small>
    </div>

    <div class="form-group">
        <ejs-textbox id="email" 
                      placeholder="Email Address" 
                      floatLabelType="Auto"
                      cssClass="e-error">
        </ejs-textbox>
        <small class="text-danger d-block mt-2">Invalid email format</small>
    </div>

    <button type="submit" class="btn btn-primary">Submit</button>
</form>
```

### Pattern 2: Password Field with Visibility Toggle

```cshtml
<div class="form-group">
    <ejs-textbox id="password" 
                  type="password"
                  placeholder="Password" 
                  floatLabelType="Auto"
                  appendTemplate="<span class='e-input-group-icon' onclick='togglePassword()'>👁️</span>">
    </ejs-textbox>
</div>

<script>
    function togglePassword() {
        const input = document.getElementById('password');
        const type = input.type === 'password' ? 'text' : 'password';
        input.type = type;
    }
</script>
```

### Pattern 3: Search Input with Icon

```cshtml
<div class="form-group">
    <ejs-textbox id="search" 
                  placeholder="Search products..." 
                  prependTemplate="<span class='e-input-group-icon'>🔍</span>"
                  floatLabelType="Auto">
    </ejs-textbox>
</div>
```

## Key Properties Reference

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `id` | string | - | Unique identifier for the TextBox |
| `value` | string | - | Initial text value |
| `placeholder` | string | - | Placeholder text displayed when empty |
| `floatLabelType` | FloatLabelType | `Never` | Label animation (Auto, Always, Never) |
| `multiline` | bool | false | Enable multiline textarea mode |
| `readonly` | bool | false | Prevent user input while allowing focus |
| `disabled` | bool | false | Disable input completely |
| `cssClass` | string | - | CSS classes (e.g., "e-error", "e-warning", "e-success") |
| `prependTemplate` | string | - | HTML template prepended to input |
| `appendTemplate` | string | - | HTML template appended to input |
| `type` | string | "text" | Input type (text, email, password, number, etc.) |

## Common Use Cases

### Use Case 1: Contact Form Builder
Create a professional contact form with floating labels, validation, and email/phone patterns:
- **When:** Building user contact information collection
- **Reference:** [validation-states.md](references/validation-states.md)
- **Key Features:** Floating labels, validation states, pattern validation

### Use Case 2: Search Interface
Implement a search box with prepended icon and dynamic filtering:
- **When:** Building product/content search features
- **Reference:** [adornments-and-icons.md](references/adornments-and-icons.md)
- **Key Features:** Icon adornments, event handling

### Use Case 3: Feedback/Comments Section
Build textarea for user comments with character counting and auto-grow:
- **When:** Creating feedback forms, comment sections
- **Reference:** [multiline-textarea.md](references/multiline-textarea.md)
- **Key Features:** Multiline mode, character limit, auto-grow

### Use Case 4: Accessible Registration Form
Create a registration form following WCAG 2.2 Level AA standards:
- **When:** Building public-facing registration forms
- **Reference:** [advanced-patterns.md](references/advanced-patterns.md)
- **Key Features:** ARIA labels, keyboard navigation, screen reader support

---

**Next Steps:**
1. Review [getting-started.md](references/getting-started.md) to set up your first TextBox
2. Choose your use case and follow the corresponding reference guide
3. Copy code examples and adapt to your project
4. Refer to [advanced-patterns.md](references/advanced-patterns.md) for complex scenarios
