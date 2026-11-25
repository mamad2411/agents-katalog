---
name: algo-suffix-arrays
description: "Build a suffix array (Manber-Myers O(n log n)) and LCP array (Kasai's O(n)) in Python; binary-search substrings, count k-mers, find longest repeated motifs. Use for text indexing, pattern search, or aligner (BWA-like) internals."
tool_type: python
primary_tool: Python
---

# Suffix Arrays

## When to Use

- Need to search a fixed text for many different patterns (build once, query O(m log n) each)
- Implementing or understanding the index behind short-read aligners (BWA, bowtie) or full-text search
- Finding the longest repeated substring/motif, counting distinct substrings, or de-duplicating k-mers in a DNA sequence
- Memory-constrained alternative to a suffix tree (an `int` array vs. a pointer-heavy tree)
- Comparing construction strategies (naive vs. doubling) for a coursework/algorithms exercise

## Version Compatibility

Pure Python 3.8+ (uses only `collections`, list slicing, `str` comparisons). No third-party dependencies. For production-scale genomic indexing (millions of bases), use `pydivsufsort` or `pysuffixarray` (SA-IS, O(n)) instead of the O(n log n) code here.

## Prerequisites

- Comfortable with Python string slicing and binary search
- Related: `algo-suffix-trees` (tree alternative), `algo-kmp-algorithm` / `algo-rabin-karp` (single-pattern search without an index)
- No external packages required

**Always append a sentinel** (e.g. `'$'`) lexicographically smaller than every other character — guarantees no suffix is a prefix of another, so sorting is well-defined.

## Construction

**Goal:** Turn a string into `SA`, an array of integers where `SA[i]` is the start position of the i-th lexicographically smallest suffix.

**Approach:** Naive sort is easiest to reason about (O(n^2 log n) — each of the O(n log n) comparisons costs O(n)). Manber-Myers replaces whole-suffix comparisons with O(1) rank-pair comparisons by doubling the compared prefix length each round, giving O(n log n).

```python
def build_suffix_array_naive(text: str) -> list[int]:
    """Sort all suffixes directly. O(n^2 log n) time, O(n^2) space.

    >>> build_suffix_array_naive("banana$")
    [6, 5, 3, 1, 0, 4, 2]
    """
    n = len(text)
    suffixes = [(text[i:], i) for i in range(n)]
    suffixes.sort(key=lambda pair: pair[0])
    return [pos for _, pos in suffixes]


def build_suffix_array_manber_myers(text: str) -> list[int]:
    """Doubling-rank construction. O(n log n) time, O(n) space.

    Each round sorts by (rank[i], rank[i+k]) pairs -- an O(1) comparison
    key -- instead of comparing raw substrings, then re-derives ranks.

    >>> build_suffix_array_manber_myers("banana$")
    [6, 5, 3, 1, 0, 4, 2]
    """
    n = len(text)
    if n <= 1:
        return list(range(n))

    sa = list(range(n))
    rank = [ord(c) for c in text]
    tmp = [0] * n
    k = 1
    while k < n:
        def key(i, k=k):
            return (rank[i], rank[i + k] if i + k < n else -1)

        sa.sort(key=key)
        tmp[sa[0]] = 0
        for i in range(1, n):
            tmp[sa[i]] = tmp[sa[i - 1]] + (1 if key(sa[i]) > key(sa[i - 1]) else 0)
        rank, tmp = tmp, rank
        if rank[sa[-1]] == n - 1:  # all ranks unique -> fully sorted
            break
        k *= 2
    return sa
```

## Pattern Search and LCP Array

**Goal:** Given `SA`, find every occurrence of a pattern, and find the longest repeated substring.

**Approach:** A pattern occurring in `text` must be a prefix of some suffix, and suffixes are sorted in `SA`, so binary search finds the contiguous range `[lower, upper)` of matching suffixes in O(m log n). Kasai's algorithm then builds the LCP array (`LCP[i]` = shared prefix length of suffixes `SA[i-1]` and `SA[i]`) in O(n) by reusing the previous match length across the pass, avoiding re-scanning from zero each time.

```python
def search_pattern(text: str, sa: list[int], pattern: str) -> list[int]:
    """Binary search for all occurrences of pattern. O(m log n).

    >>> sa = build_suffix_array_naive("banana$")
    >>> search_pattern("banana$", sa, "ana")
    [1, 3]
    """
    n, m = len(text), len(pattern)
    if m == 0:
        return list(range(n))

    def bound(strict):
        lo, hi = 0, n
        while lo < hi:
            mid = (lo + hi) // 2
            suffix_prefix = text[sa[mid]:sa[mid] + m]
            cond = suffix_prefix <= pattern if strict else suffix_prefix < pattern
            if cond:
                lo = mid + 1
            else:
                hi = mid
        return lo

    lower, upper = bound(False), bound(True)
    return sorted(sa[i] for i in range(lower, upper))


def build_lcp_array(text: str, sa: list[int]) -> list[int]:
    """Kasai's algorithm: LCP[i] = shared prefix length of SA[i-1], SA[i]. O(n).

    >>> sa = build_suffix_array_naive("banana$")
    >>> build_lcp_array("banana$", sa)
    [0, 0, 1, 3, 0, 0, 2]
    """
    n = len(text)
    rank = [0] * n
    for i, pos in enumerate(sa):
        rank[pos] = i

    lcp = [0] * n
    k = 0
    for i in range(n):
        if rank[i] == 0:
            k = 0
            continue
        j = sa[rank[i] - 1]
        while i + k < n and j + k < n and text[i + k] == text[j + k]:
            k += 1
        lcp[rank[i]] = k
        if k > 0:
            k -= 1  # LCP can drop by at most 1 between successive suffixes
    return lcp


def longest_repeated_substring(text: str) -> tuple[str, list[int]]:
    """Longest substring occurring >=2 times, via max(LCP). O(n log n).

    >>> longest_repeated_substring("banana$")
    ('ana', [1, 3])
    """
    if len(text) <= 1:
        return ("", [])
    sa = build_suffix_array_manber_myers(text)
    lcp = build_lcp_array(text, sa)
    max_idx = max(range(len(lcp)), key=lambda i: lcp[i])
    if lcp[max_idx] == 0:
        return ("", [])
    lrs = text[sa[max_idx]:sa[max_idx] + lcp[max_idx]]
    return (lrs, search_pattern(text, sa, lrs))
```

## K-mer Counting on a DNA Sequence

**Goal:** Count occurrences of every distinct k-mer in a genomic string using the suffix array instead of a hash table.

**Approach:** Build `SA`, then for each starting index derive its k-mer and use `search_pattern` (or count contiguous SA runs with the same k-length prefix) to get its frequency; distinct k-mers are deduplicated via a `set`.

```python
def count_kmer_occurrences(sequence: str, k: int) -> list[tuple[str, int]]:
    """Count every distinct k-mer using the suffix array + binary search.

    Args:
        sequence: DNA string, should end with a '$' sentinel.
        k: k-mer length.

    Returns:
        (kmer, count) pairs sorted by descending count, then kmer.
    """
    sa = build_suffix_array_naive(sequence)
    seen = set()
    counts = []
    for pos in sa:
        kmer = sequence[pos:pos + k]
        if len(kmer) < k or kmer in seen or "$" in kmer:
            continue
        seen.add(kmer)
        counts.append((kmer, len(search_pattern(sequence, sa, kmer))))
    counts.sort(key=lambda pair: (-pair[1], pair[0]))
    return counts


if __name__ == "__main__":
    dna = "ATCGATCGATCGAATTCCGATCGATCGATCG$"
    top5 = count_kmer_occurrences(dna, k=4)[:5]
    assert top5[0][0] == "ATCG" and top5[0][1] >= 4, top5
    assert longest_repeated_substring("banana$") == ("ana", [1, 3])
    print("top 4-mers:", top5)
```

## Complexity Comparison

| Method | Construction | Space | Pattern search |
|---|---|---|---|
| Naive | O(n^2 log n) | O(n^2) | O(m log n) |
| Manber-Myers | O(n log n) | O(n) | O(m log n) |
| SA-IS / DC3 | O(n) | O(n) | O(m log n) |
| LCP (Kasai) | O(n), needs SA first | O(n) | n/a |

## Pitfalls

- Forgetting the sentinel `'$'` causes incorrect sorting when one suffix is a true prefix of another (e.g. "ab" vs "abab").
- Naive construction materializes every suffix as a Python string slice — O(n^2) memory; switch to Manber-Myers (or SA-IS) once `n` exceeds a few thousand.
- `search_pattern`'s two binary searches must use `<` for the lower bound and `<=` for the upper bound (or the run range is off by one/empty).
- Kasai's algorithm requires `sa` and its `rank` (inverse permutation) both built from the *same* text — rebuild both if the text changes.
- For real genomes, use a C-backed SA-IS library (`pydivsufsort`) — the pure-Python code here is for correctness/teaching, not multi-megabase genomes.

## See Also

- `algo-suffix-trees` — pointer-based alternative structure with the same query capabilities
- `algo-kmp-algorithm`, `algo-rabin-karp` — single-pattern search without building a full index
- `algo-aho-corasick` — multi-pattern search when patterns (not the text) are fixed in advance
- `bio-read-alignment-bwa-alignment` — real-world aligner built on an FM-index/suffix-array-like structure
