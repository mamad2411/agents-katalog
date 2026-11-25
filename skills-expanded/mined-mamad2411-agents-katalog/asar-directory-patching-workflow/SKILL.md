---
name: asar-directory-patching-workflow
description: Extract an Electron .asar to a directory, surgically edit files, skip .asar.unpacked (it travels separately), and repack. Includes safe working directory management and staging conventions for multi-file edits.
category: electron-packaging
version: 1.0.0
tags: [electron, asar, patching, extract, repack, build, packaging]
source_type: extracted-from-git
source_url: https://github.com/aaddrick/claude-desktop-debian.git
source_ref: main
source_commit: 2fd9faf9db4eaa409b88310bdce397f8bdb0e916
source_project: claude-desktop-debian
imported_at: 2026-04-18T00:00:00Z
version_origin: extracted
confidence: high
---

# .asar Directory Patching Workflow

## When to use

Use this pattern when:
- You need to patch one or more files inside an Electron `.asar` archive.
- The patching involves multiple files or complex logic that is easier to apply to a directory than via streaming/in-place operations.
- You want a repeatable, auditable workflow: extract → edit files → repack.
- You need to add new files to the `.asar` (e.g., a wrapper script, a stub module).

## Pattern

```
app.asar                        (original, from upstream)
app.asar.unpacked/              (unpacked native modules — DO NOT touch)
app.asar.contents/              (extracted directory — edit here)
  .vite/build/index.js          (minified JS — patch in-place)
  package.json                  (update "main" field)
  frame-fix-wrapper.js          (new file — add here)
  node_modules/@vendor/native/  (stub module — add here)
app.asar                        (repacked output — overwrites original)
```

### Working directory convention

All patching work should happen in the staging directory. Use `cd "$staging_dir"` once and use relative paths for `asar` commands. This avoids long absolute paths in the asar commands and ensures consistent behavior.

### `.asar.unpacked` handling

The `.asar.unpacked/` directory contains files that were excluded from the archive (typically native `.node` modules). The `@electron/asar` tool tracks them via the archive header. When you extract with `asar extract` and then repack with `asar pack`, the tool automatically re-excludes them based on the header. **Do not copy `.asar.unpacked` into the extracted directory** — it will be double-packed.

## Minimal example

```bash
#!/usr/bin/env bash
# In the staging directory, assuming:
#   $staging_dir/app.asar         — original archive
#   $staging_dir/app.asar.unpacked/ — unpacked native modules
#   $asar_exec                    — path to asar binary

staging_dir="build/electron-app"
asar_exec="build/node_modules/.bin/asar"

cd "$staging_dir" || exit 1

# --- Stage 1: Extract ---
echo "Extracting app.asar..."
"$asar_exec" extract app.asar app.asar.contents
# app.asar.contents/ is now a directory with the archive contents
# app.asar.unpacked/ remains untouched alongside

# --- Stage 2: Add new files ---
echo "Adding wrapper and stub..."
cp /path/to/scripts/frame-fix-wrapper.js app.asar.contents/

# Add a stub native module
mkdir -p app.asar.contents/node_modules/@vendor/native
cp /path/to/scripts/native-stub.js app.asar.contents/node_modules/@vendor/native/index.js

# --- Stage 3: Edit package.json to inject wrapper as entry point ---
echo "Updating package.json..."
node -e "
const fs = require('fs');
const pkg = JSON.parse(fs.readFileSync('app.asar.contents/package.json', 'utf8'));
pkg.originalMain = pkg.main;
pkg.main = 'frame-fix-entry.js';
fs.writeFileSync('app.asar.contents/package.json', JSON.stringify(pkg, null, 2));
console.log('Updated main:', pkg.main, '(was:', pkg.originalMain + ')');
"

# Create the entry point file
original_main=$(node -e "console.log(require('./app.asar.contents/package.json').originalMain)")
cat > app.asar.contents/frame-fix-entry.js << ENTRY
require('./frame-fix-wrapper.js');
require('./${original_main}');
ENTRY

# --- Stage 4: Patch minified JS (in-place) ---
echo "Patching index.js..."
INDEX_JS="app.asar.contents/.vite/build/index.js"

# Extract variable names dynamically (see minified-js-variable-extraction-dynamic)
ELECTRON_VAR=$(grep -oP '\$?\w+(?=\s*=\s*require\("electron"\))' "$INDEX_JS" | head -1)
[[ -z $ELECTRON_VAR ]] && { echo "ERROR: electron var not found" >&2; exit 1; }

# Apply targeted patches
sed -i -E 's/(pattern)/\1replacement/g' "$INDEX_JS"

# --- Stage 5: Copy locale files and resources ---
echo "Copying resources..."
mkdir -p app.asar.contents/resources/i18n
cp /path/to/extracted/locale/*.json app.asar.contents/resources/i18n/

# --- Stage 6: Repack ---
echo "Repacking app.asar..."
"$asar_exec" pack app.asar.contents app.asar
# Note: asar pack reads the original header to determine which files
# were unpacked, and re-excludes them. app.asar.unpacked/ is untouched.

echo "Done. Patched app.asar is ready."
```

### Verification after repack

```bash
# Verify key files are present in the repacked archive
"$asar_exec" list app.asar | grep -q "frame-fix-wrapper.js" \
    && echo "frame-fix-wrapper.js: present" \
    || echo "WARNING: frame-fix-wrapper.js not in archive"

# Check that unpacked dir is still there and correct
[[ -d app.asar.unpacked ]] \
    && echo "app.asar.unpacked: present" \
    || echo "WARNING: app.asar.unpacked missing"
```

## Why this works

### `asar extract` produces a plain directory

The extracted directory is a regular filesystem tree. Any file editor, scripting tool, or `cp`/`mkdir` command can be used to modify it. This is far more ergonomic than modifying the binary archive directly.

### `asar pack` respects the original unpacked list

The `.asar` archive header contains a list of files that are "unpacked" (stored outside the archive). When `asar pack` reads the extracted directory to create a new archive, it checks which files were originally unpacked and re-marks them as unpacked. This preserves the `app.asar.unpacked/` symlink structure without you needing to manage it.

### `cd` to staging dir for shorter paths

The `asar` commands use relative paths (`app.asar`, `app.asar.contents`). If you invoke them from a different working directory, you need long absolute paths. A single `cd "$staging_dir"` at the start of the patching function keeps commands clean. Remember to `cd "$project_root"` when done.

### `node -e` for JSON manipulation

Minified/prettied JSON files with `sed` is error-prone (line-ending issues, escaping). Using `node -e` with `JSON.parse`/`JSON.stringify` is reliable and handles all edge cases in JSON encoding. Use `JSON.stringify(pkg, null, 2)` for readable output or `JSON.stringify(pkg)` for compact.

### Preserve `originalMain` in package.json

Storing the original `main` field as `originalMain` in `package.json` makes the injection auditable (you can inspect `app.asar.contents/package.json` to see both values) and provides a fallback if the wrapper needs to `require` the original entry point without hardcoding its path.

## Pitfalls

- **Do not run `asar pack` on `app.asar.unpacked/`** — this directory should remain untouched alongside `app.asar`. Accidentally packing it creates an invalid archive with double-nested unpacked files.
- **Pin `@electron/asar` version** — different `@electron/asar` versions have subtle differences in how they handle file ordering and compression. Pin to a known-working version in your `package.json` to avoid version drift breaking your build.
- **`asar extract` does not preserve file timestamps** — if your patch logic depends on file modification times (e.g., incremental builds), note that all extracted files get the current timestamp. Rebuild from scratch rather than patching incrementally.
- **Extracted `app.asar.contents/` must be cleaned between builds** — if you reuse the extraction directory across builds, stale files from a previous version may persist. Always `rm -rf app.asar.contents` before `asar extract`.
- **`asar list` for verification uses the new archive** — run `asar list app.asar` (not `asar list app.asar.contents`) to verify the repacked result. The repacked archive may differ from the extracted directory if any file was excluded by the packing configuration.

## Source reference

`build.sh` — `patch_app_asar()` function
