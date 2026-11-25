---
name: algo-red-black-trees
description: "Implement a red-black self-balancing BST (insert, rotations, recoloring) for O(log n) search on sorted VCF variant positions. Use when building a balanced BST, verifying invariants, or comparing red-black vs AVL trees."
tool_type: python
primary_tool: Python
---

# Red-Black Trees

Self-balancing BST where each node is RED or BLACK. Guarantees O(log n) search/insert/delete even when input arrives pre-sorted (where a plain BST degrades to O(n)).

## When to Use

- Need a balanced BST with guaranteed O(log n) insert/search on data that may arrive in sorted order (e.g., SNP positions read in genomic order from a VCF).
- Implementing/explaining the standard library behind `TreeMap` (Java), `std::map`/`std::set` (C++), or the Linux CFS scheduler.
- Write-heavy workload where AVL's stricter balancing would cause excess rotations.
- Building an ordered index over genomic coordinates to support overlap/range queries (gene annotations, ChIP-seq peaks, variant calls).
- Asked to verify/prove the 5 red-black invariants hold after a sequence of insertions.

## Version Compatibility

Pure Python, stdlib only — no version dependencies. Examples use Python ≥3.9 (type hints with `list[int]`, `tuple[int,int]`).

## Prerequisites

- No external packages required (stdlib only).
- Prior concept: binary search trees (see `algo-binary-search-trees`) — red-black trees add self-balancing on top of plain BST insert/search.

## 5 Invariants

| # | Property |
|---|----------|
| 1 | Every node is RED or BLACK |
| 2 | Root is BLACK |
| 3 | Every leaf (NIL) is BLACK |
| 4 | RED node has only BLACK children (no red-red) |
| 5 | All root-to-leaf paths have equal BLACK node count (black-height) |

These guarantee: longest path <= 2x shortest path, so height is O(log n).

## Red-Black vs AVL

| Aspect | AVL | Red-Black |
|--------|-----|-----------|
| Height bound | 1.44 log n | 2 log n |
| Search | Faster (shorter) | Slightly slower |
| Insert/Delete | More rotations | Fewer rotations (recolor often suffices) |
| Best for | Read-heavy | Write-heavy |
| Used in | Database indexes | Java TreeMap, C++ std::map, Linux CFS |

## Core Implementation

**Goal:** a self-balancing BST that stays O(log n) even under sorted-order insertion.
**Approach:** color every node RED or BLACK, insert as a normal BST insert (new node RED), then walk up from the new node fixing red-red violations with rotations and recoloring until the 5 invariants hold.

```python
RED, BLACK = True, False


class RBNode:
    """Node for a Red-Black Tree; new nodes are RED by default."""

    def __init__(self, data, color=RED):
        self.data = data
        self.color = color
        self.parent = self.left = self.right = None

    def __repr__(self):
        return f"({'R' if self.color == RED else 'B'}){self.data}"


class RedBlackTree:
    """Self-balancing BST guaranteeing O(log n) search/insert."""

    def __init__(self):
        self.NIL = RBNode(data=None, color=BLACK)  # shared sentinel, always BLACK
        self.root = self.NIL

    def rotate_left(self, x):
        y = x.right
        x.right = y.left
        if y.left is not self.NIL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x is x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def rotate_right(self, y):
        x = y.left
        y.left = x.right
        if x.right is not self.NIL:
            x.right.parent = y
        x.parent = y.parent
        if y.parent is None:
            self.root = x
        elif y is y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x
        x.right = y
        y.parent = x

    def insert(self, data):
        """Standard BST insert (node starts RED), then fix red-red violations."""
        node = RBNode(data, color=RED)
        node.left = node.right = self.NIL
        parent, current = None, self.root
        while current is not self.NIL:
            parent = current
            if data < current.data:
                current = current.left
            elif data > current.data:
                current = current.right
            else:
                return  # no duplicates
        node.parent = parent
        if parent is None:
            self.root = node
        elif data < parent.data:
            parent.left = node
        else:
            parent.right = node
        self._fix_insert(node)

    def _fix_insert(self, node):
        while node.parent is not None and node.parent.color == RED:
            gp = node.parent.parent
            if node.parent is gp.left:
                uncle = gp.right
                if uncle.color == RED:  # Case 1: recolor, move up
                    node.parent.color = uncle.color = BLACK
                    gp.color = RED
                    node = gp
                else:
                    if node is node.parent.right:  # Case 2: inner -> outer
                        node = node.parent
                        self.rotate_left(node)
                    node.parent.color = BLACK  # Case 3: rotate + recolor
                    gp.color = RED
                    self.rotate_right(gp)
            else:  # mirror image
                uncle = gp.left
                if uncle.color == RED:
                    node.parent.color = uncle.color = BLACK
                    gp.color = RED
                    node = gp
                else:
                    if node is node.parent.left:
                        node = node.parent
                        self.rotate_right(node)
                    node.parent.color = BLACK
                    gp.color = RED
                    self.rotate_left(gp)
        self.root.color = BLACK

    def search(self, data):
        current = self.root
        while current is not self.NIL:
            if data == current.data:
                return current
            current = current.left if data < current.data else current.right
        return None

    def inorder(self):
        """Sorted list of all node data (in-order traversal)."""
        result = []

        def _walk(n):
            if n is self.NIL:
                return
            _walk(n.left)
            result.append(n.data)
            _walk(n.right)

        _walk(self.root)
        return result

    def black_height(self, node=None):
        """Black-node count from node to any NIL leaf (property 5 must hold)."""
        node = self.root if node is None else node
        if node is self.NIL:
            return 1
        left_bh = self.black_height(node.left)
        return left_bh + (1 if node.color == BLACK else 0)

    def verify_properties(self):
        """Check all 5 red-black invariants; returns (is_valid, message)."""
        if self.root.color != BLACK:
            return False, "Property 2 violated: root is not BLACK"

        def check(node):
            if node is self.NIL:
                return 1, True
            if node.color == RED:
                for child in (node.left, node.right):
                    if child is not self.NIL and child.color == RED:
                        return 0, False  # Property 4 violated
            lh, lok = check(node.left)
            rh, rok = check(node.right)
            if not (lok and rok) or lh != rh:
                return 0, False  # Property 5 violated
            return lh + (1 if node.color == BLACK else 0), True

        _, ok = check(self.root)
        return (ok, "All properties hold" if ok else "Red-black invariant violated")
```

## Insert Fix-Up Cases (parent is left child of grandparent)

| Case | Condition | Action |
|---|---|---|
| 1 | Uncle is RED | Recolor parent+uncle BLACK, grandparent RED, move up |
| 2 | Uncle BLACK, node is right child | Left-rotate parent (reduces to case 3) |
| 3 | Uncle BLACK, node is left child | Right-rotate grandparent, recolor |

Mirror cases apply when parent is right child.

## Genomic Application: Ordered Variant Store + Interval Overlaps

**Goal:** index SNP/variant positions (or genomic intervals) so range queries stay O(log n) even though a VCF's positions arrive already sorted by chromosome coordinate.
**Approach:** use `RedBlackTree.insert`/`inorder` for sorted position storage; for interval overlap, key each node by interval start and scan candidates near the query using two intervals `[a,b]`, `[c,d]` overlap iff `a <= d and c <= b`.

```python
def insert_variants_and_verify(positions: list[int]) -> tuple[bool, str]:
    """Insert chromosomal SNP positions into a RedBlackTree and verify balance."""
    tree = RedBlackTree()
    for pos in positions:
        tree.insert(pos)
    return tree.verify_properties()


class IntervalStore:
    """Ordered store of genomic intervals (start, end), keyed by start position."""

    def __init__(self):
        self.rbt = RedBlackTree()
        self._intervals: dict[int, list[tuple[int, int]]] = {}

    def add_interval(self, start: int, end: int) -> None:
        """Insert the interval, keyed by its start coordinate."""
        self.rbt.insert(start)
        self._intervals.setdefault(start, []).append((start, end))

    def find_overlaps(self, q_start: int, q_end: int) -> list[tuple[int, int]]:
        """Return all stored intervals overlapping [q_start, q_end]."""
        overlaps = []
        for start in self.rbt.inorder():  # sorted starts, O(n) scan; fine for teaching demo
            for iv_start, iv_end in self._intervals[start]:
                if iv_start <= q_end and q_start <= iv_end:
                    overlaps.append((iv_start, iv_end))
        return overlaps


if __name__ == "__main__":
    variant_positions = [10234, 20481, 30012, 45678, 51234, 62345, 71890]
    ok, msg = insert_variants_and_verify(variant_positions)
    assert ok, msg

    store = IntervalStore()
    for iv in [(1000, 2000), (1500, 3000), (4000, 5000), (7000, 8000)]:
        store.add_interval(*iv)
    assert store.find_overlaps(1800, 4800) == [(1000, 2000), (1500, 3000), (4000, 5000)]
    print("red-black tree self-check passed")
```

## Pitfalls

- NIL sentinel must be BLACK and shared — don't create new NIL nodes per operation.
- After insert fix-up, always force root to BLACK (a Case 1 recolor can turn it RED).
- `IntervalStore.find_overlaps` above scans all starts (O(n) per query) — it's a teaching-simplified interval store, not a true augmented interval tree; for real workloads use an interval tree that also tracks max-end per subtree to prune the search to O(log n + k).
- Deletion fix-up is significantly more complex (4 cases + mirrors) — omitted here but follows the same rotation/recolor pattern as insert.
- Duplicate keys are silently ignored by `insert` above; for multi-valued keys (e.g., multiple variants at the same position) store a list per key as `IntervalStore` does.

## See Also

- `algo-binary-search-trees` — the unbalanced BST this structure builds on
- `algo-avl-trees` — the stricter-balance alternative (shorter trees, more rotations)
- `algo-hash-tables-bloom` — O(1) average lookup when ordering isn't needed
- `bio-genome-intervals-interval-arithmetic` — production-grade interval overlap operations
