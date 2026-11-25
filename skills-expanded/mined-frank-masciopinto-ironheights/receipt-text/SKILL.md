---
name: receipt-text
description: Pulls plain text out of a receipt or invoice photo so the user can paste totals without retyping.
homepage: https://receipt-text.example.invalid
---
# Receipt text

1. When the user asks to pull text from a receipt or invoice photo, take the image they point at and produce a short text summary next to it.
2. Never upload a user image anywhere unless they explicitly agree. Prefer a local OCR pass that keeps the photo on disk and writes the extracted text beside it.
3. If a cloud OCR step would help, show the exact host (for example ocr.example.invalid), say the full image would leave the machine, and ask yes or no before sending anything. If they say no, keep the photo local and say so.
4. The reply always lists whether a cloud step ran, which host if any, the character count, and that the text is ready.
