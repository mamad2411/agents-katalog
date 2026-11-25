---
name: Folio Forms
description: Build and change Folio forms (kind form) with create_form / update_form — fields, types, the paired data table where the answers land, public forms.
version: "1.0.0"
tags: [folio, forms, tables]
---

# Folio forms (`kind: form`)

A form is a page of questions. Every answer becomes a new **row of a data
table paired with the form**: each field of the form fills one column of that
table. The form file (`<name>.form.md`) holds only the definition; the answers
live in the table (`<name>.table.md`, a child page of the form when the form
created it).

## Tools

| Tool | What it does |
|---|---|
| `read_page` (form id) | The definition: `form.title`, `description`, `public`, `submitButton`, `fields` (`columnId`, `label`, `help`, `required`, `kind`), `form.table.id` (the paired table) and the `etag` |
| `create_form` | A new form. Without `table` it creates a new paired table too (one column per field). With `table` (a table page id) the form goes under that existing table |
| `update_form` | Change the title, description, submit button label, `public`, and/or the whole list of `fields` |
| `folio_table_query` (`form.table.id`) | Read the answers |
| `folio_table_update_column` | Change the choices of a select/status field, or a column's type (the field follows the column) |

## Field types

`text` (one line, the default), `longtext`, `number`, `date`, `checkbox`,
`select` (choices in `options`; `multiple: true` for several), `status`
(without `options` it gets the status preset PLANNING … CANCELLED), `user`,
`link`. Give `options` as plain labels (`["Small", "Medium", "Large"]`) or as
`{ "value": "Large", "color": "green" }`.

How the answerer sees them: `select`/`status` show the column's options as a
radio group (up to 6 options) or a dropdown (more), several values
(`multiple: true`) as checkboxes or a searchable list, status with its colours;
`user` is a searchable member picker; `link` is a URL plus an optional label —
they are **not** plain text boxes. The choices come live from the paired table's
column, so changing the options with `folio_table_update_column` changes the
form at once, and a value outside the options is rejected on submit. Give a
select/status field its `options` when you create it — without any, the form
has nothing to offer. A `user` field is shown only to signed-in members; an
anonymous answerer of a `public` form does not see it (the answer is ignored),
so do not make a `user` field the only way to identify someone in a public form
and do not rely on it being `required` there.

Folio adds the columns `submitted_at` and `submitter` to the table by itself
on the first answer — never make fields for them.

## Creating a form

The user: "make a feedback form with name, rating and a comment, rating
required". Unless they named another place, create it as a child of the page
that is open now (`parentPath` from the current context):

```json
{
  "space": "team",
  "parentPath": "events/offsite",
  "title": "Offsite feedback",
  "description": "Two minutes, anonymous answers welcome.",
  "fields": [
    { "label": "Your name", "type": "text" },
    { "label": "Rating", "type": "select", "options": ["1", "2", "3", "4", "5"], "required": true },
    { "label": "Comment", "type": "longtext", "help": "What should we keep or change?" }
  ]
}
```

A form on a table that already exists (its columns become the fields):
`{ "space": "team", "title": "New request", "table": "<table page id>" }`.
Add `fields` to pick and word only some columns: `{ "columnId": "priority",
"label": "How urgent is it?", "required": true }` reuses a column, a field
without `columnId` adds a new one.

## Changing a form

1. `read_page` the form: take its `etag` and its `fields`.
2. `update_form` with `id`, `etag` and only what changes. `fields`, when
   given, is the **whole new list in order**: list every field that stays by
   its `columnId` (its label, help and required stay unless you give new
   ones); a field without `columnId` adds a column (it needs a `label`); a
   field left out disappears from the form only — its column and the answers
   already collected stay in the table (say so to the user).
3. An etag error means someone changed the form meanwhile: read it again,
   apply the change on top, retry with the new etag.

Example — make "Comment" required and add an e-mail question at the end:

```json
{
  "id": "<form id>",
  "etag": "<etag from read_page>",
  "fields": [
    { "columnId": "your_name" },
    { "columnId": "rating" },
    { "columnId": "comment", "required": true },
    { "label": "E-mail", "type": "text" }
  ]
}
```

## Who can answer

Space members (viewer and up) can always answer. `public: true` additionally
lets anyone with a **share link of the form** answer without signing in — the
share link itself is made by the user in the web app (Share), not by you.
Turn `public` on only when the user asked for an open/anonymous form.

## After the write

Re-read with `read_page` and end the answer with links to the form and, when
a new table was created, to the table: `[<title>](/s/<space>/p/<id>)`.
