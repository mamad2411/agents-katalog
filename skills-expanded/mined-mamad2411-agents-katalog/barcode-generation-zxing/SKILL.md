---
name: barcode-generation-zxing
description: >
  Extends agent's knowledge of generating QR codes and barcodes in Java
  POS applications using ZXing. Use when producing receipt QR codes for
  payment links, shelf labels, or inventory barcodes.
compatibility: Java 21+
metadata:
  domain: reporting
  level: beginner
  stack: [java-21, zxing, javafx-21, slf4j-2]
  version: "1.0.0"
---

# Barcode Generation with ZXing

ZXing ("Zebra Crossing") is the standard library for generating and
decoding barcodes in Java. In POS, it generates QR codes for e-wallet
payment links and Code128 barcodes for product shelf labels.

## Concepts

- **QR Code** — 2D matrix barcode; stores up to 4,296 alphanumeric
  characters; supports error correction levels (L/M/Q/H).
- **Code128** — 1D linear barcode; compact for numeric/alphanumeric
  data; used for product EAN codes.
- **`BitMatrix`** — ZXing's internal representation; render to
  `BufferedImage` or JavaFX `Image`.
- **Error correction** — QR codes can recover data even when partially
  damaged; use `ErrorCorrectionLevel.H` for retail labels.

## Rules

1. Generate QR codes for payment URLs with minimum 200×200 px
   resolution so phone cameras can scan reliably.
2. Use `ErrorCorrectionLevel.M` for payment QR codes (15% recovery);
   use `H` for labels that may be scratched.
3. Encode Code128 for product numbers — it's more compact than QR for
   short numeric strings.
4. Cache generated barcode images for frequently-scanned product codes.
5. Validate input length before encoding — QR and Code128 have hard
   limits; throw `IllegalArgumentException` for oversize input.

## Anti-patterns

See [anti-patterns.md](./anti-patterns.md).

## Related

- jasperreports-basics — embedding barcodes in JasperReports templates
- mvvm — binding barcode images to JavaFX views
