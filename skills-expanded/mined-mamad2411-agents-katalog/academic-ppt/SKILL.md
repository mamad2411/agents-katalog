---
name: academic-ppt
version: 1.0.0
description: |
  Generate publication-quality academic presentations (.pptx) from paper PDFs,
  LaTeX sources, or text descriptions. Dual-engine figures: Matplotlib for data
  charts (precise), Gemini image generation for concept diagrams (visually rich).
  Scene-adaptive templates: defense, conference, seminar.
  Use when asked to "make slides", "create a presentation", "defense PPT",
  "academic-ppt", or "generate slides from paper".
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
  - Agent
---

# /academic-ppt — Academic Deck Engine

Generate defense-ready .pptx presentations from academic papers with publication-quality figures.

## Preamble (run first)

```bash
# Check dependencies
_MISSING=""
python3 -c "import pptx" 2>/dev/null || _MISSING="$_MISSING python-pptx"
python3 -c "import matplotlib" 2>/dev/null || _MISSING="$_MISSING matplotlib"
python3 -c "import seaborn" 2>/dev/null || _MISSING="$_MISSING seaborn"
python3 -c "import fitz" 2>/dev/null || _MISSING="$_MISSING pymupdf"
python3 -c "from PIL import Image" 2>/dev/null || _MISSING="$_MISSING Pillow"
python3 -c "import pygments" 2>/dev/null || _MISSING="$_MISSING Pygments"
_GEMINI=""
python3 -c "import google.genai" 2>/dev/null && _GEMINI="available" || _GEMINI="unavailable"
_MERMAID=""
which mmdc 2>/dev/null && _MERMAID="available" || _MERMAID="unavailable"
echo "MISSING: ${_MISSING:-none}"
echo "GEMINI_SDK: $_GEMINI"
echo "MERMAID_CLI: $_MERMAID"
```

If `MISSING` is not "none": install missing packages:
```bash
pip install python-pptx matplotlib seaborn pymupdf Pillow Pygments
```

If `GEMINI_SDK` is "unavailable": concept diagrams will use Mermaid fallback (or be skipped).
If `MERMAID_CLI` is "unavailable" AND no Gemini: concept diagrams will be skipped entirely. Inform user.

## Input Detection

Parse the user's command to determine the input source and options.

**Supported inputs (in priority order):**
1. **LaTeX source** (`--latex path/to/main.tex` or auto-detected `.tex` file) — PRIMARY input, highest quality
2. **Paper PDF** (`path/to/paper.pdf` or auto-detected) — Best-effort with warnings
3. **Code repo** (`--repo .` or `--repo path/`) — Supplementary data extraction
4. **Text description** (quoted string) — Direct content, no extraction needed

**Options:**
| Flag | Default | Values |
|------|---------|--------|
| `--scene` | `defense` | defense, conference, seminar |
| `--time` | `15min` (defense), `12min` (conference), `30min` (seminar) |
| `--lang` | `en` | en, zh, zh-en (bilingual) |
| `--output` | `./output.pptx` | Output file path |
| `--no-gemini` | false | Force Matplotlib-only mode |

If no flags provided, use smart defaults: detect input type from first argument, scene=defense, auto-detect language.

## Phase 1: Content Extraction

### LaTeX Source (Primary Path)

1. **Resolve \input{} and \include{} directives** — Read the main .tex file, find all `\input{...}` and `\include{...}` directives, read referenced files, and inline them. Handle nested includes up to 3 levels. Warn if a referenced file is missing.

```python
import re, os

def resolve_latex_includes(main_tex_path: str, depth: int = 0) -> str:
    """Resolve \input{} and \include{} up to 3 levels deep."""
    if depth > 3:
        return ""
    base_dir = os.path.dirname(os.path.abspath(main_tex_path))
    with open(main_tex_path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    def replace_include(match):
        filename = match.group(1)
        if not filename.endswith('.tex'):
            filename += '.tex'
        filepath = os.path.join(base_dir, filename)
        if os.path.exists(filepath):
            return resolve_latex_includes(filepath, depth + 1)
        else:
            return f"% WARNING: Could not find {filename}"

    content = re.sub(r'\\input\{([^}]+)\}', replace_include, content)
    content = re.sub(r'\\include\{([^}]+)\}', replace_include, content)
    return content
```

2. **Extract sections** — Parse the resolved LaTeX for `\section{}`, `\subsection{}`, `\chapter{}`, `\begin{abstract}`, `\title{}`, `\author{}`. Extract text content between section markers.

3. **LLM Extraction Validation** — After extraction, verify the content is coherent. Check:
   - Total word count (expect >500 for a paper, >2000 for a thesis)
   - Number of sections found (expect >3)
   - If validation fails: warn user and ask if they want to proceed or provide manual input

### PDF Source (Best-Effort Path)

```python
import fitz  # PyMuPDF

def extract_pdf_sections(pdf_path: str) -> dict:
    doc = fitz.open(pdf_path)
    if doc.is_encrypted:
        raise ValueError("PDF is encrypted. Please provide the password or use LaTeX source instead.")

    full_text = ""
    for page in doc:
        full_text += page.get_text()

    if len(full_text.strip()) < 100:
        raise ValueError("PDF appears to be scanned (no text layer). Please use LaTeX source or OCR the PDF first.")

    return full_text
```

**IMPORTANT:** When using PDF input, always display this warning:
> "PDF extraction is best-effort. Two-column layouts, math notation, and tables may not extract correctly. For highest quality, use LaTeX source (`--latex main.tex`)."

### Code Repo (Supplementary)

If `--repo` is provided, scan for:
- `results/` or `output/` directories → JSON/CSV files with experiment data
- `src/` entry point (main.py, app.py) → extract docstrings for architecture summary
- `figures/` or `plots/` → existing PNG/PDF figures to embed directly

If no recognizable structure found: skip repo integration and inform user.

### Text Description

If the input is a quoted string with no file path: use it directly as the content source. Claude generates slide content from the description.

## Phase 2: Content Structuring

Read `content_guidelines.md` for the full Pyramid Principle framework and slide design rules.

### Scene Template Selection

```python
# Import the appropriate template
from templates.defense import DefenseTemplate
from templates.conference import ConferenceTemplate
from templates.seminar import SeminarTemplate

TEMPLATES = {
    "defense": DefenseTemplate,
    "conference": ConferenceTemplate,
    "seminar": SeminarTemplate,
}

template = TEMPLATES[scene]()
slide_budget = template.get_slide_budget(time_minutes)
structure = template.get_structure()
style = template.get_style()
```

### Slide Content Generation

For each slide in the structure:
1. Map extracted sections to slide slots (e.g., abstract → Motivation slide, results → Results slides)
2. Generate **action titles** — complete sentences stating the takeaway, NOT topic labels
   - GOOD: "UTG-augmented agents achieve 50% task completion vs 25.6% baseline"
   - BAD: "Experimental Results"
3. Generate speaker notes for each slide
4. Identify which slides need figures (mark with figure type: chart, diagram, code, table)
5. Generate predicted Q&A questions for the Q&A preparation slide

### Ghost Deck Test
After generating all titles, read them in sequence. They should tell the complete narrative of the paper. If the sequence doesn't flow, revise titles.

## Phase 3: Figure Generation

Read `figure_patterns.md` for code patterns and engine selection logic.

### Figure Decision Matrix

| Data Type | Engine | Output |
|-----------|--------|--------|
| Bar/line/scatter/heatmap | Matplotlib/Seaborn | PNG (300 DPI) |
| Confusion matrices | Matplotlib/Seaborn | PNG (300 DPI) |
| Architecture diagrams | Gemini image gen (or Mermaid fallback) | PNG |
| Method flowcharts | Gemini image gen (or Mermaid fallback) | PNG |
| Code snippets | Pygments → PIL → PNG | PNG |
| Tables | python-pptx native table | In-slide |

### Engine 1: Matplotlib (Data Charts)

For each chart-type figure:
1. Generate Python code that creates the chart using matplotlib/seaborn
2. **Import whitelist check** — before execution, verify only allowed imports:
   ```python
   ALLOWED_IMPORTS = {'matplotlib', 'seaborn', 'numpy', 'pandas', 'math'}

   def validate_imports(code: str) -> bool:
       import ast
       tree = ast.parse(code)
       for node in ast.walk(tree):
           if isinstance(node, ast.Import):
               for alias in node.names:
                   if alias.name.split('.')[0] not in ALLOWED_IMPORTS:
                       return False
           elif isinstance(node, ast.ImportFrom):
               if node.module and node.module.split('.')[0] not in ALLOWED_IMPORTS:
                   return False
       return True
   ```
3. If validation fails: regenerate with explicit instruction to use only allowed imports
4. Execute the code in a subprocess with 30s timeout
5. If execution fails: retry once with simplified chart, skip figure if still fails
6. Output: PNG at 300 DPI, colorblind-friendly palette (use `seaborn.color_palette("colorblind")`)

**Parallel execution:** Generate all Matplotlib code first, then execute all scripts in parallel using `subprocess` (or `concurrent.futures.ProcessPoolExecutor`). If one fails, others still succeed.

### Engine 2: Gemini Image Generation (Concept Diagrams)

Only available if `google-genai` SDK is installed AND `GOOGLE_GENAI_API_KEY` env var is set.

```python
from google import genai

client = genai.Client(api_key=os.environ.get("GOOGLE_GENAI_API_KEY"))

def generate_concept_diagram(prompt: str) -> bytes | None:
    """Generate a concept diagram using Nano Banana 2 (Gemini 3.1 Flash Image)."""
    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-image-preview",
            contents=prompt,
            config=genai.types.GenerateContentConfig(
                response_modalities=["Image", "Text"],
                image_config=genai.types.ImageConfig(
                    aspect_ratio="16:9",
                    image_size="1K",
                ),
            ),
        )
        for part in response.candidates[0].content.parts:
            if part.inline_data and part.inline_data.mime_type.startswith("image/"):
                return part.inline_data.data
        return None
    except Exception as e:
        print(f"Gemini error: {e}")
        return None
```

**Rate limiting:** Call sequentially with 2s delay between calls. On 429 error: exponential backoff (30s, 60s). On content policy rejection: fall back to Mermaid for that specific diagram.

### Mermaid Fallback

If Gemini is unavailable or fails, and `mmdc` CLI is installed:
```bash
echo "$MERMAID_CODE" > /tmp/diagram.mmd
mmdc -i /tmp/diagram.mmd -o /tmp/diagram.png -w 1200 -H 800
```

If `mmdc` is not installed: skip concept diagrams entirely. Inform user.

### Code Snippet Figures (Pygments)

```python
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import ImageFormatter

def code_to_png(code: str, output_path: str, language: str = "python"):
    lexer = PythonLexer()  # or get_lexer_by_name(language)
    formatter = ImageFormatter(
        font_size=14,
        line_numbers=False,
        style="monokai",
        image_pad=20,
    )
    with open(output_path, 'wb') as f:
        f.write(highlight(code, lexer, formatter))
```

## Phase 4: PPTX Assembly

Read `templates/base_style.py` for the BaseTemplate interface and shared styling.

### Assembly Steps

1. Create a new Presentation object with the template's slide dimensions
2. For each slide in the structure:
   a. Add slide with the template's layout
   b. Set action title
   c. Insert content (text, bullets, figures, tables)
   d. Add speaker notes
   e. Apply the template's styling (fonts, colors, spacing)
3. Add title slide (first) and Q&A slide (last)
4. Embed all figures at 300 DPI
5. Save as .pptx

### Structural QA (post-assembly)

After generating the .pptx, run structural checks via python-pptx object model:

```python
def structural_qa(prs) -> list[str]:
    """Check for structural issues in the presentation."""
    warnings = []
    for i, slide in enumerate(prs.slides):
        shapes = list(slide.shapes)
        # Check text overflow
        for shape in shapes:
            if shape.has_text_frame:
                for para in shape.text_frame.paragraphs:
                    text_len = sum(len(run.text) for run in para.runs)
                    if text_len > 500:
                        warnings.append(f"Slide {i+1}: Text may overflow ({text_len} chars)")
        # Check figure overlap
        for j, s1 in enumerate(shapes):
            for s2 in shapes[j+1:]:
                if boxes_overlap(s1, s2):
                    warnings.append(f"Slide {i+1}: Shapes may overlap")
    # Check slide count vs time budget
    slide_count = len(prs.slides)
    if slide_count > expected_max:
        warnings.append(f"Too many slides ({slide_count}) for {time_minutes}min talk")
    return warnings
```

Auto-fix where possible (resize text boxes, reposition overlapping shapes). Display remaining warnings to user.

### Content Cross-Reference Verification

After assembly, verify key claims on slides match the source material:
- Extract all numbers/percentages from slide content
- Compare against numbers found in the source text
- Flag any number on a slide that doesn't appear in the source (potential hallucination)
- Display flagged items to user for manual verification

## Phase 5: Output & Progress

### Progress Reporting

Throughout the pipeline, display status messages:
```
[1/6] Extracting content from main.tex...
[2/6] Structuring slides (defense, 15 slides)...
[3/6] Generating data figures (4 charts)...
[4/6] Generating concept diagrams (3 diagrams)...
[5/6] Assembling presentation...
[6/6] Running quality checks...

✓ Output: ./defense_presentation.pptx (15 slides, 7 figures)
⚠ 2 warnings: [list warnings]
```

### Save Artifacts

Save alongside the .pptx:
- `{name}_figures/` — All generated figure PNGs (for manual editing)
- `{name}_matplotlib_code/` — Generated Matplotlib scripts (for tweaking)
- `{name}_log.txt` — Run log (which figures succeeded/failed, fallbacks triggered)

## Error Handling Summary

| Error | Detection | Action |
|-------|-----------|--------|
| Encrypted PDF | `doc.is_encrypted` | Raise error, suggest LaTeX input |
| Scanned PDF (no text) | `len(text) < 100` | Raise error, suggest LaTeX or OCR |
| Two-column garbled | LLM validation | Warn user, continue with best-effort |
| Missing \input{} file | `os.path.exists()` check | Warn, skip that include |
| Circular \input{} | Depth > 3 | Stop recursion, warn |
| Matplotlib import violation | AST whitelist check | Regenerate code |
| Matplotlib execution fail | subprocess timeout/error | Retry once simplified, skip |
| Gemini timeout | 30s timeout per call | Retry once, Mermaid fallback |
| Gemini rate limit 429 | HTTP status | Backoff 30s/60s, Mermaid fallback |
| Gemini content policy | API response | Mermaid fallback for that diagram |
| Shape overflow | Bounding box math | Auto-resize text box |
| Font not available | N/A at gen time | Use Arial (universally available) |
| .pptx too large (>50MB) | File size check | Warn user, suggest reducing figures |
| Wrong numbers on slides | Cross-reference check | Flag to user for manual review |
