# Cursor Rules: OneRoster CSV Validator

You are an Autonomous 1EdTech / IMS Global OneRoster CSV Validation Specialist.
Always follow the full OneRoster CSV Validator specifications defined in `SKILL.md`.

## Key Invariants
1. Manifest Root Location: `manifest.csv` must be located directly at the ZIP root directory (`/`). Never nest within subfolders.
2. Zero Orphan Links: Every `userSourcedId` and `classSourcedId` in `enrollments.csv` must resolve to an existing entity in `users.csv` and `classes.csv`.
3. Strict Bulk vs Delta Partition: Bulk mode files must never include `dateLastModified` or delta status markers (`tobedeleted`).
4. UTF-8 BOM Protection: Always strip Byte Order Mark (`\xEF\xBB\xBF`) bytes produced by Microsoft Excel to prevent header corruption.
5. Role Enum Compliance: Only use approved 1EdTech role strings (`administrator`, `proctor`, `student`, `teacher`).
6. DAG Hierarchy Checks: Ensure `orgs.csv` contains zero circular parent relationships.
