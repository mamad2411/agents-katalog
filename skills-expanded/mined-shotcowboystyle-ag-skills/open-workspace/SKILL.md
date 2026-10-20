---
name: open-workspace
description: Open the user's registered image workspace folder. Use when the user says "open my image workspace", "take me to my image workspace", or similar. Reads the path from workspace.json and opens a terminal (or Finder/file manager) there.
allowed-tools: Bash(test *), Bash(ls *), Bash(echo *), Bash(uname *), Bash(jq *), Bash(sed *), Bash(open *), Bash(konsole *), Bash(gnome-terminal *), Bash(xdg-open *), Bash(command *), Read
---

# Open Image Workspace

```bash
CONFIG="${CLAUDE_USER_DATA:-${XDG_DATA_HOME:-$HOME/.local/share}/claude-plugins}/image-ops/workspace.json"
test -f "$CONFIG" || { echo "No image workspace registered. Run workspace-setup first."; exit 1; }

# jq is the happy path. The fallback must be portable: `grep -oP` is GNU-only and
# errors out on the BSD grep that ships with macOS, which is exactly the case the
# fallback exists to cover.
WS=$(jq -r .path "$CONFIG" 2>/dev/null) \
  || WS=$(sed -n 's/.*"path"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' "$CONFIG")
test -d "$WS" || { echo "Workspace path missing: $WS"; exit 1; }

case "$(uname -s)" in
  Darwin)
    open -a Terminal "$WS" || open "$WS"
    ;;
  *)
    if command -v konsole >/dev/null; then
      konsole --workdir "$WS" &
    elif command -v gnome-terminal >/dev/null; then
      gnome-terminal --working-directory="$WS" &
    elif command -v xdg-open >/dev/null; then
      xdg-open "$WS" &
    else
      echo "No terminal opener found — printing the path only." >&2
    fi
    ;;
esac

echo "Workspace: $WS"
ls -la "$WS"
```

`konsole` / `gnome-terminal` / `xdg-open` are Linux-only and none exist on macOS, so without the `Darwin` branch the script silently falls through and opens nothing. Always print the path regardless of whether an opener was found — that is the part the user can still act on.

If config is missing or stale, redirect to `workspace-setup`.
