# report-generator

Report Generator mit Multi-Format Export Support

**Category:** reporting — Report Generation

## Overview

Report Generator mit Multi-Format Export Support

Unterstützte Formate:
- JSON: Vollständige Scan-Ergebnisse
- PDF: Professioneller Report mit Logo, Executive Summary (reportlab)
- HTML: Interaktiver Report für Browser (jinja2)
- XML: Für Integration mit anderen Tools

Usage:
    from modules.report_generator import ReportExportGenerator

    generator = ReportExportGenerator()

    # JSON Export
    json_data = generator.export_json(scan_id=123, findings=[...])

    # PDF Export
    pdf_bytes =

## Usage



## Agent Integration

- Agent persona: auto-selected from category 'reporting'
- MCP:
- API:  with {"tool_name": "report_generator", "target": "example.com"}
