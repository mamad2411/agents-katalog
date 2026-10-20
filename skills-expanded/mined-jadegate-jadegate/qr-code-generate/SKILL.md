---
name: qr-code-generate
description: Generate QR code image from text using public API
---

# QR Code Generator

Generate QR code image from text using public API

## When to Use

- User wants to generate qr
- User wants to qr code
- User wants to make qr
- Keywords: qrcode, generate, image, barcode

## Required Parameters

- **text** (string): Text to encode in QR code
- **size** (number): Image size in pixels

## Output

- **image_url** (string): URL of generated QR image
- **text** (string): Encoded text

## Security

- Sandbox level: strict
- Max execution time: 30000ms
- Network whitelist: api.qrserver.com
- JadeGate verified: Yes (5-layer security check passed)

## Execution Flow

Entry: `encode` -> 6 steps -> Exit: `ret_ok`, `ret_fail`
