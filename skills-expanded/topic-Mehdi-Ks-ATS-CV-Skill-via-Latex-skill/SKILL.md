---
name: latex-cv
description: >
  Generate a polished, ATS-compatible single-page CV in LaTeX from any uploaded CV file (PDF, DOCX, or plain text).
  Produces a ready-to-compile Overleaf zip containing main.tex + company logos + a step-by-step Overleaf tutorial.
  Use this skill whenever the user wants to create, rebuild, or reformat their CV in LaTeX, mentions "Overleaf",
  asks for an "ATS-compatible CV", or uploads a CV and asks to improve or redesign it.
  Trigger even if the user just says "make me a CV", "build my resume in LaTeX", or "turn my CV into a nice PDF".
---

# LaTeX CV Generator

Turns any uploaded CV into a single-page, visually polished, ATS-compatible LaTeX CV — packaged as a zip ready to drop into Overleaf.

The output always has:
- **Compiler**: XeLaTeX (mandatory — the design uses `fontspec`)
- **Design**: green accent spine, centered serif name, clickable company URLs
- **ATS compliance**: section headers use plain `\MakeUppercase` (no `LetterSpace`) so ATS extractors read "SUMMARY" not "S U M M A R Y"
- **Single page**: all spacing is tuned to fit; warn the user if content risks overflow

Read `references/base_template.tex` for the full LaTeX preamble and command definitions before generating any .tex output. Read `references/overleaf_guide.md` for the tutorial text to bundle in the zip.

---

## Step 1 — Parse the CV

Read the uploaded file. Extract these fields:

| Field | Notes |
|---|---|
| Full name | |
| Tagline | 1-line role descriptor in ALL CAPS, parts separated by ` · ` |
| Location, phone, email, LinkedIn URL | |
| Summary | 3–4 sentence prose paragraph |
| Skills | Group into categories e.g. Data & Analytics / Systems & Cloud / Engineering / Languages (adapt to the person) |
| Work experience | Per role: job title, company, location, work mode, start–end dates, 2–5 bullet points |
| Education | Institution, degree, years |
| Leadership & Recognition | Title, org, year (compact, one line each) |

If any field is ambiguous or missing, ask the user before proceeding. Do not invent content.

---

## Step 2 — Collect Company URLs

For each employer, institution, and leadership org, find the correct public website:

- Prefer official corporate/about pages over client-facing homepages
- If a company website is broken or unavailable, use their LinkedIn page: `https://www.linkedin.com/company/<slug>/`
- If unsure, leave the URL as `{}` and add a `% TODO: verify URL` comment in the .tex file
- Use web search to look up URLs you don't know

---

## Step 3 — Handle Logos

Each `\jobheader` call needs a `logo_<company>.png` file (lowercase, underscores, no spaces).

**If the user provides logos** (in a zip or folder): use them as-is, rename to match the convention.

**If no logos are provided**: generate placeholder PNGs using Python + Pillow:

```python
from PIL import Image, ImageDraw, ImageFont

def make_placeholder_logo(initials, filename, size=200,
                           bg=(15,110,86), fg=(255,255,255)):
    img = Image.new("RGBA", (size, size), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([0, 0, size-1, size-1], fill=bg)
    try:
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            size // 3)
    except Exception:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), initials, font=font)
    w, h = bbox[2]-bbox[0], bbox[3]-bbox[1]
    draw.text(((size-w)//2, (size-h)//2), initials, fill=fg, font=font)
    img.save(filename)
```

Run `pip install Pillow --break-system-packages` if needed. After generating, tell the user which logos are placeholders and suggest they replace them with real ones.

**Logo height**: use `0.50cm` for most logos. Use `0.65cm` for logos that appear small due to extra padding in the PNG.

---

## Step 4 — Generate main.tex

Read `references/base_template.tex`. It contains the complete LaTeX preamble — colors, fonts, geometry, command definitions. Do not rewrite the preamble; copy it verbatim and fill in only the document body sections marked with `% <<< FILL: ... >>>`.

**Critical rules — never break these:**
- `\cvsection` and `\sklabel` must use `\MakeUppercase`, never `\tracked` — this is the ATS fix
- All bullet itemize blocks: `{\fontsize{9}{11}\selectfont \begin{itemize} ... \end{itemize}}`
- Add `\vspace{-3pt}` before the first `\jobheader` after each `\cvsection{Work Experience}` to close the gap
- Leave `% TODO: verify URL` comments for any URL you are not confident about
- The `\jobheader` command takes **6** arguments: logo file, title, company+location, date, url, logo height
- The `\recogentry` command takes **4** arguments: logo file, title, org+date, url

**Bullet writing guide:**
- Start every bullet with a strong action verb (Architected, Delivered, Built, Led, Reduced…)
- Include at least one hard number per bullet where possible (%, ×, counts, time savings)
- Keep bullets to 1–2 rendered lines max

---

## Step 5 — Assemble and Deliver the Zip

```bash
mkdir -p /tmp/cv_latex_output
# Copy main.tex and all logo_*.png files into /tmp/cv_latex_output/
# Copy the overleaf tutorial:
cp references/overleaf_guide.md /tmp/cv_latex_output/OVERLEAF_SETUP.md
cd /tmp/cv_latex_output && zip -r /tmp/cv_overleaf.zip .
```

Save the zip to the workspace outputs folder, then present it with `present_files`.

---

## Design Constants (do not change)

| Token | Value |
|---|---|
| Accent green | `#0F6E56` |
| Accent light green | `#1D9E75` |
| Body font | TeX Gyre Heros (via `fontspec`) |
| Name font | TeX Gyre Pagella (via `\namefont`) |
| Name size | 25pt / 27pt leading |
| Accent rule under name | `\rule{0.24\textwidth}{0.8pt}` |
| Section header | 9pt bold, `\MakeUppercase`, NO LetterSpace |
| Skill label | 8.5pt bold, `\MakeUppercase` |
| Job title | 10pt bold |
| Company line | 8.5pt, accent color |
| Bullet body | 9pt / 11pt leading |
| Margins | top 5mm, bottom 4mm, left 16mm, right 10mm |
| Green spine | 4pt wide TikZ rect, left edge, full page height |
| Bullet marker | `\textcolor{accentlt}{\rule{4pt}{1.2pt}}` |

---

## Single-Page Constraint

The CV **must** fit on one page. If content is too long, in order:
1. Reduce older/less-relevant bullets first
2. Drop short internship bullets to 1 line
3. Trim the summary to 2–3 sentences
4. As a last resort, reduce bullet font from 9pt to 8.5pt

Always tell the user if content was trimmed.
