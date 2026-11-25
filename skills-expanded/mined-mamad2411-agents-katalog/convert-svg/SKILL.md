---
name: convert-svg
description: Convert bitmap images to SVG with a bunx CLI
argument-hint: "[input]"
related:
  - convert
  - idea
  - draw-svg-image

---

## Goal

Convert bitmap images (PNG/JPG) to SVG vectors with a `bunx` CLI

## Scope

- Accept an image file as input
- Use potrace-based CLIs for tracing
- Support output paths and optimization

## Execute

### 1. Identify Input

> Goal: Validate the input

1. Get the input path from the user
2. Verify the file exists and is an image (png/jpg/jpeg/gif/bmp)
3. Check the file size; if it is too large, resize first or warn the user

### 2. Choose CLI

> Goal: Pick a tool that is ready to use

1. Primary: `bunx images-to-svg convert <input>`
   - Handles both files and directories
   - Uses sharp, potrace, svgo
2. Fallback: `bunx potrace-cli <input> -o output.svg`
3. Fallback: `bunx potrace <input> -s -o output.svg`
4. Last resort: install `sharp` + `potrace` and write a Node/Bun script

### 3. Run Conversion

> Goal: Convert bitmap to SVG

1. Run the command with an output path
2. If the input is a directory → convert everything in it
3. Verify the output file

### 4. Optimize And Validate

> Goal: Make the SVG correct and ready to use

1. Optimize the output with `bunx svgo` if desired
2. Check that the SVG opens in a browser
3. Report the input/output paths

## Rules

### 1. Quality

- Tracing works best on high-contrast images
- If the input is a colorful photo → warn the user the SVG may not be faithful
- For logos/line art → best results

### 2. Color

- potrace defaults to monochrome
- For color, use `images-to-svg` or post-tracing steps

### 3. Fallback

- If the first tool fails → try `potrace-cli`
- If that fails too → use a script with `sharp` + `potrace`

- Use /convert-git-submodules if needed
- Use /idea-convert-my-global-cli-to-skills if needed
- Use /convert-files-format if needed
- Use /draw-svg-image if needed

## Expected Outcome

- A `.svg` file is generated from the bitmap
- The SVG is editable and scalable
- Report the tool used and the output path
