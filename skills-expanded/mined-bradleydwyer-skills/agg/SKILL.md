---
name: agg
description: "Convert asciicast terminal recordings (.cast) to animated GIF using agg (asciinema gif generator). Use this skill whenever the user wants to convert a .cast file to GIF, create animated terminal GIFs for documentation or READMEs, or needs a GIF from a terminal recording. Trigger when the user mentions agg, asciicast to GIF, terminal GIF, cast to GIF, or wants to generate a GIF from an asciinema recording. Also trigger when the user wants to customize terminal GIF appearance (themes, fonts, speed)."
---

# agg — asciinema gif generator

Convert asciicast v2 recordings (`.cast` files) to high-quality animated GIFs with [agg](https://github.com/asciinema/agg). Uses gifski for optimized output with accurate frame timing.

## Installation

```bash
# Homebrew
brew install agg

# Cargo (requires Rust 1.85+)
cargo install --git https://github.com/asciinema/agg

# Docker
docker run --rm -v $PWD:/data ghcr.io/asciinema/agg demo.cast demo.gif
```

Pre-compiled binaries (x86_64, aarch64, arm) on the [releases page](https://github.com/asciinema/agg/releases).

## Quick Reference

| Task | Command |
|------|---------|
| Basic conversion | `agg demo.cast demo.gif` |
| From URL | `agg https://asciinema.org/a/569727.cast demo.gif` |
| From stdin | `cat demo.cast \| agg - demo.gif` |
| 2x speed | `agg --speed 2 demo.cast demo.gif` |
| Cap idle time | `agg --idle-time-limit 2 demo.cast demo.gif` |
| Custom theme | `agg --theme monokai demo.cast demo.gif` |
| Custom font/size | `agg --font-size 20 --font-family "Fira Code" demo.cast demo.gif` |
| No loop | `agg --no-loop demo.cast demo.gif` |
| Override terminal size | `agg --cols 100 --rows 30 demo.cast demo.gif` |
| Quiet mode | `agg -q demo.cast demo.gif` |
| Record + convert | `asciinema rec demo.cast && agg demo.cast demo.gif` |
| With termsvg | `termsvg rec demo.cast && agg demo.cast demo.gif` |

## Usage

```bash
agg [OPTIONS] <INPUT> <OUTPUT>
```

`<INPUT>` is a `.cast` file path, URL (including asciinema.org URLs), or `-` for stdin. `<OUTPUT>` is the GIF file path.

### Speed and Timing

```bash
agg --speed 2 demo.cast demo.gif              # 2x playback speed
agg --speed 0.5 demo.cast demo.gif            # half speed
agg --idle-time-limit 2 demo.cast demo.gif    # cap pauses at 2 seconds
agg --last-frame-duration 5 demo.cast demo.gif # hold last frame for 5s
agg --fps-cap 15 demo.cast demo.gif           # lower FPS = smaller file
agg --no-loop demo.cast demo.gif              # play once, don't loop
```

### Themes

Built-in themes via `--theme`:

| Theme | Description |
|-------|-------------|
| `dracula` | Dracula (default) |
| `asciinema` | asciinema default palette |
| `github-dark` | GitHub dark mode |
| `github-light` | GitHub light mode |
| `monokai` | Monokai |
| `nord` | Nord |
| `solarized-dark` | Solarized Dark |
| `solarized-light` | Solarized Light |
| `gruvbox-dark` | Gruvbox Dark |
| `kanagawa` | Kanagawa |
| `kanagawa-dragon` | Kanagawa Dragon |
| `kanagawa-light` | Kanagawa Light |

**Custom theme** — pass comma-separated hex triplets (no `#`):

```bash
# 10 values: bg, fg, color0-7
agg --theme 282a36,f8f8f2,282a36,f92672,a6e22e,f4bf75,66d9ef,ae81ff,a1efe4,f8f8f2 demo.cast demo.gif

# 18 values: bg, fg, color0-7, bright0-7
agg --theme 282a36,f8f8f2,282a36,f92672,a6e22e,f4bf75,66d9ef,ae81ff,a1efe4,f8f8f2,75715e,f92672,a6e22e,f4bf75,66d9ef,ae81ff,a1efe4,f9f8f5 demo.cast demo.gif
```

If the `.cast` file embeds a theme, agg uses it automatically. `--theme` overrides embedded themes.

### Fonts

```bash
agg --font-size 20 demo.cast demo.gif
agg --font-family "Fira Code" demo.cast demo.gif
agg --font-dir ~/fonts demo.cast demo.gif      # additional font directory
agg --line-height 1.6 demo.cast demo.gif
```

Default font search order: JetBrains Mono, Fira Code, SF Mono, Menlo, Consolas, DejaVu Sans Mono, Liberation Mono. System fonts are searched automatically. DejaVu Sans and Noto Emoji are added as fallbacks for symbols and emoji.

### Rendering Backend

```bash
agg --renderer resvg demo.cast demo.gif     # default, supports color emoji
agg --renderer fontdue demo.cast demo.gif   # direct rasterization, monochrome emoji only
```

### Terminal Size Override

```bash
agg --cols 120 --rows 40 demo.cast demo.gif
```

## CLI Options

| Option | Default | Description |
|--------|---------|-------------|
| `--speed` | `1` | Playback speed multiplier |
| `--idle-time-limit` | `5` | Max idle time in seconds |
| `--last-frame-duration` | `3` | Last frame hold time in seconds |
| `--fps-cap` | `30` | Max frames per second |
| `--no-loop` | off | Disable GIF looping |
| `--theme` | `dracula` | Color theme (named or custom hex) |
| `--font-family` | JetBrains Mono fallback chain | Font family (comma-separated) |
| `--font-size` | `16` | Font size in pixels |
| `--font-dir` | — | Additional font directory (repeatable) |
| `--line-height` | `1.4` | Line height multiplier |
| `--renderer` | `resvg` | Rendering backend (`resvg` or `fontdue`) |
| `--cols` | from recording | Override terminal width |
| `--rows` | from recording | Override terminal height |
| `-v, --verbose` | off | Verbose logging (stack for debug: `-vv`) |
| `-q, --quiet` | off | Suppress output and progress bars |

## Tips

- Pair with `asciinema rec` or `termsvg rec` to record, then `agg` to convert — they all use the asciicast v2 format.
- Use `--idle-time-limit 2` to trim dead time and keep GIFs short.
- Lower `--fps-cap` (e.g., 15) for smaller file sizes when smooth animation isn't critical.
- Use `--no-loop` for GIFs that play once — useful for step-by-step demos.
- Post-process with gifsicle for further size reduction: `gifsicle --lossy=80 -k 128 -O2 -Okeep-empty demo.gif -o demo-opt.gif`
- `--last-frame-duration 5` gives viewers more time to read the final output before the GIF loops.
- agg accepts URLs directly — no need to download `.cast` files first: `agg https://asciinema.org/a/569727.cast out.gif`
