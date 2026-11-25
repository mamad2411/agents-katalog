---
name: pdf-presentation
description: "Generate professional PDF reports and presentations from structured content. Converts evaluations, proposals, and assessments into polished PDFs with tables, score visualizations, and styled sections. Use when: generate PDF, create report, export to PDF, make presentation, create proposal document, export evaluation."
license: MIT
metadata:
  version: 1.0.0
  category: document-generation
  tags: [pdf, report, presentation, export, document]
---

# PDF Presentation Skill

Generate professional PDF reports from structured content using WeasyPrint.

## When This Skill Activates

Trigger phrases: "generate PDF", "create report", "export to PDF", "make presentation", "create proposal document", "export evaluation", "PDF report".

## Workflow

### Step 1: Analyze Content

Identify what type of content needs to be exported:

- **Architect Evaluation**: Look for Value Matrix, Opportunity Score (1-10), sub-scores, risk assessment, recommendations. Structure as a full evaluation report with title page.
- **General Report/Proposal**: Any structured document with sections, headings, and body text. Structure with a cover page and sectioned layout.
- **Comparison Table**: Side-by-side analysis of options. Structure with prominent tables.
- **Scored Assessment**: Any content with numerical ratings or grades. Include SVG score visualizations.

### Step 2: Build the HTML Document

Create a complete HTML file with inline CSS. Use the template structure from `assets/templates/report.html` as reference. The HTML must be self-contained (no external stylesheets, no external images).

#### Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <style>
    /* Include all CSS inline - see template for full styles */
    /* Use CSS Paged Media for print: @page rules, page counters */
  </style>
</head>
<body>
  <div class="cover-page"><!-- Title, subtitle, date, author --></div>
  <div class="section"><!-- Each major section --></div>
</body>
</html>
```

#### CSS Guidelines

- Use the professional color palette from the template: `#1a365d` (primary navy), `#2b6cb0` (accent blue), `#e2e8f0` (light gray), `#f7fafc` (background)
- Set `@page` rules with 20mm margins, running headers/footers
- Use `page-break-before: always` for major sections
- Typography: system font stack, 11pt body, 1.6 line-height
- Tables: alternating row colors, proper padding, header styling

#### SVG Score Visualizations

For numerical scores (1-10 scale), generate inline SVG elements:

**Horizontal bar chart** for sub-scores:
```html
<svg width="300" height="24" xmlns="http://www.w3.org/2000/svg">
  <rect width="300" height="24" rx="4" fill="#e2e8f0"/>
  <rect width="210" height="24" rx="4" fill="#2b6cb0"/>
  <text x="150" y="16" text-anchor="middle" fill="white" font-size="12" font-weight="600">7/10</text>
</svg>
```
The filled width = (score / max_score) * total_width.

**Gauge circle** for overall scores:
```html
<svg width="120" height="120" viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
  <circle cx="60" cy="60" r="50" fill="none" stroke="#e2e8f0" stroke-width="10"/>
  <circle cx="60" cy="60" r="50" fill="none" stroke="#2b6cb0" stroke-width="10"
    stroke-dasharray="220" stroke-dashoffset="88" stroke-linecap="round"
    transform="rotate(-90 60 60)"/>
  <text x="60" y="65" text-anchor="middle" font-size="28" font-weight="700" fill="#1a365d">7.2</text>
  <text x="60" y="82" text-anchor="middle" font-size="11" fill="#718096">out of 10</text>
</svg>
```
The stroke-dashoffset = circumference - (score / max_score) * circumference. Circumference for r=50 is ~314.

**Color coding for scores:**
- 8-10: `#38a169` (green)
- 5-7: `#d69e2e` (amber)
- 1-4: `#e53e3e` (red)

#### Architect Evaluation Specifics

When exporting Architect evaluation results, include these sections:

1. **Cover Page**: Idea/project name, evaluation date, mode (New Idea / Existing Project)
2. **Executive Summary**: 2-3 sentence overview with Go/No-Go recommendation
3. **Opportunity Score**: Large gauge SVG with overall score, then bar chart for all 6 sub-scores
4. **Value Matrix**: 3-column table (Commercial / Educational / Social) with scores and notes
5. **Evaluator Reports**: One section per evaluator with their findings
6. **Risk Assessment**: Risk matrix table with severity/likelihood
7. **Recommendations**: Prioritized action items
8. **Next Steps**: Concrete actionable items with timeframes

### Step 3: Write the HTML File

Save the generated HTML to a temporary file. Use a descriptive filename:
- For evaluations: `evaluation-<slug>.html`
- For reports: `report-<slug>.html`
- For proposals: `proposal-<slug>.html`

Place it in the current working directory or a specified output directory.

### Step 4: Generate the PDF

Run the generation script:

```bash
python3 <skill_directory>/scripts/generate_pdf.py <input_html> -o <output_pdf>
```

Where `<skill_directory>` is the directory containing this SKILL.md file.

If the user specified an output path, use that. Otherwise default to the current working directory with a descriptive filename like `report-<slug>.pdf`.

### Step 5: Report Results

Tell the user:
- The output PDF path (absolute)
- Page count if available
- Any warnings about content that could not be rendered

## Supported Content Types

| Content Type | Key Elements | Template Sections Used |
|---|---|---|
| Architect Evaluation | Value Matrix, Opportunity Score, Risk Assessment | Cover, Summary, Scores, Matrix, Evaluators, Risk, Recommendations |
| Project Proposal | Problem, Solution, Timeline, Budget | Cover, Summary, Sections, Tables, Recommendations |
| Comparison Analysis | Options, Criteria, Scores | Cover, Summary, Comparison Tables, Scores |
| General Report | Sections, Findings, Conclusions | Cover, Summary, Sections, Recommendations |
| Meeting Notes | Agenda, Decisions, Action Items | Cover, Sections, Action Items |

## Requirements

- Python 3.8+
- WeasyPrint (`pip install weasyprint`)
- No other Python dependencies required

## Tips for Best Results

- Provide structured content with clear headings and sections
- Include numerical scores when possible for visual impact
- Specify a title if you want a custom cover page heading
- For Architect evaluations, the skill auto-detects the format from standard output

## Example Output

```
PDF generated: ./report-skills-evaluation.pdf
- Pages: 8
- Sections: Cover, Executive Summary, Value Matrix, Risk Assessment, Recommendations
- Score visualizations: Opportunity Score gauge (7.0/10), 6 sub-score bars
- File size: 245 KB
```

The PDF includes: professional cover page with title and date, table of contents, color-coded score tables, SVG bar charts for sub-scores, risk assessment with severity indicators, and numbered recommendations.

## Fallback Without WeasyPrint

If WeasyPrint is not installed, the skill generates a standalone HTML file instead. This HTML file:
- Can be opened in any browser
- Can be printed to PDF via Ctrl+P / Cmd+P
- Contains all the same styling and visualizations
- Is a valid intermediate output, not a degraded experience

## Error Handling

- **WeasyPrint not installed**: Fall back to HTML output (see above). Suggest `pip install weasyprint` for full PDF support.
- **Missing fonts**: WeasyPrint uses system fonts. If text renders incorrectly, specify a font family in the CSS or install the needed font.
- **SVG not rendering**: Ensure SVG elements use inline styles, not CSS classes. WeasyPrint has limited CSS support for SVG.
- **Large content overflows page**: The template uses CSS `page-break-inside: avoid` for tables and score blocks. If content still overflows, it splits across pages gracefully.
