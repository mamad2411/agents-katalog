---
name: poe2arb-workflow
description: Handle Flutter localization workflows backed by POEditor and poe2arb. Use when adding, changing, or removing translations, syncing ARB files with POEditor, or when the user mentions poe2arb, POEditor, upload, seed, or flutter gen-l10n.
---

# POEditor and poe2arb Workflow

Keep the localization workflow aligned with the shared localization rules.

## What to keep true

- Keep translations in package-specific `app_<language_code>.arb` files.
- Never hardcode translations.
- Use translations only in the presentation layer, inside widgets.
- Access translations as `final s = l10n(context);`
- If other layers need localized text, map message models to localized values in the presentation layer.

## Commands

All commands read the same configuration (`l10n.yaml`, `POEDITOR_TOKEN`, flags) and run from the package directory that holds `l10n.yaml`.

- `poe2arb poe` downloads translations from POEditor into the local ARB files. A read-only token is enough.
- `poe2arb upload` pushes local ARB changes to POEditor: adds new terms, overwrites existing translations and term definitions, and adds missing languages. It needs a token with write access and poe2arb 2.6.0 or newer.
- `poe2arb seed` is only for setting up a fresh POEditor project from existing ARB files. Do not use it to sync ongoing changes; use `upload`.

`upload` is destructive: POEditor ends up matching the local ARBs, so any translation edited in POEditor but not pulled locally is overwritten. With `--force` it also permanently deletes terms that exist in POEditor but not in the template ARB. Term deletion is scoped to `poeditor-term-prefix`, so packages sharing one POEditor project under a different prefix are unaffected.

## Workflow when changing translations

1. Check that `poe2arb version` is 2.6.0 or newer. If it is older, ask the user to upgrade poe2arb before syncing.
2. Run `poe2arb poe` before editing the ARB files, so they hold the latest translations from POEditor and the upload does not overwrite translators' work.
3. Add, change, or remove the translation in all relevant `app_<language_code>.arb` files.
4. Run `flutter gen-l10n`.
5. Run `poe2arb upload --dry-run` and show the user the summary: terms to add and remove, per-language added/updated/unchanged counts, and languages that would be created. Check that it matches the intended change; unexpected updates usually mean the ARBs were not pulled first.
6. Run `poe2arb upload`.
   - If it aborts because terms exist in POEditor but not locally, show the listed terms to the user. Re-run with `--force` only after the user explicitly confirms those terms should be deleted from POEditor; otherwise restore the missing terms locally or stop.

## Output expectations

- If asked to change translations, update the ARB files first.
- Clearly say which of `poe2arb poe`, `flutter gen-l10n`, `poe2arb upload --dry-run`, and `poe2arb upload` were run or still need to be run.
- Never pass `--force` without the user's explicit confirmation of the listed deletions, because deleted terms take all their translations with them.
