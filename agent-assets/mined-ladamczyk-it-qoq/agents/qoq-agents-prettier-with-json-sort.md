# @ladamczyk/qoq-prettier-with-json-sort — Agent Context

Prettier configuration template that extends `@ladamczyk/qoq-prettier` with automatic JSON key sorting.

## Usage

Reference it in `.prettierrc`:

```json
"@ladamczyk/qoq-prettier-with-json-sort"
```

Or in `prettier.config.js`:

```js
export default '@ladamczyk/qoq-prettier-with-json-sort';
```

## Config

```json
{
  "trailingComma": "es5",
  "printWidth": 100,
  "singleQuote": true,
  "plugins": ["prettier-plugin-sort-json"],
  "jsonRecursiveSort": true
}
```

All JSON files formatted by Prettier will have their keys sorted recursively. Requires `prettier-plugin-sort-json` to be installed in the consumer project.
