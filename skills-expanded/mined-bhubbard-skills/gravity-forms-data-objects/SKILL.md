---
name: gravity-forms-data-objects
description: "Guides the usage and manipulation of core Gravity Forms Data Objects."
---

# Gravity Forms Data Objects

## Introduction

Data Objects are objects/arrays that are used across all Gravity Forms APIs. They contain core Gravity Forms information such as form configuration and form submission data (a.k.a entry data). When working with Gravity Forms, you will frequently interact with these objects.

## Core Data Objects

### 1. Entry Object
The Entry object contains all properties of a particular entry such as date created, client IP, and submitted field values.
- **Reference**: [Entry Object Documentation](https://docs.gravityforms.com/entry-object/)
- **Common Usage**: Accessing submitted data inside hooks like `gform_after_submission`. Field values are typically accessed using their field ID as the key (e.g., `$entry['1']`).

### 2. Form Object
The Form object contains all properties of a particular form such as form title, fields, notification, and confirmation. This object is available to most Gravity Forms hooks.
- **Reference**: [Form Object Documentation](https://docs.gravityforms.com/form-object/)
- **Common Usage**: Iterating over `$form['fields']` to find specific fields or modifying form settings before rendering using `gform_pre_render`.

### 3. Field Object
The Field object contains all settings for a particular field. It is part of the Form object and can be manipulated to dynamically change the way the field is displayed.
- **Reference**: [Field Object Documentation](https://docs.gravityforms.com/field-object/)
- **Common Usage**: Checking the type of a field (`$field->type`) or modifying its choices dynamically.

### 4. Notifications Object
The Notifications object is an associative array containing all configured notifications for a form.
- **Reference**: [Notifications Object Documentation](https://docs.gravityforms.com/notifications-object/)
- **Common Usage**: Modifying routing or recipient emails before a notification is sent out via `gform_notification`.

### 5. Confirmations Object
The Confirmations object is an associative array containing all configured confirmations for a form.
- **Reference**: [Confirmations Object Documentation](https://docs.gravityforms.com/confirmations-object/)
- **Common Usage**: Dynamically changing the confirmation message or redirect URL via `gform_confirmation`.

### 6. Conditional Logic Object
Conditional Logic, when applied to the form or page button or to any field, controls the visibility of that element based on a choice selected or a value entered by the user.
- **Reference**: [Conditional Logic Object Documentation](https://docs.gravityforms.com/conditional-logic-object/)

### 7. Button Object
The Button Object contains the settings configured for the form button, such as the button text.
- **Reference**: [Button Object Documentation](https://docs.gravityforms.com/button-object/)

## Best Practices
- Always refer to the official documentation links provided to understand the structure of these objects.
- Remember that the `$entry` object is typically an associative array, while `$form` contains a mix of properties and arrays, and fields are usually objects instances of `GF_Field`.
