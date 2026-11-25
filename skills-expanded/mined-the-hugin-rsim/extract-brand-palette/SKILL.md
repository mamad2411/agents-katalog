# Skill: extract-brand-palette

**Purpose:** Extract brand hex color palette from image-based PDF or PNG via pixel sampling (PyMuPDF). Used as utility inside `doc-creator` and standalone.
**When:** Need exact brand colors from a PDF presentation, landing page, logo, or any raster source — and standard text parsing returns nothing.
**Output:** List of hex values (Primary / Secondary / Accent) + ready CSS variables.

---

## PROCESS

### Step 0 — Check: text PDF or image-based?

```python
import fitz
doc = fitz.open("file.pdf")
text = doc[0].get_text()
print(repr(text[:300]))
```

- **Has text** → text PDF. Colors can be found via annotations, structure, or set manually.
- **Empty / only whitespace** → image-based PDF. Continue with this skill.

> If user passed PNG/JPG directly — skip Step 0, start from Step 1.

---

### Step 1 — Install dependency (if missing)

```bash
py -m pip install pymupdf
```

Check: `py -c "import fitz; print(fitz.__version__)"` — should return version without errors.

---

### Step 2 — Pixel sampling across key zones

Zones for sampling (y = fraction of page height):

| Zone   | Y range | What we look for |
|--------|---------|-----------------|
| Header | 0–8%    | Logo, navbar, header background color |
| Footer | 92–100% | Accent bar, buttons, colored footer |
| Accent | 45–55%  | Color blocks in middle of slide |

```python
import sys, fitz
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

def sample_zone(page, y_start_pct, y_end_pct, step=5):
    """Collect dominant colors in page zone."""
    pix = page.get_pixmap(dpi=72)
    w, h = pix.width, pix.height
    y0 = int(h * y_start_pct)
    y1 = int(h * y_end_pct)
    counts = Counter()
    for y in range(y0, y1, step):
        for x in range(0, w, step):
            r, g, b = pix.pixel(x, y)[:3]
            # Filter white and black
            if r > 240 and g > 240 and b > 240: continue
            if r < 15  and g < 15  and b < 15:  continue
            # Quantize to step 8 for grouping similar colors
            key = (r // 8 * 8, g // 8 * 8, b // 8 * 8)
            counts[key] += 1
    return counts.most_common(3)

doc = fitz.open("file.pdf")
page = doc[0]  # Cover — most informative slide

zones = {
    "header": sample_zone(page, 0.00, 0.08),
    "footer": sample_zone(page, 0.92, 1.00),
    "accent": sample_zone(page, 0.45, 0.55),
}

for zone, colors in zones.items():
    print(f"\n{zone}:")
    for (r, g, b), cnt in colors:
        print(f"  #{r:02x}{g:02x}{b:02x}  (count: {cnt})")
```

---

### Step 3 — Interpret results

After output — determine color roles:

```
Primary   = most frequent color from header (header bg / main brand)
Secondary = second most frequent from header or accent
Accent    = most saturated/bright from footer (buttons, CTA)
```

**Accent color signs:** high saturation (one channel >> others), appears in footer/buttons, differs from primary in hue.

---

### Step 4 — Output CSS variables

```css
:root {
  --color-primary:   #xxxxxx;   /* header, section titles */
  --color-secondary: #xxxxxx;   /* subtitles, card backgrounds */
  --color-accent:    #xxxxxx;   /* buttons, accent borders, list markers */
  --color-bg:        #ffffff;   /* page background */
  --color-text:      #1a1a1a;   /* body text */
}
```

Show to user — wait for confirmation before applying to CSS.

---

## NOTES AND LIMITATIONS

- **Sampling step: 5px** — speed/accuracy balance. Decrease to 2 for accuracy, increase to 10 for speed on large files.
- **Quantization // 8** — groups similar colors (#1c254f and #1e274f → one group). Decrease to // 4 for finer differentiation.
- **Page 0** — usually cover. If brand shows on different page — change index.
- **Multiple pages** — for better results, average across pages 0, 1, 2 and take most stable color.
- **PNG/JPG** — use `PIL.Image` instead of `fitz`: `img.getdata()` → same Counter algorithm.
