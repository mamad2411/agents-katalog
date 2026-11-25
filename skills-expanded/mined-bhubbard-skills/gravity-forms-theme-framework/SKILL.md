---
name: gravity-forms-theme-framework
description: "Best practices for styling Gravity Forms and using the Theme Framework."
---

# Gravity Forms Theme Framework

## Introduction

The Theme Framework is a modern approach to styling and displaying Gravity Forms, introduced in Gravity Forms 2.7+. It uses a CSS API with CSS custom properties (variables) to allow easy customization without writing complex CSS overrides.

## Core Concepts

### Orbital Theme
Orbital is the default built-in theme framework for Gravity Forms. It provides a foundation that is highly customizable and accessible.
- **Reference**: [Theme Framework Documentation](https://docs.gravityforms.com/category/developers/theme-framework/)

### CSS API
Instead of targeting deep, specific CSS classes to change colors or spacing, developers can redefine CSS custom properties.
- **Example**:
  ```css
  .gform_wrapper {
      --gform-theme-control-border-color: #ff0000;
      --gform-theme-button-background-color: #0000ff;
  }
  ```

### Form Settings
Users can configure block settings in the WordPress block editor to change styling, which under the hood modifies these CSS variables.

## Best Practices
- **Do not** use `!important` tags or deeply nested CSS selectors to override default Gravity Forms styles if you are using the Orbital theme. Use the provided CSS variables instead.
- If you need to write custom CSS for specific layouts, leverage the standard CSS classes provided by Gravity Forms (e.g., `.gfield`, `.gform_wrapper`).
- When creating custom field types via the Field Framework, ensure your HTML markup aligns with the Theme Framework structure so it inherits standard styling automatically.
