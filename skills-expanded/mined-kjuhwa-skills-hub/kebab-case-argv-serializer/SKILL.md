---
name: kebab-case-argv-serializer
description: Serialize a yargs-parsed argv back into argv[] for spawning a subprocess, translating camelCase option keys to kebab-case, emitting `--no-<flag>` for booleans, and repeating flags for arrays.
category: cli
version: 1.0.0
version_origin: extracted
tags: [cli, yargs, argv, subprocess, serialization]
confidence: medium
source_type: extracted-from-git
source_url: https://github.com/ChromeDevTools/chrome-devtools-mcp.git
source_ref: main
source_commit: 0a6aaa52ebacb2db834ffa437863e5844aa3730b
source_project: chrome-devtools-mcp
source_path: src/daemon/utils.ts
imported_at: 2026-04-18T00:00:00Z
---

# Kebab-Case Argv Serializer

## When to use

- You have a CLI that parses options with yargs (camelCase keys) and needs to spawn a child process whose argv format matches the original option definitions (kebab-case `--browser-url`, `--no-headless`, `--chrome-arg foo --chrome-arg bar`).
- You want `argv` round-tripping: parse → modify → re-emit.

## How it works

- Accept the yargs options definition and the parsed argv. For each key in the options definition (skip keys not defined so you don't leak internals):
  - Skip `undefined`/`null`.
  - Convert camelCase → kebab-case: `k.replace(/[A-Z]/g, m => '-' + m.toLowerCase())`.
  - `typeof value === 'boolean'` → `--flag` if true, `--no-flag` if false.
  - `Array.isArray(value)` → push `--flag val` once per entry.
  - Otherwise → `--flag String(value)`.
- Return `string[]` suitable for `spawn(cmd, args, ...)`.

## Example

```ts
export function serializeArgs(options, argv): string[] {
  const out: string[] = [];
  for (const key of Object.keys(options)) {
    const value = argv[key];
    if (value === undefined || value === null) continue;
    const kebab = key.replace(/[A-Z]/g, m => `-${m.toLowerCase()}`);
    if (typeof value === 'boolean') out.push(value ? `--${kebab}` : `--no-${kebab}`);
    else if (Array.isArray(value)) for (const v of value) out.push(`--${kebab}`, String(v));
    else out.push(`--${kebab}`, String(value));
  }
  return out;
}
```

## Gotchas

- Iterate `Object.keys(options)`, not `Object.keys(argv)`. Yargs injects `_`, `$0`, and alias copies into argv that you don't want to re-emit.
- Always emit `--no-foo` for explicit false booleans; emitting nothing defers to the child's default, which may differ.
- For optional array-valued flags, emit `--flag val --flag val2`, not `--flag val,val2` — comma-joining only works if your option parser supports it.
- Don't serialize defaulted options unless the caller explicitly set them, or consider the default. A common enhancement is `if (value === options[key].default) continue;` but it can confuse clients that depend on explicit passthrough.
- String-ify non-string values with `String(value)`; never `JSON.stringify` or the child sees extra quotes.
