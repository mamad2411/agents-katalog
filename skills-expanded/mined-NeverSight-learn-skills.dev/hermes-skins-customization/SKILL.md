---
name: hermes-skins-customization
description: Create and apply custom visual themes (skins) for the Hermes CLI agent, including colors, ASCII art, spinners, and branding.
triggers:
  - "customize Hermes appearance"
  - "create a Hermes skin"
  - "change Hermes theme"
  - "apply custom Hermes colors"
  - "make a new Hermes visual theme"
  - "style the Hermes CLI"
  - "design Hermes ASCII banner"
  - "modify Hermes spinner text"
---

# Hermes Skins Customization

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

Custom visual themes for the [Hermes CLI agent](https://github.com/NousResearch/hermes-agent). Skins control banner colors, ASCII art, spinner text, response labels, and branding — **not** behavior or personality.

## Installation

```bash
# Clone the repository
git clone https://github.com/joeynyc/hermes-skins.git
cd hermes-skins

# Copy skins to your Hermes config directory
mkdir -p ~/.hermes/skins
cp skins/*.yaml ~/.hermes/skins/
```

## Quick Start

### Apply a Skin

```bash
# Session-only (via Hermes command)
/skin pirate

# Permanent (edit ~/.hermes/config.yaml)
echo "display:
  skin: pirate" >> ~/.hermes/config.yaml
```

### Browse Available Skins

Check `~/.hermes/skins/` or the repository's `skins/` directory:

- **pirate** — Jolly Roger skull-and-crossbones
- **vault-tec** — Fallout green CRT terminal
- **bubblegum-80s** — Neon pastels and radical vibes
- **skynet** — Cyberdyne red military AI
- **lain** — Serial Experiments Lain NAVI aesthetic
- **neonwave** — Synthwave grid horizon
- **sakura** — Cherry blossom tree
- **netrunner** — Cyberpunk neural interface
- **mythos** — Eye of Providence Greek mythology
- **nous** — Nous Research amber and gold
- **mother** — Weyland-Yutani MU-TH-UR 6000
- **dos** — Norton Commander dual-pane
- **telemate** — DOS BBS terminal
- **empire** — Death Star targeting console
- **catppuccin** — Mocha pastels with ASCII cat

Built-in skins: `default`, `ares`, `mono`, `slate`, `poseidon`, `sisyphus`, `charizard`

## Creating a Custom Skin

### Minimal Skin Example

Create `~/.hermes/skins/cyberpunk.yaml`:

```yaml
name: cyberpunk
description: Neon terminal theme with magenta and cyan accents

colors:
  # Banner colors
  banner_border: "#FF00FF"
  banner_title: "#00FFFF"
  banner_accent: "#FF1493"
  
  # Text colors
  prompt: "#FF00FF"
  user_input: "#00FFFF"
  
  # Response colors
  response_box_border: "#FF00FF"
  response_label_text: "#000000"
  response_label_bg: "#00FFFF"
  
spinner:
  thinking_verbs: ["jacking in", "decrypting", "uploading", "syncing neural net"]
  
branding:
  agent_name: "CYBERDECK AI"
  response_label: " ⚡ NETRUN "
  prompt_symbol: "▶ "
```

**Note:** Undefined keys inherit from the `default` skin.

### Full Skin Example

For production skins, define **all 28 color keys** to avoid mismatched defaults:

```yaml
name: neon-city
description: Full cyberpunk theme with neon blues and hot pinks

colors:
  # Banner section
  banner_border: "#FF006E"
  banner_title: "#00F5FF"
  banner_accent: "#FFBE0B"
  banner_subtitle: "#8338EC"
  banner_meta: "#FB5607"
  
  # Prompt section
  prompt: "#FF006E"
  user_input: "#00F5FF"
  
  # Response section
  response_box_border: "#FF006E"
  response_label_text: "#000000"
  response_label_bg: "#00F5FF"
  response_text: "#FFFFFF"
  
  # Tool activity
  tool_prefix: "#FFBE0B"
  tool_name: "#8338EC"
  tool_details: "#FB5607"
  
  # System messages
  info: "#00F5FF"
  warning: "#FFBE0B"
  error: "#FF006E"
  success: "#3A86FF"
  
  # Interactive UI
  status_bar_bg: "#1A1A2E"
  status_bar_text: "#00F5FF"
  status_bar_highlight: "#FF006E"
  
  completion_menu_bg: "#16213E"
  completion_menu_text: "#FFFFFF"
  completion_menu_selected_bg: "#FF006E"
  completion_menu_selected_text: "#000000"
  completion_menu_border: "#00F5FF"

banner:
  art: |
    ⠀⣠⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣄⡀
    ⢸⣿⠀⠀⢀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⠀⠀⠀⠀⠀⣿⡇
    ⢸⣿⠀⠀⣿⡟⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⣿⠀⠀⠀⠀⠀⣿⡇
    ⢸⣿⠀⠀⣿⡇⢀⣀⣀⣀⣀⣀⣀⣀⡀⠀⣿⠀⠀⠀⠀⠀⣿⡇
    ⢸⣿⠀⠀⣿⡇⢸⣿⣿⣿⣿⣿⣿⣿⡇⠀⣿⠀NEON⠀⣿⡇
    ⢸⣿⠀⠀⣿⡇⢸⣿⣿⣿⣿⣿⣿⣿⡇⠀⣿⠀CITY⠀⣿⡇
    ⢸⣿⠀⠀⣿⡇⠀⠉⠉⠉⠉⠉⠉⠉⠀⠀⣿⠀⠀⠀⠀⠀⣿⡇
    ⢸⣿⠀⠀⠙⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠋⠀⠀⠀⠀⠀⣿⡇
    ⠀⠙⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠋⠀

spinner:
  faces: ["◢", "◣", "◤", "◥"]
  thinking_verbs:
    - "interfacing"
    - "decrypting datastream"
    - "compiling neural pathways"
    - "syncing wetware"
    - "routing through ICE"
    - "jacking in"

branding:
  agent_name: "NEON CITY AI"
  welcome_message: "◆ NEURAL LINK ESTABLISHED ◆"
  goodbye_message: "◇ CONNECTION TERMINATED ◇"
  prompt_symbol: "▶ "
  response_label: " ⬢ UPLINK "
  tool_activity_prefix: "◈ SYS:"
```

## Configuration Reference

### Color Keys (All 28)

#### Banner Section
- `banner_border` — Border characters
- `banner_title` — Main title text
- `banner_accent` — Accent elements
- `banner_subtitle` — Subtitle text
- `banner_meta` — Version/meta info

#### Prompt Section
- `prompt` — Prompt symbol color
- `user_input` — User-typed text

#### Response Section
- `response_box_border` — Response box border
- `response_label_text` — Label text color
- `response_label_bg` — Label background
- `response_text` — Response content

#### Tool Activity
- `tool_prefix` — Tool prefix icon
- `tool_name` — Tool name
- `tool_details` — Tool details/args

#### System Messages
- `info` — Info messages
- `warning` — Warning messages
- `error` — Error messages
- `success` — Success messages

#### Interactive UI
- `status_bar_bg` — Status bar background
- `status_bar_text` — Status bar text
- `status_bar_highlight` — Status bar highlights
- `completion_menu_bg` — Autocomplete menu background
- `completion_menu_text` — Menu text
- `completion_menu_selected_bg` — Selected item background
- `completion_menu_selected_text` — Selected item text
- `completion_menu_border` — Menu border

### Banner Art

Use multiline strings with braille Unicode (`⠀⠁⠂...⣿`) or ASCII art:

```yaml
banner:
  art: |
    ╔════════════════════════════════╗
    ║   █████╗ ██╗                  ║
    ║  ██╔══██╗██║                  ║
    ║  ███████║██║                  ║
    ║  ██╔══██║██║                  ║
    ║  ██║  ██║██║                  ║
    ║  ╚═╝  ╚═╝╚═╝                  ║
    ╚════════════════════════════════╝
```

### Spinner Configuration

```yaml
spinner:
  faces: ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
  thinking_verbs:
    - "processing"
    - "analyzing"
    - "computing"
    - "calculating"
    - "synthesizing"
```

### Branding Text

```yaml
branding:
  agent_name: "MY AI ASSISTANT"
  welcome_message: "System initialized. Ready for input."
  goodbye_message: "Shutting down. Goodbye."
  prompt_symbol: "➜ "
  response_label: " RESPONSE "
  tool_activity_prefix: "→ Tool:"
```

## Common Patterns

### Dark Theme Template

```yaml
name: my-dark-theme
description: High-contrast dark theme

colors:
  banner_border: "#00FF00"
  banner_title: "#FFFFFF"
  banner_accent: "#00FF00"
  banner_subtitle: "#AAAAAA"
  banner_meta: "#666666"
  
  prompt: "#00FF00"
  user_input: "#FFFFFF"
  
  response_box_border: "#00FF00"
  response_label_text: "#000000"
  response_label_bg: "#00FF00"
  response_text: "#E0E0E0"
  
  tool_prefix: "#00FF00"
  tool_name: "#FFFF00"
  tool_details: "#CCCCCC"
  
  info: "#00AAFF"
  warning: "#FFAA00"
  error: "#FF0000"
  success: "#00FF00"
  
  status_bar_bg: "#1A1A1A"
  status_bar_text: "#00FF00"
  status_bar_highlight: "#FFFFFF"
  
  completion_menu_bg: "#2A2A2A"
  completion_menu_text: "#E0E0E0"
  completion_menu_selected_bg: "#00FF00"
  completion_menu_selected_text: "#000000"
  completion_menu_border: "#00FF00"
```

### Retro CRT Terminal

```yaml
name: retro-crt
description: Amber phosphor CRT terminal

colors:
  banner_border: "#FFAA00"
  banner_title: "#FFCC44"
  banner_accent: "#FFAA00"
  banner_subtitle: "#CC8800"
  banner_meta: "#AA6600"
  
  prompt: "#FFAA00"
  user_input: "#FFCC44"
  
  response_box_border: "#FFAA00"
  response_label_text: "#000000"
  response_label_bg: "#FFAA00"
  response_text: "#FFCC44"
  
  tool_prefix: "#FFAA00"
  tool_name: "#FFCC44"
  tool_details: "#CC8800"
  
  info: "#FFCC44"
  warning: "#FFAA00"
  error: "#FF6600"
  success: "#FFDD66"
  
  status_bar_bg: "#000000"
  status_bar_text: "#FFAA00"
  status_bar_highlight: "#FFCC44"
  
  completion_menu_bg: "#1A0A00"
  completion_menu_text: "#FFCC44"
  completion_menu_selected_bg: "#FFAA00"
  completion_menu_selected_text: "#000000"
  completion_menu_border: "#FFAA00"

spinner:
  faces: ["▖", "▘", "▝", "▗"]
  thinking_verbs: ["PROCESSING", "COMPUTING", "ANALYZING"]

branding:
  agent_name: "TERMINAL-6000"
  prompt_symbol: "C:\\> "
  response_label: " OUTPUT "
```

### Minimal Monochrome

```yaml
name: minimal-mono
description: Clean grayscale aesthetic

colors:
  banner_border: "#FFFFFF"
  banner_title: "#FFFFFF"
  banner_accent: "#CCCCCC"
  banner_subtitle: "#AAAAAA"
  banner_meta: "#888888"
  
  prompt: "#FFFFFF"
  user_input: "#EEEEEE"
  
  response_box_border: "#CCCCCC"
  response_label_text: "#000000"
  response_label_bg: "#FFFFFF"
  response_text: "#DDDDDD"
  
  tool_prefix: "#CCCCCC"
  tool_name: "#FFFFFF"
  tool_details: "#AAAAAA"
  
  info: "#BBBBBB"
  warning: "#CCCCCC"
  error: "#FFFFFF"
  success: "#AAAAAA"
  
  status_bar_bg: "#1A1A1A"
  status_bar_text: "#CCCCCC"
  status_bar_highlight: "#FFFFFF"
  
  completion_menu_bg: "#2A2A2A"
  completion_menu_text: "#CCCCCC"
  completion_menu_selected_bg: "#FFFFFF"
  completion_menu_selected_text: "#000000"
  completion_menu_border: "#888888"

spinner:
  faces: ["—", "\\", "|", "/"]
  thinking_verbs: ["thinking", "working", "processing"]

branding:
  agent_name: "Assistant"
  prompt_symbol: "> "
  response_label: " Reply "
```

## Skin Loading Order

Hermes loads skins with this priority:

1. `~/.hermes/skins/<name>.yaml` (user custom)
2. Built-in skins in `skin_engine.py`
3. `default` skin (fallback)

Missing values inherit from `default`. Unknown skin names silently fall back to `default`.

## Troubleshooting

### Skin Not Loading

```bash
# Check file exists
ls -la ~/.hermes/skins/

# Verify filename matches name field
cat ~/.hermes/skins/myskin.yaml | grep "^name:"
# Should output: name: myskin

# Check for YAML syntax errors
python3 -c "import yaml; yaml.safe_load(open('~/.hermes/skins/myskin.yaml'))"
```

### Colors Not Applying

- **Define all 28 color keys** — partial definitions inherit mismatched defaults
- Use hex format `#RRGGBB` (6 digits)
- Test in a terminal with true color support

### ASCII Art Rendering Issues

```yaml
# Use multiline string with | or >
banner:
  art: |
    Line 1
    Line 2
    Line 3

# NOT this:
banner:
  art: "Line 1\nLine 2"  # May not render correctly
```

### Spinner Not Changing

```bash
# Restart Hermes after editing skins
# Session-only skin changes require:
/skin reload  # If supported
# Or restart the agent
```

## Testing Your Skin

```bash
# Apply temporarily
hermes --skin myskin

# Or use the /skin command during session
/skin myskin

# Test all elements by triggering:
# - Banner (startup)
# - Prompt (type a message)
# - Response (get a reply)
# - Tool activity (trigger a tool call)
# - Errors (type invalid command)
# - Spinner (long-running task)
```

## Generate Screenshots

If contributing to the repository:

```bash
cd hermes-skins
python3 generate_screenshots.py
# Creates screenshots/<skinname>.png for each skin
```

## Best Practices

1. **Always define all 28 colors** for production skins
2. **Test ASCII art** with different terminal widths
3. **Use descriptive thinking verbs** that match the theme
4. **Keep branding text concise** — long labels break layouts
5. **Validate YAML syntax** before submitting PRs
6. **Include a description** in the YAML and README

## Resources

- [Full Schema Documentation](https://github.com/joeynyc/hermes-skins/blob/main/SCHEMA.md)
- [Hermes Agent Repository](https://github.com/NousResearch/hermes-agent)
- [Braille Unicode Patterns](https://en.wikipedia.org/wiki/Braille_Patterns) — U+2800 to U+28FF
- [True Color Terminal Test](https://gist.github.com/XVilka/8346728)
