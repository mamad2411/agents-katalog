---
name: algo-kmp-algorithm
description: "Find all overlapping exact occurrences of a pattern/motif/primer in a string or DNA sequence in O(n+m) time via KMP's prefix/failure-function. Use for exact substring search, motif/primer location, or a slow naive O(n*m) scan."
tool_type: python
primary_tool: Python
---

# Knuth-Morris-Pratt (KMP) Algorithm

## When to Use

- Finding all occurrences (including overlapping ones) of a short pattern in a long text/sequence in linear time.
- Locating a motif, primer, adapter, or restriction site inside a DNA/protein string without allowing mismatches.
- Any place a naive `O(n*m)` substring scan is a bottleneck (large genome/text, many matches).
- Building blocks for multi-pattern search (see Aho-Corasick) or as a subroutine in string algorithms courses/interviews.

## Version Compatibility

Pure Python standard library only — no third-party dependencies. Works unchanged on Python >= 3.8 (uses only `list`/`str` built-ins; type hints like `list[int]` need Python >= 3.9 or `from __future__ import annotations`).

## Prerequisites

- Comfortable with Python strings/lists and O-notation.
- No packages to install.
- Helpful prior context: `algo-naive-pattern-matching` (the baseline this improves on), `algo-complexity-analysis` (amortized analysis).

## Key Insight

After a partial match fails, the prefix function tells us how far to shift the pattern without re-comparing characters we already know match. The text pointer `i` never moves backward — only the pattern pointer `j` falls back.

## Prefix Function (Failure Function)

`pi[i]` = length of the longest proper prefix of `P[0..i]` that is also a suffix of `P[0..i]`.

Example: Pattern `"ABABACA"` -> `pi = [0, 0, 1, 2, 3, 0, 1]`

**Goal:** build the prefix table in O(n) so KMP search never re-scans matched characters.
**Approach:** track `j`, the length of the current longest prefix-suffix match; on a mismatch, fall back using previously computed `pi` values instead of restarting from 0.

```python
def build_prefix(pattern: str) -> list[int]:
    """Build the KMP prefix (failure) function for `pattern`.

    pi[i] = length of the longest proper prefix of pattern[0..i]
    that is also a suffix of pattern[0..i].

    Time: O(n) amortized (j increases at most n times total, so it
    can decrease at most n times total across the whole loop).
    Space: O(n).
    """
    n = len(pattern)
    if n == 0:
        return []
    pi = [0] * n
    j = 0  # length of previous longest prefix-suffix
    for i in range(1, n):
        while j > 0 and pattern[j] != pattern[i]:
            j = pi[j - 1]
        if pattern[j] == pattern[i]:
            j += 1
        pi[i] = j
    return pi
```

## KMP Search — O(n + m)

**Goal:** find every start index where `pattern` occurs in `text`, including overlapping occurrences.
**Approach:** slide `pattern` against `text` using the prefix table to skip already-verified characters after a mismatch; on a full match, fall back to `pi[j-1]` to keep looking for the next (possibly overlapping) hit instead of restarting at `j = 0`.

```python
def kmp_search(text: str, pattern: str) -> list[int]:
    """Find all (possibly overlapping) start indices of `pattern` in `text`.

    Time: O(n + m) where n = len(text), m = len(pattern).
    Space: O(m) for the prefix table.
    """
    if not pattern or len(pattern) > len(text):
        return []
    pi = build_prefix(pattern)
    matches = []
    j = 0  # number of matched pattern characters so far
    for i in range(len(text)):
        while j > 0 and text[i] != pattern[j]:
            j = pi[j - 1]
        if text[i] == pattern[j]:
            j += 1
        if j == len(pattern):
            matches.append(i - j + 1)
            j = pi[j - 1]  # keep scanning for overlapping matches
    return matches


def find_motif_in_sequence(sequence: str, motif: str) -> list[int]:
    """Convenience wrapper for DNA/protein motif search (e.g. a primer or
    restriction site) using KMP. Sequence and motif are matched literally
    (uppercase both first if case should be ignored).
    """
    return kmp_search(sequence, motif)
```

## Complexity

| | Time | Space |
|---|---|---|
| Preprocessing (prefix table) | O(m) | O(m) |
| Search | O(n) | O(1) extra |
| **Total** | **O(n + m)** | **O(m)** |

## Pitfalls

- The prefix-table build looks `O(n^2)` due to the nested `while` inside the `for`, but the amortized argument (`j` can only decrease as many times as it increased) guarantees `O(n)`.
- KMP finds overlapping matches by default — `j = pi[j - 1]` after a full match continues searching instead of resetting `j = 0`.
- KMP does exact matching only; it does not tolerate mismatches/indels — for approximate/fuzzy matching use edit-distance or seed-and-extend approaches instead.
- For searching many patterns at once, running `kmp_search` per pattern is `O(k*(n+m))`; use Aho-Corasick to search all patterns in one `O(n + sum(m) + matches)` pass.
- Empty pattern or pattern longer than text must short-circuit to `[]` — both are handled above, but easy to forget in a from-scratch reimplementation.

## See Also

- `algo-naive-pattern-matching` — the O(n*m) baseline KMP improves on.
- `algo-rabin-karp` — hashing-based alternative, good for multiple-pattern rolling-hash search.
- `algo-aho-corasick` — generalizes KMP's failure function to search many patterns simultaneously.
- `algo-dfa-matching` — builds a full state machine instead of a fallback table; O(n) search with no backtracking logic.
