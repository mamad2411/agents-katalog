---
name: nitro-model
description: For projects using nitro-web only. Adding or changing a monastery model, schema field, validation rule, or enum in a nitro-web app.
---

  - Models live in `server/models/` and are auto-loaded, the filename becomes `db.<name>`. These files start with `// @ts-nocheck`.
  - Changing the model schema fields may need a migration, see nitro-migration skill.

# Model shape

  - If several models share a field group, that's a good candidate for a shared fragment, export a function returning the fragment.
  - Default export with `fields`, optional `rules`, and lifecycle hooks.
  - Keep validation first in the fields, or if not, then in the beforeValidate hook, or then in the controller at worst.
  - A field missing from `fields` is stripped on validation.
  - Below is just a basic overview, see https://boycce.github.io/monastery/definition/ for the full documentation if needed.

  ```js
  import { statusOptions } from '../constants.js'

  export default {
    fields: {
      company: { model: 'company', required: true },      // reference to another model
      number: { type: 'string', required: true, index: 'text' },
      status: { type: 'string', enum: statusOptions.map(o => o.value), default: 'draft' },
      total: { type: 'number', default: 0 },
      lines: [{                                            // array of subdocuments
        description: { type: 'string', required: true },
        amount: { type: 'number', required: true },
      }],
    },  

    rules: { ... },
  }
  ```

# Lifecycle hooks

  Data can arrive as an array on bulk inserts, so normalise before looping.

  ```js
  beforeValidate: [
    async function (data) {
      const rows = Array.isArray(data) ? data : [data]
      for (const row of rows) { ... }
    },
  ],
  ```

# Custom rules

  `this` is the document root, and `path` is the full dotted path, which is how you reach siblings in an
  array of subdocuments.

  Attach by naming the rule on the field: `code: { type: 'string', uniqueLineCode: true }`. Add
  `validateUndefined: true` if it should also run when the value is missing.

  ```js
  rules: {
    uniqueLineCode: {
      message: 'This code is already used on another line.',
      fn: function (value, _ruleArg, path) {          // path is e.g. lines.1.code
        const index = Number(path.split('.')[1])
        return !(this.lines || []).some((l, i) => i !== index && l.code === value)
      },
    },
  }
  ```
