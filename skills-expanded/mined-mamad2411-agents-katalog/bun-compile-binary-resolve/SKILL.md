---
name: bun-compile-binary-resolve
description: Resolve external native binaries at runtime via env → config → vendor-dir chain when shipping a `bun build --compile` binary where `import.meta.url` is frozen.
category: bun
version: 1.0.0
version_origin: extracted
tags: [bun, compile, binary, resolver, vendor]
confidence: high
source_type: extracted-from-git
source_url: https://github.com/coleam00/Archon.git
source_ref: dev
source_commit: d89bc767d291f52687beea91c9fcf155459be0d9
source_project: Archon
imported_at: 2026-04-18T00:00:00Z
linked_knowledge: [bun-compile-freezes-import-meta]
---

# External Binary Resolver for `bun build --compile`

## When to use

- You use `bun build --compile` to ship a single-file binary.
- One of your dependencies (SDK, native bridge) uses `createRequire(import.meta.url)` or `__dirname`-relative lookup to locate an auxiliary native binary (Rust/C binary sibling).
- In the compiled binary, those lookups fail because Bun freezes `import.meta.url` / `import.meta.dir` to the build host's path, which doesn't exist on the user's machine.

## Steps

1. **Add a build-time constant** (e.g. `BUNDLED_IS_BINARY`) that the build script flips from `false` to `true` immediately before `bun build --compile` and restores afterward. (See the `bundled-defaults-generator` skill for the pattern.)
2. **At the binary-resolution call site**, early-return `undefined` in dev mode so the SDK uses its normal node_modules resolution:
   ```ts
   if (!BUNDLED_IS_BINARY) return undefined;
   ```
3. **Try an ordered resolution chain** in binary mode. Ordered from most explicit to least:
   1. Environment variable override (`TOOL_BIN_PATH=...`).
   2. Config file value (e.g. `.tool/config.yaml` → `assistants.codex.codexBinaryPath`).
   3. A user-writable vendor directory (`~/.tool/vendor/<pkg>/<binary-name>`).
4. **Validate each candidate with `existsSync`.** For env/config paths that are set but missing, **throw a clear error identifying which source was used** — users need to know whether to fix `TOOL_BIN_PATH` or `codexBinaryPath`.
5. **If all paths fail, throw an install-instructions error.** Print the three alternatives (install globally + set env, drop binary into vendor dir, set config path). Don't log-and-continue; the tool can't run.
6. **Platform guard:** filter `process.platform` and `process.arch` before computing the vendor filename. Unsupported combinations should skip step 3c cleanly.
7. **Wrap `existsSync`** in a trivial module-level wrapper (`function fileExists(p) { return _existsSync(p); }`) so tests can `spyOn` it — direct imports aren't spyable in Bun.

## Counter / Caveats

- Don't silently fall back to "guess a path" — that creates non-reproducible builds where the tool works for the developer and breaks for users.
- `process.execPath` in a compiled Bun binary points at the compiled binary itself, not at a Bun installation. Don't use it as an anchor for sibling lookups.
- If the binary is small enough (< 20 MB, all-platform), consider embedding it as a bytes blob via `Bun.embeddedFiles` instead of external lookup. The resolver pattern is for cases where embedding is impractical (platform-specific, license restricts embedding, or the binary is > 50 MB).
- Keep auth-variable names stable (`CODEX_BIN_PATH`) across versions — users script around them.

## Evidence

- `packages/providers/src/codex/binary-resolver.ts` (108 lines): full implementation of the env → config → vendor-dir chain, with `BUNDLED_IS_BINARY` early return for dev.
- Comment at `binary-resolver.ts:1-16`: rationale — "@openai/codex-sdk uses `createRequire(import.meta.url)` which breaks in compiled binaries where `import.meta.url` is frozen to the build host's path."
- `packages/paths/src/bundled-build.ts` (19 lines): the compile-time constant declaration, patched by the build script.
- Archon GitHub issue #979 (referenced in `bundled-build.ts:13`).
- Commit SHA: d89bc767d291f52687beea91c9fcf155459be0d9.
