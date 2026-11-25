---
name: gravity-forms-orbital-theme
description: "Deep dive into styling forms using the new Orbital Theme CSS API."
---

# Gravity Forms Orbital Theme

Introduced in Gravity Forms 2.7, the Orbital theme utilizes CSS custom properties (variables) to control the styling of forms, providing a CSS API that makes customizations drastically simpler than targeting deep, nested CSS selectors.

## Reference
[Theme Framework Documentation](https://docs.gravityforms.com/category/developers/theme-framework/)

## The CSS API
Gravity Forms defines variables at the `.gform_wrapper` level. By redefining these variables in your theme's stylesheet (or the block editor), you instantly cascade the styles down to all form components.

### Example Variables
```css
/* Container padding */
--gform-theme-spacing-container-padding: 20px;

/* Colors */
--gform-theme-color-primary: #007bff;
--gform-theme-control-background-color: #ffffff;
--gform-theme-control-border-color: #cccccc;
--gform-theme-control-border-radius: 4px;

/* Buttons */
--gform-theme-button-background-color: var(--gform-theme-color-primary);
--gform-theme-button-color: #ffffff;

/* Typography */
--gform-theme-typography-font-family: 'Open Sans', sans-serif;
```

## How to Customize

### 1. In the Block Editor (No Code)
If using the Gravity Forms block in the WordPress block editor, the settings panel provides UI controls for colors, borders, and sizes. These controls automatically inject the CSS variables inline for that specific form.

### 2. In Your Theme (Global Code)
To apply a consistent style across all forms on the site, add the CSS variables to your theme's stylesheet, targeting the `.gform_wrapper` class.

```css
.gform_wrapper {
    --gform-theme-color-primary: #ff5722;
    --gform-theme-control-border-radius: 8px;
    --gform-theme-control-border-color: #e0e0e0;
}
```

## Best Practices
- Use the CSS variables to style forms. Avoid writing rules like `.gform_wrapper input[type="text"] { border-color: red !important; }`. The `!important` flag breaks the block editor's styling controls.
- The CSS variables are thoroughly documented in the Gravity Forms stylesheet itself or via browser dev tools by inspecting the `.gform_wrapper` element.
