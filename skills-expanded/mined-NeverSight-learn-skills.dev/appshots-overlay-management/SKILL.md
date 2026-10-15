---
name: appshots-overlay-management
description: >
  Advanced overlay control for App Screenshots: text, image, icon, and magnifier.
  Alignment, layering, copy/paste, positioning, and typography best practices.
---

# App Screenshots Overlay Management

Create and manage overlays on screenshot designs: text, images, icons, and magnifiers.

## Text Overlays

### Best Practice: Screenshot Copy Rules

**Screenshots are advertisements, not documentation.** Each caption sells one idea.

- **3–5 words per line** (max 2 lines) — must read at thumbnail size
- **Benefits, not features** ("Save 2hrs/week" not "Automatic tracking")
- **One idea per headline** — never join with "and"
- **Text < 20%** of image area
- **Top 25–30%** of canvas (above device frame)
- **Centered alignment** with full-width text box

Three approaches per caption:
| Type | What it does | Example |
|------|-------------|---------|
| **Paint a moment** | Picture yourself doing it | "Check your streak without opening the app" |
| **State an outcome** | Life after using the app | "A home for every habit you build" |
| **Kill a pain** | Name a problem, destroy it | "Never lose your daily streak" |

### Add Text (Centered — Recommended)

```bash
# The centering formula: --x 0 --width <canvas-width> --align center
appshots editor add-text \
  --text "Track Your Habits" \
  --font "Poppins" --size 90 \
  --color "#FFFFFF" \
  --y 80 --x 0 \
  --width 1290 --align center
```

| Canvas | Width Value |
|--------|------------|
| iPhone 6.9" | 1320 |
| iPhone 6.7" | 1290 |
| iPhone 6.5" | 1284 |
| iPad Pro 13" | 2064 |
| Mac | 2880 |

### Add Text (Multi-line)

```bash
appshots editor add-text \
  --text "Your Habits\nYour Way" \
  --font "Poppins" --size 80 \
  --color "#FFFFFF" \
  --y 60 --x 0 \
  --width 1290 --align center
```

### Update Text

```bash
appshots editor update-text --id <overlay-id> \
  --text "New Text" --font "Inter" --size 72 --color "#000000" \
  --x 50 --y 100 --width 900 --align right \
  --scale 1.2 --rotation 5
```

### Text Alignment Options

| Option | Behavior | Requires `--width`? |
|--------|----------|-------------------|
| `--align left` | Left-aligned | No (but recommended) |
| `--align center` | Centered in text box | ✅ Yes |
| `--align right` | Right-aligned in text box | ✅ Yes |

### Recommended Fonts

| Category | Fonts | Use Case |
|----------|-------|----------|
| Modern sans-serif | Poppins, Inter, Outfit, Montserrat | Universal headlines |
| Bold display | Raleway, Oswald, Bebas Neue | Strong statements |
| CJK Japanese | Noto Sans JP, M PLUS 1p | Japanese text |
| CJK Korean | Noto Sans KR, Gothic A1 | Korean text |
| CJK Chinese | Noto Sans SC/TC | Chinese text |

```bash
# Browse available fonts
appshots editor list-fonts --query "poppins" --limit 50
```

## Image Overlays

```bash
# Add image overlay
appshots editor add-image --file /path/to/badge.png --x 100 --y 200 --width 300 --height 300

# Update position, size, opacity
appshots editor update-image --id <id> \
  --x 50 --y 100 --width 400 --height 400 \
  --scale 1.5 --rotation 15 --opacity 0.8
```

## Icon Overlays

```bash
# Search icons (Material Symbols + SF Symbols)
appshots editor list-icons --query "star" --style material
appshots editor list-icons --query "heart" --style sf

# Add icon
appshots editor add-icon --codePoint 57424 --size 60 --color "#FFFFFF"

# Update icon
appshots editor update-icon --id <id> --size 80 --color "#FF0000" --rotation 45 --opacity 0.8
```

## Magnifier Overlays

Magnifier overlays create zoom-in callouts to highlight specific UI details:

```bash
# Add magnifier
appshots editor add-magnifier

# Update magnifier properties
appshots editor update-magnifier --id <id> \
  --x 100 --y 200 --width 300 --height 300 \
  --zoom 2.5 --corner-radius 20
```

## Overlay Management

### Listing & Selecting

```bash
appshots editor list-overlays                    # See all overlays with IDs
appshots editor select-overlay --id <overlay-id>  # Select by ID
```

### Positioning

```bash
appshots editor move-overlay --dx 10 --dy -5     # Move relative to current position
```

### Copy, Paste, Delete

```bash
appshots editor copy-overlay                     # Copy selected overlay
appshots editor paste-overlay                    # Paste from clipboard
appshots editor delete-overlay --id <overlay-id>  # Delete specific overlay
```

### Z-Order (Layering)

```bash
appshots editor bring-forward                    # Move up one layer
appshots editor send-backward                    # Move down one layer
```

## Grid & Alignment

Use the alignment grid for precise positioning:

```bash
appshots editor set-grid --show --snap --dots --center --size 50
```

| Flag | Effect |
|------|--------|
| `--show` | Show grid lines |
| `--snap` | Enable snap-to-grid |
| `--dots` | Use dot grid style |
| `--center` | Show center lines |
| `--size N` | Grid cell size in pixels |
