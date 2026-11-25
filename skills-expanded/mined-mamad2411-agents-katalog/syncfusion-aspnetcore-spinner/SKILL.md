---
name: syncfusion-aspnetcore-spinner
description: Comprehensive guide for implementing loading spinners in ASP.NET Core applications using Syncfusion. Use this skill when implementing loading indicators, providing progress feedback, or blocking UI during async operations. Covers spinner creation, show/hide lifecycle, types, styling, custom templates, and configuration methods. Includes patterns for real-world scenarios like form submission and data loading.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Syncfusion ASP.NET Core Spinner

## When to Use This Skill

Use this skill when your users need to:
- **Display loading indicators** during async operations (API calls, file uploads)
- **Show progress feedback** to prevent users from thinking the app is frozen
- **Block user interaction** on specific page sections
- **Customize spinner appearance** with colors, themes, or templates
- **Target specific elements** for spinner overlay rendering
- **Manage spinner lifecycle** (create, show, hide, destroy)
- **Apply different spinner types** (Material, Fabric, Bootstrap themes)

## Spinner Overview

The Syncfusion Spinner is a lightweight loading indicator that appears over a target element to indicate ongoing processing. It's essential for providing visual feedback during async operations in web applications.

**Key Characteristics:**
- Appears as an overlay on a target element
- Renders centered within the target
- Prevents user interaction with target while visible
- Supports theme-based styling (Material, Fabric, Bootstrap)
- Can use custom HTML templates for branded indicators
- Lightweight and performant

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and prerequisite setup
- Adding Syncfusion stylesheet and script resources
- Creating your first spinner with `createSpinner()`
- Showing and hiding spinners with `showSpinner()` and `hideSpinner()`
- Targeting specific page elements
- Basic implementation patterns

### Types and Configuration
📄 **Read:** [references/spinner-types.md](references/spinner-types.md)
- Available spinner types (Material, Fabric, Bootstrap, Bootstrap4, High Contrast)
- Changing spinner type with `setSpinner()`
- Theme-based type selection
- When to use each type
- Configuration before component creation

### Styling and Customization
📄 **Read:** [references/styling-customization.md](references/styling-customization.md)
- CSS customization patterns for each theme
- Modifying stroke color and appearance
- Material theme CSS selectors
- Fabric theme CSS selectors
- Bootstrap theme CSS selectors
- Bootstrap4 theme CSS selectors
- High Contrast theme CSS selectors
- Using CSS variables and custom styles

### Custom Templates
📄 **Read:** [references/templates.md](references/templates.md)
- Creating custom spinner templates
- Using `setSpinner()` with template configuration
- Custom HTML and SVG templates
- When to use custom templates
- Template scope and initialization order
- Styling custom templates with CSS

### Configuration Methods Reference
📄 **Read:** [references/configuration-methods.md](references/configuration-methods.md)
- `createSpinner()` method and parameters
- `showSpinner()` method and behavior
- `hideSpinner()` method and cleanup
- `setSpinner()` method for type and template configuration
- Target element configuration
- Method chaining and initialization patterns

## Quick Start Example

### Minimal Implementation
```cshtml
<!-- HTML -->
<div id="container">
    <p>Content here</p>
    <button id="loadBtn">Start Loading</button>
</div>

<script>
    // Create spinner targeting the container
    var target = document.getElementById('container');
    ej.popups.createSpinner({ target: target });
    
    // Show spinner on button click
    document.getElementById('loadBtn').addEventListener('click', function() {
        ej.popups.showSpinner(target);
        
        // Simulate async work
        setTimeout(function() {
            ej.popups.hideSpinner(target);
        }, 3000);
    });
</script>
```

## Common Patterns

**Pattern 1: Form Submission with Spinner**
```javascript
function submitForm() {
    var target = document.getElementById('formContainer');
    ej.popups.createSpinner({ target: target });
    ej.popups.showSpinner(target);
    
    fetch('/api/submit', { method: 'POST', body: formData })
        .then(response => response.json())
        .then(data => {
            ej.popups.hideSpinner(target);
            showSuccessMessage('Form submitted');
        })
        .catch(error => {
            ej.popups.hideSpinner(target);
            showErrorMessage('Submission failed');
        });
}
```

**Pattern 2: Multiple Async Operations**
```javascript
var target = document.getElementById('container');
ej.popups.createSpinner({ target: target });

// Show once, hide when all complete
Promise.all([fetch1(), fetch2(), fetch3()])
    .then(() => {
        ej.popups.showSpinner(target);
        // Process results
        ej.popups.hideSpinner(target);
    });
```

**Pattern 3: Theme-Based Spinner**
```javascript
// Set spinner type before creating other components
ej.popups.setSpinner({ type: 'Bootstrap' });

var target = document.getElementById('container');
ej.popups.createSpinner({ target: target });
ej.popups.showSpinner(target);
```

## Key Methods Reference

| Method | Purpose | Usage |
|--------|---------|-------|
| `createSpinner(config)` | Initialize spinner for a target | `ej.popups.createSpinner({ target: element })` |
| `showSpinner(target)` | Display the spinner | `ej.popups.showSpinner(targetElement)` |
| `hideSpinner(target)` | Hide the spinner | `ej.popups.hideSpinner(targetElement)` |
| `setSpinner(config)` | Set spinner type/template | `ej.popups.setSpinner({ type: 'Bootstrap' })` |

**Important:** `setSpinner()` must be called BEFORE `createSpinner()` to take effect.

## Common Use Cases

**Loading Data from Server**
```javascript
// Show spinner while fetching data
ej.popups.showSpinner(target);

fetch('/api/data')
    .then(r => r.json())
    .then(data => {
        populateUI(data);
        ej.popups.hideSpinner(target);  // Hide when done
    });
```

**File Upload Progress**
```javascript
ej.popups.showSpinner(uploadTarget);

uploadFile(file)
    .then(() => {
        ej.popups.hideSpinner(uploadTarget);
        showMessage('Upload complete');
    });
```

**Grid Data Binding**
```javascript
// Show spinner while grid loads data
ej.popups.showSpinner(gridContainer);

// Grid handles its own loading after initialization
// Hide spinner when grid dataBound event fires
gridInstance.dataBound = function() {
    ej.popups.hideSpinner(gridContainer);
};
```

## Next Steps

1. **Start with Getting Started** - [references/getting-started.md](references/getting-started.md)
2. **Choose your spinner type** - [references/spinner-types.md](references/spinner-types.md)
3. **Customize appearance** - [references/styling-customization.md](references/styling-customization.md)
4. **Add custom templates if needed** - [references/templates.md](references/templates.md)
5. **Review available methods** - [references/configuration-methods.md](references/configuration-methods.md)

---

For more information on Syncfusion ASP.NET Core components, see the [main library guide](../).
