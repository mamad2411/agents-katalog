---
name: termsvg
description: "Record, replay, and export terminal sessions as animated SVG images using termsvg. Use this skill whenever the user wants to record a terminal session, replay an asciicast recording, or export a .cast file to an animated SVG. Trigger when the user mentions termsvg, terminal recording to SVG, animated terminal SVG, asciicast export, or wants to create animated terminal demos for documentation, READMEs, or presentations. Also trigger when the user has .cast files (asciinema format) they want to convert to SVG."
---

# termsvg — Record, Replay & Export Terminal Sessions as SVG

Record terminal sessions, replay them, and export to animated SVG with [termsvg](https://github.com/MrMarble/termsvg). Uses the asciicast format (compatible with asciinema `.cast` files).

## Installation

```bash
# Go install
go install github.com/mrmarble/termsvg/cmd/termsvg@latest

# Install script
curl -sL https://raw.githubusercontent.com/MrMarble/termsvg/master/scripts/install-termsvg.sh | sudo -E bash -
```

Pre-compiled binaries are available on the [releases page](https://github.com/mrmarble/termsvg/releases).

## Quick Reference

| Task | Command |
|------|---------|
| Record a session | `termsvg rec session.cast` |
| Record a specific command | `termsvg rec -c "ls -la" session.cast` |
| Skip first line of recording | `termsvg rec -s session.cast` |
| Replay a recording | `termsvg play session.cast` |
| Replay at 2x speed | `termsvg play -s 2 session.cast` |
| Replay with idle cap | `termsvg play -i 2 session.cast` |
| Export to SVG | `termsvg export session.cast` |
| Export to specific file | `termsvg export -o demo.svg session.cast` |
| Export minified | `termsvg export -m session.cast` |
| Export without window chrome | `termsvg export -n session.cast` |
| Export with custom colors | `termsvg export -b "#1e1e2e" -t "#cdd6f4" session.cast` |
| Record + export in one go | `termsvg rec session.cast && termsvg export session.cast` |

## Commands

### `termsvg rec` — Record a Terminal Session

Records terminal activity to an asciicast (`.cast`) file.

```bash
termsvg rec output.cast
termsvg rec -c "cargo build" output.cast
termsvg rec -s output.cast   # skip first line
```

- Defaults to recording `$SHELL` if no `-c` command is given.
- Pause/resume with `Ctrl+P`.
- Stop recording with `Ctrl+D` or `exit`.

| Flag | Description |
|------|-------------|
| `-c, --command` | Command to record (default: `$SHELL`) |
| `-s, --skip-first-line` | Skip the first line of the recording |

### `termsvg play` — Replay a Recording

Plays back a recorded asciicast file in the terminal.

```bash
termsvg play session.cast
termsvg play -s 3 session.cast         # 3x speed
termsvg play -i 2 session.cast         # cap idle time at 2 seconds
termsvg play -s 0.5 -i 1 session.cast  # half speed, 1s idle cap
```

Best results when the terminal is the same size as the original recording.

| Flag | Description |
|------|-------------|
| `-s, --speed` | Playback speed factor (default: 1.0, fractional values accepted) |
| `-i, --idle-cap` | Max idle time in seconds (-1 for unlimited) |

### `termsvg export` — Export to Animated SVG

Converts an asciicast file to an animated SVG image.

```bash
termsvg export session.cast                    # outputs session.svg
termsvg export -o demo.svg session.cast        # custom output path
termsvg export -m session.cast                 # minified SVG
termsvg export -n session.cast                 # no window frame
termsvg export -b "#282a36" -t "#f8f8f2" session.cast  # Dracula colors
```

| Flag | Description |
|------|-------------|
| `-o, --output` | Output file path (default: `<input>.svg`) |
| `-m, --minify` | Minify SVG output (smaller file, slower export) |
| `-n, --nowindow` | Don't render the terminal window frame |
| `-b, --background-color` | Background color in hex (e.g., `#1e1e2e`) |
| `-t, --text-color` | Text color in hex (e.g., `#cdd6f4`) |

## Typical Workflows

### Documentation / README demo

```bash
termsvg rec -c "my-cli --help" help.cast
termsvg export -m help.cast
# produces help.svg — embed in README with <img src="help.svg">
```

### Tutorial with custom appearance

```bash
termsvg rec tutorial.cast
# ... interact with the shell, then exit ...
termsvg export -b "#002b36" -t "#839496" -m tutorial.cast
```

### Converting existing asciinema recordings

termsvg reads the same asciicast format as asciinema, so existing `.cast` files work directly:

```bash
termsvg export existing-recording.cast
```

### Minimal SVG (no window chrome)

```bash
termsvg export -n -m session.cast
```

## Global Flags

| Flag | Description |
|------|-------------|
| `--debug` | Enable debug output |
| `--version` | Print version info |
| `-h, --help` | Show help (context-sensitive per command) |

## Tips

- Use `-m` (minify) for production SVGs — it reduces file size significantly.
- Use `-n` (nowindow) when embedding SVGs inline where a terminal frame would be redundant.
- Cap idle time with `play -i 2` to skip long pauses when reviewing recordings.
- Pair with asciinema: record with `asciinema rec`, export with `termsvg export`.
- The `.cast` format is plain text (JSON lines) — you can edit timestamps or trim frames manually if needed.
- On Windows, only `play` and `export` are available (`rec` requires a Unix PTY).
