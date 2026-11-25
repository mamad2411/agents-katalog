---
name: algo-rabin-karp
description: "Rabin-Karp rolling-hash search in Python for single/multi-pattern matching (DNA motifs, k-mers, plagiarism phrases). Use when finding pattern occurrences in text, explaining rolling hash, or comparing vs KMP/naive search."
tool_type: python
primary_tool: Python
---

# Rabin-Karp Algorithm

## When to Use

- Find all start positions of a pattern (or several same-length patterns) in a text or DNA/protein sequence.
- Need to scan a genome/reference for many motifs (splice sites, restriction sites, k-mers) in a single pass.
- Asked to implement/explain rolling hash, hash-based string matching, or hash collision verification.
- Comparing algorithmic tradeoffs: Rabin-Karp vs. KMP vs. naive O(nm) search.
- Building a simple plagiarism/duplicate-substring detector over same-length phrases.

## Version Compatibility

Pure Python standard library only — no third-party dependency. Works on Python ≥3.8 (uses `list[int]` / `dict[str, list[int]]` builtin generics, so use `from __future__ import annotations` or `typing.List`/`typing.Dict` on Python <3.9).

## Prerequisites

- Comfortable with modular arithmetic (`%`) and Python string slicing.
- No packages to install. For benchmarking against KMP, only `time` (stdlib) is needed.
- Related prior concept: naive pattern matching (see `algo-naive-pattern-matching`).

## Key Insight

Compare hash values instead of strings. If `hash(window) != hash(pattern)`, definitely no match. Only verify character-by-character when hashes match (may be a collision).

## Rolling Hash Formula

Treat the string as a number in base `d` (typically 256 for ASCII), mod a prime `q`:

```text
h(s[i..i+m-1]) = s[i]*d^(m-1) + s[i+1]*d^(m-2) + ... + s[i+m-1]
```

To slide the window from position `i` to `i+1` in O(1):

```text
new_hash = (d * (old_hash - s[i] * d^(m-1)) + s[i+m]) mod q
```

**Goal:** find every start index where `pattern` occurs in `text`.
**Approach:** compute the pattern hash and the first window hash once, then roll the window hash in O(1) per step; verify with a direct string comparison only when hashes match.

```python
def rabin_karp_search(text: str, pattern: str, d: int = 256, q: int = 101) -> list[int]:
    """Find all occurrences of pattern in text using Rabin-Karp rolling hash.

    O(n+m) average, O(n*m) worst case (many hash collisions).
    Always verifies on hash match to rule out collisions.

    >>> rabin_karp_search("AABAACAADAABAABA", "AABA")
    [0, 9, 12]
    """
    n, m = len(text), len(pattern)
    if m == 0 or m > n:
        return []

    # Precompute d^(m-1) mod q, the multiplier for the leftmost character
    h = pow(d, m - 1, q)

    # Initial hashes for pattern and first window
    pattern_hash = window_hash = 0
    for i in range(m):
        pattern_hash = (d * pattern_hash + ord(pattern[i])) % q
        window_hash = (d * window_hash + ord(text[i])) % q

    matches = []
    for i in range(n - m + 1):
        if pattern_hash == window_hash:
            if text[i:i + m] == pattern:  # verify to rule out collisions
                matches.append(i)
        if i < n - m:
            window_hash = (d * (window_hash - ord(text[i]) * h) + ord(text[i + m])) % q
            if window_hash < 0:
                window_hash += q
    return matches
```

## Multi-Pattern Search (Where Rabin-Karp Shines)

**Goal:** search for k patterns of the same length in one pass (e.g. scanning a reference for several splice-site motifs at once).
**Approach:** hash all patterns into a `hash -> [patterns]` table, then roll a single hash over the text and check membership in that table — average O(n + km) vs. naive O(knm).

```python
def rabin_karp_multi(text: str, patterns: list[str], d: int = 256, q: int = 101) -> dict[str, list[int]]:
    """Search for multiple equal-length patterns in a single pass over text.

    Raises ValueError if patterns have differing lengths.

    >>> rabin_karp_multi("ACTGACTGCACTG", ["ACTG", "CTGA"])
    {'ACTG': [0, 4, 9], 'CTGA': [1]}
    """
    if not patterns:
        return {}
    m = len(patterns[0])
    if not all(len(p) == m for p in patterns):
        raise ValueError("All patterns must have the same length")

    n = len(text)
    results = {p: [] for p in patterns}
    if m == 0 or m > n:
        return results

    # Map hash -> list of patterns sharing that hash (handles hash collisions)
    pattern_hashes: dict[int, list[str]] = {}
    for pattern in patterns:
        p_hash = 0
        for ch in pattern:
            p_hash = (d * p_hash + ord(ch)) % q
        pattern_hashes.setdefault(p_hash, []).append(pattern)

    h = pow(d, m - 1, q)
    window_hash = 0
    for i in range(m):
        window_hash = (d * window_hash + ord(text[i])) % q

    for i in range(n - m + 1):
        if window_hash in pattern_hashes:
            window = text[i:i + m]
            for pattern in pattern_hashes[window_hash]:
                if window == pattern:  # verify to rule out collisions
                    results[pattern].append(i)
        if i < n - m:
            window_hash = (d * (window_hash - ord(text[i]) * h) + ord(text[i + m])) % q
            if window_hash < 0:
                window_hash += q
    return results
```

## Complexity

| Case | Time | Notes |
|---|---|---|
| Average | O(n + m) | Few hash collisions |
| Worst (many collisions) | O(nm) | Every position needs verification |
| Space | O(1) | |
| Multi-pattern (k patterns) | O(n + km) average | vs. naive O(knm) |

## Why Prime q?

- Distributes hash values uniformly, reducing collision probability.
- Without modulo, hash values overflow (256^10 is astronomically large).
- Common choices: 101 (small demo), 1_000_000_007 (production).

## Pitfalls

- Always verify on hash match — collisions are inevitable, not bugs.
- Smaller `q` = more collisions = more O(m) verifications = slower.
- Python handles negative modulo correctly, but other languages may not — add `if hash < 0: hash += q`.
- Multi-pattern variant requires all patterns to be the **same length**; for varying-length patterns, Aho-Corasick is more appropriate.
- For a single pattern with guaranteed O(n+m) (no verification step, no collision risk), prefer KMP.

## See Also

- `algo-naive-pattern-matching` — the O(nm) baseline Rabin-Karp improves on.
- `algo-kmp-algorithm` — better choice for single-pattern search with guaranteed linear time.
- `algo-aho-corasick` — better choice for many patterns of differing lengths.
- `algo-hash-tables-bloom` — underlying hashing/collision concepts.
