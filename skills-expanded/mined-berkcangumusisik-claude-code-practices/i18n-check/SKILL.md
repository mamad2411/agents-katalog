---
name: i18n-check
description: Finds hardcoded strings that should be internationalized and generates translation keys
argument-hint: [file-or-directory]
user-invocable: true
allowed-tools: Read Grep Glob Edit
effort: medium
---

## Internationalization Check

Target: **$1** (or `src/` if not specified)

1. Detect i18n library:
```bash
cat package.json | grep -E '"i18next"|"react-intl"|"vue-i18n"|"@angular/localize"|"next-intl"'
ls src/locales/ src/i18n/ public/locales/ 2>/dev/null | head -10
```

2. Find hardcoded user-visible strings (not variable names, not URLs):
```bash
grep -rn '"[A-Z][a-z ]\+"\|'"'"'[A-Z][a-z ]\+'"'" ${1:-src/} --include="*.tsx" --include="*.jsx" --include="*.vue" | grep -v "className\|import\|export\|test\|spec" | head -30
```

3. For each hardcoded string:
   - Is it user-visible? (skip internal error codes, class names)
   - Generate a translation key: `page.section.description`
   - Show the replacement code using the project's i18n function

4. Update the locale file (`en.json` or equivalent) with new keys.

5. Replace hardcoded strings in source with i18n function calls.

6. Report: N strings found, N replaced, N skipped (non-user-visible).
