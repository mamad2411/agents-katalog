---
name: minified-js-variable-extraction-dynamic
description: Extract minified variable or function names from bundled JavaScript via regex capture groups anchored on stable string literals. Compose per-release sed patches using the extracted names. Handles $ prefixes from minifiers and optional whitespace in both minified and beautified forms.
category: electron-packaging
version: 1.0.0
tags: [minified-js, variable-extraction, regex, sed, electron, patching, build]
source_type: extracted-from-git
source_url: https://github.com/aaddrick/claude-desktop-debian.git
source_ref: main
source_commit: 2fd9faf9db4eaa409b88310bdce397f8bdb0e916
source_project: claude-desktop-debian
imported_at: 2026-04-18T00:00:00Z
version_origin: extracted
confidence: high
---

# Minified JS Variable Extraction (Dynamic)

## When to use

Use this pattern when:
- You need to apply a surgical patch to a minified JavaScript bundle.
- Variable and function names are randomized by the minifier and change between upstream releases.
- There are stable string literals in the code (event names, property names, constructor patterns) that remain unchanged across releases.
- You want patches that continue to work after the upstream app releases a new version without requiring manual name updates.

## Pattern

### Core technique

```bash
# grep -oP extracts the match of the capture group (after \K or in lookbehind/lookahead)
VARIABLE_NAME=$(grep -oP 'stable_literal\K\w+(?=other_stable_literal)' file.js)
```

### Rule: anchor on string literals, not identifiers

String literals in JavaScript source code (`"event-name"`, `"method-name"`, `require("module-name")`) are preserved verbatim by minifiers. Variable and function names adjacent to these literals can be captured by placing the capture group between two stable anchors.

### Escaping for sed

Variables extracted from minified code may start with `$` (e.g., `$e`, `$t`). Dollar signs must be escaped in sed patterns: `${VAR//\$/\\$}`.

## Minimal example

```bash
#!/usr/bin/env bash
JS_FILE="app.asar.contents/.vite/build/index.js"

# 1. Extract the variable that holds the electron module
#    Stable anchor: the literal string require("electron")
#    The variable assignment: `VAR = require("electron")` or `$VAR = require("electron")`
ELECTRON_VAR=$(grep -oP '\$?\w+(?=\s*=\s*require\("electron"\))' "$JS_FILE" | head -1)
[[ -z $ELECTRON_VAR ]] && { echo "ERROR: electron var not found" >&2; exit 1; }
ELECTRON_VAR_RE="${ELECTRON_VAR//\$/\\$}"   # escape $ for sed
echo "Electron var: $ELECTRON_VAR"

# 2. Extract a function name anchored on a unique event string it registers
#    Pattern: on("menuBarEnabled",()=>{ FUNC_NAME() })
#    The function is called inside the event handler
TRAY_FUNC=$(grep -oP 'on\("menuBarEnabled",\(\)=>\{\K\w+(?=\(\)\})' "$JS_FILE")
[[ -z $TRAY_FUNC ]] && { echo "ERROR: tray func not found" >&2; exit 1; }
echo "Tray func: $TRAY_FUNC"

# 3. Extract a variable name using a structural pattern
#    Pattern: });let TRAY_VAR=null;(async|)function TRAY_FUNC(
TRAY_VAR=$(grep -oP "\}\);let \K\w+(?==null;(?:async )?function ${TRAY_FUNC})" "$JS_FILE")
[[ -z $TRAY_VAR ]] && { echo "ERROR: tray var not found" >&2; exit 1; }
echo "Tray var: $TRAY_VAR"

# 4. Extract by unique method call: setAlwaysOnTop(!0,"pop-up-menu")
POPUP_VAR=$(grep -oP '\w+(?=\.setAlwaysOnTop\(\s*!0\s*,\s*"pop-up-menu"\))' "$JS_FILE" | head -1)
[[ -z $POPUP_VAR ]] && echo "WARNING: popup var not found (non-fatal)"
echo "Popup var: ${POPUP_VAR:-<not found>}"

# 5. Extract via const assignment to a known function call
#    Pattern: const MENU_BAR_VAR = someFunc("menuBarEnabled")
MENU_BAR_VAR=$(grep -oP 'const \K\w+(?=\s*=\s*\w+\("menuBarEnabled"\))' "$JS_FILE" | head -1)
[[ -n $MENU_BAR_VAR ]] && echo "Menu bar var: $MENU_BAR_VAR"

# 6. Now apply patches using the extracted names
#    Make the tray function async
sed -i "s/function ${TRAY_FUNC}(){/async function ${TRAY_FUNC}(){/g" "$JS_FILE"

#    Fix all wrong nativeTheme references
WRONG_REFS=$(grep -oP '\$?\w+(?=\.nativeTheme)' "$JS_FILE" | sort -u \
    | grep -Fxv "$ELECTRON_VAR" || true)
for REF in $WRONG_REFS; do
    REF_RE="${REF//\$/\\$}"
    sed -i -E "s/${REF_RE}\.nativeTheme/${ELECTRON_VAR_RE}.nativeTheme/g" "$JS_FILE"
done

#    Patch tray icon selection to respect dark mode
if grep -qP ':\$?\w+="TrayIconTemplate\.png"' "$JS_FILE"; then
    DARK_CHECK="${ELECTRON_VAR_RE}.nativeTheme.shouldUseDarkColors"
    sed -i -E \
        "s/:(\\\$?\w+)=\"TrayIconTemplate\.png\"/:\1=${DARK_CHECK}?\"TrayIconTemplate-Dark.png\":\"TrayIconTemplate.png\"/g" \
        "$JS_FILE"
fi

#    Patch menuBarEnabled default (!! → !==false)
if [[ -n $MENU_BAR_VAR ]] && grep -qP ",\s*!!${MENU_BAR_VAR}\s*\)" "$JS_FILE"; then
    sed -i -E "s/,\s*!!${MENU_BAR_VAR}\s*\)/,${MENU_BAR_VAR}!==false)/g" "$JS_FILE"
fi
```

### Validation before apply

```bash
# Fail loudly if extraction returns empty — better than silent no-op patch
require_var() {
    local name="$1" value="$2"
    if [[ -z $value ]]; then
        echo "ERROR: could not extract required variable: $name" >&2
        echo "  The upstream app may have restructured this code." >&2
        echo "  Inspect: $JS_FILE" >&2
        exit 1
    fi
}
require_var "ELECTRON_VAR" "$ELECTRON_VAR"
require_var "TRAY_FUNC" "$TRAY_FUNC"
```

## Why this works

### String literals survive minification

JavaScript minifiers rename variables and functions to short identifiers (`a`, `b`, `$e`) to reduce file size. However, they cannot rename string literals used as event names, JSON keys, method call arguments, or module identifiers — changing these would break the program's logic. Patterns like `require("electron")`, `on("menuBarEnabled", ...)`, `"pop-up-menu"`, and `"TrayIconTemplate.png"` are stable across all minification passes.

### `grep -oP` with `\K` and lookahead

`-o` outputs only the matched portion. `-P` enables Perl-compatible regex. `\K` is a zero-width assertion that "keeps" (resets) the match start, effectively acting as a lookbehind without the length constraint. `(?=...)` is a zero-width lookahead. Together, `prefix\K\w+(?=suffix)` extracts the identifier between `prefix` and `suffix` without including either in the output.

### `| head -1` for uniqueness

If the same pattern appears multiple times (e.g., `require("electron")` in multiple modules), `grep -oP ... | head -1` takes the first match. For well-structured single-file bundles, the first match is typically the module-level assignment. Add additional context to the pattern if disambiguation is needed.

### `${VAR//\$/\\$}` — escaping $ for sed

Some minifiers use `$` as a prefix for variable names (e.g., `$e = require("electron")`). Dollar signs have special meaning in sed replacement strings and in regex patterns. `${VAR//\$/\\$}` is a bash parameter expansion that replaces all `$` with `\$` in `$VAR`, producing a sed-safe regex.

### Verify after apply

After applying a patch, verify it took effect:
```bash
if grep -qP ',\s*!!${MENU_BAR_VAR}\s*\)' "$JS_FILE"; then
    echo "ERROR: patch did not apply — pattern still present" >&2; exit 1
fi
```

## Pitfalls

- **`-P` (Perl regex) is GNU grep** — not available on BSD grep (macOS). Use `ggrep` or install `grep` via Homebrew when developing on macOS. In Linux build environments, GNU grep is always present.
- **mapfile vs. array from grep** — use `mapfile -t array < <(grep ...)` to capture multiple matches into an array rather than iterating `$()` output in a for loop (word-splitting issues with filenames containing spaces).
- **Pattern collision on `head -1`** — if two different variables match the same extraction pattern (e.g., two `require("electron")` at different scopes in a bundled file), `head -1` may return the wrong one. Add more context to the pattern or use a numbered occurrence.
- **Whitespace in minified code** — minified code has no spaces around operators. But some build pipelines partially format the output. Always use `\s*` around `=`, `,`, `=>`, `{`, `}` in patterns that may encounter either form.
- **Non-fatal extractions should not block the build** — for variables that are optional (a feature may not be present in all app versions), use a warning instead of `exit 1`. Gate the corresponding patch on `[[ -n $OPTIONAL_VAR ]]`.

## Source reference

`build.sh` — `extract_electron_variable`, `patch_tray_menu_handler`, `patch_tray_icon_selection`, `patch_menu_bar_default` functions; `CLAUDE.md` — "Working with Minified JavaScript" section
