---
name: algo-naive-pattern-matching
description: "Brute-force O(n*m) sliding-window search for all overlapping matches of a pattern/motif/primer in text or DNA/protein strings, pure Python. Use for one-off exact search, or to benchmark the naive baseline before KMP/Rabin-Karp/Boyer-Moore."
tool_type: python
primary_tool: Python
---

# Naive Pattern Matching

## When to Use

- A quick, one-off exact substring search where preprocessing (building a prefix table, hash, or automaton) isn't worth it.
- Locating a short motif, primer, restriction site, or adapter in a DNA/protein string when the pattern is small relative to the text.
- Teaching/benchmarking context: establishing the O(n*m) baseline before introducing KMP, Rabin-Karp, or Boyer-Moore.
- Diagnosing *why* a hand-rolled substring scan is slow — e.g. it degrades toward O(n*m) on low-entropy text (poly-A runs, "AAAA...B"-style inputs, repetitive DNA).

## Version Compatibility

Pure Python standard library only — no third-party dependencies. Works unchanged on Python >= 3.8; the `list[int]` return-type hint needs Python >= 3.9 or `from __future__ import annotations` on 3.8.

## Prerequisites

- Comfortable with Python strings/lists and basic O-notation.
- No packages to install.
- Helpful next steps: `algo-kmp-algorithm` (linear-time exact match), `algo-rabin-karp` (rolling-hash alternative), `algo-complexity-analysis` (amortized analysis).

## Algorithm

Slide the pattern over the text one position at a time; at each position compare character by character until a mismatch or a full match.

**Goal:** find every start index where `pattern` occurs in `text`, including overlapping occurrences, with no preprocessing.
**Approach:** for each candidate start `i` in `range(n - m + 1)`, compare `text[i+j]` to `pattern[j]` for `j = 0..m-1`; stop at the first mismatch (short-circuit) and record `i` on a full match. Never skip ahead on mismatch — that's exactly what KMP/Boyer-Moore improve on.

```python
def naive_search(text: str, pattern: str) -> list[int]:
    """Find all (possibly overlapping) start indices of `pattern` in `text`.

    Time:  O(n) best/average case (mismatches found quickly), O(n * m) worst
           case (many partial matches, e.g. text="AAAA...AAB", pattern="AAAB").
    Space: O(1) auxiliary (O(k) for the result list with k matches).
    """
    n, m = len(text), len(pattern)
    positions: list[int] = []

    if m == 0:
        return list(range(n + 1))  # empty pattern matches everywhere
    if m > n:
        return []

    for i in range(n - m + 1):
        match = True
        for j in range(m):
            if text[i + j] != pattern[j]:
                match = False
                break  # short-circuit: this is what makes best-case O(n)
        if match:
            positions.append(i)
    return positions


def count_comparisons(text: str, pattern: str) -> int:
    """Count total character comparisons naive_search would perform.

    Useful for demonstrating best- vs worst-case behavior, e.g. on
    low-entropy DNA text: count_comparisons("AAAAAAAAAB", "AAAAB") is
    close to n * m, while a random/high-alphabet text is close to n.
    """
    n, m = len(text), len(pattern)
    total = 0
    for i in range(n - m + 1):
        for j in range(m):
            total += 1
            if text[i + j] != pattern[j]:
                break
    return total
```

Apply it directly to a DNA/protein sequence — the algorithm is alphabet-agnostic:

```python
def find_motif(sequence: str, motif: str, case_sensitive: bool = False) -> list[int]:
    """Find all start positions of `motif` (e.g. a primer or restriction
    site) in a DNA/protein `sequence` using naive search.
    """
    if not case_sensitive:
        sequence, motif = sequence.upper(), motif.upper()
    return naive_search(sequence, motif)
```

Example: `find_motif("ATGCGATCGATCGATAAG", "GATC")` returns `[4, 8]` — overlapping matches are kept.

## Complexity

| Case | Time | When |
|---|---|---|
| Best | O(n) | First character mismatches quickly (large alphabet, low repetition) |
| Worst | O(n * m) | Many partial matches, e.g. `text="AAAA...AAB"`, `pattern="AAAB"` |
| Average | O(n) for large alphabets | Random text, mismatches found in ~1-2 comparisons per position |
| Space | O(1) auxiliary | O(k) for storing k match positions |

## When Naive Is Fine

- **Small patterns:** `m` is small relative to `n` (e.g. a short primer in a document), so `O(n*m) ~ O(n)`.
- **Large alphabet:** more distinct characters means mismatches are found within the first 1-2 comparisons on average.
- **One-off search:** no preprocessing to amortize (contrast with KMP's O(m) prefix table or Boyer-Moore's shift tables).
- **Few expected occurrences:** if the pattern rarely matches, most attempts fail on the first character.

## Why It's Inefficient (and What Fixes It)

After a partial match fails, naive search discards everything it learned and restarts from scratch at the next position — it never uses the fact that, say, `text[i+1:i+5]` was already confirmed to equal `pattern[0:4]`.

| Algorithm | Time | Key Idea |
|---|---|---|
| KMP | O(n + m) | Prefix/failure function skips already-verified characters after a mismatch |
| Rabin-Karp | O(n + m) avg | Rolling hash gives O(1) amortized window comparison |
| Boyer-Moore | O(n/m) best | Bad-character/good-suffix rules skip large chunks of text |

## Pitfalls

- Finds overlapping matches by default (e.g. `naive_search("ABABABA", "ABA")` -> `[0, 2, 4]`) — this is correct, expected behavior, not a bug to "fix".
- Python's built-in `str.find()` / `in` use a highly optimized mix of Boyer-Moore-Horspool internally and will outperform a hand-written naive loop — don't hand-roll this for production code; use it only when you need custom match logic (e.g. mismatch tolerance) or are teaching the baseline.
- Worst case is triggered by low-entropy text — small alphabets like DNA's "ACGT" or poly-A/poly-T runs cause far more partial matches than English text or protein's 20-letter alphabet.
- `m > n` and `m == 0` are easy to mishandle — always short-circuit both before the main loop (empty pattern conventionally matches at every position, including `n`).

## See Also

- `algo-kmp-algorithm` — O(n + m) exact match via prefix function; the algorithm this baseline motivates.
- `algo-rabin-karp` — rolling-hash alternative, good for multiple-pattern search.
- `algo-dfa-matching` — precomputed state machine, O(n) search with zero backtracking.
- `algo-aho-corasick` — searches many patterns simultaneously in one linear pass.
