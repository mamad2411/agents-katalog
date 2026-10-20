# @ladamczyk/qoq-jscpd — Agent Context

JSCPD configuration preset used internally by `@ladamczyk/qoq-cli`.

## Config (`index.json`)

```json
{
  "absolute": true,
  "format": "javascript,jsx,typescript,tsx",
  "ignore": ["**/*.spec.js", "**/*.spec.jsx", "**/*.spec.ts", "**/*.spec.tsx"],
  "threshold": "2"
}
```

- Checks JS, JSX, TS, and TSX files
- Ignores all test/spec files
- Fails when code duplication exceeds 2%
- Uses absolute paths in output

The threshold is overridden by the `jscpd.threshold` field in `qoq.config.js` when used via `@ladamczyk/qoq-cli`.
