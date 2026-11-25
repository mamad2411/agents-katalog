---
name: algo-aho-corasick
description: "Build an Aho-Corasick automaton (trie + BFS failure links) to find every pattern occurrence in one O(n+m+z) text pass. Use for restriction-site/primer/motif search or replacing per-pattern KMP/regex loops over many fixed patterns."
tool_type: python
primary_tool: Python
---

# Aho-Corasick Algorithm

## When to Use

- Searching a text/sequence for **many fixed patterns at once** (tens to thousands), e.g. restriction enzyme recognition sites, PCR primer binding sites, transcription-factor motifs, stop/start codons, or a dictionary of known variants/k-mers.
- You would otherwise call KMP or `str.find`/regex alternation once per pattern — Aho-Corasick does it in a single pass over the text instead of `k` passes.
- Patterns are known up front and reused across many texts (build once, `search()` many times) — e.g. scanning many contigs/reads against the same motif set.
- You need **overlapping matches** reported (e.g. "he" inside "she"), which greedy single-pattern scanners typically miss.
- Not a fit: single pattern (use KMP/`algo-kmp-algorithm`), or patterns that change on every call (rebuild cost dominates).

## Version Compatibility

Pure Python standard library only — no third-party dependency. Verified on Python ≥3.9 (uses `list[tuple[str,int]]` style type hints available via `from __future__ import annotations` on 3.7+; native on 3.9+). No API has changed across Python versions relevant here.

## Prerequisites

- No packages to install — uses only `collections.deque`.
- Prior concepts: trie/prefix-tree traversal (`algo-tries`), and KMP failure functions (`algo-kmp-algorithm`) — Aho-Corasick failure links are the multi-pattern generalization of KMP's.

**Goal:** find every occurrence of every pattern in a set, in one linear pass over the text.

**Approach:** insert all patterns into a trie, run a BFS over the trie to attach a failure link to each node (pointing to the longest proper suffix of that node's string that is also some trie prefix), merge each node's failure-link output into its own output list, then scan the text once, following failure links on mismatch instead of restarting.

```python
from collections import deque


class AhoCorasickNode:
    """A node in the Aho-Corasick trie/automaton."""

    def __init__(self):
        self.children: dict[str, "AhoCorasickNode"] = {}
        self.fail: "AhoCorasickNode | None" = None
        self.output: list[str] = []  # patterns ending at this node (incl. via fail chain)


class AhoCorasick:
    """Multi-pattern matcher: O(n + m + z) build+search vs O(n*k) naive.

    n = text length, m = total pattern length, k = pattern count, z = match count.

    Example:
        >>> ac = AhoCorasick()
        >>> ac.add_patterns(["he", "she", "hers"])
        >>> ac.build()
        >>> ac.search("ushers")
        [('she', 1), ('he', 2), ('hers', 2)]
    """

    def __init__(self):
        self.root = AhoCorasickNode()
        self.root.fail = self.root
        self._built = False

    def add_pattern(self, pattern: str) -> None:
        """Insert one pattern into the trie. Must be called before build()."""
        if not pattern:
            raise ValueError("pattern cannot be empty")
        if self._built:
            raise RuntimeError("cannot add patterns after build()")
        node = self.root
        for ch in pattern:
            node = node.children.setdefault(ch, AhoCorasickNode())
        node.output.append(pattern)

    def add_patterns(self, patterns: list[str]) -> None:
        """Insert multiple patterns."""
        for p in patterns:
            self.add_pattern(p)

    def build(self) -> None:
        """Compute failure links and merge output lists via BFS. O(m) total."""
        if self._built:
            return
        queue: deque[AhoCorasickNode] = deque()
        for child in self.root.children.values():
            child.fail = self.root
            queue.append(child)

        while queue:
            current = queue.popleft()
            for ch, child in current.children.items():
                queue.append(child)
                f = current.fail
                while f is not self.root and ch not in f.children:
                    f = f.fail
                child.fail = f.children[ch] if ch in f.children else self.root
                # Inherit shorter patterns reachable via the failure chain
                # (e.g. "she" also reports "he" because fail["she"] == "he").
                child.output = child.output + child.fail.output
        self._built = True

    def search(self, text: str) -> list[tuple[str, int]]:
        """Return (pattern, start_index) for every match, in scan order."""
        if not self._built:
            raise RuntimeError("call build() before search()")
        results: list[tuple[str, int]] = []
        node = self.root
        for i, ch in enumerate(text):
            while node is not self.root and ch not in node.children:
                node = node.fail
            if ch in node.children:
                node = node.children[ch]
            for pattern in node.output:
                results.append((pattern, i - len(pattern) + 1))
        return results
```

**Goal:** apply the automaton to a real multi-pattern bioinformatics task — locating restriction enzyme recognition sites in a DNA sequence.

**Approach:** build one automaton from the enzyme-name→recognition-sequence dict, run a single `search()`, then regroup the flat `(pattern, position)` hits back by enzyme name.

```python
def find_restriction_sites(dna: str, sites: dict[str, str]) -> dict[str, list[int]]:
    """Find all restriction-enzyme cut sites in a DNA sequence.

    Args:
        dna: sequence to search (e.g. uppercase A/C/G/T).
        sites: enzyme name -> recognition sequence (e.g. {"EcoRI": "GAATTC"}).

    Returns:
        enzyme name -> sorted list of 0-based match start positions.
    """
    seq_to_name = {seq: name for name, seq in sites.items()}
    ac = AhoCorasick()
    ac.add_patterns(list(sites.values()))
    ac.build()

    hits: dict[str, list[int]] = {name: [] for name in sites}
    for seq, pos in ac.search(dna):
        hits[seq_to_name[seq]].append(pos)
    for name in hits:
        hits[name].sort()
    return hits


if __name__ == "__main__":
    RECOGNITION_SITES = {"EcoRI": "GAATTC", "BamHI": "GGATCC", "HindIII": "AAGCTT"}
    DNA = "ACGTGAATTCTAGGGATCCAAAGCTTCGATCGGAATTCTTAAGCTTGCTAGGATCCGCATGAATTCGCTAGC"

    result = find_restriction_sites(DNA, RECOGNITION_SITES)
    assert result["EcoRI"] == [4, 32, 60]
    assert result["BamHI"] == [13, 50]
    assert result["HindIII"] == [20, 40]
    print("all sites:", result)
```

## Complexity

| Phase | Time | Space |
|-------|------|-------|
| Build trie | O(m) | O(m x sigma) |
| Failure links (BFS) | O(m) | O(m) |
| Search | O(n + z) | O(1) extra |
| **Total** | **O(n + m + z)** | **O(m)** |

n = text length, m = total pattern length, z = match count, sigma = alphabet size.

## Pitfalls

- **Must call `build()` before `search()`**: failure links are unset during `add_pattern`; searching first raises `RuntimeError`.
- **Output-list merging is what makes overlaps work**: `child.output = child.output + child.fail.output` during BFS is what surfaces "he" inside "she". Skipping this step silently drops all shorter contained patterns.
- **Root's self-loop (`root.fail = root`)** is required — without it the `while` loop in `search()` never terminates on repeated mismatches.
- **Adding patterns after `build()` raises** — there is no incremental update; rebuild the whole automaton if the pattern set changes.
- **Case sensitivity**: matching is exact per-character; normalize both patterns and text (e.g. `.upper()`) before inserting/searching, especially for DNA sequences that may mix cases.
- **Empty patterns**: `add_pattern("")` raises `ValueError` — filter out empty strings from any generated pattern list first.

## See Also

- `algo-kmp-algorithm` — single-pattern failure-function matching that Aho-Corasick generalizes.
- `algo-tries` — the underlying trie/prefix-tree data structure.
- `algo-rabin-karp` — hashing-based alternative for single or small pattern sets.
- `bio-restriction-analysis-restriction-sites` — restriction-site finding using dedicated bioinformatics libraries.
