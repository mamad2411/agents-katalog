## AI contribution guidelines (Nowo Symfony bundle)

Use this when suggesting code, tests, documentation, or CI changes for this repository.

### Scope

- This is a **Symfony bundle** for **Spanish Veri\*Factu / AEAT** compliance (`nowo-tech/verifactu-bundle` on Packagist).
- Respect **PHP** and **Symfony** ranges in `composer.json` (including demo apps under `demo/`).
- Prefer **PHP 8 attributes**; do not add `doctrine/annotations` for new metadata.

### Git commits (REQ-GIT-001)

- **Never** add `Co-authored-by: Cursor <cursoragent@cursor.com>` (or any `cursoragent@cursor.com`) to commit messages.
- Never add `Co-Authored-By: Claude …` / `noreply@anthropic.com` trailers either (REQ-GIT-001).
- Human authors only in `git log`. Attribute tooling in PR descriptions or changelogs if needed.
- After clone: `make setup-hooks`. Before push/release: `make check-no-cursor-coauthor`.

### Code

- Follow **PSR-12** and project tooling (`composer cs-check`, `composer phpstan`, `composer test`).
- Hash chain, XML, XAdES, and AEAT SOAP paths must remain **explicit and auditable**; avoid silent failure paths.
- Never commit real certificates, passwords, or production AEAT credentials; use sandbox / env vars only.
- Coordinate changes across **root bundle** and **demo** `composer.json` files when dependencies shift.

### Documentation

- User-facing documentation in **English** under `docs/`.
- Never embed real NIFs used in production, certificate paths with secrets, or live AEAT credentials in examples; use AEAT test data only.

### Tests

- Add or update tests for validation, hash chain, SOAP timeout, and signing edge cases; maintain **100%** PHP line coverage (REQ-TEST-003).
