# @ladamczyk/qoq-knip — Agent Context

Knip configuration builder used internally by `@ladamczyk/qoq-cli`. Can also be used directly.

## Exports

### `getKnipConfig(srcPath?, entry?, project?, ignore?, ignoreDependencies?, ignoreBinaries?, ignoreFiles?, ignoreMembers?, ignoreUnresolved?)`

Returns a Knip configuration object. All parameters are optional with sensible defaults.

| Parameter            | Default                  |
| -------------------- | ------------------------ |
| `srcPath`            | `'.src'`                 |
| `entry`              | `['{srcPath}/index.js']` |
| `project`            | `['{srcPath}/**/*.js']`  |
| `ignore`             | `['package.json']`       |
| `ignoreDependencies` | `[]`                     |
| `ignoreBinaries`     | `[]`                     |
| `ignoreFiles`        | `[]`                     |
| `ignoreMembers`      | `[]`                     |
| `ignoreUnresolved`   | `[]`                     |

### Pre-built configs

```js
import { jsConfig, jsReactConfig, tsConfig, tsReactConfig } from '@ladamczyk/qoq-knip';
```

| Export          | Entry           | Project glob               |
| --------------- | --------------- | -------------------------- |
| `jsConfig`      | `src/index.js`  | `src/**/*.js`              |
| `jsReactConfig` | `src/index.jsx` | `src/**/*.{js,jsx}`        |
| `tsConfig`      | `src/index.ts`  | `src/**/*.{js,ts}`         |
| `tsReactConfig` | `src/index.tsx` | `src/**/*.{js,jsx,ts,tsx}` |
