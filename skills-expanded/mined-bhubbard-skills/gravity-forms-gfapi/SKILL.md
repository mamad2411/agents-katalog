---
name: gravity-forms-gfapi
description: "Deep dive into the GFAPI class for programmatic CRUD operations on Forms and Entries."
---

# Gravity Forms GFAPI Class

The `GFAPI` class is the correct and supported way to interact with Gravity Forms data programmatically. It allows you to create, read, update, and delete entries and forms, ensuring that all proper hooks and validations fire.

## Reference
[GFAPI Class Documentation](https://docs.gravityforms.com/gfapi-class/)

## Entry Operations

### Read
```php
$entry = GFAPI::get_entry( $entry_id );
$entries = GFAPI::get_entries( $form_id, $search_criteria, $sorting, $paging, $total_count );
```

### Create
```php
$entry = array(
    'form_id' => 1,
    '1'       => 'Value for field 1',
    '2'       => 'Value for field 2'
);
$result = GFAPI::add_entry( $entry );
```

### Update
```php
$entry = GFAPI::get_entry( $entry_id );
$entry['1'] = 'New Value';
$result = GFAPI::update_entry( $entry );
```

### Delete
```php
$result = GFAPI::delete_entry( $entry_id );
```

## Form Operations

### Read
```php
$form = GFAPI::get_form( $form_id );
$forms = GFAPI::get_forms();
```

### Create/Update/Delete
- `GFAPI::add_form( $form )`
- `GFAPI::update_form( $form )`
- `GFAPI::delete_form( $form_id )`

## Best Practices
- Never use `$wpdb` to directly query or update entries unless strictly necessary for complex performance reasons. Direct queries bypass important hooks (like `gform_after_submission` or `gform_entry_updated`).
