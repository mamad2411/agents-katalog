# Buddhist Contributions Hub - Project Rules

## 1. Architectural Philosophy
- **Separation of Concerns:** - `Inbox/` is the **Permanent Archive** (Read-Only for scripts).
  - `Buddhist_Hub/` is the **Generated Product** (Write-Target).
  - Never modify files in `Inbox/` during processing.
- **Obsidian Compatibility:**
  - All Markdown links must be **WikiLinks** (`[[DN1.1]]`).
  - Images must be stored in a local `attachments/` subfolder relative to the Markdown file.
  - Frontmatter must include `sutta_citations` list for Dataview querying.

## 2. Naming Conventions
- **Books (Inbox):** `Author - Title.pdf` (e.g., `Ajahn Chah - Food for the Heart.pdf`).
- **Essays (Inbox):** `Author - Topic.md` (e.g., `John Doe - Jhana Analysis.md`).
- **Folders (Library):** `Buddhist_Hub/Library/Books/{Author}/{Title}/`.
- **Assets:** Images must be renamed to avoid collisions (e.g., `BookTitle_Fig1.jpg`).

## 3. Security Protocols (The Gatekeeper)
- **Validation:** All PRs must pass `scripts/gatekeeper.py`.
- **Criteria:**
  - File must contain >5 valid Sutta citations (e.g., `DN 1.1`, `MN 10`).
  - No HTML/Script tags in Markdown files.
  - Valid Magic Numbers (PDF/EPUB headers).

## 4. Automation Workflow
- **Pull Request:** Runs `Gatekeeper` (Read-Only check).
- **Merge/Push:** Runs `Librarian` (Process & Generate).
- **Release:** Zips `Buddhist_Hub/` into `Library.zip`, `Contributions.zip`, and `Full.zip`.

## 5. Coding Standards
- **Python:** Use `pathlib` for all file paths (Cross-platform safety).
- **Dependencies:** Keep `requirements.txt` minimal (`pymupdf`, `pyyaml`).