---
name: add-entity-pattern
description: Add a new regex entity type to the extraction pipeline (e.g. a new IOC like MAC addresses, monero wallets, JA3 hashes). Walks every file that must change in sync — PatternLabel enum, REGEX_PATTERNS, README table, unit tests, optional smoke-test coverage. Use whenever the user asks to extract/detect/match a new kind of entity or pattern.
---

# add-entity-pattern — new regex entity, end to end

The single most common feature change in this repo. It looks like a one-liner but
touches five places that must stay in sync; missing any of them is a review bounce.

## Step 1 — Design the pattern

Write the regex and test it against realistic text **before** touching any file:

```bash
python -c "
import re
pat = r'YOUR_PATTERN_HERE'
good = ['should match 1', 'should match 2']
bad  = ['should NOT match', 'near-miss variant']
for t in good: assert re.findall(pat, t, re.IGNORECASE), f'missed: {t}'
for t in bad:  assert not re.findall(pat, t, re.IGNORECASE), f'false positive: {t}'
print('pattern OK')
"
```

Constraints on the pattern itself:

- It runs through `re.findall(pattern, text)` in `extract_regex_entities` (no flags) and
  `re.findall(pattern, text, re.IGNORECASE)` in `KeywordPatternRegistry.extract_all` —
  so make case-sensitivity explicit in the pattern (e.g. `[0-9a-fA-F]`) rather than
  relying on flags, like every existing pattern does.
- **Avoid capture groups.** `re.findall` returns only the captured group when one
  exists. The single existing exception is `PORT_NUMBER` (returns `"4444"`, not
  `"port 4444"`) and the tuple-handling code in `extract_regex_entities` exists solely
  because of it. Use non-capturing `(?:...)` groups.
- `\b` never matches adjacent to non-word characters — a pattern like `\b\.exe\b` works
  because it *ends* on a word char, but `\bC\+\+\b` can never match (commit `c3fef9b`).
  Check boundary behavior for any pattern containing `.`, `+`, `$`, `@`, `%`.
- Watch overlap with existing patterns: 64-hex-char strings already match `HASH_SHA256`,
  32 match `HASH_MD5`; `.onion` hosts match both `DOMAIN` and `DARK_WEB` (that overlap
  is accepted precedent). New overlaps are fine if deliberate — note them in the PR.

## Step 2 — `src/insight_extractor/config.py`

Add the member to `PatternLabel` (StrEnum, `@final`), UPPER_SNAKE name = value string,
in the same position relative to the others as you'll use in `constants.py`:

```python
MAC_ADDRESS = "MAC_ADDRESS"
```

## Step 3 — `src/insight_extractor/constants.py`

Add to `REGEX_PATTERNS`, keyed by the enum member, as a raw string:

```python
PatternLabel.MAC_ADDRESS: r"\b(?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}\b",
```

Order in the dict controls output-section order in the console/Markdown report — put it
near related patterns. Keep the line ≤100 chars (ruff E501).

## Step 4 — Unit tests

Add to `tests/unit/test_extractor.py` (or the pattern-focused test module), following
house style — plain functions, `from __future__ import annotations`, no model needed
(regex extraction is model-free):

```python
def test_regex_extracts_mac_address(tmp_path: Path) -> None:
    extractor = InsightExtractor(seed_keywords=["ransomware"], output_dir=tmp_path)
    text = "Beacon from 00:1A:2B:3C:4D:5E was observed; not-a-mac 00:1A:2B."

    result = extractor.extract_regex_entities(text)

    assert result["MAC_ADDRESS"] == ["00:1A:2B:3C:4D:5E"]
```

Required cases (quality bar):
- [ ] positive match (exact expected string, not just truthiness)
- [ ] negative / near-miss (proves the pattern isn't greedy)
- [ ] dedup behavior if duplicates are plausible (extraction dedups, preserving order)

Note: `StrEnum` means `result["MAC_ADDRESS"]` works with a plain-string key — don't use
the enum member in assertions; existing tests use plain strings.

## Step 5 — `README.md`

Add a row to the **"Regex Patterns — What Gets Extracted"** table (label, what it
matches, realistic example). The README is the user contract; a pattern absent from the
table doesn't exist as far as users know.

## Step 6 — Smoke test coverage (optional but preferred for IOC-class patterns)

If the entity is core threat-intel (hash, address, identifier), extend the CI smoke test
in `.github/workflows/ci.yml`: add one realistic line to the generated
`/tmp/smoke_input.txt` heredoc. Only add an *assertion* for it if it should gate CI.
Editing `ci.yml` gates/triggers themselves requires asking the owner first (CLAUDE.md
§6) — appending a line to the synthetic input plus at most one assert is within normal
scope; anything more, ask.

## Step 7 — Things you do NOT need to touch

- `models.py` — `regex_entities` is `dict[str, list[str]]`, shape-agnostic.
- `extractor.py` / `stemmer.py` — iteration over `REGEX_PATTERNS` picks the new entry up.
- `__init__.py` — `PatternLabel` and `REGEX_PATTERNS` are already exported.
- Keyword seeds (`THREAD_SEEDS`) — those feed the *dynamic* pipeline, unrelated to
  static patterns. (Adding a keyword is a different, smaller task: append to
  `THREAD_SEEDS`, and if it needs a category, check the term-bucket sets at the top of
  `extractor.py` — no leading/trailing spaces in set members; a stray space made
  `" deception"` unmatchable once, commit `40e81fe`.)

## Step 8 — Preflight

Run the `preflight` skill (all four gates + staging hygiene). The full checklist for
this deliverable:

- [ ] pattern verified against good/bad samples in Step 1
- [ ] `PatternLabel` member added
- [ ] `REGEX_PATTERNS` entry added (non-capturing groups, ≤100 chars)
- [ ] unit tests: positive + negative (+ dedup where plausible)
- [ ] README table row added
- [ ] smoke input line added if IOC-class
- [ ] `ruff check` / `ruff format --check` / `mypy` / `pytest tests/unit/` all green
- [ ] commit: `feat: add <LABEL> regex entity pattern` with root-cause-style body
