---
name: review-scoring-docx
description: >
  Use this skill whenever the user has one or more product review files and wants to
  (1) extract product attributes from the reviews, (2) score each product on those
  attributes, and (3) export the results into a Word document (.docx). Trigger on
  requests like 「從評論歸納屬性」、「幫我評分每個產品」、「做成 Word」、「產品屬性分析」、
  「評論轉評分表」, or any combination of "reviews → attributes → scores → Word/docx".
  Also trigger when the user uploads review files (CSV, JSON, TXT, or similar) and asks
  for comparative analysis, attribute extraction, or scoring — even without mentioning
  Maslow or Word explicitly.
---

# Review Scoring → Word Document

Converts raw product review files into a formatted Word document with two deliverables:

1. **Attribute catalog** — a minimum of 30 product attributes inferred from the full review corpus, each anchored to a Maslow need tier and accompanied by an evaluation dimension statement.
2. **Product × attribute score matrix** — every product scored 0–10 on every attribute, colour-coded by performance band, with per-attribute averages and per-product totals.

For a worked example using real Amazon reviews, see `references/worked-example.md`.

---

## Concepts and definitions

### Review corpus
All text written by customers about a product, collected across one or more files. A **valid review** is any entry whose body text exceeds 15 characters after stripping whitespace. No language filter is applied; multilingual corpora are treated identically to monolingual ones.

### Attribute
A distinct, evaluable dimension of product quality or experience that surfaces — positively or negatively — across multiple reviews. An attribute is not a feature; it is the *customer's lived experience* of that feature. For example, "anti-fog coating" is a feature; "fog resistance in practice" is an attribute.

Each attribute has four required fields:

| Field | Definition |
|-------|-----------|
| `id` | Zero-padded sequential number (01, 02 … 30+) |
| `label` | Concise display name; language matches the user's preference |
| `dimension` | One sentence stating exactly what reviewers say when this attribute is good or bad |
| `maslow_tier` | Which Maslow tier this attribute primarily satisfies (see table below) |

### Maslow tier mapping

Attributes must collectively cover all five tiers. The tiers and their characteristic questions are:

| Tier | Need type | Core question the attribute answers |
|------|-----------|--------------------------------------|
| 1 | Physiological | Does the product function as the body requires? (sensory, physical comfort) |
| 2 | Safety | Does the product reliably protect and hold up over time? |
| 3 | Belonging | Does the product connect the user to a group, relationship, or shared identity? |
| 4 | Esteem | Does the product make the user feel valued, seen, and not deceived? |
| 5 | Self-actualisation | Does the product help the user fully achieve their goal or potential? |

Minimum per-tier attribute counts: **5 for tiers 1 and 2**, **4 for tiers 3 and 4**, **5 for tier 5**.
Adjust upward if the corpus warrants richer coverage; never go below these floors.

### Score
An integer from 0 to 10 expressing the net sentiment signal for one product on one attribute, derived from the entire review set for that product.

| Band | Range | Signal |
|------|-------|--------|
| Critical failure | 0–2 | Near-universal negative; serious liability |
| Predominantly negative | 3–4 | Majority of mentions are complaints |
| Neutral / insufficient | 5 | Mixed signals, or attribute rarely mentioned |
| Mostly positive | 6–7 | Clear majority satisfied; occasional complaints |
| Strong positive | 8–9 | Consistently praised; very few negatives |
| Near-universal praise | 10 | Effectively no negative signal found |

**Absence rule:** if an attribute is never mentioned in any review for a product, assign 5.

---

## Workflow

### Step 0 — Locate required skills
Before writing any code, check the available skills listed in your context. You need a **docx skill** (any skill covering `.docx` or Word document creation). Read its SKILL.md fully before Step 4.

### Step 1 — Ingest reviews

1. Identify all uploaded review files from the conversation.
2. For each file, auto-detect the text-bearing column (common names: `body`, `Body`, `review`, `text`, `content`).
3. Load **all** valid reviews — no sampling, no row limit.
4. Print a per-product count summary before proceeding.

```python
import csv

def load_reviews(filepath):
    text_col_candidates = ['body', 'Body', 'review', 'Review', 'text', 'content']
    with open(filepath, encoding='utf-8', errors='replace') as f:
        reader = csv.DictReader(f)
        col = next((c for c in text_col_candidates if c in reader.fieldnames), None)
        if col is None:
            raise ValueError(f"No text column found. Headers: {reader.fieldnames}")
        return [r[col].strip() for r in reader
                if r[col].strip() and len(r[col].strip()) > 15]
```

### Step 2 — Discover and freeze the attribute catalog

1. Read through all reviews across all products to build a holistic picture of the corpus.
2. Identify recurring themes, complaint patterns, praise patterns, and unmet needs.
3. Formulate attributes **bottom-up from the corpus** — do not start from a fixed template.
4. Ensure all five Maslow tiers are covered at or above minimum floor counts.
5. Write out the complete catalog with all four required fields before scoring begins.
6. **Freeze it.** The catalog must not change after scoring starts.

Attribute discovery heuristics:
- Recurring noun phrases → candidate attributes
- Adjective + noun complaints (e.g. "flimsy arms", "blurry vision") → negative-pole definitions
- Absence evidence (e.g. "wish it came with a case") → packaging / completeness attribute
- Cross-language mentions count equally — translate and tally together
- After a first pass, check each Maslow tier for gaps; tier 3 (belonging) is most commonly under-represented

### Step 3 — Score every product

For each product:
1. Read through **all** its valid reviews.
2. For each attribute in the frozen catalog, tally the direction and intensity of reviewer mentions.
3. Weight by frequency (how many reviews mention it) and intensity (how strongly positive or negative).
4. Assign a single integer 0–10 per the scale defined above.

Store as: `scores: dict[product_id, list[int]]` — list length equals catalog size, ordered identically to the catalog.

### Step 4 — Build the Word document

Consult the docx skill you located in Step 0 for the full API reference. The document has two sections:

#### Section 1 — Portrait orientation: Attribute catalog table

Columns: `id` | `attribute label` | `evaluation dimension` | `Maslow tier`

- Differentiate tiers visually with distinct cell fill colours (one colour per tier, applied consistently to label and tier cells).
- Dark header row with white bold text.
- Consistent font throughout; body text 16–18 pt.

#### Section 2 — Landscape orientation: Product × attribute matrix

Columns: `id` | `attribute label` | one column per product | `row average`

- Include a **review-count sub-header row** directly below the product-ID header.
- Insert **tier separator rows** (full-width band in the tier's accent colour, bold tier label) before each tier group.
- **Colour-code score cells** by band: low → warm red; neutral → warm yellow; good → light green; excellent → strong green. Use a matching text colour within each band.
- Add a **legend row** above the matrix explaining the colour bands.
- Add a **product total-average row** at the bottom in a distinct dark header colour.

#### Docx layout rules (apply regardless of docx library)
- Use absolute units for all table widths — never percentage widths (they break in Google Docs).
- Set width on both the table-level column-widths array and on every individual cell.
- Use clear/transparent shading type, not solid fill, to prevent black-background rendering bugs.
- Landscape section: pass portrait dimensions plus an orientation flag.
- Never encode newlines as `\n` in text runs; use separate paragraph elements.

### Step 5 — Output

Write the `.docx` to the working directory, copy to the outputs directory, then call `present_files`.

Accompany the file with a prose summary stating:
- Total reviews per product and grand total
- Languages present in the corpus
- Top and bottom performers overall
- The two or three attributes with the widest score variance across products

---

## Hard rules

1. **Never truncate.** Every valid review (length > 15 chars) is read for scoring. No sampling.
2. **All languages count.** Non-English reviews carry equal weight.
3. **Freeze before scoring.** The catalog is finalised before any product is scored.
4. **Minimum 30 attributes.** Exception: corpus < 50 total reviews → 20 is acceptable; state the reason.
5. **Integer scores only.** Individual scores are whole numbers 0–10.
6. **Absolute table widths.** Percentage widths corrupt layout.
7. **Present with `present_files`.** Never ask the user to navigate to the file manually.
