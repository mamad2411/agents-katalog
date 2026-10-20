---
name: image-resize-convert
description: Resize images and convert between formats (PNG, JPG, WebP)
---

# Image Resize and Convert

Resize images and convert between formats (PNG, JPG, WebP)

## When to Use

- User wants to resize image
- User wants to convert image
- Keywords: image, resize, convert, format

## Required Parameters

- **input_path** (string): Input image path
- **output_path** (string): Output image path

## Optional Parameters

- **width** (number): Target width
- **height** (number): Target height
- **format** (string): Output format: png, jpg, webp

## Output

- **success** (boolean): Operation success
- **output_path** (string): Output file path
- **size_bytes** (number): Output file size

## Security

- Sandbox level: strict
- Max execution time: 30000ms
- JadeGate verified: Yes (5-layer security check passed)

## Execution Flow

Entry: `check_input` -> 6 steps -> Exit: `ret_ok`, `ret_fail`
