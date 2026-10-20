# HtmlToWordBundle — Copilot / AI hints

- **Runtime**: PHP `>=8.2 <8.6`; Symfony components `^6.4 || ^7.0 || ^8.0`.
- **Style**: Follow `.php-cs-fixer.dist.php`, PHPStan level from `phpstan.neon`, Rector where applicable. Prefer strict types, explicit comparisons, small focused changes.
- **Bundle**: Root config key is `nowo_html_to_word` (see `Configuration::ALIAS`). DI tags remain `html_to_word.transformer` and `html_to_word.engine`.
- **Docs**: User-facing docs in English under `docs/`; README keeps the canonical “Documentation” section layout.
- **Tests**: PHPUnit under `tests/Unit` and `tests/Integration`; match existing patterns and avoid widening scope beyond the task.

## Commits

- Never add AI co-author trailers: no `Co-authored-by: Cursor` / `cursoragent@cursor.com`, no `Co-Authored-By: Claude …` / `noreply@anthropic.com` (REQ-GIT-001).
