---
name: swiftbar
description: Create, edit, and debug SwiftBar menu bar plugins for macOS. ALWAYS use this skill when the user wants to put anything in the macOS menu bar — whether they say "menu bar plugin", "status bar widget", "menu bar item", or just want to show live data, counters, status indicators, or monitoring info in the macOS top bar. Also triggers for SwiftBar, BitBar, xbar by name, editing or debugging existing menu bar plugin scripts (.sh/.py with | parameters and --- separators), or any request to build a script that outputs formatted lines for a menu bar app. This is the go-to skill whenever macOS menu bar customization is involved, even if the user doesn't mention SwiftBar specifically — if they want a script-based menu bar item on macOS, this skill applies.
---

# SwiftBar Plugin Development

Build and maintain SwiftBar menu bar plugins for macOS. SwiftBar executes scripts in a designated Plugin Folder and parses their stdout into menu bar items and dropdown menus.

**Languages:** Bash for simple plugins, Python for anything involving APIs, JSON parsing, or complex logic. Choose based on complexity — don't use Python when 10 lines of bash would do.

## Plugin Folder

Ask the user where their SwiftBar Plugin Folder is located if you don't know. Common locations:
- `~/SwiftBar/` or `~/swiftbar/`
- `~/Library/SwiftBar/`
- Custom path set in SwiftBar preferences

Once known, install plugins directly there so the user sees results immediately.

## File Naming

```
{name}.{interval}.{ext}
```

- **name**: kebab-case identifier (e.g., `cpu-usage`, `weather`, `git-status`)
- **interval**: refresh rate — `500ms`, `1s`, `5m`, `2h`, `1d` (omit for manual-only refresh)
- **ext**: `sh` for bash, `py` for Python

Examples: `weather.10m.sh`, `cpu.2s.py`, `pomodoro.1s.sh`

## Output Protocol

Every SwiftBar plugin is a script that prints to stdout. The output follows a line-based protocol:

```
Header Line          ← Shown in menu bar
---                  ← Separator: everything below is dropdown-only
Dropdown Item 1
Dropdown Item 2
---                  ← Visual divider in dropdown
Another Item
```

**Rules:**
- Lines before the first `---` are **header lines** (displayed in the menu bar, cycled if multiple)
- Lines after the first `---` appear in the **dropdown menu**
- Additional `---` lines create visual dividers in the dropdown
- Empty output hides the plugin from the menu bar (useful for conditional display)
- Exit code 0 = normal, exit code 1 = SwiftBar shows a warning icon

### Parameters

Append parameters after a pipe `|`:

```
Item text | param1=value1 param2=value2
```

#### Text & Appearance

| Parameter | Example | Effect |
|-----------|---------|--------|
| `color` | `color=red` or `color=#ff0000` | Text color (name or hex) |
| `color` | `color=black,white` | Text color for light,dark mode |
| `font` | `font=Menlo` | macOS font name |
| `size` | `size=14` | Font size in points |
| `length` | `length=20` | Truncate text (full in tooltip) |
| `trim` | `trim=true` | Strip whitespace |
| `md` | `md=true` | Enable markdown (**bold**, *italic*) |
| `tooltip` | `tooltip=Hover text` | Tooltip on hover |

#### Icons & Images

| Parameter | Example | Effect |
|-----------|---------|--------|
| `sfimage` | `sfimage=checkmark.circle` | SF Symbol (macOS Big Sur+) |
| `sfcolor` | `sfcolor=green` | SF Symbol color |
| `image` | `image=<base64>` | Custom image |
| `templateImage` | `templateImage=<base64>` | Adaptive image (dark/light) |

#### Actions

| Parameter | Example | Effect |
|-----------|---------|--------|
| `href` | `href=https://example.com` | Open URL on click |
| `bash` | `bash=/path/to/script.sh` | Run script on click |
| `terminal` | `terminal=false` | Run bash silently (no Terminal) |
| `param0`..`paramN` | `param0=-l param1=/tmp` | Arguments for bash |
| `refresh` | `refresh=true` | Re-run plugin after click |
| `shortcut` | `shortcut=CMD+OPTION+T` | Keyboard shortcut |

#### Menu Structure

| Parameter | Example | Effect |
|-----------|---------|--------|
| `checked` | `checked=true` | Show checkmark |
| `badge` | `badge=3` | Right-aligned badge |
| `alternate` | `alternate=true` | Show when Option key held |
| `dropdown` | `dropdown=false` | Header-only (not in dropdown) |

### Submenus

Prefix lines with `--` for each nesting level:

```bash
echo "Top item"
echo "--Sub-item 1"
echo "--Sub-item 2"
echo "----Nested sub-item"
```

## Metadata

Add metadata as comments at the top of the script (after the shebang):

```bash
#!/bin/bash

# <xbar.title>Plugin Name</xbar.title>
# <xbar.version>v1.0</xbar.version>
# <xbar.author>Author Name</xbar.author>
# <xbar.author.github>github-username</xbar.author.github>
# <xbar.desc>What this plugin does</xbar.desc>
# <xbar.dependencies>jq,curl</xbar.dependencies>
```

### SwiftBar-Specific Metadata

```bash
# <swiftbar.hideAbout>true</swiftbar.hideAbout>
# <swiftbar.hideRunInTerminal>true</swiftbar.hideRunInTerminal>
# <swiftbar.hideLastUpdated>true</swiftbar.hideLastUpdated>
# <swiftbar.hideDisablePlugin>true</swiftbar.hideDisablePlugin>
# <swiftbar.hideSwiftBar>true</swiftbar.hideSwiftBar>
# <swiftbar.refreshOnOpen>true</swiftbar.refreshOnOpen>
# <swiftbar.runInBash>false</swiftbar.runInBash>
# <swiftbar.type>streamable</swiftbar.type>
# <swiftbar.environment>[API_KEY=, CITY=London]</swiftbar.environment>
# <swiftbar.schedule>0,30 * * * *</swiftbar.schedule>
```

Use `swiftbar.environment` for user-configurable values (users set them via SwiftBar's UI). Use `swiftbar.hideAbout` / `swiftbar.hideLastUpdated` etc. to clean up the dropdown.

## Environment Variables

SwiftBar injects these into every plugin:

| Variable | Purpose |
|----------|---------|
| `OS_APPEARANCE` | `Light` or `Dark` — use for adaptive styling |
| `SWIFTBAR_PLUGIN_CACHE_PATH` | Per-plugin cache dir (temp data) |
| `SWIFTBAR_PLUGIN_DATA_PATH` | Per-plugin data dir (persistent state) |
| `SWIFTBAR_PLUGINS_PATH` | Path to the plugin folder |
| `SWIFTBAR_PLUGIN_PATH` | Path to the current plugin script |

## Common Patterns

See `references/patterns.md` for detailed examples of:
- Dark/light mode handling
- Self-refreshing actions
- Error handling
- Persistent state with data/cache dirs
- Streamable (live-updating) plugins
- Option-key alternate items
- Triggering refresh from external scripts

## Plugin Types

### Standard (default)
Single execution, finite runtime. Refreshes on the interval in the filename.

### Streamable
Long-running process. Use `~~~` to signal a menu update:

```bash
# <swiftbar.type>streamable</swiftbar.type>
while true; do
    echo "Status: $(date +%H:%M)"
    echo "---"
    echo "Running..."
    echo "~~~"
    sleep 5
done
```

### Ephemeral
Temporary items via URL scheme — for notifications or transient alerts:
```bash
open -g "swiftbar://setephemeralplugin?name=alert&content=Build+Done&exitafter=10"
```

## Writing a Plugin — Checklist

1. **Shebang line** — `#!/bin/bash` or `#!/usr/bin/env python3`
2. **Metadata block** — at minimum `xbar.title`, `xbar.desc`, `xbar.author`
3. **Header output** — concise text (with optional SF Symbol) for the menu bar
4. **Dropdown content** — details, actions, sub-items after `---`
5. **Error handling** — catch failures and show friendly error in menu bar (exit 0, not 1)
6. **Make executable** — `chmod +x` the file
7. **Test** — run the script directly in terminal to check output before SwiftBar picks it up

## Debugging Existing Plugins

When a plugin isn't working:

1. **Run directly** — execute the script in terminal and inspect stdout
2. **Check shebang** — must be valid (`#!/bin/bash`, `#!/usr/bin/env python3`)
3. **Check permissions** — must be executable (`chmod +x`)
4. **Check output format** — each line must follow the protocol (text before `|`, params after)
5. **Check exit code** — exit 1 triggers SwiftBar's warning icon
6. **Check dependencies** — verify tools like `jq`, `curl`, `python3` are installed
7. **Check stderr** — SwiftBar ignores stderr, but it helps diagnose issues
8. **Refresh interval** — very fast intervals (< 1s) can cause issues

## URL Scheme

Useful for inter-plugin communication and automation:

| URL | Action |
|-----|--------|
| `swiftbar://refreshplugin?name=<name>` | Refresh specific plugin |
| `swiftbar://refreshallplugins` | Refresh all plugins |
| `swiftbar://notify?plugin=<name>&title=<t>&body=<b>` | Show notification |
| `swiftbar://enableplugin?name=<name>` | Enable plugin |
| `swiftbar://disableplugin?name=<name>` | Disable plugin |

Use `open -g` to prevent SwiftBar from stealing focus.
