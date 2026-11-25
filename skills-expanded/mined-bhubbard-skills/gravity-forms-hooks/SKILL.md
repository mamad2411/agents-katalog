---
name: gravity-forms-hooks
description: "Instructions for utilizing Gravity Forms hooks (Actions, Filters, JavaScript) to modify default functionality."
---

# Gravity Forms Hooks

## Introduction

Gravity Forms provides an extensive list of hooks (actions and filters) that can be used to modify almost any aspect of its default functionality.

## Types of Hooks

### 1. Action Hooks
Action hooks allow you to perform additional actions when an event takes place in Gravity Forms (e.g., after an entry is saved, or when a form is rendered).
- **Reference**: [Action Hooks Documentation](https://docs.gravityforms.com/category/developers/hooks/actions/)
- **Common Actions**:
  - `gform_after_submission`: Fired after a form has been successfully submitted and the entry created. Great for sending data to third-party APIs.
  - `gform_pre_submission`: Fired before the entry is saved. Useful for modifying `$_POST` data.

### 2. Filters
Filters allow you to modify data before it is used or displayed by Gravity Forms (e.g., changing the validation result, or modifying form HTML).
- **Reference**: [Filters Documentation](https://docs.gravityforms.com/category/developers/hooks/filters/)
- **Common Filters**:
  - `gform_validation`: Used to add custom validation logic to a form or field.
  - `gform_field_validation`: Used to validate a specific field.
  - `gform_pre_render`: Used to modify the form object before the form is displayed (e.g., dynamically populating dropdown choices).

### 3. JavaScript Hooks
JavaScript hooks allow you to perform actions or modify data as the user interacts with the form on the frontend.
- **Reference**: [JavaScript Hooks Documentation](https://docs.gravityforms.com/category/developers/hooks/javascript/)
- **Common JS Hooks**:
  - `gform_post_render`: Triggered after the form is rendered via AJAX. Use this to re-initialize custom scripts (like datepickers or sliders) on form load or pagination.

## Best Practices
- Many Gravity Forms hooks support appending the form ID to target a specific form (e.g., `gform_after_submission_5` targets only form ID 5). This is preferred over checking the form ID inside a generic callback.
- Always return the expected data type when using filters (e.g., `gform_pre_render` must return the `$form` object).
