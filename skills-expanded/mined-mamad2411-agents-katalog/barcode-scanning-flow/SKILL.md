# Barcode Scanning Flow

## Skill Metadata
```yaml
name: barcode-scanning-flow
domain: pos-domain
language: java
version: "1.0.0"
description: >
  Integrate barcode scanning in POS usingZXing for decode, USB keyboard wedge
  scanner input, and camera-based fallback scanning.
topics:
  - ZXing barcode decoding
  - USB keyboard wedge scanner integration
  - camera fallback scanning
  - scan result handling pipeline
constraints:
  - Use Java 21 records for scan results and commands
  - Constructor injection for all services
  - Graceful degradation: USB scanner → camera → manual entry
  - Thread-safe scanner input buffering
```

## Purpose

Handle barcode input from multiple sources in a POSterminal: USB barcode
scanners (keyboard wedge mode), built-in cameras, and manual entry fallback.
Uses ZXing for image-based decoding and raw input buffering for keyboard
wedge devices.

## Core Concepts

### USB Keyboard Wedge Scanner
- Most USB barcode scanners emulate a keyboard — they "type" the barcode data
- Detection strategy: buffer keystrokes; if a complete barcode arrives within
  a short time window (e.g., 50ms between chars, terminated by Enter), it's a scan
- Use `java.awt.KeyEvent` listening or raw HID input via `jnativehook`

### ZXing Integration
- `ZXing` (`com.google.zxing`) decodes barcodes from `BufferedImage`
- Supports: EAN-13, EAN-8, UPC-A, UPC-E, Code 128, Code 39, QR Code, Data Matrix
- `MultiFormatReader` attempts all supported formats
- Wrapped in a `BarcodeDecoder` service with constructor injection

### Camera Fallback
- When USB scanner is unavailable, use webcam via `OpenCV` or `WebcamCapture`
- Continuous capture → frame → ZXing decode → emit scan result
- Configurable capture resolution and frame rate
- Auto-focus and continuous focus mode preferred

### Architecture
- `BarcodeScanner` interface with `start()`, `stop()`, `onScan(Consumer<ScanResult>)`
- `KeyboardWedgeScanner` — USB scanner implementation
- `CameraScanner` — camera fallback implementation
- `CompositeScanner` — tries USB first, falls back to camera
- `ScanResult` record: barcode data, format, source, timestamp

## When to Use This Skill
- POS product lookup by barcode at checkout
- Inventory receiving/scanning
- Price verification stations
- Returns processing (scan receipt barcode)

## Related Skills
- `stock-movement-architecture` — scanned items feed stock movements
- `receipt-generation` — receipt barcodes for returns/verification
