# ReportLab PDF Master — Branded Audit PDF Generator
## Triggers: pdf report, audit pdf, reportlab, generate pdf, create pdf, 11-page, branded pdf

## HARD LAWS (never break these)
1. Always import: from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
2. Always use: from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
3. Colors: HexColor('#XXXXXX') — never rgb()
4. Page size: A4 or letter — never custom unless specified
5. Fonts: registerFont before use — Helvetica always available as fallback
6. Tables: col widths must sum to page_width - left_margin - right_margin
7. Images: check file exists before ImageReader — never assume path valid
8. Styles: always deepcopy base style before modifying
9. No bare except — always catch specific exceptions
10. Test render before delivery — open file, check page count
11. Brand palette: fetch from client URL using colorthief/requests
12. Output: always ~/Downloads/ — never Desktop

## QUICK START
```python
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor

doc = SimpleDocTemplate("~/Downloads/audit.pdf", pagesize=A4,
    leftMargin=2*cm, rightMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
styles = getSampleStyleSheet()
story = []
# Add content → doc.build(story)
```
