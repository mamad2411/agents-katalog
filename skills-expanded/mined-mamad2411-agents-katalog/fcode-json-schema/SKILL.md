---
name: fcode-json-schema
description: Author Factorial Code process input-parameter schemas (parametersSchema.json) — every supported input type and validation option, with a complete annotated sample. Use when creating or editing a parametersSchema.json, or defining a Factorial Code (fcode) process's input parameters or form fields.
license: MIT
metadata:
  category: factorial-code
---

# Factorial Code — input parameter schemas

A process's input parameters are defined by a JSON Schema in
`parametersSchema.json`. The same schema is what `fcode-forms` renders as a web
form, so designing the schema *is* designing the form. Values arrive in code as
`fcode.context.parameters` (see `fcode-javascript` / `fcode-python`).

Schemas render with [react-jsonschema-form](https://rjsf-team.github.io/react-jsonschema-form/),
so its `ui:` options apply.

## How to author one

1. Top level is `"type": "object"` with a `properties` map (one entry per field)
   and an optional `required` array.
2. Pick a `type` per field (`string`, `integer`, `number`, `boolean`, `array`,
   `object`) and add validation (`minimum`/`maximum`, `format`, `enum`/`oneOf`,
   `uniqueItems`, nested `properties`).
3. Control rendering with a per-field `ui` object (e.g.
   `"ui": { "ui:widget": "textarea" }`).
4. **Open `assets/parametersSchema.sample.json`** for a complete, copy-pasteable
   schema exercising every supported type — adapt fields from it rather than
   guessing the shape.

## Field types & widgets (in the sample)

- **Text** — `"type": "string"`; `format: "email"`; `ui:widget` of `textarea`,
  `color`, `hidden`, or `file`.
- **Secret** — `"isSensitive": true` masks the input (e.g. passwords/tokens).
- **Numbers** — `integer` / `number` with `minimum` / `maximum`.
- **Boolean** — `"type": "boolean"`.
- **Choices** — `enum` (select), `oneOf` of `{ const, title }` (labeled radio
  with `ui:widget: "radio"`), or an array with `ui:widget: "checkboxes"` +
  `uniqueItems`.
- **Structured** — nested `object` with its own `properties`/`required`; arrays
  of strings or of objects (`type: "array"` + `items`); raw JSON via
  `"ui": { "ui:field": "json" }`.
- **Conditional fields** — use top-level `dependencies` to show/hide fields based
  on another field's value (see `anotherBooleanField` in the sample).

## Gotchas

- **A file field** (`"ui:widget": "file"`) is auto-uploaded to Storage before
  the process runs; the parameter arrives as an `fcode.storage://…` reference,
  not the file contents. Strip the prefix before `fcode.storage.download(...)`.
- **`isSensitive: true`** only affects display/masking — still read the value
  from a secret variable, never hardcode it.
- The schema is the single source of the form's fields — to change fields, edit
  the schema, not the form embed code.
