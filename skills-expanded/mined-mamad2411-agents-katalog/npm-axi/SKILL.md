---
name: npm-axi
description: >
  Use when you need npm registry data — search for packages, check a package's latest
  version, license, dependency count or download counts, or list recent versions. Returns
  token-efficient TOON output. Read-only, no auth required.
---

# npm-axi

`npm-axi` is an [AXI](https://github.com/kunchenguid/axi) for the public npm registry. It
returns token-efficient TOON output designed for agents. Read-only, no authentication.

Run without a global install:

```sh
npx -y npm-axi <command> [args] [flags]
```

## Commands

### search — find packages

```sh
npx -y npm-axi search "react router" --limit 20
```

Returns a minimal `name,version,description` table plus the total match count:

```
count: 20 of 1240 total
packages[20]{name,version,description}:
  react-router,7.1.1,Declarative routing for React
  ...
```

### view — package details

```sh
npx -y npm-axi view zod          # preview README
npx -y npm-axi view zod --full   # complete README
```

Includes pre-computed aggregates (dependency count, weekly downloads) and a truncated
README with a size hint:

```
package:
  name: zod
  version: 3.24.1
  license: MIT
  description: TypeScript-first schema declaration and validation library
  dependencies: 0
  weeklyDownloads: 24500000
  homepage: https://zod.dev
  repository: https://github.com/colinhacks/zod
  published: 2024-12-30
  readme: First 800 chars...
    readmeChars: 5421
help[1]: Run `npm-axi view zod --full` to see complete README
```

### versions — recent versions

```sh
npx -y npm-axi versions typescript --limit 15
```

Newest-first, with the `latest` dist-tag and total version count.

### downloads — download stats

```sh
npx -y npm-axi downloads express
```

```
downloads:
  package: express
  lastWeek: 30000000
  lastMonth: 120000000
```

## Notes

- Errors are returned as structured TOON on stdout with an actionable `help` line.
- Exit codes: `0` success, `1` error (e.g. package not found), `2` usage error.
- Unknown packages return a `NOT_FOUND` error suggesting a `search`.
