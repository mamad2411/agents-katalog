---
name: Process Compliance First-Pass
description: Review a document against required elements in SharePoint before formal review and flag missing or unclear items.
---

1. Identify the document type using:
   - document metadata (preferred)
   - or document title and content if metadata is missing

2. Retrieve the corresponding checklist from the site’s Compliance Requirements list or configured reference source.

3. Review the document against each required element in the checklist.

4. For each required element, classify as:
   - Present (clearly included and complete)
   - Absent (missing entirely)
   - Unclear (partially present or insufficient detail)

5. Capture supporting context where relevant:
   - brief excerpt or explanation of why the classification was assigned

6. If the checklist or document type cannot be determined, state this clearly and stop.

7. Output results as a structured report:
   - Document Type
   - Summary Status: Pass / Flag / Needs Review
   - Table of findings:
     Element | Status | Notes

8. Highlight:
   - missing required elements
   - unclear or ambiguous sections

9. Do not modify, rewrite, or update the document. Output findings only.