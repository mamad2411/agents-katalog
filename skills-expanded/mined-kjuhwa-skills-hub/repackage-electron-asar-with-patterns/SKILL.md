---
name: repackage-electron-asar-with-patterns
description: Extract an Electron .asar archive, apply regex-based patches to minified JS that survive minifier renames by anchoring on stable string literals, then repack. Includes dynamic variable extraction so patches remain version-agnostic.
category: electron-packaging
version: 1.0.0
tags: [electron, asar, patching, regex, minified-js, build]
source_type: extracted-from-git
source_url: https://github.com/aaddrick/claude-desktop-debian.git
source_ref: main
source_commit: 2fd9faf9db4eaa409b88310bdce397f8bdb0e916
source_project: claude-desktop-debian
imported_at: 2026-04-18T00:00:00Z
version_origin: extracted
confidence: high
---

# Repackage Electron .asar with Regex Patch Patterns

## When to use

Use this pattern when:
- You are repackaging a third-party Electron app (no source access) for a new platform or environment.
- The bundled JS is minified and variable names change between upstream releases.
- You need to surgically modify specific behaviors (tray icon logic, window frame, feature flags) without full source access.
- You want patches that survive upstream version bumps without manual variable-name updates.

## Pattern

The workflow has five stages:

1. **Extract** — unpack the `.asar` to a directory.
2. **Dynamic extraction** — grep the extracted JS with a capture-group regex anchored on a stable string literal to find the current minified variable or function name.
3. **Patch** — apply `sed -E` replacements using the dynamically extracted name.
4. **Handle optional whitespace** — use `\s*` around operators so the same regex works on both minified (`a,b=>`) and beautified (`a, b =>`) code.
5. **Repack** — reassemble the `.asar` from the patched directory, skipping the `.asar.unpacked` sibling.

### Key rules

- **Never hardcode minified names** — always extract them from a known stable anchor (a string literal, a unique method call, or a structural pattern that the minifier cannot rename).
- Use `grep -oP` (Perl-regex) with `\K` and lookahead/lookbehind to extract names without capturing surrounding syntax.
- Use `sed -i -E` for the actual replacement so you can use grouping and alternation.
- Validate extraction: if `grep` returns empty, fail loudly rather than silently applying a no-op patch.

## Minimal example

```bash
#!/usr/bin/env bash
# Stage directories
STAGING="build/electron-app"
ASAR="$STAGING/app.asar"
CONTENTS="$STAGING/app.asar.contents"
INDEX_JS="$CONTENTS/.vite/build/index.js"

# 1. Extract
asar extract "$ASAR" "$CONTENTS"

# 2. Dynamic extraction — find the electron module variable by looking at
#    the require("electron") assignment.
ELECTRON_VAR=$(grep -oP '\$?\w+(?=\s*=\s*require\("electron"\))' \
    "$INDEX_JS" | head -1)
[[ -z $ELECTRON_VAR ]] && { echo "ERROR: could not find electron var" >&2; exit 1; }
ELECTRON_VAR_RE="${ELECTRON_VAR//\$/\\$}"   # escape $ for sed

# 3. Dynamic extraction — find tray function by anchoring on a stable
#    string literal it calls.
TRAY_FUNC=$(grep -oP 'on\("menuBarEnabled",\(\)=>\{\K\w+(?=\(\)\})' \
    "$INDEX_JS")
[[ -z $TRAY_FUNC ]] && { echo "ERROR: could not find tray func" >&2; exit 1; }

# 4. Patch: make the tray handler async (stable structural change)
sed -i "s/function ${TRAY_FUNC}(){/async function ${TRAY_FUNC}(){/g" "$INDEX_JS"

# 5. Patch: fix nativeTheme references on wrong variable (handle whitespace)
#    Replace wrongVar.nativeTheme with electronVar.nativeTheme
WRONG_REFS=$(grep -oP '\$?\w+(?=\.nativeTheme)' "$INDEX_JS" | sort -u \
    | grep -Fxv "$ELECTRON_VAR" || true)
for REF in $WRONG_REFS; do
    REF_RE="${REF//\$/\\$}"
    sed -i -E "s/${REF_RE}\.nativeTheme/${ELECTRON_VAR_RE}.nativeTheme/g" "$INDEX_JS"
done

# 6. Patch: handle optional whitespace in nativeTheme.on("updated") call
sed -i -E \
    's/('"${ELECTRON_VAR_RE}"'\.nativeTheme\.on\(\s*"updated"\s*,\s*\(\)\s*=>\s*\{)/let _startTime=Date.now();\1/g' \
    "$INDEX_JS"

# 7. Repack (asar skips .asar.unpacked automatically)
asar pack "$CONTENTS" "$ASAR"
```

## Why this works

### Minifier stability of string literals

Minifiers rename variables and functions aggressively, but they cannot rename string literals embedded in the source (event names, JSON keys, require paths). Patterns like `require("electron")`, `on("menuBarEnabled", ...)`, and `setAlwaysOnTop(!0, "pop-up-menu")` are stable across releases because they appear verbatim in the application's logic.

### Capture-group extraction vs brittle hardcoding

Using `grep -oP '\$?\w+(?=\.nativeTheme)'` extracts the actual current variable name at patch time. The `\K` anchor and lookahead/lookbehind mean you never capture the delimiter — you get only the identifier you need. Storing it in a shell variable and escaping `$` for sed (`${VAR//\$/\\$}`) lets you build version-agnostic sed commands.

### Optional-whitespace guards

Minified code writes `a.b.on("c",()=>{` while beautified reference copies write `a.b.on("c", () => {`. Using `\s*` between tokens in the sed pattern means the same pattern handles both forms, which is critical because some build tools or intermediate processing steps may partially format the output.

### Validation before apply

Extracting the variable name and then checking for empty string before applying the patch converts a silent "wrong patch applied" failure into an immediate loud failure. This is far cheaper to debug in CI than a silently wrong binary.

## Pitfalls

- **Do not run `asar pack` on the `.asar.unpacked` directory** — `@electron/asar` automatically excludes files listed in the `.asar` header as "unpacked". Packing the unpacked directory separately overwrites the header.
- **`sed -i` on macOS requires an argument** — use `sed -i ''` on macOS or prefer GNU sed via `gsed`.
- **Extended regex (`-E`) is needed for grouping** — POSIX BRE does not support `(a|b)` without escaping. Always use `-E`.
- **grep with `-P` (Perl regex) is GNU-specific** — not available on BSD/macOS `grep`. Use `ggrep` or install gnu-grep if building cross-platform.
- **Race condition if asar binary is not installed** — pin the `@electron/asar` package version to avoid npm-installing a breaking version. Use `--no-save` and pin to a known-good version in CI.
- **Empty extraction result on upstream refactor** — if the upstream app restructures the code, your anchor pattern may stop matching. Add a second candidate pattern (fallback) or fail with a clear error message pointing to the specific pattern.

## Source reference

`build.sh` — functions `extract_electron_variable`, `fix_native_theme_references`, `patch_tray_menu_handler`, `patch_asar_workflow`
