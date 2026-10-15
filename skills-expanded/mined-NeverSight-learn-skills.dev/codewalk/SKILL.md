---
name: codewalk
description: "Install, use, and manage CodeWalk — a macOS app + CLI for interactive visual code walkthroughs. Use this skill whenever the user mentions CodeWalk, codewalk, code walkthrough, visual code explanation, code presentation, code tour, or wants to visually walk through code with animations and highlights. Also trigger when the user says things like '코드를 가르쳐줘', '코드 설명을 눈으로 보여줘', 'UI로 보여줘', 'show me the code visually', 'teach me this code', 'walk me through', or any request to explain code in a visual/interactive way rather than plain text. Also use when the user wants to install, uninstall, update, or troubleshoot CodeWalk, or when they want to create walkthrough JSON files for code explanation."
context: fork
---

# CodeWalk

CodeWalk is a macOS native app paired with a CLI. The GUI displays code with interactive walkthrough animations (highlights, annotations, scrolling, file switching). The CLI (`codewalk`) controls the app over a local Unix socket, making it ideal for LLM-driven code explanations.

## Installation

CodeWalk requires **macOS 13+** (Ventura or newer) and **python3**.

### Option A: One-line installer (recommended)

```bash
curl -fsSL https://raw.githubusercontent.com/ai-hand/codewalk-dist/main/install.sh | sh
```

This downloads the latest release, installs `CodeWalk.app` into `/Applications` (or `~/Applications` if `/Applications` is not writable), and symlinks the `codewalk` CLI into your PATH.

The installer chooses the CLI symlink location in this priority order:
1. `/opt/homebrew/bin/codewalk` (Apple Silicon default)
2. `/usr/local/bin/codewalk` (Intel Mac default)
3. `~/.local/bin/codewalk` (fallback)

You can override locations with environment variables:

```bash
CODEWALK_APP_ROOT=~/MyApps CODEWALK_CLI_LINK=~/bin/codewalk \
  curl -fsSL https://raw.githubusercontent.com/ai-hand/codewalk-dist/main/install.sh | sh
```

### Option B: Homebrew

```bash
brew tap ai-hand/codewalk
brew install --cask codewalk
```

### Verify installation

After installing, confirm it works:

```bash
codewalk          # Should print usage/help text
codewalk open .   # Opens a session for the current directory (launches the app if needed)
codewalk list     # Should show the open session as JSON
```

If `codewalk` is not found, ensure the symlink directory is in your `$PATH`. For `~/.local/bin`:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

## Uninstallation

### If installed via Homebrew

```bash
brew uninstall --cask codewalk
```

This also removes `~/.codewalk` state data via the cask's zap directive.

### If installed via curl installer or manually

Run these three steps:

```bash
# 1. Remove the app
rm -rf /Applications/CodeWalk.app    # or ~/Applications/CodeWalk.app

# 2. Remove the CLI symlink
rm -f /opt/homebrew/bin/codewalk     # or /usr/local/bin/codewalk or ~/.local/bin/codewalk

# 3. Remove state data
rm -rf ~/.codewalk
```

To find the exact symlink location: `which codewalk`

## CLI Commands

All commands communicate with the running GUI app via a Unix domain socket at `~/.codewalk/codewalk.sock`. If the app is not running, `codewalk open` will launch it automatically.

All responses are JSON with pretty-printed output and sorted keys.

### open — Start or reuse a project session

```bash
codewalk open /absolute/path/to/project
```

Returns:
```json
{
  "session_id": "cw_abc12345",
  "project_path": "/absolute/path/to/project",
  "reused": false
}
```

The path must be absolute. If a session already exists for that path, it is reused (`"reused": true`).

### list — Show all open sessions

```bash
codewalk list
```

### status — Get session state

```bash
codewalk status --session <SESSION_ID>
```

If only one session exists, `--session` can be omitted.

### read — Read code from a session's project

```bash
codewalk read --session <SESSION_ID> --path relative/file.py
codewalk read --session <SESSION_ID> --path relative/file.py --lines 10-40
```

`--path` is relative to the project root. `--lines` selects a range (inclusive).

### run — Execute a walkthrough

From a file:
```bash
codewalk run --session <SESSION_ID> walkthrough.json
```

From stdin:
```bash
cat walkthrough.json | codewalk run --session <SESSION_ID> --stdin
```

Or inline:
```bash
printf '%s' '{"version":2,"title":"Demo","steps":[]}' | codewalk run --session <SESSION_ID> --stdin
```

### reset — Reset a session to initial state

```bash
codewalk reset --session <SESSION_ID>
```

### close — Close sessions

```bash
codewalk close --session <SESSION_ID>   # Close one session
codewalk close --all                     # Close all sessions
```

### quit — Exit the app entirely

```bash
codewalk quit
```

## Session Rules

- Sessions are identified by IDs in the format `cw_` + 8-char hex (e.g., `cw_abc12345`).
- `codewalk open <path>` creates a new session or reuses an existing one for the same path.
- When only one session exists, `--session` is optional for all commands.
- When multiple sessions exist, `--session <SESSION_ID>` is required.
- `close` ends a specific session. `quit` exits the entire app.

## Creating Walkthroughs

Walkthroughs are JSON files (version 2) that describe a sequence of steps. Each step has a `message` (the narration text) and `actions` (visual effects applied to the code viewer).

### Walkthrough JSON structure

```json
{
  "version": 2,
  "title": "Walkthrough title",
  "character": {
    "name": "Claude",
    "avatar": "default",
    "style": "friendly"
  },
  "theme": "rpg-classic",
  "settings": {
    "scroll_duration_ms": 500,
    "highlight_fade_in_ms": 220,
    "typing_speed": "normal",
    "auto_clear": true,
    "scroll_position": "top-third"
  },
  "steps": [
    {
      "message": "Let me show you how this works.",
      "actions": [
        { "type": "switch_file", "file": "src/main.py", "transition": "auto" },
        { "type": "scroll_to", "line": 12, "position": "top-third" },
        { "type": "highlight", "lines": [12, 24], "color": "info" },
        { "type": "annotate", "line": 15, "placement": "below", "color": "info", "text": "Entry point" }
      ]
    }
  ]
}
```

Only `version`, `title`, and `steps` are required. `character`, `theme`, and `settings` are optional.

### Action types

| Action | Required fields | Optional fields | Purpose |
|--------|----------------|-----------------|---------|
| `switch_file` | `file` | `transition` | Switch the displayed file |
| `scroll_to` | `line` | `position` | Jump to a line number |
| `highlight` | `lines` (array) | `color` | Highlight specific lines |
| `highlight_token` | `line`, `start_col`, `end_col` | `color` | Highlight a specific token within a line |
| `dim` | `lines` (array) | `except` | Dim lines (de-emphasize) |
| `fold` | `lines` (array) | `title` | Collapse code sections |
| `underline` | `lines` (array) | `color`, `style` | Underline specific lines |
| `annotate` | `line`, `text` | `placement`, `color` | Add a text annotation near a line |
| `clear` | — | — | Remove all visual effects |

**Colors**: `"info"`, `"warning"`, `"error"`, or theme-defined values.
**Placements** (annotate): `"above"`, `"below"`, `"inline"`.
**Positions** (scroll_to): `"top"`, `"center"`, `"top-third"`.
**Transitions** (switch_file): `"auto"`, `"instant"`.

### Best practices for walkthroughs

- Aim for 4-8 steps for a focused explanation. Fewer for simple topics, more for complex ones.
- Use `switch_file` only when switching to a different file — avoid unnecessary file switches.
- Within the same file, use `scroll_to` + `highlight` + `annotate` to guide the reader.
- Keep `message` text conversational and concise. The visual actions carry most of the explanation.
- Use `clear` between conceptually distinct sections to avoid visual clutter.
- Use `dim` to de-emphasize boilerplate when focusing on the important parts.

## Recommended workflow for LLMs

When a user asks you to explain code visually with CodeWalk:

1. **Open the project**: `codewalk open /absolute/path`
2. **Read the relevant files**: `codewalk read --session <ID> --path file.py` to understand the code
3. **Generate a walkthrough JSON** following the structure above
4. **Run it**: pipe the JSON to `codewalk run --session <ID> --stdin` or save to a file first
5. **Follow up**: use `status` and `read` for any further questions

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `codewalk: command not found` | Check `which codewalk`. Ensure symlink dir is in `$PATH`. Re-run installer if needed. |
| `codewalk open` fails | Make sure the path is absolute. Check if the app is installed: `ls /Applications/CodeWalk.app` |
| Socket connection refused | The app may not be running. Run `open /Applications/CodeWalk.app` then retry. |
| Multiple sessions error | Pass `--session <SESSION_ID>` explicitly. Use `codewalk list` to see active sessions. |
| Walkthrough fails to load | Validate the JSON. Ensure `version` is `2` and action `type` values are valid. |
| Gatekeeper blocks the app | Run `xattr -cr /Applications/CodeWalk.app` to clear quarantine attributes. |

## Updating

### Curl installer

Just re-run the install command — it replaces the existing installation:

```bash
curl -fsSL https://raw.githubusercontent.com/ai-hand/codewalk-dist/main/install.sh | sh
```

### Homebrew

```bash
brew upgrade --cask codewalk
```

## State and data locations

| Path | Purpose |
|------|---------|
| `/Applications/CodeWalk.app` | The app bundle (GUI + CLI binary) |
| `~/.codewalk/` | All runtime state |
| `~/.codewalk/codewalk.sock` | Unix domain socket for CLI-app communication |
| `~/.codewalk/sessions.json` | Persisted session metadata |
| `~/.codewalk/walkthroughs/<SESSION_ID>.json` | Loaded walkthrough data per session |
