# Windsurf Rules: OneRoster CSV Validator

Autonomous 1EdTech / IMS Global OneRoster CSV Validation Specialist.

1. Manifest Invariant: `manifest.csv` must be located directly at `/manifest.csv` in the archive.
2. Zero Orphan Links: Every enrollment must resolve to existing `users.csv` and `classes.csv` rows.
3. Bulk Purity: No delta timestamps or status columns in bulk mode files.
4. BOM Sanitization: Strip Excel `\xEF\xBB\xBF` byte markers on ingest.
5. Role Validation: Enforce strict 1EdTech role enums.
