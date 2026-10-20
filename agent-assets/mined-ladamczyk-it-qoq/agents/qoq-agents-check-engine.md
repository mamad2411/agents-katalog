# @ladamczyk/check-engine — Agent Context

`@ladamczyk/check-engine` validates that a project's `engines.node` field is consistent with the `engines.node` requirements declared by its dependencies. It is monorepo-aware.

## Command

```bash
check-engine
```

No configuration file required. Run it from the project root.

- `--include <list>` — also check these dependency groups, comma-separated: `dev` (`devDependencies`), `peer` (`peerDependencies`), `optional` (`optionalDependencies`). Any other value prints a one-line error to stderr and exits `1` without checking anything. A name in several groups is checked once (precedence: dependencies, dev, peer, optional).
- `--no-lts` — skip the Node LTS lookup and its advisory.
- `--json` — also write the report to stdout as one JSON document, `{ ok, lts, workspaces }` (`workspaces` sorted by `path`, `lts` is `null` with `--no-lts`). Human text stays on stderr.
- `--quiet` — print nothing to stderr when every workspace passes (warnings and advisories included); failures still print in full. Combined with `--json`, the document is still written.

## Node LTS advisory

Unless `--no-lts` is passed, the Node release list is fetched once per run from `https://nodejs.org/download/release/index.json`. When it is unreachable, `./node.json` in the project root is used instead; if neither works the run fails with instructions. Offline? Download `https://nodejs.org/download/release/index.json` to `./node.json` in the project root, or use `--no-lts`.

A workspace whose `engines.node` floor has a lower major than the maintained LTS gets a yellow `⚠` advisory line. The advisory never changes the result or the exit code.

## What it checks

For each `package.json` in scope:

1. Reads the package's own `engines.node` value (warns if missing).
2. Collects `engines.node` from every entry in `dependencies` (falls back to `devDependencies` when `dependencies` is empty).
3. Compares the configured range against the collected dependency requirements.
4. Prints one line per workspace and exits with code `1` once, at the end, if any workspace's `engines.node` is not compatible with a dependency's requirement. A ranged `engines.node` must be a subset of every dependency range.

## Monorepo support

Discovered automatically from the root `package.json` `workspaces` field. Glob patterns with `*` are expanded with `fs.globSync`; each discovered sub-package is checked individually.

## Integration

Typically wired into the pre-push hook via `@ladamczyk/qoq-cli`:

```json
"scripts": {
  "check:engine": "check-engine"
}
```

Or directly as part of a CI step to enforce node compatibility across all packages before publish.
