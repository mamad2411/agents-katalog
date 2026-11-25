---
name: algo-suffix-trees
description: "Build a suffix tree for O(m) pattern search, longest repeated substring, and longest common substring (LCS). Use when finding all motif occurrences in DNA/text, detecting tandem repeats, or comparing two sequences' shared region."
tool_type: python
primary_tool: Python
---

# Suffix Trees

A compressed trie of every suffix of a string. O(n) nodes, O(m) time to search for a pattern of length m, O(m+k) to report all k occurrences.

## When to Use

- Finding every occurrence of a pattern/motif in a string or DNA sequence in O(m+k) time.
- Finding the longest repeated substring (repeat detection, tandem repeats) in O(n).
- Finding the longest common substring (LCS) between two sequences via a generalized suffix tree in O(n+m).
- Explaining/choosing between suffix tree and suffix array for a string-indexing task.
- Any task phrased as "build a suffix tree", "index all suffixes", or "search substrings efficiently, repeatedly".

## Version Compatibility

Pure-Python, stdlib only — no version dependencies. Python ≥3.8 (uses `list[tuple[...]]` type hints in examples; drop hints for Python <3.9).

## Prerequisites

- No packages required (stdlib only).
- Concepts: tries (`algo-tries`), pattern matching basics (`algo-naive-pattern-matching`).
- For production-scale texts, know that this naive O(n^2) build is for learning/small inputs; real systems use Ukkonen's O(n) algorithm or a suffix array.

## Key Properties

- Exactly n leaves (one per suffix), at most n-1 internal nodes.
- Every internal node (except root) has >= 2 children.
- Edge labels are substrings, not single characters (this is what distinguishes it from a suffix trie).
- The path from root to leaf i spells the suffix starting at position i.
- Always append a unique terminal character (`$`) before building — otherwise suffixes that are prefixes of other suffixes won't get their own leaf.

## Suffix Tree vs Suffix Array

| | Suffix Tree | Suffix Array |
|---|---|---|
| Space | O(n), large constant (~20n bytes) | O(n), small constant (~5n bytes) |
| Pattern search | O(m) | O(m log n), or O(m) with LCP array |
| Construction | O(n) via Ukkonen | O(n) via SA-IS/DC3 |
| Cache behavior | Poor (pointer chasing) | Good (contiguous array) |
| Implementation | Complex | Simpler |

Prefer a suffix array (`algo-suffix-arrays`) when space or implementation simplicity matters; prefer a suffix tree when you need O(m) search without an LCP array or want to exploit suffix links for dynamic queries.

**Goal:** build a suffix tree and support exact pattern search returning all occurrence positions.
**Approach:** insert every suffix into a trie (O(n^2)), then compress every single-child chain into one edge so the tree has O(n) nodes; search by walking edges character-by-character.

```python
class SuffixTreeNode:
    """A node in the suffix tree: edge_label -> child, plus leaf metadata."""

    def __init__(self):
        self.children = {}      # edge_label (str) -> SuffixTreeNode
        self.suffix_index = -1  # leaf: starting position of the suffix; internal: -1

    def is_leaf(self):
        return len(self.children) == 0


class SuffixTree:
    """Suffix tree with naive O(n^2) construction (trie build + compression)."""

    def __init__(self, text, terminal="$"):
        self.text = text + terminal
        self.root = SuffixTreeNode()
        self._build_trie()
        self._compress(self.root)

    def _build_trie(self):
        n = len(self.text)
        for i in range(n):
            current = self.root
            for j in range(i, n):
                char = self.text[j]
                if char not in current.children:
                    current.children[char] = SuffixTreeNode()
                current = current.children[char]
            current.suffix_index = i

    def _compress(self, node):
        """Merge single-child chains into single substring-labeled edges."""
        changed = True
        while changed:
            changed = False
            for key in list(node.children.keys()):
                child = node.children[key]
                if len(child.children) == 1:
                    grandchild_key = next(iter(child.children))
                    node.children[key + grandchild_key] = child.children[grandchild_key]
                    del node.children[key]
                    changed = True
        for child in node.children.values():
            self._compress(child)

    def search(self, pattern):
        """Return sorted starting positions of every occurrence of pattern, or []."""
        node, remaining = self.root, pattern
        while remaining:
            found = False
            for edge, child in node.children.items():
                if edge[0] == remaining[0]:
                    match_len = min(len(edge), len(remaining))
                    if edge[:match_len] != remaining[:match_len]:
                        return []
                    remaining = remaining[match_len:]
                    node = child
                    found = True
                    break
            if not found:
                return []
        positions = []
        self._collect_leaves(node, positions)
        return sorted(positions)

    def _collect_leaves(self, node, positions):
        if node.is_leaf():
            positions.append(node.suffix_index)
        else:
            for child in node.children.values():
                self._collect_leaves(child, positions)


def demo_search():
    st = SuffixTree("banana")
    assert st.search("ana") == [1, 3]
    assert st.search("xyz") == []
    assert st.search("a") == [1, 3, 5]
    print("search() ok")
```

**Goal:** find the longest repeated substring (LRS) of a single sequence.
**Approach:** the LRS corresponds to the deepest internal node (>=2 children) in the suffix tree; DFS tracking path label and depth.

```python
class SuffixTreeLRS(SuffixTree):
    """Suffix tree extended to find the longest repeated substring."""

    def find_longest_repeated_substring(self):
        """Return (lrs_string, sorted_start_positions); ("", []) if no repeat."""
        self.max_depth = 0
        self.lrs_node = None
        self.lrs_path = ""

        def dfs(node, depth, path):
            if not node.is_leaf() and len(node.children) >= 2 and depth > self.max_depth:
                self.max_depth = depth
                self.lrs_node = node
                self.lrs_path = path
            for edge_label, child in node.children.items():
                dfs(child, depth + len(edge_label), path + edge_label)

        dfs(self.root, 0, "")
        if self.lrs_node is None:
            return ("", [])
        positions = []
        self._collect_leaves(self.lrs_node, positions)
        return (self.lrs_path, sorted(positions))


def demo_lrs():
    st = SuffixTreeLRS("mississippi")
    lrs, positions = st.find_longest_repeated_substring()
    assert lrs == "issi"
    assert positions == [1, 4]
    print("LRS ok:", lrs, positions)
```

**Goal:** find the longest common substring (LCS) shared by two sequences (e.g., two DNA reads).
**Approach:** concatenate `text1 + "$" + text2 + "#"` with distinct terminators, build one suffix tree, tag each leaf with which string it came from, then DFS for the deepest internal node whose subtree contains leaves from both strings.

```python
class SuffixTreeLCS(SuffixTree):
    """Generalized suffix tree over text1$text2# for longest common substring."""

    def __init__(self, text1, text2):
        self.separator_pos = len(text1)
        super().__init__(text1 + "$" + text2, terminal="#")
        self._mark_string_ids()

    def _mark_string_ids(self):
        def mark(node):
            if node.is_leaf():
                node.string_id = 1 if node.suffix_index <= self.separator_pos else 2
            else:
                for child in node.children.values():
                    mark(child)
        mark(self.root)

    def find_lcs(self):
        """Return the longest substring common to both input strings."""
        self.max_depth = 0
        self.lcs = ""

        def dfs(node, depth, path):
            if node.is_leaf():
                return {node.string_id}
            ids = set()
            for edge_label, child in node.children.items():
                ids |= dfs(child, depth + len(edge_label), path + edge_label)
            if {1, 2}.issubset(ids) and depth > self.max_depth:
                self.max_depth = depth
                self.lcs = path
            return ids

        dfs(self.root, 0, "")
        return self.lcs


def demo_lcs():
    lcs = SuffixTreeLCS("ABAB", "BABA").find_lcs()
    assert lcs in ("ABA", "BAB")
    print("LCS ok:", lcs)


if __name__ == "__main__":
    demo_search()
    demo_lrs()
    demo_lcs()
```

## Operations Complexity

| Operation | Naive Build | Ukkonen Build |
|---|---|---|
| Construction | O(n^2) | O(n) |
| Pattern search | O(m) | O(m) |
| All k occurrences | O(m + k) | O(m + k) |
| Longest repeated substring | O(n) | O(n) |
| LCS of two strings | O(n + m) | O(n + m) |

## Pitfalls

- Always append a unique terminal character (`$`, and a *different* one per string in generalized trees) — without it, suffixes that are prefixes of other suffixes silently merge and lose their leaf.
- The naive construction here is O(n^2) — fine for teaching/short sequences (up to a few thousand bp), but for chromosome-scale text implement Ukkonen's O(n) algorithm or switch to a suffix array.
- This implementation stores edge labels as literal substrings for clarity; production implementations store `(start, end)` index pairs into the original text to get true O(n) space.
- For LCS with two strings, using the *same* terminal character for both breaks the "deepest node with both string IDs" logic — terminators must differ (`$` vs `#`).
- `find_longest_repeated_substring`/`find_lcs` do a full O(n) DFS per call — fine once per tree, but don't rebuild the tree per query.

## See Also

- `algo-suffix-arrays` — smaller-footprint alternative with O(m log n) search.
- `algo-tries` — the uncompressed building block a suffix tree compresses.
- `algo-aho-corasick` — multi-pattern matching when you have many fixed patterns instead of one text to index.
- `algo-kmp-algorithm` — single-pattern search without building an index structure.
