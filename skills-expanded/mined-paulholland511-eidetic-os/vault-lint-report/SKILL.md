---
name: vault-lint-report
description: Vault health check — finds orphan notes, dead wikilinks, stale claims, and frontmatter gaps, then writes a lint report note.
---

Lint the entire markdown vault for structural rot — orphan notes, dead wikilinks,
stale dated claims, and missing frontmatter — and write or update a single lint
report note that the RAG pipeline can index.

> Placeholders: `{{VAULT_PATH}}` = your vault path (the `VAULT_PATH` env var),
> `{{EIDETIC_OS}}` = the Eidetic OS repo path. All credentials (SMTP, embeddings
> endpoint) come from environment variables — never inline a secret into this
> skill or any note it writes.

**Objective:** Produce an actionable, deterministic health report of the vault so
problems get caught before they compound. This runs UNATTENDED — make no
destructive edits, only write the report note.

**Step 1 — Gather the vault state.** Request access to `{{VAULT_PATH}}` and
enumerate every linted note:

- List all `.md` files under `{{VAULT_PATH}}`, excluding `.git/`, `.rag/`,
  `.claude/`, `.obsidian/`, and `node_modules/`.
- Read `wiki/index.md` and `wiki/log.md` to know which notes are expected to be
  linked.
- For each note, parse the YAML frontmatter and the body wikilinks
  (`[[target]]` / `[[target|alias]]`). Build an in-memory map of
  note → outbound links and note → inbound links.

**Step 2 — Build the lint findings.** Run each check and collect concrete file
paths for every issue (never summarise away the specifics):

- **Orphan notes** — notes with zero inbound wikilinks and no entry in
  `wiki/index.md`. List each as `[[note]]`.
- **Dead wikilinks** — any `[[target]]` whose target file does not exist in the
  vault. Report the source note and the broken target.
- **Stale claims** — scan note bodies for dated assertions (e.g. "as of <date>",
  "current", "latest", explicit `YYYY-MM-DD` lines) older than 180 days, and
  frontmatter `updated:` / `date:` fields past that window. Flag them as
  candidates for review.
- **Frontmatter gaps** — notes missing required keys. Validate against the repo
  schema if present:
  ```bash
  VAULT_PATH={{VAULT_PATH}} python3 {{EIDETIC_OS}}/schemas/enforce_schemas.py --check --json
  ```
  Use the script's JSON output when available; otherwise fall back to checking
  for `title`, `tags`, and `updated`.
- Tally totals per category and compute a simple health score
  (clean notes ÷ total notes, as a percentage).

**Step 3 — Save the lint report note.** Write or overwrite a single report at
`{{VAULT_PATH}}/wiki/sources/vault-lint-report.md` so it stays a stable,
re-runnable artifact:

- Frontmatter: `title`, `tags: [vault, lint, health]`, and `updated: <today>`.
- A scannable summary line: health score, total notes, and a count per issue
  category.
- One section per check (Orphans, Dead Wikilinks, Stale Claims, Frontmatter
  Gaps), each listing the affected notes as wikilinks with the specific problem
  inline. If a category is clean, state "None found".
- A "Run metadata" footer with the timestamp and total files scanned.
- Do NOT edit any other note — only this report file.
- Re-embed the updated report so it is searchable:
  ```bash
  EIDETIC_TRIGGER=scheduled VAULT_PATH={{VAULT_PATH}} eidetic embed --incremental
  ```
  (The embeddings endpoint host/port and model are read from env vars; skip
  embedding gracefully if the endpoint is unreachable rather than failing.)

**Constraints:**
- Read-only against the vault except for the single report note.
- Deterministic output — the same vault state should produce the same report.
- Never inline credentials; rely on environment variables for every endpoint.
- Be thorough on specifics, concise on prose. Make the report skimmable in 30
  seconds with full detail available below the fold.

Sign off as Eidetic.
