---
name: generate-vault-report-doc
description: Document creation — compile a set of vault notes on a topic into a polished, formatted Word (.docx) or PDF report.
---

You are Eidetic. Compile the relevant notes from the vault on a given topic into a single polished, formatted Word (.docx) or PDF report and save it to the output directory.

> Placeholders: `{{VAULT_PATH}}` = your vault path, `{{EIDETIC_OS}}` = the Eidetic OS repo path, `{{OUTPUT_DIR}}` = where the finished report is written, `{{REPORT_TOPIC}}` = the subject to compile (e.g. "Q2 infrastructure review"). The embeddings endpoint and any SMTP credentials come from env vars (`EMBED_HOST`/`EMBED_PORT`, `SMTP_APP_PASSWORD`/`SENDER_EMAIL`) — never inline them.

**Objective:** Turn scattered notes about `{{REPORT_TOPIC}}` into one clean, shareable document. Read-only on the vault — never modify source notes.

**Step 1 — Gather the source material:**

1. Request access to `{{VAULT_PATH}}`.
2. Find the notes relevant to `{{REPORT_TOPIC}}`:
   - Make sure the RAG index is current first by running `EIDETIC_TRIGGER=scheduled eidetic embed --incremental` (routes through the CLI so the run is audited).
   - Semantic search: embed the query `{{REPORT_TOPIC}}` against the vector store using the endpoint at `http://{{EMBED_HOST}}:{{EMBED_PORT}}/v1/embeddings` (model from `EMBED_MODEL`), then rank the chunks in `$RAG_DIR/vectors.json` (default `{{VAULT_PATH}}/.rag/vectors.json`) by cosine similarity and keep the top 15–20.
   - Cross-check with a filename/heading grep over `{{VAULT_PATH}}/**/*.md` (exclude `.git`, `.rag`, `.claude`, `.obsidian`) so you don't miss notes the embeddings ranked low.
3. Read the full text of each matched note. De-duplicate overlapping content and note the source filename for each fact so the report can be traced back.

**Step 2 — Build the report document:**

1. Decide the structure from the gathered material — typically: title page (`{{REPORT_TOPIC}}`, date, "Compiled by Eidetic"), executive summary, one section per sub-theme, key findings / action items, and a "Sources" appendix listing the vault notes used.
2. Synthesise — summarise and connect the notes into prose; do not paste raw note bodies. Resolve contradictions between notes and flag anything stale.
3. Render the deliverable with the `docx` skill (for `.docx`) or the `pdf` skill (for `.pdf`): headings, a table of contents, page numbers, and tables where data is tabular. Apply a clean, consistent style.
4. Save to the output directory with a dated, slugified name:
   - `.docx` → `{{OUTPUT_DIR}}/<report-topic-slug>-[YYYY-MM-DD].docx`
   - `.pdf`  → `{{OUTPUT_DIR}}/<report-topic-slug>-[YYYY-MM-DD].pdf`
   - Create `{{OUTPUT_DIR}}` if it does not exist.

**Step 3 — Deliver and record:**

1. Verify the file was written and is non-empty; report its path, format, page count, and which vault notes fed into it.
2. (Optional) If the report is meant to be shared, email it as an attachment:
   ```bash
   EIDETIC_TRIGGER=scheduled eidetic email --json '{"to":"<recipient>","subject":"Report — {{REPORT_TOPIC}}","body_html":"...","attachments":["{{OUTPUT_DIR}}/<report-topic-slug>-[YYYY-MM-DD].docx"]}'
   ```
   Credentials come from `SMTP_APP_PASSWORD` / `SENDER_EMAIL`.

**Constraints:**
- Read-only on `{{VAULT_PATH}}` — never edit or delete source notes.
- Write only inside `{{OUTPUT_DIR}}`.
- If no notes match `{{REPORT_TOPIC}}`, write nothing and report that the vault has no coverage of the topic.

Sign off as Eidetic.
