---
name: validate-vst3-editorhost
description: Test VST3 plugin UIs (.vst3 bundles) using Steinberg's EditorHost without a full DAW. Use when user says "test the plugin UI", "open in editorhost", "show the .vst3 editor", or wants to visually inspect the VST3 editor. For functional validation use validate-vst3 instead.
compatibility: macOS, Windows, Linux. Built from VST3 SDK source.
metadata:
  author: Oli Larkin
  version: 0.0.1
---

# VST3 EditorHost

Minimal VST3 host for testing plugin UIs without a full DAW.

## Plugin Install Locations

`editorhost` accepts a direct path to a `.vst3` bundle.

| Platform | User Location | System Location |
|----------|--------------|-----------------|
| macOS | `~/Library/Audio/Plug-Ins/VST3/` | `/Library/Audio/Plug-Ins/VST3/` |
| Windows | `%LOCALAPPDATA%\Programs\Common\VST3\` | `C:\Program Files\Common Files\VST3\` |
| Linux | `~/.vst3/` | `/usr/lib/vst3/` or `/usr/local/lib/vst3/` |

## Instructions

1. Build EditorHost from the VST3 SDK if not already built (see Building EditorHost below)
2. Run: `editorhost /path/to/plugin.vst3`
3. The plugin UI window should appear — verify layout, controls, and resizing
4. Test multiple editor instances with `--secondWindow`
5. If the UI doesn't appear, verify the plugin passes `validator` tests first

## Usage

```bash
# Basic usage - load plugin and show UI
editorhost /path/to/plugin.vst3

# With component handler (tests host callbacks)
editorhost --componentHandler /path/to/plugin.vst3

# Open second window (tests multiple editor instances)
editorhost --secondWindow /path/to/plugin.vst3

# Specify a particular effect class by UID
editorhost --uid "ABCD1234..." /path/to/plugin.vst3
```

### Binary Locations

| Platform | Typical Path |
|----------|-------------|
| macOS | `<vst3sdk>/build/bin/Release/editorhost.app/Contents/MacOS/editorhost` |
| Windows | `<vst3sdk>\build\bin\Release\editorhost.exe` |
| Linux | `<vst3sdk>/build/bin/Release/editorhost` |

## Building EditorHost

Clone the [VST3 SDK](https://github.com/steinbergmedia/vst3sdk) if you don't have it, then build:

```bash
cd <vst3sdk>
cmake -B build -G Ninja -DCMAKE_BUILD_TYPE=Release
cmake --build build --target editorhost
```

**Linux**: Requires X11 and GTK3 development libraries:
```bash
# Debian/Ubuntu
sudo apt install libx11-dev libgtkmm-3.0-dev libxcb-util-dev libxcb-cursor-dev libxcb-keysyms1-dev libxcb-xkb-dev

# Fedora
sudo dnf install libX11-devel gtkmm3.0-devel xcb-util-devel xcb-util-cursor-devel xcb-util-keysyms-devel libxkbcommon-x11-devel
```

## Troubleshooting

### Plugin doesn't load
- Check the plugin path is correct
- Verify the plugin passes `validator` tests first
- Check logs: Console.app (macOS), Event Viewer (Windows), or stderr (Linux)

### UI doesn't appear
- The plugin might not have an editor (`hasEditor()` returns false)
- Check if `createEditor()` is returning a valid view
- **Linux**: Ensure X11 display is available (`echo $DISPLAY`)

### UI appears but is blank/wrong size
- Check `defaultEditorSize()` returns valid dimensions
- For WebView UIs, check the HTML content is being set correctly
- Try with `--secondWindow` to see if the issue is with first-time setup
