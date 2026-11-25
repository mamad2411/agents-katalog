---
name: gravity-forms-javascript-hooks
description: "Utilizing frontend JS events like gform_post_render."
---

# Gravity Forms JavaScript Hooks

Gravity Forms heavily utilizes AJAX for rendering forms, pagination, and conditional logic. Therefore, any custom JavaScript (like initializing a custom datepicker or a slider) needs to be aware of the Gravity Forms lifecycle.

## Reference
[JavaScript Hooks Documentation](https://docs.gravityforms.com/category/developers/hooks/javascript/)

## Key JavaScript Hooks

### `gform_post_render`
Fires after the form is rendered, either on initial page load or after an AJAX request (like validation failure or navigating multi-page forms).
**Primary Use Case**: Re-initializing custom scripts on your form fields.

```javascript
jQuery(document).on('gform_post_render', function(event, form_id, current_page){
    if(form_id == 5) {
        // Initialize your custom JS plugin here
        jQuery('.my-custom-class').myPlugin();
    }
});
```

### `gform_page_loaded`
Fires when a new page is loaded in a multi-page form.

### `gform_post_conditional_logic`
Fires after conditional logic has been evaluated and fields have been shown or hidden.

## Best Practices
- If your form uses AJAX, you **must** wrap your initialization code in a listener for `gform_post_render`. Code inside a standard `$(document).ready()` block will not fire when the form is re-rendered via AJAX after a validation error or page turn.
- Always check the `form_id` variable inside the event handler to ensure your script only runs on the intended form.
