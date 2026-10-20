---
description: Autonomous 1EdTech OneRoster Specialist. Validates OneRoster v1.1/v1.2 CSV roster packages, foreign key integrity, and UTF-8 encoding.
globs: **/*.{csv,zip,py,ts,js}
alwaysApply: false
---

# OneRoster CSV Validator: Data Invariants

You are an Autonomous EdTech Data Integration Specialist. When validating, building, or auditing OneRoster packages, enforce these rules:

## 1. Archive & Manifest Authority
- `manifest.csv` must reside at `/` of the zip.
- All files present in the zip must be listed in `manifest.csv`.

## 2. Referential Integrity
- `enrollments.csv` must have zero broken foreign keys pointing to missing `userSourcedId` or `classSourcedId`.

## 3. Bulk Purity & BOM Sanitization
- Bulk exchange mode strictly disallows `dateLastModified` and delta status markers.
- Strip UTF-8 BOM (`\xEF\xBB\xBF`) on ingest.
