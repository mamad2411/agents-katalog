---
name: advanced-string-structures
description: Build tries, Aho-Corasick, and suffix arrays with Kasai LCP to index DNA/text and match many patterns in one pass. Use for genome motif scanning, k-mer indexing, longest-repeat search, or BWA/FM-index groundwork.
tool_type: python
primary_tool: Python
---

# Advanced String Structures

## When to Use
- Scanning a genome/read for **many** motifs/adapters/primers in a single O(n) pass (Aho-Corasick)
- Prefix search, autocomplete, or k-mer/barcode membership testing (Trie)
- Genome-wide exact pattern search, longest repeated substring, or k-mer counting (Suffix Array + LCP)
- Finding the longest common substring between two sequences, or tandem-repeat detection (Suffix Tree)
- Building the intuition behind index-based aligners (BWA, Bowtie) before touching their C internals

## Version Compatibility
Pure Python stdlib — no version-sensitive APIs. Works on Python ≥3.8 (uses `dict`, `collections.deque/defaultdict`, PEP 604-style hints need ≥3.10 or `from __future__ import annotations` on 3.8/3.9).

## Prerequisites
- No packages required — everything below is stdlib (`collections`).
- For production multi-pattern matching at scale, prefer `pip install pyahocorasick` (C implementation) over the pure-Python version here.
- Concept prerequisite: `string-algorithms` skill (KMP/Rabin-Karp) — this skill builds on top of single-pattern matching.

## Complexity Table

| Structure | Build | Pattern Search | Space |
|-----------|-------|---------------|-------|
| Trie | O(n·m) | O(m) | O(n·m) |
| Aho-Corasick | O(M) | O(n + M + z) | O(M) |
| Suffix Array (naive) | O(n² log n) | O(m log n) | O(n) |
| Suffix Array (Manber-Myers) | O(n log n) | O(m log n) | O(n) |
| LCP Array (Kasai) | O(n) | — | O(n) |
| Suffix Tree (Ukkonen) | O(n) | O(m + k) | O(n) |

`n` = text length, `m` = pattern length, `M` = total pattern length, `z` = number of matches.

## Trie

**Goal:** support prefix search / autocomplete / k-mer membership in O(m) per query.
**Approach:** one node per character; `is_end` marks a complete word; deletion only removes a node once it has no children.

```python
class TrieNode:
    def __init__(self):
        self.children: dict[str, "TrieNode"] = {}
        self.is_end = False

class Trie:
    """Prefix tree for exact word/k-mer membership and autocomplete."""
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
        node.is_end = True

    def search(self, word: str) -> bool:
        node = self._find(word)
        return node is not None and node.is_end

    def starts_with(self, prefix: str) -> bool:
        return self._find(prefix) is not None

    def _find(self, prefix: str):
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node

    def get_all_with_prefix(self, prefix: str) -> list[str]:
        """Return every inserted word starting with `prefix`, sorted."""
        results: list[str] = []
        node = self._find(prefix)
        if node:
            self._dfs(node, prefix, results)
        return results

    def _dfs(self, node, word, results):
        if node.is_end:
            results.append(word)
        for ch, child in sorted(node.children.items()):
            self._dfs(child, word + ch, results)
```

## Aho-Corasick

**Goal:** find every occurrence of *k* patterns (motifs, adapters, primers) in one linear pass over the text.
**Approach:** build a trie over all patterns, then BFS to attach failure links (`fail[v]` = longest proper suffix of the node's string that is also a trie prefix); propagate `output` lists along failure links so a match of a longer pattern also reports shorter patterns embedded in it (e.g. "he" inside "she").

```python
from collections import defaultdict, deque

class AhoNode:
    def __init__(self):
        self.children: dict[str, "AhoNode"] = {}
        self.patterns: list[str] = []          # patterns ending at this node
        self.fail: "AhoNode | None" = None

def build_automaton(patterns: list[str]) -> AhoNode:
    """Build an Aho-Corasick automaton (trie + failure links) over `patterns`."""
    root = AhoNode()
    for pat in patterns:
        node = root
        for ch in pat:
            node = node.children.setdefault(ch, AhoNode())
        node.patterns.append(pat)

    queue = deque()
    for child in root.children.values():
        child.fail = root
        queue.append(child)

    while queue:
        cur = queue.popleft()
        for ch, child in cur.children.items():
            queue.append(child)
            fb = cur.fail
            while fb is not None and ch not in fb.children:
                fb = fb.fail
            child.fail = fb.children[ch] if fb else root
            child.patterns = child.patterns + child.fail.patterns  # propagate output link
    return root

def find_all(text: str, patterns: list[str]) -> dict[str, list[int]]:
    """Return {pattern: [start indices]} for every occurrence of every pattern in text, O(n)."""
    root = build_automaton(patterns)
    results: dict[str, list[int]] = defaultdict(list)
    node = root
    for i, ch in enumerate(text):
        while node is not None and ch not in node.children:
            node = node.fail
        node = node.children[ch] if node else root
        for pat in node.patterns:
            results[pat].append(i - len(pat) + 1)
    return dict(results)
```

## Suffix Array + Kasai LCP + Pattern Search

**Goal:** genome-wide exact pattern search, longest repeated substring, and k-mer counting without a full suffix tree's memory cost.
**Approach:** append a sentinel `$` (smaller than every alphabet character) to force distinct suffixes; sort all suffix start indices to get `SA`; run Kasai's algorithm to get `LCP[i]` = shared prefix length between `SA[i-1]` and `SA[i]` in O(n); binary-search `SA` for pattern occurrences in O(m log n).

```python
def build_suffix_array(text: str) -> list[int]:
    """Naive O(n^2 log n) suffix array. Append '$' to text before calling."""
    return sorted(range(len(text)), key=lambda i: text[i:])

def build_lcp_array(text: str, sa: list[int]) -> list[int]:
    """Kasai's algorithm: LCP[i] = shared prefix length of suffixes SA[i-1], SA[i]. O(n)."""
    n = len(text)
    rank = [0] * n
    for i, s in enumerate(sa):
        rank[s] = i
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
        if k:
            k -= 1
    return lcp

def search_pattern(text: str, sa: list[int], pattern: str) -> list[int]:
    """Binary search SA for all start positions of `pattern`. O(m log n)."""
    n, m = len(text), len(pattern)
    left, right = 0, n
    while left < right:
        mid = (left + right) // 2
        if text[sa[mid]:sa[mid] + m] < pattern:
            left = mid + 1
        else:
            right = mid
    lo = left
    left, right = lo, n
    while left < right:
        mid = (left + right) // 2
        if text[sa[mid]:sa[mid] + m] <= pattern:
            left = mid + 1
        else:
            right = mid
    return sorted(sa[lo:left])
```

`text[sa[k]:sa[k]+lcp[k]]` where `k = lcp.index(max(lcp))` gives the longest repeated substring directly. Manber-Myers doubling (sort by 1, 2, 4, ... characters, using previous-round ranks as O(1) comparison keys) builds the same array in O(n log n) instead of O(n² log n) — switch to it once `len(text)` exceeds a few thousand bases.

## Suffix Tree (concept)

A suffix tree is a compressed trie of all suffixes: exactly `n` leaves, ≤ `n-1` internal nodes, built in O(n) via Ukkonen's algorithm. Edge labels are stored as `(start, end)` index pairs into the original text, never copied substrings, or the tree becomes O(n²) space. To find the longest common substring of two sequences, concatenate them as `seq1 + "$" + seq2 + "#"`, build the generalized suffix tree, and find the deepest internal node whose leaf set contains suffixes from both `seq1` and `seq2`.

## Pitfalls

- **Sentinel character**: suffix arrays/trees need a unique terminator (`$`) smaller than every alphabet character, or ties break the sort/traversal silently
- **Aho-Corasick output propagation**: skipping `child.patterns += child.fail.patterns` during BFS silently drops matches of shorter patterns embedded in longer ones
- **Trie deletion**: unset `is_end` only; remove the node itself only once it has zero children, otherwise you delete shared prefixes other words depend on
- **LCP indexing**: `LCP[0]` is meaningless (defined as 0); `LCP[i]` compares `SA[i-1]` and `SA[i]`, not adjacent text positions
- **Naive suffix array** is O(n² log n) from Python string slicing in the sort key — fine for reads/motifs, too slow for whole chromosomes; switch to Manber-Myers or SA-IS

## Bioinformatics Connections

| Application | Structure | Detail |
|-------------|-----------|--------|
| Short-read alignment (BWA, Bowtie) | Suffix Array + BWT/FM-index | BWT = `text[SA[i]-1]`; FM-index gives O(m) backward search |
| Multi-motif/adapter scanning | Aho-Corasick | One pass over a genome finds all k patterns at once |
| K-mer counting / assembly | Trie or Suffix Array | Binary search on SA counts k-mer occurrences |
| Longest repeated motif | Suffix Array + LCP | `max(LCP)` gives the LRS length directly |
| LCS of two sequences | Generalized Suffix Tree | Concatenate `seq1$seq2#`; deepest internal node with leaves from both |

## See Also
- `string-algorithms` — KMP/Rabin-Karp/DFA single-pattern matching (prerequisite)
- `bio-sequence-manipulation-motif-search` — biopython-level motif search for simpler cases
- `bio-read-alignment-bwa-alignment` — production FM-index-based short-read aligner built on these ideas
- `bio-genome-assembly-short-read-assembly` — k-mer/de Bruijn graph assembly using these indexes
