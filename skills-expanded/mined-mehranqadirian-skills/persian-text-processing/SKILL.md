---
name: persian-text-processing
description: Cleans and normalizes Persian (Farsi) text. Use whenever the user works with Persian or Arabic-script text and needs consistent letters, digits or spacing, such as mixed ي and ی or ك and ک, Persian versus Western digits, missing half spaces (نیم‌فاصله) in می‌رود or کتاب‌ها, spacing around ، and ؟, tatweel, hidden bidi marks, search that misses names, or joining Persian data from different sources, even if they only say "my Persian text looks wrong". Reports problems first, never changes the original.
---

# persian-text-processing

Make Persian text consistent so it looks right, stores cleanly and matches reliably. The script uses only the standard library, so it also runs in Termux.

```
persian-text-processing/
├── SKILL.md
├── scripts/
│   └── normalize_fa.py        normalize, check, or build a search key
└── references/
    └── typography.md          look-alike characters, ZWNJ rules, digits, punctuation, data pitfalls
```

## When to use

- Text mixes Arabic and Persian letters or digits
- Half spaces are missing or typed as normal spaces
- Names or titles do not match across files, tables or databases
- Preparing Persian text for a document, a website, a search index or a CSV join
- Garbled Persian output (mojibake) or invisible direction marks

For right-to-left document layout, use `document-conversion`. For dates, use `persian-dates`. For tables of Persian data, profile first with `csv-profiling`.

## Workflow

1. **Diagnose without changing anything**: `python3 scripts/normalize_fa.py --check file.txt`. It counts each problem type.
2. **Choose the rules**: always on are yeh and kaf, tatweel, bidi marks, spaces, punctuation spacing. Options: `--digits en|fa`, `--strip-diacritics`, `--punct`, `--no-zwnj`. Decide digits by purpose (people read Persian digits, data uses Western digits).
3. **Normalize into a new output**: `python3 scripts/normalize_fa.py in.txt --digits fa > out.txt`. Keep the original.
4. **Check a sample by eye**, especially half spaces. Rules cannot know every word, so mention any pattern you were unsure about.
5. **For matching**, build a key and compare keys, not display text: `echo "کتاب‌ها ۱۲" | python3 scripts/normalize_fa.py --key` gives `کتاب ها 12`.
6. **Report** what changed, with counts from `--check` before and after.

## Rules

- Never overwrite the source text; write a new file or a new column
- Store Western digits in data; convert to Persian digits only for display
- Do not insert half spaces by guesswork beyond the documented patterns; offer `--no-zwnj` for risky text
- Do not change quoted text, code, URLs or file paths; normalize only prose
- When the user's text has meaning-bearing diacritics (poetry, religious text), do not strip them
- Check encoding first if letters look like `Ù…Ø±` (see the typography reference)

## Examples

```bash
printf 'او می رود و کتاب ها را می بیند ،خوب ؟' | python3 scripts/normalize_fa.py
python3 scripts/normalize_fa.py --digits en --strip-diacritics names.txt > names_clean.txt
python3 scripts/normalize_fa.py --check article.md
```

In Python:

```python
from normalize_fa import normalize, search_key
clean = normalize(text, digits="en")
key = search_key(name)          # use this for joins and lookups
```

## What to report back

| Field | Content |
|-------|---------|
| Problems found | counts per type from `--check` |
| Rules applied | digits mode, diacritics, ZWNJ, punctuation |
| Result | where the cleaned output is, and that the original is untouched |
| Uncertain spots | words where a half space or letter choice needs a human |

## Related skills

- `persian-dates`: Jalali and Gregorian date conversion
- `csv-profiling`: find Persian digits and mixed formats across a whole file
- `document-conversion`: right-to-left Word, HTML and PDF output
