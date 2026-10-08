#!/usr/bin/env python3
"""read.py FILE — baca gambar/PDF: teks langsung + OCR. Simple, tanpa batas."""
import sys, os
f = sys.argv[1] if len(sys.argv) > 1 else ""
if not f or not os.path.exists(f):
    print("kasih path file: read.py /path/ke/file.png"); sys.exit(1)
ext = f.lower().rsplit(".", 1)[-1]
if ext == "pdf":
    import pymupdf
    doc = pymupdf.open(f)
    print(f"HALAMAN: {len(doc)}")
    for i, pg in enumerate(doc):
        print(f"--- hal {i+1} ---")
        t = pg.get_text().strip()
        if t:
            print(t)
        else:
            print("(gambar, OCR...)")
            pix = pg.get_pixmap(dpi=200)
            import pytesseract
            from PIL import Image
            import io
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            print(pytesseract.image_to_string(img))
else:
    from PIL import Image
    import pytesseract
    print(pytesseract.image_to_string(Image.open(f)))
