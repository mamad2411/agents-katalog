Add one or more translation keys to ALL locale files. $ARGUMENTS is `<key> ["English value"]` (e.g. `settings.save "Save"`).

Keys often get added to `en.json` only and then silently fall back to English in every other locale – this skill keeps them all in sync.

## Steps

1. **Locate the locale files**: `src/i18n/locales/*.json`.
2. **Add to `en.json` first** with the provided English value, nested at the right path. Match the file's key ordering and indentation.
3. **Translate into every other locale file.** Write a proper translation per language, matching the tone and formality of the neighbouring keys in each file. Never copy the English value into a non-English file unless the term is genuinely untranslated in that language (brand names, "OK").
4. **Validate**: every touched file must pass `JSON.parse` (run a node loop over them).
5. **Check usage**: if the key replaces a hardcoded string in a component, update the component(s) to use `t('<key>')`.
6. Report: key(s) added, the number of locale files updated, and the translation used for 2-3 spot-check languages.
