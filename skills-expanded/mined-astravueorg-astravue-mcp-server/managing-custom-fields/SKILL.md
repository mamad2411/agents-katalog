---
name: managing-custom-fields
description: Creates, configures, and manages custom fields and dropdown options on tasks in Astravue. Use when working with custom fields, adding dropdown options, setting field values on tasks, or asking "what custom fields does this project have?".
---

# Managing Custom Fields

## Workflow

1. **Discover existing fields**

   `astravue_get_custom_fields` — list fields for a project or get values for a specific task.

2. **Set a field value**

   - For dropdown fields, call `astravue_list_custom_field_options` first to find valid options
   - `astravue_set_custom_field_value` — set the value on a task
   - Value format depends on field type: strings for text, `true`/`false` for checkbox, `yyyy-MM-dd` for date, option name or ID for dropdowns

3. **Create a new field**

   - `astravue_create_custom_field` — define field name, type, and scope (project or space)
   - For dropdown types, add options with `astravue_create_custom_field_option`
   - Supported types: SINGLE_LINE_TEXT, MULTI_LINE_TEXT, NUMBERS, DATE, PHONE, EMAIL, CHECKBOX, SINGLE_SELECT_DROPDOWN, MULTI_SELECT_DROPDOWN, PERCENTAGE, CURRENCY, URL

4. **Delete fields or options**

   - `astravue_delete_custom_field_option` — remove a dropdown option (can migrate tasks to a replacement)
   - `astravue_delete_custom_field` — remove the field and all its values from every task in scope

   Always confirm deletions with the user. These actions cannot be undone.

## Important

- Max 5 fields per type per scope
- Requires space admin (space-level) or project admin (project-level) permissions for create and delete operations
