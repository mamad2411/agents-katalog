---
name: gravity-forms-database
description: "Understanding the Gravity Forms database schema."
---

# Gravity Forms Database

While `GFAPI` is the recommended way to interact with data, understanding the database schema is necessary for direct SQL queries when writing highly optimized reports or dealing with massive datasets where `GFAPI` would hit memory limits.

## Reference
[Database Documentation](https://docs.gravityforms.com/category/developers/database/)

## Core Tables

Gravity Forms 2.3+ significantly changed the database structure, moving away from relying heavily on standard WordPress tables.

### `wp_gf_form`
Stores the forms.
- `id`: Form ID
- `title`: Form Title
- `date_created`: Creation datetime

### `wp_gf_form_meta`
Stores the massive JSON string representing the Form Object (fields, notifications, confirmations).
- `form_id`: Relates to `wp_gf_form.id`
- `display_meta`: JSON string of the Form Object
- `entries_grid_meta`: JSON string for admin entry grid settings

### `wp_gf_entry`
Stores the core data for an entry.
- `id`: Entry ID
- `form_id`: Relates to `wp_gf_form.id`
- `date_created`: Creation datetime
- `is_starred`, `is_read`, `ip`, `source_url`, `user_agent`, `payment_status`

### `wp_gf_entry_meta`
Stores the actual submitted field values for the entries.
- `id`: Meta ID
- `form_id`: Relates to `wp_gf_form.id`
- `entry_id`: Relates to `wp_gf_entry.id`
- `meta_key`: The Field ID (e.g., '1', '4.3', or a custom string for hidden meta)
- `meta_value`: The submitted value (stored as a string)
- `item_index`: Used for repeater fields or multi-file uploads

## Best Practices
- **Never** write direct SQL INSERT or UPDATE queries to these tables unless absolutely necessary. Missing a hook or leaving data in an inconsistent state can break the form or add-on functionality. Use `GFAPI`.
- When reading from `wp_gf_entry_meta` for reporting, be aware that `meta_value` is always a string. If you are comparing numbers or dates, you must cast them in your SQL query.
