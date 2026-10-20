---
name: draw-ansi
description: Draw/fix ANSI box-drawing so outer boxes are uniform width and never distorted
argument-hint: "[input]"
related:
  - draw-svg-image
  - draw-excalidraw
  - draw-tldraw
---

## Goal

Create or fix ANSI box-drawing so every outer box has uniform width across all lines, with aligned right borders and no distortion of the inner content

## Scope

Use for:
- Creating ` ```text ` codeblocks for README UI/CLI sketches
- Checking and repairing ANSI drawings with uneven lines
- Wrapping content (text or nested boxes) in an outer box of constant size

## Execute

### 1. Install / Run

> Goal: Run the `draw-ansi` script

```bash
bunx /path/to/draw-ansi/scripts/draw-ansi.ts [options] < input.txt
bunx /path/to/draw-ansi/scripts/draw-ansi.ts --width 60 --title "My App" < input.txt
bunx /path/to/draw-ansi/scripts/draw-ansi.ts --fix --width 60 existing-box.txt
```

### 2. Input Modes

> Goal: Support every box input mode

1. Plain lines: normal lines without a border → the script wraps them in an outer box
2. Existing box: lines start with `│` or `┌`/`└` → the script tries to detect the original box, then rewraps it

### 3. Output Modes

> Goal: Support every box output mode

- `--format text` (default): plain text, put it into a ` ```text ` block
- `--format markdown`: wrapped in a ` ```text ` block, ready to use

### 4. Options

> Goal: Specify the supported options

| Option | Description | Default |
|--------|-------------|---------|
| `--width` | Inner box width (excluding borders) | 58 or auto |
| `--title` | Add a title on the first line | none |
| `--fix` | Fix an existing box to uniform size | false |
| `--format` | `text` or `markdown` | text |

## Rules

### 1. Uniform Width

- Every line in the output must be exactly the same width
- If content exceeds `--width`, truncate it or warn
- If content is shorter than `--width`, pad spaces on the right

### 2. Outer Box

- Top border: `┌` + `─` × width + `┐`
- Bottom border: `└` + `─` × width + `┘`
- Left/right borders: `│` + content (padded) + `│`

### 3. Nested Box Support

- If a nested box inside is wider than `--width`, expand the outer box to fit or warn
- Never shrink/distort the nested box, unless truncation is required

### 4. No Distortion

- No distortion from special characters or emoji
- Do not use a ` ```ansi ` block
- Output is ready to drop into a README ` ```text ` block immediately
- Use /draw-svg-image if needed
- Use /draw-excalidraw if needed
- Use /draw-tldraw if needed

## Expected Outcome

- Every line in the ANSI box has the same width
- Right borders align
- The outer box does not distort the inner content
- Ready to paste into a README immediately
