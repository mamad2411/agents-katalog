---
name: algo-avl-trees
description: "Implement a self-balancing AVL binary search tree in Python with rotation-based rebalancing (LL/RR/LR/RL) guaranteeing O(log n) insert/delete/search. Use when a user asks to build/implement an AVL tree, keep a sorted index balanced under insert/delete, explain balance factor or tree rotations, or avoid O(n) degeneration of a BST on sorted/near-sorted input (e.g. genomic positions arriving in coordinate order)."
tool_type: python
primary_tool: Python
---

# AVL Trees

## When to Use

- Implementing or explaining a self-balancing binary search tree from scratch (interview prep, coursework, "code up an AVL tree").
- Maintaining a sorted index that must stay O(log n) for search/insert/delete even when input arrives sorted or near-sorted (e.g. variant calls streaming in by chromosomal position, timestamps, incrementally arriving sequencing reads).
- Debugging a BST that "degenerates to a linked list" because inputs come pre-sorted.
- Comparing AVL vs. plain BST vs. red-black tree height/performance trade-offs.
- Walking through rotation cases (LL/RR/LR/RL) or balance-factor bookkeeping for a homework/exam question.

## Version Compatibility

Pure-Python, stdlib only — no version dependencies. Works unchanged on Python ≥ 3.8 (uses only built-in types; type hints use `Optional`/`List` from `typing`, available since 3.5+).

## Prerequisites

- Comfortable with recursive binary search tree insert/delete/search (see `algo-binary-search-trees`).
- No external packages required (`pip install` nothing).
- Helpful background: Big-O complexity analysis (`algo-complexity-analysis`).

## Key Invariant

Balance factor `bf(node) = height(left) - height(right)`. Every node must satisfy `|bf| <= 1`.
This bounds height at `h < 1.44 * log2(n+2)`, guaranteeing O(log n) operations even on adversarial (sorted) input — where a plain BST would degrade to O(n).

## Complexity

| Operation | Time | Space |
|-----------|------|-------|
| Search / Insert / Delete | O(log n) | O(log n) recursion stack |
| Single rotation | O(1) | O(1) |
| Get height / balance | O(1) | O(1) |

## Rotation Decision Table

| Node bf | Child bf | Case | Fix |
|---------|----------|------|-----|
| +2 | >= 0 | LL | Right rotation |
| +2 | < 0 | LR | Left rotation on left child, then right rotation |
| -2 | <= 0 | RR | Left rotation |
| -2 | > 0 | RL | Right rotation on right child, then left rotation |

Insertion needs at most **1** rotation (the tree is balanced from the point of insertion up). Deletion may need **O(log n)** rotations, one at every ancestor up to the root.

**Goal:** implement a fully working AVL tree supporting insert, delete, search, and sorted traversal, so a BST stays O(log n) even on sorted input.
**Approach:** store `height` on each node (not balance factor directly); after every recursive insert/delete, refresh the ancestor's height, compute its balance factor, and apply the matching rotation(s) from the table above.

```python
from typing import Optional, List, Any


class AVLNode:
    """A node in an AVL tree.

    Attributes:
        value: The data stored in the node.
        left: Reference to left child.
        right: Reference to right child.
        height: Height of the subtree rooted here (leaf = 1).
    """

    def __init__(self, value: Any) -> None:
        self.value = value
        self.left: Optional["AVLNode"] = None
        self.right: Optional["AVLNode"] = None
        self.height: int = 1


class AVLTree:
    """Self-balancing BST maintaining |balance factor| <= 1 at every node."""

    def __init__(self) -> None:
        self.root: Optional[AVLNode] = None

    # ---------- helpers ----------

    def get_height(self, node: Optional[AVLNode]) -> int:
        """Height of a node; an empty (None) node has height 0."""
        return node.height if node else 0

    def get_balance(self, node: Optional[AVLNode]) -> int:
        """Balance factor = height(left) - height(right)."""
        return self.get_height(node.left) - self.get_height(node.right) if node else 0

    def _update_height(self, node: AVLNode) -> None:
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

    # ---------- rotations ----------

    def rotate_right(self, z: AVLNode) -> AVLNode:
        """LL fix: rotate right around z, returning the new subtree root y."""
        y, T3 = z.left, z.left.right
        y.right, z.left = z, T3
        self._update_height(z)
        self._update_height(y)
        return y

    def rotate_left(self, z: AVLNode) -> AVLNode:
        """RR fix: rotate left around z, returning the new subtree root y."""
        y, T2 = z.right, z.right.left
        y.left, z.right = z, T2
        self._update_height(z)
        self._update_height(y)
        return y

    # ---------- insert ----------

    def insert(self, value: Any) -> None:
        self.root = self._insert(self.root, value)

    def _insert(self, node: Optional[AVLNode], value: Any) -> AVLNode:
        if node is None:
            return AVLNode(value)
        if value < node.value:
            node.left = self._insert(node.left, value)
        elif value > node.value:
            node.right = self._insert(node.right, value)
        else:
            return node  # no duplicates

        self._update_height(node)
        balance = self.get_balance(node)

        if balance > 1 and value < node.left.value:          # LL
            return self.rotate_right(node)
        if balance < -1 and value > node.right.value:        # RR
            return self.rotate_left(node)
        if balance > 1 and value > node.left.value:           # LR
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)
        if balance < -1 and value < node.right.value:         # RL
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)
        return node

    # ---------- delete ----------

    def delete(self, value: Any) -> None:
        self.root = self._delete(self.root, value)

    def _get_min_node(self, node: AVLNode) -> AVLNode:
        current = node
        while current.left is not None:
            current = current.left
        return current

    def _delete(self, node: Optional[AVLNode], value: Any) -> Optional[AVLNode]:
        if node is None:
            return None
        if value < node.value:
            node.left = self._delete(node.left, value)
        elif value > node.value:
            node.right = self._delete(node.right, value)
        else:
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            successor = self._get_min_node(node.right)  # inorder successor
            node.value = successor.value
            node.right = self._delete(node.right, successor.value)

        self._update_height(node)
        balance = self.get_balance(node)

        if balance > 1 and self.get_balance(node.left) >= 0:   # LL
            return self.rotate_right(node)
        if balance > 1 and self.get_balance(node.left) < 0:    # LR
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)
        if balance < -1 and self.get_balance(node.right) <= 0:  # RR
            return self.rotate_left(node)
        if balance < -1 and self.get_balance(node.right) > 0:   # RL
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)
        return node

    # ---------- search & traversal ----------

    def search(self, value: Any) -> Optional[AVLNode]:
        """Iterative O(log n) search, returning the matching node or None."""
        node = self.root
        while node is not None:
            if value == node.value:
                return node
            node = node.left if value < node.value else node.right
        return None

    def inorder(self) -> List[Any]:
        """Sorted traversal of all stored values."""
        result: List[Any] = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node: Optional[AVLNode], result: List[Any]) -> None:
        if node:
            self._inorder(node.left, result)
            result.append(node.value)
            self._inorder(node.right, result)
```

**Goal:** show *why* AVL matters — quantify how much a plain BST degrades on sorted input (e.g. variants sorted by genomic position) versus the AVL guarantee.
**Approach:** insert the same sorted sequence into a naive BST and an AVL tree and compare resulting heights.

```python
import math


class _PlainBSTNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def build_plain_bst(values):
    """Insert values into an unbalanced BST (no rotations) and return the root."""
    root = None
    for v in values:
        if root is None:
            root = _PlainBSTNode(v)
            continue
        node = root
        while True:
            if v < node.value:
                if node.left is None:
                    node.left = _PlainBSTNode(v)
                    break
                node = node.left
            else:
                if node.right is None:
                    node.right = _PlainBSTNode(v)
                    break
                node = node.right
    return root


def plain_bst_height(node) -> int:
    """Height of a plain (unbalanced) BST subtree; None has height 0."""
    if node is None:
        return 0
    return 1 + max(plain_bst_height(node.left), plain_bst_height(node.right))


def compare_heights(n: int) -> None:
    """Compare plain-BST vs AVL height for n sorted inserts (worst case for BST)."""
    sorted_vals = list(range(1, n + 1))  # e.g. genomic positions arriving in order
    bst_root = build_plain_bst(sorted_vals)
    avl = AVLTree()
    for v in sorted_vals:
        avl.insert(v)
    optimal = math.ceil(math.log2(n + 1))
    print(f"n={n}: plain BST height={plain_bst_height(bst_root)}, "
          f"AVL height={avl.get_height(avl.root)}, optimal={optimal}")


if __name__ == "__main__":
    for n in (100, 500, 1000):
        compare_heights(n)
    # BST height grows linearly with n; AVL height stays ~log2(n)
```

## Pitfalls

- **Update height before checking balance**: height must be refreshed on the way back up the recursion, before computing `bf`.
- **Deletion may cascade**: unlike insertion (at most one rotation), deletion can require rotations at every ancestor up to the root — don't `return` early after the first fix.
- **Child bf == 0 on deletion**: when a node has `bf=+2` and its left child has `bf=0`, that is still an LL case (right rotation), not LR. This differs from insertion, where `bf=0` never triggers a rotation on the child.
- **Height of None is 0, height of a leaf is 1**: mixing up these conventions causes off-by-one errors in balance-factor calculation.
- **Don't store balance factor directly**: store height and compute `bf` on the fly; storing `bf` directly requires extra bookkeeping during rotations and is easy to get wrong.
- **No duplicate handling built in**: the reference implementation silently ignores inserts of a value already present; decide explicitly whether you need multiset semantics (e.g. store a count per node) before reusing this code.

## See Also

- `algo-binary-search-trees` — the unbalanced BST this structure improves on.
- `algo-red-black-trees` — an alternative self-balancing BST with looser balance (fewer rotations on write-heavy workloads).
- `algo-suffix-trees` — a different balanced-tree use case (substring indexing) with unrelated rebalancing rules.
- `algo-complexity-analysis` — background for the O(log n) height bound derivation.
