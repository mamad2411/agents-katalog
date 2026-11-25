# Report Creator — Multi-Format Report Generator
## Triggers: create report, generate report, build report, audit report, weekly report, monthly report, client report

## FORMATS SUPPORTED
- PDF: reportlab-pdf-master skill → branded 11-page audits
- XLSX: openpyxl → data tables, charts, KPI dashboards
- DOCX: python-docx → client proposals, SOPs
- HTML: jinja2 → email-ready, browser reports

## AUTO-ROUTING
"pdf report" → reportlab-pdf-master
"excel report" / "xlsx" → openpyxl pipeline
"word report" / "docx" → python-docx pipeline
"html report" → jinja2 template

## OUTPUT: always ~/Downloads/
## BRAND: extract palette from client URL automatically
