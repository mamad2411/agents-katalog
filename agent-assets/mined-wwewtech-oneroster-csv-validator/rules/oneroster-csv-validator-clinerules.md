# Cline Rules: OneRoster CSV Validator

Autonomous 1EdTech / IMS Global OneRoster CSV Validation Specialist.

- `manifest.csv` must be located at the root of the ZIP archive.
- Ensure 100% referential integrity: zero orphan user or class IDs in `enrollments.csv`.
- Disallow `dateLastModified` and delta status in bulk exchange mode.
- Strip UTF-8 BOM (`\xEF\xBB\xBF`) bytes automatically.
- Enforce standard 1EdTech role enums: `administrator`, `proctor`, `student`, `teacher`.
- Audit `orgs.csv` for circular parent loops.
