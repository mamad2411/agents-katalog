---
name: use-table
description: Use this skill whenever the user wants to display structured data, create a table, or modify an existing data grid in Vue. You MUST invoke this skill even if the user only says "show a list of users", "add an action column", or "display the data", without explicitly mentioning "table", "Ant Design", or "template style".
---

# Ant Design Vue Table (Template Style)

Use this skill to implement Ant Design Vue tables using the **Template Style API** instead of the traditional columns array configuration. 

## When to Use

- Whenever you need to render a table (`<a-table>`) to display structured data.
- When the user asks to add columns, format table cells, or add actions to a table row.
- When migrating an existing table to the template style.

## Gotchas

- **Template Default Slot Overriding**: If a component provides only a default slot, use the shortcut syntax directly on the component tag (`<a-table-column #="{ record }">`). **Never** wrap it in `<template #default>` if it's the only slot being used.
- **Kebab-case Enforcement**: Always use kebab-case for Ant Design Vue components (e.g., `<a-table-column>`). Do not use camelCase or PascalCase in the template.
- **No `key` on `v-for`**: In this specific project, `v-for` directives inside table columns must **NOT** include a `key` attribute. This is a strict project rule that defies standard Vue conventions.
- **No `key` on Columns**: Do not add `key` attributes to `<a-table-column>` or `<a-table-column-group>`.
- **Avoid Array Configuration**: Never use the `:columns` prop with a JavaScript array to define columns. Always use the Template Style API.

## Code Example

For a complete and standard example of a table implemented according to these rules, see:
[references/EXAMPLE.md](references/EXAMPLE.md)