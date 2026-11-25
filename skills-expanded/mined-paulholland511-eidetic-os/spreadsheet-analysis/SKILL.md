---
name: spreadsheet-analysis
description: Open a spreadsheet, compute summary statistics and trends, flag anomalies, and write a short findings note.
---

Read a spreadsheet (`.xlsx` or `.csv`), compute summary statistics and trends, flag anomalies, and write a concise findings note back into the vault.

> Placeholders: `{{EIDETIC_OS}}` = the Eidetic OS repo path, `{{DATA_FILE}}` = the spreadsheet to analyse (`.xlsx`/`.csv`), `{{VAULT_PATH}}` = your vault path. SMTP credentials come from `SMTP_APP_PASSWORD` / `SENDER_EMAIL` env vars — never inline them.

**Objective:** Load the data, profile every column, surface the headline trends and any anomalies, then save a scannable findings note (and optionally email it).

**Step 1 — Gather data:**

1. Request access to `{{DATA_FILE}}` and `{{VAULT_PATH}}`.
2. Load the spreadsheet:
   - For `.xlsx`, read with `openpyxl` (read every sheet; note which sheet you analysed)
   - For `.csv`, read with the stdlib `csv` module or `pandas` if available
   - Detect the header row, infer each column's type (numeric, date, categorical, text), and record the row/column counts
3. Profile each column:
   - Numeric → count, min, max, mean, median, standard deviation, and null count
   - Date → range (earliest/latest) and any gaps in the sequence
   - Categorical → distinct value count and the top values by frequency
4. Note any data-quality issues up front: missing headers, blank rows, mixed types in one column, duplicate rows.

**Step 2 — Build the analysis:**

1. **Summary statistics** — assemble the per-column profile from Step 1 into a compact table.
2. **Trends** — for any time-ordered numeric series, compute the period-over-period change and an overall direction (rising / flat / falling); call out the largest movers.
3. **Anomalies** — flag values more than 3 standard deviations from the column mean, sudden breaks in a trend line, negative values where only positives are expected, and outlier dates outside the main range.
4. **Findings** — write 3–5 plain-language takeaways: what the data shows, what changed, and what looks wrong or worth a closer look. Lead with the most important finding.

**Step 3 — Save the findings note:**

1. Write a markdown note to `{{VAULT_PATH}}/wiki/sources/spreadsheet-analysis-[YYYY-MM-DD].md` so the RAG pipeline indexes it. Include:
   - Source file name and the sheet/row/column counts analysed
   - The summary-statistics table
   - The trends section and the anomalies list
   - The plain-language findings, most important first
2. Index the new note so it is searchable:
   ```bash
   EIDETIC_TRIGGER=scheduled VAULT_PATH={{VAULT_PATH}} eidetic embed --incremental
   ```
3. (Optional) If a recipient is configured, email the findings summary:
   ```bash
   EIDETIC_TRIGGER=scheduled eidetic email --json '{"to":"$SENDER_EMAIL","subject":"📊 Spreadsheet Analysis — [date]","body_html":"..."}'
   ```

**Constraints:**
- Do NOT modify `{{DATA_FILE}}` — read only.
- If the file is missing, unreadable, or empty, write a short note saying so and stop — do not fabricate statistics.
- Keep the findings note scannable in under a minute.

Sign off as Eidetic.
